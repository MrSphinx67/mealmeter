"""Sažeta baza (Korak 5P): data/compact.duckdb iz pune baze, bez povijesti cijena i sirovih tablica.

Upotreba: python scripts/build_compact.py [puna_baza] [izlaz]   (zadano: data/mealmeter.duckdb -> data/compact.duckdb)

Cijene se spremaju u tri tablice, a view clean.prices ima ISTA imena i stupce kao tablica u punoj bazi, pa
search.py i plan_basket rade bez promjena (baza se bira preko env MM_DB):
- clean.chain_prices: po paru (lanac, proizvod) najčešći cijeli redak cijene (sve vrijednosti osim trgovine);
- clean.store_products: trgovine čiji je redak jednak osnovnom (samo lanac, trgovina, proizvod). Trgovina
  nema svaki proizvod lanca (popunjenost je ~46 %), pa se dostupnost čuva po trgovini;
- clean.price_exceptions: puni redci trgovina koji se razlikuju (cijena, akcija, datum prenesenog cjenika...).
DuckDB je ograničen na 1,5 GB memorije (privremene datoteke u data/compact_tmp).
"""

import os
import shutil
import sys
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
KEYS = ("chain", "store_id", "product_id")
SKIP = {"prices", "price_history", "staple_prices", "staple_items"}


def build(SRC: Path, OUT: Path) -> dict:
    t0 = time.time()
    tmp = OUT.with_name(OUT.name + ".tmp")
    tmp_dir = OUT.with_name("compact_tmp")
    for f in (tmp, tmp.with_name(tmp.name + ".wal")):
        f.unlink(missing_ok=True)
    c = duckdb.connect(config={"memory_limit": "1500MB", "threads": 2, "temp_directory": str(tmp_dir),
                               "preserve_insertion_order": False})
    c.execute(f"ATTACH '{SRC}' AS src (READ_ONLY)")
    c.execute(f"ATTACH '{tmp}' AS dst")
    c.execute("CREATE SCHEMA dst.clean")
    tables = [r[0] for r in c.execute("""SELECT table_name FROM duckdb_tables() WHERE database_name = 'src'
                                         AND schema_name = 'clean' ORDER BY 1""").fetchall()]
    for tb in tables:
        if tb not in SKIP:
            c.execute(f"CREATE TABLE dst.clean.{tb} AS SELECT * FROM src.clean.{tb}")
    cols = [r[0] for r in c.execute("""SELECT column_name FROM duckdb_columns() WHERE database_name = 'src'
            AND schema_name = 'clean' AND table_name = 'prices' ORDER BY column_index""").fetchall()]
    vals = [col for col in cols if col not in KEYS]
    v = ", ".join(vals)
    # osnovni redak para: najčešći cijeli redak; pri jednakom broju najniža cijena, pa najnoviji datum
    c.execute(f"""CREATE TABLE dst.clean.chain_prices AS
        SELECT chain, product_id, {v} FROM (
          SELECT chain, product_id, {v}, count(*) AS n FROM src.clean.prices GROUP BY ALL)
        QUALIFY row_number() OVER (PARTITION BY chain, product_id
                                   ORDER BY n DESC, price_eff, date DESC, {v}) = 1""")
    same = " AND ".join(f"p.{col} IS NOT DISTINCT FROM b.{col}" for col in vals)
    c.execute(f"""CREATE TEMP TABLE marked AS
        SELECT p.chain, p.store_id, p.product_id, {same} AS is_base
        FROM src.clean.prices p JOIN dst.clean.chain_prices b USING (chain, product_id)""")
    c.execute("""CREATE TABLE dst.clean.store_products AS
        SELECT chain, store_id, product_id FROM marked WHERE is_base ORDER BY chain, store_id, product_id""")
    c.execute(f"""CREATE TABLE dst.clean.price_exceptions AS
        SELECT p.* FROM src.clean.prices p JOIN marked m USING (chain, store_id, product_id)
        WHERE NOT m.is_base ORDER BY p.chain, p.store_id, p.product_id""")
    select_cols = ", ".join([f"s.{k}" for k in KEYS] + [f"b.{col}" for col in vals])
    c.execute(f"""CREATE VIEW dst.clean.prices AS
        SELECT {select_cols} FROM clean.store_products s JOIN clean.chain_prices b USING (chain, product_id)
        UNION ALL SELECT {", ".join(cols)} FROM clean.price_exceptions""")
    from mealmeter.staples import build_staple_prices

    # kopirane iz pune baze ili ih nema; grade se iznova nad view-om cijena
    build_staple_prices(c, "dst.")
    counts = {t: c.execute(f"SELECT count(*) FROM dst.clean.{t}").fetchone()[0]
              for t in ("chain_prices", "store_products", "price_exceptions", "staple_prices")}
    full = c.execute("SELECT count(*) FROM src.clean.prices").fetchone()[0]
    view = c.execute("SELECT count(*) FROM dst.clean.prices").fetchone()[0]
    if view != full:
        raise SystemExit(f"view ima {view} redaka, a puna tablica {full}")
    c.execute("CHECKPOINT dst")
    c.close()
    shutil.rmtree(tmp_dir, ignore_errors=True)
    os.replace(tmp, OUT)  # atomarno: poslužitelj s MM_DB primijeti novu datoteku
    print(f"{OUT}: {OUT.stat().st_size / 2**20:.1f} MB; {counts}; view = {view} redaka; {time.time() - t0:.0f} s")
    return counts


def main() -> None:
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "mealmeter.duckdb",
          Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "compact.duckdb")


if __name__ == "__main__":
    main()
