import os, json
BASE="https://coursegauge.com"
BRAND="CourseGauge"
CF_BEACON_TOKEN = "73c6bccca4c14c9e95d33f88b6da2b76"
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
footer{font-size:.9rem;padding:22px 0}footer p{margin:.4em 0}.src{font-size:.9rem}.crumbs{font-size:.9rem;margin:0 0 10px}fieldset{border:1px solid #ccc;border-radius:6px;margin:0 0 14px;background:#fff}legend{font-weight:700}label{display:inline-block;padding:4px 0}button{font:inherit;padding:10px 18px;background:#1b4d3e;color:#fff;border:0;border-radius:6px;cursor:pointer}button:focus,input:focus{outline:3px solid #f2c14e}caption{text-align:left;font-weight:600;padding:6px 0}.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}img,svg{max-width:100%}@media(max-width:600px){body{font-size:16px}nav{margin-left:0;width:100%}th,td{padding:6px}}a:focus{outline:3px solid #f2c14e}"""
PAGES=[]
LASTMOD={}  # url -> real last substantive change date (only set when a page truly changes)
import re as _re, html as _H
ORG_ID=f"{BASE}/#org"; SITE_ID=f"{BASE}/#website"; OG_IMG=f"{BASE}/og-image.png"
ORG={"@type":"Organization","@id":ORG_ID,"name":"Joshua Israel Ventures LLC","url":f"{BASE}/","logo":{"@type":"ImageObject","url":f"{BASE}/logo.svg"},
     "brand":{"@type":"Brand","name":BRAND},"address":{"@type":"PostalAddress","streetAddress":"5640 W Maple Rd, Ste 101","addressLocality":"West Bloomfield","addressRegion":"MI","postalCode":"48322","addressCountry":"US"}}
# No on-site search exists, so WebSite carries no SearchAction (it would be false markup).
SITE={"@type":"WebSite","@id":SITE_ID,"name":BRAND,"url":f"{BASE}/","inLanguage":"en","publisher":{"@id":ORG_ID},"description":"Independent, sourced reviews, comparisons and price tools for online course platforms."}
PAGEINFO=[]  # (url, title, desc) for llms.txt
def _clean(h): return _re.sub(r"\s+"," ",_H.unescape(_re.sub(r"<[^>]+>","",h))).strip()
def page(path,title,desc,body,schema=None,crumbs=None,ogtype="website",faq=None):
    """crumbs: [(name, root-relative href or None for the current page), ...] after Home.
    faq: [(question, answer_html), ...] rendered visibly AND as FAQPage JSON-LD (only real, visible Q&A)."""
    url=f"{BASE}/{path}".replace("index.html","")
    r="../"*path.count("/")
    home=r or "./"
    wp={"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"isPartOf":{"@id":SITE_ID},"publisher":{"@id":ORG_ID},"inLanguage":"en","primaryImageOfPage":{"@type":"ImageObject","url":OG_IMG}}
    graph=[ORG,SITE,wp]
    crumb_html=""
    if crumbs:
        items=[("Home","")]+list(crumbs)
        bl={"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":(f"{BASE}/{h}" if h is not None else url)} for i,(n,h) in enumerate(items)]}
        graph.append(bl); wp["breadcrumb"]={"@id":url+"#breadcrumb"}
        parts=[f'<a href="{(r+h) or "./"}">{n}</a>' if h is not None else f'<span aria-current="page">{n}</span>' for n,h in items]
        crumb_html='<nav aria-label="Breadcrumb" class="crumbs">'+' <span aria-hidden="true">›</span> '.join(parts)+'</nav>'
    if faq:
        body+='<h2>Frequently asked questions</h2>'+''.join(f'<h3>{q}</h3><p>{a}</p>' for q,a in faq)
        graph.append({"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":_clean(q),"acceptedAnswer":{"@type":"Answer","text":_clean(a)}} for q,a in faq]})
    if schema:
        sc=dict(schema); sc.pop("@context",None); graph.append(sc)
    ld={"@context":"https://schema.org","@graph":graph}
    et=_H.escape(f"{title} | {BRAND}"); ed=_H.escape(desc)
    og=(f'<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_US">'
        f'<meta property="og:title" content="{_H.escape(title)}"><meta property="og:description" content="{ed}"><meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{OG_IMG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{BRAND}: sourced reviews and price tools for online course platforms">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{_H.escape(title)}"><meta name="twitter:description" content="{ed}"><meta name="twitter:image" content="{OG_IMG}">')
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="google-site-verification" content="DCgsX3z63BjvDcQOFDkDgY4Mh44YQBuzn1vVoMX8nYs"><meta name="msvalidate.01" content="942EB99DB458637348E2ADBDEBDAA7AE"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{et}</title><meta name="description" content="{ed}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{url}"><link rel="icon" href="{r}logo.svg">{og}<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False).replace("</","<\\/")}</script></head><body>
<header><div class="wrap"><a class="brand" href="{home}">{LOGO}{BRAND}</a><nav aria-label="Main"><a href="{r}reviews/">Reviews</a><a href="{r}compare/">Comparisons</a><a href="{r}pricing-tracker/">Price tracker</a><a href="{r}subscription-calculator/">Calculator</a><a href="{r}quiz/">Quiz</a><a href="{r}news/">News</a><a href="{r}about.html">About</a><a href="{r}contact.html">Contact</a></nav></div></header>
<main class="wrap">{crumb_html}
<p class="disc"><strong>Affiliate disclosure:</strong> Some links on {BRAND} may be affiliate links. If you buy through them we may earn a commission at no extra cost to you. This never changes our verdicts. <a href="{r}disclosure.html">Full disclosure</a>.</p>
{body}</main>
<footer><div class="wrap"><p>© {Y} Joshua Israel Ventures LLC. All rights reserved. {BRAND} is owned and operated by Joshua Israel Ventures LLC.</p>
<p>Joshua Israel Ventures LLC, {ADDR}</p>
<p><a href="{r}terms.html">Terms</a> · <a href="{r}privacy.html">Privacy</a> · <a href="{r}disclaimer.html">Disclaimer</a> · <a href="{r}disclosure.html">Affiliate Disclosure</a> · <a href="{r}about.html">About</a> · <a href="{r}contact.html">Contact</a></p>
<p>Platform names and trademarks belong to their respective owners and are used only to identify the services reviewed. {BRAND} is not affiliated with or endorsed by them.</p></div></footer>{BEACON}</body></html>"""
    # Internal links always point at the canonical directory URL, never .../index.html
    html=_re.sub(r"""href=(["'])((?:\.\./)*)((?:[\w-]+/)*)index\.html\1""",lambda m:f'href={m.group(1)}{(m.group(2)+m.group(3)) or "./"}{m.group(1)}',html)
    d=os.path.dirname(path)
    if d: os.makedirs(d,exist_ok=True)
    open(path,"w").write(html); PAGES.append(url); PAGEINFO.append((url,title,desc))
def srcs(l):
    seen=[];[seen.append(x) for x in l if x not in seen]
    return '<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{u}" rel="nofollow noopener">{t}</a></li>' for t,u in seen)+f'</ul><p class="src">Facts checked {CHECKED}. Prices are US list prices, change often and vary by region; confirm on the provider\'s site before buying. <a href="../about.html">How we research and check facts</a>.</p>'
R=json.load(open("data/reviews.json"))
C=json.load(open("data/compare.json"))
def rel(k):
    l=[(ck,c['title']) for ck,c in C.items() if k in c['p']]
    return ('<h2>Related comparisons</h2><ul>'+''.join(f'<li><a href="../compare/{a}.html">{b}</a></li>' for a,b in l)+'</ul>') if l else ''
def news_block(k):
    n=R[k].get("news")
    return ('<h2>Latest news</h2><ul>'+''.join(f'<li><a href="../{u}">{t}</a></li>' for t,u in n)+'</ul>') if n else ''
for k,v in R.items():
    body=f"""<h1>{v['name']} review ({Y}): {v['tagline']}</h1>
<p><strong>Short answer:</strong> {v['verdict']}</p>
<h2>Key facts</h2><div class="tw"><table>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in v['facts'])}</table></div>
<h2>Who it suits</h2><p>{v['good']}</p><h2>Who should look elsewhere</h2><p>{v['bad']}</p>
<p>Compare current prices for all platforms in our <a href="../pricing-tracker/index.html">price and free-trial tracker</a>, check whether an annual plan pays off with the <a href="../subscription-calculator/index.html">monthly vs annual calculator</a>, or take the <a href="../quiz/index.html">platform quiz</a>.</p>{news_block(k)}<h2>Our take</h2><p>{v['take']}</p><p><a href="{v['url']}" rel="nofollow noopener sponsored">Visit {v['name']}</a></p>{rel(k)}{srcs(v['sources'])}"""
    page(f"reviews/{k}.html",f"{v['name']} Review {Y}",f"{v['name']} review {Y}: {v['tagline']}. Pricing, free trial, refunds and who it suits, with official sources.",body,
      {"@context":"https://schema.org","@type":"Review","itemReviewed":{"@type":"Organization","name":v['name'],"url":v['url']},"author":{"@type":"Organization","name":BRAND,"url":f"{BASE}/"},"publisher":{"@id":ORG_ID},"reviewBody":v['verdict']},
      crumbs=[("Reviews","reviews/"),(f"{v['name']} review",None)],ogtype="article")
cards=''.join(f'<div class="card"><h3><a href="{k}.html">{v["name"]}</a></h3><p>{v["tagline"]}</p></div>' for k,v in R.items())
page("reviews/index.html","Online Course Platform Reviews","Independent reviews of 20 online course platforms, from MasterClass and Coursera to Duolingo, with prices, trials, refunds and sources.",f"<h1>Online course platform reviews</h1><p>Each review covers pricing, free trials, refund terms, certificates and who the platform suits, with every fact linked to the platform's own pages. Not sure where to start? Take the <a href='../quiz/'>platform quiz</a>, see <a href='../compare/'>side-by-side comparisons</a> or check today's figures in the <a href='../pricing-tracker/'>price tracker</a>.</p><div class='cards'>{cards}</div>",crumbs=[("Reviews",None)])
C=json.load(open("data/compare.json"))
for k,c in C.items():
    rows=''.join("<tr><th scope='row'>"+f+"</th>"+''.join(f"<td>{dict(R[p]['facts']).get(f,'—')}</td>" for p in c['p'])+"</tr>" for f in c['fields'])
    hdr=''.join(f'<th scope="col"><a href="../reviews/{p}.html">{R[p]["name"]}</a></th>' for p in c['p'])
    body=f"<h1>{c['title']}</h1><p><strong>Short answer:</strong> {c['answer']}</p><p>See every plan side by side in the <a href='../pricing-tracker/index.html'>price tracker</a> or try the <a href='../quiz/index.html'>platform quiz</a>.</p><div class='tw'><table><tr><th></th>{hdr}</tr>{rows}</table></div>"+''.join(f"<h2>{h}</h2><p>{t}</p>" for h,t in c['sections'])+srcs([s for p in c['p'] for s in R[p]['sources']])
    page(f"compare/{k}.html",c['title'],c['desc'],body,crumbs=[("Comparisons","compare/"),(c['title'],None)],ogtype="article")
cc=''.join(f'<div class="card"><h3><a href="{k}.html">{c["title"]}</a></h3></div>' for k,c in C.items())
page("compare/index.html","Course Platform Comparisons","Side-by-side comparisons of online course platforms: Coursera vs Udemy, MasterClass vs Skillshare, best free and certificate platforms and more.",f"<h1>Comparisons</h1><p>Head-to-head tables and best-of guides built from the same sourced facts as our <a href='../reviews/'>platform reviews</a>. For the raw numbers, use the <a href='../pricing-tracker/'>price and free-trial tracker</a> or the <a href='../subscription-calculator/'>monthly vs annual calculator</a>.</p><div class='cards'>{cc}</div>",crumbs=[("Comparisons",None)])
for f in sorted(os.listdir("data/legal")):
    t,body=open("data/legal/"+f).read().split("\n",1)
    LD={"about":f"About {BRAND}: who runs it (Joshua Israel Ventures LLC), how we research course platforms, cite official sources and date-check every price.",
        "contact":f"Contact {BRAND} and Joshua Israel Ventures LLC with questions, corrections or outdated prices on our online course reviews.",
        "disclaimer":f"Disclaimer for {BRAND}: our online course reviews are general information; prices and terms change, so confirm with each provider.",
        "disclosure":f"Affiliate disclosure for {BRAND}: how affiliate links work on our course reviews and why they never change our verdicts.",
        "privacy":f"Privacy policy for {BRAND}: what data we collect (very little), our cookie-free analytics, and your choices.",
        "terms":f"Terms of use for {BRAND}, the online course review site operated by Joshua Israel Ventures LLC."}
    START='<p><strong>Start here:</strong> <a href="reviews/">platform reviews</a> · <a href="compare/">comparisons</a> · <a href="pricing-tracker/">price and free-trial tracker</a> · <a href="subscription-calculator/">monthly vs annual calculator</a> · <a href="quiz/">platform quiz</a> · <a href="news/">news</a></p>'
    slug=f.replace(".html.txt","")
    page(slug+".html",t,LD.get(slug,f"{t} for {BRAND}, operated by Joshua Israel Ventures LLC."),crumbs=[(t,None)],body=(body+START).replace("{ANALYTICS}",("We use Cloudflare Web Analytics, a cookie-free, privacy-first service that counts page views without tracking individuals." if CF_BEACON_TOKEN else "If we add analytics in future, we will update this policy before doing so.")).replace("{BRAND}",BRAND).replace("{ADDR}",ADDR))
exec(open("extras.py").read())
exec(open("calc.py").read())
exec(open("news.py").read())
home=f"""<h1>Find the online course platform that fits how you learn</h1><p>{BRAND} compares subscription and pay-per-course learning platforms on what actually matters: price, trial and refund terms, certificates and the kind of teaching you get. Every fact links to a public source.</p>
<p><a href="pricing-tracker/index.html"><strong>Price and free-trial tracker</strong></a>: 20 platforms, every figure sourced. <a href="quiz/index.html"><strong>Which platform fits you?</strong></a> Take the 5-question quiz.</p>
<p><a href="subscription-calculator/index.html"><strong>Monthly or annual?</strong></a> Our break-even calculator shows how many months of use make an annual plan cheaper on 12 popular plans.</p><h2>Latest news</h2><ul>{''.join(f'<li><a href="news/{n["slug"]}.html">{n["title"]}</a> <small>({n["nice"]})</small></li>' for n in NEWS[:3])}</ul><p><a href="news/">All online learning news</a> · <a href="about.html">How we research</a></p><h2>Popular comparisons</h2><div class="cards">{cc.replace('href="','href="compare/')}</div><h2>Reviews</h2><div class="cards">{cards.replace('href="','href="reviews/')}</div>"""
page("index.html","Online Course Platform Reviews and Comparisons","Sourced, independent reviews and comparisons of MasterClass, Coursera, Skillshare, Udemy and more.",home)
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"<url><loc>{u}</loc><lastmod>{LASTMOD.get(u,'2026-10-15')}</lastmod></url>\n" for u in PAGES)+"</urlset>\n")
bots=["Googlebot","Bingbot","GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-Web","anthropic-ai","CCBot","Google-Extended","Applebot","Applebot-Extended","PerplexityBot","Bytespider","Amazonbot","meta-externalagent","cohere-ai","DuckDuckBot","YandexBot"]
open("robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
def _llms():
    I={u:(t,d) for u,t,d in PAGEINFO}
    def item(u,label=None,extra=""):
        t,d=I[u]; return f"- [{label or t}]({u}): {d}{extra}"
    sec=lambda pre:[u for u,_,_ in PAGEINFO if u.startswith(f"{BASE}/{pre}") and not u.endswith("/")]
    L=[f"# {BRAND}","",f"> {BRAND} publishes independent, sourced reviews, comparisons and free price tools for online course and learning platforms (Coursera, Udemy, MasterClass, Skillshare, edX, Codecademy, DataCamp, Duolingo and more). It is owned and operated by Joshua Israel Ventures LLC, {ADDR}, USA.","",
       "Every price, free-trial length and refund term links to the platform's own official page and carries a check date. Figures we could not confirm are shown as \"see official pricing\" rather than estimated. Prices are US list prices unless stated. Our data tables are free to reuse with a link (CC BY 4.0). We have no paid placements; some links may be affiliate links, disclosed on every page.","",
       "## Tools and data",
       item(f"{BASE}/pricing-tracker/",extra=f" CSV: {BASE}/pricing-tracker/coursegauge-pricing-tracker.csv"),
       item(f"{BASE}/subscription-calculator/",extra=f" Key finding: annual billing pays off after {lo} to {hi} months of use (median {med:g}) across {len(PLANS)} plans. CSV: {BASE}/subscription-calculator/coursegauge-annual-vs-monthly.csv"),
       item(f"{BASE}/quiz/"),"",
       "## Comparisons and best-of guides",item(f"{BASE}/compare/","All comparisons")]+[item(u) for u in sec("compare/")]+["",
       "## Platform reviews",item(f"{BASE}/reviews/","All reviews")]+[item(u) for u in sec("reviews/")]+["",
       "## News",item(f"{BASE}/news/","News index")]+[item(u,extra=f" (published {n['nice']})") for n in NEWS for u in [f"{BASE}/news/{n['slug']}.html"]]+["",
       "## About and policies",item(f"{BASE}/about.html","About CourseGauge and our method")]+[item(f"{BASE}/{p}.html") for p in ("contact","disclosure","privacy","terms","disclaimer")]+["",
       "## Optional",f"- [Sitemap]({BASE}/sitemap.xml): every indexable URL with its last substantive change date",f"- [Home]({BASE}/): overview, latest news and links to every review and comparison",""]
    open("llms.txt","w").write("\n".join(L))
_llms()
open("logo.svg","w").write(LOGO.replace('aria-hidden="true"','xmlns="http://www.w3.org/2000/svg"'))
open(".nojekyll","w").write("")
