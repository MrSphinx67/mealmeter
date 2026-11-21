"""Korak 18 (Active CPU na Vercelu): jeftini MCP zahtjevi bez SDK-a i baze, metapodaci sažete baze, libyaml, cpu_ms."""

import asyncio
import glob
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

import duckdb
import pytest
import yaml

from mealmeter import server as srv
from mealmeter import web
from mealmeter.normalize import load_yaml
from tests.test_step5a import INIT, _inner
from tests.test_step5v import _raw
from tests.test_step12 import carried  # noqa: F401  (fixture: puna i sažeta baza iz fixture-arhive)

ROOT = Path(__file__).resolve().parents[1]
HOST = {"host": "mealmeter.vercel.app"}
STD = {**HOST, "content-type": "application/json", "accept": "application/json, text/event-stream"}


def _init(version, rid=1, **extra):
    return {"jsonrpc": "2.0", "id": rid, "method": "initialize",
            "params": {"protocolVersion": version, "capabilities": {}, "clientInfo": {"name": "t", "version": "1"},
                       **extra}}


LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
NOTIF = {"jsonrpc": "2.0", "method": "notifications/initialized"}

# (opis, zaglavlja, tijelo, treba li brzi put odgovoriti)
CASES = [
    *[(f"initialize {v}", STD, _init(v), True) for v in ("2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25")],
    ("initialize nepoznata verzija", STD, _init("1999-01-01"), True),
    ("initialize 2026-07-28 u tijelu", STD, _init("2026-07-28"), True),
    ("initialize string id", STD, _init("2025-06-18", rid="abc-č"), True),
    ("initialize Claude", STD, {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {"roots": {"listChanged": True}, "sampling": {},
                                                          "elicitation": {}},
        "clientInfo": {"name": "claude-ai", "version": "0.1.0"}}}, True),
    ("initialize samo application/json", {**STD, "accept": "application/json"}, _init("2025-06-18"), True),
    ("initialize */*", {**STD, "accept": "*/*"}, _init("2025-06-18"), True),
    ("initialize content-type s charsetom", {**STD, "content-type": "application/json; charset=utf-8"},
     _init("2025-06-18"), True),
    ("initialize bez accept", {k: v for k, v in STD.items() if k != "accept"}, _init("2025-06-18"), False),
    ("initialize text/plain", {**STD, "content-type": "text/plain"}, _init("2025-06-18"), False),
    ("initialize bez clientInfo", STD, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                        "params": {"protocolVersion": "2025-06-18", "capabilities": {}}}, False),
    ("initialize zaglavlje 2026-07-28", {**STD, "mcp-protocol-version": "2026-07-28"}, _init("2026-07-28"), False),
    ("initialize batch", STD, [_init("2025-06-18")], False),
    ("initialize jsonrpc 1.0", STD, {**_init("2025-06-18"), "jsonrpc": "1.0"}, False),
    ("notifications/initialized", {**STD, "mcp-protocol-version": "2025-06-18"}, NOTIF, True),
    ("notifications/initialized bez verzije", STD, NOTIF, True),
    ("notifications/cancelled", STD, {"jsonrpc": "2.0", "method": "notifications/cancelled",
                                      "params": {"requestId": 1}}, True),
    ("notifications loša verzija", {**STD, "mcp-protocol-version": "1999-01-01"}, NOTIF, False),
    ("tools/list", {**STD, "mcp-protocol-version": "2025-06-18"}, LIST, True),
    ("tools/list bez verzije", STD, LIST, True),
    ("tools/list params {}", {**STD, "mcp-protocol-version": "2025-11-25"}, {**LIST, "params": {}}, True),
    ("tools/list _meta", STD, {**LIST, "params": {"_meta": {"progressToken": 1}}}, True),
    ("tools/list cursor", STD, {**LIST, "params": {"cursor": "x"}}, False),
    ("tools/list 2026-07-28", {**STD, "mcp-protocol-version": "2026-07-28"}, LIST, False),
    ("tools/list sesija", {**STD, "mcp-session-id": "abc"}, LIST, True),  # Korak 19: SDK bez sesija je zanemaruje
    ("ping", {**STD, "mcp-protocol-version": "2025-06-18"}, {"jsonrpc": "2.0", "id": 9, "method": "ping"}, True),
    ("resources/list", STD, {"jsonrpc": "2.0", "id": 3, "method": "resources/list"}, True),  # Korak 19: prazan popis
    ("tools/call", STD, {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                         "params": {"name": "list_staples", "arguments": {}}}, False),
]


def test_static_snapshot_is_current():
    """mcp_static.json = odgovori SDK-a za trenutne upute i opise alata (nakon promjene: --write-static)."""
    assert json.loads(web.STATIC_PATH.read_text(encoding="utf-8")) == srv.static_snapshot()


def test_fast_reply_matches_sdk_byte_for_byte(con):
    """Svaki zahtjev na koji brzi put odgovara: isti status, zaglavlja i tijelo kao SDK; ostali idu SDK-u."""
    app = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.vercel.app"], allowed_origins=[])

    async def go():
        inner = _inner(app)
        async with inner.router.lifespan_context(inner):
            return [await _raw(app, "POST", "/mcp", h, json.dumps(b).encode()) for _, h, b, _ in CASES]
    sdk = asyncio.run(go())
    for (name, headers, body, fast), (status, sdk_headers, sdk_body) in zip(CASES, sdk):
        hdrs = {k.encode(): v.encode() for k, v in headers.items()}
        reply = web.fast_reply(hdrs, json.dumps(body).encode())
        assert (reply is not None) == fast, name
        if reply:
            st, rh, rb = reply
            assert st == status and rb == sdk_body, (name, rb[:200], sdk_body[:200])
            assert dict(rh) == {k: v for k, v in sdk_headers.items() if k in (b"content-type", b"content-length")}, name
            assert set(sdk_headers) <= {b"content-type", b"content-length"}, name


def _vercel(con):
    return web.VercelApp(lambda: srv.sdk_app(srv.create_server(con=con), host="0.0.0.0"),
                         allowed_hosts=["*.vercel.app"], allowed_origins=[])


def test_vercel_app_routes_same_as_sdk(con):
    """Iste putanje i metode kao test_routes_and_methods (Korak 5V3): VercelApp i lokalni http_app (SDK) vraćaju
    isti status i tijelo; GET /, /healthz, 404 i jeftini MCP zahtjevi ne učitavaju SDK."""
    from mealmeter.asgi import LifespanOnDemand

    calls = [
        ("POST", "/mcp", STD, _init("2025-06-18")), ("POST", "/api/index/mcp", STD, _init("2025-06-18")),
        ("POST", "/mcp", STD, NOTIF), ("POST", "/mcp", STD, LIST),
        ("GET", "/mcp", HOST, None), ("DELETE", "/mcp", HOST, None), ("HEAD", "/mcp", HOST, None),
        ("GET", "/.well-known/oauth-protected-resource", HOST, None),
        ("GET", "/.well-known/oauth-protected-resource/mcp", HOST, None),
        ("GET", "/.well-known/oauth-authorization-server", HOST, None),
        ("POST", "/.well-known/oauth-authorization-server", STD, {"x": 1}),
        ("GET", "/nepostoji", HOST, None), ("GET", "/healthz", HOST, None), ("GET", "/", HOST, None),
        ("GET", "/api/index/healthz", HOST, None), ("GET", "/healthz", {"host": "evil.example.com"}, None),
    ]
    late = [("POST", "/healthz", STD, {"x": 1}), ("OPTIONS", "/mcp", HOST, None), ("POST", "/mcp", STD, LIST)]

    async def run(app, todo, light=None):
        out = [await _raw(app, m, p, h, json.dumps(b).encode() if b is not None else b"") for m, p, h, b in todo]
        loaded = light.sdk is not None if light else None
        return out, loaded

    async def go():
        vercel = _vercel(con)
        cheap, loaded_cheap = await run(vercel, calls, vercel.light)
        rest, loaded_rest = await run(vercel, late, vercel.light)
        vercel.light.shutdown()
        local = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.vercel.app"], allowed_origins=[])
        wrapped = LifespanOnDemand(local, _inner(local))
        ref, _ = await run(wrapped, calls + late)
        wrapped._task.cancel()
        return cheap + rest, ref, loaded_cheap, loaded_rest
    got, ref, loaded_cheap, loaded_rest = asyncio.run(go())
    assert not loaded_cheap and loaded_rest
    for (m, p, h, _), (gs, gh, gb), (rs, rh, rb) in zip(calls + late, got, ref):
        assert gs == rs and gb == rb, (m, p, gs, rs, gb[:200], rb[:200])
        assert gh.get(b"content-type") == rh.get(b"content-type"), (m, p)


def test_lifespan_does_not_load_sdk(con):
    app = _vercel(con)
    msgs = iter([{"type": "lifespan.startup"}, {"type": "lifespan.shutdown"}])
    sent = []

    async def receive():
        return next(msgs)

    async def send(m):
        sent.append(m["type"])
    asyncio.run(app({"type": "lifespan"}, receive, send))
    assert sent == ["lifespan.startup.complete", "lifespan.shutdown.complete"] and app.light.sdk is None


def test_tool_call_through_vercel_app(con):
    async def go():
        app = _vercel(con)
        call = {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                "params": {"name": "find_products", "arguments": {"ingredient": "brašno", "city": "Osijek"}}}
        out = await _raw(app, "POST", "/mcp", STD, json.dumps(call).encode())
        app.light.shutdown()
        return out
    status, _, body = asyncio.run(go())
    res = json.loads(body)["result"]
    assert status == 200 and not res.get("isError")
    assert json.loads(res["content"][0]["text"])["results"]


def test_cold_process_cheap_requests_without_sdk_or_db(tmp_path):
    """Novi proces kao na Vercelu (api/index.py): jeftini zahtjevi i /healthz ne uvoze duckdb, MCP SDK ni
    mealmeter.server i ne otvaraju bazu; datum je iz metapodataka (baza ovdje ni ne postoji)."""
    db = tmp_path / "compact.duckdb"
    meta = {"build_id": "b-test", "date": "2026-11-18", "date_hr": "18.11.2026.", "updated": None,
            "loaded_at": "2026-11-18T03:20:59+00:00"}
    web.meta_path(db).write_text(json.dumps(meta), encoding="utf-8")
    code = f"""
import asyncio, json, sys, importlib.util
async def _raw(app, method, path, headers, body):  # kao tests.test_step5v._raw, bez uvoza testova (duckdb)
    sent, done = [], False
    async def receive():
        nonlocal done
        if done:
            await asyncio.sleep(3600)
        done = True
        return {{"type": "http.request", "body": body, "more_body": False}}
    async def send(m):
        sent.append(m)
    hdrs = [(k.encode(), v.encode()) for k, v in headers.items()] + [(b"content-length", str(len(body)).encode())]
    await app({{"type": "http", "method": method, "path": path, "raw_path": path.encode(), "query_string": b"",
               "headers": hdrs, "client": ("10.0.0.1", 1), "server": ("x", 443), "scheme": "https",
               "http_version": "1.1", "root_path": ""}}, receive, send)
    start = next(m for m in sent if m["type"] == "http.response.start")
    return start["status"], None, b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
spec = importlib.util.spec_from_file_location("vi", {str(ROOT / "api" / "index.py")!r})
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
H = {{"host": "x.vercel.app", "content-type": "application/json", "accept": "application/json, text/event-stream"}}
INIT = {json.dumps(INIT)!r}
async def go():
    out = []
    for m, p, b in [("POST", "/mcp", INIT), ("POST", "/mcp", '{{"jsonrpc":"2.0","method":"notifications/initialized"}}'),
                    ("POST", "/mcp", '{{"jsonrpc":"2.0","id":2,"method":"tools/list"}}'), ("GET", "/mcp", ""),
                    ("GET", "/.well-known/oauth-protected-resource", ""), ("GET", "/healthz", ""), ("GET", "/", "")]:
        s, h, body = await _raw(mod.app, m, p, H, b.encode())
        out.append([s, body.decode()])
    return out
out = asyncio.run(go())
print(json.dumps({{"out": out, "mods": [m for m in ("duckdb", "mcp", "pydantic", "starlette", "mealmeter.server",
                                                   "mealmeter.search", "mealmeter.basket") if m in sys.modules]}}))
"""
    env = {**os.environ, "MM_DB": str(db), "PYTHONPATH": str(ROOT / "src")}
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=ROOT, timeout=60)
    assert p.returncode == 0, p.stderr[-2000:]
    res = json.loads(p.stdout.strip().splitlines()[-1])
    assert res["mods"] == [], res["mods"]
    statuses = [s for s, _ in res["out"]]
    assert statuses == [200, 202, 200, 405, 404, 200, 200], statuses
    assert len(json.loads(res["out"][2][1])["result"]["tools"]) == 6
    health = json.loads(res["out"][5][1])
    assert health["db_date"] == "2026-11-18" and health["status"] in ("ok", "stale")
    assert "Učitani cjenik: 2026-11-18" in res["out"][6][1]
    # zapis zahtjeva: cpu_ms, prvi zahtjev instance cold=1
    lines = [ln for ln in p.stderr.splitlines() if ln.startswith("http ")]
    assert len(lines) == 7 and all(" cpu_ms=" in ln for ln in lines), p.stderr[-2000:]
    assert " cold=1 boot_cpu_ms=" in lines[0] and not any("cold=" in ln for ln in lines[1:])


# --- metapodaci sažete baze ----------------------------------------------------------------------------------

def test_build_writes_meta(carried):  # noqa: F811
    full, compact, _, _ = carried
    meta = json.loads(web.meta_path(compact).read_text(encoding="utf-8"))
    main = duckdb.connect(str(full), read_only=True)
    d = main.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    main.close()
    c = duckdb.connect(str(compact), read_only=True)
    build_id = c.execute("SELECT build_id FROM clean.compact_build").fetchone()[0]
    c.close()
    assert meta["build_id"] == build_id and meta["date"] == d.isoformat() and meta["date_hr"] == "19.10.2026."
    assert set(meta) == {"build_id", "date", "date_hr", "updated", "loaded_at"}  # fixture nema archive_info


@pytest.fixture
def server_state():
    saved = srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key, dict(srv._date_cache)
    rejected = set(web._meta_rejected)
    yield
    srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key = saved[:4]
    srv._date_cache.clear()
    srv._date_cache.update(saved[4])
    web._meta_rejected.clear()
    web._meta_rejected.update(rejected)
    srv._local.__dict__.clear()


def test_meta_used_without_opening_db(carried, server_state, monkeypatch):  # noqa: F811
    """/healthz, GET /, convert_units i list_staples: datum iz metapodataka, baza se ne otvara."""
    _, compact, _, _ = carried
    srv.create_server(db_path=str(compact))

    def no_db():
        raise AssertionError("baza se ne smije otvarati")
    monkeypatch.setattr(srv, "_con", no_db)
    status, h = web.health()
    assert status == 200 and h["db_date"] == "2026-10-19"
    assert "Učitani cjenik: 2026-10-19" in web.home("x.vercel.app")
    assert srv.list_staples()["date_hr"] == "19.10.2026."
    assert srv.convert_units(2, "žlica", "šećer")["date"] == "2026-10-19"


def test_meta_primes_date_and_tools_unchanged(carried, server_state):  # noqa: F811
    """Otvaranje baze iste izgradnje uzima datum iz metapodataka; izlazi alata su isti kao bez metapodataka."""
    _, compact, _, _ = carried
    srv.create_server(db_path=str(compact))
    con = srv._con()
    assert srv._date_cache["owner"] is srv._shared_con and srv._date_cache["value"]["date"] == "2026-10-19"
    with_meta = (srv.find_products(ingredient="brašno", city="Osijek"), srv.get_prices("jaja:m", city="Osijek"),
                 srv.plan_basket([{"name": "brašno glatko", "amount": 250, "unit": "g"}], "Osijek"))
    srv._date_cache.update(owner=None, value=None)
    assert srv._price_list_date(con)["date"] == "2026-10-19"  # max(date) iz baze
    without = (srv.find_products(ingredient="brašno", city="Osijek"), srv.get_prices("jaja:m", city="Osijek"),
               srv.plan_basket([{"name": "brašno glatko", "amount": 250, "unit": "g"}], "Osijek"))
    assert with_meta == without


def test_meta_from_other_build_is_rejected(carried, tmp_path, server_state, caplog):  # noqa: F811
    """Metapodaci druge izgradnje (npr. prekinut build): odbačeni pri otvaranju baze, datum iz baze; prije
    otvaranja ih /healthz još koristi."""
    import shutil

    _, compact, _, _ = carried
    for f in (compact, srv.search.prices_part(compact)):
        shutil.copy(f, tmp_path / f.name)
    db = tmp_path / compact.name
    web.meta_path(db).write_text(json.dumps({"build_id": "druga", "date": "2000-01-01", "date_hr": "1.1.2000.",
                                             "updated": None, "loaded_at": None}), encoding="utf-8")
    srv.create_server(db_path=str(db))
    assert web.health()[1]["db_date"] == "2000-01-01"
    caplog.set_level(logging.WARNING)
    srv._con()
    assert "compact_meta" in caplog.text and srv._date_cache["owner"] is not srv._shared_con
    assert web.health()[1]["db_date"] == "2026-10-19" and srv.list_staples()["date"] == "2026-10-19"


def test_compact_mismatch_still_checked_on_first_open(carried, tmp_path, server_state):  # noqa: F811
    """CompactMismatch (Korak 12) ostaje: bez datoteke cijena prvo otvaranje baze pada, i uz metapodatke."""
    import shutil

    _, compact, _, _ = carried
    shutil.copy(compact, tmp_path / compact.name)
    shutil.copy(web.meta_path(compact), web.meta_path(tmp_path / compact.name))
    srv.create_server(db_path=str(tmp_path / compact.name))
    assert web.health()[0] == 200  # metapodaci: bez otvaranja baze
    with pytest.raises(srv.search.CompactMismatch):
        srv._con()


# --- ostalo --------------------------------------------------------------------------------------------------

def test_libyaml_loader_same_as_safe_load():
    files = sorted(glob.glob(str(ROOT / "data" / "*.yaml"))) + [str(ROOT / "src" / "mealmeter" / "staples.yaml")]
    assert len(files) >= 9
    for f in files:
        assert load_yaml(f) == yaml.safe_load(Path(f).read_text(encoding="utf-8")), f


def test_staple_regexes_compile(tmp_path):
    """Provjera regexa namirnica (prije u load_staples, sad staples.check_regexes) i dalje hvata neispravan uzorak."""
    from mealmeter.staples import check_regexes, load_staples

    check_regexes(load_staples(include_disabled=True))
    bad = tmp_path / "staples.yaml"
    bad.write_text("brasno:\n  unit: kg\n  must_match: ['brasn(']\n", encoding="utf-8")
    with pytest.raises(ValueError, match="brasno: regex"):
        check_regexes(load_staples(bad))


def test_tool_log_has_cpu_ms(con, caplog):
    srv.create_server(con=con)
    caplog.set_level(logging.INFO, logger="mealmeter")
    srv._as_result(srv.list_staples)()
    assert any("tool=list_staples status=ok" in r.getMessage() and " cpu_ms=" in r.getMessage()
               for r in caplog.records)


def test_vercel_files_and_threads():
    cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    assert "data/compact_meta.json" in cfg["functions"]["api/index.py"]["includeFiles"]
    src = (ROOT / "api" / "index.py").read_text(encoding="utf-8")
    assert 'os.environ.setdefault("MM_DUCKDB_THREADS", "1")' in src and "VercelApp(" in src
    assert "from mealmeter.server" not in src.split("def _sdk")[0]  # SDK se ne uvozi pri pokretanju
