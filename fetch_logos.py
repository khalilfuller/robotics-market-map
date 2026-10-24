#!/usr/bin/env python3
"""Fetch a logo image for each company in companies.csv into logos/."""
import csv, json, os, re, ssl, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "logos")
os.makedirs(OUT, exist_ok=True)
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"

def get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read(), r.headers.get("Content-Type", ""), r.geturl()

BAD = ("felicis","costanoa","signalflag","sequoia","a16z","andreessen","lux-","khosla",
       "ycombinator","y-combinator","accel","greylock","benchmark","index-ventures","nea-",
       "bessemer","firstround","first-round","eclipse","playground","obvious","usv","partner",
       "investor","backed-by","customer","client","press","award","badge","appstore",
       "google-play","linkedin","twitter","github","youtube","instagram")

class Scrape(HTMLParser):
    """Collect logo candidates. Brand icons first \u2014 page <img> tags are last and capped,
    because homepages are full of investor/customer logo strips."""
    def __init__(self):
        super().__init__()
        self.cands = []        # (priority, url)
        self.img_taken = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link":
            rel = (a.get("rel") or "").lower()
            href = a.get("href")
            if not href: return
            low = href.lower().split("?")[0]
            if "apple-touch-icon" in rel: self.cands.append((10, href))
            elif "mask-icon" in rel: self.cands.append((20, href))
            elif "icon" in rel: self.cands.append((15 if low.endswith(".svg") else 30, href))
        elif tag == "meta":
            prop = (a.get("property") or a.get("name") or "").lower()
            if prop in ("og:logo", "og:image", "twitter:image") and a.get("content"):
                self.cands.append((50 if prop == "og:logo" else 60, a["content"]))
        elif tag == "img" and self.img_taken < 2:
            src = a.get("src") or a.get("data-src") or ""
            blob = " ".join(filter(None, [src, a.get("alt"), a.get("class"), a.get("id")])).lower()
            if src and "logo" in blob and not any(b in blob for b in BAD):
                self.img_taken += 1
                self.cands.append((25 if src.lower().split("?")[0].endswith(".svg") else 40, src))

EXT = {"image/svg+xml": ".svg", "image/png": ".png", "image/jpeg": ".jpg",
       "image/webp": ".webp", "image/x-icon": ".ico", "image/vnd.microsoft.icon": ".ico",
       "image/gif": ".gif", "image/avif": ".avif"}

def slugify(n):
    return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

def save(slug, data, ctype, note):
    ext = EXT.get(ctype.split(";")[0].strip().lower())
    if not ext:
        ext = ".svg" if data[:200].lstrip()[:5].lower().startswith(b"<svg") or b"<svg" in data[:300] else ".png"
    path = os.path.join(OUT, slug + ext)
    with open(path, "wb") as f:
        f.write(data)
    return {"file": os.path.basename(path), "bytes": len(data), "via": note}

def work(row):
    name, domain = row["name"], (row["domain"] or "").strip()
    slug = slugify(name)
    res = {"name": name, "slug": slug, "domain": domain, "status": "no-domain"}
    if not domain:
        return res
    base = "https://" + domain
    html = None
    for u in (base, "https://www." + domain):
        try:
            body, _, final = get(u)
            html, base = body.decode("utf-8", "ignore"), final
            res["resolved"] = final
            break
        except Exception as e:
            res["error"] = f"{type(e).__name__}: {e}"
    if html:
        p = Scrape(); p.feed(html)
        seen = set()
        for _, href in sorted(p.cands, key=lambda c: c[0]):
            full = urllib.parse.urljoin(base, href)
            if full in seen: continue
            seen.add(full)
            try:
                data, ctype, _ = get(full)
                if len(data) < 300 or not (ctype.startswith("image") or b"<svg" in data[:400]):
                    continue
                res.update(save(slug, data, ctype, href), status="ok")
                return res
            except Exception:
                continue
    # fallback: favicon service
    try:
        data, ctype, _ = get(f"https://www.google.com/s2/favicons?domain={domain}&sz=256")
        if len(data) > 300:
            res.update(save(slug, data, ctype, "google-favicon"), status="fallback")
            return res
    except Exception as e:
        res["error"] = f"{type(e).__name__}: {e}"
    res["status"] = res.get("status") if res.get("status") == "ok" else "failed"
    return res

rows = list(csv.DictReader(open(os.path.join(ROOT, "companies.csv"))))
with ThreadPoolExecutor(max_workers=16) as ex:
    results = list(ex.map(work, rows))
json.dump(results, open(os.path.join(ROOT, "logo_report.json"), "w"), indent=2)
from collections import Counter
c = Counter(r["status"] for r in results)
print(dict(c))
for r in results:
    if r["status"] in ("failed", "no-domain"):
        print(f"  {r['status']:10} {r['name']}  {r.get('domain','')}  {r.get('error','')[:70]}")
