"""Ispiše docs/staples_review.md (top 20 kandidata + top 10 isključenih po namirnici) i
docs/staples_compact.md (top 5 + top 5 za odabrane namirnice) za ručni pregled.

Prije ispisa ponovno gradi clean.product_staples/product_attrs iz staples.yaml (par sekundi),
tako da se promjene u rječniku vide bez cijelog build_clean.

Upotreba: python scripts/staples_review.py [db_path] [out_path] [compact_path]
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
compact_path = Path(sys.argv[3] if len(sys.argv) > 3 else "docs/staples_compact.md")
COMPACT = ["brasno", "secer", "sol", "ulje", "maslac", "mlijeko", "jaja", "luk", "krumpir", "riza",
           "tjestenina", "rajcica", "kakao", "persin", "pileca_prsa"]

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
          FROM g JOIN clean.product_staples ps USING (chain, product_id) WHERE ps.staple = ? AND ps.drop_reason IS NULL GROUP BY g.gkey)
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
    WHERE ps.staple = ? AND ps.drop_reason IS NULL GROUP BY g.gkey HAVING bool_or(ps.excluded)
    ORDER BY n_chains DESC, name LIMIT ?
"""

def header(title: str, intro: list[str], keys: list[str]) -> list[str]:
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    out = [f"# {title}", "", f"Generirano skriptom `scripts/staples_review.py` iz `src/mealmeter/staples.yaml` i arhive {date}.", ""]
    out += intro + ["", "## Sadržaj", ""]
    return out + [f"- [{staples[k].name}](#{k}) (`{k}`)" for k in keys]


def section(st, top: int, n_excl: int, results: list[dict]) -> list[str]:
    n_ok, n_bad = con.execute(GROUPS_SQL, [st.key]).fetchone()
    rules = [f"jedinica: **{st.compare_unit}**", f"loose_produce: **{str(st.loose_produce).lower()}**",
             f"grupa: **{n_ok}**", f"isključenih grupa: **{n_bad}**"]
    if st.plausible_per_unit:
        rules.append(f"plausible: **{st.plausible_per_unit[0]}–{st.plausible_per_unit[1]} €/{st.compare_unit}**")
    if st.min_pack or st.max_pack:
        rules.append(f"pakiranje: **{st.min_pack}–{st.max_pack}**")
    if st.default_exclude_variants:
        rules.append("zadano bez: **" + ", ".join(f"{a}={v}" for a, v in st.default_exclude_variants) + "**")
    if st.default_attributes:
        rules.append("zadano: **" + ", ".join(f"{a}={v}" for a, v in st.default_attributes.items()) + "**")
    if st.group_by:
        rules.append(f"grupira po: **{st.group_by}**")
    if st.pantry:
        rules.append("**pantry**")
    out = ["", f'<a id="{st.key}"></a>', f"## {st.name} (`{st.key}`)", "", " · ".join(rules), "",
           f"sinonimi: {', '.join(st.synonyms)}  ", f"must_match: `{' | '.join(st.must_match)}`"]
    if st.require_any:
        out.append(f"  \nrequire_any: `{' | '.join(st.require_any)}`")
    if st.attributes:
        out.append("  \natributi: " + "; ".join(f"{a} = {', '.join(v)}" for a, v in st.attributes.items()))
    out += ["", "| # | id | naziv | pakiranje | lanaca | trgovina | €/jed | pouzdanost | atributi |",
            "|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(results[:top], 1):
        unit = f" /{r['per_unit']}" if r["per_unit"] else ""
        conf = f"{r['unit_confidence']}/{r['pack_source']}" if r["unit_confidence"] else "–"
        attrs = ", ".join(f"{k}={v}" for k, v in r["attributes"].items())
        flags = " ⚠" + str(r["n_price_suspect"]) if r.get("n_price_suspect") else ""
        out.append(
            f"| {i} | {cell(r['id'])} | {cell(r['name'])} | {cell(r['pack'])} | {r['n_chains']} | {r['n_stores']} "
            f"| {rng(r['price_per_unit_min'], r['price_per_unit_max'])}{unit}{flags} | {conf} | {cell(attrs)} |"
        )
    excluded = con.execute(EXCLUDED_SQL, [st.key, n_excl]).fetchall()
    if excluded:
        out += ["", f"<details><summary>Najčešće isključeni (top {n_excl})</summary>", "",
                "| naziv | lanaca | isključio |", "|---|---|---|"]
        for _, name, name_norm, n_chains in excluded:
            hit = next((p for p in st.must_not_match if re.search(r"(^| )(?:" + p + ")", name_norm or "")), "?")
            out.append(f"| {cell(name)} | {n_chains} | `{cell(hit)}` |")
        out += ["", "</details>"]
    return out


INTRO = [
    "**Ovo je prijedlog za ručni pregled**: za svaku namirnicu označi koji kandidati ne pripadaju",
    "(→ dodaj `must_not_match`) i koji nedostaju (→ proširi `must_match`), pa ponovno pokreni skriptu.",
    "",
    "Kandidati su grupe proizvoda (isti EAN, lanac + naziv bez EAN-a, ili klasa za jaja), poredane po",
    "relevantnosti, broju lanaca i trgovina. Prikazuje se zadani izbor: bez rasprodaje (SNIŽENJE), bez",
    "zadano isključenih varijanti i bez pakiranja izvan raspona. `€/jed` ne uključuje cijene izvan",
    "`plausible_per_unit`; ⚠N je broj takvih (odbačenih) cijena u grupi. `pouzdanost` je",
    "`unit_confidence/pack_source`. „Isključeni“ su grupe koje pogađa `must_match`, ali i `must_not_match`;",
    "uz svaku je uzorak koji ju je isključio.",
]
results = {st.key: find_products(ingredient=st.key, limit=20, con=con) for st in staples.values()}

lines = header("Pregled osnovnih namirnica", INTRO, list(staples))
for st in staples.values():
    lines += section(st, 20, 10, results[st.key])
out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Zapisano: {out_path} ({len(staples)} namirnica)")

lines = header("Pregled osnovnih namirnica (sažeto)", INTRO, COMPACT)
for key in COMPACT:
    lines += section(staples[key], 5, 5, results[key])
compact_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Zapisano: {compact_path} ({len(COMPACT)} namirnica)")
