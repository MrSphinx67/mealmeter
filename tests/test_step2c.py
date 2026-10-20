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
