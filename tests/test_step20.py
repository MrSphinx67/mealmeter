"""Korak 20: prazan store_id ne ruši bazu. Arhiva 21.11.2026., jadranka_trgovina: 8 od 18 trgovina u stores.csv i
34.462 od 133.151 retka cijena (25,9 %) bez šifre trgovine (šifra u stupcu address, grad "Roba"); jučer (20.11.) su
te trgovine (051, 508, 511, 513, 539, 540, 554, 558) imale 34.459 redaka. build_compact je padao na provjeri view-ova
(10.458 čistih cijena bez trgovine). Takvi retci se preskaču uz upozorenje (carry-forward po trgovini), a lanac s više
od MAX_EMPTY_STORE_SHARE takvih redaka izostavlja se, kao da nije objavio cjenik.

tests/fixtures/jadranka_2026-11: stvarni stores.csv oba dana (doslovno) i doslovni retci cijena i proizvoda za 40
šifri (svaka 400. šifra 21.11.), u svim trgovinama."""

import importlib.util
import shutil
import zipfile
from pathlib import Path

import duckdb
import pytest

from mealmeter.build import MAX_EMPTY_STORE_SHARE, describe_empty_stores, load_raw
from mealmeter.update import run
from tests.test_update import FIXTURE, q

ROOT = Path(__file__).resolve().parents[1]
REAL = Path(__file__).parent / "fixtures" / "jadranka_2026-11"
CHAIN = "jadranka_trgovina"
LOST = ["051", "508", "511", "513", "539", "540", "554", "558"]  # trgovine bez šifre 21.11.
EXPECTED = {"chain": CHAIN, "prices": 85, "total": 303, "pct": 100 * 85 / 303, "stores": 8, "stores_total": 18,
            "dropped": False}


def _load(root: Path):
    # štedi memoriju (Korak 20): 1 GB i 1 dretva, kao lokalna provjera bez pune baze
    con, bad, empty = duckdb.connect(config={"memory_limit": "1GB", "threads": 1}), [], []
    chains = load_raw(con, root, "2026-11-21", bad, empty)
    return con, chains, empty


def test_threshold_constant():
    assert MAX_EMPTY_STORE_SHARE == 0.5


def test_real_21_11_rows_and_stores_skipped():
    con, chains, empty = _load(REAL / "2026-11-21")
    assert chains == [CHAIN] and empty == [EXPECTED]
    assert con.execute("SELECT count(*) FROM prices WHERE trim(coalesce(store_id, '')) = ''").fetchone()[0] == 0
    assert con.execute("SELECT count(*) FROM stores WHERE trim(coalesce(store_id, '')) = ''").fetchone()[0] == 0
    assert con.execute("SELECT count(*) FROM prices").fetchone()[0] == 303 - 85
    assert con.execute("SELECT count(*) FROM stores").fetchone()[0] == 10
    assert describe_empty_stores(EXPECTED) == (
        "jadranka_trgovina: 85 od 303 redaka cijena bez store_id (28.05 %), trgovina bez šifre 8 od 18; "
        "retci preskočeni (carry-forward po trgovini)")


RAW = ROOT / "data" / "raw" / "2026-11-21" / CHAIN


@pytest.mark.skipif(not (RAW / "prices.csv").exists(), reason="stvarna arhiva 21.11.2026. nije lokalno raspakirana")
def test_real_full_archive_counts(tmp_path):
    """Cijela stvarna datoteka (kad je arhiva lokalno): 34.462 od 133.151 retka, 8 od 18 trgovina, ispod praga.
    Učitava samo jadrankine CSV-ove (simbolička veza), ne cijelu arhivu."""
    (tmp_path / CHAIN).symlink_to(RAW, target_is_directory=True)
    con, chains, empty = _load(tmp_path)
    assert chains == [CHAIN] and len(empty) == 1
    e = empty[0]
    assert (e["prices"], e["total"], e["stores"], e["stores_total"], e["dropped"]) == (34462, 133151, 8, 18, False)


def _write(root: Path, rows_fn=None):
    """Kopija stvarnog dana; `rows_fn` mijenja retke cijena (bez zaglavlja)."""
    d = root / CHAIN
    shutil.copytree(REAL / "2026-11-21" / CHAIN, d)
    if rows_fn:
        lines = (d / "prices.csv").read_bytes().splitlines(keepends=True)
        (d / "prices.csv").write_bytes(lines[0] + b"".join(rows_fn(lines[1:])))
    return root


def _blank(lines, keep: int):
    """Prvih `keep` redaka s trgovinom zadrži, ostalima obriši store_id."""
    out, kept = [], 0
    for line in lines:
        if not line.startswith(b",") and kept < keep:
            kept += 1
            out.append(line)
        elif line.startswith(b","):
            out.append(line)
        else:
            out.append(b"," + line.split(b",", 1)[1])
    return out


def test_at_threshold_rows_skipped_above_chain_dropped(tmp_path):
    # točno pola redaka bez store_id: retci preskočeni, lanac ostaje
    half = _write(tmp_path / "half", lambda ls: _blank(ls, keep=len(ls) // 2 + len(ls) % 2))
    lines = (half / CHAIN / "prices.csv").read_bytes().splitlines()[1:]
    assert sum(ln.startswith(b",") for ln in lines) * 2 <= len(lines)
    con, chains, empty = _load(half)
    assert chains == [CHAIN] and not empty[0]["dropped"]
    # više od pola: lanac se ne učitava (ni trgovine ni proizvodi), bez iznimke
    over = _write(tmp_path / "over", lambda ls: _blank(ls, keep=10))
    other = over / "aaa"  # lanac ispred njega: tablice nastaju i kad je izostavljen prvi učitani lanac
    shutil.copytree(FIXTURE / "dm", other)
    con, chains, empty = _load(over)
    assert chains == ["aaa"] and empty[0]["dropped"] and empty[0]["pct"] > 50
    assert con.execute(f"SELECT count(*) FROM stores WHERE chain = '{CHAIN}'").fetchone()[0] == 0
    assert con.execute(f"SELECT count(*) FROM products WHERE chain = '{CHAIN}'").fetchone()[0] == 0
    assert "lanac izostavljen (carry-forward kao da nije objavio cjenik)" in describe_empty_stores(empty[0])


def test_only_chain_dropped_raises(tmp_path):
    with pytest.raises(ValueError, match="nijedan lanac"):
        _load(_write(tmp_path / "x", lambda ls: _blank(ls, keep=0)))


# --- update.py: dva dana, kao u workflowu ---------------------------------------------------------------------

def _zip(path: Path, tmp: Path, day: str, rows_fn=None) -> Path:
    root = tmp / path.stem
    shutil.copytree(FIXTURE, root)
    shutil.copytree(REAL / day / CHAIN, root / CHAIN)
    if rows_fn:
        p = root / CHAIN / "prices.csv"
        lines = p.read_bytes().splitlines(keepends=True)
        p.write_bytes(lines[0] + b"".join(rows_fn(lines[1:])))
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(root.rglob("*.csv")):
            z.write(f, f.relative_to(root))
    return path


@pytest.fixture
def env(tmp_path, monkeypatch, step_summary):
    db = tmp_path / "db" / "mealmeter.duckdb"
    db.parent.mkdir()
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    base = ["--db", str(db), "--data-dir", str(tmp_path / "raw"), "--seed-date", ""]
    assert run(base + ["--archive", str(_zip(tmp_path / "d20.zip", tmp_path, "2026-11-20")), "--date",
                       "2026-11-20"]) == 0
    return {"db": db, "base": base, "tmp": tmp_path, "summary": step_summary}


def _build_compact():
    spec = importlib.util.spec_from_file_location("bc", ROOT / "scripts" / "build_compact.py")
    bc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bc)
    return bc


def test_update_real_21_11_warns_and_carries_lost_stores(env, capsys):
    """Stvarni slučaj: baza se gradi, ::warning:: i redak u sažetku; 8 trgovina bez šifre dobiva cijene od 20.11.
    (carry-forward po trgovini), nijedna cijena bez trgovine, a build_compact prolazi provjeru view-ova."""
    capsys.readouterr()
    before = dict(q(env["db"], f"""SELECT store_id, count(*) FROM main.prices WHERE chain = '{CHAIN}'
                                   AND store_id IN ({", ".join(f"'{s}'" for s in LOST)}) GROUP BY ALL"""))
    assert sorted(before) == LOST
    archive = _zip(env["tmp"] / "d21.zip", env["tmp"], "2026-11-21")
    assert run(env["base"] + ["--archive", str(archive), "--date", "2026-11-21"]) == 0
    out = capsys.readouterr().out
    line = describe_empty_stores(EXPECTED)
    assert f"::warning title=Prazan store_id {CHAIN}::{line}" in out and f"  ! {line}" in out
    assert "::error" not in out
    assert f"**Prazan store_id, {CHAIN}:** {line}" in env["summary"].read_text(encoding="utf-8")
    db = env["db"]
    assert q(db, "SELECT count(*) FROM clean.prices WHERE store_id IS NULL OR trim(store_id) = ''")[0][0] == 0
    assert q(db, "SELECT count(*) FROM main.stores WHERE store_id IS NULL OR trim(store_id) = ''")[0][0] == 0
    carried = dict(q(db, f"""SELECT store_id, count(*) FROM main.prices WHERE chain = '{CHAIN}'
                             AND date = DATE '2026-11-20' GROUP BY ALL"""))
    assert carried == before  # svih 8 trgovina, sve njihove cijene od jučer
    assert q(db, f"SELECT count(*) FROM main.prices WHERE chain = '{CHAIN}' AND date = DATE '2026-11-21'")[0][0] \
        == 303 - 85
    # trgovine i dalje postoje s adresom od 20.11. (ne "Roba")
    assert q(db, f"SELECT address, city FROM main.stores WHERE chain = '{CHAIN}' AND store_id = '051'") == \
        [("Zaglav 31", "Martinšćica")]
    _build_compact().build(db, env["tmp"] / "compact.duckdb")  # SystemExit kad view ≠ puna baza


def test_update_above_threshold_chain_carried_as_missing(env, capsys):
    """> 50 % redaka bez store_id: lanac izostavljen, cijeli lanac nasljeđuje cijene od 20.11. (chain_report: nema u
    arhivi), exit 0 i upozorenje umjesto pada baze."""
    capsys.readouterr()
    n_before = q(env["db"], f"SELECT count(*) FROM main.prices WHERE chain = '{CHAIN}'")[0][0]
    archive = _zip(env["tmp"] / "d21b.zip", env["tmp"], "2026-11-21", lambda ls: _blank(ls, keep=10))
    assert run(env["base"] + ["--archive", str(archive), "--date", "2026-11-21"]) == 0
    out = capsys.readouterr().out
    assert f"::warning title=Prazan store_id {CHAIN}::" in out and "lanac izostavljen" in out
    assert f"::warning title=Lanac {CHAIN}::{CHAIN}: nema u arhivi 1. dan" in out
    assert "::error" not in out
    db = env["db"]
    assert q(db, f"SELECT count(*), max(date) FROM main.prices WHERE chain = '{CHAIN}'")[0] == \
        (n_before, __import__("datetime").date(2026, 11, 20))
    assert q(db, "SELECT count(*) FROM clean.prices WHERE store_id IS NULL")[0][0] == 0
    _build_compact().build(db, env["tmp"] / "compact.duckdb")
