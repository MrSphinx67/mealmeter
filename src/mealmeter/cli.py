"""Mali CLI za isprobavanje pretrage.

    python -m mealmeter.cli find "brašno glatko" --city Osijek
    python -m mealmeter.cli find --ingredient brasno --attr tip=glatko --city Osijek
    python -m mealmeter.cli prices 3850104223624 --city Osijek
"""

import argparse
import json
import sys

from mealmeter import search


def _fmt_money(v) -> str:
    return "" if v is None else f"{v:.2f}".replace(".", ",")


def _fmt_range(lo, hi) -> str:
    if lo is None:
        return "-"
    return _fmt_money(lo) if lo == hi else f"{_fmt_money(lo)}–{_fmt_money(hi)}"


def _fmt_conf(r: dict) -> str:
    """unit_confidence/pack_source, npr. "high/name", "low/unit_price" ili "-"."""
    if not r.get("unit_confidence"):
        return "-"
    return f"{r['unit_confidence']}/{r['pack_source']}"


def _table(rows: list[list[str]], headers: list[str]) -> str:
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = lambda r: "  ".join(str(x).ljust(w) for x, w in zip(r, widths))  # noqa: E731
    return "\n".join([line(headers), line(["-" * w for w in widths]), *map(line, rows)])


def cmd_find(args) -> None:
    attrs = dict(a.split("=", 1) for a in args.attr) if args.attr else None
    try:
        res = search.find_products(
            args.query, city=args.city, limit=args.limit, ingredient=args.ingredient, attributes=attrs
        )
    except ValueError as e:
        sys.exit(str(e))
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if args.city and search.resolve_city(args.city) is None:
        print(f"Napomena: nema lokalnih trgovina za grad '{args.city}', prikazane su samo nacionalne cijene.\n")
    if not res:
        print("Nema rezultata.")
        return
    rows = [
        [
            r["id"],
            r["name"][:48],
            (r["brand"] or "")[:18],
            r["pack"] or "",
            _fmt_range(r["price_min"], r["price_max"]),
            _fmt_range(r["price_per_unit_min"], r["price_per_unit_max"])
            + (f" /{r['per_unit']}" if r["per_unit"] else ""),
            _fmt_conf(r),
            f"{r['n_chains']}{'*' if r.get('note') else ''}",
            r["n_stores"],
        ]
        for r in res
    ]
    headers = ["id", "naziv", "marka", "pakiranje", "cijena €", "€ po jedinici", "pouzdanost", "lanaca", "trgovina"]
    if res[0]["ingredient"]:
        headers.append("atributi")
        for row, r in zip(rows, res):
            row.append(", ".join(f"{k}={v}" for k, v in r["attributes"].items()))
        print(f"Namirnica: {res[0]['ingredient']}")
    print(f"Cijene na dan {res[0]['date_hr']}\n")
    print(_table(rows, headers))
    if any(r.get("note") for r in res):
        print(f"\n* uključuje nacionalnu cijenu. {search.NATIONAL_NOTE}")


def cmd_prices(args) -> None:
    try:
        res = search.get_prices(args.identifier, city=args.city, limit=args.limit)
    except ValueError as e:
        sys.exit(str(e))
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    if not res:
        print("Nema cijena.")
        return
    rows = [
        [
            r["chain"],
            (r["address"] or "(sve poslovnice)")[:36],
            r["city"] or "",
            _fmt_money(r["price_eff"]) + (" AKCIJA" if r["is_special"] else ""),
            (_fmt_money(r["price_per_unit"]) + f" /{r['per_unit']}") if r["per_unit"] else "-",
            _fmt_conf(r),
            r["scope"] + ("*" if r.get("note") else "") + (" (suspect)" if r["data_quality"] == "suspect" else ""),
            r["date_hr"],
        ]
        for r in res
    ]
    print(f"{res[0]['name']}  [{args.identifier}]\n")
    print(_table(rows, ["lanac", "adresa", "grad", "cijena €", "po jedinici", "pouzdanost", "scope", "datum"]))
    if any(r.get("note") for r in res):
        print(f"\n* {search.NATIONAL_NOTE}")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="mealmeter", description="Pretraga cijena u hrvatskim trgovinama")
    sub = ap.add_subparsers(required=True)

    f = sub.add_parser("find", help="pronađi proizvode po nazivu")
    f.add_argument("query", nargs="?", help="slobodan upit; sinonim namirnice (npr. 'mlijeko') koristi rječnik")
    f.add_argument("--ingredient", help="osnovna namirnica iz staples.yaml (npr. brasno)")
    f.add_argument("--attr", action="append", metavar="IME=VRIJEDNOST", help="atribut namirnice, npr. tip=glatko")
    f.add_argument("--city")
    f.add_argument("--limit", type=int, default=10)
    f.add_argument("--json", action="store_true")
    f.set_defaults(func=cmd_find)

    p = sub.add_parser("prices", help="cijene po trgovini za EAN ili lanac:product_id")
    p.add_argument("identifier")
    p.add_argument("--city")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_prices)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
