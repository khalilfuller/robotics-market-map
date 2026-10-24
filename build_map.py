#!/usr/bin/env python3
"""Generate map.html from companies.csv.

Styling follows brand.md -- update that file first, then mirror it in TOKENS.
Run: python3 -I build_map.py
"""
import csv, html, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = "--artifact" in sys.argv   # emit a body-only page for claude.ai hosting
TITLE = "ROBOTICS LANDSCAPE"   # one line, one weight (brand.md)
BYLINE   = "by Khalil Fuller & Claude"
NOTE     = ""          # optional scope caveat under the byline

# Business-model classification (lab / neo-integrator / component / platform /
# service) stays in companies.csv and in the page data. Flip this to True to
# show it again as dots, a legend and filter buttons.
SHOW_MODEL = False
WORDMARK = ""          # set a string to show a wordmark top-right

FONT_URL = "https://fonts.googleapis.com/css2?family=B612+Mono:ital,wght@0,400;0,700;1,400&display=swap"

# ------------------------------------------------------------- design tokens
# Mirrors brand.md. Change there first.
TOKENS = {
    # --- colour: black and white only, per brand.md ---
    "--bg":           "#0b0b0b",
    "--paper":        "#ffffff",
    "--ink":          "#111111",
    "--ink-soft":     "#6b6b6b",
    "--chalk":        "#ffffff",
    "--chalk-soft":   "#8a8a8a",
    "--rule":         "#2a2a2a",
    "--rule-paper":   "#e2e2e2",

    # --- corners: sharp ---
    "--r-card":       "3px",
    "--r-chip":       "2px",
    "--r-ui":         "2px",

    # --- type ---
    "--title-size":   "34px",
    "--title-track":  "0.12em",
    "--tier-size":    "11px",
    "--tier-track":   "0.26em",
    "--chip-size":    "10px",
    "--chip-track":   "0.13em",
    "--name-size":    "13.5px",
    "--name-track":   "0.01em",
    "--name-leading": "1.72",
    "--meta-size":    "11px",

    # --- layout ---
    "--page-w":       "1760px",
    "--page-pad":     "40px",
    "--cols":         "3",
    "--col-gap":      "14px",
    "--card-gap":     "14px",
    "--card-pad":     "16px 18px 18px",
    "--neo-dot":      "5px",
    "--panel-w":      "380px",
}

TIER_ORDER = ["Intelligence", "Platform", "Hardware", "Vertical Robotics Companies", "Market Infrastructure"]
BUCKET_ORDER = [
    "Foundation Models", "World Models", "Research Labs", "Simulation",
    "Training Data & Demonstration", "Evaluation & Benchmarks",
    "Dev Tools & Middleware", "Fleet Ops & Remote Operations", "Perception & Sensing",
    "Humanoids & Quadrupeds", "Arms & Cobots", "Mobile Bases & AMRs",
    "Actuators & Drives", "End Effectors & Grippers",
    "Construction", "Energy & Solar", "Agriculture & Landscaping",
    "Warehouse & Logistics", "Last-Mile & Delivery", "Manufacturing & Fabrication",
    "Data Centers", "Inspection & Infrastructure", "Marine & Subsea",
    "Food & Hospitality", "Healthcare & Life Sciences",
    "Facilities, Retail & Security", "Consumer & Home", "Defense & Aerospace",
    "Finance & Insurance", "Marketplaces & Sourcing",
    "Deployment & Field Service", "Safety & Compliance",
]
bidx = {b: i for i, b in enumerate(BUCKET_ORDER)}
MODELS = [("all", "All"), ("neo-integrator", "Neo-integrators"), ("lab", "Labs"),
          ("component", "Components"), ("platform", "Platforms"), ("service", "Services")]

rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "companies.csv")))
        if "UNVERIFIED" not in r["notes"]]
tiers = defaultdict(lambda: defaultdict(list))
for r in rows:
    tiers[r["tier"]][r["bucket"]].append(r)

data = {r["name"]: {"b": r["bucket"], "t": r["tier"], "m": r.get("model", ""),
                    "h": r["hq"], "d": r["description"], "u": r["domain"]}
        for r in rows}

tok = "\n".join(f"  {k}: {v};" for k, v in TOKENS.items())
HEAD_STANDALONE = f'''<!doctype html><html lang=en><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Robotics Landscape</title>
<link rel=preconnect href="https://fonts.googleapis.com">
<link rel=preconnect href="https://fonts.gstatic.com" crossorigin>
<link rel=stylesheet href="{FONT_URL}">'''

HEAD_ARTIFACT = f'''<title>Robotics Landscape</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel=stylesheet href="{FONT_URL}">'''

out = [(HEAD_ARTIFACT if ARTIFACT else HEAD_STANDALONE) + f"""
<style>
:root {{
{tok}
  --font: 'B612 Mono', ui-monospace, 'SF Mono', Menlo, monospace;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); font-family:var(--font);
  -webkit-font-smoothing:antialiased;
  padding-block:var(--page-pad);
  padding-left:max(var(--page-pad), env(safe-area-inset-left, 0px));
  padding-right:max(var(--page-pad), env(safe-area-inset-right, 0px)); }}
.page {{ max-width:var(--page-w); margin:0 auto; }}

header {{ display:flex; align-items:baseline; justify-content:space-between; gap:24px; margin-bottom:16px; }}
h1 {{ margin:0; font-size:var(--title-size); font-weight:700; letter-spacing:var(--title-track);
  color:var(--chalk); line-height:1; text-transform:uppercase; }}
.byline {{ margin:9px 0 0; font-size:var(--meta-size); letter-spacing:.1em;
  color:var(--chalk-soft); }}
.note {{ margin:4px 0 0; font-size:var(--meta-size); letter-spacing:.1em;
  color:var(--chalk-soft); opacity:.75; }}
.wordmark {{ font-size:12px; letter-spacing:.3em; color:var(--chalk);
  border:1.5px solid var(--chalk); padding:10px 18px; border-radius:var(--r-ui); }}

.controls {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:22px; }}
#q {{ font-family:var(--font); font-size:var(--meta-size); letter-spacing:.04em;
  background:transparent; border:1px solid var(--rule); color:var(--chalk);
  padding:7px 11px; border-radius:var(--r-ui); width:230px; }}
#q::placeholder {{ color:var(--chalk-soft); }}
#q:focus {{ outline:none; border-color:var(--chalk); }}
.filters {{ display:flex; gap:5px; flex-wrap:wrap; }}
.f {{ font-family:var(--font); font-size:10px; font-weight:700; letter-spacing:.11em;
  text-transform:uppercase; background:transparent; border:1px solid var(--rule);
  color:var(--chalk-soft); padding:6px 10px; border-radius:var(--r-ui); cursor:pointer; }}
.f:hover {{ border-color:var(--chalk); color:var(--chalk); }}
.f[aria-pressed=true] {{ background:var(--chalk); border-color:var(--chalk); color:var(--bg); }}
.count {{ font-size:10px; letter-spacing:.11em; text-transform:uppercase;
  color:var(--chalk-soft); margin-left:auto; }}
.legend {{ display:flex; align-items:center; gap:7px; font-size:10px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--chalk-soft); }}
.hint {{ font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:var(--chalk-soft); }}
.hint b {{ font-weight:700; color:var(--chalk); }}
.legend i {{ width:var(--neo-dot); height:var(--neo-dot); border-radius:50%; background:var(--chalk); }}

.tier {{ margin-bottom:28px; }}
.tier-label {{ font-size:var(--tier-size); font-weight:700; letter-spacing:var(--tier-track);
  text-transform:uppercase; color:var(--chalk); margin:0 0 11px; padding-bottom:8px;
  border-bottom:1px solid var(--rule); }}
.grid {{ columns:var(--cols); column-gap:var(--col-gap); }}
.card {{ break-inside:avoid; background:var(--paper); border-radius:var(--r-card);
  padding:var(--card-pad); margin-bottom:var(--card-gap); }}
.chip {{ display:inline-block; background:var(--ink); color:var(--paper);
  border-radius:var(--r-chip); padding:4px 9px; font-size:var(--chip-size); font-weight:700;
  letter-spacing:var(--chip-track); text-transform:uppercase; margin-bottom:12px; }}
ul {{ margin:0; padding:0; list-style:none; columns:2; column-gap:16px; }}
.card.narrow ul {{ columns:1; }}
li {{ break-inside:avoid; }}
li button {{ font-family:var(--font); font-size:var(--name-size); letter-spacing:var(--name-track);
  line-height:var(--name-leading); color:var(--ink); background:none; border:0; padding:0;
  text-align:left; cursor:pointer; display:block; width:100%; }}
li button:hover {{ text-decoration:underline; text-underline-offset:3px; }}
li button:focus-visible {{ outline:2px solid var(--ink); outline-offset:2px; }}
li.neo button::after {{ content:""; display:inline-block; width:var(--neo-dot); height:var(--neo-dot);
  border-radius:50%; background:var(--ink); margin-left:6px; vertical-align:middle; }}
li.dim {{ opacity:.2; }}
.card.hidden {{ display:none; }}

#panel {{ position:fixed; top:0; right:0; width:var(--panel-w); max-width:92vw; height:100%;
  background:var(--paper); padding:30px 28px; overflow-y:auto;
  transform:translateX(100%); transition:transform .18s ease; z-index:20; }}
#panel.open {{ transform:none; }}
#panel h2 {{ margin:0 0 6px; font-size:19px; font-weight:700; color:var(--ink);
  letter-spacing:.02em; }}
#panel .pmeta {{ font-size:10px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--ink-soft); margin-bottom:16px; line-height:1.9; }}
#panel .pbadge {{ display:inline-block; background:var(--ink); color:var(--paper);
  border-radius:var(--r-chip); padding:4px 9px; font-size:9.5px; font-weight:700;
  letter-spacing:.12em; text-transform:uppercase; margin-bottom:18px; }}
#panel p.blurb {{ font-size:13px; line-height:1.76; color:var(--ink); margin:0 0 22px; }}
#panel a {{ color:var(--ink); font-size:var(--meta-size); letter-spacing:.04em;
  text-decoration:none; border-bottom:1px solid var(--ink); word-break:break-all; }}
#closeBtn {{ position:absolute; top:20px; right:20px; background:none; border:1px solid var(--rule-paper);
  color:var(--ink-soft); font-family:var(--font); font-size:13px; line-height:1; padding:6px 9px;
  border-radius:var(--r-ui); cursor:pointer; }}
#closeBtn:hover {{ border-color:var(--ink); color:var(--ink); }}
@media (max-width:1100px) {{ :root {{ --cols:2; }} }}
@media (max-width:760px) {{
  :root {{ --cols:1; --title-size:24px; --panel-w:100%; }}
  ul, .card.narrow ul {{ columns:1; }}
  header {{ flex-wrap:wrap; gap:12px; }}
  #q {{ width:100%; }}
  .count {{ margin-left:0; }}
}}
</style>
<div class=page>
<header>
  <div>
    <h1>{TITLE}</h1>
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
out.append('<div class=hint><b>Click</b> a name for its blurb</div>')
if SHOW_MODEL:
    out.append('<div class=legend><i></i>Neo-integrator</div>')
out.append('<div class=count id=count></div></div>')

total = 0
for tier in TIER_ORDER:
    buckets = tiers.get(tier)
    if not buckets: continue
    out.append(f'<section class=tier data-tier="{html.escape(tier)}">'
               f'<div class=tier-label>{html.escape(tier)}</div><div class=grid>')
    for bucket in sorted(buckets, key=lambda b: bidx.get(b, 999)):
        items = sorted(buckets[bucket], key=lambda r: r["name"].lower())
        total += len(items)
        cls = "card narrow" if len(items) <= 4 else "card"
        lis = "".join(
            f'<li class="{"neo" if (SHOW_MODEL and r.get("model")=="neo-integrator") else ""}" '
            f'data-m="{html.escape(r.get("model",""))}" data-n="{html.escape(r["name"].lower())}">'
            f'<button data-name="{html.escape(r["name"])}">{html.escape(r["name"])}</button></li>'
            for r in items)
        out.append(f'<div class="{cls}"><div class=chip>{html.escape(bucket)}</div><ul>{lis}</ul></div>')
    out.append("</div></section>")

out.append('</div>')
out.append(f"""
<aside id=panel aria-live=polite>
  <button id=closeBtn type=button aria-label="Close">&times;</button>
  <h2 id=pname></h2><div class=pmeta id=pmeta></div>
  <div class=pbadge id=pbadge></div>
  <p class=blurb id=pblurb></p>
  <a id=plink target=_blank rel="noopener noreferrer"></a>
</aside>
<script>
const DATA = {json.dumps(data)};
const SHOW_MODEL = {json.dumps(SHOW_MODEL)};
const $ = id => document.getElementById(id);
const panel=$('panel'), q=$('q'), countEl=$('count'), closeBtn=$('closeBtn'),
      pname=$('pname'), pmeta=$('pmeta'), pbadge=$('pbadge'),
      pblurb=$('pblurb'), plink=$('plink');
let model='all';

function show(name){{
  const d=DATA[name]; if(!d) return;
  pname.textContent=name;
  pmeta.innerHTML=[d.t+' &middot; '+d.b, d.h].filter(Boolean).join('<br>');
  const showModel = SHOW_MODEL;
  pbadge.textContent=showModel?(d.m||''):'';
  pbadge.style.display=(showModel&&d.m)?'inline-block':'none';
  pblurb.textContent=d.d||'';
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
  document.querySelectorAll('.card').forEach(c=>{{
    c.classList.toggle('hidden', !c.querySelector('li:not(.dim)'));
  }});
  document.querySelectorAll('section.tier').forEach(s=>{{
    s.style.display = s.querySelector('.card:not(.hidden)') ? '' : 'none';
  }});
  countEl.textContent = n + ' shown';
}}
apply();
</script>""")

name = "map.artifact.html" if ARTIFACT else "map.html"
open(os.path.join(ROOT, name), "w").write("\n".join(out))
print(f"{name} written: {total} companies")
