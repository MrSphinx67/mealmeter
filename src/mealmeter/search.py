"""Pretraga proizvoda i cijena nad čistim tablicama (schema `clean`)."""

import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import duckdb

from mealmeter.build import NATIONAL_NOTE
from mealmeter.normalize import canonical_city, date_hr, norm_text, normalize_ean

DEFAULT_DB = Path(os.environ.get("MEALMETER_DB", Path(__file__).resolve().parents[2] / "data" / "mealmeter.duckdb"))


def connect(path: str | Path | None = None) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(path or DEFAULT_DB), read_only=True)


def _city_filter(city: str | None) -> tuple[str, list]:
    """Trgovine u gradu (preko aliasa, bez dijakritika/velikih slova) + nacionalne cijene."""
    if not city:
        return "TRUE", []
    return "(s.scope = 'national' OR s.city_key = ? OR s.city_norm = ?)", [
        norm_text(canonical_city(city)),
        norm_text(city),
    ]


def resolve_city(city: str, con: duckdb.DuckDBPyConnection | None = None) -> str | None:
    """Kanonski naziv grada ako u njemu postoji barem jedna (lokalna) trgovina, inače None."""
    con = con or connect()
    sql, params = _city_filter(city)
    row = con.execute(
        f"SELECT any_value(s.city_canonical) FROM clean.stores s WHERE s.scope = 'local' AND {sql}", params
    ).fetchone()
    return row[0] if row else None


def format_pack(amount: float | None, unit: str | None) -> str | None:
    if amount is None or unit is None:
        return None
    if unit in ("g", "ml") and amount >= 1000:
        amount, unit = amount / 1000, "kg" if unit == "g" else "l"
    num = f"{amount:g}".replace(".", ",")
    return f"{num} {unit}"


def _clean(v):
    if isinstance(v, Decimal):
        return float(v)
    return v


def _with_date(row: dict) -> dict:
    d = row.get("date")
    if isinstance(d, date):
        row["date"] = d.isoformat()
        row["date_hr"] = date_hr(d)
    return row


def find_products(
    query: str, city: str | None = None, limit: int = 10, con: duckdb.DuckDBPyConnection | None = None
) -> list[dict]:
    """Proizvodi čiji normalizirani naziv sadrži sve riječi upita.

    Grupira po EAN-u (samo globalni EAN-ovi), a inače po lancu i normaliziranom nazivu. Grupa
    ulazi u rezultat ako barem jedan njezin naziv sadrži sve riječi upita. Poredak: najprije
    grupe u kojima upit pokriva veći dio naziva ("banana" ispred "banana čips 100 g natura"),
    zatim broj lanaca i trgovina. Raspon cijene po jedinici računa iz najpouzdanijeg izvora u grupi (high > low) i
    najčešće jedinice (kg / l / kom). S `city` gleda samo trgovine u tom gradu i nacionalne cijene.
    """
    tokens = (norm_text(query) or "").split()
    if not tokens:
        return []
    con = con or connect()
    name_sql = " AND ".join("p.name_norm LIKE ?" for _ in tokens)
    n_tok = float(len(tokens))
    city_sql, city_params = _city_filter(city)
    best = "x.unit_confidence = conf.conf AND x.per_unit = unit.per_unit"
    sql = f"""
        WITH g AS (
          SELECT *, CASE WHEN ean_global THEN ean_norm ELSE chain || ':' || name_norm END AS gkey
          FROM clean.products p
        ),
        -- grupe u kojima barem jedan naziv odgovara upitu; u grupu ulaze svi proizvodi s tim
        -- EAN-om, i oni čiji naziv je skraćen ("BRAŠ.PŠ.GLATKO")
        hit AS (SELECT DISTINCT gkey FROM g p WHERE {name_sql}),
        x AS (
          SELECT p.gkey, p.chain, p.product_id, p.name, p.name_norm, p.brand,
                 p.pack_amount, p.pack_unit, p.pack_source, p.ean_norm, p.ean_global, ({name_sql}) AS name_hit,
                 -- udio "pravih" riječi naziva (bez brojeva i kratica do 2 slova) koje pokriva upit
                 CASE WHEN ({name_sql}) THEN {n_tok} / greatest({n_tok}, len(
                   [w FOR w IN string_split(p.name_norm, ' ') IF length(w) > 2 AND NOT regexp_matches(w, '^[0-9]')]
                 )) ELSE 0 END AS coverage, c.store_id, c.price_eff, c.price_per_unit, c.per_unit,
                 c.unit_confidence, c.is_special, c.date, s.scope, ch.data_quality
          FROM g p
          JOIN hit USING (gkey)
          JOIN clean.prices c USING (chain, product_id)
          JOIN clean.stores s USING (chain, store_id)
          JOIN clean.chains ch USING (chain)
          WHERE {city_sql}
        ),
        conf AS (
          SELECT gkey, CASE WHEN bool_or(unit_confidence = 'high') THEN 'high'
                            WHEN bool_or(unit_confidence = 'low') THEN 'low' END AS conf
          FROM x GROUP BY gkey
        ),
        unit AS (
          SELECT x.gkey, mode(x.per_unit) AS per_unit
          FROM x JOIN conf USING (gkey) WHERE x.unit_confidence = conf.conf GROUP BY x.gkey
        )
        SELECT
          CASE WHEN bool_or(x.ean_global) THEN any_value(x.ean_norm) FILTER (WHERE x.ean_global)
               ELSE min(x.chain || ':' || x.product_id) END AS id,
          any_value(x.ean_norm) FILTER (WHERE x.ean_global) AS ean,
          -- naziv koji odgovara upitu i sam nosi gramaturu; od takvih najduži (najmanje kratica)
          arg_max(x.name, x.name_hit::INT * 1000
                          + coalesce(x.pack_source = 'name', false)::INT * 500 + length(x.name)) AS name,
          mode(x.brand) AS brand,
          mode(CASE WHEN x.pack_unit IS NOT NULL THEN x.pack_amount::VARCHAR || '|' || x.pack_unit END) AS pack,
          count(DISTINCT x.chain) AS n_chains,
          count(DISTINCT x.chain || '/' || x.store_id) AS n_stores,
          string_agg(DISTINCT x.chain, ', ' ORDER BY x.chain) AS chains,
          min(x.price_eff) AS price_min,
          max(x.price_eff) AS price_max,
          min(x.price_per_unit) FILTER (WHERE {best}) AS price_per_unit_min,
          max(x.price_per_unit) FILTER (WHERE {best}) AS price_per_unit_max,
          unit.per_unit,
          conf.conf AS unit_confidence,
          -- izvor gramature za odabrani raspon: name / unit / ean, ili unit_price kad je confidence low
          CASE WHEN conf.conf = 'low' THEN 'unit_price'
               ELSE mode(x.pack_source) FILTER (WHERE {best}) END AS pack_source,
          string_agg(DISTINCT x.chain, ', ' ORDER BY x.chain) FILTER (WHERE x.data_quality = 'suspect') AS suspect_chains,
          bool_or(x.is_special) AS any_special,
          bool_or(x.scope = 'national') AS has_national,
          max(x.date) AS date,
          bool_or(starts_with(x.name_norm, ?)) AS _starts,
          CASE WHEN max(x.coverage) >= 0.5 THEN 0 WHEN max(x.coverage) >= 0.25 THEN 1 ELSE 2 END AS _tier
        FROM x JOIN conf USING (gkey) LEFT JOIN unit USING (gkey)
        GROUP BY x.gkey, unit.per_unit, conf.conf
        ORDER BY _tier, _starts DESC, n_chains DESC, n_stores DESC, price_per_unit_min NULLS LAST, name
        LIMIT ?
    """
    likes = [f"%{t}%" for t in tokens]
    params = likes * 3 + city_params + [tokens[0], limit]
    cur = con.execute(sql, params)
    cols = [d[0] for d in cur.description]
    out = []
    for r in cur.fetchall():
        row = {c: _clean(v) for c, v in zip(cols, r)}
        row.pop("_starts")
        row.pop("_tier")
        if row["pack"]:
            amount, unit = row["pack"].split("|")
            row["pack"] = format_pack(float(amount), unit)
        if row["has_national"]:
            row["note"] = NATIONAL_NOTE
        out.append(_with_date(row))
    return out


def get_prices(
    identifier: str, city: str | None = None, limit: int = 50, con: duckdb.DuckDBPyConnection | None = None
) -> list[dict]:
    """Cijene po trgovini za EAN ili za `lanac:product_id`, od najjeftinije."""
    ident = identifier.strip()
    if ":" in ident:
        chain, pid = ident.split(":", 1)
        prod_sql, prod_params = "p.chain = ? AND p.product_id = ?", [chain.strip(), pid.strip()]
    else:
        ean, valid, is_global = normalize_ean(ident)
        if not valid:
            raise ValueError(f"'{identifier}' nije valjan EAN; za proizvode bez EAN-a koristi 'lanac:product_id'")
        if not is_global:
            raise ValueError(f"EAN {ean} je interni kod trgovine (vaga/in-store); koristi 'lanac:product_id'")
        prod_sql, prod_params = "p.ean_norm = ?", [ean]
    con = con or connect()
    city_sql, city_params = _city_filter(city)
    cur = con.execute(
        f"""
        SELECT p.chain, s.store_id, s.address, s.city, s.scope, p.product_id, p.ean_norm AS ean, p.name,
               c.price_eff, c.is_special, c.special_price, c.anchor_price, c.best_price_30,
               c.price_per_unit, c.per_unit, c.unit_confidence,
               CASE WHEN c.unit_confidence = 'low' THEN 'unit_price'
                    WHEN c.unit_confidence = 'high' THEN p.pack_source END AS pack_source,
               ch.data_quality, c.date
        FROM clean.products p
        JOIN clean.prices c USING (chain, product_id)
        JOIN clean.stores s USING (chain, store_id)
        JOIN clean.chains ch USING (chain)
        WHERE {prod_sql} AND {city_sql}
        ORDER BY c.price_eff, p.chain, s.city, s.address
        LIMIT ?
        """,
        prod_params + city_params + [limit],
    )
    cols = [d[0] for d in cur.description]
    out = []
    for r in cur.fetchall():
        row = {c: _clean(v) for c, v in zip(cols, r)}
        if row["scope"] == "national":
            row["note"] = NATIONAL_NOTE
        out.append(_with_date(row))
    return out
