# Korak 5V2: manji paket za Vercel

| točka | stanje |
|---|---|
| 0 kako Vercel puni paket; Python 3.12; paket bez baze | gotovo |
| 1 veličina sažete baze po tablici i stupcu | - |
| 2 smanjena baza (isti view-ovi, isti rezultat) | - |
| 3 zlatni izlazi i mjerenja na novoj bazi | - |
| 4 `vercel build --prod` s bazom | - |

Ništa nije deployano.

## 0. Što ide u paket

**Ispravak 5V_STATUS:** dokumentacija kaže 500 MB za Python, ali alat za build (Vercel CLI 65.0.0, `@vercel/python`,
`dependency-externalizer`) radi drukčije:
- Prag je **225 MB** (`LAMBDA_SIZE_THRESHOLD_BYTES`). Paket do 225 MB ide cijeli (kod, datoteke iz `includeFiles`,
  ovisnosti u `_vendor/`).
- Iznad 225 MB, uz `uv.lock`, javni paketi s kompatibilnim wheelom **ne ulaze u paket**: instaliraju se pri hladnom
  startu u `/tmp/_vc_deps` (efemerni disk 500 MB), a u paket ulazi binarni `uv` (`_uv/`, ~50 MB). Ostatak
  (naše datoteke, privatni paketi, paketi bez kompatibilnog wheela i `uv`) mora stati u 225 MB. Inače:
  "exceeds the maximum function size (225 MB) even after optimizing dependencies".
- Kompatibilnost wheela: lokalno (bez `VERCEL_BUILD_IMAGE`) builder pretpostavlja **manylinux 2.17**. duckdb ima samo
  wheelove manylinux_2_26/2_28, pa je lokalno "bez kompatibilnog wheela" i uvijek u paketu (58 MB).
- "Large functions" (do 5 GB, beta) zaobilaze ovo uz `VERCEL_SUPPORT_LARGE_FUNCTIONS=1`; nisam ih koristio.
- Izvori: [Python runtime, controlling what gets bundled](https://vercel.com/docs/functions/runtimes/python#controlling-what-gets-bundled),
  [Python version](https://vercel.com/docs/functions/runtimes/python/python-version), kod
  `node_modules/vercel/node_modules/@vercel/python/dist/index.js`.

**Python 3.12:** Vercel uzima `.python-version` (3.14) čak i kad je u `.vercelignore`. Bez te datoteke uzima 3.14 iz
`requires-python = ">=3.12"` (najviša podržana). 3.12 bi tražio `requires-python` ograničen na 3.12, a to bi vezalo i
lokalni razvoj; ne može se odvojiti, a ne bi ni pomoglo, jer duckdb ostaje u paketu (manylinux 2.17 iznad).
`.python-version` je ostao 3.14.

**Paket bez baze** (`vercel build --prod`, zbroj datoteka iz `.vc-config.json` → `filePathMap`): **92,7 MB**; duckdb
57,7, cryptography 14,3, pydantic_core 4,9, pyyaml 2,7, pydantic 1,9, vercel_runtime 1,7, mcp 1,2 MB. Ispod 225 MB
nema vanjske instalacije, pa za paket ≤ 200 MB sažeta baza mora biti ≤ ~105 MB (sada 212,5 MB).

**Sigurnost:** u paketu je bio `.env.local` (i `.pytest_cache`). `.vercelignore` na `vercel build` ne djeluje, pa
`vercel.json` → `excludeFiles` sada izričito isključuje `.env*`, `.pytest_cache/**`, `__pycache__` i `_uv/**`;
provjereno: `.env*` više nije u paketu.
