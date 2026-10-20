"""Izvještaj za jutarnji pregled (Korak 2C): docs/MORNING_REVIEW.md.

Svaka točka ima svoju funkciju koja vraća Markdown; skripta ih izvodi redom nad izgrađenom bazom.

Upotreba: python scripts/morning_review.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import sys
from decimal import Decimal
from pathlib import Path

import duckdb

from mealmeter.food import food_report
from mealmeter.staples import STAPLE_PPU_SQL

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
        return str(v).replace("|", "\\|")
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


SECTIONS = [section_food, section_eggs]


def main() -> None:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "data/mealmeter.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    date = con.execute("SELECT max(date) FROM clean.prices").fetchone()[0]
    parts = [f"# Jutarnji pregled: Korak 2C (arhiva {date.isoformat()})", "",
             "Izvještaj generira `scripts/morning_review.py`. Točke 4 i 5 čekaju potvrdu vlasnika.", ""]
    parts += [f(con) + "\n" for f in SECTIONS]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"{OUT}: {len(SECTIONS)} odjeljaka")


if __name__ == "__main__":
    main()
