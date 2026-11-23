"""Korak 19: bez učitavanja SDK-a za prompts/resources i notifikacije, metoda i put u zapisu zahtjeva, zahtjevi koji
vise (tijelo koje ne stiže, prekinuta veza, čuvar vremena)."""

import asyncio
import json
import logging
import socket
import threading
import time
from pathlib import Path

import pytest

from mealmeter import server as srv
from mealmeter import web
from tests.test_step5a import _inner
from tests.test_step5v import _raw
from tests.test_step18_cpu import NOTIF, STD, _init

ROOT = Path(__file__).resolve().parents[1]


def _req(method, rid=3, **params):
    return {"jsonrpc": "2.0", "id": rid, "method": method, **({"params": params} if params else {})}


V = {**STD, "mcp-protocol-version": "2025-06-18"}
SESSION = {**STD, "mcp-session-id": "abc"}

# (opis, zaglavlja, tijelo, treba li brzi put odgovoriti); uz CASES iz Koraka 18
CASES = [
    *[(m, V, _req(m), True) for m in srv.EMPTY_LIST_METHODS],
    *[(f"{m} bez verzije", STD, _req(m), True) for m in srv.EMPTY_LIST_METHODS],
    *[(f"{m} _meta", STD, _req(m, _meta={"progressToken": 1}), True) for m in srv.EMPTY_LIST_METHODS],
    ("prompts/list string id", STD, _req("prompts/list", rid="p-1"), True),
    ("prompts/list cursor", STD, _req("prompts/list", cursor="x"), False),
    ("prompts/list 2026-07-28", {**STD, "mcp-protocol-version": "2026-07-28"}, _req("prompts/list"), False),
    ("resources/read", STD, _req("resources/read", uri="x://y"), False),
    ("prompts/get", STD, _req("prompts/get", name="x"), False),
    ("tools/list sesija", SESSION, _req("tools/list"), True),
    ("initialize sesija", SESSION, _init("2025-06-18"), True),
    ("prompts/list sesija", SESSION, _req("prompts/list"), True),
    ("notifications/initialized sesija", SESSION, NOTIF, True),
    ("notifications/initialized dodatno polje", STD, {**NOTIF, "x": 1}, True),
    ("notifications/cancelled sesija", {**SESSION, "mcp-protocol-version": "2025-11-25"},
     {"jsonrpc": "2.0", "method": "notifications/cancelled", "params": {"requestId": 7, "reason": "x"}}, True),
    ("notifications/progress", V, {"jsonrpc": "2.0", "method": "notifications/progress",
                                   "params": {"progressToken": 1, "progress": 0.5}}, True),
    ("notifications/roots/list_changed", V, {"jsonrpc": "2.0", "method": "notifications/roots/list_changed"}, True),
    ("notifications nepoznata", STD, {"jsonrpc": "2.0", "method": "notifications/nesto"}, True),
    ("notifications params lista", STD, {**NOTIF, "params": [1]}, False),
    ("notifications 2026-07-28", {**STD, "mcp-protocol-version": "2026-07-28"}, NOTIF, True),  # Korak 21
    ("notifications bez accept", {k: v for k, v in STD.items() if k != "accept"}, NOTIF, False),
    ("notifications batch", STD, [NOTIF, NOTIF], False),
    ("odgovor klijenta result", STD, {"jsonrpc": "2.0", "id": 1, "result": {}}, True),
    ("odgovor klijenta error", STD, {"jsonrpc": "2.0", "id": "a", "error": {"code": 1, "message": "x"}}, True),
    ("odgovor bez id", STD, {"jsonrpc": "2.0", "result": {}}, False),
]


def test_initialize_announces_tools_only(con):
    """initialize najavljuje samo alate; prompts/list i resources/list SDK i dalje poslužuje (prazni popisi)."""
    snap = web.static_mcp()
    assert snap["initialize"]["capabilities"] == {"tools": {"listChanged": False}}
    assert snap["empty_lists"] == {"prompts/list": {"prompts": []}, "resources/list": {"resources": []},
                                   "resources/templates/list": {"resourceTemplates": []}}
    low = srv.create_server(con=con)._lowlevel_server
    caps = low.get_capabilities()
    assert caps.prompts is None and caps.resources is None and caps.tools is not None
    assert low.get_capabilities(protocol_version="2026-07-28").prompts is None  # i server/discover


def test_fast_reply_matches_sdk_byte_for_byte(con):
    """Novi oblici brzog puta: status, zaglavlja i tijelo bajt po bajt kao SDK; ostali idu SDK-u."""
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
            assert st == status and rb == sdk_body, (name, st, status, rb[:200], sdk_body[:200])
            assert dict(rh) == {k: v for k, v in sdk_headers.items() if k in (b"content-type", b"content-length")}, name
            assert set(sdk_headers) <= {b"content-type", b"content-length"}, name


def _vercel(con, **kw):
    return web.VercelApp(lambda: srv.sdk_app(srv.create_server(con=con), host="0.0.0.0"),
                         allowed_hosts=["*.vercel.app"], allowed_origins=[], **kw)


def _http_lines(caplog):
    return [r.getMessage() for r in caplog.records if r.getMessage().startswith("http ")]


def test_claude_sequence_loads_sdk_only_for_tools_call(con, caplog):
    """Niz kakav šalje Claude: sve do tools/call bez SDK-a; zapis ima rpc, id i path."""
    caplog.set_level(logging.INFO, logger="mealmeter")
    seq = [_init("2025-06-18", rid=0), NOTIF, _req("tools/list", rid=1), _req("prompts/list", rid=2),
           _req("resources/list", rid=3), _req("resources/templates/list", rid=4)]
    call = _req("tools/call", rid=5, name="list_staples", arguments={})

    async def go():
        app = _vercel(con)
        out = [await _raw(app, "POST", "/mcp", V, json.dumps(b).encode()) for b in seq]
        loaded_before = app.light.sdk is not None
        out.append(await _raw(app, "POST", "/mcp", V, json.dumps(call).encode()))
        out.append(await _raw(app, "GET", "/mcp", {"host": "x.vercel.app"}, b""))
        loaded_after = app.light.sdk is not None
        app.light.shutdown()
        return out, loaded_before, loaded_after
    out, before, after = asyncio.run(go())
    assert [s for s, _, _ in out] == [200, 202, 200, 200, 200, 200, 200, 405]
    assert not before and after
    lines = _http_lines(caplog)
    assert len(lines) == 8
    expect = [("initialize", "0", "fast"), ("notifications/initialized", "-", "fast"), ("tools/list", "1", "fast"),
              ("prompts/list", "2", "fast"), ("resources/list", "3", "fast"), ("resources/templates/list", "4", "fast"),
              ("tools/call", "5", "sdk")]
    for line, (rpc, rid, path) in zip(lines, expect):
        assert f" rpc={rpc} " in line and f" id={rid} " in line and f" path={path}" in line, line
    assert " name=list_staples " in lines[6]
    assert " path=fast" in lines[7] and "rpc=" not in lines[7]  # 405 bez SDK-a


def test_rpc_info_is_safe():
    assert web.rpc_info(b"nije json") == {"rpc": "invalid-json"}
    assert web.rpc_info(b"[1,2]") == {"rpc": "batch2"}
    info = web.rpc_info(json.dumps(_req("tools/call", rid="a b\nc", name="plan basket",
                                        arguments={"tajno": "x"})).encode())
    assert info["rpc"] == "tools/call" and info["id"] == "a_b_c" and info["name"] == "plan_basket"
    assert "tajno" not in json.dumps(info)
    assert web.rpc_info(b'{"jsonrpc":"2.0","id":1,"result":{}}')["rpc"] == "response"


async def _partial(app, chunks, end):
    """POST /mcp kojem tijelo stiže u dijelovima; `end`: "disconnect" ili "hang" (proxy više ništa ne šalje)."""
    sent, queue = [], list(chunks)

    async def receive():
        if queue:
            return {"type": "http.request", "body": queue.pop(0), "more_body": True}
        if end == "disconnect":
            return {"type": "http.disconnect"}
        await asyncio.sleep(3600)

    async def send(m):
        sent.append(m)
    hdrs = [(k.encode(), v.encode()) for k, v in STD.items()] + [(b"content-length", b"55")]
    await app({"type": "http", "method": "POST", "path": "/mcp", "raw_path": b"/mcp", "query_string": b"",
               "headers": hdrs, "client": ("10.0.0.1", 1), "server": ("x", 443), "scheme": "https",
               "http_version": "1.1", "root_path": ""}, receive, send)
    return sent


def test_client_disconnect_mid_body_does_not_load_sdk(con, caplog):
    caplog.set_level(logging.INFO, logger="mealmeter")

    async def go():
        app = _vercel(con)
        sent = await _partial(app, [b'{"jsonrpc":"2.0",'], "disconnect")
        return sent, app.light.sdk
    sent, sdk = asyncio.run(go())
    assert sent == [] and sdk is None
    line = _http_lines(caplog)[-1]
    assert " status=499 " in line and " path=fast" in line and " phase=disconnect body=17/55" in line, line


def test_body_that_never_arrives_gets_408(con, caplog):
    caplog.set_level(logging.INFO, logger="mealmeter")

    async def go():
        app = _vercel(con, body_timeout=0.2)
        t0 = time.perf_counter()
        sent = await _partial(app, [b'{"jsonrpc":"2.0",'], "hang")
        return sent, app.light.sdk, time.perf_counter() - t0
    sent, sdk, took = asyncio.run(go())
    assert sdk is None and took < 2
    assert sent[0]["status"] == 408 and json.loads(sent[1]["body"])["error"]["message"] == "request body timeout"
    line = _http_lines(caplog)[-1]
    assert " status=408 " in line and " phase=body_timeout body=17/55" in line, line


def test_request_timeout_logs_phase_and_answers_504(caplog):
    """Čuvar vremena (RequestLog timeout): zahtjev koji visi u SDK-u ili u tijelu prekida se, uz zapis faze."""
    caplog.set_level(logging.INFO, logger="mealmeter")

    from types import SimpleNamespace

    class Hang:  # SDK aplikacija koja nikad ne odgovori (LifespanOnDemand traži router.lifespan_context)
        async def __call__(self, scope, receive, send):
            await asyncio.sleep(3600)

    class Ctx:
        async def __aenter__(self):
            return None

        async def __aexit__(self, *a):
            return False
    Hang.router = SimpleNamespace(lifespan_context=lambda app: Ctx())
    hang = Hang()

    async def go():
        app = web.VercelApp(lambda: hang, allowed_hosts=["*.vercel.app"], allowed_origins=[], request_timeout=0.3)
        t0 = time.perf_counter()
        status, _, body = await _raw(app, "POST", "/mcp", STD, json.dumps(_req("tools/call", rid=9, name="x")).encode())
        took = time.perf_counter() - t0
        slow = web.VercelApp(lambda: hang, allowed_hosts=["*.vercel.app"], allowed_origins=[], request_timeout=0.3,
                             body_timeout=0)
        sent = await _partial(slow, [b"{"], "hang")
        return status, body, took, sent
    status, body, took, sent = asyncio.run(go())
    assert status == 504 and json.loads(body) == {"jsonrpc": "2.0", "id": 9,
                                                   "error": {"code": -32603, "message": "timeout"}}
    assert took < 2 and sent[0]["status"] == 504
    lines = _http_lines(caplog)
    assert " rpc=tools/call name=x id=9 path=sdk timeout=1 phase=sdk " in lines[-2], lines[-2]
    assert " timeout=1 phase=body body=1/55" in lines[-1], lines[-1]


def test_request_timeout_after_response_started(caplog):
    """Odgovor je počeo (npr. tok koji se ne zatvara): bez drugog http.response.start, zapis s timeout=1."""
    caplog.set_level(logging.INFO, logger="mealmeter")

    async def stream(scope, receive, send):
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"x", "more_body": True})
        await asyncio.sleep(3600)
    sent = []

    async def go():
        log_app = web.RequestLog(stream, timeout=0.2)

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(m):
            sent.append(m)
        await log_app({"type": "http", "method": "GET", "path": "/s", "headers": [], "client": ("1.2.3.4", 1)},
                      receive, send)
    asyncio.run(go())
    assert [m["type"] for m in sent] == ["http.response.start", "http.response.body"]
    assert " status=200 " in _http_lines(caplog)[-1] and " timeout=1 " in _http_lines(caplog)[-1]


def test_vercel_entry_sets_request_timeout_below_max_duration():
    cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    src = (ROOT / "api" / "index.py").read_text(encoding="utf-8")
    assert 'os.environ.setdefault("MM_REQUEST_TIMEOUT", "50")' in src
    assert 50 + web.BODY_TIMEOUT < cfg["functions"]["api/index.py"]["maxDuration"] + 1
    assert 50 < cfg["functions"]["api/index.py"]["maxDuration"]


# --- stvarni HTTP poslužitelj (uvicorn, h11 kao Vercelov runtime) ----------------------------------------------

@pytest.fixture
def live(con):
    import uvicorn

    app = _vercel(con)
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, lifespan="on", log_level="warning", http="h11"))
    t = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    t.start()
    for _ in range(200):
        if server.started:
            break
        time.sleep(0.02)
    yield app, port
    server.should_exit = True
    t.join(5)
    app.light.shutdown()


def _http(port, body: bytes, close_after_send=False, length=None):
    s = socket.create_connection(("127.0.0.1", port), timeout=5)
    head = ("POST /mcp HTTP/1.1\r\nhost: mealmeter.vercel.app\r\ncontent-type: application/json\r\n"
            "accept: application/json, text/event-stream\r\nconnection: close\r\n"
            f"content-length: {length if length is not None else len(body)}\r\n\r\n").encode()
    s.sendall(head + body)
    if close_after_send:
        s.close()
        return b""
    out = b""
    while chunk := s.recv(65536):
        out += chunk
    s.close()
    return out


def test_live_server_notification_and_lists_do_not_hang(live, caplog):
    caplog.set_level(logging.INFO, logger="mealmeter")
    app, port = live
    for body, status in [(_init("2025-06-18"), b"200"), (NOTIF, b"202"), (_req("tools/list"), b"200"),
                         (_req("prompts/list"), b"200"), (_req("resources/list"), b"200")]:
        t0 = time.perf_counter()
        out = _http(port, json.dumps(body).encode())
        assert out.split(b"\r\n")[0].split()[1] == status and time.perf_counter() - t0 < 1, out[:200]
    # klijent šalje pola tijela i zatvori vezu: zapis 499, SDK se ne učitava
    _http(port, b'{"jsonrpc":"2.0",', close_after_send=True, length=55)
    for _ in range(100):
        if any(" status=499 " in ln for ln in _http_lines(caplog)):
            break
        time.sleep(0.02)
    assert any(" status=499 " in ln and "phase=disconnect" in ln for ln in _http_lines(caplog)), _http_lines(caplog)
    assert app.light.sdk is None
