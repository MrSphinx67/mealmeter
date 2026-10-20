"""Korak 2C, točke 1-11: ispravci rječnika namirnica."""

import pytest

from mealmeter.staples import extract_attributes, load_staples, name_match

S = load_staples()


# --- 1. jaja -------------------------------------------------------------------

@pytest.mark.parametrize("name,uzgoj", [
    ("N-JAJA LUKAČ A KLASA 10KOM RAZRED M KAVEZNI UZGOJ", "kavezni"),
    ("Gala Jaja svj.Aklas.Mraz.podni uzgoj10/1", "podni"),
    ("JAJA SLOBODNI UZGOJ M 10/1", "slobodni"),
    ("EKO JAJA SLOBODNI UZGOJ 6/1", "bio"),
    ("SVJEŽA JAJA RAZL. VEL. BIO 6/1", "bio"),
    ("JAJA SPAR M RAZRED 6/1", "nepoznato"),
])
def test_egg_uzgoj(name, uzgoj):
    assert extract_attributes(S["jaja"], name)["uzgoj"] == uzgoj


@pytest.mark.parametrize("name", ["FOLIJA ZA JAJA TERMOSKUPLJAJUĆA", "JAJE STOLICA RATAN CRNA",
                                  "GLAZBENO JAJE", "IGR. JAJE DINOSAUR", "OBUĆA JAJE"])
def test_egg_nonfood_excluded(name):
    assert name_match(S["jaja"], name) in ("excluded", None)


# --- 2. zadane varijante -----------------------------------------------------------

@pytest.mark.parametrize("key,name,attr,value", [
    ("brasno", "BRAŠNO GLATKO T-550 1 kg", "vrsta", "psenicno"),
    ("brasno", "BRAŠNO HELJDINO 500 g", "vrsta", "heljdino"),
    ("brasno", "BRAŠNO KUKURUZNO 1 kg", "vrsta", "kukuruzno"),
    ("secer", "ŠEĆER 1 kg", "vrsta", "bijeli"),
    ("secer", "ŠEĆER U PRAHU 500 g", "vrsta", "u_prahu"),
    ("ulje", "ULJE OMEGOL 1L ZVIJEZDA", "vrsta", "omegol"),
    ("ulje", "ULJE MEDITERAN 1 L ZVIJEZDA", "vrsta", "mediteran"),
    ("ulje", "ULJE SUNCOKRETOVO HLADNO PREŠANO 1 L", "presanje", "hladno"),
    ("rajcica", "Rajcica koktel 500g", "vrsta", "cherry"),
    ("rajcica", "RAJČICA CHERRY DATERINO 500g SG", "vrsta", "datterino"),
    ("rajcica", "RAJČICA HARMONY 500 g", "vrsta", "harmony"),
    ("rajcica", "RAJČICA CAMPARI 400g", "vrsta", "campari"),
    ("riza", "Riso Scotti riža oro dugog zrna 1kg", "vrsta", "dugo_zrno"),  # "oro" nije parboiled
])
def test_default_variant_attributes(key, name, attr, value):
    assert extract_attributes(S[key], name)[attr] == value


@pytest.mark.parametrize("key,variants", [
    ("brasno", {"vrsta=kukuruzno", "vrsta=pirovo", "vrsta=razeno", "vrsta=heljdino"}),
    ("secer", {"vrsta=u_prahu", "vrsta=kocke", "vrsta=smedi"}),
    ("ulje", {"vrsta=omegol", "vrsta=mediteran", "presanje=hladno"}),
    ("rajcica", {"vrsta=cherry", "vrsta=datterino", "vrsta=harmony", "vrsta=campari"}),
])
def test_default_exclude_variants(key, variants):
    assert variants <= {f"{a}={v}" for a, v in S[key].default_exclude_variants}


def test_riza_oro_alone_not_parboiled():
    assert "vrsta" not in extract_attributes(S["riza"], "RIŽA ORO 1 kg")


def test_riza_paraboiled_typo():
    assert extract_attributes(S["riza"], "RIZA PARABOILED DUGO ZRNO VRECICA 500 G BENS")["vrsta"] == "parboiled"


# --- 4. pileća prsa ------------------------------------------------------------------

@pytest.mark.parametrize("name", ["PILEĆA PRSA JELI GAVRILOVIĆ", "PILEĆA PRSA 350 g JE LI GAVRILOVIĆ"])
def test_chicken_jeli_temporarily_excluded(name):
    assert name_match(S["pileca_prsa"], name) == "excluded"


def test_chicken_range():
    assert S["pileca_prsa"].plausible_per_unit == (5, 20)
    assert name_match(S["pileca_prsa"], "PILEĆI FILE 500 g") == "match"


# --- 6. sol ----------------------------------------------------------------------

def test_sol_soljenka_is_salt():
    assert name_match(S["sol"], "SOL MORSKA SITNA 250G SOLJENKA") == "match"
    assert S["sol"].require_pack == ("soljenk",)


def test_sol_soljenka_without_pack_dropped(tmp_path):
    """Soljenka bez gramature (prazna posuda) ispada iz soli, a ona s gramaturom ostaje."""
    import duckdb

    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "sol.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'T1', 'konzum:T1', 'SOL MORSKA SITNA 250G SOLJENKA', 'HRANA', 'KOM'),
                 ('konzum', 'T2', 'konzum:T2', 'SOL SOLJENKA STAKLENA S POKLOPCEM', 'HRANA', 'KOM')""")
    build_clean(c)
    got = dict(c.execute("""SELECT product_id, coalesce(drop_reason, 'ok') FROM clean.product_staples
                            WHERE staple = 'sol' AND product_id IN ('T1', 'T2')""").fetchall())
    assert got == {"T1": "ok", "T2": "bez_gramature"}


# --- 7. mlijeko ------------------------------------------------------------------

def test_milk_substitutes():
    st = S["mlijeko"]
    assert st.default_attributes == {"vrsta": "trajno", "mast": "2.8"}
    assert st.accepted_values("mast", "2.8") == ("2.8", "3.2", "3.5", "3.8")
    assert st.accepted_values("mast", "3.8")[0] == "3.8"
    assert st.accepted_values("mast", "1.5") == ("1.5",)
    assert st.accepted_values("vrsta", "trajno") == ("trajno",)  # svježe i trajno nisu zamjenjivi


@pytest.mark.parametrize("name,vrsta", [
    ("MLIJEKO TR LAG JUTRO 1.5% 1L DUKAT", "trajno"),
    ("MLIJEKO SV.3,2% Z BREG.1,75 L", "svjeze"),
    ("MLIJEKO 3,2%MM 1L SVJEŽE DUKAT", "svjeze"),
])
def test_milk_vrsta(name, vrsta):
    assert extract_attributes(S["mlijeko"], name)["vrsta"] == vrsta


@pytest.mark.parametrize("name", ["PALAČINKE SA JAJIMA I MLIJEKOM", "ACIDOFILNO MLIJEKO 3,2% 1KG BOCA PET VINDIJA",
                                  "MLIJEKO KIS. ČVRSTO 3,2% 900 g", "MLIJEKO PROTEIN 0,4% 1L DUKAT",
                                  "MLIJEKO ČOKOL. TE Z BREG.0,5 L"])
def test_milk_wrong_hits(name):
    assert name_match(S["mlijeko"], name) == "excluded"


def test_basket_milk_returns_vrsta_and_mast(con):
    from mealmeter.basket import plan_basket

    res = plan_basket([{"name": "mlijeko", "amount": 0.5, "unit": "l"}], "Osijek", con=con)
    ing = res["ingredients"][0]
    assert ing["applied_attributes"] == {"vrsta": "trajno", "mast": "2.8"}
    assert ing["accepted_values"] == {"mast": ["2.8", "3.2", "3.5", "3.8"]}
    item = res["best_store"]["items"][0]
    assert item["attributes"]["vrsta"] == "trajno" and item["attributes"]["mast"] in ("2.8", "3.2", "3.5", "3.8")


# --- 8. peršin i svježe bilje ----------------------------------------------------------

def test_persin_kg_pantry():
    from mealmeter.basket import IngredientError, to_base

    st = S["persin"]
    assert st.unit == "kg" and st.pantry and st.compare_unit == "kg"
    assert to_base(20, "g", st)[:2] == (20, "g")
    with pytest.raises(IngredientError):  # vezica bez mase se ne pretvara u grame
        to_base(1, "vezica", st)


# --- 9. pretvorba mjera ------------------------------------------------------------

@pytest.mark.parametrize("amount,unit,staple,expected", [
    (1, "žlica", "brasno", (8.25, "g")),
    (2, "žličice", "sol", (12.0, "g")),
    (1, "šalica", "secer", (212.5, "g")),
    (1, "šalicu", "riza", (212.5, "g")),
    (1, "Čaša", "mlijeko", (200, "ml")),
    (2, "dcl", "ulje", (200, "ml")),
    (1, "prstohvat", "sol", (0.6, "g")),
    (2, "žlice", "maslac", (28.5, "g")),
    (1, "žlica", "med", (15, "g")),  # bez gustoće: 1 g/ml
])
def test_convert(amount, unit, staple, expected):
    from mealmeter.units import convert

    qty, base, warnings = convert(amount, unit, S[staple])
    assert (round(qty, 3), base) == expected and "procjena" in warnings[0]


def test_convert_errors():
    from mealmeter.units import convert

    with pytest.raises(ValueError):
        convert(1, "žlica", S["jaja"])  # komadi
    with pytest.raises(ValueError):
        convert(1, "lonac", S["brasno"])


def test_units_all_estimates():
    import yaml

    from mealmeter.units import UNITS_PATH

    raw = yaml.safe_load(UNITS_PATH.read_text(encoding="utf-8"))
    assert all(m["estimate"] for m in raw["measures"].values())
    assert set(raw["densities"]) == {"brasno", "secer", "sol", "ulje", "mlijeko", "maslac", "riza"}
    assert all(d["estimate"] for d in raw["densities"].values())


def test_basket_accepts_measures(con):
    from mealmeter.basket import plan_basket

    res = plan_basket([{"name": "brašno glatko", "amount": 2, "unit": "šalica"},
                       {"name": "mlijeko", "amount": 1, "unit": "čaša"}], "Osijek", con=con)
    assert not res["unmatched"]
    amounts = {i["staple"]: (i["amount"], i["unit"]) for i in res["ingredients"]}
    assert amounts == {"brasno": (275.0, "g"), "mlijeko": (200.0, "ml")}


def test_to_base_grams_of_liquid_use_density():
    from mealmeter.basket import to_base

    qty, unit, warnings = to_base(103, "g", S["mlijeko"])
    assert (round(qty, 3), unit) == (100.0, "ml") and "1.03 g/ml" in warnings[0]
