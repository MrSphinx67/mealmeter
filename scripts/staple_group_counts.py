"""Broj grupa (isti EAN ili lanac + naziv) po namirnici: uključenih i isključenih, kao JSON.

Upotreba: python scripts/staple_group_counts.py [db_path] > counts.json
"""

import json
import sys

import duckdb

con = duckdb.connect(sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb", read_only=True)
rows = con.execute("""
    WITH g AS (
      SELECT p.chain, p.product_id,
             CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END AS gkey
      FROM clean.products p
    ),
    s AS (
      SELECT ps.staple, g.gkey, bool_or(NOT ps.excluded) AS ok, bool_or(ps.excluded) AS bad
      FROM clean.product_staples ps JOIN g USING (chain, product_id) GROUP BY ALL
    )
    SELECT staple, count(*) FILTER (WHERE ok AND NOT bad), count(*) FILTER (WHERE bad)
    FROM s GROUP BY staple ORDER BY staple
""").fetchall()
print(json.dumps({k: {"groups": a, "excluded": b} for k, a, b in rows}, ensure_ascii=False, indent=1))
