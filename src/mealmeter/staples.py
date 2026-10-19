"""Rječnik osnovnih namirnica (staples.yaml): učitavanje, podudaranje s proizvodima i atributi."""

import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import duckdb
import yaml

from mealmeter.normalize import norm_text

STAPLES_PATH = Path(__file__).with_name("staples.yaml")
# loose_produce: nazivi staklenki/konzervi koji prolaze pravilo ">= 500 g" ("KRASTAVCI 6-9 cm 1580g ...
# ocijeđene mase", "KISELI ..."): kalibar u cm, ocijeđena masa, kiselo. Uzorak je na name_norm.
LOOSE_REJECT_REGEX = r"\d+ \d+ cm|(^| )ocj|(^| )ocij|(^| )kis"
# Skupine kategorija (normalize.category_group) čiji se proizvodi nikad ne vežu za namirnicu
NONFOOD_GROUPS = ("kozmetika", "higijena", "kucanstvo", "djeca", "sunce", "igracke", "ljubimci")
UNITS = ("kg", "l", "kom")


@dataclass(frozen=True)
class Staple:
    key: str
    name: str
    synonyms: tuple[str, ...]
    must_match: tuple[str, ...]
    must_not_match: tuple[str, ...]
    unit: str
    attributes: dict[str, dict[str, str]] = field(default_factory=dict, hash=False, compare=False)
    loose_produce: bool = False
    plausible_per_unit: tuple[float, float] | None = None
    min_pack: float | None = None
    max_pack: float | None = None
    default_exclude_variants: tuple[tuple[str, str], ...] = ()
    compare_by: str = "unit"
    sachet_g: float | None = None
    sachet_g_by: dict[str, dict[str, float]] = field(default_factory=dict, hash=False, compare=False)
    pantry: bool = False
    count_regex: str | None = None
    group_by: str | None = None
    require_any: tuple[str, ...] = ()
    attribute_defaults: dict[str, str] = field(default_factory=dict, hash=False, compare=False)
    disabled: bool = False
    default_attributes: dict[str, str] = field(default_factory=dict, hash=False, compare=False)
    # pakirani proizvod bez gramature u nazivu (npr. luk "RUKAVAC 4/1"): pretpostavljena masa
    assumed_pack_regex: str | None = None
    assumed_pack_g: float | None = None
    # atribut zaključen iz naziva linije, a ne izričito ("LAGANO JUTRO" -> laktoza=bez)
    inferred_attributes: dict[str, dict[str, str]] = field(default_factory=dict, hash=False, compare=False)
    # komad -> grami (za recepte u komadima: "2 luka")
    piece_g: float | None = None
    # oblik namirnice preko drugih namirnica: {"konzerva": "rajcica_konzerva", ...}
    form_staples: dict[str, str] = field(default_factory=dict, hash=False, compare=False)

    @property
    def require_regex(self) -> str | None:
        """Dodatni uvjet: barem jedan od ovih uzoraka na početku riječi (npr. dio mesa)."""
        return _word_start(self.require_any) if self.require_any else None

    @property
    def compare_unit(self) -> str:
        """Jedinica u kojoj se uspoređuje cijena: kg/l/kom, "vrecica" (pack) ili "kom" (count)."""
        return {"pack": "vrecica", "count": "kom"}.get(self.compare_by, self.unit)

    def units_in_pack(
        self, name: str, pack_amount: float | None, pack_unit: str | None, attrs: dict[str, str]
    ) -> float | None:
        """Broj jedinica usporedbe u pakiranju kad to nije kg/l: vrećice od sachet_g grama
        (compare_by: pack) ili komadi iz naziva po count_regex, npr. "10/1", "10 KOM" (count)."""
        if self.compare_by == "count":
            if self.count_regex and (m := re.search(self.count_regex, attr_text(name))):
                return float(next(g for g in m.groups() if g))
            return pack_amount if pack_unit == "kom" else None
        if self.compare_by != "pack" or not pack_amount or pack_unit != "g":
            return None
        size = self.sachet_g
        for attr, by_value in self.sachet_g_by.items():
            size = by_value.get(attrs.get(attr), size)
        return round(pack_amount / size, 3) if size else None

    @property
    def match_regex(self) -> str:
        """RE2 regex za name_norm: barem jedan uzorak na početku riječi."""
        return _word_start(self.must_match)

    @property
    def early_regex(self) -> str:
        """Uzorak među prve tri riječi naziva: "pravi" proizvod, a ne sastojak ("KEKS ... MRKVA")."""
        return "^(?:[^ ]+ ){0,2}(?:" + "|".join(self.must_match) + ")"

    @property
    def loose_regex(self) -> str:
        """Za loose_produce: uzorak kao prva ili druga riječ ("MRKVA 1kg", "LUK CRVENI", "Rajska rajčica")."""
        return "^(?:[^ ]+ )?(?:" + "|".join(self.must_match) + ")"

    @property
    def exclude_regex(self) -> str | None:
        return _word_start(self.must_not_match) if self.must_not_match else None


def _fold(s: str) -> str:
    """Isto kao norm_text, ali bez diranja interpunkcije (za regex uzorke i attr tekst)."""
    s = s.lower().replace("đ", "d").replace("dj", "d")
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def _word_start(patterns) -> str:
    return "(^| )(?:" + "|".join(patterns) + ")"


def attr_text(name: str) -> str:
    """Tekst za atribute: mala slova, bez dijakritika, zarez -> točka ("2,8%MM" -> "2.8%mm")."""
    return _fold(name).replace(",", ".")


@lru_cache(maxsize=4)
def load_staples(path: Path = STAPLES_PATH, include_disabled: bool = False) -> dict[str, Staple]:
    """Namirnice iz staples.yaml; one s `disabled: true` samo uz include_disabled=True."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    defaults = raw.pop("_defaults", {}) or {}
    default_not = [_fold(p) for p in defaults.get("must_not_match", [])]
    out = {}
    for key, d in raw.items():
        if not re.fullmatch(r"[a-z_]+", key):
            raise ValueError(f"{key}: ključ smije sadržavati samo mala slova i _")
        unit = d.get("unit")
        if unit not in UNITS:
            raise ValueError(f"{key}: unit mora biti jedan od {UNITS}, a ne {unit!r}")
        if not d.get("must_match"):
            raise ValueError(f"{key}: must_match je obavezan")
        must_not = [_fold(p) for p in d.get("must_not_match") or []]
        if not d.get("no_defaults"):
            must_not += [p for p in default_not if p not in must_not]
        raw_attrs = d.get("attributes") or {}
        # "_default" je vrijednost atributa kad nijedan uzorak ne pogodi (npr. oblik=nepoznato)
        defaults = {a: str(v.pop("_default")) for a, v in raw_attrs.items() if "_default" in v}
        attrs = {a: {str(v): _fold(rx) for v, rx in values.items()} for a, values in raw_attrs.items()}
        for a, v in defaults.items():
            attrs[a].setdefault(v, r"(?!)")  # vrijednost bez uzorka (samo kao zadana), npr. "nepoznato"
        inferred = {a: {str(v): _fold(rx) for v, rx in values.items()}
                    for a, values in (d.get("inferred_attributes") or {}).items()}
        for a, values in inferred.items():
            for v in values:
                if v not in attrs.get(a, {}):
                    raise ValueError(f"{key}: inferred_attributes {a}={v} nije definiran atribut")
        st = Staple(
            key=key,
            name=d.get("name", key),
            synonyms=tuple(dict.fromkeys([norm_text(key.replace("_", " "))] + [norm_text(s) for s in d.get("synonyms", [])])),
            must_match=tuple(_fold(p) for p in d["must_match"]),
            must_not_match=tuple(must_not),
            unit=unit,
            attributes=attrs,
            loose_produce=bool(d.get("loose_produce", False)),
            plausible_per_unit=tuple(d["plausible_per_unit"]) if d.get("plausible_per_unit") else None,
            min_pack=d.get("min_pack"),
            max_pack=d.get("max_pack"),
            default_exclude_variants=tuple(tuple(v.split("=", 1)) for v in d.get("default_exclude_variants", [])),
            compare_by=d.get("compare_by", "unit"),
            sachet_g=d.get("sachet_g"),
            sachet_g_by=d.get("sachet_g_by") or {},
            pantry=bool(d.get("pantry", False)),
            count_regex=d.get("count_regex"),
            group_by=d.get("group_by"),
            require_any=tuple(_fold(p) for p in d.get("require_any", [])),
            attribute_defaults=defaults,
            disabled=bool(d.get("disabled", False)),
            default_attributes={a: str(v) for a, v in (d.get("default_attributes") or {}).items()},
            assumed_pack_regex=_word_start([_fold(d["packaged"]["pattern"])]) if d.get("packaged") else None,
            assumed_pack_g=d["packaged"]["default_g"] if d.get("packaged") else None,
            inferred_attributes=inferred,
            piece_g=d.get("piece_g"),
            form_staples=d.get("form_staples") or {},
        )
        for a, v in st.default_attributes.items():
            if v not in attrs.get(a, {}):
                raise ValueError(f"{key}: default_attributes {a}={v} nije definiran atribut")
        if st.disabled and not include_disabled:
            continue
        if st.group_by and st.group_by not in attrs:
            raise ValueError(f"{key}: group_by {st.group_by} nije definiran atribut")
        if st.compare_by == "count" and not st.count_regex:
            raise ValueError(f"{key}: compare_by: count traži count_regex")
        for attr, value in st.default_exclude_variants:
            if value not in attrs.get(attr, {}):
                raise ValueError(f"{key}: default_exclude_variants {attr}={value} nije definiran atribut")
        if st.compare_by not in ("unit", "pack", "count") or (st.compare_by == "pack" and not st.sachet_g):
            raise ValueError(f"{key}: compare_by mora biti unit, pack (uz sachet_g) ili count")
        # Svi regexi se moraju dati kompilirati (Python re je nadskup RE2 za ove uzorke)
        re.compile(st.match_regex)
        if st.exclude_regex:
            re.compile(st.exclude_regex)
        for values in attrs.values():
            for rx in values.values():
                re.compile(rx)
        out[key] = st
    return out


def resolve_ingredient(text: str | None, staples: dict[str, Staple] | None = None) -> Staple | None:
    """Namirnica čiji su ključ ili sinonim jednaki upitu (bez dijakritika i velikih slova)."""
    if not text:
        return None
    staples = staples or load_staples()
    q = norm_text(text)
    if q.replace(" ", "_") in staples:
        return staples[q.replace(" ", "_")]
    for st in staples.values():
        if q in st.synonyms:
            return st
    return None


def name_match(staple: Staple, name: str) -> str | None:
    """Kako pravila namirnice vide jedan naziv: "match", "excluded" ili None (nije kandidat).

    Provjerava samo must_match/must_not_match (bez loose_produce i kategorije), za testove i
    pregled; build to radi u SQL-u istim uzorcima.
    """
    text = norm_text(name) or ""
    if not re.search(staple.match_regex, text):
        return None
    if staple.require_regex and not re.search(staple.require_regex, text):
        return None
    if staple.exclude_regex and re.search(staple.exclude_regex, text):
        return "excluded"
    return "match"


def extract_attributes_detail(staple: Staple, name: str) -> dict[str, tuple[str, str]]:
    """Atributi iz naziva s porijeklom: {atribut: (vrijednost, "name" | "inferred" | "default")}.

    "name": vrijednost izričito piše u nazivu (prva vrijednost čiji regex pogodi);
    "inferred": zaključena iz naziva linije (inferred_attributes, npr. LAGANO JUTRO -> bez laktoze);
    "default": nijedan uzorak nije pogodio, pa vrijedi attributes._default (npr. oblik=nepoznato).
    """
    text = attr_text(name)
    out = {}
    for attr, values in staple.attributes.items():
        for value, rx in values.items():
            if re.search(rx, text):
                out[attr] = (value, "name")
                break
        else:
            for value, rx in staple.inferred_attributes.get(attr, {}).items():
                if re.search(rx, text):
                    out[attr] = (value, "inferred")
                    break
            else:
                if attr in staple.attribute_defaults:
                    out[attr] = (staple.attribute_defaults[attr], "default")
    return out


def extract_attributes(staple: Staple, name: str) -> dict[str, str]:
    """Atributi iz naziva (vidi extract_attributes_detail)."""
    return {a: v for a, (v, _) in extract_attributes_detail(staple, name).items()}


def build_staples(con: duckdb.DuckDBPyConnection, staples: dict[str, Staple] | None = None) -> dict:
    """clean.product_staples (proizvod <-> namirnica, s oznakom isključenja) i clean.product_attrs."""
    from mealmeter.build import _temp_table  # izbjegava kružni import

    staples = staples or load_staples()
    # excluded: pogađa must_not_match -> cijela grupa (EAN) ispada iz namirnice.
    # drop_reason: samo ovaj proizvod ispada (npr. neprehrambena kategorija lanca), grupa ostaje.
    con.execute("""
        CREATE OR REPLACE TABLE clean.product_staples (
          chain VARCHAR, product_id VARCHAR, staple VARCHAR, excluded BOOLEAN, drop_reason VARCHAR)
    """)
    nonfood = ", ".join(f"'{g}'" for g in NONFOOD_GROUPS)
    for st in staples.values():
        excl = "regexp_matches(name_norm, ?)" if st.exclude_regex else "false"
        params = ([st.exclude_regex] if st.exclude_regex else []) + [st.match_regex]
        loose = ""
        if st.require_regex:
            loose += " AND regexp_matches(name_norm, ?)"
            params.append(st.require_regex)
        if st.loose_produce:
            # Svježe voće/povrće: riječ namirnice kao prva ili druga riječ naziva, i proizvod
            # na vagu (bez globalnog EAN-a), bez poznate gramature ili pakiranje >= 500 g;
            # nikad tekućina. Inače "banana" pogađa bombone, sokove i čokolade s okusom banane.
            # Staklenke ("KRASTAVCI 6-9 cm 1580g ... ocijeđene mase") odbija LOOSE_REJECT_REGEX.
            loose += """ AND regexp_matches(name_norm, ?)
                       AND (NOT ean_global OR pack_unit IS NULL OR (pack_unit = 'g' AND pack_amount >= 500))
                       AND pack_unit IS DISTINCT FROM 'ml' AND NOT regexp_matches(name_norm, ?)"""
            params += [st.loose_regex, LOOSE_REJECT_REGEX]
        con.execute(
            f"""INSERT INTO clean.product_staples
                SELECT chain, product_id, '{st.key}', {excl},
                       CASE WHEN category_group IN ({nonfood}) THEN 'kategorija:' || category_group END
                FROM clean.products WHERE regexp_matches(name_norm, ?) {loose}""",
            params,
        )

    # pravila namirnica kao tablica (za SQL i pregled)
    con.execute("""
        CREATE OR REPLACE TABLE clean.staple_rules (
          staple VARCHAR PRIMARY KEY, name VARCHAR, unit VARCHAR, compare_by VARCHAR, compare_unit VARCHAR,
          ppu_min DOUBLE, ppu_max DOUBLE, range_source VARCHAR, min_pack DOUBLE, max_pack DOUBLE,
          pantry BOOLEAN, loose_produce BOOLEAN)
    """)
    con.executemany("INSERT INTO clean.staple_rules VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        (st.key, st.name, st.unit, st.compare_by, st.compare_unit,
         *(st.plausible_per_unit or (None, None)), "manual" if st.plausible_per_unit else None,
         st.min_pack, st.max_pack, st.pantry, st.loose_produce)
        for st in staples.values()
    ])
    # pakiranje izvan [min_pack, max_pack]: porcije i ugostiteljska pakiranja ispadaju iz namirnice
    con.execute("""
        UPDATE clean.product_staples ps SET drop_reason = 'pakiranje'
        FROM clean.products p, clean.staple_rules r
        WHERE p.chain = ps.chain AND p.product_id = ps.product_id AND r.staple = ps.staple
          AND ps.drop_reason IS NULL AND NOT ps.excluded AND p.pack_amount IS NOT NULL
          AND r.compare_by <> 'count'
          AND (p.pack_amount < r.min_pack OR p.pack_amount > r.max_pack)
    """)

    rows = con.execute("""
        SELECT s.chain, s.product_id, s.staple, p.name, p.pack_amount, p.pack_unit
        FROM clean.product_staples s JOIN clean.products p USING (chain, product_id)
        WHERE NOT s.excluded AND s.drop_reason IS NULL
    """).fetchall()
    attr_rows, unit_rows = [], []
    for chain, pid, key, name, amount, pack_unit in rows:
        st = staples[key]
        detail = extract_attributes_detail(st, name)
        attrs = {a: v for a, (v, _) in detail.items()}
        attr_rows += [(chain, pid, key, a, v, how) for a, (v, how) in detail.items()]
        n = st.units_in_pack(name, amount, pack_unit, attrs)
        assumed = None
        if st.assumed_pack_regex and amount is None and re.search(st.assumed_pack_regex, norm_text(name) or ""):
            assumed = st.assumed_pack_g
        if n is not None or assumed is not None:
            unit_rows.append((chain, pid, key, n, assumed))

    _temp_table(con, "attrs_tmp", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "staple": "VARCHAR", "attr": "VARCHAR", "value": "VARCHAR",
        "how": "VARCHAR",
    }, attr_rows)
    con.execute("CREATE OR REPLACE TABLE clean.product_attrs AS SELECT * FROM attrs_tmp")
    # n_units: broj jedinica usporedbe u pakiranju kad to nije kg/l (vrećice, jaja);
    # assumed_g: pretpostavljena masa pakiranja bez gramature u nazivu (luk rukavac 500 g)
    con.execute("ALTER TABLE clean.product_staples ADD COLUMN n_units DOUBLE")
    con.execute("ALTER TABLE clean.product_staples ADD COLUMN assumed_g DOUBLE")
    _temp_table(con, "units_tmp", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "staple": "VARCHAR", "n_units": "DOUBLE", "assumed_g": "DOUBLE",
    }, unit_rows)
    con.execute("""
        UPDATE clean.product_staples ps SET n_units = u.n_units, assumed_g = u.assumed_g FROM units_tmp u
        WHERE u.chain = ps.chain AND u.product_id = ps.product_id AND u.staple = ps.staple
    """)
    # compare_by: count (jaja): raspon pakiranja vrijedi za broj komada
    counted = [st.key for st in staples.values() if st.compare_by == "count"]
    if counted:
        con.execute(f"""
            UPDATE clean.product_staples ps SET drop_reason = 'pakiranje'
            FROM clean.staple_rules r
            WHERE r.staple = ps.staple AND ps.staple IN ({", ".join(f"'{k}'" for k in counted)})
              AND ps.drop_reason IS NULL AND NOT ps.excluded AND ps.n_units IS NOT NULL
              AND (ps.n_units < r.min_pack OR ps.n_units > r.max_pack)
        """)
    return {
        "staples": len(staples),
        "matched": con.execute(
            "SELECT count(*) FROM clean.product_staples WHERE NOT excluded AND drop_reason IS NULL").fetchone()[0],
        "excluded": con.execute("SELECT count(*) FROM clean.product_staples WHERE excluded").fetchone()[0],
        "dropped": con.execute("SELECT count(*) FROM clean.product_staples WHERE drop_reason IS NOT NULL").fetchone()[0],
        "attrs": con.execute("SELECT count(*) FROM clean.product_attrs").fetchone()[0],
        "auto_ranges": set_auto_ranges(con),
        "suspect_prices": staple_price_suspects(con),
    }


# Cijena po jedinici usporedbe namirnice (aliasi: c = clean.prices, ps = clean.product_staples,
# r = clean.staple_rules). Isti izraz koriste build (granice, statistika) i pretraga.
STAPLE_PPU_SQL = """CASE
    WHEN r.compare_by IN ('pack', 'count') THEN round(c.price_eff / nullif(ps.n_units, 0), 2)
    WHEN ps.assumed_g > 0 THEN round(c.price_eff / ps.assumed_g * 1000, 2)
    WHEN c.per_unit = r.unit THEN c.price_per_unit END"""
AUTO_RANGE = (0.25, 4.0)  # automatske granice: 0.25x do 4x medijana namirnice


def set_auto_ranges(con: duckdb.DuckDBPyConnection) -> int:
    """Namirnice bez ručnog plausible_per_unit dobivaju granice 0.25x-4x medijana cijene po jedinici
    (preko svih cijena povezanih proizvoda). Vraća broj namirnica s automatskim granicama."""
    lo, hi = AUTO_RANGE
    con.execute(f"""
        UPDATE clean.staple_rules r SET ppu_min = round(m.med * {lo}, 4), ppu_max = round(m.med * {hi}, 4),
                                        range_source = 'auto'
        FROM (
          SELECT ps.staple, median({STAPLE_PPU_SQL}) AS med
          FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
          JOIN clean.prices c USING (chain, product_id)
          WHERE NOT ps.excluded AND ps.drop_reason IS NULL AND r.ppu_min IS NULL
          GROUP BY ps.staple
        ) m
        WHERE r.staple = m.staple AND m.med IS NOT NULL
    """)
    return con.execute("SELECT count(*) FROM clean.staple_rules WHERE range_source = 'auto'").fetchone()[0]


def staple_price_suspects(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Po namirnici: (namirnica, izvor granica, broj cijena izvan granica, broj usporedivih cijena)."""
    return con.execute(f"""
        SELECT staple, any_value(range_source),
               count(*) FILTER (WHERE ppu NOT BETWEEN ppu_min AND ppu_max), count(*)
        FROM (
          SELECT ps.staple, r.range_source, r.ppu_min, r.ppu_max, {STAPLE_PPU_SQL} AS ppu
          FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
          JOIN clean.prices c USING (chain, product_id)
          WHERE NOT ps.excluded AND ps.drop_reason IS NULL AND r.ppu_min IS NOT NULL
        ) WHERE ppu IS NOT NULL
        GROUP BY staple ORDER BY staple
    """).fetchall()
