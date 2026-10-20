"""Košarica za recept: plan_basket(ingredients, city, mode="single_store")."""

import difflib
import math
from dataclasses import dataclass, field

import duckdb

from mealmeter import units
from mealmeter.build import NATIONAL_NOTE
from mealmeter.normalize import date_hr, norm_text
from mealmeter.search import _candidates, _food_filter, connect, resolve_city
from mealmeter.staples import Staple, load_staples, resolve_ingredient

# jedinica u receptu -> (osnovna jedinica, faktor); kuhinjske mjere (žlica, šalica...) su u data/units.yaml
_UNIT_ALIASES = {
    "g": ("g", 1), "gr": ("g", 1), "gram": ("g", 1), "grama": ("g", 1), "dag": ("g", 10), "dkg": ("g", 10),
    "kg": ("g", 1000), "kila": ("g", 1000),
    "ml": ("ml", 1), "cl": ("ml", 10), "dl": ("ml", 100), "l": ("ml", 1000), "lit": ("ml", 1000), "litra": ("ml", 1000),
    "kom": ("kom", 1), "komad": ("kom", 1), "komada": ("kom", 1), "kos": ("kom", 1), "glavica": ("kom", 1),
    "rezanj": ("kom", 1), "rezanja": ("kom", 1), "cesanj": ("kom", 1), "cesnja": ("kom", 1),
    # vezica (svježe bilje) je komad bez mase: pretvara se samo uz piece_g, a peršin ga namjerno nema
    "vezica": ("kom", 1), "vezice": ("kom", 1),
    "vrecica": ("vrecica", 1), "vrecice": ("vrecica", 1), "paket": ("vrecica", 1), "paketic": ("vrecica", 1),
}
FLAG_TEXT = {
    "clearance": "rasprodaja (SNIŽENJE)",
    "price_suspect": "cijena izvan granica",
    "pack_confidence_low": "nesigurna gramatura (višestruko pakiranje)",
    "chain_suspect": "lanac sa sumnjivim podacima",
}


class IngredientError(ValueError):
    """Sastojak se ne može povezati: razlog ide u `unmatched`."""


class FormAmbiguity(Exception):
    """Mahunarka (ambiguous_form) bez oblika: ne pogađa se, nego se pita (`ambiguous`)."""

    def __init__(self, ambiguity: dict):
        super().__init__(ambiguity["question"])
        self.ambiguity = ambiguity


# redoslijed oblika u pitanju ("suho ili konzerva?")
FORM_ORDER = ("suho", "konzerva", "smrznuto", "svjeze")


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
    input_staple: str | None = None
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
    target = {"kg": "g", "l": "ml"}.get(staple.compare_unit, staple.compare_unit)  # g | ml | kom | vrecica
    if units.is_measure(unit):
        # žlica, šalica, čaša...: ml, pa grami preko gustoće namirnice (procjene iz data/units.yaml)
        try:
            qty, base, warnings = units.convert(amount, unit, staple)
        except ValueError as e:
            raise IngredientError(str(e)) from e
    elif key in _UNIT_ALIASES:
        base, factor = _UNIT_ALIASES[key]
        qty, warnings = amount * factor, []
    else:
        raise IngredientError(f"nepoznata jedinica '{unit}'")
    if base == target:
        return qty, target, warnings
    if {base, target} == {"g", "ml"}:
        # gustoća iz data/units.yaml (procjena), inače 1 g/ml
        density = units.load_units().densities.get(staple.key)
        if density is None:
            warnings.append(f"{qty:g} {base} uzeto kao {qty:g} {target} (gustoća 1)")
            return qty, target, warnings
        out = qty / density if target == "ml" else qty * density
        warnings.append(f"{qty:g} {base} ≈ {out:g} {target} (procjena, {density:g} g/ml)")
        return out, target, warnings
    # masa komada: data/units.yaml (pieces, procjena), inače piece_g iz staples.yaml
    piece = units.piece_weight(staple.key) or staple.piece_g
    if base == "kom" and target in ("g", "ml") and piece:
        warnings.append(f"{qty:g} kom ≈ {qty * piece:g} g (komad {piece:g} g, procjena)")
        return qty * piece, "g" if target == "g" else "ml", warnings
    if target == "kom" and base == "g" and piece:
        warnings.append(f"{qty:g} g ≈ {qty / piece:g} kom (komad {piece:g} g, procjena)")
        return qty / piece, "kom", warnings
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
    2. Najjeftinije pakiranje (apsolutna cijena) koje pokriva količinu, uz jednaku cijenu manje. Roba na vagu
       (cijena po kg/l, bez pakiranja) pokriva točno potrebnu količinu:
       - `loose` (svježe voće i povrće, svježe meso: _by_weight_primary): ravnopravan izbor;
       - inače (sirevi, šunke...): samo roba promjenjive težine ("CCA 4 KG") i samo kad u trgovini nema
         pakiranog proizvoda (rezerva, `by_weight_fallback = True`).
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
    fallback_weight = False
    if not loose and any(not o["by_weight"] for o in options):
        options = [o for o in options if not o["by_weight"]]  # pakirano ima prednost pred vagom
    elif not loose:
        fallback_weight = True
    # slabi članovi namirnice (clean.staple_groups.match_quality = 'weak') samo kad u trgovini nema snažnog
    strong = [o for o in options if o.get("match_quality") != "weak"]
    options = strong or options
    clean = [o for o in options if not o["flags"]]
    pool = clean or options

    def per_unit_cost(o):
        return o["price_per_unit"] / 1000 if o["by_weight"] else o["price_eff"] / o["qty"]

    covering = [o for o in pool if o["by_weight"] or o["qty"] >= need]
    if covering:
        # najjeftinije pakiranje koje pokriva količinu (apsolutna cijena), uz jednaku cijenu manje
        best = min(covering, key=lambda o: (o["price_per_unit"] * need / 1000 if o["by_weight"] else o["price_eff"],
                                            need if o["by_weight"] else o["qty"]))
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
            "fallback": not clean, "by_weight_fallback": fallback_weight and best["by_weight"]}


# --- plan_basket -------------------------------------------------------------------

def _rows_for(con, staple: Staple, attributes: dict, city: str, wholesale: bool = False,
              required: dict | None = None) -> list[dict]:
    # Samo provjerena hrana bez alkohola; proizvod nepoznate skupine (food_group 'unknown', npr.
    # Plodine) samo za svježe voće i povrće, gdje naziv prolazi pravilo prve ili druge riječi.
    food_sql = _food_filter(unverified="staple" if staple.loose_produce else "no")
    sql, params, _ = _candidates(staple, [], attributes, city, include_clearance=True, food_sql=food_sql,
                                 include_wholesale=wholesale, required=required)
    cur = con.execute(sql + " SELECT * FROM x", params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def _product_attrs(con, staple: Staple) -> tuple[dict[tuple, dict], dict[str, dict]]:
    """Atributi proizvoda namirnice: ((chain, product_id) -> {atribut: (vrijednost, how)},
    globalni EAN -> {atribut: najčešća vrijednost iz naziva})."""
    by_product: dict[tuple, dict] = {}
    for chain, pid, attr, value, how in con.execute(
            "SELECT chain, product_id, attr, value, how FROM clean.product_attrs WHERE staple = ?", [staple.key]).fetchall():
        by_product.setdefault((chain, pid), {})[attr] = (value, how)
    by_ean: dict[str, dict] = {}
    for ean, attr, value in con.execute("""
            SELECT p.ean_norm, a.attr, mode(a.value) FROM clean.product_attrs a JOIN clean.products p USING (chain, product_id)
            WHERE a.staple = ? AND p.ean_global AND a.how = 'name' GROUP BY ALL""", [staple.key]).fetchall():
        by_ean.setdefault(ean, {})[attr] = value
    return by_product, by_ean


def chosen_attributes(pick: dict, by_product: dict, by_ean: dict) -> dict:
    """Atributi odabranog proizvoda: iz njegova naziva, a kad ih naziv nema (ili je vrijednost samo
    zadana, how='default'), iz drugih naziva istog EAN-a ("Trajno mlijeko" bez masnoće kod Lidla)."""
    own = by_product.get((pick["chain"], pick["product_id"]), {})
    group = by_ean.get(pick["ean_norm"], {}) if pick.get("ean_global") else {}
    out = {a: v for a, (v, how) in own.items() if how != "default"}
    for a, v in group.items():
        out.setdefault(a, v)
    for a, (v, _) in own.items():
        out.setdefault(a, v)
    return out


def _group_values(con, staple: Staple, prefs: dict) -> dict[str, dict]:
    """{atribut: {bkey: vrijednost grupe}} za atribute s default_preference (clean.staple_group_attrs)."""
    out = {}
    for attr in prefs:
        out[attr] = dict(con.execute("SELECT bkey, value FROM clean.staple_group_attrs WHERE staple = ? AND attr = ?",
                                     [staple.key, attr]).fetchall())
    return out


def _choose_preferred(rows: list[dict], need: "Need", prefs: dict, group_values: dict) -> dict | None:
    """choose_product uz zadani redoslijed vrijednosti (default_preference): prva vrijednost koja u
    trgovini daje proizvod bez zastavica; inače najbolji izbor među svim kandidatima."""
    args = (need.amount, need.unit, _by_weight_unit(need.staple), _by_weight_primary(need.staple))
    for attr, order in prefs.items():
        for value in order:
            sub = [r for r in rows if group_values[attr].get(r["bkey"]) == value]
            if sub and (pick := choose_product(sub, *args)) and not pick["fallback"]:
                return pick
    return choose_product(rows, *args)


def _num(v):
    return float(v) if v is not None else None


def _prepare(con, need: Need, city: str, wholesale: bool = False) -> dict[tuple, list[dict]]:
    """Kandidati po trgovini (chain, store_id) za jedan sastojak (uz odabrani oblik)."""
    attrs = dict(need.attributes)
    if need.form and "oblik" in need.staple.attributes:
        attrs["oblik"] = need.form
    required = dict(attrs)  # traženo imenom, atributima ili oblikom: proizvod to mora imati u nazivu
    for a, v in need.staple.defaults().items():
        attrs.setdefault(a, v)
    by_store: dict[tuple, list[dict]] = {}
    for r in _rows_for(con, need.staple, attrs, city, wholesale, required):
        for k in ("price_eff", "price_per_unit", "pack_amount", "drained_amount", "n_units", "assumed_g"):
            r[k] = _num(r.get(k))
        by_store.setdefault((r["chain"], r["store_id"]), []).append(r)
    return by_store


def _resolve_form(con, need: Need, city: str, wholesale: bool = False) -> list[str]:
    """Namirnica bez oblika. Rajčica (form_staples): izaberi najjeftiniji oblik i vrati upozorenje.
    Mahunarke, kukuruz i gljive (ambiguous_form): ne pogađaj, nego digni FormAmbiguity s oblicima koji
    su dostupni u gradu i pitanjem ("suho ili konzerva?")."""
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
        for rows in _prepare(con, probe, city, wholesale).values():
            pick = choose_product(rows, probe.amount, probe.unit, _by_weight_unit(fst), _by_weight_primary(fst))
            if pick and not pick["fallback"]:
                unit_costs.append(pick["cost_used"])
        if unit_costs:
            prices[form] = min(unit_costs)
    if not prices:
        return [f"'{st.name}': nijedan oblik nije dostupan u gradu"]
    if st.ambiguous_form:
        forms = sorted(prices, key=lambda f: FORM_ORDER.index(f) if f in FORM_ORDER else len(FORM_ORDER))
        raise FormAmbiguity({"form": forms, "question": " ili ".join(forms) + "?",
                             "prices": {f: round(prices[f], 2) for f in forms}})
    form = min(prices, key=prices.get)
    need.form, need.assumed_form = form, True
    if st.form_staples:
        need.staple = options[form]
    others = ", ".join(f"{f} {prices[f]:.2f} €" for f in sorted(prices, key=prices.get) if f != form)
    return [f"'{need.input.get('name')}' bez oblika: pretpostavljen '{form}' (najjeftiniji za ovu količinu: "
            f"{prices[form]:.2f} €{'; ostali: ' + others if others else ''}). Zadaj 'form' za drugi oblik."]


def _input_amount(item: dict) -> tuple[float, str]:
    return float(item.get("amount") or 0), item.get("unit") or ""


def _by_weight_primary(st: Staple) -> bool:
    """Kupnja na vagu je ravnopravan izbor za svježe voće i povrće (loose_produce) i svježe meso
    (fresh_meat); za ostalo je samo rezerva kad nema pakiranog proizvoda."""
    return st.loose_produce or st.fresh_meat


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
                con: duckdb.DuckDBPyConnection | None = None, max_stores: int | None = None,
                include_wholesale: bool = False, already_have: list[str] | None = None) -> dict:
    """Cijena recepta po trgovini u gradu (+ nacionalne cijene) i najbolja trgovina.

    ingredients: [{"name": "brašno", "amount": 500, "unit": "g", "form": None, "attributes": {...}}]
    Vraća ingredients (povezani sastojci s pretpostavkama), unmatched, stores (svaka trgovina:
    stavke, total, broj povezanih sastojaka), best_store, warnings, date i date_hr.
    Veleprodaja (Metro, store_type 'cash_and_carry') je uključena samo uz include_wholesale=True.
    already_have: namirnice koje korisnik već ima ("sol", "papar"); ostaju u stavkama s have=true, ali ne
    ulaze u total_to_buy (cijela pakiranja za kupiti). total_used je razmjerni trošak svih stavki.
    """
    if mode != "single_store":
        raise ValueError("podržan je samo mode='single_store'")
    con = con or connect()
    out = {"city": city, "mode": mode, "ingredients": [], "unmatched": [], "ambiguous": [], "warnings": [],
           "stores": [], "best_store": None}
    resolved_city = resolve_city(city, con=con) if city else None
    if not resolved_city:
        out["city_suggestions"] = city_suggestions(con, city or "")
        out["warnings"].append(f"nepoznat grad '{city}'" + (
            f"; možda: {', '.join(out['city_suggestions'])}" if out["city_suggestions"] else ""))
        return out
    out["city"] = resolved_city
    have = set()
    for name in already_have or []:
        try:
            have.add(resolve_name(name)[0].key)
        except IngredientError:
            out["warnings"].append(f"already_have: nepoznata namirnica '{name}'")
    out["already_have"] = sorted(have)

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
            need.input_staple = staple.key  # prije oblika (rajčica -> pasirana_rajcica), za already_have
            need.warnings += _resolve_form(con, need, city, include_wholesale)
            if need.staple is not staple:  # oblik je druga namirnica: količina u njezinoj jedinici
                need.amount, need.unit, more = to_base(*_input_amount(item), need.staple)
                need.warnings += more
            needs.append(need)
        except IngredientError as e:
            out["unmatched"].append({"name": item.get("name"), "reason": str(e)})
        except FormAmbiguity as e:
            # bez oblika se ne računa: korisnik bira oblik ("form") i ponovi upit
            out["ambiguous"].append({"name": item.get("name"), "staple": staple.key, "amount": amount, "unit": unit,
                                     "ambiguity": e.ambiguity})
            out["warnings"].append(f"'{item.get('name')}': {e.ambiguity['question']} (zadaj 'form'; nije uračunato)")

    stores: dict[tuple, dict] = {}
    for idx, need in enumerate(needs):
        out["ingredients"].append({
            "name": need.input.get("name"), "staple": need.staple.key, "amount": round(need.amount, 3),
            "unit": need.unit, "attributes": need.attributes, "form": need.form,
            # traženi atributi uz zadane (mlijeko: vrsta=trajno, mast=2.8) i prihvaćene zamjene
            "applied_attributes": {a: list(v) if isinstance(v, tuple) else v
                                   for a, v in {**need.staple.defaults(), **need.attributes}.items()},
            "accepted_values": {a: list(need.staple.accepted_values(a, v)) for a, v in
                                {**need.staple.defaults(), **need.attributes}.items()
                                if len(need.staple.accepted_values(a, v)) > 1},
            "assumed_form": need.form if need.assumed_form else None, "pantry": need.staple.pantry,
            "warnings": need.warnings,
        })
        out["warnings"] += need.warnings
        attrs_of, attrs_of_ean = _product_attrs(con, need.staple)
        prefs = {a: v for a, v in need.staple.default_preference.items() if a not in need.attributes}
        group_values = _group_values(con, need.staple, prefs)
        for key, rows in _prepare(con, need, city, include_wholesale).items():
            pick = _choose_preferred(rows, need, prefs, group_values)
            if pick is None:
                continue
            first = rows[0]
            store = stores.setdefault(key, {
                "chain": first["chain"], "store_id": first["store_id"], "address": first["address"],
                "city": first["city"], "scope": first["scope"], "data_quality": first["data_quality"],
                "items": {}, "date": first["date"],
            })
            chosen = chosen_attributes(pick, attrs_of, attrs_of_ean)
            wanted = {**need.staple.defaults(), **need.attributes}
            subst = [f"{a}={chosen[a]} umjesto {v} (zamjenjivo)" for a, v in wanted.items()
                     if not isinstance(v, tuple) and chosen.get(a) not in (None, v)
                     and chosen[a] in need.staple.accepted_values(a, v)]
            subst += [f"{a}={chosen[a]}: prva dostupna po zadanom redoslijedu ({', '.join(v)})"
                      for a, v in wanted.items() if isinstance(v, tuple) and chosen.get(a) not in (None, v[0])]
            store["items"][idx] = {
                "ingredient": need.input.get("name"), "staple": need.staple.key, "need": round(need.amount, 3),
                "need_unit": need.unit, "product_id": pick["product_id"], "ean": pick["ean_norm"],
                "name": pick["name"], "attributes": chosen,
                "pack_qty": pick["qty"], "n_packs": pick["n_packs"],
                "price_eff": pick["price_eff"], "cost_pack": pick["cost_pack"], "cost_used": pick["cost_used"],
                "have": need.staple.key in have or need.input_staple in have,
                "pantry": need.staple.pantry, "price_per_unit": pick["price_per_unit"], "per_unit": pick["per_unit"],
                "unit_confidence": pick["unit_confidence"], "pack_source": pick["pack_source"],
                "is_special": pick["is_special"], "flags": pick["flags"], "notes": pick["notes"] + subst,
                "fallback": pick["fallback"], "food_unverified": pick["is_food"] is None,
                "date": pick["date"].isoformat(), "date_hr": date_hr(pick["date"]), "stale_days": pick["stale_days"],
                "match_quality": pick.get("match_quality"), "by_weight_fallback": pick["by_weight_fallback"],
            }

    n_needs = len(needs)
    for s in stores.values():
        s["missing"] = [needs[i].input.get("name") for i in range(n_needs) if i not in s["items"]]
        items = [s["items"][i] for i in sorted(s["items"])]
        s["items"] = items
        s["n_matched"] = len(items)
        s["n_ingredients"] = n_needs
        # za kupiti: cijela pakiranja svega što korisnik nema; utrošeno: razmjerno, za sve stavke
        s["total_to_buy"] = round(sum(it["cost_pack"] for it in items if not it["have"]), 2)
        s["total_used"] = round(sum(it["cost_used"] for it in items), 2)
        s["flagged_items"] = sum(1 for it in items if it["flags"])
        s["unit_confidence"] = "low" if any(it["unit_confidence"] != "high" for it in items) else "high"
        if s["scope"] == "national":
            s["note"] = NATIONAL_NOTE
        s.pop("date")
        # datum trgovine = najstarija cijena među stavkama (prenesena cijena ima stale_days > 0)
        oldest = min(items, key=lambda it: it["date"]) if items else None
        s["date"], s["date_hr"] = (oldest["date"], oldest["date_hr"]) if oldest else (None, None)
        s["stale_days"] = max((it["stale_days"] or 0 for it in items), default=0)
    ranked = sorted(stores.values(), key=lambda s: (-s["n_matched"], s["data_quality"] == "suspect",
                                                    s["flagged_items"], s["total_to_buy"]))
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
