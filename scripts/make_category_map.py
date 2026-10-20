"""Izradi data/category_map.yaml: normalizirana kategorija lanca -> skupina hrane (food_group).

Skupina se predlaže pravilima iz normalize._CATEGORY_RULES, a mapa se zatim može ručno ispraviti;
build čita samo mapu (pravila su rezerva za kategorije kojih u mapi nema). Postojeća mapa se ne
prepisuje bez --force.

Upotreba: python scripts/make_category_map.py [db_path] [--force]
"""

import sys
from pathlib import Path

import duckdb

from mealmeter.food import CATEGORY_MAP_PATH
from mealmeter.normalize import FOOD_GROUP_VALUES, category_group, norm_text

args = [a for a in sys.argv[1:] if not a.startswith("--")]
db_path = args[0] if args else "data/mealmeter.duckdb"
if CATEGORY_MAP_PATH.exists() and "--force" not in sys.argv:
    sys.exit(f"{CATEGORY_MAP_PATH} već postoji (--force za ponovnu izradu)")

con = duckdb.connect(db_path, read_only=True)
rows = con.execute("""
    SELECT category, count(*), string_agg(DISTINCT chain, ',' ORDER BY chain)
    FROM products WHERE category IS NOT NULL GROUP BY category
""").fetchall()
agg: dict[str, dict] = {}
for category, n, chains in rows:
    a = agg.setdefault(norm_text(category), {"n": 0, "chains": set(), "raw": category})
    a["n"] += n
    a["chains"].update(chains.split(","))

by_group: dict[str, list] = {}
for key, a in agg.items():
    by_group.setdefault(category_group(a["raw"]), []).append((key, a))

lines = [
    "# Kategorija lanca (norm_text: mala slova, bez dijakritika i interpunkcije) -> food_group.",
    f"# Skupine: {', '.join(FOOD_GROUP_VALUES)}.",
    "# 'unknown' znači da kategorija ništa ne govori (npr. \"Ostalo\" miješa svrdla i gastro hranu):",
    "# takvi proizvodi nasljeđuju skupinu preko EAN-a ili popisa riječi (vidi src/mealmeter/food.py).",
    "# Prijedlog je izrađen pravilima (scripts/make_category_map.py); ispravci se upisuju ovdje.",
    "# Komentar uz redak: broj proizvoda i lanci.",
]
for group in FOOD_GROUP_VALUES:
    items = sorted(by_group.get(group, []), key=lambda kv: -kv[1]["n"])
    if not items:
        continue
    lines.append(f"\n# --- {group} ({len(items)} kategorija, {sum(a['n'] for _, a in items)} proizvoda)")
    for key, a in items:
        lines.append(f'"{key}": {group}  # {a["n"]}, {",".join(sorted(a["chains"]))}')
Path(CATEGORY_MAP_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{CATEGORY_MAP_PATH}: {len(agg)} kategorija")
for group in FOOD_GROUP_VALUES:
    items = by_group.get(group, [])
    print(f"  {group:<16}{len(items):>6} kategorija{sum(a['n'] for _, a in items):>9} proizvoda")
