"""Korak 0: 5 probnih upita nad data/mealmeter.duckdb."""

import sys

import duckdb

con = duckdb.connect(sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb", read_only=True)


def q(title, sql):
    print(f"\n=== {title}")
    con.sql(sql).show(max_width=250, max_rows=60)


# Cijene bez duplikata (isti store+product ponekad dolazi više puta)
con.sql("""CREATE TEMP VIEW p AS
  SELECT chain, store_id, product_id, min(price) price, min(unit_price) unit_price,
         min(special_price) special_price, min(anchor_price) anchor_price
  FROM prices GROUP BY ALL""")

# Pomoćni makro: je li niz znamenki valjan GTIN (EAN-8/UPC-12/EAN-13/GTIN-14) po kontrolnoj znamenki
con.sql("""CREATE TEMP MACRO gtin_ok(b) AS
  regexp_full_match(b, '\\d{8}|\\d{12,14}') AND
  (10 - (list_sum([ (ascii(substr(reverse(b), i, 1)) - 48) * CASE WHEN i % 2 = 0 THEN 3 ELSE 1 END
                    FOR i IN range(2, length(b) + 1)]) % 10)) % 10
  = ascii(substr(b, length(b), 1)) - 48""")

q("(a) 'brašno glatko': 10 najjeftinijih po unit_price (kako ga lanac prijavljuje), najniža cijena po proizvodu", """
  SELECT pr.chain, pr.name, pr.unit, pr.quantity, min(p.price) price, min(p.unit_price) unit_price,
         count(*) n_stores
  FROM p JOIN products pr USING (chain, product_id)
  WHERE pr.name ILIKE '%brašno%' AND pr.name ILIKE '%glatk%' AND p.unit_price > 0
  GROUP BY ALL ORDER BY unit_price LIMIT 10""")

q("(a') provjera: 10 NAJVEĆIH unit_price za glatko brašno (otkriva lance gdje unit_price = cijena pakiranja)", """
  SELECT pr.chain, pr.name, pr.unit, pr.quantity, min(p.price) price, min(p.unit_price) unit_price, count(*) n_stores
  FROM p JOIN products pr USING (chain, product_id)
  WHERE pr.name ILIKE '%brašno%' AND pr.name ILIKE '%glatk%' AND p.unit_price > 0
    AND pr.name NOT ILIKE '%kukuruz%' AND pr.name NOT ILIKE '%raž%'
  GROUP BY ALL ORDER BY unit_price DESC LIMIT 10""")

ean = con.sql("""
  SELECT barcode FROM products
  WHERE name ILIKE '%brašno%' AND name ILIKE '%glatk%' AND gtin_ok(barcode)
  GROUP BY barcode ORDER BY count(DISTINCT chain) DESC, barcode LIMIT 1""").fetchone()[0]

q(f"(b) EAN {ean} (najrašireniji EAN glatkog brašna) po lancima", f"""
  SELECT pr.chain, any_value(pr.name) AS name, count(*) n_stores, min(p.price) min_price,
         round(avg(p.price), 2) avg_price, max(p.price) max_price,
         min(p.special_price) FILTER (WHERE p.special_price > 0) min_special, min(p.anchor_price) min_anchor
  FROM p JOIN products pr USING (chain, product_id)
  WHERE pr.barcode = '{ean}' GROUP BY pr.chain ORDER BY min_price""")

q("(c) trgovine u Osijeku (city ILIKE 'osijek%')", """
  SELECT chain, store_id, type, address, city, zipcode FROM stores
  WHERE city ILIKE 'osijek%' ORDER BY chain, address""")

q("(c') ostali zapisi s 'osijek' ili zip 31000 (provjera varijanti)", """
  SELECT chain, city, zipcode, count(*) FROM stores
  WHERE (city ILIKE '%osijek%' OR zipcode = '31000' OR address ILIKE '%osijek%') AND city NOT ILIKE 'osijek%'
  GROUP BY ALL""")

q("(d) udio proizvoda bez EAN-a po lancima (% od products.csv)", """
  SELECT chain, count(*) n_products,
    round(100 * avg((barcode ILIKE chain || ':%')::int), 1) AS pct_chain_code,
    round(100 * avg((NOT gtin_ok(barcode))::int), 1)        AS pct_not_valid_gtin,
    round(100 * avg((gtin_ok(barcode) AND length(barcode) = 13 AND barcode[1] = '2')::int), 1) AS pct_instore_2xx
  FROM products GROUP BY chain ORDER BY pct_not_valid_gtin DESC""")

q("(e) broj lanaca i trgovina", """
  SELECT count(DISTINCT chain) chains, count(*) stores,
         count(*) FILTER (WHERE store_id = 'all') national_pseudo_stores,
         count(DISTINCT lower(city)) distinct_cities,
         (SELECT count(*) FROM products) products,
         (SELECT count(DISTINCT barcode) FROM products WHERE gtin_ok(barcode)) distinct_valid_gtins,
         (SELECT count(*) FROM prices) price_rows
  FROM stores""")
