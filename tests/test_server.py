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
                 "zaliha", "stock", "izmišljaj"):
        assert word in instructions, word


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
