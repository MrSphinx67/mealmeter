"""Ispravci rječnika nakon ručnog pregleda (Korak 2A2). Svi nazivi su stvarni, iz arhive 2026-10-19."""

import pytest

from mealmeter.staples import extract_attributes, load_staples, name_match

S = load_staples()


# --- 1. pogrešna isključenja -------------------------------------------------

@pytest.mark.parametrize("key,name", [
    ("brasno", "BRAŠ.PŠE.T-1100 PODRAVKA 1 kg"),  # "PŠE." više ne pogađa pse\b (hrana za pse)
    ("brasno", "BRAŠNO PŠE. T-850 1 kg"),
    ("sol", "SOL KUHINJSKA SITNA MORSKA KUTIJA 1KG, SOLANA PAG"),
    ("sol", "SOL KRUPNA KUTIJA 1 kg"),
    ("margarin", "MARGARIN ZA KOLAČE 250g BAKINA KUHINJA"),
    ("jaja", "JAJA M 10/1 PODN.UZ. GALA"),
    ("riza", "RIŽA DUGO ZRNO PARBOIL.500g BEN'S"),
    ("riza", "RIŽA ZLATNO POLJE ZA DOMAĆA JELA 1 kg PODR"),
    ("kakao", "KAKAO U PRAHU 100g KRAŠ"),
    ("dodatak_jelima", "VEGETA NATUR VR 150g PODRAVKA"),
    ("persin", "PERŠIN KORIJEN LIST 300g"),
    ("persin", "PERSIN LIST BOC.10 G PLODINE"),
    ("tvrdi_sir", "SIR GAUDA RIBANI 200g VINDIJA"),
])
def test_wrong_exclusions_removed(key, name):
    assert name_match(S[key], name) == "match"


@pytest.mark.parametrize("key,name", [
    ("junetina", "TOMI GOVEDINA 1200 g ZA PSE"),  # "za pse" i dalje isključuje hranu za pse
    ("junetina", "Purina One hrana za pse govedina"),
])
def test_dog_food_still_excluded(key, name):
    assert name_match(S[key], name) == "excluded"


@pytest.mark.parametrize("key,name", [
    ("dodatak_jelima", "VEGETA TWIST ZA KRUMPIR 20G"),
    ("dodatak_jelima", "VEGETA GRILL ZAČIN 50G"),
    ("dodatak_jelima", "VEGETA MAESTRO PAPAR 30G"),
])
def test_vegeta_variants_excluded(key, name):
    assert name_match(S[key], name) == "excluded"


@pytest.mark.parametrize("key,name,expected", [
    ("brasno", "BRAŠ.PŠE.T-1100 PODRAVKA 1 kg", {"vrsta": "psenicno", "oznaka": "t1100"}),
    ("brasno", "BRAŠNO PŠE. T-850 1 kg", {"vrsta": "psenicno", "oznaka": "t850"}),
    ("persin", "PERŠIN KORIJEN S-BUDGET 250 g", {"dio": "korijen"}),
    ("persin", "PERSIN LIST BOC.10 G PLODINE", {"dio": "list"}),
    ("tvrdi_sir", "SIR GAUDA RIBANI 200g VINDIJA", {"oblik": "ribani", "vrsta": "gauda"}),
    ("tvrdi_sir", "SIR TVRDI RIBANAC 40g DUKAT (25)", {"oblik": "ribani"}),
])
def test_new_attributes(key, name, expected):
    assert expected.items() <= extract_attributes(S[key], name).items()
