"""Korak 4: MCP poslužitelj kroz MCP klijent u procesu (mcp.Client nad MCPServer)."""

import asyncio
import json

import pytest
from mcp import Client

from mealmeter import server as srv

TOOLS = {"find_products", "get_prices", "plan_basket", "list_stores", "convert_units", "list_staples"}


def _run(coro):
    return asyncio.run(coro)


async def _tools():
    async with Client(srv.create_server()) as c:
        return (await c.list_tools()).tools, c.instructions


def test_descriptions_bilingual():
    tools, instructions = _run(_tools())
    assert {t.name for t in tools} == TOOLS
    for t in tools:
        d = t.description
        # hrvatski / engleski: što radi (prvi redak "hr / en"), kada, parametri, primjer
        head = d.split("Kada / when")[0].strip().splitlines()  # opis: "hr / en" ili redak hr pa redak en
        assert len(head) >= 2 or " / " in head[0], t.name
        assert "Kada / when" in d and "Primjer / example" in d, t.name
        assert t.name == "list_staples" or "Parametri / parameters" in d, t.name
        assert t.annotations.read_only_hint
    for word in ("convert_units", "already_have", "store", "date_hr", "stale_days", "total_to_buy", "total_used",
                 "warnings", "ambiguity", "assumed_form", "match_quality", "alternatives", "price_overrides",
                 "zaliha", "stock", "izmišljaj",
                 # Korak 4B: jedna poruka pitanja, potvrđeni sastojci, free_text, cheaper, summary_hr, tablica
                 "JEDNOJ", "nadjev", "nije potvrdio", "free_text", "cheaper = true", "summary_hr",
                 "cijene iz cjenika od 20.10.2026.", "veličina pakiranja", "akcije se mijenjaju"):
        assert word in instructions, word
    plan = next(t for t in tools if t.name == "plan_basket").description
    for word in ("free_text", "summary_hr", "cheaper", "delta_eur", "n_stores", "pack_size"):
        assert word in plan, word
    assert "akcije se mijenjaju" in srv.PRICE_NOTE and "promotions change" in srv.PRICE_NOTE


# --- 3. ograničenja (HTTP po IP-u, veličina zahtjeva i odgovora) -------------------------------------

def _asgi_call(app, ip="1.2.3.4", length=None):
    sent = []

    async def send(msg):
        sent.append(msg)

    async def receive():
        return {"type": "http.request", "body": b""}

    headers = [(b"content-length", str(length).encode())] if length else []
    _run(app(dict(type="http", client=(ip, 1), headers=headers), receive, send))
    return sent[0]["status"]


def test_rate_limit_per_ip():
    app = srv.RateLimit(None, limit=3, window=60)
    app.app = lambda scope, receive, send: _inner_ok(send)
    assert [_asgi_call(app) for _ in range(4)] == [200, 200, 200, 429]
    assert _asgi_call(app, ip="5.6.7.8") == 200  # drugi IP ima svoju kvotu
    assert _asgi_call(app, ip="9.9.9.9", length=10**6) == 413


async def _inner_ok(send):
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"ok"})


def test_fit_truncates():
    out = srv._fit({"date": "x", "results": [{"name": "a" * 1000} for _ in range(50)]}, ("results",))
    assert out["truncated"] and srv._size(out) <= srv.MAX_RESPONSE_BYTES and len(out["results"]) < 50


def test_cli_args():
    import inspect

    src = inspect.getsource(srv.main)
    assert '"--http"' in src and '"--port"' in src and 'server.run("stdio")' in src


# --- 4. svi alati kroz MCP klijent (fixture baza) -----------------------------------------------------

SCHEMA = {  # alat -> (obavezni parametri, svi parametri)
    "find_products": (set(), {"query", "city", "ingredient", "attributes", "include_weak", "limit"}),
    "get_prices": ({"product_id"}, {"product_id", "city"}),
    "plan_basket": ({"ingredients", "city"}, {"ingredients", "city", "store", "already_have", "price_overrides",
                                              "alternatives"}),
    "list_stores": ({"city"}, {"city", "chain"}),
    "convert_units": ({"amount", "unit", "staple"}, {"amount", "unit", "staple"}),
    "list_staples": (set(), set()),
}
PANCAKES = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
            {"name": "jaja", "amount": 3, "unit": "kom"}]


async def _calls(con, calls):
    async with Client(srv.create_server(con=con)) as c:
        out = []
        for name, args in calls:
            r = await c.call_tool(name, args)
            text = r.content[0].text
            out.append((r.is_error, len(text.encode("utf-8")), json.loads(text)))
        return out


def call(con, name, args):
    return _run(_calls(con, [(name, args)]))[0]


def test_schemas():
    tools, _ = _run(_tools())
    for t in tools:
        req, props = SCHEMA[t.name]
        schema = t.input_schema
        assert set(schema.get("properties", {})) == props, t.name
        assert set(schema.get("required", [])) == req, t.name
        assert all(p.get("description") for p in schema.get("properties", {}).values()), t.name


@pytest.mark.parametrize("name,args", [
    ("find_products", {"ingredient": "brašno", "city": "Osijek"}),
    ("find_products", {"query": "mlijeko", "limit": 30}),
    ("get_prices", {"product_id": "3850104223624"}),
    ("plan_basket", {"ingredients": PANCAKES, "city": "Osijek"}),
    ("list_stores", {"city": "Osijek"}),
    ("convert_units", {"amount": 2, "unit": "žlica", "staple": "šećer"}),
    ("list_staples", {}),
])
def test_all_tools_small_and_dated(con, name, args):
    err, size, out = call(con, name, args)
    assert not err and "error" not in out
    assert size <= srv.MAX_RESPONSE_BYTES
    assert out.get("date") and (name == "plan_basket" or out.get("date_hr"))


def test_dates_per_store(con):
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek"})
    for s in out["stores"]:
        assert s["date_hr"] and "stale_days" in s
    assert "total_to_buy" in out["best_store"] and "total_used" in out["best_store"]
    _, _, stores = call(con, "list_stores", {"city": "Osijek", "chain": "konzum"})
    assert stores["stores"] and all(s["chain"] == "konzum" and "stale_days" in s for s in stores["stores"])
    _, _, prices = call(con, "get_prices", {"product_id": "3850104223624", "city": "Osijek"})
    assert all("stale_days" in r and r["date_hr"] for r in prices["stores"])


def test_errors_are_tool_errors(con):
    err, _, out = call(con, "get_prices", {"product_id": "123"})
    assert err and "error" in out
    err, _, out = call(con, "convert_units", {"amount": 1, "unit": "kom", "staple": "brašno"})
    assert err and "error" in out


def test_store(con):
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek",
                                          "store": {"chain": "spar", "address_contains": ""}})
    assert {s["chain"] for s in out["stores"]} == {"spar"} and out["best_store"]["chain"] == "spar"
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek",
                                          "store": {"chain": "konzum", "address_contains": "nema-te-ulice"}})
    assert out["stores"] == [] and out["best_store"] is None
    assert any("nema trgovine" in w for w in out["warnings"]) and out["store_suggestions"]


@pytest.fixture(scope="module")
def alt_con(tmp_path_factory):
    """Fixture baza + tri dodatna brašna u Konzumu Osijek (fixture ima jedan proizvod po namirnici i trgovini)."""
    import duckdb

    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path_factory.mktemp("alt") / "a.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'A1', 'konzum:A1', 'BRAŠNO PŠENIČNO GLATKO T-550 1 kg K PLUS', 'Brašno', 'KOM'),
                 ('konzum', 'A2', 'konzum:A2', 'BRAŠNO GLATKO T-400 1 kg MLINAR', 'Brašno', 'KOM'),
                 ('konzum', 'A3', 'konzum:A3', 'BRAŠNO GLATKO T-550 5 kg MLINAR', 'Brašno', 'KOM')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('konzum', '0907', 'A1', 0.69, DATE '2026-10-19'), ('konzum', '0907', 'A2', 0.99, DATE '2026-10-19'),
                 ('konzum', '0907', 'A3', 3.49, DATE '2026-10-19')""")
    build_clean(c)
    yield c
    c.close()


def test_alternatives(alt_con):
    con = alt_con
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek",
                                          "store": {"chain": "konzum", "address_contains": ""}})
    items = out["best_store"]["items"]
    assert all(len(it["alternatives"]) <= 2 for it in items)
    flour = next(it for it in items if it["staple"] == "brasno")
    # Korak 4C: samo jeftinije alternative; odabrano brašno je najjeftinije pakiranje koje pokriva količinu
    assert all(a["cheaper"] and a["product_id"] != flour["product_id"] for a in flour["alternatives"])
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek", "alternatives": False})
    assert all("alternatives" not in it for it in out["best_store"]["items"])


def test_price_overrides(con):
    _, _, base = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek"})
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek",
                                          "price_overrides": [{"name": "brašno", "cost_pack": 9.99}]})
    b0, b1 = base["best_store"], out["best_store"]
    flour = next(it for it in b1["items"] if it["staple"] == "brasno")
    old = next(it for it in b0["items"] if it["staple"] == "brasno")
    assert flour["user_provided"] and flour["cost_pack"] == round(9.99 * flour["n_packs"], 2)
    assert flour["computed_cost_pack"] == old["cost_pack"]
    assert b1["total_to_buy"] == pytest.approx(b0["total_to_buy"] - old["cost_pack"] + flour["cost_pack"], abs=0.011)
    assert not any(it.get("user_provided") for it in b1["items"] if it["staple"] != "brasno")
    _, _, out = call(con, "plan_basket", {"ingredients": PANCAKES, "city": "Osijek",
                                          "price_overrides": [{"name": "kavijar", "cost_pack": 1}]})
    assert any("price_overrides" in w for w in out["warnings"])
