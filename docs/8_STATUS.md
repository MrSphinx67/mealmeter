# Korak 8: workflow "update" pada na provjeri lanaca

| točka | stanje |
|---|---|
| 1 dijagnoza | gotovo: izvor stvarno nema lance (branka, dm, roto vikendom), lažne uzbune kod nas nema |
| 2 odluka | prijedlog politike niže; **čeka potvrdu**, logika provjere nije mijenjana |
| 3 update.yml: Node 24, ubuntu-24.04 | gotovo |

Ništa nije deployano.

## 1. Dijagnoza

**Log s Actionsa.** `gh` nije bio instaliran; instaliran je binarno u `~/.local/bin/gh` (2.103.2), ali nije
prijavljen (`gh auth status`: not logged in), a repozitorij je privatan, pa javni API ne vraća pokrete. Log nije
pročitan; zaključak niže dobiven je iz arhiva i lokalnog pokretanja. Za potvrdu: `gh auth login`, pa
`gh run list --workflow update.yml -L 5` i `gh run view <id> --log-failed`.

**Lokalno pokretanje.** update.py na kopiji pune baze (`data/raw/diag8/base-1020.duckdb`, zadnja učitana arhiva
20.10.), bez deploya, DuckDB `memory_limit` 1500 MB i 2 dretve (omotač u scratchpadu, kod nije mijenjan): prvo
23.10. (kao zadnji uspješni CI dan), pa 24.10. Vršna memorija procesa ~2,0 GB, 6-8 min po danu.
`data/mealmeter.duckdb` nije diran.

23.10. naspram 20.10.: exit 0, bez blokirajućih upozorenja (`! novi lanac stanic` ne blokira).

24.10. naspram 23.10.: update.py završava s **exit 0**, uz upozorenja `! nedostaje lanac branka`, `! nedostaje
lanac dm`, `! nedostaje lanac roto`. Upravo njih grep u workflowu pretvara u exit 3. Carry-forward je te lance već
pokrio: **12 trgovina, 129 434 cijene (branka, dm, roto) s datumom 23.10.**, `stale_days` 1. Čistih cijena je
17 034 672, a dan prije 17 041 200 (-0,04 %).

| lanac | trgovina 23.10. | 24.10. | proizvoda 23.10. | 24.10. | cijena 23.10. | 24.10. | promjena cijena |
|---|---:|---:|---:|---:|---:|---:|---:|
| **branka** | 2 | 0 | 14 537 | 0 | 24 575 | 0 | **-100 %** |
| **dm** | 1 | 0 | 21 910 | 0 | 21 910 | 0 | **-100 %** |
| **roto** | 9 | 0 | 9 201 | 0 | 82 949 | 0 | **-100 %** |
| kaufland | 53 | 53 | 19 354 | 19 366 | 736 890 | 741 619 | +0,6 % |
| lidl | 116 | 116 | 6 886 | 6 930 | 1 627 852 | 1 635 160 | +0,4 % |
| ostala 22 lanca | | | | | | | od -0,1 % do +0,6 % |
| ukupno | 1 569 | 1 557 | 478 668 | 433 531 | 17 930 684 | 17 821 166 | -0,6 % |

Provjeru su okinuli **branka, dm i roto** (nestali lanci); nijedan lanac nije pao za više od 20 %, a nijedan
drugi lanac nije pao za više od 0,1 %. Puni ispis: `data/raw/diag8/replay.log`.

**Sirove arhive 10.-24.10.2026.** (`/v0/list`, konačne verzije; tisuće redaka `prices.csv` po lancu, 0 = lanca
nema u arhivi):

| lanac | 10. | 11. | 12. | 13. | 14. | 15. | 16. | 17. | 18. | 19. | 20. | 21. | 22. | 23. | 24. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| dan | **sub** | **ned** | pon | uto | sri | čet | pet | **sub** | **ned** | pon | uto | sri | čet | pet | **sub** |
| boso | 73 | 73 | 73 | 73 | 73 | 73 | 73 | 74 | 74 | 74 | 74 | 74 | 74 | 75 | 75 |
| branka | **0** | **0** | 24 | 24 | 24 | 24 | 24 | **0** | **0** | 24 | 25 | 25 | 25 | 25 | **0** |
| bure | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 | 27 |
| djelo_vodice | 20 | 20 | 20 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 |
| dm | **0** | **0** | 22 | 22 | **0** | 22 | 22 | **0** | **0** | 22 | 22 | 22 | 22 | 22 | **0** |
| dukat | 5 | **0** | 5 | 5 | 4 | 5 | 5 | 5 | **0** | 5 | 5 | 5 | 5 | 5 | 5 |
| eurospin | 227 | 226 | 226 | 227 | 229 | 230 | 230 | 230 | 230 | 230 | 235 | 234 | 235 | 235 | 235 |
| gavranovic | 1690 | 1690 | 1690 | 1693 | 1699 | 1702 | 1705 | 1705 | 1477 | 1126 | 854 | **0** | 5 | 1714 | 1715 |
| jadranka_trgovina | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| kaufland | 737 | **0** | 737 | 736 | 738 | 738 | 738 | 738 | **0** | 738 | 737 | 737 | 736 | 737 | 742 |
| konzum | 1811 | 1809 | 1807 | 1805 | 1808 | 1806 | 1815 | 1818 | 1817 | 1816 | 1818 | 1825 | 1824 | 1824 | 1824 |
| ktc | 283 | 280 | 280 | 278 | 279 | 263 | 282 | 283 | 280 | 280 | 281 | 282 | 283 | 283 | 284 |
| lidl | 1694 | 1694 | 1688 | 1678 | 1677 | 1655 | 1654 | 1635 | 620 | 1635 | 1636 | 1640 | 1642 | 1628 | 1635 |
| lorenco | 20 | **0** | 20 | 20 | 20 | 20 | 20 | 20 | **0** | 20 | 20 | 20 | 20 | 20 | 20 |
| metro | 96 | 96 | 96 | 96 | 96 | 97 | 97 | 97 | 97 | 74 | 13 | 51 | **0** | 97 | 97 |
| ntl | 1550 | 1551 | 1551 | 1550 | 870 | 488 | 1561 | 1562 | 1562 | 1563 | 1565 | 1568 | 1568 | 1570 | 1571 |
| plodine | 6115 | 6116 | 6116 | 6115 | 6122 | 6125 | 6126 | 6126 | 6126 | 6125 | 6124 | 6128 | 6132 | 6110 | 6113 |
| ribola | 534 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 535 | 532 | 532 |
| roto | **0** | **0** | 83 | 83 | 83 | 83 | 83 | **0** | **0** | 83 | 83 | 83 | 83 | 83 | **0** |
| spar | 1306 | 1305 | 1304 | 1305 | 1306 | 1307 | 1307 | 1307 | 1306 | 1306 | 1308 | 1310 | 1311 | 1310 | 1310 |
| stanic | 50 | 49 | 49 | 49 | 49 | 50 | 50 | 50 | 50 | 50 | **0** | 50 | **0** | 50 | 50 |
| stridon | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 | 147 |
| studenac | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 169 | 170 | 170 |
| tommy | 994 | 994 | 991 | 992 | 992 | 993 | 994 | 994 | 994 | 991 | 991 | 991 | 992 | 992 | 993 |
| trgocentar | 43 | 43 | 43 | 43 | 43 | 43 | 43 | 43 | 23 | 43 | 43 | 43 | 43 | 43 | 43 |
| trgovina-krk | 154 | 154 | 154 | 154 | 155 | 155 | 155 | 155 | 155 | 155 | 155 | 155 | 155 | 155 | 155 |
| vrutak | 40 | **0** | 40 | 40 | 40 | 40 | 40 | 41 | 41 | 40 | 40 | 40 | 41 | 41 | 41 |
| zabac | 7 | **0** | 7 | 7 | 3 | 7 | 7 | **0** | **0** | 7 | 7 | 7 | 7 | 7 | 7 |
| **ukupno** | 17802 | 16988 | 17915 | 17904 | 17221 | 16833 | 17939 | 17792 | 15761 | 17316 | 16945 | 16200 | 16113 | 17931 | 17821 |

Zaključci:
- **branka, dm i roto nema svake subote i nedjelje** (10./11., 17./18., 24.10.), i to u konačnim arhivama (objava
  oko 22 h), ne samo u ranoj objavi u 14:26. To je obrazac izvora, ne privremeni kvar.
- Uz to izvor povremeno ispusti ili prepolovi lanac na dan-dva: nedjeljom dukat, kaufland, lorenco (11. i 18.10.,
  na 11.10. i vrutak, zabac); lidl 18.10. -62 %; ntl 14./15.10. -44 % i -69 %; gavranovic 18.-22.10. postupno do 0
  pa 23.10. natrag; metro 19.-22.10.; stanic 20. i 22.10.
- Pravilo provjere (`validate` + grep u workflowu: pad lanca > 20 % ili nestali lanac blokira) na tim podacima
  blokira **10 od 14 dana** (usporedba s prethodnim danom). Uz ponašanje CI-ja (nakon blokade se baza ne sprema u
  cache, pa se sljedeći dan uspoređuje sa zadnjom uspješnom) blokira 10.-11., 14.-15., 17.-22. i 24.10.
  Workflow postoji od 22.10.: 23.10. prolazi, **24.10. pada zbog branka, dm i roto** (oba pokušaja istog dana
  uspoređuju 24.10. s istom bazom od 23.10.).

**Je li razlika nastala kod nas?** Ne:
- usporedba je ispravna: `_previous` uzima statistiku zadnje učitane arhive (`clean.archive_stats`, sirovi retci
  prije carry-forwarda), a nova se broji iz sirovih tablica iste vrste; isti brojevi kao izravno iz zipa;
- cache: nakon blokade baza se ne sprema, pa je prethodna baza zadnja uspješna (23.10.), što je i namjera;
- carry-forward i promjene iz Koraka 7 (klasifikacija, `plan_basket`) ne utječu na provjeru, ona gleda sirove
  retke prije `carry_forward` i `build_clean`.

Jedina "naša" slabost je samo pravilo: per-lanac blokada ne odgovara izvoru koji vikendom redovito ispušta tri
lanca, a carry-forward (do 3 dana po trgovini, `stale_days` u odgovoru alata) već postoji upravo za taj slučaj, ali
ga blokada deploya preskače.

## 2. Odluka (prijedlog, čeka potvrdu)

Izvor je stvarno bez lanaca (nije lažna uzbuna kod nas), pa vrijedi prva grana: politika umjesto popravka.
Prijedlog (logika provjere **nije** mijenjana, čeka potvrdu):

1. **Izostali lanac ili pad pojedinog lanca > 20 % ne blokira deploy.** Pokriva ga postojeći carry-forward (po
   trgovini, trgovina s > 10 % manje cijena, najviše `CARRY_DAYS` = 3 dana). Prenesene cijene već imaju
   `stale_days` > 0 u odgovoru alata, a pravilo 10 uputa traži da se kaže od kojeg je datuma cjenik. update.py
   piše upozorenje s brojem prenesenih cijena i starošću, npr. `~ nedostaje lanac roto: preneseno 82949 cijena,
   stale_days 1`, a workflow ga prikaže kao `::warning::`.
2. **Blokira** (update.py exit 2, baza se ne mijenja, nema deploya):
   - ukupni broj sirovih redaka cijena pao je > 20 % naspram prethodne arhive (postojeće pravilo);
   - lanac izostaje dulje od `CARRY_DAYS`, pa bi nakon carry-forwarda ostao bez ijedne cijene, tj. nestao bi iz
     aplikacije. Trajni nestanak lanca odlučuje čovjek, uz ručno pokretanje s novim ulazom
     `allow_missing: <lanac>`;
   - nova zaštita: broj čistih cijena (`clean.prices`, nakon carry-forwarda) pao je > 20 % naspram prethodne
     baze. Hvata kvar u našoj izgradnji, ne u izvoru.
3. **Ukida se pravilo "broj lanaca pao > 20 %"**. U nedjelju 18.10. nestalo je 7 od 28 lanaca (-25 %), ali ukupno
   samo -11 % redaka, i carry-forward bi sve pokrio. Prag "više lanaca odjednom" iz zadatka ne odgovara podacima:
   svakog vikenda nestanu 3 lanca, a 18.10. 7, pa bi prag ili blokirao vikende ili bi morao biti ≥ 8 i tada ništa
   ne bi značio. Težinu nosi pravilo ukupnih redaka.
4. Blokadu određuje izlazni kod update.py, a ne grep po tekstu u workflowu. Grep `^  ! (.*->|nedostaje lanac)`
   se uklanja, pa ispis i odluka više ne mogu otići svaki na svoju stranu.
5. Testovi: vikend (3 lanca nestanu 2 dana → deploy, `stale_days` 1 i 2); 4. dan izostanka → exit 2; ukupni pad
   > 20 % → exit 2; scenarij 18.10. (7 lanaca, -11 %) → deploy; pad `clean.prices` > 20 % → exit 2.

**Simulacija na 10.-24.10.** (po lancu, ista statistika kao gore): sadašnje pravilo blokira 10 od 14 dana, a
predloženo nijedan. Najveća starost prenesenih cijena bila bi 2 dana (vikend), a najveći ukupni pad -11 %
(18.10.). Stvarni kvarovi i dalje bi blokirali: pad ukupno > 20 %, lanac bez podataka 4 dana i više ili kvar u
našoj izgradnji.

Otvoreno pitanje za tebe: treba li `allow_missing` (trajno uklanjanje lanca) ili radije zadržati njegove zadnje
cijene dulje uz veći `stale_days` (npr. 7 dana) prije blokade?

## 3. update.yml

- runner fiksiran na `ubuntu-24.04` (`ubuntu-latest` prelazi na Ubuntu 26);
- akcije na Node 24 (provjereno u `action.yml` svake verzije: `using: node24`):
  `actions/checkout@v4` -> `@v7`, `actions/cache/restore|save@v4` -> `@v6`, `astral-sh/setup-uv@v6` -> `@v10.3.2`.
  setup-uv od v8 izlazi kao nepromjenjivo izdanje bez pomičnog `v10` taga, pa je fiksiran na točnu verziju;
  `python-version` ulaz i dalje postoji. Ključevi cachea (`mealmeter-db-`) se ne mijenjaju.
- logika provjere (grep na `! ... ->` i `nedostaje lanac`) nije dirana.
