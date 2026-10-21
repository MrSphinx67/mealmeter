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
# obrnuti redoslijed: "30G*20", "7GX5", "0,5L x 6" (ali ne "50G X 10CM")
_MULTI_REV = re.compile(
    _PRE + _NUM + r"\s*" + _UNIT + r"\.?\s*[x×*]\s*(\d+)(?![\d.,])(?!\s*(?:cm|mm|m)\b)", re.I
)
# bruto/ocijeđeno: "3x80g/3x56g", "3x80/56 g", "2x80/2x52g", "3x70g/50g"
_SLASH_MULTI = re.compile(
    _PRE + r"(\d+)\s*[x×*]\s*" + _NUM + r"\s*" + _UNIT + r"?\s*/\s*(?:(\d+)\s*[x×*]\s*)?" + _NUM + r"\s*" + _UNIT + _POST,
    re.I,
)
# bruto/ocijeđeno: "565g/340g", "185/140g", "115/81G"
_SLASH = re.compile(_PRE + _NUM + r"\s*" + _UNIT + r"?\s*/\s*" + _NUM + r"\s*" + _UNIT + _POST, re.I)
# ocijeđena / neto masa: "ocijeđ mase 130g", "OC. MASA 280 g", "OCJ. MASA 120g", "O.M. 350g",
# "NETO OC.MASA 240 g", "(NETTOMASA 140G)", "(NETO 800G)", "OCIJEĐENA NASA 122 g"
_DRAINED = re.compile(
    r"(?:\bocij|\bocj|\boc\b|\bo\.\s*m\.|\bnett?o)[a-zčćšžđ]*\.?\s*(?:[mn]as[a-zčćšžđ]*\.?)?\s*-?\s*"
    + _NUM + r"\s*" + _UNIT + _POST,
    re.I,
)
# promjenjiva težina: "cca 700g", "CCA1-1,5KG", "1-1,5 kg" (cijena je po kg, gramatura nije pakiranje)
_VARIABLE = re.compile(
    r"\bcca(?=[\s\d.]|$)|(?<![\d.,])\d+(?:[.,]\d+)?\s*-\s*\d+(?:[.,]\d+)?\s*(?:kg|g)\b", re.I
)
# broj komada uz jednu gramaturu: "4+1 GRATIS", "5+1", "3/1" (ne "-25/1-", to je broj u kartonu), "6 PAK"
_PROMO = re.compile(r"(?<![\d.,])(\d{1,2})\s*\+\s*(\d)(?!\d)")
_COUNT = re.compile(r"(?<![\d\-])(?<!-\s)(\d{1,3})\s*/\s*1(?!\d)(?!\s*-)")
_PROMO_GRATIS = re.compile(r"(?<![\d.,])\d{1,2}\s*\+\s*\d(?!\d)\s*(?:gratis|grat\b\.?|gr\b\.?)?", re.I)
_PAK = re.compile(r"(?<![\d.,])(\d{1,2})\s*-?\s*(?:pak|pack)\b", re.I)
# zadnja opcija: "TUNA 2x80" bez jedinice (pretpostavljaju se grami)
_MULTI_NOUNIT = re.compile(r"(?<![\d.,])([1-9]|1[0-2])\s*[x×*]\s*(\d{2,4})(?![\d.,])(?!\s*(?:cm|mm|m\b|x|[a-z]))", re.I)
_SINGLE = re.compile(_PRE + _NUM + r"\s*" + _UNIT + r"\.?" + _POST, re.I)
# jedinica slijepljena s idućom riječi: "250 gVOĆARNA", "250 gMADIG" (mala jedinica, pa veliko slovo);
# bez razlike u veličini slova ("5 LIMUNA") ne vrijedi
_SINGLE_GLUED = re.compile(_PRE + _NUM + r"\s*(kg|gr|g|ml|l)(?=[A-ZČĆŠŽĐ])")
# gramatura do ove vrijednosti uz "4+1" / "3/1" / "6 PAK" je jedna vrećica, ako je i po komadu < 5 g
_SACHET_MAX = 30


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


def _blank(text: str, m: re.Match) -> str:
    return text[: m.start()] + " " * (m.end() - m.start()) + text[m.end():]


def _piece_count(text: str) -> int | None:
    """Broj komada iz "4+1", "3/1" ili "6 PAK" (prvo što se nađe)."""
    if m := _PROMO.search(text):
        return int(m.group(1)) + int(m.group(2))
    if (m := _COUNT.search(text)) and int(m.group(1)) > 1:
        return int(m.group(1))
    if (m := _PAK.search(text)) and int(m.group(1)) > 1:
        return int(m.group(1))
    return None


@lru_cache(maxsize=None)
def analyze_pack(name: str | None) -> tuple[tuple[float, str] | None, float | None, bool, str | None]:
    """(bruto gramatura, ocijeđena masa, promjenjiva težina, pack_confidence) iz naziva.

    - Bruto (neto s tekućinom kod konzervi): (količina, 'g' | 'ml' | 'kom') ili None. Prioritet:
      višestruko pakiranje ("6x0,33 l", "30G*20", "7GX5") > bruto iz "bruto/ocijeđeno" >
      masa/volumen > komadi. Jedna mala gramatura uz "4+1", "3/1" ili "6 PAK" množi se brojem
      komada ("7 g 4+1" -> 35 g), osim ako je očito već ukupna ("35G 4+1", "5+1 48GR").
    - Ocijeđena masa u g/ml ("185/140g" -> 140, "3x80/56 g" -> 168, "OC. MASA 280 g" -> 280).
    - Promjenjiva težina ("cca", "1-1,5 kg"): bruto je None, cijena je po kg.
    - pack_confidence: "low" kad gramatura ovisi o heuristici (broj komada uz "4+1"/"3/1"/"PAK",
      "2x80" bez jedinice, višestruko pakiranje uz "gratis"), inače "high"; None bez gramature.
    Oznake "-12/1-" (broj u kartonu) i "(10)" se ne tumače.
    """
    if not name:
        return None, None, False, None
    if _VARIABLE.search(name):
        return None, None, True, None
    text, gross, drained = name, None, None
    gratis = bool(re.search(r"gratis|\bgrat\b", name, re.I))

    if m := _SLASH_MULTI.search(text):
        n, unit_b = int(m.group(1)), m.group(6)
        a, unit = _to_base(m.group(2), m.group(3) or unit_b)
        b, _ = _to_base(m.group(5), unit_b)
        if n > 0 and 0 < b:
            gross = (round(n * a, 3), unit)
            drained = round((int(m.group(4)) if m.group(4) else (n if b < a else 1)) * b, 3)
            text = _blank(text, m)
    elif (m := _SLASH.search(text)) and (m.group(2) or _num(m.group(1)) >= 20):
        a, unit = _to_base(m.group(1), m.group(2) or m.group(4))
        b, unit_b = _to_base(m.group(3), m.group(4))
        if unit == unit_b and 0 < b < a and _num(m.group(3)) >= 10:
            gross, drained = (a, unit), b
            text = _blank(text, m)
    if drained is None and (m := _DRAINED.search(text)) and _num(m.group(1)) > 0:
        drained = _to_base(m.group(1), m.group(2))[0]
        text = _blank(text, m)
    if gross:
        return gross, drained, False, "high"

    if (m := _MULTI.search(text)) and int(m.group(1)) > 0 and _num(m.group(2)) > 0:
        amount, unit = _to_base(m.group(2), m.group(3))
        return (round(int(m.group(1)) * amount, 3), unit), drained, False, "low" if gratis else "high"
    if (m := _MULTI_REV.search(text)) and int(m.group(3)) > 0 and _num(m.group(1)) > 0:
        amount, unit = _to_base(m.group(1), m.group(2))
        return (round(int(m.group(3)) * amount, 3), unit), drained, False, "low" if gratis else "high"

    k_all = _piece_count(text)
    # "4+1 GR." / "4+1 GRATIS": "GR." je kratica za gratis, ne grami
    singles_text = _PROMO_GRATIS.sub(lambda m: " " * len(m.group(0)), text)
    found = [_to_base(m.group(1), m.group(2)) for m in _SINGLE.finditer(singles_text) if not _is_age(singles_text, m)]
    found = [f for f in found if f[0] > 0]
    pick = next((f for f in found if f[1] != "kom"), found[0] if found else None)
    if pick:
        amount, unit = pick
        k = k_all if unit != "kom" else None
        confidence = "high"
        if k:
            confidence = "low"  # "4+1"/"3/1"/"PAK": je li gramatura po komadu ili ukupna, procjena je
            if amount <= _SACHET_MAX and amount / k < 5:
                amount = round(amount * k, 3)
        return (amount, unit), drained, False, confidence
    if m := _MULTI_NOUNIT.search(text):
        return (float(int(m.group(1)) * int(m.group(2))), "g"), drained, False, "low"
    if (m := _SINGLE_GLUED.search(text)) and _num(m.group(1)) > 0:
        return _to_base(m.group(1), m.group(2)), drained, False, "high"
    return None, drained, False, None


def parse_pack(name: str | None) -> tuple[float, str] | None:
    """Bruto gramatura iz naziva: (količina, 'g' | 'ml' | 'kom') ili None (vidi analyze_pack)."""
    return analyze_pack(name)[0]


def parse_drained(name: str | None) -> float | None:
    """Ocijeđena (neto) masa konzerve u g/ml ili None (vidi analyze_pack)."""
    return analyze_pack(name)[1]


def is_variable_weight(name: str | None) -> bool:
    """Artikl promjenjive težine ("CCA 1 kg", "1-1,5KG"): cijena je po kg, gramatura nije pakiranje."""
    return analyze_pack(name)[2]


def pack_confidence(name: str | None) -> str | None:
    """"high" / "low" (heuristika višestrukog pakiranja) / None (nema gramature), vidi analyze_pack."""
    return analyze_pack(name)[3]


def is_clearance(name: str | None) -> bool:
    """Rasprodaja / sniženje zbog roka ili kvalitete: "SNIŽENJE", "SNIŽENO", "SNIŽENI"."""
    return bool(name) and bool(re.search(r"(^| )snizen", norm_text(name) or ""))


def parse_pack_unit_field(unit: str | None) -> tuple[float, str] | None:
    """Gramatura iz stupca `unit` kad lanac tamo upisuje veličinu pakiranja (Lidl: "80g", "10x1kg").

    Više različitih veličina ("123g,200g,77g") znači miks varijanti, pa vraća None.
    """
    if not unit or not any(c.isdigit() for c in unit) or len(_SINGLE.findall(unit)) > 1 and not _MULTI.search(unit):
        return None
    return parse_pack(unit)


def parse_multipack_unit(unit: str | None) -> tuple[int, float, str] | None:
    """Višestruko pakiranje iz stupca `unit` (Lidl: "6x12g", "6x8g", "4x0,5l", "30G*20"): (broj komada,
    količina jednog komada, 'g' | 'ml' | 'kom'), inače None."""
    if not unit:
        return None
    if (m := _MULTI.search(unit)) and int(m.group(1)) > 0 and _num(m.group(2)) > 0:
        return int(m.group(1)), *_to_base(m.group(2), m.group(3))
    if (m := _MULTI_REV.search(unit)) and int(m.group(3)) > 0 and _num(m.group(1)) > 0:
        return int(m.group(3)), *_to_base(m.group(1), m.group(2))
    return None


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


# --- Kategorije ----------------------------------------------------------------

# Skupine hrane (food_group): is_food je true za FOOD_GROUPS, false za NONFOOD_GROUPS, a
# 'unknown' (is_food NULL) kad kategorija lanca ništa ne govori (nema je, ili je "Ostalo").
FOOD_GROUPS = ("hrana", "pice", "alkohol")
NONFOOD_GROUPS = ("kozmetika", "higijena", "kucanstvo", "djeca", "kucni_ljubimci", "ostalo")
FOOD_GROUP_VALUES = FOOD_GROUPS + NONFOOD_GROUPS + ("unknown",)

# (grupa, uzorci na početku riječi u norm_text(category)); prvo pravilo koje pogodi pobjeđuje.
# Uzorci su u normaliziranom obliku: "dječja" -> "decja", "za djecu" -> "za decu".
# "Ostalo" kod NTL-a, trgovine Krk, Gavranovića i Žabca miješa svrdla, ručnike i gastro hranu, pa su
# takve kategorije (cijeli naziv) 'unknown'.
_UNINFORMATIVE_CATEGORIES = {"ostalo", "razno", "mix", "mjesavine", "trgovacka roba", "izbaceni", "valentinovo",
                             "impuls", "usluge", "mita bozicni asortiman"}
# Pravila služe za izradu data/category_map.yaml (scripts/make_category_map.py) i kao rezerva za
# kategorije kojih u mapi nema. Kategorija bez pogotka je 'unknown'.
_CATEGORY_RULES = [
    ("hrana", r"ocat\b"),  # "ALKOHOLNI OCAT", "VINSKI OCAT"
    ("djeca", r"decj|decij|decu\b|deca\b|bebe|baby|dojenc|pelen"),
    ("kucni_ljubimci", r"ljubim|za pse|za macke"),
    ("alkohol", r"vino|vina\b|pivo|piva\b|zestok|pjenus|liker|whisk|gin\b|rum\b|rakij|pelinkovac|prosek|"
                r"cider|konjak|tequila|vodk|sljivovic|orahovac|travaric|radler|bib bijelo|bib crno|"
                r"alkoholn|gotovi koktel|aperitiv|brandy|core 0 5|premium 0 5|kruskovac|komovica|jeger"),
    ("ostalo", r"duhan|cigaret|tel kartice|bonovi|zdravlje|dodaci prehrani|prezervativ|kondom|zarulj|upaljac|"
               r"album|slicice|flaster|hanzaplast|vata\b|cvijece|sjemenj|elektricn|igrack|tekstil|obuc|"
               r"skolsk|uredsk|poklon|party|neprehrana|sumece tablete|sumace tablete|foto\b|tisak"),
    ("higijena", r"toaletn|higijen|tampon|ulosc|usta zubi|njega usana|zubn|cetkica za zube|britvic|brijac|"
                 r"vlazne maramice|maramic|sapun|blazinice|njega zubi"),
    ("kozmetika", r"kozm|njega|sampon|tijelo|lice\b|kosa\b|kosu\b|mirisi|parfem|drogerij|dekorativ|deo\b|"
                  r"dezodor|gel za tus|gel za brij|gel za kosu|pjena za brij|losion|balzam|regenerator|labelo|"
                  r"krema za ruke|krema od|krema do|krema for|krema za brij|univerzalna krema|pjenaste kupke|suncanj|"
                  r"zastita od sunca|spf|depilac|pasta za ruke"),
    ("kucanstvo", r"kucanstv|kucn|kucansk|domacinstv|sredstva za|sredstvo|sred za|cisc|ciisc|deterg|det za|"
                  r"omeksiv|rublj|posud|oprema|ambalaz|papirna|svijec|uredenje|zice|celicna|spuzv|krpe|krpa|"
                  r"metl|lopatica|rukavice|vrece|folij|papir za pecenje|kuhinjski rucnici|salvete|cackalice|"
                  r"stapici drveni|odcepljivac|odstranjivac|odmascivac|izbjeljivac|kamenca|perilic|miris za wc|"
                  r"wc\b|uradi sam|gel za rublje|deterdzent|vrecice za led|ljepilo|cistaci|sibice|patrone|persil|"
                  r"krpica|filter za kavu"),
    ("pice", r"pic|sok|vod|napitc|napitak|kava|kave\b|cappuccino|caj\b|cajev|ledeni caj|tonic|smoothie|cedevita|funkcionaln|"
             r"instant mjesavina za kavu|bio napitak|bezalkohol|kavovina|energetski|dodaci za koktele"),
    ("hrana", r"hran|namirnic|meso|mesn|mlijec|mlijek|sir|povrc|voc|kruh|pekar|tjestenin|riza|zitaric|"
              r"zacin|konzerv|slatk|slan|grickal|keks|cokolad|bombon|smrz|svjez|delikat|riba|ulje|ocat|"
              r"dorucak|kolac|kiselin|juhe|juha|umac|umak|deserti|desert|prehrana|program|tuna|odjel|"
              r"priprem|musli|kase\b|kasa\b|protein|suhomesn|cips|zvak|toploteka|ferment|marmelad|dzem|"
              r"pekmez|slastic|kreker|lizalic|secer|sol\b|zasladiv|kikiriki|praline|pakirano|vafl|med\b|"
              r"papar|kroasan|piletin|puretin|flips|pasiran|rajcic|sladoled|puding|sardin|tost|brasno|zoben|"
              r"sunka|salam|gotova jela|gotovo jelo|zitna|vrhnj|spageti|prsut|pastet|parizer|namaz|panceta|"
              r"medenjac|krastav|kokic|peciv|snack|vanilin|pereci|parmezan|brusket|skamp|palent|"
              r"mix za pecenje|dvopek|corn flakes|biskvit|petit beurre|orah|koncentrat|jaffa|stapici|skus|"
              r"rezanc|paprika|lazanj|krumpir|tortil|kvasac|kefir|kobasic|hrenovk|majonez|fusilli|feferon|"
              r"lignj|ribic|origano|narezak|maslin|krusne|ketchup|kiseli|jogurt|jaja|grasak|zm\b|filet|"
              r"tortel|skittles|senf|sampinj|prasak|pommes|muffin|mentos|kukuruz|kompot|kapula|luk\b|"
              r"ferrero|cikla|njok|zimska|tic tac|rakovi|mozzar|kulen|kocka|griz|grah|fidelin|drops|"
              r"borovnic|bananic|aceto|balsam|hobotnic|tartar|strudl|sezam|puzic|pez\b|masla|incun|"
              r"listovi za pite|kuglof|kakao|gauda|ajvar|penne|rolada|panettone|sitni|fant\b|subioti|"
              r"trajna|budola|mlinc|tijest|lisnat|gastro|jela\b|jelo\b|bakalar|badem|ulja|masti|mast\b|slag|ragu|"
              r"preljev|pomfrit|pistaci|piskot|munchmallow|salata|margarin|mahun|gulas|gouda|gljiv|pahulj|"
              r"brusnic|bezgluten|bajadera|temeljac|temeljci|suncokret|soda bikarbona|sljiva|skoljk|papaja|"
              r"odrezak|mileram|knedl|jecam|hren|hamburger|grozd|fileki|chia|agrumi|tirolsk|tarana|"
              r"tagliatelle|spinat|slova|pogac|pecenic|mortadel|meksicki|kozic|marelic|mak\b|ljesnjak|leca|"
              r"krafn|ementaler|cvarc|crnilo|sjemenke|aroma|acedofil|zvjezdic|worcester|visnj|uht\b|crijeva|"
              r"somboled|plodovi mora|lokum|kore za tortu|jabuka|duvec|carska|brokul|bob\b|blitva|banana|"
              r"led\b|dodatak jelu|pelat|praskasti"),
]


def category_group(category: str | None) -> str:
    """Skupina kategorije lanca prema pravilima (_CATEGORY_RULES): hrana, pice, alkohol, kozmetika,
    higijena, kucanstvo, djeca, kucni_ljubimci, ostalo ili 'unknown' (nema kategorije ili ništa
    ne pogađa). Build koristi data/category_map.yaml, a ova pravila samo za kategorije izvan mape."""
    if not category:
        return "unknown"
    text = norm_text(category)
    if text in _UNINFORMATIVE_CATEGORIES:
        return "unknown"
    for group, pattern in _CATEGORY_RULES:
        if re.search(r"(^| )(?:" + pattern + ")", text):
            return group
    return "unknown"
