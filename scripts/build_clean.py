"""Gradi čiste tablice (schema `clean`) iz sirovih tablica u DuckDB-u i ispisuje statistiku.

Upotreba: python scripts/build_clean.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import sys

import duckdb

from mealmeter.build import build_clean

db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
con = duckdb.connect(db_path)

# Provjera pravila price_eff = coalesce(nullif(special_price,0), price) na poznatim akcijskim artiklima,
# prije čišćenja (sirovi podaci): Eurospin (price = redovna) i Konzum (price = već snižena).
print("=== Provjera price_eff na akcijskim artiklima (sirovi podaci)")
con.sql("""
    SELECT p.chain, p.store_id, pr.name, p.price, p.special_price, p.best_price_30, p.anchor_price,
           p.unit_price, pr.quantity,
           coalesce(nullif(p.special_price, 0), p.price) AS price_eff
    FROM prices p JOIN products pr USING (chain, product_id)
    WHERE (p.chain = 'eurospin' AND p.store_id = '310017' AND p.product_id = '001761601')
       OR (p.chain = 'konzum' AND p.store_id = '0001' AND p.product_id = '01310151')
    GROUP BY ALL
""").show(max_width=250)
con.sql("""
    SELECT chain, count(*) AS n_special,
           count(*) FILTER (WHERE special_price = price) AS eq_price,
           count(*) FILTER (WHERE special_price < price) AS below_price,
           count(*) FILTER (WHERE special_price > price) AS above_price
    FROM prices WHERE special_price > 0 GROUP BY chain ORDER BY chain
""").show(max_rows=50)

stats = build_clean(con)

print("\n=== Cijene po lancu: sirovo -> čisto (uklonjeni duplikati i retci bez cijene)")
print(f"{'lanac':<20}{'sirovo':>10}{'čisto':>10}{'uklonjeno':>11}{'od toga cijena 0/NULL':>23}")
for chain, n_raw, n_clean, n_zero in stats["dedup"]:
    print(f"{chain:<20}{n_raw:>10}{n_clean:>10}{n_raw - n_clean:>11}{n_zero:>23}")
tot_raw = sum(r[1] for r in stats["dedup"])
tot_clean = sum(r[2] for r in stats["dedup"])
print(f"{'UKUPNO':<20}{tot_raw:>10}{tot_clean:>10}{tot_raw - tot_clean:>11}")

print("\n=== unit_confidence po lancu (% cijena)")
print(f"{'lanac':<20}{'high':>8}{'low':>8}{'nema':>8}")
for chain, hi, lo, none in stats["confidence"]:
    print(f"{chain:<20}{hi:>8}{lo:>8}{none:>8}")

print("\n=== Kontrola: naša cijena/kg (iz naziva) vs. unit_price lanca, % unutar 5 %")
for chain, n, pct in stats["unit_agreement"]:
    print(f"{chain:<20}{n:>10}{pct:>8}")

print("\n=== Kvaliteta podataka po lancu (%: unit_price prazan, cijena >3x/<1/3 sidrene, bez kategorije,")
print("    bez marke, neprepoznata jedinica; omjer cijene prema ostalim lancima za isti EAN i % odstupanja >2x)")
print(f"{'lanac':<20}{'kvaliteta':<10}{'up_0':>7}{'sidro':>7}{'kat':>7}{'marka':>7}{'jed':>7}{'omjer':>7}{'>2x':>7}")
for row in stats["quality"]:
    chain, dq, *vals = row
    print(f"{chain:<20}{dq:<10}" + "".join(f"{'' if v is None else v:>7}" for v in vals))

food = stats["food"]
print("\n=== Filtar hrane (food.py): proizvodi bez korisne kategorije lanca po lancu")
print(f"{'lanac':<20}{'proizvoda':>10}{'bez kat.':>10}{'EAN':>8}{'% EAN':>7}{'riječi':>8}{'unknown':>9}{'sukob':>7}")
for chain, n, n_no, n_ean, n_words, n_unk, n_conf in food["by_chain"]:
    if n_no:
        print(f"{chain:<20}{n:>10}{n_no:>10}{n_ean:>8}{100 * n_ean / n_no:>7.1f}{n_words:>8}{n_unk:>9}{n_conf:>7}")
if food["unmapped_categories"]:
    print("  kategorije izvan data/category_map.yaml (vrijede pravila):", food["unmapped_categories"][:20])
print(f"{'skupina':<16}{'is_food':<9}{'izvor':<15}{'proizvoda':>10}")
for group, is_food, source, n in food["by_group"]:
    print(f"{group:<16}{str(is_food):<9}{source:<15}{n:>10}")

st = dict(stats["staples"])
suspects = st.pop("suspect_prices")
print("\n=== Osnovne namirnice (staples.yaml):", {k: v for k, v in st.items() if k != "auto_ranges"})
print(f"\n=== Cijene izvan granica (price_suspect: izvan min/max i plan_basket); automatskih granica: {st.pop('auto_ranges')}")
print(f"{'namirnica':<20}{'granice':<8}{'odbačeno':>10}{'od':>10}{'%':>7}")
for staple, source, n_bad, n_all in suspects:
    print(f"{staple:<20}{source:<8}{n_bad:>10}{n_all:>10}{100 * n_bad / n_all:>7.1f}")
print("\n=== Proizvodi izbačeni iz namirnica (drop_reason)")
for reason, n in con.execute("""
        SELECT split_part(drop_reason, ':', 1) || CASE WHEN drop_reason LIKE 'kategorija:%' THEN ':*' ELSE '' END,
               count(*) FROM clean.product_staples WHERE drop_reason IS NOT NULL GROUP BY 1 ORDER BY 2 DESC""").fetchall():
    print(f"  {reason:<16}{n:>8}")
for col in ("clearance", "variable_weight"):
    n = con.execute(f"SELECT count(*) FROM clean.products WHERE {col}").fetchone()[0]
    print(f"  proizvoda s {col}: {n}")
n = con.execute("SELECT count(*) FROM clean.products WHERE drained_amount IS NOT NULL").fetchone()[0]
print(f"  proizvoda s ocijeđenom masom: {n}")

for t in ("stores", "products", "prices", "city_alias", "chains", "staple_rules", "product_staples", "product_attrs"):
    print(f"clean.{t}:", con.execute(f"SELECT count(*) FROM clean.{t}").fetchone()[0])
