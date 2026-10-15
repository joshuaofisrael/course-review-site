import os, json
BASE="https://coursegauge.com"
BRAND="CourseGauge"
CF_BEACON_TOKEN=""  # Cloudflare Web Analytics token; leave empty until issued
BEACON=(f'<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{{"token": "{CF_BEACON_TOKEN}"}}\'></script>' if CF_BEACON_TOKEN else "")
Y=2026; CHECKED="October 15, 2026"
ADDR="5640 W Maple Rd, Ste 101, West Bloomfield, MI 48322"
LOGO='<svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="#1b4d3e"/><path d="M6 20 A10 10 0 0 1 26 20" stroke="#f2c14e" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M16 20 L22 12" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/><circle cx="16" cy="20" r="2.5" fill="#fff"/></svg>'
CSS="""*{box-sizing:border-box}body{margin:0;font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1a1a;background:#fbfaf7}
a{color:#0b5a8a}header,footer{background:#1b4d3e;color:#fff}header a,footer a{color:#fff}.wrap{max-width:860px;margin:auto;padding:0 18px}
header .wrap{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:12px 18px}.brand{font-weight:700;font-size:1.2rem;text-decoration:none;display:flex;gap:8px;align-items:center}
nav{margin-left:auto;display:flex;gap:14px;flex-wrap:wrap}main{padding:24px 0 40px}.disc{background:#fff6dc;border:1px solid #e6cf8a;padding:10px 14px;border-radius:6px;font-size:.92rem}
table{border-collapse:collapse;width:100%;font-size:.95rem;background:#fff}th,td{border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top}th{background:#eef3f1}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px}
footer{font-size:.9rem;padding:22px 0}footer p{margin:.4em 0}.src{font-size:.9rem}.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}img,svg{max-width:100%}@media(max-width:600px){body{font-size:16px}nav{margin-left:0;width:100%}th,td{padding:6px}}a:focus{outline:3px solid #f2c14e}"""
PAGES=[]
def page(path,title,desc,body,schema=None):
    url=f"{BASE}/{path}".replace("index.html","")
    ld=[{"@context":"https://schema.org","@type":"WebPage","name":title,"url":url,"description":desc,
        "publisher":{"@type":"Organization","name":"Joshua Israel Ventures LLC","address":{"@type":"PostalAddress","streetAddress":"5640 W Maple Rd, Ste 101","addressLocality":"West Bloomfield","addressRegion":"MI","postalCode":"48322","addressCountry":"US"}}}]
    if schema: ld.append(schema)
    r="../"*path.count("/")
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {BRAND}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{url}"><link rel="icon" href="{r}logo.svg"><style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld)}</script></head><body>
<header><div class="wrap"><a class="brand" href="{r}index.html">{LOGO}{BRAND}</a><nav><a href="{r}reviews/index.html">Reviews</a><a href="{r}compare/index.html">Comparisons</a><a href="{r}about.html">About</a><a href="{r}contact.html">Contact</a></nav></div></header>
<main class="wrap">
<p class="disc"><strong>Affiliate disclosure:</strong> Some links on {BRAND} may be affiliate links. If you buy through them we may earn a commission at no extra cost to you. This never changes our verdicts. <a href="{r}disclosure.html">Full disclosure</a>.</p>
{body}</main>
<footer><div class="wrap"><p>© {Y} Joshua Israel Ventures LLC. All rights reserved. {BRAND} is owned and operated by Joshua Israel Ventures LLC.</p>
<p>Joshua Israel Ventures LLC, {ADDR}</p>
<p><a href="{r}terms.html">Terms</a> · <a href="{r}privacy.html">Privacy</a> · <a href="{r}disclaimer.html">Disclaimer</a> · <a href="{r}disclosure.html">Affiliate Disclosure</a> · <a href="{r}about.html">About</a> · <a href="{r}contact.html">Contact</a></p>
<p>Platform names and trademarks belong to their respective owners and are used only to identify the services reviewed. {BRAND} is not affiliated with or endorsed by them.</p></div></footer>{BEACON}</body></html>"""
    d=os.path.dirname(path)
    if d: os.makedirs(d,exist_ok=True)
    open(path,"w").write(html); PAGES.append(url)
def srcs(l):
    seen=[];[seen.append(x) for x in l if x not in seen]
    return '<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{u}" rel="nofollow noopener">{t}</a></li>' for t,u in seen)+f'</ul><p class="src">Facts checked {CHECKED}. Prices are US list prices, change often and vary by region; confirm on the provider\'s site before buying.</p>'
R=json.load(open("data/reviews.json"))
C=json.load(open("data/compare.json"))
def rel(k):
    l=[(ck,c['title']) for ck,c in C.items() if k in c['p']]
    return ('<h2>Related comparisons</h2><ul>'+''.join(f'<li><a href="../compare/{a}.html">{b}</a></li>' for a,b in l)+'</ul>') if l else ''
for k,v in R.items():
    body=f"""<h1>{v['name']} review ({Y}): {v['tagline']}</h1>
<p><strong>Short answer:</strong> {v['verdict']}</p>
<h2>Key facts</h2><div class="tw"><table>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in v['facts'])}</table></div>
<h2>Who it suits</h2><p>{v['good']}</p><h2>Who should look elsewhere</h2><p>{v['bad']}</p>
<h2>Our take</h2><p>{v['take']}</p><p><a href="{v['url']}" rel="nofollow noopener sponsored">Visit {v['name']}</a></p>{rel(k)}{srcs(v['sources'])}"""
    page(f"reviews/{k}.html",f"{v['name']} Review {Y}",f"{v['name']} review: pricing, trials, refunds and who it suits, with sources.",body,
      {"@context":"https://schema.org","@type":"Review","itemReviewed":{"@type":"Organization","name":v['name']},"author":{"@type":"Organization","name":BRAND},"reviewBody":v['verdict']})
cards=''.join(f'<div class="card"><h3><a href="{k}.html">{v["name"]}</a></h3><p>{v["tagline"]}</p></div>' for k,v in R.items())
page("reviews/index.html","Online Course Platform Reviews","Independent, sourced reviews of online course platforms.",f"<h1>Online course platform reviews</h1><div class='cards'>{cards}</div>")
C=json.load(open("data/compare.json"))
for k,c in C.items():
    rows=''.join("<tr><th scope='row'>"+f+"</th>"+''.join(f"<td>{dict(R[p]['facts']).get(f,'—')}</td>" for p in c['p'])+"</tr>" for f in c['fields'])
    hdr=''.join(f'<th scope="col"><a href="../reviews/{p}.html">{R[p]["name"]}</a></th>' for p in c['p'])
    body=f"<h1>{c['title']}</h1><p><strong>Short answer:</strong> {c['answer']}</p><div class='tw'><table><tr><th></th>{hdr}</tr>{rows}</table></div>"+''.join(f"<h2>{h}</h2><p>{t}</p>" for h,t in c['sections'])+srcs([s for p in c['p'] for s in R[p]['sources']])
    page(f"compare/{k}.html",c['title'],c['desc'],body)
cc=''.join(f'<div class="card"><h3><a href="{k}.html">{c["title"]}</a></h3></div>' for k,c in C.items())
page("compare/index.html","Course Platform Comparisons","Side-by-side comparisons of online course platforms.",f"<h1>Comparisons</h1><div class='cards'>{cc}</div>")
home=f"""<h1>Find the online course platform that fits how you learn</h1><p>{BRAND} compares subscription and pay-per-course learning platforms on what actually matters: price, trial and refund terms, certificates and the kind of teaching you get. Every fact links to a public source.</p>
<h2>Popular comparisons</h2><div class="cards">{cc.replace('href="','href="compare/')}</div><h2>Reviews</h2><div class="cards">{cards.replace('href="','href="reviews/')}</div>"""
page("index.html","Online Course Platform Reviews and Comparisons","Sourced, independent reviews and comparisons of MasterClass, Coursera, Skillshare, Udemy and more.",home)
for f in sorted(os.listdir("data/legal")):
    t,body=open("data/legal/"+f).read().split("\n",1)
    page(f.replace(".html.txt",".html"),t,f"{t} for {BRAND}, operated by Joshua Israel Ventures LLC.",body.replace("{ANALYTICS}",("We use Cloudflare Web Analytics, a cookie-free, privacy-first service that counts page views without tracking individuals." if CF_BEACON_TOKEN else "If we add analytics in future, we will update this policy before doing so.")).replace("{BRAND}",BRAND).replace("{ADDR}",ADDR))
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"<url><loc>{u}</loc><lastmod>2026-10-15</lastmod></url>\n" for u in PAGES)+"</urlset>\n")
bots=["Googlebot","Bingbot","GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-Web","anthropic-ai","CCBot","Google-Extended","Applebot","Applebot-Extended","PerplexityBot","Bytespider","Amazonbot","meta-externalagent","cohere-ai","DuckDuckBot","YandexBot"]
open("robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
open("llms.txt","w").write(f"# {BRAND}\n> Independent, sourced reviews and comparisons of online course platforms. Owned by Joshua Israel Ventures LLC.\n\n"+"\n".join(f"- {u}" for u in PAGES)+"\n")
open("logo.svg","w").write(LOGO.replace('aria-hidden="true"','xmlns="http://www.w3.org/2000/svg"'))
open(".nojekyll","w").write("")
