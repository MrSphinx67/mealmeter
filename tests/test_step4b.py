"""Korak 4B: plan_basket (summary_hr, alternative s razlikom, free_text, spajanje trgovina istog lanca)."""

import re

import duckdb
import pytest

from mealmeter.basket import plan_basket
from mealmeter.build import build_clean, load_raw
from tests.conftest import FIXTURE

PANCAKES = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
            {"name": "jaja", "amount": 3, "unit": "kom"}]


@pytest.fixture(scope="module")
def con4b(tmp_path_factory):
    """Fixture baza + tri brašna i tahini u Konzumu Osijek (0907) i druga Konzumova trgovina u Osijeku (0908)
    s istim cijenama."""
    c = duckdb.connect(str(tmp_path_factory.mktemp("s4b") / "a.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'A1', 'konzum:A1', 'BRAŠNO PŠENIČNO GLATKO T-550 1 kg K PLUS', 'Brašno', 'KOM'),
                 ('konzum', 'A2', 'konzum:A2', 'BRAŠNO GLATKO T-400 1 kg MLINAR', 'Brašno', 'KOM'),
                 ('konzum', 'A3', 'konzum:A3', 'BRAŠNO GLATKO T-550 5 kg MLINAR', 'Brašno', 'KOM'),
                 ('konzum', 'T1', 'konzum:T1', 'TAHINI SEZAMOVA PASTA 300 g', 'HRANA', 'KOM'),
                 ('konzum', 'T2', 'konzum:T2', 'TAHINI 600 g', 'HRANA', 'KOM'),
                 ('konzum', 'T3', 'konzum:T3', 'HALVA OD SEZAMA S TAHINI 250 g', 'HRANA', 'KOM')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('konzum', '0907', 'A1', 0.69, DATE '2026-10-19'), ('konzum', '0907', 'A2', 0.99, DATE '2026-10-19'),
                 ('konzum', '0907', 'A3', 3.49, DATE '2026-10-19'), ('konzum', '0907', 'T1', 3.99, DATE '2026-10-19'),
                 ('konzum', '0907', 'T2', 5.99, DATE '2026-10-19'), ('konzum', '0907', 'T3', 1.50, DATE '2026-10-19')""")
    c.execute("""INSERT INTO stores SELECT chain, '0908', type, 'Vukovarska 1', city, zipcode FROM stores
                 WHERE chain = 'konzum' AND store_id = '0907'""")
    c.execute("""INSERT INTO prices SELECT chain, '0908', product_id, price, unit_price, best_price_30, anchor_price,
                 special_price, date FROM prices WHERE chain = 'konzum' AND store_id = '0907'""")
    build_clean(c)
    yield c
    c.close()


KONZUM = {"chain": "konzum", "address_contains": ""}


def test_summary_hr(con4b):
    res = plan_basket(PANCAKES, "Osijek", con=con4b)
    best = res["best_store"]
    assert re.fullmatch(r"Za kupiti: \d+,\d\d €\. Stvarno utrošeno: \d+,\d\d €\.", res["summary_hr"])
    assert f"{best['total_to_buy']:.2f}".replace(".", ",") in res["summary_hr"]
    assert f"{best['total_used']:.2f}".replace(".", ",") in res["summary_hr"]
    assert plan_basket(PANCAKES, "Atlantida", con=con4b)["summary_hr"].startswith("Nepoznat grad")


def test_alternatives_delta_and_cheaper(con4b):
    res = plan_basket(PANCAKES, "Osijek", con=con4b, store=KONZUM, alternatives=True)
    flour = next(it for it in res["best_store"]["items"] if it["staple"] == "brasno")
    alts = flour["alternatives"]
    assert 1 <= len(alts) <= 2
    assert [a["cost_pack"] for a in alts] == sorted(a["cost_pack"] for a in alts)  # od najjeftinije
    for a in alts:
        assert a["delta_eur"] == round(a["cost_pack"] - flour["cost_pack"], 2)
        assert a["cheaper"] is (a["cost_pack"] < flour["cost_pack"])
        assert a["product_id"] != flour["product_id"] and a["pack_size"]
    # najbolji izbor je najjeftinije pakiranje koje pokriva količinu, pa nijedna alternativa nije jeftinija
    assert not any(a["cheaper"] for a in alts)
    # alternative samo u odabranoj (najboljoj) trgovini
    res = plan_basket(PANCAKES, "Osijek", con=con4b, alternatives=True)
    for s in res["stores"]:
        assert all(("alternatives" in it) == (s is res["best_store"]) for it in s["items"])


def test_free_text(con4b):
    ing = PANCAKES + [{"name": "tahini", "amount": 400, "unit": "g", "free_text": True}]
    res = plan_basket(ing, "Osijek", con=con4b, store=KONZUM, alternatives=True)
    best = res["best_store"]
    tahini = next(it for it in best["items"] if it["ingredient"] == "tahini")
    # najjeftinije pakiranje koje pokriva 400 g: TAHINI 600 g (300 g ne pokriva; halva nema riječ u prve tri)
    assert tahini["product_id"] == "T2" and tahini["n_packs"] == 1 and tahini["cost_pack"] == 5.99
    assert tahini["match_quality"] == "free_text" and tahini["staple"] is None and tahini["pack_size"] == "600 g"
    assert all(a["product_id"] != "T3" for a in tahini["alternatives"])
    assert best["total_to_buy"] == round(sum(it["cost_pack"] for it in best["items"] if not it["have"]), 2)
    assert any("slobodna pretraga" in w for w in res["warnings"])
    ing200 = [{"name": "tahini", "amount": 200, "unit": "g", "free_text": True}]
    assert plan_basket(ing200, "Osijek", con=con4b, store=KONZUM)["best_store"]["items"][0]["product_id"] == "T1"
    # već kod kuće: ne ulazi u total_to_buy
    res = plan_basket(ing200, "Osijek", con=con4b, store=KONZUM, already_have=["tahini"])
    assert res["best_store"]["items"][0]["have"] and res["best_store"]["total_to_buy"] == 0
    assert not any("already_have" in w for w in res["warnings"])


def test_free_text_unmatched(con4b):
    ing = [{"name": "zmajevo voće sušeno", "amount": 100, "unit": "g", "free_text": True}]
    res = plan_basket(ing, "Osijek", con=con4b)
    assert res["best_store"] is None and len(res["unmatched"]) == 1
    u = res["unmatched"][0]
    assert u["free_text"] and "zmajevo" in u["reason"] and len(u["suggestions"]) <= 3
    # bez free_text: nepoznata namirnica s prijedlogom da se pošalje kao free_text
    res = plan_basket([{"name": "tahini", "amount": 100, "unit": "g"}], "Osijek", con=con4b)
    assert "free_text" in res["unmatched"][0]["hint"]


def test_merge_same_chain(con4b):
    res = plan_basket(PANCAKES, "Osijek", con=con4b, store=KONZUM)
    konzum = [s for s in res["stores"] if s["scope"] == "local"]
    assert len(konzum) == 1
    assert konzum[0]["n_stores"] == 2 and konzum[0]["addresses"] == ["Ive Tijardovića 4A", "Vukovarska 1"]
    res = plan_basket(PANCAKES, "Osijek", con=con4b)
    assert all(s["n_stores"] >= 1 and len(s["addresses"]) <= 3 for s in res["stores"])
    assert sum(1 for s in res["stores"] if s["chain"] == "konzum" and s["scope"] == "local") <= 1


# --- 3. nove namirnice: čokoladni namaz i džem ----------------------------------------------------------

@pytest.mark.parametrize("key,name,expected", [
    ("cokoladni_namaz", "NUTELLA 750 g", "match"),
    ("cokoladni_namaz", "NAMAZ NUTELLA 750 g", "match"),
    ("cokoladni_namaz", "Krema od lješnjaka 150g Zigante", "match"),
    ("cokoladni_namaz", "NAMAZ OD LJEŠNJAKA NUTRITELLA ORGANSKI 400 g", "match"),
    ("cokoladni_namaz", "LINO LADA GOLD 350g", "match"),
    ("cokoladni_namaz", "NUTELLA BISCUITS 304g", "excluded"),
    ("cokoladni_namaz", "NAPITAK NUTELLA 250 ml", "excluded"),
    ("cokoladni_namaz", "TORTA NUTELLA 500 g", "excluded"),
    ("cokoladni_namaz", "SLADOLED NUTELLA CUP 470ml", "excluded"),
    ("dzem", "DŽEM MARELICA 670 g PODRAVKA", "match"),
    ("dzem", "PEKMEZ OD ŠLJIVA 350g PODRAVKA", "match"),
    ("dzem", "MARMELADA NARANČA 450 g", "match"),
    ("dzem", "KRAFNA S DŽEMOM 80 g RADNIK", None),
    ("dzem", "KEKSI S DŽEMOM 200 g", None),
])
def test_new_staples_rules(key, name, expected):
    from mealmeter.staples import load_staples, name_match

    assert name_match(load_staples()[key], name) == expected


def test_new_staples_resolve_and_density():
    from mealmeter import units
    from mealmeter.basket import resolve_name, to_base

    assert resolve_name("nutella")[0].key == "cokoladni_namaz"
    assert resolve_name("namaz od lješnjaka")[0].key == "cokoladni_namaz"
    assert resolve_name("pekmez")[0].key == "dzem" and resolve_name("marmelada")[0].key == "dzem"
    dens = units.load_units().densities
    assert dens["cokoladni_namaz"] == 1.2 and dens["dzem"] == 1.3
    raw = __import__("yaml").safe_load(units.UNITS_PATH.read_text(encoding="utf-8"))["densities"]
    assert raw["cokoladni_namaz"]["estimate"] is True and raw["dzem"]["estimate"] is True
    g, unit, warn = to_base(2, "žlica", resolve_name("džem")[0])
    assert unit == "g" and g == pytest.approx(39) and "procjena" in warn[0]


# --- 4. višestruka pakiranja iz stupca unit -----------------------------------------------------------

def test_parse_multipack_unit():
    from mealmeter.normalize import parse_multipack_unit

    assert parse_multipack_unit("6x12g") == (6, 12.0, "g")
    assert parse_multipack_unit("6x8g") == (6, 8.0, "g")
    assert parse_multipack_unit("4x0,5l") == (4, 500.0, "ml")
    assert parse_multipack_unit("30G*20") == (20, 30.0, "g")
    assert parse_multipack_unit("80g") is None and parse_multipack_unit("10komad") is None
    assert parse_multipack_unit(None) is None


@pytest.mark.parametrize("key,name,unit,n", [
    ("prasak_za_pecivo", "Dolcela Prašak za pecivo", "6x12g", 6),
    ("vanilin_secer", "Dolcela Vanilin šećer", "6x8g", 6),
    ("vanilin_secer", "Vanilin šećer", "80g", 1),  # rinfuza: jedno pakiranje
    ("prasak_za_pecivo", "Prašak za pecivo 10kom.", "150g", 10),  # naziv ima prednost
])
def test_units_in_pack_from_unit_field(key, name, unit, n):
    from mealmeter.normalize import parse_pack_unit_field
    from mealmeter.staples import load_staples

    st = load_staples()[key]
    amount, pack_unit = parse_pack_unit_field(unit)
    assert st.units_in_pack(name, amount, pack_unit, {}, unit_field=unit) == n


def test_lidl_multipack_in_build(tmp_path):
    """Lidlova Dolcela vrećica 6x12g u bazi: 6 vrećica, cijena po vrećici 0,99 / 6, bez unit_suspect."""
    c = duckdb.connect(str(tmp_path / "m.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('lidl', 'D1', '4056489000001', 'Dolcela Prašak za pecivo', 'Pečenje', '6x12g'),
                 ('lidl', 'D2', '4056489000002', 'Dolcela Vanilin šećer', 'Pečenje', '6x8g')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('lidl', '105', 'D1', 0.99, DATE '2026-10-19'), ('lidl', '105', 'D2', 0.99, DATE '2026-10-19')""")
    build_clean(c)
    rows = dict(c.execute("""SELECT product_id, n_units FROM clean.product_staples
                             WHERE chain = 'lidl' AND product_id IN ('D1', 'D2') AND drop_reason IS NULL""").fetchall())
    assert rows == {"D1": 6.0, "D2": 6.0}
    assert c.execute("""SELECT pack_amount FROM clean.products WHERE chain = 'lidl' AND product_id = 'D1'""").fetchone()[0] == 72
    assert not c.execute("""SELECT bool_or(unit_suspect) FROM clean.product_staples
                            WHERE chain = 'lidl' AND product_id IN ('D1', 'D2')""").fetchone()[0]
    c.close()


# --- 5. jaja: granice cijene ---------------------------------------------------------------------------

def test_egg_bounds():
    from mealmeter.staples import load_staples

    st = load_staples()["jaja"]
    assert st.plausible_by == {"uzgoj": {"bio": (0.30, 1.00), "_other": (0.10, 0.55)}}


def test_cheap_eggs_not_suspect(tmp_path):
    """Lidl "Jaja iz kaveznog uzgoja, razred S" 10 kom za 0,99 € (1,19 € je u granicama, 0,89 € nije)."""
    c = duckdb.connect(str(tmp_path / "e.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('lidl', 'E1', '4056489000011', 'Jaja iz kaveznog uzgoja, razred "S"', 'Jaja', '10komad'),
                 ('lidl', 'E2', '4056489000012', 'Jaja iz kaveznog uzgoja, razred M', 'Jaja', '10komad'),
                 ('lidl', 'E3', '4056489000013', 'BIO jaja razred M', 'Jaja', '10komad')""")
    c.execute("""INSERT INTO prices (chain, store_id, product_id, price, date) VALUES
                 ('lidl', '105', 'E1', 1.19, DATE '2026-10-19'), ('lidl', '105', 'E2', 0.89, DATE '2026-10-19'),
                 ('lidl', '105', 'E3', 1.19, DATE '2026-10-19')""")
    build_clean(c)
    flags = dict(c.execute("""SELECT product_id, unit_suspect FROM clean.product_staples
                              WHERE chain = 'lidl' AND product_id IN ('E1', 'E2', 'E3') AND staple = 'jaja'""").fetchall())
    assert flags == {"E1": False, "E2": True, "E3": True}  # 0,119 u granicama; 0,089 ispod 0,10; bio 0,119 < 0,30
    c.close()
