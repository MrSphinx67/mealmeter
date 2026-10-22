# Korak 5V3: routing na Vercelu

| točka | stanje |
|---|---|
| 1 izlaz `vercel build` i dokumentacija | gotovo |
| 2 sve putanje i metode do ASGI aplikacije | gotovo: uklonjen rewrite iz vercel.json |
| 3 nepoznate putanje i /.well-known/* → JSON 404 | gotovo |
| 4 testovi; `vercel build --prod` | gotovo: 973 testa prolaze; build prolazi, 184,9 MB |
| 5 provjera nakon deploya u docs/DEPLOY.md | gotovo |

Ništa nije deployano.

## 1. Uzrok

`.vercel/output` prije popravka: **nema statičnih datoteka** (`static/` ne postoji), pa ni početna stranica ni /mcp nisu
prerenderirani. Funkcija se zove `python` (Python backend, ulazna točka `api/index.py`), a ne `/api/index`. Rute:

1. `handle: filesystem`;
2. **naš rewrite** iz vercel.json: `^/(.*)$ → /api/index` (`check: true`);
3. `handle: error`: 404 `/404.html` za putanje izvan `/api`;
4. `handle: rewrite`: ruta buildera `/(.*) → /python` uz `request.path = /$1` (izvorna putanja).

Builder sam šalje SVE putanje funkciji s izvornom putanjom. Dokumentacija za Python backend kaže da se aplikacija
gradi u jednu funkciju koja prima sve zahtjeve, a za FastAPI da sve metode osim GET/HEAD uvijek stižu do funkcije.
Upozorenje buildera "Internal rewrites in backend framework projects now route requests using the rewritten
destination path" znači da je naš rewrite aplikaciji predavao putanju `/api/index`. Omotač ju je svodio na `/`, pa je
svaki GET (i `/mcp`, i `/.well-known/*`) vraćao početnu stranicu (200). POST je nakon rewritea na nepostojeću
putanju (`check: true`) završavao u Vercelovom odgovoru `405, allow: GET, HEAD`.

Izvori: [FastAPI na Vercelu (routing backend aplikacije)](https://vercel.com/docs/frameworks/backend/fastapi),
[Python runtime](https://vercel.com/docs/functions/runtimes/python),
[Rewrites](https://vercel.com/docs/routing/rewrites),
[Python projects now support routing rules](https://vercel.com/changelog/python-projects-now-support-routing-rules).

## 2.-3. Popravak

- `vercel.json`: uklonjen `rewrites`. Nakon `vercel build --prod` ostaje samo ruta buildera (`/(.*) → /python`,
  izvorna putanja); upozorenja više nema.
- `api/index.py` / `mealmeter.asgi`: omotač i dalje svodi `/api/index/...` na ostatak putanje, pa radi i s
  prepisanom i s izvornom putanjom (test za oba).
- `server.http_app`: Starletteove greške (nepoznata putanja, kriva metoda) vraćaju JSON (`{"error": "not found",
  "path": ...}`, 404 ili 405) umjesto teksta. `/.well-known/oauth-protected-resource[/mcp]` i
  `/.well-known/oauth-authorization-server` daju 404, pa Claude konektor zna da prijave nema.
- `GET /mcp` ostaje kakav je u SDK-u (stateless, bez SSE): 406 bez `Accept: text/event-stream`, a DELETE i OPTIONS
  daju 405. MCP specifikacija to dopušta poslužitelju koji ne nudi SSE tok ni sesije.

## 4. Provjera

- `tests/test_step5v.py::test_routes_and_methods`: POST /mcp i POST /api/index/mcp → 200 sa serverInfo; GET, DELETE
  i OPTIONS /mcp stižu do MCP aplikacije (JSON-RPC 405/406); tri OAuth .well-known putanje (GET i POST) i
  nepoznata putanja → JSON 404; /healthz i / → 200; POST /healthz → JSON 405.
- `vercel build --prod`: `config.json` ima samo `handle: error` (404.html za putanje izvan /api, za promašaje
  datotečnog sustava) i `/(.*) → /python` s `request.path = /$1`. Statičnih datoteka nema. Paket je 184,9 MB,
  a najveća datoteka 92,3 MB.

Nakon deploya treba provjeriti (curl blok u DEPLOY.md) da Vercelova ruta `handle: error` ne zamijeni naš JSON 404
svojim `/404.html`. Lokalno se to ne može provjeriti.
