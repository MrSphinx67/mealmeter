"""Korak 13: marka (proizvođač) uz svaki proizvod u izlazima plan_basket, find_products i get_prices."""

import duckdb
import pytest

from mealmeter import server as srv
from mealmeter.brands import brand_from_name, clean_brand, display_brand, group_brand
from mealmeter.build import build_clean, load_raw
from tests.conftest import FIXTURE

D = "DATE '2026-10-19'"


# --- čišćenje stupca brand ------------------------------------------------------------------------------------

@pytest.mark.parametrize("raw,chain", [
    (None, "konzum"), ("", "konzum"), ("   ", "konzum"), ("-", "lidl"), ("#", "kaufland"), ("N/A", "spar"),
    ("NO BRAND", "eurospin"), ("AMIGA NO BRAND", "plodine"), ("ITALIJA - UNOS", "plodine"),
    ("KINA - UVOZ", "plodine"), ("ORBICO D.O.O.", "ntl"), ("KOOPMAN INTERNATIONAL B.V.", "ntl"),
    ("AWT INTERNATIONAL d.o.o.", "gavranovic"), ("ATLANTIC TRADE", "vrutak"), ("EUROCOM", "boso"),
    ("NARODNI TRGOVAČKI LANAC d.o.o.", "gavranovic"), ("Narodni trgovački lanac d.o.o.", "ntl"),
    ("NTL", "boso"), ("TRGOVINA KRK D.D.", "trgovina-krk"), ("NTL - Voće i povrće", "trgovina-krk"),
    ("STUDENAC-ROBNA MARKA", "studenac"), ("SKLADIŠTE VIP DUGOPOLJE", "tommy"), ("BOSO VOĆE", "boso"),
    ("SPAR", "konzum"), ("Crveno meso", "ribola"), ("SM. RIBLJI PROIZVODI NEP.", "stanic"),
    ("HL. SIRNI PROIZVODI BUCO", "stanic"), ("Autres marques tarif", "dukat"),
])
def test_junk_is_none(raw, chain):
    assert clean_brand(raw, chain) is None


@pytest.mark.parametrize("raw,chain,want", [
    ("K PLUS", "konzum", "K Plus"), ("Milbona", "lidl", "Milbona"), ("S-BUDGET", "spar", "S-Budget"),
    ("K-Classic", "kaufland", "K-Classic"), ("SPAR", "spar", "Spar"), ("SPAR Natur*pur", "spar", "SPAR Natur*pur"),
    ("METRO CHEF", "metro", "Metro Chef"), ("PODRAVKA d.d. KOPRIVNICA", "ktc", "Podravka"),
    ("PODRAVKA, KOPRIVNICA", "trgocentar", "Podravka"), ("VINDIJA D.O.O.", "ntl", "Vindija"),
    ("DR.OETKER", "ribola", "Dr. Oetker"), ("Z'BREGOV", "konzum", "Z bregov"), ("dmBio", "dm", "dmBio"),
    ("PIK VRBOVEC PLUS D.O.O.", "trgovina-krk", "PIK"), ("TRE MULINI", "eurospin", "Tre Mulini"),
    ("Deluxe", "lidl", "Deluxe"),
])
def test_real_brands_kept(raw, chain, want):
    assert clean_brand(raw, chain) == want


def test_brand_from_name_and_never_invented():
    assert brand_from_name("BRAŠNO GLATKO T-550 1kg MLINETA") == "Mlineta"
    assert brand_from_name("Brašno glatko T-550") is None
    assert brand_from_name("KEKSI S NUTELLOM 200 g") is None  # sastojak, ne proizvođač
    assert brand_from_name("Palačinke punjene Lino ladom") is None
    # stupac je dobavljač: marka iz naziva; stupac prazan: iz naziva; ničega: None
    assert display_brand("ORBICO D.O.O.", "NUTELLA 400 g FERRERO", "ntl") == "Nutella"
    assert display_brand("EUROCOM", "NUTELLA 400 g", "boso") == "Nutella"  # dobavljač bez pravnog oblika
    assert display_brand(None, "VANILIN ŠEĆER 8g DOLCELA", "lorenco") == "Dolcela"
    assert display_brand(None, "KRUMPIR 5 KG", "lorenco") is None
    assert display_brand("Krumpir", "Krumpir", "lidl") is None  # stupac samo ponavlja naziv
    # stupac s markom ima prednost pred nazivom (Podravka je proizvođač Vegete)
    assert display_brand("PODRAVKA", "VEGETA 500 g", "konzum") == "Podravka"
    # nepoznata marka iz stupca ostaje kad naziv ne počinje markom iz brands.yaml
    assert display_brand("GRANORO", "TJESTENINA LASAGNA 500 G GRANORO", "plodine") == "Granoro"


def test_group_brand():
    rows = [("PODRAVKA", "BRAŠNO", "konzum"), ("PODRAVKA D.D.", "BRAŠNO", "ntl"), ("ORBICO D.O.O.", "BRAŠNO", "ntl")]
    assert group_brand(rows) == "Podravka"
    assert group_brand([("-", "BRAŠNO", "lidl")]) is None
    # klasa namirnice (jaja:m:podni): marka samo kad je svima ista
    eggs = [("BALTICOVO", "JAJA M", "konzum"), (None, "JAJA M LUKAČ", "konzum")]
    assert group_brand(eggs) == "Balticovo" and group_brand(eggs, unique=True) is None
    assert group_brand([("K PLUS", "JAJA", "konzum"), ("K PLUS", "JAJA L", "konzum")], unique=True) == "K Plus"


# --- izlazi alata -------------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def con13(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s13") / "c.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    products = [  # (lanac, id, naziv, marka, unit, cijena)
        ("konzum", "B1", "BRAŠNO GLATKO T-550 1kg MLINETA", "ORBICO D.O.O.", "ko", 1.29),
        ("konzum", "B2", "BRAŠNO PŠENIČNO GLATKO T-550 1 kg K PLUS", "K PLUS", "ko", 0.69),
        ("lidl", "B3", "Brašno pšenično glatko T-550", "-", "1kg", 0.59),
        ("konzum", "M1", "MIJEŠANO MLJEVENO MESO 500 g PIK", "PIK VRBOVEC PLUS D.O.O.", "ko", 4.99),
        ("konzum", "M2", "SVINJSKO MLJEVENO MESO 500 g PIK", None, "ko", 3.99),
    ]
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, brand, category, unit) "
                  "VALUES (?, ?, ?, ?, ?, 'HRANA', ?)",
                  [(ch, pid, f"{ch}:{pid}", n, b, u) for ch, pid, n, b, u, _ in products])
    c.executemany(f"INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, ?, {D})",
                  [(ch, {"konzum": "0907", "lidl": "105"}[ch], pid, p) for ch, pid, _, _, _, p in products])
    build_clean(c)
    srv.create_server(con=c)
    yield c
    c.close()


def test_plan_basket_items_and_alternatives_have_brand(con13):
    ing = [{"name": "brašno glatko", "amount": 1000, "unit": "g"}, {"name": "mljeveno meso", "amount": 500, "unit": "g"}]
    res = srv.plan_basket(ingredients=ing, city="Osijek", store={"chain": "konzum", "address_contains": ""})
    items = {it["staple"]: it for it in res["best_store"]["items"]}
    assert all("brand" in it for it in items.values())
    assert items["brasno"]["name"].endswith("K PLUS") and items["brasno"]["brand"] == "K Plus"
    meat = items["mljeveno_meso"]
    assert meat["brand"] == "PIK"
    assert [(a["name"], a["brand"]) for a in meat["alternatives"]] == [("SVINJSKO MLJEVENO MESO 500 g PIK", "PIK")]
    lidl = srv.plan_basket(ingredients=ing[:1], city="Osijek", store={"chain": "lidl", "address_contains": ""})
    item = lidl["best_store"]["items"][0]
    assert "brand" in item and item["brand"] is None  # "-" i naziv bez marke: null, ne izmišlja se


def test_plan_basket_detail_has_brand(con13):
    res = srv.plan_basket(ingredients=[{"name": "brašno glatko", "amount": 1000, "unit": "g"}], city="Osijek",
                          detail=True)
    for store in res["stores"]:
        for it in store["items"]:
            assert "brand" in it


def test_find_products_and_get_prices_brand(con13):
    res = srv.find_products(ingredient="brašno", city="Osijek")
    brands = {r["name"]: r["brand"] for r in res["results"]}
    assert brands["BRAŠNO GLATKO T-550 1kg MLINETA"] == "Mlineta"  # dobavljač u stupcu, marka iz naziva
    assert brands["BRAŠNO PŠENIČNO GLATKO T-550 1 kg K PLUS"] == "K Plus"
    assert brands["Brašno pšenično glatko T-550"] is None
    stores = srv.get_prices(product_id="konzum:B1", city="Osijek")["stores"]
    assert stores and all(s["brand"] == "Mlineta" for s in stores)
    assert all(s["brand"] is None for s in srv.get_prices(product_id="lidl:B3", city="Osijek")["stores"])
