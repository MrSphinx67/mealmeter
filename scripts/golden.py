"""Zlatni izlazi (Korak 5P): 22 scenarija alata nad stvarnom bazom, spremljeni u tests/golden/*.json.

    python scripts/golden.py --write [--db data/mealmeter.duckdb]   # spremi izlaze (prije promjena)
    python scripts/golden.py --check [--db data/compact.duckdb]     # usporedi; ispiše razlike po scenariju

plan_basket se poziva s detail=true (sva polja). Izlazi ovise o učitanom cjeniku, pa se zapisuju uz datum baze;
nakon dnevnog ažuriranja treba ih ponovno zapisati (--write).
"""

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden"

PALACINKE = [{"name": "brašno glatko", "amount": 250, "unit": "g"}, {"name": "mlijeko", "amount": 500, "unit": "ml"},
             {"name": "jaja", "amount": 3, "unit": "kom"}, {"name": "šećer", "amount": 15, "unit": "g"},
             {"name": "sol", "amount": 1, "unit": "g"}, {"name": "ulje", "amount": 30, "unit": "ml"},
             {"name": "vanilin šećer", "amount": 1, "unit": "kom"}]
BOLONJEZ = [{"name": "špageti", "amount": 400, "unit": "g"}, {"name": "mljeveno meso", "amount": 500, "unit": "g"},
            {"name": "rajčica", "amount": 700, "unit": "g", "form": "pasirana"}, {"name": "luk", "amount": 1, "unit": "kom"},
            {"name": "maslinovo ulje", "amount": 30, "unit": "ml"}, {"name": "parmezan"}, {"name": "sol"}]
VARIVO = [{"name": "grašak", "amount": 800, "unit": "g", "form": "smrznuto"}, {"name": "luk", "amount": 1, "unit": "kom"},
          {"name": "mrkva", "amount": 2, "unit": "kom"}, {"name": "krumpir", "amount": 2, "unit": "kom"},
          {"name": "brašno glatko", "amount": 20, "unit": "g"}, {"name": "mljevena paprika", "amount": 5, "unit": "g"},
          {"name": "dimljena kobasica", "amount": 400, "unit": "g"}, {"name": "ulje", "amount": 30, "unit": "ml"},
          {"name": "sol", "amount": 5, "unit": "g"}, {"name": "papar", "amount": 1, "unit": "g"}]

SCENARIOS = {
    # find_products
    "find_brasno_osijek": ("find_products", {"ingredient": "brašno", "city": "Osijek"}),
    "find_mlijeko_zagreb": ("find_products", {"ingredient": "mlijeko", "city": "Zagreb", "limit": 15}),
    "find_jaja_split": ("find_products", {"ingredient": "jaja", "city": "Split"}),
    "find_query_nutella": ("find_products", {"query": "nutella", "city": "Osijek"}),
    "find_papar_zrno": ("find_products", {"ingredient": "papar", "attributes": {"oblik": "zrno"}, "city": "Rijeka"}),
    "find_kobasica_osijek": ("find_products", {"ingredient": "kobasica", "city": "Osijek", "include_weak": True}),
    # get_prices
    "prices_ean_osijek": ("get_prices", {"product_id": "3850104223624", "city": "Osijek"}),
    "prices_class_jaja_m": ("get_prices", {"product_id": "jaja:m", "city": "Zagreb"}),
    "prices_lidl_brasno": ("get_prices", {"product_id": "lidl:0002225", "city": "Osijek"}),
    # plan_basket
    "basket_palacinke_osijek": ("plan_basket", {"ingredients": PALACINKE, "city": "Osijek"}),
    "basket_bolonjez_zagreb": ("plan_basket", {"ingredients": BOLONJEZ, "city": "Zagreb"}),
    "basket_varivo_slavonski_brod": ("plan_basket", {"ingredients": VARIVO, "city": "Slavonski Brod"}),
    "basket_store_konzum_osijek": ("plan_basket", {"ingredients": PALACINKE, "city": "Osijek",
                                                   "store": {"chain": "konzum", "address_contains": ""}}),
    "basket_already_have_zagreb": ("plan_basket", {"ingredients": BOLONJEZ, "city": "Zagreb",
                                                   "already_have": ["sol", "papar", "ulje"]}),
    "basket_price_overrides": ("plan_basket", {"ingredients": PALACINKE, "city": "Osijek",
                                               "price_overrides": [{"name": "brašno", "cost_pack": 1.2}]}),
    "basket_free_text_tahini": ("plan_basket", {"ingredients": PALACINKE[:3] + [
        {"name": "tahini", "amount": 200, "unit": "g", "free_text": True}], "city": "Osijek"}),
    "basket_grasak_bez_oblika": ("plan_basket", {"ingredients": [{"name": "grašak", "amount": 800, "unit": "g"}],
                                                 "city": "Osijek"}),
    "basket_krumpir_rijeka": ("plan_basket", {"ingredients": [{"name": "krumpir", "amount": 1000, "unit": "g"}],
                                              "city": "Rijeka"}),
    "basket_nepoznato": ("plan_basket", {"ingredients": [{"name": "šafran", "amount": 1, "unit": "g"},
                                                         {"name": "zmajevo voće", "amount": 100, "unit": "g",
                                                          "free_text": True}], "city": "Osijek"}),
    "basket_lidl_varivo_zagreb": ("plan_basket", {"ingredients": VARIVO, "city": "Zagreb",
                                                  "store": {"chain": "lidl", "address_contains": ""}}),
    # Korak 5V5: stvarni test na Vercelu (Lorenco se pojavio kao najjeftiniji)
    "basket_palacinke_nutella_osijek": ("plan_basket", {"ingredients": PALACINKE[:3] + [
        {"name": "šećer", "amount": 15, "unit": "g"}, {"name": "sol", "amount": 1, "unit": "g"},
        {"name": "ulje", "amount": 30, "unit": "ml"}, {"name": "nutella", "amount": 300, "unit": "g"}],
        "city": "Osijek", "already_have": ["sol", "ulje", "šećer"]}),
    # Korak 6.0: suhi grah 500/1000 g bez oznake oblika (Lidl, Eurospin, NTL, Roto su bili "nedostaje")
    "basket_grah_suho_osijek": ("plan_basket", {"ingredients": [{"name": "grah", "amount": 500, "unit": "g",
                                                                 "form": "suho"}], "city": "Osijek"}),
}
# lanci koji nikad ne smiju biti u izlazu plan_basketa: nepouzdani podaci (Lorenco) i veleprodaja (Metro)
EXCLUDED_CHAINS = ("lorenco", "metro")


def run(db: str | None) -> dict:
    from mealmeter import server as srv

    srv.create_server(db_path=db)
    out = {}
    for name, (tool, args) in SCENARIOS.items():
        fn = getattr(srv, tool)
        res = fn(**args, detail=True) if tool == "plan_basket" else fn(**args)
        out[name] = json.loads(srv._dumps(res))
    return out


def diff(a, b, path="", out=None, limit=8):
    """Putanje na kojima se a i b razlikuju (najviše `limit`)."""
    out = [] if out is None else out
    if len(out) >= limit:
        return out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}.{k}: {'samo novo' if k not in a else 'samo zlatno'}")
            else:
                diff(a[k], b[k], f"{path}.{k}", out, limit)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path}: duljina {len(a)} -> {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, f"{path}[{i}]", out, limit)
    elif a != b:
        out.append(f"{path}: {json.dumps(a, ensure_ascii=False)[:60]} -> {json.dumps(b, ensure_ascii=False)[:60]}")
    return out


def check(db: str | None, verbose: bool = True) -> dict[str, list[str]]:
    got = run(db)
    result = {}
    for name in SCENARIOS:
        gold = json.loads((GOLDEN / f"{name}.json").read_text(encoding="utf-8"))
        result[name] = diff(gold, got[name])
        if verbose:
            print(f"{'OK ' if not result[name] else 'RAZLIKA'} {name}" + "".join(f"\n    {d}" for d in result[name]))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--db", default=None)
    args = ap.parse_args()
    t = time.time()
    if args.write:
        GOLDEN.mkdir(parents=True, exist_ok=True)
        for name, res in run(args.db).items():
            (GOLDEN / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                                 encoding="utf-8")
        print(f"zapisano {len(SCENARIOS)} scenarija u {GOLDEN} ({time.time() - t:.0f} s)")
        return 0
    bad = sum(1 for d in check(args.db).values() if d)
    print(f"{len(SCENARIOS) - bad}/{len(SCENARIOS)} jednako ({time.time() - t:.0f} s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
