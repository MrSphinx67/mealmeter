# Deploy na Vercel (ručni koraci)

Mealmeter na Vercelu radi kao jedna Python funkcija (`api/index.py`) sa sažetom bazom `data/compact.duckdb`
(~92 MB) u paketu (184,9 MB; `vercel build` pada iznad 225 MB, a `vercel deploy` na Hobby planu odbija datoteke veće od 100 MB, vidi docs/5V2_STATUS.md). Baza nije u Gitu, pa Vercel ne smije graditi iz Gita
(`vercel.json`: `git.deploymentEnabled: false`); deploy ide samo preko Vercel CLI-ja: ručno ili iz GitHub Actionsa.

## 1. Jednom: projekt na Vercelu

1. Račun na vercel.com (Hobby je dovoljan) i Vercel CLI: `npm install --global vercel`, zatim `vercel login`.
2. U repozitoriju izgradi bazu i sažetu bazu:
   ```sh
   uv sync
   uv run python scripts/update.py          # puna baza data/mealmeter.duckdb (~1,5 GB, ~10 min)
   uv run python scripts/build_compact.py   # data/compact.duckdb (~92 MB; mora biti < 95 MB)
   ```
3. `vercel link`: odaberi ili stvori projekt (Framework Preset: **Other**). Nastaje `.vercel/project.json` s `orgId` i
   `projectId` (mapa `.vercel/` je u `.gitignore`).
4. Na vercel.com, Project Settings → Functions: provjeri da je **Fluid compute** uključen (zadano za nove projekte).
   Python je 3.12 (zadano).
5. Ne povezuj Git repozitorij s projektom (Settings → Git). Ako je povezan, `git.deploymentEnabled: false` ionako
   isključuje automatske deployeve.

## 2. Prvi deploy

```sh
vercel build --prod
vercel deploy --prebuilt --prod
```
(ili `vercel deploy --prod`; `.vercelignore` tada ne šalje punu bazu ni arhive, ali šalje sažetu bazu).

Provjera, uz `<host>` = adresa projekta, npr. `mealmeter.vercel.app`:
```sh
curl https://<host>/healthz      # {"status":"ok","db_date":"...","db_age_hours":...,"version":"..."}
```
`https://<host>/` je kratka stranica s uputom i točnim URL-om konektora.

### Provjera nakon deploya

```sh
H=https://mealmeter.vercel.app   # ili tvoj <host>

# 1. OAuth .well-known: mora biti 404 s JSON-om (poslužitelj nema prijave), ne 200
for p in /.well-known/oauth-protected-resource /.well-known/oauth-protected-resource/mcp /.well-known/oauth-authorization-server; do
  curl -s -o /dev/null -w "%{http_code} %{content_type}  $p\n" "$H$p"
done
# očekivano: 404 application/json  (svaki redak)

# 2. MCP initialize: 200 i serverInfo "mealmeter"
curl -s -X POST "$H/mcp" \
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}' \
  -w '\n%{http_code}\n'
# očekivano: {"jsonrpc":"2.0","id":1,"result":{...,"serverInfo":{"name":"mealmeter",...}}} i 200

# 3. GET /mcp: odmah 405 s "allow: POST" (bez SSE toka koji bi visio); -m 5 prekida ako visi
curl -s -m 5 -o /dev/null -w "%{http_code} allow=%header{allow}\n" "$H/mcp"   # očekivano: 405 allow=POST

# 4. Zdravlje i početna stranica
curl -s "$H/healthz"                                # {"status":"ok","db_date":"...",...}
curl -s -o /dev/null -w "%{http_code}\n" "$H/"     # 200
```

Ako POST /mcp vrati `405` s `server: Vercel` i `allow: GET, HEAD`, zahtjev ne stiže do funkcije: provjeri da
`vercel.json` nema `rewrites` (Korak 5V3).

## 3. Dnevno ažuriranje (GitHub Actions)

1. Na vercel.com → Account Settings → Tokens stvori token.
2. Na GitHubu, repozitorij → Settings → Secrets and variables → Actions → New repository secret:
   - `VERCEL_TOKEN`: token iz koraka 1;
   - `VERCEL_ORG_ID`: `orgId` iz `.vercel/project.json`;
   - `VERCEL_PROJECT_ID`: `projectId` iz `.vercel/project.json`.
3. Actions → **update** → Run workflow (prvi put ručno). Prvo pokretanje gradi bazu bez prethodne
   (nema usporedbe ni prenošenja cijena); zatim workflow radi sam u 13:30 i 21:30 UTC.
4. Workflow ne deploya ako: update.py završi s izlazom 2 (broj čistih cijena nakon carry-forwarda pao je
   > 20 %); zlatni izlazi sažete baze nisu jednaki punoj; testovi ne prolaze; paket je veći
   od 220 MB ili datoteka veća od 95 MB. Izvor ne prekida deploy (Korak 8): izostali ili prepolovljeni lanac
   zadržava cijene najviše 7 dana (`CARRY_DAYS`, uz `stale_days`), a on i ukupni pad sirovih cijena > 20 % javljaju
   se kao `::warning::` i u sažetku pokretanja.

## 4. Postavke (po želji: Project Settings → Environment Variables)

Zadane vrijednosti su u `api/index.py`: `MM_ALLOWED_HOSTS=*.vercel.app`, `TRUSTED_PROXY=vercel`,
`MM_RATE_IP=60`, `MM_RATE_SESSION=30`, `MM_RATE_GLOBAL=600` (u minuti, po instanci funkcije). Za vlastitu domenu
postavi npr. `MM_ALLOWED_HOSTS=*.vercel.app,cijene.example.hr`. Za strogo ograničenje upita koristi Vercel Firewall
(brojači u poslužitelju vrijede za jednu instancu).

## 5. Dodavanje u Claude

claude.ai (ili Claude Desktop) → **Settings → Connectors → Add custom connector**:
- Name: `Mealmeter`
- URL: `https://<host>/mcp`
- bez prijave (OAuth nije potreban; podaci su javni i samo za čitanje).

Zatim u razgovoru uključi konektor i pitaj npr. "Koliko u Osijeku koštaju sastojci za palačinke za 4 osobe?".
