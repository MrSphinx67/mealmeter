"""Učitaj jednu dnevnu arhivu cijene.dev u DuckDB (sirove tablice), bez normalizacije.

Upotreba: python scripts/load.py <extracted_dir> <YYYY-MM-DD> <db_path>
"""

import sys
from pathlib import Path

import duckdb

from mealmeter.build import load_raw

root, archive_date, db_path = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
con = duckdb.connect(db_path)
load_raw(con, root, archive_date)
for t in ("stores", "products", "prices"):
    print(t, con.execute(f"SELECT count(*) FROM {t}").fetchone()[0])
