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
        # jaja: kavezna i podna M iste cijene, jeftinija kavezna S, skuplja slobodna L
        ("konzum", "E1", "JAJA SVJEŽA KAVEZNI UZGOJ M 10/1", "HRANA", "ko", 1.99),
        ("konzum", "E2", "JAJA SVJEŽA PODNI UZGOJ M 10/1", "HRANA", "ko", 1.99),
        ("konzum", "E3", "JAJA KAVEZNI UZGOJ RAZRED S 10/1", "HRANA", "ko", 1.29),
        ("konzum", "E4", "JAJA SLOBODNI UZGOJ L 10/1", "HRANA", "ko", 2.49),
        ("lidl", "E5", "Jaja iz kaveznog uzgoja, razred M", "HRANA", "10komad", 0.89),
        ("lidl", "E6", "Jaja iz kaveznog uzgoja, razred S", "HRANA", "10komad", 0.79),
        # čokoladni namaz: Nutella samo u Konzumu
        ("konzum", "N1", "NUTELLA 400 g FERRERO", "HRANA", "ko", 4.49),
        ("konzum", "N2", "NAMAZ OD LJEŠNJAKA K PLUS 400 g", "HRANA", "ko", 1.99),
        ("lidl", "N3", "Namaz od lješnjaka", "HRANA", "400g", 2.99),
        # free_text: kikiriki maslac uz okus, grickalicu i porciju; sok kao piće
        ("konzum", "K1", "KIKIRIKI MASLAC 350 g", "HRANA", "ko", 2.99),
        ("konzum", "K2", "ZOE KIKIRIKI MASLAC ČOKO 250 g", "HRANA", "ko", 1.99),
        ("konzum", "K3", "SPORTNESS KOŠARICE KIKIRIKI MASLAC 42 g", "HRANA", "ko", 0.99),
        ("konzum", "K4", "KIKIRIKI MASLAC MINI 20 g", "HRANA", "ko", 0.49),
        ("konzum", "K5", "KIKIRIKI MASLAC CRUNCHY 1 kg", "HRANA", "ko", 6.99),
        ("konzum", "J1", "SOK JUICY ZMAJEVO VOĆE 1,5 L", "PIĆA", "ko", 1.99),
        # vrećice: Lidlova rinfuza 80 g i višestruko pakiranje 6x8g
        ("lidl", "V1", "Vanilin šećer", "HRANA", "80g", 0.39),
        ("lidl", "V2", "Dolcela Vanilin šećer", "HRANA", "6x8g", 0.99),
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


# --- 2. jaja ----------------------------------------------------------------------------------------------

EGGS = [{"name": "jaja", "amount": 3, "unit": "kom"}]


def test_eggs_default_m_l_better_than_cage(con4c):
    res = plan_basket(EGGS, "Osijek", con=con4c, store=KONZUM, alternatives=True)
    eggs = res["best_store"]["items"][0]
    # podna M i kavezna M su iste cijene: bira se bolji uzgoj; kavezna S je samo jeftinija alternativa
    assert eggs["product_id"] == "E2" and eggs["attributes"]["uzgoj"] == "podni"
    assert [(a["product_id"], a["note"]) for a in eggs["alternatives"]] == [("E3", "kavezni, S")]
    assert eggs["alternatives"][0]["cheaper"]


def test_eggs_only_cage_marked(con4c):
    lidl = {"chain": "lidl", "address_contains": ""}
    eggs = plan_basket(EGGS, "Osijek", con=con4c, store=lidl)["best_store"]["items"]
    # Lidl (fixture) nema jaja izvan kaveza: kavezna M je izbor (S tek kad nema ni M/L), uz napomenu
    assert eggs[0]["product_id"] == "E5" and "izvan zadanog izbora: kavezni" in eggs[0]["notes"]


def test_egg_price_per_piece_not_rounded(con4c):
    rows = dict(con4c.execute("""
        SELECT ps.product_id, c.price_eff / ps.n_units FROM clean.product_staples ps JOIN clean.prices c
        USING (chain, product_id) WHERE ps.staple = 'jaja' AND ps.product_id IN ('E5', 'E6')""").fetchall())
    assert float(rows["E5"]) == pytest.approx(0.089) and float(rows["E6"]) == pytest.approx(0.079)
    suspect = dict(con4c.execute("""SELECT product_id, unit_suspect FROM clean.product_staples
                                    WHERE staple = 'jaja' AND product_id IN ('E5', 'E6')""").fetchall())
    assert suspect == {"E5": False, "E6": True}  # 0,089 u granicama [0,08, 0,55], 0,079 ispod
    assert load_staples()["jaja"].plausible_by == {"uzgoj": {"bio": (0.30, 1.00), "_other": (0.08, 0.55)}}


# --- 3. marka u nazivu sastojka -----------------------------------------------------------------------------

NUTELLA = [{"name": "nutella", "amount": 300, "unit": "g"}]


def test_brand_preferred_in_store(con4c):
    item = plan_basket(NUTELLA, "Osijek", con=con4c, store=KONZUM)["best_store"]["items"][0]
    # Nutella je skuplja od namaza K PLUS, ali tražena je marka
    assert item["product_id"] == "N1" and "substitution" not in item


def test_brand_missing_substitution_and_other_store(con4c):
    res = plan_basket(NUTELLA, "Osijek", con=con4c, store={"chain": "lidl", "address_contains": ""}, alternatives=True)
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "N3"
    assert item["substitution"] == {"requested": "nutella", "brand": "Nutella", "chosen": "Namaz od lješnjaka"}
    other = [a for a in item["alternatives"] if a.get("other_store")]
    assert len(other) == 1 and other[0]["product_id"] == "N1" and other[0]["chain"] == "konzum"
    assert other[0]["delta_eur"] == 1.50 and not other[0]["cheaper"]
    # generički naziv: bez marke, najjeftiniji namaz
    generic = plan_basket([{"name": "čokoladni namaz", "amount": 300, "unit": "g"}], "Osijek", con=con4c, store=KONZUM)
    assert generic["best_store"]["items"][0]["product_id"] == "N2"


def test_brand_in():
    from mealmeter.basket import brand_in

    assert brand_in("nutella")[0] == "Nutella" and brand_in("Vegeta")[0] == "Vegeta"
    assert brand_in("mlijeko Dukat")[0] == "Dukat" and brand_in("čokoladni namaz") is None


# --- 4. free_text ------------------------------------------------------------------------------------------

def test_free_text_peanut_butter(con4c):
    ing = [{"name": "kikiriki maslac", "amount": 200, "unit": "g", "free_text": True}]
    res = plan_basket(ing, "Osijek", con=con4c, store=KONZUM, alternatives=True)
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "K1" and item["needs_confirmation"] and item["match_quality"] == "free_text"
    names = [c["name"] for c in item["candidates"]] + [a["name"] for a in item["alternatives"]]
    assert not any("ČOKO" in n or "SPORTNESS" in n or "MINI" in n for n in names)
    assert [c["product_id"] for c in item["candidates"]] == ["K1", "K5"] and item["candidates"][0]["cost_pack"] == 2.99
    assert res["ingredients"][0]["needs_confirmation"]


def test_free_ok():
    from mealmeter.basket import free_ok

    assert not free_ok("zoe kikiriki maslac coko 250 g", "kikiriki maslac")
    assert not free_ok("sportness kosarice kikiriki maslac 42 g", "kikiriki maslac")
    assert free_ok("kikiriki maslac 350 g", "kikiriki maslac")
    assert free_ok("tahini sezamova pasta 300 g", "tahini")
    assert free_ok("zoe kikiriki maslac coko 250 g", "kikiriki maslac coko")  # okus iz upita je dopušten


def test_unmatched_suggestions_without_drinks(con4c):
    assert con4c.execute("SELECT food_group FROM clean.products WHERE product_id = 'J1'").fetchone()[0] == "pice"
    res = plan_basket([{"name": "zmajevo voće", "amount": 100, "unit": "g", "free_text": True}], "Osijek", con=con4c)
    assert res["unmatched"] and not any("SOK" in s for s in res["unmatched"][0]["suggestions"])


# --- 5. vrećice iz rinfuze ---------------------------------------------------------------------------------

def test_bulk_sachet_share(con4c, capsys):
    lidl = {"chain": "lidl", "address_contains": ""}
    res = plan_basket([{"name": "vanilin šećer", "amount": 1, "unit": "vrećica"}], "Osijek", con=con4c, store=lidl)
    item = res["best_store"]["items"][0]
    print(f"{item['name']} | {item['pack_size']} | izvor gramature: {item['pack_source']}")
    assert item["product_id"] == "V1" and item["pack_source"] == "unit"
    assert item["pack_size"] == "80 g (≈ 10 vrećica od 8 g)"
    assert item["cost_pack"] == 0.39 and item["cost_used"] == round(1 * 8 / 80 * 0.39, 2)
    assert any("udio 8 g od 80 g" in n for n in item["notes"])
    # višestruko pakiranje vrećica ostaje po vrećici: 1 od 6
    rows = [it for it in plan_basket([{"name": "vanilin šećer", "amount": 3, "unit": "vrećica"}], "Osijek",
                                     con=con4c, store=lidl)["best_store"]["items"]]
    assert rows[0]["product_id"] in ("V1", "V2")
    from mealmeter.basket import bulk_sachets
    r = {"pack_unit": "g", "pack_amount": 48.0, "n_units": 6.0}
    bulk_sachets(r, load_staples()["vanilin_secer"])
    assert r["n_units"] == 6.0 and "bulk_sachet_g" not in r
    assert "Vanilin šećer | 80 g" in capsys.readouterr().out


# --- 7. dvosmislen sastojak: ask_user ------------------------------------------------------------------------

def test_ambiguous_ask_user(con4c):
    ing = [{"name": "grah", "amount": 500, "unit": "g"}, {"name": "šećer", "amount": 100, "unit": "g"}]
    res = plan_basket(ing, "Osijek", con=con4c, store=KONZUM)
    if not res["ambiguous"]:
        pytest.skip("fixture nema oba oblika graha u Osijeku")
    ask = res["ask_user"][0]
    assert ask["ingredient"] == "grah" and ask["question"].startswith("grah: ") and ask["question"].endswith("?")
    assert all(o["price_note"].endswith("za traženu količinu") and o["price_eur"] > 0 for o in ask["options"])
    best = res["best_store"]
    assert [it["staple"] for it in best["items"]] == ["secer"]  # ostali sastojci su izračunati
    assert res["summary_hr"].startswith("Bez graha: za kupiti ")
    assert f"{best['total_to_buy']:.2f}".replace(".", ",") in res["summary_hr"]


def test_summary_hr_without():
    from mealmeter.basket import summary_hr

    best = {"total_to_buy": 5.2, "total_used": 1.19}
    assert summary_hr(best, [], [{"ingredient": "grah", "genitive": "graha"}]) == \
        "Bez graha: za kupiti 5,20 €, stvarno utrošeno 1,19 €."
    assert summary_hr(best, [], [{"ingredient": "grah", "genitive": "graha"}, {"ingredient": "leća", "genitive": "leće"}]
                      ).startswith("Bez graha i leće:")
    assert summary_hr(best) == "Za kupiti: 5,20 €. Stvarno utrošeno: 1,19 €."
    assert load_staples()["grah"].genitive == "graha" and load_staples()["slanutak"].genitive == "slanutka"
