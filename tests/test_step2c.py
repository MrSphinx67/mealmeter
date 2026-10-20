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
