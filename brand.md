# Brand

Single source of truth for how the robotics market map looks. Update this file
first, then mirror it in `TOKENS` in `build_map.py`. Anything new we build
follows it.

## Typeface

**B612 Mono** everywhere — title, labels, company names, body. No second family.

```
https://fonts.googleapis.com/css2?family=B612+Mono:ital,wght@0,400;0,700;1,400&display=swap
```

B612 was drawn by Airbus for cockpit displays, built to stay legible at small
sizes under bad conditions. It suits a dense reference document.

**One weight per element.** The title is a single weight — never mix 400 and 700
inside one line. Emphasis comes from size, space and case, not from weight shifts
mid-phrase.

| use | weight | size | tracking | case |
|---|---|---|---|---|
| page title | 700 | 34px | 0.12em | upper |
| tier label | 700 | 11px | 0.26em | upper |
| bucket chip | 700 | 10px | 0.13em | upper |
| company name | 400 | 13.5px | 0.01em | as written |
| detail / meta | 400 | 11px | 0.04em | as written |

## Colour

**Black and white only.** No blues, no brand hue. If something needs emphasis,
use weight, size, space or inversion — never colour.

| token | value | use |
|---|---|---|
| `--bg` | `#0b0b0b` | page canvas |
| `--paper` | `#ffffff` | cards and panel |
| `--ink` | `#111111` | text on paper |
| `--ink-soft` | `#6b6b6b` | secondary text on paper |
| `--chalk` | `#ffffff` | text on canvas |
| `--chalk-soft` | `#8a8a8a` | secondary text on canvas |
| `--rule` | `#2a2a2a` | hairlines on canvas |
| `--rule-paper` | `#e2e2e2` | hairlines on paper |

Chips are inverted: black fill, white text. The neo-integrator marker is a solid
black dot on paper, a solid white dot on canvas.

## Corners

Sharp. Nothing is pill-shaped.

| element | radius |
|---|---|
| cards, panel | 3px |
| chips, buttons, inputs | 2px |
| dots and markers | full circle (the one exception) |

## Layout

- Max canvas `1760px`, page padding `40px`
- Three columns per tier section, `14px` gutters
- Cards with four or fewer companies render single-column
- Density over whitespace: this is a reference document, not a landing page

## Voice

- Blurbs are one sentence; say what the company does and for whom
- No "leading", "innovative", "cutting-edge", "revolutionary"
- Funding only when it is the point — a round that defines the company's position
