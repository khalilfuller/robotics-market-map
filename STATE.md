# Where we left off — 6 Nov 2026

**Live site:** https://khalilfuller.github.io/robotics-market-map/
**Claude artifact:** https://claude.ai/artifact/DkB4hnUpUssNbfrmkYwjKS
**Repo:** https://github.com/khalilfuller/robotics-market-map — **public**

451 companies on the map, 455 in `companies.csv`, 5 tiers, 39 categories.

## 14 Nov 2026: Contract Manufacturing

New category under Vertical Robotics Companies for firms that build robots and other hardware
for the companies that design them. Added Matter; moved Foundry Robotics in from Metal & Fabrication.

## Weekly sweep 2026-11-13

Added 3:
- GreyOrange: Fleet Ops & Remote Operations
- Ocado Intelligent Automation: Warehouse & Logistics (part of Ocado Group)
- Intuitive: Healthcare & Life Sciences

## Added 2026-11-11

- Tau Robotics: Consumer & Home
- DEEP Robotics: Humanoids & Quadrupeds

## Weekly sweep 2026-11-09

Added 4:
- Fauna Robotics: Humanoids & Quadrupeds (part of Amazon)
- Motherboard Labs: Fleet Ops & Remote Operations
- NorBot: Robot Operators & RaaS
- Helsing: Defense & Aerospace

## 6 Nov 2026 — channel and service layer

Market Infrastructure restructured around who owns the customer:
- **Robot Operators & RaaS** (new): own the contract, run several makers' robots as a monthly
  service. Formic (from Finance), Cardinal Robotics (from Field Service), Deploy (from Fleet Ops),
  SoftBank Robotics, TechForce Robotics.
- **Deployment & Field Service**: now strictly subcontracted uptime work for makers. Added Ricoh Service Advantage.
- **Distribution & Dealer Channels** (new): Crickets Continuum, Allied Universal Technology Services,
  Trimble, Motion Automation Intelligence, Applied Industrial Technologies, RobotLAB.
- Finance + Mitsubishi HC Capital America; Marketplaces + Konnex, RobotShop.

38 companies added, mostly facility service-line makers (cleaning, security, hospital logistics,
UV, aerial and sewer inspection, milking, solar cleaning). Cardinal's 35,000-robot / 3,000-tech /
$800M figures are the company's own claims (cardinalrobot.com), labelled as such.
No domain found yet: TechForce Robotics, Crickets Continuum, Mitsubishi HC Capital America, Konnex,
Asylon, UVD Robots. Left off on purpose: non-robotics channel analogs (Telarus, ADT, JAN-PRO).

```
python3 -I build_map.py              # index.html        — the public site
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
- Should capital sources (funds) get a box after all? Currently no, by the rule above.

**Data gaps**
- 4 unverified, excluded from the map: TempoWorks, MWbotics, Workwise Robotics, Hexagon Robotics
- 2 ambiguous, on the map but unconfirmed: AgRobotics, Intuition.dev
- No domain, after a full sweep: AMI (ami.inc is an unrelated Japanese medtech firm),
  Mantle, Cortex AI, Moving Atoms, Synapse Semiconductor, Libra Robotics, Manifold,
  Deploy, and Project Prometheus (deliberately stealth, no public site)
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
