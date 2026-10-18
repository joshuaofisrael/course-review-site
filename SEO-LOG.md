# CourseGauge SEO log

## 2026-10-16 (daily SEO routine)
**Data reviewed:** site went live on HTTPS on Oct 15; GSC and Bing were set up last night, so there is no search data yet. Live checks: /, sitemap.xml, pricing tracker, reviews and comparisons all return 200; www redirects 301 to the apex; robots.txt allows all crawlers. (Plain http:// could not be tested from the box because outbound port 80 is blocked for every site, not just ours.)

**Price check:** `update_prices.py` flagged Coursera, Codecademy, Brilliant and Domestika as "changed", but the pages were served in GBP because the box IP geolocated to the UK today; the GBP price structures match the USD figures, so these were false positives. Baseline NOT re-saved. Fixed the script to report this as REGION instead of CHANGED. 403 (unchecked) sources unchanged from before: MasterClass, Skillshare, Udemy, edX, Udacity, FutureLearn. Babbel page returned no prices to the script (JS-rendered); verify by hand at the next browser check.

**Highest-value action: built a new linkable asset, /subscription-calculator/** (the "next asset" in BACKLINK-PLAN.md). Why: a brand-new site has no rankings to compound yet, so the best long-run lever is a citable, original resource to lead outreach with. The page has an in-browser calculator (pick a plan or enter any prices, enter months of use, get the cheaper option and savings), a static break-even table for 11 plans (Coursera Plus, Codecademy Plus/Pro, DataCamp Premium, Brilliant Individual/Family, Pluralsight Core Tech/Complete, Babbel, Rosetta Stone, Domestika Plus) using the Oct 15 verified official prices, original findings (annual pays off from 5 to 9 months, median 7; 29% to 60% saving over a year), refund and renewal caveats, method, CSV download (CC BY 4.0), WebApplication JSON-LD. Promotional prices labelled (DataCamp special, Domestika first year).

**Internal links:** calculator added to the top nav, home page and every review page; News added to nav.

**News post:** "Alison adds free in-browser Python coding labs" at /news/alison-free-interactive-python-coding-labs.html (new /news/ section, NewsArticle JSON-LD, visible date). Sources: Alison press release (Oct 15, 2026), Alison blog post, Alison Python course page (fetched, confirms free interactive courses), Codecademy pricing. Own words, no images, says we haven't tested the labs. Linked from the Alison review ("Latest news") and to coding, free and certificate guides.

**Technical:** sitemap lastmod is now per page (LASTMOD in build.py) and only bumped for pages that really changed (home, Alison review, calculator, news). 49 URLs. All pages index,follow; LLC footer and West Bloomfield address present.

**Deploy:** pushed 5e180c8; calculator and news pages live (200), live sitemap 49 URLs; IndexNow returned 200.

**Next:** use the calculator as the lead asset in outreach (personal-finance and student-money targets); when GSC data appears, review queries and compound on any page with impressions.

## 2026-10-18 (daily SEO routine, first run under the 18 Oct SEO max directive)
**Data reviewed:** no search or analytics data is available to check without the browser (GSC and Bing were set up on Oct 15 and the Cloudflare beacon went live on Oct 16, so little or no data is expected yet). Ran a new site-wide audit of all 49 built pages instead. Baseline (`reports/audit-2026-10-18-before.txt`): **946 issues across 16 checks**. 441 internal links pointed at non-canonical `.../index.html` URLs. All 49 pages were missing Open Graph/Twitter tags and top-level Organization + WebSite JSON-LD, and 36 reviews/comparisons/news pages had no BreadcrumbList. There were 10 meta descriptions under 70 characters and 2 over 160, 1 title over 65 characters, 7 pages with fewer than 3 contextual links out, and weak inbound links to the hubs (reviews/compare index pages had 0 contextual inbound, about had 0, news index had 1). There were no broken links, no noindex, every page had the LLC footer and West Bloomfield address plus the beacon, and the sitemap was complete.

**Highest-value action: technical/structured-data and internal-link fixes across the whole site.** Why: on a three-day-old site with no rankings yet, the best way to compound is fixing every page at once. That means clean canonical signals, an entity graph, rich-result eligibility, a share preview and stronger hub linking. Doing this before outreach and news add more pages beats writing new content.

**What changed (all in the generators, not hand-edited output):**
- `audit.py` (new, stdlib): runs every check in the directive checklist and writes reports to `reports/`.
- `page()` now emits one JSON-LD `@graph`: Organization (LLC, West Bloomfield address, logo), WebSite, WebPage, BreadcrumbList on reviews, comparisons, news, hubs, tools and legal pages, plus FAQPage only where a visible FAQ is rendered. WebSite has no SearchAction because the site has no search, so the markup would be false. There is no ratings markup; the existing Review schema stays rating-free, with publisher and the reviewed platform's URL added.
- Open Graph + Twitter `summary_large_image` tags on every page, plus an original 1200x630 share image (`og-image.png`, drawn by `make_og.py`).
- Visible breadcrumbs. All internal links rewritten to canonical directory URLs (`reviews/` rather than `reviews/index.html`).
- Real visible FAQs with FAQPage markup on `/subscription-calculator/` (4 Qs, computed from the page's own data) and `/pricing-tracker/` (4 Qs from the Oct 15 verified figures: free platforms, trials, refunds, monthly vs annual).
- About page: new "Our method in practice" section (E-E-A-T: official sources, re-check script, open CSV data, honesty about untested features, no paid placement). Every review and comparison now links to it ("How we research and check facts").
- Home page: "Latest news" block. Reviews, comparisons and news hubs get intro text with contextual links. Legal pages get a "Start here" links line.
- Meta descriptions: review descriptions now use each platform's tagline (unique, 117 to 148 characters). Rewrote the hub, legal and 3 short comparison descriptions. Calculator title trimmed to 62 characters and its description to 160 or less, and the Alison news description to 160 or less.
- `llms.txt` rebuilt with sections (tools and data with CSV links and the calculator's key finding, comparisons, reviews, news, about/policies) and a one-line factual summary per page. `robots.txt` unchanged: it already allows every crawler, including GPTBot, ClaudeBot, CCBot, Google-Extended, Bytespider and PerplexityBot, and lists the sitemap.

**Audit after:** 0 issues across 49 pages (`reports/audit-2026-10-18-after.txt`). Legal pages are exempt from the 3-contextual-inbound rule because the site-wide footer links them.

**Sitemap lastmod:** bumped only for pages whose visible content changed: home, about, pricing tracker, calculator and news index (2026-10-18). Everything else got only head/markup or breadcrumb changes, so it keeps its earlier dates.

**News post:** no relevant news. I searched Oct 15 to 18 for MasterClass, Coursera, Udemy, Skillshare, edX, Codecademy, DataCamp, LinkedIn Learning, Duolingo and Alison. The newest items were Alison's coding labs (already covered on Oct 16), MasterClass's Oct 6 to 8 class and podcast launches, Coursera/Udemy's Oct 6 program announcement and DataCamp's Oct 13 UAE schools partnership. All were either too old or not useful to course shoppers.

**Deploy:** pushed 0e0e833. Live checks all returned 200: /, calculator (FAQ present), tracker, about, news, a review, a comparison, llms.txt, og-image.png, sitemap.xml and robots.txt. og:image is live. IndexNow returned 200.

**Next:** visible FAQs on the top comparison pages (Coursera vs Udemy, best free platforms, certificates), but only real Q&A. Compress or lazy-load check is not needed yet (there are no raster images in page bodies), but run a PageSpeed/CWV spot check when the browser slot allows. Review GSC/Bing and Cloudflare data at the next browser slot. Keep the calculator as the lead outreach asset.
