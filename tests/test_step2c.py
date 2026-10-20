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
