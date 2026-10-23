"""Korak 7: mljeveno meso (nazivi sastojaka i proizvoda, vrsta) i upute poslužitelja za stvarne razgovore."""

import json
import os
from pathlib import Path

import pytest

from mealmeter.basket import resolve_name
from mealmeter.staples import extract_attributes, load_staples, name_match
from tests.test_step5b import con5b  # noqa: F401  (fixture)

S = load_staples()


# --- 0. mljeveno meso ----------------------------------------------------------------------------------------

@pytest.mark.parametrize("name,vrsta", [
    ("mljeveno meso junetina", "junece"),
    ("juneće mljeveno meso", "junece"),
    ("mljevena junetina", "junece"),
    ("junetina mljevena", "junece"),
    ("mljeveno juneće", "junece"),
    ("mljeveno juneće meso", "junece"),
    ("mljeveno goveđe meso", "junece"),
    ("faširano juneće", "junece"),
    ("mljevena svinjetina", "svinjsko"),
    ("svinjsko mljeveno meso", "svinjsko"),
    ("miješano mljeveno meso", "mijesano"),
    ("mljeveno mješano meso", "mijesano"),
    ("faširano", None),  # vrsta nije navedena: zadano miješano (default_preference)
    ("mljeveno meso", None),
])
def test_minced_meat_names(name, vrsta):
    st, attrs = resolve_name(name)
    assert st.key == "mljeveno_meso"
    assert attrs.get("vrsta") == vrsta
    if vrsta is None:
        assert st.default_preference["vrsta"][0] == "mijesano"


@pytest.mark.parametrize("name,key", [
    ("junetina", "junetina"), ("mljevena paprika", "mljevena_paprika"), ("mljeveni papar", "papar"),
])
def test_other_names_unchanged(name, key):
    assert resolve_name(name)[0].key == key


@pytest.mark.parametrize("name,vrsta", [
    ("JUN MLJEV MESO 850g MA PIK VRBOVEC", "junece"),  # Konzum: prije zadano miješano
    ("JUNETINA MLJEVENA", "junece"),  # Konzum: prije nije bilo namirnica
    ("JUN MLJEVENA 540G (MA)", "junece"),
    ("MLJEVENA JUN. 450 g LIPI BOKUN", "junece"),  # Tommy
    ("Juneći but mljeveni", "junece"),  # Spar
    ("MLJEVENO MJEŠANO MESO", "mijesano"),
    ("MLJEVENO MIJEŠ. 450g BOKUN GUŠTA", "mijesano"),
    ("MESO MLJ. MIJ. (SVI+JUN) PIK 850 g", "mijesano"),
    ("MESO MIJEŠANO 1 kg MLJEVENO PAK", "mijesano"),
    ("MLJEVENO JUNEĆE I SVINJSKO MESO", "mijesano"),
    ("SV.MLJ.MESO 540g PIK", "svinjsko"),
    ("SV MLJEV MESO 850G MA PIK VRBOVEC (6)", "svinjsko"),  # Roto: prije miješano
    ("Svinjska lopatica mljevena", "svinjsko"),
    ("MLJEVENA TELETINA", "telece"),
])
def test_minced_meat_products(name, vrsta):
    st = S["mljeveno_meso"]
    assert name_match(st, name) == "match"
    assert extract_attributes(st, name)["vrsta"] == vrsta


@pytest.mark.parametrize("name", [
    "MJEŠ. KURK. MLJ.35 gKOTANYI", "KLC.Mješavina začina za gulaš mljev.30g", "Grčka pita s mljevenim mesom",
    "ŽELAT DR.OE 10 g GOVEĐA MLJEVENA", "KEKS MLJEVENI 300 g SMIJEŠAK", "MJEŠAVINA ŽITARICA MLJEVENA 25 kg TSH",
])
def test_minced_meat_not_products(name):
    assert name_match(S["mljeveno_meso"], name) is None


GOLD = Path(__file__).parent / "golden" / "basket_bolonjez_junece_osijek.json"


@pytest.mark.skipif(os.environ.get("MM_GOLDEN") != "1", reason="zlatni izlazi traže stvarnu bazu (MM_GOLDEN=1)")
def test_golden_bolonjez_junece():
    out = json.loads(GOLD.read_text(encoding="utf-8"))
    assert not out["unmatched"]
    rows = out["comparison"] + out["more_chains"]
    assert {"konzum", "lidl", "kaufland", "plodine", "spar"} <= {r["chain"] for r in rows}
    meat = [i for i in out["best_store"]["items"] if i["staple"] == "mljeveno_meso"]
    assert meat and meat[0]["attributes"]["vrsta"] == "junece"


# --- 1.-6. upute poslužitelja ----------------------------------------------------------------------------------

def _instructions() -> str:
    """Upute bez prijeloma redaka i uvlaka (pravila se uspoređuju neovisno o prelamanju)."""
    from mealmeter.server import INSTRUCTIONS

    return " ".join(INSTRUCTIONS.split())


def _rule(n: int) -> str:
    text = _instructions()
    return text.split(f" {n}. ", 1)[1].split(f" {n + 1}. ", 1)[0]


def test_rule_call_again():
    text = _instructions()
    for phrase in ("Za svako novo jelo, promjenu broja osoba, sastojaka, grada ili trgovine ponovno pozovi plan_basket",
                   "nikad ne procjenjuj cijene niti ih prenosi iz ranijeg odgovora",
                   "Every new dish or change of servings, ingredients, city or store: call plan_basket again",
                   "never estimate, reuse or add up prices yourself"):
        assert phrase in text, phrase


def test_rule_when_to_ask():
    rule1 = _rule(1)
    for phrase in ("samo recept, bez pitanja o cijeni ili kupnji", "jednu kratku rečenicu",
                   "koliko košta i gdje to može kupiti u svom gradu", "Ne zovi plan_basket dok ne pristane"):
        assert phrase in rule1, phrase
    rule2 = _rule(2)
    for phrase in ("Kad pita koliko košta ili gdje kupiti", "JEDNOJ poruci", "samo ono što još ne znaš", "grad;",
                   "što već ima doma",
                   '"U koju trgovinu ideš (može i adresa ili kvart), ili da usporedim sve u gradu?"',
                   "nadjev ili dodatke kad je relevantno", "Ne pretpostavljaj što korisnik ima doma",
                   "izričito traži brz odgovor bez pitanja", "navedi pretpostavke i ponudi ponovni izračun",
                   "Never assume what is at home"):
        assert phrase in rule2, phrase


def _store(chain, address, *costs, have=()):
    return {"chain": chain, "address": address,
            "items": {i: {"cost_pack": c, "have": i in have} for i, c in enumerate(costs)}}


def test_cheaper_elsewhere_thresholds():
    from mealmeter.basket import cheaper_elsewhere

    others = [_store("lidl", "A 1", 1.0, 2.0), _store("lidl", "B 2", 1.5, 2.0), _store("konzum", "C 3", 2.0, 2.0)]
    # 10,00 -> 3,00: više od 2 €
    out = cheaper_elsewhere({"total_to_buy": 10.0}, others)
    assert out == {"chain": "lidl", "address": "A 1", "n_stores_city": 2, "total_to_buy": 3.0, "difference_eur": 7.0}
    # 3,60 -> 3,00: 0,60 € je više od 15 % od 3,60 (0,54 €)
    assert cheaper_elsewhere({"total_to_buy": 3.6}, others)["chain"] == "lidl"
    # 3,40 -> 3,00: 0,40 € je manje od 2 € i od 15 % (0,51 €)
    assert cheaper_elsewhere({"total_to_buy": 3.4}, others) is None
    # 20,00 -> 18,00: 2 € nije više od 2 €, a 10 % nije više od 15 %
    assert cheaper_elsewhere({"total_to_buy": 20.0}, [_store("spar", "D", 18.0)]) is None
    # ono što korisnik ima ne ulazi u zbroj
    assert cheaper_elsewhere({"total_to_buy": 5.0}, [_store("spar", "D", 1.0, 9.0, have=(1,))])["total_to_buy"] == 1.0


def test_cheaper_elsewhere_only_with_store(con5b):  # noqa: F811
    from mealmeter.basket import plan_basket

    ing = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"}]
    assert "cheaper_elsewhere" not in plan_basket(ing, "Osijek", con=con5b)
    res = plan_basket(ing, "Osijek", con=con5b, store={"chain": "konzum", "address_contains": ""})
    if "cheaper_elsewhere" in res:
        ce = res["cheaper_elsewhere"]
        assert ce["chain"] != "konzum" and ce["difference_eur"] == round(res["best_store"]["total_to_buy"] - ce["total_to_buy"], 2)


def test_rule_known_store():
    text = _instructions()
    for phrase in ("Trgovina poznata: plan_basket zovi sa store, a odgovor je točan popis za tu trgovinu",
                   "Ostale lance ne nabrajaj, osim jedne rečenice ako je neki drugi lanac u gradu jeftiniji za više od ~2 € ili 15 %",
                   "cheaper_elsewhere", "Known store"):
        assert phrase in text, phrase


# --- 4. bez zadane trgovine -----------------------------------------------------------------------------------

def test_compare_only_complete_chains():
    from collections import Counter

    from mealmeter.basket import compare_chains

    def store(chain, total, n, missing=()):
        return {"chain": chain, "total_to_buy": total, "total_used": total, "n_matched": n, "missing": list(missing),
                "address": f"{chain} 1", "addresses": [f"{chain} 1", f"{chain} 2", f"{chain} 3"]}
    # NTL (prije u more_chains sa 6 od 7 sastojaka, bez mesa) je sada u incomplete
    ranked = [store("konzum", 16.53, 7), store("eurospin", 17.4, 7), store("ntl", 15.07, 6, ["juneće mljeveno meso"])]
    rows, incomplete, more = compare_chains(ranked, Counter({"konzum": 7, "eurospin": 2}), 7)
    assert [r["chain"] for r in rows] == ["konzum", "eurospin"] and not more
    assert all(r["complete"] and len(r["addresses"]) == 2 for r in rows) and rows[0]["n_stores_city"] == 7
    assert incomplete == [{"chain": "ntl", "n_matched": 6, "total_to_buy": 15.07, "missing": ["juneće mljeveno meso"],
                           "note": "nedostaje: juneće mljeveno meso"}]


def test_price_spread():
    from mealmeter.basket import price_spread

    rows = [{"chain": c, "total_to_buy": t} for c, t in [("kaufland", 2.99), ("lidl", 2.99), ("eurospin", 4.36)]]
    sp = price_spread(rows)
    assert sp == {"cheapest": ["kaufland", "lidl"], "cheapest_total": 2.99, "most_expensive": ["eurospin"],
                  "most_expensive_total": 4.36, "difference_eur": 1.37, "difference_pct": 46, "small": True}
    # male razlike: manje od ~1,5 € ili od 15 % (dovoljan je jedan uvjet)
    assert price_spread([{"chain": "a", "total_to_buy": 3.0}, {"chain": "b", "total_to_buy": 4.2}])["small"]  # 1,20 €
    assert price_spread([{"chain": "a", "total_to_buy": 40.0}, {"chain": "b", "total_to_buy": 43.0}])["small"]  # 7,5 %
    # 2 € i 20 %: nije malo
    assert not price_spread([{"chain": "a", "total_to_buy": 10.0}, {"chain": "b", "total_to_buy": 12.0}])["small"]
    assert price_spread(rows[:1]) is None


def test_price_spread_only_without_store(con5b):  # noqa: F811
    from mealmeter.basket import plan_basket

    ing = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"}]
    res = plan_basket(ing, "Osijek", con=con5b)
    rows = res["comparison"] + res["more_chains"]
    if len(rows) >= 2:
        assert res["price_spread"]["cheapest_total"] == min(r["total_to_buy"] for r in rows)
    assert all(i["missing"] for i in res["incomplete"])
    assert "price_spread" not in plan_basket(ing, "Osijek", con=con5b, store={"chain": "konzum", "address_contains": ""})


def test_rule_no_store():
    text = _instructions()
    for phrase in ('Trgovina nije zadana ili korisnik kaže "svejedno": odgovor počinje s "Sve možeš kupiti u:"',
                   "lanaca koji imaju sve sastojke", "poredanih po cijeni", "najviše 2 SVOJE adrese i broj trgovina",
                   "koji je najjeftiniji i kolika je razlika do najskupljeg u popisu", "~1,5 € ili 15 %",
                   "razlike male", "najpraktičnije", 'idu na kraj, s "nedostaje: ..."',
                   "ponudi točan popis za trgovinu koju odabere", "price_spread"):
        assert phrase in text, phrase
    assert "Preporuka je trgovina s najmanjim total_to_buy" not in text


# --- 5. popis umjesto tablice -----------------------------------------------------------------------------------

def test_rule_list_not_table():
    text = _instructions()
    for phrase in ("Stavke prikaži kao popis: proizvod, veličina pakiranja (pack_size), cijena pakiranja (cost_pack)",
                   "tablicu koristi samo ako je korisnik traži", "Usporedbu lanaca također kao popis, jedan lanac po retku",
                   "a table only if asked"):
        assert phrase in text, phrase
    assert "Tablica stavki ima stupce" not in text and "Item table columns" not in text


# --- 7. nema starih proturječnih formulacija, duljina -----------------------------------------------------------

OLD_INSTRUCTIONS_LEN = 5036  # upute prije Koraka 7


@pytest.mark.parametrize("old", [
    "Odgovor počni sa summary_hr", "Start with summary_hr",  # proturječi "Sve možeš kupiti u:"
    "Preporuka je trgovina s najmanjim total_to_buy", "The recommendation is the store",  # zamijenjeno pravilom 8
    "Tablica stavki ima stupce", "Item table columns", "utrošak (cost_used)",  # tablica -> popis
    "Usporedba (comparison) mora obuhvatiti", "more_chains su potpuni lanci izvan",  # staro pravilo o usporedbi
    "ide li u određenu trgovinu", "želi li nadjev",  # staro pravilo 1
])
def test_no_old_formulations(old):
    assert old not in _instructions()


def test_instructions_length_and_numbering():
    import re

    from mealmeter.server import INSTRUCTIONS

    assert len(INSTRUCTIONS) <= OLD_INSTRUCTIONS_LEN * 1.2
    assert [int(n) for n in re.findall(r"(?m)^(\d+)\. ", INSTRUCTIONS)] == list(range(1, 14))
    # svako pravilo je dvojezično (hr / en)
    for n in range(1, 14):
        assert " / " in _rule(n), n


def test_tool_description_aligned():
    from mealmeter.server import DESCRIPTIONS

    plan = DESCRIPTIONS["plan_basket"]
    assert "počni njime" not in plan and "Preporuka je" not in plan and ">= 80 %" not in plan
    for word in ("Samo recept: ne zovi dok korisnik ne pristane", "Svaka promjena: novi poziv", "price_spread",
                 "cheaper_elsewhere", "lanci sa svim sastojcima"):
        assert word in plan, word
