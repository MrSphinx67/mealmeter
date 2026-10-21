"""docs/ean_incoherent.md: razdvojene EAN grupe (Korak 4B.6, build.flag_incoherent_eans).

Upotreba: python scripts/ean_incoherent.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import random
import sys
from pathlib import Path

import duckdb

db = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
out = Path(__file__).resolve().parents[1] / "docs" / "ean_incoherent.md"
con = duckdb.connect(db, read_only=True)

by_reason = con.execute("""SELECT reason, count(DISTINCT ean_norm), count(*) FROM clean.ean_incoherent
                           GROUP BY reason ORDER BY reason""").fetchall()
by_chain = con.execute("""
    SELECT chain, count(DISTINCT ean_norm) FILTER (WHERE reason = 'group'),
           count(DISTINCT ean_norm) FILTER (WHERE reason = 'outlier'), count(*)
    FROM clean.ean_incoherent GROUP BY chain ORDER BY 2 + 3 DESC, chain""").fetchall()
names = {}
for ean, reason, chain, name in con.execute("""
        SELECT ean_norm, reason, chain, name FROM clean.ean_incoherent ORDER BY ean_norm, chain, name""").fetchall():
    names.setdefault((ean, reason), []).append(f"{chain}: {name}")
# za izdvojene lance i ostatak grupe (koji ostaje zajedno)
kept = {}
for ean, chain, name in con.execute("""
        SELECT p.ean_norm, p.chain, p.name FROM clean.products p
        WHERE p.ean_global AND p.ean_norm IN (SELECT ean_norm FROM clean.ean_incoherent WHERE reason = 'outlier')
        ORDER BY p.chain""").fetchall():
    kept.setdefault(ean, []).append(f"{chain}: {name}")

random.seed(46)
groups = [k for k in names if k[1] == "group"]
outliers = [k for k in names if k[1] == "outlier"]
sample = random.sample(groups, min(20, len(groups))) + random.sample(outliers, min(10, len(outliers)))

lines = [
    "# Nekoherentne EAN grupe (Korak 4B.6)",
    "",
    f"Baza: `{db}`, skripta `scripts/ean_incoherent.py`, pravilo `build.ean_coherence`.",
    "",
    "Grupa istog globalnog EAN-a u >= 2 lanca je nekoherentna kad nijedna riječ naziva nije u nazivima >= 50 %",
    "lanaca (i barem dva lanca). Riječ je \"u nazivu\" i kao kratica (\"REB\" / \"REBRA\") ili uz razliku u slovu-dva;",
    "kandidati su riječi od >= 3 slova s markom, jer je strogo pravilo (>= 4 slova, bez marke) označilo ~1 550",
    "grupa, uglavnom isti proizvod. Takva grupa se razdvaja po lancu + name_norm (`ean_global = false`,",
    "`ean_incoherent = true`). U koherentnoj grupi s >= 3 lanca izdvaja se lanac koji ne dijeli nijednu riječ",
    "ni s jednim drugim lancem (razlog `outlier`). Poznata cijena: sinonimi bez zajedničke riječi (GLJIVE /",
    "ŠAMPINJONI, ZELJE / KUPUS KIS.) također se razdvajaju; tada se svaki lanac procjenjuje po svom nazivu.",
    "",
    "| razlog | grupa | proizvoda |",
    "|---|---|---|",
    *[f"| {r} | {g} | {n} |" for r, g, n in by_reason],
    "",
    "## Po lancu",
    "",
    "| lanac | razdvojenih grupa | izdvojen iz grupe | proizvoda |",
    "|---|---|---|---|",
    *[f"| {c} | {g} | {o} | {n} |" for c, g, o, n in by_chain],
    "",
    f"## {len(sample)} primjera (20 razdvojenih grupa, 10 izdvojenih lanaca)",
    "",
    "| EAN | razlog | nazivi |",
    "|---|---|---|",
]
for ean, reason in sample:
    text = "; ".join(names[(ean, reason)])
    if reason == "outlier":
        text += " — ostaje: " + "; ".join(kept.get(ean, []))
    lines.append(f"| {ean} | {reason} | {text.replace('|', '/')[:300]} |")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{out}: {len(lines)} redaka")
