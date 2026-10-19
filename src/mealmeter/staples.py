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
        )
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
    con.execute("""
        CREATE OR REPLACE TABLE clean.product_staples (
          chain VARCHAR, product_id VARCHAR, staple VARCHAR, excluded BOOLEAN)
    """)
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
                SELECT chain, product_id, '{st.key}', {excl}
                FROM clean.products WHERE regexp_matches(name_norm, ?) {loose}""",
            params,
        )

    rows = con.execute("""
        SELECT s.chain, s.product_id, s.staple, p.name
        FROM clean.product_staples s JOIN clean.products p USING (chain, product_id)
        WHERE NOT s.excluded
    """).fetchall()

    def attr_rows():
        for chain, pid, key, name in rows:
            for attr, value in extract_attributes(staples[key], name).items():
                yield chain, pid, key, attr, value

    _temp_table(con, "attrs_tmp", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "staple": "VARCHAR", "attr": "VARCHAR", "value": "VARCHAR",
    }, attr_rows())
    con.execute("CREATE OR REPLACE TABLE clean.product_attrs AS SELECT * FROM attrs_tmp")
    return {
        "staples": len(staples),
        "matched": con.execute("SELECT count(*) FROM clean.product_staples WHERE NOT excluded").fetchone()[0],
        "excluded": con.execute("SELECT count(*) FROM clean.product_staples WHERE excluded").fetchone()[0],
        "attrs": con.execute("SELECT count(*) FROM clean.product_attrs").fetchone()[0],
    }
