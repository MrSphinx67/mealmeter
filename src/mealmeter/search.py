"""Pretraga proizvoda i cijena nad čistim tablicama (schema `clean`)."""

import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import duckdb

from mealmeter.build import NATIONAL_NOTE
from mealmeter.normalize import canonical_city, date_hr, norm_text, normalize_ean
from mealmeter.staples import BKEY_SQL, STAPLE_PPU_SQL, load_staples, resolve_ingredient, staple_suspect_sql

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


def _food_filter(include_nonfood: bool = False, include_alcohol: bool = False, unverified: str = "no") -> str:
    """SQL uvjet nad clean.products (alias p) za filtar hrane (food.py).

    Zadano samo is_food = true i bez alkohola. `unverified`: "no" (food_group 'unknown' ne ulazi),
    "yes" (ulazi) ili "staple" (ulazi samo proizvod koji je sam povezan s namirnicom, psu; za
    loose_produce u košarici, gdje naziv već prolazi strogo pravilo prve ili druge riječi).
    """
    allowed = ["p.is_food"]
    if include_nonfood:
        allowed.append("NOT p.is_food")
    if unverified == "yes":
        allowed.append("p.is_food IS NULL")
    elif unverified == "staple":
        allowed.append("(p.is_food IS NULL AND psu.staple IS NOT NULL AND NOT psu.excluded)")
    sql = "(" + " OR ".join(f"coalesce({a}, false)" for a in allowed) + ")"
    if not include_alcohol:
        sql += " AND p.food_group <> 'alkohol'"
    return sql


def _candidates(staple, tokens: list[str], attributes: dict | None, city: str | None,
                include_clearance: bool, food_sql: str | None = None,
                include_ambiguous: bool = False, include_wholesale: bool = False) -> tuple[str, list, str]:
    """SQL (CTE-ovi g, hit, x) za kandidate: jedan redak po (trgovina, proizvod).

    x sadrži sve proizvode iz grupa koje odgovaraju upitu/namirnici, s cijenom po jedinici u
    jedinici usporedbe namirnice (STAPLE_PPU_SQL), pouzdanošću, izvorom gramature i zastavicama
    (price_suspect, clearance, pack_confidence, data_quality). Koriste ga find_products i plan_basket.
    `food_sql` je uvjet filtra hrane (_food_filter; zadano samo provjerena hrana bez alkohola).
    Grupe (bkey: EAN, inače lanac + naziv) biraju se po clean.staple_groups (status 'member'; uz
    include_ambiguous i 'ambiguous') i atributima grupe (clean.staple_group_attrs). Kod namirnice s
    group_by (jaja) izlazni ključ gkey je klasa, a izbor je i dalje po EAN grupi.
    Vraća (sql, parametri, stupac relevantnosti za razinu grupe).
    """
    food_sql = food_sql or _food_filter()
    city_sql, city_params = _city_filter(city)
    name_sql = " AND ".join("p.name_norm LIKE ?" for _ in tokens) or "TRUE"
    likes = [f"%{t}%" for t in tokens]

    # --- koje grupe ulaze u rezultat ---
    hit_parts, hit_params = [], []
    if tokens:
        hit_parts.append(f"SELECT DISTINCT bkey FROM g p WHERE {name_sql}")
        hit_params += likes
    if staple:
        statuses = "'member', 'ambiguous'" if include_ambiguous else "'member'"
        hit_parts.append(f"SELECT bkey FROM clean.staple_groups WHERE staple = ? AND status IN ({statuses})")
        hit_params.append(staple.key)
        for attr, value in (attributes or {}).items():
            # zamjenjive vrijednosti (mlijeko: mast 2.8 = 3.2 = 3.5 = 3.8)
            accepted = staple.accepted_values(attr, value)
            hit_parts.append(f"""
                SELECT bkey FROM clean.staple_group_attrs
                WHERE staple = ? AND attr = ? AND value IN ({", ".join("?" for _ in accepted)})""")
            hit_params += [staple.key, attr, *accepted]
    hit_sql = " INTERSECT ".join(f"({h})" for h in hit_parts)
    if staple:
        # zadano isključene varijante (bez glutena, integralno...) osim ako je atribut tražen
        for attr, value in staple.default_exclude_variants:
            if attr in (attributes or {}):
                continue
            hit_sql = f"""({hit_sql}) EXCEPT (
                SELECT bkey FROM clean.staple_group_attrs WHERE staple = ? AND attr = ? AND value = ?)"""
            hit_params += [staple.key, attr, value]

    if staple:
        # "pogodak" za izbor prikaznog naziva; razina 0 ako je riječ namirnice među prve tri riječi
        # u većini naziva grupe (prosjek: "CEDEVITA KIDS BANANA" ne čini Cedevitu bananom)
        name_hit_sql = f"""EXISTS (SELECT 1 FROM clean.product_staples ps WHERE ps.chain = p.chain
                              AND ps.product_id = p.product_id AND ps.staple = '{staple.key}'
                              AND NOT ps.excluded AND ps.drop_reason IS NULL)"""
        name_hit_params = []
        coverage_sql = f"CASE WHEN {name_hit_sql} AND regexp_matches(p.name_norm, ?) THEN 1.0 ELSE 0.0 END"
        coverage_params = [staple.early_regex]
        cov_col = "cov.cov_avg"
        # članovi grupe koje namirnica odbacuje (neprehrambena kategorija, pakiranje) ne ulaze u cijene
        drop_sql = f"""NOT EXISTS (SELECT 1 FROM clean.product_staples d WHERE d.chain = p.chain
                      AND d.product_id = p.product_id AND d.staple = '{staple.key}' AND d.drop_reason IS NOT NULL)"""
        rules_join = f"""LEFT JOIN clean.product_staples psu ON psu.chain = p.chain
                           AND psu.product_id = p.product_id AND psu.staple = '{staple.key}'
                         CROSS JOIN (SELECT * FROM clean.staple_rules WHERE staple = '{staple.key}') r
                         LEFT JOIN clean.staple_groups sg ON sg.staple = '{staple.key}' AND sg.bkey = p.bkey"""
        quality_sql = "sg.match_quality"
        ppu_sql = STAPLE_PPU_SQL.replace("ps.", "psu.")
        per_unit_sql = """CASE WHEN r.compare_by IN ('pack', 'count') THEN CASE WHEN psu.n_units > 0 THEN r.compare_unit END
                               WHEN psu.assumed_g > 0 THEN r.unit ELSE c.per_unit END"""
        conf_sql = """CASE WHEN r.compare_by IN ('pack', 'count') THEN CASE WHEN psu.n_units > 0 THEN 'high' END
                           WHEN psu.assumed_g > 0 THEN 'low' ELSE c.unit_confidence END"""
        source_sql = """CASE WHEN r.compare_by = 'count' AND psu.n_units > 0 THEN 'name'
                             WHEN r.compare_by = 'pack' AND psu.n_units > 0 THEN p.pack_source
                             WHEN psu.assumed_g > 0 THEN 'assumed'
                             WHEN c.unit_confidence = 'low' THEN 'unit_price' ELSE p.pack_source END"""
        suspect_sql = f"""coalesce(({per_unit_sql}) = r.compare_unit
                                   AND {staple_suspect_sql(ppu_sql, "psu.n_units", "psu")}, false)"""
        n_units_sql, assumed_sql = "psu.n_units", "psu.assumed_g"
        clearance_sql = "TRUE" if include_clearance else "NOT p.clearance"
    else:
        name_hit_sql, name_hit_params = f"({name_sql})", likes
        n_tok = float(len(tokens))
        # udio "pravih" riječi naziva (bez brojeva i kratica do 2 slova) koje pokriva upit
        coverage_sql = f"""CASE WHEN ({name_sql}) THEN {n_tok} / greatest({n_tok}, len(
                   [w FOR w IN string_split(p.name_norm, ' ') IF length(w) > 2 AND NOT regexp_matches(w, '^[0-9]')]
                 )) ELSE 0 END"""
        coverage_params = likes
        cov_col = "cov.cov_max"
        drop_sql, rules_join, quality_sql = "TRUE", "", "NULL::VARCHAR"
        ppu_sql, per_unit_sql, conf_sql = "c.price_per_unit", "c.per_unit", "c.unit_confidence"
        source_sql = "CASE WHEN c.unit_confidence = 'low' THEN 'unit_price' ELSE p.pack_source END"
        suspect_sql, n_units_sql, assumed_sql, clearance_sql = "false", "NULL::DOUBLE", "NULL::DOUBLE", "TRUE"

    gkey_expr, gkey_join = _gkey_sql(staple)
    sql = f"""
        WITH g AS (
          SELECT p.*, {gkey_expr} AS gkey, {BKEY_SQL} AS bkey FROM clean.products p {gkey_join}
        ),
        hit AS ({hit_sql}),
        x AS (
          SELECT p.gkey, p.chain, p.product_id, p.name, p.name_norm, p.brand,
                 p.pack_amount, p.pack_unit, p.pack_confidence, p.drained_amount, p.ean_norm, p.ean_global,
                 {name_hit_sql} AS name_hit,
                 {coverage_sql} AS coverage,
                 c.store_id, c.price_eff, ({ppu_sql}) AS price_per_unit, ({per_unit_sql}) AS per_unit,
                 ({conf_sql}) AS unit_confidence, ({source_sql}) AS pack_source, ({suspect_sql}) AS price_suspect,
                 {n_units_sql} AS n_units, {assumed_sql} AS assumed_g,
                 c.price_per_kg_drained, p.variable_weight, p.clearance,
                 c.is_special, c.date, s.scope, s.address, s.city, ch.data_quality,
                 p.is_food, p.food_group, p.category_source, p.bkey, {quality_sql} AS match_quality
          FROM g p
          JOIN hit USING (bkey)
          JOIN clean.prices c USING (chain, product_id)
          JOIN clean.stores s USING (chain, store_id)
          JOIN clean.chains ch USING (chain)
          {rules_join}
          WHERE {city_sql} AND {drop_sql} AND {clearance_sql} AND {food_sql}
            AND {"TRUE" if include_wholesale else "s.store_type <> 'cash_and_carry'"}
        )"""
    return sql, hit_params + name_hit_params + coverage_params + city_params, cov_col


def find_products(
    query: str | None = None,
    city: str | None = None,
    limit: int = 10,
    con: duckdb.DuckDBPyConnection | None = None,
    ingredient: str | None = None,
    attributes: dict[str, str] | None = None,
    include_clearance: bool = False,
    include_nonfood: bool = False,
    include_alcohol: bool = False,
    include_unverified: bool = False,
    include_ambiguous: bool = False,
    include_wholesale: bool = False,
) -> list[dict]:
    """Pronađi proizvode po nazivu ili po osnovnoj namirnici (staples.yaml).

    Zadano vraća samo hranu (is_food = true) bez alkohola. `include_nonfood` dodaje neprehrambene
    proizvode, `include_alcohol` alkoholna pića, a `include_unverified` proizvode nepoznate skupine
    (food_group 'unknown', npr. Plodine bez EAN-a u drugim lancima); grupa sastavljena samo od
    takvih nosi `food_unverified = true`. Za namirnicu se zadano vraćaju samo grupe sa statusom
    'member' (clean.staple_groups: većina lanaca ima naziv namirnice); `include_ambiguous` dodaje
    dvosmislene grupe ("KUPUS KIS MASL ULJE" kod maslinovog ulja). Veleprodaja (Metro,
    store_type 'cash_and_carry') zadano nije uključena (`include_wholesale`).

    - Slobodan upit: proizvod odgovara ako normalizirani naziv sadrži sve riječi upita. Ako je
      upit točno sinonim namirnice ("mlijeko", "brašno"), automatski se koristi namirnica.
    - `ingredient` (kanonski ključ ili sinonim): pravila namirnice (must_match/must_not_match),
      cijena po jedinici u njezinoj jedinici (kg/l/kom), a `attributes` filtrira po atributima
      iz naziva, npr. {"tip": "glatko"}. Uz `ingredient` slobodan upit dodatno sužava po nazivu.
      Za namirnicu se zadano izostavljaju: rasprodaja ("SNIŽENJE"; `include_clearance=True` ih
      vraća), varijante iz default_exclude_variants (osim ako je atribut izričito zadan),
      pakiranja izvan min_pack/max_pack, a cijene po jedinici izvan plausible_per_unit
      (price_suspect) ne ulaze u raspon cijena.

    Grupira po EAN-u (samo globalni EAN-ovi), a inače po lancu i normaliziranom nazivu; grupa
    ulazi ako barem jedan njezin naziv odgovara (kod namirnice: i nijedan nije isključen).
    Poredak za slobodan upit: najprije grupe u kojima upit pokriva veći dio naziva ("banana"
    ispred "banana čips 100 g natura"); za namirnicu najprije grupe u kojima je riječ namirnice
    među prve tri riječi naziva ("MRKVA ..." ispred "KEKS NUTRI MRKVA"). Zatim broj lanaca i trgovina. Raspon cijene po jedinici
    računa se iz najpouzdanijeg izvora u grupi (high > low) i najčešće jedinice. S `city` gleda
    samo trgovine u tom gradu i nacionalne cijene.
    """
    staple = None
    if ingredient:
        staple = resolve_ingredient(ingredient)
        if staple is None:
            raise ValueError(f"Nepoznata namirnica '{ingredient}' (vidi staples.yaml)")
    elif attributes:
        raise ValueError("attributes se koriste samo uz ingredient")
    else:
        staple = resolve_ingredient(query)
        if staple:
            query = None  # upit je samo naziv namirnice
    if staple and staple.defaults():
        # zadani filtar namirnice (mlijeko: vrsta=trajno; mljeveno meso: miješano, juneće ili svinjsko)
        # osim ako je atribut zadan
        attributes = {**staple.defaults(), **(attributes or {})}
    if attributes:
        unknown = {a: v for a, v in attributes.items()
                   if any(x not in staple.attributes.get(a, {}) for x in (v if isinstance(v, tuple) else (v,)))}
        if unknown:
            available = {a: list(v) for a, v in staple.attributes.items()}
            raise ValueError(f"Nepoznati atributi za '{staple.key}': {unknown}; dostupni: {available}")

    tokens = (norm_text(query) or "").split()
    if not tokens and staple is None:
        return []
    con = con or connect()
    food_sql = _food_filter(include_nonfood, include_alcohol, "yes" if include_unverified else "no")
    cand_sql, cand_params, cov_col = _candidates(staple, tokens, attributes, city, include_clearance, food_sql,
                                                 include_ambiguous, include_wholesale)
    best = "x.unit_confidence = pick.conf AND x.per_unit = pick.per_unit AND NOT x.price_suspect"
    sql = f"""
        {cand_sql},
        -- relevantnost grupe po različitim proizvodima (ne po broju trgovina)
        cov AS (
          SELECT gkey, max(coverage) AS cov_max, avg(coverage) AS cov_avg
          FROM (SELECT DISTINCT gkey, chain, product_id, coverage FROM x) GROUP BY gkey
        ),
        -- izvor cijene po jedinici za grupu: jedinica namirnice (ako je zadana), zatim high > low,
        -- zatim najčešća jedinica
        pick AS (
          SELECT gkey, unit_confidence AS conf, per_unit FROM (
            SELECT gkey, unit_confidence, per_unit, count(*) AS n FROM x
            WHERE unit_confidence IS NOT NULL AND NOT price_suspect GROUP BY ALL
          )
          QUALIFY row_number() OVER (
            PARTITION BY gkey
            ORDER BY coalesce(per_unit = ?, false) DESC, (unit_confidence = 'high') DESC, n DESC, per_unit) = 1
        )
        SELECT
          x.gkey AS _gkey,
          CASE WHEN x.gkey LIKE '{staple.key if staple and staple.group_by else "-"}:%' THEN x.gkey
               WHEN bool_or(x.ean_global) THEN any_value(x.ean_norm) FILTER (WHERE x.ean_global)
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
          pick.per_unit,
          pick.conf AS unit_confidence,
          -- izvor gramature za odabrani raspon: name / unit / ean, ili unit_price kad je confidence low
          mode(x.pack_source) FILTER (WHERE {best}) AS pack_source,
          string_agg(DISTINCT x.chain, ', ' ORDER BY x.chain) FILTER (WHERE x.data_quality = 'suspect') AS suspect_chains,
          count(*) FILTER (WHERE x.price_suspect) AS n_price_suspect,
          min(x.price_per_kg_drained) AS price_per_kg_drained_min,
          max(x.price_per_kg_drained) AS price_per_kg_drained_max,
          bool_or(x.variable_weight) AS any_variable_weight,
          bool_or(x.is_special) AS any_special,
          bool_or(x.scope = 'national') AS has_national,
          mode(x.food_group) AS food_group,
          -- pripadnost namirnici (clean.staple_groups): strong / weak (rangira se ispod snažnih)
          any_value(x.match_quality) AS match_quality,
          bool_and(x.is_food IS NULL) AS food_unverified,
          max(x.date) AS date,
          bool_or(starts_with(x.name_norm, ?)) AS _starts,
          CASE WHEN any_value({cov_col}) >= 0.5 THEN 0 WHEN any_value({cov_col}) >= 0.25 THEN 1 ELSE 2 END AS _tier
        FROM x LEFT JOIN pick USING (gkey) JOIN cov USING (gkey)
        GROUP BY x.gkey, pick.per_unit, pick.conf
        ORDER BY coalesce(any_value(x.match_quality) = 'weak', false), _tier, _starts DESC, n_chains DESC, n_stores DESC, price_per_unit_min NULLS LAST, name
        LIMIT ?
    """
    params = cand_params + [staple.compare_unit if staple else None, tokens[0] if tokens else "", limit]
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
        row["ingredient"] = staple.key if staple else None
        if staple:
            row["compare_by"] = staple.compare_by
            row["pantry"] = staple.pantry
        out.append(_with_date(row))
    if staple and out:
        _attach_attributes(con, staple, out)
    for row in out:
        row.pop("_gkey")
    return out


def _gkey_sql(staple) -> tuple[str, str]:
    """SQL za ključ grupe (alias p) i potreban JOIN.

    Zadano: globalni EAN, inače lanac + normalizirani naziv. Namirnica s group_by (jaja) grupira
    po vrijednostima atributa ("jaja:m:podni"), jer se uspoređuje klasa, a ne pojedini EAN. Bez
    vrijednosti prvog atributa (veličine) proizvod ostaje u svojoj EAN grupi.
    """
    base = "CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END"
    if not (staple and staple.group_by):
        return base, ""
    joins, parts = [], []
    for i, attr in enumerate(staple.group_by):
        joins.append(f"""LEFT JOIN clean.product_attrs gb{i} ON gb{i}.chain = p.chain AND gb{i}.product_id = p.product_id
               AND gb{i}.staple = '{staple.key}' AND gb{i}.attr = '{attr}'""")
        parts.append(f"coalesce(gb{i}.value, 'nepoznato')")
    key = " || ':' || ".join(parts)
    return f"CASE WHEN gb0.value IS NOT NULL THEN '{staple.key}:' || {key} ELSE {base} END", "\n".join(joins)


def _attach_attributes(con: duckdb.DuckDBPyConnection, staple, rows: list[dict]) -> None:
    """Atributi grupe: vrijednost iz naziva ispred zaključene i zadane, zatim najčešća u grupi.

    attribute_sources daje za svaki atribut {"name": naziv proizvoda, "how": "name" | "inferred" | "heuristic" |
    "default"}: "name" ako barem jedan proizvod u grupi vrijednost izričito ima u nazivu, inače
    "inferred" (zaključeno, npr. LAGANO JUTRO -> bez laktoze) ili "default" (npr. oblik=nepoznato).
    """
    keys = [r["_gkey"] for r in rows]
    placeholders = ", ".join("?" for _ in keys)
    gkey_expr, gkey_join = _gkey_sql(staple)
    found = con.execute(
        f"""
        SELECT gkey, attr, value, name, how FROM (
          SELECT {gkey_expr} AS gkey, pa.attr, pa.value, p.name, pa.how
          FROM clean.products p {gkey_join}
          JOIN clean.product_attrs pa ON pa.chain = p.chain AND pa.product_id = p.product_id
          WHERE pa.staple = ?
        ) WHERE gkey IN ({placeholders})
        """,
        [staple.key, *keys],
    ).fetchall()
    counts: dict[tuple, dict[str, int]] = {}
    sources: dict[tuple, dict] = {}
    rank = {"name": 0, "inferred": 1, "heuristic": 2, "default": 3}
    for gkey, attr, value, name, how in found:
        counts.setdefault((gkey, attr), {}).setdefault(value, 0)
        counts[(gkey, attr)][value] += 1
        cur = sources.get((gkey, attr, value))
        if cur is None or rank[how] < rank[cur["how"]]:
            sources[(gkey, attr, value)] = {"name": name, "how": how}
    for r in rows:
        r["attributes"], r["attribute_sources"] = {}, {}
        for (gkey, attr), by_value in counts.items():
            if gkey == r["_gkey"]:
                # kao clean.staple_group_attrs: vrijednost iz naziva ispred zadane, zatim broj proizvoda
                value = min(sorted(by_value), key=lambda v: (rank[sources[(gkey, attr, v)]["how"]], -by_value[v]))
                r["attributes"][attr] = value
                r["attribute_sources"][attr] = sources[(gkey, attr, value)]


def get_prices(
    identifier: str, city: str | None = None, limit: int = 50, con: duckdb.DuckDBPyConnection | None = None,
    include_nonfood: bool = False, include_alcohol: bool = False, include_unverified: bool = False,
    include_wholesale: bool = False,
) -> list[dict]:
    """Cijene po trgovini za EAN, `lanac:product_id` ili id klase (npr. "jaja:m"), od najjeftinije.

    Filtar hrane kao u find_products: zadano samo is_food = true i bez alkohola; retci nepoznate
    skupine (include_unverified=True) nose `food_unverified = true`."""
    ident = identifier.strip()
    staples = load_staples()
    prefix = ident.split(":", 1)[0].strip()
    if ":" in ident and prefix in staples and staples[prefix].group_by:
        # id klase iz find_products ("jaja:m:podni", ili samo "jaja:m" za sve uzgoje): proizvodi
        # namirnice sa zadanim vrijednostima atributa iz group_by, redom
        st = staples[prefix]
        values = [v.strip() for v in ident.split(":")[1:]]
        if len(values) > len(st.group_by) or any(v not in st.attributes[a] for a, v in zip(st.group_by, values)):
            options = "; ".join(f"{a}: {', '.join(st.attributes[a])}" for a in st.group_by)
            raise ValueError(f"'{identifier}': nepoznata klasa; moguće ({':'.join(st.group_by)}): {options}")
        prod_sql = " AND ".join(f"""EXISTS (SELECT 1 FROM clean.product_attrs pa JOIN clean.product_staples ps USING (chain, product_id, staple)
                              WHERE pa.chain = p.chain AND pa.product_id = p.product_id AND pa.staple = ?
                                AND pa.attr = ? AND pa.value = ? AND NOT ps.excluded AND ps.drop_reason IS NULL)"""
                                for _ in values)
        prod_params = [x for a, v in zip(st.group_by, values) for x in (st.key, a, v)]
    elif ":" in ident:
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
               ch.data_quality, c.price_per_kg_drained, p.drained_amount, p.variable_weight, p.clearance, c.date,
               p.food_group, p.is_food IS NULL AS food_unverified
        FROM clean.products p
        JOIN clean.prices c USING (chain, product_id)
        JOIN clean.stores s USING (chain, store_id)
        JOIN clean.chains ch USING (chain)
        WHERE {prod_sql} AND {city_sql}
          AND {_food_filter(include_nonfood, include_alcohol, "yes" if include_unverified else "no")}
          AND {"TRUE" if include_wholesale else "s.store_type <> 'cash_and_carry'"}
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
