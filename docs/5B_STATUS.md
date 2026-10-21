# Korak 5B: stanje

| točka | stanje |
|---|---|
| 1 zbrojevi (total_used = zbroj redaka, from_stock_value) | gotovo |
| 2 preporuka po total_to_buy, usporedba lanaca | - |
| 3 prinos oblika mahunarki (data/yields.yaml) | - |
| 4 nove namirnice | - |
| 5 free_text sinonimi (data/synonyms.yaml) | - |
| 6 pretpostavke (assumptions) | - |
| 7 alternative na istu količinu | - |
| 8 upute poslužitelja | - |
| 9 smoke_5b | - |

**Točka 1, uzrok razlike od 0,07 €:** zaokruživanje nije uzrok, jer se zbrajaju već zaokruženi iznosi. total_used je
zbrajao utrošak SVIH stavki, i onih iz already_have (sol, papar, ulje), a stavke "imam" nisu među redcima za
kupiti. Primjer, varivo od graška u Lidlu: ulje 0,0414 → 0,04 € i papar 0,0529 → 0,05 € = 0,09 €
(2,42 naspram 2,33). Sada se te stavke ne zbrajaju u total_to_buy ni u total_used, nego u from_stock_value.

Hosting: nije dirano.
