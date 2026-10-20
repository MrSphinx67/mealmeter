"""Sažetak Koraka 2F za razgovor: docs/REVIEW_2F.md, najviše 100 redaka.

Upotreba: python scripts/review_2f.py [db_path]
"""

import json
import subprocess
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import hr, md_table  # noqa: E402
from step2e_review import FUNNEL_CHAINS  # noqa: E402
from weak_suspects import weak_suspects  # noqa: E402

from mealmeter.basket import plan_basket  # noqa: E402
from mealmeter.staples import STAPLE_PPU_SQL  # noqa: E402

UNIT_SUSPECT_RATIO = (0.6, 1.6)  # pravilo iz Koraka 2F (u Koraku 4 zamijenjeno, vidi staples.flag_unit_suspects)

OUT = Path("docs/REVIEW_2F.md")
MAX_LINES = 100
TESTS = {
    "2": ["tests/test_step2f.py::test_spageti_excludes_bucatini", "tests/test_step2f.py::test_product_without_required_attr_dropped"],
    "3": ["tests/test_step2f.py::test_loose_piece_with_global_ean"],
}


def run_tests(ids: list[str]) -> str:
    res = subprocess.run([sys.executable, "-m", "pytest", "-q", *ids], capture_output=True, text=True)
    last = [ln for ln in res.stdout.splitlines() if ln.strip()][-1]
    return f"{'prolazi' if res.returncode == 0 else 'NE PROLAZI'} ({last.strip()})"


def point1(con) -> list[str]:
    rows = con.execute("""SELECT chain, ean_note, count(DISTINCT ean_norm), count(*) FROM clean.products
                          WHERE ean_note IS NOT NULL GROUP BY ALL ORDER BY 4 DESC""").fetchall()
    return ["## 1. Lažni EAN-ovi", "", "Po lancu i razlogu (EAN-ova, proizvoda): "
            + "; ".join(f"{c} {r}: {e} / {n}" for c, r, e, n in rows)
            + ". Eurospinove mrkve i krumpir više nemaju begonija (`test_eurospin_no_begonia`).", ""]


def point23() -> list[str]:
    return ["## 2. i 3. Testovi", "",
            f"- „špageti“ ne vraća „TJESTENINA BUCATINI 500 G RISCOSSA“; proizvod bez traženog oblika ispada: "
            f"{run_tests(TESTS['2'])}",
            f"- „KRASTAVAC SALATAR kom“ (globalni EAN, na komad) je krastavac, „PAPRIKA AJVAR kom“ nije: {run_tests(TESTS['3'])}",
            ""]


def funnel3() -> list[str]:
    b = json.loads(Path("docs/data/funnel_before_2f3.json").read_text(encoding="utf-8"))
    a = json.loads(Path("docs/data/funnel_after_2f3.json").read_text(encoding="utf-8"))
    parts = [f"{k} {sum(b[k][ch][7] for ch in FUNNEL_CHAINS)} → {sum(a[k][ch][7] for ch in FUNNEL_CHAINS)}"
             for k in b]
    return ["Lijevak, konačno (zbroj 8 lanaca), prije → poslije točke 3: " + ", ".join(parts)
            + ". Po fazama: `docs/data/funnel_*_2f3.json`.", ""]


def point4(con) -> list[str]:
    total, n_bad, sample = weak_suspects(con, 20)
    return [f"## 4. Slabi članovi koji izgledaju krivo ({n_bad} od {total}; riječ namirnice nije među prve tri ni u jednom nazivu)", "",
            md_table(["namirnica", "nazivi po lancu"], [(st, names[:105]) for st, _, _, names in sample]), ""]


def point6(con) -> list[str]:
    lo, hi = UNIT_SUSPECT_RATIO
    rows = con.execute(f"""
        WITH u AS (
          SELECT ps.staple, p.name, p.unit, p.pack_source, ps.unit_suspect, median({STAPLE_PPU_SQL}) AS ppu
          FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
          JOIN clean.prices c USING (chain, product_id) JOIN clean.products p USING (chain, product_id)
          WHERE p.chain = 'lidl' AND ps.staple IN ('mlijeko', 'ulje', 'brasno', 'secer') AND NOT ps.excluded
            AND (ps.drop_reason IS NULL OR ps.unit_suspect)
          GROUP BY ps.staple, ps.chain, ps.product_id, p.name, p.unit, p.pack_source, ps.unit_suspect
        ),
        m AS (SELECT ps.staple, median({STAPLE_PPU_SQL}) AS med FROM clean.product_staples ps
              JOIN clean.staple_rules r USING (staple) JOIN clean.prices c USING (chain, product_id)
              WHERE NOT ps.excluded AND (ps.drop_reason IS NULL OR ps.unit_suspect) GROUP BY 1)
        SELECT u.staple, u.name, u.unit, u.pack_source, count(*), min(u.ppu), max(u.ppu), round(max(u.ppu) / any_value(m.med), 2),
               CASE WHEN bool_or(u.unit_suspect) THEN 'DA' ELSE '' END
        FROM u JOIN m USING (staple) GROUP BY u.staple, u.name, u.unit, u.pack_source ORDER BY 1, 2""").fetchall()
    out = [(st, name[:40], unit, src, n,
            "-" if mn is None else hr(mn) if mn == mx else f"{hr(mn)}–{hr(mx)}", "-" if r is None else hr(r), sus)
           for st, name, unit, src, n, mn, mx, r, sus in rows]
    n_all = con.execute("SELECT count(*) FROM clean.product_staples WHERE unit_suspect").fetchone()[0]
    return [f"## 6. Lidl: mlijeko, ulje, brašno, šećer (unit_suspect: pack_source unit i omjer izvan {lo}–{hi}x medijana)",
            f"Ukupno je `unit_suspect` {n_all} Lidlovih proizvoda. **Pogađa i ispravne jeftine** (trajno mlijeko 0,52 €/l, "
            "kristal šećer): prijedlog je 0,3–3x.", "",
            md_table(["namirnica", "naziv", "unit", "izvor", "kom", "€/jed", "omjer", "suspect"], out), ""]


def baskets(con) -> list[str]:
    out = ["## Košarice u Osijeku", ""]
    for recipe in ("test_palacinke", "test_bolonjez"):
        data = json.loads(Path(f"data/recipes/{recipe}.json").read_text(encoding="utf-8"))
        best = plan_basket(data["ingredients"], "Osijek", con=con)["best_store"]
        items = "; ".join(f"{it['ingredient']}: {it['name'][:30]} {hr(it['cost_pack'])}/{hr(it['cost_used'])}"
                          + (" (slabi)" if it.get("match_quality") == "weak" else "")
                          + (" (vaga, rezerva)" if it.get("by_weight_fallback") else "") for it in best["items"])
        out += [f"**{data['name']}**: {best['chain']}, {best['address']} · {best['n_matched']}/{best['n_ingredients']} · "
                f"total_to_buy **{hr(best['total_to_buy'])} €**, total_used {hr(best['total_used'])} € · {best['date_hr']}",
                f"Stavke (cost_pack/cost_used €): {items}.", ""]
    return out


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    lines = [f"# Pregled za razgovor: Korak 2F (arhiva {date.isoformat()}; `scripts/review_2f.py`, odluke 81–86)", ""]
    lines += point1(con) + point23() + funnel3() + point4(con) + point6(con) + baskets(con)
    text = "\n".join(lines).rstrip() + "\n"
    n = text.count("\n")
    if n > MAX_LINES:
        raise SystemExit(f"{OUT}: {n} redaka (najviše {MAX_LINES})")
    OUT.write_text(text, encoding="utf-8")
    print(f"{OUT}: {n} redaka")


if __name__ == "__main__":
    main()
