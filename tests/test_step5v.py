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
    for excluded in ("data/mealmeter.duckdb", "data/raw/**", "tests/**", "docs/**", ".env*", ".pytest_cache/**"):
        assert excluded in fn["excludeFiles"]
    assert cfg["rewrites"] == [{"source": "/(.*)", "destination": "/api/index"}]
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
    assert "nedostaje lanac" in runs and "exit 3" in runs  # pad lanca > 20 % prekida deploy
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
