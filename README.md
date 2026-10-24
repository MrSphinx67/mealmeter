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

Pitanje:

> Radim grah varivo u Osijeku, treba mi 500 g kuhanog graha, a kupit ću suhi. Gdje je najjeftinije?

Claude pozove `plan_basket` i odgovori otprilike ovako (cijene iz cjenika od 20.10.2026.):

> Za 500 g kuhanog graha treba oko 200 g suhog (procjena). Najjeftinije: Konzum (GRAH PINTO VEDRINI 500 g) i Spar,
> 1,19 € za pakiranje; utrošak je 0,48 €. Kaufland i Lidl 1,49 €, Plodine 1,51 €, Eurospin 1,59 €, Roto 2,16 €,
> NTL 2,69 €.

Točan tekst ovisi o asistentu; brojke dolaze iz alata.

### Izvor podataka i licence

- **Podaci:** cijene.dev (DobarKod), prema [uvjetima korištenja](https://cijene.dev/uvjeti-koristenja) cijene.dev.
  cijene.dev prikuplja službene cjenike koje trgovci objavljuju po Odluci o objavi cjenika (NN 75/2025). Mealmeter ih
  samo čita i ne mijenja cijene.
- **Kod:** [MIT](LICENSE).

### Ograničenja

- **Cijene su iz cjenika, a ne sa zalihe.** Cjenik ne kaže ima li proizvoda na polici, a cijena u trgovini može biti
  drukčija. Neki lanci objavljuju iste cijene za cijelu zemlju. Ako lanac jedan dan ne objavi cjenik, uzima se
  prethodni (najviše 7 dana) i navodi se njegov datum.
- **Točnost nije izmjerena.** Provjerena je samo ručno, na nekoliko recepata i trgovina; sustavne usporedbe s
  cijenama na polici nema.
- **Oko 80 osnovnih namirnica** (`list_staples`), ne svi proizvodi. Ostalo se traži slobodnim tekstom, slabije.
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
uv run python scripts/update.py          # preuzme zadnju arhivu s cijene.dev i izgradi bazu (~1,1 GB, ~10 min)
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
2. `scripts/build_compact.py` napravi sažetu bazu (~92 MB) koja stane u Vercel.
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

Question:

> I'm making bean stew in Osijek and need 500 g of cooked beans; I'll buy dried. Where is it cheapest?

Claude calls `plan_basket` and answers roughly like this (prices from the 20 Oct 2026 price lists):

> 500 g of cooked beans is about 200 g dried (an estimate). Cheapest: Konzum (GRAH PINTO VEDRINI 500 g) and Spar,
> €1.19 per pack; the amount used costs €0.48. Kaufland and Lidl €1.49, Plodine €1.51, Eurospin €1.59, Roto €2.16,
> NTL €2.69.

The wording depends on the assistant; the numbers come from the tool.

### Data source and licenses

- **Data:** cijene.dev (DobarKod), under the cijene.dev [terms of use](https://cijene.dev/uvjeti-koristenja).
  cijene.dev collects the official price lists that retailers publish under the Croatian price list decision
  (NN 75/2025). Mealmeter only reads them and does not change prices.
- **Code:** [MIT](LICENSE).

### Limitations

- **Prices come from price lists, not stock.** A price list does not say whether the product is on the shelf, and the
  in-store price may differ. Some chains publish one national price list. If a chain skips a day, the previous list
  is used (at most 3 days old) and its date is shown.
- **Accuracy has not been measured.** It has only been checked by hand, on a few recipes and stores; there is no
  systematic comparison with shelf prices.
- **About 80 basic staples** (`list_staples`), not every product. Anything else is searched as free text, less
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
uv run python scripts/update.py          # downloads the latest cijene.dev archive and builds the database (~1.1 GB, ~10 min)
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
2. `scripts/build_compact.py` builds the compact database (~92 MB) that fits on Vercel.
3. Golden outputs (the full and compact databases must give the same answers) and tests.
4. `vercel build` and `vercel deploy --prebuilt --prod`.

The databases are not in Git. Manual deployment: [docs/DEPLOY.md](docs/DEPLOY.md) (Croatian).
