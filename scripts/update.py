"""Dnevno ažuriranje baze iz cijene.dev (vidi mealmeter.update).

    uv run python scripts/update.py                  # najnovija arhiva
    uv run python scripts/update.py --date 2026-10-19
    uv run python scripts/update.py --print-schedule # naredba za cron / systemd timer

Izlazni kod: 0 uspjeh ili već učitano, 1 greška, 2 provjera nije prošla (baza nije promijenjena): ukupni broj
sirovih ili čistih cijena pao > 20 %. Izostali ili prepolovljeni lanac je samo upozorenje (Korak 8).
"""

from mealmeter.update import main

main()
