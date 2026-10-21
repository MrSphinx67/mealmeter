"""Smoke test (Korak 4B, 4C): scenariji kroz MCP klijent u procesu nad stvarnom bazom; sažeci u docs/.

Upotreba: python scripts/smoke_4b.py [db_path] [--out docs/smoke_4c.md] [--set 5b]   (zadano:
data/mealmeter.duckdb, docs/smoke_4b.md; --set 5b: palačinke, bolonjez i varivo od graška u Osijeku, Zagrebu i
Slavonskom Brodu uz "imam sol, papar, ulje"). Svaki scenarij ide sažeto (zadani odgovor) i s detail=true, radi veličine odgovora.
Uz to stvara data/eval/shelf_check.csv (ako ne postoji): stavke najboljih trgovina za provjeru na polici.
"""

import asyncio
import csv
import json
import sys
from pathlib import Path

from mcp import Client

from mealmeter import server as srv

ROOT = Path(__file__).resolve().parents[1]
_args = sys.argv[1:]
OUT = ROOT / (_args.pop(_args.index("--out") + 1) if "--out" in _args else "docs/smoke_4b.md")
SET = _args.pop(_args.index("--set") + 1) if "--set" in _args else "4b"
_args = [a for a in _args if a not in ("--out", "--set")]
DB = _args[0] if _args else str(ROOT / "data" / "mealmeter.duckdb")
SHELF = ROOT / "data" / "eval" / "shelf_check.csv"
SHELF_HEADER = ["recept", "trgovina", "sastojak", "alat_proizvod", "alat_cijena", "polica_proizvod", "polica_cijena",
                "napomena"]

PALACINKE = [  # 4 osobe; žlice i prstohvat već pretvoreni u g/ml
    {"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
    {"name": "jaja", "amount": 3, "unit": "kom"}, {"name": "šećer", "amount": 15, "unit": "g"},
    {"name": "sol", "amount": 1, "unit": "g"}, {"name": "ulje", "amount": 30, "unit": "ml"},
    {"name": "vanilin šećer", "amount": 1, "unit": "kom"},
]
BOLONJEZ = [
    {"name": "špageti", "amount": 400, "unit": "g"}, {"name": "mljeveno meso", "amount": 500, "unit": "g"},
    {"name": "rajčica", "amount": 700, "unit": "g"}, {"name": "luk", "amount": 1, "unit": "kom"},
    {"name": "maslinovo ulje", "amount": 30, "unit": "ml"}, {"name": "parmezan", "amount": 40, "unit": "g"},
    {"name": "sol", "amount": 5, "unit": "g"},
]
SCENARIOS = [
    ("Palačinke, Osijek", "palacinke", "plan_basket", {"ingredients": PALACINKE, "city": "Osijek"}),
    ("Palačinke, Konzum Osijek, \"imam sol i ulje\"", "palacinke", "plan_basket",
     {"ingredients": PALACINKE, "city": "Osijek", "store": {"chain": "konzum", "address_contains": ""},
      "already_have": ["sol", "ulje"]}),
    ("Palačinke, Osijek, stvarna cijena brašna 1,20 €", "palacinke", "plan_basket",
     {"ingredients": PALACINKE, "city": "Osijek", "price_overrides": [{"name": "brašno", "cost_pack": 1.20}]}),
    ("Špageti bolonjez, Zagreb", "bolonjez", "plan_basket", {"ingredients": BOLONJEZ, "city": "Zagreb"}),
    ("Grah bez oblika, Osijek", None, "plan_basket",
     {"ingredients": [{"name": "grah", "amount": 500, "unit": "g"}], "city": "Osijek"}),
    ("Krumpir 1 kg, Osijek", None, "plan_basket",
     {"ingredients": [{"name": "krumpir", "amount": 1000, "unit": "g"}], "city": "Osijek"}),
    ("Palačinke s nutellom 300 g (free_text), Osijek", "palacinke_nutella", "plan_basket",
     {"ingredients": PALACINKE + [{"name": "nutella", "amount": 300, "unit": "g", "free_text": True}],
      "city": "Osijek"}),
    ("Palačinke i grah bez oblika, Osijek", None, "plan_basket",
     {"ingredients": PALACINKE + [{"name": "grah", "amount": 500, "unit": "g"}], "city": "Osijek"}),
    ("Nepoznate namirnice, Osijek", None, "plan_basket",
     {"ingredients": [{"name": "šafran", "amount": 1, "unit": "g"},
                      {"name": "tahini", "amount": 200, "unit": "g", "free_text": True},
                      {"name": "zmajevo voće sušeno", "amount": 100, "unit": "g", "free_text": True},
                      {"name": "kikiriki maslac", "amount": 200, "unit": "g", "free_text": True}],
      "city": "Osijek"}),
]


# Korak 5B: tri recepta u tri grada; bolonjez bez količine parmezana i soli (pretpostavke)
BOLONJEZ_5B = [
    {"name": "špageti", "amount": 400, "unit": "g"}, {"name": "mljeveno meso", "amount": 500, "unit": "g"},
    {"name": "rajčica", "amount": 700, "unit": "g", "form": "pasirana"}, {"name": "luk", "amount": 1, "unit": "kom"},
    {"name": "maslinovo ulje", "amount": 30, "unit": "ml"}, {"name": "parmezan"}, {"name": "sol"},
    {"name": "lovorov list", "amount": 2, "unit": "list"}, {"name": "origano"},
]
VARIVO = [
    {"name": "grašak", "amount": 800, "unit": "g", "form": "smrznuto"}, {"name": "luk", "amount": 1, "unit": "kom"},
    {"name": "mrkva", "amount": 2, "unit": "kom"}, {"name": "krumpir", "amount": 2, "unit": "kom"},
    {"name": "brašno glatko", "amount": 20, "unit": "g"}, {"name": "mljevena paprika", "amount": 5, "unit": "g"},
    {"name": "dimljena kobasica", "amount": 400, "unit": "g"}, {"name": "ulje", "amount": 30, "unit": "ml"},
    {"name": "sol", "amount": 5, "unit": "g"}, {"name": "papar", "amount": 1, "unit": "g"},
]
HAVE = ["sol", "papar", "ulje"]
SCENARIOS_5B = [
    (f"{title}, {city}", recipe, "plan_basket", {"ingredients": ing, "city": city, "already_have": HAVE})
    for city in ("Osijek", "Zagreb", "Slavonski Brod")
    for title, recipe, ing in (("Palačinke", "palacinke", PALACINKE), ("Bolonjez", "bolonjez", BOLONJEZ_5B),
                               ("Varivo od graška", "varivo", VARIVO))
] + [("Varivo od graška bez oblika graška, Slavonski Brod", None, "plan_basket",
      {"ingredients": [{"name": "grašak", "amount": 800, "unit": "g"}] + VARIVO[1:], "city": "Slavonski Brod",
       "already_have": HAVE})]
if SET == "5b":
    SCENARIOS = SCENARIOS_5B


def eur(x) -> str:
    return "-" if x is None else f"{x:.2f}".replace(".", ",")


def store_line(s: dict) -> str:
    if "addresses" in s and "n_stores_city" in s:  # redak usporedbe (comparison)
        where = f"{s['chain']} ({s['n_stores_city']} trg.; {'; '.join(s['addresses']) or 'nacionalno'})"
    else:
        where = f"{s['chain']}, {s.get('address') or 'nacionalno'}"
        if (s.get("n_stores") or 1) > 1:
            where += f" (+{s['n_stores'] - 1} istog lanca)"
    extra = f", iz zalihe {eur(s['from_stock_value'])} €" if s.get("from_stock_value") else ""
    return (f"{where}: za kupiti {eur(s['total_to_buy'])} €, utrošeno {eur(s['total_used'])} €{extra}, "
            f"{s['n_matched']}/{s.get('n_ingredients', '?')}")


def item_line(it: dict) -> str:
    extra = [x for x in ("imam" if it.get("have") else "", it.get("match_quality") or "",
                         "korisnik" if it.get("user_provided") else "", ",".join(it.get("flags") or []),
                         (f"zamjena za {it['substitution']['requested']}"
                          + (f": {it['substitution']['note']}" if it['substitution'].get('note') else ""))
                         if it.get("substitution") else "",
                         "POTVRDA" if it.get("needs_confirmation") else "",
                         "; ".join(it.get("notes") or [])) if x]
    line = (f"{it['ingredient']}: {it['name']} ({it['pack_size'] or '-'}"
            f"{' x' + str(it['n_packs']) if (it.get('n_packs') or 1) > 1 else ''}) {eur(it['cost_pack'])} / "
            f"{eur(it['cost_used'])} €" + (f" [{'; '.join(extra)}]" if extra else ""))
    alts = [f"{a['name']} {eur(a['cost_pack'])} € ({eur(a['delta_eur'])}"
            + (f", {a['note']}" if a.get("note") else "") + (f", {a['chain']}" if a.get("other_store") else "")
            + (f"; {a['size_note']}" if a.get("size_note") else "") + ")"
            for a in it.get("alternatives") or []]
    if alts:
        line += " — alternative: " + "; ".join(alts)
    if it.get("candidates"):
        line += " — kandidati: " + "; ".join(f"{c['name']} {eur(c['cost_pack'])} €" for c in it["candidates"])
    return line


def summarize(title: str, size: int, detail_size: int, out: dict) -> list[str]:
    lines = [f"## {title}", "", f"Odgovor {size} B (detail=true {detail_size} B). {out.get('summary_hr', '')} "
             f"Cjenik: {out.get('date_hr') or '-'}"]
    best = out.get("best_store")
    if best:
        lines += ["", f"Najbolja: {store_line(best)}", ""] + [f"- {item_line(it)}" for it in best["items"]]
    if out.get("comparison"):
        lines += ["", "Usporedba: " + " | ".join(store_line(s) for s in out["comparison"])]
    if out.get("more_chains"):
        lines += ["", "Još lanaca s >= 80 % sastojaka: " + ", ".join(
            f"{m['chain']} {eur(m['total_to_buy'])} € ({m['n_matched']})" for m in out["more_chains"])]
    if out.get("incomplete"):
        lines += ["", "Nepotpuni: " + "; ".join(f"{i['chain']} ({i['note']})" for i in out["incomplete"])]
    if out.get("assumptions"):
        lines += ["", "Pretpostavke: " + "; ".join(f"{a['ingredient']}: {a['text']}" for a in out["assumptions"])]
    for q in out.get("ask_user") or []:
        lines += ["", f"Pitanje: {q['question']} " + ", ".join(
            f"{o['form']} {o.get('amount', '?'):g} {o.get('unit', '')} {eur(o['price_eur'])} €" for o in q["options"])
            + f" ({q['options'][0]['price_note']})"]
    for u in out.get("unmatched") or []:
        lines += ["", f"Nije pronađeno: {u['name']}: {u['reason']}; prijedlozi: {', '.join(u.get('suggestions') or []) or '-'}"]
    if out.get("warnings"):
        lines += ["", "Upozorenja: " + " · ".join(dict.fromkeys(out["warnings"]))]
    return lines + [""]


async def run() -> tuple[list[str], list[list]]:
    lines = [f"# Smoke test ({OUT.stem}, {DB})", "",
             "Scenariji kroz MCP klijent u procesu (`scripts/smoke_4b.py`). Stavka: proizvod (pakiranje) cijena "
             "pakiranja / utrošak; alternative su jeftinije (razlika u €).", ""]
    sizes = []
    shelf = []
    async with Client(srv.create_server(db_path=DB)) as c:
        for title, recipe, tool, args in SCENARIOS:
            r = await c.call_tool(tool, args)
            text = r.content[0].text
            out = json.loads(text)
            if r.is_error:
                lines += [f"## {title}", "", f"GREŠKA: {out.get('error')}", ""]
                continue
            full = await c.call_tool(tool, {**args, "detail": True})
            size, detail_size = len(text.encode("utf-8")), len(full.content[0].text.encode("utf-8"))
            sizes.append((title, len(args["ingredients"]), size, detail_size))
            lines += summarize(title, size, detail_size, out)
            best = out.get("best_store")
            if recipe and best and not args.get("price_overrides") and not args.get("already_have"):
                for it in best["items"]:
                    shelf.append([recipe, f"{best['chain']}, {best['address'] or 'nacionalno'}", it["ingredient"],
                                  it["name"], eur(it["cost_pack"] / (it["n_packs"] or 1)), "", "", ""])
    lines += ["## Veličine odgovora", "", "| scenarij | sastojaka | sažeto (B) | detail (B) |", "|---|---|---|---|"]
    lines += [f"| {t} | {n} | {a} | {b} |" for t, n, a, b in sizes]
    return lines, shelf


def main() -> None:
    lines, shelf = asyncio.run(run())
    OUT.write_text("\n".join(lines), encoding="utf-8")
    SHELF.parent.mkdir(parents=True, exist_ok=True)
    note = "postoji, nije dirano"
    if not SHELF.exists():  # ne prepisuje provjere upisane na polici
        with SHELF.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(SHELF_HEADER)
            w.writerows(shelf)
        note = f"{len(shelf)} stavki za provjeru"
    print(f"{OUT}: {len(lines)} redaka; {SHELF}: {note}")


if __name__ == "__main__":
    main()
