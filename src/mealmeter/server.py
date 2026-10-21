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
from typing import Any

import duckdb
from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult, TextContent, ToolAnnotations

from mealmeter import basket, search
from mealmeter.normalize import date_hr, norm_text
from mealmeter.staples import load_staples

MAX_RESPONSE_BYTES = 20_000
RATE_LIMIT = 60  # upita po IP-u u minuti (HTTP)
MAX_REQUEST_BYTES = 64_000
PRICE_NOTE = ("Cijene su iz službenih cjenika trgovina (cijene.dev); u trgovini se mogu razlikovati, a cjenik "
              "nije zaliha. / Prices come from the stores' official price lists (cijene.dev); in-store prices "
              "may differ and a price list is not stock.")

INSTRUCTIONS = """\
Mealmeter: cijene namirnica u hrvatskim trgovinama iz službenih dnevnih cjenika (cijene.dev).
Mealmeter: grocery prices in Croatian stores from the official daily price lists (cijene.dev).

Pravila / rules:
1. Količine šalji u g, ml ili kom. Žlice, šalice, prstohvat, češnjeve i glavice pretvori sam ili pozovi
   convert_units. / Send amounts in g, ml or kom (pieces); convert cups, spoons, cloves etc. yourself or
   call convert_units.
2. Prije plan_basket pitaj korisnika: grad, što već ima kod kuće (already_have) i ide li u određenu
   trgovinu (store; list_stores daje adrese). / Before plan_basket ask for the city, what the user already
   has at home (already_have) and whether they shop at a particular store (store; see list_stores).
3. Uvijek prikaži datum cjenika (date_hr) i starost podataka (stale_days > 0 znači prenesenu cijenu).
   / Always show the price-list date (date_hr) and data age (stale_days > 0 = carried-forward price).
4. Navedi oba zbroja: total_to_buy (cijela pakiranja koja treba kupiti) i total_used (razmjerni trošak
   utrošene količine). / Report both total_to_buy (whole packs to buy) and total_used (cost of the amount
   actually used).
5. Ne izmišljaj cijene ni proizvode: koristi samo ono što alati vrate. / Never invent prices or products;
   use only what the tools return.
6. Prenesi korisniku warnings, ambiguity (pitanje o obliku: zadaj form i ponovi), assumed_form i
   match_quality = 'weak' (slabije podudaranje). / Pass on warnings, ambiguity (ask, then retry with form),
   assumed_form and match_quality = 'weak'.
7. Kad proizvoda nema na polici, ponudi alternatives iz iste trgovine. / If a product is not on the shelf,
   offer the item's alternatives from the same store.
8. Kad korisnik kaže stvarnu cijenu, ponovno pozovi plan_basket s price_overrides; ne zbrajaj sam.
   / When the user reports a real price, call plan_basket again with price_overrides; do not add up
   totals yourself.
9. Uz cijene dodaj: cijene su iz cjenika, u trgovini se mogu razlikovati, cjenik nije zaliha. / With prices,
   add that they come from price lists, may differ in store, and a price list is not stock.
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


# --- alati --------------------------------------------------------------------------------------------

def find_products(query: str | None = None, city: str | None = None, ingredient: str | None = None,
                  attributes: dict[str, str] | None = None, include_weak: bool = False, limit: int = 10) -> dict:
    con = _con()
    try:
        rows = search.find_products(query, city=city, limit=max(1, min(limit, 30)), con=con,
                                    ingredient=ingredient, attributes=attributes, include_weak=include_weak)
    except ValueError as e:
        return _error(e)
    out = {**_price_list_date(con), "stale_days": max((r.get("stale_days") or 0 for r in rows), default=0),
           "results": rows, "note": PRICE_NOTE}
    return _fit(out, ("results",))


def get_prices(product_id: str, city: str | None = None) -> dict:
    con = _con()
    try:
        rows = search.get_prices(product_id, city=city, limit=50, con=con)
    except ValueError as e:
        return _error(e)
    out = {**_price_list_date(con), "product_id": product_id, "stores": rows, "note": PRICE_NOTE}
    return _fit(out, ("stores",))


def plan_basket(ingredients: list[dict[str, Any]], city: str, store: dict[str, str] | None = None,
                already_have: list[str] | None = None, price_overrides: list[dict[str, Any]] | None = None,
                alternatives: bool = True) -> dict:
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


def list_stores(city: str, chain: str | None = None) -> dict:
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


def convert_units(amount: float, unit: str, staple: str) -> dict:
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
Prije poziva pitaj grad, already_have i store. / Before calling, ask for city, already_have and store.
Parametri / parameters: ingredients [{"name", "amount", "unit" (g|ml|kom), "form"?, "attributes"?}],
city, store? {"chain", "address_contains"} (jedna trgovina; nacionalne cijene lanca vrijede / one store;
the chain's national prices still apply), already_have? ["sol", "papar"], price_overrides?
[{"name", "cost_pack"}] (stvarna cijena pakiranja, samo za ovaj poziv / real pack price, this call only),
alternatives (zadano true: do 2 druga proizvoda po stavci / up to 2 other products per item).
Vraća / returns: best_store s total_to_buy i total_used, stores (do 3), warnings, ambiguous, date_hr.
Primjer / example: {"ingredients": [{"name": "brašno glatko", "amount": 250, "unit": "g"},
{"name": "mlijeko", "amount": 500, "unit": "ml"}, {"name": "jaja", "amount": 3, "unit": "kom"}],
"city": "Osijek", "already_have": ["sol"]}""",
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
