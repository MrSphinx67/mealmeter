import json
from dataclasses import replace
from pathlib import Path

import pytest

from mealmeter import search
from mealmeter.basket import IngredientError, choose_product, plan_basket, resolve_name, to_base
from mealmeter.staples import load_staples

S = load_staples()
RECIPES = Path(__file__).resolve().parents[1] / "data" / "recipes"


# --- naziv i jedinice ---------------------------------------------------------

@pytest.mark.parametrize("name,key,attrs", [
    ("brašno", "brasno", {}),
    ("brašno glatko", "brasno", {"tip": "glatko"}),
    ("glatko brašno", "brasno", {"tip": "glatko"}),
    ("špageti", "tjestenina", {"oblik": "spageti"}),
    ("koncentrat rajčice", "koncentrat_rajcice", {}),
    ("Iceberg", "zelena_salata", {"vrsta": "iceberg"}),  # sinonim je i vrijednost atributa
])
def test_resolve_name(name, key, attrs):
    st, got = resolve_name(name)
    assert st.key == key and got == attrs


@pytest.mark.parametrize("name", ["šafran", "lovorov list", "brašno mekano", ""])
def test_resolve_name_unknown(name):
    with pytest.raises(IngredientError):
        resolve_name(name)


@pytest.mark.parametrize("key,amount,unit,expected", [
    ("brasno", 0.5, "kg", (500, "g")),
    ("brasno", 25, "dag", (250, "g")),
    ("mlijeko", 0.5, "l", (500, "ml")),
    ("mlijeko", 2, "dl", (200, "ml")),
    ("jaja", 3, "kom", (3, "kom")),
    ("luk", 2, "kom", (300, "g")),  # piece_g 150
    ("cesnjak", 3, "režanj", (15, "g")),
    ("secer", 1, "žlica", (15, "g")),
    ("ulje", 2, "žlica", (30, "ml")),
    ("vanilin_secer", 1, "vrećica", (1, "vrecica")),
    ("kvasac", 14, "g", (2, "vrecica")),
])
def test_to_base(key, amount, unit, expected):
    qty, base, _ = to_base(amount, unit, S[key])
    assert (pytest.approx(qty), base) == (expected[0], expected[1])


@pytest.mark.parametrize("key,amount,unit", [("brasno", 2, "šalica"), ("brasno", 3, "kom"), ("brasno", 0, "g")])
def test_to_base_errors(key, amount, unit):
    with pytest.raises(IngredientError):
        to_base(amount, unit, S[key])


# --- odabir proizvoda (čista funkcija) -------------------------------------------

def row(pid, price, amount=None, unit="g", **kw):
    return {"product_id": pid, "price_eff": price, "pack_amount": amount, "pack_unit": unit if amount else None,
            "price_per_unit": kw.pop("ppu", None), "per_unit": kw.pop("per_unit", "kg"), **kw}


def test_smallest_covering_pack():
    rows = [row("1kg", 0.79, 1000), row("2kg", 1.49, 2000), row("500g", 0.55, 500)]
    pick = choose_product(rows, 700, "g", "kg", loose=False)
    assert pick["product_id"] == "1kg" and pick["n_packs"] == 1
    assert pick["cost_pack"] == 0.79 and pick["cost_used"] == pytest.approx(0.55, abs=0.01)


def test_cheapest_per_unit_when_nothing_covers():
    rows = [row("1kg", 0.79, 1000), row("2kg", 1.40, 2000)]
    pick = choose_product(rows, 5000, "g", "kg", loose=False)
    assert pick["product_id"] == "2kg" and pick["n_packs"] == 3 and pick["cost_pack"] == pytest.approx(4.20)


def test_flagged_avoided_unless_nothing_else():
    rows = [row("snizenje", 0.30, 1000, clearance=True), row("normal", 0.80, 1000)]
    assert choose_product(rows, 500, "g", "kg")["product_id"] == "normal"
    only = choose_product([rows[0]], 500, "g", "kg")
    assert only["product_id"] == "snizenje" and only["fallback"] and only["flags"] == ["clearance"]
    for flag in ({"price_suspect": True}, {"pack_confidence": "low"}, {"data_quality": "suspect"}):
        assert choose_product([row("x", 0.5, 1000, **flag), row("ok", 0.9, 1000)], 500, "g", "kg")["product_id"] == "ok"


def test_drained_mass_used_for_cans():
    can = row("grah", 1.19, 800, drained_amount=460)
    pick = choose_product([can], 400, "g", "kg", loose=False)
    assert pick["qty"] == 460 and "ocijeđena masa" in pick["notes"]


def test_by_weight_only_for_loose_or_variable_weight():
    loose = row("banana", 0, None, ppu=1.59)
    assert choose_product([loose], 300, "g", "kg", loose=True)["cost_pack"] == pytest.approx(0.48)
    assert choose_product([loose], 300, "g", "kg", loose=False) is None
    deli = row("grana", 0, None, ppu=22.0, variable_weight=True)
    assert choose_product([deli], 50, "g", "kg", loose=False)["cost_pack"] == pytest.approx(1.10)


def test_count_and_sachets():
    eggs = [row("10", 2.45, n_units=10), row("6", 1.59, n_units=6)]
    assert choose_product(eggs, 3, "kom", None)["product_id"] == "6"
    yeast = [row("5x7", 1.20, n_units=5), row("1x7", 0.29, n_units=1)]
    assert choose_product(yeast, 2, "vrecica", None)["product_id"] == "5x7"


# --- plan_basket (fixture) ---------------------------------------------------------

BASIC = [
    {"name": "brašno glatko", "amount": 500, "unit": "g"},
    {"name": "mlijeko", "amount": 1, "unit": "l"},
    {"name": "banana", "amount": 300, "unit": "g"},
    {"name": "šafran", "amount": 1, "unit": "g"},
]


def test_plan_basket_osijek(con):
    res = plan_basket(BASIC, "osijek", con=con)
    assert res["city"] == "Osijek" and res["date"] == "2026-10-19" and res["date_hr"] == "19.10.2026."
    assert res["unmatched"] == [{"name": "šafran", "reason": "nepoznata namirnica 'šafran' (nema je u staples.yaml)"}]
    assert [i["staple"] for i in res["ingredients"]] == ["brasno", "mlijeko", "banana"]
    best = res["best_store"]
    assert best["n_matched"] == 2 and best["n_ingredients"] == 3 and len(best["missing"]) == 1
    assert best["total"] == pytest.approx(sum(i["counted"] for i in best["items"]))
    for s in res["stores"]:
        assert s["date_hr"] == "19.10.2026."
        assert s["city"] == "Osijek" or s["scope"] == "national"
    # najbolja: najviše povezanih sastojaka, zatim najmanji zbroj
    top = [s for s in res["stores"] if s["n_matched"] == best["n_matched"]]
    assert best["total"] == min(s["total"] for s in top)


def test_plan_basket_avoids_clearance(con):
    res = plan_basket([{"name": "banana", "amount": 300, "unit": "g"}], "Osijek", con=con)
    ntl = next(s for s in res["stores"] if s["chain"] == "ntl")  # Plodine (fixture) ima jeftiniju bananu
    item = ntl["items"][0]
    assert item["product_id"] == "245063"  # "BANANA", a ne "BANANA SNIŽENJE"
    assert item["n_packs"] is None and item["unit_confidence"] == "low" and item["pack_source"] == "unit_price"


def test_plan_basket_brasno_smallest_pack(con):
    res = plan_basket([{"name": "brašno glatko", "amount": 500, "unit": "g"}], "Osijek", con=con)
    qty = {s["chain"]: s["items"][0]["pack_qty"] for s in res["stores"]}
    # 1 kg je najmanje pakiranje koje pokriva 500 g; Lidl u fixtureu ima samo 3 kg i 4x1 kg
    assert qty == {"konzum": 1000, "ntl": 1000, "spar": 1000, "roto": 1000, "eurospin": 1000, "lidl": 3000,
                   "plodine": 1000}  # Plodine: skupina hrana naslijeđena preko EAN-a


def test_unknown_city_suggestions(con):
    res = plan_basket(BASIC, "Osjek", con=con)
    assert res["stores"] == [] and "Osijek" in res["city_suggestions"]


def test_ambiguous_form_without_products_warns(con):
    res = plan_basket([{"name": "grah", "amount": 400, "unit": "g"}], "Osijek", con=con)
    assert any("nijedan oblik" in w for w in res["warnings"])
    bad = plan_basket([{"name": "grah", "amount": 400, "unit": "g", "form": "zamrznut"}], "Osijek", con=con)
    assert "nepoznat oblik" in bad["unmatched"][0]["reason"]


def test_only_single_store_mode(con):
    with pytest.raises(ValueError):
        plan_basket(BASIC, "Osijek", mode="multi_store", con=con)


@pytest.mark.parametrize("path", sorted(RECIPES.glob("test_*.json")))
def test_recipes_resolve_and_run(path, con):
    recipe = json.loads(path.read_text(encoding="utf-8"))
    unknown = {"lovorov list", "bosiljak"}
    for item in recipe["ingredients"]:
        if item["name"] in unknown:
            continue
        st, _ = resolve_name(item["name"])
        to_base(item["amount"], item["unit"], st)
    res = plan_basket(recipe["ingredients"], "Osijek", con=con)
    assert {u["name"] for u in res["unmatched"]} <= unknown
    assert len(res["ingredients"]) + len(res["unmatched"]) == len(recipe["ingredients"])


def test_three_recipes_exist():
    assert len(list(RECIPES.glob("test_*.json"))) == 3


# --- get_prices: id klase ----------------------------------------------------------

def test_get_prices_class_id(con, monkeypatch):
    by_type = dict(S, brasno=replace(S["brasno"], group_by=("tip",)))
    monkeypatch.setattr(search, "load_staples", lambda *a, **k: by_type)
    rows = search.get_prices("brasno:ostro", con=con)
    assert {r["product_id"] for r in rows} == {"04030162"}
    with pytest.raises(ValueError):
        search.get_prices("brasno:mekano", con=con)


def test_get_prices_egg_class_runs(con):
    assert search.get_prices("jaja:m", con=con) == []  # fixture nema jaja, ali id klase je valjan


def test_get_prices_two_level_class_id(con, monkeypatch):
    two = dict(S, brasno=replace(S["brasno"], group_by=("tip", "vrsta")))
    monkeypatch.setattr(search, "load_staples", lambda *a, **k: two)
    assert search.get_prices("brasno:ostro", con=con)  # samo prvi atribut
    with pytest.raises(ValueError):
        search.get_prices("brasno:ostro:kokosovo", con=con)
