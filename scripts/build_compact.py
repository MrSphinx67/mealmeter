"""Sažeta baza (Korak 5P, 5V2, 12): data/compact.duckdb iz pune baze, bez povijesti cijena i sirovih tablica.

Upotreba: python scripts/build_compact.py [puna_baza] [izlaz]   (zadano: data/mealmeter.duckdb -> data/compact.duckdb)

Dvije datoteke (Korak 12; Vercel Hobby odbija datoteke veće od 100 MB): glavna (izlaz: proizvodi, trgovine,
namirnice, view-ovi) i datoteka cijena uz nju (search.prices_part: compact_prices.duckdb, tablice chain_prices_k,
store_products_k, price_exceptions_k). View clean.prices ih čita kao mm_prices.clean.* (search.PRICES_ALIAS), pa ju
search.connect i server._open priključuju pod tim imenom (search.attach_prices). Obje imaju clean.compact_build s
istom oznakom izgradnje; pri neslaganju otvaranje baze javlja grešku (CompactMismatch), a ne tuđe cijene.

View clean.prices i clean.staple_prices te tablica clean.staple_items imaju ista imena i stupce koje alati čitaju, pa
search.py i plan_basket rade bez promjena (baza se bira preko env MM_DB). Ispod njih su cjelobrojni ključevi
(clean.products.pk INTEGER, clean.stores.sk SMALLINT) i tablice složene radi kompresije:
- clean.stores.sk_date, sk_stale_days (Korak 12): datum cijena trgovine (najčešći datum njezinih redaka) i
  njegova starost; date i stale_days nisu među stupcima vrijednosti, pa preneseni redci (carry-forward, cijela
  trgovina "ista kao dan X") ostaju osnovni i ne povećavaju bazu;
- [datoteka cijena] clean.chain_prices_k (pk, vrijednosti): po paru (lanac, proizvod) najčešći redak cijene;
- [datoteka cijena] clean.store_products_k (sk, pk): trgovine čiji je redak jednak osnovnom i čiji je datum datum trgovine
  (trgovina nema svaki proizvod lanca, popunjenost ~46 %, pa se dostupnost čuva po trgovini);
- [datoteka cijena] clean.price_exceptions_k (sk, pk, vrijednosti, date): redci trgovina koji se razlikuju (cijena, akcija...);
  date samo kad se razlikuje od datuma trgovine (trgovina s djelomičnim padom: preneseni i svježi redci), inače NULL;
- clean.staple_prices_k: cijene namirnica samo sa stupcima koje čita upit kandidata (STAPLE_PRICE_COLS);
  price_per_unit, per_unit, unit_confidence i price_per_kg_drained view računa iz proizvoda kad se daju izračunati
  (pakiranje g/ml/kom, ocijeđena masa), inače su spremljeni (*_x); clean.staple_items: proizvodi namirnice.
  U clean.prices su ti stupci spremljeni: izračun nad cijelim view-om bio je 2,5-3,5x sporiji (free_text, Korak 12).
Izostavljeni su stupci koje alati ne čitaju (DROP_PRICE_COLS, DROP_PRODUCT_COLS); ostali su isti. Na kraju se
provjerava da svaki view vraća točno iste retke kao puna baza (broj redaka i zbroj hash-eva redaka).
DuckDB je ograničen na 1,5 GB memorije (privremene datoteke u data/compact_tmp).
"""

import os
import shutil
import sys
import time
import uuid
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mealmeter.search import PRICES_ALIAS, prices_part  # noqa: E402
from mealmeter.staples import BKEY_SQL  # noqa: E402

KEYS = ("chain", "store_id", "product_id")
# tablice koje se ne kopiraju (zamijenjene view-ovima ili samo za build)
SKIP = {"prices", "price_history", "staple_prices", "staple_items", "products", "stores"}
# stupci koje alati (search.py, basket.py, server.py) ne čitaju; koristi ih samo build pune baze
DROP_PRICE_COLS = ("price", "unit_price", "price_date")
# stupci cijena koje čita upit kandidata za namirnicu (search._candidates, STAPLE_PPU_SQL)
STAPLE_PRICE_COLS = ("chain", "store_id", "product_id", "date", "stale_days", "price_eff", "is_special",
                     "price_per_unit", "per_unit", "unit_confidence", "price_per_kg_drained")
# datum i starost cijene: iz clean.stores (sk_date, sk_stale_days), a u iznimkama samo kad se razlikuju
DATE_COLS = ("date", "stale_days")
# izvedeni stupci cijena namirnica (kao u build.build_clean): izračunavi kad proizvod ima pakiranje g/ml/kom
DERIVABLE = "(p.pack_unit IN ('g', 'ml', 'kom') AND p.pack_amount > 0)"
DERIVED = {
    "price_per_unit": f"""CASE WHEN {DERIVABLE} THEN round(CASE p.pack_unit WHEN 'kom' THEN x.price_eff / p.pack_amount
                           ELSE x.price_eff / p.pack_amount * 1000 END, 2)::DECIMAL(10,2) ELSE x.price_per_unit_x END""",
    "per_unit": f"""CASE WHEN {DERIVABLE} THEN CASE p.pack_unit WHEN 'g' THEN 'kg' WHEN 'ml' THEN 'l' ELSE 'kom' END
                     ELSE x.per_unit_x END""",
    "unit_confidence": f"CASE WHEN {DERIVABLE} THEN 'high' ELSE x.unit_confidence_x END",
    "price_per_kg_drained": "round(x.price_eff / nullif(p.drained_amount, 0) * 1000, 2)::DECIMAL(10,2)",
}
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
    part = prices_part(OUT)
    tmp_part = part.with_name(part.name + ".tmp")
    tmp_dir = OUT.with_name("compact_tmp")
    for f in (tmp, tmp.with_name(tmp.name + ".wal"), tmp_part, tmp_part.with_name(tmp_part.name + ".wal")):
        f.unlink(missing_ok=True)
    c = duckdb.connect(config={"memory_limit": "1500MB", "threads": 2, "temp_directory": str(tmp_dir),
                               "preserve_insertion_order": False})
    c.execute(f"ATTACH '{SRC}' AS src (READ_ONLY)")
    c.execute(f"ATTACH '{tmp}' AS dst")
    c.execute("CREATE SCHEMA dst.clean")
    # P: datoteka cijena; view-ovi glavne datoteke je čitaju pod istim imenom pod kojim je priključuju alati
    c.execute(f"ATTACH '{tmp_part}' AS {PRICES_ALIAS}")
    c.execute(f"CREATE SCHEMA {PRICES_ALIAS}.clean")
    P = f"{PRICES_ALIAS}.clean"
    build_id = f"{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:12]}"
    c.execute("CREATE TABLE dst.clean.compact_build AS SELECT ? AS build_id, ? AS prices_file", [build_id, part.name])
    c.execute(f"CREATE TABLE {P}.compact_build AS SELECT ? AS build_id", [build_id])
    for tb in [r[0] for r in c.execute("""SELECT table_name FROM duckdb_tables() WHERE database_name = 'src'
                                          AND schema_name = 'clean' ORDER BY 1""").fetchall()]:
        if tb not in SKIP:
            c.execute(f"CREATE TABLE dst.clean.{tb} AS SELECT * FROM src.clean.{tb}")

    # ključevi: proizvod (pk) i trgovina (sk), redom (lanac, šifra)
    pcols = [col for col in _cols(c, "products") if col not in DROP_PRODUCT_COLS]
    c.execute(f"""CREATE TABLE dst.clean.products AS
        SELECT {", ".join(pcols)}, (row_number() OVER (ORDER BY chain, product_id))::INTEGER AS pk
        FROM src.clean.products ORDER BY chain, product_id""")
    # datum cjenika: date + stale_days je isti za sve retke (build_clean: max(date) - date)
    snaps = c.execute("""SELECT DISTINCT date + stale_days::INTEGER FROM src.clean.prices""").fetchall()
    if len(snaps) > 1:
        raise SystemExit(f"date + stale_days nije jednak za sve cijene: {sorted(snaps)}")
    snap = f"DATE '{snaps[0][0]}'" if snaps else "NULL::DATE"
    # datum trgovine: najčešći datum njezinih cijena (pri jednakom broju noviji)
    c.execute(f"""CREATE TABLE dst.clean.stores AS
        SELECT s.*, (row_number() OVER (ORDER BY s.chain, s.store_id))::SMALLINT AS sk, d.sk_date,
               {snap} - d.sk_date AS sk_stale_days
        FROM src.clean.stores s LEFT JOIN (
          SELECT chain, store_id, date AS sk_date FROM (
            SELECT chain, store_id, date, count(*) AS n FROM src.clean.prices GROUP BY ALL)
          QUALIFY row_number() OVER (PARTITION BY chain, store_id ORDER BY n DESC, date DESC) = 1) d
          ON d.chain = s.chain AND d.store_id = s.store_id
        ORDER BY s.chain, s.store_id""")

    cols = [col for col in _cols(c, "prices") if col not in DROP_PRICE_COLS]
    vals = [col for col in cols if col not in KEYS + DATE_COLS]
    v = ", ".join(vals)
    # osnovni redak para: najčešći redak (bez izostavljenih stupaca i datuma); pri jednakom broju najniža cijena
    c.execute(f"""CREATE TEMP TABLE base AS
        SELECT chain, product_id, {v} FROM (
          SELECT chain, product_id, {v}, count(*) AS n FROM src.clean.prices GROUP BY ALL)
        QUALIFY row_number() OVER (PARTITION BY chain, product_id ORDER BY n DESC, price_eff, {v}) = 1""")
    c.execute(f"""CREATE TABLE {P}.chain_prices_k AS
        SELECT p.pk, {", ".join(f"b.{x}" for x in vals)} FROM base b JOIN dst.clean.products p USING (chain, product_id)
        ORDER BY p.pk""")
    same = " AND ".join(f"r.{col} IS NOT DISTINCT FROM b.{col}" for col in vals)
    c.execute(f"""CREATE TEMP TABLE marked AS
        SELECT s.sk, p.pk, {same} AND r.date IS NOT DISTINCT FROM s.sk_date AS is_base,
               CASE WHEN r.date IS DISTINCT FROM s.sk_date THEN r.date END AS date, {", ".join(f"r.{x}" for x in vals)}
        FROM src.clean.prices r JOIN base b USING (chain, product_id)
        JOIN dst.clean.products p USING (chain, product_id) JOIN dst.clean.stores s USING (chain, store_id)""")
    c.execute(f"CREATE TABLE {P}.store_products_k AS SELECT sk, pk FROM marked WHERE is_base ORDER BY sk, pk")
    # iznimke po (proizvod, trgovina): cijene istog proizvoda u trgovinama su slične, pa se bolje sažimaju
    c.execute(f"""CREATE TABLE {P}.price_exceptions_k AS
        SELECT pk, sk, {v}, date FROM marked WHERE NOT is_base ORDER BY pk, sk""")
    c.execute("DROP TABLE marked")
    c.execute("DROP TABLE base")

    def out(src: str, exc: bool) -> str:
        """Stupci view-a redom kao u punoj bazi; datum iz trgovine, u iznimci njezin ako ga ima."""
        expr = {"chain": "s.chain", "store_id": "s.store_id", "product_id": "p.product_id",
                "date": f"coalesce({src}.date, s.sk_date)" if exc else "s.sk_date",
                "stale_days": f"coalesce({snap} - {src}.date, s.sk_stale_days)" if exc else "s.sk_stale_days"}
        return ", ".join(f"{expr[col]} AS {col}" if col in expr else f"{src}.{col}" for col in cols)

    c.execute(f"""CREATE VIEW dst.clean.prices AS
        SELECT {out("x", False)} FROM {P}.store_products_k a JOIN {P}.chain_prices_k x USING (pk)
          JOIN clean.products p USING (pk) JOIN clean.stores s USING (sk)
        UNION ALL
        SELECT {out("x", True)} FROM {P}.price_exceptions_k x JOIN clean.products p USING (pk)
          JOIN clean.stores s USING (sk)""")

    # predizračun za namirnice (kao staples.build_staple_prices, nad punom bazom), s ključevima
    staple_src = f"""SELECT DISTINCT sg.staple, c.* FROM src.clean.staple_groups sg
        JOIN (SELECT chain, product_id, {BKEY_SQL} AS bkey FROM src.clean.products p) pb ON pb.bkey = sg.bkey
        JOIN src.clean.prices c USING (chain, product_id) WHERE sg.status IN ('member', 'ambiguous')"""
    # cijene namirnica kao tablica s tekstualnim ključevima, ali samo sa stupcima koje čita upit kandidata
    # (search._candidates); view nad ključevima bio je ~20 % sporiji (spajanje s products i chain_prices_k)
    # izvedeni stupci se ne spremaju kad se daju izračunati iz proizvoda (DERIVED), datum kao u iznimkama
    stored = {"price_per_unit": "price_per_unit_x", "per_unit": "per_unit_x", "unit_confidence": "unit_confidence_x"}
    staple_vals = [col for col in STAPLE_PRICE_COLS if col not in KEYS + DATE_COLS + ("price_per_kg_drained",)]
    sel = ", ".join(f"CASE WHEN {DERIVABLE} THEN NULL ELSE x.{col} END AS {stored[col]}" if col in stored else f"x.{col}"
                    for col in staple_vals)
    c.execute(f"""CREATE TABLE dst.clean.staple_prices_k AS
        SELECT x.staple, s.sk, p.pk, {sel}, CASE WHEN x.date IS DISTINCT FROM s.sk_date THEN x.date END AS date
        FROM ({staple_src}) x
        JOIN dst.clean.products p USING (chain, product_id) JOIN dst.clean.stores s USING (chain, store_id)
        ORDER BY x.staple, p.pk, s.sk""")
    sexpr = {"chain": "s.chain", "store_id": "s.store_id", "product_id": "p.product_id",
             "date": "coalesce(x.date, s.sk_date)", "stale_days": f"coalesce({snap} - x.date, s.sk_stale_days)", **DERIVED}
    c.execute(f"""CREATE VIEW dst.clean.staple_prices AS
        SELECT x.staple, {", ".join(f"{sexpr[col]} AS {col}" if col in sexpr else f"x.{col}" for col in STAPLE_PRICE_COLS)}
        FROM clean.staple_prices_k x JOIN clean.products p USING (pk) JOIN clean.stores s USING (sk)""")
    # proizvodi namirnice kao tablica (ne view): view nad products bi pri svakom upitu čitao cijelu tablicu proizvoda
    c.execute("""CREATE TABLE dst.clean.staple_items AS
        SELECT k.staple, p.* FROM (SELECT DISTINCT staple, pk FROM dst.clean.staple_prices_k) k
        JOIN dst.clean.products p USING (pk) ORDER BY k.staple, p.chain, p.product_id""")

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
    counts = {t: c.execute(f"SELECT count(*) FROM {db}.{t}").fetchone()[0]
              for db, tbs in ((P, ("chain_prices_k", "store_products_k", "price_exceptions_k")),
                              ("dst.clean", ("staple_prices_k", "staple_items"))) for t in tbs}
    counts.update(store_products=counts["store_products_k"], price_exceptions=counts["price_exceptions_k"],
                  exceptions_with_date=c.execute(f"SELECT count(date) FROM {P}.price_exceptions_k").fetchone()[0])
    c.execute("CHECKPOINT dst")
    c.execute(f"CHECKPOINT {PRICES_ALIAS}")
    c.close()
    shutil.rmtree(tmp_dir, ignore_errors=True)
    # prvo datoteka cijena, pa glavna: poslužitelj koji između otvori staru glavnu i novu datoteku cijena dobije
    # CompactMismatch (ne tuđe cijene), a nova glavna datoteka promijeni ključ i otvori se nova veza
    os.replace(tmp_part, part)
    os.replace(tmp, OUT)
    print(f"{OUT}: {OUT.stat().st_size / 2**20:.1f} MB, {part.name}: {part.stat().st_size / 2**20:.1f} MB; "
          f"izgradnja {build_id}; {counts}; provjera view-ova OK; {time.time() - t0:.0f} s")
    return counts


def main() -> None:
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "mealmeter.duckdb",
          Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "compact.duckdb")


if __name__ == "__main__":
    main()
