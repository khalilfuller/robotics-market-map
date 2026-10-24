#!/usr/bin/env python3
"""Fetch <title> + meta description for every company domain -> site_meta.json"""
import csv, json, os, re, ssl, urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
ROOT=os.path.dirname(os.path.abspath(__file__))
CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.title=""; s.desc=""; s.og=""; s._t=False
    def handle_starttag(s,t,a):
        d=dict(a)
        if t=="title": s._t=True
        if t=="meta":
            k=(d.get("name") or d.get("property") or "").lower(); c=d.get("content","")
            if k=="description" and not s.desc: s.desc=c
            if k in("og:description","twitter:description") and not s.og: s.og=c
    def handle_endtag(s,t):
        if t=="title": s._t=False
    def handle_data(s,x):
        if s._t and not s.title: s.title=x.strip()

def grab(row):
    dom=(row["domain"] or "").strip()
    out={"name":row["name"],"domain":dom}
    if not dom: return out
    for u in ("https://"+dom,"https://www."+dom):
        try:
            req=urllib.request.Request(u,headers={"User-Agent":UA})
            with urllib.request.urlopen(req,timeout=15,context=CTX) as r:
                html=r.read(400_000).decode("utf-8","ignore")
            p=P(); p.feed(html)
            out["title"]=re.sub(r"\s+"," ",p.title)[:200]
            out["desc"]=re.sub(r"\s+"," ",(p.desc or p.og))[:400]
            out["url"]=r.geturl() if False else u
            return out
        except Exception as e:
            out["error"]=f"{type(e).__name__}"
    return out

rows=list(csv.DictReader(open(os.path.join(ROOT,"companies.csv"))))
with ThreadPoolExecutor(max_workers=16) as ex: res=list(ex.map(grab,rows))
json.dump(res,open(os.path.join(ROOT,"site_meta.json"),"w"),indent=2)
ok=sum(1 for r in res if r.get("desc") or r.get("title"))
print(f"fetched metadata for {ok}/{len(res)}")
