"""Korak 21: MCP 2026-07-28 (moderna era, bez handshakea). server/discover, tools/list i prazni popisi iz snimke bez
SDK-a; subscriptions/listen odmah -32601 Method not found (HTTP 404), bez otvorenog SSE toka; discover ne najavljuje
pretpregledavanje promjena (tools.listChanged = false)."""

import asyncio
import json
import logging
import time

from mealmeter import server as srv
from mealmeter import web
from tests.test_step5a import _inner
from tests.test_step18_cpu import STD

PV = "2026-07-28"
META = {"io.modelcontextprotocol/protocolVersion": PV, "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {"name": "claude-ai", "version": "0.1.0"}}
# sposobnosti kakve šalje klijent s podrškom za proširenja i elicitaciju
CAPS = {"roots": {"listChanged": True}, "elicitation": {"form": {}, "url": {}},
        "extensions": {"io.modelcontextprotocol/ui": {"mimeTypes": ["text/html;profile=mcp-app"]}}}
LISTEN = {"toolsListChanged": True, "promptsListChanged": True, "resourcesListChanged": True}


def _h(method, **extra):
    return {**STD, "mcp-protocol-version": PV, "mcp-method": method, **extra}


def _m(method, rid=1, meta=None, **params):
    return {"jsonrpc": "2.0", "id": rid, "method": method, "params": {**params, "_meta": META if meta is None else meta}}


def _meta(**kw):
    out = dict(META)
    for k, v in kw.items():
        key = {"caps": "io.modelcontextprotocol/clientCapabilities", "info": "io.modelcontextprotocol/clientInfo",
               "pv": "io.modelcontextprotocol/protocolVersion", "log": "io.modelcontextprotocol/logLevel"}.get(k, k)
        if v is None:
            out.pop(key, None)
        else:
            out[key] = v
    return out


NOTIF = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {"_meta": META}}
ACCEPT_JSON = {"accept": "application/json"}

# (opis, zaglavlja, tijelo, treba li brzi put odgovoriti)
CASES = [
    *[(m, _h(m), _m(m), True) for m in srv.MODERN_RESULTS],
    *[(f"{m} not found", _h(m), _m(m, **srv.MODERN_PARAMS.get(m, {})), True) for m in srv.MODERN_NOT_FOUND],
    ("discover string id", _h("server/discover"), _m("server/discover", rid="server-discover-probe-1"), True),
    ("discover bez clientInfo", _h("server/discover"), _m("server/discover", meta=_meta(info=None)), True),
    ("discover sposobnosti", _h("server/discover"), _m("server/discover", meta=_meta(caps=CAPS)), True),
    ("discover clientInfo title", _h("server/discover"),
     _m("server/discover", meta=_meta(info={"name": "c", "version": "1", "title": "C"})), True),
    ("discover progressToken", _h("server/discover"), _m("server/discover", meta=_meta(progressToken=5)), True),
    ("discover tuđi _meta ključ", _h("server/discover"),
     _m("server/discover", meta=_meta(**{"com.example/trace": {"a": 1}})), True),
    ("discover mcp-name", _h("server/discover", **{"mcp-name": "x"}), _m("server/discover"), True),
    ("discover accept json", _h("server/discover", **ACCEPT_JSON), _m("server/discover"), True),
    ("discover accept */*", _h("server/discover", accept="*/*"), _m("server/discover"), True),
    ("tools/list sesija", _h("tools/list", **{"mcp-session-id": "abc"}), _m("tools/list"), True),
    ("listen prazan filtar", _h("subscriptions/listen"), _m("subscriptions/listen", notifications={}), True),
    ("listen sve", _h("subscriptions/listen"), _m("subscriptions/listen", notifications=LISTEN), True),
    ("listen resursi", _h("subscriptions/listen"),
     _m("subscriptions/listen", rid="listen:0", notifications={**LISTEN, "resourceSubscriptions": ["x://y"]}), True),
    ("listen sposobnosti", _h("subscriptions/listen"),
     _m("subscriptions/listen", rid="listen:1", meta=_meta(caps=CAPS), notifications=LISTEN), True),
    ("ping s parametrima", _h("ping"), _m("ping"), True),
    ("notifikacija", _h("notifications/initialized"), NOTIF, True),
    ("notifikacija bez params", _h("notifications/cancelled"),
     {"jsonrpc": "2.0", "method": "notifications/cancelled"}, True),
    # SDK-u (greške ili drukčija provjera)
    ("listen bez filtra", _h("subscriptions/listen"), _m("subscriptions/listen"), False),
    ("listen filtar nije bool", _h("subscriptions/listen"),
     _m("subscriptions/listen", notifications={"toolsListChanged": "da"}), False),
    ("listen accept json", _h("subscriptions/listen", **ACCEPT_JSON),
     _m("subscriptions/listen", notifications=LISTEN), False),
    ("discover bez mcp-method", {k: v for k, v in _h("server/discover").items() if k != "mcp-method"},
     _m("server/discover"), False),
    ("discover krivi mcp-method", _h("tools/list"), _m("server/discover"), False),
    ("discover verzija u tijelu", _h("server/discover"), _m("server/discover", meta=_meta(pv="2025-11-25")), False),
    ("discover bez _meta", _h("server/discover"), {"jsonrpc": "2.0", "id": 1, "method": "server/discover"}, False),
    ("discover bez sposobnosti", _h("server/discover"), _m("server/discover", meta=_meta(caps=None)), False),
    ("discover logLevel", _h("server/discover"), _m("server/discover", meta=_meta(log="info")), False),
    ("discover clientInfo bez verzije", _h("server/discover"),
     _m("server/discover", meta=_meta(info={"name": "c"})), False),
    ("tools/list cursor", _h("tools/list"), _m("tools/list", cursor="x"), False),
    ("tools/call", _h("tools/call", **{"mcp-name": "list_staples"}), _m("tools/call", name="list_staples"), False),
    ("odgovor klijenta", _h("server/discover"), {"jsonrpc": "2.0", "id": 1, "result": {}}, False),
    ("nepoznata verzija", {**_h("server/discover"), "mcp-protocol-version": "2027-01-01"},
     _m("server/discover", meta=_meta(pv="2027-01-01")), False),
]


async def _raw(app, headers, body: bytes, extra_headers: list | None = None):
    """POST /mcp; klijent ne odlazi (SSE put SDK-a bi inače prekinuo obradu)."""
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
    await asyncio.wait_for(app({"type": "http", "method": "POST", "path": "/mcp", "raw_path": b"/mcp",
                                "query_string": b"", "headers": hdrs + (extra_headers or []),
                                "client": ("10.0.0.1", 1), "server": ("x", 443), "scheme": "https",
                                "http_version": "1.1", "root_path": ""}, receive, send), 10)
    start = next(m for m in sent if m["type"] == "http.response.start")
    return start["status"], dict(start["headers"]), b"".join(m.get("body", b"") for m in sent
                                                              if m["type"] == "http.response.body")


def _sdk_replies(con, cases):
    app = srv.http_app(srv.create_server(con=con), allowed_hosts=["*.vercel.app"], allowed_origins=[])

    async def go():
        inner = _inner(app)
        async with inner.router.lifespan_context(inner):
            return [await _raw(app, h, json.dumps(b).encode()) for _, h, b, _ in cases]
    return asyncio.run(go())


def test_snapshot_is_current():
    """mcp_static.json je jednak trenutnom SDK-u (python -m mealmeter.server --write-static)."""
    assert web.static_mcp() == json.loads(json.dumps(srv.static_snapshot(), ensure_ascii=False))


def test_discover_announces_no_subscriptions():
    """server/discover: samo alati, bez listChanged (nema pretplata ni obavijesti); listen nije poslužen."""
    modern = web.static_mcp()["modern"][PV]
    disc = modern["results"]["server/discover"]
    assert disc["capabilities"] == {"tools": {"listChanged": False}}
    assert disc["supportedVersions"] == [PV] and disc["instructions"] == srv.INSTRUCTIONS
    assert disc["_meta"]["io.modelcontextprotocol/serverInfo"]["name"] == "mealmeter"
    assert modern["errors"]["subscriptions/listen"] == [404, {"code": -32601, "message": "Method not found",
                                                              "data": "subscriptions/listen"}]
    assert "subscriptions/listen" not in srv.create_server()._lowlevel_server._request_handlers


def test_modern_fast_reply_matches_sdk_byte_for_byte(con):
    """Oblici moderne ere: status, zaglavlja i tijelo bajt po bajt kao SDK; ostali idu SDK-u (s razlogom why)."""
    sdk = _sdk_replies(con, CASES)
    for (name, headers, body, fast), (status, sdk_headers, sdk_body) in zip(CASES, sdk):
        hdrs = {k.encode(): v.encode() for k, v in headers.items()}
        why: dict = {}
        reply = web.fast_reply(hdrs, json.dumps(body).encode(), why)
        assert (reply is not None) == fast, (name, why, status, sdk_body[:200])
        if reply:
            st, rh, rb = reply
            assert st == status and rb == sdk_body, (name, st, status, rb[:300], sdk_body[:300])
            assert dict(rh) == {k: v for k, v in sdk_headers.items() if k in (b"content-type", b"content-length")}, name
            assert set(sdk_headers) <= {b"content-type", b"content-length"}, (name, sdk_headers)
        elif name not in ("tools/call",):
            assert why.get("why"), name


def test_duplicate_routing_header_goes_to_sdk(con):
    """Ponovljeno MCP-Protocol-Version ili Mcp-Method: SDK odbija (HEADER_MISMATCH), brzi put ne odgovara."""
    h = _h("server/discover")
    for dup in ([(b"mcp-method", b"server/discover")], [(b"mcp-protocol-version", PV.encode())]):
        pairs = [(k.encode(), v.encode()) for k, v in h.items()] + dup
        why: dict = {}
        assert web.fast_reply(pairs, json.dumps(_m("server/discover")).encode(), why) is None
        assert why["why"] == "dup_header"


def _vercel(con, **kw):
    return web.VercelApp(lambda: srv.sdk_app(srv.create_server(con=con), host="0.0.0.0"),
                         allowed_hosts=["*.vercel.app"], allowed_origins=[], **kw)


def _http_lines(caplog):
    return [r.getMessage() for r in caplog.records if r.getMessage().startswith("http ")]


def test_claude_modern_sequence(con, caplog):
    """Niz kakav sada šalje Claude (server/discover, tools/list, subscriptions/listen, tools/call): sve osim
    tools/call bez SDK-a i odmah; listen 404 -32601 kao JSON, bez SSE toka."""
    caplog.set_level(logging.INFO, logger="mealmeter")
    seq = [("server/discover", _m("server/discover", rid="server-discover-probe-1")),
           ("notifications/initialized", NOTIF),
           ("tools/list", _m("tools/list", rid=0)),
           ("subscriptions/listen", _m("subscriptions/listen", rid="listen:0", notifications=LISTEN)),
           ("subscriptions/listen", _m("subscriptions/listen", rid="listen:1", meta=_meta(caps=CAPS),
                                       notifications={"toolsListChanged": True})),
           ("prompts/list", _m("prompts/list", rid=2)),
           ("ping", _m("ping", rid=3))]
    call = ("tools/call", _m("tools/call", rid=5, name="list_staples", arguments={}))

    async def go():
        app = _vercel(con, request_timeout=5)
        out = []
        for method, body in seq:
            t0 = time.perf_counter()
            out.append((*await _raw(app, _h(method), json.dumps(body).encode()), time.perf_counter() - t0))
        loaded_before = app.light.sdk is not None
        out.append((*await _raw(app, _h("tools/call", **{"mcp-name": "list_staples"}), json.dumps(call[1]).encode()),
                    0.0))
        loaded_after = app.light.sdk is not None
        app.light.shutdown()
        return out, loaded_before, loaded_after
    out, before, after = asyncio.run(go())
    assert [s for s, _, _, _ in out] == [200, 202, 200, 404, 404, 200, 404, 200]
    assert not before and after
    assert all(dt < 0.5 for *_, dt in out[:-1]), [dt for *_, dt in out]
    for status, headers, body, _ in out[3:5]:
        assert headers[b"content-type"] == b"application/json"
        assert json.loads(body)["error"]["code"] == -32601
    assert json.loads(out[3][2])["id"] == "listen:0"
    res = json.loads(out[-1][2])["result"]
    assert res["content"] and not res.get("isError")
    lines = _http_lines(caplog)
    assert len(lines) == 8
    for line, (method, _) in zip(lines, [*seq, call]):
        assert f" rpc={method} " in line, line
        assert (" path=sdk" in line) == (method == "tools/call"), line
        assert "timeout=1" not in line and "why=" not in line, line


def test_modern_sdk_path_logs_reason(con, caplog):
    """Zahtjev moderne ere koji ide SDK-u ima why= u zapisu (npr. logLevel u _meta)."""
    caplog.set_level(logging.INFO, logger="mealmeter")

    async def go():
        app = _vercel(con)
        r = await _raw(app, _h("server/discover"), json.dumps(_m("server/discover", meta=_meta(log="info"))).encode())
        app.light.shutdown()
        return r
    status, _, body = asyncio.run(go())
    assert status == 200 and "result" in json.loads(body)
    (line,) = _http_lines(caplog)
    assert " rpc=server/discover " in line and " path=sdk" in line and " why=meta_key" in line, line


def test_failed_build_removes_duckdb_spill_dir(tmp_path, monkeypatch):
    """update.build_database: nakon neuspjele izgradnje briše i DuckDB-ovu mapu za prelijevanje (<tmp>.tmp/)."""
    import pytest

    from mealmeter import update

    db = tmp_path / "mealmeter.duckdb"
    spill = tmp_path / "mealmeter.duckdb.tmp-2026-11-21.tmp"

    def boom(con, *a, **k):
        spill.mkdir()
        (spill / "duckdb_temp_storage-0.tmp").write_bytes(b"x" * 10)
        raise MemoryError("OOM")
    monkeypatch.setattr(update, "load_raw", boom)
    with pytest.raises(MemoryError):
        update.build_database(tmp_path, "2026-11-21", db)
    assert not spill.exists() and not (tmp_path / "mealmeter.duckdb.tmp-2026-11-21").exists()
