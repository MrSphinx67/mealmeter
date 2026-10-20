"""Izvještaj za jutarnji pregled (Korak 2C): docs/MORNING_REVIEW.md.

Svaka točka ima svoju funkciju koja vraća Markdown; skripta ih izvodi redom nad izgrađenom bazom.

Upotreba: python scripts/morning_review.py [db_path]   (zadano: data/mealmeter.duckdb)
"""

import sys
from pathlib import Path

import duckdb

from mealmeter.food import food_report

OUT = Path("docs/MORNING_REVIEW.md")


def md_table(headers: list[str], rows) -> str:
    def cell(v):
        if v is None:
            return ""
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


SECTIONS = [section_food]


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
