"""Korak 8: izvor nikad ne blokira update; carry-forward do CARRY_DAYS dana, ukupni pad sirovih cijena > 20 % je
upozorenje, a blokada (exit 2) samo kad broj čistih cijena nakon carry-forwarda padne > 20 %. Sintetičke arhive iz tests/fixtures/archive (80 cijena, 10 lanaca)."""

import datetime as dt

import pytest

from mealmeter import update
from mealmeter.update import CARRY_DAYS, describe_total, run, total_drop, validate
from tests.test_update import make_zip_custom, q

WEEKEND = {"dm", "roto", "trgovina-krk"}  # kao branka, dm i roto vikendom (branke nema u fixtureu)


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    db = tmp_path / "db" / "mealmeter.duckdb"
    db.parent.mkdir()
    return {"db": db, "base": ["--db", str(db), "--data-dir", str(tmp_path / "raw")],
            "full": make_zip_custom(tmp_path / "full.zip"), "tmp": tmp_path}


def load(env, archive, day: str) -> int:
    return run(env["base"] + ["--archive", str(archive), "--date", day])


def stale(db, chain: str):
    return q(db, f"SELECT DISTINCT stale_days FROM clean.prices WHERE chain = '{chain}' ORDER BY 1")


def test_carry_days_constant():
    assert CARRY_DAYS == 7


def test_weekend_three_chains_missing(env, capsys, monkeypatch):
    """Subota i nedjelja bez 3 lanca: deploy ide, cijene prenesene (stale_days 1, 2); u ponedjeljak svježe."""
    db = env["db"]
    weekend = make_zip_custom(env["tmp"] / "weekend.zip", skip=WEEKEND)
    summary = env["tmp"] / "summary.md"
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert load(env, env["full"], "2026-10-23") == 0
    capsys.readouterr()
    for day, days in (("2026-10-24", 1), ("2026-10-25", 2)):
        assert load(env, weekend, day) == 0
        out = capsys.readouterr().out
        for chain in WEEKEND:
            assert stale(db, chain) == [(days,)]
            assert f"::warning title=Lanac {chain}::{chain}: nema u arhivi {days}. dan, zadnje cijene 23.10.2026." in out
            assert f"  ~ {chain}: nema u arhivi {days}. dan" in out
        assert "::error" not in out
    text = summary.read_text(encoding="utf-8")
    assert "| dm | nema u arhivi | 1 | 23.10.2026. | 1 |" in text and "| roto | nema u arhivi | 2 | 23.10.2026. |" in text
    assert load(env, env["full"], "2026-10-26") == 0
    assert "::warning" not in capsys.readouterr().out
    assert all(stale(db, c) == [(0,)] for c in WEEKEND)


def test_sunday_18_10(env, capsys):
    """Kao 18.10.: 30 % lanaca nestane (staro pravilo o broju lanaca blokiralo bi) i lidl -67 %, ukupno -12,5 %."""
    db = env["db"]
    sunday = make_zip_custom(env["tmp"] / "sunday.zip", skip=WEEKEND, drop_rows={("lidl", "105"): 4, ("lidl", "192"): 2})
    assert load(env, env["full"], "2026-10-17") == 0
    n_clean = q(db, "SELECT count(*) FROM clean.prices")[0][0]
    n_lidl = q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'lidl'")[0][0]
    capsys.readouterr()
    assert load(env, sunday, "2026-10-18") == 0
    out = capsys.readouterr().out
    fresh = q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'lidl' AND stale_days = 0")[0][0]
    assert f"  ~ lidl: redaka cijena 9 -> 3 (-67 %), preneseno {n_lidl - fresh} cijena" in out
    assert all(f"  ~ {c}: nema u arhivi 1. dan" in out for c in WEEKEND)
    assert q(db, "SELECT count(*) FROM clean.prices")[0][0] == n_clean  # alat vidi sve, dio s 1 dan starim cijenama
    assert q(db, "SELECT count(*) FROM clean.prices WHERE chain = 'lidl' AND stale_days = 1")[0][0] == n_lidl - fresh > 0


def test_chain_missing_4_and_8_days(env, capsys):
    """dm izostaje: 4. i 7. dan još u rezultatima (stale_days 4, 7), 8. dan ispada iz clean.prices, ali ostaje u
    povijesti; deploy ni tada ne pada. Kad se vrati u arhivi, opet je svjež."""
    db = env["db"]
    no_dm = make_zip_custom(env["tmp"] / "no_dm.zip", skip={"dm"})
    start = dt.date(2026, 10, 10)
    assert load(env, env["full"], start.isoformat()) == 0
    for n in range(1, 9):
        capsys.readouterr()
        assert load(env, no_dm, (start + dt.timedelta(days=n)).isoformat()) == 0
        out = capsys.readouterr().out
        if n in (4, 7):
            assert stale(db, "dm") == [(n,)]
            assert f"  ~ dm: nema u arhivi {n}. dan, zadnje cijene 10.10.2026., preneseno 1 cijena (stale_days {n})" in out
    assert stale(db, "dm") == []  # 8. dan: ispao iz rezultata alata
    assert "  ~ dm: nema u arhivi 8. dan, zadnje cijene 10.10.2026.; ispao iz rezultata alata" in out
    assert q(db, "SELECT count(*) FROM clean.price_history WHERE chain = 'dm'")[0][0] == 1  # nije obrisan iz baze
    assert load(env, env["full"], (start + dt.timedelta(days=9)).isoformat()) == 0
    assert stale(db, "dm") == [(0,)]


def test_big_chain_missing_warns(env, capsys, monkeypatch):
    """Kao nestanak Plodina (34 % svih redaka): eurospin je 32 od 80 cijena u fixtureu. Ukupno sirovih -40 % je samo
    upozorenje (::warning:: i redak u sažetku s lancima koji su najviše pridonijeli); deploy ide, cijene prenesene."""
    db = env["db"]
    no_big = make_zip_custom(env["tmp"] / "no_eurospin.zip", skip={"eurospin"})
    assert load(env, env["full"], "2026-10-19") == 0
    n_clean = q(db, "SELECT count(*) FROM clean.prices")[0][0]
    summary = env["tmp"] / "summary.md"
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    capsys.readouterr()
    assert load(env, no_big, "2026-10-20") == 0
    out = capsys.readouterr().out
    assert "  ! ukupno sirovih redaka cijena 80 -> 48 (-40 %); najviše pridonijeli: eurospin -32" in out
    assert "::warning title=Ukupno sirovih cijena -40 %::ukupno sirovih redaka cijena 80 -> 48 (-40 %)" in out
    assert "::error" not in out
    assert "**Ukupno sirovih cijena -40 %** (80 -> 48); najviše pridonijeli: eurospin (-32)." in summary.read_text(encoding="utf-8")
    assert stale(db, "eurospin") == [(1,)] and q(db, "SELECT count(*) FROM clean.prices")[0][0] == n_clean


def test_total_raw_drop_three_chains_warns(env, capsys):
    """Bez konzuma, lidla i eurospina: ukupno -74 %, upozorenje navodi tri lanca od najvećeg pada; exit 0."""
    small = make_zip_custom(env["tmp"] / "small.zip", skip={"konzum", "lidl", "eurospin"})
    assert load(env, env["full"], "2026-10-19") == 0
    capsys.readouterr()
    assert load(env, small, "2026-10-20") == 0
    assert ("  ! ukupno sirovih redaka cijena 80 -> 21 (-74 %); najviše pridonijeli: eurospin -32, konzum -18, lidl -9"
            in capsys.readouterr().out)


def test_clean_drop_blocks(env, capsys, monkeypatch):
    """Sirovi retci jednaki, ali izgradnja izgubi pola čistih cijena (kvar kod nas): exit 2, baza netaknuta,
    ::error:: i razlog u sažetku."""
    db = env["db"]
    assert load(env, env["full"], "2026-10-19") == 0
    mtime = db.stat().st_mtime
    summary = env["tmp"] / "summary.md"
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    build_clean = update.build_clean

    def broken(con):
        out = build_clean(con)
        con.execute("DELETE FROM clean.prices WHERE hash(product_id) % 2 = 0")
        return out

    monkeypatch.setattr(update, "build_clean", broken)
    capsys.readouterr()
    assert load(env, env["full"], "2026-10-20") == 2
    assert db.stat().st_mtime == mtime and not list(db.parent.glob("*.tmp-*"))
    assert "::error title=update.py::broj čistih cijena (nakon carry-forwarda) pao s " in capsys.readouterr().out
    assert "**Provjera nije prošla:** broj čistih cijena (nakon carry-forwarda) pao s " in summary.read_text(encoding="utf-8")


def test_validate_and_total_drop():
    old = [("konzum", 1, 10, 1000), ("lidl", 1, 10, 1000), ("ntl", 1, 10, 1000), ("dm", 1, 1, 10)]
    assert validate(old[:3], old) == []  # nestali lanac javlja chain_report
    assert validate([("konzum", 1, 10, 1000), ("lidl", 1, 10, 1000), ("spar", 1, 1, 500)], old) == ["novi lanac spar"]
    assert validate([("konzum", 1, 10, 1000)], old) == []  # ni ukupni pad -67 % više ne diže grešku
    assert total_drop([old[0], old[1], ("ntl", 1, 10, 500), old[3]], old) is None  # -17 %: bez upozorenja
    d = total_drop([("konzum", 1, 10, 900), ("lidl", 1, 10, 1000), ("spar", 1, 1, 50)], old)  # 3010 -> 1950
    assert d == {"before": 3010, "after": 1950, "pct": 35, "chains": [("ntl", -1000), ("konzum", -100), ("dm", -10)]}
    assert describe_total(d) == ("ukupno sirovih redaka cijena 3010 -> 1950 (-35 %); "
                                 "najviše pridonijeli: ntl -1000, konzum -100, dm -10")
    assert total_drop(old, []) is None


def test_stale_chain_in_comparison(env):
    """Bez zadane trgovine: lanac s prenesenim cijenama u usporedbi nosi date_hr i stale_days (pravilo 10)."""
    from mealmeter.basket import plan_basket
    import duckdb

    db = env["db"]
    drop = make_zip_custom(env["tmp"] / "drop.zip", drop_rows={("konzum", "0907"): 11})  # cijela trgovina, -14 %
    assert load(env, env["full"], "2026-10-19") == 0
    assert load(env, drop, "2026-10-20") == 0
    con = duckdb.connect(str(db), read_only=True)
    try:
        res = plan_basket([{"name": "brašno glatko", "amount": 500, "unit": "g"}], "Osijek", con=con)
    finally:
        con.close()
    rows = res["comparison"] + res.get("more_chains", []) + res.get("incomplete", [])
    konzum = [r for r in rows if r["chain"] == "konzum"]
    assert konzum and konzum[0]["stale_days"] == 1 and konzum[0]["date_hr"] == "19.10.2026."
    assert all("stale_days" not in r for r in rows if r["chain"] != "konzum")  # svježi lanci bez dodatnih polja


def test_drop_after_missing_day(env, capsys):
    """Kao gavranovic 21./22.10.: lanca nema, a sutradan se vrati s djelićem cijena. Pad se mjeri prema zadnjem
    danu kad je lanac imao cijene (ne prema 0 od jučer), pa se javlja kao pad, a ne kao novi lanac."""
    no_lidl = make_zip_custom(env["tmp"] / "no_lidl.zip", skip={"lidl"})
    tiny = make_zip_custom(env["tmp"] / "tiny.zip", drop_rows={("lidl", "105"): 5, ("lidl", "192"): 3})
    assert load(env, env["full"], "2026-10-20") == 0
    assert load(env, no_lidl, "2026-10-21") == 0
    capsys.readouterr()
    assert load(env, tiny, "2026-10-22") == 0
    out = capsys.readouterr().out
    assert "  ~ lidl: redaka cijena 9 -> 1 (-89 %), preneseno " in out
