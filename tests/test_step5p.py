"""Korak 5P: alternative iste vrste, zlatni izlazi, sažeta baza."""

from mealmeter.basket import kind_note, plan_basket
from tests.test_step5b import con5b  # noqa: F401  (fixture)


# --- 0. alternative iste vrste ------------------------------------------------------------------------------

def test_sausage_alternative_other_kind_has_note(con5b):  # noqa: F811
    res = plan_basket([{"name": "kobasica", "amount": 400, "unit": "g"}], "Osijek", con=con5b,
                      store={"chain": "konzum", "address_contains": ""}, alternatives=True)
    item = res["best_store"]["items"][0]
    assert item["product_id"] == "P21" and item["attributes"]["vrsta"] == "dimljena"
    for alt in item["alternatives"]:
        if alt["product_id"] in ("P22", "P28"):
            assert alt.get("note", "").startswith("nije dimljena"), alt
    posebna = [a for a in item["alternatives"] if a["product_id"] == "P28"]
    assert posebna and posebna[0]["note"] == "nije dimljena (posebna)"


def test_kind_note():
    assert kind_note({"vrsta": "dimljena"}, {"vrsta": "dimljena"}) is None
    assert kind_note({"vrsta": "dimljena"}, {"vrsta": "posebna"}) == "nije dimljena (posebna)"
    assert kind_note({"vrsta": "dimljena"}, {}) == "nije označeno kao dimljena"
    assert kind_note({"vrsta": "nepoznato"}, {"vrsta": "kulen"}) is None and kind_note({}, {"vrsta": "x"}) is None
