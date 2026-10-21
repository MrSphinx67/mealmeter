"""Korak 4C: alternative po pravilima glavnog izbora, jaja, marka, free_text, vrećice, veličina odgovora,
dvosmisleni sastojci."""

import duckdb
import pytest

from mealmeter.basket import alt_eligible, plan_basket, portion_pack
from mealmeter.build import build_clean, load_raw
from mealmeter.staples import load_staples
from tests.conftest import FIXTURE

D = "DATE '2026-10-19'"


@pytest.fixture(scope="module")
def con4c(tmp_path_factory):
    """Fixture baza + proizvodi u Konzumu Osijek (0907) i Lidlu Osijek (105) za scenarije Koraka 4C."""
    c = duckdb.connect(str(tmp_path_factory.mktemp("s4c") / "c.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    products = [  # (lanac, id, naziv, kategorija, unit, cijena)
        ("konzum", "S1", "ŠEĆER KRISTAL 1 kg VIROVITICA", "HRANA", "ko", 0.99),
        ("konzum", "S2", "ŠEĆER MINUTE BIJELI 1000X4g", "HRANA", "ko", 0.50),
        ("konzum", "G1", "GRANA PADANO cca 1KG METRO", "HRANA", "kg", 9.90),
        ("konzum", "G2", "SIR GRANA PADANO 200 g ZANETTI", "HRANA", "ko", 3.49),
        ("konzum", "M1", "MIJEŠANO MLJEVENO MESO 500 g PIK", "HRANA", "ko", 4.99),
        ("konzum", "M2", "SVINJSKO MLJEVENO MESO 500 g PIK", "HRANA", "ko", 3.99),
        ("konzum", "M3", "JUNEĆE MLJEVENO MESO 500 g PIK", "HRANA", "ko", 5.49),
    ]
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES (?, ?, ?, ?, ?, ?)",
                  [(ch, pid, f"{ch}:{pid}", n, cat, u) for ch, pid, n, cat, u, _ in products])
    c.executemany(f"INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, ?, {D})",
                  [(ch, {"konzum": "0907", "lidl": "105"}[ch], pid, p) for ch, pid, _, _, _, p in products])
    build_clean(c)
    yield c
    c.close()


KONZUM = {"chain": "konzum", "address_contains": ""}


# --- 1. alternative ---------------------------------------------------------------------------------------

def test_alt_eligible_rules():
    st = load_staples()
    sugar, cheese = st["secer"], st["parmezan"]
    base = {"chain": "konzum", "name": "ŠEĆER KRISTAL 1 kg", "variable_weight": False}
    assert alt_eligible(base, sugar)
    assert portion_pack({"name": "ŠEĆER MINUTE BIJELI 1000X4g"}, sugar)
    assert not alt_eligible({**base, "name": "ŠEĆER MINUTE BIJELI 1000X4g"}, sugar)
    assert not portion_pack({"name": "Dolcela Vanilin šećer 6x8g"}, st["vanilin_secer"])  # vrećice nisu porcije
    assert not alt_eligible({**base, "name": "GRANA PADANO cca 1KG METRO", "variable_weight": True}, cheese)
    assert not alt_eligible({**base, "chain": "metro"}, sugar)
    for flag in ("price_suspect", "unit_suspect"):
        assert not alt_eligible({**base, flag: True}, sugar)
    assert not alt_eligible({**base, "match_quality": "weak"}, sugar)


def test_alternatives_only_cheaper_and_eligible(con4c):
    ing = [{"name": "šećer", "amount": 100, "unit": "g"}, {"name": "parmezan", "amount": 40, "unit": "g"},
           {"name": "mljeveno meso", "amount": 500, "unit": "g"}]
    res = plan_basket(ing, "Osijek", con=con4c, store=KONZUM, alternatives=True)
    items = {it["staple"]: it for it in res["best_store"]["items"]}
    names = [a["name"] for it in items.values() for a in it["alternatives"]]
    assert not any("MINUTE" in n or "cca" in n for n in names)
    assert items["secer"]["product_id"] == "S1"  # porcijsko pakiranje nije ni glavni izbor
    for it in items.values():
        assert len(it["alternatives"]) <= 2
        assert all(a["cheaper"] and a["delta_eur"] < 0 for a in it["alternatives"])
        assert [a["cost_pack"] for a in it["alternatives"]] == sorted(a["cost_pack"] for a in it["alternatives"])
    meat = items["mljeveno_meso"]
    assert meat["product_id"] == "M1" and [a["product_id"] for a in meat["alternatives"]] == ["M2"]
    assert meat["alternatives"][0]["delta_eur"] == -1.0
