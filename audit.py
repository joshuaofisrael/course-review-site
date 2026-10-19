#!/usr/bin/env python3
"""CourseGauge site-wide SEO audit (stdlib only). Run after `python3 build.py`.

Checks every built HTML page for: unique <title> and meta description, exactly one H1,
canonical (matching the page URL), robots index,follow and no noindex, Open Graph + Twitter
card tags, JSON-LD present and parseable, image alt text, LLC footer with the West Bloomfield
address, the Cloudflare Web Analytics beacon, >=3 contextual internal links out, inbound
internal links (orphans / weakly linked), broken internal links, links to non-canonical
URLs (e.g. .../index.html), and sitemap coverage.

Usage: python3 audit.py [--out reports/audit-YYYY-MM-DD.txt]
Exit code 0 always; the summary line reports the issue count.
"""
import os, re, sys, json, datetime, collections
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE = "https://coursegauge.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
ADDR = "5640 W Maple Rd, Ste 101, West Bloomfield, MI 48322"
SKIP_DIRS = {".git", "data", "outreach", "reports", "node_modules"}
MIN_OUT = 3
MIN_IN = 3
# Legal pages are linked from the site-wide footer; contextual inbound links are not expected.
LEGAL = {"terms.html", "privacy.html", "disclaimer.html", "disclosure.html", "contact.html"}
# Form-confirmation page (shown after the contact form posts); it is not meant to be linked contextually.
UTILITY = {"thanks.html"}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.title = None; s._in_title = False; s.meta = {}; s.links = []; s.canon = []
        s.h1 = 0; s.ld = []; s._ld = None; s.imgs_noalt = 0; s.imgs = 0
        s.zone = []  # stack of header/nav/main/footer
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ("header", "nav", "main", "footer"): s.zone.append(t)
        if t == "title": s._in_title = True; s.title = ""
        elif t == "meta":
            k = a.get("name") or a.get("property")
            if k: s.meta.setdefault(k.lower(), []).append(a.get("content", ""))
        elif t == "link" and (a.get("rel") or "").lower() == "canonical": s.canon.append(a.get("href", ""))
        elif t == "h1": s.h1 += 1
        elif t == "a" and a.get("href"): s.links.append((a["href"], "main" in s.zone and "nav" not in s.zone, a.get("class", "")))
        elif t == "img":
            s.imgs += 1
            if not (a.get("alt") or "").strip(): s.imgs_noalt += 1
        elif t == "script" and (a.get("type") or "") == "application/ld+json": s._ld = ""
    def handle_endtag(s, t):
        if t in ("header", "nav", "main", "footer") and s.zone and s.zone[-1] == t: s.zone.pop()
        if t == "title": s._in_title = False
        if t == "script" and s._ld is not None: s.ld.append(s._ld); s._ld = None
    def handle_data(s, d):
        if s._in_title: s.title += d
        if s._ld is not None: s._ld += d

def url_for(rel):
    u = BASE + "/" + rel
    return u[:-len("index.html")] if u.endswith("index.html") else u

def file_for(url):
    p = urlparse(url)
    if p.netloc and p.netloc not in ("coursegauge.com", "www.coursegauge.com"): return None
    path = p.path.lstrip("/")
    if path == "" or path.endswith("/"): path += "index.html"
    return path

def main():
    out = None
    if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]
    pages = []
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if x not in SKIP_DIRS and not x.startswith(".")]
        for f in fs:
            if f.endswith(".html"): pages.append(os.path.relpath(os.path.join(d, f), ROOT))
    pages.sort()
    sm = open(os.path.join(ROOT, "sitemap.xml")).read()
    sm_urls = set(re.findall(r"<loc>(.*?)</loc>", sm))
    issues = collections.defaultdict(list)  # check -> [page: detail]
    titles = collections.defaultdict(list); descs = collections.defaultdict(list)
    inbound_ctx = collections.defaultdict(set); inbound_any = collections.defaultdict(set)
    outcount = {}; stats = {}
    for rel in pages:
        raw = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        p = P(); p.feed(raw)
        me = url_for(rel)
        def bad(check, detail=""): issues[check].append(f"{rel}" + (f": {detail}" if detail else ""))
        t = (p.title or "").strip()
        if not t: bad("missing <title>")
        else:
            titles[t].append(rel)
            if len(t) > 65: bad("title over 65 chars", f"{len(t)} chars")
        d = (p.meta.get("description") or [""])[0].strip()
        if not d: bad("missing meta description")
        else:
            descs[d].append(rel)
            if len(d) > 160: bad("meta description over 160 chars", f"{len(d)} chars")
            if len(d) < 70: bad("meta description under 70 chars", f"{len(d)} chars")
        if p.h1 != 1: bad("H1 count not 1", str(p.h1))
        if len(p.canon) != 1: bad("canonical count not 1", str(len(p.canon)))
        elif p.canon[0] != me: bad("canonical mismatch", p.canon[0])
        rb = ",".join(p.meta.get("robots", [])).replace(" ", "").lower()
        if "noindex" in raw.lower() or "nofollow" in rb: bad("noindex/nofollow present")
        if "index" not in rb or "follow" not in rb: bad("robots meta not index,follow")
        for k in ("og:title", "og:description", "og:url", "og:type", "og:site_name", "og:image", "twitter:card"):
            if k not in p.meta: bad(f"missing {k}")
        if "og:url" in p.meta and p.meta["og:url"][0] != me: bad("og:url mismatch", p.meta["og:url"][0])
        types = []
        if not p.ld: bad("no JSON-LD")
        for blk in p.ld:
            try:
                j = json.loads(blk)
                for it in (j if isinstance(j, list) else [j]):
                    g = it.get("@graph", [it]) if isinstance(it, dict) else []
                    for x in g:
                        ty = x.get("@type"); types += ty if isinstance(ty, list) else [ty]
            except Exception as e: bad("JSON-LD parse error", str(e)[:80])
        for need in ("Organization", "WebSite"):
            if need not in types: bad(f"JSON-LD missing {need}")
        if rel.startswith(("reviews/", "compare/", "news/")) and not rel.endswith("index.html") and "BreadcrumbList" not in types:
            bad("JSON-LD missing BreadcrumbList")
        if p.imgs_noalt: bad("images without alt", str(p.imgs_noalt))
        if ADDR not in raw or "Joshua Israel Ventures LLC" not in raw: bad("LLC footer/address missing")
        if "Farmington" in raw or "Horton" in raw: bad("FORBIDDEN home address present")
        if "static.cloudflareinsights.com/beacon.min.js" not in raw: bad("Cloudflare beacon missing")
        ctx_targets = set(); any_targets = set()
        for href, in_main, cls in p.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "#")): continue
            absu = urljoin(me, href)
            pu = urlparse(absu)
            if pu.netloc not in ("coursegauge.com", "www.coursegauge.com"): continue
            f = file_for(absu.split("#")[0].split("?")[0])
            if f is None: continue
            if not os.path.exists(os.path.join(ROOT, f)): bad("broken internal link", href); continue
            if pu.path.endswith("/index.html") or pu.path == "/index.html": bad("link to non-canonical index.html URL", href)
            if not f.endswith(".html"): continue
            if f == rel: continue
            any_targets.add(f)
            if in_main: ctx_targets.add(f)
        for f in any_targets: inbound_any[f].add(rel)
        for f in ctx_targets: inbound_ctx[f].add(rel)
        outcount[rel] = len(ctx_targets)
        if len(ctx_targets) < MIN_OUT: bad(f"fewer than {MIN_OUT} contextual internal links out", str(len(ctx_targets)))
        if me not in sm_urls: bad("not in sitemap.xml")
        stats[rel] = types
    for rel in pages:
        if not inbound_any[rel] and rel != "index.html" and rel not in UTILITY: issues["orphan (no inbound links at all)"].append(rel)
        if len(inbound_ctx[rel]) < MIN_IN and rel != "index.html" and rel not in LEGAL and rel not in UTILITY:
            issues[f"fewer than {MIN_IN} contextual inbound links"].append(f"{rel}: {len(inbound_ctx[rel])}")
    for t, l in titles.items():
        if len(l) > 1: issues["duplicate title"].append(f"{t!r}: {', '.join(l)}")
    for t, l in descs.items():
        if len(l) > 1: issues["duplicate meta description"].append(f"{t[:60]!r}...: {', '.join(l)}")
    for u in sorted(sm_urls):
        f = file_for(u)
        if not f or not os.path.exists(os.path.join(ROOT, f)): issues["sitemap URL without file"].append(u)
    total = sum(len(v) for v in issues.values())
    lines = [f"CourseGauge SEO audit, {datetime.datetime.now():%Y-%m-%d %H:%M} (box local time)",
             f"Pages audited: {len(pages)} | sitemap URLs: {len(sm_urls)} | checks failing: {len(issues)} | total issues: {total}", ""]
    for k in sorted(issues, key=lambda k: -len(issues[k])):
        lines.append(f"## {k} ({len(issues[k])})")
        lines += [f"  - {x}" for x in issues[k][:60]]
        if len(issues[k]) > 60: lines.append(f"  ... and {len(issues[k]) - 60} more")
        lines.append("")
    lines.append("## Contextual internal links per page (out / in)")
    for rel in pages: lines.append(f"  {rel}: out {outcount[rel]} / in {len(inbound_ctx[rel])}  [{', '.join(str(x) for x in stats[rel])}]")
    rep = "\n".join(lines) + "\n"
    if out:
        os.makedirs(os.path.dirname(os.path.join(ROOT, out)) or ".", exist_ok=True)
        open(os.path.join(ROOT, out), "w").write(rep)
    print("\n".join(lines[:2]))
    for k in sorted(issues, key=lambda k: -len(issues[k])): print(f"  {len(issues[k]):3d}  {k}")
    return total

if __name__ == "__main__":
    main()
