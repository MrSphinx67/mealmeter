# Mealmeter

Besplatan open-source MCP connector koji za jelo ili sastojke i grad pronalazi cijene u hrvatskim trgovinama (podaci: dnevne CSV arhive s [cijene.dev](https://cijene.dev)).

## Lokalno pokretanje

```sh
uv sync
curl -o data/raw/2026-10-19.zip https://api.cijene.dev/v0/archive/2026-10-19.zip
unzip data/raw/2026-10-19.zip -d data/raw/extracted
uv run python scripts/load.py data/raw/extracted 2026-10-19 data/mealmeter.duckdb
uv run python scripts/build_clean.py
uv run python -m mealmeter.cli find "brašno glatko" --city Osijek
uv run python -m mealmeter.cli prices 3850104223624 --city Osijek
uv run pytest
```

Dokumentacija: [docs/SCHEMA.md](docs/SCHEMA.md) (podaci), [docs/DECISIONS.md](docs/DECISIONS.md) (odluke).
