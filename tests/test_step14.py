"""Korak 14: _brand_substitutions bira istu alternativu marke neovisno o redoslijedu skupa `branded`
(hash seed procesa); prije je min po cost_pack kod izjednačenja ovisio o redoslijedu (pad workflowa 4.11.2026)."""

from itertools import permutations
from types import SimpleNamespace

from mealmeter.basket import _brand_substitutions


def _item(pid, name, pack, used, size):
    return {"product_id": pid, "ean": pid, "name": name, "pack_size": size, "n_packs": 1, "price_eff": pack,
            "cost_pack": pack, "cost_used": used}


def _stores():
    return {
        ("ntl", "1"): {"chain": "ntl", "address": "P.SVACICA 6",
                       "items": {0: _item("150170", "NAMAZ NUTELLA 400g FERRERO", 3.74, 3.74, "400 g")}},
        ("konzum", "2"): {"chain": "konzum", "address": "Trg Ante Starčevića 10",
                          "items": {0: _item("04230973", "NAMAZ NUTELLA 400g STAKLO", 3.74, 3.74, "400 g")}},
        ("kaufland", "3"): {"chain": "kaufland", "address": "Svilajska Ulica 37",
                            "items": {0: _item("00147377", "Nutella Namaz od lješnjaka 600 g", 3.74, 2.5, "600 g")}},
        ("lidl", "4"): {"chain": "lidl", "address": "X", "items": {0: _item("9", "Namaz lješnjak 400 g", 2.0, 2.0, "400 g")}},
    }


NEED = SimpleNamespace(input={"name": "nutella"}, brand=("Nutella", "nutella"))


def test_brand_alt_ne_ovisi_o_redoslijedu():
    keys = [("ntl", "1"), ("konzum", "2"), ("kaufland", "3")]
    picked = set()
    for order in permutations(keys):
        stores = _stores()
        branded = dict.fromkeys(order)  # redoslijed umetanja kao različiti hash seed
        _brand_substitutions(stores, 0, NEED, branded.keys())
        alt = stores[("lidl", "4")]["items"][0]["_brand_alt"]
        picked.add((alt["chain"], alt["product_id"]))
    # isti cost_pack: manji utrošak (veće pakiranje) pobjeđuje
    assert picked == {("kaufland", "00147377")}


def test_brand_alt_izjednacenje_po_lancu():
    picked = set()
    for order in permutations([("ntl", "1"), ("konzum", "2")]):
        stores = _stores()
        del stores[("kaufland", "3")]
        _brand_substitutions(stores, 0, NEED, dict.fromkeys(order).keys())
        picked.add(stores[("lidl", "4")]["items"][0]["_brand_alt"]["chain"])
    assert picked == {"konzum"}
