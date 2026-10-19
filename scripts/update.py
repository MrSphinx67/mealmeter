"""Dnevno ažuriranje baze iz cijene.dev (vidi mealmeter.update).

    uv run python scripts/update.py                  # najnovija arhiva
    uv run python scripts/update.py --date 2026-10-19
    uv run python scripts/update.py --print-schedule # naredba za cron / systemd timer

Izlazni kod: 0 uspjeh ili već učitano, 1 greška, 2 provjera nije prošla (baza nije promijenjena).
"""

from mealmeter.update import main

main()
