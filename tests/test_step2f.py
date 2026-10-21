"""Korak 2F: lažni EAN-ovi, obavezni atributi, svježe povrće na komad, slabi članovi, vaga, jedinica."""

import duckdb
import pytest

from mealmeter.search import find_products
from mealmeter.staples import load_staples

S = load_staples()


# --- 1. lažni EAN ------------------------------------------------------------------------------

def test_dummy_ean_not_global(con):
    rows = con.execute("""SELECT product_id, ean_global, ean_note FROM clean.products
                          WHERE ean_norm = '9999999999994' ORDER BY 1""").fetchall()
    assert rows and all(not g and note == "dummy_list" for _, g, note in rows)


@pytest.mark.parametrize("key", ["mrkva", "krumpir"])
def test_eurospin_no_begonia(con, key):
    res = find_products(ingredient=key, con=con, limit=100)
    names = [r["name"] for r in res if "eurospin" in r["chains"]]
    assert names and not any("BEGONIJA" in n or "BILJKA" in n for n in names)


def test_multi_name_ean_flagged():
    """EAN koji jedan lanac koristi za >= 5 različitih naziva nije globalan (samo u tom lancu)."""
    from mealmeter.build import flag_dummy_eans

    c = duckdb.connect()
    c.execute("CREATE SCHEMA clean")
    c.execute("CREATE TABLE clean.products (chain VARCHAR, product_id VARCHAR, ean_norm VARCHAR, ean_global BOOLEAN, name_norm VARCHAR)")
    rows = [("a", str(i), "3850104223624", True, f"naziv {i}") for i in range(5)]
    rows += [("b", "x", "3850104223624", True, "brasno"), ("a", "y", "4006381333931", True, "jedan")]
    rows += [("c", "z", "2222222222222", True, "isto")]
    c.executemany("INSERT INTO clean.products VALUES (?, ?, ?, ?, ?)", rows)
    flag_dummy_eans(c)
    got = {(ch, pid): (g, note) for ch, pid, g, note in c.execute(
        "SELECT chain, product_id, ean_global, ean_note FROM clean.products").fetchall()}
    assert got[("a", "0")] == (False, "multi_name") and got[("b", "x")] == (True, None)
    assert got[("a", "y")] == (True, None) and got[("c", "z")] == (False, "repeated_digit")


# --- 2. obavezni atribut ------------------------------------------------------------------------

def test_spageti_excludes_bucatini(con):
    from mealmeter.basket import plan_basket

    res = find_products(ingredient="tjestenina", attributes={"oblik": "spageti"}, con=con, limit=50)
    names = [r["name"] for r in res]
    assert not any("BUCATINI" in n for n in names)
    rows = plan_basket([{"name": "špageti", "amount": 400, "unit": "g"}], "Osijek", con=con)
    assert all("BUCATINI" not in it["name"] for s in rows["stores"] for it in s["items"])


@pytest.mark.parametrize("name,shape", [
    ("TJESTENINA BUCATINI 500 G RISCOSSA", "bucatini"), ("LINGUINE 500 g BARILLA", "linguine"),
    ("SPAGHETTI N.5 500g", "spageti"), ("SPAGETINI 500 g", "spageti"), ("TAGLIATELLE 250 g", "tagliatelle"),
])
def test_pasta_shapes(name, shape):
    from mealmeter.staples import extract_attributes

    assert extract_attributes(S["tjestenina"], name)["oblik"] == shape


def test_required_attr_default_never_passes():
    from mealmeter.search import _required_attrs_sql

    sql = _required_attrs_sql(S["grah"], {"oblik": "suho"})
    assert "how <> 'default'" in sql and "'suho'" in sql


def test_product_without_required_attr_dropped(tmp_path):
    """Grupa (isti EAN) je "špageti" po nazivu drugog lanca, ali proizvod bez oblika u svom nazivu ispada."""
    from mealmeter.build import build_clean, load_raw
    from mealmeter.search import _candidates
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "r.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'T1', '8011780000960', 'TJESTENINA RISCOSSA 500 G', 'HRANA', 'KOM'),
                 ('spar', 'T2', '8011780000960', 'TJESTENINA ŠPAGETI RISCOSSA 500 G', 'Hrana', 'KOM')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('konzum', '0907', 'T1', 1.09, DATE '2026-10-19'), ('spar', '87089', 'T2', 1.19, DATE '2026-10-19')""")
    build_clean(c)
    st = S["tjestenina"]
    names = {}
    for req in (None, {"oblik": "spageti"}):
        sql, params, _ = _candidates(st, [], {"oblik": "spageti"}, None, False, required=req)
        names[bool(req)] = {n for (n,) in c.execute(sql + " SELECT DISTINCT name FROM x", params).fetchall()}
    assert "TJESTENINA RISCOSSA 500 G" in names[False]  # bez pravila ulazi preko grupe
    assert names[True] >= {"TJESTENINA ŠPAGETI RISCOSSA 500 G"} and "TJESTENINA RISCOSSA 500 G" not in names[True]


# --- 3. svježe povrće na komad ------------------------------------------------------------------

def _ean(first12: str) -> str:
    """EAN-13 s ispravnom kontrolnom znamenkom."""
    total = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(first12))
    return first12 + str((10 - total % 10) % 10)


def _loose_build(tmp_path, rows):
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "l.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES (?, ?, ?, ?, 'HRANA', 'KOM')", rows)
    build_clean(c)
    return c


def test_loose_piece_with_global_ean(tmp_path):
    c = _loose_build(tmp_path, [
        ("spar", "K1", "8058056199577", "KRASTAVAC SALATAR kom"),  # globalni EAN, na komad
        ("spar", "K2", _ean("383000000002"), "KRASTAVCI 680 G STAKLENKA"),  # fiksno pakiranje u g < 500? ne: 680 g
        ("spar", "K3", _ean("383000000003"), "PAPRIKA AJVAR kom"),  # riječ prerade
    ])
    got = {pid: st for pid, st in c.execute("""SELECT product_id, staple FROM clean.product_staples
                                               WHERE product_id IN ('K1', 'K2', 'K3') AND NOT excluded""").fetchall()}
    assert got.get("K1") == "krastavac" and "K3" not in got


# --- 4. slabi članovi --------------------------------------------------------------------------

def _row(pid, price, quality, grams=500):
    return {"product_id": pid, "price_eff": price, "pack_amount": grams, "pack_unit": "g", "price_per_unit": None,
            "per_unit": "kg", "match_quality": quality}


def test_weak_only_without_strong():
    from mealmeter.basket import choose_product

    pick = choose_product([_row("weak", 0.50, "weak"), _row("strong", 0.90, "strong")], 400, "g", "kg", loose=False)
    assert pick["product_id"] == "strong" and pick["match_quality"] == "strong"
    pick = choose_product([_row("weak", 0.50, "weak")], 400, "g", "kg", loose=False)
    assert pick["product_id"] == "weak" and pick["match_quality"] == "weak" and not pick["fallback"]


@pytest.mark.parametrize("key,name", [
    ("grasak", "POLI SALAMA S GRAŠKOM"), ("med", "ČOKOLADA RIKI PŠENICA I MED KANDIT 230 g"),
    ("med", "MEDENJACI 400g LAMBERTS MLIJEČ.ČOKOLADA"), ("med", "LAMBERTZ SRCA ML.ČOK. 400G"),
    ("med", "KEKS S MEDOM 200 g"),
])
def test_point4_exclusions(key, name):
    from mealmeter.staples import name_match

    assert name_match(S[key], name) in ("excluded", None)


# --- 5. kupnja na vagu ------------------------------------------------------------------------------

def _w(pid, ppu, **kw):
    return {"product_id": pid, "price_eff": ppu, "pack_amount": None, "pack_unit": None, "price_per_unit": ppu,
            "per_unit": "kg", **kw}


def test_parmezan_packed_before_weight():
    from mealmeter.basket import choose_product

    packed = {**_row("pak", 2.49, "strong", grams=100)}
    cca = _w("cca", 22.0, variable_weight=True)
    pick = choose_product([cca, packed], 50, "g", "kg", loose=False)
    assert pick["product_id"] == "pak" and not pick["by_weight_fallback"]
    pick = choose_product([cca], 50, "g", "kg", loose=False)
    assert pick["product_id"] == "cca" and pick["by_weight"] and pick["by_weight_fallback"]


def test_fresh_meat_by_weight_primary():
    from mealmeter.basket import _by_weight_primary, choose_product

    assert _by_weight_primary(S["svinjetina"]) and _by_weight_primary(S["luk"]) and not _by_weight_primary(S["tvrdi_sir_talijanski"])
    counter = _w("vaga", 6.0)  # bez pakiranja i bez "cca": vaga u mesnici
    pick = choose_product([counter, _row("pak", 4.50, "strong", grams=500)], 500, "g", "kg", loose=True)
    assert pick["product_id"] == "vaga" and not pick["by_weight_fallback"]  # 3,00 € < 4,50 €


# --- 6. provjera jedinice (pack_source = unit) ---------------------------------------------------------

def test_unit_suspect(tmp_path):
    """Korak 4: unit_suspect = cijena izvan ručnih granica ili daleko od istog EAN-a u >= 2 druga lanca;
    označeni se ne izbacuju (drop_reason ostaje prazan)."""
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "u.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('lidl', 'L1', 'lidl:L1', 'Brašno pšenično glatko', 'Hrana', '1kg'),
                 ('lidl', 'L2', 'lidl:L2', 'Brašno pšenično oštro', 'Hrana', '500g'),
                 ('lidl', 'M1', 'lidl:M1', 'Križevačka mljekara Trajno mlijeko', 'Hrana', '1l'),
                 ('lidl', 'M2', 'lidl:M2', 'Milkland trajno mlijeko 2,8%', 'Hrana', '1l'),
                 ('lidl', 'B1', '3850104223624', 'Brašno glatko Podravka', 'Hrana', '1kg')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('lidl', '105', 'L1', 0.69, DATE '2026-10-19'), ('lidl', '105', 'L2', 3.50, DATE '2026-10-19'),
                 ('lidl', '105', 'M1', 0.52, DATE '2026-10-19'), ('lidl', '105', 'M2', 0.25, DATE '2026-10-19'),
                 ('lidl', '105', 'B1', 0.75, DATE '2026-10-19')""")
    build_clean(c)
    got = dict(c.execute("""SELECT product_id, unit_suspect FROM clean.product_staples
                            WHERE product_id IN ('L1', 'L2', 'M1', 'M2', 'B1') AND NOT excluded""").fetchall())
    # L2: 7 €/kg > 6 (plausible); M1: 0,52 €/l u granicama; M2: 0,25 < 0,3 (Korak 5A; stvarna Milkland 0,39 je u granicama); B1: isti EAN kao Podravka 1 kg
    # u 5 lanaca (~0,79 €/kg), 0,75 €/kg -> omjer 0,95, nije označen
    assert got == {"L1": False, "L2": True, "M1": False, "M2": True, "B1": False}
    assert c.execute("SELECT count(*) FROM clean.product_staples WHERE unit_suspect AND drop_reason IS NOT NULL").fetchone()[0] == 0


def test_unit_suspect_ean_ratio(tmp_path):
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "e.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    # isti EAN kao Podravkino brašno 1 kg (5 lanaca u fixtureu, ~0,79 €/kg); stupac unit kaže 1 kg, a cijena
    # 2,20 € je cijena manjeg pakiranja: 2,20 €/kg je u granicama (0,4-6), ali 2,8x medijana drugih lanaca.
    # (Različita gramatura od ostalih s istim EAN-om već ispada kao drop_reason 'pakiranje'.)
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('lidl', 'B2', '3850104223624', 'Brašno glatko Podravka', 'Hrana', '1kg')""")
    c.execute("INSERT INTO prices (chain, store_id, product_id, price, date) VALUES ('lidl', '105', 'B2', 2.20, DATE '2026-10-19')")
    build_clean(c)
    assert c.execute("SELECT unit_suspect FROM clean.product_staples WHERE product_id = 'B2' AND staple = 'brasno'").fetchone() == (True,)


def test_unit_suspect_basket_fallback():
    from mealmeter.basket import choose_product

    sus = {**_row("sus", 0.39, "strong", grams=1000), "unit_suspect": True}
    ok = _row("ok", 0.79, "strong", grams=1000)
    pick = choose_product([sus, ok], 500, "g", None)
    assert pick["product_id"] == "ok" and not pick["fallback"]
    pick = choose_product([sus], 500, "g", None)
    assert pick["product_id"] == "sus" and pick["fallback"] and "unit_suspect" in pick["flags"]


# --- Korak 4, 0.2: slabi članovi zadano izvan find_products; u košarici samo s riječju namirnice rano ---------

@pytest.fixture(scope="module")
def weak_db(tmp_path_factory):
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path_factory.mktemp("weak") / "w.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    e1, e2 = _ean("385999000001"), _ean("385999000002")
    # dvije grupe s m = 50 % (slabi članovi): u prvoj je "margarin" prva riječ, u drugoj tek peta
    c.executemany("INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES (?, ?, ?, ?, 'Hrana', 'kom')", [
        ("konzum", "W1", e1, "MARGARIN ZLATNI 250 g"), ("spar", "W2", e1, "ZLATNI 250 g"),
        ("konzum", "W3", e2, "PECIVO MINI MARELICA I MARGARIN 250 g"), ("spar", "W4", e2, "PECIVO MINI MARELICA 250 g")])
    c.executemany("INSERT INTO prices (chain, store_id, product_id, price, date) VALUES (?, ?, ?, 1.20, DATE '2026-10-19')",
                  [("konzum", "0907", "W1"), ("konzum", "0907", "W3"), ("spar", "87089", "W2"), ("spar", "87089", "W4")])
    build_clean(c)
    return c, e1, e2


def test_weak_groups_early_name(weak_db):
    c, e1, e2 = weak_db
    got = dict(c.execute(f"""SELECT bkey, (match_quality, early_name) FROM clean.staple_groups
                             WHERE staple = 'margarin' AND bkey IN ('{e1}', '{e2}')""").fetchall())
    assert got == {e1: ("weak", True), e2: ("weak", False)}


def test_find_products_include_weak(weak_db):
    c, _, _ = weak_db
    default = {r["name"] for r in find_products(ingredient="margarin", con=c, limit=200)}
    assert not any("ZLATNI" in n or "PECIVO MINI" in n for n in default)
    weak = [r for r in find_products(ingredient="margarin", con=c, limit=200, include_weak=True)
            if "ZLATNI" in r["name"] or "PECIVO MINI" in r["name"]]
    assert len(weak) == 2 and all(r["match_quality"] == "weak" for r in weak)


def test_basket_weak_needs_early_word(weak_db):
    from mealmeter.basket import _rows_for

    c, _, _ = weak_db
    ids = {r["product_id"] for r in _rows_for(c, S["margarin"], {}, None)}
    assert {"W1", "W2"} <= ids and not ids & {"W3", "W4"}


@pytest.mark.parametrize("key,name", [
    ("maslac", "LA GALETTE ALL BUTTER ST MICHEL 130"), ("maslac", "PREMIUM PETIT BEU. 13% MASLACA KOESTLIN 250 g"),
    ("maslac", "PECIVO GOLOSINI S MASLACEM I PUNJENJEM OD MARELICE 200 g"),
    ("maslac", "MINI CROASANI S MASLACEM PUNJENI ČOKOLADOM 200 g"), ("margarin", "KORA ZA BAKLAVU RAMA 500 g"),
    ("mlijeko", "SISAC ANTI-COLIK SILIKON 2/2 MLIJEKO"), ("med", "AIRWAV.HONEY LEM.DR. 33,5 G"),
    ("riza", "SHAKER + BOJA + MAGIČNA RIŽA ORIO"), ("riza", "CJEDILO ZA RIŽU"),
    ("jogurt", "LAMBERTZ WAFER YOGURT-LIME 200G"), ("riza", "PENNE RIGATE MAIS/RISO 400 GR (12) DIVELLA (IT)"),
    ("ocat", "CITRES LUK SREDNJI U OCTU 1550 g"), ("tjestenina", "KRUPICA DURUM ZA TJEST 1 kg FARINA"),
    ("papar", "TUNJ U MASL ULJ LIMUN PAPAR 3X52g RM"),
])
def test_step4_exclusions(key, name):
    from mealmeter.staples import name_match

    assert name_match(S[key], name) != "match"
