# Where we left off — 24 Oct 2026

**Live map:** https://claude.ai/artifact/DkB4hnUpUssNbfrmkYwjKS (v14)
**Repo:** https://github.com/khalilfuller/robotics-market-map — **private**

396 companies on the map, 399 in `companies.csv`, 5 tiers, 37 categories.

```
python3 -I build_map.py              # map.html          — standalone
python3 -I build_map.py --artifact   # map.artifact.html — then publish this one
```

## Tags

| tag | what it is |
|---|---|
| `v1` | black and white, B612 Mono, 312 companies |
| `v2` | IBM Plex, no cards, light+dark — **less usable, superseded** |
| `v3` | cards restored on dark canvas, amber accent — current direction |

## Decisions already made (don't relitigate)

- **Cards stay.** v2 removed them and the map got harder to scan. See brand.md.
- **One accent** (amber `#F26B21`), on tier labels and interaction only.
- **Owned companies get a `*`**, not grey — grey made them the hardest to read.
- **Business-model tags are in the data, off on the site.** `SHOW_MODEL = True`
  in build_map.py brings back the neo-integrator dots, legend and filters.
- **AVs stay** (Waymo, Zoox, Wayve, Plus AI, Gatik) and the "omitting" note is gone.
- **Funds are not on the map.** RoboStrategy, Lux, Eclipse and a16z are sources,
  not entries. Finance & Insurance means financing and insuring *deployments*.

## Open threads

**Decide**
- Make the repo public? It's private now.
- Should capital sources (funds) get a box after all? Currently no, by the rule above.

**Data gaps**
- 3 unverified, excluded from the map: TempoWorks, MWbotics, Workwise Robotics
- 2 ambiguous, on the map but unconfirmed: AgRobotics, Intuition.dev
- No domain: AMI (ami.inc is an unrelated Japanese medtech firm), Mantle, TempoWorks
- Lux and Eclipse sites only exposed partial portfolios — more to pull

**Known structural weaknesses** (from the critique, still true)
- The taxonomy mixes stack layers with go-to-market, so companies that are both
  a model lab and a deployer (Mind Robotics, Dyna, Eka) appear once and read as half
- No quality bar: Anduril and a two-person YC company carry identical weight
- Vertical Robotics Companies is 149 of 369 — nearly half the map

**Interactive ideas parked** (in rough order of value)
1. Vertical stack view — pick Energy & Solar, see the whole column serving it
2. Dependency edges — pi powers Ultra, Field AI powers robot.com, ASI owns Scythe
3. Capital scrubber — size by money raised, scrubbed over time
4. Geography toggle — `cluster` and `hq` are already populated
