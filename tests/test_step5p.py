"""Korak 5P: alternative iste vrste, zlatni izlazi, sažeta baza."""

from mealmeter.basket import kind_note, plan_basket
from tests.test_step5b import con5b  # noqa: F401  (fixture)


# --- 0. alternative iste vrste ------------------------------------------------------------------------------

def test_sausage_alternative_other_kind_has_note(con5b):  # noqa: F811
    res = plan_basket([{"name": "kobasica", "amount": 400, "unit": "g"}], "Osijek", con=con5b,
                      store={"chain": "konzum", "address_contains": ""}, alternatives=True)
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "P21" and item["attributes"]["vrsta"] == "dimljena"
    for alt in item["alternatives"]:
        if alt["product_id"] in ("P22", "P28"):
            assert alt.get("note", "").startswith("nije dimljena"), alt
    posebna = [a for a in item["alternatives"] if a["product_id"] == "P28"]
    assert posebna and posebna[0]["note"] == "nije dimljena (posebna)"


def test_kind_note():
    assert kind_note({"vrsta": "dimljena"}, {"vrsta": "dimljena"}) is None
    assert kind_note({"vrsta": "dimljena"}, {"vrsta": "posebna"}) == "nije dimljena (posebna)"
    assert kind_note({"vrsta": "dimljena"}, {}) == "nije označeno kao dimljena"
    assert kind_note({"vrsta": "nepoznato"}, {"vrsta": "kulen"}) is None and kind_note({}, {"vrsta": "x"}) is None


# --- 1. zlatni izlazi (stvarna baza; samo uz MM_GOLDEN=1, jer ovise o učitanom cjeniku) --------------------

import os  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_outputs():
    import importlib.util
    from pathlib import Path

    spec = importlib.util.spec_from_file_location("golden", Path(__file__).parents[1] / "scripts" / "golden.py")
    golden = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(golden)
    diffs = golden.check(os.environ.get("MM_DB"), verbose=False)
    assert not {k: v for k, v in diffs.items() if v}


def test_golden_files_present():
    from pathlib import Path

    files = sorted((Path(__file__).parent / "golden").glob("*.json"))
    assert len(files) == 20
    kinds = {f.name.split("_")[0] for f in files}
    assert kinds == {"find", "prices", "basket"}


# --- 2. sažeta baza: isti izlazi kao puna (fixture baza) ---------------------------------------------------

def test_compact_db_same_outputs(tmp_path):
    import importlib.util
    import json
    from pathlib import Path

    import duckdb

    from mealmeter import server as srv
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    full = tmp_path / "full.duckdb"
    c = duckdb.connect(str(full))
    load_raw(c, FIXTURE, "2026-10-19")
    # dvije Konzumove trgovine u Osijeku: ista cijena (osnovni redak) i druga cijena (iznimka)
    c.execute("""INSERT INTO stores SELECT chain, '0908', type, 'Vukovarska 1', city, zipcode FROM stores
                 WHERE chain = 'konzum' AND store_id = '0907'""")
    c.execute("""INSERT INTO prices SELECT chain, '0908', product_id, price + 0.10, unit_price, best_price_30,
                 anchor_price, special_price, date FROM prices WHERE chain = 'konzum' AND store_id = '0907'""")
    build_clean(c)
    c.close()
    spec = importlib.util.spec_from_file_location("bc", Path(__file__).parents[1] / "scripts" / "build_compact.py")
    bc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bc)
    counts = bc.build(full, tmp_path / "compact.duckdb")
    assert counts["price_exceptions"] > 0 and counts["store_products"] > 0

    pancakes = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
                {"name": "jaja", "amount": 3, "unit": "kom"}]
    calls = [("plan_basket", dict(ingredients=pancakes, city="Osijek", detail=True)),
             ("find_products", dict(ingredient="brašno", city="Osijek")),
             ("get_prices", dict(product_id="3850104223624")), ("list_stores", dict(city="Osijek"))]
    state = (srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key)
    try:
        outs = []
        for db in (full, tmp_path / "compact.duckdb"):
            srv.create_server(db_path=str(db))
            outs.append([json.loads(srv._dumps(getattr(srv, name)(**args))) for name, args in calls])
    finally:
        srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key = state
    assert outs[0] == outs[1]


# --- 4. predizračunate cijene po namirnici: isti rezultat kao preko svih cijena ----------------------------

def test_staple_prices_same_as_full_scan(con5b, monkeypatch):  # noqa: F811
    from mealmeter import basket, search

    assert search.has_staple_prices(con5b)
    n = con5b.execute("SELECT count(*) FROM clean.staple_prices").fetchone()[0]
    assert n and con5b.execute("SELECT count(*) FROM clean.staple_items").fetchone()[0]
    ing = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
           {"name": "jaja", "amount": 3, "unit": "kom"}, {"name": "kobasica", "amount": 400, "unit": "g"},
           {"name": "grašak", "amount": 800, "unit": "g"}]
    fast = (basket.plan_basket(ing, "Osijek", con=con5b, alternatives=True),
            search.find_products(ingredient="jaja", city="Osijek", con=con5b))
    monkeypatch.setattr(search, "has_staple_prices", lambda con: False)
    monkeypatch.setattr(basket, "has_staple_prices", lambda con: False)
    slow = (basket.plan_basket(ing, "Osijek", con=con5b, alternatives=True),
            search.find_products(ingredient="jaja", city="Osijek", con=con5b))
    assert fast == slow
