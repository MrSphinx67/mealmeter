"""Sažetak Koraka 4 za razgovor: docs/REVIEW_4.md, najviše 100 redaka.

Upotreba: python scripts/review_4.py [db_path]
"""

import json
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import hr, md_table  # noqa: E402
from unit_suspects import unit_suspects  # noqa: E402
from weak_suspects import weak_early_sample  # noqa: E402

from mealmeter.basket import plan_basket  # noqa: E402

OUT = Path("docs/REVIEW_4.md")
MAX_LINES = 100


def point01(con) -> list[str]:
    by_chain, rows = unit_suspects(con, 30)
    total = sum(n for _, n in by_chain)
    return ["## 0.1 unit_suspect (izvan plausible granica ili 0,4–2,5x medijana istog EAN-a u ≥ 2 druga lanca)", "",
            md_table(["lanac", "označenih"], by_chain + [("ukupno", total)]), "",
            f"Svi primjeri ({len(rows)}; traženo do 30). Označeni se rangiraju niže i u košarici su samo rezerva.", "",
            md_table(["lanac", "namirnica", "naziv", "unit", "€/jed", "razlog"],
                     [(c, s, n[:40], u, hr(p), w) for c, s, n, u, p, w in rows]), ""]


def point02(con) -> list[str]:
    total, rows = weak_early_sample(con, 40)
    return [f"## 0.2 Slabi članovi koji prolaze test riječi: 40 slučajnih od {total}", "",
            md_table(["namirnica", "m %", "nazivi po lancu"], [(s, f"{m:g}", names[:110]) for s, m, names in rows]), ""]


def baskets(con) -> list[str]:
    out = ["## Košarice u Osijeku", ""]
    for recipe in ("test_palacinke", "test_bolonjez"):
        data = json.loads(Path(f"data/recipes/{recipe}.json").read_text(encoding="utf-8"))
        best = plan_basket(data["ingredients"], "Osijek", con=con)["best_store"]
        items = "; ".join(f"{it['ingredient']}: {it['name'][:30]} {hr(it['cost_pack'])}/{hr(it['cost_used'])}"
                          + (" (slabi)" if it.get("match_quality") == "weak" else "")
                          + (" (rezerva)" if it.get("fallback") else "") for it in best["items"])
        out += [f"**{data['name']}**: {best['chain']}, {best['address']} · {best['n_matched']}/{best['n_ingredients']} · "
                f"total_to_buy **{hr(best['total_to_buy'])} €**, total_used {hr(best['total_used'])} € · {best['date_hr']}",
                f"Stavke (cost_pack/cost_used €): {items}.", ""]
    return out


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    lines = [f"# Pregled za razgovor: Korak 4 (arhiva {date.isoformat()}; `scripts/review_4.py`, odluke 88–91)", ""]
    lines += point01(con) + point02(con) + baskets(con)
    text = "\n".join(lines).rstrip() + "\n"
    n = text.count("\n")
    if n > MAX_LINES:
        raise SystemExit(f"{OUT}: {n} redaka (najviše {MAX_LINES})")
    OUT.write_text(text, encoding="utf-8")
    print(f"{OUT}: {n} redaka")


if __name__ == "__main__":
    main()
