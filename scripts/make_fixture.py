"""Izreže malu fixture-arhivu (isti format kao cijene.dev) iz sirovih tablica za pytest.

Upotreba: python scripts/make_fixture.py [db_path] [out_dir]
"""

import sys
from pathlib import Path

import duckdb

db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
out = Path(sys.argv[2] if len(sys.argv) > 2 else "tests/fixtures/archive")
con = duckdb.connect(db_path, read_only=True)

# (lanac) -> trgovine i proizvodi; odabrani da pokriju rubne slučajeve
PICK = {
    "konzum": (["0907", "0001", "0201"], ["04030203", "01490037", "01310151"]),  # Osijek, Zagreb, Sesvete; akcija
    "eurospin": (["310017", "310002"], ["900006101", "001761601"]),  # akcija s price > special, duplikati, 0.00
    "lidl": (["105", "192"], ["6907930", "6909648", "6904110"]),  # duplikati, gramatura u `unit`
    "ntl": (["20654", "10102"], ["169600", "245063", "110379"]),  # PLU banana, Tabasco 11 znamenki
    "spar": (["87089"], ["18058"]),  # adresa sa sufiksom "87089 Spar"
    "roto": (["D22"], ["04030203", "15598"]),  # cijena 0.00
    "dm": (["all"], ["1000105"]),  # nacionalna cijena
}

for chain, (stores, products) in PICK.items():
    d = out / chain
    d.mkdir(parents=True, exist_ok=True)
    s_in, p_in = ", ".join(f"'{s}'" for s in stores), ", ".join(f"'{p}'" for p in products)
    for name, sql in {
        "stores.csv": f"SELECT store_id, type, address, city, zipcode FROM stores WHERE chain = '{chain}' AND store_id IN ({s_in}) ORDER BY ALL",
        "products.csv": f"SELECT product_id, barcode, name, brand, category, unit, quantity FROM products WHERE chain = '{chain}' AND product_id IN ({p_in}) ORDER BY ALL",
        "prices.csv": f"SELECT store_id, product_id, price, unit_price, best_price_30, anchor_price, special_price FROM prices WHERE chain = '{chain}' AND store_id IN ({s_in}) AND product_id IN ({p_in}) ORDER BY ALL",
    }.items():
        con.execute(f"COPY ({sql}) TO '{d / name}' (HEADER, DELIMITER ',')")
