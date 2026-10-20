"""Ispravci rječnika nakon ručnog pregleda (Korak 2A2). Svi nazivi su stvarni, iz arhive 2026-10-19."""

import pytest

from mealmeter.staples import extract_attributes, load_staples, name_match

S = load_staples()


# --- 1. pogrešna isključenja -------------------------------------------------

@pytest.mark.parametrize("key,name", [
    ("brasno", "BRAŠ.PŠE.T-1100 PODRAVKA 1 kg"),  # "PŠE." više ne pogađa pse\b (hrana za pse)
    ("brasno", "BRAŠNO PŠE. T-850 1 kg"),
    ("sol", "SOL KUHINJSKA SITNA MORSKA KUTIJA 1KG, SOLANA PAG"),
    ("sol", "SOL KRUPNA KUTIJA 1 kg"),
    ("margarin", "MARGARIN ZA KOLAČE 250g BAKINA KUHINJA"),
    ("jaja", "JAJA M 10/1 PODN.UZ. GALA"),
    ("riza", "RIŽA DUGO ZRNO PARBOIL.500g BEN'S"),
    ("riza", "RIŽA ZLATNO POLJE ZA DOMAĆA JELA 1 kg PODR"),
    ("kakao", "KAKAO U PRAHU 100g KRAŠ"),
    ("dodatak_jelima", "VEGETA NATUR VR 150g PODRAVKA"),
    ("persin", "PERŠIN KORIJEN LIST 300g"),
    ("persin", "PERSIN LIST BOC.10 G PLODINE"),
    ("tvrdi_sir", "SIR GAUDA RIBANI 200g VINDIJA"),
])
def test_wrong_exclusions_removed(key, name):
    assert name_match(S[key], name) == "match"


@pytest.mark.parametrize("key,name", [
    ("junetina", "TOMI GOVEDINA 1200 g ZA PSE"),  # "za pse" i dalje isključuje hranu za pse
    ("junetina", "Purina One hrana za pse govedina"),
])
def test_dog_food_still_excluded(key, name):
    # "excluded" (za pse) ili None (nema dijela mesa iz require_any, Korak 2A2.5)
    assert name_match(S[key], name) != "match"


@pytest.mark.parametrize("key,name", [
    ("dodatak_jelima", "VEGETA TWIST ZA KRUMPIR 20G"),
    ("dodatak_jelima", "VEGETA GRILL ZAČIN 50G"),
    ("dodatak_jelima", "VEGETA MAESTRO PAPAR 30G"),
])
def test_vegeta_variants_excluded(key, name):
    assert name_match(S[key], name) == "excluded"


@pytest.mark.parametrize("key,name,expected", [
    ("brasno", "BRAŠ.PŠE.T-1100 PODRAVKA 1 kg", {"vrsta": "psenicno", "oznaka": "t1100"}),
    ("brasno", "BRAŠNO PŠE. T-850 1 kg", {"vrsta": "psenicno", "oznaka": "t850"}),
    ("persin", "PERŠIN KORIJEN S-BUDGET 250 g", {"dio": "korijen"}),
    ("persin", "PERSIN LIST BOC.10 G PLODINE", {"dio": "list"}),
    ("tvrdi_sir", "SIR GAUDA RIBANI 200g VINDIJA", {"oblik": "ribani", "vrsta": "gauda"}),
    ("tvrdi_sir", "SIR TVRDI RIBANAC 40g DUKAT (25)", {"oblik": "ribani"}),
])
def test_new_attributes(key, name, expected):
    assert expected.items() <= extract_attributes(S[key], name).items()


# --- 2. neprehrambeni proizvodi ----------------------------------------------

@pytest.mark.parametrize("category,group", [
    ("HRANA", "hrana"), ("PAKIRANA HRANA I PIĆE", "pice"), ("PIĆE", "pice"),
    ("KOZMETIKA", "kozmetika"), ("dekorativna kozmetika", "kozmetika"), ("tijelo", "kozmetika"),
    ("TOALETNE POTREPŠTINE", "higijena"), ("ZUBNA PASTA", "higijena"),
    ("PROIZVODI ZA KUĆANSTVO", "kucanstvo"), ("SREDSTVA ZA ČIŠĆENJE", "kucanstvo"), ("NEPREHRANA", "ostalo"),
    ("bebe & djeca", "djeca"), ("DJEČJA HRANA", "djeca"), ("KOZMETIKA ZA DJECU", "djeca"),
    ("KOZMETIKA ZA SUNČANJE", "kozmetika"), ("SUNCOKRETOVO ULJE", "hrana"),
    ("IGRAČKE", "ostalo"), ("kućni ljubimci", "kucni_ljubimci"), ("Ostalo", "unknown"), (None, "unknown"),
    ("VINO DOMAĆE", "alkohol"), ("ŽESTOKO", "alkohol"), ("BEZALKOHOLNA PIĆA", "pice"),
    ("ALKOHOLNI OCAT", "hrana"), ("PRIPREMA JELA", "hrana"), ("cajno pecivo punjeno", "hrana"),
    ("zdravlje", "ostalo"), ("trgovacka roba", "unknown"),
])
def test_category_group(category, group):
    from mealmeter.normalize import category_group
    assert category_group(category) == group


@pytest.mark.parametrize("key,name", [
    ("ulje", "PIZ BUN ULJE SPF 15"),
    ("ulje", "EVELINE ULJE ZA SUNČANJE S AKCELERATOROM ZF 10 150ML"),
    ("ulje", "PRONTO ULJE ZA REST.NAMJEŠTAJA 100mL"),
    ("ulje", "N-ULJE BECUTAN 200ML ZA DJECU-12/1-"),
    ("sol", "PIVO SOL 0,33L"),
    ("sol", "N-*PIVO SOL 0.33L -24/1- 4.5%ALC BOCA"),
    ("sol", "NITRITNA SOL 1/1 DERMA SEZONA"),
    ("jaja", "ŽLIČICE ZA JAJA 6/1 FACKELMANN"),
    ("jaja", "JAJE ZA CAJ VELIKO 49162"),
    ("jaja", "DEKORATIVNA JAJA ZA OSLIKAVANJE 6KOM"),
    ("kakao", "KOLAČ MUFFIN KAKAO 40 gr BEZ GLUTENA"),
    ("kakao", "KOL. TORTINA KAKAO VINCINI 200 g"),
    ("kakao", "DONUT GLAZ KAKAO 69 g SMRZ BOB"),
    ("maslac", "BOMBON BUTTER CANDIES 100g"),
    ("maslac", "MASLAC SA ZAČINSKIM BILJEM 125g MEGL"),
    ("secer", "SECER KOKOS PALME 200 G ENCIAN"),
    ("secer", "SECER S AROMOM NARANCE 50 G KOTANYI"),
    ("rajcica", "RAJČICA SJEC.SIT.MUTTI 3X400 g"),
    ("rajcica", "PAPRIKA PARADAJZERICA NTL"),
    ("paprika", "PAPRIKA LJUTA 1KG NADALINA"),
    ("paprika", "PAPRIKA GOLDEW PEPPADEW 3 kg"),
    ("parmezan", "SALAMA S PARMEZANOM 75 g"),
    ("parmezan", "RIŽOT S PARMEZANOM I CARNAROLI RIŽOM 210 g NIKA"),
    ("vanilin_secer", "VANILIN KIFLICE 400 G"),
    ("vanilin_secer", "SLADILO SWEET ZERO VANILIN 8 g DR.OETKER"),
    ("limun", "TORTA LIMUN 500 g COOP"),
    ("limun", "MUFFIN LIMUN 80 g PAN PEK"),
    ("jabuka", "PJESCANIK JABUKA CRVENI"),
    ("naranca", "Torta naranča 1950g"),
    ("banana", "DONUT BANANA TOCKICE 54 G LA LORRAINE"),
    ("riza", "TJESTO RIŽA VERMICELLI 250G"),
    ("riza", "TJESTENINA OD RIŽE 250g YOUWOK"),
    ("tjestenina", "Talianetta Tjestenina Milaneze 155g"),
    ("tjestenina", "MAKARON NAPOLITANA 160g TALIAN POD"),
    ("pileca_prsa", "PILEĆI FILE ZABATKA 500g SVJ.PIPO"),
    ("pileca_prsa", "FILE PILEĆEG BATKA ZABATKA 500 g SVJEŽI PERUTNINA"),
    ("kukuruz", "KUKURUZ CHIO SLANI ZA MIKROVALNU 80g"),
    ("kukuruz", "KUKURUZ PRŽ. SLANI S OKUSOM ČILIJA 55 g MOGYI"),
    ("kukuruz", "KUKURUZ ZA MKV PEĆ.(3x100) 300G FRANCK (16)"),
    ("jogurt", "JOGURT DUKATOS BADEM PISTACIJA 150 g DUKAT"),
    ("jogurt", "JOGURT NAR./CIMET150 g DUKATOS"),
    ("svjezi_sir", "DUKATINO SVJEŽI SIR S VOĆEM 6X50G (8) DUKAT"),
    ("svjezi_sir", "ŠTRUKLI SA SVJ SIR SLATKI 600g SMRZ"),
])
def test_point2_exclusions(key, name):
    # kakao od Koraka 2C ima pozitivno podudaranje, pa takvi nazivi nisu ni kandidati (None)
    assert name_match(S[key], name) in (("excluded", None) if key == "kakao" else ("excluded",))


@pytest.mark.parametrize("key,name", [
    # "sun" iz zadatka je dodan kao sun\b + suncan, da suncokretovo ulje ostane
    ("ulje", "ULJE SUNCOKRET PVC 1L (15) (PAL 675), ZVIJEZDA"),
    ("ulje", "N-ULJE SUNCOKRET 1L TENA-10/1 (pal.750kom)"),
    ("jogurt", "N-*DUKAT JOGURT 1000G TEKUĆI-6/1- 2.8%MM 32363"),
    ("kukuruz", "KUKURUZ ŠEĆERAC 340 g PODRAVKA (10) OC. MASA 280 g"),
])
def test_point2_keeps_real_products(key, name):
    assert name_match(S[key], name) == "match"


# --- 3. sustavna pravila ------------------------------------------------------

from dataclasses import replace  # noqa: E402

import duckdb  # noqa: E402

from mealmeter import search  # noqa: E402
from mealmeter.build import build_clean, load_raw  # noqa: E402
from mealmeter.normalize import analyze_pack, is_clearance  # noqa: E402

# (naziv, bruto (količina, jedinica) ili None, ocijeđena masa ili None) — stvarni nazivi
MULTIPACK = [
    # tuna
    ("CALVO TUNA U MASLINOVOM ULJU 3X65g", (195, "g"), None),
    ("EVA TUNA KOM.BILJ 4*80 GR", (320, "g"), None),
    ("EVA TUNA KOMADI B.U. 4 x 80 g 3+1 GRATIS", (320, "g"), None),
    ("KFJ TUNA 2x80 g", (160, "g"), None),
    ("EVA TUNA FILETI U ULJU RIBA 115/81G, (30) (PAL144)", (115, "g"), 81),
    ("KLC.Tuna u extr.djev.maslin.ulju185/140g", (185, "g"), 140),
    ("KLC.Tuna u suncokretovom ulju 3x80/56 g", (240, "g"), 168),
    ("KLC.File tune u suncokr.ulju 3x80g/3x56g", (240, "g"), 168),
    ("KLC.File tune u masl.ulju 3x70g/50g", (210, "g"), 150),
    ("Kaiser Franz J.tuna u ulju 2x80/2x52g", (160, "g"), 104),
    ("TUNA KOMADI NATURALE RIO MARE 160 g (OCIJEĐENA MASA 122 g) ORBICO", (160, "g"), 122),
    ("TUNA ŽUTOPERAJNA ODREZ. U SUNC. ULJU 170g (OCJ. MASA 120g)GIANA", (170, "g"), 120),
    # kvasac
    ("7GX5 DR.OETKER KVASAC(4+1)", (35, "g"), None),
    ("DI-GO INST. SUHI PEKARSKI KVASAC 7 g 4+1 GRAT (10)", (35, "g"), None),
    ("DOLCELA INSTANT SUHI KVASAC 7 g 4+1 GRATIS, PODRAVKA", (35, "g"), None),
    ("INSTANT SUHI KVASAC 35G 4+1GRATIS", (35, "g"), None),  # 35 g je već ukupno
    ("DI-GO KVASAC 5X7G PODRAVKA", (35, "g"), None),
    ("KVASAC DI-GO -10/1 35G 5*7G SUHI -10/1-", (35, "g"), None),  # -10/1- je karton
    ("2X25G DUOS SVJEŽI PEK KVASAC", (50, "g"), None),
    ("KVASAC 4+1", None, None),
    # vanilin šećer
    ("DOLCELA VANILIN ŠEĆER 8 g 5+1 GRATIS PODRAVKA (44)", (48, "g"), None),
    ("DOLCELA VANILIN ŠEĆER 8 g 6 PAK PODRAVKA (16)", (48, "g"), None),
    ("DR.OETKER VANILIN ŠEĆER 5+1 48GR", (48, "g"), None),
    ("8GX10 DR.OETK.VANILIN ŠEĆ. 8+2", (80, "g"), None),
    ("VANILIN ŠEĆER BOUR. DOLCELA 10 g 3/1", (30, "g"), None),
    ("ULTRA VANILIN ŠEĆER 5/1 50G (45)", (50, "g"), None),
    ("KOTANYI 20G BOURBON VANILIN ŠEĆER -25/1-", (20, "g"), None),
    # prašak za pecivo
    ("PRAŠAK ZA PECIVO 12 g 5+1 GRATIS PODRAVKA", (72, "g"), None),
    ("PRAŠAK ZA PECIVO 12 G 6PAK DOLCELA", (72, "g"), None),
    ("DOLCELA PRAŠAK ZA PECIVO 12 g 10 pak (48) PODRAVKA", (120, "g"), None),
    ("PRASAK ZA PECIVO 96 G 6+2 GRATIS", (96, "g"), None),
    ("PRAŠAK ZA PECIVO (5 x 12g) 60g FINETA", (60, "g"), None),
    ("PRAŠAK ZA PECIVO 10*12 g DOLCE", (120, "g"), None),
    # konzerve
    ("KUKURUZ ŠEĆERAC 340 g PODRAVKA (10) OC. MASA 280 g", (340, "g"), 280),
    ("N-KUKURUZ ŠEĆERAC 170G (NETTOMASA 140G)BONDUELLE-12/1 0504", (170, "g"), 140),
    ("GRAH SMEĐI 800g LIM.PODRAVKA-ocijeđene mase 460g", (800, "g"), 460),
    ("KRASTAVCI MARINO O.M.350g", None, 350),
]


@pytest.mark.parametrize("name,gross,drained", MULTIPACK)
def test_multipack_and_drained(name, gross, drained):
    got_gross, got_drained, variable, _ = analyze_pack(name)
    assert not variable
    assert got_gross == (None if gross is None else (pytest.approx(gross[0]), gross[1]))
    assert got_drained == (None if drained is None else pytest.approx(drained))


def test_enough_multipack_examples():
    sachet = [n for n, *_ in MULTIPACK if any(w in n.upper() for w in ("TUN", "KVAS", "VANILIN", "PRAŠAK", "PRASAK"))]
    assert len(sachet) >= 20


@pytest.mark.parametrize("name", [
    "CCA1-1,5KG PILE GRILL SMRZ",
    "CCA1,6KG CEKIN HRVATSKO PILE",
    "Dimljena svinjska rebra, cca. 700g",
    "SIR TILZIT CCA 4,5 KG VALIO EESTI AS",
    "PILE GRILL 1-1,5 KG",
])
def test_variable_weight(name):
    assert analyze_pack(name) == (None, None, True, None)


@pytest.mark.parametrize("name,expected", [
    ("BANANA SNIŽENJE", True), ("KUPUS CRVENI SNIŽENJE", True), ("PAPRIKA PARADAJZERICA SNIŽENJE", True),
    ("TIKVICA SNIŽENO", True), ("KIVI SNIŽENI", True), ("MRKVA ŽUTA SNIŽENA", True), ("BANANA", False),
])
def test_clearance(name, expected):
    assert is_clearance(name) is expected


@pytest.mark.parametrize("key,amount,attrs,expected", [
    ("kvasac", 35, {}, 5), ("kvasac", 7, {"vrsta": "suhi"}, 1), ("kvasac", 42, {"vrsta": "svjezi"}, 1),
    ("vanilin_secer", 48, {}, 6), ("prasak_za_pecivo", 1000, {}, pytest.approx(83.333, rel=1e-3)),
    ("brasno", 1000, {}, None),
])
def test_sachet_units(key, amount, attrs, expected):
    assert S[key].units_in_pack("", amount, "g", attrs) == expected


def test_new_staple_fields():
    assert S["mlijeko"].plausible_per_unit == (0.5, 4)
    assert S["maslac"].plausible_per_unit == (6, 40) and S["maslinovo_ulje"].plausible_per_unit == (4, 60)
    assert S["kvasac"].compare_unit == "vrecica" and S["brasno"].compare_unit == "kg"
    assert all(S[k].pantry for k in ("papar", "sol", "mljevena_paprika", "ocat", "dodatak_jelima"))
    assert ("laktoza", "bez") in S["mlijeko"].default_exclude_variants
    assert ("tip", "integralno") in S["brasno"].default_exclude_variants


def test_clearance_excluded_by_default(con):
    ids = {r["id"] for r in search.find_products(ingredient="banana", con=con)}
    assert "ntl:001069" not in ids
    with_clearance = {r["id"] for r in search.find_products(ingredient="banana", con=con, include_clearance=True)}
    assert "ntl:001069" in with_clearance


def test_plausible_range_marks_suspect(con):
    # pretraga čita granice iz clean.staple_rules (ručne ili automatske)
    old = con.execute("SELECT ppu_min, ppu_max FROM clean.staple_rules WHERE staple = 'brasno'").fetchone()
    con.execute("UPDATE clean.staple_rules SET ppu_min = 0.4, ppu_max = 0.7 WHERE staple = 'brasno'")
    try:
        res = search.find_products(ingredient="brasno", con=con)
        assert any(r["n_price_suspect"] > 0 for r in res)
        assert all(r["price_per_unit_max"] is None or r["price_per_unit_max"] <= 0.7 for r in res)
    finally:
        con.execute("UPDATE clean.staple_rules SET ppu_min = ?, ppu_max = ? WHERE staple = 'brasno'", old)


def test_manual_and_auto_ranges(con):
    rules = dict(con.execute("SELECT staple, range_source FROM clean.staple_rules").fetchall())
    assert rules["brasno"] == "manual" and rules["mlijeko"] == "manual"
    # fixture: med i banana nemaju ručne granice -> 0.25x-4x medijana
    lo, hi, src = con.execute("SELECT ppu_min, ppu_max, range_source FROM clean.staple_rules WHERE staple = 'banana'").fetchone()
    assert src == "auto" and hi == pytest.approx(16 * lo, rel=1e-3)  # granice su zaokružene na 4 decimale


def test_default_exclude_variants(con, monkeypatch):
    hide_ostro = replace(S["brasno"], default_exclude_variants=(("tip", "ostro"),))
    monkeypatch.setattr(search, "resolve_ingredient", lambda _: hide_ostro)
    assert "3850104223631" not in {r["id"] for r in search.find_products(ingredient="brasno", con=con)}
    asked = search.find_products(ingredient="brasno", attributes={"tip": "ostro"}, con=con)
    assert [r["id"] for r in asked] == ["3850104223631"]


def test_pack_range_drops_products(tmp_path, monkeypatch):
    from mealmeter import staples as staples_mod
    from tests.conftest import FIXTURE
    big_only = dict(S, brasno=replace(S["brasno"], min_pack=2000))
    monkeypatch.setattr(staples_mod, "load_staples", lambda *a, **k: big_only)
    c = duckdb.connect(str(tmp_path / "t.duckdb"))
    load_raw(c, FIXTURE, "2026-10-19")
    build_clean(c)
    rows = c.execute("""SELECT p.pack_amount, ps.drop_reason FROM clean.product_staples ps
                        JOIN clean.products p USING (chain, product_id) WHERE ps.staple = 'brasno'""").fetchall()
    assert rows and all((r[1] == "pakiranje") == (r[0] < 2000) for r in rows if r[0])


# --- 4. atributi --------------------------------------------------------------

@pytest.mark.parametrize("name,vrsta", [
    ("Riso Scotti riža originario okr.zrno 1kg", "originario"),  # originario nije arborio
    ("Riso Scotti riža oro dugog zrna 1kg", "dugo_zrno"),  # oro nije parboiled
    ("Riso Scotti riža arborio dugo zrno 1kg", "arborio"),
    ("Riso Scotti riža carnaroli 500g", "carnaroli"),
    ("RIŽA BASMATI 1 KG (20) SHAZIA", "basmati"),
    ("RIŽA JASMINE PURE THAI 1 KG (12)", "jasmin"),
    ("RIŽA DUGO ZRNO PARBOIL.500g BEN'S", "parboiled"),
    ("BEN'S ORIGINAL RIŽA INTEGR.500g", "integralna"),
    ("RIŽA BIJELA 800 g VREĆICA ZLATO POLJE", None),
])
def test_rice_variety(name, vrsta):
    assert extract_attributes(S["riza"], name).get("vrsta") == vrsta


def test_rice_varieties_exactly():
    assert list(S["riza"].attributes["vrsta"]) == [
        "basmati", "jasmin", "arborio", "carnaroli", "originario", "parboiled", "integralna", "dugo_zrno"]


@pytest.mark.parametrize("name,expected", [
    ("MLIJEKO LAGANO JUTRO 0% 1L DUKAT", {"mast": "0", "laktoza": "bez"}),
    ("DUKAT MLIJEKO LAGANO JUTRO 0%MM 1L", {"mast": "0", "laktoza": "bez"}),
    ("MLIJEKO LAGANO JUTRO0,0% MM", {"mast": "0", "laktoza": "bez"}),
    ("MLIJEKO LAGANO JUTRO 1,5% 1L DUKAT", {"mast": "1.5", "laktoza": "bez"}),  # linija bez laktoze
    ("MLIJEKO TRAJNO 2.8% 1L BOCA DUKAT", {"mast": "2.8"}),
])
def test_milk_fat_zero_and_lactose(name, expected):
    got = extract_attributes(S["mlijeko"], name)
    assert expected.items() <= got.items()
    if "laktoza" not in expected:
        assert "laktoza" not in got


@pytest.mark.parametrize("name,size,count", [
    ("JAJA S RAZRED 10/1 PODNI UZGOJ GALA", "s", 10),
    ("JAJA M 10/1 PODN.UZ. GALA", "m", 10),
    ("JAJA KL. A RAZ. L 10/1 GALA", "l", 10),
    ("JAJA XL RAZRED 10/1 PODNI UZGOJ VRANA", "xl", 10),
    ("N-JAJA PERFA AKLASARAZRED M 10KOM -18/1", "m", 10),  # -18/1 je karton
    ("JAJA SVJEŽA L 10/1 KOKA TOMCRO (18)", "l", 10),
    ("SVJEŽA JAJA RAZL. VEL. BIO 6/1", None, 6),
])
def test_egg_size_and_count(name, size, count):
    st = S["jaja"]
    assert extract_attributes(st, name).get("velicina") == size
    assert st.units_in_pack(name, None, None, {}) == count


def test_eggs_compare_by_class():
    st = S["jaja"]
    assert st.compare_by == "count" and st.compare_unit == "kom" and st.group_by == ("velicina", "uzgoj")
    assert name_match(st, "DESERT QUARK MAXI JAJE S IGRAČ 160g") == "excluded"
    assert name_match(st, "COKO.JAJE ROCHER 212,5 G FERRERO") == "excluded"


@pytest.mark.parametrize("name,namjena", [
    ("KRUMPIR PAK. ZA KUHANJE 2,5 kg", "kuhanje"),
    ("KRUMPIR PAK. ZA PEČENJE 2,5 kg", "pecenje"),
    ("KRUMPIR PAK. ZA SALATU 2,5 kg", "salata"),
    ("KRUMPIR LIČKI 2,5 kg AGROVEL.", None),
])
def test_potato_purpose(name, namjena):
    assert extract_attributes(S["krumpir"], name).get("namjena") == namjena


# --- 5. sadržaj ---------------------------------------------------------------

from mealmeter.staples import LOOSE_REJECT_REGEX, resolve_ingredient  # noqa: E402
from mealmeter.normalize import norm_text  # noqa: E402


def test_disabled_staples():
    for key in ("voda", "kruh", "kava"):
        assert key not in S and resolve_ingredient(key) is None
        assert load_staples(include_disabled=True)[key].disabled


@pytest.mark.parametrize("name,oblik", [
    ("BIO PELAT 400g", "pelati"),
    ("RAJČICA PELATI OGULJENA CIJELA 400G ULTRA", "pelati"),
    ("RAJČICA MUTTI 400G POLPA-12/1- SITNO SJECKANA 41050", "polpa"),
    ("RAJČICA SJEC.SIT.MUTTI 3X400 g", "sjeckana"),
])
def test_canned_tomato(name, oblik):
    assert name_match(S["rajcica_konzerva"], name) == "match"
    assert extract_attributes(S["rajcica_konzerva"], name)["oblik"] == oblik
    assert name_match(S["pasirana_rajcica"], name) != "match"


@pytest.mark.parametrize("key,name,oblik", [
    ("grah", "GRAH SMEĐI 800g LIM.PODRAVKA-ocijeđene mase 460g", "konzerva"),
    ("grah", "GRAH ŠARENI NATURA 500 g", "nepoznato"),  # bez oznake se ne pogađa
    ("grah", "GRAH 1 kg ZLATNO ZRNO", "nepoznato"),
    ("leca", "LEĆA LIM 400 g NETO OC.MASA 240 g (12) PODRAVKA", "konzerva"),
    ("leca", "LEĆA ZELENA 500G NATURA MARJAN VOĆE", "nepoznato"),
    ("slanutak", "SLANUTAK 800 g LIMENKA ( OCJ. MASA 480 g) PODRA", "konzerva"),
    ("grasak", "N-LEDO GRAŠAK 400G -18/1- 065672", "smrznuto"),
    ("grasak", "GRAŠAK U LIMENCI 850G/520G I KVALITETA (6),(PAL 96) PODRAVKA", "konzerva"),
    ("kukuruz", "KUKURUZ ŠEĆERAC 340 g PODRAVKA (10) OC. MASA 280 g", "konzerva"),
    ("gljive", "ŠAMPINJONI 500G BEZ KORIJENA(PODLOŽAK) 1150", "svjeze"),
    ("gljive", "ULTRA ŠAMPINJONI REZANI 400GR./200GR. (12)", "konzerva"),
])
def test_form_attribute(key, name, oblik):
    assert extract_attributes(S[key], name)["oblik"] == oblik


@pytest.mark.parametrize("key,name,expected", [
    ("junetina", "Junetina za gulaš", "match"),
    ("junetina", "JUNEĆI BUT BK", "match"),
    ("junetina", "INSTANT NOODLI GOVEDINA 93 G U CASI YAKISOBA", None),  # nema dijela mesa
    ("junetina", "BUREK JUNETINA DS 190G PEKAR TOMO", None),
    ("svinjetina", "N-SVINJSKI VRAT SK PIK 640G ODREZAK -3/1- MAP", "match"),
    ("svinjetina", "Ajinmoto Gyoza sa svinjetinom 600 g", None),
])
def test_meat_requires_cut(key, name, expected):
    assert name_match(S[key], name) == expected


@pytest.mark.parametrize("name,vrsta", [
    ("MLJEVENO MESO MJEŠANO", "mijesano"),
    ("Mljeveno meso junetina", "junece"),
    ("PURECE MLJEVENO MESO 500 G VINDON (41304)", "purece"),
    ("MLJEVENO MESO ZA KOBASICE", "mijesano"),  # bez oznake vrste -> _default
])
def test_minced_meat_default(name, vrsta):
    assert extract_attributes(S["mljeveno_meso"], name)["vrsta"] == vrsta


def test_minced_meat_default_filter():
    # Korak 2D: redoslijed umjesto jedne vrijednosti
    assert S["mljeveno_meso"].default_preference == {"vrsta": ("mijesano", "junece", "svinjsko")}


def test_default_attributes_applied(con, monkeypatch):
    only_ostro = replace(S["brasno"], default_attributes={"tip": "ostro"})
    monkeypatch.setattr(search, "resolve_ingredient", lambda _: only_ostro)
    assert [r["id"] for r in search.find_products(ingredient="brasno", con=con)] == ["3850104223631"]
    glatko = search.find_products(ingredient="brasno", attributes={"tip": "glatko"}, con=con)
    assert glatko and all(r["attributes"]["tip"] == "glatko" for r in glatko)


@pytest.mark.parametrize("key,name,expected", [
    ("zelena_salata", "SALATA ICEBERG KOMAD", "iceberg"),
    ("zelena_salata", "SALATA PUTERICA KOMAD", "puterica"),
    ("zelena_salata", "SALATA KRISTALKA -KOMAD", "kristalka"),
    ("zelena_salata", "1KG MC SALATA ICEBERG LEDENKA", "iceberg"),
])
def test_lettuce_heads(key, name, expected):
    assert name_match(S[key], name) == "match"
    assert extract_attributes(S[key], name)["vrsta"] == expected


@pytest.mark.parametrize("key,name,expected", [
    ("zelena_salata", "SJEME SALATA KRISTALKA", "excluded"),
    ("zelena_salata", "RIKOLA 100 g", None),
    ("rukola", "RIKOLA 100 g", "match"),
    ("rukola", "Salata rukola", "match"),
    ("matovilac", "MATOVILAC 100 G", "match"),
    ("radic", "SALATA RADIČ 250g", "match"),
    ("radic", "MATOVILAC RADIČ 125 grama", "excluded"),
    ("endivija", "SALATA ENDIVIJA kom", "match"),
])
def test_leafy_split(key, name, expected):
    assert name_match(S[key], name) == expected


@pytest.mark.parametrize("name,rejected", [
    ("KRASTAVCI 6-9 cm 1580g ZORELA ocijeđene mase 820g", True),
    ("KRASTAVCI KISELI 1500G DELIKATES", True),
    ("KRASTAVCI 4 kg MARI UG.", False),
    ("KRASTAVAC MINI 250G.", False),
])
def test_loose_produce_rejects_jars(name, rejected):
    import re
    assert bool(re.search(LOOSE_REJECT_REGEX, norm_text(name))) is rejected


# --- 2B ispravci ----------------------------------------------------------------

from mealmeter.staples import extract_attributes_detail  # noqa: E402


@pytest.mark.parametrize("name,expected", [
    ("MLIJEKO LAGANO JUTRO 1,5% 1L DUKAT", ("bez", "inferred")),
    ("MLIJEKO TRAJNO LAGANO JUTRO 1,5% BEZ LAKTOZE 0,5L DUKAT BOCA", ("bez", "name")),
    ("MLIJEKO BEZ LAKTOZE 1,5% 1L LAGANO JUTRO", ("bez", "name")),
])
def test_lactose_inferred(name, expected):
    assert extract_attributes_detail(S["mlijeko"], name)["laktoza"] == expected


def test_milk_attribute_sources_have_origin(con):
    r = search.find_products(ingredient="mlijeko", attributes={"mast": "2.8"}, con=con)[0]
    assert r["attribute_sources"]["mast"] == {"name": "MLIJEKO TRAJNO 2.8% 1L BOCA DUKAT", "how": "name"}


@pytest.mark.parametrize("name,expected", [
    ("LUK CRVENI RUKAVAC 4/1", "match"),
    ("LUK RUKAVAC LJUBIČASTI 4 KOM", "match"),
    ("LUK ŽUTI RUKAVAC VH 4/1", "match"),
])
def test_onion_net_included(name, expected):
    assert name_match(S["luk"], name) == expected
    assert S["luk"].assumed_pack_g == 500


@pytest.mark.parametrize("name,match,vrsta", [
    ("ULJE SUNCOKRET PVC 1L (15) (PAL 675), ZVIJEZDA", "match", "suncokretovo"),
    ("ULJE KOŠTICA GROŽĐA 1 L FARCHI", "match", "grozde"),  # dopušteno, ali ne zadano
    ("ULJE AVOKADA 500 ML PIETRO CORICCELI", "match", "avokado"),
    ("ULJE PISTACIJE 500 ML BASSO", "match", "specijalno"),
    ("SUN CARE MARM.SOHO ULJE SP.150ML", None, None),  # sun\b (kozmetiku inače izbacuje kategorija)
])
def test_oil_kinds(name, match, vrsta):
    st = S["ulje"]
    assert (name_match(st, name) == "match") == (match == "match")
    if vrsta:
        assert extract_attributes(st, name)["vrsta"] == vrsta


def test_oil_default_selection():
    excluded = {v for a, v in S["ulje"].default_exclude_variants if a == "vrsta"}
    assert excluded == {"avokado", "sezam", "kokos", "grozde", "specijalno", "omegol", "mediteran"}
    assert name_match(S["ulje"], "ULJE ZA KOSU ARGAN 100ML") == "excluded"


@pytest.mark.parametrize("key,name", [
    ("maslac", "TIKVA PUTER"), ("maslac", "SALATA PUTER KOMAD"), ("maslac", "TOAST S MASLACEM 500 G MULINI"),
    ("mlijeko", "LONCIC ZA MLIJEKO 800 ML COLOR"),
])
def test_obvious_wrong_hits_excluded(key, name):
    assert name_match(S[key], name) == "excluded"


def test_lettuce_synonyms():
    assert {"iceberg", "ledenka", "kristalka", "lollo", "puterica"} <= set(S["zelena_salata"].synonyms)
    assert resolve_ingredient("Lollo").key == "zelena_salata"


@pytest.mark.parametrize("name,conf", [
    ("DOLCELA INSTANT SUHI KVASAC 7 g 4+1 GRATIS, PODRAVKA", "low"),
    ("Di-go Kvasac suhi instant 5x35 g 1gratis", "low"),
    ("KFJ TUNA 2x80 g", "high"),
    ("BRAŠNO GLATKO T-550 1kg PODRAVKA", "high"),
    ("VANILIN ŠEĆER BOUR. DOLCELA 10 g 3/1", "low"),
    ("BANANA", None),
])
def test_pack_confidence(name, conf):
    assert analyze_pack(name)[3] == conf


@pytest.mark.parametrize("key,name", [
    # neprehrambeni kandidati pronađeni u lancima bez kategorije (Plodine, Lorenco, Stridon) i NTL-u
    ("ulje", "VALVOLINE ULJE ALL CLIM.EXTRA 10W40 4 L"),
    ("jaja", "JAJE STOLICA RATAN CRNA 120X96X70"),
    ("jaja", "GLAZBENO JAJE SA SLATKISIMA 150 G WINDEL"),
    ("jaja", "OBUCI JAJE TERMOSKUPLJAJUĆA FOLIJA 12/1"),
    ("jaja", "IGR.DINOSAUR JAJE 12/1 74571"),
    ("luk", "VRTNI LUK HY16-01 140X240 CM"),
    ("spinat", "SJEME BLITVA SREBRNOLISNA"),
    ("spinat", "SJEME SPINAT MATADOR"),
    ("griz", "DR.IGR DINO GRIZ"),
    ("limun", "CITRONELA LIMUN I MELISA"),
    ("sol", "NATUR PUR JUNEĆI ODRESCI (ŠOL)"),
    ("ulje", "ULJE EDM 0,5 l ZVIJEZDA"),  # EDM = ekstra djevičansko maslinovo
    ("ocat", "OCAT ACETO BALS.0,5L ZVIJEZDA"),
    ("krumpir", "PEKARSKI KRUMPIR 680 G EASY CHEF"),
    ("kecap", "CHIO TIP TOP CUBICS KETCHUP INTERSNACK 50 g (30)"),
    ("krusne_mrvice", "GASTRO NUGGETSI PILEĆI U PANKO PANADI"),
])
def test_remaining_wrong_hits_excluded(key, name):
    assert name_match(S[key], name) == "excluded"


@pytest.mark.parametrize("name,vrsta", [("LUK MLADI - VEZICA", "mladi"), ("500G LUK ECHALION", "ljutika")])
def test_onion_variants_not_default(name, vrsta):
    assert extract_attributes(S["luk"], name)["vrsta"] == vrsta
    assert ("vrsta", vrsta) in S["luk"].default_exclude_variants
