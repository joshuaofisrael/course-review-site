# News posts: at most one a day, only real relevant news, own words, cited. Newest first.
NEWS=[
{"slug":"alison-free-interactive-python-coding-labs","date":"2026-10-16","nice":"October 16, 2026",
 "title":"Alison adds free in-browser Python coding labs",
 "desc":"Alison launched Interactive Coding Labs on October 15, 2026: free Python courses where you write and run code in the browser. What's included and how it compares.",
 "body":"""<p>Free course platform Alison announced Interactive Coding Labs on October 15, 2026, starting with Python. Instead of only watching video lessons, learners type and run Python code in an editor that sits next to the lesson instructions, then see straight away whether it works. Alison says there is nothing to install: the coding environment runs in the browser.</p>
<h2>What's available</h2>
<p>According to Alison's announcement, the collection is one foundation course followed by six advanced specialisations. Five courses are live now: the Complete Python Bootcamp, which Alison pitches as taking learners from beginner to upper-intermediate, and Advanced Python courses for data analysis, machine learning, web development, and automation and scripting. The other two specialisations are due in November 2026.</p>
<p>Like the rest of Alison's catalogue, the courses are free to study and complete. A certificate or diploma is an optional purchase after you pass.</p>
<h2>Why it matters if you're learning to code</h2>
<p>Write-and-run practice inside the lesson has been one of the main reasons people pay for platforms such as Codecademy and DataCamp, and it is the format many beginners find sticks better than video alone. Codecademy already has a free Basic tier, but its paid Plus and Pro plans start at $14.99 a month billed annually (US list price, checked October 15, 2026). A free hands-on Python option from Alison gives beginners on a zero budget another way to practise before deciding whether a paid plan is worth it.</p>
<p>Two caveats. First, we have not yet worked through the new labs ourselves, so treat this as news rather than a review. Second, Alison's certificates are its own CPD-accredited credentials, not university certificates; if you need a credential employers widely recognise, compare the options in our <a href="../compare/best-online-course-platforms-for-certificates.html">certificates guide</a>.</p>
<h2>Where to go next</h2>
<ul><li><a href="../reviews/alison.html">Alison review</a>: how its free courses and paid certificates work</li>
<li><a href="../compare/best-platforms-to-learn-coding-and-tech.html">Best platforms to learn coding and tech</a></li>
<li><a href="../compare/codecademy-vs-datacamp.html">Codecademy vs DataCamp</a></li>
<li><a href="../compare/best-free-online-course-platforms.html">Best free online course platforms</a></li>
<li><a href="../subscription-calculator/index.html">Monthly vs annual calculator</a>, if you do go paid</li></ul>""",
 "sources":[("Alison press release: Alison Launches Interactive Coding Labs (Oct 15, 2026)","https://alison.com/press-room/company-news-&-announcements/alison-launches-interactive-coding-labs-that-let-learners-write-and-run-real-code-inside-the-courses"),
  ("Alison Blog: Learn Python by Doing, Not Just Watching","https://alison.com/blog/learn-python-not-just-watching"),
  ("Alison: Python coding courses","https://alison.com/tag/python-coding"),
  ("Codecademy pricing","https://www.codecademy.com/pricing")]},
]
for n in NEWS:
    src='<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{H.escape(u)}" rel="nofollow noopener">{H.escape(t)}</a></li>' for t,u in n["sources"])+'</ul>'
    body=f'<p><a href="index.html">News</a></p><article><h1>{n["title"]}</h1><p><small>By the {BRAND} editors · Published <time datetime="{n["date"]}">{n["nice"]}</time></small></p>{n["body"]}{src}<p class="src">Written by {BRAND} from the sources above. No sponsorship or payment from any company mentioned. Spotted an error? <a href="../contact.html">Tell us</a>.</p></article>'
    url=f'{BASE}/news/{n["slug"]}.html'
    ld={"@context":"https://schema.org","@type":"NewsArticle","headline":n["title"],"description":n["desc"],"datePublished":n["date"],"dateModified":n["date"],"url":url,"mainEntityOfPage":url,"author":{"@type":"Organization","name":BRAND,"url":BASE},"publisher":{"@type":"Organization","name":"Joshua Israel Ventures LLC","logo":{"@type":"ImageObject","url":f"{BASE}/logo.svg"}}}
    page(f'news/{n["slug"]}.html',n["title"],n["desc"],body,ld)
    LASTMOD[url]=n["date"]
li="".join(f'<li><a href="{n["slug"]}.html">{n["title"]}</a> <small>({n["nice"]})</small></li>' for n in NEWS)
page("news/index.html","Online Learning News","Short, sourced news on online course platforms: launches, price changes and what they mean for learners.",f"<h1>Online learning news</h1><p>Short, sourced updates on course platforms, written in our own words with links to the original announcements. We only post when something genuinely matters to learners.</p><ul>{li}</ul>")
LASTMOD[f"{BASE}/news/"]=NEWS[0]["date"]
LASTMOD[f"{BASE}/reviews/alison.html"]="2026-10-16"
LASTMOD[f"{BASE}/"]="2026-10-16"
