"""Korak 2D: pripadnost grupa, zadani izbori, mjere."""

import duckdb
import pytest

from mealmeter.search import find_products
from mealmeter.staples import build_staple_groups, load_staples

S = load_staples()


# --- 1. pripadnost grupe (EAN) namirnici ------------------------------------------------

def _mini_groups(rows):
    """build_staple_groups nad malom bazom: rows = [(chain, ean, name_norm, excluded | None)]."""
    c = duckdb.connect()
    c.execute("CREATE SCHEMA clean")
    c.execute("""CREATE TABLE clean.products (chain VARCHAR, product_id VARCHAR, ean_norm VARCHAR,
                 ean_global BOOLEAN, name_norm VARCHAR)""")
    c.execute("""CREATE TABLE clean.product_staples (chain VARCHAR, product_id VARCHAR, staple VARCHAR,
                 excluded BOOLEAN, drop_reason VARCHAR)""")
    c.execute("""CREATE TABLE clean.product_attrs (chain VARCHAR, product_id VARCHAR, staple VARCHAR,
                 attr VARCHAR, value VARCHAR, how VARCHAR)""")
    for i, (chain, ean, name, excluded) in enumerate(rows):
        c.execute("INSERT INTO clean.products VALUES (?, ?, ?, true, ?)", [chain, str(i), ean, name])
        if excluded is not None:
            c.execute("INSERT INTO clean.product_staples VALUES (?, ?, 'x', ?, NULL)", [chain, str(i), excluded])
    build_staple_groups(c)
    return dict(c.execute("SELECT bkey, status FROM clean.staple_groups").fetchall())


def test_group_majority_rule():
    got = _mini_groups([
        ("a", "1", "masl ulje", False), ("b", "1", "masl ulje", False), ("c", "1", "brand", None),  # 2/3
        ("a", "2", "masl ulje", False), ("b", "2", "brand", None), ("c", "2", "brand", None),  # 1/3
        ("a", "3", "x", False), ("b", "3", "x", False), ("c", "3", "x", False), ("d", "3", "y", True),  # 25 % isklj.
        ("a", "4", "x", False), ("b", "4", "x", False), ("c", "4", "x", False), ("d", "4", "x", False),
        ("e", "4", "y", True),  # 20 % isključenog naziva: dopušteno
        ("a", "5", "y", True), ("b", "5", "brand", None),  # nijedan naziv ne prolazi
    ])
    assert got == {"1": "member", "2": "ambiguous", "3": "ambiguous", "4": "member", "5": "excluded"}


def test_turkey_mince_not_default_mince(con):
    # "PUREĆE MLJEVENO MESO" je u svim lancima pureće, pa grupa nije zadano miješano meso
    res = find_products(ingredient="mljeveno_meso", con=con)
    assert all("pure" not in r["name"].lower() for r in res)
    res = find_products(ingredient="mljeveno_meso", attributes={"vrsta": "purece"}, con=con)
    assert res and res[0]["attributes"]["vrsta"] == "purece"


def test_group_attrs_prefer_name(con):
    rows = con.execute("""SELECT value, how FROM clean.staple_group_attrs
                          WHERE staple = 'mljeveno_meso' AND attr = 'vrsta' AND bkey = '3850339413043'""").fetchall()
    assert rows == [("purece", "name")]
