# Mealmeter

[Hrvatski](#hrvatski) · [English](#english)

## Hrvatski

Mealmeter je besplatan open-source MCP poslužitelj (konektor za AI asistente) koji za jelo ili popis
sastojaka i grad pronalazi cijene u hrvatskim trgovinama. Prikazuje koliko košta košarica u svakoj
trgovini u gradu i koja je najjeftinija.

- **Izvor podataka:** dnevni službeni cjenici trgovina koje prikuplja [cijene.dev](https://cijene.dev)
  (DobarKod). Mealmeter ih samo čita.
- **Kako se računa cijena:** iz cjenika se računa cijena cijelih pakiranja koja treba kupiti
  (`total_to_buy`) i razmjerni trošak utrošene količine (`total_used`).

### Alati

| alat | što radi |
|---|---|
| `find_products` | proizvodi po nazivu ili namirnici, s rasponom cijena |
| `get_prices` | cijene jednog proizvoda (EAN) po trgovinama |
| `plan_basket` | košarica za recept: cijena po trgovini, najbolja trgovina, alternative, stvarne cijene korisnika |
| `list_stores` | trgovine u gradu s adresama |
| `convert_units` | žlice, šalice, komadi → g/ml (procjena) |
| `list_staples` | podržane namirnice i njihovi atributi |

### Pokretanje

```sh
uv sync
uv run python scripts/update.py          # preuzme najnoviju arhivu s cijene.dev i izgradi bazu
uv run python -m mealmeter.server        # stdio (Claude Desktop)
uv run python -m mealmeter.server --http --port 8000   # streamable HTTP na http://127.0.0.1:8000/mcp
```

HTTP poslužitelj je bez prijave, jer su podaci javni i samo za čitanje. Ograničenja (u minuti, env varijable):
- 60 upita po IP-u (`MM_RATE_IP`), 30 po MCP sesiji (`MM_RATE_SESSION`), 1000 ukupno (`MM_RATE_GLOBAL`);
  IP iz `CF-Connecting-IP` / `X-Forwarded-For` samo uz `TRUSTED_PROXY=1`;
- zahtjev do 64 KB;
- odgovor alata do 20 KB. `plan_basket` zadano vraća sažet odgovor (oko 2-3 KB za 7 sastojaka): najbolju
  trgovinu sa stavkama i najviše 2 druge trgovine kao jedan redak; `detail: true` vraća sve trgovine i polja.

Poslužitelj sam primijeti kad `scripts/update.py` zamijeni datoteku baze i otvori novu, bez restarta.

### Dodavanje u Claude

**Claude Desktop (lokalno, stdio):** u `claude_desktop_config.json` dodaj sadržaj datoteke
[docs/claude_desktop_config.json](docs/claude_desktop_config.json). Putanju zamijeni stvarnom putanjom do
repozitorija. Ako `uv` nije u PATH-u, upiši punu putanju do `uv`. Zatim ponovno pokreni Claude Desktop.

**Claude (web, udaljeno):** kad poslužitelj radi preko HTTPS-a (`--http` iza HTTPS proxyja), dodaj URL
`https://<domena>/mcp` kao prilagođeni konektor (Settings → Connectors).

### Dodavanje u ChatGPT

ChatGPT spaja samo udaljene MCP poslužitelje preko HTTPS-a:
1. Pokreni `--http` iza HTTPS-a.
2. Dodaj URL `https://<domena>/mcp` kao konektor (Settings → Connectors, uz uključen developer mode).

Javni URL još ne postoji.

### Primjeri upita

- „Koliko u Osijeku košta 250 g glatkog brašna, 0,5 l mlijeka i 3 jaja? Sol imam.“
- „Napravi košaricu za špagete bolonjez za 4 osobe u Zagrebu, idem u Konzum na Savskoj.“
- „Brašno je u trgovini zapravo 1,20 €, preračunaj.“
- „Gdje je najjeftinije trajno mlijeko 2,8 % u Splitu?“
- „Koliko grama su 2 žlice šećera?“

### Ograničenja

- **Odabrane namirnice:** oko 75 osnovnih namirnica (`list_staples`), ne svi proizvodi iz trgovine.
- **Mahunarke:** za grah, leću, slanutak i grašak recept obično ne kaže je li suho ili iz konzerve.
  Košarica ih ne računa dok se oblik (`form`) ne zada, nego vraća pitanje.
- **Bez prinosa:** ne računa se gubitak pri čišćenju i kuhanju (kora, kosti, upijanje vode).
- **Cijene su iz cjenika:** u trgovini se mogu razlikovati, a cjenik nije zaliha. Neki lanci objavljuju
  nacionalne cijene; stara cijena se prenosi najviše 3 dana i označena je sa `stale_days`.
- **Procjene:** kuhinjske mjere i komadi pretvaraju se procjenom.

### Licenca

Kod: [MIT](LICENSE). Uvjeti korištenja podataka o cijenama su na [cijene.dev](https://cijene.dev).

## English

Mealmeter is a free, open-source MCP server (a connector for AI assistants). Given a dish or an
ingredient list and a city, it finds grocery prices in Croatian stores. It shows what the basket costs in
each store in the city and which store is cheapest.

- **Data source:** the stores' official daily price lists, collected by [cijene.dev](https://cijene.dev)
  (DobarKod). Mealmeter only reads them.
- **How prices are computed:** from the price lists, both the cost of the whole packs to buy
  (`total_to_buy`) and the cost of the amount actually used (`total_used`).

### Tools

| tool | what it does |
|---|---|
| `find_products` | products by name or staple, with price ranges |
| `get_prices` | prices of one product (EAN) per store |
| `plan_basket` | recipe basket: cost per store, best store, alternatives, user-reported prices |
| `list_stores` | stores in a city with addresses |
| `convert_units` | spoons, cups, pieces → g/ml (estimate) |
| `list_staples` | supported staples and their attributes |

### Running

```sh
uv sync
uv run python scripts/update.py          # downloads the latest archive from cijene.dev and builds the database
uv run python -m mealmeter.server        # stdio (Claude Desktop)
uv run python -m mealmeter.server --http --port 8000   # streamable HTTP at http://127.0.0.1:8000/mcp
```

The HTTP server needs no login, because the data is public and read-only. Limits (per minute, env variables):
- 60 requests per IP (`MM_RATE_IP`), 30 per MCP session (`MM_RATE_SESSION`), 1000 in total (`MM_RATE_GLOBAL`);
  the IP comes from `CF-Connecting-IP` / `X-Forwarded-For` only with `TRUSTED_PROXY=1`;
- requests up to 64 KB;
- tool responses up to 20 KB. `plan_basket` returns a compact response by default (about 2-3 KB for 7
  ingredients): the best store with its items and at most 2 other stores as one row each; `detail: true`
  returns all stores and fields.

The server notices when `scripts/update.py` replaces the database file and reopens it without a restart.

### Adding to Claude

**Claude Desktop (local, stdio):** add the contents of
[docs/claude_desktop_config.json](docs/claude_desktop_config.json) to `claude_desktop_config.json` and
replace the path with the real path to the repository. If `uv` is not on your PATH, use the full path
to `uv`. Then restart Claude Desktop.

**Claude (web, remote):** once the server runs over HTTPS (`--http` behind an HTTPS proxy), add
`https://<domain>/mcp` as a custom connector (Settings → Connectors).

### Adding to ChatGPT

ChatGPT connects only to remote MCP servers over HTTPS:
1. Run `--http` behind HTTPS.
2. Add `https://<domain>/mcp` as a connector (Settings → Connectors, with developer mode on).

There is no public URL yet.

### Example prompts

- "How much do 250 g of plain flour, 0.5 l of milk and 3 eggs cost in Osijek? I have salt."
- "Make a basket for spaghetti bolognese for 4 in Zagreb, I shop at Konzum on Savska."
- "The flour actually costs €1.20 in the store, recalculate."
- "Where is the cheapest UHT milk 2.8% in Split?"
- "How many grams are 2 tablespoons of sugar?"

### Limitations

- **Selected staples:** about 75 basic staples (`list_staples`), not every product in the store.
- **Legumes:** for beans, lentils, chickpeas and peas, recipes rarely say whether they are dried or
  canned. The basket does not count them until a `form` is given; it returns a question instead.
- **No yields:** losses from peeling, bones or cooking are not modeled.
- **Prices come from price lists:** they may differ in store, and a price list is not stock. Some chains
  publish national prices; an old price is carried forward for at most 3 days and marked with `stale_days`.
- **Estimates:** kitchen measures and pieces are converted by estimate.

### License

Code: [MIT](LICENSE). Terms of use for the price data are on [cijene.dev](https://cijene.dev).
