"""Korak 5B: zbrojevi, preporuka i usporedba lanaca, prinos oblika, nove namirnice, free_text sinonimi,
pretpostavke, alternative na istu količinu."""

import duckdb
import pytest

from mealmeter.basket import plan_basket
from mealmeter.build import build_clean, load_raw
from tests.conftest import FIXTURE

# (id, naziv, unit, cijene po trgovini {trgovina: cijena}); trgovine: Konzum Osijek 0907 i Zagreb 0001,
# Lidl Osijek 105, Spar Osijek 87089
K, KZ, L, SP = ("konzum", "0907"), ("konzum", "0001"), ("lidl", "105"), ("spar", "87089")
PRODUCTS = [
    ("P1", "TJESTENINA ŠPAGETI 500 g", "ko", {K: 0.89, KZ: 0.89, L: 0.79}),
    ("P2", "MIJEŠANO MLJEVENO MESO 500 g", "ko", {K: 4.99, KZ: 4.99, L: 4.29}),
    ("P3", "PASIRANA RAJČICA 700 g", "ko", {K: 1.29, KZ: 1.29, L: 0.99}),
    ("P4", "LUK CRVENI 1 kg", "ko", {K: 0.99, KZ: 0.99, L: 0.79, SP: 1.19}),
    ("P5", "ULJE SUNCOKRETOVO 1 L", "ko", {K: 1.49, KZ: 1.49, L: 1.38, SP: 1.59}),
    ("P6", "SOL MORSKA 1 kg", "ko", {K: 0.49, KZ: 0.49, L: 0.35, SP: 0.59}),
    ("P7", "PAPAR CRNI MLJEVENI 50 g", "ko", {K: 1.19, KZ: 1.19, L: 0.99, SP: 1.29}),
    ("P8", "GRAŠAK SMRZNUTI 1 kg", "ko", {K: 2.29, L: 1.99, SP: 2.49}),
    ("P9", "MRKVA 1 kg", "ko", {K: 0.79, L: 0.79, SP: 0.99}),
    ("P10", "BRAŠNO GLATKO T-550 1 kg", "ko", {K: 0.69, KZ: 0.69, L: 0.75, SP: 0.79}),
    ("P11", "MLIJEKO TRAJNO 2,8% 1 L", "ko", {K: 0.99, KZ: 0.99, L: 0.52, SP: 1.09}),
    ("P12", "JAJA SVJEŽA PODNI UZGOJ M 10/1", "ko", {K: 1.99, KZ: 1.99, L: 1.85, SP: 2.19}),
    ("P13", "ŠEĆER KRISTAL 1 kg", "ko", {K: 0.99, KZ: 0.99, L: 0.75, SP: 1.09}),
]


@pytest.fixture(scope="module")
def con5b(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s5b") / "b.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    rows, prices = [], []
    for pid, name, unit, by_store in PRODUCTS:
        for (chain, store), price in by_store.items():
            if (chain, pid) not in {(r[0], r[1]) for r in rows}:
                rows.append((chain, pid, f"{chain}:{pid}", name, "HRANA", unit))
            prices.append((chain, store, pid, price))
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES (?, ?, ?, ?, ?, ?)", rows)
    c.executemany("INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, ?, DATE '2026-10-19')",
                  prices)
    build_clean(c)
    yield c
    c.close()

BOLONJEZ = [{"name": "špageti", "amount": 400, "unit": "g"}, {"name": "mljeveno meso", "amount": 500, "unit": "g"},
            {"name": "rajčica", "amount": 700, "unit": "g", "form": "pasirana"}, {"name": "luk", "amount": 1, "unit": "kom"},
            {"name": "ulje", "amount": 30, "unit": "ml"}, {"name": "sol", "amount": 5, "unit": "g"}]
VARIVO = [{"name": "grašak", "amount": 800, "unit": "g", "form": "smrznuto"}, {"name": "luk", "amount": 1, "unit": "kom"},
          {"name": "mrkva", "amount": 2, "unit": "kom"}, {"name": "brašno glatko", "amount": 20, "unit": "g"},
          {"name": "ulje", "amount": 30, "unit": "ml"}, {"name": "sol", "amount": 5, "unit": "g"},
          {"name": "papar", "amount": 2, "unit": "g"}]
PALACINKE = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
             {"name": "jaja", "amount": 3, "unit": "kom"}, {"name": "šećer", "amount": 15, "unit": "g"},
             {"name": "sol", "amount": 1, "unit": "g"}, {"name": "ulje", "amount": 30, "unit": "ml"}]
HAVE = ["sol", "papar", "ulje"]


# --- 1. zbrojevi --------------------------------------------------------------------------------------------

@pytest.mark.parametrize("recipe,city", [(BOLONJEZ, "Zagreb"), (VARIVO, "Osijek"), (PALACINKE, "Osijek")])
def test_row_sums_equal_totals(con5b, recipe, city):
    res = plan_basket(recipe, city, con=con5b, already_have=HAVE)
    assert res["stores"]
    for s in res["stores"]:
        buy = [it for it in s["items"] if not it["have"]]
        assert s["total_used"] == round(sum(it["cost_used"] for it in buy), 2)
        assert s["total_to_buy"] == round(sum(it["cost_pack"] for it in buy), 2)
        assert s["from_stock_value"] == round(sum(it["cost_used"] for it in s["items"] if it["have"]), 2)
    assert any(it["have"] for s in res["stores"] for it in s["items"])


# --- 2. preporuka i usporedba lanaca ----------------------------------------------------------------------

def test_best_by_total_to_buy_and_comparison(con5b):
    res = plan_basket(PALACINKE, "Osijek", con=con5b)
    complete = [s for s in res["stores"] if not s["missing"]]
    assert res["best_store"]["total_to_buy"] == min(s["total_to_buy"] for s in complete)
    rows = res["comparison"]
    assert 1 <= len(rows) <= 6 and len({r["chain"] for r in rows}) == len(rows)
    assert [r["total_to_buy"] for r in rows if r["complete"]] == sorted(r["total_to_buy"] for r in rows if r["complete"])
    assert all(r["n_matched"] / r["n_ingredients"] >= 0.8 and len(r["addresses"]) <= 2 and r["n_stores_city"] >= 1
               for r in rows)
    assert {"lidl", "konzum", "spar"} <= {r["chain"] for r in rows}
    lidl = next(r for r in rows if r["chain"] == "lidl")
    assert lidl["total_to_buy"] == res["best_store"]["total_to_buy"]  # Lidl je najjeftiniji (fixture)
    for inc in res["incomplete"]:
        assert inc["note"].startswith("nedostaje: ") and inc["missing"]


def test_incomplete_chain_listed(con5b):
    # Spar (fixture) nema špagete, meso ni rajčicu: bolonjez u Osijeku ima Spar samo kao nepotpun
    res = plan_basket(BOLONJEZ, "Osijek", con=con5b)
    spar = [i for i in res["incomplete"] if i["chain"] == "spar"]
    assert spar and "špageti" in spar[0]["missing"] and spar[0]["note"].startswith("nedostaje: ")
    assert "spar" not in {r["chain"] for r in res["comparison"]}
