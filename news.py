# News posts: at most one a day, only real relevant news, own words, cited. Newest first.
NEWS=[
{"slug":"edx-fall-2026-discount-verified-certificates","date":"2026-10-25","nice":"October 25, 2026",
 "modified":"2026-11-21","modified_nice":"November 21, 2026",
 "title":"edX's certificate code is now CYBERMONTH2026",
 "desc":"On 21 Nov 2026 edX's promo page showed CYBERMONTH2026 for 15% off select certificates until Nov 26. FALL2026 was gone.",
 "next":[("../reviews/edx.html","edX review","cat-general"),
         ("../compare/coursera-vs-edx.html","Coursera vs edX","cat-general"),
         ("../compare/best-online-course-platforms-for-certificates.html","Best platforms for certificates","cat-general"),
         ("../compare/best-free-online-course-platforms.html","Best free course platforms","cat-general")],
 "body":"""<p><strong>Updated November 21, 2026.</strong> The promo URL we cited in October no longer mentions FALL2026. On 21 Nov the same page, <a href="https://www.edx.org/courses-and-programs-promo" rel="nofollow noopener">edx.org/courses-and-programs-promo</a>, was headlined as Cyber Month. Its body says to take 15% off selected verified courses, Professional Certificates, MicroBachelors programs and MicroMasters programs with the code <strong>CYBERMONTH2026</strong>, until November 26. A banner on that page also says "save up to 20%" and names the same code. The FAQ and the asterisk disclaimer both say the offer runs until 11:59 p.m. US Eastern Time on November 26, 2026, does not apply to degree programs, cannot be combined with other discounts, and can be changed or cancelled by edX. We have not put the code through a checkout, so the percentage a given course actually drops is whatever that checkout shows.</p>
<h2>What the October note said</h2>
<p>On October 25 the same URL advertised FALL2026, 15% off select verified courses and those same program types, ending at 11:59 p.m. Eastern on November 4. That wording is no longer on the page. If a cart still accepts FALL2026, that is edX's checkout, not something this page can promise.</p>
<h2>Whether the discount is worth using</h2>
<p>It only matters if you were going to pay. Most edX courses can still be audited for free, with temporary access to the materials and no graded assignments or certificate. Audit the opening material, decide whether you want the verified certificate, and only then try the code, before November 26 and before that course's own upgrade deadline. Our <a href="../compare/coursera-vs-edx.html">Coursera vs edX comparison</a> puts per-course pricing next to Coursera Plus.</p>
<p>This is edX's own offer. CourseGauge has no affiliate relationship with edX and earns nothing if you use the code.</p>""",
 "sources":[("edX promo page, read 21 Nov 2026 (CYBERMONTH2026, through Nov 26)","https://www.edx.org/courses-and-programs-promo"),
  ("edX Help: Audit vs verified courses","https://support.edx.org/hc/en-us/articles/360013426573-What-are-the-differences-between-audit-free-and-verified-paid-courses")]},
{"slug":"alison-free-interactive-python-coding-labs","date":"2026-10-16","nice":"October 16, 2026",
 "title":"Alison adds free in-browser Python coding labs",
 "desc":"Alison launched Interactive Coding Labs on Oct 15, 2026: free Python courses where you write and run code in your browser. What's included and how it compares.",
 "body":"""<p>Free course platform Alison announced Interactive Coding Labs on October 15, 2026, starting with Python. Instead of only watching video lessons, learners type and run Python code in an editor that sits next to the lesson instructions, then see straight away whether it works. Alison says there is nothing to install: the coding environment runs in the browser.</p>
<h2>What's available</h2>
<p>According to Alison's announcement, the collection is one foundation course followed by six advanced specialisations. Five courses are live now: the Complete Python Bootcamp, which Alison pitches as taking learners from beginner to upper-intermediate, and Advanced Python courses for data analysis, machine learning, web development, and automation and scripting. The other two specialisations are due in November 2026.</p>
<p>Like the rest of Alison's catalogue, the courses are free to study and complete. A certificate or diploma is an optional purchase after you pass.</p>
<h2>Why it matters if you're learning to code</h2>
<p>Write-and-run practice inside the lesson has been one of the main reasons people pay for platforms such as Codecademy and DataCamp, and it is the format many beginners find sticks better than video alone. Codecademy already has a free Basic tier, but its paid Plus and Pro plans start at $14.99 a month billed annually (US list price, checked October 15, 2026). A free hands-on Python option from Alison gives beginners on a zero budget another way to practise before deciding whether a paid plan is worth it.</p>
<p>Two caveats. First, we have not yet worked through the new labs ourselves, so treat this as news rather than a review. Second, Alison's certificates are its own CPD-accredited credentials, not university certificates; if you need a credential employers widely recognise, compare the options in our <a href="../compare/best-online-course-platforms-for-certificates.html">certificates guide</a>.</p>
""",
 "next":[("../reviews/alison.html","Alison review","cat-general"),
         ("../compare/best-platforms-to-learn-coding-and-tech.html","Best platforms to learn coding","cat-tech"),
         ("../compare/codecademy-vs-datacamp.html","Codecademy vs DataCamp","cat-tech"),
         ("../reviews/codecademy.html","Codecademy review","cat-tech")],
 "sources":[("Alison press release: Alison Launches Interactive Coding Labs (Oct 15, 2026)","https://alison.com/press-room/company-news-&-announcements/alison-launches-interactive-coding-labs-that-let-learners-write-and-run-real-code-inside-the-courses"),
  ("Alison Blog: Learn Python by Doing, Not Just Watching","https://alison.com/blog/learn-python-not-just-watching"),
  ("Alison: Python coding courses","https://alison.com/tag/python-coding"),
  ("Codecademy pricing","https://www.codecademy.com/pricing")]},
]
for n in NEWS:
    src='<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{H.escape(u)}" rel="nofollow noopener">{H.escape(t)}</a></li>' for t,u in n["sources"])+'</ul>'
    mod=n.get("modified",n["date"])
    when=f'Published <time datetime="{n["date"]}">{n["nice"]}</time>'
    if mod!=n["date"]:
        when+=f' · Updated <time datetime="{mod}">{n["modified_nice"]}</time>'
    follow=next_reads(n.get("next") or [],heading="Keep reading")
    body=f'<article><h1>{n["title"]}</h1><p><small>By the {BRAND} editors · {when}</small></p>{n["body"]}{follow}{src}<p class="src">Written by {BRAND} from the sources above. No sponsorship or payment from any company mentioned. Spotted an error? <a href="../contact.html">Tell us</a>.</p></article>'
    url=f'{BASE}/news/{n["slug"]}.html'
    ld={"@context":"https://schema.org","@type":"NewsArticle","headline":n["title"],"description":n["desc"],"datePublished":n["date"],"dateModified":mod,"url":url,"mainEntityOfPage":url,"author":{"@type":"Organization","name":BRAND,"url":BASE},"publisher":{"@id":ORG_ID},"image":OG_IMG,"isAccessibleForFree":True}
    page(f'news/{n["slug"]}.html',n["title"],n["desc"],body,ld,crumbs=[("News","news/"),(n["title"],None)],ogtype="article")
    LASTMOD[url]=mod
li="".join(f'<li><a href="{n["slug"]}.html">{n["title"]}</a> <small>({n["nice"]})</small></li>' for n in NEWS)
page("news/index.html","Online Learning News","Short, sourced news on online course platforms: launches, price changes and what they mean for learners.",f"<h1>Online learning news</h1><p>Short, sourced updates on course platforms, written in our own words with links to the original announcements. We only post when something genuinely matters to learners.</p><ul>{li}</ul><h2>Evergreen guides</h2><p>News moves fast; these pages are kept up to date: <a href='../pricing-tracker/'>price and free-trial tracker</a> · <a href='../subscription-calculator/'>monthly vs annual calculator</a> · <a href='../reviews/'>platform reviews</a> · <a href='../compare/'>comparisons</a>.</p>",crumbs=[("News",None)])
LASTMOD[f"{BASE}/news/"]=max(NEWS[0]["date"],"2026-10-18")  # Oct 18: evergreen links added
LASTMOD[f"{BASE}/reviews/alison.html"]="2026-10-16"
LASTMOD[f"{BASE}/"]="2026-11-21"  # Nov 21: homepage news line updated after the edX promo page changed
LASTMOD[f"{BASE}/about.html"]="2026-10-18"  # Oct 18: method section expanded
LASTMOD[f"{BASE}/pricing-tracker/"]=max(["2026-10-18"]+[r[8]["checked"] for r in json.load(open("data/pricing.json")) if len(r)>8])  # Oct 18 FAQ; later = dated row re-checks
