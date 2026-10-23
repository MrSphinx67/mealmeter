# Korak 7: ponašanje u stvarnim razgovorima

| točka | stanje |
|---|---|
| 0 mljeveno meso (juneće, svinjsko, miješano) | gotovo: nazivi sastojaka, nazivi proizvoda, vrsta; zlatni scenarij |

Ništa nije deployano.

## 0. Mljeveno meso

**Nazivi sastojaka.** Prije: "mljeveno meso junetina", "mljevena junetina" i "faširano" bili su `nepoznata namirnica`
(zato je Claude morao koristiti free_text i find_products); "juneće mljeveno meso" i "mljeveno juneće" već su radili,
ali "mljeveno juneće meso" nije. Popravak:
- `staples.yaml`, `mljeveno_meso`: sinonimi `mljevena`, `mljeveno mijesano meso`, `faširano`, `faširano meso`,
  `samljeveno meso`, i novo polje `value_words` (riječ u nazivu sastojka -> vrijednost atributa): junetina, juneće,
  govedina, goveđe... -> `vrsta=junece`; svinjetina, svinjski... -> `svinjsko`; mješano, miješana... -> `mijesano`;
  puretina, piletina, teletina.
- `basket.resolve_name`: uz vrijednosti atributa prepoznaje i `value_words`, a riječi iz sinonima iste namirnice
  ("meso" u "mljeveno juneće meso") ne smetaju.
- Vrsta nije navedena: kao i prije zadano miješano (`default_preference: miješano, juneće, svinjsko`, prva dostupna).

**Nazivi proizvoda.** Na stvarnim podacima (20.10.2026.) mnogi proizvodi mljevenog mesa uopće nisu bili namirnica
`mljeveno_meso`, a neki su imali krivu vrstu:
- nisu bili namirnica: Konzum "JUNETINA MLJEVENA", "JUN MLJEVENA 540G (MA)", "MLJEVENO MJEŠANO MESO", "MLJEVENA
  TELETINA"; Roto "JUN MLJEVENA 540G (MA) (8)"; Tommy "MLJEVENA JUN. 450 g", "MLJEVENO MIJEŠ. 450g", "MLJEVENO
  MIJ.MESO GASTRO"; Spar "Svinjetina mljevena", "Svinjska lopatica mljevena", "Juneći but mljeveni"; Kaufland "K-Pur
  mije. mlj. meso"; Studenac "MESO MLJ. MIJ. (SVI+JUN)"; Boso, Bure, Ribola, Djelo... Dodani `must_match` uzorci
  (`jun\w* mljev`, `mljeven\w* (jun|svinj|tele|mij|mjes|pur|pil)`, `mij\w* mlj`, `meso (mij|mjes)\w*( \w+){0,2} mlj`,
  `sv mlj`...). Ne pogađaju začine ("MJEŠ. KURK. MLJ."), keks, želatinu, pite i tjesteninu s mljevenim mesom (test).
- kriva vrsta: Konzum "JUN MLJEV MESO 850g" bio je zadano miješano (uzorak je tražio "jun."), Roto "SV MLJEV MESO
  850G" miješano umjesto svinjsko, Studenac "MLJEVENO JUNEĆE I SVINJSKO MESO" juneće umjesto miješano. Popravljeni
  uzorci vrste (`\bjun\b`, `\bsv\.?\s*mlj`, "X i/+/ Y" je miješano).

**Koji lanci imaju koju vrstu** (`plan_basket` 500 g sa `store`, puna baza od 20.10.2026., nakon popravka):

| lanac | Osijek: juneće | Zagreb: juneće | svinjsko (oba grada) | miješano (oba grada) |
|---|---|---|---|---|
| Konzum | JUN MLJEVENA 540G (MA), 6,59 € (prije: nema) | isto | SV MLJEVENA 540G (MA), 2,22 € (prije: nema) | da |
| Lidl | Mljeveno meso junetina 450 g, 10,78 € | isto | da | da |
| Kaufland | KPur. Juneće mljeveno meso 450 g, 10,78 € | isto | da | da |
| Spar | JUNEĆE MLJEVENO MESO 540 g, 6,59 € | isto | da | da |
| Plodine | JUNECE MLJEVENO MESO E500 G, 5,99 € | na vagu, 5,50 € | da | da |
| Eurospin | juneće obiteljsko pak., na vagu, 5,75 € | isto | da | da |
| Roto | JUN MLJEVENA 540G (MA) (8), 6,30 € (prije: nema) | isto | SV MLJEV MESO 850G | da |
| Tommy | nema trgovine u gradu | GOVEĐE MLJEVENO MESO, na vagu, 2,65 € | Zagreb | Zagreb |
| NTL | nema | nema | nema | da |
| Studenac | nema trgovine u gradu | nema trgovine u gradu | - | - |

Tommyjevo goveđe mljeveno meso je u cjeniku 5,31 €/kg (jedna trgovina, Ulica 144. brigade HV 5), što je neobično
jeftino za junetinu, ali je tako u službenom cjeniku; nije mijenjano.

**Zlatni scenarij** `basket_bolonjez_junece_osijek` (bolonjez iz zlatnih scenarija, "juneće mljeveno meso" 500 g,
Osijek): najjeftiniji Konzum 16,53 € (JUN MLJEVENA 540G), pa Eurospin 17,40, Roto 17,82, Plodine 18,00, Spar 19,40,
Lidl 20,68, Kaufland 21,46 €. Test provjerava da nema `unmatched`, da su Konzum, Lidl, Kaufland, Plodine i Spar u
usporedbi i da je odabrano meso `vrsta=junece`. (NTL je u `more_chains` sa 6 od 7 sastojaka, bez mesa: vidi točku 4.)

**Promjena ostalih zlatnih izlaza.** Od 22 postojeća scenarija promijenila su se samo dva bolonjeza u Zagrebu
(`basket_bolonjez_zagreb`, `basket_already_have_zagreb`): Tommy sad ima mljeveno meso ("MLJEVENO MIJ.MESO GASTRO",
na vagu 3,98 €/kg), pa je najjeftiniji Tommy 10,92 € umjesto Stridona 12,52 €; Kaufland 16,07 -> 15,47 €. Ostalih 20
je nepromijenjeno. Zlatni izlazi ponovno zapisani (23 scenarija).

**Provjera:**
- `tests/test_step7.py`: 14 naziva sastojaka (vrsta ili zadano miješano), nepromijenjeni "junetina", "mljevena
  paprika", "mljeveni papar"; 14 naziva proizvoda s vrstom; 6 naziva koji nisu mljeveno meso.
- Puna baza ponovno izgrađena (`build_clean`, uz memory_limit 2 GB: bez toga je proces ubijen zbog memorije), sažeta
  baza (`scripts/build_compact.py`, 92,3 MB) također.
- pytest: izlazni kod 0 (1031 prolazi, 3 preskočena); uz `MM_GOLDEN=1` (puna baza) izlazni kod 0; sažeta baza:
  `golden.py --check` 23/23 jednako.
