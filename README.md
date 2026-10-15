# course-review-site (working brand: Studyvane)

Static online course review site for Joshua Israel Ventures LLC. Plain HTML/CSS, no JS, no build dependencies.

- Edit content in `data/reviews.json`, `data/compare.json`, `data/legal/*.html.txt`
- Regenerate: `python3 build.py` (stdlib only, runs in under a second)
- Output: `index.html`, `reviews/`, `compare/`, legal pages, `sitemap.xml`, `robots.txt`, `llms.txt`
- `BASE` in `build.py` must be updated when a custom domain is attached.

## Intellectual property
All writing, structure, design, the "Studyvane" name and the SVG logo are original work of Joshua Israel Ventures LLC. Reviews are based on platforms' own public pricing/help pages, cited on every page; no text is copied or paraphrased from competitor review sites. Course platform names are used only descriptively (nominative fair use) and never in our brand or domain. No third-party images are used; any future image must be original or properly licensed (CC0 or credited open licence). The brand name has not yet had a trademark clearance check.
