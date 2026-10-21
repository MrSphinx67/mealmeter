"""MCP poslužitelj (službeni Python SDK, mcp 2.x: MCPServer, nekadašnji FastMCP).

Pokretanje:
    python -m mealmeter.server                    # stdio (Claude Desktop, lokalno)
    python -m mealmeter.server --http --port 8000 # streamable HTTP na /mcp

Javni podaci samo za čitanje, bez prijave. HTTP ima ograničenje upita po IP-u (RATE_LIMIT u minuti) i
veličine zahtjeva; svaki odgovor alata je najviše MAX_RESPONSE_BYTES (dulji popisi se skraćuju, uz
truncated = true). Baza: MEALMETER_DB ili data/mealmeter.duckdb.
"""

import argparse
import functools
import inspect
import json
import os
import threading
import time
from collections import defaultdict, deque
from typing import Annotated, Any

import duckdb
from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult, TextContent, ToolAnnotations
from pydantic import Field

from mealmeter import basket, search
from mealmeter.normalize import date_hr, norm_text
from mealmeter.staples import load_staples

MAX_RESPONSE_BYTES = 20_000
RATE_LIMIT = 60  # upita po IP-u u minuti (HTTP)
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
8. Prenesi warnings, ambiguity (pitaj o obliku, zadaj form i ponovi), assumed_form, slabije podudaranje
   (match_quality = 'weak') i stavke nađene slobodnom pretragom (match_quality = 'free_text': neka korisnik
   provjeri proizvod), sve običnim riječima. / Pass on warnings, ambiguity (ask, then retry with form),
   assumed_form, weaker matches and free-text matches (ask the user to check the product), in plain words.
9. Kad korisnik kaže stvarnu cijenu, ponovno pozovi plan_basket s price_overrides; ne zbrajaj sam.
   / When the user reports a real price, call plan_basket again with price_overrides; do not add up
   totals yourself.
10. Uz cijene uvijek dodaj: cijene su iz cjenika, u trgovini se mogu razlikovati, cjenik nije zaliha,
   a akcije se mijenjaju. / With prices always add that they come from price lists, may differ in store, a price list
   is not stock, and promotions change.
"""

_local = threading.local()
_db_path: str | None = None
_shared_con: duckdb.DuckDBPyConnection | None = None


def _con() -> duckdb.DuckDBPyConnection:
    """Kursor po dretvi nad jednom read-only vezom (ili vezom zadanom za testove)."""
    global _shared_con
    if _shared_con is None:
        _shared_con = search.connect(_db_path)  # MEALMETER_DB ili data/mealmeter.duckdb, read-only
    cur = getattr(_local, "cur", None)
    if cur is None or getattr(_local, "owner", None) is not _shared_con:
        _local.cur, _local.owner = _shared_con.cursor(), _shared_con
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
        description="Do 2 druga proizvoda po stavci, s delta_eur i cheaper / up to 2 alternatives per item, with "
                    "delta_eur and cheaper")] = True,
) -> dict:
    con = _con()
    try:
        res = basket.plan_basket(ingredients, city, con=con, max_stores=3, already_have=already_have,
                                 store=store, alternatives=alternatives, price_overrides=price_overrides)
    except ValueError as e:
        return _error(e)
    res.setdefault("date", _price_list_date(con)["date"])
    res["note"] = PRICE_NOTE
    # ostale trgovine bez alternativa (alternative nosi best_store), da odgovor ostane kratak
    for s in res["stores"]:
        if s is not res["best_store"]:
            for it in s["items"]:
                it.pop("alternatives", None)
    return _fit(res, ("stores", "best_store.items"))


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
Vraća / returns: summary_hr (počni njime / start with it), best_store (items s pack_size, cost_pack,
cost_used), stores (do 3; trgovine istog lanca s istim proizvodima spojene: n_stores, addresses), warnings,
ambiguous, unmatched (s prijedlozima / with suggestions), date_hr.
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


def _as_result(fn):
    """Alat vraća CallToolResult sa sažetim JSON-om (bez uvlačenja i bez dvostrukog structured_content),
    tako da je ograničenje MAX_RESPONSE_BYTES stvarna veličina odgovora; {"error": ...} je isError."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> CallToolResult:
        out = fn(*args, **kwargs)
        return CallToolResult(content=[TextContent(type="text", text=_dumps(out))], is_error="error" in out)

    wrapper.__signature__ = inspect.signature(fn).replace(return_annotation=CallToolResult)
    wrapper.__annotations__ = {**fn.__annotations__, "return": CallToolResult}
    return wrapper


def create_server(con: duckdb.DuckDBPyConnection | None = None, db_path: str | None = None) -> MCPServer:
    """Poslužitelj s alatima. `con` (testovi) ili `db_path` zamjenjuju zadanu bazu."""
    global _shared_con, _db_path
    if con is not None:
        _shared_con = con
    if db_path:
        _db_path = db_path
    server = MCPServer(name="mealmeter", title="Mealmeter", instructions=INSTRUCTIONS,
                       description="Cijene namirnica u hrvatskim trgovinama / grocery prices in Croatian stores")
    ro = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
    for fn in TOOLS:
        server.tool(name=fn.__name__, description=DESCRIPTIONS[fn.__name__], annotations=ro)(_as_result(fn))
    return server


class RateLimit:
    """ASGI: najviše `limit` HTTP zahtjeva po IP-u u `window` sekundi (429) i veličina tijela (413)."""

    def __init__(self, app, limit: int = RATE_LIMIT, window: float = 60.0, max_body: int = MAX_REQUEST_BYTES):
        self.app, self.limit, self.window, self.max_body = app, limit, window, max_body
        self.hits: dict[str, deque] = defaultdict(deque)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        ip = (scope.get("client") or ("?", 0))[0]
        now, q = time.monotonic(), self.hits[ip]
        while q and now - q[0] > self.window:
            q.popleft()
        length = dict(scope.get("headers") or []).get(b"content-length")
        if length and int(length) > self.max_body:
            return await self._reply(send, 413, "zahtjev je prevelik / request too large")
        if len(q) >= self.limit:
            return await self._reply(send, 429, "previše upita, pokušaj za minutu / too many requests, retry in a minute")
        q.append(now)
        return await self.app(scope, receive, send)

    @staticmethod
    async def _reply(send, status: int, text: str):
        body = json.dumps({"error": text}, ensure_ascii=False).encode()
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"application/json"), (b"retry-after", b"60")]})
        await send({"type": "http.response.body", "body": body})


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Mealmeter MCP poslužitelj")
    ap.add_argument("--http", action="store_true", help="streamable HTTP umjesto stdio")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--db", default=None, help="putanja baze (inače MEALMETER_DB ili data/mealmeter.duckdb)")
    args = ap.parse_args(argv)
    server = create_server(db_path=args.db)
    if not args.http:
        server.run("stdio")
        return
    import uvicorn

    app = server.streamable_http_app(stateless_http=True, json_response=True, max_request_body_size=MAX_REQUEST_BYTES,
                                     host=args.host)
    uvicorn.run(RateLimit(app), host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
