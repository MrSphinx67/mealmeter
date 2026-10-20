import pytest

from mealmeter.search import find_products, get_prices, resolve_city

PODRAVKA_1KG = "3850104223624"


def q(con, sql, *params):
    return con.execute(sql, list(params)).fetchall()


# --- build_clean ---------------------------------------------------------------


def test_dedup_counts(built):
    con, stats = built
    dedup = {chain: (n_raw, n_clean) for chain, n_raw, n_clean, _ in stats["dedup"]}
    assert dedup["eurospin"] == (12, 4)  # svaki red 3x
    assert dedup["lidl"][0] - dedup["lidl"][1] > 0
    assert dedup["roto"] == (2, 1)  # red s cijenom 0.00 izbačen
    assert q(con, """SELECT count(*) FROM (SELECT chain, store_id, product_id FROM clean.prices
                     GROUP BY ALL HAVING count(*) > 1)""") == [(0,)]


def test_price_eff_rule(con):
    # Eurospin: price je redovna, special niža -> price_eff = special
    row = q(con, """SELECT price, special_price, price_eff, is_special FROM clean.prices
                    WHERE chain = 'eurospin' AND product_id = '001761601' AND store_id = '310017'""")
    assert [tuple(map(str, r)) for r in row] == [("3.15", "2.69", "2.69", "True")]
    # Konzum: price je već snižena i jednaka special
    row = q(con, """SELECT price, special_price, price_eff FROM clean.prices
                    WHERE chain = 'konzum' AND product_id = '01310151' AND store_id = '0907'""")
    assert row and row[0][0] == row[0][1] == row[0][2]


def test_zero_to_null(con):
    # Eurospin special_price / best_price_30 = 0.00 u sirovim podacima
    assert q(con, """SELECT special_price, best_price_30, is_special FROM clean.prices
                     WHERE chain = 'eurospin' AND product_id = '900006101' LIMIT 1""") == [(None, None, False)]


def test_ean_norm(con):
    rows = q(con, "SELECT DISTINCT ean_norm, ean_valid, ean_global FROM clean.products WHERE barcode = '11210000018'")
    assert rows == [("0011210000018", True, True)]
    rows = q(con, "SELECT ean_norm, ean_valid FROM clean.products WHERE chain = 'ntl' AND product_id = '245063'")
    assert rows == [(None, False)]  # BANANA, PLU "1570"


def test_pack_and_price_per_unit(con):
    row = q(con, """SELECT p.pack_amount, p.pack_unit, p.pack_source, c.price_per_unit, c.per_unit, c.unit_confidence
                    FROM clean.prices c JOIN clean.products p USING (chain, product_id)
                    WHERE c.chain = 'lidl' AND c.product_id = '6907930' AND c.store_id = '105'""")
    amount, unit, source, ppu, per_unit, conf = row[0]
    assert (amount, unit, source, per_unit, conf) == (3000, "g", "unit", "kg", "high")
    # Banana nema gramaturu -> cijena po kg iz unit_price lanca
    row = q(con, """SELECT per_unit, unit_confidence FROM clean.prices
                    WHERE chain = 'ntl' AND product_id = '245063' LIMIT 1""")
    assert row == [("kg", "low")]


def test_stores_clean(con):
    assert q(con, "SELECT address FROM clean.stores WHERE chain = 'spar'") == [("Kneza Trpimira 14",)]
    assert q(con, "SELECT scope, city FROM clean.stores WHERE chain = 'dm'") == [("national", None)]
    assert q(con, "SELECT DISTINCT city_canonical FROM clean.stores WHERE city = 'Sesvete'") == [("Zagreb",)]


def test_name_norm(con):
    assert q(con, "SELECT name_norm FROM clean.products WHERE chain = 'spar'") == [("bras ps glatko t 550 pod 1 kg",)]


# --- find_products -------------------------------------------------------------


def test_find_groups_by_ean(con):
    res = find_products("brašno glatko", con=con)
    top = res[0]
    assert top["id"] == PODRAVKA_1KG
    assert top["n_chains"] == 5  # konzum, ntl, spar, roto, plodine (bez kategorije, hrana preko EAN-a)
    assert top["pack"] == "1 kg"
    assert top["per_unit"] == "kg" and top["unit_confidence"] == "high"
    assert top["date"] == "2026-10-19" and top["date_hr"] == "19.10.2026."


def test_output_has_confidence_and_source(con):
    top = next(r for r in find_products("brasno glatko", con=con) if r["id"] == PODRAVKA_1KG)
    assert (top["unit_confidence"], top["pack_source"]) == ("high", "name")
    banana = find_products("banana", con=con)[0]
    assert (banana["unit_confidence"], banana["pack_source"]) == ("low", "unit_price")
    rows = get_prices("lidl:6907930", con=con)
    assert {(r["unit_confidence"], r["pack_source"]) for r in rows} == {("high", "unit")}


def test_chain_quality(con):
    assert q(con, "SELECT chain, data_quality FROM clean.chains WHERE data_quality <> 'ok'") == []  # fixture nema Lorenca
    assert all(r["data_quality"] == "ok" for r in get_prices(PODRAVKA_1KG, con=con))


def test_find_ignores_diacritics_and_case(con):
    a = find_products("BRASNO glatko", con=con)
    b = find_products("brašno GLATKO", con=con)
    assert [r["id"] for r in a] == [r["id"] for r in b]


def test_find_city_filter(con):
    res = find_products("brasno glatko", city="osijek", con=con)
    top = next(r for r in res if r["id"] == PODRAVKA_1KG)
    assert top["n_chains"] == 5 and top["n_stores"] == 5  # po jedna trgovina u Osijeku
    # Jastrebarsko nema konzum/ntl/spar/roto -> Podravka se ne pojavljuje
    assert all(r["id"] != PODRAVKA_1KG for r in find_products("brasno glatko", city="Jastrebarsko", con=con))


def test_find_city_alias(con):
    # Sesvete -> Zagreb: pretraga za Zagreb uključuje trgovine iz Sesveta, a "Sesvete" je isto što i Zagreb
    zg = next(r for r in find_products("brasno glatko", city="Zagreb", con=con) if r["id"] == PODRAVKA_1KG)
    sesvete = next(r for r in find_products("brasno glatko", city="SESVETE", con=con) if r["id"] == PODRAVKA_1KG)
    assert zg["n_stores"] == 3  # konzum Zagreb, konzum Sesvete, ntl Sesvete
    assert sesvete["n_stores"] == zg["n_stores"]


def test_find_matches_abbreviated_names_via_ean(con):
    # Spar zove proizvod "BRAŠ.PŠ.GLATKO T-550 POD 1 kg", ali dijeli EAN s Podravkom
    top = next(r for r in find_products("brasno glatko", con=con) if r["id"] == PODRAVKA_1KG)
    assert "spar" in top["chains"]


def test_find_national_scope(con):
    # HiPP je u dm-ovoj kategoriji "bebe & djeca" (food_group djeca), pa samo uz include_nonfood
    assert find_products("hipp", city="Osijek", con=con) == []
    res = find_products("hipp", city="Osijek", con=con, include_nonfood=True)
    assert len(res) == 1 and res[0]["chains"] == "dm" and "note" in res[0]


def test_find_fresh_without_ean(con):
    res = find_products("banana", con=con)
    assert res and res[0]["ean"] is None and res[0]["id"].startswith("ntl:")


def test_find_empty_query(con):
    assert find_products("  ", con=con) == []


# --- get_prices ----------------------------------------------------------------


def test_get_prices_by_ean(con):
    res = get_prices(PODRAVKA_1KG, city="Osijek", con=con)
    assert {r["chain"] for r in res} == {"konzum", "ntl", "spar", "roto", "plodine"}
    assert [r["price_eff"] for r in res] == sorted(r["price_eff"] for r in res)
    assert all(r["date_hr"] == "19.10.2026." and r["scope"] == "local" for r in res)


def test_get_prices_accepts_short_upc(con):
    assert {r["chain"] for r in get_prices("11210000018", con=con)} == {"konzum", "lidl", "ntl"}


def test_get_prices_by_chain_id_and_special(con):
    res = get_prices("eurospin:001761601", con=con)
    assert len(res) == 2 and all(r["is_special"] and r["price_eff"] == 2.69 for r in res)


def test_get_prices_national(con):
    assert get_prices("dm:1000105", city="Osijek", con=con) == []  # djeca: neprehrambeno
    res = get_prices("dm:1000105", city="Osijek", con=con, include_nonfood=True)
    assert len(res) == 1 and res[0]["scope"] == "national" and "note" in res[0]


def test_get_prices_rejects_bad_ids(con):
    with pytest.raises(ValueError):
        get_prices("3850104223625", con=con)  # kriva kontrolna znamenka
    with pytest.raises(ValueError):
        get_prices("2111111012450", con=con)  # in-store kod


def test_resolve_city(con):
    assert resolve_city("OSIJEK", con=con) == "Osijek"
    assert resolve_city("sesvete", con=con) == "Zagreb"
    assert resolve_city("Atlantida", con=con) is None
