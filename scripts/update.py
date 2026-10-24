"""Dnevno ažuriranje baze iz cijene.dev (vidi mealmeter.update).

    uv run python scripts/update.py                  # najnovija arhiva
    uv run python scripts/update.py --date 2026-10-19
    uv run python scripts/update.py --print-schedule # naredba za cron / systemd timer

Izlazni kod: 0 uspjeh ili već učitano, 1 greška, 2 provjera nije prošla (baza nije promijenjena): broj čistih
cijena nakon carry-forwarda pao > 20 %. Ukupni pad sirovih cijena i izostali lanac su samo upozorenja (Korak 8).
"""

from mealmeter.update import main

main()
