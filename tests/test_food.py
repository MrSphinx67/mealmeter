"""Filtar hrane (food.py): skupine, nasljeđivanje preko EAN-a, riječi i zadani filtar pretrage."""

import pytest

from mealmeter.basket import plan_basket
from mealmeter.food import chain_group, is_alcohol, load_category_map, words_group
from mealmeter.normalize import FOOD_GROUP_VALUES
from mealmeter.search import find_products, get_prices


def test_category_map_values():
    cmap = load_category_map()
    assert cmap and set(cmap.values()) <= set(FOOD_GROUP_VALUES)
    assert cmap["ostalo"] == "unknown" and cmap["hrana"] == "hrana"


@pytest.mark.parametrize("category,name,group", [
    ("PIĆE", "VINO CHARDONNAY 0,75L VEZAK", "alkohol"),
    ("PIĆE", "VODA SARA 1,5 l NEGAZIRANA", "pice"),
    ("Piće", "Karlovačko svijetlo pivo 5% 2l PET", "alkohol"),
    ("PIĆE", "BADEL DOMAĆI 35% 0,5L", "alkohol"),  # postotak alkohola u kategoriji pića
    ("PIĆE", "NEK.HAPPY DAY JAGODA 35% 1 L", "pice"),  # nektar s 35 % voća
    ("PIĆE", "Union Pivo Radler Isot.lim.0% 0,5L PB", "pice"),
    ("PJENUŠCI DOMAĆI", "PJENUŠAC FREIXENET 0,0% 0,75 L", "pice"),
    ("HRANA", "OCAT ALKOHOLNI 9% 1L", "hrana"),
    ("Ostalo", "SVRDLO SDS+ 8X210/150", "unknown"),
    (None, "BANANA SORTA CAVENDISH", "unknown"),
])
def test_chain_group(category, name, group):
    assert chain_group(category, name) == group


@pytest.mark.parametrize("name,group", [
    ("HRANA ZA PSE PLODINE 15 KG FRIENDS", "kucni_ljubimci"),
    ("BRAŠ.PŠE.GLATKO T-550 1KG", None),  # "pše" je pšenično, a ne psi
    ("PIVO OLD PRAGUE PSENICNO SVJETLO 5,2% 0,5 L", "alkohol"),
    ("KRUH S BUCINIM SJEMENKAMA 400 G", None),
    ("SJEME KUKURUZ SECERAC", "ostalo"),
    ("NIVEA SUN SENS.SPREJ ZA ZAŠ. SPF 50", "kozmetika"),
    ("ČAŠA ZA PIVO S TISKOM 500ML", "kucanstvo"),
    ("JOG.TEK.0.9% 500 G CASA VINDIJA", None),
    ("WHISKAS 12*100g", None),  # nije whisky
    ("S.BRIOCHE PECIVO S POSIPOM 120 G", None),  # nije pošip
    ("LAMP.MAJA MALA TOMISLAV (15 kom)", None),  # marke piva samo u kategoriji pića
    ("STOLICA JULIE GRAPHITE 61,5X58,5X79 CM", "ostalo"),
])
def test_words_group(name, group):
    assert words_group(name) == group


def test_is_alcohol_drink_only_rules():
    assert is_alcohol("TOMISLAV PIVO 0,5") and not is_alcohol("KOZEL BOCA 0,5L")
    assert is_alcohol("KOZEL BOCA 0,5L", drink=True)
    assert not is_alcohol("ČOKOLADA 70% 100G")  # postotak se gleda samo u kategoriji pića
    assert not is_alcohol("Vindija Legenda kefir 3,5%m.m.330g PET", drink=True)


# --- build (fixture) -------------------------------------------------------------

def _food(con, chain, pid):
    return con.execute("SELECT food_group, is_food, category_source FROM clean.products WHERE chain = ? AND product_id = ?",
                       [chain, pid]).fetchone()


def test_build_sources(con):
    assert _food(con, "konzum", "04030203") == ("hrana", True, "chain")
    # Plodine nemaju kategoriju: brašno nasljeđuje skupinu od istog EAN-a (Konzum, Spar...)
    assert _food(con, "plodine", "040151") == ("hrana", True, "ean_inherited")
    assert _food(con, "plodine", "689540") == ("kucni_ljubimci", False, "words")
    assert _food(con, "plodine", "100101") == ("unknown", None, "none")


def test_nonfood_kept_in_db(con):
    assert con.execute("SELECT count(*) FROM clean.products WHERE NOT is_food").fetchone()[0] > 0


def test_find_default_excludes_unverified(con):
    names = [r["name"] for r in find_products("banana", con=con)]
    assert "BANANA SORTA CAVENDISH" not in names and "BANANA CIPS BIO 150 G LIVE FREE ORGANIC" not in names
    res = find_products("banana", con=con, include_unverified=True)
    hit = next(r for r in res if r["name"] == "BANANA SORTA CAVENDISH")
    assert hit["food_unverified"] and hit["food_group"] == "unknown"
    assert all(not r["food_unverified"] for r in res if r["name"] != hit["name"] and "plodine" not in r["chains"])


def test_find_nonfood_flag(con):
    assert find_products("hrana za pse", con=con) == []
    res = find_products("hrana za pse", con=con, include_nonfood=True)
    assert res and res[0]["food_group"] == "kucni_ljubimci" and not res[0]["food_unverified"]


def test_find_inherited_ean_group_includes_plodine(con):
    res = find_products("brasno glatko", con=con)
    assert any("plodine" in r["chains"] for r in res)


def test_get_prices_unverified(con):
    assert get_prices("plodine:100101", con=con) == []
    rows = get_prices("plodine:100101", con=con, include_unverified=True)
    assert rows and rows[0]["food_unverified"]


def test_basket_loose_produce_allows_unverified(con):
    # Plodine banana nema kategoriju ni EAN, ali je svježe voće (riječ je prva u nazivu)
    res = plan_basket([{"name": "banana", "amount": 1, "unit": "kg"}], "Osijek", con=con)
    plodine = [s for s in res["stores"] if s["chain"] == "plodine"]
    assert plodine and plodine[0]["items"][0]["food_unverified"]
    assert plodine[0]["items"][0]["name"] == "BANANA SORTA CAVENDISH"


@pytest.mark.parametrize("name", ["HRANA ZA PSE FRISK.VITAL.S.500 g ALCA",
                                  "HRANA ZA MAČKE WHISKAS 85G TASTY MIX KREMASTA KREACIJA"])
def test_pet_food_in_food_category(name):
    assert chain_group("Hrana", name) == "kucni_ljubimci"


def test_learn_prefix_rules():
    """Korak 2E.11: prefiks šifre Plodina -> skupina, samo čisti prefiksi s dovoljno primjera."""
    import duckdb

    from mealmeter.food import learn_prefix_rules

    c = duckdb.connect()
    c.execute("CREATE SCHEMA clean")
    c.execute("CREATE TEMP TABLE food_final (chain VARCHAR, product_id VARCHAR, food_group VARCHAR, category_source VARCHAR)")
    rows = [("plodine", f"12{i:04d}", "hrana", "ean_inherited") for i in range(60)]  # čist prefiks
    rows += [("plodine", f"34{i:04d}", "hrana" if i % 2 else "kucanstvo", "ean_inherited") for i in range(60)]  # 50/50
    rows += [("plodine", f"56{i:04d}", "kozmetika", "ean_inherited") for i in range(10)]  # premalo primjera
    rows += [("plodine", "129999", "unknown", "none"), ("plodine", "349999", "unknown", "none"),
             ("plodine", "569999", "unknown", "none")]
    c.executemany("INSERT INTO food_final VALUES (?, ?, ?, ?)", rows)
    stats = learn_prefix_rules(c)
    got = dict(c.execute("SELECT product_id, food_group || '/' || category_source FROM food_final "
                         "WHERE product_id LIKE '%9999'").fetchall())
    assert got == {"129999": "hrana/prefix", "349999": "unknown/none", "569999": "unknown/none"}
    applied = {(pre, g) for _, pre, _, g, _, _, _, ok in stats if ok}
    assert ("12", "hrana") in applied and not any(pre.startswith(("34", "56")) for pre, _ in applied)
