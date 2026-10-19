"""Izvještaji o namirnicama nad izgrađenom bazom:

- docs/price_outliers.md: za namirnice s > 5 % odbačenih cijena (price_suspect) 15 najčešćih
  odbačenih grupa proizvoda s nazivom
- docs/ranges.md: min_pack/max_pack i granice cijena (ručne i automatske) za sve namirnice
- na ekran: broj grupa s oblik=nepoznato po namirnici

Upotreba: python scripts/staple_reports.py [db_path]
"""

import sys
from pathlib import Path

import duckdb

from mealmeter.staples import STAPLE_PPU_SQL, load_staples, staple_price_suspects

db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
con = duckdb.connect(db_path, read_only=True)
staples = load_staples()
date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
GKEY = "CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END"


def money(v):
    return "–" if v is None else f"{v:.2f}".replace(".", ",")


# --- price_outliers.md ---------------------------------------------------------
suspects = staple_price_suspects(con)
lines = [
    "# Odbačene cijene po namirnici",
    "",
    f"Generirano skriptom `scripts/staple_reports.py` iz arhive {date}. Za svaku namirnicu s više od 5 %",
    "cijena izvan granica (`price_suspect`) ispisano je 15 grupa proizvoda s najviše odbačenih cijena.",
    "Granice su ručne (`plausible_per_unit` u staples.yaml) ili automatske (0,25x–4x medijana namirnice).",
    "Odbačena cijena ne ulazi u raspon cijena ni u plan_basket. Česte odbačene grupe obično su krivi pogoci",
    "rječnika (→ `must_not_match`) ili krivo pročitana gramatura.",
    "",
    "| namirnica | granice | €/jed | odbačeno | od | % |",
    "|---|---|---|---|---|---|",
]
heavy = []
for key, source, n_bad, n_all in suspects:
    lo, hi, unit = con.execute(
        "SELECT ppu_min, ppu_max, compare_unit FROM clean.staple_rules WHERE staple = ?", [key]).fetchone()
    pct = 100 * n_bad / n_all
    lines.append(f"| {key} | {source} | {money(lo)}–{money(hi)} /{unit} | {n_bad} | {n_all} | {pct:.1f} |")
    if pct > 5:
        heavy.append((key, lo, hi, unit, pct))
for key, lo, hi, unit, pct in heavy:
    rows = con.execute(f"""
        SELECT any_value(p.name), count(*) AS n, count(DISTINCT p.chain), median(ppu), min(ppu), max(ppu),
               any_value(p.pack_amount), any_value(p.pack_unit), any_value(ps.assumed_g)
        FROM (
          SELECT ps.*, {STAPLE_PPU_SQL} AS ppu, c.store_id
          FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
          JOIN clean.prices c USING (chain, product_id)
          WHERE ps.staple = ? AND NOT ps.excluded AND ps.drop_reason IS NULL
        ) ps JOIN clean.products p USING (chain, product_id)
        WHERE ps.ppu IS NOT NULL AND ps.ppu NOT BETWEEN ? AND ?
        GROUP BY {GKEY} ORDER BY n DESC LIMIT 15
    """, [key, lo, hi]).fetchall()
    lines += ["", f"## {staples[key].name} (`{key}`): {pct:.1f} % odbačeno, granice {money(lo)}–{money(hi)} €/{unit}", "",
              "| naziv | odbačenih cijena | lanaca | €/jed (medijan) | raspon | pakiranje |", "|---|---|---|---|---|---|"]
    for name, n, n_chains, med, mn, mx, amount, pack_unit, assumed in rows:
        pack = f"{amount:g} {pack_unit}" if amount else (f"pretp. {assumed:g} g" if assumed else "–")
        lines.append(f"| {name} | {n} | {n_chains} | {money(med)} | {money(mn)}–{money(mx)} | {pack} |")
Path("docs/price_outliers.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Zapisano: docs/price_outliers.md ({len(heavy)} namirnica s > 5 % odbačenih)")

# --- ranges.md -----------------------------------------------------------------
lines = [
    "# Granice po namirnici",
    "",
    f"Generirano skriptom `scripts/staple_reports.py` iz `staples.yaml` i arhive {date}.",
    "",
    "- `min_pack`/`max_pack`: dopušteno pakiranje u g, ml ili kom (za jaja broj komada); izvan raspona",
    "  proizvod dobiva `drop_reason='pakiranje'`. Vrijednosti su prijedlog iz Koraka 2A2 i čekaju pregled.",
    "- granice cijene: `manual` = `plausible_per_unit` iz staples.yaml (vlasnik: mlijeko, brašno, šećer,",
    "  sol, ulje, maslinovo ulje, maslac; prijedlog: jaja), `auto` = 0,25x–4x medijana cijene po jedinici",
    "  namirnice u ovoj arhivi. Cijena izvan granica je `price_suspect`.",
    "",
    "| namirnica | jedinica | min_pack | max_pack | €/jed min | €/jed max | granice |",
    "|---|---|---|---|---|---|---|",
]
for key, unit, mn, mx, lo, hi, src in con.execute("""
        SELECT staple, compare_unit, min_pack, max_pack, ppu_min, ppu_max, coalesce(range_source, '–')
        FROM clean.staple_rules ORDER BY staple""").fetchall():
    fmt = lambda v: "–" if v is None else f"{v:g}"  # noqa: E731
    lines.append(f"| {key} | {unit} | {fmt(mn)} | {fmt(mx)} | {money(lo)} | {money(hi)} | {src} |")
Path("docs/ranges.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Zapisano: docs/ranges.md")

# --- oblik=nepoznato ------------------------------------------------------------
print("\nGrupe s oblik=nepoznato (od grupa s atributom oblik):")
for key, unknown, total in con.execute(f"""
        SELECT pa.staple, count(DISTINCT {GKEY}) FILTER (WHERE pa.value = 'nepoznato'), count(DISTINCT {GKEY})
        FROM clean.product_attrs pa JOIN clean.products p USING (chain, product_id)
        WHERE pa.attr = 'oblik' GROUP BY pa.staple ORDER BY pa.staple""").fetchall():
    print(f"  {key:<18}{unknown:>6} / {total}")
