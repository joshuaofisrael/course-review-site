"""Recheck pricing-tracker sources and flag changes.
Usage: python3 update_prices.py          # compare with snapshot, print changes
       python3 update_prices.py --save   # store current state as the new baseline
Pages that block bots (403) are reported as UNCHECKED; verify them by hand.
Never edits data/pricing.json automatically: a human verifies, then edits and rebuilds."""
import json,re,sys,hashlib,urllib.request,html,datetime
P=json.load(open("data/pricing.json")); SNAP="data/price-snapshots.json"
try: old=json.load(open(SNAP))
except FileNotFoundError: old={}
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36 CourseGaugePriceCheck"}
new={};changes=[]
for row in P:
    k,url=row[0],row[7]
    try:
        raw=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=25).read().decode("utf-8","ignore")
        text=html.unescape(re.sub(r"<[^>]+>"," ",re.sub(r"(?is)<(script|style).*?</\1>"," ",raw)))
        prices=sorted(set(re.findall(r"[$€£]\s?\d[\d,]*(?:\.\d{2})?",text)))
        trials=sorted(set(re.findall(r"\b\d+[- ]day\b",text,re.I)))
        new[k]={"url":url,"prices":prices,"trials":trials,"status":"ok"}
    except Exception as e:
        new[k]={"url":url,"status":f"UNCHECKED ({getattr(e,'code',e)})"}
        changes.append(f"{k}: UNCHECKED {new[k]['status']} -> check {url} by hand"); continue
    o=old.get(k)
    if o and o.get("status")=="ok" and any(p.startswith("$") for p in o["prices"]) and prices and not any(p.startswith("$") for p in prices):
        changes.append(f"{k}: REGION non-US currency served ({prices[:3]}...), verify US price by hand ({url})"); new[k]=o; continue
    if o and o.get("status")=="ok" and (o["prices"]!=new[k]["prices"] or o["trials"]!=new[k]["trials"]):
        changes.append(f"{k}: CHANGED prices {o['prices']} -> {new[k]['prices']}; trials {o['trials']} -> {new[k]['trials']} ({url})")
print(f"Price check {datetime.date.today()}: {len(P)} sources")
print("\n".join(changes) if changes else "No changes detected on reachable pages.")
if "--save" in sys.argv: json.dump(new,open(SNAP,"w"),indent=1); print("Baseline saved to",SNAP)
