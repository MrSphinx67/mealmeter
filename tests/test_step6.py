"""Korak 6: suhe mahunarke u pakiranju od točno 500 g ili 1 kg bez oznake oblika su oblik=suho (dry_rule.pack_exact);
oznake konzerve "OM 240g", "u slanoj vodi" i "sterilizirani" za grah."""

import json
import os
from pathlib import Path

import pytest

from mealmeter.staples import extract_attributes, form_heuristic, load_staples

S = load_staples()


@pytest.mark.parametrize("key,name,unit,amount,pack_unit,expected", [
    ("grah", "GRAH PINTO 1 kg", "kg", 1000, "g", "suho"),  # NTL
    ("grah", "Grah trešnjevac", "500g", 500, "g", "suho"),  # Lidl
    ("grah", "GRAH BORLOTTI ŠARENI 500g", "KG", 500, "g", "suho"),  # Eurospin
    ("grah", "GRAH ŠARENI RIAL 1000g (8)", "KOM", 1000, "g", "suho"),  # Roto
    ("leca", "KLC.Leća crvena 500g", "KOM", 500, "g", "suho"),
    ("slanutak", "SLANUTAK SPAR 500 g", "kg", 500, "g", "suho"),
    ("grah", "Grah trešnjevac", "800g", 800, "g", None),  # 800 g je i veličina limenke
    ("grah", "GRAH BIJELI 480g ZORELA", "kg", 480, "g", None),
    ("grah", "BIJELI GRAH ZA GASTRO 1 kg", "kg", 1000, "g", None),  # not_words
    ("leca", "VARIVO OD LEĆE SA KOBASICOM 1 kg TK", "kg", 1000, "g", None),
    ("grah", "GRAH ŠARENI ZA GASTRO 1 L", "kg", 1000, "ml", None),
    ("grasak", "GRAŠAK GARDEN GOOD 1kg", "ko", 1000, "g", None),  # grašak 1 kg je obično smrznut: bez pack_exact
])
def test_pack_exact(key, name, unit, amount, pack_unit, expected):
    assert form_heuristic(S[key], name, unit, amount, pack_unit) == expected


@pytest.mark.parametrize("name", ["Bijeli grah, OM 240g", "Podravka Bijeli grah (OM 460g)",
                                  "GRAH ŠARENI U SLANOJ VODI 480 g GIANA", "Sterilizirani crveni grah"])
def test_grah_can_markers(name):
    assert extract_attributes(S["grah"], name)["oblik"] == "konzerva"


GOLD = Path(__file__).parent / "golden" / "basket_grah_suho_osijek.json"


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_grah_suho_all_chains():
    out = json.loads(GOLD.read_text(encoding="utf-8"))
    chains = {r["chain"] for r in out["comparison"]} | {r["chain"] for r in out["more_chains"]}
    assert {"lidl", "eurospin", "ntl", "roto"} <= chains
    assert not out["incomplete"]


def test_data_attribution_in_tools_and_home():
    """Korak 6.3: navod izvora podataka u odgovoru alata (note) i na početnoj stranici."""
    from mealmeter import server as srv

    for text in (srv.PRICE_NOTE, srv.home("mealmeter.vercel.app")):
        for word in ("cijene.dev (DobarKod)", "https://cijene.dev/uvjeti-koristenja", "Podaci", "Data"):
            assert word in text
    assert "MIT" in srv.home("mealmeter.vercel.app")
