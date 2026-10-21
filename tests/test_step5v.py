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
