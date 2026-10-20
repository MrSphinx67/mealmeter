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


# --- Korak 2E.7: carry-forward po trgovini ------------------------------------------------------

def make_zip_custom(path: Path, skip: set[str] = frozenset(), drop_rows: dict | None = None) -> Path:
    """Kao make_zip, uz `drop_rows`: {(lanac, store_id): broj redaka cijena koje treba izbaciti}."""
    drop_rows = dict(drop_rows or {})
    with zipfile.ZipFile(path, "w") as z:
        for f in sorted(FIXTURE.rglob("*.csv")):
            chain = f.parent.name
            if chain in skip:
                continue
            if f.name == "prices.csv" and any(c == chain for c, _ in drop_rows):
                lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
                out = [lines[0]]
                for ln in lines[1:]:
                    key = (chain, ln.split(",", 1)[0])
                    if drop_rows.get(key, 0) > 0:
                        drop_rows[key] -= 1
                        continue
                    out.append(ln)
                z.writestr(str(f.relative_to(FIXTURE)), "".join(out))
            else:
                z.write(f, f.relative_to(FIXTURE))
    return path


def test_carry_forward(env, tmp_path):
    db, base = env["db"], env["base"]
    no_dm = make_zip_custom(tmp_path / "no_dm.zip", skip={"dm"})
    drop2 = make_zip_custom(tmp_path / "drop2.zip", drop_rows={("konzum", "0907"): 2})  # 2/11 = 18 %
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-19"]) == 0

    # 1) nedostaje lanac (dm): njegove cijene se prenose, uz price_date 19.10. i stale_days 1
    assert run(base + ["--archive", str(no_dm), "--date", "2026-10-20"]) == 0
    rows = q(db, "SELECT price_date, stale_days FROM clean.prices WHERE chain = 'dm'")
    assert rows and all(d.isoformat() == "2026-10-19" and s == 1 for d, s in rows)
    assert q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'konzum' AND stale_days <> 0")[0][0] == 0
    assert q(db, "SELECT count(*) FROM clean.price_history WHERE chain = 'dm' AND date = DATE '2026-10-20'")[0][0] == 0

    # 2) pad > 10 % u trgovini (2 od 11): nedostajuće cijene te trgovine se prenose
    assert run(base + ["--archive", str(drop2), "--date", "2026-10-21"]) == 0
    stale = q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'konzum' AND store_id = '0907' AND stale_days = 1")
    assert stale[0][0] == 2
    assert q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'konzum' AND store_id = '0907'")[0][0] == 11

    # 3) dm ponovno nestane od 22.10.: cijene od 21.10. prenose se 1, 2 i 3 dana, a 4. dan (25.10.) više ne
    assert q(db, "SELECT DISTINCT stale_days FROM clean.prices WHERE chain = 'dm'") == [(0,)]
    for day, stale in (("2026-10-22", 1), ("2026-10-23", 2), ("2026-10-24", 3)):
        assert run(base + ["--archive", str(no_dm), "--date", day]) == 0
        assert q(db, "SELECT DISTINCT stale_days FROM clean.prices WHERE chain = 'dm'") == [(stale,)]
    assert run(base + ["--archive", str(no_dm), "--date", "2026-10-25"]) == 0
    assert q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'dm'")[0][0] == 0


def test_small_drop_not_carried(env, tmp_path):
    db, base = env["db"], env["base"]
    drop1 = make_zip_custom(tmp_path / "drop1.zip", drop_rows={("konzum", "0907"): 1})  # 9 % < 10 %
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-19"]) == 0
    assert run(base + ["--archive", str(drop1), "--date", "2026-10-20"]) == 0
    assert q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'konzum' AND store_id = '0907'")[0][0] == 10
    assert q(db, "SELECT max(stale_days) FROM clean.prices")[0][0] == 0


def test_stale_days_in_outputs(env, tmp_path):
    """Korak 2E.8: find_products, get_prices i plan_basket vraćaju date, date_hr i stale_days."""
    from mealmeter.basket import plan_basket
    from mealmeter.search import find_products, get_prices

    db, base = env["db"], env["base"]
    no_dm = make_zip_custom(tmp_path / "no_dm.zip", skip={"dm"})
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-19"]) == 0
    assert run(base + ["--archive", str(no_dm), "--date", "2026-10-20"]) == 0
    con = duckdb.connect(str(db), read_only=True)
    try:
        rows = get_prices("dm:1000105", con=con, include_nonfood=True)
        assert rows and rows[0]["stale_days"] == 1 and rows[0]["date"] == "2026-10-19" and rows[0]["date_hr"] == "19.10.2026."
        res = find_products("hipp", con=con, include_nonfood=True)
        assert res[0]["stale_days"] == 1 and res[0]["date"] == "2026-10-19"
        fresh = get_prices("3850104223624", city="Osijek", con=con)
        assert fresh and all(r["stale_days"] == 0 and r["date"] == "2026-10-20" for r in fresh)
        basket = plan_basket([{"name": "brašno glatko", "amount": 500, "unit": "g"}], "Osijek", con=con)
        store = basket["best_store"]
        assert store["stale_days"] == 0 and store["date"] == "2026-10-20"
        assert all({"date", "date_hr", "stale_days"} <= set(it) for it in store["items"])
    finally:
        con.close()


def test_reload_older_then_newer_carries(env, tmp_path):
    """Ponovno učitavanje starijeg dana (--force) pa novijeg: prethodna je učitana arhiva, pa radi carry-forward."""
    db, base = env["db"], env["base"]
    no_dm = make_zip_custom(tmp_path / "no_dm.zip", skip={"dm"})
    assert run(base + ["--archive", str(no_dm), "--date", "2026-10-20"]) == 0
    assert run(base + ["--archive", str(env["full"]), "--date", "2026-10-19", "--force"]) == 0
    assert run(base + ["--archive", str(no_dm), "--date", "2026-10-20", "--force"]) == 0
    assert q(db, "SELECT DISTINCT stale_days FROM clean.prices WHERE chain = 'dm'") == [(1,)]
