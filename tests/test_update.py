import json
import zipfile
from pathlib import Path

import duckdb
import pytest

from mealmeter.update import ValidationError, latest_archive, run, validate

FIXTURE = Path(__file__).parent / "fixtures" / "archive"


def make_zip(path: Path, skip: set[str] = frozenset()) -> Path:
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(FIXTURE.rglob("*.csv")):
            if f.parent.name not in skip:
                z.write(f, f.relative_to(FIXTURE))
    return path


def q(db: Path, sql: str):
    con = duckdb.connect(str(db), read_only=True)
    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()


@pytest.fixture
def env(tmp_path):
    full = make_zip(tmp_path / "full.zip")
    small = make_zip(tmp_path / "small.zip", skip={"konzum", "lidl", "eurospin"})
    db = tmp_path / "db" / "mealmeter.duckdb"
    db.parent.mkdir()
    base = ["--db", str(db), "--data-dir", str(tmp_path / "raw")]
    return {"full": full, "small": small, "db": db, "base": base}


def test_update_cycle(env):
    db, base = env["db"], env["base"]
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-19"]) == 0
    assert q(db, "SELECT DISTINCT date FROM clean.price_history") == [(__import__("datetime").date(2026, 10, 19),)]
    n_prices = q(db, "SELECT count(*) FROM clean.prices")[0][0]
    assert n_prices > 0

    # ista arhiva ponovno: ništa za napraviti
    mtime = db.stat().st_mtime
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-19"]) == 0
    assert db.stat().st_mtime == mtime

    # sljedeći dan: povijest ima oba dana, clean.prices samo novi
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-20"]) == 0
    days = [d.isoformat() for (d,) in q(db, "SELECT DISTINCT date FROM clean.price_history ORDER BY 1")]
    assert days == ["2026-10-19", "2026-10-20"]
    assert q(db, "SELECT DISTINCT date FROM clean.prices") == [(__import__("datetime").date(2026, 10, 20),)]
    assert q(db, "SELECT count(DISTINCT date) FROM clean.archive_stats")[0][0] == 2

    # nepotpuna arhiva (bez 3 lanca, > 20 % manje redaka): izlaz 2, baza netaknuta
    mtime = db.stat().st_mtime
    assert run(base + ["--archive", str(env["small"]), "--date", "2026-10-21"]) == 2
    assert db.stat().st_mtime == mtime
    assert q(db, "SELECT max(date) FROM clean.prices")[0][0].isoformat() == "2026-10-20"
    assert not list(db.parent.glob("*.tmp-*"))  # privremena baza obrisana

    # zadržavanje povijesti: --keep-days 2 ostavlja samo zadnja dva dana
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-22", "--keep-days", "2"]) == 0
    days = [d.isoformat() for (d,) in q(db, "SELECT DISTINCT date FROM clean.price_history ORDER BY 1")]
    assert days == ["2026-10-22"]  # 21. ne postoji (odbijen), 20. je stariji od 2 dana


def test_archive_without_date_is_error(env):
    assert run(env["base"] + ["--archive", str(env["full"])]) == 1
    assert not env["db"].exists()


def test_broken_archive_is_error(env, tmp_path):
    bad = tmp_path / "bad.zip"
    bad.write_bytes(b"not a zip")
    assert run(env["base"] + ["--archive", str(bad), "--date", "2026-10-19"]) == 1
    assert not env["db"].exists()


def test_print_schedule(capsys):
    assert run(["--print-schedule"]) == 0
    out = capsys.readouterr().out
    assert "scripts/update.py" in out and "OnCalendar=*-*-* 15:30" in out and "30 15,23 * * *" in out


def test_validate():
    old = [("konzum", 1, 10, 1000), ("lidl", 1, 10, 1000), ("ntl", 1, 10, 1000)]
    assert validate(old, old) == []
    with pytest.raises(ValidationError):
        validate([("konzum", 1, 10, 1000)], old)  # 3 -> 1 lanac
    with pytest.raises(ValidationError):
        validate([("konzum", 1, 10, 500), ("lidl", 1, 10, 500), ("ntl", 1, 10, 1000)], old)  # 3000 -> 2000
    warns = validate([("konzum", 1, 10, 700), ("lidl", 1, 10, 1150), ("ntl", 1, 10, 1150), ("spar", 1, 1, 10)], old)
    assert "konzum: redaka cijena 1000 -> 700" in warns and "novi lanac spar" in warns
    assert validate(old, []) == ["nema prethodne arhive za usporedbu (prvo učitavanje)"]


def test_latest_archive_from_list(tmp_path):
    listing = {"archives": [
        {"date": "2026-10-18", "url": "https://api.cijene.dev/v0/archive/2026-10-18.zip", "size": 1},
        {"date": "2026-10-19", "url": "https://api.cijene.dev/v0/archive/2026-10-19.zip", "size": 2},
    ]}
    f = tmp_path / "list.json"
    f.write_text(json.dumps(listing))
    assert latest_archive(f.as_uri())["date"] == "2026-10-19"
    assert latest_archive(f.as_uri(), date="2026-10-18")["size"] == 1
    with pytest.raises(RuntimeError):
        latest_archive(f.as_uri(), date="2026-01-01")


def test_compare_stats():
    from mealmeter.update import compare_stats

    rows = compare_stats([("konzum", 2, 10, 100), ("spar", 1, 5, 50)], [("konzum", 1, 8, 90), ("lidl", 1, 4, 40)])
    assert rows[0] == ("konzum", 2, 1, 10, 2, 100, 10)
    assert rows[1] == ("lidl", 0, -1, 0, -4, 0, -40) and rows[2] == ("spar", 1, 1, 5, 5, 50, 50)
    assert rows[-1][1:] == (3, 1, 15, 3, 150, 20) and rows[-1][0].startswith("UKUPNO (2 lanaca")


def test_republished_archive_reloads(env, tmp_path, monkeypatch):
    """Ista arhiva (datum + updated) se ne učitava ponovno; ponovno objavljena (novi updated) da."""
    import mealmeter.update as upd

    db, base = env["db"], env["base"]
    listing = {"archives": [{"date": "2026-10-20", "url": env["full"].as_uri(), "size": env["full"].stat().st_size,
                             "updated": "2026-10-20T14:26:59+02:00"}]}
    lst = tmp_path / "list.json"
    lst.write_text(json.dumps(listing))
    args = base + ["--list-url", lst.as_uri()]
    assert run(args) == 0
    assert q(db, "SELECT updated FROM clean.archive_info") == [("2026-10-20T14:26:59+02:00",)]
    mtime = db.stat().st_mtime
    assert run(args) == 0 and db.stat().st_mtime == mtime  # 23:30, ista verzija: ništa
    listing["archives"][0]["updated"] = "2026-10-20T21:59:00+02:00"
    lst.write_text(json.dumps(listing))
    assert run(args) == 0 and db.stat().st_mtime != mtime
    assert q(db, "SELECT updated FROM clean.archive_info") == [("2026-10-20T21:59:00+02:00",)]
