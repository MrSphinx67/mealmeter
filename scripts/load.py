"""Korak 0: učitaj jednu dnevnu arhivu cijene.dev u DuckDB, bez normalizacije.

Upotreba: python scripts/load.py <extracted_dir> <YYYY-MM-DD> <db_path>
"""

import sys
from pathlib import Path

import duckdb

root, archive_date, db_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
con = duckdb.connect(db_path)

PRICE_COLS = ["price", "unit_price", "best_price_30", "anchor_price", "special_price"]


def raw(chain: str, name: str) -> str:
    # Sve kao tekst: šifre imaju vodeće nule, a cijene provjeravamo zasebno
    return f"read_csv('{root / chain / name}', header=true, all_varchar=true)"


chains = sorted(p.name for p in root.iterdir() if p.is_dir())

con.execute("DROP TABLE IF EXISTS stores; DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS prices")
for i, chain in enumerate(chains):
    verb = "CREATE TABLE {} AS" if i == 0 else "INSERT INTO {}"
    con.execute(f"{verb.format('stores')} SELECT '{chain}' AS chain, * FROM {raw(chain, 'stores.csv')}")
    con.execute(f"{verb.format('products')} SELECT '{chain}' AS chain, * FROM {raw(chain, 'products.csv')}")
    casts = ", ".join(f"TRY_CAST({c} AS DECIMAL(10,2)) AS {c}" for c in PRICE_COLS)
    con.execute(
        f"{verb.format('prices')} SELECT '{chain}' AS chain, store_id, product_id, {casts}, "
        f"DATE '{archive_date}' AS price_date FROM {raw(chain, 'prices.csv')}"
    )
    # Provjera: nijedna neprazna cijena ne smije pasti na castu
    bad = con.execute(
        f"SELECT count(*) FROM {raw(chain, 'prices.csv')} WHERE "
        + " OR ".join(f"({c} IS NOT NULL AND TRY_CAST({c} AS DECIMAL(10,2)) IS NULL)" for c in PRICE_COLS)
    ).fetchone()[0]
    if bad:
        print(f"UPOZORENJE {chain}: {bad} redaka s neparsabilnom cijenom")

for t in ("stores", "products", "prices"):
    print(t, con.execute(f"SELECT count(*) FROM {t}").fetchone()[0])
