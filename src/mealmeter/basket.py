"""Košarica za recept: plan_basket(ingredients, city, mode="single_store")."""

import difflib
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import duckdb

from mealmeter import units
from mealmeter.build import NATIONAL_NOTE
from mealmeter.build import WHOLESALE_CHAINS
from mealmeter.normalize import date_hr, norm_text, parse_multipack_unit
from mealmeter.search import _candidates, _food_filter, connect, find_products, format_pack, resolve_city
from mealmeter.staples import Staple, extract_attributes_detail, load_staples, resolve_ingredient

# jedinica u receptu -> (osnovna jedinica, faktor); kuhinjske mjere (žlica, šalica...) su u data/units.yaml
_UNIT_ALIASES = {
    "g": ("g", 1), "gr": ("g", 1), "gram": ("g", 1), "grama": ("g", 1), "dag": ("g", 10), "dkg": ("g", 10),
    "kg": ("g", 1000), "kila": ("g", 1000),
    "ml": ("ml", 1), "cl": ("ml", 10), "dl": ("ml", 100), "l": ("ml", 1000), "lit": ("ml", 1000), "litra": ("ml", 1000),
    "kom": ("kom", 1), "komad": ("kom", 1), "komada": ("kom", 1), "kos": ("kom", 1), "glavica": ("kom", 1),
    "rezanj": ("kom", 1), "rezanja": ("kom", 1), "cesanj": ("kom", 1), "cesnja": ("kom", 1),
    "list": ("kom", 1), "lista": ("kom", 1), "listova": ("kom", 1), "listic": ("kom", 1),
    # vezica (svježe bilje) je komad bez mase: pretvara se samo uz piece_g, a peršin ga namjerno nema
    "vezica": ("kom", 1), "vezice": ("kom", 1),
    "vrecica": ("vrecica", 1), "vrecice": ("vrecica", 1), "paket": ("vrecica", 1), "paketic": ("vrecica", 1),
}
FLAG_TEXT = {
    "clearance": "rasprodaja (SNIŽENJE)",
    "price_suspect": "cijena izvan granica",
    "pack_confidence_low": "nesigurna gramatura (višestruko pakiranje)",
    "chain_suspect": "lanac sa sumnjivim podacima",
    "unit_suspect": "gramatura iz stupca unit izgleda krivo (cijena izvan granica ili daleko od drugih lanaca)",
    "portion_pack": "porcijsko pakiranje (>= 20 komada po <= 20 g)",
}


BRANDS_PATH = Path(__file__).resolve().parents[2] / "data" / "brands.yaml"


@lru_cache(maxsize=2)
def load_brands(path: Path = BRANDS_PATH) -> tuple[tuple[str, str], ...]:
    """Marke iz data/brands.yaml kao (naziv, regex na početku riječi normaliziranog teksta)."""
    import yaml

    if not Path(path).exists():
        return ()
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return tuple((name, "(^| )(?:" + "|".join(pats) + ")") for name, pats in raw.items())


def brand_in(name: str | None) -> tuple[str, str] | None:
    """Marka iz naziva sastojka ("nutella" -> ("Nutella", regex)), inače None."""
    text = norm_text(name or "") or ""
    return next(((b, rx) for b, rx in load_brands() if re.search(rx, text)), None)


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
    """Sastojak recepta preveden u namirnicu i količinu u njezinoj osnovnoj jedinici. Sastojak izvan
    rječnika (free_text) nema namirnicu (staple None) i nosi kandidate po trgovini iz pretrage po nazivu."""
    input: dict
    staple: Staple | None
    amount: float  # u `unit`
    unit: str  # g | ml | kom | vrecica
    attributes: dict = field(default_factory=dict)
    form: str | None = None
    assumed_form: bool = False
    input_staple: str | None = None
    warnings: list = field(default_factory=list)
    free_text: bool = False
    free_rows: dict = field(default_factory=dict)
    attr_fn: object = None  # odabrani proizvod -> atributi (chosen_attributes), za alternative
    brand: tuple | None = None  # (naziv marke, regex) iz naziva sastojka (data/brands.yaml)
    note_fn: object = None  # atributi -> napomena za alternativu izvan zadanog izbora ("kavezni, s")


def resolve_name(name: str) -> tuple[Staple, dict]:
    """Naziv sastojka -> (namirnica, atributi). Točan sinonim, ili sinonim + vrijednosti atributa
    ("glatko brašno" -> brasno, tip=glatko). Inače IngredientError."""
    if st := resolve_ingredient(name):
        # sinonim koji je i vrijednost atributa ("špageti" -> tjestenina, oblik=spageti)
        q = norm_text(name)
        hit = [(a, v) for a, vals in st.attributes.items() for v in vals if norm_text(v.replace("_", " ")) == q]
        attrs = dict(hit[:1])
        # riječi sinonima zamjenjuju zadanu vrijednost atributa ("ljuta paprika": vrsta=ljuta, ne zadana slatka)
        detail = extract_attributes_detail(st, name)
        for a in st.default_attributes:
            if a in detail and detail[a][1] == "name":
                attrs.setdefault(a, detail[a][0])
        return st, attrs
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
    if row.get("unit_suspect"):
        out.append("unit_suspect")
    if row.get("portion_pack"):
        out.append("portion_pack")
    return out


PORTION_MIN_COUNT, PORTION_MAX_G, PORTION_STAPLE_MIN_PACK = 20, 20, 250


def portion_pack(row: dict, staple: Staple | None) -> bool:
    """Porcijsko pakiranje ("ŠEĆER MINUTE 1000X4g"): >= 20 komada po <= 20 g, kod namirnica čije je
    najmanje pakiranje >= 250 g (šećer, brašno...), gdje porcije nisu usporedive kupnja."""
    if not (staple and (staple.min_pack or 0) >= PORTION_STAPLE_MIN_PACK and staple.unit in ("kg", "l")):
        return False
    multi = parse_multipack_unit(row.get("name"))
    return bool(multi and multi[0] >= PORTION_MIN_COUNT and multi[2] in ("g", "ml") and multi[1] <= PORTION_MAX_G)


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
    # Slabi članovi samo s riječju namirnice među prve tri riječi (weak="early"; choose_product ih uzima
    # tek kad trgovina nema snažnog). Samo provjerena hrana bez alkohola; proizvod nepoznate skupine (food_group 'unknown', npr.
    # Plodine) samo za svježe voće i povrće, gdje naziv prolazi pravilo prve ili druge riječi.
    food_sql = _food_filter(unverified="staple" if staple.loose_produce else "no")
    sql, params, _ = _candidates(staple, [], attributes, city, include_clearance=True, food_sql=food_sql,
                                 include_wholesale=wholesale, required=required, weak="early")
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
    if need.staple.quality_rank and need.attr_fn:
        rows = sorted(rows, key=lambda r: quality_key(need.staple, need.attr_fn(r)))  # jednaka cijena: bolji prvi
    for tier in tiers_for(need):
        sub = [r for r in rows if in_tier(need.attr_fn(r), tier)]
        if sub and (pick := choose_product(sub, *args)) and not pick["fallback"]:
            return pick
    for attr, order in prefs.items():
        for value in order:
            sub = [r for r in rows if group_values[attr].get(r["bkey"]) == value]
            if sub and (pick := choose_product(sub, *args)) and not pick["fallback"]:
                return pick
    return choose_product(rows, *args)


def tiers_for(need: "Need") -> list[dict]:
    """Razine zadanog izbora (preferred_tiers) bez atributa koje je korisnik sam zadao."""
    if need.free_text or not need.attr_fn:
        return []
    tiers = [{a: v for a, v in t.items() if a not in need.attributes} for t in need.staple.preferred_tiers]
    return [t for t in tiers if t]


def in_tier(attrs: dict, tier: dict) -> bool:
    """Atributi proizvoda unutar razine; "_none" znači da atribut nije poznat."""
    return all(attrs.get(a, "_none") in values for a, values in tier.items())


def quality_key(staple: Staple, attrs: dict) -> tuple:
    return tuple(order.index(attrs[a]) if attrs.get(a) in order else len(order) for a, order in staple.quality_rank.items())


def tier_note(need: "Need", attrs: dict) -> str | None:
    """Napomena za proizvod izvan prve razine zadanog izbora: vrijednosti izvan nje ("kavezni, S")."""
    tiers = tiers_for(need)
    if not tiers or in_tier(attrs, tiers[0]):
        return None
    order = sorted(tiers[0], key=lambda a: a not in need.staple.quality_rank)  # najprije uzgoj, pa veličina
    out = [attrs.get(a, "nepoznato") for a in order if attrs.get(a, "_none") not in tiers[0][a]]
    return ", ".join(v.upper() if len(v) <= 2 else v for v in out) or None


BULK_MIN_SACHETS = 3


def bulk_sachets(row: dict, staple: Staple) -> None:
    """Rinfuza namirnice u vrećicama (compare_by: pack): pakiranje od >= 3 vrećice (pack_amount >= 3 *
    sachet_g, npr. Lidlov "Vanilin šećer" 80 g) računa se kao pack_amount / sachet_g vrećica, pa je utrošak
    za n vrećica (n * sachet_g / pack_amount) * cijena, a ne cijelo pakiranje."""
    if (staple.compare_by != "pack" or not staple.sachet_g or row.get("pack_unit") != "g"
            or (row.get("n_units") or 1) > 1 or (row.get("pack_amount") or 0) < BULK_MIN_SACHETS * staple.sachet_g):
        return
    row["n_units"] = row["pack_amount"] / staple.sachet_g
    row["bulk_sachet_g"] = staple.sachet_g


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
        r["portion_pack"] = portion_pack(r, need.staple)
        bulk_sachets(r, need.staple)
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
    prices, amounts = {}, {}
    for form, fst in options.items():
        probe = Need(need.input, fst, need.amount, need.unit, dict(need.attributes),
                     form=form if fst is st else None)
        try:
            probe.amount, probe.unit, _ = to_base(*_input_amount(need.input), fst)
        except IngredientError:
            continue
        apply_yield(probe, form)  # usporedba na istu količinu gotovog proizvoda (suho / 2,5)
        unit_costs = []
        for rows in _prepare(con, probe, city, wholesale).values():
            pick = choose_product(rows, probe.amount, probe.unit, _by_weight_unit(fst), _by_weight_primary(fst))
            if pick and not pick["fallback"]:
                unit_costs.append(pick["cost_used"])
        if unit_costs:
            prices[form], amounts[form] = min(unit_costs), round(probe.amount, 1)
    if not prices:
        return [f"'{st.name}': nijedan oblik nije dostupan u gradu"]
    if st.ambiguous_form:
        forms = sorted(prices, key=lambda f: FORM_ORDER.index(f) if f in FORM_ORDER else len(FORM_ORDER))
        raise FormAmbiguity({"form": forms, "question": " ili ".join(forms) + "?",
                             "prices": {f: round(prices[f], 2) for f in forms},
                             "amounts": {f: amounts[f] for f in forms}, "unit": need.unit})
    form = min(prices, key=prices.get)
    need.form, need.assumed_form = form, True
    if st.form_staples:
        need.staple = options[form]
    others = ", ".join(f"{f} {prices[f]:.2f} €" for f in sorted(prices, key=prices.get) if f != form)
    return [f"'{need.input.get('name')}' bez oblika: pretpostavljen '{form}' (najjeftiniji za ovu količinu: "
            f"{prices[form]:.2f} €{'; ostali: ' + others if others else ''}). Zadaj 'form' za drugi oblik."]


def apply_yield(need: "Need", form: str | None) -> list[str]:
    """Količina gotovog proizvoda -> količina u obliku (suho: / faktor iz data/yields.yaml, procjena)."""
    factor = units.yield_factor(need.staple.key, form)
    if not factor or need.unit != "g":
        return []
    ready = need.amount
    need.amount = ready / factor
    return [f"{ready:g} g gotovog ≈ {need.amount:g} g u obliku '{form}' (procjena, prinos {factor:g}x)"]


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


def _filter_store(stores: dict[tuple, dict], spec: dict, out: dict) -> dict[tuple, dict]:
    """Trgovine lanca `spec["chain"]` čija adresa sadrži `spec["address_contains"]` (bez dijakritika i
    velikih slova). Nacionalne cijene lanca popunjavaju sastojke koje lokalna trgovina nema."""
    chain = norm_text(spec.get("chain") or "")
    addr = norm_text(spec.get("address_contains") or "")
    of_chain = {k: s for k, s in stores.items() if norm_text(s["chain"]) == chain}
    national = [s for s in of_chain.values() if s["scope"] == "national"]
    local = {k: s for k, s in of_chain.items() if s["scope"] != "national"
             and (not addr or addr in (norm_text(s["address"] or "") or ""))}
    if not local:
        if national and not addr:
            return {k: s for k, s in of_chain.items() if s["scope"] == "national"}
        known = sorted({s["address"] for s in of_chain.values() if s["address"]})
        out["warnings"].append(f"store: nema trgovine '{spec.get('chain')}'"
                               + (f" s adresom '{spec.get('address_contains')}'" if addr else "")
                               + " u gradu" + (f"; adrese lanca: {'; '.join(known[:10])}" if known else ""))
        out["store_suggestions"] = known[:20]
        return {}
    for s in local.values():
        for nat in national:
            for idx, it in nat["items"].items():
                if idx not in s["items"]:
                    s["items"][idx] = {**it, "notes": it["notes"] + ["nacionalna cijena lanca"],
                                       "_from_store": nat["store_id"]}
    return local


def _choose_args(need: "Need") -> tuple:
    """Argumenti choose_product za sastojak: količina, jedinica, kupnja na vagu."""
    if need.free_text:
        # slobodan naziv: na vagu samo roba promjenjive težine i samo bez pakiranog proizvoda
        return need.amount, need.unit, {"g": "kg", "ml": "l"}.get(need.unit), False
    return need.amount, need.unit, _by_weight_unit(need.staple), _by_weight_primary(need.staple)


def pack_size(pick: dict, need_unit: str) -> str | None:
    """Veličina jednog pakiranja za prikaz ("500 g", "1 l", "6 vrećica, 72 g", "na vagu")."""
    if pick.get("by_weight"):
        return "na vagu"
    if pick.get("assumed_g"):
        return "≈ " + format_pack(pick["assumed_g"], "g")
    size = format_pack(pick.get("pack_amount"), pick.get("pack_unit"))
    if pick.get("bulk_sachet_g"):
        return f"{size} (≈ {pick['n_units']:g} vrećica od {pick['bulk_sachet_g']:g} g)"
    if need_unit == "vrecica" and (pick.get("n_units") or 0) > 1:
        return f"{pick['n_units']:g} vrećica" + (f", {size}" if size else "")
    return size or format_pack(pick.get("qty"), need_unit)


def alt_eligible(row: dict, staple: Staple | None) -> bool:
    """Proizvod smije biti alternativa: ista pravila kao glavni izbor bez rezerve, tj. bez veleprodaje,
    robe promjenjive težine ("GRANA PADANO cca 1KG"), cijene ili gramature izvan granica, porcijskih
    pakiranja i slabih članova namirnice."""
    return not (row["chain"] in WHOLESALE_CHAINS or row.get("variable_weight") or row.get("price_suspect")
                or row.get("unit_suspect") or row.get("clearance") or portion_pack(row, staple)
                or row.get("match_quality") == "weak" or row.get("data_quality") == "suspect")


def quality_better(staple: Staple | None, alt_attrs: dict, item_attrs: dict) -> bool:
    """Je li alternativa bolje kvalitete po quality_rank namirnice (jaja: bolji uzgoj)."""
    for attr, order in (staple.quality_rank.items() if staple else ()):
        a, b = alt_attrs.get(attr), item_attrs.get(attr)
        if a in order and (b not in order or order.index(a) < order.index(b)):
            return True
    return False


def _alternatives(rows: list[dict], need: "Need", item: dict, n: int = 2) -> list[dict]:
    """Jeftinije alternative u istoj trgovini (cheaper = true), najviše n, od najjeftinije; uz to iznimno
    jedna iste cijene i bolje kvalitete (quality_rank, npr. bolji uzgoj jaja). Kandidati prolaze
    alt_eligible; delta_eur je alternativa minus odabrano."""
    args = _choose_args(need)
    seen, picks = {item["product_id"], item["name"]}, []
    for r in rows:
        if r["product_id"] in seen or r["name"] in seen or not alt_eligible(r, need.staple):
            continue
        if pick := choose_product([r], *args):
            seen.update((r["product_id"], r["name"]))
            picks.append(pick)
    attrs = need.attr_fn or (lambda p: {})
    cheaper = sorted((p for p in picks if p["cost_pack"] < item["cost_pack"]), key=lambda p: p["cost_pack"])[:n]
    same = [p for p in picks if p["cost_pack"] == item["cost_pack"]
            and quality_better(need.staple, attrs(p), item.get("attributes") or {})][:1]
    out = []
    for p in cheaper + same:
        alt = {"product_id": p["product_id"], "ean": p["ean_norm"], "name": p["name"],
               "pack_size": pack_size(p, need.unit), "n_packs": p["n_packs"], "price_eff": p["price_eff"],
               "cost_pack": p["cost_pack"], "cost_used": p["cost_used"],
               "delta_eur": round(p["cost_pack"] - item["cost_pack"], 2), "cheaper": p["cost_pack"] < item["cost_pack"],
               "price_per_unit": p["price_per_unit"], "per_unit": p["per_unit"],
               "match_quality": "free_text" if need.free_text else p.get("match_quality")}
        if note := need.note_fn(attrs(p)) if need.note_fn else None:
            alt["note"] = note
        out.append(alt)
    return out


# --- sastojak izvan rječnika (free_text) ---------------------------------------------

def _free_tokens(name: str) -> list[str]:
    """Riječi naziva za pretragu: bez brojeva i riječi kraćih od 2 slova."""
    return [w for w in (norm_text(name) or "").split() if len(w) >= 2 and not w[0].isdigit()]


def _free_need(item: dict) -> "Need":
    """Sastojak bez namirnice: količina u g, ml ili kom (žlice preko 1 g/ml, uz upozorenje)."""
    amount, unit = _input_amount(item)
    if amount <= 0:
        raise IngredientError("količina mora biti pozitivna")
    if not _free_tokens(item.get("name") or ""):
        raise IngredientError(f"'{item.get('name')}': nema riječi za pretragu")
    key = norm_text(unit) or ""
    if units.is_measure(unit):
        qty, base, warnings = units.convert(amount, unit, norm_text(item.get("name") or ""))
    elif key in _UNIT_ALIASES and _UNIT_ALIASES[key][0] in ("g", "ml", "kom"):
        base, factor = _UNIT_ALIASES[key]
        qty, warnings = amount * factor, []
    else:
        raise IngredientError(f"nepoznata jedinica '{unit}' (free_text: g, ml ili kom)")
    return Need(item, None, qty, base, free_text=True,
                warnings=warnings + [f"'{item.get('name')}': slobodna pretraga po nazivu (nije u rječniku); provjeri proizvod"])


# free_text: okusi (osim ako su u upitu) i grickalice/porcije nisu sastojak ("kikiriki maslac" nije
# "ZOE KIKIRIKI MASLAC ČOKO" ni "SPORTNESS KOŠARICE KIKIRIKI MASLAC 42 g")
FREE_FLAVOR_RX = (r"(^| )(?:cok\b|coko|cokolad|choco|kakao|karamel|vanil|jagod|malin|banan|kokos|lijesn|ljesn|"
                  r"pistac|menta|mint\b|limun|naranc|visnj|borovnic|cimet|med\b|slani karamel)")
FREE_SNACK_RX = (r"(^| )(?:grickal|snack|kosaric|bar\b|barovi|pločic|plocic|chips|cips|keks|pralin|cokoladic|bombon|"
                 r"krem\b|protein|napitak|sladoled)")
FREE_MIN_PACK_SHARE = 0.25  # pakiranje manje od 25 % medijana pakiranja kandidata u gradu je porcija


def free_ok(name_norm: str, query: str) -> bool:
    """Proizvod ne smije imati okus ni oznaku grickalice kojih nema u upitu."""
    return all(not re.search(rx, name_norm) or re.search(rx, query) for rx in (FREE_FLAVOR_RX, FREE_SNACK_RX))


def _free_rows(con, need: "Need", city: str, wholesale: bool = False) -> dict[tuple, list[dict]]:
    """Kandidati po trgovini za slobodan naziv, kao find_products: samo provjerena hrana bez alkohola, a SVE
    riječi upita među prve tri riječi naziva proizvoda ("NUTELLA 400 g", a ne "KEKSI S NUTELLOM"); bez
    okusa i grickalica kojih nema u upitu (free_ok) i bez pakiranja manjih od FREE_MIN_PACK_SHARE medijana
    pakiranja kandidata u gradu. Bez namirnice nema slabih članova (match_quality je 'free_text')."""
    query = norm_text(need.input.get("name") or "") or ""
    tokens = _free_tokens(query)
    sql, params, _ = _candidates(None, tokens, None, city, include_clearance=False, food_sql=_food_filter(),
                                 include_wholesale=wholesale)
    early = " AND ".join("regexp_matches(name_norm, ?)" for _ in tokens)
    cur = con.execute(sql + f" SELECT * FROM x WHERE {early}",
                      params + ["^(?:[^ ]+ ){0,2}" + re.escape(t) for t in tokens])
    cols = [d[0] for d in cur.description]
    rows = []
    for r in (dict(zip(cols, row)) for row in cur.fetchall()):
        if not free_ok(r["name_norm"] or "", query):
            continue
        for k in ("price_eff", "price_per_unit", "pack_amount", "drained_amount", "n_units", "assumed_g"):
            r[k] = _num(r.get(k))
        rows.append(r)
    packs = sorted(r["pack_amount"] for r in rows if r.get("pack_unit") in ("g", "ml") and r.get("pack_amount"))
    floor = packs[len(packs) // 2] * FREE_MIN_PACK_SHARE if packs else 0
    by_store: dict[tuple, list[dict]] = {}
    for r in rows:
        if r.get("pack_unit") in ("g", "ml") and (r.get("pack_amount") or 0) < floor:
            continue
        by_store.setdefault((r["chain"], r["store_id"]), []).append(r)
    return by_store


def free_candidates(rows: list[dict], need: "Need", n: int = 3) -> list[dict]:
    """Do n proizvoda u trgovini za potvrdu slobodne pretrage, od najjeftinijeg pakiranja koje pokriva količinu."""
    picks, seen = [], set()
    for r in rows:
        if r["name"] not in seen and (p := choose_product([r], *_choose_args(need))):
            seen.add(r["name"])
            picks.append(p)
    return [{"product_id": p["product_id"], "name": p["name"], "pack_size": pack_size(p, need.unit),
             "n_packs": p["n_packs"], "cost_pack": p["cost_pack"]}
            for p in sorted(picks, key=lambda p: (p["cost_pack"], p["name"]))[:n]]


def suggestions(con, name: str, city: str | None, n: int = 3) -> list[str]:
    """Do n prijedloga za sastojak bez pogotka: slične namirnice iz rječnika, zatim proizvodi koji imaju
    barem jednu riječ naziva (najdulja riječ prva)."""
    q = norm_text(name) or ""
    synonyms = {syn: st.name for st in load_staples().values() for syn in st.synonyms}
    out = [synonyms[h] for h in difflib.get_close_matches(q, list(synonyms), n=n, cutoff=0.75)]
    for token in sorted(_free_tokens(name), key=len, reverse=True):
        if len(out) >= n:
            break
        try:  # bez pića ("ZMAJEVO VOĆE" ne predlaže sok)
            out += [r["name"] for r in find_products(token, city=city, limit=n + 5, con=con)
                    if r.get("food_group") not in ("pice", "alkohol")]
        except ValueError:
            continue
    return list(dict.fromkeys(out))[:n]


def _apply_overrides(store: dict, overrides: list[dict], out: dict) -> None:
    """Stvarna cijena pakiranja (korisnik) umjesto izračunate, za stavku po nazivu sastojka, namirnici ili
    nazivu proizvoda. cost_pack = cijena x broj pakiranja; cost_used u istom omjeru."""
    for ov in overrides:
        key = norm_text(str(ov.get("name") or ""))
        try:
            price = float(ov["cost_pack"])
        except (KeyError, TypeError, ValueError):
            out["warnings"].append(f"price_overrides: neispravna cijena za '{ov.get('name')}'")
            continue
        try:
            staple_key = resolve_name(ov.get("name") or "")[0].key
        except IngredientError:
            staple_key = None
        hits = [it for it in store["items"] if key and (
            norm_text(it["ingredient"] or "") == key or (staple_key and it["staple"] == staple_key)
            or key in norm_text(it["name"]))]
        if not hits:
            out["warnings"].append(f"price_overrides: '{ov.get('name')}' nije stavka košarice")
            continue
        for it in hits:
            n = it["n_packs"] or 1
            old = it["cost_pack"]
            it["computed_cost_pack"] = old
            it["cost_pack"] = round(price * n, 2)
            it["cost_used"] = round(it["cost_used"] * it["cost_pack"] / old, 2) if old else it["cost_pack"]
            it["user_provided"] = True
    set_totals(store, store["items"])


def plan_basket(ingredients: list[dict], city: str, mode: str = "single_store",
                con: duckdb.DuckDBPyConnection | None = None, max_stores: int | None = None,
                include_wholesale: bool = False, already_have: list[str] | None = None,
                store: dict | None = None, alternatives: bool = False,
                price_overrides: list[dict] | None = None) -> dict:
    """Cijena recepta po trgovini u gradu (+ nacionalne cijene) i najbolja trgovina.

    ingredients: [{"name": "brašno", "amount": 500, "unit": "g", "form": None, "attributes": {...}}]
    Vraća ingredients (povezani sastojci s pretpostavkama), unmatched, stores (svaka trgovina:
    stavke, total, broj povezanih sastojaka), best_store, warnings, date i date_hr.
    Veleprodaja (Metro, store_type 'cash_and_carry') je uključena samo uz include_wholesale=True.
    already_have: namirnice koje korisnik već ima ("sol", "papar"); ostaju u stavkama s have=true, ali ne
    ulaze u total_to_buy (cijela pakiranja za kupiti). total_used je razmjerni trošak svih stavki.
    store: {"chain": "konzum", "address_contains": "Starčevića"} ograničava rezultat na trgovine lanca
    (i adresu); nacionalne cijene istog lanca (dm, Lorenco) i dalje vrijede i popunjavaju sastojke koje
    lokalna trgovina nema. Bez pogotka: upozorenje i popis adresa lanca u gradu.
    alternatives: uz svaku stavku do 2 druga proizvoda u istoj trgovini (alternatives), s cijenom.
    price_overrides: [{"name": "brašno", "cost_pack": 1.2}]: stvarna cijena jednog pakiranja koju je
    korisnik vidio, samo za ovaj poziv i samo u trgovini iz `store` (inače u best_store). Stavka dobiva
    user_provided = true i preračunate cost_pack/cost_used; zbrojevi se preračunavaju, poredak ne.
    """
    if mode != "single_store":
        raise ValueError("podržan je samo mode='single_store'")
    store_spec = store  # `store` je niže varijabla petlje
    con = con or connect()
    out = {"city": city, "mode": mode, "ingredients": [], "unmatched": [], "ambiguous": [], "warnings": [],
           "stores": [], "best_store": None}
    resolved_city = resolve_city(city, con=con) if city else None
    if not resolved_city:
        out["city_suggestions"] = city_suggestions(con, city or "")
        out["warnings"].append(f"nepoznat grad '{city}'" + (
            f"; možda: {', '.join(out['city_suggestions'])}" if out["city_suggestions"] else ""))
        out["summary_hr"] = f"Nepoznat grad '{city}'."
        return out
    out["city"] = resolved_city
    have = set()
    free_names = {norm_text(i.get("name") or "") for i in ingredients if i.get("free_text")}
    have_text = set()  # already_have po nazivu, za sastojke izvan rječnika (free_text)
    for name in already_have or []:
        have_text.add(norm_text(name))
        try:
            have.add(resolve_name(name)[0].key)
        except IngredientError:
            if norm_text(name) not in free_names:
                out["warnings"].append(f"already_have: nepoznata namirnica '{name}'")
    out["already_have"] = sorted(have | (have_text & free_names))

    needs = []
    for item in ingredients:
        try:
            try:
                staple, attrs = resolve_name(item.get("name", ""))
            except IngredientError:
                if not item.get("free_text"):
                    raise
                # izvan rječnika: pretraga po nazivu u svakoj trgovini; bez pogotka ide u unmatched
                need = _free_need(item)
                need.free_rows = _free_rows(con, need, city, include_wholesale)
                if not need.free_rows:
                    out["unmatched"].append({
                        "name": item.get("name"), "free_text": True,
                        "reason": f"nijedan prehrambeni proizvod s nazivom '{item.get('name')}' u gradu",
                        "suggestions": suggestions(con, item.get("name") or "", city)})
                    continue
                needs.append(need)
                continue
            attrs.update(item.get("attributes") or {})
            for a, v in attrs.items():
                if v not in staple.attributes.get(a, {}):
                    raise IngredientError(f"nepoznat atribut {a}={v} za '{staple.name}'")
            amount, unit, warns = to_base(*_input_amount(item), staple)
            need = Need(item, staple, amount, unit, attrs, form=item.get("form"), warnings=warns,
                        brand=brand_in(item.get("name")))
            need.input_staple = staple.key  # prije oblika (rajčica -> pasirana_rajcica), za already_have
            need.warnings += _resolve_form(con, need, city, include_wholesale)
            if need.staple is not staple:  # oblik je druga namirnica: količina u njezinoj jedinici
                need.amount, need.unit, more = to_base(*_input_amount(item), need.staple)
                need.warnings += more
            need.warnings += apply_yield(need, need.form)
            needs.append(need)
        except IngredientError as e:
            entry = {"name": item.get("name"), "reason": str(e)}
            if str(e).startswith("nepoznata namirnica"):
                entry["suggestions"] = suggestions(con, item.get("name") or "", city)
                entry["hint"] = 'pošalji s "free_text": true za pretragu po nazivu proizvoda'
            out["unmatched"].append(entry)
        except FormAmbiguity as e:
            # bez oblika se ne računa: korisnik bira oblik ("form") i ponovi upit
            out["ambiguous"].append({"name": item.get("name"), "staple": staple.key, "amount": amount, "unit": unit,
                                     "ambiguity": e.ambiguity})
            # pitanje za korisnika; ostali sastojci se računaju bez ovoga
            out.setdefault("ask_user", []).append({
                "ingredient": item.get("name"), "question": f"{item.get('name')}: {e.ambiguity['question']}",
                "options": [{"form": f, "price_eur": e.ambiguity["prices"][f],
                             "amount": e.ambiguity["amounts"][f], "unit": e.ambiguity["unit"],
                             "price_note": "najjeftinije u gradu, za traženu količinu gotovog proizvoda"}
                            for f in e.ambiguity["form"]],
                "genitive": staple.genitive or item.get("name")})
            out["warnings"].append(f"'{item.get('name')}': {e.ambiguity['question']} (zadaj 'form'; nije uračunato)")

    stores: dict[tuple, dict] = {}
    store_rows: dict[tuple, list] = {}  # (trgovina, sastojak) -> kandidati, za alternative
    for idx, need in enumerate(needs):
        out["warnings"] += need.warnings
        if need.free_text:
            out["ingredients"].append({
                "name": need.input.get("name"), "staple": None, "free_text": True, "needs_confirmation": True,
                "amount": round(need.amount, 3),
                "unit": need.unit, "attributes": {}, "form": None, "assumed_form": None, "pantry": False,
                "warnings": need.warnings})
            for key, rows in need.free_rows.items():
                if pick := choose_product(rows, *_choose_args(need)):
                    store_rows[(key, idx)] = rows
                    _add_item(stores, key, rows, need, idx, pick, {}, [], norm_text(need.input.get("name") or "") in have_text)
                    # slobodna pretraga: korisnik potvrđuje proizvod, uz do 3 kandidata s cijenom
                    stores[key]["items"][idx].update(needs_confirmation=True, candidates=free_candidates(rows, need))
            continue
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
        attrs_of, attrs_of_ean = _product_attrs(con, need.staple)
        need.attr_fn = lambda p, a=attrs_of, e=attrs_of_ean: chosen_attributes(p, a, e)
        need.note_fn = lambda attrs, n=need: tier_note(n, attrs)
        prefs = {a: v for a, v in need.staple.default_preference.items() if a not in need.attributes}
        group_values = _group_values(con, need.staple, prefs)
        branded = set()  # trgovine u kojima je odabran proizvod tražene marke
        for key, rows in _prepare(con, need, city, include_wholesale).items():
            pick = None
            if need.brand:  # marka iz naziva sastojka ("nutella"): proizvod te marke ima prednost
                own = [r for r in rows if re.search(need.brand[1], r["name_norm"] or "")
                       or re.search(need.brand[1], norm_text(r.get("brand") or "") or "")]
                if own and (pick := _choose_preferred(own, need, prefs, group_values)) and pick["fallback"]:
                    pick = None
                if pick:
                    branded.add(key)
            pick = pick or _choose_preferred(rows, need, prefs, group_values)
            if pick is None:
                continue
            store_rows[(key, idx)] = rows
            chosen = chosen_attributes(pick, attrs_of, attrs_of_ean)
            wanted = {**need.staple.defaults(), **need.attributes}
            subst = [f"{a}={chosen[a]} umjesto {v} (zamjenjivo)" for a, v in wanted.items()
                     if not isinstance(v, tuple) and chosen.get(a) not in (None, v)
                     and chosen[a] in need.staple.accepted_values(a, v)]
            subst += [f"{a}={chosen[a]}: prva dostupna po zadanom redoslijedu ({', '.join(v)})"
                      for a, v in wanted.items() if isinstance(v, tuple) and chosen.get(a) not in (None, v[0])]
            if note := tier_note(need, chosen):
                subst.append(f"izvan zadanog izbora: {note}")
            _add_item(stores, key, rows, need, idx, pick, chosen, subst,
                      need.staple.key in have or need.input_staple in have)
            stores[key]["items"][idx].update(confirm_and_substitution(need, chosen, pick["name"]))
        if need.brand:
            _brand_substitutions(stores, idx, need, branded)

    if store_spec:
        stores = _filter_store(stores, store_spec, out)
    n_needs = len(needs)
    for s in stores.values():
        s["missing"] = [needs[i].input.get("name") for i in range(n_needs) if i not in s["items"]]
        items = [s["items"][i] for i in sorted(s["items"])]
        s["items"] = items
        s["n_matched"] = len(items)
        s["n_ingredients"] = n_needs
        set_totals(s, items)
        s["flagged_items"] = sum(1 for it in items if it["flags"])
        s["unit_confidence"] = "low" if any(it["unit_confidence"] != "high" for it in items) else "high"
        if s["scope"] == "national":
            s["note"] = NATIONAL_NOTE
        s.pop("date")
        # datum trgovine = najstarija cijena među stavkama (prenesena cijena ima stale_days > 0)
        oldest = min(items, key=lambda it: it["date"]) if items else None
        s["date"], s["date_hr"] = (oldest["date"], oldest["date_hr"]) if oldest else (None, None)
        s["stale_days"] = max((it["stale_days"] or 0 for it in items), default=0)
    in_city = Counter(s["chain"] for s in stores.values())  # trgovine lanca u gradu s barem jednim sastojkom
    merged = merge_same_chain(list(stores.values()))
    # preporuka: najviše povezanih sastojaka, zatim najmanji total_to_buy (total_used je samo informativan);
    # stavke sa zastavicama tek pri jednakoj cijeni
    ranked = sorted(merged, key=lambda s: (-s["n_matched"], s["data_quality"] == "suspect",
                                           s["total_to_buy"], s["flagged_items"]))
    out["stores"] = ranked[:max_stores] if max_stores else ranked
    out["comparison"], out["incomplete"] = compare_chains(ranked, in_city, n_needs)
    eligible = [s for s in ranked if s["data_quality"] != "suspect"] or ranked
    if eligible:
        out["best_store"] = eligible[0]
        if eligible[0]["data_quality"] == "suspect":
            out["warnings"].append("najbolja trgovina je lanac sa sumnjivim podacima (nema druge)")
    if alternatives and out["best_store"]:
        # alternative samo za trgovinu iz `store` (filtrirane su) ili najbolju; tražena marka iz druge trgovine
        # dolazi na kraj (other_store = true)
        s = out["best_store"]
        for it in s["items"]:
            rows = store_rows.get(((s["chain"], it.get("_from_store", s["store_id"])), it["_idx"]), [])
            it["alternatives"] = _alternatives(rows, needs[it["_idx"]], it)
            if brand_alt := it.get("_brand_alt"):
                it["alternatives"].append({**brand_alt, "delta_eur": round(brand_alt["cost_pack"] - it["cost_pack"], 2),
                                           "cheaper": brand_alt["cost_pack"] < it["cost_pack"]})
    for s in ranked:
        for it in s["items"]:
            it.pop("_idx", None)
            it.pop("_from_store", None)
            it.pop("_brand_alt", None)
    if price_overrides and out["best_store"]:
        _apply_overrides(out["best_store"], price_overrides, out)
    out["summary_hr"] = summary_hr(out["best_store"], out["ambiguous"], out.get("ask_user"))
    for q in out.get("ask_user", []):
        q.pop("genitive", None)
    dates = [s["date"] for s in ranked]
    if dates:
        out["date"] = max(dates)
        out["date_hr"] = next(s["date_hr"] for s in ranked if s["date"] == out["date"])
    return out


def _brand_substitutions(stores: dict, idx: int, need: Need, branded: set) -> None:
    """Trgovine bez tražene marke: stavka dobiva substitution {"requested", "chosen"}, a najjeftiniji proizvod
    marke iz druge trgovine u gradu ide kao alternativa (_brand_alt, vidi plan_basket)."""
    offers = [(stores[k]["items"][idx], stores[k]) for k in branded]
    best = min(offers, key=lambda o: o[0]["cost_pack"]) if offers else None
    for key, store in stores.items():
        it = store["items"].get(idx)
        if it is None or key in branded:
            continue
        it["substitution"] = {"requested": need.input.get("name"), "brand": need.brand[0], "chosen": it["name"]}
        if best:
            b, bs = best
            it["_brand_alt"] = {"product_id": b["product_id"], "ean": b["ean"], "name": b["name"],
                                "pack_size": b["pack_size"], "n_packs": b["n_packs"], "price_eff": b["price_eff"],
                                "cost_pack": b["cost_pack"], "cost_used": b["cost_used"], "brand": need.brand[0],
                                "other_store": True, "chain": bs["chain"], "address": bs["address"]}


def confirm_and_substitution(need: Need, chosen: dict, product: str) -> dict:
    """Polja stavke iz pravila namirnice: needs_confirmation kad odabrana vrijednost nije zadana
    (confirm_unless; kobasica bez dimljene u trgovini) i substitution kad je odabrana vrijednost zamjena
    (substitution_values; Grana Padano umjesto Parmigiano Reggiana), osim ako je tražena imenom."""
    out = {}
    for attr, value in need.staple.confirm_unless.items():
        if attr not in need.attributes and chosen.get(attr) != value:
            out["needs_confirmation"] = True
            out["confirm_note"] = (f"{need.staple.name}: odabrano {attr}={chosen.get(attr, 'nepoznato')}, jer "
                                   f"{value} nema u trgovini; potvrdi s korisnikom")
    name = norm_text(need.input.get("name") or "") or ""
    for attr, by_value in need.staple.substitution_values.items():
        rule = by_value.get(chosen.get(attr))
        if rule and not re.search(r"(^| )" + rule["unless"], name):
            out["substitution"] = {"requested": need.input.get("name"), "chosen": product, "note": rule["note"]}
    return out


def set_totals(store: dict, items: list[dict]) -> None:
    """Zbrojevi trgovine iz prikazanih (na cent zaokruženih) iznosa stavki: total_to_buy (cijela pakiranja) i
    total_used (utrošeni dio) samo za ono što korisnik nema; stavke iz already_have idu u from_stock_value
    (informativno, vrijednost utroška iz zalihe), pa je total_used točno zbroj redaka za kupiti (Korak 5B)."""
    buy = [it for it in items if not it["have"]]
    store["total_to_buy"] = round(sum(it["cost_pack"] for it in buy), 2)
    store["total_used"] = round(sum(it["cost_used"] for it in buy), 2)
    store["from_stock_value"] = round(sum(it["cost_used"] for it in items if it["have"]), 2)


def _add_item(stores: dict, key: tuple, rows: list[dict], need: Need, idx: int, pick: dict, chosen: dict,
              notes: list[str], have: bool) -> None:
    """Odabrani proizvod kao stavka trgovine `key` (trgovina se stvara pri prvoj stavci)."""
    first = rows[0]
    store = stores.setdefault(key, {
        "chain": first["chain"], "store_id": first["store_id"], "address": first["address"],
        "city": first["city"], "scope": first["scope"], "data_quality": first["data_quality"],
        "items": {}, "date": first["date"],
    })
    store["items"][idx] = {
        "ingredient": need.input.get("name"), "staple": need.staple.key if need.staple else None,
        "need": round(need.amount, 3), "need_unit": need.unit, "product_id": pick["product_id"],
        "ean": pick["ean_norm"], "name": pick["name"], "attributes": chosen,
        "pack_size": pack_size(pick, need.unit), "pack_qty": pick["qty"], "n_packs": pick["n_packs"],
        "price_eff": pick["price_eff"], "cost_pack": pick["cost_pack"], "cost_used": pick["cost_used"],
        "have": have, "pantry": bool(need.staple and need.staple.pantry),
        "price_per_unit": pick["price_per_unit"], "per_unit": pick["per_unit"],
        "unit_confidence": pick["unit_confidence"], "pack_source": pick["pack_source"],
        "is_special": pick["is_special"], "flags": pick["flags"], "notes": pick["notes"] + notes + (
            [f"rinfuza {format_pack(pick['pack_amount'], 'g')} (gramatura iz: {pick['pack_source']}): utrošak je udio "
             f"{need.amount * pick['bulk_sachet_g']:g} g od {pick['pack_amount']:g} g"] if pick.get("bulk_sachet_g") else []),
        "fallback": pick["fallback"], "food_unverified": pick["is_food"] is None,
        "date": pick["date"].isoformat(), "date_hr": date_hr(pick["date"]), "stale_days": pick["stale_days"],
        "match_quality": "free_text" if need.free_text else pick.get("match_quality"),
        "by_weight_fallback": pick["by_weight_fallback"], "_idx": idx,
    }


MAX_ADDRESSES = 3


COMPARE_MIN_SHARE, COMPARE_ROWS, COMPARE_ADDRESSES = 0.8, 6, 2


def compare_chains(ranked: list[dict], in_city: Counter, n_needs: int) -> tuple[list[dict], list[dict]]:
    """Usporedba lanaca: po jedan redak (najjeftinija trgovina lanca s najviše sastojaka) za lance s >= 80 %
    povezanih sastojaka, od najmanjeg total_to_buy, najviše COMPARE_ROWS redaka i COMPARE_ADDRESSES adrese;
    ostali lanci idu u incomplete s popisom onoga što nedostaje ("nedostaje: X, Y")."""
    best: dict[str, dict] = {}
    for s in ranked:  # ranked: najviše sastojaka, pa najmanji total_to_buy
        best.setdefault(s["chain"], s)
    rows, incomplete = [], []
    for s in sorted(best.values(), key=lambda s: (-s["n_matched"], s["total_to_buy"])):
        if n_needs and s["n_matched"] / n_needs >= COMPARE_MIN_SHARE and len(rows) < COMPARE_ROWS:
            addresses = [a for a in (s.get("addresses") or [s["address"]]) if a][:COMPARE_ADDRESSES]
            rows.append({"chain": s["chain"], "addresses": addresses,
                         "n_stores_city": in_city.get(s["chain"], 1), "total_to_buy": s["total_to_buy"],
                         "total_used": s["total_used"], "n_matched": s["n_matched"], "n_ingredients": n_needs,
                         "complete": not s["missing"], **({"missing": s["missing"]} if s["missing"] else {})})
        else:
            incomplete.append({"chain": s["chain"], "n_matched": s["n_matched"], "missing": s["missing"],
                               "note": "nedostaje: " + ", ".join(s["missing"])})
    return rows, incomplete


def merge_same_chain(stores: list[dict]) -> list[dict]:
    """Trgovine istog lanca (i opsega) s istim proizvodima, količinama, zbrojevima i datumom postaju jedan
    unos: prva po adresi, uz n_stores i addresses (prve MAX_ADDRESSES adrese)."""
    groups: dict[tuple, list[dict]] = {}
    for s in stores:
        key = (s["chain"], s["scope"], s["total_to_buy"], s["total_used"], s["date"], tuple(s["missing"]),
               tuple((it["product_id"], it["n_packs"], it["cost_pack"], it["have"]) for it in s["items"]))
        groups.setdefault(key, []).append(s)
    out = []
    for group in groups.values():
        group.sort(key=lambda s: (s["address"] or "", s["store_id"]))
        rep = group[0]
        rep["n_stores"] = len(group)
        rep["addresses"] = [s["address"] for s in group[:MAX_ADDRESSES] if s["address"]]
        out.append(rep)
    return out


def _eur(x: float) -> str:
    return f"{x:.2f}".replace(".", ",") + " €"


def summary_hr(best: dict | None, ambiguous: list[dict] | None = None, ask: list[dict] | None = None) -> str:
    """Dvije rečenice za korisnika: cijena cijelih pakiranja i stvarno utrošenog dijela. Uz dvosmislen sastojak
    (ask_user) košarica je bez njega: "Bez graha: za kupiti X €, stvarno utrošeno Y €." Bez košarice: pitanje
    o obliku ako ga ima, inače da nijedna trgovina nema sastojke."""
    if not best:
        if ambiguous:
            return "Prije izračuna treba odgovor: " + "; ".join(
                f"{a['name']}: {a['ambiguity']['question']}" for a in ambiguous)
        return "Nijedna trgovina u gradu nema ove sastojke."
    if ask:
        names = [q.get("genitive") or q["ingredient"] for q in ask]
        joined = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " i " + names[-1]
        return (f"Bez {joined}: za kupiti {_eur(best['total_to_buy'])}, stvarno utrošeno "
                f"{_eur(best['total_used'])}.")
    return f"Za kupiti: {_eur(best['total_to_buy'])}. Stvarno utrošeno: {_eur(best['total_used'])}."
