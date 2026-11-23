"""Lagani HTTP sloj poslužitelja (Korak 18): bez duckdb-a, MCP SDK-a, starlettea i pydantica.

Vercel naplaćuje Active CPU, a Claude šalje nalete jeftinih POST /mcp zahtjeva (initialize, tools/list, notifications),
često na hladnoj instanci. Import MCP SDK-a sam troši ~1 s CPU-a (mcp_types: pydantic modeli), pa ga Vercelov ulaz
(api/index.py, `vercel_app`) učitava tek kad zatreba:

- initialize, tools/list, ping i notifications/* (u obliku koji SDK prihvaća bez greške, verzije iz handshakea ili bez
  zaglavlja) dobivaju odgovor iz snimke SDK-ovih odgovora (mcp_static.json, `python -m mealmeter.server
  --write-static`; test provjerava da je snimka jednaka SDK-u bajt po bajt);
- GET / i /healthz čitaju datum cjenika iz metapodataka sažete baze (data/compact_meta.json, build_compact.py), bez
  otvaranja baze; nepoznate putanje (i /.well-known/oauth-*) su JSON 404 kao iz SDK aplikacije;
- sve ostalo (tools/call, neobični zahtjevi, druge verzije protokola) ide SDK aplikaciji, koja se tada učita jednom
  po instanci; baza se otvara tek u prvom alatu kojem treba (server._con), uz provjeru oznake izgradnje.

Ovdje su i ASGI omotači koje koristi i lokalni HTTP način (server.http_app): RequestLog, HostGuard, RateLimit,
McpPostOnly.

Korak 21 (MCP 2026-07-28, bez handshakea): server/discover, tools/list i prazni popisi iz snimke moderne ere;
subscriptions/listen odmah -32601 Method not found (HTTP 404), kao SDK sa subscriptions=False: poslužitelj nema
obavijesti, pa pretplate ne najavljuje (tools.listChanged = false) i ne drži otvoren SSE tok (prije: 50 s do čuvara
vremena i ponovni pokušaji klijenta). Zahtjev moderne ere koji ide SDK-u ima u zapisu `why=` (razlog, bez sadržaja).

Korak 19: brzi put odgovara i na prompts/list, resources/list, resources/templates/list (prazni popisi; initialize ih
više ne najavljuje) i na svaku notifikaciju (202). Zapis zahtjeva ima JSON-RPC metodu (`rpc=`), id (`id=`, `-` za
notifikaciju) i `path=fast|sdk`. Tijelo zahtjeva čita se najviše MM_BODY_TIMEOUT s (408), prekinuta veza se ne šalje
SDK-u, a RequestLog uz MM_REQUEST_TIMEOUT prekida zahtjev prije Vercelovog maxDuration i zapisuje gdje je zapeo
(`timeout=1 phase=...`), umjesto da platforma ubije instancu bez zapisa.
"""

import asyncio
import json
import logging
import os
import re
import sys
import time
from collections import defaultdict, deque
from functools import lru_cache
from pathlib import Path

log = logging.getLogger("mealmeter")

ROOT = Path(__file__).resolve().parents[2]
MAX_REQUEST_BYTES = 64_000
RATE_LIMIT = 60  # upita po IP-u u minuti (HTTP), MM_RATE_IP
RATE_SESSION = 30  # upita po MCP sesiji (Mcp-Session-Id) u minuti, MM_RATE_SESSION
RATE_GLOBAL = 1000  # upita ukupno u minuti, MM_RATE_GLOBAL
HEALTH_MAX_AGE_HOURS = 48  # starija baza: status "stale" (ažuriranje dvaput dnevno, vidi update.py)
STATIC_PATH = Path(__file__).with_name("mcp_static.json")
BODY_TIMEOUT = 10.0  # s, najdulje čitanje tijela POST /mcp (MM_BODY_TIMEOUT); tijelo je najviše 64 KB
INFO_KEY = "mealmeter.info"  # ključ u ASGI scopeu: podaci o zahtjevu za RequestLog (rpc, id, path, phase)


# --- baza i metapodaci (bez duckdb-a) ---------------------------------------------------------------------

def default_db() -> Path:
    """MM_DB (npr. data/compact.duckdb, scripts/build_compact.py), inače MEALMETER_DB, inače puna baza."""
    return Path(os.environ.get("MM_DB") or os.environ.get("MEALMETER_DB") or ROOT / "data" / "mealmeter.duckdb")


def meta_path(db: str | Path) -> Path:
    """Metapodaci uz sažetu bazu (data/compact.duckdb -> data/compact_meta.json), zapisuje ih build_compact.py."""
    db = Path(db)
    return db.with_name(f"{db.stem}_meta.json")


_meta_cache: dict = {"key": None, "value": None}
_meta_rejected: set[str] = set()  # oznake izgradnje čiji se metapodaci nisu slagali s otvorenom bazom


def read_meta(db: str | Path) -> dict | None:
    """{"build_id", "date", "date_hr", "updated", "loaded_at"} iz metapodataka uz bazu `db`, ili None (nema ih, nisu
    čitljivi ili ih je otvorena baza odbila). Datoteka se čita ponovno tek kad se promijeni (inode, mtime, veličina)."""
    path = meta_path(db)
    try:
        st = path.stat()
    except OSError:
        return None
    key = (str(path), st.st_ino, st.st_mtime_ns, st.st_size)
    if _meta_cache["key"] != key:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or not value.get("build_id") or not value.get("date"):
                value = None
        except (OSError, ValueError):
            value = None
        _meta_cache.update(key=key, value=value)
    value = _meta_cache["value"]
    if value is None or value["build_id"] in _meta_rejected:
        return None
    return value


def reject_meta(build_id: str) -> None:
    """Otvorena baza je iz druge izgradnje: metapodaci s ovom oznakom se više ne koriste (datum iz baze)."""
    _meta_rejected.add(build_id)


def current_meta() -> dict | None:
    """Metapodaci baze koju poslužitelj koristi; None kad je veza zadana izvana (testovi) ili ih nema."""
    srv = sys.modules.get("mealmeter.server")
    if srv is None:
        return read_meta(default_db())
    if srv._fixed_con:
        return None
    return read_meta(srv._db_path or srv.search.DEFAULT_DB)


@lru_cache(maxsize=1)
def version() -> str:
    try:
        from importlib.metadata import version as _v
        return _v("mealmeter")
    except Exception:  # noqa: BLE001
        return "dev"


def _age_hours(updated: str | None, loaded_at) -> float | None:
    import datetime as dt

    ts = dt.datetime.fromisoformat(updated) if updated else (
        dt.datetime.fromisoformat(loaded_at) if isinstance(loaded_at, str) else loaded_at.astimezone()
        if loaded_at else None)
    return round((dt.datetime.now(dt.timezone.utc) - ts).total_seconds() / 3600, 1) if ts else None


def health() -> tuple[int, dict]:
    """GET /healthz: {status, db_date, db_age_hours, version}. Starost je od objave učitanog cjenika
    (clean.archive_info.updated), inače od učitavanja; "stale" iznad HEALTH_MAX_AGE_HOURS, "error" (503) kad baza nije
    čitljiva. Sa sažetom bazom sve iz metapodataka (bez otvaranja baze), inače iz baze."""
    try:
        if meta := current_meta():
            db_date, age = meta["date"], _age_hours(meta.get("updated"), meta.get("loaded_at"))
        else:
            from mealmeter import server

            con = server._con()
            db_date, updated, loaded = server._price_list_date(con)["date"], None, None
            try:
                updated, loaded = con.execute(
                    "SELECT updated, loaded_at FROM clean.archive_info ORDER BY date DESC LIMIT 1").fetchone()
            except Exception:  # noqa: BLE001  (baza bez archive_info, npr. testovi)
                pass
            age = _age_hours(updated, loaded)
    except Exception:  # noqa: BLE001
        return 503, {"status": "error", "db_date": None, "db_age_hours": None, "version": version()}
    status = "ok" if age is None or age <= HEALTH_MAX_AGE_HOURS else "stale"
    return 200, {"status": status, "db_date": db_date, "db_age_hours": age, "version": version()}


HOME_HTML = """<!doctype html>
<html lang="hr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mealmeter</title>
<style>body{{font-family:system-ui,sans-serif;max-width:42rem;margin:2rem auto;padding:0 1rem;line-height:1.5}}
code{{background:#eee;padding:.1rem .3rem;border-radius:3px}}</style></head><body>
<h1>Mealmeter</h1>
<p><strong>Hrvatski.</strong> MCP konektor koji za jelo ili popis namirnica i grad pronalazi cijene u hrvatskim
trgovinama i najjeftiniju trgovinu. Besplatan, otvorenog koda, bez prijave.</p>
<p><strong>Dodavanje u Claude:</strong> Postavke &rarr; Konektori &rarr; Dodaj prilagođeni konektor, URL
<code>{url}</code>.</p>
<p><strong>Izvor podataka:</strong> službeni dnevni cjenici trgovina, preuzeti s
<a href="https://cijene.dev">cijene.dev</a> (DobarKod). Učitani cjenik: {db_date}.</p>
<p><strong>Podaci:</strong> cijene.dev (DobarKod), prema <a href="https://cijene.dev/uvjeti-koristenja">uvjetima
korištenja</a> cijene.dev. <strong>Kod:</strong> licenca MIT.</p>
<p><strong>Napomena:</strong> cijene su iz cjenika; u trgovini se mogu razlikovati, cjenik nije zaliha, a akcije se
mijenjaju.</p>
<p><strong>Privatnost:</strong> nema računa ni kolačića. Sadržaj upita se ne sprema; zapisuje se samo broj poziva
po alatu, status i trajanje, bez punih IP adresa.</p>
<hr>
<p><strong>English.</strong> An MCP connector that finds grocery prices in Croatian stores for a dish or a shopping
list in a given city, and the cheapest store. Free, open source, no login.</p>
<p><strong>Add to Claude:</strong> Settings &rarr; Connectors &rarr; Add custom connector, URL <code>{url}</code>.</p>
<p><strong>Data source:</strong> the stores' official daily price lists via <a href="https://cijene.dev">cijene.dev</a>
(DobarKod). Loaded price list: {db_date}.</p>
<p><strong>Data:</strong> cijene.dev (DobarKod), under the cijene.dev
<a href="https://cijene.dev/uvjeti-koristenja">terms of use</a>. <strong>Code:</strong> MIT license.</p>
<p><strong>Note:</strong> prices come from price lists; in-store prices may differ, a price list is not stock, and
promotions change.</p>
<p><strong>Privacy:</strong> no accounts or cookies. Query content is not stored; only the number of calls per tool,
status and duration are logged, without full IP addresses.</p>
<p><small>Mealmeter {version} · <a href="/healthz">/healthz</a></small></p>
</body></html>
"""


def home(host: str | None, proto: str | None = None) -> str:
    """GET /: kratka stranica (hr i en) s URL-om MCP endpointa za ovaj Host."""
    import html

    host = host or "localhost:8000"
    local = HostGuard._hostname(host) in LOCAL_HOSTS
    scheme = proto or ("http" if local else "https")
    _, h = health()
    return HOME_HTML.format(url=html.escape(f"{scheme}://{host}/mcp"), db_date=html.escape(h["db_date"] or "-"),
                            version=html.escape(h["version"]))


# --- ASGI omotači -------------------------------------------------------------------------------------------

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


class RateLimit:
    """ASGI: ograničenja HTTP zahtjeva u `window` sekundi (429) i veličina tijela (413).

    - po IP-u (`limit`, MM_RATE_IP): IP klijenta iz veze; uz TRUSTED_PROXY=vercel iz x-vercel-forwarded-for /
      x-real-ip / x-forwarded-for (Vercel ih postavlja sam); samo uz TRUSTED_PROXY=1 (poslužitelj iza vlastitog
      proxyja) iz CF-Connecting-IP, inače iz zadnjeg unosa X-Forwarded-For (adresa koju je vidio naš proxy;
      raniji unosi dolaze od klijenta i mogu se krivotvoriti);
    - po MCP sesiji (`session_limit`, MM_RATE_SESSION), kad zahtjev nosi Mcp-Session-Id;
    - ukupno (`global_limit`, MM_RATE_GLOBAL), visoko, kao zaštita poslužitelja.
    """

    def __init__(self, app, limit: int | None = None, window: float = 60.0, max_body: int = MAX_REQUEST_BYTES,
                 session_limit: int | None = None, global_limit: int | None = None,
                 trusted_proxy: bool | None = None):
        self.app, self.window, self.max_body = app, window, max_body
        self.limit = limit if limit is not None else _env_int("MM_RATE_IP", RATE_LIMIT)
        self.session_limit = session_limit if session_limit is not None else _env_int("MM_RATE_SESSION", RATE_SESSION)
        self.global_limit = global_limit if global_limit is not None else _env_int("MM_RATE_GLOBAL", RATE_GLOBAL)
        if trusted_proxy is None:  # "1": vlastiti proxy (CF-Connecting-IP / X-Forwarded-For); "vercel": Vercelova zaglavlja
            env = os.environ.get("TRUSTED_PROXY", "")
            trusted_proxy = "vercel" if env == "vercel" else env == "1"
        self.trusted_proxy = trusted_proxy
        self.hits: dict[str, deque] = defaultdict(deque)  # "ip:..." / "session:..." / "global"
        self._last_prune = time.monotonic()

    def client_ip(self, scope, headers: dict[bytes, bytes]) -> str:
        if self.trusted_proxy == "vercel":
            # Vercel prepisuje X-Forwarded-For IP-om klijenta (ne prosljeđuje vanjske IP-ove); x-vercel-forwarded-for i
            # x-real-ip su isti. CF-Connecting-IP bi klijent na Vercelu mogao sam poslati, pa se ne čita.
            for name in (b"x-vercel-forwarded-for", b"x-real-ip", b"x-forwarded-for"):
                if ip := headers.get(name, b"").decode("latin-1").split(",")[0].strip():
                    return ip
        elif self.trusted_proxy:
            if cf := headers.get(b"cf-connecting-ip", b"").decode("latin-1").strip():
                return cf
            if xff := [p.strip() for p in headers.get(b"x-forwarded-for", b"").decode("latin-1").split(",") if p.strip()]:
                return xff[-1]
        return (scope.get("client") or ("?", 0))[0]

    def _over(self, key: str, limit: int, now: float) -> bool:
        q = self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        return len(q) >= limit

    def _prune(self, now: float) -> None:
        """Ključevi bez zahtjeva u prozoru se brišu (sesije i IP-ovi ne rastu bez granice)."""
        if now - self._last_prune < self.window:
            return
        self._last_prune = now
        for key in [k for k, q in self.hits.items() if not q or now - q[-1] > self.window]:
            del self.hits[key]

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = {k.lower(): v for k, v in scope.get("headers") or []}
        length = headers.get(b"content-length")
        if length and int(length) > self.max_body:
            return await self._reply(send, 413, "zahtjev je prevelik / request too large")
        now = time.monotonic()
        self._prune(now)
        keys = [("global", self.global_limit, "poslužitelj je zauzet / server is busy"),
                ("ip:" + self.client_ip(scope, headers), self.limit, "previše upita s ove adrese / too many requests")]
        if session := headers.get(b"mcp-session-id", b"").decode("latin-1").strip():
            keys.append(("session:" + session[:128], self.session_limit,
                         "previše upita u ovoj sesiji / too many requests in this session"))
        for key, limit, text in keys:
            if self._over(key, limit, now):
                return await self._reply(send, 429, f"{text}, pokušaj za minutu / retry in a minute")
        for key, _, _ in keys:
            self.hits[key].append(now)
        return await self.app(scope, receive, send)

    @staticmethod
    async def _reply(send, status: int, text: str):
        body = json.dumps({"error": text}, ensure_ascii=False).encode()
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"application/json"), (b"retry-after", b"60")]})
        await send({"type": "http.response.body", "body": body})


LOCAL_HOSTS = ("127.0.0.1", "localhost", "[::1]", "::1")
LOCAL_ORIGINS = ("http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*")


def _match(value: str, pattern: str) -> bool:
    """Obrazac s * (bilo koji niz znakova); sve ostalo doslovno ("[::1]" nije skup znakova kao u fnmatch)."""
    return re.fullmatch(".*".join(re.escape(part) for part in pattern.split("*")), value) is not None


def _split_env(name: str) -> list[str]:
    return [p.strip() for p in os.environ.get(name, "").split(",") if p.strip()]


class HostGuard:
    """ASGI: zaštita od DNS rebindinga s obrascima hostova. SDK (TransportSecuritySettings) zna samo točne
    vrijednosti i "host:*" (bilo koji port), pa za tunel ("*.trycloudflare.com") njegovu provjeru gasimo i
    provjeravamo ovdje: Host bez porta mora pogoditi lokalni host ili obrazac iz MM_ALLOWED_HOSTS (* je bilo koji
    niz, "*.trycloudflare.com"), inače 421; Origin, ako ga ima, lokalni ili iz MM_ALLOWED_ORIGINS, inače 403."""

    def __init__(self, app, allowed_hosts: list[str] | None = None, allowed_origins: list[str] | None = None):
        self.app = app
        hosts = allowed_hosts if allowed_hosts is not None else _split_env("MM_ALLOWED_HOSTS")
        origins = allowed_origins if allowed_origins is not None else _split_env("MM_ALLOWED_ORIGINS")
        self.hosts = [h.lower() for h in (*LOCAL_HOSTS, *hosts)]
        self.origins = [o.lower().rstrip("/") for o in (*LOCAL_ORIGINS, *origins)]

    @staticmethod
    def _hostname(host: str) -> str:
        host = host.strip().lower()
        if host.startswith("["):  # [::1]:8000
            return host.split("]")[0] + "]"
        return host.rsplit(":", 1)[0] if host.count(":") == 1 else host

    def host_ok(self, host: str | None) -> bool:
        if not host:
            return False
        name = self._hostname(host)
        return any(_match(name, p) or _match(host.strip().lower(), p) for p in self.hosts)

    def origin_ok(self, origin: str | None) -> bool:
        if not origin:  # klijenti izvan preglednika ne šalju Origin
            return True
        origin = origin.lower().rstrip("/")
        return any(_match(origin, p) or (p.endswith(":*") and _match(origin, p[:-2])) for p in self.origins)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = {k.lower(): v.decode("latin-1") for k, v in scope.get("headers") or []}
        if not self.host_ok(headers.get(b"host")):
            return await _text(send, 421, "Invalid Host header (MM_ALLOWED_HOSTS)")
        if not self.origin_ok(headers.get(b"origin")):
            return await _text(send, 403, "Invalid Origin header (MM_ALLOWED_ORIGINS)")
        return await self.app(scope, receive, send)


async def _text(send, status: int, text: str, content_type: bytes = b"text/plain; charset=utf-8"):
    body = text.encode("utf-8")
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", content_type), (b"content-length", str(len(body)).encode())]})
    await send({"type": "http.response.body", "body": body})


def anon_ip(ip: str | None) -> str:
    """IP bez zadnjeg dijela: IPv4 /24 ("203.0.113.x"), IPv6 /48 ("2001:db8:1::x")."""
    if not ip:
        return "?"
    if ":" in ip:
        return ":".join(ip.split(":")[:3]) + "::x"
    parts = ip.split(".")
    return ".".join(parts[:3]) + ".x" if len(parts) == 4 else "?"


class RequestLog:
    """ASGI: jedan redak po HTTP zahtjevu (metoda, putanja bez upita, status, trajanje, CPU vrijeme, skraćeni IP).
    Tijelo zahtjeva (sadržaj upita) i query string se ne zapisuju; zamjenjuje uvicornov access log.

    cpu_ms je CPU vrijeme procesa za trajanja zahtjeva (time.process_time, sve dretve, i DuckDB-ove; zahtjevi koji
    se preklapaju dijele ga). Prvi zahtjev procesa (hladni start instance) ima cold=1 i boot_cpu_ms, CPU potrošen
    prije njega (interpreter i import).

    Unutarnja aplikacija (web.Light) upisuje u scope[INFO_KEY] JSON-RPC metodu (`rpc=`, za tools/call i `name=`),
    id (`id=`, `-` za notifikaciju), `path=fast|sdk` i fazu (`phase`); `default_path` je put kad ga nitko ne upiše
    (VercelApp: "fast", jer 405/404/429 ne učitavaju SDK). Uz `timeout` (s, MM_REQUEST_TIMEOUT, 0 = bez) zahtjev
    koji traje dulje prekida se, klijent dobiva 504 ako odgovor još nije počeo, a zapis ima `timeout=1 phase=...
    body=<primljeno>/<content-length>`: na Vercelu tako zapis postoji i instanca ostaje živa, umjesto "Task timed
    out" bez zapisa i hladnog starta sljedećeg zahtjeva."""

    _cold = True  # po procesu: prvi zahtjev bilo kojeg RequestLog-a

    def __init__(self, app, trusted_proxy: bool | None = None, timeout: float | None = None,
                 default_path: str | None = None):
        self.app = app
        self.ip = RateLimit(None, trusted_proxy=trusted_proxy).client_ip
        if timeout is None:
            try:
                timeout = float(os.environ.get("MM_REQUEST_TIMEOUT", "0"))
            except ValueError:
                timeout = 0.0
        self.timeout = timeout if timeout > 0 else None
        self.default_path = default_path

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        start, cpu0, status = time.perf_counter(), time.process_time(), 500
        cold = ""
        if RequestLog._cold:
            RequestLog._cold = False
            cold = f" cold=1 boot_cpu_ms={cpu0 * 1000:.0f}"
        info: dict = {}
        if self.default_path:
            info["path"] = self.default_path
        scope = {**scope, INFO_KEY: info}
        started = timed_out = False

        async def send_status(msg):
            nonlocal status, started
            if msg["type"] == "http.response.start":
                status, started = msg["status"], True
            await send(msg)

        try:
            async with asyncio.timeout(self.timeout):
                await self.app(scope, receive, send_status)
        except TimeoutError:
            timed_out = True
            if not started:
                rid = info.get("rid")
                body = _dumps({"jsonrpc": "2.0", "id": rid if _is_id(rid) else None,
                               "error": {"code": -32603, "message": "timeout"}})
                try:
                    await send_status({"type": "http.response.start", "status": 504, "headers": _json_headers(body)})
                    await send({"type": "http.response.body", "body": body, "more_body": False})
                except Exception:  # noqa: BLE001  (veza možda više ne postoji)
                    pass
        finally:
            headers = {k.lower(): v for k, v in scope.get("headers") or []}
            extra = "".join(f" {k}={info[k]}" for k in ("rpc", "name", "id", "path", "why") if k in info)
            if timed_out:
                extra += f" timeout=1 phase={info.get('phase', '?')} body={info.get('body_bytes', 0)}/" + \
                         headers.get(b"content-length", b"-").decode("latin-1")[:12]
            elif info.get("phase") in ("body_timeout", "disconnect"):
                extra += f" phase={info['phase']} body={info.get('body_bytes', 0)}/" + \
                         headers.get(b"content-length", b"-").decode("latin-1")[:12]
            log.info("http %s %s status=%d ms=%d cpu_ms=%d ip=%s%s%s", scope.get("method"), scope.get("path"),
                     info.get("status", status), (time.perf_counter() - start) * 1000,
                     (time.process_time() - cpu0) * 1000, anon_ip(self.ip(scope, headers)), extra, cold)


class McpPostOnly:
    """ASGI: GET, HEAD i DELETE na /mcp odmah dobivaju 405 (JSON, Allow: POST); POST ide dalje.

    Poslužitelj je stateless: nema sesija (DELETE) ni poruka koje bi slao SSE tokom (GET). MCP Streamable HTTP tada
    dopušta 405. SDK bi na GET s `Accept: text/event-stream` otvorio tok i držao vezu, što na Vercelu troši trajanje
    funkcije (do 300 s) i može se zlorabiti (Korak 5V4)."""

    METHODS = {"GET", "HEAD", "DELETE"}

    def __init__(self, app, path: str = "/mcp"):
        self.app, self.path = app, path

    async def __call__(self, scope, receive, send):
        if (scope["type"] == "http" and scope.get("method") in self.METHODS
                and scope.get("path", "").rstrip("/") == self.path):
            body = json.dumps({"jsonrpc": "2.0", "id": None, "error": {
                "code": -32000, "message": "Method not allowed: koristi POST / use POST"}}).encode()
            await send({"type": "http.response.start", "status": 405,
                        "headers": [(b"content-type", b"application/json"), (b"allow", b"POST"),
                                    (b"content-length", str(len(body)).encode())]})
            await send({"type": "http.response.body",
                        "body": b"" if scope["method"] == "HEAD" else body})
            return
        await self.app(scope, receive, send)


# --- brzi put: odgovori bez MCP SDK-a -----------------------------------------------------------------------

@lru_cache(maxsize=1)
def static_mcp() -> dict:
    """Snimka SDK-ovih odgovora na initialize i tools/list (mcp_static.json)."""
    return json.loads(STATIC_PATH.read_text(encoding="utf-8"))


def _dumps(obj) -> bytes:
    # isti zapis kao SDK (pydantic model_dump_json): bez razmaka, UTF-8 bez \u-escapea
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _json_headers(body: bytes) -> list:
    return [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())]


def _content_type_json(value: str) -> bool:
    """Kao SDK (_check_content_type): neki dio prije ';' je točno application/json."""
    return any(p.strip() == "application/json" for p in value.split(";")[0].split(","))


def _accepts_json(value: str) -> bool:
    """Kao SDK (check_accept_headers) u JSON načinu: application/json, application/* ili */*."""
    types = [t.strip().split(";")[0].strip().lower() for t in value.split(",")]
    return any(t in ("application/json", "application/*", "*/*") for t in types)


def _is_id(value) -> bool:
    return (isinstance(value, int) and not isinstance(value, bool)) or isinstance(value, str)


def _meta_only(params) -> bool:
    return params is None or (isinstance(params, dict) and set(params) <= {"_meta"}
                              and isinstance(params.get("_meta", {}), dict))


_CLIENT_INFO_KEYS = {"name", "version", "title", "description", "websiteUrl"}


_LOG_TOKEN = re.compile(r"[^A-Za-z0-9_./:-]")


def _token(value, limit: int = 40) -> str:
    """Vrijednost za redak loga: bez razmaka i posebnih znakova, skraćena."""
    return _LOG_TOKEN.sub("_", str(value))[:limit] or "_"


def rpc_info(body: bytes) -> dict:
    """JSON-RPC metoda, id i (za tools/call) naziv alata, za zapis zahtjeva; argumenti alata se ne zapisuju."""
    try:
        msg = json.loads(body)
    except ValueError:
        return {"rpc": "invalid-json"}
    if isinstance(msg, list):
        return {"rpc": f"batch{len(msg)}"}
    if not isinstance(msg, dict):
        return {"rpc": "invalid"}
    method = msg.get("method")
    if isinstance(method, str):
        out = {"rpc": _token(method)}
    else:
        out = {"rpc": "response" if ("result" in msg or "error" in msg) else "invalid"}
    out["id"] = _token(msg["id"], 32) if "id" in msg else "-"
    if "id" in msg:
        out["rid"] = msg["id"]
    params = msg.get("params")
    if method == "tools/call" and isinstance(params, dict) and isinstance(params.get("name"), str):
        out["name"] = _token(params["name"])
    return out


def fast_reply(headers, body: bytes, why: dict | None = None) -> tuple[int, list, bytes] | None:
    """Odgovor na jeftin MCP zahtjev bez SDK-a, ili None (zahtjev ide SDK-u). Samo zahtjevi koje bi SDK (stateless,
    JSON odgovori) prihvatio i odgovorio jednako; sve neobično (verzija protokola izvan handshakea, batch, dodatna
    polja u zahtjevu, nevaljani oblik) ide SDK-u, koji vraća i odgovarajuću grešku.

    Korak 19: SDK bez sesija zaglavlje Mcp-Session-Id zanemaruje (odgovor je isti), pa ono više ne šalje zahtjev
    SDK-u; svaka notifikacija (i s dodatnim poljima, nepoznata notifications/*) i JSON-RPC odgovor klijenta dobivaju
    202 kao od SDK-a; prompts/list, resources/list i resources/templates/list prazne popise iz snimke.

    Korak 21: zaglavlje MCP-Protocol-Version moderne ere (2026-07-28, snap["modern"]) ide u _modern_reply.
    `headers` je dict ili popis parova (ASGI, s ponovljenim zaglavljima); u `why["why"]` se upisuje zašto zahtjev
    moderne ere ide SDK-u (za zapis zahtjeva, bez sadržaja)."""
    snap = static_mcp()
    versions = snap["handshake_versions"]
    pairs = list(headers.items() if isinstance(headers, dict) else headers)
    h = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in pairs}
    if not _accepts_json(h.get("accept", "")) or not _content_type_json(h.get("content-type", "")):
        return _no(why, "accept")
    pv = h.get("mcp-protocol-version")
    if pv is not None and pv in snap.get("modern", {}):
        return _modern_reply(snap["modern"][pv], pv, h, pairs, body, why)
    if pv is not None and pv not in versions:
        return _no(why, "version")
    try:
        msg = json.loads(body)
    except ValueError:
        return None
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
        return None
    if "method" not in msg and "id" in msg and _is_id(msg["id"]) and (
            ("result" in msg) != ("error" in msg)) and set(msg) <= {"jsonrpc", "id", "result", "error"}:
        return 202, _json_headers(b""), b""  # odgovor klijenta (SDK: 202, ovaj poslužitelj ne šalje zahtjeve)
    if not isinstance(msg.get("method"), str):
        return None
    method, params = msg["method"], msg.get("params")
    if "id" not in msg:
        if method.startswith("notifications/") and (params is None or isinstance(params, dict)):
            return 202, _json_headers(b""), b""
        return None
    rid = msg["id"]
    if not _is_id(rid) or not set(msg) <= {"jsonrpc", "id", "method", "params"}:
        return None
    if method == "initialize":
        if not (isinstance(params, dict) and set(params) <= {"protocolVersion", "capabilities", "clientInfo", "_meta"}
                and isinstance(params.get("protocolVersion"), str) and isinstance(params.get("capabilities"), dict)
                and all(isinstance(v, dict) for v in params["capabilities"].values())
                and isinstance(params.get("_meta", {}), dict)):
            return None
        info = params.get("clientInfo")
        if not (isinstance(info, dict) and {"name", "version"} <= set(info) <= _CLIENT_INFO_KEYS
                and all(isinstance(v, str) for v in info.values())):
            return None
        result = dict(snap["initialize"])
        req = params["protocolVersion"]
        result["protocolVersion"] = req if req in versions else snap["fallback_version"]
    elif method == "tools/list" and _meta_only(params):
        result = snap["tools_list"]
    elif method == "ping" and _meta_only(params):
        result = {}
    elif method in snap["empty_lists"] and _meta_only(params):
        result = snap["empty_lists"][method]
    else:
        return None
    out = _dumps({"jsonrpc": "2.0", "id": rid, "result": result})
    return 200, _json_headers(out), out


def _no(why: dict | None, reason: str) -> None:
    if why is not None:
        why["why"] = reason
    return None


PV_META = "io.modelcontextprotocol/protocolVersion"
CAPS_META = "io.modelcontextprotocol/clientCapabilities"
INFO_META = "io.modelcontextprotocol/clientInfo"
_RESERVED_META = "io.modelcontextprotocol/"
_ROUTING_HEADERS = {b"mcp-protocol-version", b"mcp-method", b"mcp-name"}
_FILTER_FLAGS = {"toolsListChanged", "promptsListChanged", "resourcesListChanged"}


def _accepts_sse(value: str) -> bool:
    """Kao SDK (check_accept_headers): text/event-stream, text/* ili */*."""
    types = [t.strip().split(";")[0].strip().lower() for t in value.split(",")]
    return any(t in ("text/event-stream", "text/*", "*/*") for t in types)


def _modern_meta_ok(meta, pv: str) -> str | None:
    """None kad je _meta zahtjeva moderne ere u obliku koji SDK prihvaća jednako, inače razlog."""
    if not isinstance(meta, dict) or meta.get(PV_META) != pv:
        return "meta"
    caps = meta.get(CAPS_META)
    if not isinstance(caps, dict) or not all(isinstance(v, dict) for v in caps.values()):
        return "caps"
    if INFO_META in meta:
        info = meta[INFO_META]
        if not (isinstance(info, dict) and {"name", "version"} <= set(info) <= _CLIENT_INFO_KEYS
                and all(isinstance(v, str) for v in info.values())):
            return "client_info"
    if any(k.startswith(_RESERVED_META) for k in set(meta) - {PV_META, CAPS_META, INFO_META}):
        return "meta_key"  # npr. logLevel: SDK ga provjerava
    return None


def _filter_ok(value) -> bool:
    """SubscriptionFilter iz subscriptions/listen: zastavice (bool) i resourceSubscriptions (popis URI-ja)."""
    if not isinstance(value, dict) or not set(value) <= _FILTER_FLAGS | {"resourceSubscriptions"}:
        return False
    if not all(isinstance(value[k], bool) for k in set(value) & _FILTER_FLAGS):
        return False
    subs = value.get("resourceSubscriptions", [])
    return isinstance(subs, list) and all(isinstance(u, str) for u in subs)


def _modern_reply(snap: dict, pv: str, h: dict, pairs: list, body: bytes,
                  why: dict | None) -> tuple[int, list, bytes] | None:
    """Moderna era (Korak 21, MCP 2026-07-28: bez handshakea, svaki zahtjev nosi _meta s verzijom i sposobnostima):
    server/discover, tools/list i prazni popisi iz snimke (snap["results"]); subscriptions/listen i metode kojih u toj
    verziji nema (ping, initialize, ...) dobivaju -32601 Method not found s HTTP 404 kao od SDK-a (snap["errors"]):
    poslužitelj nema obavijesti, pa pretplate ne poslužuje i ne najavljuje (tools.listChanged = false); notifikacije
    202. Zapis kao SDK u ovoj eri (json.dumps, \\u-escape). Sve što SDK provjerava drukčije (zaglavlja Mcp-Method i
    MCP-Protocol-Version različita od tijela ili ponovljena, nepoznati parametri, _meta izvan uobičajenog oblika,
    listen bez text/event-stream u Accept) ide SDK-u."""
    if sum(1 for k, _ in pairs if k.lower() in _ROUTING_HEADERS) != len(
            {k.lower() for k, _ in pairs if k.lower() in _ROUTING_HEADERS}):
        return _no(why, "dup_header")
    try:
        msg = json.loads(body)
    except ValueError:
        return _no(why, "json")
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return _no(why, "shape")
    method, params = msg["method"], msg.get("params")
    if "id" not in msg:
        if (params is None or isinstance(params, dict)) and set(msg) <= {"jsonrpc", "method", "params"}:
            return 202, [(b"content-length", b"0")], b""  # SDK: potvrđuje i odbacuje, bez content-type
        return _no(why, "shape")
    rid = msg["id"]
    if not _is_id(rid) or not set(msg) <= {"jsonrpc", "id", "method", "params"} or not isinstance(params, dict):
        return _no(why, "shape")
    if h.get("mcp-method") != method:
        return _no(why, "mcp_method")
    if reason := _modern_meta_ok(params.get("_meta"), pv):
        return _no(why, reason)
    allowed = {"_meta"}
    if method == "subscriptions/listen":
        if not _accepts_sse(h.get("accept", "")):
            return _no(why, "accept_sse")  # SDK: 406
        if not _filter_ok(params.get("notifications")):
            return _no(why, "filter")
        allowed.add("notifications")
    if not set(params) <= allowed:
        return _no(why, "params")
    if method in snap["results"]:
        status, payload = 200, {"jsonrpc": "2.0", "id": rid, "result": snap["results"][method]}
    elif method in snap["errors"]:
        status, error = snap["errors"][method]
        payload = {"jsonrpc": "2.0", "id": rid, "error": error}
    else:
        return _no(why, "method")
    out = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return status, _json_headers(out), out


async def _read_body(receive, limit: int, timeout: float | None = None,
                     info: dict | None = None) -> tuple[bytes, list, str]:
    """Tijelo zahtjeva (do `limit` bajtova), primljene poruke (za ponovno slanje SDK-u) i ishod: "ok", "too_large"
    (SDK vraća 413), "disconnect" (klijent je otišao) ili "timeout" (tijelo nije stiglo u `timeout` s)."""
    chunks, msgs, size = [], [], 0
    try:
        async with asyncio.timeout(timeout):
            while True:
                msg = await receive()
                msgs.append(msg)
                if msg["type"] != "http.request":
                    return b"", msgs, "disconnect"
                chunks.append(msg.get("body", b""))
                size += len(chunks[-1])
                if info is not None:
                    info["body_bytes"] = size
                if size > limit:
                    return b"", msgs, "too_large"
                if not msg.get("more_body"):
                    return b"".join(chunks), msgs, "ok"
    except TimeoutError:
        return b"", msgs, "timeout"


def _replay(msgs: list, receive):
    queue = list(msgs)

    async def replay():
        return queue.pop(0) if queue else await receive()
    return replay


async def _send(send, status: int, headers: list, body: bytes) -> None:
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body, "more_body": False})


class Light:
    """ASGI: brzi put (fast_reply, GET /, GET /healthz, JSON 404) i lijena SDK aplikacija za sve ostalo.

    `make_sdk()` vraća unutarnju Starlette aplikaciju SDK-a (server.sdk_app); poziva se pri prvom zahtjevu koji je
    treba, a njezin lifespan (MCP session manager) pokreće LifespanOnDemand."""

    KNOWN = {"", "/healthz", "/mcp"}  # putanje SDK aplikacije (bez završne kose crte); ostalo je 404

    def __init__(self, make_sdk, body_timeout: float | None = None):
        self.make_sdk = make_sdk
        self.sdk = None
        self.fast = 0  # broj zahtjeva odgovorenih bez SDK-a (testovi)
        if body_timeout is None:
            try:
                body_timeout = float(os.environ.get("MM_BODY_TIMEOUT", BODY_TIMEOUT))
            except ValueError:
                body_timeout = BODY_TIMEOUT
        self.body_timeout = body_timeout if body_timeout > 0 else None

    async def _sdk(self, scope, receive, send, info: dict):
        info["path"], info["phase"] = "sdk", "sdk_load"
        app = self.load()
        info["phase"] = "sdk"
        return await app(scope, receive, send)

    def load(self):
        if self.sdk is None:
            from mealmeter.asgi import LifespanOnDemand

            t0, c0 = time.perf_counter(), time.process_time()
            inner = self.make_sdk()
            self.sdk = LifespanOnDemand(inner, inner)
            log.info("sdk loaded ms=%d cpu_ms=%d", (time.perf_counter() - t0) * 1000, (time.process_time() - c0) * 1000)
        return self.sdk

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.load()(scope, receive, send)
        info = scope.get(INFO_KEY)
        if info is None:
            info = {}
        method, path = scope.get("method"), scope.get("path", "")
        if method == "POST" and path == "/mcp":
            info["phase"] = "body"
            body, msgs, outcome = await _read_body(receive, MAX_REQUEST_BYTES, self.body_timeout, info)
            if outcome == "disconnect":
                # klijent je otišao prije kraja tijela: nema kome odgovoriti (SDK bi ga čekao ili vratio 500)
                info.update(path="fast", phase="disconnect", status=499)
                return
            if outcome == "timeout":
                info.update(path="fast", phase="body_timeout")
                out = _dumps({"jsonrpc": "2.0", "id": None,
                              "error": {"code": -32600, "message": "request body timeout"}})
                return await _send(send, 408, _json_headers(out), out)
            if outcome == "ok":
                info.update(rpc_info(body))
            reply = fast_reply(scope.get("headers") or [], body, info) if outcome == "ok" else None
            if info.get("rpc") == "tools/call":
                info.pop("why", None)  # tools/call uvijek ide SDK-u; why= je za jeftine zahtjeve koji nisu na brzom putu
            if reply:
                self.fast += 1
                info.update(path="fast", phase="send")
                return await _send(send, *reply)
            return await self._sdk(scope, _replay(msgs, receive), send, info)
        if method == "GET" and path == "/healthz":
            status, body = health()
            out = _dumps(body)
            self.fast += 1
            return await _send(send, status, [(b"cache-control", b"no-store"), (b"content-length", str(len(out)).encode()),
                                              (b"content-type", b"application/json")], out)
        if method == "GET" and path == "/":
            headers = {k.lower(): v.decode("latin-1") for k, v in scope.get("headers") or []}
            out = home(headers.get(b"host"), headers.get(b"x-forwarded-proto")).encode("utf-8")
            self.fast += 1
            return await _send(send, 200, [(b"content-length", str(len(out)).encode()),
                                           (b"content-type", b"text/html; charset=utf-8")], out)
        if path.rstrip("/") not in self.KNOWN:
            out = _dumps({"error": "not found", "path": path})
            self.fast += 1
            return await _send(send, 404, [(b"content-length", str(len(out)).encode()),
                                           (b"content-type", b"application/json")], out)
        return await self._sdk(scope, receive, send, info)

    def shutdown(self):
        if self.sdk is not None and self.sdk._task:
            self.sdk._task.cancel()


class VercelApp:
    """ASGI ulaz za Vercel (api/index.py): /api/index... -> ostatak putanje, lifespan bez učitavanja SDK-a, pa
    RequestLog -> HostGuard -> RateLimit -> McpPostOnly -> Light. `request_timeout` / `body_timeout`: s, inače
    MM_REQUEST_TIMEOUT / MM_BODY_TIMEOUT (api/index.py: 50 s, ispod maxDuration 60 s u vercel.json)."""

    def __init__(self, make_sdk, allowed_hosts: list[str] | None = None, allowed_origins: list[str] | None = None,
                 request_timeout: float | None = None, body_timeout: float | None = None):
        self.light = Light(make_sdk, body_timeout=body_timeout)
        self.app = RequestLog(HostGuard(RateLimit(McpPostOnly(self.light)), allowed_hosts, allowed_origins),
                              timeout=request_timeout, default_path="fast")

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            while True:
                msg = await receive()
                if msg["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif msg["type"] == "lifespan.shutdown":
                    self.light.shutdown()
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        path = scope.get("path", "")
        if path == "/api/index" or path.startswith("/api/index/"):
            rest = path[len("/api/index"):] or "/"
            scope = {**scope, "path": rest, "raw_path": rest.encode()}
        await self.app(scope, receive, send)


def setup_logging() -> None:
    """Kao MCP SDK (MCPServer -> configure_logging, bez paketa rich): INFO, samo poruka, na stderr. SDK se na Vercelu
    učitava tek kad zatreba, pa bez ovoga retci RequestLog-a jeftinih zahtjeva ne bi bili u logovima."""
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()])

