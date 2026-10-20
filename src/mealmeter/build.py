"""Učitavanje dnevne arhive cijene.dev u DuckDB i izgradnja čistih tablica (schema `clean`)."""

import csv
import os
import tempfile
from pathlib import Path

import duckdb

from mealmeter.food import build_food
from mealmeter.staples import build_staples, match_text
from mealmeter.normalize import (
    CITY_ALIASES,
    analyze_pack,
    canonical_city,
    is_clearance,
    norm_text,
    normalize_ean,
    parse_pack_unit_field,
    unit_hint,
)

PRICE_COLS = ["price", "unit_price", "best_price_30", "anchor_price", "special_price"]

# Trgovine s praznim gradom, a grad je zapisan u adresi (provjereno ručno)
CITY_FIXES = {
    ("kaufland", "5330"): "Zagreb",  # Ventilatorska Cesta 1 Lucko
    ("kaufland", "6630"): "Krk",  # Ulica Stjepana Radića 31B Krk
}

# Lanci čiji podaci nisu pouzdani: ostaju u bazi, ali se ne koriste za preporuke (plan_basket).
# Razlozi se računaju pri svakom buildu (chain_quality_report) i zapisuju u clean.chains.
SUSPECT_CHAINS = {"lorenco"}
# Veleprodaja (cash & carry): clean.stores.store_type = 'cash_and_carry'. Prodaje kartone i ugostiteljska
# pakiranja ("10/1 JAJA" je deset kutija), pa je izvan zadanog izbora i košarice (include_wholesale).
WHOLESALE_CHAINS = {"metro"}

NATIONAL_NOTE = "Nacionalna cijena (web/sve poslovnice); provjeri dostupnost u svom gradu."


def load_raw(con: duckdb.DuckDBPyConnection, root: Path, archive_date: str) -> list[str]:
    """Sirovi CSV-ovi u tablice stores/products/prices, bez normalizacije.

    Dodaje stupac `chain` (naziv mape) i `date` (dan iz naziva arhive) u prices.
    """

    def raw(chain: str, name: str) -> str:
        # Sve kao tekst: šifre imaju vodeće nule
        return f"read_csv('{root / chain / name}', header=true, all_varchar=true)"

    chains = sorted(p.name for p in Path(root).iterdir() if p.is_dir())
    con.execute("DROP TABLE IF EXISTS stores; DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS prices")
    casts = ", ".join(f"TRY_CAST({c} AS DECIMAL(10,2)) AS {c}" for c in PRICE_COLS)
    for i, chain in enumerate(chains):
        verb = "CREATE TABLE {} AS" if i == 0 else "INSERT INTO {}"
        con.execute(f"{verb.format('stores')} SELECT '{chain}' AS chain, * FROM {raw(chain, 'stores.csv')}")
        con.execute(f"{verb.format('products')} SELECT '{chain}' AS chain, * FROM {raw(chain, 'products.csv')}")
        con.execute(
            f"{verb.format('prices')} SELECT '{chain}' AS chain, store_id, product_id, {casts}, "
            f"DATE '{archive_date}' AS date FROM {raw(chain, 'prices.csv')}"
        )
        bad = con.execute(
            f"SELECT count(*) FROM {raw(chain, 'prices.csv')} WHERE "
            + " OR ".join(f"({c} IS NOT NULL AND TRY_CAST({c} AS DECIMAL(10,2)) IS NULL)" for c in PRICE_COLS)
        ).fetchone()[0]
        if bad:
            raise ValueError(f"{chain}: {bad} redaka s neparsabilnom cijenom")
    return chains


def _temp_table(con: duckdb.DuckDBPyConnection, name: str, columns: dict[str, str], rows) -> None:
    """Python retke u privremenu tablicu preko CSV-a (Python UDF-ovi u DuckDB-u traže numpy)."""
    with tempfile.NamedTemporaryFile("w", suffix=".csv", newline="", delete=False) as f:
        w = csv.writer(f)
        w.writerow(columns)
        w.writerows(rows)
    try:
        cols = ", ".join(f"'{c}': '{t}'" for c, t in columns.items())
        con.execute(
            f"CREATE OR REPLACE TEMP TABLE {name} AS SELECT * FROM "
            f"read_csv('{f.name}', header=true, columns={{{cols}}}, nullstr='', quote='\"')"
        )
    finally:
        os.unlink(f.name)


def build_clean(con: duckdb.DuckDBPyConnection) -> dict:
    """Iz sirovih tablica gradi clean.stores, clean.products, clean.prices i clean.city_alias.

    Vraća statistiku za ispis (duplikati po lancu, odbačeni retci, slaganje gramature).
    """
    con.execute("CREATE SCHEMA IF NOT EXISTS clean")

    # --- gradovi / trgovine ---
    con.execute("CREATE OR REPLACE TABLE clean.city_alias (alias_norm VARCHAR PRIMARY KEY, city VARCHAR)")
    con.executemany("INSERT INTO clean.city_alias VALUES (?, ?)", list(CITY_ALIASES.items()))

    def store_rows():
        for chain, store_id, city in con.execute("SELECT chain, store_id, city FROM stores").fetchall():
            city = (city or "").strip() or CITY_FIXES.get((chain, store_id))
            canonical = canonical_city(city)
            yield chain, store_id, city, norm_text(city), canonical, norm_text(canonical)

    _temp_table(con, "store_derived", {
        "chain": "VARCHAR", "store_id": "VARCHAR", "city": "VARCHAR", "city_norm": "VARCHAR",
        "city_canonical": "VARCHAR", "city_key": "VARCHAR",
    }, store_rows())
    wholesale = ", ".join(f"'{c}'" for c in sorted(WHOLESALE_CHAINS))
    con.execute(f"""
        CREATE OR REPLACE TABLE clean.stores AS
        SELECT r.chain, r.store_id, r.type,
               CASE WHEN r.chain = 'spar'  -- "Optujska 171 87001 Spar" -> "Optujska 171"
                    THEN regexp_replace(r.address, '\\s+' || r.store_id || '\\s+\\S+$', '')
                    ELSE r.address END AS address,
               d.city, r.zipcode,
               CASE WHEN r.store_id = 'all' THEN 'national' ELSE 'local' END AS scope,
               d.city_norm, d.city_canonical, d.city_key,
               CASE WHEN r.chain IN ({wholesale}) THEN 'cash_and_carry' ELSE 'retail' END AS store_type
        FROM stores r JOIN store_derived d USING (chain, store_id)
    """)

    # --- proizvodi ---
    def product_rows():
        q = "SELECT chain, product_id, barcode, name, unit, quantity FROM products"
        for chain, pid, barcode, name, unit, quantity in con.execute(q).fetchall():
            ean, valid, glob = normalize_ean(barcode)
            pack, drained, variable, confidence = analyze_pack(name)
            source = "name"
            # promjenjiva težina: nema pakiranja ni iz stupca unit (cijena je po kg od lanca)
            if pack is None and not variable and (pack := parse_pack_unit_field(unit)):
                source, confidence = "unit", "high"
            amount, pack_unit = pack or (None, None)
            yield (chain, pid, ean, valid, glob, norm_text(name), match_text(name), amount, pack_unit,
                   source if pack else None, unit_hint(unit, quantity),
                   drained, variable, is_clearance(name), confidence)

    _temp_table(con, "product_derived", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "ean_norm": "VARCHAR", "ean_valid": "BOOLEAN",
        "ean_global": "BOOLEAN", "name_norm": "VARCHAR", "match_norm": "VARCHAR", "pack_amount": "DOUBLE", "pack_unit": "VARCHAR",
        "pack_source": "VARCHAR", "unit_hint": "VARCHAR",
        "drained_amount": "DOUBLE", "variable_weight": "BOOLEAN", "clearance": "BOOLEAN",
        "pack_confidence": "VARCHAR",
    }, product_rows())
    con.execute("""
        CREATE OR REPLACE TABLE clean.products AS
        SELECT r.chain, r.product_id, r.barcode, d.ean_norm, d.ean_valid, d.ean_global,
               r.name, d.name_norm, d.match_norm, r.brand, r.category, r.unit, r.quantity,
               d.pack_amount, d.pack_unit, d.pack_source, d.unit_hint,
               d.drained_amount, d.variable_weight, d.clearance, d.pack_confidence
        FROM products r JOIN product_derived d USING (chain, product_id)
    """)

    # Isti globalni EAN = isti proizvod: gramaturu bez naziva ("BRAŠNO GLATKO 1/1") naslijedi od
    # drugih lanaca, ali samo ako se svi parsirani nazivi za taj EAN slažu.
    con.execute("""
        UPDATE clean.products p SET pack_amount = e.amount, pack_unit = e.unit, pack_source = 'ean',
                                    pack_confidence = e.conf
        FROM (
          SELECT ean_norm, any_value(pack_amount) AS amount, any_value(pack_unit) AS unit,
                 CASE WHEN bool_or(pack_confidence = 'low') THEN 'low' ELSE 'high' END AS conf
          FROM clean.products WHERE ean_global AND pack_unit IS NOT NULL AND NOT variable_weight
          GROUP BY ean_norm HAVING count(DISTINCT (pack_amount, pack_unit)) = 1
        ) e
        WHERE p.ean_norm = e.ean_norm AND p.ean_global AND p.pack_unit IS NULL AND NOT p.variable_weight
    """)
    # food_group, is_food, category_source (kategorija lanca -> EAN -> riječi), vidi food.py
    food_stats = build_food(con)

    # --- cijene ---
    # 0.00 je u ovim podacima uvijek "prazno" (cijena 0 € ne postoji), pa sve cijene 0 -> NULL.
    nz = ", ".join(f"nullif({c}, 0) AS {c}" for c in PRICE_COLS)
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE prices_nz AS
        SELECT chain, store_id, product_id, date, {nz},
               coalesce(nullif(special_price, 0), nullif(price, 0)) AS price_eff
        FROM prices
    """)
    # Duplikati (chain, store, product): zadržava se red s najnižom price_eff
    con.execute("""
        CREATE OR REPLACE TABLE clean.prices AS
        WITH d AS (
          SELECT * FROM prices_nz WHERE price_eff IS NOT NULL
          QUALIFY row_number() OVER (
            PARTITION BY chain, store_id, product_id
            ORDER BY price_eff, unit_price NULLS LAST, anchor_price NULLS LAST, best_price_30 NULLS LAST) = 1
        )
        SELECT d.chain, d.store_id, d.product_id, d.date,
               -- datum cijene (preneseni redak trgovine bez novih cijena zadržava svoj) i starost u danima
               d.date AS price_date, (SELECT max(date) FROM prices) - d.date AS stale_days,
               d.price, d.special_price, d.price_eff, d.special_price IS NOT NULL AS is_special,
               d.unit_price, d.best_price_30, d.anchor_price,
               round(CASE
                 WHEN p.pack_unit IN ('g', 'ml') AND p.pack_amount > 0 THEN d.price_eff / p.pack_amount * 1000
                 WHEN p.pack_unit = 'kom' AND p.pack_amount > 0 THEN d.price_eff / p.pack_amount
                 -- unit_price lanca je računat iz redovne cijene (Eurospin), pa ga skaliramo
                 WHEN p.unit_hint IS NOT NULL THEN d.unit_price * d.price_eff / coalesce(d.price, d.price_eff)
               END, 2)::DECIMAL(10,2) AS price_per_unit,
               CASE p.pack_unit WHEN 'g' THEN 'kg' WHEN 'ml' THEN 'l' WHEN 'kom' THEN 'kom'
                    ELSE CASE WHEN d.unit_price IS NOT NULL THEN p.unit_hint END END AS per_unit,
               -- low: jedinica (kg/l) mora biti poznata iz unit/quantity, inače nema cijene po jedinici
               CASE WHEN p.pack_unit IS NOT NULL THEN 'high'
                    WHEN d.unit_price IS NOT NULL AND p.unit_hint IS NOT NULL THEN 'low' END AS unit_confidence,
               -- konzerve: cijena po kg ocijeđene mase, uz bruto price_per_unit
               round(d.price_eff / nullif(p.drained_amount, 0) * 1000, 2)::DECIMAL(10,2) AS price_per_kg_drained
        FROM d JOIN clean.products p USING (chain, product_id)
    """)

    # --- lanci ---
    con.execute("CREATE OR REPLACE TEMP TABLE suspect (chain VARCHAR)")
    con.executemany("INSERT INTO suspect VALUES (?)", [(c,) for c in sorted(SUSPECT_CHAINS)])
    con.execute("""
        CREATE OR REPLACE TABLE clean.chains AS
        SELECT s.chain, count(*) AS n_stores,
               CASE WHEN bool_and(s.scope = 'national') THEN 'national' ELSE 'local' END AS scope,
               CASE WHEN s.chain IN (SELECT chain FROM suspect) THEN 'suspect' ELSE 'ok' END AS data_quality
        FROM clean.stores s GROUP BY s.chain
    """)

    stats = {"food": food_stats}
    stats["quality"] = chain_quality_report(con)
    stats["staples"] = build_staples(con)
    stats["dedup"] = con.execute("""
        SELECT r.chain, r.n_raw, coalesce(c.n_clean, 0) AS n_clean, r.n_zero_price
        FROM (SELECT chain, count(*) n_raw, count(*) FILTER (WHERE price_eff IS NULL) n_zero_price
              FROM prices_nz GROUP BY chain) r
        LEFT JOIN (SELECT chain, count(*) n_clean FROM clean.prices GROUP BY chain) c USING (chain)
        ORDER BY r.chain
    """).fetchall()
    # Slaganje naše cijene/kg s unit_price lanca (gdje je lančev unit_price po kg/l)
    stats["unit_agreement"] = con.execute("""
        SELECT c.chain, count(*) AS n,
               round(100 * avg((abs(c.price_per_unit - c.unit_price * c.price_eff / coalesce(c.price, c.price_eff))
                               <= 0.05 * c.price_per_unit)::int), 1) AS pct_within_5
        FROM clean.prices c JOIN clean.products p USING (chain, product_id)
        WHERE c.unit_confidence = 'high' AND p.pack_unit IN ('g', 'ml') AND c.unit_price IS NOT NULL
        GROUP BY c.chain ORDER BY c.chain
    """).fetchall()
    stats["confidence"] = con.execute("""
        SELECT chain,
               round(100 * avg(coalesce(unit_confidence = 'high', false)::int), 1) AS pct_high,
               round(100 * avg(coalesce(unit_confidence = 'low', false)::int), 1) AS pct_low,
               round(100 * avg((unit_confidence IS NULL)::int), 1) AS pct_none
        FROM clean.prices GROUP BY chain ORDER BY chain
    """).fetchall()
    return stats


def chain_quality_report(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Pokazatelji kvalitete po lancu (za obrazloženje data_quality).

    Stupci: chain, data_quality, % unit_price prazno/0, % cijena > 3x ili < 1/3 sidrene,
    % bez kategorije, % bez marke, % neprepoznatih jedinica, medijan omjera cijene prema
    ostalim lancima za isti EAN, % artikala s odstupanjem > 2x.
    """
    return con.execute("""
        WITH e AS (
          SELECT p.ean_norm, c.chain, median(c.price_eff) AS pe
          FROM clean.prices c JOIN clean.products p USING (chain, product_id)
          WHERE p.ean_global GROUP BY ALL
        ),
        r AS (
          SELECT a.chain, a.pe / median(b.pe) AS ratio
          FROM e a JOIN e b ON a.ean_norm = b.ean_norm AND a.chain <> b.chain
          GROUP BY a.chain, a.ean_norm, a.pe
        ),
        rr AS (SELECT chain, median(ratio) AS med_ratio, avg((ratio > 2 OR ratio < 0.5)::INT) AS off2 FROM r GROUP BY chain),
        pr AS (
          SELECT chain,
                 avg((unit_price IS NULL)::INT) AS up_missing,
                 avg(coalesce(price_eff > 3 * anchor_price OR price_eff < anchor_price / 3, false)::INT) AS anchor_off
          FROM clean.prices GROUP BY chain
        ),
        pd AS (
          SELECT chain, avg((category IS NULL)::INT) AS no_cat, avg((brand IS NULL)::INT) AS no_brand,
                 avg((NOT regexp_full_match(lower(coalesce(unit, '')),
                     'kg|g|l|ml|kom|komad|ko|ea|pak|set|m|kilogram|litra|lt|pz|kpl|par|kut|kar|kmd|gr')
                     AND NOT regexp_matches(coalesce(unit, ''), '[0-9]'))::INT) AS bad_unit
          FROM clean.products GROUP BY chain
        )
        SELECT ch.chain, ch.data_quality,
               round(100 * pr.up_missing, 1), round(100 * pr.anchor_off, 1),
               round(100 * pd.no_cat, 1), round(100 * pd.no_brand, 1), round(100 * pd.bad_unit, 1),
               round(rr.med_ratio, 2), round(100 * rr.off2, 1)
        FROM clean.chains ch JOIN pr USING (chain) JOIN pd USING (chain) LEFT JOIN rr USING (chain)
        ORDER BY ch.data_quality DESC, ch.chain
    """).fetchall()
