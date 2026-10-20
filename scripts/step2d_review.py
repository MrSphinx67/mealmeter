"""Izvještaj za pregled Koraka 2D: docs/STEP2D_REVIEW.md.

Upotreba: python scripts/step2d_review.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import md_table  # noqa: E402

from mealmeter.staples import BKEY_SQL  # noqa: E402

OUT = Path("docs/STEP2D_REVIEW.md")


def old_membership_sql() -> str:
    """Pravilo prije Koraka 2D: grupa pripada ako barem jedan njezin (neizbačeni) proizvod prolazi pravila,
    a nijedan nije isključen."""
    return f"""
        SELECT ps.staple, {BKEY_SQL} AS bkey,
               bool_or(NOT ps.excluded) AND NOT bool_or(ps.excluded) AS old_member
        FROM clean.product_staples ps JOIN clean.products p USING (chain, product_id)
        WHERE ps.drop_reason IS NULL GROUP BY ALL"""


def section_groups(con) -> str:
    cmp = f"""
        SELECT g.staple, g.bkey, g.status, g.n_chains, g.share_match, g.share_excluded,
               coalesce(o.old_member, false) AS old_member
        FROM clean.staple_groups g LEFT JOIN ({old_membership_sql()}) o USING (staple, bkey)
        WHERE g.n_usable > 0 OR o.old_member
    """  # grupe samo od izbačenih proizvoda (pakiranje) ne mijenjaju izbor
    per = con.execute(f"""
        SELECT staple, count(*) FILTER (WHERE old_member), count(*) FILTER (WHERE status = 'member'),
               count(*) FILTER (WHERE status = 'ambiguous'),
               count(*) FILTER (WHERE old_member AND status <> 'member'),
               count(*) FILTER (WHERE NOT old_member AND status = 'member')
        FROM ({cmp}) GROUP BY staple
        HAVING count(*) FILTER (WHERE old_member AND status <> 'member') > 0
            OR count(*) FILTER (WHERE NOT old_member AND status = 'member') > 0
        ORDER BY 5 DESC, 6 DESC""").fetchall()
    con.execute("SELECT setseed(0.21)")
    examples = con.execute(f"""
        SELECT c.staple, c.bkey, CASE WHEN c.old_member THEN 'član → ' || c.status ELSE 'izvan → član' END,
               c.n_chains, round(100 * c.share_match), round(100 * c.share_excluded),
               (SELECT string_agg(DISTINCT p.chain || ': ' || p.name, '; ') FROM clean.products p
                 WHERE {BKEY_SQL} = c.bkey)
        FROM ({cmp}) c WHERE c.old_member <> (c.status = 'member') AND c.n_chains > 1
        ORDER BY random() LIMIT 30""").fetchall()
    return "\n".join([
        "## 1. Pripadnost grupe (EAN) namirnici", "",
        "Grupa pripada namirnici (`clean.staple_groups.status = 'member'`) ako naziv prolazi pravila u više od "
        "50 % lanaca grupe i nijedan isključeni naziv nema udio ≥ 25 % lanaca; inače je `ambiguous` i nije u "
        "zadanom izboru (`find_products(include_ambiguous=True)` je vraća); `excluded` ako nijedan naziv ne prolazi. Prije: dovoljan je bio jedan naziv, "
        "a bilo koji isključeni naziv rušio je cijelu grupu. Atributi grupe (`clean.staple_group_attrs`): "
        "vrijednost iz naziva ima prednost pred zadanom, zatim broj lanaca. Neprehrambeni član (kategorija) "
        "ne računa se kao pogodak naziva.", "",
        "**Cijena pravila:** grupe u kojima većina lanaca proizvod zove skraćeno ili samo markom ispadaju "
        "(„PRAŠ. PEC. 12 g Dr.Oetker“, „FUŽI 250g AURELIA“, „PASTA ZARA 573 SPIRALI“, „SIR ORODUR“), jer "
        "`must_match` ne pogađa takve nazive. Najviše gubi tjestenina (nazivi oblika bez riječi tjestenina). "
        "Rješenje bi bili sinonimi oblika u `must_match` (fuži, spirali, penne…) ili niži prag za grupe bez "
        "isključenih naziva; nisam ih uvodio jer pravilo traži većinu.", "",
        "Namirnice s promjenama (broj grupa):", "",
        md_table(["namirnica", "članova prije", "članova sada", "dvosmislenih", "ispalo", "ušlo"], per), "",
        "30 nasumičnih promijenjenih grupa (s više od jednog lanca):", "",
        md_table(["namirnica", "grupa", "promjena", "lanaca", "% naziva namirnice", "% isključenog naziva",
                  "nazivi"], examples),
    ])


SECTIONS = [section_groups]


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    parts = [f"# Pregled Koraka 2D (arhiva {date.isoformat()})", "",
             "Izvještaj generira `scripts/step2d_review.py` nad izgrađenom bazom.", ""]
    parts += [f(con) + "\n" for f in SECTIONS]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT}: {len(SECTIONS)} odjeljaka")


if __name__ == "__main__":
    main()
