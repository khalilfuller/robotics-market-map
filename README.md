# Robotics Market Map

## Build

```
python3 -I build_map.py              # map.html          — standalone file
python3 -I build_map.py --artifact   # map.artifact.html — for claude.ai hosting
```

**Hosted:** https://claude.ai/artifact/DkB4hnUpUssNbfrmkYwjKS
Private by default — share it from the page's Share menu.
To update, rebuild with `--artifact` and republish the same file path.

Open `map.html` directly in a browser — self-contained apart from the Google Fonts link.

The map is interactive: click any company for a card with its blurb, HQ and link;
filter by business model; search by name.

## Files

| file | what it is |
|---|---|
| `companies.csv` | source of truth — 166 companies. Edit this. |
| `build_map.py` | generator: design tokens + layout + ordering |
| `map.html` | the rendered map, interactive (generated — don't hand-edit) |
| `brand.md` | type, colour, corners, voice — the design source of truth |
| `enrich.py` | fetches each site's title + meta description into `site_meta.json` |
| `WORDMARK` in build_map.py | empty = no wordmark; set a string to show one top-right |
| `companies.json` | same data as CSV, for other consumers |
| `logos/`, `fetch_logos.py`, `contact-sheet.html` | logo experiment — not used by the map |

## Brand

[brand.md](brand.md) is the source of truth for type, colour, corners and voice.
Change it first, then mirror it in `TOKENS` in `build_map.py`.

## Adjusting the styling

Everything visual is in two places at the top of `build_map.py`:

- **`TOKENS`** — a dict of CSS custom properties: colors, radii, padding, type
  sizes, tracking, column count. Change a value, re-run, done. These are emitted
  into `:root`, so you can also live-tweak them in browser devtools first and
  then paste the winning values back.
- **`TITLE` / `BYLINE` / `WORDMARK`** — header text; empty `WORDMARK` hides it
- **`SHOW_MODEL`** — off. True re-enables the business-model dots, legend and filters
- **`TIER_ORDER` / `BUCKET_ORDER`** — controls what appears where. A bucket not
  listed in `BUCKET_ORDER` sorts to the end.

Layout knobs worth knowing:
- `--cols` — columns per tier section (currently 3)
- `--page-w` — total canvas width; raise for a wider poster format
- `.card.narrow` — cards with ≤4 companies render in one column instead of two

## Data model

`name, tier, bucket, domain, hq, description, source, notes, logo_file, logo_status, model, cluster, status`

- `status` — `active`, or `part of <parent>` for an acquired company or subsidiary.
  Those render in grey on the map, with the parent shown in the detail card.

- `model` — business model, per the neo-integrator framing
  (avi.dog/articles/the-rise-of-the-neo-integrator). **Kept in the data but not
  shown on the site**: set `SHOW_MODEL = True` in `build_map.py` to bring back
  the dots, legend and filter buttons.
  - `lab` — sells intelligence; the commoditizing layer
  - `neo-integrator` — owns deployment in a vertical; teleop/RaaS revenue, data compounds
  - `component` — sells hardware into someone else's deployment
  - `platform` — sells tooling to the other layers
  - `service` — sells deployment labor, sourcing, capital or risk cover


- `tier` — Intelligence / Platform / Hardware / Vertical Robotics Companies / Market Infrastructure
- `source` — `obvious`, `baymap`, `userlist`, `research`, `pi-api-beta`, `ziegler-map`
- `cluster` — which regional ecosystem map the company appeared on (Bay Area / Zurich / Boston);
  reserved for a geography view later
- `notes` — rows containing `UNVERIFIED` are **excluded from the map** by the builder.
  Rows marked `AMBIGUOUS` are included but need confirming.

## Structure

5 tiers, 37 buckets, 396 companies on the map (399 in the CSV; 3 held back as unverified).

By cluster: 55 Bay Area, 37 Boston, 26 Zurich. 27 companies are owned by a larger company.

A bucket belongs to exactly one tier. `build_map.py` sorts unlisted buckets last,
so add any new bucket to `BUCKET_ORDER`.
