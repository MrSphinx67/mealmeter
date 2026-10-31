"""Korak 5V: Vercel omotač (api/index.py) bez i sa ASGI lifespanom."""

import asyncio
import json
from pathlib import Path

from tests.test_step5a import INIT, _inner, _request

ROOT = Path(__file__).resolve().parents[1]


def _wrapper_class():
    from mealmeter.asgi import LifespanOnDemand

    return LifespanOnDemand


def test_wrapper_without_lifespan(con):
    from mealmeter import server as srv

    Wrapper = _wrapper_class()
    http = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.vercel.app"], allowed_origins=[])
    app = Wrapper(http, _inner(http))
    starts = []
    orig = app.start

    async def counting_start():
        starts.append(1)
        await orig()
    app.start = counting_start

    async def go():
        # dva istodobna prva zahtjeva, bez lifespan poruka platforme
        a, b = await asyncio.gather(_request(app, "POST", "/mcp", "x.vercel.app", INIT),
                                    _request(app, "GET", "/healthz", "x.vercel.app"))
        listing = await _request(app, "POST", "/mcp", "x.vercel.app", {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        rewritten = await _request(app, "GET", "/api/index/healthz", "x.vercel.app")
        app._task.cancel()
        return a, b, listing, rewritten
    a, b, listing, rewritten = asyncio.run(go())
    assert a[0] == 200 and json.loads(a[1])["result"]["serverInfo"]["name"] == "mealmeter"
    assert b[0] == 200 and json.loads(b[1])["status"] in ("ok", "stale")
    assert listing[0] == 200 and len(json.loads(listing[1])["result"]["tools"]) == 6
    assert rewritten[0] == 200 and app._ready


def test_wrapper_lifespan_protocol(con):
    from mealmeter import server as srv

    Wrapper = _wrapper_class()
    http = srv.http_app(srv.create_server(con=con))
    app = Wrapper(http, _inner(http))
    sent = []
    msgs = iter([{"type": "lifespan.startup"}, {"type": "lifespan.shutdown"}])

    async def receive():
        return next(msgs)

    async def send(m):
        sent.append(m["type"])
    asyncio.run(app({"type": "lifespan"}, receive, send))
    assert sent == ["lifespan.startup.complete", "lifespan.shutdown.complete"]


def test_index_defaults():
    src = (ROOT / "api" / "index.py").read_text(encoding="utf-8")
    assert 'os.environ.setdefault("MM_DB", str(ROOT / "data" / "compact.duckdb"))' in src
    assert 'os.environ.setdefault("MM_DUCKDB_TEMP", "/tmp")' in src and "\napp = " in src


def test_vercel_config():
    cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    fn = cfg["functions"]["api/index.py"]
    assert "data/compact.duckdb" in fn["includeFiles"] and "data/*.yaml" in fn["includeFiles"]
    assert "data/compact_prices.duckdb" in fn["includeFiles"]  # Korak 12: datoteka cijena sažete baze
    for excluded in ("data/mealmeter.duckdb", "data/raw/**", "tests/**", "docs/**", ".env*", ".pytest_cache/**"):
        assert excluded in fn["excludeFiles"]
    # Korak 5V3: bez rewritea; Python backend dobiva sve putanje s izvornom putanjom (rewrite je slao /api/index)
    assert "rewrites" not in cfg and "routes" not in cfg
    assert cfg["git"] == {"deploymentEnabled": False}  # baza nije u Gitu: deploy samo preko CLI-ja / workflowa
    ignore = (ROOT / ".vercelignore").read_text(encoding="utf-8").splitlines()
    assert "data/mealmeter.duckdb" in ignore and not any("compact" in line and not line.startswith("#")
                                                          for line in ignore if "compact_tmp" not in line)


def test_update_workflow():
    import yaml

    text = (ROOT / ".github" / "workflows" / "update.yml").read_text(encoding="utf-8")
    wf = yaml.safe_load(text)
    on = wf[True] if True in wf else wf["on"]  # PyYAML čita ključ "on" kao True
    assert len(on["schedule"]) == 1 and len(on["schedule"][0]["cron"].split()[1].split(",")) == 2  # 2x dnevno
    runs = "\n".join(s.get("run", "") for s in wf["jobs"]["update"]["steps"])
    order = ["scripts/update.py", "scripts/build_compact.py", "golden.py --check", "vercel build",
             "vercel deploy --prebuilt --prod"]
    assert [runs.index(x) for x in order] == sorted(runs.index(x) for x in order)
    for secret in ("VERCEL_TOKEN", "VERCEL_ORG_ID", "VERCEL_PROJECT_ID"):
        assert f"secrets.{secret}" in text
    assert "git commit" not in text and "git push" not in text  # baza se ne commita
    # Korak 8: deploy prekida samo izlazni kod update.py (pipefail), a ne grep po upozorenjima lanaca
    assert "pipefail" in runs and "nedostaje lanac" not in runs and "exit 3" not in runs
    assert "vercel_bundle_size.py --max-mb 220 --max-file-mb 95" in runs  # stvarna veličina paketa (5V2), ne du na .vercel/output


def test_vercel_client_ip(monkeypatch):
    from mealmeter.server import RateLimit

    monkeypatch.setenv("TRUSTED_PROXY", "vercel")
    rl = RateLimit(None, limit=2, session_limit=100, global_limit=100)
    assert rl.trusted_proxy == "vercel"
    scope = {"client": ("10.0.0.1", 1)}
    # klijent pošalje lažni CF-Connecting-IP: na Vercelu se ne čita
    assert rl.client_ip(scope, {b"cf-connecting-ip": b"1.1.1.1", b"x-vercel-forwarded-for": b"203.0.113.5",
                                b"x-forwarded-for": b"203.0.113.5"}) == "203.0.113.5"
    assert rl.client_ip(scope, {b"x-real-ip": b"203.0.113.6"}) == "203.0.113.6"
    assert rl.client_ip(scope, {b"x-forwarded-for": b"203.0.113.7"}) == "203.0.113.7"
    assert rl.client_ip(scope, {}) == "10.0.0.1"
    monkeypatch.setenv("TRUSTED_PROXY", "1")
    assert RateLimit(None).trusted_proxy is True
    monkeypatch.delenv("TRUSTED_PROXY")
    assert RateLimit(None).trusted_proxy is False


def test_index_vercel_settings():
    src = (ROOT / "api" / "index.py").read_text(encoding="utf-8")
    for line in ('"MM_ALLOWED_HOSTS", "*.vercel.app"', '"TRUSTED_PROXY", "vercel"', '"MM_RATE_IP", "60"',
                 '"MM_RATE_GLOBAL", "600"', '"MM_ALLOWED_ORIGINS"'):
        assert line in src, line


def test_bundle_size_script(tmp_path):
    """scripts/vercel_bundle_size.py: zbraja filePathMap i pada na datoteci većoj od --max-file-mb."""
    import subprocess
    import sys

    func = tmp_path / "functions" / "python.func"
    func.mkdir(parents=True)
    big, small = tmp_path / "big.bin", tmp_path / "small.bin"
    big.write_bytes(b"\0" * (3 * 2**20))
    small.write_bytes(b"\0" * (1 * 2**20))
    (func / ".vc-config.json").write_text(json.dumps({"filePathMap": {"data/compact.duckdb": str(big),
                                                                      "_vendor/x.so": str(small)}}))
    script = str(ROOT / "scripts" / "vercel_bundle_size.py")

    def run(*args):
        return subprocess.run([sys.executable, script, "--root", str(tmp_path / "functions"), *args],
                              capture_output=True, text=True)
    ok = run("--max-mb", "10", "--max-file-mb", "5")
    assert ok.returncode == 0 and "python.func: 4.0 MB" in ok.stdout and "data/compact.duckdb" in ok.stdout
    too_big_file = run("--max-mb", "10", "--max-file-mb", "2")
    assert too_big_file.returncode == 1 and "data/compact.duckdb ima 3.0 MB" in too_big_file.stdout
    assert run("--max-mb", "3.5", "--max-file-mb", "5").returncode == 1


# --- Korak 5V3: putanje i metode kroz Vercel omotač ---------------------------------------------------------

def test_routes_and_methods(con):
    from mealmeter import server as srv
    from mealmeter.asgi import LifespanOnDemand

    http = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.vercel.app"], allowed_origins=[])
    app = LifespanOnDemand(http, _inner(http))
    host = "mealmeter.vercel.app"
    calls = [
        ("POST", "/mcp", INIT),  # izvorna putanja
        ("POST", "/api/index/mcp", INIT),  # prepisana putanja
        ("GET", "/mcp", None), ("DELETE", "/mcp", None), ("OPTIONS", "/mcp", None),
        ("GET", "/.well-known/oauth-protected-resource", None),
        ("GET", "/.well-known/oauth-protected-resource/mcp", None),
        ("GET", "/.well-known/oauth-authorization-server", None),
        ("POST", "/.well-known/oauth-authorization-server", {"x": 1}),
        ("GET", "/nepostoji", None),
        ("GET", "/healthz", None), ("GET", "/", None), ("POST", "/healthz", {"x": 1}),
    ]

    async def go():
        out = [await _request(app, m, p, host, b) for m, p, b in calls]
        app._task.cancel()
        return out
    res = dict(zip([f"{m} {p}" for m, p, _ in calls], asyncio.run(go())))
    for key in ("POST /mcp", "POST /api/index/mcp"):
        status, body = res[key]
        assert status == 200 and json.loads(body)["result"]["serverInfo"]["name"] == "mealmeter", key
    # GET/DELETE /mcp: 405 iz McpPostOnly (Korak 5V4); OPTIONS stiže do MCP aplikacije (405 iz SDK-a)
    for key in ("GET /mcp", "DELETE /mcp", "OPTIONS /mcp"):
        status, body = res[key]
        assert status == 405 and json.loads(body)["jsonrpc"] == "2.0", key
    # nepoznate putanje, uključujući OAuth .well-known: JSON 404 (konektor tako zna da nema prijave)
    for key in ("GET /.well-known/oauth-protected-resource", "GET /.well-known/oauth-protected-resource/mcp",
                "GET /.well-known/oauth-authorization-server", "POST /.well-known/oauth-authorization-server",
                "GET /nepostoji"):
        status, body = res[key]
        assert status == 404 and json.loads(body)["error"] == "not found", key
    assert res["GET /healthz"][0] == 200 and res["GET /"][0] == 200
    assert res["POST /healthz"][0] == 405 and json.loads(res["POST /healthz"][1])["error"] == "method not allowed"


# --- Korak 5V4: GET i DELETE /mcp → 405 odmah (bez SSE toka) -----------------------------------------------

async def _raw(app, method, path, headers, body=b""):
    sent, done = [], False

    async def receive():
        nonlocal done
        if done:
            await asyncio.sleep(3600)
        done = True
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(m):
        sent.append(m)
    hdrs = [(k.encode(), v.encode()) for k, v in headers.items()] + [(b"content-length", str(len(body)).encode())]
    await app({"type": "http", "method": method, "path": path, "raw_path": path.encode(), "query_string": b"",
               "headers": hdrs, "client": ("10.0.0.1", 1), "server": ("x", 443), "scheme": "https",
               "http_version": "1.1", "root_path": ""}, receive, send)
    start = next(m for m in sent if m["type"] == "http.response.start")
    return start["status"], dict(start["headers"]), b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")


def test_mcp_get_delete_405_immediately(con):
    from mealmeter import server as srv
    from mealmeter.asgi import LifespanOnDemand

    def fresh():  # session manager smije se pokrenuti samo jednom po instanci
        return srv.http_app(srv.create_server(con=con), allowed_hosts=["*.vercel.app"], allowed_origins=[])
    host = {"host": "mealmeter.vercel.app"}
    accepts = [{}, {"accept": "text/event-stream"}, {"accept": "application/json, text/event-stream"}, {"accept": "*/*"}]

    async def go(app):
        out = []
        for method in ("GET", "DELETE", "HEAD"):
            for path in ("/mcp", "/mcp/"):
                for acc in accepts:
                    # odmah: bez SSE toka, inače bi wait_for istekao
                    out.append((method, path, acc, await asyncio.wait_for(_raw(app, method, path, {**host, **acc}), 2)))
        init = await asyncio.wait_for(_raw(app, "POST", "/mcp", {**host, "content-type": "application/json",
                                                                 "accept": "application/json, text/event-stream"},
                                           json.dumps(INIT).encode()), 10)
        return out, init

    local, vercel = fresh(), fresh()
    for label, app in (("lokalni HTTP", local), ("Vercel omotač", LifespanOnDemand(vercel, _inner(vercel)))):
        async def run(app=app):
            if isinstance(app, LifespanOnDemand):
                try:
                    return await go(app)
                finally:
                    app._task.cancel()
            inner = _inner(app)
            async with inner.router.lifespan_context(inner):
                return await go(app)
        out, init = asyncio.run(run())
        for method, path, acc, (status, headers, body) in out:
            assert status == 405 and headers[b"allow"] == b"POST", (label, method, path, acc)
            assert headers[b"content-type"] == b"application/json"
            if method != "HEAD":
                assert json.loads(body)["error"]["message"].startswith("Method not allowed")
        assert init[0] == 200 and json.loads(init[2])["result"]["serverInfo"]["name"] == "mealmeter", label
