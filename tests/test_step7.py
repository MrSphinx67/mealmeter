"""Korak 7: mljeveno meso (nazivi sastojaka i proizvoda, vrsta) i upute poslužitelja za stvarne razgovore."""

import json
import os
from pathlib import Path

import pytest

from mealmeter.basket import resolve_name
from mealmeter.staples import extract_attributes, load_staples, name_match

S = load_staples()


# --- 0. mljeveno meso ----------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,vrsta", [
    ("mljeveno meso junetina", "junece"),
    ("juneće mljeveno meso", "junece"),
    ("mljevena junetina", "junece"),
    ("junetina mljevena", "junece"),
    ("mljeveno juneće", "junece"),
    ("mljeveno juneće meso", "junece"),
    ("mljeveno goveđe meso", "junece"),
    ("faširano juneće", "junece"),
    ("mljevena svinjetina", "svinjsko"),
    ("svinjsko mljeveno meso", "svinjsko"),
    ("miješano mljeveno meso", "mijesano"),
    ("mljeveno mješano meso", "mijesano"),
    ("faširano", None),  # vrsta nije navedena: zadano miješano (default_preference)
    ("mljeveno meso", None),
])
def test_minced_meat_names(name, vrsta):
    st, attrs = resolve_name(name)
    assert st.key == "mljeveno_meso"
    assert attrs.get("vrsta") == vrsta
    if vrsta is None:
        assert st.default_preference["vrsta"][0] == "mijesano"


@pytest.mark.parametrize("name,key", [
    ("junetina", "junetina"), ("mljevena paprika", "mljevena_paprika"), ("mljeveni papar", "papar"),
])
def test_other_names_unchanged(name, key):
    assert resolve_name(name)[0].key == key


@pytest.mark.parametrize("name,vrsta", [
    ("JUN MLJEV MESO 850g MA PIK VRBOVEC", "junece"),  # Konzum: prije zadano miješano
    ("JUNETINA MLJEVENA", "junece"),  # Konzum: prije nije bilo namirnica
    ("JUN MLJEVENA 540G (MA)", "junece"),
    ("MLJEVENA JUN. 450 g LIPI BOKUN", "junece"),  # Tommy
    ("Juneći but mljeveni", "junece"),  # Spar
    ("MLJEVENO MJEŠANO MESO", "mijesano"),
    ("MLJEVENO MIJEŠ. 450g BOKUN GUŠTA", "mijesano"),
    ("MESO MLJ. MIJ. (SVI+JUN) PIK 850 g", "mijesano"),
    ("MESO MIJEŠANO 1 kg MLJEVENO PAK", "mijesano"),
    ("MLJEVENO JUNEĆE I SVINJSKO MESO", "mijesano"),
    ("SV.MLJ.MESO 540g PIK", "svinjsko"),
    ("SV MLJEV MESO 850G MA PIK VRBOVEC (6)", "svinjsko"),  # Roto: prije miješano
    ("Svinjska lopatica mljevena", "svinjsko"),
    ("MLJEVENA TELETINA", "telece"),
])
def test_minced_meat_products(name, vrsta):
    st = S["mljeveno_meso"]
    assert name_match(st, name) == "match"
    assert extract_attributes(st, name)["vrsta"] == vrsta


@pytest.mark.parametrize("name", [
    "MJEŠ. KURK. MLJ.35 gKOTANYI", "KLC.Mješavina začina za gulaš mljev.30g", "Grčka pita s mljevenim mesom",
    "ŽELAT DR.OE 10 g GOVEĐA MLJEVENA", "KEKS MLJEVENI 300 g SMIJEŠAK", "MJEŠAVINA ŽITARICA MLJEVENA 25 kg TSH",
])
def test_minced_meat_not_products(name):
    assert name_match(S["mljeveno_meso"], name) is None


GOLD = Path(__file__).parent / "golden" / "basket_bolonjez_junece_osijek.json"


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_bolonjez_junece():
    out = json.loads(GOLD.read_text(encoding="utf-8"))
    assert not out["unmatched"]
    rows = out["comparison"] + out["more_chains"]
    assert {"konzum", "lidl", "kaufland", "plodine", "spar"} <= {r["chain"] for r in rows}
    meat = [i for i in out["best_store"]["items"] if i["staple"] == "mljeveno_meso"]
    assert meat and meat[0]["attributes"]["vrsta"] == "junece"


# --- 1.-6. upute poslužitelja ----------------------------------------------------------------------------------

def _instructions() -> str:
    from mealmeter.server import INSTRUCTIONS

    return INSTRUCTIONS


def test_rule_call_again():
    text = _instructions()
    for phrase in ("Za svako novo jelo, promjenu broja osoba, sastojaka, grada ili trgovine ponovno pozovi plan_basket",
                   "nikad ne\n   procjenjuj cijene niti ih prenosi iz ranijeg odgovora",
                   "Every new dish or change of servings, ingredients, city or store: call plan_basket again",
                   "never estimate or reuse earlier prices"):
        assert phrase in text, phrase


def test_rule_when_to_ask():
    text = _instructions()
    rule1 = text.split("\n1. ", 1)[1].split("\n2. ", 1)[0]
    for phrase in ("samo recept, bez pitanja o cijeni ili kupnji", "jednu kratku rečenicu",
                   "koliko košta i gdje to može kupiti u svom gradu", "Ne zovi plan_basket dok ne pristane"):
        assert phrase in rule1, phrase
    rule2 = text.split("\n2. ", 1)[1].split("\n3. ", 1)[0]
    for phrase in ("Kad pita koliko košta ili gdje kupiti", "JEDNOJ poruci", "samo ono što još ne znaš", "grad;",
                   "što već ima doma",
                   '"U koju trgovinu ideš (može i adresa ili kvart), ili da usporedim sve u\n   gradu?"',
                   "nadjev ili dodatke kad je relevantno", "Ne pretpostavljaj što korisnik\n   ima doma",
                   "izričito traži brz odgovor bez pitanja", "navedi\n   pretpostavke i ponudi ponovni izračun",
                   "Never assume what is at home"):
        assert phrase in rule2, phrase
