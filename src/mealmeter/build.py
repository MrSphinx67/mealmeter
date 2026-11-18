"""Učitavanje dnevne arhive cijene.dev u DuckDB i izgradnja čistih tablica (schema `clean`)."""

import csv
import difflib
import os
import re
import tempfile
from pathlib import Path

import duckdb

from mealmeter.food import build_food
from mealmeter.staples import build_staple_prices, build_staples, match_text
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
# Neprehrambene poslovnice (Korak 15): od 17.11.2026. (NN 101/26, 110/26) cjenike objavljuju i usluge i druge
# djelatnosti lanca (KTC: poljoljekarne, benzinske, autopraona, frizerski i kozmetički salon). Prepoznaju se po
# tipu poslovnice (norm_text, bilo gdje u tekstu) i ne ulaze u clean.stores ni clean.prices, pa ni u alate i
# košaricu; sirove tablice ih zadržavaju. Novi tip poslovnice koji nije ovdje ostaje u bazi (vidi docs/15_STATUS.md).
NONFOOD_STORE_TYPES = ("ljekarn", "apotek", "benzin", "crpk", "praon", "salon", "frizer", "kozmet", "servis",
                       "vulkaniz")

# roba na vagu u nazivu (Korak 17): "rinfuza", "rinfuzo"
LOOSE_NAME_RX = re.compile(r"(^| )rinfuz")

NATIONAL_NOTE = "Nacionalna cijena (web/sve poslovnice); provjeri dostupnost u svom gradu."


def nonfood_store_type(store_type: str | None) -> bool:
    """Tip poslovnice je usluga ili neprehrambena djelatnost (NONFOOD_STORE_TYPES)."""
    t = norm_text(store_type) or ""
    return any(w in t for w in NONFOOD_STORE_TYPES)


# CSV arhive (Korak 18): navodnik zadan izričito. Sniffer DuckDB-a ga inače ne prepozna kad u datoteci postoji samo
# jedan polje u navodnicima (vrutak 18.11.2026.: `vodovodna,"219602,",7.99,15.98`), pa pomakne stupce: šifra '"219602',
# cijena '"'. S navodnikom je to šifra "219602," (ista kao u products.csv) i cijena 7.99.
CSV_OPTS = "header=true, all_varchar=true, quote='\"', escape='\"'"

# Neparsabilne cijene (Korak 18): redak s cijenom koja se ne da pročitati preskače se uz upozorenje; baza se odbija
# tek kad je takvih više od MAX_BAD_PRICE_SHARE redaka cijena nekog lanca (kvar izvoza, a ne jedan loš redak).
MAX_BAD_PRICE_SHARE = 0.01
BAD_PRICE_EXAMPLES = 3
# decimalni zarez ("7,99") je ispravna cijena u drugom zapisu: čita se kao 7.99
DECIMAL_COMMA_RX = r"[+-]?[0-9]+,[0-9]+"


class BadPriceError(ValueError):
    """Lanac ima više od MAX_BAD_PRICE_SHARE redaka s neparsabilnom cijenom."""


def price_sql(col: str) -> str:
    """SQL: sirova cijena (tekst) u DECIMAL(10,2); prazno je NULL, decimalni zarez se prihvaća, ostalo NULL."""
    t = f"trim({col})"
    return (f"TRY_CAST(CASE WHEN regexp_full_match({t}, '{DECIMAL_COMMA_RX}') THEN replace({t}, ',', '.') "
            f"ELSE NULLIF({t}, '') END AS DECIMAL(10,2))")


def bad_price_sql(col: str) -> str:
    """SQL: sirova cijena nije prazna, a ne da se pročitati."""
    return f"(NULLIF(trim({col}), '') IS NOT NULL AND {price_sql(col)} IS NULL)"


def describe_bad_prices(b: dict) -> str:
    """Jedan redak za lanac s neparsabilnim cijenama (iz load_raw)."""
    return (f"{b['chain']}: {b['bad']} od {b['total']} redaka cijena s neparsabilnom cijenom ({b['pct']:.2f} %); "
            f"primjeri: {'; '.join(b['examples'])}")


def load_raw(con: duckdb.DuckDBPyConnection, root: Path, archive_date: str,
             bad_prices: list[dict] | None = None) -> list[str]:
    """Sirovi CSV-ovi u tablice stores/products/prices, bez normalizacije.

    Dodaje stupac `chain` (naziv mape) i `date` (dan iz naziva arhive) u prices. Retci s neparsabilnom cijenom se
    preskaču i dodaju u `bad_prices` ({chain, bad, total, pct, examples}); više od MAX_BAD_PRICE_SHARE takvih redaka
    jednog lanca diže BadPriceError.
    """

    def raw(chain: str, name: str) -> str:
        # Sve kao tekst: šifre imaju vodeće nule
        return f"read_csv('{root / chain / name}', {CSV_OPTS})"

    chains = sorted(p.name for p in Path(root).iterdir() if p.is_dir())
    con.execute("DROP TABLE IF EXISTS stores; DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS prices")
    casts = ", ".join(f"{price_sql(c)} AS {c}" for c in PRICE_COLS)
    bad = " OR ".join(bad_price_sql(c) for c in PRICE_COLS)
    for i, chain in enumerate(chains):
        n_total, n_bad = con.execute(
            f"SELECT count(*), count(*) FILTER (WHERE {bad}) FROM {raw(chain, 'prices.csv')}").fetchone()
        if n_bad:
            # primjer: trgovina/šifra i sirove vrijednosti samo neparsabilnih stupaca
            flags = ", ".join(f"{bad_price_sql(c)}" for c in PRICE_COLS)
            rows = con.execute(
                f"SELECT store_id, product_id, {', '.join(PRICE_COLS)}, {flags} FROM {raw(chain, 'prices.csv')} "
                f"WHERE {bad} ORDER BY store_id, product_id LIMIT {BAD_PRICE_EXAMPLES}").fetchall()
            k = len(PRICE_COLS)
            examples = [f"{r[0]}/{r[1]} " + ", ".join(f"{c}={v!r}" for c, v, f in zip(PRICE_COLS, r[2:2 + k], r[2 + k:])
                                                    if f)
                        for r in rows]
            info = {"chain": chain, "bad": n_bad, "total": n_total, "pct": 100 * n_bad / n_total,
                    "examples": examples}
            if n_bad > n_total * MAX_BAD_PRICE_SHARE:
                raise BadPriceError(f"{describe_bad_prices(info)}; više od {100 * MAX_BAD_PRICE_SHARE:g} % redaka "
                                    f"lanca, baza odbijena")
            if bad_prices is not None:
                bad_prices.append(info)
        verb = "CREATE TABLE {} AS" if i == 0 else "INSERT INTO {}"
        con.execute(f"{verb.format('stores')} SELECT '{chain}' AS chain, * FROM {raw(chain, 'stores.csv')}")
        con.execute(f"{verb.format('products')} SELECT '{chain}' AS chain, * FROM {raw(chain, 'products.csv')}")
        con.execute(
            f"{verb.format('prices')} SELECT '{chain}' AS chain, store_id, product_id, {casts}, "
            f"DATE '{archive_date}' AS date FROM {raw(chain, 'prices.csv')} WHERE NOT ({bad})"
        )
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
        for chain, store_id, city, typ in con.execute("SELECT chain, store_id, city, type FROM stores").fetchall():
            city = (city or "").strip() or CITY_FIXES.get((chain, store_id))
            canonical = canonical_city(city)
            yield (chain, store_id, city, norm_text(city), canonical, norm_text(canonical),
                   nonfood_store_type(typ))

    _temp_table(con, "store_derived", {
        "chain": "VARCHAR", "store_id": "VARCHAR", "city": "VARCHAR", "city_norm": "VARCHAR",
        "city_canonical": "VARCHAR", "city_key": "VARCHAR", "nonfood": "BOOLEAN",
    }, store_rows())
    con.execute("""CREATE OR REPLACE TEMP TABLE nonfood_stores AS
                   SELECT DISTINCT r.chain, r.store_id, r.type FROM stores r JOIN store_derived d USING (chain, store_id)
                   WHERE d.nonfood""")
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
        WHERE NOT d.nonfood
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
            elif pack and pack[1] == "g" and (by_unit := parse_pack_unit_field(unit)) and by_unit[1] == "ml":
                # tekućina: stupac unit kaže l/ml, a naziv daje grame ("Suncokretovo ulje 20g Lidla", unit 1l):
                # vrijedi unit (Korak 5A, docs/lidl_raw_check.md)
                pack, source, confidence = by_unit, "unit", "high"
            hint = unit_hint(unit, quantity)
            if source == "unit" and pack == (1000.0, "g") and LOOSE_NAME_RX.search(norm_text(name) or ""):
                # Korak 17: Lidl "Mrkva rinfuza", unit "1kg": roba na vagu, cijena je po kg, a ne pakiranje od 1 kg
                pack, variable, hint, confidence = None, True, "kg", None
            amount, pack_unit = pack or (None, None)
            yield (chain, pid, ean, valid, glob, norm_text(name), match_text(name), amount, pack_unit,
                   source if pack else None, hint,
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

    stats_dummy = flag_dummy_eans(con)
    stats_incoherent = flag_incoherent_eans(con)

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
        FROM prices r
        WHERE NOT EXISTS (SELECT 1 FROM nonfood_stores n WHERE n.chain = r.chain AND n.store_id = r.store_id)
    """)
    quantity_packs(con)
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

    stats = {"food": food_stats, "dummy_eans": stats_dummy, "ean_incoherent": stats_incoherent,
             "nonfood_stores": con.execute("""SELECT chain, type, count(*) FROM nonfood_stores
                                              GROUP BY ALL ORDER BY chain, type""").fetchall()}
    stats["quality"] = chain_quality_report(con)
    stats["staples"] = build_staples(con)
    stats["staple_prices"] = build_staple_prices(con)  # cijene po namirnici za brze kandidate (Korak 5P)
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


# Korak 17: pakiranje iz stupca quantity. Proizvod bez gramature u nazivu ("CELER LIST KOM", quantity "0.50 kg",
# cijena 1,99 €, unit_price 3,98 €/kg) prodaje se na komad: cijena je za komad mase quantity, a unit_price lanca je
# cijena / quantity. Bez toga ga košarica računa na vagu (50 g x 3,98 €/kg = 0,20 €). Vrijedi samo kad quantity ima
# jedinicu mase ili volumena (ili je jedinica cijene kg/l) i kad je u većini cijena cijena / unit_price = quantity
# (±5 %); quantity od 1 kg/l je i "cijena po kg", pa se preskače. Broj komada ("10.00" kod jaja) i boce bez jedinice
# ("0,7500") se ne čitaju.
QUANTITY_PACK_TOLERANCE = 0.05


def quantity_packs(con: duckdb.DuckDBPyConnection) -> int:
    """pack_amount/pack_unit iz quantity (pack_source 'quantity') za proizvode bez gramature; treba prices_nz.
    Vraća broj proizvoda."""
    num = r"^\s*([0-9]*[.,]?[0-9]+)\s*[a-zA-Z]*\s*$"
    unit = r"^\s*[0-9]*[.,]?[0-9]+\s*([a-zA-Z]*)\s*$"
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE quantity_pack AS
        WITH q AS (
          SELECT chain, product_id, unit_hint,
                 try_cast(replace(regexp_extract(quantity, '{num}', 1), ',', '.') AS DOUBLE) AS qn,
                 lower(regexp_extract(quantity, '{unit}', 1)) AS qu
          FROM clean.products WHERE pack_amount IS NULL AND quantity IS NOT NULL
        ),
        w AS (
          SELECT chain, product_id,
                 CASE WHEN qu IN ('g', 'gr', 'ml') THEN qn
                      WHEN qu IN ('kg', 'l') OR (qu = '' AND unit_hint IN ('kg', 'l')) THEN qn * 1000 END AS amount,
                 CASE WHEN qu IN ('ml', 'l') OR (qu = '' AND unit_hint = 'l') THEN 'ml'
                      WHEN qu IN ('g', 'gr', 'kg') OR (qu = '' AND unit_hint = 'kg') THEN 'g' END AS unit
          FROM q
        ),
        r AS (
          SELECT w.chain, w.product_id, w.amount, w.unit,
                 abs(coalesce(p.price, p.price_eff) / p.unit_price - w.amount / 1000)
                   <= {QUANTITY_PACK_TOLERANCE} * w.amount / 1000 AS ok
          FROM w JOIN prices_nz p USING (chain, product_id)
          WHERE w.amount > 0 AND w.unit IS NOT NULL AND abs(w.amount - 1000) > 10 AND p.unit_price > 0
            AND coalesce(p.price, p.price_eff) > 0
        )
        SELECT chain, product_id, amount, unit FROM r GROUP BY ALL HAVING avg(ok::int) > 0.5
    """)
    con.execute("""
        UPDATE clean.products p SET pack_amount = q.amount, pack_unit = q.unit, pack_source = 'quantity',
                                    pack_confidence = 'high'
        FROM quantity_pack q WHERE p.chain = q.chain AND p.product_id = q.product_id""")
    return con.execute("SELECT count(*) FROM quantity_pack").fetchone()[0]


DUMMY_EANS_PATH = Path(__file__).resolve().parents[2] / "data" / "dummy_eans.yaml"
DUMMY_MIN_NAMES = 5  # isti EAN za toliko različitih name_norm u jednom lancu = zamjenski barkod


def flag_dummy_eans(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Lažni EAN-ovi postaju ean_global = false (grupa po lancu + name_norm), uz razlog u ean_note:
    - 'dummy_list': na popisu data/dummy_eans.yaml (svi lanci);
    - 'repeated_digit': jedna ponavljajuća znamenka, npr. 0000000000000 (svi lanci);
    - 'multi_name': lanac ga koristi za >= DUMMY_MIN_NAMES različitih name_norm (samo taj lanac;
      Eurospinov 9999999999994 za biljke, voće i povrće).
    Vraća (lanac, razlog, EAN-ova, proizvoda)."""
    import yaml

    listed = [str(e) for e in (yaml.safe_load(DUMMY_EANS_PATH.read_text(encoding="utf-8")) or [])] \
        if DUMMY_EANS_PATH.exists() else []
    con.execute("ALTER TABLE clean.products ADD COLUMN ean_note VARCHAR")
    con.execute("CREATE OR REPLACE TEMP TABLE dummy_list (ean VARCHAR)")
    con.executemany("INSERT INTO dummy_list VALUES (?)", [(e,) for e in listed])
    con.execute("""
        UPDATE clean.products SET ean_global = false,
               ean_note = CASE WHEN ean_norm IN (SELECT ean FROM dummy_list) THEN 'dummy_list' ELSE 'repeated_digit' END
        WHERE ean_norm IS NOT NULL
          AND (ean_norm IN (SELECT ean FROM dummy_list) OR length(ltrim(ean_norm, left(ean_norm, 1))) = 0)
    """)
    con.execute(f"""
        UPDATE clean.products p SET ean_global = false, ean_note = 'multi_name'
        FROM (SELECT chain, ean_norm FROM clean.products WHERE ean_global
              GROUP BY ALL HAVING count(DISTINCT name_norm) >= {DUMMY_MIN_NAMES}) d
        WHERE p.chain = d.chain AND p.ean_norm = d.ean_norm
    """)
    return con.execute("""SELECT chain, ean_note, count(DISTINCT ean_norm), count(*) FROM clean.products
                          WHERE ean_note IS NOT NULL GROUP BY ALL ORDER BY 4 DESC""").fetchall()


# Koherentnost EAN grupe (Korak 4B): značajne riječi naziva su bez brojeva, riječi kraćih od 4 slova, marke
# i ovih riječi (jedinice, pakiranje, akcije)
EAN_STOPWORDS = frozenset("""
    komad komada komadi kom. grama gram litra litre pakiranje pakiranja paket pack gratis akcija cijena super
    novo novi nova extra plus mini maxi ultra classic original""".split())
EAN_COHERENT_SHARE = 0.5


def _ean_tokens(text: str | None, brand: str | None) -> set[str]:
    """Značajne riječi naziva (match_norm): samo slova, >= 4 slova, bez marke i EAN_STOPWORDS."""
    brand_words = set((norm_text(brand) or "").split())
    return {w for w in _ean_words(text) if len(w) >= 4 and w not in brand_words}


def _ean_words(text: str | None) -> set[str]:
    """Sve riječi naziva kao dokaz prisutnosti: samo slova, >= 3 slova (kratice "reb", "dim"), s markom."""
    return {w for w in (text or "").split() if len(w) >= 3 and w.isalpha() and w not in EAN_STOPWORDS}


def _shares(a: str, b: str) -> bool:
    """Ista riječ, jedna je početak druge (kratice: "reb" / "rebra") ili se razlikuju u slovu-dva
    ("ementaler" / "emmentaler")."""
    if a.startswith(b) or b.startswith(a):
        return True
    m = difflib.SequenceMatcher(None, a, b)
    return m.real_quick_ratio() >= 0.8 and m.ratio() >= 0.8


def ean_coherence(chains: dict[str, tuple[set[str], set[str]]]) -> tuple[bool, set[str]]:
    """(koherentna, lanci izvan grupe) za EAN grupu {lanac: (značajne riječi, sve riječi)} svih njegovih naziva.

    Značajna riječ (_ean_tokens) je "u nazivima lanca" ako je lanac ima ili ima njezinu kraticu ili
    marku-riječ koja je pokriva (_ean_words, _shares): nazivi lanaca su jako skraćeni ("PIVAC DIM.SVINJ REB").
    Koherentna je grupa u kojoj je barem jedna značajna riječ u nazivima >= 50 % lanaca i barem dva lanca
    (kod dva lanca riječ jednog lanca inače uvijek pokriva 50 %). Lanci bez ijedne riječi ne glasaju.
    U koherentnoj grupi s >= 3 lanca ispada lanac koji ne dijeli nijednu riječ ni s jednim drugim lancem
    (KIBLA ZA VINO, KIBLA PVC / JOGURT TEK.)."""
    voting = {c: tw for c, tw in chains.items() if tw[1]}
    if len(voting) < 2:
        return True, set()
    need = max(2, EAN_COHERENT_SHARE * len(voting))

    def has(words: set[str], token: str) -> bool:
        return any(_shares(token, w) for w in words)

    # kandidati: značajne riječi i, jer su nazivi često samo marka i kratice ("BEBIMIL 1 600 g", "SIR ABC
    # 200G"), sve riječi od >= 3 slova s markom; strogo pravilo (samo značajne riječi) označilo je ~1 550
    # grupa, uglavnom isti proizvod (pregled Korak 4B)
    candidates = {t for sig, words in voting.values() for t in sig | words}
    if not any(sum(has(words, t) for _, words in voting.values()) >= need for t in candidates):
        return False, set()
    if len(voting) < 3:
        return True, set()
    outliers = {c for c, (_, words) in voting.items()
                if not any(has(other, w) for w in words for d, (_, other) in voting.items() if d != c)}
    return True, outliers


def flag_incoherent_eans(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Globalni EAN koji u različitim lancima nosi nespojive nazive (isti barkod za "MRKVA 500 G" i
    "KUKURUZ ŠEĆERAC 3/1") nije isti proizvod: grupa se razdvaja po lancu + name_norm (ean_global = false,
    ean_incoherent = true); kod koherentne grupe ispada samo lanac bez zajedničkih riječi (ean_coherence).
    Detalji su u clean.ean_incoherent (ean, lanac, naziv, razlog 'group' | 'outlier').
    Vraća (lanac, grupa, proizvoda) za izvještaj."""
    con.execute("ALTER TABLE clean.products ADD COLUMN ean_incoherent BOOLEAN DEFAULT false")
    rows = con.execute("""
        SELECT ean_norm, chain, product_id, name, match_norm, brand FROM clean.products
        WHERE ean_global AND ean_norm IN (
          SELECT ean_norm FROM clean.products WHERE ean_global GROUP BY ALL HAVING count(DISTINCT chain) >= 2)
        ORDER BY ean_norm, chain, product_id""").fetchall()
    groups: dict[str, list[tuple]] = {}
    for r in rows:
        groups.setdefault(r[0], []).append(r)
    flagged = []
    for ean, members in groups.items():
        by_chain: dict[str, tuple[set[str], set[str]]] = {}
        for _, chain, _, _, text, brand in members:
            sig, words = by_chain.setdefault(chain, (set(), set()))
            sig.update(_ean_tokens(text, brand))
            words.update(_ean_words(text))
        ok, outliers = ean_coherence(by_chain)
        for _, chain, pid, name, _, _ in members:
            if not ok or chain in outliers:
                flagged.append((ean, chain, pid, name, "group" if not ok else "outlier"))
    _temp_table(con, "incoherent_tmp", {"ean_norm": "VARCHAR", "chain": "VARCHAR", "product_id": "VARCHAR",
                                        "name": "VARCHAR", "reason": "VARCHAR"}, flagged)
    con.execute("CREATE OR REPLACE TABLE clean.ean_incoherent AS SELECT * FROM incoherent_tmp")
    con.execute("""
        UPDATE clean.products p SET ean_global = false, ean_incoherent = true
        FROM clean.ean_incoherent i WHERE p.chain = i.chain AND p.product_id = i.product_id""")
    return con.execute("""SELECT chain, reason, count(DISTINCT ean_norm), count(*) FROM clean.ean_incoherent
                          GROUP BY ALL ORDER BY 3 DESC""").fetchall()


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
