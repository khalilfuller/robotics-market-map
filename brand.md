# Brand — v2

Source of truth for how the map looks. Change this first, then mirror it in
`TOKENS` in `build_map.py`.

## Direction

A technical reference document, not a poster. The subject is machinery, so the
page borrows from the things that document machinery: parts catalogues, datasheets,
engineering indexes. Dense, ruled, quiet. Information first.

v1 was a black terminal with white cards. v2 drops the cards entirely — at 340+
entries the boxes cost more space than the grouping they bought, and the page
reads better as ruled columns of type.

## Typeface

**IBM Plex**, both widths. Drawn for an engineering company, which is the point,
and it is neither of the two faces that make a page look auto-generated.

```
https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@400;600;700&display=swap
```

- **IBM Plex Sans Condensed** — title, tier labels, category labels, UI
- **IBM Plex Mono** — company names, metadata, anything that reads as data

Fallbacks: `ui-sans-serif, system-ui` and `ui-monospace, Menlo, monospace`.

**One weight per element.** Never mix weights inside a line.

| use | face | weight | size | tracking | case |
|---|---|---|---|---|---|
| page title | Sans Cond | 700 | 30px | 0.02em | upper |
| byline / note | Mono | 400 | 11px | 0.02em | as written |
| tier label | Sans Cond | 700 | 12px | 0.22em | upper |
| category label | Sans Cond | 600 | 10.5px | 0.16em | upper |
| company name | Mono | 400 | 12.5px | 0 | as written |
| UI / meta | Mono | 400 | 10.5px | 0.08em | upper |

## Colour

Light by default, with a real dark mode — not an inversion. Every colour is a
token defined on `:root` first, so neither theme can go missing.

| token | light | dark | use |
|---|---|---|---|
| `--paper` | `#FBFBF9` | `#121415` | page |
| `--ink` | `#16181A` | `#EDEEEA` | primary text |
| `--ink-2` | `#5E6468` | `#8A9196` | secondary text, owned companies |
| `--rule` | `#DEDFDA` | `#2A2E30` | hairlines |
| `--rule-2` | `#C6C8C2` | `#3A4042` | heavier rules |
| `--accent` | `#C2410C` | `#F97316` | links, hover, focus |

One accent, drawn from the safety-amber of machine guarding. It appears on
interaction and nowhere else. Emphasis otherwise comes from weight, space and case.

## Rules, not boxes

- Categories are separated by a 1px `--rule`, never a border or a fill
- Tier headings sit on a 2px `--rule-2`
- No card backgrounds, no shadows, no radius above 2px
- Nothing is pill-shaped

## Status

A company owned by a larger one is set in `--ink-2` rather than `--ink`, with a
key in the header. Acquisition is information, not a footnote: the map should not
present a subsidiary as an independent company.

## Layout

- Max canvas `1700px`, page padding `36px`
- Four columns per tier at full width, two at 1100px, one at 760px
- Name lists run two columns inside a category, one when narrow
- Density over whitespace

## Voice

- One sentence per company; what it does and for whom
- No "leading", "innovative", "cutting-edge", "revolutionary"
- Funding only when it defines the company's position
