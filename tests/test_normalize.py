from datetime import date

import pytest

from mealmeter.normalize import (
    canonical_city,
    date_hr,
    gtin_ok,
    norm_text,
    normalize_ean,
    parse_pack,
    parse_pack_unit_field,
    unit_hint,
)

# Stvarni nazivi iz arhive cijene.dev 2026-10-19 -> očekivana gramatura (g / ml / kom)
REAL_NAMES = [
    # kg
    ("PECIVO KROASAN SA ČOKOLADOM 0,08 kg", (80, "g")),
    ("TJ.BARILLA 1 kg PENNE RIGATE", (1000, "g")),
    ("PUNJENI ŠAMPINJONI 1 kg TK", (1000, "g")),
    ("1KG MC SPRING ROL POVRĆE 50/1", (1000, "g")),
    ("5KG GRAH BIJELI -VC", (5000, "g")),
    ("ULTRA DRVENI UGLJEN 2,5KG (120)", (2500, "g")),
    ("BRAŠNO GLATKO 25kg ČK.MLINOVI", (25000, "g")),
    ("BRAŠNO CRNO T-1600 1kg FARINA", (1000, "g")),
    ("BRAŠNO B.G. 1 kg ADVENT", (1000, "g")),
    ("BRAŠNO GLATKO T-550 1kg ČAKOVEČKI", (1000, "g")),
    ("BRASNO T-550 5 KG GLATKO CAKOVECKI MLINOVI", (5000, "g")),
    ("MAST SVINJ 1kg VRBOVEC", (1000, "g")),
    # g
    ("AIRWICK GEL 150 g MA GNOLIA", (150, "g")),
    ("Francuski baguet.premium 400 g", (400, "g")),
    ("KAŠICA JAB/BRE/Š.VOĆ. 100 g HI", (100, "g")),
    ("JOGURT TEKUĆI 0.9%MM LIGHT 200g Z'BREGOV VINDIJA", (200, "g")),
    ("KLC.Đumbir mljeveni 30g", (30, "g")),
    ("DVOPEK FETTE DORATE 315g 2060 AWT", (315, "g")),
    ("ORBIT REFRESHERS PEPERMINT DRAŽEJE 15,6g", (15.6, "g")),
    ("Gavrilović namaz s kom.zimske salame100g", (100, "g")),
    ("350G GAVRILOVIĆ TIROLSKA KOB", (350, "g")),
    ("670G ARO MIJEŠANA SALATA", (670, "g")),
    ("UMAK PIZZA RAJČICA CLASIC 4100G MUTTI", (4100, "g")),
    ("200GR SILMA ČVARCI", (200, "g")),
    ("ČUNGA LUNGA LIZALICA FACE 2 8,5 GR.", (8.5, "g")),
    ("ŠLAG PJENA 36 g 3+1GR PODRAVK", (36, "g")),
    # točka iz kratice nije decimalni separator
    ("KRUH MANJE UG.190 g BEZ GLUTEN BALVITE", (190, "g")),
    ("ČOK.ORAN.BIS.160 g J IMMY", (160, "g")),
    ("MAHUNE LIM.420 g PODRAVKA", (420, "g")),
    ("Nutrino Kaša voć.jab.,man.,pap.,ban.100g", (100, "g")),
    # l / ml / dl
    ("SOK PAGO JABUKA 0,20 L STAKLO JAMNI", (200, "ml")),
    ("NAT.SOK MRK.I JAB.0,72L 100% BEZ.Š.", (720, "ml")),
    ("KARLOVAČKO RADLER LIMENKA 0,5L (24)", (500, "ml")),
    ("PIVO PAN 0,5 l LIM", (500, "ml")),
    ("DET COCCOLINO ULTRA CARE 1.48 L 37PR", (1480, "ml")),
    ("*SEMISWEET RED GATO NEGRO 0.75L POLUSLATKO -12/1-", (750, "ml")),
    ("N-SOK BRAVO 2.00L JABUKA 50% NEKTAR", (2000, "ml")),
    ("Palmolive Men gel za tuš.Pure arc750 ml", (750, "ml")),
    ("DET. LIKVI UL. ORIGINAL 900 ml", (900, "ml")),
    ("ČAŠA PROZIRNA 2dl 20KOM BRODPLAST", (200, "ml")),
    ("ČAŠA 0,5dl PROZIRNA 20/1", (50, "ml")),
    ("VODA JANA 0,5L", (500, "ml")),
    # postotak se ne smije pročitati kao gramatura
    ("PIVO STAROPRAMEN 0,0% 0,5L LIMENKA", (500, "ml")),
    ("MLIJEKO TRAJNO 1,5%MM 1l ALPSKO", (1000, "ml")),
    ("Maraska Liker voćni Maraschino 32% 0,7 L", (700, "ml")),
    ("DUKAT TRAJNO MLIJEKO 2.8% 0.2 L", (200, "ml")),
    # višestruka pakiranja
    ("KEKS PLAZMA 2X300 G BAMBI", (600, "g")),
    ("DOMESTOS WC OSVJEZIVAC 2X40 G DUOPACK PINE 1+1", (80, "g")),
    (".PIVO BEST BRAU LAGER 8x500ml", (4000, "ml")),
    ("ČAJ LEMON&GINGER 40G (20X2G)", (40, "g")),
    ("30G*20 PLAZMA STICKS KIKIRIKI-KARAMELA", (600, "g")),
    # oznaka dobi na dječjoj hrani nije gramatura
    ("KAŠICA HIPP OBROK PURETINA+1g 220g", (220, "g")),
    ("babylove EKO vafli 1G+ borov. 30 g", (30, "g")),
    ("BRAŠNO KARLA GLATKO T-550 1kg+DIGO KVASAC U LIMENCI", (1000, "g")),
    # bruto uz ocijeđenu masu (ocijeđena se vraća zasebno, vidi test_parse_drained)
    ("GRAH ŠARENI 400g/240g O.M. CANNELLINI", (400, "g")),
    ("KOMPOT BRESKVA FRUTTAMO 820g/470g", (820, "g")),
    ("KRASTAVCI 6-9 cm 1580g ZORELA ocijeđene mase 820g", (1580, "g")),
    ("TUNA KOMADI GIANA 185g BILJNO ULJE - ocijeđ mase 130g", (185, "g")),
    ("SALATA ČETIRI GRAHA 425g GIANA - ocijeđ mase240g", (425, "g")),
    # komadi
    ("ULOŠCI HIGIJENSKI NORMAL PLUS DUO 20 kom ALWAYS", (20, "kom")),
    ("Zubobran inter.čet. perf.smile 1 kom.", (1, "kom")),
    ("Vileda spužvasta krpa 10kom", (10, "kom")),
    # ništa: bez gramature, "N/1" pakiranja, promjenjiva težina (cca), dimenzije
    ("BANANA", None),
    ("AVOKADO KOM SNIŽENJE", None),
    ("BRAŠNO GLATKO T-550 1/1", None),
    ("BRAŠNO PŠENIČNO T-550 GLATKO 5/1 PODRAVKA (1PAL=112KOM)", None),
    ("VILEDA SPUŽ. KRPA PRO CLEAN 3/1", None),
    ("MESO SRNE ZA GULAŠ CCA 1 kg", None),
    ("Dimljena svinjska rebra, cca. 700g", None),
    ("DEKA DJ. JEDNOBOJNA 110X140 CM WIM", None),
    ("LAGUNA MALVAZIJA 0,187 (20)", None),
    ("JAJA 10/1 L TOM CRO", None),  # L je veličina jaja, a "10/1" broj komada
    # jedinica zalijepljena za sljedeću riječ (Korak 2D): mala jedinica pa veliko slovo
    ("ULTRA PENNE RIG.500gPAGANI", (500, "g")),
]


@pytest.mark.parametrize("name,expected", REAL_NAMES)
def test_parse_pack_real_names(name, expected):
    got = parse_pack(name)
    if expected is None:
        assert got is None
    else:
        assert got == (pytest.approx(expected[0]), expected[1])


def test_enough_real_names():
    assert len(REAL_NAMES) >= 50


@pytest.mark.parametrize(
    "unit,expected",
    [
        ("80g", (80, "g")),
        ("10x1kg", (10000, "g")),
        ("1,8l", (1800, "ml")),
        ("4x50g", (200, "g")),
        ("1komad", (1, "kom")),
        ("123g,200g,77g", None),  # miks varijanti
        ("KG", None),
        (None, None),
    ],
)
def test_parse_pack_unit_field(unit, expected):
    got = parse_pack_unit_field(unit)
    assert got == (None if expected is None else (pytest.approx(expected[0]), expected[1]))


@pytest.mark.parametrize(
    "unit,quantity,expected",
    [("ko", "0.20 kg", "kg"), ("KOM", "100 G", "kg"), ("L", "1.000 L", "l"), ("kg", "1", "kg"),
     ("KILOGRAM", None, "kg"), ("KOM", "1", None), (None, None, None)],
)
def test_unit_hint(unit, quantity, expected):
    assert unit_hint(unit, quantity) == expected


def test_gtin_ok():
    assert gtin_ok("3850104223624")
    assert not gtin_ok("3850104223625")
    assert gtin_ok("80511717")  # EAN-8
    assert not gtin_ok("11210000018")  # 11 znamenki nije GTIN


@pytest.mark.parametrize(
    "barcode,expected",
    [
        ("3850104223624", ("3850104223624", True, True)),
        ("11210000018", ("0011210000018", True, True)),  # UPC-A bez vodeće nule
        ("011210000018", ("0011210000018", True, True)),  # UPC-A
        ("00011210000018", ("0011210000018", True, True)),  # GTIN-14
        ("80511717", ("80511717", True, True)),
        ("2111111012450", ("2111111012450", True, False)),  # in-store (vaga)
        ("20342890", ("20342890", True, False)),  # EAN-8 ograničene upotrebe
        ("3850104223625", (None, False, False)),  # kriva kontrolna znamenka
        ("290318", (None, False, False)),  # PLU šifra
        ("ktc:00032", (None, False, False)),
        ("ribola: 070703", (None, False, False)),
        (None, (None, False, False)),
    ],
)
def test_normalize_ean(barcode, expected):
    assert normalize_ean(barcode) == expected


def test_norm_text():
    assert norm_text("BRAŠNO PŠENIČNO T-550") == "brasno psenicno t 550"
    assert norm_text("Đakovo") == norm_text("Djakovo") == norm_text("DAKOVO") == "dakovo"
    assert norm_text("ČEVAPČIĆI, Žuti") == "cevapcici zuti"
    assert norm_text(None) is None


def test_city():
    assert canonical_city("Sesvete") == "Zagreb"
    assert canonical_city("ZAGREB-DUBRAVA") == "Zagreb"
    assert canonical_city("Kaštel Stari") == "Kaštela"
    assert canonical_city("Osijek") == "Osijek"


def test_date_hr():
    assert date_hr(date(2026, 10, 19)) == "19.10.2026."
    assert date_hr(date(2026, 3, 5)) == "05.03.2026."
