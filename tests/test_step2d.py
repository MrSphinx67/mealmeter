"""Korak 2D: pripadnost grupa, zadani izbori, mjere."""

import duckdb
import pytest

from mealmeter.search import find_products
from mealmeter.staples import build_staple_groups, load_staples

S = load_staples()


# --- 1. pripadnost grupe (EAN) namirnici ------------------------------------------------

def _mini_groups(rows, pack_unit=None):
    """build_staple_groups nad malom bazom: rows = [(chain, ean, name_norm, excluded | None)];
    hard_nonfood se računa iz naziva (food.hard_nonfood)."""
    from mealmeter.food import hard_nonfood

    c = duckdb.connect()
    c.execute("CREATE SCHEMA clean")
    c.execute("""CREATE TABLE clean.products (chain VARCHAR, product_id VARCHAR, ean_norm VARCHAR,
                 ean_global BOOLEAN, name_norm VARCHAR, pack_unit VARCHAR, hard_nonfood BOOLEAN)""")
    c.execute("""CREATE TABLE clean.product_staples (chain VARCHAR, product_id VARCHAR, staple VARCHAR,
                 excluded BOOLEAN, drop_reason VARCHAR, n_units DOUBLE, assumed_g DOUBLE)""")
    c.execute("""CREATE TABLE clean.product_attrs (chain VARCHAR, product_id VARCHAR, staple VARCHAR,
                 attr VARCHAR, value VARCHAR, how VARCHAR)""")
    c.execute("""CREATE TABLE clean.staple_rules AS SELECT 'x' AS staple, 'kg' AS unit, 'unit' AS compare_by,
                 NULL::DOUBLE AS ppu_min, NULL::DOUBLE AS ppu_max, NULL::DOUBLE AS piece_g""")
    c.execute("""CREATE TABLE clean.prices (chain VARCHAR, product_id VARCHAR, price_eff DOUBLE, per_unit VARCHAR,
                 price_per_unit DOUBLE)""")
    for i, (chain, ean, name, excluded) in enumerate(rows):
        c.execute("INSERT INTO clean.products VALUES (?, ?, ?, true, ?, ?, ?)",
                  [chain, str(i), ean, name, pack_unit, hard_nonfood(name, None, pack_unit)])
        if excluded is not None:
            c.execute("INSERT INTO clean.product_staples VALUES (?, ?, 'x', ?, NULL, NULL, NULL)", [chain, str(i), excluded])
    build_staple_groups(c)
    return {b: (st, q) for b, st, q in c.execute("SELECT bkey, status, match_quality FROM clean.staple_groups").fetchall()}


def test_group_tiers():
    # Korak 2E: snažni m > 50 % i x < 10 %; slabi x = 0 i m >= 25 %; inače ambiguous (m > 0) ili excluded
    rows = [("a", "1", "masl ulje", False), ("b", "1", "masl ulje", False), ("c", "1", "brand", None),  # 2/3
            ("a", "2", "masl ulje", False), ("b", "2", "brand", None), ("c", "2", "brand", None),  # 1/3, x = 0
            ("a", "3", "x", False), ("b", "3", "x", False), ("c", "3", "x", False), ("d", "3", "y", True),  # x 25 %
            ("a", "5", "y", True), ("b", "5", "brand", None),  # m = 0
            ("a", "6", "x", False), ("b", "6", "b", None), ("c", "6", "b", None), ("d", "6", "b", None),  # 25 %
            ("a", "7", "x", False), *[(ch, "7", "b", None) for ch in "bcde"]]  # 20 %
    rows += [(ch, "4", "x", False) for ch in "abcdefghij"] + [("z", "4", "y", True)]  # x = 1/11 < 10 %
    got = _mini_groups(rows)
    assert got == {"1": ("member", "strong"), "2": ("member", "weak"), "3": ("ambiguous", None),
                   "4": ("member", "strong"), "5": ("excluded", None), "6": ("member", "weak"),
                   "7": ("ambiguous", None)}


def test_weak_needs_compatible_unit():
    rows = [("a", "1", "x", False), ("b", "1", "b", None), ("c", "1", "b", None)]
    assert _mini_groups(rows, pack_unit="kom")["1"] == ("ambiguous", None)  # kg namirnica, komad bez mase komada
    assert _mini_groups(rows, pack_unit="g")["1"] == ("member", "weak")
    assert _mini_groups(rows, pack_unit="ml")["1"] == ("member", "weak")  # g i ml su zamjenjivi


def test_turkey_mince_not_default_mince(con):
    # "PUREĆE MLJEVENO MESO" je u svim lancima pureće, pa grupa nije zadano miješano meso
    res = find_products(ingredient="mljeveno_meso", con=con)
    assert all("pure" not in r["name"].lower() for r in res)
    res = find_products(ingredient="mljeveno_meso", attributes={"vrsta": "purece"}, con=con)
    assert res and res[0]["attributes"]["vrsta"] == "purece"


def test_group_attrs_prefer_name(con):
    rows = con.execute("""SELECT value, how FROM clean.staple_group_attrs
                          WHERE staple = 'mljeveno_meso' AND attr = 'vrsta' AND bkey = '3850339413043'""").fetchall()
    assert rows == [("purece", "name")]


# --- 2. isključenja i gramatura ----------------------------------------------------------

@pytest.mark.parametrize("key,name", [
    ("maslinovo_ulje", "KUPUS KIS MASL ULJE ČEŠNJAK 250g"),
    ("maslinovo_ulje", "PREMIUM SAL. KIS.KUPUS S EX.DJE. MASL. ULJEM I CES. 250G"),
    ("parmezan", "RIBAN.PARMEZAN GREEN VIE 100 g"),
    ("mozzarella", "MOZZARELLA VEGAN 200 g"),
    ("tvrdi_sir", "SIR TVRDI BILJNI 200 g"),
    ("maslac", "BILJNA ZAMJENA ZA MASLAC 250 g"),
    ("grah", "GRAH S KOB.SMRZ."),
    ("slanutak", "SIPA SA SLANUTKOM SMRZ."),
    ("grasak", "GRAŠAK I SIPA 400 g"),
    ("grah", "BRUDET GRAH 400 g"),
    ("leca", "LEĆA ORZO 300 g"),
])
def test_point2_exclusions(key, name):
    from mealmeter.staples import name_match

    assert name_match(S[key], name) == "excluded"


def test_felix_only_pet_food():
    from mealmeter.staples import name_match

    assert name_match(S["kecap"], "KETCHUP FELIX BLAGI 500g") == "match"
    assert name_match(S["tuna"], "HRANA ZA MAČKE FELIX TUNA 85 g") == "excluded"


def test_kupus_and_vegan_parmezan_not_in_default(con):
    names = [r["name"] for r in find_products(ingredient="maslinovo_ulje", limit=100, con=con)]
    assert not any("KUPUS" in n for n in names)
    names = [r["name"] for r in find_products(ingredient="parmezan", limit=100, con=con, include_ambiguous=True)]
    assert not any("BILJ" in n.upper() or "GREEN" in n.upper() for n in names)


@pytest.mark.parametrize("name,pack", [
    ("PERŠIN KOR LIS 250 gVOĆARNA STUDENAC", (250, "g")),
    ("KIS.KUP. ČEŠNJ.250 gMADIG", (250, "g")),
    ("5 LIMUNA", None),  # bez razlike u veličini slova jedinica se ne odvaja
])
def test_pack_glued_unit(name, pack):
    from mealmeter.normalize import parse_pack

    assert parse_pack(name) == pack


# --- 3. mljeveno meso -----------------------------------------------------------------

def _row(bkey, price, grams=500, **kw):
    return {"bkey": bkey, "price_eff": price, "pack_amount": grams, "pack_unit": "g", "n_units": None,
            "assumed_g": None, "drained_amount": None, "price_per_unit": price / grams * 1000, "per_unit": "kg",
            "clearance": False, "price_suspect": False, "pack_confidence": "high", "data_quality": "ok",
            "variable_weight": False, **kw}


@pytest.mark.parametrize("available,expected", [
    ({"m": "mijesano", "j": "junece", "s": "svinjsko"}, "m"),  # miješano iako je skuplje
    ({"j": "junece", "s": "svinjsko"}, "j"),
    ({"s": "svinjsko", "p": "purece"}, "s"),
])
def test_minced_meat_preference(available, expected):
    from mealmeter.basket import Need, _choose_preferred

    prices = {"m": 6.0, "j": 5.0, "s": 4.0, "p": 3.0}
    rows = [_row(k, prices[k]) for k in available]
    need = Need({"name": "mljeveno meso"}, S["mljeveno_meso"], 500, "g")
    pick = _choose_preferred(rows, need, S["mljeveno_meso"].default_preference, {"vrsta": available})
    assert pick["bkey"] == expected


def test_minced_meat_find_default_values(con):
    res = find_products(ingredient="mljeveno_meso", limit=50, con=con)
    assert all(r["attributes"].get("vrsta") in ("mijesano", "junece", "svinjsko") for r in res)


# --- 4. pileća prsa: stanje ------------------------------------------------------------------

@pytest.mark.parametrize("name,stanje", [
    ("PILEĆI FILE SMRZNUTI", "smrznuto"), ("PILEĆI FILE BRAZILSKI SMRZNUTI", "smrznuto"),
    ("PILEĆI FILE SOLJENI 6X2 BRAZIL", "smrznuto"), ("PILEĆA PRSA LEDO 1 kg", "smrznuto"),
    ("PILEĆI FILE FROZEN 1kg", "smrznuto"), ("PRSA PILEĆA K PLUS BEZ KOŽE", "svjeze"),
])
def test_chicken_stanje(name, stanje):
    from mealmeter.staples import extract_attributes

    assert extract_attributes(S["pileca_prsa"], name)["stanje"] == stanje


def test_chicken_rules(con):
    st = S["pileca_prsa"]
    assert st.default_attributes == {"stanje": "svjeze"}
    from mealmeter.staples import name_match

    assert name_match(st, "PILEĆA PRSA JELI GAVRILOVIĆ") == "excluded"
    lo, hi, src = con.execute("SELECT ppu_min, ppu_max, range_source FROM clean.staple_rules WHERE staple = 'pileca_prsa'").fetchone()
    assert (lo, hi, src) == (2, 20, "manual")  # najširi raspon; po proizvodu vrijedi raspon stanja

# --- 5. luk ----------------------------------------------------------------------------

@pytest.mark.parametrize("name,vrsta", [
    ("LUK SREBRENAC (10)", "srebrenac"),
    ("LUK LJUBIČ./BIJELI ZA GASTRO 1 kg", "ljubicasti"),
    ("KAPULA ŽUTA (CRV.LUK)", "zuti"),
    ("LUK CRVENI", "crveni"),
    ("LUK CRVENI SLATKI 50-70", "slatki"),
    ("LUK BORETTANE 250 g", "borettan"),
    ("KAPULA", "obicni"),
    ("LUK MLADI VEZICA", "mladi"),
])
def test_onion_vrsta(name, vrsta):
    from mealmeter.staples import extract_attributes

    assert extract_attributes(S["luk"], name)["vrsta"] == vrsta


def test_onion_default_and_garlic():
    from mealmeter.staples import name_match

    st = S["luk"]
    excluded = {v for a, v in st.default_exclude_variants if a == "vrsta"}
    assert {"srebrenac", "ljubicasti", "mladi", "slatki", "borettan", "perlice"} <= excluded
    assert not {"crveni", "zuti", "obicni"} & excluded
    assert name_match(st, "LUK BIJELI RFS") == "excluded"  # češnjak
    assert name_match(st, "LUK LJUBIČ./BIJELI ZA GASTRO 1 kg") == "match"


def test_onion_rukavac_assumed_500g():
    st = S["luk"]
    assert st.assumed_pack_g == 500 and st.assumed_pack_regex


# --- 6. jaja i veleprodaja ------------------------------------------------------------------

def test_egg_ranges_by_uzgoj():
    assert S["jaja"].plausible_by == {"uzgoj": {"bio": (0.30, 1.00), "_other": (0.15, 0.55)}}
    assert S["jaja"].plausible_per_unit is None


def test_wholesale_store_type(con):
    assert con.execute("SELECT DISTINCT store_type FROM clean.stores WHERE chain = 'metro'").fetchall() == [
        ("cash_and_carry",)]
    assert con.execute("SELECT count(*) FROM clean.stores WHERE store_type = 'retail'").fetchone()[0] > 0


def test_wholesale_egg_cartons_not_counted(con):
    # "10/1 ARO JAJA" kod Metroa je deset kutija, a ne deset jaja
    assert S["jaja"].units_in_pack("10/1 ARO JAJA A KL M", None, None, {}, wholesale=True) is None
    assert S["jaja"].units_in_pack("10/1 ARO JAJA A KL M", None, None, {}) == 10
    assert S["jaja"].units_in_pack("JAJA 30 KOM", None, None, {}, wholesale=True) == 30
    n = con.execute("SELECT n_units FROM clean.product_staples WHERE chain = 'metro' AND staple = 'jaja'").fetchall()
    assert n and all(v is None for (v,) in n)


def test_wholesale_excluded_by_default(con):
    from mealmeter.basket import plan_basket
    from mealmeter.search import get_prices

    assert not any("metro" in r["chains"] for r in find_products("aro jaja", city="Osijek", con=con))
    assert any("metro" in r["chains"] for r in find_products("aro jaja", city="Osijek", con=con,
                                                            include_wholesale=True))
    assert get_prices("metro:226729", con=con) == []
    assert get_prices("metro:226729", con=con, include_wholesale=True)
    res = plan_basket([{"name": "jaja", "amount": 2, "unit": "kom"}], "Osijek", con=con)
    assert not any(s["chain"] == "metro" for s in res["stores"])


# --- 7. vrećice ------------------------------------------------------------------------

@pytest.mark.parametrize("name,count", [
    ("VANIL ŠEĆER 8 g DOLCELA 5+1 GRAT", 6), ("PRAŠAK ZA PECIVO 3 PAK", 3), ("6X8G DOLCELA VANILIN ŠEĆER", 6),
    ("12GX6 DOLCELA PRAŠAK ZA PECIVO", 6), ("DOLCELA VANILIN ŠEĆER 8 g 10kom PODRAVKA", 10),
    ("VANILIN AROMA (5VRE.)2G", 5), ("KVASAC SVJEŽI 50g(2*25g) DUOS", 2), ("KVASAC SUH.10g ALEVA", 1),
    ("KVASAC 500 g RINFUZA", 1),
])
def test_sachet_count(name, count):
    from mealmeter.staples import sachet_count

    assert sachet_count(name) == count


@pytest.mark.parametrize("key,name,price,suspect", [
    ("vanilin_secer", "KOTANYI BOURBON VANILIN ŠEĆER 10g", 1.19, False),
    ("kvasac", "KVASAC SUH.10g ALEVA", 0.36, False),
    ("kvasac", "KLC.Suhi kvasac 7 g", 0.13, False),
    ("kvasac", "42G DI-GO DOMAĆI SVJ. KVAS.", 19.50, True),
    ("prasak_za_pecivo", "12GX6 DOLCELA PRAŠAK ZA PECIVO", 32.40, True),  # 5,40 €/vrećica
])
def test_sachet_price_ranges(con, key, name, price, suspect):
    from mealmeter.staples import staple_suspect_sql

    n = S[key].units_in_pack(name, None, None, {})
    lo, hi = S[key].plausible_per_pack
    got = con.execute(f"SELECT {staple_suspect_sql(str(price / n), str(n))} FROM (SELECT ? AS ppu_min, ? AS ppu_max) r",
                      [lo, hi]).fetchone()[0]
    assert got is suspect


def test_sachet_ranges_values():
    assert S["kvasac"].plausible_per_pack == (0.10, 1.50)
    assert S["prasak_za_pecivo"].plausible_per_pack == (0.10, 0.60)
    assert S["vanilin_secer"].plausible_per_pack == (0.10, 1.80)


# --- 8. peršin -------------------------------------------------------------------------

def test_persin_default_leaf():
    from mealmeter.basket import resolve_name
    from mealmeter.staples import extract_attributes

    st = S["persin"]
    assert st.default_attributes == {"dio": "list"} and st.assume_piece
    assert extract_attributes(st, "PERŠIN")["dio"] == "list"
    assert extract_attributes(st, "PERŠIN KORJEN AGROVIR")["dio"] == "korijen"
    assert resolve_name("peršin korijen") == (st, {"dio": "korijen"})
    assert resolve_name("peršin") == (st, {})


def test_persin_bunch_assumed(tmp_path):
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "p.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'P1', 'konzum:P1', 'PERŠIN LIST', 'HRANA', 'KOM'),
                 ('konzum', 'P2', 'konzum:P2', 'PERŠIN LIST', 'HRANA', 'KG')""")
    build_clean(c)
    got = dict(c.execute("""SELECT product_id, assumed_g FROM clean.product_staples
                            WHERE staple = 'persin' AND product_id IN ('P1', 'P2')""").fetchall())
    assert got == {"P1": 50, "P2": None}  # na vagu (kg) bez procjene


# --- 9. mjere i težine komada ----------------------------------------------------------------

@pytest.mark.parametrize("amount,unit,staple,expected", [
    (1, "žlica", "kakao", 6.75), (1, "žlica", "med", 21.0), (1, "žličica", "prasak_za_pecivo", 4.0),
    (1, "šalica", "griz", 162.5), (1, "šalica", "zobene_pahuljice", 90.0), (1, "žlica", "krusne_mrvice", 6.75),
    (1, "žličica", "mljevena_paprika", 2.25), (1, "žličica", "papar", 2.5), (1, "žličica", "dodatak_jelima", 4.5),
    (1, "žlica", "persin", 3.75),
    (2, "kom", "luk", 300), (3, "češnja", "cesnjak", 15), (1, "kom", "mrkva", 100), (1, "kom", "krumpir", 200),
    (1, "kom", "rajcica", 120), (1, "kom", "paprika", 150), (1, "kom", "tikvica", 250), (1, "kom", "jabuka", 180),
    (1, "kom", "limun", 120), (1, "kom", "naranca", 200), (1, "kom", "banana", 150), (1, "vezica", "persin", 50),
])
def test_convert_measures_and_pieces(amount, unit, staple, expected):
    from mealmeter.units import convert

    qty, base, warnings = convert(amount, unit, S[staple])
    assert base == "g" and qty == pytest.approx(expected) and "procjena" in warnings[0]


def test_convert_vinegar_spoon_is_ml():
    from mealmeter.units import convert

    assert convert(1, "žlica", S["ocat"])[:2] == (15, "ml")


def test_convert_piece_unknown():
    from mealmeter.units import convert

    with pytest.raises(ValueError):
        convert(1, "kom", S["brasno"])


def test_all_units_estimates():
    import yaml

    from mealmeter.units import UNITS_PATH

    raw = yaml.safe_load(UNITS_PATH.read_text(encoding="utf-8"))
    for section in ("measures", "densities", "pieces"):
        assert all(v["estimate"] for v in raw[section].values()), section
    assert not any(st.piece_g for st in S.values())  # mase komada su samo u units.yaml


# --- 10. filtar hrane: neprehrana u kategoriji hrane ---------------------------------------------

@pytest.mark.parametrize("name,broad,group", [
    ("IGRAČKA HUGI WUGI BLOW BUBBLE 12/1", False, "ostalo"),
    ("SALVETE DAISY MI BOŽIĆNA ZVIJEZDA 20/1", False, "kucanstvo"),
    ("BOŽ.SVIJEĆA 12 cm BIJELA", False, "kucanstvo"),
    ("BATERIJE AA 4/1", False, "kucanstvo"),
    ("SJEME KUKURUZ SECERAC", False, "ostalo"),
    ("TANJURIĆI STAKLO 15X15cm HO-rasprodaja", False, None),  # samo širi popis
    ("TANJURIĆI STAKLO 15X15cm HO-rasprodaja", True, "kucanstvo"),
    ("KUHINJSKA KRPA SET 2/1 50X70CM", True, "kucanstvo"),
    ("CVIJE ORHID.POSUD.CIKL.47 cm", True, "ostalo"),
    ("SLADOLED ČAŠA VANILIJA 150 ml", True, None),  # "ČAŠA" u sladoledu je pakiranje
    ("KRUH KALUP 500g", True, None),
    ("WHISKY BALLANTINES 2 ČAŠE 0,7 l", True, "kucanstvo"),
    ("DEKOR ŠARENO PISMO 76 g DR.OET", True, None),
    ("BOMBONI 4g +IGRAČKA PONY", False, None),
])
def test_nonfood_in_food(name, broad, group):
    from mealmeter.food import nonfood_in_food

    assert nonfood_in_food(name, broad=broad) == group


def test_chain_verify_map():
    from mealmeter.food import load_chain_verify

    v = load_chain_verify()
    assert v["gavranovic"] == {"hrana"} and v["boso"] == {"zeleni program"} and v["studenac"] == {"hrana"}
    assert v["plodine"] == {"ean_inherited"}


def test_cup_rule_words():
    from mealmeter.food import words_group

    assert words_group("ČAŠE ZA VODU 6/1 280 ml") == "kucanstvo"
    assert words_group("ČAŠA ZA PIVO 565ml") == "kucanstvo"
    assert words_group("JOG.TEK.0.9% 500 G ČAŠA VINDIJA") is None


@pytest.mark.parametrize("name", ["KULENOV CVIJET NARESCI 80g GAVRILOVIĆ", "Milka Paket s plišanom igračkom 96 g",
                                  "FLIPS S IGRAČKOM 60 g GUSTO", "KOŠARICE ZA PRINCES KRAFNE 120 g",
                                  "BIO CVIJET SOLI 125 g ADRIATIQ"])
def test_nonfood_in_food_edible_guard(name):
    from mealmeter.food import nonfood_in_food

    assert nonfood_in_food(name, broad=True) is None


# --- 12. mahunarke bez oblika ---------------------------------------------------------------

def test_beans_without_form_ask(con):
    from mealmeter.basket import plan_basket

    res = plan_basket([{"name": "grah", "amount": 400, "unit": "g"}], "Osijek", con=con)
    assert res["ambiguous"] and not res["ingredients"]
    amb = res["ambiguous"][0]["ambiguity"]
    assert amb["form"] == ["suho", "konzerva"] and amb["question"] == "suho ili konzerva?"
    assert set(amb["prices"]) == {"suho", "konzerva"}
    res = plan_basket([{"name": "grah", "amount": 400, "unit": "g", "form": "suho"}], "Osijek", con=con)
    assert not res["ambiguous"] and res["best_store"]["items"][0]["attributes"]["oblik"] == "suho"


def test_drained_mass_means_can():
    from mealmeter.staples import form_heuristic

    assert form_heuristic(S["grah"], "GRAH CRVENI 400/240 g E BUONO", "KOM", 400, "g", 240) == "konzerva"


def _groups_for(staple_key: str, names: list[str], pack_unit="g"):
    """Grupa od jednog EAN-a s nazivom po lancu; podudaranje prema stvarnim pravilima namirnice."""
    from mealmeter.staples import name_match

    rows = []
    for i, name in enumerate(names):
        hit = name_match(S[staple_key], name)
        rows.append((f"lanac{i}", "1", name, None if hit is None else hit == "excluded"))
    return _mini_groups(rows, pack_unit=pack_unit)["1"]


def test_cavatappi_member():
    # Korak 2E.1: bez kratica samo "TJESTENINA ..." prolazi (m = 50 %) -> slabi član. Od točke 4 se "TJ."
    # proširuje u "tjestenina" (data/abbrev.yaml), pa oba naziva prolaze i grupa je snažni član.
    assert _groups_for("tjestenina", ["TJ.CAVATAPPI 63 500 g", "TJESTENINA CAVATAPPI 63 500G"]) == ("member", "strong")
    assert _groups_for("tjestenina", ["RUMMO 63 500 g", "TJESTENINA CAVATAPPI 63 500G"]) == ("member", "weak")


# --- 2E.2 tvrda neprehrana na razini grupe ---------------------------------------------------

@pytest.mark.parametrize("name,category,unit,hard", [
    ("SJEME GARDEN KARANFIL FIORI SEMP", "ZELENI PROGRAM", None, True),
    ("SJEME KUKURUZ SECERAC", None, None, True),
    ("BUČINO SJEME 150 g II KL", "VOĆE I POVRĆE", "g", False),
    ("SUNCOKRETOVO SJEME OLJUŠTENO 200 g", None, "g", False),  # nesigurno: ostaje unknown
    ("GRAH ŽUTI GARDEN 100 g", "ZELENI PROGRAM", "g", True),
    ("IGRAČKA S BOMBONIMA", "HRANA", None, True), ("SAPUN TEKUĆI 500 ml", None, "ml", True),
    ("SVIJEĆA MIRISNA", None, None, True), ("BATERIJE AA", None, None, True),
    ("GLAZBENA ČESTITKA", None, None, True), ("MLIJEKO 1L", "HRANA", "ml", False),
])
def test_hard_nonfood(name, category, unit, hard):
    from mealmeter.food import hard_nonfood

    assert hard_nonfood(name, category, unit) is hard


def test_hard_nonfood_excludes_group():
    rows = [("a", "1", "grasak", False), ("b", "1", "grasak", False), ("c", "1", "sjeme garden grasak", True)]
    assert _mini_groups(rows)["1"] == ("excluded", None)


def test_seed_words_unsure_stays_unknown():
    from mealmeter.food import words_group

    assert words_group("SUNCOKRETOVO SJEME OLJUŠTENO 200 g", None, "g") is None
    assert words_group("SJEME KUKURUZ SECERAC", None, None) == "ostalo"



@pytest.mark.parametrize("name", ["GRAH CRVENI GARDEN GOOD 3X210/140 g", "AJVAR GARDEN GOOD BLAGI PREM 290g",
                                  "OKRUGLICE VEGAN GARDEN GOURMET 300g", "DANISH WHITE 800 g DIVAN GARDEN",
                                  "Garden eko riža integralna 500g", "Garden Leća crvena bio 500 g"])
def test_garden_food_brands_not_hard(name):
    from mealmeter.food import hard_nonfood

    assert not hard_nonfood(name, "HRANA", "g")


# --- 2E.3 jedinica pakiranja ---------------------------------------------------------------

def test_egg_in_grams_dropped(tmp_path):
    from mealmeter.build import build_clean, load_raw
    from tests.conftest import FIXTURE

    c = duckdb.connect(str(tmp_path / "u.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    c.execute("""INSERT INTO products (chain, product_id, barcode, name, category, unit) VALUES
                 ('konzum', 'E1', 'konzum:E1', 'JAJE PRINCESS SUPRISE 15g', 'HRANA', 'KOM'),
                 ('konzum', 'E2', 'konzum:E2', 'JAJA M 10 KOM 600 g', 'HRANA', 'KOM'),
                 ('konzum', 'S1', 'konzum:S1', 'SALATA PUTERICA 1KOM', 'HRANA', 'KOM'),
                 ('konzum', 'V1', 'konzum:V1', 'VRHNJE ZA KUHANJE 20% 200 g', 'HRANA', 'KOM')""")
    build_clean(c)
    got = dict(c.execute("""SELECT product_id, coalesce(drop_reason, 'ok') FROM clean.product_staples
                            WHERE product_id IN ('E1', 'E2', 'S1', 'V1') AND NOT excluded""").fetchall())
    assert got == {"E1": "jedinica", "E2": "ok", "S1": "ok", "V1": "ok"}



# --- 2E.4 kratice i sinonimi --------------------------------------------------------------------

@pytest.mark.parametrize("name,expected", [
    ("PRAŠ. PEC. 12 g Dr.Oetker", "prasak za pecivo 12 g dr oetker"),
    ("BRAŠ.PŠ.GLATKO T-550", "brasno ps glatko t 550"),
    ("MLIJ.ČOK. 0,5L", "mlijeko cok 0 5l"),
    ("JOG.2,8% 330g MEGGLE", "jogurt 2 8 330g meggle"),
    ("TJ.CAVATAPPI 63 500 g", "tjestenina cavatappi 63 500 g"),
    ("PEČ.SLANI KUKURUZ", "pec slani kukuruz"),  # "pec." sam nije pecivo
])
def test_match_text_abbrev(name, expected):
    from mealmeter.staples import match_text

    assert match_text(name) == expected


@pytest.mark.parametrize("key,name,expected", [
    ("tjestenina", "CONCHIGLIE 500 g", "match"), ("tjestenina", "ŠKOLJKE DAGNJE 1 kg", "excluded"),
    ("tjestenina", "PILEĆI REZANCI 400 g", "excluded"), ("tjestenina", "LAZANJE 500g LISTOVI", "match"),
    ("jogurt", "JOG.2,8% 330g MEGGLE", "match"), ("pileca_prsa", "ODRESCI PILEĆI FILE 500 g", "match"),
    ("pileca_prsa", "PILEĆI FILE OD PRSA", "match"), ("svinjetina", "SV REBRA", "match"),
    ("vrhnje_za_kuhanje", "CREME CUISINE 200ml", "match"), ("tvrdi_sir", "LEERDAMMER 200 g", "match"),
    ("tvrdi_sir", "EDAMAME 300g", None), ("tuna", "TUNA SAL.RIO MARE COUS 2X160 g", "excluded"),
    ("prasak_za_pecivo", "PRAŠ. PEC. 12 g Dr.Oetker", "match"),
])
def test_point4_rules(key, name, expected):
    from mealmeter.staples import name_match

    assert name_match(S[key], name) == expected


def test_tuna_cous_cous_not_member():
    assert _groups_for("tuna", ["TUNA SAL.RIO MARE COUS 2X160 g", "Rio Mare Insal.sal.tuna cous cous2x160g",
                                "TUNJ SALATA COUS COUS 2X160g RIO MARE"])[0] != "member"


@pytest.mark.parametrize("key,name,expected", [
    ("pileca_prsa", "Cekin Pil. prsa bk, svj. 650g", "match"),  # "cca" je namjerno isključen
    ("tvrdi_sir", "UMAK SM CHEDDAR PINATA 3000g", "excluded"),
    ("mlijeko", "SET.SEC./MLIJ.KER.MORE 027756 MJ", "excluded"),
    ("tjestenina", "RANA LASAGNE RICOTTA SPIN 350 g", "excluded"),
    ("tjestenina", "TIJESTO ŠIR VALJ REZANCI S JAJIMA 400g", "match"),
    ("tjestenina", "PRAL.SPAR PREMIUM ŠKOLJK.250 g", "excluded"),
    ("tjestenina", "ELINA ARGAN MLIJEKO ZA TJ 250ml", "excluded"),
])
def test_point4_false_hits(key, name, expected):
    from mealmeter.staples import name_match

    assert name_match(S[key], name) == expected
