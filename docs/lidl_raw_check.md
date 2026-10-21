# Lidl: sirovi retci arhive 2026-10-20 i što parser izvodi (Korak 4C.9)

Izvor: `data/raw/2026-10-20/lidl/{products,prices}.csv`. Pakiranje opisuju samo stupci `unit` i `quantity`. Cijena je ista u svih 116/232 trgovina, a special_price je prazan u svim retcima. Parser je `analyze_pack(naziv)`, a kad naziv nema gramaturu, `parse_pack_unit_field(unit)`. ppu je price / pakiranje (€/kg, €/l ili €/kom).

| naziv | unit | quantity | price | unit_price | parser (pakiranje, izvor) | ppu | ocjena |
|---|---|---|---|---|---|---|---|
| Križevačka mljekara Trajno mlijeko | 1l | 1 | 0,52 | 0,52 | 1000 ml, unit | 0,52 | ✔ sigurno |
| Milkland trajno mlijeko 2,8% | 1l | 1.03 | 0,39 | 0,39 | 1000 ml, unit | 0,39 | ✔ slaže se; quantity 1.03 je bruto masa (kg) |
| Trajno mlijeko 2,8% (EAN 5998200400179) | 1l | 1 | 0,44 | 0,44 | 1000 ml, unit | 0,44 | ✔ |
| Viro Kristalni šećer | 1kg | 1 | 0,75 | 0,75 | 1000 g, unit | 0,75 | ✔ sigurno |
| Kiara Kristal šećer 1kg | 1kg | 1 | 0,99 | 0,99 | 1000 g, naziv | 0,99 | ✔ sigurno |
| Tena suncokretovo ulje | 1l | 0.92 | 1,45 | 1,45 | 1000 ml, unit | 1,45 | ✔ sigurno (0.92 = masa u kg) |
| Suncokretovo ulje (6906127) | 1l | 0.92 | 1,49 | 1,49 | 1000 ml, unit | 1,49 | ✔ |
| **Suncokretovo ulje 20g Lidla** | 1l | 0.92 | 1,38 | 1,38 | **20 g, naziv** | **69,00** | ✘ naziv ima prednost, a "20g" nije pakiranje; ispravno je 1 l (unit, quantity, unit_price) |
| Brašno TIP 550 glatko, 1kg | 1kg | 1 | 0,75 | 0,75 | 1000 g, naziv | 0,75 | ✔ sigurno |
| Vanilin šećer | 80g | 0.08 | 0,39 | 4,88 | 80 g, unit | 4,875 | ✔ sigurno (rinfuza, 10 vrećica od 8 g) |
| Dolcela Vanilin šećer | 6x8g | 0.048 | 0,99 | 0,99 | 48 g, unit (6 vrećica) | 0,165/vreć. | ✔; unit_price je po pakiranju, ne po kg |
| Dolcela Vanilin šećer | 8x8g | 0.064 | 0,59 | 9,22 | 64 g, unit (8 vrećica) | 0,074/vreć. | ✔; unit_price je po kg |
| Jaja iz kaveznog uzgoja, razred "S" | 10komad | 0.5 | 0,99 | 0,10 | 10 kom, unit | 0,099 | ✔ sigurno (unit_price po komadu) |
| Žito Jaja razred S | 10komad | 0.48 | 1,79 | 0,18 | 10 kom, unit | 0,179 | ✔ |
| Žito Jaja iz podnog uzgoja razred S | 10 komada | 0.48 | 1,59 | **1,59** | 10 kom, unit | 0,159 | ✔ naše; unit_price je po pakiranju |
| Piko Jaja razred S, Klasa A | 10komad | **1.06** | 1,79 | 0,18 | 10 kom, unit | 0,179 | ✔ naše; quantity 1,06 kg za 10 jaja S nije moguće |
| Samita jaja S klasa | 10komad | **0.049** | 1,99 | 0,20 | 10 kom, unit | 0,199 | ✔ naše; quantity 0,049 je krivo |

**Razlike:**
1. `unit` je pouzdan izvor pakiranja; u svim retcima osim jednog slaže se s nazivom i s unit_price.
2. `quantity` je masa u kg (ulje 1 l = 0,92), a kod jaja je nedosljedan (0,049 / 0,48 / 0,5 / 1,06), pa se ne koristi.
3. `unit_price` je za većinu proizvoda po kg, l ili komadu, ali za Dolcela 6x8g i Žito podna jaja S jednak je cijeni pakiranja. Zato se ne koristi kao provjera bez pakiranja.
4. Jedina greška parsera je "Suncokretovo ulje 20g Lidla": gramatura iz naziva (20 g) pobjeđuje stupac unit (1l). Prijedlog: kad unit
   daje drugu jedinicu (ml naspram g) ili > 10x veće pakiranje, vrijedi unit. Nije primijenjeno (točka je samo čitanje).
5. "Maria Orginal XXL (suncokret. ulje)" (5x200g) su keksi; pravila namirnice ulje ih isključuju.

**Sigurno ispravni** (unit, naziv i unit_price se slažu): Križevačka, Milkland, Viro, Kiara, Tena, Brašno TIP 550 1kg, Vanilin šećer 80 g, kavezna jaja S i Žito jaja S. Cijene Milklanda (0,39 €/l) i kaveznih jaja S (0,099 €/kom) su stvarne, a ne greške pakiranja.
