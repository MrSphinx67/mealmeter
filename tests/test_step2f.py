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
