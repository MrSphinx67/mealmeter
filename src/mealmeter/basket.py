"""Košarica za recept: plan_basket(ingredients, city, mode="single_store")."""

import difflib
import math
from dataclasses import dataclass, field

import duckdb

from mealmeter.build import NATIONAL_NOTE
from mealmeter.normalize import date_hr, norm_text
from mealmeter.search import _candidates, connect, resolve_city
from mealmeter.staples import Staple, load_staples, resolve_ingredient

# jedinica u receptu -> (osnovna jedinica, faktor); "spoon" = približno (gustoća 1)
_UNIT_ALIASES = {
    "g": ("g", 1), "gr": ("g", 1), "gram": ("g", 1), "grama": ("g", 1), "dag": ("g", 10), "dkg": ("g", 10),
    "kg": ("g", 1000), "kila": ("g", 1000),
    "ml": ("ml", 1), "cl": ("ml", 10), "dl": ("ml", 100), "l": ("ml", 1000), "lit": ("ml", 1000), "litra": ("ml", 1000),
    "kom": ("kom", 1), "komad": ("kom", 1), "komada": ("kom", 1), "kos": ("kom", 1), "glavica": ("kom", 1),
    "rezanj": ("kom", 1), "rezanja": ("kom", 1), "cesanj": ("kom", 1), "cesnja": ("kom", 1),
    "vrecica": ("vrecica", 1), "vrecice": ("vrecica", 1), "paket": ("vrecica", 1), "paketic": ("vrecica", 1),
    "zlica": ("spoon", 15), "zlice": ("spoon", 15), "jusna zlica": ("spoon", 15),
    "zlicica": ("spoon", 5), "zlicice": ("spoon", 5), "cajna zlicica": ("spoon", 5),
    "prstohvat": ("spoon", 0.5),
}
FLAG_TEXT = {
    "clearance": "rasprodaja (SNIŽENJE)",
    "price_suspect": "cijena izvan granica",
    "pack_confidence_low": "nesigurna gramatura (višestruko pakiranje)",
    "chain_suspect": "lanac sa sumnjivim podacima",
}


class IngredientError(ValueError):
    """Sastojak se ne može povezati: razlog ide u `unmatched`."""


@dataclass
class Need:
    """Sastojak recepta preveden u namirnicu i količinu u njezinoj osnovnoj jedinici."""
    input: dict
    staple: Staple
    amount: float  # u `unit`
    unit: str  # g | ml | kom | vrecica
    attributes: dict = field(default_factory=dict)
    form: str | None = None
    assumed_form: bool = False
    warnings: list = field(default_factory=list)


def resolve_name(name: str) -> tuple[Staple, dict]:
    """Naziv sastojka -> (namirnica, atributi). Točan sinonim, ili sinonim + vrijednosti atributa
    ("glatko brašno" -> brasno, tip=glatko). Inače IngredientError."""
    if st := resolve_ingredient(name):
        # sinonim koji je i vrijednost atributa ("špageti" -> tjestenina, oblik=spageti)
        q = norm_text(name)
        hit = [(a, v) for a, vals in st.attributes.items() for v in vals if norm_text(v.replace("_", " ")) == q]
        return st, dict(hit[:1])
    words = (norm_text(name) or "").split()
    for st in load_staples().values():
        for syn in sorted(st.synonyms, key=len, reverse=True):
            syn_words = syn.split()
            for i in range(len(words) - len(syn_words) + 1):
                if words[i:i + len(syn_words)] != syn_words:
                    continue
                rest = words[:i] + words[i + len(syn_words):]
                attrs, ok = {}, True
                for w in rest:
                    hit = [(a, v) for a, vals in st.attributes.items() for v in vals if norm_text(v.replace("_", " ")) == w]
                    if len(hit) != 1:
                        ok = False
                        break
                    attrs[hit[0][0]] = hit[0][1]
                if ok:
                    return st, attrs
    raise IngredientError(f"nepoznata namirnica '{name}' (nema je u staples.yaml)")


def to_base(amount: float, unit: str, staple: Staple) -> tuple[float, str, list[str]]:
    """Količina iz recepta u osnovnu jedinicu namirnice: g, ml, kom ili vrecica."""
    if amount is None or amount <= 0:
        raise IngredientError("količina mora biti pozitivna")
    key = norm_text(unit or "") or ""
    if key not in _UNIT_ALIASES:
        raise IngredientError(f"nepoznata jedinica '{unit}'")
    base, factor = _UNIT_ALIASES[key]
    qty, warnings = amount * factor, []
    target = {"kg": "g", "l": "ml"}.get(staple.compare_unit, staple.compare_unit)  # g | ml | kom | vrecica
    if base == "spoon":
        warnings.append(f"{amount:g} {unit} ≈ {qty:g} {'ml' if target == 'ml' else 'g'} (približno)")
        base = "ml" if target == "ml" else "g"
    if base == target:
        return qty, target, warnings
    if {base, target} == {"g", "ml"}:
        warnings.append(f"{qty:g} {base} uzeto kao {qty:g} {target} (gustoća 1)")
        return qty, target, warnings
    if base == "kom" and target in ("g", "ml") and staple.piece_g:
        warnings.append(f"{qty:g} kom ≈ {qty * staple.piece_g:g} g (komad {staple.piece_g:g} g)")
        return qty * staple.piece_g, "g" if target == "g" else "ml", warnings
    if target == "kom" and base == "g" and staple.piece_g:
        warnings.append(f"{qty:g} g ≈ {qty / staple.piece_g:g} kom (komad {staple.piece_g:g} g)")
        return qty / staple.piece_g, "kom", warnings
    if target == "vrecica" and base in ("g", "kom"):
        if base == "kom":
            return qty, "vrecica", warnings
        warnings.append(f"{qty:g} g ≈ {qty / staple.sachet_g:g} vrećica od {staple.sachet_g:g} g")
        return qty / staple.sachet_g, "vrecica", warnings
    raise IngredientError(f"jedinica '{unit}' se ne može pretvoriti u {staple.compare_unit} za '{staple.name}'")


# --- odabir proizvoda u jednoj trgovini ------------------------------------------

def candidate_qty(row: dict, need_unit: str) -> tuple[float | None, list[str]]:
    """Količina u pakiranju u jedinici potrebe; za konzerve ocijeđena masa ako je poznata."""
    if need_unit in ("kom", "vrecica"):
        if row.get("n_units"):
            return row["n_units"], []
        if need_unit == "kom" and row.get("pack_unit") == "kom" and row.get("pack_amount"):
            return row["pack_amount"], []
        return None, []
    if row.get("assumed_g"):
        return row["assumed_g"], ["pretpostavljena masa pakiranja"]
    if row.get("drained_amount"):
        return row["drained_amount"], ["ocijeđena masa"]
    if row.get("pack_amount") and row.get("pack_unit") in ("g", "ml"):
        note = [] if row["pack_unit"] == need_unit else [f"{row['pack_unit']} uzeto kao {need_unit}"]
        return row["pack_amount"], note
    return None, []


def flags_of(row: dict) -> list[str]:
    out = []
    if row.get("clearance"):
        out.append("clearance")
    if row.get("price_suspect"):
        out.append("price_suspect")
    if row.get("pack_confidence") == "low":
        out.append("pack_confidence_low")
    if row.get("data_quality") == "suspect":
        out.append("chain_suspect")
    return out


def choose_product(rows: list[dict], need: float, need_unit: str, by_weight_unit: str | None,
                   loose: bool = True) -> dict | None:
    """Odabir proizvoda za količinu `need` (u `need_unit`) među kandidatima jedne trgovine.

    1. Kandidati bez zastavica (rasprodaja, cijena izvan granica, nesigurna gramatura, sumnjiv
       lanac); samo ako takvih nema, uzimaju se označeni.
    2. Najmanje pakiranje koje pokriva količinu (uz jednaku veličinu najjeftinije). Roba na vagu
       (cijena po kg/l, bez pakiranja: svježe voće/povrće ako je `loose`, inače samo promjenjiva
       težina) pokriva točno potrebnu količinu.
    3. Inače najjeftinije po jedinici, u potrebnom broju pakiranja.
    """
    options = []
    for r in rows:
        qty, notes = candidate_qty(r, need_unit)
        if qty and qty > 0:
            options.append({**r, "qty": qty, "notes": notes, "flags": flags_of(r), "by_weight": False})
        elif (by_weight_unit and r.get("price_per_unit") and r.get("per_unit") == by_weight_unit
              and (loose or r.get("variable_weight"))):
            options.append({**r, "qty": None, "notes": ["na vagu"], "flags": flags_of(r), "by_weight": True})
    if not options:
        return None
    clean = [o for o in options if not o["flags"]]
    pool = clean or options

    def per_unit_cost(o):
        return o["price_per_unit"] / 1000 if o["by_weight"] else o["price_eff"] / o["qty"]

    covering = [o for o in pool if o["by_weight"] or o["qty"] >= need]
    if covering:
        best = min(covering, key=lambda o: (need if o["by_weight"] else o["qty"], o["price_eff"] if not o["by_weight"]
                                            else o["price_per_unit"] * need / 1000))
    else:
        best = min(pool, key=per_unit_cost)
    if best["by_weight"]:
        n_packs, cost_pack = None, round(best["price_per_unit"] * need / 1000, 2)
        cost_used = cost_pack
    else:
        n_packs = max(1, math.ceil(need / best["qty"] - 1e-9))
        cost_pack = round(n_packs * best["price_eff"], 2)
        cost_used = round(best["price_eff"] / best["qty"] * need, 2)
    return {**best, "n_packs": n_packs, "cost_pack": cost_pack, "cost_used": cost_used,
            "fallback": not clean}


# --- plan_basket -------------------------------------------------------------------

def _rows_for(con, staple: Staple, attributes: dict, city: str) -> list[dict]:
    sql, params, _ = _candidates(staple, [], attributes, city, include_clearance=True)
    cur = con.execute(sql + " SELECT * FROM x", params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def _num(v):
    return float(v) if v is not None else None


def _prepare(con, need: Need, city: str) -> dict[tuple, list[dict]]:
    """Kandidati po trgovini (chain, store_id) za jedan sastojak (uz odabrani oblik)."""
    attrs = dict(need.attributes)
    if need.form and "oblik" in need.staple.attributes:
        attrs["oblik"] = need.form
    for a, v in need.staple.default_attributes.items():
        attrs.setdefault(a, v)
    by_store: dict[tuple, list[dict]] = {}
    for r in _rows_for(con, need.staple, attrs, city):
        for k in ("price_eff", "price_per_unit", "pack_amount", "drained_amount", "n_units", "assumed_g"):
            r[k] = _num(r.get(k))
        by_store.setdefault((r["chain"], r["store_id"]), []).append(r)
    return by_store


def _resolve_form(con, need: Need, city: str) -> list[str]:
    """Dvosmislena namirnica bez oblika: izaberi najjeftiniji oblik (po jedinici) i vrati upozorenje."""
    st = need.staple
    if st.form_staples:  # oblik je druga namirnica (rajčica)
        options = {f: load_staples()[k] for f, k in st.form_staples.items()}
    elif st.ambiguous_form:
        options = {f: st for f in st.attributes["oblik"] if f != "nepoznato"}
    else:
        return []
    if need.form:
        if need.form not in options:
            raise IngredientError(f"nepoznat oblik '{need.form}' za '{st.name}'; mogući: {', '.join(options)}")
        if st.form_staples:
            need.staple = options[need.form]
        return []
    prices = {}
    for form, fst in options.items():
        probe = Need(need.input, fst, need.amount, need.unit, dict(need.attributes),
                     form=form if fst is st else None)
        try:
            probe.amount, probe.unit, _ = to_base(*_input_amount(need.input), fst)
        except IngredientError:
            continue
        unit_costs = []
        for rows in _prepare(con, probe, city).values():
            pick = choose_product(rows, probe.amount, probe.unit, _by_weight_unit(fst), fst.loose_produce)
            if pick and not pick["fallback"]:
                unit_costs.append(pick["cost_used"])
        if unit_costs:
            prices[form] = min(unit_costs)
    if not prices:
        return [f"'{st.name}': nijedan oblik nije dostupan u gradu"]
    form = min(prices, key=prices.get)
    need.form, need.assumed_form = form, True
    if st.form_staples:
        need.staple = options[form]
    others = ", ".join(f"{f} {prices[f]:.2f} €" for f in sorted(prices, key=prices.get) if f != form)
    return [f"'{need.input.get('name')}' bez oblika: pretpostavljen '{form}' (najjeftiniji za ovu količinu: "
            f"{prices[form]:.2f} €{'; ostali: ' + others if others else ''}). Zadaj 'form' za drugi oblik."]


def _input_amount(item: dict) -> tuple[float, str]:
    return float(item.get("amount") or 0), item.get("unit") or ""


def _by_weight_unit(st: Staple) -> str | None:
    """Jedinica kupnje na vagu (kg/l) za svježe voće/povrće; za ostale namirnice samo roba
    promjenjive težine (vidi choose_product)."""
    return st.unit if st.compare_by == "unit" and st.unit in ("kg", "l") else None


def city_suggestions(con, city: str, n: int = 5) -> list[str]:
    names = {r[0] for r in con.execute(
        "SELECT DISTINCT city_canonical FROM clean.stores WHERE scope = 'local' AND city_canonical IS NOT NULL").fetchall()}
    by_norm = {norm_text(c): c for c in names}
    hits = difflib.get_close_matches(norm_text(city) or "", list(by_norm), n=n, cutoff=0.6)
    return [by_norm[h] for h in hits]


def plan_basket(ingredients: list[dict], city: str, mode: str = "single_store",
                con: duckdb.DuckDBPyConnection | None = None, max_stores: int | None = None) -> dict:
    """Cijena recepta po trgovini u gradu (+ nacionalne cijene) i najbolja trgovina.

    ingredients: [{"name": "brašno", "amount": 500, "unit": "g", "form": None, "attributes": {...}}]
    Vraća ingredients (povezani sastojci s pretpostavkama), unmatched, stores (svaka trgovina:
    stavke, total, broj povezanih sastojaka), best_store, warnings, date i date_hr.
    """
    if mode != "single_store":
        raise ValueError("podržan je samo mode='single_store'")
    con = con or connect()
    out = {"city": city, "mode": mode, "ingredients": [], "unmatched": [], "warnings": [], "stores": [],
           "best_store": None}
    resolved_city = resolve_city(city, con=con) if city else None
    if not resolved_city:
        out["city_suggestions"] = city_suggestions(con, city or "")
        out["warnings"].append(f"nepoznat grad '{city}'" + (
            f"; možda: {', '.join(out['city_suggestions'])}" if out["city_suggestions"] else ""))
        return out
    out["city"] = resolved_city

    needs = []
    for item in ingredients:
        try:
            staple, attrs = resolve_name(item.get("name", ""))
            attrs.update(item.get("attributes") or {})
            for a, v in attrs.items():
                if v not in staple.attributes.get(a, {}):
                    raise IngredientError(f"nepoznat atribut {a}={v} za '{staple.name}'")
            amount, unit, warns = to_base(*_input_amount(item), staple)
            need = Need(item, staple, amount, unit, attrs, form=item.get("form"), warnings=warns)
            need.warnings += _resolve_form(con, need, city)
            if need.staple is not staple:  # oblik je druga namirnica: količina u njezinoj jedinici
                need.amount, need.unit, more = to_base(*_input_amount(item), need.staple)
                need.warnings += more
            needs.append(need)
        except IngredientError as e:
            out["unmatched"].append({"name": item.get("name"), "reason": str(e)})

    stores: dict[tuple, dict] = {}
    for idx, need in enumerate(needs):
        out["ingredients"].append({
            "name": need.input.get("name"), "staple": need.staple.key, "amount": round(need.amount, 3),
            "unit": need.unit, "attributes": need.attributes, "form": need.form,
            "assumed_form": need.form if need.assumed_form else None, "pantry": need.staple.pantry,
            "warnings": need.warnings,
        })
        out["warnings"] += need.warnings
        for key, rows in _prepare(con, need, city).items():
            pick = choose_product(rows, need.amount, need.unit, _by_weight_unit(need.staple), need.staple.loose_produce)
            if pick is None:
                continue
            first = rows[0]
            store = stores.setdefault(key, {
                "chain": first["chain"], "store_id": first["store_id"], "address": first["address"],
                "city": first["city"], "scope": first["scope"], "data_quality": first["data_quality"],
                "items": {}, "date": first["date"],
            })
            store["items"][idx] = {
                "ingredient": need.input.get("name"), "staple": need.staple.key, "need": round(need.amount, 3),
                "need_unit": need.unit, "product_id": pick["product_id"], "ean": pick["ean_norm"],
                "name": pick["name"], "pack_qty": pick["qty"], "n_packs": pick["n_packs"],
                "price_eff": pick["price_eff"], "cost_pack": pick["cost_pack"], "cost_used": pick["cost_used"],
                "counted": pick["cost_used"] if need.staple.pantry else pick["cost_pack"],
                "pantry": need.staple.pantry, "price_per_unit": pick["price_per_unit"], "per_unit": pick["per_unit"],
                "unit_confidence": pick["unit_confidence"], "pack_source": pick["pack_source"],
                "is_special": pick["is_special"], "flags": pick["flags"], "notes": pick["notes"],
                "fallback": pick["fallback"],
            }

    n_needs = len(needs)
    for s in stores.values():
        s["missing"] = [needs[i].input.get("name") for i in range(n_needs) if i not in s["items"]]
        items = [s["items"][i] for i in sorted(s["items"])]
        s["items"] = items
        s["n_matched"] = len(items)
        s["n_ingredients"] = n_needs
        s["total"] = round(sum(it["counted"] for it in items), 2)
        s["total_pack"] = round(sum(it["cost_pack"] for it in items), 2)
        s["flagged_items"] = sum(1 for it in items if it["flags"])
        s["unit_confidence"] = "low" if any(it["unit_confidence"] != "high" for it in items) else "high"
        if s["scope"] == "national":
            s["note"] = NATIONAL_NOTE
        d = s.pop("date")
        s["date"], s["date_hr"] = d.isoformat(), date_hr(d)
    ranked = sorted(stores.values(), key=lambda s: (-s["n_matched"], s["data_quality"] == "suspect",
                                                    s["flagged_items"], s["total"]))
    out["stores"] = ranked[:max_stores] if max_stores else ranked
    eligible = [s for s in ranked if s["data_quality"] != "suspect"] or ranked
    if eligible:
        out["best_store"] = eligible[0]
        if eligible[0]["data_quality"] == "suspect":
            out["warnings"].append("najbolja trgovina je lanac sa sumnjivim podacima (nema druge)")
    dates = [s["date"] for s in ranked]
    if dates:
        out["date"] = max(dates)
        out["date_hr"] = next(s["date_hr"] for s in ranked if s["date"] == out["date"])
    return out
