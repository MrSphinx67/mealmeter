"""Slabi članovi koji izgledaju krivo: nijedan naziv grupe nema riječ namirnice među prve tri riječi.

Upotreba: python scripts/weak_suspects.py [db_path] [n]   (ispis; koristi ga i review_2f.py)
"""

import re
import sys

import duckdb

from mealmeter.staples import BKEY_SQL, load_staples


def weak_suspects(con, n: int = 20, seed: float = 0.4) -> tuple[int, int, list[tuple]]:
    staples = load_staples()
    rows = con.execute(f"""
        SELECT g.staple, g.bkey, round(100 * g.share_match),
               (SELECT list(DISTINCT p.chain || ': ' || p.name) FROM clean.products p WHERE {BKEY_SQL} = g.bkey),
               (SELECT list(DISTINCT p.match_norm) FROM clean.products p WHERE {BKEY_SQL} = g.bkey)
        FROM clean.staple_groups g WHERE g.match_quality = 'weak' ORDER BY g.staple, g.bkey""").fetchall()
    bad = [(st, bkey, m, "; ".join(names)) for st, bkey, m, names, norms in rows
           if not any(re.search(staples[st].early_regex, t or "") for t in norms)]
    import random
    random.Random(seed).shuffle(bad)
    return len(rows), len(bad), bad[:n]


if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    total, n_bad, sample = weak_suspects(duckdb.connect(db, read_only=True), int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    print(f"slabih: {total}, sumnjivih: {n_bad}")
    for row in sample:
        print(" ", row[0], row[1], f"m={row[2]:g}%", row[3][:150])


def weak_early_sample(con, n: int = 40, seed: float = 0.42) -> tuple[int, list[tuple]]:
    """Slučajni uzorak slabih članova koji prolaze test riječi (staple_groups.early_name), za pregled."""
    total = con.execute("SELECT count(*) FROM clean.staple_groups WHERE match_quality = 'weak' AND early_name").fetchone()[0]
    con.execute(f"SELECT setseed({seed})")
    rows = con.execute(f"""
        SELECT g.staple, round(100 * g.share_match),
               (SELECT string_agg(DISTINCT p.chain || ': ' || p.name, '; ') FROM clean.products p WHERE {BKEY_SQL} = g.bkey)
        FROM (SELECT * FROM clean.staple_groups WHERE match_quality = 'weak' AND early_name ORDER BY staple, bkey) g
        ORDER BY random() LIMIT {n}""").fetchall()
    return total, rows
