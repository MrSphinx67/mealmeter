"""Izvještaj za jutarnji pregled (Korak 2C): docs/MORNING_REVIEW.md.

Svaka točka ima svoju funkciju koja vraća Markdown; skripta ih izvodi redom nad izgrađenom bazom.

Upotreba: python scripts/morning_review.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import sys
from decimal import Decimal
from pathlib import Path

import duckdb

from mealmeter.food import food_report
from mealmeter.search import find_products
from mealmeter.staples import SINGLE_PACK_UNITS, STAPLE_PPU_SQL, load_staples, staple_price_suspects, staple_suspect_sql

OUT = Path("docs/MORNING_REVIEW.md")


def hr(v, d: int = 2) -> str:
    """Broj s decimalnim zarezom."""
    return f"{float(v):.{d}f}".replace(".", ",")


def md_table(headers: list[str], rows) -> str:
    def cell(v):
        if v is None:
            return ""
        if isinstance(v, Decimal):
            v = float(v)
        if isinstance(v, float):
            return f"{v:.2f}".replace(".", ",")
        return str(v).replace("|", "\\|").replace("*", "\\*")
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(cell(v) for v in r) + " |" for r in rows]
    return "\n".join(lines)


def section_food(con) -> str:
    by_chain = con.execute("""
        SELECT chain, count(*) AS n,
               count(*) FILTER (WHERE category_source <> 'chain') AS n_no,
               count(*) FILTER (WHERE category_source = 'ean_inherited') AS n_ean,
               count(*) FILTER (WHERE category_source = 'words') AS n_words,
               count(*) FILTER (WHERE food_group = 'unknown') AS n_unknown
        FROM clean.products GROUP BY chain HAVING n_no > 0 ORDER BY n_no DESC
    """).fetchall()
    rows = [(c, n, no, ean, f"{100 * ean / no:.1f} %", w, unk) for c, n, no, ean, w, unk in by_chain]
    rep = food_report(con)
    out = ["## 0. Filtar hrane", "",
           "Proizvodi bez korisne kategorije lanca (nema je, ili je „Ostalo“) po lancu: koliko ih je "
           "naslijedilo skupinu preko globalnog EAN-a (većinska skupina u lancima s kategorijom, > 50 %), "
           "koliko ih je razvrstano popisom riječi i koliko ostaje `unknown`.", "",
           md_table(["lanac", "proizvoda", "bez kategorije", "EAN", "udio EAN", "riječi", "unknown"], rows), "",
           "Proizvodi izvan zadanog izbora (`find_products`/`get_prices` bez `include_*`), po skupini. "
           "Nijedan nije obrisan iz baze.", "",
           md_table(["skupina", "proizvoda", "iz kategorije", "preko EAN-a", "iz riječi"], rep["excluded"]), "",
           f"20 nasumičnih proizvoda s `is_food = true` čiji naziv izgleda neprehrambeno "
           f"(od {rep['n_suspect']} koje pogađa `food.SUSPECT_NONFOOD_REGEX`):", "",
           md_table(["lanac", "naziv", "kategorija lanca", "skupina", "izvor"], rep["suspects"])]
    return "\n".join(out)


def _staple_prices(staple: str, extra_attrs: tuple[str, ...] = ()) -> str:
    """SQL: cijene po jedinici usporedbe za proizvode namirnice (bez isključenih; samo provjerena hrana),
    sa stupcima chain, product_id, name, price_eff, ppu i vrijednostima atributa iz extra_attrs."""
    joins = "".join(
        f""" LEFT JOIN clean.product_attrs a_{a} ON a_{a}.chain = ps.chain AND a_{a}.product_id = ps.product_id
              AND a_{a}.staple = ps.staple AND a_{a}.attr = '{a}'""" for a in extra_attrs)
    cols = "".join(f", coalesce(a_{a}.value, '-') AS {a}" for a in extra_attrs)
    return f"""
        SELECT p.chain, p.product_id, p.name, c.price_eff, {STAPLE_PPU_SQL} AS ppu, c.per_unit,
               c.price_per_unit, p.pack_amount, p.pack_unit, ps.n_units{cols}
        FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
        JOIN clean.prices c USING (chain, product_id) JOIN clean.products p USING (chain, product_id){joins}
        WHERE ps.staple = '{staple}' AND NOT ps.excluded AND ps.drop_reason IS NULL AND p.is_food"""


def section_eggs(con) -> str:
    base = _staple_prices("jaja", ("velicina", "uzgoj"))
    distinct = f"SELECT DISTINCT chain, name, velicina, uzgoj, ppu FROM ({base}) WHERE ppu IS NOT NULL"
    extreme = con.execute(f"""
        SELECT chain, name, n_units, price_eff, ppu, count(*) FROM ({base})
        WHERE velicina = 'm' AND (ppu >= 1.0 OR ppu <= 0.16) GROUP BY ALL ORDER BY ppu DESC""").fetchall()
    q_all = con.execute(f"SELECT count(*), quantile_cont(ppu, [0.05, 0.5, 0.95]) FROM ({distinct})").fetchone()
    by_uzgoj = con.execute(f"""
        SELECT uzgoj, count(*), quantile_cont(ppu, 0.05), quantile_cont(ppu, 0.5), quantile_cont(ppu, 0.95),
               count(*) FILTER (WHERE ppu NOT BETWEEN (SELECT ppu_min FROM clean.staple_rules WHERE staple = 'jaja')
                                                  AND (SELECT ppu_max FROM clean.staple_rules WHERE staple = 'jaja'))
        FROM ({distinct}) GROUP BY uzgoj ORDER BY count(*) DESC""").fetchall()
    classes = con.execute(f"""SELECT velicina || ':' || uzgoj, count(*) FROM ({distinct})
                              GROUP BY 1 ORDER BY 1""").fetchall()
    n, (p5, p50, p95) = q_all
    lo, hi = con.execute("SELECT ppu_min, ppu_max FROM clean.staple_rules WHERE staple = 'jaja'").fetchone()
    return "\n".join([
        "## 1. Jaja", "",
        "Uzgoj iz naziva: BIO/EKO → bio (prvi, jer „EKO … SLOBODNI UZGOJ“ je ekološki), KAVEZNI → kavezni, "
        "PODNI → podni, SLOBODNI → slobodni, inače `nepoznato`. Grupe su `jaja:<veličina>:<uzgoj>` "
        "(`get_prices` prima i `jaja:m` za sve uzgoje), a `plan_basket` vraća `attributes` odabranog "
        "proizvoda (velicina, uzgoj).", "",
        "Nazivi u `jaja:m` s krajnjim cijenama po jajetu (≥ 1,00 ili ≤ 0,16 €; 1,30 € je Metroov karton, "
        "a 0,10 € je bila donja granica starog raspona):", "",
        md_table(["lanac", "naziv", "komada", "cijena €", "€/kom", "trgovina"], extreme), "",
        f"Distribucija cijene po jajetu (provjerena hrana, {n} različitih parova proizvod × cijena): 5. percentil "
        f"**{hr(p5)}**, medijan {hr(p50)}, 95. percentil **{hr(p95)}** €. "
        f"**Primijenjeno: `plausible_per_unit: [{lo:g}, {hi:g}]`** (prije [0.1, 1.5]). "
        f"Bio i dio slobodnog uzgoja su iznad {hr(hi)} €; ako ih želiš u zadanom izboru, gornja granica bi "
        "trebala biti oko 0,55 €.", "",
        md_table(["uzgoj", "proizvoda", "p5", "medijan", "p95", "izvan granica"], by_uzgoj), "",
        "Klase (veličina:uzgoj) i broj različitih proizvoda: "
        + ", ".join(f"`{k}` {v}" for k, v in classes),
    ])


def section_variants(con) -> str:
    staples = load_staples()
    rows = []
    for key in ("brasno", "secer", "ulje", "rajcica"):
        st = staples[key]
        for attr, value in st.default_exclude_variants:
            n, example = con.execute("""
                SELECT count(DISTINCT CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END),
                       min(p.name)
                FROM clean.product_attrs a JOIN clean.products p USING (chain, product_id)
                WHERE a.staple = ? AND a.attr = ? AND a.value = ? AND p.is_food""", [key, attr, value]).fetchone()
            rows.append((key, f"{attr}={value}", n, example))
    rice = find_products(ingredient="riza", limit=10, con=con)
    rice_rows = [(r["id"], r["name"], ", ".join(f"{a}={v}" for a, v in r["attributes"].items()),
                  "; ".join(f"{a}: {src['how']} („{src['name']}“)" for a, src in r["attribute_sources"].items()))
                 for r in rice]
    return "\n".join([
        "## 2. Zadane varijante", "",
        "Zadano isključene varijante (vraćaju se samo kad je atribut izričito zadan) i broj grupa (EAN ili "
        "lanac + naziv) s tom vrijednošću:", "",
        md_table(["namirnica", "varijanta", "grupa", "primjer"], rows), "",
        "- brašno: `vrsta` bez oznake je `psenicno` (zadano); heljdino više nije u `must_not_match`, nego je varijanta.",
        "- šećer: `vrsta` bez oznake je `bijeli`.",
        "- ulje: Zvijezda Omegol i Mediteran su `vrsta=omegol|mediteran`, hladno prešano je `presanje=hladno`.",
        "- rajčica: cherry (i koktel, cocktail, mini), datterino, harmony i campari su izvan zadanog izbora.", "",
        "**Riža i „oro“:** nijedan proizvod ne dobiva `parboiled` bez riječi „parboiled“ u nazivu "
        "(test `test_riza_oro_alone_not_parboiled`). Grupa 8001860190520 prikazuje se kao „Riso Scotti riža oro "
        "dugog zrna“, ali isti EAN u 10 lanaca glasi „RIŽA ORO PARBOILED“, pa je skupni atribut `parboiled` "
        "s izvorom `name`. To nisam mijenjao: Scotti Oro jest parboiled riža.", "",
        "Izvor atributa za 10 grupa riže (`find_products(ingredient=\"riza\")`):", "",
        md_table(["id", "naziv", "atributi", "izvor (how, naziv)"], rice_rows),
    ])


# broj grupa kakaa prije promjene pravila (find_products(ingredient="kakao"), commit fcbd8be)
KAKAO_GROUPS_BEFORE = 173


def section_kakao(con) -> str:
    res = find_products(ingredient="kakao", limit=10000, con=con)
    top = [(r["id"], r["name"], r["pack"], r["n_chains"],
            f"{hr(r['price_per_unit_min'])}–{hr(r['price_per_unit_max'])}" if r["price_per_unit_min"] else "")
           for r in res[:10]]
    return "\n".join([
        "## 3. Kakao", "",
        "Pozitivno podudaranje: naziv počinje s „kakao“ ili sadrži „kakao prah“, „prah kakao“, „kakao u prahu“ "
        "(i „kakao u pr.“), „kakao za kolače“. Isključeno: tortela, tortin, muffin, krema, benquick, napitak, "
        "choco box, te (moja dopuna) desert, kolač, rolice, šnite, biskvit, krafne, tabla (čokolada), instant i vending napitci, Dolce Gusto, „XXL“ i Lumpi (instant napitak).", "",
        f"Grupa prije: **{KAKAO_GROUPS_BEFORE}**, poslije: **{len(res)}**.", "",
        "Top 10:", "",
        md_table(["id", "naziv", "pakiranje", "lanaca", "€/kg"], top),
    ])


def section_chicken(con) -> str:
    rows = con.execute("""
        SELECT CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END AS grp,
               string_agg(DISTINCT p.name, '; ' ORDER BY p.name), string_agg(DISTINCT p.chain, ', ' ORDER BY p.chain),
               min(c.price_per_unit), median(c.price_per_unit), max(c.price_per_unit), count(*)
        FROM clean.product_staples ps JOIN clean.products p USING (chain, product_id)
        JOIN clean.prices c USING (chain, product_id)
        WHERE ps.staple = 'pileca_prsa' AND c.per_unit = 'kg' AND regexp_matches(p.name_norm, '(^| )(jeli|je li)\\b')
        GROUP BY grp ORDER BY median(c.price_per_unit)""").fetchall()
    lo, hi, n_bad, n_all = con.execute(f"""
        SELECT any_value(r.ppu_min), any_value(r.ppu_max),
               count(*) FILTER (WHERE c.price_per_unit NOT BETWEEN r.ppu_min AND r.ppu_max), count(*)
        FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple) JOIN clean.prices c USING (chain, product_id)
        WHERE ps.staple = 'pileca_prsa' AND NOT ps.excluded AND ps.drop_reason IS NULL AND c.per_unit = 'kg'""").fetchone()
    outside = con.execute("""
        SELECT p.chain, p.name, min(c.price_per_unit), max(c.price_per_unit), count(*)
        FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
        JOIN clean.prices c USING (chain, product_id) JOIN clean.products p USING (chain, product_id)
        WHERE ps.staple = 'pileca_prsa' AND NOT ps.excluded AND ps.drop_reason IS NULL AND c.per_unit = 'kg'
          AND c.price_per_unit NOT BETWEEN r.ppu_min AND r.ppu_max
        GROUP BY ALL ORDER BY count(*) DESC LIMIT 15""").fetchall()
    return "\n".join([
        "## 4. Pileća prsa: „Jeli“ (ČEKA POTVRDU)", "",
        f"`plausible_per_unit: [{lo:g}, {hi:g}]` €/kg je primijenjen: izvan granica je {n_bad} od {n_all} cijena "
        "po kg preostalih (neisključenih) proizvoda.", "",
        "Sve grupe s „jeli“ ili „je li“ u nazivu. To je Gavrilovićeva linija **Jeli**: delikatesna pileća prsa "
        "(narezak od 350 g i štruca od 2,6 kg), a ne svježi file. **Privremeno su isključene** iz `pileca_prsa` "
        "(`must_not_match: jeli\\b, je li\\b`) dok ne potvrdiš. Ako ih treba vratiti, dovoljno je obrisati ta "
        "dva uzorka u `staples.yaml`.", "",
        md_table(["grupa", "nazivi", "lanci", "min €/kg", "medijan €/kg", "max €/kg", "cijena"], rows), "",
        "Napomena: štruca od 2,6 kg ima 2,30–4,38 €/kg, pa vjerojatno nosi cijenu po kg kao cijenu "
        "pakiranja (lanac je cijenu po kg upisao kao cijenu proizvoda).", "",
        "**Upozorenje uz granicu od 5 €/kg:** ispod nje su i stvarna svježa prsa po akcijskoj ili diskontnoj "
        "cijeni (Konzum K Plus 4,69 €/kg u 184 trgovine, Eurospin 4,99 €/kg). Ona sada postaju `price_suspect` "
        "i u košarici su samo rezerva. Prijedlog: donja granica 2,5 ili 3 €/kg. Najčešće cijene izvan granica:", "",
        md_table(["lanac", "naziv", "min €/kg", "max €/kg", "cijena"], outside),
    ])


def section_onion(con) -> str:
    rows = con.execute(f"""
        SELECT p.name,
               CASE WHEN bool_or(ps.excluded) THEN 'isključen' WHEN bool_or(ps.drop_reason IS NOT NULL)
                    THEN any_value(ps.drop_reason) ELSE 'luk' END AS status,
               coalesce(any_value(a.value), '-') AS vrsta,
               min({STAPLE_PPU_SQL}), max({STAPLE_PPU_SQL}),
               count(DISTINCT p.chain), string_agg(DISTINCT p.chain, ', ' ORDER BY p.chain)
        FROM clean.product_staples ps JOIN clean.staple_rules r USING (staple)
        JOIN clean.products p USING (chain, product_id) JOIN clean.prices c USING (chain, product_id)
        LEFT JOIN clean.product_attrs a ON a.chain = ps.chain AND a.product_id = ps.product_id
             AND a.staple = 'luk' AND a.attr = 'vrsta'
        WHERE ps.staple = 'luk' AND regexp_matches(p.name_norm, '(^| )(crven|ljubicast|srebren|zut|bijel)')
        GROUP BY p.name ORDER BY vrsta, status, p.name""").fetchall()
    return "\n".join([
        "## 5. Luk: nazivi s bojom (ČEKA POTVRDU, mapiranje nije mijenjano)", "",
        "Svi različiti nazivi kandidata za `luk` (`must_match` luk/kapula) koji sadrže crveni, ljubičasti, "
        "srebrenac, žuti ili bijeli, uz trenutni status, vrstu iz naziva, raspon cijene po kg (s pretpostavljenih "
        "500 g za „rukavac“) i broj lanaca. `vrsta`: crveni = crven|ljubičast, žuti = žut|srebren, "
        "bijeli = bijel.", "",
        md_table(["naziv", "status", "vrsta", "min €/kg", "max €/kg", "lanaca", "lanci"], rows), "",
        "Zapažanja (bez promjene mapiranja):",
        "- „LUK BIJELI (ČEŠNJAK)“ je češnjak; isključen je kroz `cesnjak`. Vrsta `bijeli` zato pogađa samo "
        "„LUK LJUBIČ./BIJELI ZA GASTRO“, koji je ljubičasti luk: kratica „ljubič.“ ne pogađa `ljubicast`.",
        "- „LUK SREBRENAC“ postoji u 20-ak lanaca i **jest u namirnici** (vrsta `zuti`): uzorak `srebrn` u "
        "`must_not_match` ne pogađa „srebrenac“ (srebr-e-nac), pa ništa ne isključuje. Ako je srebrenac "
        "trebao biti isključen, uzorak bi bio `srebren`.",
        "- Pakiranja bez gramature („LUK SREBRENAC 4/1“, „3/1“) nemaju cijenu po kg; `packaged` (500 g) "
        "vrijedi samo za „rukavac“.",
        "- Metroove vreće od 10 kg imaju oko 0,74 €/kg, a „slatki“ crveni luk 3,28 €/kg.",
    ])


def section_salt(con) -> str:
    rows = con.execute("""
        SELECT p.chain, p.name, p.pack_amount, coalesce(ps.drop_reason, 'sol') FROM clean.product_staples ps
        JOIN clean.products p USING (chain, product_id)
        WHERE ps.staple = 'sol' AND NOT ps.excluded AND regexp_matches(p.name_norm, '(^| )soljenk')
        ORDER BY 4, p.chain, p.name""").fetchall()
    target = [r for r in rows if r[1].upper().startswith("SOL MORSKA SITNA 250G SOLJENKA")]
    return "\n".join([
        "## 6. Sol i soljenka", "",
        "`soljenk` više nije u `must_not_match`. Novo polje `require_pack: [soljenk]`: soljenka ispada iz soli "
        "samo ako nema gramature (`drop_reason = 'bez_gramature'`, prazna posuda).", "",
        f"Test „SOL MORSKA SITNA 250G SOLJENKA“: {'u soli' if target and target[0][3] == 'sol' else 'NIJE u soli'} "
        f"({', '.join(f'{r[0]}: {r[3]}' for r in target)}); testovi `test_sol_soljenka_*`.", "",
        f"Svi proizvodi soli sa „soljenk“ ({len(rows)}):", "",
        md_table(["lanac", "naziv", "g", "status"], rows),
    ])


def section_milk(con) -> str:
    from mealmeter.basket import plan_basket

    dist = con.execute("""
        SELECT coalesce(v.value, '-'), coalesce(m.value, '-'), count(DISTINCT p.chain || p.product_id)
        FROM clean.product_staples ps JOIN clean.products p USING (chain, product_id)
        LEFT JOIN clean.product_attrs v ON v.chain = ps.chain AND v.product_id = ps.product_id
             AND v.staple = 'mlijeko' AND v.attr = 'vrsta'
        LEFT JOIN clean.product_attrs m ON m.chain = ps.chain AND m.product_id = ps.product_id
             AND m.staple = 'mlijeko' AND m.attr = 'mast'
        WHERE ps.staple = 'mlijeko' AND NOT ps.excluded AND ps.drop_reason IS NULL AND p.is_food
        GROUP BY ALL ORDER BY 1, 2""").fetchall()
    res = plan_basket([{"name": "mlijeko", "amount": 0.5, "unit": "l"}], "Osijek", con=con)
    items = [(s["chain"], s["address"], s["items"][0]["name"], s["items"][0]["attributes"].get("vrsta"),
              s["items"][0]["attributes"].get("mast"), s["items"][0]["cost_pack"],
              "; ".join(n for n in s["items"][0]["notes"] if "zamjenjivo" in n))
             for s in res["stores"][:8]]
    return "\n".join([
        "## 7. Mlijeko", "",
        "Zadano `vrsta=trajno, mast=2.8` (`default_attributes`), a masnoća 2,8–3,8 % je zamjenjiva "
        "(`substitutes: {mast: [2.8, 3.2, 3.5, 3.8]}`). Svježe i trajno su zasebne vrste (nisu zamjenjive). "
        "`plan_basket` vraća `applied_attributes` i `accepted_values` po sastojku, te `attributes` (vrsta, mast) "
        "odabranog proizvoda; zamjena ide u `notes`. Novo prepoznavanje: „TR“ = trajno, „SV.“ = svježe.", "",
        "Isključeni krivi pogoci: palačinke s mlijekom, acidofilno, kiselo („KIS.“), protein, „ČOKOL.“.", "",
        "Proizvodi po vrsti i masnoći (`-` = nije u nazivu; bez vrste ne ulaze u zadani izbor):", "",
        md_table(["vrsta", "mast", "proizvoda"], dist), "",
        "Primjer: `plan_basket` 0,5 l mlijeka u Osijeku (prvih 8 trgovina):", "",
        md_table(["lanac", "adresa", "proizvod", "vrsta", "mast", "€", "zamjena"], items),
    ])


def section_parsley(con) -> str:
    from mealmeter.basket import plan_basket

    rows = con.execute(f"""
        SELECT CASE WHEN ppu IS NULL THEN 'bez cijene po kg (vezica/komad)' ELSE 'cijena po kg' END,
               count(DISTINCT chain || product_id), min(ppu), median(ppu), max(ppu), min(name)
        FROM ({_staple_prices('persin')}) GROUP BY 1 ORDER BY 1""").fetchall()
    res = plan_basket([{"name": "peršin", "amount": 20, "unit": "g"}], "Zagreb", con=con)
    best = res["best_store"]
    it = best["items"][0] if best else None
    example = (f"`plan_basket` 20 g peršina u Zagrebu: {best['chain']}, „{it['name']}“, pakiranje "
               f"{hr(it['cost_pack'])} €, utrošeno (u ukupno) {hr(it['cost_used'])} €." if it else "")
    return "\n".join([
        "## 8. Peršin i svježe bilje", "",
        "Peršin: `unit: kg`, `pantry: true` (u ukupno ulazi utrošeni dio). Proizvodi bez gramature i bez "
        "cijene po kg (vezice, komadi) se ne pretvaraju: nemaju cijenu po kg, pa ne ulaze u usporedbu ni u "
        "košaricu, a jedinica „vezica“ u receptu daje grešku (nema pretpostavljene mase). Drugog svježeg "
        "bilja u rječniku još nema (bosiljak, kopar i vlasac su samo isključenja kod drugih namirnica).", "",
        md_table(["proizvodi", "broj", "min €/kg", "medijan €/kg", "max €/kg", "primjer"], rows), "",
        example,
    ])


def section_units(con) -> str:
    import yaml

    from mealmeter.units import UNITS_PATH, convert

    raw = yaml.safe_load(UNITS_PATH.read_text(encoding="utf-8"))
    staples = load_staples()
    measures = [(k, hr(m["ml"], 1), ", ".join(m["aliases"]), "da" if m["estimate"] else "ne")
                for k, m in raw["measures"].items()]
    dens = []
    for k, d in raw["densities"].items():
        row = [k, hr(d["g_per_ml"])]
        for m in ("zlica", "zlicica", "salica"):
            qty, base, _ = convert(1, m, staples[k])
            row.append(f"{hr(qty, 1)} {base}")
        dens.append((*row, "da" if d["estimate"] else "ne"))
    return "\n".join([
        "## 9. Pretvorba mjera (PROCJENE, za pregled)", "",
        "`data/units.yaml` i `src/mealmeter/units.py` (`convert(amount, unit, staple)` → (količina, g|ml, "
        "upozorenja)). `plan_basket` prima ove mjere; svaka pretvorba vraća upozorenje s korištenom "
        "vrijednošću. Namirnica bez gustoće računa se s 1 g/ml (uz upozorenje), a namirnica u komadima "
        "(jaja) ne može se mjeriti žlicom.", "",
        md_table(["mjera", "ml", "aliasi", "procjena"], measures), "",
        md_table(["namirnica", "g/ml", "1 žlica", "1 žličica", "1 šalica", "procjena"], dens),
    ])


# cijene izvan automatskih granica prije Koraka 2C.10 (build_clean.py, commit f1c5420): (odbačeno, od)
SACHET_SUSPECTS_BEFORE = {"kvasac": (2250, 12364), "prasak_za_pecivo": (10, 6024), "vanilin_secer": (333, 9639)}


def section_sachets(con) -> str:
    suspects = {k: (bad, n) for k, _, bad, n in staple_price_suspects(con)}
    rows, outliers = [], []
    for key in ("kvasac", "prasak_za_pecivo", "vanilin_secer"):
        base = _staple_prices(key)
        single = f"SELECT DISTINCT chain, name, ppu FROM ({base}) WHERE n_units <= {SINGLE_PACK_UNITS}"
        n, q, mx = con.execute(f"SELECT count(*), quantile_cont(ppu, [0.05, 0.5, 0.95]), max(ppu) FROM ({single})").fetchone()
        lo, hi = con.execute("SELECT ppu_min, ppu_max FROM clean.staple_rules WHERE staple = ?", [key]).fetchone()
        b_bad, b_n = SACHET_SUSPECTS_BEFORE[key]
        a_bad, a_n = suspects.get(key, (0, 0))
        rows.append((key, n, hr(q[0]), hr(q[1]), hr(q[2]), hr(mx), f"{hr(lo)}–{hr(hi)}",
                     f"{b_bad} / {b_n} ({hr(100 * b_bad / b_n, 1)} %)",
                     f"{a_bad} / {a_n} ({hr(100 * a_bad / a_n, 1)} %)" if a_n else "-"))
        outliers += con.execute(f"""
            SELECT '{key}', b.chain, b.name, b.n_units, b.price_eff, b.ppu, count(*) FROM ({base}) b,
                   (SELECT * FROM clean.staple_rules WHERE staple = '{key}') r
            WHERE {staple_suspect_sql('b.ppu', 'b.n_units')} GROUP BY ALL ORDER BY count(*) DESC LIMIT 5""").fetchall()
    return "\n".join([
        "## 10. Kvasac, prašak za pecivo, vanilin šećer: granice po vrećici", "",
        "Automatske granice (0,25x–4x medijana) su ugašene; cijena se uspoređuje po vrećici (`compare_by: pack`), "
        "a granice su `plausible_per_pack` (`clean.staple_rules.range_source = 'pack'`). Prijedlog iz podataka: "
        "5. percentil do 1,25 × 95. percentila cijene **pojedinačnih vrećica**, zaokruženo na 0,05 €. "
        "`price_suspect` je cijena po vrećici iznad gornje granice, ili pojedinačna vrećica ispod donje; "
        "rinfuza i višestruka pakiranja smiju biti jeftinija po vrećici (prije je zato 18 % kvasca bilo odbačeno).", "",
        md_table(["namirnica", "pojedinačnih vrećica", "p5 €", "medijan €", "p95 €", "max €", "granice €",
                  "odbačeno prije", "odbačeno sada"], rows), "",
        "Najčešće cijene izvan granica:", "",
        md_table(["namirnica", "lanac", "naziv", "vrećica", "cijena €", "€/vrećica", "trgovina"], outliers), "",
        "Napomena: donja granica kvasca (0,30 €) pogađa i vjerojatno stvarne cijene trgovačkih marki "
        "(Kaufland 0,13 €, Harmer 0,24 €). Ako su to stvarne cijene, donja granica bi trebala biti oko 0,10 €.",
    ])


# grupe po obliku prije Koraka 2C.11: pravila iz staples.yaml u commitu 2918655 na istim grupama, uz isti
# izbor vrijednosti grupe (najviše proizvoda, pa abecedno)
FORMS = ("konzerva", "suho", "smrznuto", "svjeze", "nepoznato")
FORMS_BEFORE = {
    "gljive": (7, 1, 1, 17, 90), "grah": (72, 28, 4, 1, 313), "grasak": (24, 4, 19, 0, 106),
    "kukuruz": (27, 0, 5, 2, 126), "leca": (10, 11, 0, 0, 111), "slanutak": (20, 7, 2, 0, 98),
}
FORM_STAPLES = tuple(FORMS_BEFORE)


def section_forms(con) -> str:
    keys = ", ".join(f"'{k}'" for k in FORM_STAPLES)
    groups = f"""
        WITH m AS (
          SELECT ps.staple, CASE WHEN p.ean_global THEN p.ean_norm ELSE p.chain || ':' || p.name_norm END AS grp,
                 a.value, a.how, p.name, p.pack_amount
          FROM clean.product_staples ps JOIN clean.products p USING (chain, product_id)
          JOIN clean.product_attrs a ON a.chain = ps.chain AND a.product_id = ps.product_id
               AND a.staple = ps.staple AND a.attr = 'oblik'
          WHERE ps.staple IN ({keys}) AND NOT ps.excluded AND ps.drop_reason IS NULL AND p.is_food IS NOT false
        ),
        v AS (  -- vrijednost grupe: najviše proizvoda, pa abecedno
          SELECT staple, grp, value FROM (SELECT staple, grp, value, count(*) AS n FROM m GROUP BY ALL)
          QUALIFY row_number() OVER (PARTITION BY staple, grp ORDER BY n DESC, value) = 1
        )
        SELECT m.staple, m.grp, v.value AS oblik, bool_or(m.how = 'heuristic' AND m.value = v.value) AS heur,
               max(m.name) AS name, any_value(m.pack_amount) AS pack
        FROM m JOIN v USING (staple, grp) GROUP BY ALL"""
    counts = dict(((k, f), n) for k, f, n in con.execute(
        f"SELECT staple, oblik, count(*) FROM ({groups}) GROUP BY ALL").fetchall())
    forms = list(FORMS)
    count_rows = [(k, *[f"{counts.get((k, f), 0)} ({b})" for f, b in zip(forms, FORMS_BEFORE[k])])
                  for k in FORM_STAPLES]
    con.execute("SELECT setseed(0.11)")
    out = ["## 11. Oblik mahunarki, kukuruza i gljiva", "",
           "Heuristika: konzerva ako naziv ili stupac `unit` sadrži LIM, LIMENK, OC.MASA, OCIJE, STAKLO, VAKUM ili "
           "NALJEV (uz postojeće oznake: konz, ocij., neto, 400/240 g…). Smrznuto ako sadrži LEDO, SMRZ, FROZY, "
           "FRESCO ili ZAMRZ. Suho (`dry_rule`, `how = heuristic`) ako je pakiranje 400–1000 g, nema oznaka "
           "konzerve ni smrznutog, a `unit` je rinfuza ili naziv sadrži PVC, VREĆICA, NATURA, VEDRINI, PRIMAVITA ili "
           "ADVENT. Vrećica i PVC više sami ne znače suho, nego samo uz taj uvjet. Gljive nemaju `dry_rule` "
           "(500 g u vrećici su svježi šampinjoni). Stupac `unit` u ovoj arhivi nikad ne sadrži LIM ni RINF "
           "(KOM/KG), pa provjera stupca zasad ništa ne mijenja.", "",
           "Broj grupa po obliku, sada (prije); vrijednost grupe je ona s najviše proizvoda:", "",
           md_table(["namirnica", *forms], count_rows)]
    for form in ("konzerva", "suho", "smrznuto"):
        sample = con.execute(f"""SELECT staple, grp, name, pack, CASE WHEN heur THEN 'heuristika' ELSE 'naziv' END
                                 FROM ({groups}) WHERE oblik = ? ORDER BY random() LIMIT 20""", [form]).fetchall()
        out += ["", f"20 nasumičnih grupa: **{form}**", "",
                md_table(["namirnica", "grupa", "naziv", "g", "izvor"], sample)]
    out += ["", "Zapažanja:",
            "- Većina preostalih `nepoznato` su konzerve bez oznake u nazivu („GRAH ZVIJEZDA 420 g“, „GRAŠAK 400 g "
            "ZVIJEZDA“, „KUKURUZ ŠEĆERAC 340g“). Dodatni signal mogao bi biti tipična gramatura limenke "
            "(212/340/400/425 g) uz marku konzervi, ali to nije dio zadane heuristike.",
            "- Krivi pogoci u uzorku (gotova jela): „GRAH S KOB.SMRZ.“ („KOB.“ nije `kobasic`) i „SIPA SA SLANUTKOM SMRZ.“; "
            "nisu ispravljeni u ovom koraku."]
    return "\n".join(out)


def section_api(con) -> str:
    return "\n".join([
        "## 12. cijene.dev bez API ključa", "",
        "Provjereno 2026-10-20 (curl, bez zaglavlja `Authorization`):", "",
        md_table(["zahtjev", "HTTP", "napomena"], [
            ("GET https://api.cijene.dev/v0/list", 200, "JSON s popisom arhiva (~70 kB)"),
            ("HEAD https://api.cijene.dev/v0/archive/2026-10-19.zip", 200, "content-length 128.905.233"),
            ("GET …/2026-10-19.zip, Range: bytes=0-1023", 206, "application/zip"),
            ("HEAD https://api.cijene.dev/v0/archive/2026-10-20.zip", 200, "objavljena u 14:26"),
        ]), "",
        "Ključ nije potreban, pa `update.py` nije mijenjan; zapis je u SCHEMA.md (Dnevno ažuriranje).",
    ])


def section_found(con) -> str:
    return "\n".join([
        "## Otkriveno usput (nije ispravljano u Koraku 2C)", "",
        "Košarica `data/recipes/test_bolonjez.json` u Osijeku (Konzum) bira tri kriva proizvoda. Uzrok je stariji "
        "od ovog koraka: grupa (EAN) ulazi u namirnicu ako joj **jedan** naziv odgovara, a zatim ulaze svi "
        "proizvodi grupe.", "",
        "- **mljeveno meso → „PUREĆE MLJEVENO MESO 500g VINDIJA“**: zadano je `vrsta=mijesano`, a naziv istog EAN-a "
        "u drugom lancu nema vrstu (pa se računa kao miješano), pa cijela grupa prolazi.",
        "- **maslinovo ulje → „KUPUS KIS MASL ULJE ČEŠNJAK 250g“**: `must_match` „masl ulje“ pogađa kiseli kupus "
        "u maslinovom ulju; nedostaje `kupus`/`kis` u `must_not_match`.",
        "- **parmezan → „PROIZ BILJ BAZ OKUS PARMEZ RIB 100g“** (biljni nadomjestak): ulazi preko istog EAN-a kao "
        "naziv koji odgovara parmezanu.",
        "- `_defaults.must_not_match` sadrži `felix`, a Felix je i marka kečapa i kiselih krastavaca: 6 proizvoda "
        "kečapa je isključeno.",
        "- „PERŠIN KOR LIS 250 gVOĆARNA“: gramatura bez razmaka iza jedinice se ne čita.",
    ])


SECTIONS = [section_chicken, section_onion, section_food, section_eggs, section_variants, section_kakao,
            section_salt, section_milk, section_parsley, section_units, section_sachets,
            section_forms, section_api, section_found]


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    parts = [f"# Jutarnji pregled: Korak 2C (arhiva {date.isoformat()})", "",
             "Izvještaj generira `scripts/morning_review.py` nad izgrađenom bazom. Točke 4 i 5 su na vrhu jer "
             "čekaju potvrdu. Uz njih treba pogledati i vrijednosti označene kao prijedlog:", "",
             "- **4.** pileća prsa „Jeli“ privremeno isključena; donja granica 5 €/kg odbacuje stvarna svježa prsa po 4,69 €",
             "- **5.** luk: nazivi s bojom, mapiranje nije mijenjano",
             "- **1.** jaja: `plausible_per_unit` [0,19; 0,47] (5.–95. percentil); bio jaja su djelomično iznad",
             "- **9.** mjere i gustoće (sve procjene)",
             "- **10.** granice po vrećici za kvasac, prašak i vanilin šećer",
             "- **0.** `data/category_map.yaml` (1.334 kategorije, ručno ispravljiva) i 20 sumnjivih „hrana“ proizvoda", ""]
    parts += [f(con) + "\n" for f in SECTIONS]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT}: {len(SECTIONS)} odjeljaka")


if __name__ == "__main__":
    main()
