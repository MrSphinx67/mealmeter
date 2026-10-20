"""Filtar hrane: food_group, is_food i category_source za svaki proizvod (clean.products).

Redoslijed izvora (category_source):
1. `chain`: kategorija lanca preko data/category_map.yaml (kategorije izvan mape: pravila iz
   normalize.category_group). Pića s nazivom alkoholnog pića postaju `alkohol`.
2. `ean_inherited`: proizvod bez korisne kategorije (Lorenco, Plodine, dio Stridona, "Ostalo")
   nasljeđuje većinsku skupinu istog globalnog EAN-a iz lanaca s kategorijom (> 50 % glasova);
   ako se skupine razilaze, ostaje 'unknown'.
3. `words`: popis neprehrambenih riječi (NONFOOD_WORDS) ili naziv alkoholnog pića.
4. `none`: ništa od navedenog; food_group = 'unknown', is_food = NULL.

is_food: true za hrana/pice/alkohol, false za neprehrambene skupine, NULL za 'unknown'.
"""

import re
from functools import lru_cache
from pathlib import Path

import duckdb
import yaml

from mealmeter.normalize import FOOD_GROUP_VALUES, FOOD_GROUPS, NONFOOD_GROUPS, category_group, norm_text
from mealmeter.staples import attr_text

CATEGORY_MAP_PATH = Path(__file__).resolve().parents[2] / "data" / "category_map.yaml"

# Neprehrambene riječi za proizvode bez kategorije (na početku riječi u name_norm) -> skupina.
# "pse" samo kao cijela riječ (prefiks bi pogodio "PŠENIČNO"), a ne iza "bras" ("BRAŠ.PŠE." je
# pšenično brašno, odluka 23); "sjeme" samo kao cijela riječ ("KRUH SA SJEMENKAMA" je hrana).
NONFOOD_WORDS = [
    (r"za pse|psec|(?<!bras )pse\b|macke", "kucni_ljubimci"),
    (r"kosu\b|sun\b|spf|sampon|dezodor", "kozmetika"),
    (r"perilic|deterdzent", "kucanstvo"),
    (r"pelene", "djeca"),
    (r"zubn", "higijena"),
    (r"motorn|igrac|sjeme\b|dekor|stolic", "ostalo"),
    # proširenje popisa: pribor za piće, inače bi ga alkoholna riječ označila kao piće; čaše vidi _CUPS
    (r"garn\b|depozit|otvarac|vadicep|clip\b", "kucanstvo"),
]
_NONFOOD_RX = [(re.compile(r"(^| )(?:" + p + ")"), g) for p, g in NONFOOD_WORDS]
# Hrana za ljubimce u lančevoj kategoriji "Hrana" ("HRANA ZA PSE FRISK.VITAL."): naziv ima prednost
_PET_RX = re.compile(r"(^| )(?:hrana za (?:pse|macke|ptice|ribice|glodavce)|za pse\b|za macke|poslastic\w* za (?:pse|macke)|"
                     r"whiskas|friskies|pedigree|kitekat|purina|gourmet gold|dreamies|brit care)")
# "ČAŠA" je i pakiranje hrane ("JOGURT 500 G ČAŠA", "SLADOLED ČAŠA"), pa je neprehrana samo množina
# "ČAŠE" ili dodatak uz piće ("WHISKY 0,7 L + ČAŠA"); provjera na attr_text (zadržava "+")
_CUPS = re.compile(r"(^|[\s(/.,])case\b|\+\s*cas|(^|[\s(/.,])casa za\b")  # i "ČAŠA ZA PIVO" (moja dopuna)
_CUP_FOOD = re.compile(r"(^| )(?:jog|vrhnj|puding|desert|kefir|sir\b|namaz|mlijek|napitak|sok\b|sladoled)")

# Alkoholna pića po nazivu (name_norm, na početku riječi). Opće riječi vrijede za skupinu `pice`
# (lanci miješaju sokove i vino u "PIĆE") i za proizvode bez kategorije; marke piva i žestica te
# postotak alkohola samo za `pice` ("LAMP.MAJA TOMISLAV" je majica, "ČOKOLADA 70%" nije piće).
ALCOHOL_WORDS = (
    r"vino|vina\b|vinu\b|vinjak|pivo|piva\b|lager\b|pils\b|radler|stout\b|cider|jabukovac|pjenus|sampanj|"
    r"champagne|prosecco|prosek|lambrusco|chianti|rioja|grasevin|malvazij|merlot|cabernet|chardonnay|"
    r"sauvignon|riesling|rizling|syrah|shiraz|zinfandel|pinot|plavac|dingac|postup\b|vranac|teran\b|"
    r"frankovk|zweigelt|portugizac|traminac|zlahtin|posip\b|vugava|marastina|kujundzus|crljenak|"
    r"muskat\b|moscato|bermet|vermut|aperol|campari|jagermeister|amaro\b|ouzo|sambuca|grappa|absint|"
    r"baileys|limoncello|kruskovac|visnjevac|teranino|pelinkovac|travaric|sljivovic|lozovac|loza\b|"
    r"komovic|viljamovk|rakij|vodk|votk|whisky|whiskey|viski|bourbon|scotch|gin\b|rum\b|liker|tequil|"
    r"mezcal|brandy|brandi\b|konjak|cognac|medica\b|biska\b|orahovac|alkohol"
)
ALCOHOL_BRANDS = (
    r"ozujsko|karlovacko|tomislav|heineken|staropramen|lasko|becks|stella artois|tuborg|carlsberg|corona|"
    r"guinness|budweiser|paulaner|erdinger|krusovice|kozel|zlatorog|grimbergen|leffe|hoegaarden|desperados|"
    r"somersby|jameson|johnnie walker|jack daniel|ballantine|chivas|tullamore|jim beam|martini|"
    r"grey goose|smirnoff|absolut|beefeater|tanqueray|bacardi|havana club|captain morgan|stock\b|koktel"
)
# Nije alkoholno piće iako naziv sadrži alkoholnu riječ (na izvornom nazivu, malim slovima)
NOT_ALCOHOL_REGEX = (r"bezalkohol|bez alkohola|alkoholfrei|alcohol free|\b0[.,]0 ?%|(?<!\d)(?<!\d[.,])0 ?%|\bocat|\baroma|"
                     r"kuglic|\bumak|\bsok od")
# Postotak alkohola u nazivu pića ("40% 0,7L", "4,5% 0,33l"); sokovi, nektari i mliječna mast ne
ABV_REGEX = r"(?<![\d.,])(\d{1,2}(?:[.,]\d{1,2})?) ?% ?(?!m\.?m|mm|voc)"
_NOT_ABV_CONTEXT = re.compile(r"(^| )(?:nektar|nek\b|sok|juice|juicy|voc|cappy|pago|toco|jabuk|naranc|multivit|smoothie|"
                              r"sirup|mlijek|kefir|jogurt|milk|napit|cedevita|limunad|ledeni)")
_ALCOHOL_RX = re.compile(r"(^| )(?:" + ALCOHOL_WORDS + ")")
_ALCOHOL_BRAND_RX = re.compile(r"(^| )(?:" + ALCOHOL_BRANDS + ")")
_NOT_ALCOHOL_RX = re.compile(NOT_ALCOHOL_REGEX)
_ABV_RX = re.compile(ABV_REGEX)


@lru_cache(maxsize=2)
def load_category_map(path: Path = CATEGORY_MAP_PATH) -> dict[str, str]:
    """{norm_text(kategorija): food_group}; prazno ako mapa ne postoji (tada vrijede pravila)."""
    if not Path(path).exists():
        return {}
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    raw.pop("_chain_verify", None)
    bad = {k: v for k, v in raw.items() if v not in FOOD_GROUP_VALUES}
    if bad:
        raise ValueError(f"{path}: nepoznate skupine {bad}; dopuštene: {FOOD_GROUP_VALUES}")
    return {norm_text(str(k)): v for k, v in raw.items()}


@lru_cache(maxsize=2)
def load_chain_verify(path: Path = CATEGORY_MAP_PATH) -> dict[str, set[str]]:
    """{lanac: {norm_text(kategorija) | "ean_inherited"}}: kategorije čija se hrana provjerava širim popisom
    neprehrambenih riječi (category_map.yaml, _chain_verify)."""
    if not Path(path).exists():
        return {}
    raw = (yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}).get("_chain_verify") or {}
    return {chain: {norm_text(c) if c != "ean_inherited" else c for c in cats} for chain, cats in raw.items()}


def is_alcohol(name: str | None, drink: bool = False) -> bool:
    """Naziv alkoholnog pića. `drink=True` (proizvod iz kategorije pića): i marke i postotak
    alkohola od 3,5 do 80 %; inače samo opće riječi (vino, pivo, rakija...)."""
    if not name:
        return False
    raw, text = name.lower(), norm_text(name) or ""
    if _NOT_ALCOHOL_RX.search(raw):
        return False
    if _ALCOHOL_RX.search(text):
        return True
    if not drink:
        return False
    if _ALCOHOL_BRAND_RX.search(text):
        return True
    if _NOT_ABV_CONTEXT.search(text):
        return False
    return any(3.5 <= float(m.group(1).replace(",", ".")) <= 80 for m in _ABV_RX.finditer(raw))


def chain_group(category: str | None, name: str | None, cmap: dict[str, str] | None = None) -> str:
    """Skupina iz kategorije lanca (mapa, pa pravila); pića s alkoholnim nazivom su `alkohol`,
    bezalkoholna u alkoholnoj kategoriji ("PJENUŠAC 0,0%") su `pice`, a hrana za ljubimce u
    kategoriji hrane je `kucni_ljubimci`."""
    cmap = load_category_map() if cmap is None else cmap
    group = cmap.get(norm_text(category)) if category else None
    group = group or category_group(category)
    if group in FOOD_GROUPS and _PET_RX.search(norm_text(name) or ""):
        return "kucni_ljubimci"
    if group == "pice" and is_alcohol(name, drink=True):
        return "alkohol"
    if group == "alkohol" and name and _NOT_ALCOHOL_RX.search(name.lower()):
        return "pice"
    return group


def words_group(name: str | None) -> str | None:
    """Skupina iz naziva za proizvode bez kategorije: neprehrambena riječ ili alkoholno piće."""
    text = norm_text(name) or ""
    for rx, group in _NONFOOD_RX:
        if rx.search(text):
            return group
    if _CUPS.search(attr_text(name)) and not _CUP_FOOD.search(text):
        return "kucanstvo"
    return "alkohol" if is_alcohol(name) else None


def build_food(con: duckdb.DuckDBPyConnection) -> dict:
    """Dodaje clean.products.food_group, is_food i category_source. Vraća statistiku za ispis."""
    from mealmeter.build import _temp_table  # izbjegava kružni import

    cmap, verify = load_category_map(), load_chain_verify()
    unmapped: dict[str, int] = {}

    def rows():
        for chain, pid, category, name in con.execute(
                "SELECT chain, product_id, category, name FROM clean.products").fetchall():
            if category and norm_text(category) not in cmap:
                unmapped[category] = unmapped.get(category, 0) + 1
            group, refined = chain_group(category, name, cmap), None
            if group in FOOD_GROUPS:
                # neprehrana u kategoriji hrane: strogi popis svuda, širi za nepouzdane kategorije lanaca
                refined = nonfood_in_food(name, broad=norm_text(category or "") in verify.get(chain, ()))
            yield chain, pid, refined or group, words_group(name) if group == "unknown" else None, bool(refined)

    _temp_table(con, "food_tmp", {
        "chain": "VARCHAR", "product_id": "VARCHAR", "chain_group": "VARCHAR", "words_group": "VARCHAR",
        "refined": "BOOLEAN",
    }, rows())
    food = ", ".join(f"'{g}'" for g in FOOD_GROUPS)
    nonfood = ", ".join(f"'{g}'" for g in NONFOOD_GROUPS)
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE food_final AS
        WITH votes AS (  -- skupine istog globalnog EAN-a u lancima s korisnom kategorijom
          SELECT p.ean_norm, f.chain_group AS grp, count(*) AS n
          FROM clean.products p JOIN food_tmp f USING (chain, product_id)
          WHERE p.ean_global AND f.chain_group <> 'unknown' GROUP BY ALL
        ),
        inherit AS (
          SELECT ean_norm, arg_max(grp, n) AS grp, max(n) / sum(n) AS share FROM votes GROUP BY ean_norm
        )
        SELECT p.chain, p.product_id,
               CASE WHEN f.chain_group <> 'unknown' THEN f.chain_group
                    WHEN i.share > 0.5 THEN i.grp
                    WHEN f.words_group IS NOT NULL THEN f.words_group
                    ELSE 'unknown' END AS food_group,
               CASE WHEN f.refined THEN 'words' WHEN f.chain_group <> 'unknown' THEN 'chain'
                    WHEN i.share > 0.5 THEN 'ean_inherited'
                    WHEN f.words_group IS NOT NULL THEN 'words'
                    ELSE 'none' END AS category_source,
               i.share IS NOT NULL AND i.share <= 0.5 AS ean_conflict
        FROM clean.products p JOIN food_tmp f USING (chain, product_id)
        -- inherit sadrži samo globalne EAN-ove (globalnost ovisi samo o kodu)
        LEFT JOIN inherit i ON i.ean_norm = p.ean_norm
    """)
    # hrana naslijeđena preko EAN-a u lancima iz _chain_verify (Plodine): širi popis neprehrambenih riječi
    inherited_chains = [c for c, cats in verify.items() if "ean_inherited" in cats]
    if inherited_chains:
        names = con.execute(f"""
            SELECT f.chain, f.product_id, p.name FROM food_final f JOIN clean.products p USING (chain, product_id)
            WHERE f.category_source = 'ean_inherited' AND f.food_group IN ({food})
              AND f.chain IN ({", ".join("?" for _ in inherited_chains)})""", inherited_chains).fetchall()
        fixes = [(c, pid, g) for c, pid, name in names if (g := nonfood_in_food(name, broad=True))]
        if fixes:
            _temp_table(con, "food_fix", {"chain": "VARCHAR", "product_id": "VARCHAR", "grp": "VARCHAR"}, fixes)
            con.execute("""UPDATE food_final f SET food_group = x.grp, category_source = 'words' FROM food_fix x
                           WHERE f.chain = x.chain AND f.product_id = x.product_id""")
    con.execute(f"""
        CREATE OR REPLACE TABLE clean.products AS
        SELECT p.*, f.food_group,
               CASE WHEN f.food_group IN ({food}) THEN true WHEN f.food_group IN ({nonfood}) THEN false END AS is_food,
               f.category_source
        FROM clean.products p JOIN food_final f USING (chain, product_id)
    """)
    return {
        "unmapped_categories": sorted(unmapped.items(), key=lambda kv: -kv[1]),
        "by_chain": con.execute("""
            SELECT p.chain, count(*) AS n,
                   count(*) FILTER (WHERE f.category_source <> 'chain') AS n_no_category,
                   count(*) FILTER (WHERE f.category_source = 'ean_inherited') AS n_inherited,
                   count(*) FILTER (WHERE f.category_source = 'words') AS n_words,
                   count(*) FILTER (WHERE f.food_group = 'unknown') AS n_unknown,
                   count(*) FILTER (WHERE f.ean_conflict AND f.category_source <> 'chain') AS n_conflict
            FROM clean.products p JOIN food_final f USING (chain, product_id)
            GROUP BY p.chain ORDER BY n_no_category DESC, p.chain
        """).fetchall(),
        "by_group": con.execute("""
            SELECT food_group, is_food, category_source, count(*) FROM clean.products
            GROUP BY ALL ORDER BY food_group, category_source
        """).fetchall(),
    }


# Neprehrana unutar "hrane" (na početku riječi u name_norm) -> skupina. STRICT vrijedi za sve proizvode s
# is_food = true; BROAD samo za kategorije lanaca s poznatim neprehrambenim artiklima (category_map.yaml,
# _chain_verify: Gavranović "Hrana", Boso "ZELENI PROGRAM", Studenac "HRANA", Plodine preko EAN-a).
STRICT_NONFOOD_IN_FOOD = [
    (r"igrac|sjeme\b|cvijet", "ostalo"),
    (r"svijec|baterij|salvet|ukrasn", "kucanstvo"),
]
BROAD_NONFOOD_IN_FOOD = STRICT_NONFOOD_IN_FOOD + [
    (r"sampon|regenerator|gel za tus|tus gel|krema za (?:lice|ruke|tijelo|suncanje)|losion|dezodor", "kozmetika"),
    (r"toaletni papir|maramic|pelen|ulosc|tampon|cetkic|zubna pasta|britv|sapun", "higijena"),
    (r"hrana za (?:pse|macke)|za pse|za macke|psec|macj|pijesak za|granule za", "kucni_ljubimci"),
    (r"igrack|cigaret|duhan|olovk|biljeznic|baloni|cestitk|naljepnic|cvijec|orhid|lonc", "ostalo"),
    (r"deterdz|omeksiv|sredstvo za|spuzv|krpa|krpe|vrecice za smece|vrece za|aluminijsk|papirnat|ubrus|"
     r"zarulj|upaljac|kalup za|posud|tanjur|lonac|tava|noz\b|vilic|kuhac|ukras|stolnjak|tegla za|"
     r"vrecica ukrasn|kosaric", "kucanstvo"),
]
# Jestivo usprkos riječi s popisa ("CVJETIĆI UKRASNI" od šećera, "DEKOR ŠARENO PISMO DR.OETKER",
# "BOMBONI + IGRAČKA", "KOŠARICE CVIJET" od čokolade, "KULENOV CVIJET NARESCI", "FLIPS S IGRAČKOM")
_EDIBLE_GUARD = re.compile(r"(^| )(?:jestiv|secern|cokol|marcipan|fondan|bombon|lizalic|zvak|keks|sladoled|"
                           r"kruh|jogurt|dr oet|oetker|tort|kolac|posip\b|confileta|sir\b|narez|naresc|kulen|"
                           r"igrackom|milka|flips|krafn|cips|smoki|salam|cvijet soli|soli\b)")
_STRICT_RX = [(re.compile(r"(^| )(?:" + p + ")"), g) for p, g in STRICT_NONFOOD_IN_FOOD]
_BROAD_RX = [(re.compile(r"(^| )(?:" + p + ")"), g) for p, g in BROAD_NONFOOD_IN_FOOD]


def nonfood_in_food(name: str | None, broad: bool = False) -> str | None:
    """Neprehrambena skupina za proizvod iz kategorije hrane čiji naziv to otkriva, ili None."""
    text = norm_text(name) or ""
    if _EDIBLE_GUARD.search(text):
        return None
    for rx, group in (_BROAD_RX if broad else _STRICT_RX):
        if rx.search(text):
            return group
    if broad and _CUPS.search(attr_text(name or "")) and not _CUP_FOOD.search(text):
        return "kucanstvo"
    return None


# Za provjeru: riječi koje u "hrani" upućuju na neprehrambeni proizvod (izvještaj, ne filtar). "ČAŠA" i
# "KALUP" samo kao "ČAŠE"/"KALUP ZA" ("SLADOLED ČAŠA", "KRUH KALUP" su hrana)
SUSPECT_NONFOOD_REGEX = (
    r"(^| )(?:sampon|regenerator|gel za tus|tus gel|krema za (?:lice|ruke|tijelo|suncanje)|losion|dezodor|"
    r"deterdz|omeksiv|sredstvo za|spuzv|krpa|krpe|vrecice za smece|vrece za|aluminijsk|papirnat|"
    r"salvet|ubrus|toaletni papir|maramic|pelen|ulosc|tampon|cetkic|zubna pasta|britv|sapun|svijec|"
    r"baterij|zarulj|upaljac|igrack|igrac|kalup za|posud|tanjur|case\b|lonac|tava|noz\b|vilic|"
    r"kuhac|ukrasn|naljepnic|stolnjak|hrana za (?:pse|macke)|za pse|za macke|psec|"
    r"macj|pijesak za|granule za|cigaret|duhan|olovk|biljeznic|baloni|cestitk|cvijet|sjeme\b|tegla za)"
)


def food_report(con: duckdb.DuckDBPyConnection, n_sample: int = 20, seed: float = 0.42) -> dict:
    """Izvještaj filtra: broj proizvoda izvan zadanog izbora po skupini i nasumični uzorak
    "hrane" (is_food = true) čiji naziv izgleda neprehrambeno (SUSPECT_NONFOOD_REGEX)."""
    excluded = con.execute("""
        SELECT food_group, count(*) AS n, count(*) FILTER (WHERE category_source = 'chain') AS n_chain,
               count(*) FILTER (WHERE category_source = 'ean_inherited') AS n_ean,
               count(*) FILTER (WHERE category_source = 'words') AS n_words
        FROM clean.products WHERE is_food IS DISTINCT FROM true OR food_group = 'alkohol'
        GROUP BY food_group ORDER BY n DESC
    """).fetchall()
    con.execute(f"SELECT setseed({seed})")
    suspects = con.execute("""
        SELECT chain, name, category, food_group, category_source FROM clean.products
        WHERE is_food AND regexp_matches(name_norm, ?)
        ORDER BY random() LIMIT ?
    """, [SUSPECT_NONFOOD_REGEX, n_sample]).fetchall()
    n_suspect = con.execute("SELECT count(*) FROM clean.products WHERE is_food AND regexp_matches(name_norm, ?)",
                            [SUSPECT_NONFOOD_REGEX]).fetchone()[0]
    return {"excluded": excluded, "suspects": suspects, "n_suspect": n_suspect}
