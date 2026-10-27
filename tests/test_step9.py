"""Korak 9: izbor proizvoda iz stvarnog testa (bolonjez, Osijek, 27.10.2026.): zadano kravlji maslac i obične
mliječne namirnice; posebne vrste (kozje, ovčje, bivolje, bez laktoze, biljno, ghee) samo na zahtjev. Zadano obična
tjestenina; sa špinatom, integralna, bez glutena, s jajima, svježa i ostale vrste samo na zahtjev. Vino za kuhanje:
najjeftinije mirno crno ili bijelo vino, bez ostalih alkoholnih pića."""

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
    ("P1", "TJESTENINA TAGLIATELLE 500 G", {K: 1.49, L: 1.59}),
    ("P2", "TJESTENINA TAGLIATELLE VERDI 500 G RISCOSA", {K: 0.99, L: 0.99}),
    ("P3", "REZANCI ŠIROKI S JAJ 400g K PLUS", {K: 0.89}),
    ("P4", "TIJESTO TAGLIATELLE PIR 400g SIMPLY PASTA", {K: 0.79}),
    ("P5", "Kritharaki rezanci", {L: 0.79}),
    ("P6", "TJE.INTE.PENNE RIGATE BRONZO 500g", {K: 0.59}),
    ("P7", "TJESTENINA PENNE RIGATE 500g", {K: 0.89}),
    ("P8", "TJESTENINA TAGLIATELLE 1 kg", {K: 2.49}),  # za 400 g jeftinije od 500 g, a na blagajni skuplje
]
# (id, naziv, kategorija lanca, cijene): vino je u kategoriji alkohola (category_map: "vino", "zestoko")
DRINKS = [
    ("W1", "VINO CRNO 1L KASTELAN", "VINO", {K: 2.49}),
    ("W2", "VINO BIJELO SUHO 1 L", "VINO", {K: 1.86}),
    ("W3", "Matić Vino crno Muškat Ruža 0,5L", "VINO", {K: 0.99}),  # stvarni test, Kaufland (desertno)
    ("W4", "PJENUŠAVO VINO BRUT 0,75 L", "VINO", {K: 0.89}),
    ("W5", "VINO ROSE 0,75L DALMACIJAVINO", "VINO", {K: 0.79}),
    ("W6", "VINO VENUS 1L TETRAPAK", "VINO", {K: 0.59}),  # boja nepoznata
    ("W7", "VERITAS VRANAC 1 L", "VINO", {L: 1.99}),  # bez riječi "vino"
    ("W8", "RAKIJA LOZA MALVAZIJA ISTARSKA 0,7", "ZESTOKO", {K: 0.49}),
]


@pytest.fixture(scope="module")
def con9(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s9") / "s9.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    rows, prices = [], []
    for pid, name, category, by_store in [(p, n, "HRANA", b) for p, n, b in PRODUCTS] + DRINKS:
        for chain, store in by_store:
            if (chain, pid) not in {(r[0], r[1]) for r in rows}:
                rows.append((chain, pid, f"{chain}:{pid}", name, category, "ko"))
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


# --- 2. tjestenina: zadano obična ----------------------------------------------------------------------------

@pytest.mark.parametrize("name,attrs", [
    ("tagliatelle", {"oblik": "tagliatelle"}),
    ("rezanci", {"oblik": "tagliatelle"}),
    ("široki rezanci", {"oblik": "tagliatelle"}),
    ("zelene tagliatelle", {"oblik": "tagliatelle", "vrsta": "sa_spinatom"}),
    ("tagliatelle sa špinatom", {"oblik": "tagliatelle", "vrsta": "sa_spinatom"}),
    ("tagliatelle s jajima", {"oblik": "tagliatelle", "vrsta": "s_jajima"}),
    ("jajčani rezanci", {"oblik": "tagliatelle", "vrsta": "s_jajima"}),
    ("svježe tagliatelle", {"oblik": "tagliatelle", "vrsta": "svjeza"}),
    ("integralni špageti", {"oblik": "spageti", "vrsta": "integralna"}),
    ("pirovi špageti", {"oblik": "spageti", "vrsta": "od_pira"}),
    ("tjestenina bez glutena", {"vrsta": "bez_glutena"}),
    ("bezglutenska tjestenina", {"vrsta": "bez_glutena"}),
    ("rezanci za juhu", {"oblik": "jusni"}),
    ("farfalle", {"oblik": "farfalle"}),
    ("špageti", {"oblik": "spageti"}),
])
def test_pasta_names(name, attrs):
    st, got = resolve_name(name)
    assert st.key == "tjestenina" and got == attrs


@pytest.mark.parametrize("name,attr,value", [
    ("TJESTENINA TAGLIATELLE VERDI 500 G RISCOSA", "vrsta", "sa_spinatom"),  # stvarni test, Plodine
    ("TJ.TAGLIATELLE SA SPIN.250 G DE CECCO VRECICA", "vrsta", "sa_spinatom"),
    ("TJ.TAGLIATELLE 500 g ŠIPNAT BR98 BARI", "vrsta", "sa_spinatom"),
    ("TJES.PREMIUM ZELE.REZANC.400 g", "vrsta", "sa_spinatom"),
    ("REZANCI ŠIROKI S JAJ 400g K PLUS", "vrsta", "s_jajima"),
    ("K-Favourites NMNP Šir.rezanc.s jaji.400g", "vrsta", "s_jajima"),
    ("LM pl.linija tagliatelle 203 s.j.250g", "vrsta", "s_jajima"),
    ("REZANCI SIROKI RAVNI JAJCANI XXL 600 G", "vrsta", "s_jajima"),
    ("TIJESTO TAGLIATELLE PIR 400g SIMPLY PASTA", "vrsta", "od_pira"),
    ("TJE.INTE.PENNE RIGATE BRONZO 500g", "vrsta", "integralna"),
    ("TJ.FUSILLI B.G. CR.LEĆA 250 g", "vrsta", "bez_glutena"),
    ("TJ.PENNE CRV.LECA 250 G BARILLA", "vrsta", "od_mahunarki"),
    ("ZP REZANCI OD HELJDE 400g", "vrsta", "bez_glutena"),
    ("TJEST. REZANCI CRNI 400 g MARIOLINA", "vrsta", "obojena"),
    ("CIKLA REZANCI 680 g PODRAVKA", "vrsta", "obojena"),
    ("TJ.PANONA 400g TRICOLORE", "vrsta", "obojena"),
    ("TJ.REGGIA 500g TAGLIATELLE SVJEŽE", "vrsta", "svjeza"),
    ("Kritharaki rezanci", "oblik", "jusni"),  # stvarni test, Lidl
    ("REZANCI ZA JUHU 400 g RAFAJAC", "oblik", "jusni"),
    ("REZANCI JAPAN 300 g SAITAKU SOBA", "oblik", "azijski"),
])
def test_pasta_special_variants(name, attr, value):
    st = S["tjestenina"]
    assert extract_attributes(st, name).get(attr) == value
    if attr == "vrsta":
        assert (attr, value) in st.default_exclude_variants


@pytest.mark.parametrize("name,oblik", [
    ("1KG MC TAGLIATELLE BEZ JAJA", "tagliatelle"),  # "bez jaja" nije s jajima
    ("La Molisana tagliatelle 103 b.j. 500g", "tagliatelle"),
    ("TJESTENINA TAGLIATELLE 500 G RUMMO", "tagliatelle"),
    ("TJ. INTERSPAR PENNE 500g", "penne"),  # "INTERSPAR" nije integralna
    ("Ragusa široki rezanci 400 g", "tagliatelle"),
    ("TJESTENINA ŠPAGETI 400 g PANEA", "spageti"),
])
def test_pasta_plain(name, oblik):
    attrs = extract_attributes(S["tjestenina"], name)
    assert attrs.get("oblik") == oblik and "vrsta" not in attrs


@pytest.mark.parametrize("name", ["STROJ ZA REZANCE-rasprodaja", "400G B.L REZANCI KADAIF"])
def test_pasta_not_members(name):
    assert name_match(S["tjestenina"], name) == "excluded"


@pytest.mark.parametrize("name,amount,chain,expected", [
    # VERDI, s jajima i od pira su jeftiniji, ali "tagliatelle" bira obične
    ("tagliatelle", 400, "konzum", "TJESTENINA TAGLIATELLE 500 G"),
    ("tagliatelle", 400, "lidl", "TJESTENINA TAGLIATELLE 500 G"),  # Kritharaki nisu tagliatelle
    ("zelene tagliatelle", 400, "konzum", "TJESTENINA TAGLIATELLE VERDI 500 G RISCOSA"),
    ("tagliatelle s jajima", 400, "konzum", "REZANCI ŠIROKI S JAJ 400g K PLUS"),
    ("penne", 400, "konzum", "TJESTENINA PENNE RIGATE 500g"),
    ("integralni penne", 400, "konzum", "TJE.INTE.PENNE RIGATE BRONZO 500g"),
])
def test_pasta_basket_choice(con9, name, amount, chain, expected):
    assert pick(con9, name, amount, "g", chain)["name"] == expected


def test_tagliatelle_free_text_uses_staple(con9):
    """Stvarni ulaz iz testa: "tagliatelle" s free_text: true. Naziv je sada namirnica, pa vrijede zadana
    isključenja (prije slobodna pretraga: najjeftinije bilo kakve tagliatelle, u Plodinama VERDI)."""
    out = plan_basket([{"name": "tagliatelle", "amount": 400, "unit": "g", "free_text": True}], "Osijek", con=con9,
                      store={"chain": "konzum", "address_contains": ""})
    item = out["best_store"]["items"][0]
    assert item["staple"] == "tjestenina" and item["name"] == "TJESTENINA TAGLIATELLE 500 G"


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_tagliatelle_plodine():
    """Stvarni test: "tagliatelle" (free_text) u Plodinama Osijek nisu VERDI, ni s jajima ni druga posebna vrsta."""
    out = json.loads((GOLDEN / "basket_tagliatelle_plodine_osijek.json").read_text(encoding="utf-8"))
    assert not out["unmatched"]
    items = out["best_store"]["items"]
    assert items and out["best_store"]["chain"] == "plodine"
    for i in items + [i for s in out["stores"] for i in s["items"]]:
        assert i["staple"] == "tjestenina" and i["attributes"].get("oblik") == "tagliatelle", i["name"]
        assert "vrsta" not in i["attributes"] and "VERDI" not in i["name"].upper(), i["name"]


# --- 3. vino za kuhanje -------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,attrs", [
    ("vino", {}),
    ("vino za kuhanje", {}),
    ("crno vino", {"boja": "crno"}),
    ("crveno vino", {"boja": "crno"}),
    ("bijelo vino", {"boja": "bijelo"}),
    ("suho bijelo vino", {"boja": "bijelo"}),
    ("crno vino za kuhanje", {"boja": "crno"}),
    ("rose vino", {"boja": "rose"}),
])
def test_wine_names(name, attrs):
    st, got = resolve_name(name)
    assert st.key == "vino" and st.alcohol and got == attrs


@pytest.mark.parametrize("name", ["rakija", "pivo", "pjenušac", "liker"])
def test_other_alcohol_not_staple(name):
    with pytest.raises(Exception):
        resolve_name(name)


@pytest.mark.parametrize("name,boja", [
    ("VINO CRNO MERLOT KASTELAN 1L", "crno"),
    ("vino cab sauv vrh 0 75l", "crno"),  # cabernet sauvignon je crno, ne sauvignon
    ("VERITAS VRANAC 1,0", "crno"),
    ("VINO STOLNO BIJELO 2 L HAČKO", "bijelo"),
    ("Vina Belje Graševina kvalitetno vino 1 l", "bijelo"),
    ("vino orahovica frankovka rose 0 75l", "rose"),  # rose prije crnog (frankovka)
    ("VINO VENUS 1L TETRAPAK", "nepoznato"),
])
def test_wine_colour(name, boja):
    st = S["vino"]
    assert name_match(st, name) == "match"
    assert extract_attributes(st, name)["boja"] == boja


@pytest.mark.parametrize("name", [
    "Matić Vino crno Muškat Ruža 0,5L", "PJENUŠAVO VINO BRUT 0,75 L", "vino grasecco brut 0 2 l",
    "Secco Vino bijelo gazirano 0,2L LIM", "venus vranac poluslatko", "slatko crveno vino 0 75l pop art",
    "rakija loza malvazija istarska rossi 0 7", "liker teran s cvij soli 0 2 l", "KUHANO VINO VRECICA 35g",
    "zero sl zero rosso bezalkoholno vino 750ml", "*CABERNET - SYRAH ALCOHOL FREE J.P.CHENET 0.75L",
    "Dolin Vino aromat.Vermouth Blanc 0,75L", "200g boskarin salama crno vino", "casa za vino 370 ml",
    "0,5L KVASINA PLAVAC MALI", "GROŽĐE CRNO VRANAC", "aromatizirano pjenusavo vino gallei hugo 0 75 l",
])
def test_wine_not_members(name):
    assert name_match(S["vino"], name) in (None, "excluded")


@pytest.mark.parametrize("name", ["KRUH FRANCUZ 500 g BABIĆ", "Mini posip za kolače SK2", "NESTLE SMARTIES POSIP 500 GRAMA"])
def test_grape_brand_homonyms_not_wine(name):
    """Babić je i pekara, pošip je i posip za kolače: sorte samo uz riječ "vino"."""
    assert name_match(S["vino"], name) is None


@pytest.mark.parametrize("name,chain,expected", [
    ("crno vino", "konzum", "VINO CRNO 1L KASTELAN"),  # desertno, pjenušac, rose i nepoznata boja su jeftiniji
    ("bijelo vino", "konzum", "VINO BIJELO SUHO 1 L"),
    ("vino", "konzum", "VINO BIJELO SUHO 1 L"),  # bez boje: najjeftinije od crnog i bijelog
    ("rose vino", "konzum", "VINO ROSE 0,75L DALMACIJAVINO"),
    ("crno vino", "lidl", "VERITAS VRANAC 1 L"),
])
def test_wine_basket_choice(con9, name, chain, expected):
    assert pick(con9, name, 200, "ml", chain)["name"] == expected


def test_wine_free_text_uses_staple(con9):
    """Stvarni ulaz: "crno vino" kao free_text. Prije: slobodna pretraga bez alkohola, pa vina nije bilo."""
    out = plan_basket([{"name": "crno vino", "amount": 200, "unit": "ml", "free_text": True}], "Osijek", con=con9,
                      store={"chain": "konzum", "address_contains": ""})
    item = out["best_store"]["items"][0]
    assert item["staple"] == "vino" and item["name"] == "VINO CRNO 1L KASTELAN"


def test_other_alcohol_still_excluded(con9):
    """Rakija (najjeftinija, u istoj trgovini) nije ni free_text ni u find_products za vino."""
    from mealmeter.search import find_products

    out = plan_basket([{"name": "rakija", "amount": 100, "unit": "ml", "free_text": True}], "Osijek", con=con9)
    assert out["unmatched"] and not out["comparison"]
    names = {r["name"] for r in find_products(ingredient="vino", city="Osijek", con=con9, limit=50)}
    assert "VINO CRNO 1L KASTELAN" in names and not any("RAKIJA" in n.upper() for n in names)
    assert not find_products("rakija", city="Osijek", con=con9)


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_crno_vino_osijek():
    """Stvarni test: "crno vino" (free_text) u Osijeku nije bilo nigdje osim desertnog vina u Kauflandu; sada je
    mirno crno vino u svim velikim lancima."""
    out = json.loads((GOLDEN / "basket_crno_vino_osijek.json").read_text(encoding="utf-8"))
    assert not out["unmatched"]
    chains = {r["chain"] for r in out["comparison"] if r["complete"]} | {r["chain"] for r in out["more_chains"]}
    assert {"konzum", "lidl", "kaufland", "plodine", "spar"} <= chains
    for i in out["best_store"]["items"] + [i for s in out["stores"] for i in s["items"]]:
        assert i["staple"] == "vino" and i["attributes"]["boja"] == "crno", i["name"]
        assert not any(w in i["name"].upper() for w in ("MUŠKAT", "PJENUŠ", "BRUT", "SLAT")), i["name"]


# --- 4. upute: što nedostaje uz cijenu, cheaper = false nije ušteda ---------------------------------------------

def _instructions() -> str:
    from mealmeter.server import INSTRUCTIONS

    return " ".join(INSTRUCTIONS.split())


def _rule(n: int) -> str:
    return _instructions().split(f" {n}. ", 1)[1].split(f" {n + 1}. ", 1)[0]


def test_rule_missing_next_to_price():
    """Stvarni test: "Lidl oko 26 €" bez napomene da nedostaje pancetta."""
    r8 = _rule(8)
    for phrase in ('s "nedostaje: ..."', "uz cijenu takvog lanca to uvijek navedi, gdje god je spomeneš",
                   '("Lidl oko 26 €, nedostaje: pancetta")', "nije najjeftiniji",
                   "always with what is missing next to their price"):
        assert phrase in r8, phrase
    r7 = _rule(7)
    assert "Ako joj nešto nedostaje, uz ukupnu cijenu navedi što" in r7 and "(and what it lacks)" in r7


def test_rule_cheaper_false_never_saving():
    r11 = _rule(11)
    for phrase in ('Alternativu zovi "jeftinijom" ili uštedom samo kad je cheaper = true',
                   "cheaper = false nikad nije ušteda", "na blagajni može biti skuplje",
                   '"cheaper" or a saving only when cheaper = true', "cheaper = false never is"):
        assert phrase in r11, phrase


def test_incomplete_chain_carries_missing(con9):
    """Podaci za pravilo 8: lanac kojem nešto nedostaje ima cijenu i popis onoga što nedostaje (note)."""
    out = plan_basket([{"name": "maslac", "amount": 50, "unit": "g"},
                       {"name": "rose vino", "amount": 200, "unit": "ml"}], "Osijek", con=con9)
    lidl = [r for r in out["incomplete"] if r["chain"] == "lidl"]
    assert lidl and lidl[0]["total_to_buy"] > 0 and lidl[0]["note"] == "nedostaje: rose vino"


def test_alternatives_cheaper_flag(con9):
    """Podaci za pravilo 11: cheaper = true znači jeftinije za istu potrebnu količinu (delta_eur < 0), a ne na
    blagajni: veće pakiranje (size_note) ima veći cost_pack."""
    out = plan_basket([{"name": "tagliatelle", "amount": 400, "unit": "g"}], "Osijek", con=con9, alternatives=True,
                      store={"chain": "konzum", "address_contains": ""})
    item = out["best_store"]["items"][0]
    assert item["name"] == "TJESTENINA TAGLIATELLE 500 G"
    alts = {a["name"]: a for a in item["alternatives"]}
    big = alts["TJESTENINA TAGLIATELLE 1 kg"]
    assert big["cheaper"] and big["delta_eur"] < 0 and big["size_note"]
    assert big["cost_pack"] > item["cost_pack"]  # na blagajni skuplje: pravilo 11 traži da se to kaže
    assert all(a["cheaper"] == (a["delta_eur"] < 0) for a in item["alternatives"])
