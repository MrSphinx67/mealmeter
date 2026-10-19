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
def load_staples(path: Path = STAPLES_PATH) -> dict[str, Staple]:
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
        attrs = {
            a: {str(v): _fold(rx) for v, rx in values.items()} for a, values in (d.get("attributes") or {}).items()
        }
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
        )
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
    if staple.exclude_regex and re.search(staple.exclude_regex, text):
        return "excluded"
    return "match"


def extract_attributes(staple: Staple, name: str) -> dict[str, str]:
    """Atributi iz naziva; za svaki atribut pobjeđuje prva vrijednost čiji regex pogodi."""
    text = attr_text(name)
    out = {}
    for attr, values in staple.attributes.items():
        for value, rx in values.items():
            if re.search(rx, text):
                out[attr] = value
                break
    return out


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
        if st.loose_produce:
            # Svježe voće/povrće: riječ namirnice kao prva ili druga riječ naziva, i proizvod
            # na vagu (bez globalnog EAN-a), bez poznate gramature ili pakiranje >= 500 g;
            # nikad tekućina. Inače "banana" pogađa bombone, sokove i čokolade s okusom banane.
            loose = """AND regexp_matches(name_norm, ?)
                       AND (NOT ean_global OR pack_unit IS NULL OR (pack_unit = 'g' AND pack_amount >= 500))
                       AND pack_unit IS DISTINCT FROM 'ml'"""
            params.append(st.loose_regex)
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
          ppu_min DOUBLE, ppu_max DOUBLE, min_pack DOUBLE, max_pack DOUBLE,
          pantry BOOLEAN, loose_produce BOOLEAN)
    """)
    con.executemany("INSERT INTO clean.staple_rules VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        (st.key, st.name, st.unit, st.compare_by, st.compare_unit,
         *(st.plausible_per_unit or (None, None)), st.min_pack, st.max_pack, st.pantry, st.loose_produce)
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
        attrs = extract_attributes(staples[key], name)
        attr_rows += [(chain, pid, key, a, v) for a, v in attrs.items()]
        if (n := staples[key].units_in_pack(name, amount, pack_unit, attrs)) is not None:
            unit_rows.append((chain, pid, key, n))

    _temp_table(con, "attrs_tmp", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "staple": "VARCHAR", "attr": "VARCHAR", "value": "VARCHAR",
    }, attr_rows)
    con.execute("CREATE OR REPLACE TABLE clean.product_attrs AS SELECT * FROM attrs_tmp")
    # n_units: broj jedinica usporedbe u pakiranju kad to nije kg/l (vrećice; kasnije i jaja)
    con.execute("ALTER TABLE clean.product_staples ADD COLUMN n_units DOUBLE")
    _temp_table(con, "units_tmp", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "staple": "VARCHAR", "n_units": "DOUBLE",
    }, unit_rows)
    con.execute("""
        UPDATE clean.product_staples ps SET n_units = u.n_units FROM units_tmp u
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
        "suspect_prices": staple_price_suspects(con),
    }


def staple_price_suspects(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Po namirnici: broj cijena (trgovina x proizvod) izvan plausible_per_unit i ukupno usporedivih."""
    return con.execute("""
        SELECT ps.staple, count(*) FILTER (WHERE c.price_per_unit NOT BETWEEN r.ppu_min AND r.ppu_max) AS suspect,
               count(*) AS total
        FROM clean.product_staples ps
        JOIN clean.staple_rules r USING (staple)
        JOIN clean.prices c USING (chain, product_id)
        WHERE NOT ps.excluded AND ps.drop_reason IS NULL AND r.ppu_min IS NOT NULL AND c.per_unit = r.unit
        GROUP BY ps.staple ORDER BY ps.staple
    """).fetchall()
