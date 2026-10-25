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
footer{font-size:.9rem;padding:22px 0}footer p{margin:.4em 0}.src{font-size:.9rem}.crumbs{font-size:.9rem;margin:0 0 10px}fieldset{border:1px solid #ccc;border-radius:6px;margin:0 0 14px;background:#fff}legend{font-weight:700}label{display:inline-block;padding:4px 0}button{font:inherit;padding:10px 18px;background:#1b4d3e;color:#fff;border:0;border-radius:6px;cursor:pointer}button:focus,input:focus{outline:3px solid #f2c14e}caption{text-align:left;font-weight:600;padding:6px 0}.cform input[type=text],.cform input[type=email],.cform textarea{width:100%;max-width:560px;font:inherit;padding:8px;border:1px solid #999;border-radius:6px}.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}img,svg{max-width:100%}@media(max-width:600px){body{font-size:16px}nav{margin-left:0;width:100%}th,td{padding:6px}}a:focus{outline:3px solid #f2c14e}
h1{color:#1b4d3e;line-height:1.2;margin:.4em 0 .5em}h2{color:#1b4d3e;margin:1.6em 0 .5em;padding-bottom:.2em;border-bottom:2px solid #f2c14e;display:inline-block}
header{background:linear-gradient(135deg,#1b4d3e,#256a55);box-shadow:0 2px 8px rgba(0,0,0,.15)}main{padding-top:28px}
.card{box-shadow:0 1px 4px rgba(0,0,0,.08);transition:box-shadow .2s,transform .2s}.card:hover{box-shadow:0 6px 16px rgba(0,0,0,.14);transform:translateY(-2px)}
.card.t{padding:0;overflow:hidden}.card.t img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}.card .cb{padding:12px 14px}.card h3{margin:.2em 0}
figure.ban{margin:0 0 18px}figure.ban img{display:block;width:100%;height:auto;border-radius:12px;box-shadow:0 4px 18px rgba(0,0,0,.18);background:#e9e5da}figure.ban.art{margin:18px 0}figure.ban figcaption{font-size:.82rem;color:#555;margin-top:6px}
.hero{position:relative;margin:0 0 22px;border-radius:14px;overflow:hidden;box-shadow:0 6px 24px rgba(0,0,0,.22);background:#1b4d3e}.hero img{display:block;width:100%;height:auto;aspect-ratio:2/1;object-fit:cover}
.hero .ht{position:absolute;inset:auto 0 0 0;padding:70px 22px 20px;background:linear-gradient(to top,rgba(10,35,28,.92),rgba(10,35,28,0))}.hero h1{color:#fff;margin:0 0 .25em;font-size:clamp(1.5rem,4.5vw,2.3rem);text-shadow:0 1px 6px rgba(0,0,0,.5)}.hero p{color:#f3f3ea;margin:0;font-size:1rem}
table{box-shadow:0 1px 4px rgba(0,0,0,.06)}@media(max-width:600px){.hero img{aspect-ratio:4/3}.hero .ht{padding:40px 14px 12px}.hero p{font-size:.9rem}}"""
PAGES=[]
LASTMOD={}  # url -> real last substantive change date (only set when a page truly changes)
import re as _re, html as _H
ORG_ID=f"{BASE}/#org"; SITE_ID=f"{BASE}/#website"; OG_IMG=f"{BASE}/og-image.png"
ORG={"@type":"Organization","@id":ORG_ID,"name":BRAND,"url":f"{BASE}/","logo":{"@type":"ImageObject","url":f"{BASE}/logo.svg"},
     "brand":{"@type":"Brand","name":BRAND},"address":{"@type":"PostalAddress","streetAddress":"5640 W Maple Rd, Ste 101","addressLocality":"West Bloomfield","addressRegion":"MI","postalCode":"48322","addressCountry":"US"}}
# No on-site search exists, so WebSite carries no SearchAction (it would be false markup).
SITE={"@type":"WebSite","@id":SITE_ID,"name":BRAND,"url":f"{BASE}/","inLanguage":"en","publisher":{"@id":ORG_ID},"description":"Independent, sourced reviews, comparisons and price tools for online course platforms."}

IMGS={ # name -> (alt text describing the photo)
 "hero-home":"Laptop, notebook, coffee mug, headphones and a plant on a sunlit wooden desk, a home study setup for online courses",
 "hub-reviews":"Stack of notebooks, a spiral notepad with a pen and a tablet on a light desk",
 "hub-compare":"Two laptops side by side on a clean desk with a notepad and pen between them",
 "hub-tracker":"Calculator, notepad, coffee cup and a laptop showing a spreadsheet on a wooden desk",
 "hub-quiz":"Notebook with a pen, a smartphone, a coffee mug and reading glasses on a sunlit desk",
 "hub-calc":"Desk calendar, steaming coffee cup, pen and closed laptop on a wooden table",
 "hub-news":"Folded newspaper, coffee cup, reading glasses and a tablet on a table by a window",
 "cat-creative":"Home creative studio with a camera on a tripod, softbox light, sketchbook, brushes and a guitar",
 "cat-tech":"Dark developer desk with a laptop and monitor showing code, a mechanical keyboard and headphones",
 "cat-business":"Office desk with a laptop, leather notebook, fountain pen, coffee cup and plant in front of a city window",
 "cat-general":"Reading nook with a stack of books, open notebook, tablet, tea and headphones by a sunlit window"}
IMGDIM={"hero-home":(1280,720)}
CAT={"creative":["masterclass","skillshare","domestika"],"tech":["codecademy","datacamp","pluralsight","udacity"],"business":["linkedin-learning","teachable"]}
def catof(keys):
    c=[next((g for g,l in CAT.items() if k in l),"general") for k in keys]
    return "cat-"+max(sorted(set(c)),key=lambda g:(c.count(g),-c.index(g)))
HUBIMG={"reviews/index.html":"hub-reviews","compare/index.html":"hub-compare","pricing-tracker/index.html":"hub-tracker","quiz/index.html":"hub-quiz","subscription-calculator/index.html":"hub-calc","news/index.html":"hub-news","index.html":"hero-home"}
def imgfor(path):
    if path in HUBIMG: return HUBIMG[path]
    d,_,f=path.partition("/")
    if d=="reviews" and f: return catof([f[:-5]])
    if d=="compare" and f: return catof(C[f[:-5]]["p"]) if f[:-5] in C else None
    if d=="news" and f: return "hub-news"
    return None
def pic(name,suf,r,cls="",eager=False,w=None,h=None):
    w,h=(w,h) if w else IMGDIM.get(name,(1024,576)) if suf=="" else {"-md":(800,450),"-sm":(480,270)}[suf]
    return f'<img src="{r}images/{name}{suf}.webp" width="{w}" height="{h}" alt="{_H.escape(IMGS[name])}"'+(' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"')+'>'
def thumb(name): return f'<img src="@@/images/{name}-sm.webp" width="480" height="270" alt="{_H.escape(IMGS[name])}" loading="lazy" decoding="async">'
def inject_img(body,path,r):
    n=imgfor(path)
    if not n or path=="index.html": return body
    if path in HUBIMG:
        f=f'<figure class="ban">{pic(n,"",r,eager=True)}</figure>'
        return body.replace("</h1>","</h1>"+f,1) if "</h1>" in body else body
    f=f'<figure class="ban art">{pic(n,"-md",r)}</figure>'
    m=_re.search(r"</h1>(?:\s*<p class=\"src\">.*?</p>|\s*<p><small>.*?</small></p>)?\s*<p>.*?</p>",body,_re.S)
    return body[:m.end()]+f+body[m.end():] if m else body
PAGEINFO=[]  # (url, title, desc) for llms.txt
def _clean(h): return _re.sub(r"\s+"," ",_H.unescape(_re.sub(r"<[^>]+>","",h))).strip()
def _legal_foot(path):
    if os.path.basename(path) in ("terms.html","privacy.html","disclaimer.html","disclosure.html","contact.html"):
        return f"<p>© {Y} Joshua Israel Ventures LLC. All rights reserved. {BRAND} is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company.</p>\n<p>Joshua Israel Ventures LLC, {ADDR}</p>"
    return f"<p>{ADDR}</p>"
def page(path,title,desc,body,schema=None,crumbs=None,ogtype="website",faq=None,modified=None):
    """crumbs: [(name, root-relative href or None for the current page), ...] after Home.
    faq: [(question, answer_html), ...] rendered visibly AND as FAQPage JSON-LD (only real, visible Q&A)."""
    url=f"{BASE}/{path}".replace("index.html","")
    r="../"*path.count("/")
    home=r or "./"
    _n=imgfor(path); OG_IMG=f"{BASE}/images/{_n}-og.jpg" if _n else globals()["OG_IMG"]
    _oa=IMGS[_n] if _n else f"{BRAND}: sourced reviews and price tools for online course platforms"
    body=inject_img(body,path,r)
    wp={"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"isPartOf":{"@id":SITE_ID},"publisher":{"@id":ORG_ID},"inLanguage":"en","primaryImageOfPage":{"@type":"ImageObject","url":OG_IMG}}
    if modified: wp["dateModified"]=modified  # only passed for a real, dated content change
    graph=[ORG,SITE,wp]
    crumb_html=""
    if crumbs:
        items=[("Home","")]+list(crumbs)
        bl={"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":(f"{BASE}/{h}" if h is not None else url)} for i,(n,h) in enumerate(items)]}
        graph.append(bl); wp["breadcrumb"]={"@id":url+"#breadcrumb"}
        parts=[f'<a href="{(r+h) or "./"}">{n}</a>' if h is not None else f'<span aria-current="page">{n}</span>' for n,h in items]
        crumb_html='<nav aria-label="Breadcrumb" class="crumbs">'+' <span aria-hidden="true">›</span> '.join(parts)+'</nav>'
    if faq:
        fh='<h2>Frequently asked questions</h2>'+''.join(f'<h3>{q}</h3><p>{a}</p>' for q,a in faq)
        body=body.replace("<!--FAQ-->",fh) if "<!--FAQ-->" in body else body+fh
        graph.append({"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":_clean(q),"acceptedAnswer":{"@type":"Answer","text":_clean(a)}} for q,a in faq]})
    if schema:
        sc=dict(schema); sc.pop("@context",None); graph.append(sc)
    ld={"@context":"https://schema.org","@graph":graph}
    et=_H.escape(f"{title} | {BRAND}"); ed=_H.escape(desc)
    og=(f'<meta property="og:type" content="{ogtype}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_US">'
        f'<meta property="og:title" content="{_H.escape(title)}"><meta property="og:description" content="{ed}"><meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{OG_IMG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{_H.escape(_oa)}">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{_H.escape(title)}"><meta name="twitter:description" content="{ed}"><meta name="twitter:image" content="{OG_IMG}">')
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="google-site-verification" content="DCgsX3z63BjvDcQOFDkDgY4Mh44YQBuzn1vVoMX8nYs"><meta name="msvalidate.01" content="942EB99DB458637348E2ADBDEBDAA7AE"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{et}</title><meta name="description" content="{ed}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{url}"><link rel="icon" href="{r}logo.svg">{og}<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False).replace("</","<\\/")}</script></head><body>
<header><div class="wrap"><a class="brand" href="{home}">{LOGO}{BRAND}</a><nav aria-label="Main"><a href="{r}reviews/">Reviews</a><a href="{r}compare/">Comparisons</a><a href="{r}pricing-tracker/">Price tracker</a><a href="{r}subscription-calculator/">Calculator</a><a href="{r}quiz/">Quiz</a><a href="{r}news/">News</a><a href="{r}about.html">About</a><a href="{r}contact.html">Contact</a></nav></div></header>
<main class="wrap">{crumb_html}
<p class="disc"><strong>Disclosure:</strong> {BRAND} currently has no affiliate relationships with the platforms we review and earns no commission from links on this page. If that changes, affiliate links will be labelled next to the link and on our disclosure page. <a href="{r}disclosure.html">Full disclosure</a>.</p>
{body}</main>
<footer><div class="wrap">{_legal_foot(path)}
<p><a href="{r}terms.html">Terms</a> · <a href="{r}privacy.html">Privacy</a> · <a href="{r}disclaimer.html">Disclaimer</a> · <a href="{r}disclosure.html">Affiliate Disclosure</a> · <a href="{r}about.html">About</a> · <a href="{r}contact.html">Contact</a></p>
<p>Platform names and trademarks belong to their respective owners and are used only to identify the services reviewed. {BRAND} is not affiliated with or endorsed by them.</p></div></footer>{BEACON}</body></html>"""
    # Internal links always point at the canonical directory URL, never .../index.html
    html=_re.sub(r"""href=(["'])((?:\.\./)*)((?:[\w-]+/)*)index\.html\1""",lambda m:f'href={m.group(1)}{(m.group(2)+m.group(3)) or "./"}{m.group(1)}',html)
    d=os.path.dirname(path)
    if d: os.makedirs(d,exist_ok=True)
    open(path,"w").write(html); PAGES.append(url); PAGEINFO.append((url,title,desc))
def upd(u):
    """Visible, dated note for a real content change (u = {"date","nice","note"}); nothing if unchanged."""
    return f'<p class="src"><strong>Updated {u["nice"]}:</strong> {u["note"]}</p>' if u else ''
def topupd(u): return f'<p class="src">Last updated {u["nice"]}</p>' if u else ''
def srcs(l,u=None):
    seen=[];[seen.append(x) for x in l if x not in seen]
    return '<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{u}" rel="nofollow noopener">{t}</a></li>' for t,u in seen)+f'</ul><p class="src">Facts checked {CHECKED}. Prices are US list prices, change often and vary by region; confirm on the provider\'s site before buying. <a href="../about.html">How we research and check facts</a>.</p>'+upd(u)
R=json.load(open("data/reviews.json"))
C=json.load(open("data/compare.json"))
def rel(k):
    l=[(ck,c['title']) for ck,c in C.items() if k in c['p']]
    return ('<h2>Related comparisons</h2><ul>'+''.join(f'<li><a href="../compare/{a}.html">{b}</a></li>' for a,b in l)+'</ul>') if l else ''
def news_block(k):
    n=R[k].get("news")
    return ('<h2>Latest news</h2><ul>'+''.join(f'<li><a href="../{u}">{t}</a></li>' for t,u in n)+'</ul>') if n else ''
for k,v in R.items():
    body=f"""<h1>{v['name']} review ({Y}): {v['tagline']}</h1>{topupd(v.get('updated'))}
<p><strong>Short answer:</strong> {v['verdict']}</p>
<h2>Key facts</h2><div class="tw"><table>{''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in v['facts'])}</table></div>
<h2>Who it suits</h2><p>{v['good']}</p><h2>Who should look elsewhere</h2><p>{v['bad']}</p>
<p>Compare current prices for all platforms in our <a href="../pricing-tracker/index.html">price and free-trial tracker</a>, check whether an annual plan pays off with the <a href="../subscription-calculator/index.html">monthly vs annual calculator</a>, or take the <a href="../quiz/index.html">platform quiz</a>.</p>{news_block(k)}<h2>Our take</h2><p>{v['take']}</p><p><a href="{v['url']}" rel="nofollow noopener">Visit {v['name']}</a></p>{rel(k)}{srcs(v['sources'],v.get('updated'))}"""
    if v.get('updated'): LASTMOD[f"{BASE}/reviews/{k}.html"]=v['updated']['date']
    page(f"reviews/{k}.html",f"{v['name']} Review {Y}",f"{v['name']} review {Y}: {v['tagline']}. Pricing, free trial, refunds and who it suits, with official sources.",body,
      {"@context":"https://schema.org","@type":"Review","itemReviewed":{"@type":"Organization","name":v['name'],"url":v['url']},"author":{"@type":"Organization","name":BRAND,"url":f"{BASE}/"},"publisher":{"@id":ORG_ID},"reviewBody":v['verdict']},
      crumbs=[("Reviews","reviews/"),(f"{v['name']} review",None)],ogtype="article",modified=(v.get('updated') or {}).get('date'))
cards=''.join(f'<div class="card t">{thumb(catof([k]))}<div class="cb"><h3><a href="{k}.html">{v["name"]}</a></h3><p>{v["tagline"]}</p></div></div>' for k,v in R.items())
page("reviews/index.html","Online Course Platform Reviews","Independent reviews of 20 online course platforms, from MasterClass and Coursera to Duolingo, with prices, trials, refunds and sources.",f"<h1>Online course platform reviews</h1><p>Each review covers pricing, free trials, refund terms, certificates and who the platform suits, with every fact linked to the platform's own pages. Not sure where to start? Take the <a href='../quiz/'>platform quiz</a>, see <a href='../compare/'>side-by-side comparisons</a> or check today's figures in the <a href='../pricing-tracker/'>price tracker</a>.</p><div class='cards'>{cards.replace('@@/','../')}</div>",crumbs=[("Reviews",None)])
C=json.load(open("data/compare.json"))
for k,c in C.items():
    rows=''.join("<tr><th scope='row'>"+f+"</th>"+''.join(f"<td>{dict(R[p]['facts']).get(f,'—')}</td>" for p in c['p'])+"</tr>" for f in c['fields'])
    hdr=''.join(f'<th scope="col"><a href="../reviews/{p}.html">{R[p]["name"]}</a></th>' for p in c['p'])
    body=f"<h1>{c['title']}</h1>{topupd(c.get('updated'))}<p><strong>Short answer:</strong> {c['answer']}</p><p>See every plan side by side in the <a href='../pricing-tracker/index.html'>price tracker</a> or try the <a href='../quiz/index.html'>platform quiz</a>.</p><div class='tw'><table><tr><th></th>{hdr}</tr>{rows}</table></div>"+''.join(f"<h2>{h}</h2><p>{t}</p>" for h,t in c['sections'])+("<!--FAQ-->" if c.get('faq') else "")+srcs(c.get('sources',[])+[s for p in c['p'] for s in R[p]['sources']],c.get('updated'))
    if c.get('updated'): LASTMOD[f"{BASE}/compare/{k}.html"]=c['updated']['date']
    page(f"compare/{k}.html",c['title'],c['desc'],body,crumbs=[("Comparisons","compare/"),(c['title'],None)],ogtype="article",faq=[tuple(x) for x in c.get('faq',[])] or None,modified=(c.get('updated') or {}).get('date'))
cc=''.join(f'<div class="card t">{thumb(catof(c["p"]))}<div class="cb"><h3><a href="{k}.html">{c["title"]}</a></h3></div></div>' for k,c in C.items())
page("compare/index.html","Course Platform Comparisons","Side-by-side comparisons of online course platforms: Coursera vs Udemy, MasterClass vs Skillshare, best free and certificate platforms and more.",f"<h1>Comparisons</h1><p>Head-to-head tables and best-of guides built from the same sourced facts as our <a href='../reviews/'>platform reviews</a>. For the raw numbers, use the <a href='../pricing-tracker/'>price and free-trial tracker</a> or the <a href='../subscription-calculator/'>monthly vs annual calculator</a>.</p><div class='cards'>{cc.replace('@@/','../')}</div>",crumbs=[("Comparisons",None)])
for f in sorted(os.listdir("data/legal")):
    t,body=open("data/legal/"+f).read().split("\n",1)
    LD={"about":f"About {BRAND}: how we research course platforms, cite official sources and date-check every price.",
        "contact":f"Contact {BRAND} with questions, corrections or outdated prices on our online course reviews.",
        "disclaimer":f"Disclaimer for {BRAND}: our online course reviews are general information; prices and terms change, so confirm with each provider.",
        "disclosure":f"Disclosure for {BRAND}: we currently have no affiliate relationships or paid placements, and how we will label affiliate links if that changes.",
        "privacy":f"Privacy policy for {BRAND}: what data we collect (very little), our cookie-free analytics, and your choices.",
        "terms":f"Terms of use for {BRAND}, the independent online course review site, covering content, links, liability and governing law.",
        "thanks":f"Thanks for contacting {BRAND}. Your message reached our team; meanwhile, try our price tracker or platform quiz."}
    START='<p><strong>Start here:</strong> <a href="reviews/">platform reviews</a> · <a href="compare/">comparisons</a> · <a href="pricing-tracker/">price and free-trial tracker</a> · <a href="subscription-calculator/">monthly vs annual calculator</a> · <a href="quiz/">platform quiz</a> · <a href="news/">news</a></p>'
    slug=f.replace(".html.txt","")
    page(slug+".html",t,LD.get(slug,f"{t} for {BRAND}."),crumbs=[(t,None)],body=(body+START).replace("{ANALYTICS}",("We use Cloudflare Web Analytics, a cookie-free, privacy-first service that counts page views without tracking individuals." if CF_BEACON_TOKEN else "If we add analytics in future, we will update this policy before doing so.")).replace("{BRAND}",BRAND).replace("{ADDR}",ADDR))
exec(open("extras.py").read())
exec(open("calc.py").read())
exec(open("news.py").read())
home=f"""<div class="hero">{pic("hero-home","","",eager=True)}<div class="ht"><h1>Find the online course platform that fits how you learn</h1><p>Independent, sourced reviews, comparisons and price tools.</p></div></div><p>{BRAND} compares subscription and pay-per-course learning platforms on what actually matters: price, trial and refund terms, certificates and the kind of teaching you get. Every fact links to a public source.</p>
<p><a href="pricing-tracker/index.html"><strong>Price and free-trial tracker</strong></a>: 20 platforms, every figure sourced. <a href="quiz/index.html"><strong>Which platform fits you?</strong></a> Take the 5-question quiz.</p>
<p><a href="subscription-calculator/index.html"><strong>Monthly or annual?</strong></a> Our break-even calculator shows how many months of use make an annual plan cheaper on 12 popular plans.</p><h2>Latest news</h2><ul>{''.join(f'<li><a href="news/{n["slug"]}.html">{n["title"]}</a> <small>({n["nice"]})</small></li>' for n in NEWS[:3])}</ul><p><a href="news/">All online learning news</a> · <a href="about.html">How we research</a></p><h2>Popular comparisons</h2><div class="cards">{cc.replace('href="','href="compare/').replace('@@/','')}</div><h2>Reviews</h2><div class="cards">{cards.replace('href="','href="reviews/').replace('@@/','')}</div>"""
page("index.html","Online Course Platform Reviews and Comparisons","Sourced, independent reviews and comparisons of MasterClass, Coursera, Skillshare, Udemy and more.",home)
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f"<url><loc>{u}</loc><lastmod>{LASTMOD.get(u,'2026-10-15')}</lastmod></url>\n" for u in PAGES)+"</urlset>\n")
bots=["Googlebot","Bingbot","GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-Web","anthropic-ai","CCBot","Google-Extended","Applebot","Applebot-Extended","PerplexityBot","Bytespider","Amazonbot","meta-externalagent","cohere-ai","DuckDuckBot","YandexBot"]
open("robots.txt","w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
def _llms():
    I={u:(t,d) for u,t,d in PAGEINFO}
    def item(u,label=None,extra=""):
        t,d=I[u]; return f"- [{label or t}]({u}): {d}{extra}"
    sec=lambda pre:[u for u,_,_ in PAGEINFO if u.startswith(f"{BASE}/{pre}") and not u.endswith("/")]
    L=[f"# {BRAND}","",f"> {BRAND} publishes independent, sourced reviews, comparisons and free price tools for online course and learning platforms (Coursera, Udemy, MasterClass, Skillshare, edX, Codecademy, DataCamp, Duolingo and more). Legal operator details are on its Terms and Privacy pages.","",
       "Every price, free-trial length and refund term links to the platform's own official page and carries a check date. Figures we could not confirm are shown as \"see official pricing\" rather than estimated. Prices are US list prices unless stated. Our data tables are free to reuse with a link (CC BY 4.0). We have no paid placements and currently no affiliate relationships; if that changes, affiliate links will be labelled next to the link.","",
       "## Recent fact updates (checked against official sources)",
       f"- October 19, 2026: Coursera completed its combination with Udemy on May 11, 2026; Udemy is a wholly owned Coursera subsidiary, but the platforms, accounts and subscriptions still run separately. See {BASE}/compare/coursera-vs-udemy.html",
       f"- October 19, 2026: Coursera replaced free course auditing with a free preview of the first module of most courses in August 2025; edX still offers a free audit track. See {BASE}/compare/best-free-online-course-platforms.html",
       f"- October 19, 2026: MasterClass sells MasterClass Certificates separately from its membership: 15 to 20-hour courses with a capstone project, from $299 per course or a Certificates Annual Pass. See {BASE}/reviews/masterclass.html","",
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
