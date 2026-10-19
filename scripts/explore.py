"""Korak 0: pregled CSV datoteka iz dnevne arhive cijene.dev."""

import sys
from pathlib import Path

import duckdb

root = Path(sys.argv[1])
con = duckdb.connect()

for csv in sorted(root.glob("*/*.csv")):
    rel = csv.relative_to(root)
    # all_varchar: gledamo sirove vrijednosti, bez pogađanja tipova
    src = f"read_csv('{csv}', header=true, all_varchar=true)"
    cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM {src}").fetchall()]
    n = con.execute(f"SELECT count(*) FROM {src}").fetchone()[0]
    print(f"\n### {rel}  ({n} redaka)")
    print("  stupci:", ", ".join(cols))
    for row in con.execute(f"SELECT * FROM {src} LIMIT 5").fetchall():
        print("  ", row)
