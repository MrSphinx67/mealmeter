"""Ispiše docs/staples_review.md: top 20 kandidata po osnovnoj namirnici za ručni pregled.

Prije ispisa ponovno gradi clean.product_staples/product_attrs iz staples.yaml (par sekundi),
tako da se promjene u rječniku vide bez cijelog build_clean.

Upotreba: python scripts/staples_review.py [db_path] [out_path]
"""

import re
import sys
import time
from pathlib import Path

import duckdb

from mealmeter.search import find_products, format_pack
from mealmeter.staples import build_staples, load_staples

db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
out_path = Path(sys.argv[2] if len(sys.argv) > 2 else "docs/staples_review.md")

con = duckdb.connect(db_path)
staples = load_staples()
t = time.time()
stats = build_staples(con, staples)
print(f"build_staples: {stats} ({time.time() - t:.1f}s)")


def money(v):
    return "" if v is None else f"{v:.2f}".replace(".", ",")


def rng(lo, hi):
    if lo is None:
        return "–"
    return money(lo) if lo == hi else f"{money(lo)}–{money(hi)}"


def cell(s) -> str:
    return str(s or "").replace("|", "/")


GROUPS_SQL = """
    WITH g AS (
      SELECT p.*, CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END AS gkey
      FROM clean.products p
    )
    SELECT count(DISTINCT gkey) FILTER (WHERE ok AND NOT bad), count(DISTINCT gkey) FILTER (WHERE bad)
    FROM (SELECT g.gkey, bool_or(NOT ps.excluded) ok, bool_or(ps.excluded) bad
          FROM g JOIN clean.product_staples ps USING (chain, product_id) WHERE ps.staple = ? GROUP BY g.gkey)
"""
EXCLUDED_SQL = """
    WITH g AS (
      SELECT p.*, CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END AS gkey
      FROM clean.products p
    )
    SELECT g.gkey, arg_max(g.name, length(g.name)) FILTER (WHERE ps.excluded) AS name,
           arg_max(g.name_norm, length(g.name)) FILTER (WHERE ps.excluded) AS name_norm,
           count(DISTINCT g.chain) AS n_chains
    FROM g JOIN clean.product_staples ps USING (chain, product_id)
    WHERE ps.staple = ? GROUP BY g.gkey HAVING bool_or(ps.excluded)
    ORDER BY n_chains DESC, name LIMIT 10
"""

lines = [
    "# Pregled osnovnih namirnica",
    "",
    "Generirano skriptom `scripts/staples_review.py` iz `src/mealmeter/staples.yaml` i arhive "
    f"{con.execute('SELECT max(date) FROM clean.prices').fetchone()[0]}. **Ovo je prijedlog za ručni pregled**:",
    "za svaku namirnicu označi koji kandidati ne pripadaju (→ dodaj `must_not_match`) i koji nedostaju",
    "(→ proširi `must_match`), pa ponovno pokreni skriptu.",
    "",
    "Kandidati su grupe proizvoda (isti EAN, ili lanac + naziv bez EAN-a), poredane po broju lanaca i",
    "trgovina. Cijena po jedinici je u jedinici namirnice gdje postoji; `pouzdanost` je",
    "`unit_confidence/pack_source`. „Isključeni“ su grupe koje pogađa `must_match`, ali i `must_not_match`;",
    "uz svaku je uzorak koji ju je isključio.",
    "",
    "## Sadržaj",
    "",
]
lines += [f"- [{st.name}](#{st.key}) (`{st.key}`)" for st in staples.values()]

for st in staples.values():
    n_ok, n_bad = con.execute(GROUPS_SQL, [st.key]).fetchone()
    lines += [
        "",
        f'<a id="{st.key}"></a>',
        f"## {st.name} (`{st.key}`)",
        "",
        f"jedinica: **{st.unit}** · loose_produce: **{str(st.loose_produce).lower()}** · "
        f"grupa: **{n_ok}** · isključenih grupa: **{n_bad}**",
        "",
        f"sinonimi: {', '.join(st.synonyms)}  ",
        f"must_match: `{' | '.join(st.must_match)}`",
    ]
    if st.attributes:
        lines.append("atributi: " + "; ".join(f"{a} = {', '.join(v)}" for a, v in st.attributes.items()))
    lines += ["", "| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |",
              "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(find_products(ingredient=st.key, limit=20, con=con), 1):
        unit = f" /{r['per_unit']}" if r["per_unit"] else ""
        conf = f"{r['unit_confidence']}/{r['pack_source']}" if r["unit_confidence"] else "–"
        attrs = ", ".join(f"{k}={v}" for k, v in r["attributes"].items())
        lines.append(
            f"| {i} | {cell(r['id'])} | {cell(r['name'])} | {cell(r['pack'])} | {r['n_chains']} | {r['n_stores']} "
            f"| {rng(r['price_per_unit_min'], r['price_per_unit_max'])}{unit} | {conf} | {cell(attrs)} |"
        )
    excluded = con.execute(EXCLUDED_SQL, [st.key]).fetchall()
    if excluded:
        lines += ["", "<details><summary>Najčešće isključeni (top 10)</summary>", "",
                  "| naziv | lanaca | isključio |", "|---|---|---|"]
        for _, name, name_norm, n_chains in excluded:
            hit = next((p for p in st.must_not_match if re.search(r"(^| )(?:" + p + ")", name_norm or "")), "?")
            lines.append(f"| {cell(name)} | {n_chains} | `{cell(hit)}` |")
        lines += ["", "</details>"]

out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Zapisano: {out_path} ({len(staples)} namirnica)")
