"""MCP poslužitelj (službeni Python SDK, mcp 2.x: MCPServer, nekadašnji FastMCP).

Pokretanje:
    python -m mealmeter.server                    # stdio (Claude Desktop, lokalno)
    python -m mealmeter.server --http --port 8000 # streamable HTTP na /mcp

Javni podaci samo za čitanje, bez prijave. HTTP ima ograničenja upita u minuti po IP-u, po MCP sesiji i
ukupno (MM_RATE_IP, MM_RATE_SESSION, MM_RATE_GLOBAL; IP iz CF-Connecting-IP / X-Forwarded-For samo uz
TRUSTED_PROXY=1) i veličine zahtjeva; svaki odgovor alata je najviše MAX_RESPONSE_BYTES (dulji popisi se skraćuju, uz
truncated = true). Baza: MM_DB (npr. data/compact.duckdb), MEALMETER_DB ili data/mealmeter.duckdb.
"""

import argparse
import functools
import inspect
import json
import logging
import os
import threading
import time
from collections import Counter
from typing import Annotated, Any

import duckdb
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, TextContent, ToolAnnotations
from pydantic import Field

from mealmeter import basket, search, web
from mealmeter.normalize import date_hr, norm_text
from mealmeter.staples import load_staples
from mealmeter.web import MAX_REQUEST_BYTES, RATE_GLOBAL, RATE_LIMIT, RATE_SESSION  # noqa: F401

MAX_RESPONSE_BYTES = 20_000
PRICE_NOTE = ("Cijene su iz službenih cjenika trgovina (cijene.dev); u trgovini se mogu razlikovati, cjenik "
              "nije zaliha, a akcije se mijenjaju. / Prices come from the stores' official price lists "
              "(cijene.dev); in-store prices may differ, a price list is not stock, and promotions change.")
# Korak 6.3: navod izvora podataka. cijene.dev za dnevne arhive ne navodi licencu, nego uvjete korištenja
# (CC BY-NC-SA 4.0 je samo za enrichment/products.csv u repozitoriju cijene-api, koji Mealmeter ne koristi).
TERMS_URL = "https://cijene.dev/uvjeti-koristenja"
DATA_NOTE = (f"Podaci: cijene.dev (DobarKod), prema uvjetima korištenja ({TERMS_URL}). / "
             f"Data: cijene.dev (DobarKod), under its terms of use ({TERMS_URL}).")
PRICE_NOTE = f"{PRICE_NOTE} {DATA_NOTE}"

INSTRUCTIONS = """\
Mealmeter: cijene namirnica u hrvatskim trgovinama iz službenih dnevnih cjenika (cijene.dev).
Mealmeter: grocery prices in Croatian stores from the official daily price lists (cijene.dev).

Pravila / rules:
1. Kad korisnik traži samo recept, bez pitanja o cijeni ili kupnji: daj recept i na kraju jednu kratku rečenicu s
   ponudom da izračunaš koliko košta i gdje to može kupiti u svom gradu. Ne zovi plan_basket dok ne pristane.
   / Recipe only, no question about price or shopping: give the recipe and end with one short sentence offering to
   work out the cost and where to buy it in their city. Do not call plan_basket until they agree.
2. Kad pita koliko košta ili gdje kupiti, prije plan_basket u JEDNOJ poruci pitaj samo ono što još ne znaš: grad;
   što već ima doma (already_have); "U koju trgovinu ideš (može i adresa ili kvart), ili da usporedim sve u
   gradu?" (store; list_stores daje adrese); nadjev ili dodatke kad je relevantno. Ne pretpostavljaj što korisnik
   ima doma. Samo ako izričito traži brz odgovor bez pitanja, smiješ pretpostaviti, ali tada na kraju jasno navedi
   pretpostavke i ponudi ponovni izračun.
   / Asked the cost or where to buy: before plan_basket ask in ONE message only what is unknown: city, what they
   have at home, which store (address or neighbourhood) or all stores, extras. Never assume what is at home unless
   they explicitly want a quick answer; then list the assumptions and offer to recalculate.
3. Za svako novo jelo, promjenu broja osoba, sastojaka, grada ili trgovine ponovno pozovi plan_basket; nikad ne
   procjenjuj cijene niti ih prenosi iz ranijeg odgovora. Kad korisnik kaže stvarnu cijenu, pozovi ga s
   price_overrides. Nikad ne zbrajaj cijene sam. / Every new dish or change of servings, ingredients, city or
   store: call plan_basket again; never estimate, reuse or add up prices yourself (real price: price_overrides).
4. Ne dodaji sastojke koje korisnik nije potvrdio. Sastojak kojeg nema u list_staples šalji kao {"name", "amount",
   "unit", "free_text": true}. / Do not add unconfirmed ingredients; items outside list_staples use free_text.
5. Količine šalji u g, ml ili kom (convert_units za žlice i šalice); kod mahunarki je količina gotov proizvod.
   Bez količine (posipanje, začini) plan_basket uzima pretpostavku: navedi korisniku assumptions. Uvijek navedi
   u kojem je obliku količina iz recepta (suho, kuhano, smrznuto) i pitaj kad je to dvosmisleno.
   / Amounts in g, ml or kom (convert_units for spoons, cups); legumes: the ready amount. Tell the user the
   assumptions; state which form the recipe amount is in (dry, cooked, frozen) and ask when it is ambiguous.
6. Ne izmišljaj cijene ni proizvode: koristi samo ono što alati vrate. Sastojak iz unmatched nije uračunat: reci
   to i nikad mu ne procjenjuj cijenu (ni "otprilike X €"); odmah pokušaj find_products ili free_text (i drugi
   naziv) i ponudi candidates. Ne zaključuj da proizvoda nema nakon
   jedne pretrage. / Never invent prices or products. An unmatched ingredient is not counted: say so, never
   estimate its price; at once try find_products or free_text and offer candidates.
7. Trgovina poznata: plan_basket zovi sa store, a odgovor je točan popis za tu trgovinu. Ostale lance ne
   nabrajaj, osim jedne rečenice ako je neki drugi lanac u gradu jeftiniji za više od 2 € (cheaper_elsewhere).
   Ako joj nešto nedostaje, uz ukupnu cijenu navedi što. / Known store: call with store, answer with its exact
   list (and what it lacks); other chains only in one sentence if one is cheaper by more than 2 €.
8. Trgovina nije zadana ili korisnik kaže "svejedno": odgovor počinje s "Sve možeš kupiti u:" i popisom lanaca koji
   imaju sve sastojke (comparison, pa more_chains) s cijenom za kupiti, poredanih po cijeni; po lancu najviše 2
   SVOJE adrese i broj trgovina (lance iste cijene ne spajaj). Zatim jedna rečenica (price_spread): koji je
   najjeftiniji i kolika je razlika do najskupljeg u popisu; ako je razlika najviše 2 € (small), reci
   da su razlike male i da može ići gdje mu je najpraktičnije. Lanci kojima nešto nedostaje (incomplete) idu na
   kraj, s "nedostaje: ...", i uz cijenu takvog lanca to uvijek navedi, gdje god je spomeneš ("Lidl oko 26 €,
   nedostaje: pancetta"); nije najjeftiniji. Na kraju ponudi točan popis za trgovinu koju odabere.
   / No store or "any": start with "Sve možeš kupiti u:", complete chains by price to buy (max 2 own addresses,
   number of stores; never merge chains); one sentence on cheapest vs dearest (price_spread; small: go where it is
   convenient); incomplete chains last, always with what is missing next to their price; offer the exact list.
9. Stavke prikaži kao popis: proizvod, marka (brand) kad je poznata, veličina pakiranja (pack_size), cijena
   pakiranja (cost_pack), npr. "Brašno glatko T-550, Mlineta, 1 kg"; kad je brand null, marku izostavi i ne
   izmišljaj je. Tablicu koristi samo ako je korisnik traži. Usporedbu lanaca također kao popis, jedan lanac po retku.
   / Items and chains as lists (product, brand when known, pack size, pack price; brand null: omit it, never guess
   one; one chain per line); a table only if asked.
10. Piši prirodnim jezikom, bez internih naziva polja (stale_days, total_to_buy, total_used, match_quality,
   cheaper, delta_eur); utrošak (total_used) i from_stock_value su samo informativni. Datum piši kao "cijene iz
   cjenika od 20.10.2026." (date_hr); ako je cijena iz starijeg cjenika (stale_days > 0, i kod lanca u
   usporedbi), reci od kojeg datuma.
   / Natural language, no internal field names; date as "cijene iz cjenika od 20.10.2026.".
11. Alternativu zovi "jeftinijom" ili uštedom samo kad je cheaper = true (za istu potrebnu količinu; uz size_note
   je pakiranje drukčije i na blagajni može biti skuplje); cheaper = false nikad nije ušteda. Kad proizvoda nema
   na polici, ponudi alternatives iz iste trgovine. / An alternative is "cheaper" or a saving only when
   cheaper = true (same needed amount); cheaper = false never is.
12. Kod nesigurnog izbora pitaj: ask_user (oblik, cijene po obliku su za traženu količinu), needs_confirmation
   (free_text, kobasica bez dimljene), substitution (druga marka ili Grana Padano). Prenesi i warnings,
   assumed_form i slabije podudaranje (match_quality = 'weak'), običnim riječima; unit_uncertain: cijena je
   možda po komadu, neka je provjeri na polici. / When a choice is uncertain,
   ask: ask_user / ambiguity, needs_confirmation, substitution; pass on warnings, assumed_form, weaker matches.
13. Uz cijene uvijek dodaj: cijene su iz cjenika, u trgovini se mogu razlikovati, cjenik nije zaliha,
   a akcije se mijenjaju. / Always add: prices come from price lists, may differ in store, a price list is not
   stock, and promotions change.
"""

_local = threading.local()
_lock = threading.Lock()
_db_path: str | None = None
_shared_con: duckdb.DuckDBPyConnection | None = None
_fixed_con = False  # veza zadana izvana (testovi): bez praćenja datoteke
_db_key: tuple | None = None  # (inode, mtime_ns, veličina) glavne datoteke i datoteke cijena otvorene baze


def _file_key(path) -> tuple | None:
    try:
        st = os.stat(path)
    except OSError:  # datoteka upravo nestaje ili nije dostupna: ostaje otvorena veza
        return None
    return st.st_ino, st.st_mtime_ns, st.st_size


def _open(path) -> duckdb.DuckDBPyConnection:
    """Read-only baza kao ATTACH u novoj instanci u memoriji. duckdb.connect(putanja) bi vratio već otvorenu
    instancu iste putanje (predmemorija instanci po procesu), pa bi poslužitelj nakon zamjene datoteke i dalje
    čitao staru; ovako je svaka zamjena nova instanca. Kursori trebaju USE (vidi _con)."""
    # ograničenje memorije DuckDB-a (međuspremnik blokova); veći upiti se prelijevaju na disk (Korak 5P)
    # i broj dretvi (manje dretvi = manje alokatorskih arena po dretvi, manji RSS; upiti su mali)
    config = {"memory_limit": os.environ.get("MM_DUCKDB_MEMORY", "300MB"),
              "threads": int(os.environ.get("MM_DUCKDB_THREADS", "2"))}
    # serverless (Vercel): samo /tmp je zapisiv, pa privremene datoteke i "home" DuckDB-a idu tamo
    if tmp := os.environ.get("MM_DUCKDB_TEMP"):
        config.update(temp_directory=tmp, home_directory=tmp)
    con = duckdb.connect(":memory:", config=config)
    con.execute(f"ATTACH '{str(path).replace(chr(39), chr(39) * 2)}' AS {_DB_ALIAS} (READ_ONLY)")
    try:
        # sažeta baza u dvije datoteke (Korak 12): datoteka cijena i provjera oznake izgradnje
        search.attach_prices(con, path, _DB_ALIAS)
    except Exception:
        con.close()
        raise
    con.execute(f"USE {_DB_ALIAS}")
    return con


def _check_meta(con, path) -> dict | None:
    """Metapodaci uz sažetu bazu (web.read_meta) ako su iz iste izgradnje kao otvorena baza, inače None; kad se
    oznake ne slažu, metapodaci se odbacuju (web.reject_meta) i datum se dalje čita iz baze."""
    meta = web.read_meta(path)
    if meta is None:
        return None
    try:
        build_id = con.execute("SELECT build_id FROM clean.compact_build").fetchone()[0]
    except Exception:  # noqa: BLE001  (puna baza ili fixture: nema clean.compact_build)
        build_id = None
    if build_id != meta["build_id"]:
        log.warning("compact_meta: izgradnja %s, a baza %s; datum iz baze", meta["build_id"], build_id)
        web.reject_meta(meta["build_id"])
        return None
    return meta


_DB_ALIAS = "mm"


def _con() -> duckdb.DuckDBPyConnection:
    """Kursor po dretvi nad jednom read-only vezom (ili vezom zadanom za testove).

    Pri svakom pozivu provjerava datoteku baze: kad ju je update.py zamijenio (os.replace: novi inode, mtime
    ili veličina), otvara novu vezu bez restarta. Stara veza ostaje dok je drže kursori drugih dretvi
    (zamijenjena datoteka je i dalje čitljiva), a zatim je zatvara sakupljač smeća."""
    global _shared_con, _db_key
    with _lock:
        path = None if _fixed_con else (_db_path or search.DEFAULT_DB)  # MEALMETER_DB ili data/mealmeter.duckdb
        # glavna datoteka i datoteka cijena sažete baze (Korak 12): zamjena bilo koje otvara novu vezu
        key = (_file_key(path), _file_key(search.prices_part(path))) if path else None
        if _shared_con is None or (key is not None and key[0] is not None and key != _db_key):
            _shared_con = _open(path)
            _db_key = key
            # datum cjenika iz metapodataka iste izgradnje (Korak 18): bez max(date) nad view-om (~0,3 s CPU-a)
            if meta := _check_meta(_shared_con, path):
                _date_cache.update(owner=_shared_con, value={"date": meta["date"], "date_hr": meta["date_hr"]})
        shared, attached = _shared_con, not _fixed_con
    cur = getattr(_local, "cur", None)
    if cur is None or getattr(_local, "owner", None) is not shared:
        cur = shared.cursor()
        if attached:
            cur.execute(f"USE {_DB_ALIAS}")
        _local.cur, _local.owner = cur, shared
    return _local.cur


_date_cache: dict = {"owner": None, "value": None}


def _price_list_date(con=None) -> dict:
    """Datum cjenika (max date). Pamti se po vezi baze: mijenja se tek kad se datoteka zamijeni (nova veza), a
    na sažetoj bazi max(date) preko view-a clean.prices traje ~0,3 s (Korak 5P); uz metapodatke iste izgradnje
    (compact_meta.json) se ne računa (_con). Bez `con` (alati kojima baza ne treba: convert_units, list_staples)
    datum je iz metapodataka, bez otvaranja baze; bez njih se baza otvara."""
    if con is None:
        if meta := web.current_meta():
            return {"date": meta["date"], "date_hr": meta["date_hr"]}
        con = _con()
    owner = getattr(_local, "owner", None) if getattr(_local, "cur", None) is con else con
    if _date_cache["owner"] is not owner or owner is None:
        d = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
        _date_cache.update(owner=owner, value={"date": d.isoformat(), "date_hr": date_hr(d)} if d
                           else {"date": None, "date_hr": None})
    return dict(_date_cache["value"])


def _dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str, separators=(",", ":"))


def _size(obj) -> int:
    return len(_dumps(obj).encode("utf-8"))


def _fit(out: dict, lists: tuple[str, ...]) -> dict:
    """Skrati popise (redom iz `lists`, putanje s točkom) dok odgovor ne stane u MAX_RESPONSE_BYTES."""
    def get(path):
        cur = out
        for part in path.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        return cur

    for path in lists:
        while _size(out) > MAX_RESPONSE_BYTES:
            seq = get(path)
            if not isinstance(seq, list) or not seq:
                break
            seq.pop()
            out["truncated"] = True
    if _size(out) > MAX_RESPONSE_BYTES:
        raise ValueError("odgovor je prevelik; suzi upit / response too large; narrow the query")
    return out


def _error(e: Exception) -> dict:
    return {"error": str(e)}


# --- opisi parametara (JSON shema alata) ---
City = Annotated[str | None, Field(description="Grad, npr. 'Osijek' (uz nacionalne cijene) / city, e.g. 'Osijek'")]
Ingredient = Annotated[str | None, Field(description="Namirnica: ključ ili sinonim iz list_staples / staple key or synonym")]
Attributes = Annotated[dict[str, str] | None, Field(
    description='Atributi namirnice, npr. {"tip": "glatko"} (list_staples) / staple attributes')]

# --- alati --------------------------------------------------------------------------------------------

def find_products(
    query: Annotated[str | None, Field(description="Slobodan tekst naziva / free-text product name")] = None,
    city: City = None, ingredient: Ingredient = None, attributes: Attributes = None,
    include_weak: Annotated[bool, Field(description="Uključi slabija podudaranja / include weaker matches")] = False,
    limit: Annotated[int, Field(ge=1, le=30, description="Najviše grupa (1-30) / max groups")] = 10,
) -> dict:
    con = _con()
    try:
        rows = search.find_products(query, city=city, limit=max(1, min(limit, 30)), con=con,
                                    ingredient=ingredient, attributes=attributes, include_weak=include_weak)
    except ValueError as e:
        return _error(e)
    out = {**_price_list_date(con), "stale_days": max((r.get("stale_days") or 0 for r in rows), default=0),
           "results": rows, "note": PRICE_NOTE}
    return _fit(out, ("results",))


def get_prices(
    product_id: Annotated[str, Field(description='EAN, "lanac:product_id" ili id klase ("jaja:m") iz find_products')],
    city: City = None,
) -> dict:
    con = _con()
    try:
        rows = search.get_prices(product_id, city=city, limit=50, con=con)
    except ValueError as e:
        return _error(e)
    out = {**_price_list_date(con), "product_id": product_id, "stores": rows, "note": PRICE_NOTE}
    return _fit(out, ("stores",))


def plan_basket(
    ingredients: Annotated[list[dict[str, Any]], Field(
        description='[{"name": "brašno glatko", "amount": 250, "unit": "g"|"ml"|"kom", "form"?: "...", '
                    '"attributes"?: {...}, "free_text"?: true}]; mjere pretvori u g/ml/kom ili convert_units; '
                    'free_text: sastojak izvan list_staples, traži se po nazivu / ingredient outside list_staples, '
                    'searched by name')],
    city: Annotated[str, Field(description="Grad / city, npr. 'Osijek'")],
    store: Annotated[dict[str, str] | None, Field(
        description='Jedna trgovina / one store: {"chain": "konzum", "address_contains": "Starčevića"} (list_stores)')] = None,
    already_have: Annotated[list[str] | None, Field(
        description='Što korisnik već ima / what the user already has: ["sol", "papar"]')] = None,
    price_overrides: Annotated[list[dict[str, Any]] | None, Field(
        description='Stvarne cijene pakiranja / real pack prices: [{"name": "brašno", "cost_pack": 1.2}]')] = None,
    alternatives: Annotated[bool, Field(
        description="Do 2 jeftinije alternative po stavci (cheaper = true) i iznimno jedna iste cijene i bolje "
                    "kvalitete (cheaper = false), s delta_eur / up to 2 cheaper alternatives per item (cheaper = true) "
                    "and at most one of the same price and better quality (cheaper = false), with delta_eur")] = True,
    detail: Annotated[bool, Field(
        description="Puni odgovor (sve trgovine i sva polja) umjesto sažetog / full response instead of the compact "
                    "one")] = False,
) -> dict:
    con = _con()
    try:
        res = basket.plan_basket(ingredients, city, con=con, max_stores=3, already_have=already_have,
                                 store=store, alternatives=alternatives, price_overrides=price_overrides)
    except ValueError as e:
        return _error(e)
    res.setdefault("date", _price_list_date(con)["date"])
    res["note"] = PRICE_NOTE  # alternative nosi samo best_store (basket.plan_basket)
    if detail:
        return _fit(res, ("stores", "best_store.items"))
    return _fit(compact_basket(res), ("incomplete", "comparison", "best_store.items"))


_ITEM_KEYS = ("ingredient", "staple", "name", "brand", "pack_size", "n_packs", "cost_pack", "cost_used")
_ITEM_OPTIONAL = ("have", "user_provided", "computed_cost_pack", "substitution", "needs_confirmation", "candidates")
_ALT_KEYS = ("name", "pack_size", "cost_pack", "cost_used", "delta_eur", "cheaper", "size_note", "note", "brand",
             "other_store", "chain", "address")


# napomene stavke koje ostaju u sažetom odgovoru (Korak 17: nesigurna jedinica, cijena za komad)
_NOTE_PREFIXES = ("izvan zadanog", "rinfuza", "nacionalna", "na vagu", "jedinica nesigurna", "cijena za komad")


def _compact_item(it: dict) -> dict:
    out = {k: it[k] for k in _ITEM_KEYS}
    out.update({k: it[k] for k in _ITEM_OPTIONAL if it.get(k)})
    if it.get("match_quality") in ("weak", "free_text"):
        out["match_quality"] = it["match_quality"]
    if it.get("flags"):
        out["flags"] = it["flags"]
    if it.get("stale_days"):
        out["date_hr"], out["stale_days"] = it["date_hr"], it["stale_days"]
    notes = [n for n in it.get("notes") or [] if n.startswith(_NOTE_PREFIXES)]
    if notes:
        out["notes"] = notes
    if "alternatives" in it:
        # brand je uvijek tu (null kad marka nije poznata, Korak 13); ostala polja samo kad imaju vrijednost
        out["alternatives"] = [{k: a.get(k) for k in _ALT_KEYS if a.get(k) is not None or k == "brand"}
                               for a in it["alternatives"]]
    return out


def compact_basket(res: dict) -> dict:
    """Sažet odgovor plan_basket (zadano): najbolja trgovina (najmanji total_to_buy) sa stavkama i usporedba
    lanaca (comparison: jedan redak po lancu, najviše 6; incomplete: lanci bez dovoljno sastojaka). Puni
    odgovor daje detail=true."""
    best = res.get("best_store")
    out = {k: res[k] for k in ("city", "date", "date_hr", "summary_hr") if k in res}
    if best:
        out["best_store"] = {
            **{k: best[k] for k in ("chain", "address", "n_stores", "addresses", "total_to_buy", "total_used",
                                    "from_stock_value", "n_matched", "n_ingredients", "missing", "date_hr",
                                    "stale_days") if k in best},
            **({"note": best["note"]} if best.get("note") else {}),
            "items": [_compact_item(it) for it in best["items"]]}
    else:
        out["best_store"] = None
    # usporedba lanaca (basket.compare_chains): najviše 6 potpunih lanaca, ostali potpuni u more_chains, nepotpuni
    # u incomplete
    out["comparison"] = res.get("comparison", [])
    for k in ("incomplete", "more_chains", "price_spread", "cheaper_elsewhere", "assumptions", "ask_user", "unmatched", "warnings",
              "store_suggestions", "city_suggestions", "already_have"):
        if res.get(k):
            out[k] = res[k]
    out["note"] = res["note"]
    return out


def list_stores(
    city: Annotated[str, Field(description="Grad / city")],
    chain: Annotated[str | None, Field(description="Lanac, npr. 'konzum', 'lidl' / chain")] = None,
) -> dict:
    con = _con()
    resolved = search.resolve_city(city, con=con)
    if not resolved:
        return {**_price_list_date(con), "city": city, "stores": [],
                "warnings": [f"nepoznat grad '{city}'"], "city_suggestions": basket.city_suggestions(con, city)}
    city_sql, params = search._city_filter(city)
    chain_sql = "AND s.chain = ?" if chain else ""
    rows = con.execute(f"""
        SELECT s.chain, s.store_id, s.address, s.city, s.scope, s.store_type,
               max(c.date) AS date, min(c.stale_days) AS stale_days, count(*) AS n_prices
        FROM clean.stores s JOIN clean.prices c USING (chain, store_id)
        JOIN clean.products p USING (chain, product_id)
        WHERE {city_sql} {chain_sql} AND p.{search.STORE_PRODUCTS_SQL}
        GROUP BY ALL ORDER BY s.scope DESC, s.chain, s.address""",
                       params + ([chain.strip().lower()] if chain else [])).fetchall()
    stores = [{"chain": ch, "store_id": sid, "address": addr, "city": c, "scope": scope, "store_type": st,
               "date": d.isoformat(), "date_hr": date_hr(d), "stale_days": stale, "n_prices": n}
              for ch, sid, addr, c, scope, st, d, stale, n in rows]
    return _fit({**_price_list_date(con), "city": resolved, "stores": stores}, ("stores",))


def convert_units(
    amount: Annotated[float, Field(description="Količina / amount")],
    unit: Annotated[str, Field(description="Mjera: žlica, žličica, šalica, prstohvat, kom, češanj, g, ml... / unit")],
    staple: Annotated[str, Field(description="Namirnica (ključ ili sinonim) / staple")],
) -> dict:
    try:
        st, _ = basket.resolve_name(staple)
        value, base, notes = basket.to_base(amount, unit, st)
    except (ValueError, basket.IngredientError) as e:
        return {**_price_list_date(), **_error(e)}
    return {**_price_list_date(), "staple": st.key, "amount": round(value, 2), "unit": base, "notes": notes}


def list_staples() -> dict:
    staples = [{"key": s.key, "name": s.name, "unit": s.unit, "synonyms": list(s.synonyms[:6]),
                "attributes": {a: list(v) for a, v in s.attributes.items()}}
               for s in load_staples().values()]
    return _fit({**_price_list_date(), "staples": staples}, ("staples",))


DESCRIPTIONS = {
    "find_products": """\
Traži proizvode po nazivu ili po namirnici; vraća grupe (isti EAN u više lanaca) s rasponom cijena.
Searches products by name or by staple ingredient; returns groups (same EAN across chains) with price ranges.
Kada / when: korisnik pita što postoji i koliko košta / the user asks what exists and what it costs.
Parametri / parameters: query (slobodan tekst / free text), city (grad / city), ingredient (ključ ili
sinonim iz list_staples / staple key or synonym), attributes (npr. {"tip": "glatko"}), include_weak
(slabija podudaranja / weaker matches, zadano false), limit (1-30).
Vraća / returns: results (id, name, brand: marka ili null / brand or null, pack, raspon cijena / price range).
Primjer / example: {"ingredient": "brašno", "attributes": {"tip": "glatko"}, "city": "Osijek"}""",
    "get_prices": """\
Cijene jednog proizvoda po trgovinama, od najjeftinije. / Prices of one product per store, cheapest first.
Kada / when: nakon find_products, za detalje / after find_products, for details.
Parametri / parameters: product_id = EAN, "lanac:product_id" ili id klase (npr. "jaja:m"); city.
Vraća / returns: stores (lanac, adresa, name, brand: marka ili null / brand or null, price_eff).
Primjer / example: {"product_id": "3850104223624", "city": "Osijek"}""",
    "plan_basket": """\
Košarica za recept: cijena svih sastojaka po trgovini u gradu i najbolja trgovina.
Basket for a recipe: cost of all ingredients per store in the city, and the best store.
Kada / when: korisnik želi znati koliko košta jelo ili popis / the user wants the cost of a dish or list.
Samo recept: ne zovi dok korisnik ne pristane. Prije poziva u jednoj poruci pitaj samo što nedostaje: grad,
already_have, store ili usporedba svih, nadjev ili dodaci. Svaka promjena: novi poziv. / Recipe only: do not call
until the user agrees. Before calling, ask in one message only for what is missing (city, already_have, store or
all, extras). Any change: call again.
Parametri / parameters: ingredients [{"name", "amount", "unit" (g|ml|kom), "form"?, "attributes"?,
"free_text"?}] (free_text: true za sastojak izvan list_staples, npr. "nutella" / for an ingredient outside
list_staples), city, store? {"chain", "address_contains"} (jedna trgovina; nacionalne cijene lanca vrijede /
one store; the chain's national prices still apply), already_have? ["sol", "papar"], price_overrides?
[{"name", "cost_pack"}] (stvarna cijena pakiranja, samo za ovaj poziv / real pack price, this call only),
alternatives (zadano true: do 2 druga proizvoda po stavci s delta_eur i cheaper / up to 2 other products
per item with delta_eur and cheaper).
best_store: najviše sastojaka, pa najmanji total_to_buy; total_used i from_stock_value (already_have) su
informativni. / best_store: most ingredients, then lowest total_to_buy; total_used, from_stock_value informative.
Vraća / returns (sažeto / compact): summary_hr (zbroj za best_store / totals of best_store), best_store (items s brand
(marka ili null / brand or null), pack_size, cost_pack, cost_used, alternatives; trgovine istog lanca s istim proizvodima spojene: n_stores, addresses),
comparison (lanci sa svim sastojcima, po lancu jedan redak, do 6 / chains with every ingredient, one row per
chain, up to 6: chain, addresses, n_stores_city, total_to_buy, total_used), more_chains (ostali potpuni lanci /
further complete chains), price_spread (najjeftiniji i najskuplji potpuni lanac, difference_eur, small: <= 2 € / cheapest
and dearest complete chain), incomplete (lanci kojima nešto nedostaje: missing / chains missing ingredients),
cheaper_elsewhere (uz store: drugi lanac u gradu jeftiniji za > 2 € / with store: another chain in the
city cheaper by > 2 €), assumptions (pretpostavljene količine i vrijednosti / assumed amounts and values), ask_user
(oblik ili atribut, npr. celer: stabljika ili korijen / form or attribute), warnings, unmatched (nije uračunato, bez
cijene; s prijedlozima / not counted, no price; with suggestions), date_hr. detail=true: sve trgovine i sva polja /
all stores and fields.
Primjer / example: {"ingredients": [{"name": "brašno glatko", "amount": 250, "unit": "g"},
{"name": "mlijeko", "amount": 500, "unit": "ml"}, {"name": "jaja", "amount": 3, "unit": "kom"},
{"name": "nutella", "amount": 300, "unit": "g", "free_text": true}], "city": "Osijek", "already_have": ["sol"]}""",
    "list_stores": """\
Trgovine u gradu s adresama i datumom cjenika. / Stores in a city with addresses and price-list date.
Kada / when: korisnik ide u određenu trgovinu (za store u plan_basket) / the user shops at a specific store.
Parametri / parameters: city, chain? (npr. "konzum").
Primjer / example: {"city": "Osijek", "chain": "konzum"}""",
    "convert_units": """\
Pretvara kuhinjsku mjeru ili komade u g/ml za namirnicu (procjena). / Converts a kitchen measure or
pieces to g/ml for a staple (estimate).
Kada / when: recept ima žlice, šalice, prstohvat, češnjeve... / the recipe uses spoons, cups, cloves...
Parametri / parameters: amount, unit (žlica, šalica, prstohvat, kom, češanj...), staple.
Primjer / example: {"amount": 2, "unit": "žlica", "staple": "šećer"}""",
    "list_staples": """\
Popis podržanih namirnica s jedinicom, sinonimima i atributima. / List of supported staples with unit,
synonyms and attributes.
Kada / when: provjera je li sastojak podržan i koji atributi postoje / to check support and attributes.
Primjer / example: {}""",
}

TOOLS = (find_products, get_prices, plan_basket, list_stores, convert_units, list_staples)


log = logging.getLogger("mealmeter")
# broj poziva po alatu i statusu ("ok" | "error" | "exception"), od pokretanja procesa
TOOL_CALLS: Counter = Counter()


def _as_result(fn):
    """Alat vraća CallToolResult sa sažetim JSON-om (bez uvlačenja i bez dvostrukog structured_content),
    tako da je ograničenje MAX_RESPONSE_BYTES stvarna veličina odgovora; {"error": ...} je isError.
    Zapisuje samo naziv alata, status, trajanje i veličinu odgovora, nikad argumente (sadržaj upita)."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> CallToolResult:
        start, cpu0, status = time.perf_counter(), time.process_time(), "exception"
        try:
            out = fn(*args, **kwargs)
            status = "error" if "error" in out else "ok"
            text = _dumps(out)
            return CallToolResult(content=[TextContent(type="text", text=text)], is_error="error" in out)
        finally:
            TOOL_CALLS[(fn.__name__, status)] += 1
            log.info("tool=%s status=%s ms=%d cpu_ms=%d calls=%d", fn.__name__, status,
                     (time.perf_counter() - start) * 1000, (time.process_time() - cpu0) * 1000,
                     sum(n for (t, _), n in TOOL_CALLS.items() if t == fn.__name__))

    wrapper.__signature__ = inspect.signature(fn).replace(return_annotation=CallToolResult)
    wrapper.__annotations__ = {**fn.__annotations__, "return": CallToolResult}
    return wrapper


def create_server(con: duckdb.DuckDBPyConnection | None = None, db_path: str | None = None) -> MCPServer:
    """Poslužitelj s alatima. `con` (testovi) ili `db_path` zamjenjuju zadanu bazu."""
    global _shared_con, _db_path, _fixed_con
    if con is not None:
        _shared_con, _fixed_con = con, True
    elif db_path:
        _db_path, _shared_con, _fixed_con = db_path, None, False
    server = MCPServer(name="mealmeter", title="Mealmeter", instructions=INSTRUCTIONS,
                       description="Cijene namirnica u hrvatskim trgovinama / grocery prices in Croatian stores")
    ro = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
    for fn in TOOLS:
        server.tool(name=fn.__name__, description=DESCRIPTIONS[fn.__name__], annotations=ro)(_as_result(fn))
    return server


# HTTP omotači, /healthz i / su u laganom modulu web (Korak 18: Vercel ih koristi bez učitavanja SDK-a)
from mealmeter.web import (HEALTH_MAX_AGE_HOURS, HOME_HTML, LOCAL_HOSTS, LOCAL_ORIGINS,  # noqa: E402,F401
                           HostGuard, McpPostOnly, RateLimit, RequestLog, _env_int, _match, _split_env, _text,
                           anon_ip, health, home, version)


def sdk_app(server: MCPServer, host: str = "127.0.0.1"):
    """Starlette aplikacija SDK-a: MCP na /mcp (streamable HTTP, bez sesija, JSON odgovori), GET /healthz i /, JSON
    404/405. SDK-ova provjera Hosta je ugašena jer je zamjenjuje HostGuard (http_app, web.VercelApp)."""
    from starlette.requests import Request
    from starlette.responses import HTMLResponse, JSONResponse
    from starlette.routing import Route

    app = server.streamable_http_app(
        stateless_http=True, json_response=True, max_request_body_size=MAX_REQUEST_BYTES, host=host,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))

    async def healthz(request: Request):
        status, body = health()
        return JSONResponse(body, status_code=status, headers={"cache-control": "no-store"})

    async def index(request: Request):
        return HTMLResponse(home(request.headers.get("host"), request.headers.get("x-forwarded-proto")))

    app.router.routes[:0] = [Route("/healthz", healthz, methods=["GET"]), Route("/", index, methods=["GET"])]

    async def http_error(request: Request, exc):
        # nepoznata putanja (i /.well-known/oauth-*) je JSON 404: klijent (npr. Claude konektor) tako zna da
        # poslužitelj nema prijave (OAuth), umjesto da dobije HTML ili tekst
        status = getattr(exc, "status_code", 500)
        text = {404: "not found", 405: "method not allowed"}.get(status, getattr(exc, "detail", "error"))
        return JSONResponse({"error": text, "path": request.url.path}, status_code=status,
                            headers=getattr(exc, "headers", None))

    from starlette.exceptions import HTTPException as StarletteHTTPException

    app.add_exception_handler(StarletteHTTPException, http_error)
    return app


def http_app(server: MCPServer, host: str = "127.0.0.1", allowed_hosts: list[str] | None = None,
             allowed_origins: list[str] | None = None):
    """ASGI aplikacija za lokalni HTTP način: sdk_app iza RequestLog, HostGuard (Host/Origin), RateLimit i
    McpPostOnly. Vercel koristi web.VercelApp (isti omotači, SDK tek kad zatreba)."""
    return RequestLog(HostGuard(RateLimit(McpPostOnly(sdk_app(server, host))), allowed_hosts, allowed_origins))


# --- snimka jeftinih MCP odgovora za web.fast_reply (Korak 18) -------------------------------------------------

async def _post(app, body: dict, headers: dict | None = None) -> tuple[int, bytes]:
    data = json.dumps(body).encode()
    sent, out = False, {"status": None, "body": b""}

    async def receive():
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": data, "more_body": False}
        return {"type": "http.disconnect"}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]
        elif msg["type"] == "http.response.body":
            out["body"] += msg.get("body", b"")
    hdrs = {"host": "localhost", "content-type": "application/json", "accept": "application/json, text/event-stream",
            **(headers or {})}
    await app({"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": "POST", "path": "/mcp",
               "raw_path": b"/mcp", "query_string": b"", "root_path": "", "scheme": "http",
               "headers": [(k.encode(), v.encode()) for k, v in hdrs.items()], "client": ("127.0.0.1", 1),
               "server": ("localhost", 80)}, receive, send)
    return out["status"], out["body"]


def static_snapshot() -> dict:
    """Odgovori SDK-a (ovog poslužitelja) na initialize i tools/list, za web.fast_reply: rezultat initialize jednak je
    za sve verzije handshakea osim protocolVersion (tražena verzija, inače fallback_version)."""
    import asyncio

    from mcp_types.version import HANDSHAKE_PROTOCOL_VERSIONS

    def init(v):
        return {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": v, "capabilities": {}, "clientInfo": {"name": "snapshot", "version": "1"}}}

    async def go():
        app = sdk_app(create_server())  # bez con i db_path: zadana baza se ne mijenja ni ne otvara
        async with app.router.lifespan_context(app):
            inits = {v: await _post(app, init(v)) for v in (*HANDSHAKE_PROTOCOL_VERSIONS, "0000-00-00")}
            tools = await _post(app, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        return inits, tools
    inits, tools = asyncio.run(go())
    results = {}
    for v, (status, body) in inits.items():
        assert status == 200, (v, status, body[:200])
        results[v] = json.loads(body)["result"]
    base = dict(results[HANDSHAKE_PROTOCOL_VERSIONS[0]], protocolVersion=None)
    for v in HANDSHAKE_PROTOCOL_VERSIONS:
        assert results[v]["protocolVersion"] == v and dict(results[v], protocolVersion=None) == base, v
    assert tools[0] == 200
    return {"_comment": "Snimka odgovora MCP SDK-a za web.fast_reply; python -m mealmeter.server --write-static",
            "handshake_versions": list(HANDSHAKE_PROTOCOL_VERSIONS),
            "fallback_version": results["0000-00-00"]["protocolVersion"],
            "initialize": base, "tools_list": json.loads(tools[1])["result"]}


def write_static() -> None:
    web.STATIC_PATH.write_text(json.dumps(static_snapshot(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Mealmeter MCP poslužitelj")
    ap.add_argument("--http", action="store_true", help="streamable HTTP umjesto stdio")
    ap.add_argument("--host", default="127.0.0.1", help="adresa slušanja (zadano 127.0.0.1; tunel spaja lokalno)")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", default=None, help="putanja baze (inače MM_DB, MEALMETER_DB ili data/mealmeter.duckdb)")
    ap.add_argument("--write-static", action="store_true",
                    help="zapiši snimku odgovora initialize i tools/list (src/mealmeter/mcp_static.json) i izađi")
    args = ap.parse_args(argv)
    if args.write_static:
        write_static()
        print(f"zapisano: {web.STATIC_PATH}")
        return
    server = create_server(db_path=args.db)
    if not args.http:
        server.run("stdio")
        return
    import uvicorn

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    # access_log=False: uvicornov access log zapisuje punu IP adresu i query string; zamjenjuje ga RequestLog
    uvicorn.run(http_app(server, args.host), host=args.host, port=args.port, log_level="info", access_log=False)


if __name__ == "__main__":
    main()
