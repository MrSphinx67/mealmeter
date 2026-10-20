"""Izvještaj za pregled Koraka 2D: docs/STEP2D_REVIEW.md.

Upotreba: python scripts/step2d_review.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import md_table  # noqa: E402

from mealmeter.search import _candidates  # noqa: E402
from mealmeter.staples import BKEY_SQL, load_staples, staple_suspect_sql  # noqa: E402

OUT = Path("docs/STEP2D_REVIEW.md")


def old_membership_sql() -> str:
    """Pravilo prije Koraka 2D: grupa pripada ako barem jedan njezin (neizbačeni) proizvod prolazi pravila,
    a nijedan nije isključen."""
    return f"""
        SELECT ps.staple, {BKEY_SQL} AS bkey,
               bool_or(NOT ps.excluded) AND NOT bool_or(ps.excluded) AS old_member
        FROM clean.product_staples ps JOIN clean.products p USING (chain, product_id)
        WHERE ps.drop_reason IS NULL GROUP BY ALL"""


def section_groups(con) -> str:
    cmp = f"""
        SELECT g.staple, g.bkey, g.status, g.n_chains, g.share_match, g.share_excluded,
               coalesce(o.old_member, false) AS old_member
        FROM clean.staple_groups g LEFT JOIN ({old_membership_sql()}) o USING (staple, bkey)
        WHERE g.n_usable > 0 OR o.old_member
    """  # grupe samo od izbačenih proizvoda (pakiranje) ne mijenjaju izbor
    per = con.execute(f"""
        SELECT staple, count(*) FILTER (WHERE old_member), count(*) FILTER (WHERE status = 'member'),
               count(*) FILTER (WHERE status = 'ambiguous'),
               count(*) FILTER (WHERE old_member AND status <> 'member'),
               count(*) FILTER (WHERE NOT old_member AND status = 'member')
        FROM ({cmp}) GROUP BY staple
        HAVING count(*) FILTER (WHERE old_member AND status <> 'member') > 0
            OR count(*) FILTER (WHERE NOT old_member AND status = 'member') > 0
        ORDER BY 5 DESC, 6 DESC""").fetchall()
    con.execute("SELECT setseed(0.21)")
    examples = con.execute(f"""
        SELECT c.staple, c.bkey, CASE WHEN c.old_member THEN 'član → ' || c.status ELSE 'izvan → član' END,
               c.n_chains, round(100 * c.share_match), round(100 * c.share_excluded),
               (SELECT string_agg(DISTINCT p.chain || ': ' || p.name, '; ') FROM clean.products p
                 WHERE {BKEY_SQL} = c.bkey)
        FROM ({cmp}) c WHERE c.old_member <> (c.status = 'member') AND c.n_chains > 1
        ORDER BY random() LIMIT 30""").fetchall()
    return "\n".join([
        "## 1. Pripadnost grupe (EAN) namirnici", "",
        "Grupa pripada namirnici (`clean.staple_groups.status = 'member'`) ako naziv prolazi pravila u više od "
        "50 % lanaca grupe i nijedan isključeni naziv nema udio ≥ 25 % lanaca; inače je `ambiguous` i nije u "
        "zadanom izboru (`find_products(include_ambiguous=True)` je vraća); `excluded` ako nijedan naziv ne prolazi. Prije: dovoljan je bio jedan naziv, "
        "a bilo koji isključeni naziv rušio je cijelu grupu. Atributi grupe (`clean.staple_group_attrs`): "
        "vrijednost iz naziva ima prednost pred zadanom, zatim broj lanaca. Neprehrambeni član (kategorija) "
        "ne računa se kao pogodak naziva.", "",
        "**Cijena pravila:** grupe u kojima većina lanaca proizvod zove skraćeno ili samo markom ispadaju "
        "(„PRAŠ. PEC. 12 g Dr.Oetker“, „FUŽI 250g AURELIA“, „PASTA ZARA 573 SPIRALI“, „SIR ORODUR“), jer "
        "`must_match` ne pogađa takve nazive. Najviše gubi tjestenina (nazivi oblika bez riječi tjestenina). "
        "Rješenje bi bili sinonimi oblika u `must_match` (fuži, spirali, penne…) ili niži prag za grupe bez "
        "isključenih naziva; nisam ih uvodio jer pravilo traži većinu.", "",
        "Namirnice s promjenama (broj grupa):", "",
        md_table(["namirnica", "članova prije", "članova sada", "dvosmislenih", "ispalo", "ušlo"], per), "",
        "30 nasumičnih promijenjenih grupa (s više od jednog lanca):", "",
        md_table(["namirnica", "grupa", "promjena", "lanaca", "% naziva namirnice", "% isključenog naziva",
                  "nazivi"], examples),
    ])


def section_chicken(con) -> str:
    rows = con.execute(f"""
        SELECT a.value, count(DISTINCT p.chain || p.product_id), any_value(ps.ppu_min), any_value(ps.ppu_max),
               count(*) FILTER (WHERE {staple_suspect_sql('c.price_per_unit', 'ps.n_units', 'ps')}), count(*),
               median(c.price_per_unit)
        FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
        JOIN clean.products p USING (chain, product_id) JOIN clean.prices c USING (chain, product_id)
        JOIN clean.product_attrs a ON a.chain = ps.chain AND a.product_id = ps.product_id
             AND a.staple = ps.staple AND a.attr = 'stanje'
        WHERE ps.staple = 'pileca_prsa' AND NOT ps.excluded AND ps.drop_reason IS NULL AND c.per_unit = 'kg'
        GROUP BY a.value ORDER BY a.value""").fetchall()
    return "\n".join([
        "## 4. Pileća prsa: stanje", "",
        "Atribut `stanje`: smrznuto ako naziv sadrži SMRZ, LEDO, FROZ, ZAMRZ ili BRAZIL, inače svježe; zadano "
        "svježe. Granice po stanju (`plausible_by`): svježe 3–20 €/kg, smrznuto 2–12 €/kg. „Jeli“ ostaje "
        "isključeno. Prije (jedna granica 5–20 €/kg) je odbačeno 528 od 10.613 cijena po kg.", "",
        md_table(["stanje", "proizvoda", "min €/kg", "max €/kg", "izvan granica", "cijena", "medijan €/kg"], rows),
    ])


# proizvodi kojima je Korak 2D.10 promijenio skupinu (chain, product_id, before, after), iz snimke prije promjene
FOOD_CHANGES = Path("docs/data/food_changes_2d10.csv")


def section_food(con) -> str:
    from mealmeter.food import SUSPECT_NONFOOD_REGEX

    changes = f"read_csv('{FOOD_CHANGES}', header=true, all_varchar=true, quote='\"')"
    moved = con.execute(f"SELECT before || ' → ' || after, count(*) FROM {changes} GROUP BY 1 ORDER BY 2 DESC").fetchall()
    con.execute("SELECT setseed(0.3)")
    sample = con.execute(f"""
        SELECT p.chain, p.name, p.category, o.before, p.food_group, p.category_source FROM clean.products p
        JOIN {changes} o USING (chain, product_id)
        WHERE o.before IN ('hrana', 'pice') AND p.is_food IS DISTINCT FROM true ORDER BY random() LIMIT 20""").fetchall()
    con.execute("SELECT setseed(0.42)")
    suspects = con.execute("""SELECT chain, name, category, food_group, category_source FROM clean.products
                              WHERE is_food AND regexp_matches(name_norm, ?) ORDER BY random() LIMIT 20""",
                           [SUSPECT_NONFOOD_REGEX]).fetchall()
    n_susp = con.execute("SELECT count(*) FROM clean.products WHERE is_food AND regexp_matches(name_norm, ?)",
                         [SUSPECT_NONFOOD_REGEX]).fetchone()[0]
    return "\n".join([
        "## 10. Filtar hrane: neprehrana u kategoriji hrane", "",
        "- Strogi popis (igrač, svijeć, baterij, sjeme, cvijet, salvet, ukrasn) vrijedi za sve proizvode s "
        "`is_food = true`; pogođeni idu u `ostalo` ili `kucanstvo` (`category_source = 'words'`).",
        "- Širi popis (posuđe, krpe, kozmetika, higijena, cvijeće…) vrijedi za ručne iznimke u "
        "`category_map.yaml` (`_chain_verify`): Gavranović „Hrana“, Boso „ZELENI PROGRAM“, Studenac „HRANA“ i "
        "Plodine naslijeđene preko EAN-a.",
        "- Jestivo usprkos riječi ostaje hrana (šećerni ukrasi, čokolada, Dr. Oetker, bomboni s igračkom).",
        "- „ČAŠA“ je neprehrana samo kao „ČAŠE“, „+ ČAŠ…“ ili „ČAŠA ZA“ (moja dopuna), pa „SLADOLED ČAŠA“ "
        "ostaje hrana; „KALUP“ samo kao „KALUP ZA“.", "",
        "Promjene skupine (prije → poslije):", "",
        md_table(["promjena", "proizvoda"], moved), "",
        "20 nasumičnih proizvoda koji su bili hrana ili piće, a sada nisu:", "",
        md_table(["lanac", "naziv", "kategorija", "prije", "poslije", "izvor"], sample), "",
        f"20 nasumičnih „hrana“ proizvoda koji i dalje izgledaju neprehrambeno (od {n_susp}; u Koraku 2C "
        "ih je bilo 2.168, ali s drugim popisom za izvještaj):", "",
        md_table(["lanac", "naziv", "kategorija", "skupina", "izvor"], suspects),
    ])


COVERAGE_CHAINS = ("plodine", "konzum", "spar", "lidl", "kaufland", "tommy", "studenac", "eurospin")


def coverage(con) -> list[dict]:
    """Po namirnici: lanci s barem jednim proizvodom u zadanom izboru (kao find_products: zadani atributi,
    bez rasprodaje, bez price_suspect), i procjena dobitka od strogo pozitivnog food_unverified (naziv
    počinje riječju namirnice, cijena u granicama, poznata gramatura). Procjena se NE primjenjuje."""
    out = []
    for st in load_staples().values():
        strict = f"""(coalesce(p.is_food, false) OR (p.is_food IS NULL AND psu.staple IS NOT NULL AND NOT psu.excluded
                      AND regexp_matches(p.name_norm, '^(?:{"|".join(st.must_match)})')))
                     AND p.food_group <> 'alkohol'"""
        counts = {}
        for label, food_sql in (("default", None), ("strict", strict)):
            sql, params, _ = _candidates(st, [], st.defaults() or None, None, False, food_sql)
            rows = con.execute(sql + """ SELECT chain, count(DISTINCT product_id) FROM x
                                        WHERE NOT price_suspect
                                          AND (? = 'default' OR is_food IS NOT NULL OR price_per_unit IS NOT NULL)
                                        GROUP BY chain""", params + [label]).fetchall()
            counts[label] = dict(rows)
        out.append({"staple": st.key, **counts})
    return out


def section_coverage(con) -> str:
    cov = coverage(con)
    rows = []
    for c in cov:
        d, s = c["default"], c["strict"]
        gained = sorted(set(s) - set(d))
        rows.append((c["staple"], len(d), *[d.get(ch, 0) for ch in COVERAGE_CHAINS],
                     s.get("plodine", 0) - d.get("plodine", 0), len(s), ", ".join(gained)))
    zero = [c["staple"] for c in cov if not c["default"].get("plodine")]
    return "\n".join([
        "## 11. Pokrivenost (zadani izbor, cijela Hrvatska)", "",
        f"{len(cov)} aktivnih namirnica. Stupci lanaca: broj proizvoda u zadanom izboru (bez rasprodaje i "
        "`price_suspect`, sa zadanim atributima). Veleprodaja (Metro) nije uključena.", "",
        "**Procjena, nije primijenjeno:** strogo pozitivni `food_unverified` (proizvod nepoznate skupine ulazi ako "
        "naziv počinje riječju namirnice, cijena je u granicama i gramatura je poznata). Stupac „+Plodine“ je "
        "dobitak proizvoda za Plodine, „lanaca (strogo)“ broj lanaca s tim pravilom, a zadnji stupac novi lanci.", "",
        md_table(["namirnica", "lanaca", *COVERAGE_CHAINS, "+Plodine", "lanaca (strogo)", "novi lanci"], rows), "",
        f"Namirnice bez ijednog proizvoda u Plodinama (zadano): {len(zero)} od {len(cov)}"
        + (f" ({', '.join(zero)})." if zero else ".") + " Svježe voće i povrće Plodina (bez kategorije i "
        "EAN-a) `plan_basket` ipak koristi (`food_unverified`, pravilo prve ili druge riječi); u ovoj tablici "
        "i u `find_products` nije.",
    ])


SECTIONS = [section_groups, section_chicken, section_food, section_coverage]


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    parts = [f"# Pregled Koraka 2D (arhiva {date.isoformat()})", "",
             "Izvještaj generira `scripts/step2d_review.py` nad izgrađenom bazom.", ""]
    parts += [f(con) + "\n" for f in SECTIONS]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT}: {len(SECTIONS)} odjeljaka")


if __name__ == "__main__":
    main()
