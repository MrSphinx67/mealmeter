"""Korak 10: nalazi iz testa bolonjeza (Osijek, 28.10.2026.). "pancetta" (talijanski pravopis) nije bila prepoznata;
namirnice celer (stabljika ili korijen; uz luk i mrkvu stabljika, inače pitanje) i kocka za juhu / temeljac (kocke i
prah po kg, tekući temeljac po l; zadano povrtni)."""

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
# (id, naziv, unit, quantity, cijene); ono što ne smije biti izabrano je jeftinije od onoga što mora biti
PRODUCTS = [
    ("S1", "PANCETA DALMATINSKA NAREZAK 100 g", "ko", None, {K: 1.99}),
    ("S2", "SLANINA DIMLJENA 200 g", "ko", None, {K: 1.49}),
    ("S3", "HRSKAVI KIKIRIKI OKUS SLANINE 100g", "ko", None, {L: 0.79}),  # stvarni Eurospin (bio je "pancetta")
    ("S4", "PUREĆA SLANINA NAR 100g", "ko", None, {K: 0.99}),  # stvarni Konzum (bio je "pancetta")
    ("S5", "Dalmatinska panceta, narezak 100 g", "ko", None, {L: 1.99}),
    ("C1", "CELER LIST 500 G", "KOM", None, {K: 1.29}),
    ("C2", "CELER KORIJEN 500 g", "ko", None, {K: 0.89}),
    ("C3", "CELER 500 g", "ko", None, {K: 0.49}),  # bez oznake: nije zadani izbor
    ("C4", "Celer list", "1komad", "0.458", {L: 1.29}),  # stvarni Lidl: komad bez težine (svežanj)
    ("C5", "SJEME CELER LISCAR", "ko", None, {K: 0.19}),
    ("K1", "KOCKA ZA JUHU POVRTNA 110g", "ko", None, {K: 0.79}),
    ("K2", "KOCKA ZA JUHU GOVEĐA 110g", "ko", None, {K: 0.69}),
    ("K3", "TEMELJAC POVRTNI 112g PODRAVKA", "ko", None, {K: 0.59}),  # gel: samo na zahtjev
    ("K4", "TEMELJAC RIBLJI 450 g", "ko", None, {K: 0.39}),
    ("K5", "KOKOS KOCKE XXL S&G 900g", "ko", None, {L: 0.49}),  # stvarni Eurospin (bio je "pileća kocka")
    ("K6", "Kocke za juhu goveđe 120g", "ko", None, {L: 0.75}),
    ("K7", "JUHA-KOCKA POVR.S-BUDGET 110 g", "ko", None, {SP: 0.68}),  # "juha" je inače isključena
    ("T1", "TEMELJAC POVRTNI 1 L PODRAVKA", "ko", None, {K: 1.99}),
    ("T2", "JUŠNI TEMELJ.DESPAR POVRĆE 1 L", "ko", None, {SP: 1.69}),
    ("T3", "KLC.Goveđi temeljac 140ml", "ko", None, {K: 0.99}),  # tekući koncentrat: premalo pakiranje
    ("V1", "LUK CRVENI 1 kg", "ko", None, {K: 0.99, L: 0.99, SP: 0.99}),
    ("V2", "MRKVA 1 kg", "ko", None, {K: 0.89, L: 0.89, SP: 0.89}),
]


@pytest.fixture(scope="module")
def con10(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s10") / "s10.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    rows, prices = [], []
    for pid, name, unit, quantity, by_store in PRODUCTS:
        for chain, store in by_store:
            if (chain, pid) not in {(r[0], r[1]) for r in rows}:
                rows.append((chain, pid, f"{chain}:{pid}", name, "HRANA", unit, quantity))
            prices.append((chain, store, pid, by_store[(chain, store)]))
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit, quantity) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    c.executemany("INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, ?, DATE '2026-10-19')",
                  prices)
    build_clean(c)
    yield c
    c.close()


def basket(con, ingredients: list[dict], chain: str | None = None) -> dict:
    return plan_basket(ingredients, "Osijek", con=con,
                       store={"chain": chain, "address_contains": ""} if chain else None)


def pick(con, name: str, amount: float, unit: str, chain: str = "konzum") -> dict:
    """Odabrani proizvod u zadanom lancu (Osijek)."""
    out = basket(con, [{"name": name, "amount": amount, "unit": unit}], chain)
    assert not out["unmatched"] and not out.get("ask_user"), (out["unmatched"], out.get("ask_user"))
    return out["best_store"]["items"][0]


# --- 1. nazivi sastojaka ----------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,staple,attrs", [
    ("pancetta", "slanina", {"vrsta": "panceta"}),
    ("panceta", "slanina", {"vrsta": "panceta"}),
    ("pancetta kockice", "slanina", {"vrsta": "panceta", "oblik": "kockice"}),
    ("slanina", "slanina", {}),
    ("pureća slanina", "slanina", {"vrsta": "pureca"}),
    ("celer", "celer", {}),
    ("celer korijen", "celer", {"vrsta": "korijen"}),
    ("korijen celera", "celer", {"vrsta": "korijen"}),
    ("stabljika celera", "celer", {"vrsta": "stabljika"}),
    ("celer list", "celer", {"vrsta": "stabljika"}),
    ("kocka za juhu", "kocka_za_juhu", {}),
    ("goveđa kocka za juhu", "kocka_za_juhu", {"okus": "govedi"}),
    ("pileća kocka za juhu", "kocka_za_juhu", {"okus": "kokosji"}),
    ("temeljac", "kocka_za_juhu", {}),
    ("povrtni temeljac", "kocka_za_juhu", {"okus": "povrtni"}),
    ("bujon", "kocka_za_juhu", {}),
    ("tekući temeljac", "tekuci_temeljac", {}),
    ("tekući goveđi temeljac", "kocka_za_juhu", {"okus": "govedi"}),  # oblik iz riječi "tekući" (form_words)
])
def test_names(name, staple, attrs):
    st, got = resolve_name(name)
    assert st.key == staple and got == attrs


@pytest.mark.parametrize("name,staple", [("mozzarela", "mozzarella"), ("pancetta", "slanina"),
                                         ("špagetti", "tjestenina")])
def test_doubled_letters(name, staple):
    """Pravopis s udvojenim slovom: "pancetta" je prije bila nepoznata namirnica."""
    assert resolve_name(name)[0].key == staple


@pytest.mark.parametrize("staple,name,attrs", [
    ("slanina", "PANCETA DALM.PIVAC 200 g NAR", {"vrsta": "panceta"}),
    ("slanina", "PUREĆA SLANINA NAR 100g", {"vrsta": "pureca"}),
    ("celer", "CELER LIST KOM", {"vrsta": "stabljika"}),
    ("celer", "200G CELER STABLJIKA", {"vrsta": "stabljika"}),
    ("celer", "Celer štapići 180 g", {"vrsta": "stabljika"}),
    ("celer", "CELER GLAVA", {"vrsta": "korijen"}),
    ("celer", "Celer korijen list", {"vrsta": "korijen"}),
    ("celer", "CELER KOR. SNIŽENJE", {"vrsta": "korijen"}),
    ("celer", "CELER 500g", {"vrsta": "nepoznato"}),
    ("kocka_za_juhu", "KOCKA ZA JUHU POVRTNA 110g VISPAK", {"okus": "povrtni", "vrsta": "kocka"}),
    ("kocka_za_juhu", "KOCKA KOKOSJA 120 G PODRAVKA", {"okus": "kokosji", "vrsta": "kocka"}),
    ("kocka_za_juhu", "JUHA-KOCKA MAGGI GOVEĐA 120 g", {"okus": "govedi", "vrsta": "kocka"}),
    ("kocka_za_juhu", "KOCKA ZA JUHU SA MESOM 220g", {"okus": "mesni", "vrsta": "kocka"}),
    ("kocka_za_juhu", "1KG MAGGI POVRTNI TEMELJ.PRAH", {"okus": "povrtni", "vrsta": "prah"}),
    ("kocka_za_juhu", "Podravka goveđi temeljac 4x28g 112 g", {"okus": "govedi", "vrsta": "gel"}),
    ("kocka_za_juhu", "TEMELJAC U ŽELATINI PILEĆI 112g", {"okus": "kokosji", "vrsta": "gel"}),
    ("tekuci_temeljac", "TEMELJAC OD MESA ZA JUHU 1l", {"okus": "mesni"}),
    ("tekuci_temeljac", "JUŠNI TEMELJ.DESPAR GOVED.1 L", {"okus": "govedi"}),
])
def test_attributes(staple, name, attrs):
    got = extract_attributes(S[staple], name)
    assert {a: got.get(a) for a in attrs} == attrs


@pytest.mark.parametrize("staple,name", [
    ("slanina", "HRSKAVI KIKIRIKI OKUS SLANINE 100g"), ("slanina", "BO Štangica sa slaninom"),
    ("celer", "SJEME CELER LISCAR"), ("celer", "SOK CELER I KRUSKA 0,7 L NATURA"), ("celer", "SALATA OD CELERA SPAR 650 g"),
    ("celer", "Celer korijen - ribani"), ("celer", "CELER KORIJEN GRANULE 30g SOTINAC"),
    ("kocka_za_juhu", "TEMELJAC RIBLJI 450 g"), ("kocka_za_juhu", "Perla Temeljac od škampa smrznuti 450 g"),
    ("kocka_za_juhu", "TEMELJAC SPAR ZA GULAŠ 69 g"), ("kocka_za_juhu", "ZAČIN KOTANYI TEMELJAC 18 g"),
    ("kocka_za_juhu", "TEMELJAC POVRTNI 1 L PODRAVKA"),  # tekući je druga namirnica
    ("tekuci_temeljac", "TESSAROL EGALIN TEMELJ ZA ŽELJEZO SIVI 0,75 L"),
])
def test_not_members(staple, name):
    assert name_match(S[staple], name) == "excluded"


@pytest.mark.parametrize("staple,name", [("kocka_za_juhu", "KOKOS KOCKE XXL S&G 900g"),
                                         ("tekuci_temeljac", "TEMELJAC POVRTNI 112g PODRAVKA")])
def test_not_candidates(staple, name):
    assert name_match(S[staple], name) is None


# --- 2. pancetta ------------------------------------------------------------------------------------------------

def test_pancetta_picks_panceta(con10):
    """Stvarni test: "pancetta" nije bila prepoznata. Sada je to panceta, i kad je obična slanina jeftinija; Lidl
    ne bira kikiriki s okusom slanine."""
    assert pick(con10, "pancetta", 100, "g")["name"] == "PANCETA DALMATINSKA NAREZAK 100 g"
    assert pick(con10, "pancetta", 100, "g", "lidl")["name"] == "Dalmatinska panceta, narezak 100 g"
    assert pick(con10, "slanina", 100, "g")["name"] == "SLANINA DIMLJENA 200 g"  # bez pureće, iako je jeftinija
    assert pick(con10, "pureća slanina", 100, "g")["name"] == "PUREĆA SLANINA NAR 100g"


def test_pancetta_free_text_uses_staple(con10):
    out = basket(con10, [{"name": "pancetta", "amount": 100, "unit": "g", "free_text": True}], "konzum")
    assert not out["unmatched"] and out["best_store"]["items"][0]["staple"] == "slanina"


# --- 3. celer ---------------------------------------------------------------------------------------------------

SOFFRITTO = [{"name": "luk", "amount": 1, "unit": "kom"}, {"name": "mrkva", "amount": 1, "unit": "kom"}]


def test_celer_with_onion_and_carrot_is_stalk(con10):
    out = basket(con10, SOFFRITTO + [{"name": "celer", "amount": 1, "unit": "kom"}], "konzum")
    assert not out.get("ask_user")
    item = next(i for i in out["best_store"]["items"] if i["ingredient"] == "celer")
    assert item["name"] == "CELER LIST 500 G"  # ne "CELER 500 g" bez oznake, iako je jeftiniji
    assumed = next(a for a in out["assumptions"] if a["ingredient"] == "celer")
    assert assumed["attributes"] == {"vrsta": "stabljika"} and "luk i mrkva" in assumed["text"]


def test_celer_alone_asks(con10):
    """Bez luka i mrkve vrsta se ne pogađa: ask_user sa stabljikom i korijenom; komad korijena je 400 g."""
    out = basket(con10, [{"name": "celer", "amount": 1, "unit": "kom"}, SOFFRITTO[0]])
    (ask,) = out["ask_user"]
    opts = {tuple(o["attributes"].items())[0][1]: o for o in ask["options"]}
    assert set(opts) == {"stabljika", "korijen"} and ask["question"] == "celer: stabljika ili korijen?"
    assert opts["stabljika"]["amount"] == 50 and opts["korijen"]["amount"] == 400
    assert out["ambiguous"][0]["staple"] == "celer"
    assert all(i["ingredient"] != "celer" for s in out["stores"] for i in s["items"])
    assert any("zadaj 'attributes.vrsta'" in w for w in out["warnings"])


def test_celer_root_piece_weight(con10):
    item = pick(con10, "celer korijen", 1, "kom")
    assert item["name"] == "CELER KORIJEN 500 g"
    out = basket(con10, [{"name": "celer", "amount": 1, "unit": "kom", "attributes": {"vrsta": "korijen"}}], "konzum")
    assert out["ingredients"][0]["amount"] == 400 and not out.get("ask_user")


def test_celer_bunch_without_weight(con10):
    """Stvarni Lidl: "Celer list" 1komad bez težine je svežanj od ≈ 450 g (prije nije imao količinu)."""
    out = basket(con10, SOFFRITTO + [{"name": "celer", "amount": 1, "unit": "kom"}], "lidl")
    item = next(i for i in out["best_store"]["items"] if i["ingredient"] == "celer")
    assert item["name"] == "Celer list" and item["pack_size"] == "≈ 450 g" and item["cost_pack"] == 1.29


# --- 4. kocka za juhu i temeljac --------------------------------------------------------------------------------

def test_stock_cube_default_vegetable(con10):
    """Zadano povrtna kocka; gel i goveđa su jeftiniji, riblji temeljac nije kocka za juhu."""
    item = pick(con10, "kocka za juhu", 1, "kom")
    assert item["name"] == "KOCKA ZA JUHU POVRTNA 110g" and item["n_packs"] == 1
    assert pick(con10, "goveđa kocka za juhu", 1, "kom")["name"] == "KOCKA ZA JUHU GOVEĐA 110g"
    out = basket(con10, [{"name": "kocka za juhu", "amount": 1, "unit": "kom", "attributes": {"vrsta": "gel"}}], "konzum")
    assert out["best_store"]["items"][0]["name"] == "TEMELJAC POVRTNI 112g PODRAVKA"


def test_stock_cube_other_flavour_when_no_vegetable(con10):
    assert pick(con10, "kocka za juhu", 1, "kom", "lidl")["name"] == "Kocke za juhu goveđe 120g"  # ne kokos
    assert pick(con10, "kocka za juhu", 1, "kom", "spar")["name"] == "JUHA-KOCKA POVR.S-BUDGET 110 g"


def test_stock_amounts(con10):
    """Kocka je 10 g; temeljac u ml preračunava se u grame koncentrata (10 g za 0,5 l)."""
    out = basket(con10, [{"name": "kocka za juhu", "amount": 2, "unit": "kom"}], "konzum")
    assert out["ingredients"][0]["amount"] == 20 and out["ingredients"][0]["unit"] == "g"
    out = basket(con10, [{"name": "temeljac", "amount": 500, "unit": "ml"}], "konzum")
    ing = out["ingredients"][0]
    assert ing["staple"] == "kocka_za_juhu" and ing["amount"] == 10 and ing["assumed_form"] == "koncentrat"
    assert any("pretpostavljen 'koncentrat'" in w and "tekuci" in w for w in out["warnings"])


def test_liquid_stock(con10):
    item = pick(con10, "tekući temeljac", 500, "ml")
    assert item["name"] == "TEMELJAC POVRTNI 1 L PODRAVKA"  # ne tekući koncentrat od 140 ml
    assert pick(con10, "tekući temeljac", 500, "ml", "spar")["name"] == "JUŠNI TEMELJ.DESPAR POVRĆE 1 L"
    out = basket(con10, [{"name": "temeljac", "amount": 500, "unit": "ml", "form": "tekuci"}], "konzum")
    assert out["ingredients"][0]["staple"] == "tekuci_temeljac"


# --- zlatni scenarij ---------------------------------------------------------------------------------------------

@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_bolonjez_osijek_10():
    """Stvarni test 28.10.: "pancetta", "celer" i "kocka za juhu" nisu bili prepoznati (Lidl "nedostaje: pancetta").
    Sada su svi sastojci prepoznati, panceta je panceta, celer stabljika, kocka povrtna, vino crno, maslac kravlji."""
    out = json.loads((GOLDEN / "basket_bolonjez_osijek_10.json").read_text(encoding="utf-8"))
    assert not out["unmatched"] and not out.get("ask_user")
    complete = {r["chain"] for r in out["comparison"] if r["complete"]} | {r["chain"] for r in out["more_chains"]}
    assert {"konzum", "plodine", "spar", "kaufland", "lidl"} <= complete
    for i in out["best_store"]["items"] + [i for s in out["stores"] for i in s["items"]]:
        attrs = i.get("attributes") or {}
        if i["ingredient"] == "pancetta":
            assert attrs.get("vrsta") == "panceta" and "PANCET" in i["name"].upper(), i["name"]
        elif i["ingredient"] == "celer":
            assert attrs.get("vrsta") == "stabljika", i["name"]
        elif i["ingredient"] == "kocka za juhu":
            assert attrs.get("vrsta") == "kocka" and attrs.get("okus") == "povrtni", i["name"]
        elif i["ingredient"] == "crno vino":
            assert attrs.get("boja") == "crno", i["name"]
        elif i["ingredient"] == "maslac":
            assert "vrsta_mlijeka" not in attrs and attrs.get("vrsta") != "ghee", i["name"]
