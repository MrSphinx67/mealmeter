# Mealmeter

[Hrvatski](#hrvatski) · [English](#english)

## Hrvatski

### Što je Mealmeter

Mealmeter je MCP poslužitelj (konektor za AI asistente poput Claudea). Za jelo ili popis namirnica i grad
računa koliko košarica stoji u svakom trgovačkom lancu u gradu i koja je trgovina najjeftinija. Cijene čita iz
službenih dnevnih cjenika hrvatskih trgovina. Besplatan je, otvorenog koda i bez prijave.

Alati: `plan_basket` (košarica za recept), `find_products` (proizvodi i rasponi cijena), `get_prices` (cijene jednog
proizvoda po trgovinama), `list_stores` (trgovine u gradu), `convert_units` (žlice i šalice u g/ml), `list_staples`
(podržane namirnice).

### Dodavanje u Claude

Postavke → Konektori → Dodaj prilagođeni konektor (Settings → Connectors → Add custom connector), URL:

```
https://mealmeter.vercel.app/mcp
```

Prijava nije potrebna.

### Primjer

Stvarni razgovor (29.10.2026.), skraćen:

> **Ti:** Koliko košta bolonjez za 4 osobe?
>
> **Claude:** U kojem si gradu, što već imaš doma i ideš li u određenu trgovinu ili da usporedim sve u gradu?
>
> **Ti:** Osijek, imam sol, papar i ulje, usporedi sve.

Claude pozove `plan_basket` (tagliatelle, mljeveno meso, panceta, luk, mrkva, celer, češnjak, pasirana rajčica,
crno vino, kocka za juhu, maslac, parmezan) i odgovori otprilike ovako:

> Sve možeš kupiti u:
> - Plodine (J. J. Strossmayera 343; 2 trgovine): 17,87 €
> - Konzum (Sjenjak 133, Trg Ante Starčevića 10; 7 trgovina): 18,83 €
> - Lidl (Sv. Leopolda Bogdana Mandića 33 A, J. J. Strossmayera 350; 3 trgovine): 20,44 €
> - Spar (Sv. Leopolda B. Mandića 7, Svilajska 31A; 5 trgovina): 21,60 €
> - Kaufland (Josipa Reihl-Kira 40; 2 trgovine): 23,95 €
>
> Najjeftinije su Plodine, 6,08 € manje od Kauflanda; od toga se u jelu stvarno potroši oko 9,24 €.
> Eurospin oko 18,85 €, nedostaje: celer. Umjesto parmezana je Grana Padano (sličan tvrdi sir).
> Cijene iz cjenika od 28.10.2026.; u trgovini se mogu razlikovati.

Točan tekst ovisi o asistentu; brojke dolaze iz alata.

### Izvor podataka i zahvale

Cijene dolaze iz službenih cjenika koje trgovci moraju javno objavljivati
(NN 75/25; od 17. 11. 2026. NN 101/26 i 110/26).
Mealmeter koristi pročišćene dnevne arhive s **[cijene.dev](https://cijene.dev)**,
koje izrađuje i održava Senko Rašić ([DobarKod](https://dobarkod.hr)).
Bez tog posla ovaj projekt ne bi postojao, hvala!

Podaci se koriste prema [uvjetima korištenja cijene.dev](https://cijene.dev/uvjeti-koristenja).
Mealmeter koristi samo javne dnevne arhive (ne njihov API ni kod) i nije povezan s
cijene.dev ni DobarKodom. Za greške u Mealmeteru javi se ovdje, ne njima.

### Licenca

Kod: [MIT](LICENSE).

### Ograničenja

- **Cijene su iz cjenika, a ne sa zalihe.** Cjenik ne kaže ima li proizvoda na polici, a cijena u trgovini može biti
  drukčija. Neki lanci objavljuju iste cijene za cijelu zemlju. Ako lanac jedan dan ne objavi cjenik, uzima se
  prethodni (najviše 7 dana) i navodi se njegov datum.
- **Točnost nije izmjerena.** Provjerena je samo ručno, na nekoliko recepata i trgovina; sustavne usporedbe s
  cijenama na polici nema.
- **Oko 95 osnovnih namirnica** (`list_staples`), ne svi proizvodi. Ostalo se traži slobodnim tekstom, slabije.
- **Procjene:** žlice, šalice, komadi i prinos suhih mahunarki pretvaraju se procjenom. Gubitak pri čišćenju i kuhanju
  (kora, kosti) se ne računa.
- **Mahunarke:** ako se ne kaže je li grah, leća, slanutak ili grašak suh, iz konzerve ili smrznut, alat pita.

### Privatnost

Nema računa ni kolačića. Sadržaj upita (sastojci, grad) se ne sprema. Zapisuje se samo naziv alata, status, trajanje
i skraćena IP adresa (bez zadnjeg dijela, npr. `203.0.113.x`). Poslužitelj radi na Vercelu.

### Lokalno pokretanje

Potrebni su Python 3.12 i [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run python scripts/update.py          # preuzme zadnju arhivu s cijene.dev i izgradi bazu (~1,5 GB, ~10 min)
uv run python -m mealmeter.server        # stdio, za Claude Desktop
uv run python -m mealmeter.server --http --port 8000   # HTTP na http://127.0.0.1:8000/mcp
uv run pytest -q                         # testovi
```

Za Claude Desktop: sadržaj [docs/claude_desktop_config.json](docs/claude_desktop_config.json) dodaj u svoj
`claude_desktop_config.json` i upiši stvarnu putanju do repozitorija.

### Kako se osvježava

GitHub Actions ([.github/workflows/update.yml](.github/workflows/update.yml)) se pokreće dva puta dnevno
(13:30 i 21:30 UTC):

1. `scripts/update.py` preuzme novu dnevnu arhivu s cijene.dev i izgradi bazu. Lanac koji nedostaje (npr. vikendom)
   zadržava prethodne cijene najviše 7 dana, uz upozorenje. Ako je i nakon toga cijena manje za više od 20 %,
   postupak staje i ništa se ne objavljuje.
2. `scripts/build_compact.py` napravi sažetu bazu (dvije datoteke, ~46 i ~43 MB) koja stane u Vercel.
3. Zlatni izlazi (puna i sažeta baza moraju dati iste odgovore) i testovi.
4. `vercel build` i `vercel deploy --prebuilt --prod`.

Baze nisu u Gitu. Ručni deploy: [docs/DEPLOY.md](docs/DEPLOY.md).

## English

### What Mealmeter is

Mealmeter is an MCP server (a connector for AI assistants such as Claude). Given a dish or a shopping list and a
city, it works out what the basket costs at each grocery chain in that city and which store is cheapest. Prices come
from the official daily price lists of Croatian stores. It is free, open source, and needs no login.

Tools: `plan_basket` (basket for a recipe), `find_products` (products and price ranges), `get_prices` (prices of one
product per store), `list_stores` (stores in a city), `convert_units` (spoons and cups to g/ml), `list_staples`
(supported staples).

### Adding it to Claude

Settings → Connectors → Add custom connector, URL:

```
https://mealmeter.vercel.app/mcp
```

No login is needed.

### Example

A real conversation (29 Oct 2026), shortened:

> **You:** How much does a bolognese for 4 people cost?
>
> **Claude:** Which city are you in, what do you already have at home, and are you going to a particular store or
> should I compare all of them?
>
> **You:** Osijek, I have salt, pepper and oil, compare everything.

Claude calls `plan_basket` (tagliatelle, minced meat, pancetta, onion, carrot, celery, garlic, passata, red wine,
stock cube, butter, parmesan) and answers roughly like this:

> You can buy everything at:
> - Plodine (J. J. Strossmayera 343; 2 stores): €17.87
> - Konzum (Sjenjak 133, Trg Ante Starčevića 10; 7 stores): €18.83
> - Lidl (Sv. Leopolda Bogdana Mandića 33 A, J. J. Strossmayera 350; 3 stores): €20.44
> - Spar (Sv. Leopolda B. Mandića 7, Svilajska 31A; 5 stores): €21.60
> - Kaufland (Josipa Reihl-Kira 40; 2 stores): €23.95
>
> Plodine is cheapest, €6.08 less than Kaufland; about €9.24 of that is actually used in the dish.
> Eurospin about €18.85, missing: celery. Grana Padano (a similar hard cheese) instead of parmesan.
> Prices from the 28 Oct 2026 price lists; in-store prices may differ.

The wording depends on the assistant; the numbers come from the tool.

### Data source and acknowledgements

Prices come from the official price lists that Croatian retailers are required to publish
(NN 75/25; from 17 Nov 2026, NN 101/26 and 110/26).
Mealmeter uses the cleaned daily archives from **[cijene.dev](https://cijene.dev)**,
built and maintained by Senko Rašić ([DobarKod](https://dobarkod.hr)).
This project would not exist without that work, thank you!

The data is used under the [cijene.dev terms of use](https://cijene.dev/uvjeti-koristenja).
Mealmeter only uses the public daily archives (not their API or code) and is not affiliated
with cijene.dev or DobarKod. Please report Mealmeter issues here, not to them.

### License

Code: [MIT](LICENSE).

### Limitations

- **Prices come from price lists, not stock.** A price list does not say whether the product is on the shelf, and the
  in-store price may differ. Some chains publish one national price list. If a chain skips a day, the previous list
  is used (at most 7 days old) and its date is shown.
- **Accuracy has not been measured.** It has only been checked by hand, on a few recipes and stores; there is no
  systematic comparison with shelf prices.
- **About 95 basic staples** (`list_staples`), not every product. Anything else is searched as free text, less
  reliably.
- **Estimates:** spoons, cups, pieces and the yield of dried legumes are estimated. Losses from peeling and cooking
  (skins, bones) are not modelled.
- **Legumes:** if you don't say whether beans, lentils, chickpeas or peas are dried, canned or frozen, the tool asks.

### Privacy

No accounts, no cookies. Query content (ingredients, city) is not stored. Only the tool name, status, duration and a
shortened IP address (last part removed, e.g. `203.0.113.x`) are logged. The server runs on Vercel.

### Running locally

You need Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run python scripts/update.py          # downloads the latest cijene.dev archive and builds the database (~1.5 GB, ~10 min)
uv run python -m mealmeter.server        # stdio, for Claude Desktop
uv run python -m mealmeter.server --http --port 8000   # HTTP at http://127.0.0.1:8000/mcp
uv run pytest -q                         # tests
```

For Claude Desktop, add the contents of [docs/claude_desktop_config.json](docs/claude_desktop_config.json) to your
`claude_desktop_config.json` and put in the real path to the repository.

### How updates work

GitHub Actions ([.github/workflows/update.yml](.github/workflows/update.yml)) runs twice a day (13:30 and 21:30 UTC):

1. `scripts/update.py` downloads the new daily archive from cijene.dev and builds the database. A missing chain
   (e.g. at weekends) keeps its previous prices for up to 7 days, with a warning. If there are still more than
   20 % fewer prices after that, the run stops and nothing is published.
2. `scripts/build_compact.py` builds the compact database (two files, ~46 and ~43 MB) that fits on Vercel.
3. Golden outputs (the full and compact databases must give the same answers) and tests.
4. `vercel build` and `vercel deploy --prebuilt --prod`.

The databases are not in Git. Manual deployment: [docs/DEPLOY.md](docs/DEPLOY.md) (Croatian).
