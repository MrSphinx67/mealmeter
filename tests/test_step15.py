"""Korak 15: arhiva 17.11.2026. (NN 101/26, 110/26): memorija polja proizvoda (prazna kategorija, quantity, Lidlov
unit "g (1kg)"), neprehrambene poslovnice (KTC: poljoljekarne, benzinske, saloni) izvan alata, sužen upit sažete baze."""

import duckdb
import pytest

from mealmeter import server as srv
from mealmeter.build import build_clean, load_raw, nonfood_store_type
from mealmeter.update import extract_products, remember_fields
from tests.conftest import FIXTURE

D = "DATE '2026-10-19'"


# --- neprehrambene poslovnice --------------------------------------------------------------------------------

@pytest.mark.parametrize("typ", ["poljoljekarna", "benzinska", "autopraona", "frizerski salon", "kozmeti^ki salon",
                                 "Kozmetički salon", "LJEKARNA", "auto servis"])
def test_nonfood_store_types(typ):
    assert nonfood_store_type(typ)


# svi tipovi poslovnica iz arhive 17.11.2026. osim KTC-ovih usluga
@pytest.mark.parametrize("typ", ["supermarket", "hipermarket", "minimarket", "prodavaonica", "prodavaona", "market",
                                 "mali", "super", "maxi", "trgovina", "diskont", "diskontna_prodavaonica", "store",
                                 "webshop", "Cash & Carry", "cash and carry prodavaonica", "prod.c. stridon shop",
                                 "prod.centar", "skladiste za trgovanje robom na veliko i malo", "Supermarket", None, ""])
def test_grocery_store_types_stay(typ):
    assert not nonfood_store_type(typ)


@pytest.fixture(scope="module")
def con15(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s15") / "c.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO stores (chain, store_id, type, address, city) VALUES
                 ('ktc', 'PJPJ10', 'poljoljekarna', 'Markoviceva 64', 'Osijek'),
                 ('ktc', 'PJPJ15', 'benzinska', 'Nikole Tesle 20', 'Osijek'),
                 ('ktc', 'K1', 'trgovina', 'Glavna 1', 'Osijek')""")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('ktc', 'B1', 'ktc:B1', 'BRAŠNO GLATKO T-550 1kg', 'HRANA', 'kom')""")
    c.execute(f"""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                  ('ktc', 'PJPJ10', 'B1', 0.10, {D}), ('ktc', 'PJPJ15', 'B1', 0.11, {D}), ('ktc', 'K1', 'B1', 0.99, {D})""")
    stats = build_clean(c)
    srv.create_server(con=c)
    yield c, stats
    c.close()


def test_nonfood_stores_not_in_clean_tables(con15):
    c, stats = con15
    assert c.execute("SELECT store_id FROM clean.stores WHERE chain = 'ktc' ORDER BY 1").fetchall() == [("K1",)]
    assert c.execute("SELECT store_id FROM clean.prices WHERE chain = 'ktc' ORDER BY 1").fetchall() == [("K1",)]
    assert ("ktc", "benzinska", 1) in stats["nonfood_stores"] and ("ktc", "poljoljekarna", 1) in stats["nonfood_stores"]
    # sirove tablice ih zadržavaju
    assert c.execute("SELECT count(*) FROM stores WHERE chain = 'ktc'").fetchone()[0] == 3


def test_nonfood_stores_not_in_tools(con15):
    stores = srv.list_stores(city="Osijek", chain="ktc")["stores"]
    assert [s["store_id"] for s in stores] == ["K1"]
    res = srv.plan_basket(ingredients=[{"name": "brašno glatko", "amount": 1000, "unit": "g"}], city="Osijek",
                          store={"chain": "ktc", "address_contains": ""})
    text = str(res)
    assert "PJPJ" not in text and "Markoviceva" not in text and "Nikole Tesle" not in text


# --- memorija polja proizvoda --------------------------------------------------------------------------------

def _raw(con, rows):
    con.execute("""CREATE OR REPLACE TABLE products (chain VARCHAR, product_id VARCHAR, barcode VARCHAR, name VARCHAR,
                   brand VARCHAR, category VARCHAR, unit VARCHAR, quantity VARCHAR)""")
    if rows:
        con.executemany("INSERT INTO products VALUES (?, ?, ?, ?, NULL, ?, ?, ?)", rows)


def _fields(con):
    return {(c, p): (cat, u, q) for c, p, cat, u, q in con.execute(
        "SELECT chain, product_id, category, unit, quantity FROM products").fetchall()}


@pytest.fixture
def old_db(tmp_path):
    """Prethodna baza s memorijom (16.11.): kategorije, Lidlova veličina pakiranja, quantity."""
    path = tmp_path / "old.duckdb"
    c = duckdb.connect(str(path))
    _raw(c, [])
    c.execute("CREATE TABLE prices (date DATE)")
    remember_fields(c, None, "2026-11-16")
    c.execute("""INSERT INTO clean.product_fields VALUES
        ('konzum', '1', '3850000000001', 'Mlijeko', 'kom', '1', DATE '2026-11-16'),
        ('lidl', '1000225', '4335619249684', 'Hrana', '1kg', '1', DATE '2026-11-16'),
        ('lidl', '0000003', '4335000000003', 'Hrana', '500g', '0.5', DATE '2026-11-16'),
        ('boso', '28', '3850000000028', 'KAVA', 'KG', '100 G', DATE '2026-11-16'),
        ('dm', 'old', 'x', 'Prehrana', '', '', DATE '2026-10-01')""")
    c.close()
    return path


def test_empty_fields_get_last_known(tmp_path, old_db):
    c = duckdb.connect(str(tmp_path / "new.duckdb"))
    _raw(c, [
        ("konzum", "1", "3850000000001", "MLIJEKO", "", "kom", "1"),          # kategorija prazna
        ("lidl", "1000225", "4335619249684", "Mrežasti krumpirići", "", "g (1kg)", "1"),  # Lidl: novi unit
        ("lidl", "1001902", "4335000000003", "Proizvod nove šifre", "", "g (1kg)", "0.5"),  # nova šifra, isti barkod
        ("lidl", "1001999", "4335000000999", "Novi proizvod", "", "g (1kg)", "0.4"),        # nema memorije
        ("boso", "28", "3850000000028", "KAVA ROKI 100 g", "", "KG", ""),     # prazna kategorija i quantity
        ("konzum", "2", "3850000000002", "JOGURT", "Mliječni", "kom", "1"),   # ima svoju: ostaje
    ])
    filled = remember_fields(c, old_db, "2026-11-17")
    f = _fields(c)
    assert f[("konzum", "1")] == ("Mlijeko", "kom", "1")
    assert f[("lidl", "1000225")] == ("Hrana", "1kg", "1")
    assert f[("lidl", "1001902")] == ("Hrana", "500g", "0.5")
    assert f[("lidl", "1001999")] == ("", "g (1kg)", "0.4")
    assert f[("boso", "28")] == ("KAVA", "KG", "100 G")
    assert f[("konzum", "2")] == ("Mliječni", "kom", "1")
    assert ("lidl", "unit", 2) in filled and ("konzum", "category", 1) in filled and ("boso", "quantity", 1) in filled
    mem = {(r[0], r[1]): r for r in c.execute("SELECT * FROM clean.product_fields").fetchall()}
    # danas viđeni s popunjenim vrijednostima, stari zapis koji se nije pojavio ostaje (unutar FIELD_KEEP_DAYS)
    assert mem[("lidl", "1001902")][3:6] == ("Hrana", "500g", "0.5")
    assert ("lidl", "0000003") in mem and ("dm", "old") in mem
    # zapis stariji od FIELD_KEEP_DAYS ispada
    c2 = duckdb.connect(str(tmp_path / "later.duckdb"))
    _raw(c2, [])
    remember_fields(c2, old_db, "2026-12-31", keep_days=90)
    assert c2.execute("SELECT count(*) FROM clean.product_fields WHERE product_id = 'old'").fetchone()[0] == 0


def test_leading_zeros_dropped_from_code(tmp_path, old_db):
    """Lidl 17.11.: "0000003" -> "3" (drukčiji barkod): ista šifra bez vodećih nula, samo kad je jednoznačna."""
    c = duckdb.connect(str(tmp_path / "z.duckdb"))
    _raw(c, [("lidl", "3", "4335999999999", "Proizvod", "", "g (1kg)", "0.5"),
             ("lidl", "1000225", "4335619249684", "Krumpir", "", "kg (1kg)", "1")])
    remember_fields(c, old_db, "2026-11-17")
    f = _fields(c)
    assert f[("lidl", "3")] == ("Hrana", "500g", "0.5")
    assert f[("lidl", "1000225")] == ("Hrana", "1kg", "1")
    c.close()
    # drugo učitavanje: nova šifra je već u memoriji (prvi put upisana s praznim poljima), stara i dalje vrijedi
    mem = duckdb.connect(str(tmp_path / "z.duckdb"))
    mem.execute("""UPDATE clean.product_fields SET category = '', unit = 'g (1kg)'
                   WHERE chain = 'lidl' AND product_id = '3'""")
    mem.close()
    c2 = duckdb.connect(str(tmp_path / "z2.duckdb"))
    _raw(c2, [("lidl", "3", "4335999999999", "Proizvod", "", "g (1kg)", "0.5")])
    remember_fields(c2, tmp_path / "z.duckdb", "2026-11-18")
    assert _fields(c2)[("lidl", "3")] == ("Hrana", "500g", "0.5")


def test_leading_zeros_ambiguous_not_used(tmp_path):
    old = tmp_path / "old.duckdb"
    c = duckdb.connect(str(old))
    _raw(c, [])
    c.execute("CREATE TABLE prices (date DATE)")
    remember_fields(c, None, "2026-11-16")
    c.execute("""INSERT INTO clean.product_fields VALUES
        ('lidl', '007', 'a', 'Hrana', '500g', '0.5', DATE '2026-11-16'),
        ('lidl', '0007', 'b', 'Neprehrana', '1kom', '1', DATE '2026-11-16')""")
    c.close()
    c = duckdb.connect(str(tmp_path / "new.duckdb"))
    _raw(c, [("lidl", "7", "c", "Proizvod", "", "g (1kg)", "0.5")])
    remember_fields(c, old, "2026-11-17")
    assert _fields(c)[("lidl", "7")] == ("", "g (1kg)", "0.5")


def test_seed_from_archive_and_previous_raw(tmp_path):
    """Prva memorija: sirovi proizvodi prethodne baze, a gdje su prazni, arhiva SEED_DATE."""
    seed = tmp_path / "seed" / "konzum"
    seed.mkdir(parents=True)
    (seed / "products.csv").write_text("product_id,barcode,name,brand,category,unit,quantity\n"
                                       "1,385,MLIJEKO,,Mlijeko i mliječni,kom,1\n"
                                       "2,386,JOGURT,,Stari,kom,1\n", encoding="utf-8")
    old = tmp_path / "old.duckdb"
    c = duckdb.connect(str(old))
    _raw(c, [("konzum", "1", "385", "MLIJEKO", "", "kom", "1"), ("konzum", "2", "386", "JOGURT", "Noviji", "kom", "1")])
    c.execute("CREATE TABLE prices (date DATE)")
    c.close()
    c = duckdb.connect(str(tmp_path / "new.duckdb"))
    _raw(c, [("konzum", "1", "385", "MLIJEKO", "", "kom", "1"), ("konzum", "2", "386", "JOGURT", "", "kom", "1")])
    remember_fields(c, old, "2026-11-17", seed_root=tmp_path / "seed")
    f = _fields(c)
    assert f[("konzum", "1")][0] == "Mlijeko i mliječni"
    assert f[("konzum", "2")][0] == "Noviji"


def test_extract_products_only(tmp_path):
    import zipfile
    z = tmp_path / "a.zip"
    with zipfile.ZipFile(z, "w") as zz:
        zz.writestr("konzum/products.csv", "product_id\n1\n")
        zz.writestr("konzum/prices.csv", "x\n")
        zz.writestr("../evil/products.csv", "x\n")
    out = extract_products(z, tmp_path / "out")
    assert [p.relative_to(out).as_posix() for p in sorted(out.rglob("*.csv"))] == ["konzum/products.csv"]


# --- sažeta baza: zadano bez anchor_price, uz MM_COMPACT_ANCHOR=1 po trgovini (Korak 16) ---------------------

def _compact_outputs(tmp_path, monkeypatch, anchor: bool):
    import importlib.util
    import json
    from pathlib import Path

    full = tmp_path / "full.duckdb"
    c = duckdb.connect(str(full))
    load_raw(c, FIXTURE, "2026-10-19")
    # druga Konzumova trgovina s drukčijom sidrenom cijenom (inače isti redak): iznimka samo zbog anchor_price
    c.execute("""INSERT INTO stores SELECT chain, '0908', type, 'Vukovarska 1', city, zipcode FROM stores
                 WHERE chain = 'konzum' AND store_id = '0907'""")
    c.execute("""INSERT INTO prices SELECT chain, '0908', product_id, price, unit_price, best_price_30,
                 anchor_price + 0.05, special_price, date FROM prices WHERE chain = 'konzum' AND store_id = '0907'""")
    build_clean(c)
    c.close()
    if anchor:
        monkeypatch.setenv("MM_COMPACT_ANCHOR", "1")
    else:
        monkeypatch.delenv("MM_COMPACT_ANCHOR", raising=False)
    spec = importlib.util.spec_from_file_location("bc", Path(__file__).parents[1] / "scripts" / "build_compact.py")
    bc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bc)
    counts = bc.build(full, tmp_path / "compact.duckdb")
    calls = [("get_prices", dict(product_id="3850104223624", city="Osijek")),
             ("plan_basket", dict(ingredients=[{"name": "brašno glatko", "amount": 250, "unit": "g"}], city="Osijek",
                                  detail=True))]
    state = (srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key)
    try:
        outs = []
        for db in (full, tmp_path / "compact.duckdb"):
            srv.create_server(db_path=str(db))
            outs.append([json.loads(srv._dumps(getattr(srv, name)(**args))) for name, args in calls])
    finally:
        srv._shared_con, srv._fixed_con, srv._db_path, srv._db_key = state
    return counts, outs


def test_compact_anchor_option_keeps_price_per_store(tmp_path, monkeypatch):
    counts, (full, compact) = _compact_outputs(tmp_path, monkeypatch, anchor=True)
    assert full == compact
    anchors = {(r["chain"], r["store_id"]): r["anchor_price"] for r in compact[0]["stores"]}
    assert anchors[("konzum", "0908")] is not None and anchors[("konzum", "0908")] != anchors[("konzum", "0907")]


def test_compact_default_without_anchor(tmp_path, monkeypatch):
    counts, (full, compact) = _compact_outputs(tmp_path, monkeypatch, anchor=False)
    assert all(r["anchor_price"] is None for r in compact[0]["stores"])
    assert any(r["anchor_price"] is not None for r in full[0]["stores"])
    for res in (full[0], compact[0]):
        for r in res["stores"]:
            r.pop("anchor_price")
    assert full == compact
