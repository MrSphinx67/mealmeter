"""Smoke test Koraka 4B: scenariji kroz MCP klijent u procesu nad stvarnom bazom; sažeci u docs/smoke_4b.md.

Upotreba: python scripts/smoke_4b.py [db_path]   (zadano: data/mealmeter.duckdb)
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
DB = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data" / "mealmeter.duckdb")
OUT = ROOT / "docs" / "smoke_4b.md"
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
    ("Nepoznate namirnice, Osijek", None, "plan_basket",
     {"ingredients": [{"name": "šafran", "amount": 1, "unit": "g"},
                      {"name": "tahini", "amount": 200, "unit": "g", "free_text": True},
                      {"name": "zmajevo voće sušeno", "amount": 100, "unit": "g", "free_text": True},
                      {"name": "kikiriki maslac", "amount": 200, "unit": "g", "free_text": True}],
      "city": "Osijek"}),
]


def eur(x) -> str:
    return "-" if x is None else f"{x:.2f}".replace(".", ",")


def store_line(s: dict) -> str:
    where = f"{s['chain']}, {s['address'] or 'nacionalno'}"
    if s.get("n_stores", 1) > 1:
        where += f" (+{s['n_stores'] - 1} istog lanca: {'; '.join(s['addresses'][1:])})"
    return (f"{where} · {s['n_matched']}/{s['n_ingredients']} · za kupiti {eur(s['total_to_buy'])} €, "
            f"utrošeno {eur(s['total_used'])} € · cjenik {s['date_hr']}" + (f", star {s['stale_days']} d" if s["stale_days"] else ""))


def summarize(title: str, size: int, out: dict) -> list[str]:
    lines = [f"## {title}", "", f"Odgovor: {size} B. {out.get('summary_hr', '')} Cjenik: {out.get('date_hr') or '-'}"]
    best = out.get("best_store")
    if best:
        lines += ["", f"**Najbolja**: {store_line(best)}", "",
                  "| sastojak | proizvod | pakiranje | kom | cijena pak. | utrošak | napomena |", "|---|---|---|---|---|---|---|"]
        for it in best["items"]:
            note = ", ".join(filter(None, [
                "imam" if it["have"] else "", it["match_quality"] if it["match_quality"] in ("weak", "free_text") else "",
                "korisnik" if it.get("user_provided") else "", ",".join(it["flags"])]))
            lines.append(f"| {it['ingredient']} | {it['name']} | {it['pack_size'] or '-'} | {it['n_packs'] or '-'} | "
                         f"{eur(it['cost_pack'])} | {eur(it['cost_used'])} | {note} |")
        alts = [(it["ingredient"], a) for it in best["items"] for a in it.get("alternatives", [])]
        if alts:
            lines += ["", "Alternative: " + "; ".join(
                f"{ing} → {a['name']} {eur(a['cost_pack'])} € ({'+' if a['delta_eur'] >= 0 else ''}{eur(a['delta_eur'])}, "
                f"{'jeftinije' if a['cheaper'] else 'nije jeftinije'})" for ing, a in alts[:8])]
    others = [s for s in out.get("stores", []) if s is not best and s != best]
    if others:
        lines += ["", "Ostale: " + " | ".join(store_line(s) for s in others)]
    for key, label in (("ambiguous", "Pitanje"), ("unmatched", "Nije pronađeno")):
        for a in out.get(key, []):
            if key == "ambiguous":
                lines += ["", f"{label}: {a['name']}: {a['ambiguity']['question']} cijene po obliku: {a['ambiguity']['prices']}"]
            else:
                lines += ["", f"{label}: {a['name']}: {a['reason']}; prijedlozi: {', '.join(a.get('suggestions') or []) or '-'}"]
    if out.get("warnings"):
        lines += ["", "Upozorenja: " + " · ".join(dict.fromkeys(out["warnings"]))]
    return lines + [""]


async def run() -> tuple[list[str], list[list]]:
    lines = [f"# Smoke test Korak 4B ({DB})", "",
             "Scenariji kroz MCP klijent u procesu (`scripts/smoke_4b.py`); sažeti odgovori plan_basket.", ""]
    shelf = []
    async with Client(srv.create_server(db_path=DB)) as c:
        for title, recipe, tool, args in SCENARIOS:
            r = await c.call_tool(tool, args)
            text = r.content[0].text
            out = json.loads(text)
            if r.is_error:
                lines += [f"## {title}", "", f"GREŠKA: {out.get('error')}", ""]
                continue
            lines += summarize(title, len(text.encode("utf-8")), out)
            best = out.get("best_store")
            if recipe and best and not args.get("price_overrides") and not args.get("already_have"):
                for it in best["items"]:
                    shelf.append([recipe, f"{best['chain']}, {best['address'] or 'nacionalno'}", it["ingredient"],
                                  it["name"], eur(it["cost_pack"] / (it["n_packs"] or 1)), "", "", ""])
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
