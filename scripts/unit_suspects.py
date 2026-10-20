"""Proizvodi s unit_suspect (gramatura iz stupca unit): broj po lancu i primjeri s razlogom.

Upotreba: python scripts/unit_suspects.py [db_path] [n]   (koristi ga i review_4.py)
"""

import sys

import duckdb

from mealmeter.staples import STAPLE_PPU_SQL, UNIT_SUSPECT_EAN_RATIO, UNIT_SUSPECT_MIN_CHAINS


def unit_suspects(con, n: int = 30) -> tuple[list[tuple], list[tuple]]:
    by_chain = con.execute("""SELECT chain, count(*) FROM clean.product_staples WHERE unit_suspect
                              GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    rows = con.execute(f"""
        WITH u AS (
          SELECT ps.staple, ps.chain, ps.product_id, p.name, p.unit, p.ean_norm, p.ean_global, ps.unit_suspect,
                 any_value(coalesce(ps.ppu_min, CASE WHEN r.range_source = 'manual' THEN r.ppu_min END)) AS lo,
                 any_value(coalesce(ps.ppu_max, CASE WHEN r.range_source = 'manual' THEN r.ppu_max END)) AS hi,
                 median({STAPLE_PPU_SQL}) AS ppu
          FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
          JOIN clean.prices c USING (chain, product_id) JOIN clean.products p USING (chain, product_id)
          WHERE NOT ps.excluded AND ps.drop_reason IS NULL
          GROUP BY ps.staple, ps.chain, ps.product_id, p.name, p.unit, p.ean_norm, p.ean_global, ps.unit_suspect
        )
        SELECT u.chain, u.staple, u.name, u.unit, u.ppu, u.lo, u.hi,
               (SELECT count(DISTINCT o.chain) FROM u o WHERE u.ean_global AND o.ean_norm = u.ean_norm
                  AND o.staple = u.staple AND o.chain <> u.chain),
               (SELECT median(o.ppu) FROM u o WHERE u.ean_global AND o.ean_norm = u.ean_norm
                  AND o.staple = u.staple AND o.chain <> u.chain)
        FROM u WHERE u.unit_suspect ORDER BY u.chain, u.staple, u.name LIMIT {n}""").fetchall()
    lo_r, hi_r = UNIT_SUSPECT_EAN_RATIO
    out = []
    for chain, staple, name, unit, ppu, lo, hi, n_other, med in rows:
        if lo is not None and ppu < lo:
            why = f"ispod granice {lo:g}"
        elif hi is not None and ppu > hi:
            why = f"iznad granice {hi:g}"
        elif n_other and n_other >= UNIT_SUSPECT_MIN_CHAINS and med:
            why = f"{ppu / med:.2f}x medijana EAN-a u {n_other} lanaca"
        else:
            why = "?"
        out.append((chain, staple, name, unit, round(ppu, 2), why))
    return by_chain, out


if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    by_chain, rows = unit_suspects(duckdb.connect(db, read_only=True), int(sys.argv[2]) if len(sys.argv) > 2 else 30)
    print("po lancu:", by_chain)
    for r in rows:
        print(" ", *r)
