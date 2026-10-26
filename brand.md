# Brand — v4

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

**B612**, both the sans and the mono. Drawn by Airbus for cockpit displays, so
it is built to stay legible at small sizes under bad conditions — which is the
same problem a 400-entry reference page has.

```
https://fonts.googleapis.com/css2?family=B612:ital,wght@0,400;0,700;1,400&family=B612+Mono:ital,wght@0,400;0,700;1,400&display=swap
```

- **B612** (sans) — title, tier labels, category chips, UI
- **B612 Mono** — company names, metadata, anything that reads as data

Fallbacks: `ui-sans-serif, system-ui` and `ui-monospace, SF Mono, Menlo, monospace`.

**One weight per element.** Never mix weights inside a line.

| use | face | weight | size | tracking | case |
|---|---|---|---|---|---|
| page title | Sans | 700 | 32px | 0.02em | upper |
| byline / note | Mono | 400 | 11px | 0.02em | as written |
| tier label | Sans | 700 | 12px | 0.22em | upper |
| category label | Sans | 600 | 10.5px | 0.14em | upper |
| scope note | Mono | 400 | 10.5px | 0 | sentence |
| company name | Mono | 400 | 14px | 0 | as written |
| UI / meta | Mono | 400 | 11px | 0.08em | upper |

**B612 Mono is wider than most monos**, so anything sized against it needs
measuring rather than assuming. Switching to it from IBM Plex pushed the longest
company name to 239px and clipped the search placeholder at its old 220px width.

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

## Scope notes

A category whose boundary confuses gets one line of `--ink-2` mono under its
label, saying where the neighbouring cases live. They exist to answer "why isn't
X in here?" before the reader has to ask it. Defined in `FOOTNOTES` in
`build_map.py`; only add one where the edge is genuinely ambiguous, since a note
on every box is noise.

## Status

A company owned by a larger one gets an accent-coloured `*` after its name, with
a key in the header. The name itself stays at full contrast — greying it out made
those 27 entries harder to read than everything around them, which punished the
reader for a fact about the company. Acquisition is information, not a demotion:
the map should not present a subsidiary as independent, nor bury it.

## Layout

- Max canvas `1680px`, page padding `36px`
- Three cards across above 1400px, two at 1400px, one below 760px. The 1400px
  threshold is not arbitrary: below it a card is too narrow to hold two name
  columns, and three grid columns then make the page *taller* than two would
- Name lists use `columns: 185px 2`, sized so two columns fit inside a card at
  full width. A name too long for its column wraps at a space with a `-1.1em`
  hanging indent, so it still reads as one entry and never spills into the
  neighbouring column
- Company names are `14px / 1.8`; readability beats density at this size
- On phones, name rows get `8px` vertical padding so tap targets reach ~41px

## Voice

- One sentence per company; what it does and for whom
- No "leading", "innovative", "cutting-edge", "revolutionary"
- Funding only when it defines the company's position
