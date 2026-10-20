"""Korak 2F: lažni EAN-ovi, obavezni atributi, svježe povrće na komad, slabi članovi, vaga, jedinica."""

import duckdb
import pytest

from mealmeter.search import find_products
from mealmeter.staples import load_staples

S = load_staples()


# --- 1. lažni EAN ------------------------------------------------------------------------------

def test_dummy_ean_not_global(con):
    rows = con.execute("""SELECT product_id, ean_global, ean_note FROM clean.products
                          WHERE ean_norm = '9999999999994' ORDER BY 1""").fetchall()
    assert rows and all(not g and note == "dummy_list" for _, g, note in rows)


@pytest.mark.parametrize("key", ["mrkva", "krumpir"])
def test_eurospin_no_begonia(con, key):
    res = find_products(ingredient=key, con=con, limit=100)
    names = [r["name"] for r in res if "eurospin" in r["chains"]]
    assert names and not any("BEGONIJA" in n or "BILJKA" in n for n in names)


def test_multi_name_ean_flagged():
    """EAN koji jedan lanac koristi za >= 5 različitih naziva nije globalan (samo u tom lancu)."""
    from mealmeter.build import flag_dummy_eans

    c = duckdb.connect()
    c.execute("CREATE SCHEMA clean")
    c.execute("CREATE TABLE clean.products (chain VARCHAR, product_id VARCHAR, ean_norm VARCHAR, ean_global BOOLEAN, name_norm VARCHAR)")
    rows = [("a", str(i), "3850104223624", True, f"naziv {i}") for i in range(5)]
    rows += [("b", "x", "3850104223624", True, "brasno"), ("a", "y", "4006381333931", True, "jedan")]
    rows += [("c", "z", "2222222222222", True, "isto")]
    c.executemany("INSERT INTO clean.products VALUES (?, ?, ?, ?, ?)", rows)
    flag_dummy_eans(c)
    got = {(ch, pid): (g, note) for ch, pid, g, note in c.execute(
        "SELECT chain, product_id, ean_global, ean_note FROM clean.products").fetchall()}
    assert got[("a", "0")] == (False, "multi_name") and got[("b", "x")] == (True, None)
    assert got[("a", "y")] == (True, None) and got[("c", "z")] == (False, "repeated_digit")


# --- 2. obavezni atribut ------------------------------------------------------------------------

def test_spageti_excludes_bucatini(con):
    from mealmeter.basket import plan_basket

    res = find_products(ingredient="tjestenina", attributes={"oblik": "spageti"}, con=con, limit=50)
    names = [r["name"] for r in res]
    assert not any("BUCATINI" in n for n in names)
    rows = plan_basket([{"name": "špageti", "amount": 400, "unit": "g"}], "Osijek", con=con)
    assert all("BUCATINI" not in it["name"] for s in rows["stores"] for it in s["items"])


@pytest.mark.parametrize("name,shape", [
    ("TJESTENINA BUCATINI 500 G RISCOSSA", "bucatini"), ("LINGUINE 500 g BARILLA", "linguine"),
    ("SPAGHETTI N.5 500g", "spageti"), ("SPAGETINI 500 g", "spageti"), ("TAGLIATELLE 250 g", "tagliatelle"),
])
def test_pasta_shapes(name, shape):
    from mealmeter.staples import extract_attributes

    assert extract_attributes(S["tjestenina"], name)["oblik"] == shape


def test_required_attr_default_never_passes():
    from mealmeter.search import _required_attrs_sql

    sql = _required_attrs_sql(S["grah"], {"oblik": "suho"})
    assert "how <> 'default'" in sql and "'suho'" in sql


def test_product_without_required_attr_dropped(tmp_path):
    """Grupa (isti EAN) je "špageti" po nazivu drugog lanca, ali proizvod bez oblika u svom nazivu ispada."""
    from mealmeter.build import build_clean, load_raw
    from mealmeter.search import _candidates
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "r.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'T1', '8011780000960', 'TJESTENINA RISCOSSA 500 G', 'HRANA', 'KOM'),
                 ('spar', 'T2', '8011780000960', 'TJESTENINA ŠPAGETI RISCOSSA 500 G', 'Hrana', 'KOM')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('konzum', '0907', 'T1', 1.09, DATE '2026-10-19'), ('spar', '87089', 'T2', 1.19, DATE '2026-10-19')""")
    build_clean(c)
    st = S["tjestenina"]
    names = {}
    for req in (None, {"oblik": "spageti"}):
        sql, params, _ = _candidates(st, [], {"oblik": "spageti"}, None, False, required=req)
        names[bool(req)] = {n for (n,) in c.execute(sql + " SELECT DISTINCT name FROM x", params).fetchall()}
    assert "TJESTENINA RISCOSSA 500 G" in names[False]  # bez pravila ulazi preko grupe
    assert names[True] >= {"TJESTENINA ŠPAGETI RISCOSSA 500 G"} and "TJESTENINA RISCOSSA 500 G" not in names[True]
