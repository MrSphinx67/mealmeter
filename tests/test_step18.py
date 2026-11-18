"""Korak 18: neparsabilna cijena ne blokira bazu. Arhiva 18.11.2026., vrutak: `vodovodna,"219602,",7.99,15.98,...` je
jedino polje u navodnicima u datoteci, sniffer DuckDB-a nije prepoznao navodnik i pomaknuo stupce (cijena '"').
Navodnik je sada zadan (build.CSV_OPTS), decimalni zarez se čita, a stvarno neparsabilni retci se preskaču uz
upozorenje; baza se odbija tek iznad MAX_BAD_PRICE_SHARE redaka lanca."""

import shutil
import zipfile
from pathlib import Path

import duckdb
import pytest

from mealmeter.build import MAX_BAD_PRICE_SHARE, BadPriceError, load_raw
from mealmeter.update import run
from tests.test_update import FIXTURE, q

N = 200  # redaka cijena sintetičkog lanca; 1 % = 2 retka
HEADER = "store_id,product_id,price,unit_price,best_price_30,anchor_price,special_price,available,special_sale_type,anchor_price_date"


def price_rows(bad: dict[int, str] | None = None) -> list[str]:
    """N redaka cijena lanca vrutak; `bad` zamjenjuje cijenu i-tog retka sirovim tekstom."""
    rows = []
    for i in range(N):
        price = (bad or {}).get(i, f"{1 + i / 100:.2f}")
        rows.append(f"vodovodna,{i:06d},{price},0.00,,,,,,")
    return rows


def write_chain(root: Path, rows: list[str], products: list[str] | None = None) -> None:
    d = root / "vrutak"
    d.mkdir(parents=True)
    (d / "stores.csv").write_text("store_id,type,address,city,zipcode\nvodovodna,supermarket,Vodovodna 1,Zagreb,\n",
                                  encoding="utf-8")
    prods = products or [f"{i:06d},,ARTIKL {i},,,KOM,1" for i in range(N)]
    (d / "products.csv").write_text("product_id,barcode,name,brand,category,unit,quantity\n" + "\n".join(prods) + "\n",
                                    encoding="utf-8")
    (d / "prices.csv").write_text(HEADER + "\r\n" + "\r\n".join(rows) + "\r\n", encoding="utf-8")


def load(root: Path):
    con, bad = duckdb.connect(), []
    load_raw(con, root, "2026-11-18", bad)
    return con, bad


def test_threshold_constant():
    assert MAX_BAD_PRICE_SHARE == 0.01


def test_vrutak_18_11_lone_quoted_field(tmp_path):
    """Stvarni redak iz arhive 18.11.: šifra u navodnicima sa zarezom, jedini navodnik u datoteci. Čita se ispravno
    (šifra "219602," kao u products.csv, cijena 7.99, cijena po jedinici 15.98), bez upozorenja."""
    rows = price_rows()
    rows[100] = 'vodovodna,"219602,",7.99,15.98,,,,,,'
    write_chain(tmp_path, rows, [f"{i:06d},,ARTIKL {i},,,KOM,1" for i in range(N)]
                + ['"219602,",9005800388922,N-NIVEA HAIR ŠAMPON 500ML ANTIGREAS -6/1-,NIVEA-BEIERSDORF,,KOM,"0,5 L"'])
    con, bad = load(tmp_path)
    assert bad == []
    assert con.execute("SELECT count(*) FROM prices").fetchone()[0] == N
    assert con.execute("SELECT price::VARCHAR, unit_price::VARCHAR FROM prices WHERE product_id = '219602,'"
                       ).fetchall() == [("7.99", "15.98")]
    assert con.execute("SELECT count(*) FROM products WHERE product_id = '219602,'").fetchone()[0] == 1


def test_decimal_comma_read(tmp_path):
    """Drugi decimalni separator nije greška: "7,99" (u navodnicima) i 3,5 se čitaju kao 7.99 i 3.50."""
    rows = price_rows()
    rows[0] = 'vodovodna,000000,"7,99","15,98",,,,,,'
    rows[1] = 'vodovodna,000001," 3,5 ",0.00,,,,,,'
    write_chain(tmp_path, rows)
    con, bad = load(tmp_path)
    assert bad == []
    got = con.execute("SELECT product_id, price, unit_price FROM prices WHERE product_id IN ('000000', '000001') "
                      "ORDER BY 1").fetchall()
    assert [(p, float(a), float(b)) for p, a, b in got] == [("000000", 7.99, 15.98), ("000001", 3.5, 0.0)]


def test_one_bad_row_skipped_with_warning(tmp_path):
    rows = price_rows({7: "n/a"})
    write_chain(tmp_path, rows)
    con, bad = load(tmp_path)
    assert con.execute("SELECT count(*) FROM prices").fetchone()[0] == N - 1
    assert con.execute("SELECT count(*) FROM prices WHERE product_id = '000007'").fetchone()[0] == 0
    assert bad == [{"chain": "vrutak", "bad": 1, "total": N, "pct": 0.5,
                    "examples": ["vodovodna/000007 price='n/a'"]}]


def test_at_threshold_passes_above_blocks(tmp_path):
    """Točno 1 % (2 od 200) prolazi uz upozorenje i najviše 3 primjera; 3 od 200 (1,5 %) diže BadPriceError."""
    write_chain(tmp_path / "a", price_rows({1: "x", 2: "1.2.3"}))
    _, bad = load(tmp_path / "a")
    assert bad[0]["bad"] == 2 and bad[0]["examples"] == ["vodovodna/000001 price='x'", "vodovodna/000002 price='1.2.3'"]
    write_chain(tmp_path / "b", price_rows({1: "x", 2: "y", 3: "z", 4: "w"}))
    with pytest.raises(BadPriceError, match=r"vrutak: 4 od 200 redaka .*\(2\.00 %\); primjeri: vodovodna/000001 "
                                            r"price='x'; vodovodna/000002 price='y'; vodovodna/000003 price='z'; "
                                            r"više od 1 % redaka lanca"):
        load(tmp_path / "b")


def make_zip(path: Path, tmp: Path, rows: list[str]) -> Path:
    root = tmp / path.stem
    shutil.copytree(FIXTURE, root)
    write_chain(root, rows)
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(root.rglob("*.csv")):
            z.write(f, f.relative_to(root))
    return path


@pytest.fixture
def env(tmp_path, monkeypatch, step_summary):
    db = tmp_path / "db" / "mealmeter.duckdb"
    db.parent.mkdir()
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    return {"db": db, "base": ["--db", str(db), "--data-dir", str(tmp_path / "raw")], "tmp": tmp_path,
            "summary": step_summary}


def test_update_one_bad_row_warns(env, capsys):
    """Kao vrutak 18.11.: jedan loš redak malog lanca; baza se gradi, ::warning:: i redak u sažetku pokretanja."""
    archive = make_zip(env["tmp"] / "one_bad.zip", env["tmp"], price_rows({5: "N/A"}))
    assert run(env["base"] + ["--archive", str(archive), "--date", "2026-11-18"]) == 0
    out = capsys.readouterr().out
    line = "vrutak: 1 od 200 redaka cijena s neparsabilnom cijenom (0.50 %); primjeri: vodovodna/000005 price='N/A'"
    assert f"::warning title=Neparsabilne cijene vrutak::{line}; retci preskočeni" in out
    assert f"  ! {line}; retci preskočeni" in out
    assert "::error" not in out
    text = env["summary"].read_text(encoding="utf-8")
    assert ("**Neparsabilne cijene, vrutak:** preskočeno 1 od 200 redaka (0.50 %); primjeri: "
            "`vodovodna/000005 price='N/A'`") in text
    assert q(env["db"], "SELECT count(*) FROM main.prices WHERE chain = 'vrutak'")[0][0] == N - 1


def test_update_above_threshold_blocks(env, capsys):
    """> 1 % redaka lanca: exit 2, ::error::, sažetak, baza nije promijenjena."""
    good = make_zip(env["tmp"] / "good.zip", env["tmp"], price_rows())
    assert run(env["base"] + ["--archive", str(good), "--date", "2026-11-17"]) == 0
    before = q(env["db"], "SELECT max(date), count(*) FROM main.prices")
    capsys.readouterr()
    broken = make_zip(env["tmp"] / "broken.zip", env["tmp"], price_rows({i: "?" for i in range(10)}))
    assert run(env["base"] + ["--archive", str(broken), "--date", "2026-11-18"]) == 2
    out = capsys.readouterr().out
    assert "PROVJERA NIJE PROŠLA: vrutak: 10 od 200 redaka cijena s neparsabilnom cijenom (5.00 %)" in out
    assert "::error title=update.py::vrutak: 10 od 200" in out and "baza odbijena" in out
    assert "**Provjera nije prošla:** vrutak: 10 od 200" in env["summary"].read_text(encoding="utf-8")
    assert q(env["db"], "SELECT max(date), count(*) FROM main.prices") == before
