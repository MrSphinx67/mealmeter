"""CPU vrijeme poslužitelja po vrsti zahtjeva (Korak 18, Active CPU na Vercelu).

    uv run python scripts/cpu_profile.py [--runs 5] [--threads 2] [--json izlaz.json]

Svaki scenarij se pokreće u novom procesu (hladni start, kao nova instanca funkcije), vezan na jednu jezgru
(taskset -c 0; Vercel Hobby ima 1 vCPU), uz MM_DUCKDB_MEMORY=300MB i MM_DB=data/compact.duckdb. Aplikacija je
`app` iz api/index.py (isti omotač kao na Vercelu), zahtjevi idu izravno kroz ASGI (bez mreže). Za svaki korak
se mjeri CPU vrijeme procesa (time.process_time: sve dretve, i DuckDB-ove) i stvarno vrijeme; ispisuje se medijan.

Scenariji:
  claude: import, initialize, notifications/initialized, tools/list, plan_basket x2, get_prices, find_products,
          pa topli initialize i tools/list (naleti koje Claude šalje između poziva alata)
  cheap:  import, initialize, notifications/initialized, tools/list, GET /mcp, /.well-known (hladni start bez alata)
  web:    import, GET /, GET /healthz
  open:   import mealmeter.server i prvo otvaranje baze (server._con) s datumom cjenika
"""

import argparse
import asyncio
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PALACINKE = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
             {"name": "jaja", "amount": 3, "unit": "kom"}, {"name": "šećer", "amount": 15, "unit": "g"},
             {"name": "ulje", "amount": 30, "unit": "ml"}]
BOLONJEZ = [{"name": "špageti", "amount": 400, "unit": "g"}, {"name": "mljeveno meso", "amount": 500, "unit": "g"},
            {"name": "rajčica", "amount": 700, "unit": "g", "form": "pasirana"},
            {"name": "luk", "amount": 1, "unit": "kom"}, {"name": "maslinovo ulje", "amount": 30, "unit": "ml"},
            {"name": "parmezan"}, {"name": "sol"}]

INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "probe", "version": "1"}}}
NOTIF = {"jsonrpc": "2.0", "method": "notifications/initialized"}
LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}


def call(name, args, rid=3):
    return {"jsonrpc": "2.0", "id": rid, "method": "tools/call", "params": {"name": name, "arguments": args}}


SCENARIOS = {
    "claude": [("initialize", "POST", "/mcp", INIT), ("notifications/initialized", "POST", "/mcp", NOTIF),
               ("tools/list", "POST", "/mcp", LIST),
               ("plan_basket (1.)", "POST", "/mcp", call("plan_basket", {"ingredients": BOLONJEZ, "city": "Zagreb"})),
               ("plan_basket (2.)", "POST", "/mcp", call("plan_basket", {"ingredients": PALACINKE, "city": "Osijek"})),
               ("get_prices", "POST", "/mcp", call("get_prices", {"product_id": "3850104223624", "city": "Osijek"})),
               ("find_products", "POST", "/mcp", call("find_products", {"ingredient": "brašno", "city": "Osijek"})),
               ("initialize (topli)", "POST", "/mcp", INIT), ("tools/list (topli)", "POST", "/mcp", LIST)],
    "cheap": [("initialize", "POST", "/mcp", INIT), ("notifications/initialized", "POST", "/mcp", NOTIF),
              ("tools/list", "POST", "/mcp", LIST), ("GET /mcp (405)", "GET", "/mcp", None),
              ("GET /.well-known (404)", "GET", "/.well-known/oauth-protected-resource", None)],
    "web": [("GET /", "GET", "/", None), ("GET /healthz", "GET", "/healthz", None)],
    "open": [],
}


async def asgi(app, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else b""
    done = asyncio.Event()
    sent = False
    out = {"status": None, "body": b""}

    async def receive():
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": data, "more_body": False}
        await done.wait()
        return {"type": "http.disconnect"}

    async def send(msg):
        if msg["type"] == "http.response.start":
            out["status"] = msg["status"]
        elif msg["type"] == "http.response.body":
            out["body"] += msg.get("body", b"")
            if not msg.get("more_body"):
                done.set()

    headers = [(b"host", b"mealmeter.vercel.app"), (b"content-type", b"application/json"),
               (b"accept", b"application/json, text/event-stream"), (b"mcp-protocol-version", b"2025-06-18"),
               (b"x-vercel-forwarded-for", b"203.0.113.5"), (b"content-length", str(len(data)).encode())]
    scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1", "method": method, "path": path,
             "raw_path": path.encode(), "query_string": b"", "headers": headers, "client": ("203.0.113.5", 1234),
             "server": ("mealmeter.vercel.app", 443), "scheme": "https", "root_path": ""}
    await app(scope, receive, send)
    return out


def child(scenario: str) -> None:
    rows = []

    def step(name, fn):
        c0, w0 = time.process_time(), time.perf_counter()
        res = fn()
        rows.append({"step": name, "cpu_ms": (time.process_time() - c0) * 1000,
                     "wall_ms": (time.perf_counter() - w0) * 1000})
        return res

    if scenario == "open":
        sys.path.insert(0, str(ROOT / "src"))
        srv = step("import mealmeter.server", lambda: __import__("mealmeter.server", fromlist=["x"]))
        step("otvaranje baze + datum", lambda: srv._price_list_date(srv._con()))
        print(json.dumps({"rows": rows, "duckdb_loaded": "duckdb" in sys.modules}))
        return

    import importlib.util

    def load():
        spec = importlib.util.spec_from_file_location("vercel_index", ROOT / "api" / "index.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.app

    app = step("import (api/index.py)", load)
    loop = asyncio.new_event_loop()
    loaded = {}
    for name, method, path, body in SCENARIOS[scenario]:
        res = step(name, lambda: loop.run_until_complete(asgi(app, method, path, body)))
        if res["status"] not in (200, 202, 404, 405):
            raise SystemExit(f"{name}: HTTP {res['status']} {res['body'][:300]!r}")
        if b'"isError":true' in res["body"]:
            raise SystemExit(f"{name}: {res['body'][:300]!r}")
        loaded[name] = "duckdb" in sys.modules
    print(json.dumps({"rows": rows, "duckdb_loaded": loaded}))


def run(scenario: str, runs: int, env: dict) -> tuple[list[dict], dict]:
    cmd = [sys.executable, str(Path(__file__).resolve()), "--child", scenario]
    if shutil.which("taskset"):
        cmd = ["taskset", "-c", "0", *cmd]
    samples, loaded = [], {}
    for _ in range(runs):
        p = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=ROOT)
        if p.returncode:
            raise SystemExit(f"{scenario}: {p.stderr[-2000:]}")
        out = json.loads(p.stdout.strip().splitlines()[-1])
        samples.append(out["rows"])
        loaded = out["duckdb_loaded"]
    rows = []
    for i, r in enumerate(samples[0]):
        rows.append({"scenario": scenario, "step": r["step"],
                     "cpu_ms": round(statistics.median(s[i]["cpu_ms"] for s in samples)),
                     "wall_ms": round(statistics.median(s[i]["wall_ms"] for s in samples))})
    return rows, loaded


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--child")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--threads", default=None, help="MM_DUCKDB_THREADS (zadano: kako je u kodu)")
    ap.add_argument("--scenarios", default="claude,cheap,web,open")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    if args.child:
        child(args.child)
        return 0
    env = {**os.environ, "MM_DUCKDB_MEMORY": "300MB", "MM_DB": str(ROOT / "data" / "compact.duckdb"),
           "PYTHONDONTWRITEBYTECODE": "0"}
    env.pop("MM_DUCKDB_THREADS", None)
    if args.threads:
        env["MM_DUCKDB_THREADS"] = args.threads
    table, loaded = [], {}
    for sc in args.scenarios.split(","):
        rows, loaded[sc] = run(sc, args.runs, env)
        table += rows
    print("| scenarij | korak | CPU ms | stvarno ms |\n|---|---|---:|---:|")
    for r in table:
        print(f"| {r['scenario']} | {r['step']} | {r['cpu_ms']} | {r['wall_ms']} |")
    print("duckdb učitan:", json.dumps(loaded, ensure_ascii=False))
    if args.json:
        Path(args.json).write_text(json.dumps({"rows": table, "duckdb_loaded": loaded}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
