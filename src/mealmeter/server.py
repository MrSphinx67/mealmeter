"""MCP poslužitelj (službeni Python SDK, mcp 2.x: MCPServer, nekadašnji FastMCP).

Pokretanje:
    python -m mealmeter.server                    # stdio (Claude Desktop, lokalno)
    python -m mealmeter.server --http --port 8000 # streamable HTTP na /mcp

Javni podaci samo za čitanje, bez prijave. HTTP ima ograničenja upita u minuti po IP-u, po MCP sesiji i
ukupno (MM_RATE_IP, MM_RATE_SESSION, MM_RATE_GLOBAL; IP iz CF-Connecting-IP / X-Forwarded-For samo uz
TRUSTED_PROXY=1) i veličine zahtjeva; svaki odgovor alata je najviše MAX_RESPONSE_BYTES (dulji popisi se skraćuju, uz
truncated = true). Baza: MEALMETER_DB ili data/mealmeter.duckdb.
"""

import argparse
import functools
import inspect
import json
import logging
import os
import re
import threading
import time
from collections import Counter, defaultdict, deque
from typing import Annotated, Any

import duckdb
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, TextContent, ToolAnnotations
from pydantic import Field

from mealmeter import basket, search
from mealmeter.normalize import date_hr, norm_text
from mealmeter.staples import load_staples

MAX_RESPONSE_BYTES = 20_000
RATE_LIMIT = 60  # upita po IP-u u minuti (HTTP), MM_RATE_IP
RATE_SESSION = 30  # upita po MCP sesiji (Mcp-Session-Id) u minuti, MM_RATE_SESSION
RATE_GLOBAL = 1000  # upita ukupno u minuti, MM_RATE_GLOBAL
MAX_REQUEST_BYTES = 64_000
PRICE_NOTE = ("Cijene su iz službenih cjenika trgovina (cijene.dev); u trgovini se mogu razlikovati, cjenik "
              "nije zaliha, a akcije se mijenjaju. / Prices come from the stores' official price lists "
              "(cijene.dev); in-store prices may differ, a price list is not stock, and promotions change.")

INSTRUCTIONS = """\
Mealmeter: cijene namirnica u hrvatskim trgovinama iz službenih dnevnih cjenika (cijene.dev).
Mealmeter: grocery prices in Croatian stores from the official daily price lists (cijene.dev).

Pravila / rules:
1. Prije plan_basket u JEDNOJ poruci pitaj samo ono što korisnik još nije rekao: grad; što već ima kod
   kuće (already_have); ide li u određenu trgovinu (store; list_stores daje adrese) ili da se usporede sve
   trgovine; želi li nadjev ili dodatke. Ne pitaj ponovno ono što je već rekao.
   / Before plan_basket ask, in ONE message, only what the user has not said yet: city; what they already
   have at home (already_have); a particular store (store; see list_stores) or a comparison of all stores;
   whether they want a filling or extras. Do not ask again for what they already told you.
2. Ne dodaji sastojke koje korisnik nije potvrdio. Svaki dodatak (nadjev, prilog) ide kroz plan_basket;
   sastojak kojeg nema u list_staples šalji kao {"name", "amount", "unit", "free_text": true}. Nikad ne
   zbrajaj cijene sam. / Do not add ingredients the user has not confirmed. Every extra goes through
   plan_basket; an ingredient missing from list_staples goes as {"name", "amount", "unit", "free_text": true}.
   Never add up prices yourself.
3. Količine šalji u g, ml ili kom. Žlice, šalice, prstohvat, češnjeve i glavice pretvori sam ili pozovi
   convert_units. / Send amounts in g, ml or kom (pieces); convert cups, spoons, cloves etc. yourself or
   call convert_units.
4. Ne izmišljaj cijene ni proizvode: koristi samo ono što alati vrate. / Never invent prices or products;
   use only what the tools return.
5. Odgovor počni sa summary_hr. Piši prirodnim jezikom, bez internih naziva polja (stale_days,
   total_to_buy, total_used, match_quality, cheaper, delta_eur). Datum piši kao "cijene iz cjenika od
   20.10.2026." (date_hr); ako je cijena prenesena iz starijeg cjenika (stale_days > 0), reci od kojeg je
   datuma. / Start the answer with summary_hr. Write natural language without internal field names; give the
   date as "cijene iz cjenika od 20.10.2026." (date_hr) and say when a price comes from an older list.
6. Tablica stavki ima stupce: proizvod, veličina pakiranja (pack_size), cijena pakiranja (cost_pack),
   utrošak (cost_used). / The item table has the columns product, pack size, pack price, cost of the amount
   used.
7. Alternativu zovi "jeftinijom" samo kad je cheaper = true; inače je "druga mogućnost" uz razliku u cijeni.
   Kad proizvoda nema na polici, ponudi alternatives iz iste trgovine. / Call an alternative "cheaper" only
   when cheaper = true, otherwise "another option" with the price difference. If a product is not on the
   shelf, offer the item's alternatives from the same store.
8. Prenesi warnings, ask_user (pitaj o obliku, zadaj form i ponovi; cijene po obliku su za traženu količinu),
   assumed_form, slabije podudaranje
   (match_quality = 'weak') i stavke nađene slobodnom pretragom (match_quality = 'free_text': neka korisnik
   provjeri proizvod), sve običnim riječima. / Pass on warnings, ask_user / ambiguity (ask, then retry with form),
   assumed_form, weaker matches and free-text matches (ask the user to check the product), in plain words.
9. Kad korisnik kaže stvarnu cijenu, ponovno pozovi plan_basket s price_overrides; ne zbrajaj sam.
   / When the user reports a real price, call plan_basket again with price_overrides; do not add up
   totals yourself.
10. Uz cijene uvijek dodaj: cijene su iz cjenika, u trgovini se mogu razlikovati, cjenik nije zaliha,
   a akcije se mijenjaju. / With prices always add that they come from price lists, may differ in store, a price list
   is not stock, and promotions change.
"""

_local = threading.local()
_lock = threading.Lock()
_db_path: str | None = None
_shared_con: duckdb.DuckDBPyConnection | None = None
_fixed_con = False  # veza zadana izvana (testovi): bez praćenja datoteke
_db_key: tuple | None = None  # (inode, mtime_ns, veličina) otvorene datoteke baze


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
    con = duckdb.connect(":memory:")
    con.execute(f"ATTACH '{str(path).replace(chr(39), chr(39) * 2)}' AS {_DB_ALIAS} (READ_ONLY)")
    con.execute(f"USE {_DB_ALIAS}")
    return con


_DB_ALIAS = "mm"


def _con() -> duckdb.DuckDBPyConnection:
    """Kursor po dretvi nad jednom read-only vezom (ili vezom zadanom za testove).

    Pri svakom pozivu provjerava datoteku baze: kad ju je update.py zamijenio (os.replace: novi inode, mtime
    ili veličina), otvara novu vezu bez restarta. Stara veza ostaje dok je drže kursori drugih dretvi
    (zamijenjena datoteka je i dalje čitljiva), a zatim je zatvara sakupljač smeća."""
    global _shared_con, _db_key
    with _lock:
        path = None if _fixed_con else (_db_path or search.DEFAULT_DB)  # MEALMETER_DB ili data/mealmeter.duckdb
        key = _file_key(path) if path else None
        if _shared_con is None or (key is not None and key != _db_key):
            _shared_con = _open(path)
            _db_key = key
        shared, attached = _shared_con, not _fixed_con
    cur = getattr(_local, "cur", None)
    if cur is None or getattr(_local, "owner", None) is not shared:
        cur = shared.cursor()
        if attached:
            cur.execute(f"USE {_DB_ALIAS}")
        _local.cur, _local.owner = cur, shared
    return _local.cur


def _price_list_date(con) -> dict:
    d = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    return {"date": d.isoformat(), "date_hr": date_hr(d)} if d else {"date": None, "date_hr": None}


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
        description="Do 2 jeftinije alternative po stavci, s delta_eur i cheaper / up to 2 cheaper alternatives per "
                    "item, with delta_eur and cheaper")] = True,
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


_ITEM_KEYS = ("ingredient", "staple", "name", "pack_size", "n_packs", "cost_pack", "cost_used")
_ITEM_OPTIONAL = ("have", "user_provided", "computed_cost_pack", "substitution", "needs_confirmation", "candidates")
_ALT_KEYS = ("name", "pack_size", "cost_pack", "cost_used", "delta_eur", "cheaper", "size_note", "note", "brand",
             "other_store", "chain", "address")


def _compact_item(it: dict) -> dict:
    out = {k: it[k] for k in _ITEM_KEYS}
    out.update({k: it[k] for k in _ITEM_OPTIONAL if it.get(k)})
    if it.get("match_quality") in ("weak", "free_text"):
        out["match_quality"] = it["match_quality"]
    if it.get("flags"):
        out["flags"] = it["flags"]
    if it.get("stale_days"):
        out["date_hr"], out["stale_days"] = it["date_hr"], it["stale_days"]
    notes = [n for n in it.get("notes") or [] if n.startswith(("izvan zadanog", "rinfuza", "nacionalna", "na vagu"))]
    if notes:
        out["notes"] = notes
    if "alternatives" in it:
        out["alternatives"] = [{k: a[k] for k in _ALT_KEYS if a.get(k) is not None} for a in it["alternatives"]]
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
    # usporedba lanaca (basket.compare_chains): najviše 6 redaka s >= 80 % sastojaka, ostali kao incomplete
    out["comparison"] = res.get("comparison", [])
    for k in ("incomplete", "assumptions", "ask_user", "unmatched", "warnings", "store_suggestions",
              "city_suggestions", "already_have"):
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
        WHERE {city_sql} {chain_sql}
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
    con = _con()
    try:
        st, _ = basket.resolve_name(staple)
        value, base, notes = basket.to_base(amount, unit, st)
    except (ValueError, basket.IngredientError) as e:
        return {**_price_list_date(con), **_error(e)}
    return {**_price_list_date(con), "staple": st.key, "amount": round(value, 2), "unit": base, "notes": notes}


def list_staples() -> dict:
    con = _con()
    staples = [{"key": s.key, "name": s.name, "unit": s.unit, "synonyms": list(s.synonyms[:6]),
                "attributes": {a: list(v) for a, v in s.attributes.items()}}
               for s in load_staples().values()]
    return _fit({**_price_list_date(con), "staples": staples}, ("staples",))


DESCRIPTIONS = {
    "find_products": """\
Traži proizvode po nazivu ili po namirnici; vraća grupe (isti EAN u više lanaca) s rasponom cijena.
Searches products by name or by staple ingredient; returns groups (same EAN across chains) with price ranges.
Kada / when: korisnik pita što postoji i koliko košta / the user asks what exists and what it costs.
Parametri / parameters: query (slobodan tekst / free text), city (grad / city), ingredient (ključ ili
sinonim iz list_staples / staple key or synonym), attributes (npr. {"tip": "glatko"}), include_weak
(slabija podudaranja / weaker matches, zadano false), limit (1-30).
Primjer / example: {"ingredient": "brašno", "attributes": {"tip": "glatko"}, "city": "Osijek"}""",
    "get_prices": """\
Cijene jednog proizvoda po trgovinama, od najjeftinije. / Prices of one product per store, cheapest first.
Kada / when: nakon find_products, za detalje / after find_products, for details.
Parametri / parameters: product_id = EAN, "lanac:product_id" ili id klase (npr. "jaja:m"); city.
Primjer / example: {"product_id": "3850104223624", "city": "Osijek"}""",
    "plan_basket": """\
Košarica za recept: cijena svih sastojaka po trgovini u gradu i najbolja trgovina.
Basket for a recipe: cost of all ingredients per store in the city, and the best store.
Kada / when: korisnik želi znati koliko košta jelo ili popis / the user wants the cost of a dish or list.
Prije poziva u jednoj poruci pitaj samo što nedostaje: grad, already_have, store ili usporedba svih, nadjev
ili dodaci. Ne dodaji nepotvrđene sastojke. / Before calling, ask in one message only for what is missing:
city, already_have, a store or all stores, filling or extras. Do not add unconfirmed ingredients.
Parametri / parameters: ingredients [{"name", "amount", "unit" (g|ml|kom), "form"?, "attributes"?,
"free_text"?}] (free_text: true za sastojak izvan list_staples, npr. "nutella" / for an ingredient outside
list_staples), city, store? {"chain", "address_contains"} (jedna trgovina; nacionalne cijene lanca vrijede /
one store; the chain's national prices still apply), already_have? ["sol", "papar"], price_overrides?
[{"name", "cost_pack"}] (stvarna cijena pakiranja, samo za ovaj poziv / real pack price, this call only),
alternatives (zadano true: do 2 druga proizvoda po stavci s delta_eur i cheaper / up to 2 other products
per item with delta_eur and cheaper).
Vraća / returns (sažeto / compact): summary_hr (počni njime / start with it), best_store (items s pack_size,
cost_pack, cost_used, alternatives; trgovine istog lanca s istim proizvodima spojene: n_stores, addresses),
comparison (po lancu do 6 redaka / one row per chain, up to 6: chain, addresses, n_stores_city, total_to_buy,
total_used, n_matched), incomplete (lanci bez >= 80 % sastojaka: missing / chains missing ingredients), ask_user,
warnings, unmatched (s prijedlozima / with suggestions), date_hr. detail=true: sve trgovine i sva polja /
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
        start, status = time.perf_counter(), "exception"
        try:
            out = fn(*args, **kwargs)
            status = "error" if "error" in out else "ok"
            text = _dumps(out)
            return CallToolResult(content=[TextContent(type="text", text=text)], is_error="error" in out)
        finally:
            TOOL_CALLS[(fn.__name__, status)] += 1
            log.info("tool=%s status=%s ms=%d calls=%d", fn.__name__, status, (time.perf_counter() - start) * 1000,
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


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


class RateLimit:
    """ASGI: ograničenja HTTP zahtjeva u `window` sekundi (429) i veličina tijela (413).

    - po IP-u (`limit`, MM_RATE_IP): IP klijenta iz veze; samo uz TRUSTED_PROXY=1 (poslužitelj iza vlastitog
      proxyja) iz CF-Connecting-IP, inače iz zadnjeg unosa X-Forwarded-For (adresa koju je vidio naš proxy;
      raniji unosi dolaze od klijenta i mogu se krivotvoriti);
    - po MCP sesiji (`session_limit`, MM_RATE_SESSION), kad zahtjev nosi Mcp-Session-Id;
    - ukupno (`global_limit`, MM_RATE_GLOBAL), visoko, kao zaštita poslužitelja.
    """

    def __init__(self, app, limit: int | None = None, window: float = 60.0, max_body: int = MAX_REQUEST_BYTES,
                 session_limit: int | None = None, global_limit: int | None = None,
                 trusted_proxy: bool | None = None):
        self.app, self.window, self.max_body = app, window, max_body
        self.limit = limit if limit is not None else _env_int("MM_RATE_IP", RATE_LIMIT)
        self.session_limit = session_limit if session_limit is not None else _env_int("MM_RATE_SESSION", RATE_SESSION)
        self.global_limit = global_limit if global_limit is not None else _env_int("MM_RATE_GLOBAL", RATE_GLOBAL)
        self.trusted_proxy = (os.environ.get("TRUSTED_PROXY") == "1") if trusted_proxy is None else trusted_proxy
        self.hits: dict[str, deque] = defaultdict(deque)  # "ip:..." / "session:..." / "global"
        self._last_prune = time.monotonic()

    def client_ip(self, scope, headers: dict[bytes, bytes]) -> str:
        if self.trusted_proxy:
            if cf := headers.get(b"cf-connecting-ip", b"").decode("latin-1").strip():
                return cf
            if xff := [p.strip() for p in headers.get(b"x-forwarded-for", b"").decode("latin-1").split(",") if p.strip()]:
                return xff[-1]
        return (scope.get("client") or ("?", 0))[0]

    def _over(self, key: str, limit: int, now: float) -> bool:
        q = self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        return len(q) >= limit

    def _prune(self, now: float) -> None:
        """Ključevi bez zahtjeva u prozoru se brišu (sesije i IP-ovi ne rastu bez granice)."""
        if now - self._last_prune < self.window:
            return
        self._last_prune = now
        for key in [k for k, q in self.hits.items() if not q or now - q[-1] > self.window]:
            del self.hits[key]

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = {k.lower(): v for k, v in scope.get("headers") or []}
        length = headers.get(b"content-length")
        if length and int(length) > self.max_body:
            return await self._reply(send, 413, "zahtjev je prevelik / request too large")
        now = time.monotonic()
        self._prune(now)
        keys = [("global", self.global_limit, "poslužitelj je zauzet / server is busy"),
                ("ip:" + self.client_ip(scope, headers), self.limit, "previše upita s ove adrese / too many requests")]
        if session := headers.get(b"mcp-session-id", b"").decode("latin-1").strip():
            keys.append(("session:" + session[:128], self.session_limit,
                         "previše upita u ovoj sesiji / too many requests in this session"))
        for key, limit, text in keys:
            if self._over(key, limit, now):
                return await self._reply(send, 429, f"{text}, pokušaj za minutu / retry in a minute")
        for key, _, _ in keys:
            self.hits[key].append(now)
        return await self.app(scope, receive, send)

    @staticmethod
    async def _reply(send, status: int, text: str):
        body = json.dumps({"error": text}, ensure_ascii=False).encode()
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"application/json"), (b"retry-after", b"60")]})
        await send({"type": "http.response.body", "body": body})


# --- HTTP: Host/Origin (DNS rebinding) ----------------------------------------------------------------------

LOCAL_HOSTS = ("127.0.0.1", "localhost", "[::1]", "::1")
LOCAL_ORIGINS = ("http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*")


def _match(value: str, pattern: str) -> bool:
    """Obrazac s * (bilo koji niz znakova); sve ostalo doslovno ("[::1]" nije skup znakova kao u fnmatch)."""
    return re.fullmatch(".*".join(re.escape(part) for part in pattern.split("*")), value) is not None


def _split_env(name: str) -> list[str]:
    return [p.strip() for p in os.environ.get(name, "").split(",") if p.strip()]


class HostGuard:
    """ASGI: zaštita od DNS rebindinga s obrascima hostova. SDK (TransportSecuritySettings) zna samo točne
    vrijednosti i "host:*" (bilo koji port), pa za tunel ("*.trycloudflare.com") njegovu provjeru gasimo i
    provjeravamo ovdje: Host bez porta mora pogoditi lokalni host ili obrazac iz MM_ALLOWED_HOSTS (* je bilo koji
    niz, "*.trycloudflare.com"), inače 421; Origin, ako ga ima, lokalni ili iz MM_ALLOWED_ORIGINS, inače 403."""

    def __init__(self, app, allowed_hosts: list[str] | None = None, allowed_origins: list[str] | None = None):
        self.app = app
        hosts = allowed_hosts if allowed_hosts is not None else _split_env("MM_ALLOWED_HOSTS")
        origins = allowed_origins if allowed_origins is not None else _split_env("MM_ALLOWED_ORIGINS")
        self.hosts = [h.lower() for h in (*LOCAL_HOSTS, *hosts)]
        self.origins = [o.lower().rstrip("/") for o in (*LOCAL_ORIGINS, *origins)]

    @staticmethod
    def _hostname(host: str) -> str:
        host = host.strip().lower()
        if host.startswith("["):  # [::1]:8000
            return host.split("]")[0] + "]"
        return host.rsplit(":", 1)[0] if host.count(":") == 1 else host

    def host_ok(self, host: str | None) -> bool:
        if not host:
            return False
        name = self._hostname(host)
        return any(_match(name, p) or _match(host.strip().lower(), p) for p in self.hosts)

    def origin_ok(self, origin: str | None) -> bool:
        if not origin:  # klijenti izvan preglednika ne šalju Origin
            return True
        origin = origin.lower().rstrip("/")
        return any(_match(origin, p) or (p.endswith(":*") and _match(origin, p[:-2])) for p in self.origins)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = {k.lower(): v.decode("latin-1") for k, v in scope.get("headers") or []}
        if not self.host_ok(headers.get(b"host")):
            return await _text(send, 421, "Invalid Host header (MM_ALLOWED_HOSTS)")
        if not self.origin_ok(headers.get(b"origin")):
            return await _text(send, 403, "Invalid Origin header (MM_ALLOWED_ORIGINS)")
        return await self.app(scope, receive, send)


async def _text(send, status: int, text: str, content_type: bytes = b"text/plain; charset=utf-8"):
    body = text.encode("utf-8")
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", content_type), (b"content-length", str(len(body)).encode())]})
    await send({"type": "http.response.body", "body": body})


HEALTH_MAX_AGE_HOURS = 48  # starija baza: status "stale" (ažuriranje dvaput dnevno, vidi update.py)


def version() -> str:
    try:
        from importlib.metadata import version as _v
        return _v("mealmeter")
    except Exception:  # noqa: BLE001
        return "dev"


def health() -> tuple[int, dict]:
    """GET /healthz: {status, db_date, db_age_hours, version}. Starost je od objave učitanog cjenika
    (clean.archive_info.updated), inače od izgradnje baze; "stale" iznad HEALTH_MAX_AGE_HOURS, "error" (503)
    kad baza nije čitljiva."""
    import datetime as dt

    try:
        con = _con()
        db_date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
        ts = None
        try:
            updated, loaded = con.execute(
                "SELECT updated, loaded_at FROM clean.archive_info ORDER BY date DESC LIMIT 1").fetchone()
            ts = dt.datetime.fromisoformat(updated) if updated else loaded.astimezone()
        except Exception:  # noqa: BLE001  (baza bez archive_info, npr. testovi)
            pass
        age = round((dt.datetime.now(dt.timezone.utc) - ts).total_seconds() / 3600, 1) if ts else None
    except Exception:  # noqa: BLE001
        return 503, {"status": "error", "db_date": None, "db_age_hours": None, "version": version()}
    status = "ok" if age is None or age <= HEALTH_MAX_AGE_HOURS else "stale"
    return 200, {"status": status, "db_date": db_date.isoformat() if db_date else None, "db_age_hours": age,
                 "version": version()}


HOME_HTML = """<!doctype html>
<html lang="hr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mealmeter</title>
<style>body{{font-family:system-ui,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;line-height:1.5}}
code{{background:#eee;padding:.1rem .3rem;border-radius:3px}}</style></head><body>
<h1>Mealmeter</h1>
<p><strong>Hrvatski.</strong> MCP konektor koji za jelo ili popis namirnica i grad pronalazi cijene u hrvatskim
trgovinama i najjeftiniju trgovinu. Besplatan, otvorenog koda, bez prijave.</p>
<p><strong>Dodavanje u Claude:</strong> Postavke &rarr; Konektori &rarr; Dodaj prilagođeni konektor, URL
<code>{url}</code>.</p>
<p><strong>Izvor podataka:</strong> službeni dnevni cjenici trgovina, preuzeti s
<a href="https://cijene.dev">cijene.dev</a> (DobarKod). Učitani cjenik: {db_date}.</p>
<p><strong>Napomena:</strong> cijene su iz cjenika; u trgovini se mogu razlikovati, cjenik nije zaliha, a akcije se
mijenjaju.</p>
<p><strong>Privatnost:</strong> nema računa ni kolačića. Sadržaj upita se ne sprema; zapisuje se samo broj poziva
po alatu, status i trajanje, bez punih IP adresa.</p>
<hr>
<p><strong>English.</strong> An MCP connector that finds grocery prices in Croatian stores for a dish or a shopping
list in a given city, and the cheapest store. Free, open source, no login.</p>
<p><strong>Add to Claude:</strong> Settings &rarr; Connectors &rarr; Add custom connector, URL <code>{url}</code>.</p>
<p><strong>Data source:</strong> the stores' official daily price lists via <a href="https://cijene.dev">cijene.dev</a>
(DobarKod). Loaded price list: {db_date}.</p>
<p><strong>Note:</strong> prices come from price lists; in-store prices may differ, a price list is not stock, and
promotions change.</p>
<p><strong>Privacy:</strong> no accounts or cookies. Query content is not stored; only the number of calls per tool,
status and duration are logged, without full IP addresses.</p>
<p><small>Mealmeter {version} · <a href="/healthz">/healthz</a></small></p>
</body></html>
"""


def home(host: str | None, proto: str | None = None) -> str:
    """GET /: kratka stranica (hr i en) s URL-om MCP endpointa za ovaj Host."""
    import html

    host = host or "localhost:8000"
    local = HostGuard._hostname(host) in LOCAL_HOSTS
    scheme = proto or ("http" if local else "https")
    _, h = health()
    return HOME_HTML.format(url=html.escape(f"{scheme}://{host}/mcp"), db_date=html.escape(h["db_date"] or "-"),
                            version=html.escape(h["version"]))


def anon_ip(ip: str | None) -> str:
    """IP bez zadnjeg dijela: IPv4 /24 ("203.0.113.x"), IPv6 /48 ("2001:db8:1::x")."""
    if not ip:
        return "?"
    if ":" in ip:
        return ":".join(ip.split(":")[:3]) + "::x"
    parts = ip.split(".")
    return ".".join(parts[:3]) + ".x" if len(parts) == 4 else "?"


class RequestLog:
    """ASGI: jedan redak po HTTP zahtjevu (metoda, putanja bez upita, status, trajanje, skraćeni IP).
    Tijelo zahtjeva (sadržaj upita) i query string se ne zapisuju; zamjenjuje uvicornov access log."""

    def __init__(self, app, trusted_proxy: bool | None = None):
        self.app = app
        self.ip = RateLimit(None, trusted_proxy=trusted_proxy).client_ip

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        start, status = time.perf_counter(), 500

        async def send_status(msg):
            nonlocal status
            if msg["type"] == "http.response.start":
                status = msg["status"]
            await send(msg)

        try:
            await self.app(scope, receive, send_status)
        finally:
            headers = {k.lower(): v for k, v in scope.get("headers") or []}
            log.info("http %s %s status=%d ms=%d ip=%s", scope.get("method"), scope.get("path"), status,
                     (time.perf_counter() - start) * 1000, anon_ip(self.ip(scope, headers)))


def http_app(server: MCPServer, host: str = "127.0.0.1", allowed_hosts: list[str] | None = None,
             allowed_origins: list[str] | None = None):
    """ASGI aplikacija za HTTP način: MCP na /mcp (streamable HTTP, bez sesija, JSON odgovori), zatim
    HostGuard (Host/Origin) i RateLimit. SDK-ova provjera Hosta je ugašena jer je zamjenjuje HostGuard."""
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
    return RequestLog(HostGuard(RateLimit(app), allowed_hosts, allowed_origins))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Mealmeter MCP poslužitelj")
    ap.add_argument("--http", action="store_true", help="streamable HTTP umjesto stdio")
    ap.add_argument("--host", default="127.0.0.1", help="adresa slušanja (zadano 127.0.0.1; tunel spaja lokalno)")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", default=None, help="putanja baze (inače MEALMETER_DB ili data/mealmeter.duckdb)")
    args = ap.parse_args(argv)
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
