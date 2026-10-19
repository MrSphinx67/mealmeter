"""Normalizacija teksta, EAN-a, gramature i gradova (čiste funkcije, bez baze)."""

import re
import unicodedata
from datetime import date
from functools import lru_cache


def norm_text(s: str | None) -> str | None:
    """Mala slova, bez dijakritika, interpunkcija u razmake.

    'đ' i 'dj' oboje postaju 'd', tako da se "Đakovo", "Djakovo" i "Dakovo" podudaraju.
    """
    if s is None:
        return None
    s = s.lower().replace("đ", "d").replace("dj", "d")
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def date_hr(d: date) -> str:
    return f"{d.day:02d}.{d.month:02d}.{d.year}."


# --- EAN / GTIN ---------------------------------------------------------------


def gtin_ok(code: str) -> bool:
    """Provjera kontrolne znamenke za EAN-8, UPC-A (12), EAN-13 i GTIN-14."""
    if not code.isdigit() or len(code) not in (8, 12, 13, 14):
        return False
    body, check = code[:-1], int(code[-1])
    total = sum(int(c) * (3 if i % 2 == 0 else 1) for i, c in enumerate(reversed(body)))
    return (10 - total % 10) % 10 == check


@lru_cache(maxsize=None)
def normalize_ean(barcode: str | None) -> tuple[str | None, bool, bool]:
    """Vrati (ean_norm, ean_valid, ean_global).

    - 11 znamenki: UPC-A kojem je izgubljena vodeća nula, pa se dopuni ako postane valjan.
    - 12 znamenki (UPC-A) i 14 znamenki s vodećom nulom svode se na EAN-13, da se isti
      proizvod podudara među lancima.
    - ean_norm je NULL ako kod nije valjan GTIN.
    - ean_global je False za kodove ograničene upotrebe (in-store / vaga: EAN-13 s prefiksom
      2, 02x, 04x; EAN-8 s prefiksom 0 ili 2). Takve kodove ne spajamo među lancima.
    """
    if barcode is None:
        return None, False, False
    b = barcode.strip()
    if not b.isdigit():
        return None, False, False
    if len(b) == 11 and gtin_ok("0" + b):
        b = "0" + b
    if len(b) == 12 and gtin_ok(b):
        b = "0" + b
    if len(b) == 14 and b[0] == "0" and gtin_ok(b):
        b = b[1:]
    if not gtin_ok(b) or len(b) == 12:
        return None, False, False
    restricted = (len(b) == 13 and (b[0] == "2" or b[:2] in ("02", "04"))) or (
        len(b) == 8 and b[0] in "02"
    )
    return b, True, not restricted


# --- Gramatura iz naziva -------------------------------------------------------

_NUM = r"(\d+(?:[.,]\d+)?)"
# jedinica -> (osnovna jedinica, faktor)
_UNITS = {
    "kg": ("g", 1000), "kgr": ("g", 1000), "dag": ("g", 10),
    "g": ("g", 1), "gr": ("g", 1), "grama": ("g", 1),
    "l": ("ml", 1000), "lt": ("ml", 1000), "ltr": ("ml", 1000), "lit": ("ml", 1000),
    "litra": ("ml", 1000), "litre": ("ml", 1000), "litara": ("ml", 1000),
    "dl": ("ml", 100), "cl": ("ml", 10), "ml": ("ml", 1),
    "kom": ("kom", 1), "komad": ("kom", 1), "komada": ("kom", 1), "kos": ("kom", 1),
}
# Duže varijante prve, da 'kg' ne bude pročitan kao 'k' + 'g'
_UNIT = "(" + "|".join(sorted(_UNITS, key=len, reverse=True)) + ")"
# Broj ne smije biti nastavak drugog broja ("1.5" -> ne "5"), dio "PAL=112KOM" ni nazivnik
# razlomka ("JAJA 10/1 L" je veličina L, ne 1 litra); točka iza slova je kratica
# ("UG.190 g" -> 190 g), a ne decimalni separator
_PRE = r"(?<![\d=/])(?<!\d[.,])"
_POST = r"(?![a-zčćšžđ])"

_MULTI = re.compile(_PRE + r"(\d+)\s*[x×*]\s*" + _NUM + r"\s*" + _UNIT + r"\.?" + _POST, re.I)
# obrnuti redoslijed: "30G*20", "0,5L x 6" (ali ne "50G X 10CM")
_MULTI_REV = re.compile(
    _PRE + _NUM + r"\s*" + _UNIT + r"\.?\s*[x×*]\s*(\d+)(?![\d.,])(?!\s*(?:cm|mm|m)\b)", re.I
)
_SLASH = re.compile(_PRE + _NUM + r"\s*" + _UNIT + r"\s*/\s*" + _NUM + r"\s*" + _UNIT + _POST, re.I)
_DRAINED = re.compile(r"ocij[a-zčćšžđ]*\.?\s*(?:mas[a-zčćšžđ]*\.?)?\s*" + _NUM + r"\s*" + _UNIT + _POST, re.I)
# "cca 700g" = artikl promjenjive težine koji se prodaje po kg; gramatura nije pakiranje
_APPROX = re.compile(r"\bcca\b", re.I)
_SINGLE = re.compile(_PRE + _NUM + r"\s*" + _UNIT + r"\.?" + _POST, re.I)


def _num(s: str) -> float:
    return float(s.replace(",", "."))


def _to_base(amount: str, unit: str) -> tuple[float, str]:
    base, factor = _UNITS[unit.lower()]
    return round(_num(amount) * factor, 3), base


def _is_age(name: str, m: re.Match) -> bool:
    """Oznaka dobi na dječjoj hrani ("+1g", "1g.+" = od 1 godine), a ne 1 gram."""
    if m.group(2).lower() != "g" or _num(m.group(1)) > 3:
        return False
    before = name[: m.start()].rstrip()
    after = name[m.end():].lstrip()
    return before.endswith("+") or after.startswith("+")


@lru_cache(maxsize=None)
def parse_pack(name: str | None) -> tuple[float, str] | None:
    """Gramatura iz naziva: (količina, 'g' | 'ml' | 'kom') ili None.

    Prioritet: višestruko pakiranje ("6x0,33 l", "30G*20") > ocijeđena masa ("185g ocijeđ.mase 130g",
    "565g/340g": uzima se drugi broj) > masa/volumen > komadi. Oznake poput "5/1" ili "(10)"
    se ne tumače. Nazivi s "cca" (promjenjiva težina, cijena po kg) vraćaju None.
    """
    if not name or _APPROX.search(name):
        return None
    if (m := _MULTI.search(name)) and int(m.group(1)) > 0 and _num(m.group(2)) > 0:
        amount, unit = _to_base(m.group(2), m.group(3))
        return round(int(m.group(1)) * amount, 3), unit
    if (m := _MULTI_REV.search(name)) and int(m.group(3)) > 0 and _num(m.group(1)) > 0:
        amount, unit = _to_base(m.group(1), m.group(2))
        return round(int(m.group(3)) * amount, 3), unit
    if (m := _DRAINED.search(name)) and _num(m.group(1)) > 0:
        return _to_base(m.group(1), m.group(2))
    if m := _SLASH.search(name):
        a1, u1 = _to_base(m.group(1), m.group(2))
        a2, u2 = _to_base(m.group(3), m.group(4))
        if u1 == u2 and a2 > 0:
            return a2, u2
    found = [_to_base(m.group(1), m.group(2)) for m in _SINGLE.finditer(name) if not _is_age(name, m)]
    found = [f for f in found if f[0] > 0]
    for amount, unit in found:
        if unit != "kom":
            return amount, unit
    return found[0] if found else None


def parse_pack_unit_field(unit: str | None) -> tuple[float, str] | None:
    """Gramatura iz stupca `unit` kad lanac tamo upisuje veličinu pakiranja (Lidl: "80g", "10x1kg").

    Više različitih veličina ("123g,200g,77g") znači miks varijanti, pa vraća None.
    """
    if not unit or not any(c.isdigit() for c in unit) or len(_SINGLE.findall(unit)) > 1 and not _MULTI.search(unit):
        return None
    return parse_pack(unit)


def unit_hint(unit: str | None, quantity: str | None) -> str | None:
    """Na koju jedinicu se (vjerojatno) odnosi unit_price lanca: 'kg', 'l' ili None.

    Koristi se samo za unit_confidence='low'. Prvo gleda jedinicu u stupcu quantity
    ("0.20 kg", "100 G"), zatim stupac unit.
    """
    if quantity and (p := parse_pack(quantity)) and p[1] != "kom":
        return "kg" if p[1] == "g" else "l"
    u = norm_text(unit) or ""
    if u in ("kg", "kilogram", "kgm"):
        return "kg"
    if u in ("l", "lt", "lit", "litra"):
        return "l"
    return None


# --- Gradovi -------------------------------------------------------------------

# norm(alias) -> kanonski naziv grada. Ključevi su normalizirani s norm_text.
CITY_ALIASES = {
    "sesvete": "Zagreb",
    "sesvete kraljevec": "Zagreb",
    "sesvetski kraljevec": "Zagreb",
    "zagreb dubrava": "Zagreb",
    "dubrava": "Zagreb",
    "novi zagreb": "Zagreb",
    "lucko": "Zagreb",
    "kasina": "Zagreb",
    "v gorica": "Velika Gorica",
    "hrv kostajnica": "Hrvatska Kostajnica",
    "umag umago": "Umag",
    "laslovo szentlaszlo": "Laslovo",
    "kastel gomilica": "Kaštela",
    "kastel kambelovac": "Kaštela",
    "kastel luksic": "Kaštela",
    "kastel novi": "Kaštela",
    "kastel stari": "Kaštela",
    "kastel sucurac": "Kaštela",
    "kastel stafilic": "Kaštela",
}


def canonical_city(city: str | None) -> str | None:
    if city is None:
        return None
    return CITY_ALIASES.get(norm_text(city), city.strip())
