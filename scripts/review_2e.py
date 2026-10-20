"""Sažetak Koraka 2E za razgovor: docs/REVIEW_2E.md, najviše 150 redaka (detalji: STEP2E_REVIEW.md).

Upotreba: python scripts/review_2e.py [db_path]
"""

import json
import random
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import hr, md_table  # noqa: E402
from step2e_review import DATA, FUNNEL_CHAINS, FUNNEL_STAGES, FUNNEL_STAPLES, _names, funnel  # noqa: E402

from mealmeter.basket import plan_basket  # noqa: E402

OUT = Path("docs/REVIEW_2E.md")
MAX_LINES = 150


def tiers(con) -> list[str]:
    rows = con.execute("""
        SELECT staple, count(*) FILTER (WHERE match_quality = 'strong'), count(*) FILTER (WHERE match_quality = 'weak'),
               count(*) FILTER (WHERE status = 'ambiguous'), count(*) FILTER (WHERE status = 'excluded')
        FROM clean.staple_groups GROUP BY staple ORDER BY staple""").fetchall()
    half = (len(rows) + 1) // 2
    pairs = [(*a, *b) for a, b in zip(rows[:half], rows[half:] + [("",) * 5])]
    head = ["namirnica", "snaž.", "slab.", "dvos.", "isklj."]
    return ["## Razine pripadnosti po namirnici (snažni / slabi / dvosmisleni / isključeni)", "",
            md_table(head + head, pairs), ""]


def samples(con) -> list[str]:
    con.execute("SELECT setseed(0.17)")
    weak = con.execute(f"""SELECT g.staple, {_names()} FROM clean.staple_groups g WHERE g.match_quality = 'weak'
                           ORDER BY random() LIMIT 5""").fetchall()
    ch1 = f"read_csv('{DATA / 'groups_changes_2e1.csv'}', header=true, all_varchar=true, quote='\"')"
    moved = con.execute(f"""SELECT g.staple, {_names()} FROM clean.staple_groups g JOIN {ch1} o USING (staple, bkey)
                            WHERE o.before = 'member' AND g.status = 'ambiguous' ORDER BY random() LIMIT 4""").fetchall()
    ch4 = f"read_csv('{DATA / 'groups_changes_2e4.csv'}', header=true, all_varchar=true, quote='\"')"
    back = con.execute(f"""SELECT o.staple, {_names()} FROM {ch4} o JOIN clean.staple_groups g USING (staple, bkey)
                           WHERE o.before <> 'member' AND o.after = 'member' ORDER BY random() LIMIT 5""").fetchall()
    ch5 = f"read_csv('{DATA / 'food_changes_2e5.csv'}', header=true, all_varchar=true, quote='\"')"
    cv = con.execute(f"""SELECT p.chain, p.name, o.before FROM clean.products p JOIN {ch5} o USING (chain, product_id)
                         WHERE o.after = 'hrana' AND regexp_matches(p.name_norm, '(^| )cvijet') ORDER BY random() LIMIT 5""").fetchall()
    cut = [(a, b[:110]) for a, b in weak]
    return ["## Uzorci", "", "Slabi članovi (točka 1):", "", md_table(["namirnica", "nazivi po lancu"], cut), "",
            "Iz člana u `ambiguous` (točka 1):", "", md_table(["namirnica", "nazivi po lancu"], [(a, b[:110]) for a, b in moved]), "",
            "Vraćeno sinonimima i kraticama (točka 4):", "", md_table(["namirnica", "nazivi po lancu"],
                                                                     [(a, b[:110]) for a, b in back]), "",
            "„cvijet“ vraćen u hranu (točka 5):", "", md_table(["lanac", "naziv", "prije"], cv), ""]


def funnel_lines(con) -> list[str]:
    rows = []
    for key in FUNNEL_STAPLES:
        counts, lost = funnel(con, key)
        total = [sum(counts[ch][i] for ch in FUNNEL_CHAINS) for i in range(len(FUNNEL_STAGES))]
        reasons = {}
        for _, _, stage in lost:
            reasons[stage] = reasons.get(stage, 0) + 1
        top = max(reasons, key=reasons.get) if reasons else "-"
        rows.append((key, " → ".join(map(str, total)), top))
    return ["## Lijevak za svježe povrće (točka 9, zbroj 8 lanaca)", "",
            f"Faze: {' → '.join(FUNNEL_STAGES)}. Po lancu u STEP2E_REVIEW.md.", "",
            md_table(["namirnica", "proizvoda po fazi", "najčešći gubitak"], rows), ""]


def prefix_lines(con) -> list[str]:
    n_rules, n_test, acc = con.execute("""SELECT count(*), sum(n_test), sum(n_test * accuracy) / sum(n_test)
                                          FROM clean.prefix_rules WHERE applied""").fetchone()
    by = con.execute("""SELECT food_group, count(*) FROM clean.products WHERE chain = 'plodine'
                        AND category_source = 'prefix' GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    unk = con.execute("SELECT count(*) FROM clean.products WHERE chain = 'plodine' AND food_group = 'unknown'").fetchone()[0]
    return ["## Plodine: prefiks šifre (točka 11)", "",
            f"{n_rules} prefiksa (čistoća ≥ 95 %, ≥ 30 primjera), točnost na odloženih 20 %: {hr(100 * acc, 1)} % "
            f"({n_test} proizvoda). Iz `unknown` izlazi {sum(n for _, n in by)} Plodina ("
            + ", ".join(f"{g} {n}" for g, n in by) + f"); ostaje {unk}.", ""]


def basket_lines(con) -> list[str]:
    out = ["## Košarice u Osijeku", ""]
    for recipe in ("test_palacinke", "test_bolonjez"):
        data = json.loads(Path(f"data/recipes/{recipe}.json").read_text(encoding="utf-8"))
        res = plan_basket(data["ingredients"], "Osijek", con=con)
        best = res["best_store"]
        rows = [(it["ingredient"], it["name"][:34], f"{it['n_packs']} x {hr(it['pack_qty'], 0)} {it['need_unit']}"
                 if it["n_packs"] else "na vagu", hr(it["cost_pack"]), hr(it["cost_used"]),
                 f"{it['unit_confidence']}/{it['pack_source']}" + (" slabi" if "weak_match" in it["flags"] else ""))
                for it in best["items"]]
        out += [f"**{data['name']}**: {best['chain']}, {best['address']} · {best['n_matched']}/{best['n_ingredients']} · "
                f"**total_to_buy {hr(best['total_to_buy'])} €**, total_used {hr(best['total_used'])} € · {best['date_hr']}", "",
                md_table(["sastojak", "proizvod", "pakiranje", "cost_pack €", "cost_used €", "pouzdanost"], rows), ""]
    return out


def main() -> None:
    random.seed(0)
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    lines = [f"# Pregled za razgovor: Korak 2E (arhiva {date.isoformat()})", "",
             "Generira `scripts/review_2e.py`; detalji u STEP2E_REVIEW.md i DECISIONS.md (68–79).", ""]
    lines += tiers(con) + samples(con) + funnel_lines(con) + prefix_lines(con) + basket_lines(con)
    text = "\n".join(lines).rstrip() + "\n"
    n = text.count("\n")
    if n > MAX_LINES:
        raise SystemExit(f"{OUT}: {n} redaka (najviše {MAX_LINES})")
    OUT.write_text(text, encoding="utf-8")
    print(f"{OUT}: {n} redaka")


if __name__ == "__main__":
    main()
