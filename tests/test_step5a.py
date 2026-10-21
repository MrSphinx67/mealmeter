"""Korak 5A: ispravci iz 4C (unit stupac za tekućine, razred jaja u navodnicima, mlijeko) i HTTP."""

import duckdb
import pytest

from mealmeter.build import build_clean, load_raw
from mealmeter.staples import extract_attributes, load_staples
from tests.conftest import FIXTURE


# --- 0. ispravci iz 4C ------------------------------------------------------------------------------------

def test_liquid_unit_column_wins(tmp_path):
    c = duckdb.connect(str(tmp_path / "o.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit, quantity) VALUES
                 ('lidl', 'U1', 'lidl:U1', 'Suncokretovo ulje 20g Lidla', 'Hrana', '1l', '0.92'),
                 ('lidl', 'U2', 'lidl:U2', 'Brašno glatko 1kg', 'Hrana', '1kg', '1')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('lidl', '105', 'U1', 1.38, DATE '2026-10-19'), ('lidl', '105', 'U2', 0.75, DATE '2026-10-19')""")
    build_clean(c)
    rows = {r[0]: r[1:] for r in c.execute("""SELECT p.product_id, p.pack_amount, p.pack_unit, p.pack_source,
               c.price_per_unit::DOUBLE FROM clean.products p JOIN clean.prices c USING (chain, product_id)
               WHERE p.chain = 'lidl' AND p.product_id IN ('U1', 'U2')""").fetchall()}
    assert rows["U1"] == (1000.0, "ml", "unit", 1.38)
    assert rows["U2"][:3] == (1000.0, "g", "name")  # grami iz naziva uz kg u unit: naziv ostaje
    c.close()


@pytest.mark.parametrize("name,size", [
    ('Jaja iz kaveznog uzgoja, razred "S"', "s"),
    ('Jaja razred " S "', "s"),
    ('JAJA "M" 10 KOM', "m"),
    ('Jaja razred „L“', "l"),
    ("Perfa Jaja iz podnog uzgoja,M,bijel", "m"),
    ("Jaja, M razred, 30kom", "m"),
    ("Jaja iz podnog uzgoja XXL, razred L", "l"),
    ("Lukač Jaja podni uzgoj, razred S", "s"),
    ("JAJE S IGRAČKOM", None),
])
def test_egg_size_in_quotes(name, size):
    assert extract_attributes(load_staples()["jaja"], name).get("velicina") == size


def test_milk_lower_bound():
    assert load_staples()["mlijeko"].plausible_per_unit == (0.3, 4)
