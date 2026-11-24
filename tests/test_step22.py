"""Korak 22: lanac s datotekom koja nedostaje, prazna je ili nečitljiva ne ruši bazu. Arhiva 24.11.2026.,
trgovina-krk: mapa lanca postoji, ali ima samo stores.csv (1098 B, 14 trgovina, isti kao 21.11.); products.csv i
prices.csv nema, pa je update pao na "IO Error: No files found that match the pattern .../trgovina-krk/prices.csv"
(provjera praznog store_id). Takav lanac se izostavlja kao da taj dan nije objavio cjenik: ::warning::, redak u
GITHUB_STEP_SUMMARY, carry-forward lanca, a izgradnja se nastavlja.

tests/fixtures/krk_2026-11-24/trgovina-krk/stores.csv: stvarna datoteka iz arhive 24.11. (doslovno). Ostalo su
sintetičke izmjene fixture-arhive; ništa ne gradi punu bazu."""

import datetime as dt
import shutil
import zipfile
from pathlib import Path

import duckdb
import pytest

from mealmeter.build import CHAIN_FILES, chain_file_problems, describe_broken_chain, load_raw
from mealmeter.update import extract, remember_fields, run
from tests.test_update import FIXTURE, q

ROOT = Path(__file__).resolve().parents[1]
KRK = "trgovina-krk"
REAL = Path(__file__).parent / "fixtures" / "krk_2026-11-24"
REAL_PROBLEMS = ["nedostaje products.csv", "nedostaje prices.csv"]


def _con():
    # štedi memoriju: 1 GB i 1 dretva, kao lokalna provjera bez pune baze
    return duckdb.connect(config={"memory_limit": "1GB", "threads": 1})


def _archive(root: Path, change=None) -> Path:
    """Kopija fixture-arhive; `change(chain_dir)` mijenja datoteke trgovine-krk."""
    shutil.copytree(FIXTURE, root)
    if change:
        change(root / KRK)
    return root


def _load(root: Path):
    con, bad, empty, broken = _con(), [], [], []
    chains = load_raw(con, root, "2026-11-24", bad, empty, broken)
    return con, chains, broken


def _real_krk(d: Path):
    shutil.rmtree(d)
    shutil.copytree(REAL / KRK, d)


def _drop(name: str):
    return lambda d: (d / name).unlink()


def _empty(name: str):
    return lambda d: (d / name).write_bytes(b"")


def _header_only(name: str):
    return lambda d: (d / name).write_bytes((d / name).read_bytes().splitlines(keepends=True)[0])


def _assert_skipped(con, chains, broken, problems):
    all_chains = sorted(p.name for p in FIXTURE.iterdir() if p.is_dir())
    assert chains == [c for c in all_chains if c != KRK]
    assert broken == [{"chain": KRK, "problems": problems}]
    for t in ("stores", "products", "prices"):
        assert con.execute(f"SELECT count(*) FROM {t} WHERE chain = '{KRK}'").fetchone()[0] == 0
        assert con.execute(f"SELECT count(DISTINCT chain) FROM {t}").fetchone()[0] == len(chains)


def test_real_24_11_krk_has_only_stores():
    files = sorted(p.name for p in (REAL / KRK).iterdir())
    assert files == ["stores.csv"] and (REAL / KRK / "stores.csv").stat().st_size == 1098
    con = _con()
    assert chain_file_problems(con, REAL, KRK) == REAL_PROBLEMS
    assert describe_broken_chain({"chain": KRK, "problems": REAL_PROBLEMS}) == (
        "trgovina-krk: nedostaje products.csv; nedostaje prices.csv; lanac izostavljen (carry-forward kao da nije "
        "objavio cjenik)")


@pytest.mark.parametrize("change, problems", [
    (_real_krk, REAL_PROBLEMS),
    (_drop("prices.csv"), ["nedostaje prices.csv"]),
    (_drop("stores.csv"), ["nedostaje stores.csv"]),
    (_drop("products.csv"), ["nedostaje products.csv"]),
    (_empty("prices.csv"), ["prices.csv prazna (0 B)"]),
    (_empty("stores.csv"), ["stores.csv prazna (0 B)"]),
    (_header_only("prices.csv"), ["prices.csv prazna (samo zaglavlje)"]),
    (_header_only("products.csv"), ["products.csv prazna (samo zaglavlje)"]),
], ids=["real-24-11", "no-prices", "no-stores", "no-products", "empty-prices", "empty-stores", "header-prices",
        "header-products"])
def test_load_raw_skips_chain(tmp_path, change, problems):
    con, chains, broken = _load(_archive(tmp_path / "a", change))
    _assert_skipped(con, chains, broken, problems)


def test_missing_column_is_unreadable(tmp_path):
    def change(d):
        p = d / "prices.csv"
        p.write_text(p.read_text().replace("store_id,", "trgovina,", 1))
    con, chains, broken = _load(_archive(tmp_path / "a", change))
    _assert_skipped(con, chains, broken, ["prices.csv nečitljiva (nema stupaca store_id)"])


def test_binary_garbage_is_unreadable(tmp_path):
    con, chains, broken = _load(_archive(tmp_path / "a", lambda d: (d / "stores.csv").write_bytes(
        b"\x00\xff\xfe" * 100)))
    assert chains and broken[0]["chain"] == KRK and "stores.csv" in broken[0]["problems"][0]
    assert "nečitljiva" in broken[0]["problems"][0] or "prazna" in broken[0]["problems"][0]


def test_csv_error_late_in_file_rolls_back_chain(tmp_path):
    """Kvar tek iza uzorka sniffera (nezatvoreni navodnik u zadnjem retku): provjera zaglavlja prolazi, učitavanje
    pada usred lanca; transakcija se poništi, nijedan redak lanca ne ostaje, a lanac ispred i iza se učitavaju.
    Lanac je prvi (aaa), pa tablice nastaju tek sa sljedećim lancem."""
    def change(d):
        shutil.move(d, d.parent / "aaa")
        d = d.parent / "aaa"
        p = d / "prices.csv"
        head, row = p.read_text().splitlines()[:2]
        store, _, rest = row.partition(",")
        _, _, rest = rest.partition(",")
        rows = [f"{store},{i:07d},{rest}" for i in range(60_000)]
        p.write_text("\n".join([head, *rows, f'{store},9999999,"1.09,2.18,,1.09,']) + "\n")
    root = _archive(tmp_path / "a", change)
    assert chain_file_problems(_con(), root, "aaa") == []
    con, chains, broken = _load(root)
    assert "aaa" not in chains and len(chains) == len([p for p in FIXTURE.iterdir() if p.is_dir()]) - 1
    assert len(broken) == 1 and broken[0]["chain"] == "aaa"
    assert broken[0]["problems"][0].startswith("nečitljiva datoteka (")
    for t in ("stores", "products", "prices"):
        assert con.execute(f"SELECT count(*) FROM {t} WHERE chain = 'aaa'").fetchone()[0] == 0


def test_all_chains_broken_raises(tmp_path):
    root = tmp_path / "a"
    (root / KRK).mkdir(parents=True)
    shutil.copy(REAL / KRK / "stores.csv", root / KRK)
    with pytest.raises(ValueError, match="nijedan lanac"):
        _load(root)


def test_extra_and_reordered_columns_load_by_name(tmp_path):
    """stores/products se učitavaju po nazivu stupca (CHAIN_FILES), pa dodatni ili drukčije poredani stupci ne
    pomiču vrijednosti."""
    def change(d):
        (d / "stores.csv").write_text("city,store_id,novo,type,address,zipcode\n"
                                      "Krk,set._sv._bernardina_6c_krk,x,supermarket,Set. sv. Bernardina 6C,\n")
    con, chains, broken = _load(_archive(tmp_path / "a", change))
    assert KRK in chains and not broken
    assert con.execute(f"SELECT store_id, type, address, city FROM stores WHERE chain = '{KRK}'").fetchall() == [
        ("set._sv._bernardina_6c_krk", "supermarket", "Set. sv. Bernardina 6C", "Krk")]
    assert [r[0] for r in con.execute("DESCRIBE stores").fetchall()] == ["chain", *CHAIN_FILES["stores.csv"]]


def test_extract_keeps_chain_dir_without_prices(tmp_path):
    """Arhiva s jednim lancem bez prices.csv nije "arhiva s jednom korijenskom mapom"."""
    z = tmp_path / "a.zip"
    with zipfile.ZipFile(z, "w") as f:
        f.write(REAL / KRK / "stores.csv", f"{KRK}/stores.csv")
    root = extract(z, tmp_path / "x")
    assert root == tmp_path / "x" and (root / KRK / "stores.csv").exists()


def test_seed_skips_empty_products(tmp_path):
    seed = tmp_path / "seed"
    shutil.copytree(FIXTURE, seed)
    (seed / KRK / "products.csv").write_bytes(b"")
    (seed / "dm" / "products.csv").write_bytes(b"product_id,barcode\n1,2\n")  # bez stupaca
    con = _con()
    load_raw(con, FIXTURE, "2026-11-24")
    remember_fields(con, None, "2026-11-24", seed)  # ne pada
    assert con.execute("SELECT count(*) FROM clean.product_fields").fetchone()[0] > 0


# --- update.py: dva dana, kao u workflowu ---------------------------------------------------------------------

def _zip(path: Path, tmp: Path, change=None) -> Path:
    root = _archive(tmp / path.stem, change)
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(p for p in root.rglob("*") if p.is_file()):
            z.write(f, f.relative_to(root))
    return path


@pytest.fixture
def env(tmp_path, monkeypatch, step_summary):
    db = tmp_path / "db" / "mealmeter.duckdb"
    db.parent.mkdir()
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    base = ["--db", str(db), "--data-dir", str(tmp_path / "raw"), "--seed-date", ""]
    assert run(base + ["--archive", str(_zip(tmp_path / "d23.zip", tmp_path)), "--date", "2026-11-23"]) == 0
    return {"db": db, "base": base, "tmp": tmp_path, "summary": step_summary}


@pytest.mark.parametrize("change, problems", [
    (_real_krk, REAL_PROBLEMS),
    (_drop("stores.csv"), ["nedostaje stores.csv"]),
    (_empty("prices.csv"), ["prices.csv prazna (0 B)"]),
], ids=["real-24-11", "no-stores", "empty-prices"])
def test_update_warns_and_carries_chain(env, capsys, change, problems):
    capsys.readouterr()
    db = env["db"]
    before = q(db, f"SELECT store_id, product_id, price FROM main.prices WHERE chain = '{KRK}' ORDER BY ALL")
    assert before
    archive = _zip(env["tmp"] / "d24.zip", env["tmp"], change)
    assert run(env["base"] + ["--archive", str(archive), "--date", "2026-11-24"]) == 0
    out = capsys.readouterr().out
    line = describe_broken_chain({"chain": KRK, "problems": problems})
    assert f"::warning title=Datoteke lanca {KRK}::{line}" in out and f"  ! {line}" in out
    assert f"::warning title=Lanac {KRK}::{KRK}: nema u arhivi 1. dan" in out
    assert "::error" not in out
    assert f"**Datoteke lanca, {KRK}:** {line}" in env["summary"].read_text(encoding="utf-8")
    # carry-forward lanca: cijene od 23.11. ostaju, i u čistim cijenama (stale)
    assert q(db, f"SELECT store_id, product_id, price FROM main.prices WHERE chain = '{KRK}' ORDER BY ALL") == before
    assert q(db, f"SELECT DISTINCT date FROM main.prices WHERE chain = '{KRK}'") == [(dt.date(2026, 11, 23),)]
    assert q(db, f"SELECT count(*) FROM clean.prices WHERE chain = '{KRK}'")[0][0] == len(before)
    assert q(db, "SELECT max(date) FROM clean.archive_info")[0][0] == dt.date(2026, 11, 24)
    assert q(db, "SELECT count(*) FROM main.prices WHERE date = DATE '2026-11-24'")[0][0] > 0


RAW = ROOT / "data" / "raw" / "2026-11-24" / KRK


@pytest.mark.skipif(not RAW.is_dir(), reason="stvarna arhiva 24.11.2026. nije lokalno raspakirana")
def test_real_archive_krk_dir():
    """Stvarna mapa iz raspakirane arhive (kad postoji lokalno): samo trgovina-krk, ne cijela arhiva."""
    assert chain_file_problems(_con(), RAW.parent, KRK) == REAL_PROBLEMS
