import pytest

from mealmeter.search import find_products
from mealmeter.staples import extract_attributes, load_staples, resolve_ingredient

STAPLES = load_staples()


def test_dictionary_loads_and_is_valid():
    assert len(STAPLES) >= 60
    for st in STAPLES.values():
        assert st.unit in ("kg", "l", "kom")
        assert st.must_match and st.synonyms
    for key in ("brasno", "secer", "sol", "ulje", "maslac", "mlijeko", "jaja", "luk", "krumpir",
                "rajcica", "riza", "tjestenina"):
        assert key in STAPLES


def test_required_attributes_exist():
    assert {"glatko", "ostro", "integralno"} <= set(STAPLES["brasno"].attributes["tip"])
    assert {"0.5", "1.5", "2.8", "3.2"} <= set(STAPLES["mlijeko"].attributes["mast"])
    assert "vrsta" in STAPLES["riza"].attributes
    assert STAPLES["krumpir"].loose_produce and not STAPLES["brasno"].loose_produce


@pytest.mark.parametrize("text,key", [
    ("Brašno", "brasno"), ("BRASNO", "brasno"), ("kokošja jaja", "jaja"), ("jaje", "jaja"),
    ("šećer", "secer"), ("Mlijeko", "mlijeko"), ("špageti", "tjestenina"), ("pasirana_rajcica", "pasirana_rajcica"),
])
def test_resolve_ingredient(text, key):
    assert resolve_ingredient(text).key == key


@pytest.mark.parametrize("text", ["čokoladno mlijeko", "brašno glatko", "", None, "xyz"])
def test_resolve_ingredient_only_exact(text):
    assert resolve_ingredient(text) is None


@pytest.mark.parametrize("key,name,expected", [
    # stvarni nazivi iz arhive
    ("brasno", "BRAŠNO GLATKO T-550 1kg PODRAVKA", {"tip": "glatko", "oznaka": "t550"}),
    ("brasno", "BRAŠNO PŠEN. T-400 OŠTRO 1 KG (10) (PAL60) PODRAVKA", {"tip": "ostro", "vrsta": "psenicno", "oznaka": "t400"}),
    ("brasno", "BRAŠNO KUKURUZNO 1KG (10) (PAL 60), PODRAVKA", {"vrsta": "kukuruzno"}),
    ("mlijeko", "N-MLIJEKO DUKAT 1.00L 2.8%MM EDGE -12/1- 11214", {"mast": "2.8"}),
    ("mlijeko", "MLIJEKO DUKAT 1.00L 1.5%MM EDGE LAGANO JUTRO TRAJNO -12/1", {"mast": "1.5", "vrsta": "trajno"}),
    ("mlijeko", "MLIJEKO TRAJNO LAGANO JUTRO 1,5 % mm 1L EDGE", {"mast": "1.5", "vrsta": "trajno"}),
    ("mlijeko", "N-*MLIJEKO Z BREGOV SVJEŽE 3.2%MM 1L 21 DAN", {"mast": "3.2", "vrsta": "svjeze"}),
    ("mlijeko", "Mlijeko trajno 1,5 L", {"vrsta": "trajno"}),  # 1,5 L je volumen, ne mast
    ("riza", "RIŽA BASMATI BIJELA DUGOGA ZRNA 1kg RIO-PAK", {"vrsta": "basmati"}),
    ("riza", "Riso Scotti riža arborio dugo zrno 1kg", {"vrsta": "arborio"}),
    ("jaja", "N-JAJA PERFA AKLASARAZRED M 10KOM -18/1", {"velicina": "m"}),
])
def test_extract_attributes(key, name, expected):
    got = extract_attributes(STAPLES[key], name)
    assert expected.items() <= got.items()


# --- find_products s namirnicom (fixture) -------------------------------------


def test_milk_excludes_chocolate_and_soy(con):
    res = find_products("mlijeko", con=con)
    names = [r["name"].lower() for r in res]
    assert res and all(r["ingredient"] == "mlijeko" for r in res)
    assert any("trajno" in n for n in names)
    assert not any("čokolad" in n or "soj" in n for n in names)
    # slobodnim upitom čokoladno mlijeko i dalje se može naći
    assert any("ČOKOLADNO" in r["name"] for r in find_products("čokoladno mlijeko", con=con))


def test_milk_attribute_and_unit(con):
    res = find_products(ingredient="mlijeko", attributes={"mast": "2.8"}, con=con)
    assert len(res) == 1
    r = res[0]
    assert r["attributes"]["mast"] == "2.8" and r["per_unit"] == "l"
    assert (r["unit_confidence"], r["pack_source"]) == ("high", "name")
    assert find_products(ingredient="mlijeko", attributes={"mast": "0.5"}, con=con) == []


def test_flour_type_filter(con):
    glatko = find_products(ingredient="brasno", attributes={"tip": "glatko"}, con=con)
    ostro = find_products(ingredient="brašno", attributes={"tip": "ostro"}, con=con)
    assert glatko and ostro
    assert all(r["attributes"]["tip"] == "glatko" for r in glatko)
    assert [r["id"] for r in ostro] == ["3850104223631"]
    assert {r["id"] for r in find_products(ingredient="brasno", con=con)} == {r["id"] for r in glatko + ostro}


def test_ingredient_with_city_and_query(con):
    res = find_products("podravka", ingredient="brasno", city="Osijek", con=con)
    assert res and all("podravka" in r["name"].lower() for r in res)


def test_ingredient_validation(con):
    with pytest.raises(ValueError):
        find_products(ingredient="nepostojece", con=con)
    with pytest.raises(ValueError):
        find_products(ingredient="brasno", attributes={"tip": "mekano"}, con=con)
    with pytest.raises(ValueError):
        find_products("brasno", attributes={"tip": "glatko"}, con=con)


def test_loose_produce_banana(con):
    res = find_products(ingredient="banana", con=con)
    assert res and all(r["id"].startswith("ntl:") for r in res)
    assert {r["per_unit"] for r in res} == {"kg"}
