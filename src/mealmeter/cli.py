"""Mali CLI za isprobavanje pretrage.

    python -m mealmeter.cli find "brašno glatko" --city Osijek
    python -m mealmeter.cli find --ingredient brasno --attr tip=glatko --city Osijek
    python -m mealmeter.cli prices 3850104223624 --city Osijek
    python -m mealmeter.cli basket data/recipes/test_palacinke.json --city Osijek
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


def _food_kwargs(args) -> dict:
    return {"include_nonfood": args.include_nonfood, "include_alcohol": args.include_alcohol,
            "include_unverified": args.include_unverified, "include_wholesale": args.include_wholesale}


def _add_food_args(parser) -> None:
    parser.add_argument("--include-nonfood", action="store_true", help="i neprehrambeni proizvodi")
    parser.add_argument("--include-alcohol", action="store_true", help="i alkoholna pića")
    parser.add_argument("--include-unverified", action="store_true",
                        help="i proizvodi nepoznate skupine (oznaka (?) u nazivu)")
    parser.add_argument("--include-wholesale", action="store_true", help="i veleprodaja (Metro)")


def cmd_find(args) -> None:
    attrs = dict(a.split("=", 1) for a in args.attr) if args.attr else None
    try:
        res = search.find_products(
            args.query, city=args.city, limit=args.limit, ingredient=args.ingredient, attributes=attrs,
            **_food_kwargs(args),
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
            r["name"][:48] + (" (?)" if r.get("food_unverified") else ""),
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
        res = search.get_prices(args.identifier, city=args.city, limit=args.limit, **_food_kwargs(args))
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


def cmd_basket(args) -> None:
    from mealmeter.basket import plan_basket

    recipe = json.loads(open(args.recipe, encoding="utf-8").read())
    ingredients = recipe["ingredients"] if isinstance(recipe, dict) else recipe
    have = [h.strip() for h in (args.have or "").split(",") if h.strip()]
    res = plan_basket(ingredients, args.city, already_have=have)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        return
    title = recipe.get("name", args.recipe) if isinstance(recipe, dict) else args.recipe
    print(f"{title}  ·  {res['city']}" + (f"  ·  cijene na dan {res['date_hr']}" if res.get("date_hr") else ""))
    for w in res["warnings"]:
        print(f"  ! {w}")
    for u in res["unmatched"]:
        print(f"  ✗ {u['name']}: {u['reason']}")
    best = res["best_store"]
    if not best:
        print("\nNema trgovine s ovim sastojcima.")
        return
    print(f"\nNajbolja trgovina: {best['chain']}, {best['address'] or '(sve poslovnice)'}, {best['city'] or ''}"
          f"  ·  {best['n_matched']}/{best['n_ingredients']} sastojaka  ·  za kupiti {_fmt_money(best['total_to_buy'])} €"
          f"  ·  utrošeno {_fmt_money(best['total_used'])} €")
    if best["missing"]:
        print(f"  nedostaje: {', '.join(best['missing'])}")
    rows = [
        [
            it["ingredient"],
            it["name"][:42],
            f"{it['n_packs']} x {_fmt_money(it['price_eff'])}" if it["n_packs"] else "na vagu",
            _fmt_money(it["cost_pack"]) + (" (imam)" if it["have"] else ""),
            _fmt_money(it["cost_used"]),
            f"{it['unit_confidence']}/{it['pack_source']}",
            ", ".join(f"{k}={v}" for k, v in it["attributes"].items()),
            ", ".join([search_flag(f) for f in it["flags"]] + [n for n in it["notes"] if "zamjenjivo" in n]
                      + ([f"cijena od {it['date_hr']} ({it['stale_days']} d)"] if it.get("stale_days") else [])),
        ]
        for it in best["items"]
    ]
    print()
    print(_table(rows, ["sastojak", "proizvod", "pakiranja", "cijena €", "utrošeno €", "pouzdanost", "atributi",
                        "napomena"]))
    print("  za kupiti = cijela pakiranja bez onoga što već imaš (--have); utrošeno = razmjerni dio svih stavki")
    print()
    rows = [[s["chain"], (s["address"] or "(sve poslovnice)")[:34], f"{s['n_matched']}/{s['n_ingredients']}",
             _fmt_money(s["total_to_buy"]), s["scope"] + (" (suspect)" if s["data_quality"] == "suspect" else "")]
            for s in res["stores"][: args.top]]
    print(_table(rows, ["lanac", "adresa", "sastojaka", "za kupiti €", "scope"]))


def search_flag(flag: str) -> str:
    from mealmeter.basket import FLAG_TEXT

    return FLAG_TEXT.get(flag, flag)


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
    _add_food_args(f)
    f.set_defaults(func=cmd_find)

    p = sub.add_parser("prices", help="cijene po trgovini za EAN ili lanac:product_id")
    p.add_argument("identifier")
    p.add_argument("--city")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--json", action="store_true")
    _add_food_args(p)
    p.set_defaults(func=cmd_prices)

    b = sub.add_parser("basket", help="cijena recepta po trgovini (recept.json)")
    b.add_argument("recipe", help='JSON: {"name": ..., "ingredients": [{"name", "amount", "unit", "form"?}]}')
    b.add_argument("--city", required=True)
    b.add_argument("--top", type=int, default=8, help="koliko trgovina ispisati")
    b.add_argument("--have", help='namirnice koje već imaš, odvojene zarezom (npr. "sol,papar,ulje")')
    b.add_argument("--json", action="store_true")
    b.set_defaults(func=cmd_basket)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
