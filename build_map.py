#!/usr/bin/env python3
"""Generate map.html from companies.csv.

Styling follows brand.md -- update that file first, then mirror it in TOKENS.
Run: python3 -I build_map.py
"""
import csv, html, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = "--artifact" in sys.argv   # emit a body-only page for claude.ai hosting
TITLE = "Robotics & Physical AI Landscape"   # one line, one weight (brand.md)
BYLINE   = "by Khalil Fuller & Claude"
NOTE     = ""          # optional scope caveat under the byline

# Business-model classification (lab / neo-integrator / component / platform /
# service) stays in companies.csv and in the page data. Flip this to True to
# show it again as dots, a legend and filter buttons.
SHOW_MODEL = False
WORDMARK = ""          # set a string to show a wordmark top-right

FONT_URL = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500"
            "&family=IBM+Plex+Sans+Condensed:wght@400;600;700&display=swap")

# ------------------------------------------------------------- design tokens
# Mirrors brand.md. Change there first.
TOKENS = {
    # Dark canvas, white cards -- the v1 structure, which read better.
    # Single committed look; the amber accent carries all interaction.
    "--bg":           "#0E0F10",
    "--paper":        "#FFFFFF",
    "--ink":          "#15171A",
    "--ink-2":        "#747B80",   # owned by a larger company
    "--chalk":        "#F2F3F1",
    "--chalk-2":      "#8C9398",
    "--rule":         "#2B2E30",   # hairlines on the canvas
    "--rule-paper":   "#E6E7E3",   # hairlines on a card
    "--accent":       "#F26B21",

    # --- type: bigger and looser than v2 ---
    "--title-size":   "32px",
    "--title-track":  "0.02em",
    "--tier-size":    "12px",
    "--tier-track":   "0.22em",
    "--cat-size":     "10.5px",
    "--cat-track":    "0.14em",
    "--name-size":    "14px",
    "--name-leading": "1.8",
    "--meta-size":    "11px",

    # --- layout: wider cards, fewer wrapped names ---
    "--page-w":       "1680px",
    "--page-pad":     "36px",
    "--cols":         "3",
    "--col-gap":      "16px",
    "--card-gap":     "16px",
    "--card-pad":     "18px 20px 20px",
    "--r-card":       "3px",
    "--r-chip":       "2px",
    "--panel-w":      "400px",
}

TIER_ORDER = ["Intelligence", "Platform", "Hardware", "Vertical Robotics Companies", "Market Infrastructure"]
BUCKET_ORDER = [
    "Foundation Models", "World Models", "Research Labs", "Simulation",
    "Training Data & Demonstration", "Evaluation & Benchmarks",
    "Dev Tools & Middleware", "Robot Compute & Runtime", "Fleet Ops & Remote Operations", "Perception & Sensing",
    "Humanoids & Quadrupeds", "Arms & Cobots", "Mobile Bases & AMRs",
    "Actuators & Motion", "Power & Connectivity", "End Effectors & Grippers",
    "Construction", "Energy & Solar", "Agriculture & Landscaping",
    "Warehouse & Logistics", "Last-Mile & Delivery", "Manufacturing & Fabrication",
    "Data Centers", "Inspection & Infrastructure", "Marine & Subsea",
    "Food & Hospitality", "Healthcare & Life Sciences",
    "Facilities, Retail & Security", "Consumer & Home", "Defense & Aerospace",
    "Finance & Insurance", "Marketplaces & Sourcing",
    "Classic Automation Integrators", "Deployment & Field Service", "Safety & Compliance",
]
# Scope notes: one line under a category label saying where its boundary is.
# These exist to pre-empt "why isn't X in here?" -- the question a market map
# gets asked most. Only categories whose edge genuinely confuses get one.
FOOTNOTES = {
    "Foundation Models":
        "Companies that sell models to others. Ones that build a model and also ship the system running it sit in their vertical.",
    "Research Labs":
        "Corporate and nonprofit research organisations, not vendors.",
    "Simulation":
        "Physics engines and simulators. Simulation used as CI for robot policies is under Dev Tools.",
    "Training Data & Demonstration":
        "Collecting, capturing and curating data to train on. Teleoperation used to run live fleets is under Fleet Ops.",
    "Fleet Ops & Remote Operations":
        "Running and supervising deployed fleets, teleoperation included. Teleop for data capture is under Training Data; companies whose whole product is remote-operated work sit in their vertical.",
    "Robot Compute & Runtime":
        "Robotics-specific silicon and runtimes. General GPU clouds and AI infrastructure are out of scope.",
    "Humanoids & Quadrupeds":
        "Grouped by form factor. Several target the home; consumer robots already shipping are under Consumer & Home.",
    "Mobile Bases & AMRs":
        "Platforms sold for others to build on. Companies operating warehouse fleets are under Warehouse & Logistics.",
    "Consumer & Home":
        "Consumer products on sale today. Home humanoids still in development are under Humanoids & Quadrupeds.",
    "Marine & Subsea":
        "Commercial marine work. Naval and armed maritime autonomy is under Defense & Aerospace.",
    "Metal & Fabrication":
        "Welding, grinding, machining and additive. General assembly and machine tending is the next box.",
    "Assembly & Machine Tending":
        "Assembly, material handling and tending machines. Metalworking is the previous box.",
    "Classic Automation Integrators":
        "Project work: designing and building the cell. Keeping it running afterwards is under Deployment & Field Service.",
    "Deployment & Field Service":
        "Installing, repairing and maintaining robots someone else built. The firms that design the system are under Classic Automation Integrators.",
    "Finance & Insurance":
        "Financing and insuring deployments. Venture funds and equity vehicles are not on this map.",
}

bidx = {b: i for i, b in enumerate(BUCKET_ORDER)}
MODELS = [("all", "All"), ("neo-integrator", "Neo-integrators"), ("lab", "Labs"),
          ("component", "Components"), ("platform", "Platforms"), ("service", "Services")]

rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "companies.csv")))
        if "UNVERIFIED" not in r["notes"]]
# A bucket must live in exactly one tier, or it renders as two separate cards.
# This has bitten twice now: moving a company's bucket without its tier.
_bt = defaultdict(set)
for _r in rows:
    _bt[_r["bucket"]].add(_r["tier"])
_split = {b: sorted(t) for b, t in _bt.items() if len(t) > 1}
if _split:
    raise SystemExit(f"bucket spans more than one tier: {_split}")

tiers = defaultdict(lambda: defaultdict(list))
for r in rows:
    tiers[r["tier"]][r["bucket"]].append(r)

data = {r["name"]: {"b": r["bucket"], "t": r["tier"], "m": r.get("model", ""),
                    "h": r["hq"], "d": r["description"], "u": r["domain"],
                    "s": r.get("status", "active"), "f": r.get("funding", ""),
                    "i": r.get("lead_investor", "")}
        for r in rows}

tok = "\n".join(f"  {k}: {v};" for k, v in TOKENS.items())
HEAD_STANDALONE = f'''<!doctype html><html lang=en><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Robotics &amp; Physical AI Landscape</title>
<link rel=preconnect href="https://fonts.googleapis.com">
<link rel=preconnect href="https://fonts.gstatic.com" crossorigin>
<link rel=stylesheet href="{FONT_URL}">'''

HEAD_ARTIFACT = f'''<title>Robotics &amp; Physical AI Landscape</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel=stylesheet href="{FONT_URL}">'''

out = [(HEAD_ARTIFACT if ARTIFACT else HEAD_STANDALONE) + f"""
<style>
:root {{
{tok}
  --sans: 'IBM Plex Sans Condensed', ui-sans-serif, system-ui, sans-serif;
  --mono: 'IBM Plex Mono', ui-monospace, Menlo, monospace;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--chalk);
  font-family:var(--sans); -webkit-font-smoothing:antialiased;
  padding-block:var(--page-pad);
  padding-left:max(16px, env(safe-area-inset-left, 0px));
  padding-right:max(16px, env(safe-area-inset-right, 0px)); }}
.page {{ max-width:var(--page-w); margin:0 auto; }}

header {{ display:flex; align-items:flex-start; justify-content:space-between; gap:24px; }}
h1 {{ margin:0; font-size:var(--title-size); font-weight:700;
  letter-spacing:var(--title-track); line-height:1; text-transform:uppercase;
  color:var(--chalk); }}
.byline, .note {{ margin:9px 0 0; font-family:var(--mono); font-size:var(--meta-size);
  color:var(--chalk-2); letter-spacing:.02em; }}
.note {{ margin-top:3px; }}
.wordmark {{ font-size:11px; letter-spacing:.3em; text-transform:uppercase;
  border:1px solid var(--rule); padding:9px 15px; color:var(--chalk); }}

.controls {{ display:flex; align-items:center; gap:16px; flex-wrap:wrap;
  margin:22px 0 26px; padding-bottom:16px; border-bottom:1px solid var(--rule); }}
#q {{ font-family:var(--mono); font-size:var(--meta-size); letter-spacing:.04em;
  background:transparent; border:1px solid var(--rule); color:var(--chalk);
  padding:8px 11px; border-radius:var(--r-chip); width:220px; }}
#q::placeholder {{ color:var(--chalk-2); }}
#q:focus {{ outline:none; border-color:var(--accent); }}
.filters {{ display:flex; gap:14px; flex-wrap:wrap; }}
.f {{ font-family:var(--mono); font-size:var(--meta-size); letter-spacing:.08em;
  text-transform:uppercase; background:none; border:0; border-bottom:1px solid transparent;
  color:var(--chalk-2); padding:2px 0; cursor:pointer; }}
.f:hover {{ color:var(--accent); }}
.f[aria-pressed=true] {{ color:var(--chalk); border-bottom-color:var(--accent); }}
.hint, .key, .count {{ font-family:var(--mono); font-size:var(--meta-size);
  letter-spacing:.08em; text-transform:uppercase; color:var(--chalk-2); }}
.hint b {{ color:var(--accent); font-weight:500; }}
.key i {{ font-style:normal; color:var(--accent); }}
.count {{ margin-left:auto; }}

.tier {{ margin-bottom:30px; }}
.tier-label {{ font-size:var(--tier-size); font-weight:700; letter-spacing:var(--tier-track);
  text-transform:uppercase; color:var(--accent); margin:0 0 13px; padding-bottom:9px;
  border-bottom:1px solid var(--rule); }}
.grid {{ columns:var(--cols); column-gap:var(--col-gap); }}

.cat {{ break-inside:avoid; background:var(--paper); border-radius:var(--r-card);
  padding:var(--card-pad); margin-bottom:var(--card-gap); }}
.cat-label {{ display:inline-block; background:var(--ink); color:var(--paper);
  border-radius:var(--r-chip); padding:5px 10px; font-size:var(--cat-size);
  font-weight:600; letter-spacing:var(--cat-track); text-transform:uppercase;
  margin-bottom:14px; }}
.cat-note {{ margin:-6px 0 14px; font-family:var(--mono); font-size:10.5px;
  line-height:1.65; color:var(--ink-2); max-width:46ch; }}
ul {{ margin:0; padding:0; list-style:none; columns:220px 2; column-gap:22px; }}
.cat.narrow ul {{ columns:1; }}
li {{ break-inside:avoid; }}
li button {{ font-family:var(--mono); font-size:var(--name-size);
  line-height:var(--name-leading); color:var(--ink); background:none; border:0;
  padding:1px 0 1px 1.1em; text-indent:-1.1em; text-align:left; cursor:pointer;
  display:block; width:100%; overflow-wrap:normal; word-break:normal; }}
.own {{ color:var(--accent); margin-left:2px; }}
li button:hover {{ color:var(--accent); }}
li button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
li.neo button::after {{ content:""; display:inline-block; width:5px; height:5px;
  border-radius:50%; background:var(--accent); margin-left:6px; vertical-align:middle; }}
li.dim {{ opacity:.2; }}
.cat.hidden {{ display:none; }}

#panel {{ position:fixed; top:0; right:0; width:var(--panel-w); max-width:92vw;
  height:100%; background:var(--paper); padding:34px 30px; overflow-y:auto;
  transform:translateX(101%); transition:transform .18s ease; z-index:20; }}
#panel.open {{ transform:none; }}
#panel h2 {{ margin:0 0 10px; font-family:var(--mono); font-size:18px; font-weight:500;
  color:var(--ink); }}
#panel .pmeta {{ font-family:var(--mono); font-size:var(--meta-size); letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink-2); line-height:1.95;
  padding-bottom:14px; border-bottom:1px solid var(--rule-paper); margin-bottom:16px; }}
#panel .pbadge {{ display:inline-block; font-family:var(--mono); font-size:9.5px;
  letter-spacing:.12em; text-transform:uppercase; color:var(--accent);
  border:1px solid var(--accent); border-radius:var(--r-chip); padding:3px 7px;
  margin-bottom:14px; }}
#panel p.blurb {{ font-size:14px; line-height:1.74; color:var(--ink); margin:0 0 22px; }}
#panel .pfund {{ font-family:var(--mono); font-size:var(--meta-size); line-height:1.8;
  color:var(--ink); padding-top:14px; border-top:1px solid var(--rule-paper);
  margin-bottom:22px; }}
#panel .pfund .k {{ display:block; font-size:9.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-2); margin-bottom:5px; }}
#panel a {{ font-family:var(--mono); font-size:var(--meta-size); color:var(--accent);
  text-decoration:none; border-bottom:1px solid var(--accent); word-break:break-all; }}
#closeBtn {{ position:absolute; top:22px; right:22px; background:none;
  border:1px solid var(--rule-paper); color:var(--ink-2); font-family:var(--mono);
  font-size:14px; line-height:1; padding:5px 9px; border-radius:var(--r-chip);
  cursor:pointer; }}
#closeBtn:hover {{ border-color:var(--accent); color:var(--accent); }}

@media (max-width:1150px) {{ :root {{ --cols:2; }} }}
@media (max-width:760px) {{
  :root {{ --cols:1; --title-size:23px; --panel-w:100%; }}
  ul, .cat.narrow ul {{ columns:1; }}
  header {{ flex-wrap:wrap; gap:12px; }}
  #q {{ width:100%; }}
  .count {{ margin-left:0; }}
}}
</style>
<div class=page>
<header>
  <div>
    <h1>{html.escape(TITLE)}</h1>
    <p class=byline>{BYLINE}</p>
    {f'<p class=note>{NOTE}</p>' if NOTE else ''}
  </div>
  {f'<div class=wordmark>{WORDMARK}</div>' if WORDMARK else ''}
</header>
<div class=controls>
  <input id=q type=search placeholder="Search companies" autocomplete=off>"""]

if SHOW_MODEL:
    out.append('<div class=filters>')
    for key, label in MODELS:
        pressed = "true" if key == "all" else "false"
        out.append(f'<button class=f data-m="{key}" aria-pressed={pressed}>{label}</button>')
    out.append('</div>')
out.append('<div class=hint><b>Click</b> a name for its blurb</div>'
           '<div class=key><i>*</i> = owned by a larger company</div>')
if SHOW_MODEL:
    out.append('<div class=legend><i></i>Neo-integrator</div>')
out.append('<div class=count id=count></div></div>')

def li(r):
    """One company: muted when it is owned by a larger company."""
    classes = []
    if SHOW_MODEL and r.get("model") == "neo-integrator":
        classes.append("neo")
    if r.get("status", "active") != "active":
        classes.append("owned")
    name = html.escape(r["name"])
    mark = '<span class=own>*</span>' if "owned" in classes else ""
    return (f'<li class="{" ".join(classes)}" data-m="{html.escape(r.get("model", ""))}" '
            f'data-n="{html.escape(r["name"].lower())}">'
            f'<button data-name="{name}">{name}{mark}</button></li>')


total = 0
for tier in TIER_ORDER:
    buckets = tiers.get(tier)
    if not buckets: continue
    out.append(f'<section class=tier data-tier="{html.escape(tier)}">'
               f'<div class=tier-label>{html.escape(tier)}</div><div class=grid>')
    for bucket in sorted(buckets, key=lambda b: bidx.get(b, 999)):
        items = sorted(buckets[bucket], key=lambda r: r["name"].lower())
        total += len(items)
        cls = "cat narrow" if len(items) <= 4 else "cat"
        lis = "".join(li(r) for r in items)
        note = FOOTNOTES.get(bucket, "")
        note_el = f'<p class=cat-note>{html.escape(note)}</p>' if note else ''
        out.append(f'<div class="{cls}"><div class=cat-label>{html.escape(bucket)}</div>'
                   f'{note_el}<ul>{lis}</ul></div>')
    out.append("</div></section>")

out.append('</div>')
out.append(f"""
<aside id=panel aria-live=polite>
  <button id=closeBtn type=button aria-label="Close">&times;</button>
  <h2 id=pname></h2><div class=pmeta id=pmeta></div>
  <div class=pbadge id=pbadge></div>
  <p class=blurb id=pblurb></p>
  <div class=pfund id=pfund hidden></div>
  <a id=plink target=_blank rel="noopener noreferrer"></a>
</aside>
<script>
const DATA = {json.dumps(data)};
const SHOW_MODEL = {json.dumps(SHOW_MODEL)};
const $ = id => document.getElementById(id);
const panel=$('panel'), q=$('q'), countEl=$('count'), closeBtn=$('closeBtn'),
      pname=$('pname'), pmeta=$('pmeta'), pbadge=$('pbadge'), pfund=$('pfund'),
      pblurb=$('pblurb'), plink=$('plink');
let model='all';

function show(name){{
  const d=DATA[name]; if(!d) return;
  pname.textContent=name;
  pmeta.innerHTML=[d.t+' &middot; '+d.b, d.h, d.s&&d.s!=='active'?d.s:''].filter(Boolean).join('<br>');
  const showModel = SHOW_MODEL;
  pbadge.textContent=showModel?(d.m||''):'';
  pbadge.style.display=(showModel&&d.m)?'inline-block':'none';
  pblurb.textContent=d.d||'';
  if(d.f||d.i){{
    pfund.innerHTML='<span class=k>Funding</span>'+
      [d.f,d.i?'Led by '+d.i:''].filter(Boolean).join('<br>');
    pfund.hidden=false;
  }} else {{ pfund.hidden=true; }}
  if(d.u){{ plink.href='https://'+d.u; plink.textContent=d.u; plink.style.display='inline'; }}
  else {{ plink.style.display='none'; }}
  panel.classList.add('open');
}}
document.addEventListener('click',e=>{{
  const b=e.target.closest('li button'); if(b) return show(b.dataset.name);
  const f=e.target.closest('.f');
  if(f){{ model=f.dataset.m;
    document.querySelectorAll('.f').forEach(x=>x.setAttribute('aria-pressed',x===f));
    apply(); }}
  // tap anywhere outside the card to dismiss it -- there is no Escape on a phone
  if(!e.target.closest('#panel')) panel.classList.remove('open');
}});
closeBtn.addEventListener('click',()=>panel.classList.remove('open'));
document.addEventListener('keydown',e=>{{ if(e.key==='Escape') panel.classList.remove('open'); }});
q.addEventListener('input',apply);

function apply(){{
  const term=q.value.trim().toLowerCase(); let n=0;
  document.querySelectorAll('li').forEach(li=>{{
    const okM = model==='all' || li.dataset.m===model;
    const okQ = !term || li.dataset.n.includes(term);
    li.classList.toggle('dim', !(okM&&okQ));
    if(okM&&okQ) n++;
  }});
  document.querySelectorAll('.cat').forEach(c=>{{
    c.classList.toggle('hidden', !c.querySelector('li:not(.dim)'));
  }});
  document.querySelectorAll('section.tier').forEach(s=>{{
    s.style.display = s.querySelector('.cat:not(.hidden)') ? '' : 'none';
  }});
  countEl.textContent = n + ' shown';
}}
apply();
</script>""")

name = "map.artifact.html" if ARTIFACT else "map.html"
open(os.path.join(ROOT, name), "w").write("\n".join(out))
print(f"{name} written: {total} companies")
