"""Marka (proizvođač) proizvoda za prikaz u izlazima alata (Korak 13).

Redoslijed: stupac `brand` iz cjenika, očišćen; kad je prazan ili nije marka, marka iz naziva proizvoda preko
data/brands.yaml; inače None. Marka se nikad ne izmišlja: dobavljač, distributer ili uvoznik (d.o.o., Orbico,
„ITALIJA - UNOS”), skupina robe (Stanić) ili naziv drugog lanca nisu marka. Vlastite marke lanaca (K Plus,
Milbona, S-Budget, K-Classic, Spar u Sparu) jesu.
"""

import re
from functools import lru_cache
from pathlib import Path

from mealmeter.normalize import norm_text

BRANDS_PATH = Path(__file__).resolve().parents[2] / "data" / "brands.yaml"


@lru_cache(maxsize=2)
def load_brands(path: Path = BRANDS_PATH) -> tuple[tuple[str, str], ...]:
    """Marke iz data/brands.yaml kao (naziv, regex na početku riječi normaliziranog teksta)."""
    import yaml

    if not Path(path).exists():
        return ()
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return tuple((name, "(^| )(?:" + "|".join(pats) + ")") for name, pats in raw.items())


@lru_cache(maxsize=1)
def _brand_rx() -> tuple[tuple[str, re.Pattern], ...]:
    return tuple((name, re.compile(rx)) for name, rx in load_brands())


# lanci u kojima stupac brand nije marka nego skupina robe ("SM. RIBLJI PROIZVODI NEP.", "HL. SIRNI PROIZVODI BUCO")
NOT_BRAND_CHAINS = frozenset({"stanic"})

# pravni oblik tvrtke (dobavljač ili distributer, ne marka); na normaliziranom tekstu ("d.o.o." -> "d o o")
_COMPANY_RX = re.compile(
    r"(^| )(j d o o|d o o|doo|d d|dd|b v|bv|gmbh|s p a|spa|s r l|srl|ltd|kft|s r o|sro|co kg|kg|s a|sa|ag|inc|llc"
    r"|obrt|tr obrt)( |$)")
# vrijednosti koje nisu marka: bez marke, ostalo, uvoz, skladište, vlastita marka bez imena
_JUNK_RX = re.compile(
    r"(^| )(no brand|nobrand|bez marke|nepoznat\w*|ostalo|razno|generic|unos|uvoz|skladiste|robna marka"
    r"|autres marques|societe|tarif|nep)( |$)")
_JUNK_EXACT = frozenset({"", "na", "n a", "nn", "x", "xx", "0", "00", "none", "null", "nema", "brand", "marka",
                         "ostalo", "razno"})

# distributeri i dobavljači koji se u stupcu pojavljuju i bez pravnog oblika (normalizirani početak vrijednosti)
DISTRIBUTORS = (
    "orbico", "awt", "atlantic trade", "ira commerce", "koopman", "eurocom", "nird", "brodplast", "sumoopskrba",
    "tekstilpromet", "alca", "emo adria", "krena", "lapis", "offertissima", "filir", "maja papirus", "kb",
    "ivmar", "petason", "dobro rjesenje", "phoenix trade", "hp hobby program", "mat tr", "toi toys", "edco",
    "berisic", "tojeto", "aranea toys", "kaemingk", "turistika", "forum knjige", "karneval bw", "ultra", "vm2",
    "opskrba",
)
_DISTRIBUTOR_RX = re.compile(r"^(?:" + "|".join(re.escape(d) for d in DISTRIBUTORS) + r")( |$)")

# nazivi lanaca (normalizirani) i lanci kojima je to i vlastita marka (SPAR u Sparu, PLODINE u Plodinama)
CHAIN_NAMES = {
    "narodni trgovacki lanac": "ntl", "ntl": "ntl", "konzum": "konzum", "plodine": "plodine", "spar": "spar",
    "interspar": "spar", "studenac": "studenac", "tommy": "tommy", "kaufland": "kaufland", "lidl": "lidl",
    "trgovina krk": "trgovina-krk", "gavranovic": "gavranovic", "ktc": "ktc", "ribola": "ribola", "boso": "boso",
    "stridon": "stridon", "vrutak": "vrutak", "trgocentar": "trgocentar", "eurospin": "eurospin", "metro": "metro",
    "dm": "dm", "zabac": "zabac", "lorenco": "lorenco", "bure": "bure", "jadranka": "jadranka_trgovina",
    "stanic": "stanic", "branka": "branka", "roto": "roto",
}
OWN_BRAND_CHAINS = frozenset({"spar", "plodine", "metro", "dm", "lidl", "kaufland", "konzum", "tommy", "eurospin"})

# riječ prije marke u nazivu koja znači da je marka sastojak ili okus, a ne proizvođač ("keksi s Nutellom")
# vrijednosti samo od ovih riječi su odjel ili vrsta robe, ne marka ("Crveno meso", "Povrće svježe", "Boso voće")
_GENERIC_WORDS = frozenset({"voce", "povrce", "svjeze", "svjezi", "svjeza", "meso", "crveno", "bijelo", "riba", "ribe",
                            "kruh", "pekara", "mlijecni", "proizvodi", "delikatesa", "delikatese", "gastro", "i",
                            "prehrana", "neprehrana", "vlastita", "proizvodnja", "kolaci", "sirevi", "suhomesnato",
                            "map", "pakiranja", "pakiranje"})

_INGREDIENT_BEFORE = frozenset({"s", "sa", "i", "okus", "okusom", "punjen", "punjena", "punjeno", "punjeni", "za",
                                "od", "with", "a la", "preljev", "krema", "kremom"})

_KEEP_LOWER = frozenset({"di", "da", "del", "della", "dal", "la", "le", "de", "e", "i", "s", "sa", "od", "von", "van",
                         "und", "and", "of"})


def _known(text: str, anywhere: bool = True) -> str | None:
    """Marka iz brands.yaml u normaliziranom tekstu: najranije podudaranje (pri istom mjestu prva u datoteci).
    anywhere=False: samo na početku teksta. Riječ ispred iz _INGREDIENT_BEFORE poništava podudaranje."""
    best = None
    for name, rx in _brand_rx():
        for m in rx.finditer(text):
            pos = m.start() + (1 if m.group(0).startswith(" ") else 0)
            if not anywhere and pos > 0:
                break
            before = text[:pos].split()
            if before and (before[-1] in _INGREDIENT_BEFORE or " ".join(before[-2:]) in _INGREDIENT_BEFORE):
                continue
            if best is None or pos < best[0]:
                best = (pos, name)
            break
    return best[1] if best else None


def _pretty(raw: str) -> str:
    """Prikaz vrijednosti iz cjenika: dio prije zareza ("PODRAVKA, KOPRIVNICA"), višestruki razmaci, a vrijednost
    pisana samo velikim slovima ("K PLUS", "METRO CHEF") kao "K Plus", "Metro Chef"."""
    s = re.sub(r"\s+", " ", raw.split(",")[0]).strip(" -_*.;/")
    if any(c.islower() for c in s):
        return s
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i and lw in _KEEP_LOWER:
            out.append(lw)
        else:
            out.append("-".join(p[:1].upper() + p[1:].lower() for p in w.split("-")))
    return " ".join(out)


def clean_brand(raw: str | None, chain: str | None = None) -> str | None:
    """Marka iz stupca brand cjenika ili None kad vrijednost nije marka."""
    if raw is None or chain in NOT_BRAND_CHAINS:
        return None
    text = norm_text(raw) or ""
    if text in _JUNK_EXACT or not re.search(r"[a-z]", text):
        return None
    if known := _known(text):  # "PODRAVKA d.d. KOPRIVNICA", "VINDIJA D.O.O.", "DR.OETKER" -> marka iz brands.yaml
        return known
    if _COMPANY_RX.search(text) or _JUNK_RX.search(text) or _DISTRIBUTOR_RX.search(text):
        return None
    base = norm_text(raw.split(",")[0]) or ""
    words = base.split()
    if all(w in _GENERIC_WORDS for w in words):
        return None
    # naziv lanca ("NTL", "NARODNI TRGOVAČKI LANAC") ili lanac s odjelom ("NTL - Voće i povrće", "Boso voće"): marka
    # samo kao vlastita marka toga lanca ("SPAR", "SPAR Natur*pur", "Plodine Gastro"), i to ne kad je ostatak odjel
    for n in (3, 2, 1):
        head = " ".join(words[:n])
        if len(words) >= n and head in CHAIN_NAMES:
            own = CHAIN_NAMES[head] == chain and chain in OWN_BRAND_CHAINS
            rest = words[n:]
            if not own or (rest and all(w in _GENERIC_WORDS for w in rest)):
                return None
            break
    return _pretty(raw) or None


def brand_from_name(name: str | None) -> str | None:
    """Marka iz naziva proizvoda preko brands.yaml ("Brašno glatko T-550 Mlineta 1 kg" -> "Mlineta"), inače None."""
    return _known(norm_text(name or "") or "")


@lru_cache(maxsize=65536)
def display_brand(raw: str | None, name: str | None, chain: str | None = None) -> str | None:
    """Marka za prikaz: očišćen stupac brand; marka iz brands.yaml na početku naziva ima prednost pred vrijednošću
    stupca koja nije u brands.yaml (dobavljač bez pravnog oblika, npr. "EUROCOM" uz "NUTELLA 400G"); kad stupca
    nema, marka iz naziva; inače None."""
    col = clean_brand(raw, chain)
    if col is not None and norm_text(col) == norm_text(name or ""):  # stupac ponavlja naziv ("Krumpir"): nije marka
        col = None
    if col is not None and _known(norm_text(col) or "") == col:
        return col
    lead = _known(norm_text(name or "") or "", anywhere=False)
    if lead and col is not None:
        return lead
    return col if col is not None else brand_from_name(name)


def group_brand(rows: list[tuple[str | None, str | None, str | None]], unique: bool = False) -> str | None:
    """Marka grupe proizvoda (isti EAN u više lanaca) iz [(brand, name, chain)]: najčešća marka za prikaz, pri
    jednakom broju abecedno prva; None kad nijedan redak nema marku. unique=True (klasa namirnice s proizvodima
    više proizvođača): marka samo kad svi proizvodi imaju istu marku (nijedan bez marke)."""
    counts: dict[str, int] = {}
    for raw, name, chain in rows:
        b = display_brand(raw, name, chain)
        if b is None and unique:
            return None
        if b:
            counts[b] = counts.get(b, 0) + 1
    if not counts or (unique and len(counts) > 1):
        return None
    return min(counts, key=lambda b: (-counts[b], b))
