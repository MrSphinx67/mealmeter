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
    ("P14", "GRAŠAK SUHI ZELENI 500 g", "ko", {K: 1.49}),
    # Korak 5B.4: nove namirnice
    ("P15", "PAPAR CRNI U ZRNU 50 g", "ko", {K: 0.89}),
    ("P16", "PAPRIKA SLATKA MLJEVENA 100 g", "ko", {K: 1.29}),
    ("P17", "PAPRIKA LJUTA MLJEVENA 100 g", "ko", {K: 1.09}),
    ("P18", "ORIGANO 10 g KOTANYI", "ko", {K: 0.99, L: 0.79}),
    ("P19", "BOSILJAK SUŠENI 10 g", "ko", {K: 0.99}),
    ("P20", "LOVOROV LIST 5 g", "ko", {K: 0.69, L: 0.59}),
    ("P21", "KOBASICA SLAVONSKA DIMLJENA 400 g", "ko", {K: 3.99}),
    ("P22", "KOBASICA SVJEŽA ZA ROŠTILJ 400 g", "ko", {K: 2.99, L: 2.49}),
    ("P23", "PANCETA DIMLJENA NAREZANA 100 g", "ko", {K: 1.79, L: 1.49}),
    ("P24", "SIR PARMIGIANO REGGIANO 200 g", "ko", {K: 4.99}),
    ("P25", "SIR GRANA PADANO 200 g", "ko", {L: 3.49}),
    # Korak 5B.7: alternative na istu količinu
    ("P26", "NUTELLA 400 g", "ko", {K: 4.49}),
    ("P27", "LINO LADA GOLD 350 g", "ko", {K: 3.49}),
    # Korak 5P.0: jeftinija kobasica druge vrste
    ("P28", "PILEĆA POSEBNA KOBASICA 400 g", "ko", {K: 1.59}),
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


# --- 3. prinos oblika -------------------------------------------------------------------------------------

def test_yields_data():
    from mealmeter import units

    for key in ("grah", "leca", "slanutak", "grasak"):
        assert units.yield_factor(key, "suho") == 2.5
    assert units.yield_factor("grasak", "smrznuto") is None and units.yield_factor("grasak", "konzerva") is None
    raw = __import__("yaml").safe_load(units.YIELDS_PATH.read_text(encoding="utf-8"))
    assert all(v["suho"]["estimate"] is True for v in raw.values())


def test_peas_ready_to_dry(con5b):
    res = plan_basket([{"name": "grašak", "amount": 800, "unit": "g"}], "Osijek", con=con5b)
    opts = {o["form"]: o for o in res["ask_user"][0]["options"]}
    assert opts["suho"]["amount"] == pytest.approx(320) and opts["smrznuto"]["amount"] == pytest.approx(800)
    assert all(o["price_note"].endswith("za traženu količinu gotovog proizvoda") for o in opts.values())
    res = plan_basket([{"name": "grašak", "amount": 800, "unit": "g", "form": "suho"}], "Osijek", con=con5b)
    ing = res["ingredients"][0]
    assert ing["amount"] == pytest.approx(320) and any("prinos 2.5x" in w for w in ing["warnings"])
    res = plan_basket([{"name": "grašak", "amount": 800, "unit": "g", "form": "smrznuto"}], "Osijek", con=con5b)
    assert res["ingredients"][0]["amount"] == pytest.approx(800)


# --- 4. nove namirnice -----------------------------------------------------------------------------------

@pytest.mark.parametrize("key,name,attrs", [
    ("origano", "ORIGANO 10 g KOTANYI", {}),
    ("bosiljak", "BOSILJAK SUŠENI 10 g", {"oblik": "suhi"}),
    ("lovorov_list", "LOVOROV LIST 5 g", {}),
    ("papar", "PAPAR CRNI 50 g", {"oblik": "mljeveni", "vrsta": "crni"}),
    ("papar", "PAPAR CRNI U ZRNU 50 g", {"oblik": "zrno"}),
    ("mljevena_paprika", "PAPRIKA MLJEVENA 100 g", {"vrsta": "slatka"}),
    ("mljevena_paprika", "PAPRIKA DIMLJENA SLATKA MLJEVENA 70 g", {"vrsta": "dimljena"}),
    ("kobasica", "KOBASICA SLAVONSKA DIMLJENA 400 g", {"vrsta": "dimljena"}),
    ("kobasica", "KULEN SLAVONSKI 400 g", {"vrsta": "kulen"}),
    ("kobasica", "PARIZER 500 g", {"vrsta": "posebna"}),
    ("kobasica", "KOBASICA SVJEŽA ZA ROŠTILJ 400 g", {"vrsta": "svjeza"}),
    ("slanina", "PANCETA DIMLJENA NAREZANA 100 g", {"oblik": "narezana"}),
    ("tvrdi_sir_talijanski", "SIR GRANA PADANO 200 g", {"vrsta": "grana_padano"}),
    ("tvrdi_sir_talijanski", "SIR PARMIGIANO REGGIANO 200 g", {"vrsta": "parmigiano_reggiano"}),
])
def test_new_staples_match(key, name, attrs):
    from mealmeter.staples import extract_attributes, load_staples, name_match

    st = load_staples()[key]
    assert name_match(st, name) == "match"
    got = extract_attributes(st, name)
    assert {a: got.get(a) for a in attrs} == attrs


@pytest.mark.parametrize("key,name", [
    ("papar", "Mljeveni kajenski papar / Chili"), ("papar", "PAPAR LJUTI CHILI 50 g"),
    ("kobasica", "GRAH S KOBASICAMA 400 g"), ("kobasica", "PIZZA S KOBASICOM"), ("bosiljak", "PESTO BOSILJAK 190 g"),
    ("origano", "UMAK ZA PIZZU S ORIGANOM"), ("lovorov_list", "ULJE LOVOR 50 ml"),
])
def test_new_staples_excluded(key, name):
    from mealmeter.staples import load_staples, name_match

    assert name_match(load_staples()[key], name) in ("excluded", None)


def _item(con, name, amount, unit, chain, **extra):
    store = {"chain": chain, "address_contains": ""}
    res = plan_basket([{"name": name, "amount": amount, "unit": unit, **extra}], "Osijek", con=con, store=store)
    return res["best_store"]["items"][0]


def test_new_staples_in_basket(con5b):
    assert _item(con5b, "papar", 2, "g", "konzum")["product_id"] == "P7"  # mljeveni zadano, iako je zrno jeftiniji
    assert _item(con5b, "papar", 2, "g", "konzum", attributes={"oblik": "zrno"})["product_id"] == "P15"
    assert _item(con5b, "mljevena paprika", 5, "g", "konzum")["product_id"] == "P16"  # slatka zadano
    assert _item(con5b, "ljuta paprika", 5, "g", "konzum")["product_id"] == "P17"
    lovor = _item(con5b, "lovorov list", 2, "list", "konzum")
    assert lovor["product_id"] == "P20" and lovor["need"] == pytest.approx(0.4)
    assert _item(con5b, "origano", 2, "g", "lidl")["product_id"] == "P18"
    assert _item(con5b, "panceta", 100, "g", "lidl")["product_id"] == "P23"
    for key in ("origano", "bosiljak", "lovorov_list"):
        assert load_staples()[key].pantry


def test_sausage_default_smoked_or_confirm(con5b):
    k = _item(con5b, "kobasica", 400, "g", "konzum")
    assert k["product_id"] == "P21" and not k.get("needs_confirmation")
    lidl = _item(con5b, "kobasica", 400, "g", "lidl")
    assert lidl["product_id"] == "P22" and lidl["needs_confirmation"] and "dimljena" in lidl["confirm_note"]


def test_italian_cheese_substitution(con5b):
    k = _item(con5b, "parmezan", 40, "g", "konzum")
    assert k["product_id"] == "P24" and "substitution" not in k
    lidl = _item(con5b, "parmezan", 40, "g", "lidl")
    assert lidl["product_id"] == "P25" and lidl["substitution"]["chosen"] == "SIR GRANA PADANO 200 g"
    assert "Grana Padano" in lidl["substitution"]["note"]
    assert "substitution" not in _item(con5b, "grana padano", 40, "g", "lidl")


from mealmeter.staples import load_staples  # noqa: E402


# --- 5. free_text: sinonimi i najbliži kandidati -------------------------------------------------------------

def test_free_text_synonyms(con5b):
    from mealmeter.basket import load_synonyms

    assert load_synonyms()["dimljena kobasica"] == ("slavonska kobasica", "kulen", "suha kobasica")
    res = plan_basket([{"name": "domaća kobasica", "amount": 400, "unit": "g", "free_text": True}], "Osijek",
                      con=con5b, store={"chain": "konzum", "address_contains": ""})
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "P21" and item["match_quality"] == "free_text"
    assert any("traženo kao 'slavonska kobasica'" in w for w in res["warnings"])


def test_free_text_near_candidates(con5b):
    res = plan_basket([{"name": "kobasica tartufata", "amount": 200, "unit": "g", "free_text": True}], "Osijek",
                      con=con5b)
    u = res["unmatched"][0]
    assert u["tried_synonyms"] == [] and 1 <= len(u["candidates"]) <= 3
    assert all(c["reason"] and c["name"] for c in u["candidates"])
    assert any("nema: tartufata" in c["reason"] for c in u["candidates"])


# --- 6. pretpostavke --------------------------------------------------------------------------------------

def test_assumptions_for_missing_amounts(con5b):
    ing = [{"name": "špageti", "amount": 400, "unit": "g"}, {"name": "parmezan"},
           {"name": "sol", "unit": "po ukusu"}, {"name": "lovorov list", "amount": 0}]
    res = plan_basket(ing, "Osijek", con=con5b, store={"chain": "konzum", "address_contains": ""})
    got = {a["ingredient"]: (a["amount"], a["unit"], a["text"]) for a in res["assumptions"]}
    assert got == {"parmezan": (40, "g", "40 g za posipanje"), "sol": (5, "g", "5 g (žličica) po ukusu"),
                   "lovorov list": (2, "kom", "2 lista")}
    items = {it["ingredient"]: it for it in res["best_store"]["items"]}
    assert items["parmezan"]["need"] == 40 and items["lovorov list"]["need"] == pytest.approx(0.4)
    # namirnica bez pretpostavke: jasan razlog
    res = plan_basket([{"name": "špageti"}], "Osijek", con=con5b)
    assert "količina nije navedena" in res["unmatched"][0]["reason"] and res["assumptions"] == []


# --- 7. alternative na istu količinu -----------------------------------------------------------------------

def test_alternative_delta_on_needed_amount(con5b):
    res = plan_basket([{"name": "nutella", "amount": 300, "unit": "g"}], "Osijek", con=con5b,
                      store={"chain": "konzum", "address_contains": ""}, alternatives=True)
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "P26" and item["cost_used"] == round(4.49 / 400 * 300, 2)  # 3,37
    lino = next(a for a in item["alternatives"] if a["product_id"] == "P27")
    # cijela pakiranja: 3,49 - 4,49 = -1,00; za potrebnih 300 g: 2,99 - 3,37 = -0,38
    assert lino["cost_used"] == round(3.49 / 350 * 300, 2) and lino["delta_eur"] == -0.38 and lino["cheaper"]
    assert lino["size_note"] == "usporedba za 300 g: pakiranje 350 g, odabrano 400 g"


def test_compare_chains_overflow_and_major_without_items():
    from collections import Counter

    from mealmeter.basket import compare_chains

    def store(chain, total, n=2, missing=()):
        return {"chain": chain, "total_to_buy": total, "total_used": total / 2, "n_matched": n, "missing": list(missing),
                "address": f"{chain} 1", "addresses": [f"{chain} 1", f"{chain} 2", f"{chain} 3"]}
    ranked = [store(c, i + 1.0) for i, c in enumerate(["a", "b", "c", "d", "e", "f", "g"])] + [store("h", 9, 1, ["x"])]
    rows, incomplete, more = compare_chains(ranked, Counter(), 2, city_chains={"studenac", "a"})
    assert [r["chain"] for r in rows] == ["a", "b", "c", "d", "e", "f"] and all(len(r["addresses"]) == 2 for r in rows)
    assert more == [{"chain": "g", "total_to_buy": 7.0, "n_matched": 2}]
    assert [(i["chain"], i["note"]) for i in incomplete] == [("h", "nedostaje: x"), ("studenac", "nedostaje: ")]
