"""Kuhinjske mjere (žlica, šalica...) i gustoće namirnica iz data/units.yaml.

Sve vrijednosti su procjene; convert() zato uvijek vraća i upozorenje s korištenom vrijednošću.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from mealmeter.normalize import norm_text

UNITS_PATH = Path(__file__).resolve().parents[2] / "data" / "units.yaml"


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


def piece_weight(staple_key: str) -> float | None:
    """Procijenjena masa jednog komada namirnice u g (data/units.yaml, pieces), ili None."""
    return load_units().pieces.get(staple_key)


def is_measure(unit: str | None) -> bool:
    return norm_text(unit or "") in load_units().measures


def convert(amount: float, unit: str, staple) -> tuple[float, str, list[str]]:
    """Količina u kuhinjskoj mjeri -> (količina, "g" | "ml", upozorenja) za namirnicu `staple`
    (Staple ili ključ). Namirnica u kg dobiva grame preko gustoće (g/ml; bez gustoće 1 g/ml),
    a namirnica u l mililitre. Namirnica u komadima (jaja) ne može se mjeriti žlicom: ValueError."""
    units = load_units()
    key = norm_text(unit or "")
    if key not in units.measures:
        raise ValueError(f"nepoznata mjera '{unit}'; poznate: {', '.join(sorted(set(units.names.values())))}")
    staple_key = getattr(staple, "key", staple)
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
