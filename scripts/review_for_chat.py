"""Kratki pregled za razgovor (Korak 2D, točka 14): docs/REVIEW_FOR_CHAT.md, najviše 150 redaka.

Sadrži košarice (palačinke, bolonjez u Osijeku), mjere i težine komada iz data/units.yaml, pokrivenost
(točka 11) i rezultat dnevnog ažuriranja (točka 13, iz docs/data/update_<datum>.txt).

Upotreba: python scripts/review_for_chat.py [db_path]
"""

import json
import sys
from pathlib import Path

import duckdb
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import hr, md_table  # noqa: E402
from step2d_review import COVERAGE_CHAINS, coverage  # noqa: E402

from mealmeter.basket import plan_basket  # noqa: E402
from mealmeter.units import UNITS_PATH  # noqa: E402

OUT = Path("docs/REVIEW_FOR_CHAT.md")
MAX_LINES = 150
RECIPES = ("test_palacinke", "test_bolonjez")


def basket_lines(con, recipe: str) -> list[str]:
    data = json.loads(Path(f"data/recipes/{recipe}.json").read_text(encoding="utf-8"))
    res = plan_basket(data["ingredients"], "Osijek", con=con)
    best = res["best_store"]
    rows = [(it["ingredient"], it["name"][:38], f"{it['n_packs']} x {hr(it['pack_qty'], 0)} {it['need_unit']}" if it["n_packs"] else "na vagu",
             hr(it["cost_pack"]), hr(it["cost_used"]), f"{it['unit_confidence']}/{it['pack_source']}")
            for it in best["items"]]
    extra = [f"nije povezano: {u['name']} ({u['reason']})" for u in res["unmatched"]]
    extra += [f"pitanje: {a['name']}: {a['ambiguity']['question']}" for a in res["ambiguous"]]
    return [f"**{data['name']}**: {best['chain']}, {best['address']} · {best['n_matched']}/{best['n_ingredients']} "
            f"sastojaka · za kupiti {hr(best['total_to_buy'])} € · utrošeno {hr(best['total_used'])} € · "
            f"{res.get('date_hr', '')}", "",
            md_table(["sastojak", "proizvod", "pakiranje", "cost_pack €", "cost_used €", "pouzdanost"], rows),
            *([""] + [f"- {e}" for e in extra] if extra else []), ""]


def units_lines() -> list[str]:
    raw = yaml.safe_load(UNITS_PATH.read_text(encoding="utf-8"))
    measures = ", ".join(f"{k} {hr(m['ml'], 1).rstrip('0').rstrip(',')} ml" for k, m in raw["measures"].items())

    def columns(items, k=3):
        """Parovi (naziv, vrijednost) u k stupaca po retku, da tablica bude kratka."""
        items = list(items)
        n = -(-len(items) // k)
        cols = [items[i * n:(i + 1) * n] + [("", "")] * (n - len(items[i * n:(i + 1) * n])) for i in range(k)]
        return [tuple(x for col in cols for x in col[r]) for r in range(n)]

    dens = columns((k, hr(v["g_per_ml"])) for k, v in raw["densities"].items())
    pieces = columns((k + (f" ({v['piece']})" if v.get("piece") else ""), f"{v['g']:g}") for k, v in raw["pieces"].items())
    return ["## Mjere i težine komada (data/units.yaml, sve procjene)", "", f"Mjere: {measures}.", "",
            md_table(["namirnica", "g/ml"] * 3, dens), "",
            md_table(["komad", "g"] * 3, pieces), ""]


def coverage_lines(con) -> list[str]:
    rows = []
    for c in coverage(con):
        d, s = c["default"], c["strict"]
        rows.append((c["staple"], len(d), *[d.get(ch, 0) for ch in COVERAGE_CHAINS],
                     s.get("plodine", 0) - d.get("plodine", 0)))
    short = [ch[:5] for ch in COVERAGE_CHAINS]
    return ["## Pokrivenost (točka 11)", "",
            "Lanaca s barem jednim proizvodom u zadanom izboru, i broj proizvoda po lancu. „+Plod“ je procjena dobitka "
            "za Plodine uz strogo pozitivni `food_unverified` (nije primijenjeno).", "",
            md_table(["namirnica", "lanaca", *short, "+Plod"], rows), ""]


def update_lines() -> list[str]:
    files = sorted(Path("docs/data").glob("update_*.txt"))
    if not files:
        return ["## Dnevno ažuriranje (točka 13)", "", "(nema zapisa)"]
    text = files[-1].read_text(encoding="utf-8").splitlines()
    keep = [ln for ln in text if ln.strip().startswith(("datum:", "lanaca:", "trgovina:", "proizvoda:", "redaka cijena:",
                                                         "!", "UKUPNO"))]
    return ["## Dnevno ažuriranje (točka 13)", "",
            f"`scripts/update.py` uzima najnoviju arhivu iz /v0/list; zapis: `{files[-1]}`.", "", "```",
            *[ln.rstrip() for ln in keep], "```"]


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    lines = [f"# Pregled za razgovor: Korak 2D (arhiva {date.isoformat()})", "",
             "## Košarice u Osijeku (najbolja trgovina; generira `scripts/review_for_chat.py`, detalji u "
             "STEP2D_REVIEW.md)", ""]
    for recipe in RECIPES:
        lines += basket_lines(con, recipe)
    lines += units_lines() + coverage_lines(con) + update_lines()
    text = "\n".join(lines).rstrip() + "\n"
    n = text.count("\n")
    if n > MAX_LINES:
        raise SystemExit(f"{OUT}: {n} redaka (najviše {MAX_LINES})")
    OUT.write_text(text, encoding="utf-8")
    print(f"{OUT}: {n} redaka")


if __name__ == "__main__":
    main()
