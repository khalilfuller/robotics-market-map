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
bidx = {b: i for i, b in enumerate(BUCKET_ORDER)}
MODELS = [("all", "All"), ("neo-integrator", "Neo-integrators"), ("lab", "Labs"),
          ("component", "Components"), ("platform", "Platforms"), ("service", "Services")]

rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "companies.csv")))
        if "UNVERIFIED" not in r["notes"]]
tiers = defaultdict(lambda: defaultdict(list))
for r in rows:
    tiers[r["tier"]][r["bucket"]].append(r)

data = {r["name"]: {"b": r["bucket"], "t": r["tier"], "m": r.get("model", ""),
                    "h": r["hq"], "d": r["description"], "u": r["domain"],
                    "s": r.get("status", "active")}
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
ul {{ margin:0; padding:0; list-style:none; columns:225px 2; column-gap:22px; }}
.cat.narrow ul {{ columns:1; }}
li button {{ white-space:nowrap; }}
li {{ break-inside:avoid; }}
li button {{ font-family:var(--mono); font-size:var(--name-size);
  line-height:var(--name-leading); color:var(--ink); background:none; border:0;
  padding:1px 0; text-align:left; cursor:pointer; display:block; width:100%; }}
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
li button {{ white-space:nowrap; }}
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
        out.append(f'<div class="{cls}"><div class=cat-label>{html.escape(bucket)}</div><ul>{lis}</ul></div>')
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
  pmeta.innerHTML=[d.t+' &middot; '+d.b, d.h, d.s&&d.s!=='active'?d.s:''].filter(Boolean).join('<br>');
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
