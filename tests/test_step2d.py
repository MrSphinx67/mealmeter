"""Korak 2D: pripadnost grupa, zadani izbori, mjere."""

import duckdb
import pytest

from mealmeter.search import find_products
from mealmeter.staples import build_staple_groups, load_staples

S = load_staples()


# --- 1. pripadnost grupe (EAN) namirnici ------------------------------------------------

def _mini_groups(rows):
    """build_staple_groups nad malom bazom: rows = [(chain, ean, name_norm, excluded | None)]."""
    c = duckdb.connect()
    c.execute("CREATE SCHEMA clean")
    c.execute("""CREATE TABLE clean.products (chain VARCHAR, product_id VARCHAR, ean_norm VARCHAR,
                 ean_global BOOLEAN, name_norm VARCHAR)""")
    c.execute("""CREATE TABLE clean.product_staples (chain VARCHAR, product_id VARCHAR, staple VARCHAR,
                 excluded BOOLEAN, drop_reason VARCHAR)""")
    c.execute("""CREATE TABLE clean.product_attrs (chain VARCHAR, product_id VARCHAR, staple VARCHAR,
                 attr VARCHAR, value VARCHAR, how VARCHAR)""")
    for i, (chain, ean, name, excluded) in enumerate(rows):
        c.execute("INSERT INTO clean.products VALUES (?, ?, ?, true, ?)", [chain, str(i), ean, name])
        if excluded is not None:
            c.execute("INSERT INTO clean.product_staples VALUES (?, ?, 'x', ?, NULL)", [chain, str(i), excluded])
    build_staple_groups(c)
    return dict(c.execute("SELECT bkey, status FROM clean.staple_groups").fetchall())


def test_group_majority_rule():
    got = _mini_groups([
        ("a", "1", "masl ulje", False), ("b", "1", "masl ulje", False), ("c", "1", "brand", None),  # 2/3
        ("a", "2", "masl ulje", False), ("b", "2", "brand", None), ("c", "2", "brand", None),  # 1/3
        ("a", "3", "x", False), ("b", "3", "x", False), ("c", "3", "x", False), ("d", "3", "y", True),  # 25 % isklj.
        ("a", "4", "x", False), ("b", "4", "x", False), ("c", "4", "x", False), ("d", "4", "x", False),
        ("e", "4", "y", True),  # 20 % isključenog naziva: dopušteno
        ("a", "5", "y", True), ("b", "5", "brand", None),  # nijedan naziv ne prolazi
    ])
    assert got == {"1": "member", "2": "ambiguous", "3": "ambiguous", "4": "member", "5": "excluded"}


def test_turkey_mince_not_default_mince(con):
    # "PUREĆE MLJEVENO MESO" je u svim lancima pureće, pa grupa nije zadano miješano meso
    res = find_products(ingredient="mljeveno_meso", con=con)
    assert all("pure" not in r["name"].lower() for r in res)
    res = find_products(ingredient="mljeveno_meso", attributes={"vrsta": "purece"}, con=con)
    assert res and res[0]["attributes"]["vrsta"] == "purece"


def test_group_attrs_prefer_name(con):
    rows = con.execute("""SELECT value, how FROM clean.staple_group_attrs
                          WHERE staple = 'mljeveno_meso' AND attr = 'vrsta' AND bkey = '3850339413043'""").fetchall()
    assert rows == [("purece", "name")]


# --- 2. isključenja i gramatura ----------------------------------------------------------

@pytest.mark.parametrize("key,name", [
    ("maslinovo_ulje", "KUPUS KIS MASL ULJE ČEŠNJAK 250g"),
    ("maslinovo_ulje", "PREMIUM SAL. KIS.KUPUS S EX.DJE. MASL. ULJEM I CES. 250G"),
    ("parmezan", "RIBAN.PARMEZAN GREEN VIE 100 g"),
    ("mozzarella", "MOZZARELLA VEGAN 200 g"),
    ("tvrdi_sir", "SIR TVRDI BILJNI 200 g"),
    ("maslac", "BILJNA ZAMJENA ZA MASLAC 250 g"),
    ("grah", "GRAH S KOB.SMRZ."),
    ("slanutak", "SIPA SA SLANUTKOM SMRZ."),
    ("grasak", "GRAŠAK I SIPA 400 g"),
    ("grah", "BRUDET GRAH 400 g"),
    ("leca", "LEĆA ORZO 300 g"),
])
def test_point2_exclusions(key, name):
    from mealmeter.staples import name_match

    assert name_match(S[key], name) == "excluded"


def test_felix_only_pet_food():
    from mealmeter.staples import name_match

    assert name_match(S["kecap"], "KETCHUP FELIX BLAGI 500g") == "match"
    assert name_match(S["tuna"], "HRANA ZA MAČKE FELIX TUNA 85 g") == "excluded"


def test_kupus_and_vegan_parmezan_not_in_default(con):
    names = [r["name"] for r in find_products(ingredient="maslinovo_ulje", limit=100, con=con)]
    assert not any("KUPUS" in n for n in names)
    names = [r["name"] for r in find_products(ingredient="parmezan", limit=100, con=con, include_ambiguous=True)]
    assert not any("BILJ" in n.upper() or "GREEN" in n.upper() for n in names)


@pytest.mark.parametrize("name,pack", [
    ("PERŠIN KOR LIS 250 gVOĆARNA STUDENAC", (250, "g")),
    ("KIS.KUP. ČEŠNJ.250 gMADIG", (250, "g")),
    ("5 LIMUNA", None),  # bez razlike u veličini slova jedinica se ne odvaja
])
def test_pack_glued_unit(name, pack):
    from mealmeter.normalize import parse_pack

    assert parse_pack(name) == pack


# --- 3. mljeveno meso -----------------------------------------------------------------

def _row(bkey, price, grams=500, **kw):
    return {"bkey": bkey, "price_eff": price, "pack_amount": grams, "pack_unit": "g", "n_units": None,
            "assumed_g": None, "drained_amount": None, "price_per_unit": price / grams * 1000, "per_unit": "kg",
            "clearance": False, "price_suspect": False, "pack_confidence": "high", "data_quality": "ok",
            "variable_weight": False, **kw}


@pytest.mark.parametrize("available,expected", [
    ({"m": "mijesano", "j": "junece", "s": "svinjsko"}, "m"),  # miješano iako je skuplje
    ({"j": "junece", "s": "svinjsko"}, "j"),
    ({"s": "svinjsko", "p": "purece"}, "s"),
])
def test_minced_meat_preference(available, expected):
    from mealmeter.basket import Need, _choose_preferred

    prices = {"m": 6.0, "j": 5.0, "s": 4.0, "p": 3.0}
    rows = [_row(k, prices[k]) for k in available]
    need = Need({"name": "mljeveno meso"}, S["mljeveno_meso"], 500, "g")
    pick = _choose_preferred(rows, need, S["mljeveno_meso"].default_preference, {"vrsta": available})
    assert pick["bkey"] == expected


def test_minced_meat_find_default_values(con):
    res = find_products(ingredient="mljeveno_meso", limit=50, con=con)
    assert all(r["attributes"].get("vrsta") in ("mijesano", "junece", "svinjsko") for r in res)


# --- 4. pileća prsa: stanje ------------------------------------------------------------------

@pytest.mark.parametrize("name,stanje", [
    ("PILEĆI FILE SMRZNUTI", "smrznuto"), ("PILEĆI FILE BRAZILSKI SMRZNUTI", "smrznuto"),
    ("PILEĆI FILE SOLJENI 6X2 BRAZIL", "smrznuto"), ("PILEĆA PRSA LEDO 1 kg", "smrznuto"),
    ("PILEĆI FILE FROZEN 1kg", "smrznuto"), ("PRSA PILEĆA K PLUS BEZ KOŽE", "svjeze"),
])
def test_chicken_stanje(name, stanje):
    from mealmeter.staples import extract_attributes

    assert extract_attributes(S["pileca_prsa"], name)["stanje"] == stanje


def test_chicken_rules(con):
    st = S["pileca_prsa"]
    assert st.default_attributes == {"stanje": "svjeze"}
    from mealmeter.staples import name_match

    assert name_match(st, "PILEĆA PRSA JELI GAVRILOVIĆ") == "excluded"
    lo, hi, src = con.execute("SELECT ppu_min, ppu_max, range_source FROM clean.staple_rules WHERE staple = 'pileca_prsa'").fetchone()
    assert (lo, hi, src) == (2, 20, "manual")  # najširi raspon; po proizvodu vrijedi raspon stanja

# --- 5. luk ----------------------------------------------------------------------------

@pytest.mark.parametrize("name,vrsta", [
    ("LUK SREBRENAC (10)", "srebrenac"),
    ("LUK LJUBIČ./BIJELI ZA GASTRO 1 kg", "ljubicasti"),
    ("KAPULA ŽUTA (CRV.LUK)", "zuti"),
    ("LUK CRVENI", "crveni"),
    ("LUK CRVENI SLATKI 50-70", "slatki"),
    ("LUK BORETTANE 250 g", "borettan"),
    ("KAPULA", "obicni"),
    ("LUK MLADI VEZICA", "mladi"),
])
def test_onion_vrsta(name, vrsta):
    from mealmeter.staples import extract_attributes

    assert extract_attributes(S["luk"], name)["vrsta"] == vrsta


def test_onion_default_and_garlic():
    from mealmeter.staples import name_match

    st = S["luk"]
    excluded = {v for a, v in st.default_exclude_variants if a == "vrsta"}
    assert {"srebrenac", "ljubicasti", "mladi", "slatki", "borettan", "perlice"} <= excluded
    assert not {"crveni", "zuti", "obicni"} & excluded
    assert name_match(st, "LUK BIJELI RFS") == "excluded"  # češnjak
    assert name_match(st, "LUK LJUBIČ./BIJELI ZA GASTRO 1 kg") == "match"


def test_onion_rukavac_assumed_500g():
    st = S["luk"]
    assert st.assumed_pack_g == 500 and st.assumed_pack_regex
