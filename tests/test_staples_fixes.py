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
    assert name_match(S[key], name) == "excluded"


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
    ("HRANA", "hrana"), ("PAKIRANA HRANA I PIĆE", "hrana"), ("PIĆE", "pice"),
    ("KOZMETIKA", "kozmetika"), ("dekorativna kozmetika", "kozmetika"), ("tijelo", "kozmetika"),
    ("TOALETNE POTREPŠTINE", "higijena"), ("ZUBNA PASTA", "higijena"),
    ("PROIZVODI ZA KUĆANSTVO", "kucanstvo"), ("SREDSTVA ZA ČIŠĆENJE", "kucanstvo"), ("NEPREHRANA", "kucanstvo"),
    ("bebe & djeca", "djeca"), ("DJEČJA HRANA", "djeca"), ("KOZMETIKA ZA DJECU", "djeca"),
    ("KOZMETIKA ZA SUNČANJE", "sunce"), ("SUNCOKRETOVO ULJE", "hrana"),
    ("IGRAČKE", "igracke"), ("kućni ljubimci", "ljubimci"), ("Ostalo", "ostalo"), (None, None),
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
    assert name_match(S[key], name) == "excluded"


@pytest.mark.parametrize("key,name", [
    # "sun" iz zadatka je dodan kao sun\b + suncan, da suncokretovo ulje ostane
    ("ulje", "ULJE SUNCOKRET PVC 1L (15) (PAL 675), ZVIJEZDA"),
    ("ulje", "N-ULJE SUNCOKRET 1L TENA-10/1 (pal.750kom)"),
    ("jogurt", "N-*DUKAT JOGURT 1000G TEKUĆI-6/1- 2.8%MM 32363"),
    ("kukuruz", "KUKURUZ ŠEĆERAC 340 g PODRAVKA (10) OC. MASA 280 g"),
])
def test_point2_keeps_real_products(key, name):
    assert name_match(S[key], name) == "match"
