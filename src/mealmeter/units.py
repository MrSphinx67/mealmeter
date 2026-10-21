"""Kuhinjske mjere (žlica, šalica...) i gustoće namirnica iz data/units.yaml.

Sve vrijednosti su procjene; convert() zato uvijek vraća i upozorenje s korištenom vrijednošću.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from mealmeter.normalize import norm_text

UNITS_PATH = Path(__file__).resolve().parents[2] / "data" / "units.yaml"
YIELDS_PATH = Path(__file__).resolve().parents[2] / "data" / "yields.yaml"


@dataclass(frozen=True)
class Units:
    measures: dict[str, float]  # norm_text(alias) -> ml
    names: dict[str, str]  # norm_text(alias) -> ključ mjere (zlica, salica...)
    densities: dict[str, float]  # namirnica -> g/ml
    pieces: dict[str, float]  # namirnica -> g po komadu (luk, češanj češnjaka, vezica peršina)


@lru_cache(maxsize=2)
def load_units(path: Path = UNITS_PATH) -> Units:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    measures, names = {}, {}
    for key, m in raw["measures"].items():
        for alias in [key, *m.get("aliases", [])]:
            measures[norm_text(alias)] = float(m["ml"])
            names[norm_text(alias)] = key
    densities = {k: float(v["g_per_ml"]) for k, v in (raw.get("densities") or {}).items()}
    pieces = {k: float(v["g"]) for k, v in (raw.get("pieces") or {}).items()}
    return Units(measures, names, densities, pieces)


@lru_cache(maxsize=2)
def load_yields(path: Path = YIELDS_PATH) -> dict[str, dict[str, float]]:
    """Prinos oblika (data/yields.yaml, procjene): {namirnica: {oblik: g gotovog po g u obliku}}."""
    if not Path(path).exists():
        return {}
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return {k: {f: float(v["factor"]) for f, v in forms.items()} for k, forms in raw.items()}


def yield_factor(staple_key: str, form: str | None) -> float | None:
    """Faktor gotovo/oblik (suhi grah 2,5), ili None (1:1 ili nepoznato)."""
    return load_yields().get(staple_key, {}).get(form or "")


def piece_weight(staple_key: str) -> float | None:
    """Procijenjena masa jednog komada namirnice u g (data/units.yaml, pieces), ili None."""
    return load_units().pieces.get(staple_key)


def is_measure(unit: str | None) -> bool:
    return norm_text(unit or "") in load_units().measures


# komad u receptu: masa iz pieces (luk, češanj češnjaka, vezica peršina...)
PIECE_UNITS = {"kom", "komad", "komada", "komadi", "kos", "glavica", "glavice", "cesanj", "cesnja", "cesnjeva",
               "rezanj", "rezanja", "vezica", "vezice", "list", "lista", "listova", "listic"}


def is_piece(unit: str | None) -> bool:
    return norm_text(unit or "") in PIECE_UNITS


def convert(amount: float, unit: str, staple) -> tuple[float, str, list[str]]:
    """Količina u kuhinjskoj mjeri ili komadima -> (količina, "g" | "ml", upozorenja) za namirnicu
    `staple` (Staple ili ključ). Mjera: namirnica u kg dobiva grame preko gustoće (g/ml; bez gustoće
    1 g/ml), a namirnica u l mililitre. Komad ("kom", "glavica", "češanj", "vezica"): grami iz pieces;
    namirnica bez mase komada daje ValueError, kao i žlica za namirnicu u komadima (jaja)."""
    units = load_units()
    key = norm_text(unit or "")
    staple_key = getattr(staple, "key", staple)
    if key in PIECE_UNITS:
        g = units.pieces.get(staple_key)
        if g is None:
            raise ValueError(f"nema procijenjene mase komada za '{staple_key}' (data/units.yaml, pieces)")
        return amount * g, "g", [f"{amount:g} {unit} ≈ {amount * g:g} g (procjena, komad {g:g} g)"]
    if key not in units.measures:
        raise ValueError(f"nepoznata mjera '{unit}'; poznate: {', '.join(sorted(set(units.names.values())))}")
    staple_unit = getattr(staple, "unit", "kg")
    ml = amount * units.measures[key]
    label = f"{amount:g} {unit} ≈ {ml:g} ml"
    if staple_unit == "l":
        return ml, "ml", [f"{label} (procjena)"]
    if staple_unit != "kg":
        raise ValueError(f"mjera '{unit}' ne može se pretvoriti u {staple_unit} za '{staple_key}'")
    density = units.densities.get(staple_key)
    if density is None:
        return ml, "g", [f"{label} ≈ {ml:g} g (procjena, gustoća 1 g/ml)"]
    return ml * density, "g", [f"{label} ≈ {ml * density:g} g (procjena, {density:g} g/ml)"]
