"""Korak 5A: ispravci iz 4C (unit stupac za tekućine, razred jaja u navodnicima, mlijeko) i HTTP."""

import duckdb
import pytest

from mealmeter.build import build_clean, load_raw
from mealmeter.staples import extract_attributes, load_staples
from tests.conftest import FIXTURE


# --- 0. ispravci iz 4C ------------------------------------------------------------------------------------

def test_liquid_unit_column_wins(tmp_path):
    c = duckdb.connect(str(tmp_path / "o.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit, quantity) VALUES
                 ('lidl', 'U1', 'lidl:U1', 'Suncokretovo ulje 20g Lidla', 'Hrana', '1l', '0.92'),
                 ('lidl', 'U2', 'lidl:U2', 'Brašno glatko 1kg', 'Hrana', '1kg', '1')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('lidl', '105', 'U1', 1.38, DATE '2026-10-19'), ('lidl', '105', 'U2', 0.75, DATE '2026-10-19')""")
    build_clean(c)
    rows = {r[0]: r[1:] for r in c.execute("""SELECT p.product_id, p.pack_amount, p.pack_unit, p.pack_source,
               c.price_per_unit::DOUBLE FROM clean.products p JOIN clean.prices c USING (chain, product_id)
               WHERE p.chain = 'lidl' AND p.product_id IN ('U1', 'U2')""").fetchall()}
    assert rows["U1"] == (1000.0, "ml", "unit", 1.38)
    assert rows["U2"][:3] == (1000.0, "g", "name")  # grami iz naziva uz kg u unit: naziv ostaje
    c.close()


@pytest.mark.parametrize("name,size", [
    ('Jaja iz kaveznog uzgoja, razred "S"', "s"),
    ('Jaja razred " S "', "s"),
    ('JAJA "M" 10 KOM', "m"),
    ('Jaja razred „L“', "l"),
    ("Perfa Jaja iz podnog uzgoja,M,bijel", "m"),
    ("Jaja, M razred, 30kom", "m"),
    ("Jaja iz podnog uzgoja XXL, razred L", "l"),
    ("Lukač Jaja podni uzgoj, razred S", "s"),
    ("JAJE S IGRAČKOM", None),
])
def test_egg_size_in_quotes(name, size):
    assert extract_attributes(load_staples()["jaja"], name).get("velicina") == size


def test_milk_lower_bound():
    assert load_staples()["mlijeko"].plausible_per_unit == (0.3, 4)


# --- 1. HTTP: Host zaglavlje tunela -------------------------------------------------------------------------

import asyncio  # noqa: E402
import json  # noqa: E402

INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "test", "version": "0"}}}


async def _request(app, method, path, host, body=None, origin=None, client=("10.0.0.1", 1)):
    headers = [(b"host", host.encode())]
    if body is not None:
        headers += [(b"content-type", b"application/json"), (b"accept", b"application/json, text/event-stream")]
    if origin:
        headers.append((b"origin", origin.encode()))
    data = json.dumps(body).encode() if body is not None else b""
    headers.append((b"content-length", str(len(data)).encode()))
    sent, done = [], False

    async def receive():
        nonlocal done
        if done:
            await asyncio.sleep(3600)
        done = True
        return {"type": "http.request", "body": data, "more_body": False}

    async def send(msg):
        sent.append(msg)

    scope = {"type": "http", "method": method, "path": path, "raw_path": path.encode(), "query_string": b"",
             "headers": headers, "client": client, "server": ("127.0.0.1", 8000), "scheme": "http",
             "http_version": "1.1", "root_path": ""}
    await app(scope, receive, send)
    start = next(m for m in sent if m["type"] == "http.response.start")
    body_bytes = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    return start["status"], body_bytes


def _inner(app):
    while hasattr(app, "app"):
        app = app.app
    return app


def run_http(app, calls):
    async def go():
        starlette_app = _inner(app)
        async with starlette_app.router.lifespan_context(starlette_app):
            return [await _request(app, *c) for c in calls]
    return asyncio.run(go())


def test_tunnel_host_accepted(con):
    from mealmeter import server as srv

    app = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.trycloudflare.com"], allowed_origins=[])
    out = run_http(app, [
        ("POST", "/mcp", "example.trycloudflare.com", INIT),
        ("POST", "/mcp", "example.trycloudflare.com", {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
        ("POST", "/mcp", "evil.example.com", INIT),
        ("POST", "/mcp", "127.0.0.1:8000", INIT),
        ("POST", "/mcp", "example.trycloudflare.com", INIT, "https://evil.example.com"),
    ])
    assert out[0][0] == 200 and json.loads(out[0][1])["result"]["serverInfo"]["name"] == "mealmeter"
    assert out[1][0] == 200 and len(json.loads(out[1][1])["result"]["tools"]) == 6
    assert out[2] == (421, b"Invalid Host header (MM_ALLOWED_HOSTS)")
    assert out[3][0] == 200  # lokalno uvijek
    assert out[4][0] == 403


def test_sdk_default_would_reject_tunnel(con):
    """Zašto HostGuard: SDK uz host=127.0.0.1 sam uključi zaštitu i pušta samo localhost (421)."""
    from mealmeter import server as srv

    server = srv.create_server(con=con)
    app = server.streamable_http_app(stateless_http=True, json_response=True, host="127.0.0.1")
    status, body = run_http(app, [("POST", "/mcp", "example.trycloudflare.com", INIT)])[0]
    assert status == 421 and b"Invalid Host header" in body


def test_host_guard_patterns(monkeypatch):
    from mealmeter.server import HostGuard

    monkeypatch.setenv("MM_ALLOWED_HOSTS", "mealmeter.example.hr, *.trycloudflare.com")
    monkeypatch.setenv("MM_ALLOWED_ORIGINS", "https://claude.ai")
    g = HostGuard(None)
    assert g.host_ok("abc-def.trycloudflare.com") and g.host_ok("abc.trycloudflare.com:443")
    assert g.host_ok("mealmeter.example.hr") and g.host_ok("localhost:8000") and g.host_ok("[::1]:8000")
    assert not g.host_ok("trycloudflare.com.evil.net") and not g.host_ok("evil.com") and not g.host_ok(None)
    assert g.origin_ok(None) and g.origin_ok("https://claude.ai") and g.origin_ok("http://localhost:6274")
    assert not g.origin_ok("https://evil.example.com")


# --- 2. /healthz i / ----------------------------------------------------------------------------------------

def test_healthz_and_home(con):
    from mealmeter import server as srv

    app = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.trycloudflare.com"], allowed_origins=[])
    (hs, hb), (ps, pb), (bs, _) = run_http(app, [("GET", "/healthz", "example.trycloudflare.com"),
                                                 ("GET", "/", "example.trycloudflare.com"),
                                                 ("GET", "/healthz", "evil.example.com")])
    h = json.loads(hb)
    assert hs == 200 and set(h) == {"status", "db_date", "db_age_hours", "version"}
    assert h["status"] in ("ok", "stale") and h["db_date"] == "2026-10-19" and h["version"]
    page = pb.decode()
    assert ps == 200 and "https://example.trycloudflare.com/mcp" in page
    for word in ("cijene.dev", "DobarKod", "Privatnost", "Privacy", "nije zaliha", "not stock", "Konektori"):
        assert word in page, word
    assert bs == 421


# --- 4. logiranje bez sadržaja upita i punih IP adresa ---------------------------------------------------

def test_logs_without_content_or_ip(con, caplog):
    import logging

    from mealmeter import server as srv

    caplog.set_level(logging.DEBUG)
    app = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.trycloudflare.com"], allowed_origins=[])
    call = {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "plan_basket", "arguments": {
                "ingredients": [{"name": "TAJNISASTOJAK", "amount": 1, "unit": "g"}], "city": "Osijek"}}}
    before = srv.TOOL_CALLS[("plan_basket", "ok")]
    out = run_http(app, [("POST", "/mcp", "example.trycloudflare.com", INIT, None, ("203.0.113.77", 5)),
                         ("POST", "/mcp", "example.trycloudflare.com", call, None, ("203.0.113.77", 5))])
    assert [s for s, _ in out] == [200, 200]
    text = "\n".join(r.getMessage() for r in caplog.records)
    assert "TAJNISASTOJAK" not in text and "Osijek" not in text and "203.0.113.77" not in text
    assert "tool=plan_basket status=ok" in text and "ip=203.0.113.x" in text and "http POST /mcp status=200" in text
    assert srv.TOOL_CALLS[("plan_basket", "ok")] == before + 1


def test_anon_ip_and_no_access_log():
    import inspect

    from mealmeter import server as srv

    assert srv.anon_ip("203.0.113.77") == "203.0.113.x" and srv.anon_ip("2001:db8:1:2::5") == "2001:db8:1::x"
    assert srv.anon_ip(None) == "?"
    assert "access_log=False" in inspect.getsource(srv.main)
