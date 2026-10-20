"""Izreže malu fixture-arhivu (isti format kao cijene.dev) iz sirovih tablica za pytest.

Upotreba: python scripts/make_fixture.py [db_path] [out_dir]
"""

import sys
from pathlib import Path

import duckdb

db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
out = Path(sys.argv[2] if len(sys.argv) > 2 else "tests/fixtures/archive")
con = duckdb.connect(db_path, read_only=True)

# (lanac) -> trgovine i proizvodi; odabrani da pokriju rubne slučajeve.
# Proizvod može biti ("id", [trgovine]) da se ograniči na dio trgovina (fixture ostaje < 100 redaka).
OSIJEK_ONLY = ["0907"]
PICK = {
    "konzum": (
        ["0907", "0001", "0201"],  # Osijek, Zagreb, Sesvete
        ["04030203", "01490037", "01310151",  # brašno glatko, Tabasco (11 znamenki), akcija
         ("02230471", OSIJEK_ONLY), ("02230085", OSIJEK_ONLY), ("04030162", OSIJEK_ONLY),  # mlijeko, čokoladno, oštro
         ("02451416", OSIJEK_ONLY), ("90348702", OSIJEK_ONLY), ("90263987", ["0001"])],  # pureće mljeveno, kupus u masl. ulju, biljni parmezan
    ),
    "eurospin": (["310017", "310002"], ["900006101", "001761601"]),  # akcija s price > special, duplikati, 0.00
    "lidl": (["105", "192"], ["6907930", "6909648", "6904110", ("6905984", ["105"])]),  # duplikati, gramatura u `unit`; pureće mljeveno
    "ntl": (["20654", "10102"], ["169600", "245063", "110379",  # PLU banana, Tabasco 11 znamenki
                                 ("001069", ["20654"])]),  # "BANANA SNIŽENJE" (rasprodaja)
    "spar": (["87089"], ["18058", "48759", "306692"]),  # adresa sa sufiksom "87089 Spar"; pureće mljeveno, GreenVie parmezan
    "roto": (["D22"], ["04030203", "15598"]),  # cijena 0.00
    "dm": (["all"], ["1000105"]),  # nacionalna cijena
    "plodine": (["053"], ["021793",  # "NAPITAK SOJINO MLIJEKO" (Osijek), bez kategorije
                          "040151", "100101", "613881", "689540"]),  # brašno (EAN), banana, čips, hrana za pse
}

for chain, (stores, products) in PICK.items():
    d = out / chain
    d.mkdir(parents=True, exist_ok=True)
    s_in = ", ".join(f"'{s}'" for s in stores)
    p_in = ", ".join(f"'{p if isinstance(p, str) else p[0]}'" for p in products)
    # (store, product) parovi za cijene
    pairs = " OR ".join(
        f"(product_id = '{p}' AND store_id IN ({s_in}))" if isinstance(p, str)
        else f"(product_id = '{p[0]}' AND store_id IN ({', '.join(repr(x) for x in p[1])}))"
        for p in products
    )
    for name, sql in {
        "stores.csv": f"SELECT store_id, type, address, city, zipcode FROM stores WHERE chain = '{chain}' AND store_id IN ({s_in}) ORDER BY ALL",
        "products.csv": f"SELECT product_id, barcode, name, brand, category, unit, quantity FROM products WHERE chain = '{chain}' AND product_id IN ({p_in}) ORDER BY ALL",
        "prices.csv": f"SELECT store_id, product_id, price, unit_price, best_price_30, anchor_price, special_price FROM prices WHERE chain = '{chain}' AND ({pairs}) ORDER BY ALL",
    }.items():
        con.execute(f"COPY ({sql}) TO '{d / name}' (HEADER, DELIMITER ',')")
