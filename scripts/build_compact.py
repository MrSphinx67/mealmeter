"""Sažeta baza (Korak 5P, 5V2): data/compact.duckdb iz pune baze, bez povijesti cijena i sirovih tablica.

Upotreba: python scripts/build_compact.py [puna_baza] [izlaz]   (zadano: data/mealmeter.duckdb -> data/compact.duckdb)

View clean.prices i tablice clean.staple_prices i clean.staple_items imaju ista imena i stupce koje alati čitaju, pa
search.py i plan_basket rade bez promjena (baza se bira preko env MM_DB). Ispod njih su cjelobrojni ključevi
(clean.products.pk INTEGER, clean.stores.sk SMALLINT) i tablice složene radi kompresije:
- clean.chain_prices_k (pk, vrijednosti): po paru (lanac, proizvod) najčešći redak cijene;
- clean.store_products_k (sk, pk): trgovine čiji je redak jednak osnovnom (trgovina nema svaki proizvod lanca,
  popunjenost ~46 %, pa se dostupnost čuva po trgovini);
- clean.price_exceptions_k (sk, pk, vrijednosti): redci trgovina koji se razlikuju (cijena, akcija, datum...);
- clean.staple_prices: cijene namirnica samo sa stupcima koje čita upit kandidata (STAPLE_PRICE_COLS);
  clean.staple_items: proizvodi namirnice (bez izostavljenih stupaca).
Izostavljeni su stupci koje alati ne čitaju (DROP_PRICE_COLS, DROP_PRODUCT_COLS); ostali su isti. Na kraju se
provjerava da svaki view vraća točno iste retke kao puna baza (broj redaka i zbroj hash-eva redaka).
DuckDB je ograničen na 1,5 GB memorije (privremene datoteke u data/compact_tmp).
"""

import os
import shutil
import sys
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mealmeter.staples import BKEY_SQL  # noqa: E402

KEYS = ("chain", "store_id", "product_id")
# tablice koje se ne kopiraju (zamijenjene view-ovima ili samo za build)
SKIP = {"prices", "price_history", "staple_prices", "staple_items", "products", "stores"}
# stupci koje alati (search.py, basket.py, server.py) ne čitaju; koristi ih samo build pune baze
DROP_PRICE_COLS = ("price", "unit_price", "price_date")
# stupci cijena koje čita upit kandidata za namirnicu (search._candidates, STAPLE_PPU_SQL)
STAPLE_PRICE_COLS = ("chain", "store_id", "product_id", "date", "stale_days", "price_eff", "is_special",
                     "price_per_unit", "per_unit", "unit_confidence", "price_per_kg_drained")
DROP_PRODUCT_COLS = ("barcode", "ean_valid", "match_norm", "category", "unit", "quantity", "unit_hint", "ean_note",
                     "ean_incoherent", "hard_nonfood")


def _cols(c, table: str, db: str = "src") -> list[str]:
    return [r[0] for r in c.execute(f"""SELECT column_name FROM duckdb_columns() WHERE database_name = '{db}'
            AND schema_name = 'clean' AND table_name = '{table}' ORDER BY column_index""").fetchall()]


def _fingerprint(c, sql: str, cols: list[str]) -> tuple:
    """Broj redaka i zbroj hash-eva redaka: jednaki multiskupovi redaka daju isti otisak."""
    return c.execute(f"SELECT count(*), sum(hash({', '.join(cols)})) FROM ({sql})").fetchone()


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
    for tb in [r[0] for r in c.execute("""SELECT table_name FROM duckdb_tables() WHERE database_name = 'src'
                                          AND schema_name = 'clean' ORDER BY 1""").fetchall()]:
        if tb not in SKIP:
            c.execute(f"CREATE TABLE dst.clean.{tb} AS SELECT * FROM src.clean.{tb}")

    # ključevi: proizvod (pk) i trgovina (sk), redom (lanac, šifra)
    pcols = [col for col in _cols(c, "products") if col not in DROP_PRODUCT_COLS]
    c.execute(f"""CREATE TABLE dst.clean.products AS
        SELECT {", ".join(pcols)}, (row_number() OVER (ORDER BY chain, product_id))::INTEGER AS pk
        FROM src.clean.products ORDER BY chain, product_id""")
    c.execute("""CREATE TABLE dst.clean.stores AS
        SELECT *, (row_number() OVER (ORDER BY chain, store_id))::SMALLINT AS sk
        FROM src.clean.stores ORDER BY chain, store_id""")

    cols = [col for col in _cols(c, "prices") if col not in DROP_PRICE_COLS]
    vals = [col for col in cols if col not in KEYS]
    v = ", ".join(vals)
    # osnovni redak para: najčešći redak (bez izostavljenih stupaca); pri jednakom broju najniža cijena, pa novi datum
    c.execute(f"""CREATE TEMP TABLE base AS
        SELECT chain, product_id, {v} FROM (
          SELECT chain, product_id, {v}, count(*) AS n FROM src.clean.prices GROUP BY ALL)
        QUALIFY row_number() OVER (PARTITION BY chain, product_id ORDER BY n DESC, price_eff, date DESC, {v}) = 1""")
    c.execute(f"""CREATE TABLE dst.clean.chain_prices_k AS
        SELECT p.pk, {", ".join(f"b.{x}" for x in vals)} FROM base b JOIN dst.clean.products p USING (chain, product_id)
        ORDER BY p.pk""")
    same = " AND ".join(f"r.{col} IS NOT DISTINCT FROM b.{col}" for col in vals)
    c.execute(f"""CREATE TEMP TABLE marked AS
        SELECT s.sk, p.pk, {same} AS is_base, {", ".join(f"r.{x}" for x in vals)}
        FROM src.clean.prices r JOIN base b USING (chain, product_id)
        JOIN dst.clean.products p USING (chain, product_id) JOIN dst.clean.stores s USING (chain, store_id)""")
    c.execute("CREATE TABLE dst.clean.store_products_k AS SELECT sk, pk FROM marked WHERE is_base ORDER BY sk, pk")
    # iznimke po (proizvod, trgovina): cijene istog proizvoda u trgovinama su slične, pa se bolje sažimaju
    c.execute(f"""CREATE TABLE dst.clean.price_exceptions_k AS
        SELECT pk, sk, {v} FROM marked WHERE NOT is_base ORDER BY pk, sk""")
    c.execute("DROP TABLE marked")
    c.execute("DROP TABLE base")
    out_cols = ", ".join(["s.chain", "s.store_id", "p.product_id"] + [f"x.{col}" for col in vals])
    c.execute(f"""CREATE VIEW dst.clean.prices AS
        SELECT {out_cols} FROM clean.store_products_k a JOIN clean.chain_prices_k x USING (pk)
          JOIN clean.products p USING (pk) JOIN clean.stores s USING (sk)
        UNION ALL
        SELECT {out_cols} FROM clean.price_exceptions_k x JOIN clean.products p USING (pk) JOIN clean.stores s USING (sk)""")

    # predizračun za namirnice (kao staples.build_staple_prices, nad punom bazom), s ključevima
    staple_src = f"""SELECT DISTINCT sg.staple, c.* FROM src.clean.staple_groups sg
        JOIN (SELECT chain, product_id, {BKEY_SQL} AS bkey FROM src.clean.products p) pb ON pb.bkey = sg.bkey
        JOIN src.clean.prices c USING (chain, product_id) WHERE sg.status IN ('member', 'ambiguous')"""
    # cijene namirnica kao tablica s tekstualnim ključevima, ali samo sa stupcima koje čita upit kandidata
    # (search._candidates); view nad ključevima bio je ~20 % sporiji (spajanje s products i chain_prices_k)
    sp = ", ".join(f"x.{col}" for col in STAPLE_PRICE_COLS)
    c.execute(f"""CREATE TABLE dst.clean.staple_prices AS
        SELECT x.staple, {sp} FROM ({staple_src}) x ORDER BY x.staple, x.chain, x.product_id, x.store_id""")
    # proizvodi namirnice kao tablica (ne view): view nad products bi pri svakom upitu čitao cijelu tablicu proizvoda
    c.execute("""CREATE TABLE dst.clean.staple_items AS
        SELECT k.staple, p.* FROM (SELECT DISTINCT staple, chain, product_id FROM dst.clean.staple_prices) k
        JOIN dst.clean.products p USING (chain, product_id) ORDER BY k.staple, p.chain, p.product_id""")

    # provjera: view-ovi vraćaju točno iste retke kao puna baza (za stupce koji su ostali)
    checks = {
        "prices": (f"SELECT {', '.join(cols)} FROM src.clean.prices", f"SELECT * FROM dst.clean.prices", cols),
        "staple_prices": (f"SELECT staple, {', '.join(STAPLE_PRICE_COLS)} FROM ({staple_src})",
                          "SELECT * FROM dst.clean.staple_prices", ["staple", *STAPLE_PRICE_COLS]),
        "staple_items": (f"""SELECT DISTINCT x.staple, {', '.join(f'p.{col}' for col in pcols)} FROM ({staple_src}) x
                             JOIN src.clean.products p USING (chain, product_id)""",
                         f"SELECT staple, {', '.join(pcols)} FROM dst.clean.staple_items", ["staple"] + pcols),
    }
    for name, (want, got, kcols) in checks.items():
        a, b = _fingerprint(c, want, kcols), _fingerprint(c, got, kcols)
        if a != b:
            raise SystemExit(f"{name}: view se razlikuje od pune baze ({a} != {b})")
    counts = {t: c.execute(f"SELECT count(*) FROM dst.clean.{t}").fetchone()[0]
              for t in ("chain_prices_k", "store_products_k", "price_exceptions_k", "staple_prices", "staple_items")}
    counts.update(store_products=counts["store_products_k"], price_exceptions=counts["price_exceptions_k"])
    c.execute("CHECKPOINT dst")
    c.close()
    shutil.rmtree(tmp_dir, ignore_errors=True)
    os.replace(tmp, OUT)  # atomarno: poslužitelj s MM_DB primijeti novu datoteku
    print(f"{OUT}: {OUT.stat().st_size / 2**20:.1f} MB; {counts}; provjera view-ova OK; {time.time() - t0:.0f} s")
    return counts


def main() -> None:
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "mealmeter.duckdb",
          Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "compact.duckdb")


if __name__ == "__main__":
    main()
