# CourseGauge SEO log

## 2026-10-16 (daily SEO routine)
**Data reviewed:** site went live on HTTPS on Oct 15; GSC and Bing were set up last night, so there is no search data yet. Live checks: /, sitemap.xml, pricing tracker, reviews and comparisons all return 200; www redirects 301 to the apex; robots.txt allows all crawlers. (Plain http:// could not be tested from the box because outbound port 80 is blocked for every site, not just ours.)

**Price check:** `update_prices.py` flagged Coursera, Codecademy, Brilliant and Domestika as "changed", but the pages were served in GBP because the box IP geolocated to the UK today; the GBP price structures match the USD figures, so these were false positives. Baseline NOT re-saved. Fixed the script to report this as REGION instead of CHANGED. 403 (unchecked) sources unchanged from before: MasterClass, Skillshare, Udemy, edX, Udacity, FutureLearn. Babbel page returned no prices to the script (JS-rendered); verify by hand at the next browser check.

**Highest-value action: built a new linkable asset, /subscription-calculator/** (the "next asset" in BACKLINK-PLAN.md). Why: a brand-new site has no rankings to compound yet, so the best long-run lever is a citable, original resource to lead outreach with. The page has an in-browser calculator (pick a plan or enter any prices, enter months of use, get the cheaper option and savings), a static break-even table for 11 plans (Coursera Plus, Codecademy Plus/Pro, DataCamp Premium, Brilliant Individual/Family, Pluralsight Core Tech/Complete, Babbel, Rosetta Stone, Domestika Plus) using the Oct 15 verified official prices, original findings (annual pays off from 5 to 9 months, median 7; 29% to 60% saving over a year), refund and renewal caveats, method, CSV download (CC BY 4.0), WebApplication JSON-LD. Promotional prices labelled (DataCamp special, Domestika first year).

**Internal links:** calculator added to the top nav, home page and every review page; News added to nav.

**News post:** "Alison adds free in-browser Python coding labs" at /news/alison-free-interactive-python-coding-labs.html (new /news/ section, NewsArticle JSON-LD, visible date). Sources: Alison press release (Oct 15, 2026), Alison blog post, Alison Python course page (fetched, confirms free interactive courses), Codecademy pricing. Own words, no images, says we haven't tested the labs. Linked from the Alison review ("Latest news") and to coding, free and certificate guides.

**Technical:** sitemap lastmod is now per page (LASTMOD in build.py) and only bumped for pages that really changed (home, Alison review, calculator, news). 49 URLs. All pages index,follow; LLC footer and West Bloomfield address present.

**Next:** use the calculator as the lead asset in outreach (personal-finance and student-money targets); when GSC data appears, review queries and compound on any page with impressions.
