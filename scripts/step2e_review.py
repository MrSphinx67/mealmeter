"""Izvještaj za pregled Koraka 2E: docs/STEP2E_REVIEW.md (detalji; sažetak je docs/REVIEW_2E.md).

Upotreba: python scripts/step2e_review.py [db_path] [odjeljak ...]   (zadano: data/mealmeter.duckdb, svi)
"""

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import md_table  # noqa: E402

from mealmeter.staples import BKEY_SQL  # noqa: E402

OUT = Path("docs/STEP2E_REVIEW.md")
DATA = Path("docs/data")
# grupe kojima je Korak 2E.1 promijenio status (staple, bkey, before, after), iz snimke prije promjene
GROUP_CHANGES = DATA / "groups_changes_2e1.csv"


def _names(bkey_col: str = "g.bkey") -> str:
    return f"""(SELECT string_agg(DISTINCT p.chain || ': ' || p.name, '; ') FROM clean.products p
                WHERE {BKEY_SQL} = {bkey_col})"""


def section_tiers(con) -> str:
    per = con.execute("""
        SELECT staple, count(*) FILTER (WHERE match_quality = 'strong'), count(*) FILTER (WHERE match_quality = 'weak'),
               count(*) FILTER (WHERE status = 'ambiguous'), count(*) FILTER (WHERE status = 'excluded')
        FROM clean.staple_groups GROUP BY staple ORDER BY staple""").fetchall()
    con.execute("SELECT setseed(0.17)")
    weak = con.execute(f"""
        SELECT g.staple, g.bkey, round(100 * g.share_match), {_names()} FROM clean.staple_groups g
        WHERE g.match_quality = 'weak' ORDER BY random() LIMIT 30""").fetchall()
    changes = f"read_csv('{GROUP_CHANGES}', header=true, all_varchar=true, quote='\"')"
    con.execute("SELECT setseed(0.18)")
    moved = con.execute(f"""
        SELECT g.staple, g.bkey, round(100 * g.share_match), round(100 * g.share_excluded), {_names()}
        FROM clean.staple_groups g JOIN {changes} o USING (staple, bkey)
        WHERE o.before = 'member' AND o.after = 'ambiguous' ORDER BY random() LIMIT 30""").fetchall()
    n_moved = con.execute(f"""
        SELECT count(*) FILTER (WHERE before = 'member' AND after = 'ambiguous'),
               count(*) FILTER (WHERE before <> 'member' AND after = 'member'),
               count(*) FILTER (WHERE before = 'member' AND after = 'excluded') FROM {changes}""").fetchone()
    return "\n".join([
        "## 1. Pripadnost grupe: tri razine", "",
        "m = udio lanaca čiji naziv prolazi `must_match` bez `must_not_match`, x = udio lanaca čiji naziv pogađa "
        "`must_not_match`. **Snažni** član: m > 50 % i x < 10 %. **Slabi** (`match_quality = 'weak'`): x = 0, "
        "m ≥ 25 %, jedinica spojiva, barem jedan proizvod unutar min/max pakiranja i medijan cijene po jedinici u "
        "granicama; u zadanom je izboru, ali ispod snažnih i označen (`find_products.match_quality`, u košarici "
        "zastavica `weak_match`). Inače `ambiguous` (m > 0) ili `excluded` (m = 0).", "",
        f"Prema pravilu iz 2D: {n_moved[0]} grupa prelazi iz člana u `ambiguous`, {n_moved[2]} u `excluded`, "
        f"a {n_moved[1]} postaje član.", "",
        md_table(["namirnica", "snažnih", "slabih", "dvosmislenih", "isključenih"], per), "",
        "Napomena: među slabim članovima ima krivih pogodaka kad drugi lanci proizvod zovu samo markom, a jedan "
        "naziv prolazi `must_match` (npr. „ČOKOLADA RIKI PŠENICA I MED“ kao med, „MINI CROASANI S MASLACEM“ kao "
        "maslac). Rangirani su ispod snažnih i označeni; točka 4 (kratice, `must_not_match`) dio njih uklanja.", "",
        "30 slučajnih slabih članova:", "",
        md_table(["namirnica", "grupa", "m %", "nazivi po lancu"], weak), "",
        "30 grupa koje prelaze iz člana (2D) u `ambiguous`:", "",
        md_table(["namirnica", "grupa", "m %", "x %", "nazivi po lancu"], moved),
    ])


SECTIONS = {"1": section_tiers}


def main() -> None:
    args = sys.argv[1:]
    db_path = args.pop(0) if args and not args[0].isdigit() else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    parts = [f"# Pregled Koraka 2E (arhiva {date.isoformat()})", "",
             "Generira `scripts/step2e_review.py` nad izgrađenom bazom; sažetak je u REVIEW_2E.md.", ""]
    parts += [f(con) + "\n" for key, f in SECTIONS.items() if not args or key in args]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT}: {len(parts) - 4} odjeljaka")


if __name__ == "__main__":
    main()
