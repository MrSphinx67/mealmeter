"""Korak 12: sažeta baza s datumom po trgovini (preneseni redci ne povećavaju bazu)."""

import importlib.util
import json
from pathlib import Path

import duckdb
import pytest

from mealmeter import server as srv
from mealmeter.build import build_clean, load_raw
from tests.conftest import FIXTURE

ROOT = Path(__file__).parents[1]


def _build_compact():
    spec = importlib.util.spec_from_file_location("bc", ROOT / "scripts" / "build_compact.py")
    bc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bc)
    return bc


@pytest.fixture(scope="module")
def carried(tmp_path_factory):
    """Puna baza iz fixture-arhive uz dvije Konzumove trgovine s prenesenim cijenama: 0908 cijela od jučer
    (ista kao 0907), 0909 pola od jučer, pola danas (djelomičan pad). Vraća (puna, sažeta, brojevi)."""
    d = tmp_path_factory.mktemp("step12")
    full = d / "full.duckdb"
    c = duckdb.connect(str(full))
    load_raw(c, FIXTURE, "2026-10-19")
    for sid in ("0908", "0909"):
        c.execute(f"""INSERT INTO stores SELECT chain, '{sid}', type, 'Vukovarska {sid}', city, zipcode FROM stores
                      WHERE chain = 'konzum' AND store_id = '0907'""")
    c.execute("""INSERT INTO prices SELECT chain, '0908', product_id, price, unit_price, best_price_30, anchor_price,
                 special_price, date - 1 FROM prices WHERE chain = 'konzum' AND store_id = '0907'""")
    c.execute("""INSERT INTO prices SELECT chain, '0909', product_id, price, unit_price, best_price_30, anchor_price,
                 special_price, CASE WHEN hash(product_id) % 2 = 0 THEN date - 1 ELSE date END
                 FROM prices WHERE chain = 'konzum' AND store_id = '0907'""")
    build_clean(c)
    n = c.execute("""SELECT count(*) FILTER (WHERE store_id = '0908'), count(*) FILTER (WHERE store_id = '0909'),
                     count(*) FILTER (WHERE store_id = '0909' AND stale_days = 1)
                     FROM clean.prices WHERE chain = 'konzum'""").fetchone()
    c.close()
    counts = _build_compact().build(full, d / "compact.duckdb")
    return full, d / "compact.duckdb", counts, n


def test_carried_store_is_not_an_exception(carried):
    full, compact, counts, (n0908, n0909, n0909_old) = carried
    assert n0908 > 0 and 0 < n0909_old < n0909
    c = duckdb.connect(str(compact), read_only=True)
    sk = dict(c.execute("SELECT store_id, sk FROM clean.stores WHERE chain = 'konzum'").fetchall())
    # cijela trgovina od jučer: datum trgovine je jučerašnji, a nijedan redak nije iznimka zbog datuma
    assert c.execute("SELECT sk_stale_days FROM clean.stores WHERE sk = ?", [sk["0908"]]).fetchone()[0] == 1
    assert c.execute("SELECT count(*) FROM clean.price_exceptions_k WHERE sk = ?", [sk["0908"]]).fetchone()[0] == \
        c.execute("SELECT count(*) FROM clean.price_exceptions_k WHERE sk = ?", [sk["0907"]]).fetchone()[0]
    # djelomičan pad: redci s drugim datumom od datuma trgovine su iznimke sa svojim datumom
    n_dated = c.execute("SELECT count(date) FROM clean.price_exceptions_k WHERE sk = ?", [sk["0909"]]).fetchone()[0]
    assert n_dated == min(n0909_old, n0909 - n0909_old) and counts["exceptions_with_date"] >= n_dated
    # view vraća iste datume i starost kao puna baza
    c.execute(f"ATTACH '{full}' AS f (READ_ONLY)")
    q = """SELECT store_id, product_id, date, stale_days, price_per_unit, per_unit, unit_confidence, price_per_kg_drained
           FROM {} WHERE chain = 'konzum' ORDER BY ALL"""
    assert c.execute(q.format("clean.prices")).fetchall() == c.execute(q.format("f.clean.prices")).fetchall()
    sq = """SELECT staple, store_id, product_id, date, stale_days, price_per_unit, per_unit, unit_confidence,
            price_per_kg_drained FROM {} ORDER BY ALL"""
    assert c.execute(sq.format("clean.staple_prices")).fetchall() == c.execute(sq.format("f.clean.staple_prices")).fetchall()


def test_carried_same_tool_outputs(carried):
    full, compact, _, _ = carried
    pancakes = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
                {"name": "jaja", "amount": 3, "unit": "kom"}]
    calls = [("plan_basket", dict(ingredients=pancakes, city="Osijek", detail=True)),
             ("plan_basket", dict(ingredients=pancakes, city="Osijek", detail=True,
                                  store={"chain": "konzum", "address_contains": "0909"})),
             ("list_stores", dict(city="Osijek", chain="konzum")), ("get_prices", dict(product_id="3850104223624"))]
    state = (srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key)
    try:
        outs = []
        for db in (full, compact):
            srv.create_server(db_path=str(db))
            outs.append([json.loads(srv._dumps(getattr(srv, name)(**args))) for name, args in calls])
    finally:
        srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key = state
    assert outs[0] == outs[1]
    stores = {s["store_id"]: s for s in outs[1][2]["stores"]}
    assert stores["0908"]["stale_days"] == 1 and stores["0907"]["stale_days"] == 0
