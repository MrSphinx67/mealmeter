"""Korak 5V5: lanci s nepouzdanim podacima (Lorenco) i veleprodaja (Metro) nikad nisu u izlazu plan_basketa;
usporedba ima zaseban redak po lancu s vlastitim adresama."""

import json

import duckdb
import pytest

from mealmeter.basket import plan_basket
from mealmeter.build import build_clean, load_raw
from tests.conftest import FIXTURE

D = "DATE '2026-10-19'"
PANCAKES = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
            {"name": "jaja", "amount": 3, "unit": "kom"}, {"name": "nutella", "amount": 300, "unit": "g"}]


@pytest.fixture(scope="module")
def con5v5(tmp_path_factory):
    """Fixture baza + Lorenco (nacionalni cjenik, lanac 'suspect') i Metro (veleprodaja), oba najjeftinija; uz to
    Konzum i Lidl u Osijeku s istim zbrojem (dva lanca iste cijene)."""
    c = duckdb.connect(str(tmp_path_factory.mktemp("s5v5") / "l.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO stores (chain, store_id, type, address, city, zipcode)
                 VALUES ('lorenco', 'all', 'web', NULL, NULL, NULL)""")
    rows = []
    for chain, store in (("lorenco", "all"), ("metro", "S14"), ("konzum", "0907"), ("lidl", "105")):
        cheap = 0.01 if chain in ("lorenco", "metro") else 1.0
        for pid, name, price in (("B", "BRAŠNO GLATKO T-550 1 kg", 0.69), ("M", "MLIJEKO TRAJNO 2,8% 1 L", 0.99),
                                 ("J", "JAJA SVJEŽA PODNI UZGOJ M 10/1", 1.99), ("N", "NUTELLA 400 g", 4.49)):
            rows.append((chain, store, f"X{pid}", name, round(price * cheap, 2) or 0.01))
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES (?, ?, ?, ?, 'HRANA', 'ko')",
                  [(ch, pid, f"{ch}:{pid}", n) for ch, _, pid, n, _ in rows])
    c.executemany(f"INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, ?, {D})",
                  [(ch, st, pid, p) for ch, st, pid, _, p in rows])
    build_clean(c)
    assert c.execute("SELECT data_quality FROM clean.chains WHERE chain = 'lorenco'").fetchone() == ("suspect",)
    yield c
    c.close()


def test_suspect_and_wholesale_never_in_basket(con5v5):
    for kwargs in ({}, {"alternatives": True}, {"already_have": ["sol"]}):
        res = plan_basket(PANCAKES, "Osijek", con=con5v5, **kwargs)
        text = json.dumps(res, ensure_ascii=False, default=str).lower()
        assert "lorenco" not in text and '"metro"' not in text, kwargs
        assert res["best_store"]["chain"] in ("konzum", "lidl")
        chains = {r["chain"] for r in res["comparison"]} | {m["chain"] for m in res["more_chains"]} \
            | {i["chain"] for i in res["incomplete"]} | {s["chain"] for s in res["stores"]}
        assert not chains & {"lorenco", "metro"}
    # izričito traženi Lorenco: upozorenje, bez košarice
    res = plan_basket(PANCAKES, "Osijek", con=con5v5, store={"chain": "lorenco", "address_contains": ""})
    assert res["best_store"] is None and any("nepouzdane podatke" in w for w in res["warnings"])


def test_comparison_rows_per_chain_with_own_addresses(con5v5):
    res = plan_basket(PANCAKES, "Osijek", con=con5v5)
    rows = res["comparison"]
    assert len({r["chain"] for r in rows}) == len(rows)  # jedan redak po lancu
    same_total = [r for r in rows if r["chain"] in ("konzum", "lidl")]
    assert len(same_total) == 2 and same_total[0]["total_to_buy"] == same_total[1]["total_to_buy"]
    addresses = {ch: {a for (a,) in con5v5.execute(
        "SELECT address FROM clean.stores WHERE chain = ? AND address IS NOT NULL", [ch]).fetchall()}
        for ch in ("konzum", "lidl")}
    for r in same_total:
        assert r["addresses"] and set(r["addresses"]) <= addresses[r["chain"]], r


# --- Korak 5V6: uz jednaku cijenu veće pakiranje --------------------------------------------------------------

def test_equal_price_prefers_larger_pack(tmp_path):
    from mealmeter.basket import choose_product

    c = duckdb.connect(str(tmp_path / "n.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    # kao Kaufland Osijek 20.10.2026.: Nutella 400 g i 600 g, obje 4,99 € (fixture nema Kauflanda, pa Konzum Osijek)
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'N4', 'konzum:N4', 'Nutella 400g', 'HRANA', 'KOM'),
                 ('konzum', 'N6', 'konzum:N6', 'Nutella Namaz od lješnjaka 600 g', 'HRANA', 'KOM')""")
    c.execute(f"""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                  ('konzum', '0907', 'N4', 4.99, {D}), ('konzum', '0907', 'N6', 4.99, {D})""")
    build_clean(c)
    res = plan_basket([{"name": "nutella", "amount": 300, "unit": "g"}], "Osijek", con=c,
                      store={"chain": "konzum", "address_contains": ""})
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "N6" and item["cost_pack"] == 4.99 and item["pack_size"] == "600 g"
    # 700 g: nijedno pakiranje ne pokriva količinu, pa vrijedi najjeftinije po jedinici (600 g), kao i prije
    item = plan_basket([{"name": "nutella", "amount": 700, "unit": "g"}], "Osijek", con=c,
                       store={"chain": "konzum", "address_contains": ""})["best_store"]["items"][0]
    assert item["product_id"] == "N6" and item["n_packs"] == 2
    c.close()
    # isti iznos i ista količina: ostaje redoslijed redaka (product_id); jeftinije ostaje jeftinije
    rows = [{"product_id": pid, "name": n, "price_eff": 4.99, "pack_amount": 400.0, "pack_unit": "g",
             "price_per_unit": 12.48, "per_unit": "kg"} for pid, n in (("A1", "x"), ("A2", "y"))]
    assert choose_product(rows, 300, "g", None, False)["product_id"] == "A1"
    rows.append({"product_id": "B", "name": "z", "price_eff": 4.98, "pack_amount": 400.0, "pack_unit": "g",
                 "price_per_unit": 12.45, "per_unit": "kg"})
    rows.append({"product_id": "C", "name": "w", "price_eff": 4.99, "pack_amount": 600.0, "pack_unit": "g",
                 "price_per_unit": 8.32, "per_unit": "kg"})
    assert choose_product(rows, 300, "g", None, False)["product_id"] == "B"  # jeftinije pakiranje i dalje pobjeđuje
