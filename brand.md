# Brand — v3

Source of truth for how the map looks. Change this first, then mirror it in
`TOKENS` in `build_map.py`.

## Direction

A dense reference document. Dark canvas, white cards, one accent.

**Cards earn their keep.** v2 replaced them with hairline rules on a light page
and the map got harder to use: without an edge, the eye has nothing to stop at,
and 33 categories ran together. The boxes are back. A category is an object, and
it should look like one.

The accent — a safety amber borrowed from machine guarding — carries every
interactive state and the tier headings. Nothing else is coloured.

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
| page title | Sans Cond | 700 | 32px | 0.02em | upper |
| byline / note | Mono | 400 | 11px | 0.02em | as written |
| tier label | Sans Cond | 700 | 12px | 0.22em | upper |
| category label | Sans Cond | 600 | 10.5px | 0.16em | upper |
| company name | Mono | 400 | 14px | 0 | as written |
| UI / meta | Mono | 400 | 10.5px | 0.08em | upper |

## Colour

A single committed dark look — deliberately one theme, not a missing one.

| token | value | use |
|---|---|---|
| `--bg` | `#0E0F10` | canvas |
| `--paper` | `#FFFFFF` | cards and panel |
| `--ink` | `#15171A` | text on a card |
| `--ink-2` | `#747B80` | secondary text on a card |
| `--chalk` | `#F2F3F1` | text on the canvas |
| `--chalk-2` | `#8C9398` | secondary text on the canvas |
| `--rule` | `#2B2E30` | hairlines on the canvas |
| `--rule-paper` | `#E6E7E3` | hairlines on a card |
| `--accent` | `#F26B21` | tier labels, hover, focus, links |

## Boxes

- A category is a white card: `3px` radius, `18px 20px 20px` padding
- Category label is a filled chip, `--ink` on white, `2px` radius
- Tier headings are accent-coloured over a `--rule` hairline
- No shadows. Nothing is pill-shaped.

## Status

A company owned by a larger one gets an accent-coloured `*` after its name, with
a key in the header. The name itself stays at full contrast — greying it out made
those 27 entries harder to read than everything around them, which punished the
reader for a fact about the company. Acquisition is information, not a demotion:
the map should not present a subsidiary as independent, nor bury it.

## Layout

- Max canvas `1680px`, page padding `36px`
- Three cards across at full width, two at 1150px, one at 760px
- Name lists use `columns: 225px 2` — a second column appears only when each
  can hold the longest company name, so a name never breaks mid-way
- Company names are `14px / 1.8`; readability beats density at this size

## Voice

- One sentence per company; what it does and for whom
- No "leading", "innovative", "cutting-edge", "revolutionary"
- Funding only when it defines the company's position
