"""Izvještaj za pregled Koraka 2E: docs/STEP2E_REVIEW.md (detalji; sažetak je docs/REVIEW_2E.md).

Upotreba: python scripts/step2e_review.py [db_path] [odjeljak ...]   (zadano: data/mealmeter.duckdb, svi)
"""

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from morning_review import md_table  # noqa: E402

from mealmeter.staples import BKEY_SQL  # noqa: E402

OUT = Path("docs/STEP2E_REVIEW.md")
DATA = Path("docs/data")
# grupe kojima je Korak 2E.1 promijenio status (staple, bkey, before, after), iz snimke prije promjene
GROUP_CHANGES = DATA / "groups_changes_2e1.csv"


def _names(bkey_col: str = "g.bkey") -> str:
    return f"""(SELECT string_agg(DISTINCT p.chain || ': ' || p.name, '; ') FROM clean.products p
                WHERE {BKEY_SQL} = {bkey_col})"""


def section_tiers(con) -> str:
    per = con.execute("""
        SELECT staple, count(*) FILTER (WHERE match_quality = 'strong'), count(*) FILTER (WHERE match_quality = 'weak'),
               count(*) FILTER (WHERE status = 'ambiguous'), count(*) FILTER (WHERE status = 'excluded')
        FROM clean.staple_groups GROUP BY staple ORDER BY staple""").fetchall()
    con.execute("SELECT setseed(0.17)")
    weak = con.execute(f"""
        SELECT g.staple, g.bkey, round(100 * g.share_match), {_names()} FROM clean.staple_groups g
        WHERE g.match_quality = 'weak' ORDER BY random() LIMIT 30""").fetchall()
    changes = f"read_csv('{GROUP_CHANGES}', header=true, all_varchar=true, quote='\"')"
    con.execute("SELECT setseed(0.18)")
    moved = con.execute(f"""
        SELECT g.staple, g.bkey, round(100 * g.share_match), round(100 * g.share_excluded), {_names()}
        FROM clean.staple_groups g JOIN {changes} o USING (staple, bkey)
        WHERE o.before = 'member' AND o.after = 'ambiguous' ORDER BY random() LIMIT 30""").fetchall()
    n_moved = con.execute(f"""
        SELECT count(*) FILTER (WHERE before = 'member' AND after = 'ambiguous'),
               count(*) FILTER (WHERE before <> 'member' AND after = 'member'),
               count(*) FILTER (WHERE before = 'member' AND after = 'excluded') FROM {changes}""").fetchone()
    return "\n".join([
        "## 1. Pripadnost grupe: tri razine", "",
        "m = udio lanaca čiji naziv prolazi `must_match` bez `must_not_match`, x = udio lanaca čiji naziv pogađa "
        "`must_not_match`. **Snažni** član: m > 50 % i x < 10 %. **Slabi** (`match_quality = 'weak'`): x = 0, "
        "m ≥ 25 %, jedinica spojiva, barem jedan proizvod unutar min/max pakiranja i medijan cijene po jedinici u "
        "granicama; u zadanom je izboru, ali ispod snažnih i označen (`find_products.match_quality`, u košarici "
        "zastavica `weak_match`). Inače `ambiguous` (m > 0) ili `excluded` (m = 0).", "",
        f"Prema pravilu iz 2D: {n_moved[0]} grupa prelazi iz člana u `ambiguous`, {n_moved[2]} u `excluded`, "
        f"a {n_moved[1]} postaje član.", "",
        md_table(["namirnica", "snažnih", "slabih", "dvosmislenih", "isključenih"], per), "",
        "Napomena: među slabim članovima ima krivih pogodaka kad drugi lanci proizvod zovu samo markom, a jedan "
        "naziv prolazi `must_match` (npr. „ČOKOLADA RIKI PŠENICA I MED“ kao med, „MINI CROASANI S MASLACEM“ kao "
        "maslac). Rangirani su ispod snažnih i označeni; točka 4 (kratice, `must_not_match`) dio njih uklanja.", "",
        "30 slučajnih slabih članova:", "",
        md_table(["namirnica", "grupa", "m %", "nazivi po lancu"], weak), "",
        "30 grupa koje prelaze iz člana (2D) u `ambiguous`:", "",
        md_table(["namirnica", "grupa", "m %", "x %", "nazivi po lancu"], moved),
    ])


def section_synonyms(con) -> str:
    changes = f"read_csv('{DATA / 'groups_changes_2e4.csv'}', header=true, all_varchar=true, quote='\"')"
    per = con.execute(f"""
        SELECT staple, count(*) FILTER (WHERE before <> 'member' AND after = 'member'),
               count(*) FILTER (WHERE before = 'member' AND after <> 'member')
        FROM {changes} GROUP BY staple ORDER BY 2 DESC, 3 DESC""").fetchall()
    con.execute("SELECT setseed(0.44)")
    examples = con.execute(f"""
        SELECT o.staple, g.match_quality, {_names()} FROM {changes} o
        JOIN clean.staple_groups g USING (staple, bkey)
        WHERE o.before <> 'member' AND o.after = 'member' ORDER BY random() LIMIT 30""").fetchall()
    return "\n".join([
        "## 4. Sinonimi i kratice", "",
        "`data/abbrev.yaml` proširuje kratice prije podudaranja (`clean.products.match_norm`; izvorni naziv i "
        "`name_norm` ostaju): praš. pec. → prašak za pecivo, braš. → brašno, mlij. → mlijeko, jog. → jogurt, "
        "tj./tje./tjest. → tjestenina, vrh. → vrhnje, pil. → pileći, kuh. → kuhanje, „ŠIR VALJ“ → široki. "
        "„pec.“ i „sv.“ sami se ne šire (peč./pečeni, svinjski/svježe).", "",
        "Novi `must_match`: tjestenina (oblici i marke iz zahtjeva), jogurt `jog\\b`, pileća prsa (odresci, file od "
        "prsa, pileći file; `odresc` više nije isključen), svinjetina (rebra), vrhnje za kuhanje (creme cuisine), "
        "tvrdi sir (leerdammer, emmental, maasdam, edam\\b, cheddar). Tuna isključuje cous, bowl, sal, salat. "
        "Uz „školjke“ i „tj“ dodana su isključenja (morski plodovi, pralines, čarape, „za tj“ = za tijelo, gotove "
        "lazanje).", "",
        "Grupe vraćene u namirnicu (i izgubljene) po namirnici:", "",
        md_table(["namirnica", "vraćeno", "izgubljeno"], per), "",
        "30 nasumičnih vraćenih grupa:", "",
        md_table(["namirnica", "razina", "nazivi po lancu"], examples),
    ])


def section_cvijet(con) -> str:
    changes = f"read_csv('{DATA / 'food_changes_2e5.csv'}', header=true, all_varchar=true, quote='\"')"
    moved = con.execute(f"SELECT before || ' → ' || after, count(*) FROM {changes} GROUP BY 1 ORDER BY 2 DESC").fetchall()
    cvijet = f"""FROM clean.products p JOIN {changes} o USING (chain, product_id)
                 WHERE o.after = 'hrana' AND regexp_matches(p.name_norm, '(^| )(cvijet|cvjet)')"""
    n = con.execute(f"SELECT count(*) {cvijet}").fetchone()[0]
    con.execute("SELECT setseed(0.5)")
    sample = con.execute(f"SELECT p.chain, p.name, p.category, o.before {cvijet} ORDER BY random() LIMIT 20").fetchall()
    kids = con.execute(f"""SELECT p.chain, p.name, o.before, o.after FROM clean.products p JOIN {changes} o
                           USING (chain, product_id) WHERE o.after = 'pice' ORDER BY p.chain, p.name LIMIT 12""").fetchall()
    return "\n".join([
        "## 5. „cvijet“ i dječji pjenušac", "",
        "„cvijet“ više nije u strogom popisu neprehrane (vrijedi za sve proizvode), nego samo u širem popisu za ručne "
        "iznimke po lancu, uz zaštite: čaj, brokula, cvjetača, sol, kulen, kamilica, bazga, neven, lipa, ukrasni "
        "cvjetići. Dječji pjenušac (dječj…, spužva bob, bez alkohola, 0,0, i kategorija „DJEČJI PJENUŠCI“) je "
        "`pice`, ne `alkohol`.", "",
        md_table(["promjena", "proizvoda"], moved), "",
        f"Vraćeno u `hrana` s „cvijet“ u nazivu: **{n}**. 20 primjera:", "",
        md_table(["lanac", "naziv", "kategorija", "prije"], sample), "",
        "Napomena: Metro „BEGONIJA CVIJET KOM“ (biljka u kategoriji hrane) se vraća u hranu, jer Metro nije među "
        "ručnim iznimkama po lancu; vrećice sjemena („SJEME GARDEN CVJETAČA“) ostaju neprehrana.", "",
        "Primjeri novog `pice`:", "",
        md_table(["lanac", "naziv", "prije", "poslije"], kids),
    ])


SECTIONS = {"1": section_tiers, "4": section_synonyms, "5": section_cvijet}


def main() -> None:
    args = sys.argv[1:]
    db_path = args.pop(0) if args and not args[0].isdigit() else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    parts = [f"# Pregled Koraka 2E (arhiva {date.isoformat()})", "",
             "Generira `scripts/step2e_review.py` nad izgrađenom bazom; sažetak je u REVIEW_2E.md.", ""]
    parts += [f(con) + "\n" for key, f in SECTIONS.items() if not args or key in args]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT}: {len(parts) - 4} odjeljaka")


if __name__ == "__main__":
    main()
