"""Rječnik osnovnih namirnica (staples.yaml): učitavanje, podudaranje s proizvodima i atributi."""

import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import duckdb
import yaml

from mealmeter.normalize import norm_text
from mealmeter.units import piece_weight

STAPLES_PATH = Path(__file__).with_name("staples.yaml")
# loose_produce: nazivi staklenki/konzervi koji prolaze pravilo ">= 500 g" ("KRASTAVCI 6-9 cm 1580g ...
# ocijeđene mase", "KISELI ..."): kalibar u cm, ocijeđena masa, kiselo. Uzorak je na name_norm.
LOOSE_REJECT_REGEX = r"\d+ \d+ cm|(^| )ocj|(^| )ocij|(^| )kis"
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
    # realna cijena jedne vrećice (compare_by: pack); zamjenjuje automatske granice, vidi STAPLE_SUSPECT_SQL
    plausible_per_pack: tuple[float, float] | None = None
    # granice po vrijednosti atributa: {"stanje": {"svjeze": (3, 20), "smrznuto": (2, 12)}}; "_other"
    # vrijedi za ostale vrijednosti (jaja: bio i ostali uzgoji)
    plausible_by: dict[str, dict[str, tuple[float, float]]] = field(default_factory=dict, hash=False, compare=False)
    min_pack: float | None = None
    max_pack: float | None = None
    default_exclude_variants: tuple[tuple[str, str], ...] = ()
    compare_by: str = "unit"
    sachet_g: float | None = None
    sachet_g_by: dict[str, dict[str, float]] = field(default_factory=dict, hash=False, compare=False)
    pantry: bool = False
    count_regex: str | None = None
    # atributi po kojima se grupira umjesto EAN-a (jaja: velicina, uzgoj -> "jaja:m:podni")
    group_by: tuple[str, ...] = ()
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
    ambiguous_form: bool = False
    # proizvod bez gramature koji se ne prodaje na vagu dobiva procijenjenu težinu komada iz
    # data/units.yaml (vezica peršina 50 g), uz unit_confidence=low i pack_source=assumed
    assume_piece: bool = False
    # oblik=suho bez oznake u nazivu: {"pack_g": (400, 1000), "unit": (...), "words": (...)}
    dry_rule: dict = field(default_factory=dict, hash=False, compare=False)
    # uzorci: proizvod ispada samo ako nema gramature (prazna soljenka), drop_reason 'bez_gramature'
    require_pack: tuple[str, ...] = ()
    # zamjenjive vrijednosti atributa: {"mast": ("2.8", "3.2", "3.5", "3.8")}; traženi ili zadani
    # 2.8 prihvaća bilo koju vrijednost iz iste skupine (vidi accepted_values)
    substitutes: dict[str, tuple[str, ...]] = field(default_factory=dict, hash=False, compare=False)
    # zadani redoslijed vrijednosti kad atribut nije tražen (mljeveno meso: miješano, pa juneće, pa
    # svinjsko); ostale vrijednosti (pureće, pileće) samo kad se izričito traže
    default_preference: dict[str, tuple[str, ...]] = field(default_factory=dict, hash=False, compare=False)

    def defaults(self) -> dict:
        """Zadani filtri atributa: vrijednost (default_attributes) ili n-torka redoslijeda (default_preference)."""
        return {**self.default_attributes, **self.default_preference}

    def accepted_values(self, attr: str, value) -> tuple[str, ...]:
        """Vrijednosti atributa koje vrijede kao `value` (s njom na prvom mjestu); n-torka iz
        default_preference vrijedi takva kakva jest."""
        if isinstance(value, tuple):
            return value
        group = self.substitutes.get(attr, ())
        return (value, *[v for v in group if v != value]) if value in group else (value,)

    @property
    def require_regex(self) -> str | None:
        """Dodatni uvjet: barem jedan od ovih uzoraka na početku riječi (npr. dio mesa)."""
        return _word_start(self.require_any) if self.require_any else None

    @property
    def compare_unit(self) -> str:
        """Jedinica u kojoj se uspoređuje cijena: kg/l/kom, "vrecica" (pack) ili "kom" (count)."""
        return {"pack": "vrecica", "count": "kom"}.get(self.compare_by, self.unit)

    def units_in_pack(
        self, name: str, pack_amount: float | None, pack_unit: str | None, attrs: dict[str, str],
        wholesale: bool = False,
    ) -> float | None:
        """Broj jedinica usporedbe u pakiranju kad to nije kg/l: vrećice od sachet_g grama
        (compare_by: pack) ili komadi iz naziva po count_regex, npr. "10/1", "10 KOM" (count).
        Kod veleprodaje (wholesale) "10/1" je broj kutija, pa vrijedi samo "10 KOM" (zadnja grupa regexa)."""
        if self.compare_by == "count":
            for m in re.finditer(self.count_regex or r"(?!)", attr_text(name)):
                groups = m.groups()[-1:] if wholesale else m.groups()
                if any(groups):
                    return float(next(g for g in groups if g))
            return pack_amount if pack_unit == "kom" and not wholesale else None
        if self.compare_by != "pack":
            return None
        # vrećica = proizvod kakav se prodaje: broj vrećica iz naziva ("5+1", "3 PAK", "6x8g"), inače 1;
        # gramatura se ne dijeli veličinom vrećice (rinfuza od 500 g je jedno pakiranje)
        return float(sachet_count(name))

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


# broj vrećica u pakiranju (attr_text): "5+1", "3 PAK", "10kom", "(5VRE.)", "6x8g", "2*25g", "12GX6"
_SACHET_COUNT = [
    (re.compile(r"(?<![\d.])(\d{1,2})\s*\+\s*(\d)(?!\d)"), lambda m: int(m.group(1)) + int(m.group(2))),
    (re.compile(r"(?<![\d.])(\d{1,2})\s*[x×*]\s*\d+(?:\.\d+)?\s*g"), lambda m: int(m.group(1))),
    (re.compile(r"(?<![\d.])\d+(?:\.\d+)?\s*g\s*[x×*]\s*(\d{1,2})(?!\d)"), lambda m: int(m.group(1))),
    (re.compile(r"(?<![\d.])(\d{1,2})\s*-?\s*(?:pak|pack|kom|vre|vr\.)"), lambda m: int(m.group(1))),
]


def sachet_count(name: str) -> int:
    """Broj vrećica u proizvodu iz naziva, inače 1 (compare_by: pack)."""
    text = attr_text(name)
    for rx, count in _SACHET_COUNT:
        if (m := rx.search(text)) and count(m) > 0:
            return count(m)
    return 1


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
            plausible_per_pack=tuple(d["plausible_per_pack"]) if d.get("plausible_per_pack") else None,
            plausible_by={a: {str(v): tuple(r) for v, r in vals.items()}
                          for a, vals in (d.get("plausible_by") or {}).items()},
            min_pack=d.get("min_pack"),
            max_pack=d.get("max_pack"),
            default_exclude_variants=tuple(tuple(v.split("=", 1)) for v in d.get("default_exclude_variants", [])),
            compare_by=d.get("compare_by", "unit"),
            sachet_g=d.get("sachet_g"),
            sachet_g_by=d.get("sachet_g_by") or {},
            pantry=bool(d.get("pantry", False)),
            count_regex=d.get("count_regex"),
            group_by=tuple([d["group_by"]] if isinstance(d.get("group_by"), str) else d.get("group_by") or ()),
            require_any=tuple(_fold(p) for p in d.get("require_any", [])),
            attribute_defaults=defaults,
            disabled=bool(d.get("disabled", False)),
            default_attributes={a: str(v) for a, v in (d.get("default_attributes") or {}).items()},
            assumed_pack_regex=_word_start([_fold(d["packaged"]["pattern"])]) if d.get("packaged") else None,
            assumed_pack_g=d["packaged"]["default_g"] if d.get("packaged") else None,
            inferred_attributes=inferred,
            piece_g=d.get("piece_g"),
            form_staples=d.get("form_staples") or {},
            ambiguous_form=bool(d.get("ambiguous_form", False)),
            require_pack=tuple(_fold(p) for p in d.get("require_pack", [])),
            assume_piece=bool(d.get("assume_piece", False)),
            dry_rule={k: tuple(_fold(str(x)) if k != "pack_g" else float(x) for x in v)
                      for k, v in (d.get("dry_rule") or {}).items()},
            substitutes={a: tuple(str(v) for v in vals) for a, vals in (d.get("substitutes") or {}).items()},
            default_preference={a: tuple(str(v) for v in vals)
                                for a, vals in (d.get("default_preference") or {}).items()},
        )
        for a, vals in st.default_preference.items():
            if any(v not in attrs.get(a, {}) for v in vals) or a in st.default_attributes:
                raise ValueError(f"{key}: default_preference {a}={vals}: nedefinirana vrijednost ili i default_attributes")
        for a, vals in st.substitutes.items():
            if any(v not in attrs.get(a, {}) for v in vals):
                raise ValueError(f"{key}: substitutes {a}={vals} sadrži nedefiniranu vrijednost")
        if st.ambiguous_form and "oblik" not in attrs:
            raise ValueError(f"{key}: ambiguous_form traži atribut oblik")
        if st.dry_rule and not (st.ambiguous_form and "suho" in attrs["oblik"] and len(st.dry_rule.get("pack_g", ())) == 2):
            raise ValueError(f"{key}: dry_rule traži ambiguous_form, oblik=suho i pack_g: [min, max]")
        for a, v in st.default_attributes.items():
            if v not in attrs.get(a, {}):
                raise ValueError(f"{key}: default_attributes {a}={v} nije definiran atribut")
        if st.disabled and not include_disabled:
            continue
        for attr in st.group_by:
            if attr not in attrs:
                raise ValueError(f"{key}: group_by {attr} nije definiran atribut")
        if st.compare_by == "count" and not st.count_regex:
            raise ValueError(f"{key}: compare_by: count traži count_regex")
        for attr, value in st.default_exclude_variants:
            if value not in attrs.get(attr, {}):
                raise ValueError(f"{key}: default_exclude_variants {attr}={value} nije definiran atribut")
        if st.plausible_by and (len(st.plausible_by) != 1 or st.plausible_per_unit or st.plausible_per_pack
                                or any(v != "_other" and v not in attrs.get(a, {})
                                       for a, vals in st.plausible_by.items() for v in vals)):
            raise ValueError(f"{key}: plausible_by: jedan definiran atribut, bez plausible_per_unit/per_pack")
        if st.plausible_per_pack and (st.compare_by != "pack" or st.plausible_per_unit):
            raise ValueError(f"{key}: plausible_per_pack vrijedi samo uz compare_by: pack i bez plausible_per_unit")
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
    for st in out.values():
        for form, key in st.form_staples.items():
            if key not in out:
                raise ValueError(f"{st.key}: form_staples {form} -> {key} ne postoji")
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
    Build uz to može postaviti oblik s how="heuristic" (form_heuristic: stupac unit, dry_rule).

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


def form_heuristic(staple: Staple, name: str, unit: str | None, pack_amount: float | None,
                   pack_unit: str | None, drained_amount: float | None = None) -> str | None:
    """Oblik (konzerva/smrznuto/suho) kad ga naziv ne kaže, za namirnice s ambiguous_form.

    0. Poznata ocijeđena masa ("GRAH CRVENI 400/240 g") znači konzervu (Korak 2D).

    1. Oznaka konzerve ili smrznutog u stupcu `unit` (isti uzorci kao za naziv).
    2. dry_rule: pakiranje u rasponu pack_g (g), bez oznake konzerve/smrznutog u nazivu i unit-u, a
       unit pogađa dry_rule.unit (rinfuza) ili naziv pogađa dry_rule.words (vrećica, PVC, marke).
    """
    if not staple.ambiguous_form:
        return None
    forms = staple.attributes["oblik"]
    if drained_amount and "konzerva" in forms:
        return "konzerva"
    unit_text = attr_text(unit or "")
    for form in ("konzerva", "smrznuto"):
        if form in forms and unit_text and re.search(forms[form], unit_text):
            return form
    rule = staple.dry_rule
    if not rule or pack_unit != "g" or pack_amount is None:
        return None
    lo, hi = rule["pack_g"]
    text = attr_text(name)
    if not lo <= pack_amount <= hi or any(re.search(forms[f], text) for f in ("konzerva", "smrznuto") if f in forms):
        return None
    words = _word_start(rule.get("words", ()))
    if (rule.get("unit") and re.search(_word_start(rule["unit"]), unit_text)) or (rule.get("words") and re.search(words, text)):
        return "suho"
    return None


def extract_attributes(staple: Staple, name: str) -> dict[str, str]:
    """Atributi iz naziva (vidi extract_attributes_detail)."""
    return {a: v for a, (v, _) in extract_attributes_detail(staple, name).items()}


def build_staples(con: duckdb.DuckDBPyConnection, staples: dict[str, Staple] | None = None) -> dict:
    """clean.product_staples (proizvod <-> namirnica, s oznakom isključenja) i clean.product_attrs."""
    from mealmeter.build import WHOLESALE_CHAINS, _temp_table  # izbjegava kružni import

    staples = staples or load_staples()
    # excluded: pogađa must_not_match -> cijela grupa (EAN) ispada iz namirnice.
    # drop_reason: samo ovaj proizvod ispada (neprehrambena skupina ili alkohol, food.py), grupa ostaje.
    # Proizvodi s food_group='unknown' ostaju; pretraga i košarica ih filtriraju (is_food IS NULL).
    con.execute("""
        CREATE OR REPLACE TABLE clean.product_staples (
          chain VARCHAR, product_id VARCHAR, staple VARCHAR, excluded BOOLEAN, drop_reason VARCHAR)
    """)
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
                       CASE WHEN NOT is_food OR food_group = 'alkohol' THEN 'kategorija:' || food_group END
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
         *(st.plausible_per_unit or st.plausible_per_pack or _envelope(st.plausible_by) or (None, None)),
         "manual" if st.plausible_per_unit or st.plausible_by else "pack" if st.plausible_per_pack else None,
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

    # require_pack: npr. soljenka je sol samo kad ima gramaturu
    for st in staples.values():
        if st.require_pack:
            con.execute("""
                UPDATE clean.product_staples ps SET drop_reason = 'bez_gramature'
                FROM clean.products p
                WHERE p.chain = ps.chain AND p.product_id = ps.product_id AND ps.staple = ?
                  AND ps.drop_reason IS NULL AND NOT ps.excluded AND p.pack_amount IS NULL
                  AND regexp_matches(p.name_norm, ?)
            """, [st.key, _word_start(st.require_pack)])

    rows = con.execute("""
        SELECT s.chain, s.product_id, s.staple, p.name, p.pack_amount, p.pack_unit, p.unit, p.unit_hint,
               p.drained_amount
        FROM clean.product_staples s JOIN clean.products p USING (chain, product_id)
        WHERE NOT s.excluded AND s.drop_reason IS NULL
    """).fetchall()
    attr_rows, unit_rows = [], []
    for chain, pid, key, name, amount, pack_unit, unit, hint, drained in rows:
        st = staples[key]
        detail = extract_attributes_detail(st, name)
        if st.ambiguous_form and detail.get("oblik", (None, "default"))[1] == "default":
            if form := form_heuristic(st, name, unit, amount, pack_unit, drained):
                detail["oblik"] = (form, "heuristic")
        attrs = {a: v for a, (v, _) in detail.items()}
        attr_rows += [(chain, pid, key, a, v, how) for a, (v, how) in detail.items()]
        n = st.units_in_pack(name, amount, pack_unit, attrs, wholesale=chain in WHOLESALE_CHAINS)
        assumed = None
        if st.assumed_pack_regex and amount is None and re.search(st.assumed_pack_regex, norm_text(name) or ""):
            assumed = st.assumed_pack_g
        elif st.assume_piece and amount is None and hint != "kg":
            # komad bez težine koji se ne prodaje na vagu (vezica peršina): procjena iz data/units.yaml
            assumed = piece_weight(st.key)
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
    # granice cijene proizvoda po vrijednosti atributa (plausible_by), inače NULL (vrijede granice namirnice)
    con.execute("ALTER TABLE clean.product_staples ADD COLUMN ppu_min DOUBLE")
    con.execute("ALTER TABLE clean.product_staples ADD COLUMN ppu_max DOUBLE")
    for st in staples.values():
        for attr, by_value in st.plausible_by.items():
            other = by_value.get("_other")
            cases_lo = " ".join(f"WHEN '{v}' THEN {lo}" for v, (lo, _) in by_value.items() if v != "_other")
            cases_hi = " ".join(f"WHEN '{v}' THEN {hi}" for v, (_, hi) in by_value.items() if v != "_other")
            con.execute(f"""
                UPDATE clean.product_staples ps
                SET ppu_min = CASE a.value {cases_lo} ELSE {other[0] if other else 'NULL'} END,
                    ppu_max = CASE a.value {cases_hi} ELSE {other[1] if other else 'NULL'} END
                FROM (SELECT ps2.chain, ps2.product_id, pa.value FROM clean.product_staples ps2
                      LEFT JOIN clean.product_attrs pa ON pa.chain = ps2.chain AND pa.product_id = ps2.product_id
                           AND pa.staple = ps2.staple AND pa.attr = ?
                      WHERE ps2.staple = ?) a
                WHERE ps.chain = a.chain AND ps.product_id = a.product_id AND ps.staple = ?
            """, [attr, st.key, st.key])
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
    auto_ranges = set_auto_ranges(con)  # granice prije grupa: slabi član traži cijenu u granicama
    groups = build_staple_groups(con)
    return {
        "staples": len(staples),
        "groups": groups,
        "matched": con.execute(
            "SELECT count(*) FROM clean.product_staples WHERE NOT excluded AND drop_reason IS NULL").fetchone()[0],
        "excluded": con.execute("SELECT count(*) FROM clean.product_staples WHERE excluded").fetchone()[0],
        "dropped": con.execute("SELECT count(*) FROM clean.product_staples WHERE drop_reason IS NOT NULL").fetchone()[0],
        "attrs": con.execute("SELECT count(*) FROM clean.product_attrs").fetchone()[0],
        "auto_ranges": auto_ranges,
        "suspect_prices": staple_price_suspects(con),
    }


# Ključ grupe proizvoda (alias p = clean.products): globalni EAN, inače lanac + normalizirani naziv
BKEY_SQL = "CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END"
# Pripadnost grupe namirnici (Korak 2E): snažni član m > 50 % i x < 10 %; slabi x = 0 i m >= 25 % (uz
# provjeru jedinice, pakiranja i cijene); m i x su udjeli lanaca, vidi build_staple_groups
STRONG_SHARE, STRONG_MAX_EXCLUDED, WEAK_SHARE = 0.5, 0.10, 0.25
HOW_RANK_SQL = "CASE how WHEN 'name' THEN 0 WHEN 'inferred' THEN 1 WHEN 'heuristic' THEN 2 ELSE 3 END"


def unit_compatible_sql(staple_unit: str, pack_unit: str, compare_by: str = "'unit'") -> str:
    """SQL: je li jedinica pakiranja spojiva s jedinicom namirnice (kom -> kom, kg -> g, l -> ml).
    Nepoznata jedinica pakiranja ne isključuje; vrećice (compare_by pack) primaju sve."""
    return f"""({pack_unit} IS NULL OR {compare_by} = 'pack'
               OR ({staple_unit} = 'kom' AND {pack_unit} = 'kom') OR ({staple_unit} = 'kg' AND {pack_unit} = 'g')
               OR ({staple_unit} = 'l' AND {pack_unit} = 'ml'))"""


def build_staple_groups(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """clean.staple_groups i clean.staple_group_attrs: pripadnost grupe (EAN) namirnici i atributi grupe.

    Po grupi: m = udio lanaca čiji naziv prolazi must_match bez must_not_match, x = udio lanaca čiji
    naziv pogađa must_not_match (neprehrambeni član po kategoriji nije ni m ni x).
    - 'member' / match_quality 'strong': m > 50 % i x < 10 %;
    - 'member' / 'weak': x = 0, m >= 25 %, jedinica spojiva, barem jedan proizvod u min/max pakiranja
      (izvan raspona su već izbačeni) i medijan cijene po jedinici u granicama (ako je poznat);
    - inače 'ambiguous' ako je m > 0, a 'excluded' ako je m = 0;
    - 'excluded' i kad naziv bilo kojeg lanca u grupi pogađa tvrdu neprehranu (clean.products.hard_nonfood).
    Vrijednost atributa grupe: najprije iz naziva (how name > inferred > heuristic > default), zatim
    po broju lanaca, pa abecedno. Vraća (namirnica, snažnih, slabih, dvosmislenih, isključenih).
    """
    con.execute(f"""CREATE OR REPLACE TEMP TABLE product_bkeys AS
                     SELECT p.chain, p.product_id, p.name_norm, {BKEY_SQL} AS bkey FROM clean.products p""")
    con.execute("""
        CREATE OR REPLACE TEMP TABLE staple_bkeys AS
        SELECT DISTINCT ps.staple, pb.bkey FROM clean.product_staples ps JOIN product_bkeys pb USING (chain, product_id)
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE clean.staple_groups AS
        WITH m AS (  -- svi proizvodi grupa koje namirnica dotiče
          SELECT b.staple, b.bkey, p.chain, p.product_id,
                 coalesce(NOT ps.excluded AND NOT coalesce(starts_with(ps.drop_reason, 'kategorija:'), false), false) AS hit,
                 coalesce(ps.excluded, false) AS miss,
                 coalesce(ps.drop_reason IS NULL AND NOT ps.excluded, false) AS usable
          FROM staple_bkeys b JOIN product_bkeys p USING (bkey)
          LEFT JOIN clean.product_staples ps ON ps.chain = p.chain AND ps.product_id = p.product_id
               AND ps.staple = b.staple
        ),
        h AS (  -- tvrda neprehrana u nazivu bilo kojeg lanca isključuje grupu (food.HARD_NONFOOD_REGEX)
          SELECT b.staple, b.bkey, bool_or(p.hard_nonfood) AS hard
          FROM staple_bkeys b JOIN product_bkeys pb USING (bkey) JOIN clean.products p USING (chain, product_id)
          GROUP BY ALL
        ),
        n AS (SELECT staple, bkey, count(DISTINCT chain) AS n_chains,
                     count(DISTINCT chain) FILTER (WHERE hit) AS n_match,
                     count(DISTINCT chain) FILTER (WHERE miss) AS n_miss,
                     count(DISTINCT chain) FILTER (WHERE usable) AS n_usable FROM m GROUP BY ALL),
        u AS (  -- jedinica i cijena po jedinici iskoristivih proizvoda (za slabe članove)
          SELECT m.staple, m.bkey,
                 bool_and({unit_compatible_sql("r.unit", "p.pack_unit", "r.compare_by")}) AS unit_ok
          FROM m JOIN clean.products p USING (chain, product_id) JOIN clean.staple_rules r USING (staple)
          WHERE m.usable GROUP BY ALL
        ),
        pr AS (
          SELECT m.staple, m.bkey, median({STAPLE_PPU_SQL}) AS ppu_med, any_value(r.ppu_min) AS lo, any_value(r.ppu_max) AS hi
          FROM m JOIN clean.product_staples ps USING (staple, chain, product_id)
          JOIN clean.staple_rules r USING (staple) JOIN clean.prices c USING (chain, product_id)
          WHERE m.usable GROUP BY ALL
        ),
        g AS (
          SELECT n.*, n.n_match / n.n_chains AS share_match, n.n_miss / n.n_chains AS share_excluded,
                 coalesce(u.unit_ok, true) AS unit_ok,
                 coalesce(pr.ppu_med IS NULL OR pr.lo IS NULL OR pr.ppu_med BETWEEN pr.lo AND pr.hi, true) AS price_ok,
                 coalesce(h.hard, false) AS hard_nonfood
          FROM n LEFT JOIN u USING (staple, bkey) LEFT JOIN pr USING (staple, bkey) LEFT JOIN h USING (staple, bkey)
        )
        SELECT staple, bkey, n_chains, n_usable, share_match, share_excluded, unit_ok, price_ok, hard_nonfood,
               CASE WHEN hard_nonfood THEN NULL WHEN share_match > {STRONG_SHARE} AND share_excluded < {STRONG_MAX_EXCLUDED} THEN 'strong'
                    WHEN share_excluded = 0 AND share_match >= {WEAK_SHARE} AND unit_ok AND price_ok
                         AND n_usable > 0 THEN 'weak' END AS match_quality,
               CASE WHEN hard_nonfood THEN 'excluded'
                    WHEN share_match > {STRONG_SHARE} AND share_excluded < {STRONG_MAX_EXCLUDED} THEN 'member'
                    WHEN share_excluded = 0 AND share_match >= {WEAK_SHARE} AND unit_ok AND price_ok
                         AND n_usable > 0 THEN 'member'
                    WHEN n_match > 0 THEN 'ambiguous' ELSE 'excluded' END AS status
        FROM g
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE clean.staple_group_attrs AS
        SELECT staple, bkey, attr, value, how FROM (
          SELECT a.staple, p.bkey, a.attr, a.value, arg_min(a.how, {HOW_RANK_SQL}) AS how,
                 min({HOW_RANK_SQL}) AS rnk, count(DISTINCT a.chain) AS n
          FROM clean.product_attrs a JOIN product_bkeys p USING (chain, product_id)
          GROUP BY ALL
        ) QUALIFY row_number() OVER (PARTITION BY staple, bkey, attr ORDER BY rnk, n DESC, value) = 1
    """)
    return con.execute("""
        SELECT staple, count(*) FILTER (WHERE match_quality = 'strong'), count(*) FILTER (WHERE match_quality = 'weak'),
               count(*) FILTER (WHERE status = 'ambiguous'), count(*) FILTER (WHERE status = 'excluded')
        FROM clean.staple_groups GROUP BY staple ORDER BY staple""").fetchall()


# Cijena po jedinici usporedbe namirnice (aliasi: c = clean.prices, ps = clean.product_staples,
# r = clean.staple_rules). Isti izraz koriste build (granice, statistika) i pretraga.
STAPLE_PPU_SQL = """CASE
    WHEN r.compare_by IN ('pack', 'count') THEN round(c.price_eff / nullif(ps.n_units, 0), 2)
    WHEN ps.assumed_g > 0 THEN round(c.price_eff / ps.assumed_g * 1000, 2)
    WHEN c.per_unit = r.unit THEN c.price_per_unit END"""
AUTO_RANGE = (0.25, 4.0)  # automatske granice: 0.25x do 4x medijana namirnice
# Je li cijena po jedinici `ppu` izvan granica [ppu_min, ppu_max] (r = clean.staple_rules). Kod vrećica
# (range_source 'pack') ppu je cijena jedne vrećice, i u višestrukom pakiranju (Korak 2D).
SINGLE_PACK_UNITS = 1.5  # "pojedinačna vrećica" u izvještajima (n_units <= 1,5)


def _envelope(by: dict) -> tuple[float, float] | None:
    """Najširi raspon iz plausible_by (za clean.staple_rules)."""
    ranges = [r for vals in by.values() for r in vals.values()]
    return (min(r[0] for r in ranges), max(r[1] for r in ranges)) if ranges else None


def staple_suspect_sql(ppu: str, n_units: str, ps: str | None = None) -> str:
    """SQL: je li cijena izvan granica. `ps` je alias clean.product_staples s granicama proizvoda
    (plausible_by, npr. svježa/smrznuta prsa); bez njega vrijede granice namirnice (r)."""
    lo = f"coalesce({ps}.ppu_min, r.ppu_min)" if ps else "r.ppu_min"
    hi = f"coalesce({ps}.ppu_max, r.ppu_max)" if ps else "r.ppu_max"
    # range_source 'pack' (vrećice): ppu je cijena po vrećici, i za višestruka pakiranja
    return f"""(NOT (({ppu}) BETWEEN {lo} AND {hi}))"""


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
               count(*) FILTER (WHERE suspect), count(*)
        FROM (
          SELECT ps.staple, r.range_source, {STAPLE_PPU_SQL} AS ppu,
                 {staple_suspect_sql(STAPLE_PPU_SQL, "ps.n_units", "ps")} AS suspect
          FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
          JOIN clean.prices c USING (chain, product_id)
          WHERE NOT ps.excluded AND ps.drop_reason IS NULL AND r.ppu_min IS NOT NULL
        ) WHERE ppu IS NOT NULL
        GROUP BY staple ORDER BY staple
    """).fetchall()
