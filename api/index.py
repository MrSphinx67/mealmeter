"""Vercel ulazna točka (Korak 5V): ASGI aplikacija `app` oko HTTP poslužitelja (/mcp, /healthz, /).

Vercel učitava varijablu `app` iz api/index.py: Python backend je jedna funkcija ("python") i Vercel joj šalje SVE
putanje i metode s izvornom putanjom (ruta buildera "/(.*)" -> funkcija, request.path = "/$1"), pa vercel.json nema
rewrite. Rewrite na /api/index bi aplikaciji dao prepisanu putanju (Korak 5V3: svaki GET je vraćao početnu stranicu,
a POST /mcp je dobivao 405 od Vercela). Omotač i dalje "/api/index/..." vraća na ostatak putanje. Dokumentacija ne kaže
šalje li Python runtime ASGI lifespan, a MCP session manager bez njega pada ("Task group is not initialized"),
pa ga omotač pokreće sam: pri prvom zahtjevu u zasebnom dugotrajnom zadatku (ne u zadatku zahtjeva). Ako
platforma ipak pošalje lifespan, omotač ga obrađuje isto.

Baza: MM_DB (zadano data/compact.duckdb uz kod, uz nju data/compact_prices.duckdb, Korak 12), samo za čitanje
(ATTACH ... READ_ONLY); privremene datoteke DuckDB-a u /tmp (MM_DUCKDB_TEMP), jer je na Vercelu samo /tmp zapisiv.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))  # paket mealmeter iz repozitorija, i kad nije instaliran

os.environ.setdefault("MM_DB", str(ROOT / "data" / "compact.duckdb"))
os.environ.setdefault("MM_DUCKDB_TEMP", "/tmp")
# Vercel (Korak 5V.4); svaka se može promijeniti u Project Settings -> Environment Variables (npr. vlastita domena)
os.environ.setdefault("MM_ALLOWED_HOSTS", "*.vercel.app")
os.environ.setdefault("MM_ALLOWED_ORIGINS", "https://claude.ai,https://*.claude.ai,https://*.vercel.app")
os.environ.setdefault("TRUSTED_PROXY", "vercel")  # IP klijenta iz Vercelovih zaglavlja (x-vercel-forwarded-for)
os.environ.setdefault("MM_RATE_IP", "60")  # po instanci funkcije: Fluid compute ih može imati više
os.environ.setdefault("MM_RATE_SESSION", "30")
os.environ.setdefault("MM_RATE_GLOBAL", "600")

from mealmeter.asgi import LifespanOnDemand, inner_app  # noqa: E402
from mealmeter.server import create_server, http_app  # noqa: E402

_http = http_app(create_server(), host="0.0.0.0")
app = LifespanOnDemand(_http, inner_app(_http))
