"""Korak 9: izbor proizvoda iz stvarnog testa (bolonjez, Osijek, 27.10.2026.): zadano kravlji maslac i obične
mliječne namirnice; posebne vrste (kozje, ovčje, bivolje, bez laktoze, biljno, ghee) samo na zahtjev."""

import json
import os
from pathlib import Path

import duckdb
import pytest

from mealmeter.basket import plan_basket, resolve_name
from mealmeter.build import build_clean, load_raw
from mealmeter.staples import extract_attributes, load_staples, name_match
from tests.conftest import FIXTURE

S = load_staples()
GOLDEN = Path(__file__).parent / "golden"

# trgovine iz fixture-arhive: Konzum Osijek 0907, Lidl Osijek 105, Spar Osijek 87089
K, L, SP = ("konzum", "0907"), ("lidl", "105"), ("spar", "87089")
# posebna vrsta je uvijek jeftinija od obične, da se vidi da je zadano isključena, a ne samo skuplja
PRODUCTS = [
    ("M1", "MASLAC 250 g", {K: 2.49, L: 2.29}),
    ("M2", "MASLAC KOZJI 125 G EUROSER", {K: 0.99, L: 0.99}),
    ("M3", "Kfree.Maslac 82% m.m. bez laktoze 125g", {K: 0.89}),
    ("M4", "dmBio ghee maslac 180 g", {K: 0.79}),
    ("J1", "JOGURT TEKUĆI 2,8% 1 kg", {K: 1.29}),
    ("J2", "Alpro Soja jogurt 400g Natur bez šećera", {K: 0.69}),
    ("J3", "JOG.OD KOZ.MLIJ.GABRIEL 0,5 L", {K: 0.59}),
    ("Z1", "MOZZARELLA 125 G", {K: 1.19}),
    ("Z2", "SIR MOZZARELLA BUFALA 125 g", {K: 0.99}),
    ("Z3", "MOZZARELLA BEZ LAKTOZE 125 G LIVE LACTOSE FREE", {K: 0.89}),
    ("T1", "SIR GAUDA 250 g", {K: 2.49}),
    ("T2", "SIR TVRDI OVČJI 200g", {K: 1.99}),
    ("T3", "SIR TOPLJ LIST GOUDA DELISO 200g", {K: 1.49}),
    ("S1", "SIR SVJEŽI 250 G", {K: 0.99, SP: 1.09}),
    ("S2", "SIR SVJEŽI FREE FROM 250 g", {SP: 0.89}),
    ("S3", "Fruit King Pripravak od svj. sira", {SP: 0.79}),
    ("V1", "VRHNJE ZA KUHANJE 200 ml", {K: 0.99}),
    ("V2", "VRHNJE ZA KUH. BILJNO 500 ml HOPLA", {K: 0.89}),
    ("V3", "VRHNJE ZA KUH 200ml BEZ LAKT Z BR", {K: 0.79}),
    ("L1", "MLIJEKO TR 2.8% BEZ LAKT 1L LJUB MLEK", {K: 0.49}),
    ("L2", "KOZJE MLIJEKO TRAJNO 2,8% 1 L", {K: 0.45}),
]


@pytest.fixture(scope="module")
def con9(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s9") / "s9.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    rows, prices = [], []
    for pid, name, by_store in PRODUCTS:
        for chain, store in by_store:
            if (chain, pid) not in {(r[0], r[1]) for r in rows}:
                rows.append((chain, pid, f"{chain}:{pid}", name, "HRANA", "ko"))
            prices.append((chain, store, pid, by_store[(chain, store)]))
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES (?, ?, ?, ?, ?, ?)",
                  rows)
    c.executemany("INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, ?, DATE '2026-10-19')",
                  prices)
    build_clean(c)
    yield c
    c.close()


def pick(con, name: str, amount: float, unit: str, chain: str = "konzum") -> dict:
    """Odabrani proizvod u zadanom lancu (Osijek)."""
    out = plan_basket([{"name": name, "amount": amount, "unit": unit}], "Osijek", con=con,
                      store={"chain": chain, "address_contains": ""})
    assert not out["unmatched"], out["unmatched"]
    return out["best_store"]["items"][0]


# --- 1. mliječne namirnice: kravlje i obično zadano -------------------------------------------------------------

@pytest.mark.parametrize("name,staple,attrs", [
    ("maslac", "maslac", {}),
    ("kravlji maslac", "maslac", {}),
    ("kozji maslac", "maslac", {"vrsta_mlijeka": "kozje"}),
    ("maslac od kozjeg mlijeka", "maslac", {"vrsta_mlijeka": "kozje"}),
    ("maslac bez laktoze", "maslac", {"laktoza": "bez"}),
    ("ghee", "maslac", {"vrsta": "ghee"}),
    ("mlijeko bez laktoze", "mlijeko", {"laktoza": "bez"}),
    ("kozje mlijeko", "mlijeko", {"vrsta_mlijeka": "kozje"}),
    ("jogurt bez laktoze", "jogurt", {"laktoza": "bez"}),
    ("sojin jogurt", "jogurt", {"vrsta_mlijeka": "biljno"}),
    ("biljno vrhnje za kuhanje", "vrhnje_za_kuhanje", {"vrsta_mlijeka": "biljno"}),
    ("vrhnje za kuhanje bez laktoze", "vrhnje_za_kuhanje", {"laktoza": "bez"}),
    ("ovčji tvrdi sir", "tvrdi_sir", {"vrsta_mlijeka": "ovcje"}),
    ("svježi sir bez laktoze", "svjezi_sir", {"laktoza": "bez"}),
    ("mozzarella di bufala", "mozzarella", {"vrsta_mlijeka": "bivolje"}),
    ("bivolja mozzarella", "mozzarella", {"vrsta_mlijeka": "bivolje"}),
])
def test_dairy_names(name, staple, attrs):
    st, got = resolve_name(name)
    assert st.key == staple and got == attrs


@pytest.mark.parametrize("staple,name,attr,value", [
    ("maslac", "MASLAC KOZJI 125 G EUROSER", "vrsta_mlijeka", "kozje"),
    ("maslac", "Maslac od kozijeg mlijeka 125 g", "vrsta_mlijeka", "kozje"),
    ("maslac", "125G KOZJI MASLAC, SLANI", "vrsta_mlijeka", "kozje"),
    ("maslac", "Kfree.Maslac 82% m.m. bez laktoze 125g", "laktoza", "bez"),
    ("maslac", "800G GHEE MASLAC LA VACHE", "vrsta", "ghee"),
    ("maslac", "KLC.Maslac pročišćeni 500 g", "vrsta", "ghee"),
    ("mlijeko", "MLIJEKO TR 1.5% BEZ LAKT 1L LJUB MLEK", "laktoza", "bez"),  # prije: "bez laktoze" samo cijelom riječi
    ("jogurt", "JOG.OD KOZ.MLIJ.GABRIEL 0,5 L", "vrsta_mlijeka", "kozje"),
    ("jogurt", "EKO JOG.KOZ. 0,5 l CAPRA DOMESTICA", "vrsta_mlijeka", "kozje"),
    ("jogurt", "Alpro Soja jogurt 400g Natur bez šećera", "vrsta_mlijeka", "biljno"),
    ("jogurt", "dmBio jogurt od zobi 160 g T", "vrsta_mlijeka", "biljno"),
    ("tvrdi_sir", "SIR TVRDI OVČJI MANCHEGO CCA 3kg", "vrsta_mlijeka", "ovcje"),
    ("tvrdi_sir", "SIR TVRDI KOZJI CAPRODUR 280G VINDIJA", "vrsta_mlijeka", "kozje"),
    ("tvrdi_sir", "Sir Trapist, bez laktoze", "laktoza", "bez"),
    ("svjezi_sir", "SIR SVJEŽI KOZJA SKUTA CAPRA DOM", "vrsta_mlijeka", "kozje"),
    ("svjezi_sir", "SIR SVJEŽI FREE FROM 250 g", "laktoza", "bez"),
    ("mozzarella", "125G MOZZARELLA DI BUFALA DOP", "vrsta_mlijeka", "bivolje"),
    ("mozzarella", "Mozzarella od bivoljeg mlijeka", "vrsta_mlijeka", "bivolje"),
    ("mozzarella", "MOZZARELLA BEZ LAKTOZE 125 G LIVE LACTOSE FREE", "laktoza", "bez"),
    ("vrhnje_za_kuhanje", "VRHNJE ZA KUH. BILJNO 500 ml HOPLA", "vrsta_mlijeka", "biljno"),
    ("vrhnje_za_kuhanje", "VRH. ZA KUH. 250 ml ZOBENO APLRO", "vrsta_mlijeka", "biljno"),
    ("vrhnje_za_kuhanje", "Bio Soja vrhnje za kuhanje", "vrsta_mlijeka", "biljno"),
    ("slatko_vrhnje", "VRHNJE ZA ŠLAG BILJNO 1l DECORINO DUKAT", "vrsta_mlijeka", "biljno"),
])
def test_dairy_special_variants(staple, name, attr, value):
    assert extract_attributes(S[staple], name).get(attr) == value
    assert (attr, value) in S[staple].default_exclude_variants


@pytest.mark.parametrize("staple,name", [
    ("maslac", "MASLAC 250 g"), ("maslac", "DUKAT MASLAC 250 g"), ("jogurt", "JOGURT TEKUĆI 2,8% 1 kg"),
    ("mozzarella", "MOZZARELLA 125 G DOLINE"), ("tvrdi_sir", "SIR GAUDA 250 g"),
    ("vrhnje_za_kuhanje", "VRHNJE ZA KUHANJE 20 % 0,2 L VINDIJA"),
])
def test_dairy_plain_has_no_special_variant(staple, name):
    attrs = extract_attributes(S[staple], name)
    assert not {(a, v) for a, v in attrs.items()} & set(S[staple].default_exclude_variants)


@pytest.mark.parametrize("staple,name", [
    ("tvrdi_sir", "SIR TOPLJ LIST GOUDA DELISO 200g"),  # topljeni sir (skraćeno)
    ("svjezi_sir", "Fruit King Pripravak od svj. sira"),  # voćni desert
])
def test_dairy_not_members(staple, name):
    assert name_match(S[staple], name) == "excluded"


@pytest.mark.parametrize("name,amount,unit,chain,expected", [
    # stvarni test: Plodine su za "maslac" dale MASLAC KOZJI; ovdje su kozji, bez laktoze i ghee jeftiniji
    ("maslac", 50, "g", "konzum", "MASLAC 250 g"),
    ("maslac", 50, "g", "lidl", "MASLAC 250 g"),
    ("kozji maslac", 50, "g", "konzum", "MASLAC KOZJI 125 G EUROSER"),
    ("maslac bez laktoze", 50, "g", "konzum", "Kfree.Maslac 82% m.m. bez laktoze 125g"),
    ("ghee", 50, "g", "konzum", "dmBio ghee maslac 180 g"),
    ("jogurt", 500, "g", "konzum", "JOGURT TEKUĆI 2,8% 1 kg"),
    ("sojin jogurt", 400, "g", "konzum", "Alpro Soja jogurt 400g Natur bez šećera"),
    ("mozzarella", 125, "g", "konzum", "MOZZARELLA 125 G"),
    ("mozzarella di bufala", 125, "g", "konzum", "SIR MOZZARELLA BUFALA 125 g"),
    ("tvrdi sir", 200, "g", "konzum", "SIR GAUDA 250 g"),
    ("svježi sir", 250, "g", "spar", "SIR SVJEŽI 250 G"),
    ("vrhnje za kuhanje", 200, "ml", "konzum", "VRHNJE ZA KUHANJE 200 ml"),
    ("mlijeko bez laktoze", 1000, "ml", "konzum", "MLIJEKO TR 2.8% BEZ LAKT 1L LJUB MLEK"),
    ("kozje mlijeko", 1000, "ml", "konzum", "KOZJE MLIJEKO TRAJNO 2,8% 1 L"),
])
def test_dairy_basket_choice(con9, name, amount, unit, chain, expected):
    assert pick(con9, name, amount, unit, chain)["name"] == expected


def test_plain_milk_not_goat_or_lactose_free(con9):
    """Kozje i bez laktoze su jeftiniji od svih običnih, ali "mlijeko" ih ne bira."""
    item = pick(con9, "mlijeko", 1000, "ml")
    assert "KOZJE" not in item["name"] and "LAKT" not in item["name"]


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_maslac_plodine():
    """Stvarni test: Plodine Osijek za "maslac" biraju kravlji, a ne MASLAC KOZJI (ni ghee ni bez laktoze)."""
    out = json.loads((GOLDEN / "basket_maslac_plodine_osijek.json").read_text(encoding="utf-8"))
    assert not out["unmatched"]
    items = out["best_store"]["items"] + [i for s in out["stores"] for i in s["items"]]
    assert items and out["best_store"]["chain"] == "plodine"
    for i in items:
        attrs = i.get("attributes") or {}
        assert "vrsta_mlijeka" not in attrs and attrs.get("vrsta") != "ghee" and "laktoza" not in attrs, i["name"]
        assert "KOZJ" not in i["name"].upper()
