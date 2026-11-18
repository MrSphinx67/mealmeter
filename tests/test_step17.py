"""Korak 17: točnost košarice nakon NN 101/26, 110/26.

A) proizvodi bez kategorije (is_food NULL): EAN drugih lanaca kad su svi glasovi na istoj strani (hrana ili
   neprehrana), puni neprehrambeni izrazi, i hrana samo za namirnicu (jak član, prva ili druga riječ, cijena u
   granicama) uz dopune must_not_match.
B) proizvodi na komad: pakiranje iz quantity (cijena / unit_price = quantity), nesigurna jedinica (unit_uncertain),
   najmanje jedan svežanj na vagu (units.yaml bunches), Lidlova rinfuza na vagu.
"""

import duckdb
import pytest

from mealmeter import server as srv
from mealmeter.basket import choose_product
from mealmeter.build import build_clean, load_raw
from mealmeter.food import words_group
from mealmeter.units import bunch_rule
from tests.conftest import FIXTURE

D = "DATE '2026-10-19'"


def ean13(body: str) -> str:
    digits = [int(c) for c in body]
    check = (10 - sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits)) % 10) % 10
    return body + str(check)


E = ean13("385999000001")  # zajednički EAN neprehrambenog proizvoda u tri lanca

PRODUCTS = [
    # chain, product_id, barcode, name, category, unit, quantity, price, unit_price
    ("tla", "CEL", "tla:CEL", "CELER LIST KOM", "HRANA", "ko", "0.50 kg", 1.99, 3.98),
    ("tla", "MRK", "tla:MRK", "Mrkva rinfuza", "HRANA", "1kg", "1", 0.79, 0.79),
    ("tla", "JAJ", "tla:JAJ", "JAJA M 10/1", "HRANA", "KOM", "10.00", 2.45, 0.25),
    ("tla", "SPU", E, "SPUŽVA ABC", "proizvodi za kucanstvo", "kom", "1", 1.00, 1.00),
    ("tlb", "CEL", "tlb:CEL", "Celer list", "HRANA", "kg", "1", 3.49, 3.49),
    ("tlb", "M1", "tlb:M1", "MASLAC 250 G DOLINE", None, None, None, 2.50, None),
    ("tlb", "M2", "tlb:M2", "DESERT OD VANILIJE I MASLAC 120 G", None, None, None, 1.20, None),
    ("tlb", "M3", "tlb:M3", "TROKUT S MASLACEM 100 G", None, None, None, 0.99, None),
    ("tlb", "M4", "tlb:M4", "MASLAC 250 G JEFTINI", None, None, None, 0.20, None),
    ("tlb", "KJ", "tlb:KJ", "KUTIJA ZA JAJA PVC 12/1", None, None, None, 1.99, None),
    ("tlb", "MOT", "tlb:MOT", "ULJE MOTORNO 10W-40 1L", None, None, None, 9.99, None),
    ("tlb", "SPU", E, "SPUŽVA ABC", "kozmetika", "kom", "1", 1.10, 1.10),
    ("tlc", "ICE", "tlc:ICE", "SALATA ICEBERG KOMAD", "HRANA", "KG", "1", 1.44, 1.44),
    ("tlc", "SPU", E, "SPUŽVA ABC", None, None, None, 1.20, None),
]


@pytest.fixture(scope="module")
def con17(tmp_path_factory):
    c = duckdb.connect(str(tmp_path_factory.mktemp("s17") / "c.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.executemany("INSERT INTO stores (chain, store_id, type, address, city) VALUES (?, 'S1', 'supermarket', ?, 'Osijek')",
                  [("tla", "Prva 1"), ("tlb", "Druga 2"), ("tlc", "Treca 3")])
    c.executemany("""INSERT INTO products (chain, product_id, barcode, name, category, unit, quantity)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""", [p[:7] for p in PRODUCTS])
    c.executemany(f"""INSERT INTO prices (chain, store_id, product_id, price, unit_price, date)
                      VALUES (?, 'S1', ?, ?, ?, {D})""", [(p[0], p[1], p[7], p[8]) for p in PRODUCTS])
    build_clean(c)
    srv.create_server(con=c)
    yield c
    c.close()


def _product(c, chain, pid):
    cur = c.execute("SELECT * FROM clean.products WHERE chain = ? AND product_id = ?", [chain, pid])
    return dict(zip([d[0] for d in cur.description], cur.fetchone()))


def _items(res):
    return {it["ingredient"]: it for it in res["best_store"]["items"]} if res.get("best_store") else {}


def _basket(chain, ingredients):
    return srv.plan_basket(ingredients=ingredients, city="Osijek", store={"chain": chain, "address_contains": ""},
                           detail=True)


# --- A: kategorija -------------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,group", [
    ("ULJE MOTORNO 10W-40 1L", "ostalo"), ("ULJE MOBIL SUPER 2000X1 10W-40 1/1", "ostalo"),
    ("ULJE ZA LANCE MOT.PILA 1 l", "ostalo"), ("PARAFINSKO ULJE 1L", "ostalo"), ("SVRDLO SDS+ 10 X 260", "ostalo"),
    ("STOČNA SOL UNIVER. MULTIVIT 5KG", "kucanstvo"), ("MIRISNA SOL ZIP 1 KG MAGNOLIJA", "kucanstvo"),
    ("SOL ZA PERILICE POSUĐA 1,1kg", "kucanstvo"), ("ESENS MLIJEKO ZA TIJELO 500 ML", "kozmetika"),
    ("HRANA ZA RIBE 250 ML VITA", "kucni_ljubimci"), ("SUHI VINSKI KVASAC 10G", "ostalo"),
    ("KUTIJA ZA JAJA PVC 12/1 K", "kucanstvo"), ("PLASTIČNA JAJA 6 cm", "kucanstvo"),
    ("KANTA ZA MLIJEKO 2 L", "ostalo"), ("MAZIVA MAST LITOL 800G", "ostalo"),
])
def test_nonfood_phrases(name, group):
    assert words_group(name) == group


# dvosmisleni nazivi koji su hrana: puni izrazi ih ne smiju pogoditi
@pytest.mark.parametrize("name", [
    "ULJE SUNCOKRETOVO 1L", "ULJE ZA PRŽENJE ZVIJEZDA GASTRO", "SUNCOKRET ULJE 1L ZA PEČENJE", "SOL MORSKA 1 KG",
    "Začinska sol za piletinu", "OCAT ALKOHOLNI 1 L", "KVASAC SVJEŽI PEKARSKI", "SUHI KVASAC 10G",
    "MLIJEKO TRAJNO 2,8% 1L", "TJESTENINA SVRDLA N48 500 gr RISCOSSA", "SVRDLA 400G LOVITA",
    "JUNEĆA LOPATICA BK", "KREMA ZA TORTE VANILIJA 45 g", "ZAMJENSKO MLIJEKO NAN 1 400 G", "CARPACIO OD TARTUFA 40g",
    "ZELJE KIS.RINF.KANTA 15/1", "VEGETA TWIST ZA SVINJETINU 30 g", "JAJA PLODINE M 10/1", "MAST SVINJSKA 1/1",
])
def test_food_names_not_nonfood(name):
    assert words_group(name) is None


def test_ean_one_side_inherits_is_food(con17):
    # kucanstvo 1 : kozmetika 1 (share 0,5), ali oboje neprehrana: proizvod bez kategorije je neprehrana
    p = _product(con17, "tlc", "SPU")
    assert p["is_food"] is False and p["category_source"] == "ean_inherited"


def test_nonfood_phrase_product_out(con17):
    p = _product(con17, "tlb", "MOT")
    assert p["is_food"] is False and p["food_group"] == "ostalo" and p["category_source"] == "words"


def test_unverified_food_only_strict(con17):
    assert _product(con17, "tlb", "M1")["is_food"] is None
    res = _basket("tlb", [{"name": "maslac", "amount": 100, "unit": "g"}])
    item = _items(res)["maslac"]
    # jeftiniji kandidati bez kategorije ispadaju: riječ namirnice nije prva ili druga (desert), "s maslacem"
    # (must_not_match), cijena izvan granica (0,80 €/kg)
    assert item["name"] == "MASLAC 250 G DOLINE" and item["food_unverified"]


def test_two_words_flag(con17):
    rows = dict(con17.execute("""SELECT product_id, two_words FROM clean.product_staples
                                 WHERE chain = 'tlb' AND staple = 'maslac'""").fetchall())
    assert rows["M1"] and not rows["M2"]
    assert "M3" not in rows or con17.execute("""SELECT excluded FROM clean.product_staples
                                               WHERE chain = 'tlb' AND product_id = 'M3' AND staple = 'maslac'""").fetchone()[0]


def test_egg_box_not_eggs(con17):
    res = _basket("tlb", [{"name": "jaja", "amount": 3, "unit": "kom"}])
    assert "KUTIJA" not in str(res)


# --- B: komad, svežanj, rinfuza ------------------------------------------------------------------------------

def test_piece_pack_from_quantity(con17):
    p = _product(con17, "tla", "CEL")
    assert (p["pack_amount"], p["pack_unit"], p["pack_source"]) == (500.0, "g", "quantity")
    res = _basket("tla", [{"name": "celer", "amount": 1, "unit": "kom", "attributes": {"vrsta": "stabljika"}}])
    item = _items(res)["celer"]
    assert item["cost_pack"] == 1.99 and item["pack_size"] == "500 g"
    assert any(n.startswith("cijena za komad") for n in item["notes"])


def test_count_quantity_not_a_weight(con17):
    assert _product(con17, "tla", "JAJ")["pack_source"] != "quantity"


def test_rinfuza_is_by_weight(con17):
    p = _product(con17, "tla", "MRK")
    assert p["pack_amount"] is None and p["variable_weight"]
    res = _basket("tla", [{"name": "mrkva", "amount": 100, "unit": "g"}])
    item = _items(res)["mrkva"]
    assert item["pack_size"] == "na vagu" and item["cost_pack"] == pytest.approx(0.08, abs=0.01)


def test_bunch_minimum_by_weight(con17):
    res = _basket("tlb", [{"name": "celer", "amount": 1, "unit": "kom", "attributes": {"vrsta": "stabljika"}}])
    item = _items(res)["celer"]
    # 50 g stabljike, ali na vagu najmanje svežanj od 450 g: 3,49 €/kg x 0,45 kg
    assert item["cost_pack"] == pytest.approx(1.57, abs=0.01) and item["cost_used"] == pytest.approx(0.17, abs=0.01)
    assert any("svežanj" in n for n in item["notes"])


def test_unit_uncertain_flag_and_note(con17):
    assert con17.execute("""SELECT unit_uncertain FROM clean.product_staples
                            WHERE chain = 'tlc' AND product_id = 'ICE'""").fetchone()[0]
    res = _basket("tlc", [{"name": "zelena salata", "amount": 1, "unit": "kom"}])
    item = _items(res)["zelena salata"]
    assert "unit_uncertain" in item["flags"]
    assert any(n.startswith("jedinica nesigurna: 1,44 €") for n in item["notes"])
    compact = srv._compact_item(item)
    assert any(n.startswith("jedinica nesigurna") for n in compact["notes"])


def test_unit_uncertain_in_instructions():
    from mealmeter.server import INSTRUCTIONS

    assert "unit_uncertain" in INSTRUCTIONS


def test_bunch_rules():
    assert bunch_rule("celer").matches("celer list") and not bunch_rule("celer").matches("celer korijen list")
    assert bunch_rule("luk").matches("luk mladi vezica") and not bunch_rule("luk").matches("luk crveni")
    assert bunch_rule("spinat").matches("blitva") and not bunch_rule("spinat").matches("blitva briket 650g ledo")
    assert bunch_rule("persin").matches("persin list") and not bunch_rule("persin").matches("persin korijen")
    assert bunch_rule("mrkva") is None


def test_choose_product_bunch_unit():
    rows = [{"product_id": "w", "price_eff": 3.49, "pack_amount": None, "pack_unit": None, "price_per_unit": 3.49,
             "per_unit": "kg", "bunch_g": 450.0},
            {"product_id": "p", "price_eff": 1.99, "pack_amount": 500.0, "pack_unit": "g", "price_per_unit": 3.98,
             "per_unit": "kg"}]
    pick = choose_product(rows, 50, "g", "kg")
    # svežanj na vagu 1,57 € < komad 1,99 €
    assert pick["product_id"] == "w" and pick["cost_pack"] == pytest.approx(1.57, abs=0.01)
    rows[0]["bunch_g"] = None
    assert choose_product(rows, 50, "g", "kg")["cost_pack"] == pytest.approx(0.17, abs=0.01)
