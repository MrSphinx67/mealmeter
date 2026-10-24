"""Dnevno ažuriranje: najnovija arhiva cijene.dev -> provjera -> nova baza -> atomarna zamjena.

Izlazni kodovi: 0 = uspjeh ili arhiva već učitana, 1 = greška, 2 = provjera nije prošla
(ukupni broj sirovih cijena ili čistih cijena nakon carry-forwarda pao je više od dopuštenog).
Pojedini lanac nikad ne blokira (Korak 8): izostali ili prepolovljeni lanac nasljeđuje prethodne cijene
(carry-forward, najviše CARRY_DAYS dana) i javlja se kao upozorenje.
"""

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import duckdb

from mealmeter.build import build_clean, load_raw

LIST_URL = "https://api.cijene.dev/v0/list"
ARCHIVE_URL = "https://api.cijene.dev/v0/archive/{date}.zip"
KEEP_DAYS = 30
MAX_DROP = 0.20
# carry-forward: trgovina koja nedostaje ili ima > 10 % manje cijena zadržava prethodne cijene, najviše
# CARRY_DAYS dana (stale_days u odgovoru alata); poslije toga ispada iz rezultata alata, a u povijesti cijena
# (clean.price_history) ostaje i vraća se sama kad se ponovno pojavi u arhivi
CARRY_DROP = 0.10
CARRY_DAYS = 7

SCHEDULE = """\
# Dva pokretanja dnevno (15:30 i 23:30). Najnovija arhiva uzima se iz /v0/list, a ne po satu: 20.10. je
# objavljena već u 14:26, a ponekad se kasnije ponovno objavi. Pokretanje je idempotentno: ista arhiva
# (datum + "updated" iz popisa) se ne učitava ponovno, a ponovno objavljena se učitava.
# cron:
30 15,23 * * *  cd {root} && {uv} run python scripts/update.py >> data/update.log 2>&1

# ili systemd (korisnički timer), ~/.config/systemd/user/mealmeter-update.service:
[Unit]
Description=Mealmeter: dnevno ažuriranje cijena

[Service]
Type=oneshot
WorkingDirectory={root}
ExecStart={uv} run python scripts/update.py

# ~/.config/systemd/user/mealmeter-update.timer:
[Unit]
Description=Mealmeter: dnevno ažuriranje cijena

[Timer]
OnCalendar=*-*-* 15:30
OnCalendar=*-*-* 23:30
Persistent=true

[Install]
WantedBy=timers.target

# uključivanje (ručno): systemctl --user daemon-reload && systemctl --user enable --now mealmeter-update.timer
"""


class ValidationError(RuntimeError):
    """Nova arhiva izgleda nepotpuno u odnosu na prethodnu."""


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# --- pronalazak i preuzimanje arhive -------------------------------------------------

def latest_archive(list_url: str = LIST_URL, date: str | None = None, timeout: int = 30) -> dict:
    """{date, url, size} najnovije (ili zadane) arhive iz /v0/list; ako popis nije dostupan,
    ispituje obrazac URL-a za zadnjih 7 dana."""
    try:
        with urllib.request.urlopen(list_url, timeout=timeout) as resp:
            archives = json.load(resp)["archives"]
        if date:
            match = [a for a in archives if a["date"] == date]
            if not match:
                raise RuntimeError(f"arhiva za {date} nije na popisu {list_url}")
            return match[0]
        return max(archives, key=lambda a: a["date"])
    except (urllib.error.URLError, KeyError, ValueError, TimeoutError) as e:
        log(f"popis arhiva nije dostupan ({e}); ispitujem obrazac URL-a")
    days = [date] if date else [(dt.date.today() - dt.timedelta(days=i)).isoformat() for i in range(7)]
    for day in days:
        url = ARCHIVE_URL.format(date=day)
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return {"date": day, "url": url, "size": int(resp.headers.get("Content-Length") or 0) or None}
        except urllib.error.HTTPError:
            continue
    raise RuntimeError("nijedna arhiva nije pronađena")


def download(url: str, dest: Path, expected_size: int | None = None) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=60) as resp, open(part, "wb") as f:
        shutil.copyfileobj(resp, f, length=1 << 20)
    if expected_size and part.stat().st_size != expected_size:
        raise RuntimeError(f"preuzeto {part.stat().st_size} B, očekivano {expected_size} B")
    part.replace(dest)
    return dest


def extract(zip_path: Path, dest: Path) -> Path:
    """Raspakira u svježu mapu (stari sadržaj se briše); vraća mapu s mapama lanaca."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():  # zaštita od putanja izvan odredišta
            target = (dest / member).resolve()
            if not str(target).startswith(str(dest.resolve())):
                raise RuntimeError(f"sumnjiva putanja u arhivi: {member}")
        z.extractall(dest)
    chains = [p for p in dest.iterdir() if p.is_dir()]
    if len(chains) == 1 and not (chains[0] / "prices.csv").exists():
        return chains[0]  # arhiva s jednom korijenskom mapom
    return dest


# --- provjera -----------------------------------------------------------------------

def archive_stats(con) -> list[tuple]:
    """(chain, n_stores, n_products, n_prices) iz sirovih tablica."""
    return con.execute("""
        SELECT s.chain, s.n_stores, p.n_products, coalesce(c.n_prices, 0)
        FROM (SELECT chain, count(*) n_stores FROM stores GROUP BY chain) s
        JOIN (SELECT chain, count(*) n_products FROM products GROUP BY chain) p USING (chain)
        LEFT JOIN (SELECT chain, count(*) n_prices FROM prices GROUP BY chain) c USING (chain)
        ORDER BY s.chain
    """).fetchall()


def validate(new: list[tuple], old: list[tuple], max_drop: float = MAX_DROP) -> list[str]:
    """Usporedba s prethodnom arhivom. Pad ukupnih redaka cijena veći od max_drop -> ValidationError.
    Broj lanaca i pojedini lanac ne blokiraju (Korak 8: izvor vikendom redovito nema branka, dm i roto);
    izostale i prepolovljene lance javlja chain_report."""
    if not old:
        return ["nema prethodne arhive za usporedbu (prvo učitavanje)"]
    rows_new, rows_old = sum(r[3] for r in new), sum(r[3] for r in old)
    if rows_new < rows_old * (1 - max_drop):
        raise ValidationError(
            f"broj redaka cijena pao s {rows_old} na {rows_new} ({100 * (1 - rows_new / rows_old):.0f} %)")
    new_by, old_by = {r[0] for r in new}, {r[0] for r in old}
    return [f"novi lanac {chain}" for chain in sorted(new_by - old_by)]


def chain_report(con, date: str, new: list[tuple], max_drop: float = MAX_DROP,
                 max_days: int = CARRY_DAYS) -> list[dict]:
    """Lanci koji nedostaju u arhivi (a imaju cijene u povijesti) ili imaju > max_drop manje redaka nego zadnji
    dan kad su ih imali: {chain, missing, days, last_date, drop_pct, carried, in_results}. `days` je koliko dana
    lanac izostaje (= stale_days prenesenih cijena), `carried` broj prenesenih cijena u clean.prices, a
    `in_results` je False kad je lanac izostao dulje od max_days i više nije u rezultatima alata. Usporedba sa
    zadnjim danom s cijenama, a ne samo s jučer: gavranovic 21.10.2026. nije bio u arhivi, a 22.10. je imao
    5445 od ~1,7 milijuna cijena. Traži clean.prices, clean.price_history i clean.archive_stats nove baze."""
    new_by = {r[0]: r[3] for r in new}
    old_by = {chain: n for chain, n in con.execute("""
        SELECT chain, arg_max(n_prices, date) FROM clean.archive_stats
        WHERE date < ? AND n_prices > 0 GROUP BY chain""", [date]).fetchall()}
    last = dict(con.execute("SELECT chain, max(date) FROM clean.price_history WHERE date < ? GROUP BY chain",
                            [date]).fetchall())
    carried = dict(con.execute("SELECT chain, count(*) FROM clean.prices WHERE date < ? GROUP BY chain",
                               [date]).fetchall())
    today = dt.date.fromisoformat(date)
    report = []
    for chain in sorted(set(last) | set(old_by)):
        if not new_by.get(chain):
            if chain not in last:
                continue
            days = (today - last[chain]).days
            report.append({"chain": chain, "missing": True, "days": days, "last_date": last[chain],
                           "drop_pct": 100, "carried": carried.get(chain, 0), "in_results": days <= max_days})
        elif old_by.get(chain) and new_by[chain] < old_by[chain] * (1 - max_drop):
            report.append({"chain": chain, "missing": False, "days": 0, "last_date": today,
                           "drop_pct": round(100 * (1 - new_by[chain] / old_by[chain])),
                           "carried": carried.get(chain, 0), "in_results": True,
                           "before": old_by[chain], "after": new_by[chain]})
    return report


def describe_chain(r: dict, max_days: int = CARRY_DAYS) -> str:
    """Jedan redak upozorenja za lanac iz chain_report."""
    last = f"{r['last_date']:%d.%m.%Y.}"
    if not r["missing"]:
        return (f"{r['chain']}: redaka cijena {r['before']} -> {r['after']} (-{r['drop_pct']} %), "
                f"preneseno {r['carried']} cijena")
    if r["in_results"]:
        return (f"{r['chain']}: nema u arhivi {r['days']}. dan, zadnje cijene {last}, preneseno {r['carried']} "
                f"cijena (stale_days {r['days']})")
    return (f"{r['chain']}: nema u arhivi {r['days']}. dan, zadnje cijene {last}; ispao iz rezultata alata "
            f"(carry-forward najviše {max_days} dana), vraća se kad se pojavi u arhivi")


def github_report(report: list[dict], error: str | None = None) -> None:
    """U GitHub Actionsu: ::warning:: po lancu (::error:: kad provjera nije prošla) i sažetak u
    GITHUB_STEP_SUMMARY. Izvan Actionsa ne radi ništa."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    for r in report:
        print(f"::warning title=Lanac {r['chain']}::{describe_chain(r)}", flush=True)
    if error:
        print(f"::error title=update.py::{error}; baza nije promijenjena, ne deployam", flush=True)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path or not (report or error):
        return
    lines = ["### update.py: lanci", ""]
    if error:
        lines += [f"**Provjera nije prošla:** {error}. Baza nije promijenjena, nema deploya.", ""]
    if report:
        lines += ["| lanac | stanje | dana izostaje | zadnje cijene | preneseno cijena |", "|---|---|---:|---|---:|"]
        for r in report:
            state = (("nema u arhivi" if r["in_results"] else "nema u arhivi, ispao iz rezultata")
                     if r["missing"] else f"pad -{r['drop_pct']} %")
            lines.append(f"| {r['chain']} | {state} | {r['days']} | {r['last_date']:%d.%m.%Y.} | {r['carried']} |")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n")


# --- carry-forward po trgovini -------------------------------------------------------------

def carry_forward(con, old_db: Path, date: str, max_drop: float = CARRY_DROP, max_days: int = CARRY_DAYS) -> list[tuple]:
    """Sirove tablice nove arhive (stores, products, prices) dopuni prethodnim cijenama trgovina koje
    nedostaju ili imaju više od `max_drop` manje cijena nego prije. Prethodni redak zadržava svoj datum
    (prices.date), a prenosi se samo ako nije stariji od `max_days` dana, pa se ni preneseni ne prenose
    zauvijek. Dodaje samo (lanac, trgovina, proizvod) kojih u novoj arhivi nema. Vraća
    (lanac, trgovina, prije, sada, preneseno)."""
    if not old_db.exists():
        return []
    con.execute(f"ATTACH '{old_db}' AS prev (READ_ONLY)")
    try:
        tables = {r[0] for r in con.execute(
            "SELECT table_name FROM duckdb_tables() WHERE database_name = 'prev' AND schema_name = 'main'").fetchall()}
        if not {"stores", "products", "prices"} <= tables:
            return []
        cutoff = (dt.date.fromisoformat(date) - dt.timedelta(days=max_days)).isoformat()
        con.execute(f"""
            CREATE OR REPLACE TEMP TABLE carry_stores AS
            WITH o AS (SELECT chain, store_id, count(*) AS n_old FROM prev.main.prices
                       WHERE date >= DATE '{cutoff}' AND date < DATE '{date}' GROUP BY ALL),
                 n AS (SELECT chain, store_id, count(*) AS n_new FROM prices GROUP BY ALL)
            SELECT o.chain, o.store_id, o.n_old, coalesce(n.n_new, 0) AS n_new
            FROM o LEFT JOIN n USING (chain, store_id)
            WHERE coalesce(n.n_new, 0) < o.n_old * (1 - {max_drop})
        """)
        con.execute(f"""
            CREATE OR REPLACE TEMP TABLE carry_prices AS
            SELECT o.* FROM prev.main.prices o JOIN carry_stores USING (chain, store_id)
            WHERE o.date >= DATE '{cutoff}' AND o.date < DATE '{date}'
              AND NOT EXISTS (SELECT 1 FROM prices n WHERE n.chain = o.chain AND n.store_id = o.store_id
                              AND n.product_id = o.product_id)
        """)
        con.execute("""INSERT INTO stores SELECT o.* FROM prev.main.stores o JOIN carry_stores USING (chain, store_id)
                       WHERE NOT EXISTS (SELECT 1 FROM stores n WHERE n.chain = o.chain AND n.store_id = o.store_id)""")
        con.execute("""INSERT INTO products SELECT o.* FROM prev.main.products o
                       WHERE (o.chain, o.product_id) IN (SELECT chain, product_id FROM carry_prices)
                         AND NOT EXISTS (SELECT 1 FROM products n WHERE n.chain = o.chain AND n.product_id = o.product_id)""")
        con.execute("INSERT INTO prices SELECT * FROM carry_prices")
        return con.execute("""
            SELECT s.chain, s.store_id, s.n_old, s.n_new, count(c.product_id)
            FROM carry_stores s LEFT JOIN carry_prices c USING (chain, store_id)
            GROUP BY ALL ORDER BY s.chain, s.store_id""").fetchall()
    finally:
        con.execute("DETACH prev")


# --- izgradnja i zamjena ---------------------------------------------------------------

def compare_stats(new: list[tuple], old: list[tuple]) -> list[tuple]:
    """Razlike po lancu: (lanac, trgovina, Δ, proizvoda, Δ, cijena, Δ) i zadnji redak UKUPNO;
    lanac koji nedostaje u novoj arhivi ima nule."""
    new_by, old_by = {r[0]: r for r in new}, {r[0]: r for r in old}
    rows = []
    for chain in sorted(set(new_by) | set(old_by)):
        n, o = new_by.get(chain, (chain, 0, 0, 0)), old_by.get(chain, (chain, 0, 0, 0))
        rows.append((chain, n[1], n[1] - o[1], n[2], n[2] - o[2], n[3], n[3] - o[3]))
    tot = [sum(r[i] for r in rows) for i in range(1, 7)]
    rows.append((f"UKUPNO ({len(new_by)} lanaca, {len(new_by) - len(old_by):+d})", *tot))
    return rows


def _loaded_version(db_path: Path) -> dict | None:
    """{date, updated, size} zadnje učitane arhive (clean.archive_info), ili None."""
    if not db_path.exists():
        return None
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        if not con.execute("SELECT count(*) FROM duckdb_tables() WHERE schema_name = 'clean' "
                           "AND table_name = 'archive_info'").fetchone()[0]:
            return None
        row = con.execute("SELECT date, updated, size FROM clean.archive_info ORDER BY loaded_at DESC LIMIT 1").fetchone()
        return {"date": row[0].isoformat(), "updated": row[1], "size": row[2]} if row else None
    finally:
        con.close()


def _previous(db_path: Path) -> tuple[str | None, list[tuple]]:
    """(datum, statistika) zadnje učitane arhive u postojećoj bazi."""
    if not db_path.exists():
        return None, []
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        tables = {r[0] for r in con.execute(
            "SELECT schema_name || '.' || table_name FROM duckdb_tables()").fetchall()}
        if "clean.archive_stats" in tables:
            # učitana arhiva (archive_info), a ne najveći datum u povijesti: nakon ponovnog učitavanja
            # starijeg dana (--force) prethodna je ta, a ne noviji dan iz povijesti
            last = None
            if "clean.archive_info" in tables:
                last = con.execute("SELECT max(date) FROM clean.archive_info").fetchone()[0]
            last = last or con.execute("SELECT max(date) FROM clean.archive_stats").fetchone()[0]
            if last:
                rows = con.execute("SELECT chain, n_stores, n_products, n_prices FROM clean.archive_stats "
                                   "WHERE date = ? ORDER BY chain", [last]).fetchall()
                return last.isoformat(), rows
        if "main.prices" in tables:  # baza iz vremena prije update.py
            last = con.execute("SELECT max(date) FROM prices").fetchone()[0]
            return (last.isoformat() if last else None), archive_stats(con)
        return None, []
    finally:
        con.close()


def _clean_count(db_path: Path) -> int | None:
    """Broj čistih cijena (clean.prices) u postojećoj bazi, ili None."""
    if not db_path.exists():
        return None
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        if not con.execute("SELECT count(*) FROM duckdb_tables() WHERE schema_name = 'clean' "
                           "AND table_name = 'prices'").fetchone()[0]:
            return None
        return con.execute("SELECT count(*) FROM clean.prices").fetchone()[0]
    finally:
        con.close()


def build_database(root: Path, date: str, db_path: Path, keep_days: int = KEEP_DAYS,
                   max_drop: float = MAX_DROP, info: dict | None = None) -> dict:
    """Izgradi novu bazu u privremenu datoteku, provjeri je, prenese povijest cijena i atomarno
    zamijeni `db_path`. Pri bilo kojoj grešci stara baza ostaje netaknuta."""
    prev_date, prev_stats = _previous(db_path)
    prev_clean = _clean_count(db_path)
    tmp = db_path.with_name(f"{db_path.name}.tmp-{date}")
    tmp.unlink(missing_ok=True)
    try:
        con = duckdb.connect(str(tmp))
        load_raw(con, root, date)
        stats = archive_stats(con)
        warnings = validate(stats, prev_stats if prev_date != date else [], max_drop)
        # provjera gleda stvarnu arhivu; zatim nepotpune trgovine nasljeđuju prethodne cijene
        carried = carry_forward(con, db_path, date) if prev_date and prev_date != date else []
        build_clean(con)
        # druga zaštita: što alat stvarno vidi (nakon carry-forwarda); hvata kvar u našoj izgradnji
        n_clean = con.execute("SELECT count(*) FROM clean.prices").fetchone()[0]
        if prev_clean and n_clean < prev_clean * (1 - max_drop):
            raise ValidationError(f"broj čistih cijena (nakon carry-forwarda) pao s {prev_clean} na {n_clean} "
                                  f"({100 * (1 - n_clean / prev_clean):.0f} %)")

        # statistika arhiva i povijest cijena (zadnjih keep_days dana, uključujući današnji)
        cutoff = (dt.date.fromisoformat(date) - dt.timedelta(days=keep_days - 1)).isoformat()
        con.execute("""CREATE TABLE clean.archive_stats (date DATE, chain VARCHAR, n_stores BIGINT,
                       n_products BIGINT, n_prices BIGINT)""")
        con.execute("""CREATE TABLE clean.price_history (date DATE, chain VARCHAR, store_id VARCHAR,
                       product_id VARCHAR, price DECIMAL(10,2), special_price DECIMAL(10,2),
                       price_eff DECIMAL(10,2), price_per_unit DECIMAL(10,2), per_unit VARCHAR)""")
        if db_path.exists():
            con.execute(f"ATTACH '{db_path}' AS old (READ_ONLY)")
            old_tables = {r[0] for r in con.execute(
                "SELECT schema_name || '.' || table_name FROM duckdb_tables() WHERE database_name = 'old'").fetchall()}
            if "clean.price_history" in old_tables:
                con.execute("INSERT INTO clean.price_history SELECT * FROM old.clean.price_history "
                            "WHERE date >= ? AND date <> ?", [cutoff, date])
            elif "clean.prices" in old_tables:  # stara baza bez povijesti: njezin dan postaje povijest
                con.execute("""INSERT INTO clean.price_history
                               SELECT date, chain, store_id, product_id, price, special_price, price_eff,
                                      price_per_unit, per_unit FROM old.clean.prices WHERE date >= ? AND date <> ?""",
                            [cutoff, date])
            if "clean.archive_stats" in old_tables:
                con.execute("INSERT INTO clean.archive_stats SELECT * FROM old.clean.archive_stats "
                            "WHERE date >= ? AND date <> ?", [cutoff, date])
            con.execute("DETACH old")
        con.executemany("INSERT INTO clean.archive_stats VALUES (?, ?, ?, ?, ?)",
                        [(date, *r) for r in stats])
        # koja je verzija arhive učitana ("updated" i veličina iz /v0/list), za idempotentno pokretanje
        con.execute("""CREATE TABLE clean.archive_info (date DATE, updated VARCHAR, size BIGINT, url VARCHAR,
                       loaded_at TIMESTAMP)""")
        con.execute("INSERT INTO clean.archive_info VALUES (?, ?, ?, ?, now())",
                    [date, (info or {}).get("updated"), (info or {}).get("size"), (info or {}).get("url")])
        # samo cijene ovog dana: preneseni retci (carry-forward) već su u povijesti pod svojim datumom
        con.execute("""INSERT INTO clean.price_history
                       SELECT date, chain, store_id, product_id, price, special_price, price_eff,
                              price_per_unit, per_unit FROM clean.prices WHERE date = ?""", [date])
        report = chain_report(con, date, stats, max_drop)
        summary = {
            "date": date, "previous_date": prev_date, "warnings": warnings, "chain_report": report,
            "chains": len(stats), "stores": sum(r[1] for r in stats), "products": sum(r[2] for r in stats),
            "price_rows": sum(r[3] for r in stats),
            "price_rows_previous": sum(r[3] for r in prev_stats) if prev_stats else None,
            "diff": compare_stats(stats, prev_stats) if prev_stats and prev_date != date else [],
            "carried": carried,
            "clean_prices": n_clean, "clean_prices_previous": prev_clean,
            "history_days": [d.isoformat() for (d,) in con.execute(
                "SELECT DISTINCT date FROM clean.price_history ORDER BY date").fetchall()],
        }
        con.execute("CHECKPOINT")
        con.close()
        os.replace(tmp, db_path)  # atomarno na istom datotečnom sustavu
        return summary
    except BaseException:
        try:
            con.close()
        except Exception:
            pass
        tmp.unlink(missing_ok=True)
        tmp.with_name(tmp.name + ".wal").unlink(missing_ok=True)
        raise


def run(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dnevno ažuriranje Mealmeter baze iz cijene.dev")
    ap.add_argument("--db", default="data/mealmeter.duckdb")
    ap.add_argument("--data-dir", default="data/raw", help="gdje se spremaju zip i raspakirane datoteke")
    ap.add_argument("--date", help="YYYY-MM-DD (zadano: najnovija arhiva)")
    ap.add_argument("--archive", help="lokalni zip umjesto preuzimanja (uz --date)")
    ap.add_argument("--list-url", default=LIST_URL)
    ap.add_argument("--keep-days", type=int, default=KEEP_DAYS)
    ap.add_argument("--max-drop", type=float, default=MAX_DROP)
    ap.add_argument("--force", action="store_true", help="ponovno učitaj i ako je arhiva već u bazi")
    ap.add_argument("--print-schedule", action="store_true", help="ispiši naredbu za cron/systemd i izađi")
    args = ap.parse_args(argv)

    if args.print_schedule:
        root = Path.cwd()
        uv = shutil.which("uv") or str(Path.home() / ".local/bin/uv")
        print(SCHEDULE.format(root=root, uv=uv))
        return 0
    started = time.time()
    db_path, data_dir = Path(args.db), Path(args.data_dir)
    try:
        if args.archive:
            if not args.date:
                raise RuntimeError("--archive traži --date")
            info = {"date": args.date, "url": None, "size": None}
            zip_path = Path(args.archive)
        else:
            info = latest_archive(args.list_url, args.date)
        date = info["date"]
        prev_date, _ = _previous(db_path)
        loaded = _loaded_version(db_path)
        republished = (loaded and loaded["date"] == date and info.get("updated")
                       and loaded["updated"] and loaded["updated"] != info["updated"])
        if prev_date and date < prev_date and not args.force:
            log(f"najnovija arhiva {date} je starija od učitane {prev_date}; ništa za napraviti")
            return 0
        if prev_date == date and not republished and not args.force:
            log(f"arhiva {date} je već učitana; ništa za napraviti (--force za ponovno učitavanje)")
            return 0
        if republished:
            log(f"arhiva {date} je ponovno objavljena ({loaded['updated']} -> {info['updated']}); učitavam")
        if not args.archive:
            zip_path = data_dir / f"{date}.zip"
            if zip_path.exists() and info.get("size") and zip_path.stat().st_size == info["size"]:
                log(f"zip već postoji: {zip_path}")
            else:
                log(f"preuzimam {info['url']}")
                download(info["url"], zip_path, info.get("size"))
        root = extract(zip_path, data_dir / date)
        log(f"gradim bazu za {date} (prethodna: {prev_date or '-'})")
        summary = build_database(root, date, db_path, args.keep_days, args.max_drop, info)
    except ValidationError as e:
        log(f"PROVJERA NIJE PROŠLA: {e}; baza nije promijenjena")
        github_report([], str(e))
        return 2
    except Exception as e:  # noqa: BLE001
        log(f"GREŠKA: {type(e).__name__}: {e}; baza nije promijenjena")
        return 1
    prev_rows = summary["price_rows_previous"]
    delta = f" ({summary['price_rows'] - prev_rows:+d} naspram {summary['previous_date']})" if prev_rows else ""
    log(f"gotovo za {time.time() - started:.0f} s: {db_path}")
    print(f"  datum:           {summary['date']}")
    print(f"  lanaca:          {summary['chains']}")
    print(f"  trgovina:        {summary['stores']}")
    print(f"  proizvoda:       {summary['products']}")
    print(f"  redaka cijena:   {summary['price_rows']}{delta}")
    prev_clean = summary["clean_prices_previous"]
    print(f"  čistih cijena:   {summary['clean_prices']}"
          + (f" ({summary['clean_prices'] - prev_clean:+d})" if prev_clean else ""))
    print(f"  povijest:        {len(summary['history_days'])} dana ({summary['history_days'][0]} .. {summary['history_days'][-1]})")
    for w in summary["warnings"]:
        print(f"  ! {w}")
    for r in summary["chain_report"]:
        print(f"  ~ {describe_chain(r)}")
    if summary["carried"]:
        n_rows = sum(r[4] for r in summary["carried"])
        chains = sorted({r[0] for r in summary["carried"]})
        print(f"  carry-forward:   {len(summary['carried'])} trgovina, {n_rows} cijena ({', '.join(chains)})")
    if summary["diff"]:
        print(f"\n  razlike naspram {summary['previous_date']} (sirove tablice):")
        print(f"  {'lanac':<28}{'trgovina':>9}{'Δ':>6}{'proizvoda':>11}{'Δ':>8}{'cijena':>11}{'Δ':>9}")
        for chain, st, dst, pr, dpr, pc, dpc in summary["diff"]:
            print(f"  {chain:<28}{st:>9}{dst:>+6}{pr:>11}{dpr:>+8}{pc:>11}{dpc:>+9}")
    github_report(summary["chain_report"])
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
