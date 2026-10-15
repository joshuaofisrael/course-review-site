# course-review-site (working brand: CourseGauge)

Static online course review site for Joshua Israel Ventures LLC. Plain HTML/CSS, no JS, no build dependencies.

- Edit content in `data/reviews.json`, `data/compare.json`, `data/legal/*.html.txt`
- Regenerate: `python3 build.py` (stdlib only, runs in under a second)
- Output: `index.html`, `reviews/`, `compare/`, legal pages, `sitemap.xml`, `robots.txt`, `llms.txt`
- `BASE` in `build.py` must be updated when a custom domain is attached.

## Intellectual property
All writing, structure, design, the "CourseGauge" name and the SVG logo are original work of Joshua Israel Ventures LLC. Reviews are based on platforms' own public pricing/help pages, cited on every page; no text is copied or paraphrased from competitor review sites. Course platform names are used only descriptively (nominative fair use) and never in our brand or domain. No third-party images are used; any future image must be original or properly licensed (CC0 or credited open licence). Name check (Oct 15, 2026): see BRAND-CHECK.md.

## IndexNow
Key file: `2e39508c439447c8b3541321bc9f2792.txt` (key also in `.indexnow-key`). After each deploy, run `python3 indexnow.py` to submit every URL in the sitemap.

## Price tracker and quiz
- `/pricing-tracker/`: built from `data/pricing.json` (columns: monthly, annual, trial, free tier, refund, certificate, source). Use "SEE" for any figure not verified on an official page; it renders as "see official pricing" with a link. The CSV is generated alongside.
- Daily: `python3 update_prices.py` flags changed prices or trial lengths against `data/price-snapshots.json`, plus any sources that block bots (403). Verify by hand, edit `data/pricing.json`, update the check date in `extras.py`, run `python3 build.py`, then `python3 update_prices.py --save` and `python3 indexnow.py`.
- `/quiz/`: vanilla JS, no storage or trackers, with a noscript fallback. Logic is in `extras.py`.
