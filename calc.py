# Monthly vs annual break-even calculator (linkable asset). Prices: data/pricing.json, checked Oct 15, 2026.
import math, statistics, html as H
SRC={r[0]:r[7] for r in P}
REF={r[0]:r[5] for r in P}
# key, plan, monthly price, first-year annual total, renewal annual total, how the annual price is shown, note
PLANS=[
("coursera","Coursera Plus",59,399,399,"$399/yr","Annual plan has a 14-day money-back guarantee."),
("codecademy","Codecademy Plus",29.99,179.88,179.88,"$14.99/mo billed annually",""),
("codecademy","Codecademy Pro",39.99,239.88,239.88,"$19.99/mo billed annually",""),
("datacamp","DataCamp Premium",35,168,168,"$14/mo billed annually (special price)","Annual figure is a special price; at the struck-out $28/mo ($336/yr) break-even would be 10 months."),
("brilliant","Brilliant Individual",30,240,240,"$20/mo billed annually",""),
("brilliant","Brilliant Family (up to 6)",60,480,480,"$40/mo billed annually",""),
("pluralsight","Pluralsight Core Tech",30,252,252,"$21/mo billed yearly","No refunds on individual subscriptions."),
("pluralsight","Pluralsight Complete",55,468,468,"$39/mo billed yearly","No refunds on individual subscriptions."),
("babbel","Babbel (1-month vs 12-month)",17.95,107.40,107.40,"$107.40/yr","Babbel also sells 3- and 6-month plans and a $299.99 lifetime plan."),
("rosetta-stone","Rosetta Stone",19.99,159,159,"$159/yr",""),
("domestika","Domestika Plus",33.90,164.50,329,"$164.50 first year, renews at $329","First-year price is an introductory offer; at the $329 renewal price break-even is 10 months."),
]
def be(m,a): return math.ceil(a/m-1e-9)
rows=[];bes=[];data=[]
for k,name,m,a,ren,shown,note in PLANS:
    b=be(m,a); bes.append(b); save=12*m-a; pct=round(100*save/(12*m))
    rows.append(f'<tr><th scope="row"><a href="../reviews/{k}.html">{name}</a></th><td>${m:,.2f}</td><td>${a:,.2f}<br><small>{H.escape(shown)}</small></td><td>${a/12:,.2f}</td><td><strong>{b} months</strong></td><td>${save:,.2f} ({pct}%)</td><td><a href="{SRC[k]}" rel="nofollow noopener">Official page</a>{"<br><small>"+H.escape(note)+"</small>" if note else ""}</td></tr>')
    data.append({"k":k,"n":name,"m":m,"a":a,"r":ren})
lo,hi,med=min(bes),max(bes),statistics.median(bes)
os.makedirs("subscription-calculator",exist_ok=True)
pcts=[round(100*(12*m-a)/(12*m)) for k,name,m,a,ren,shown,note in PLANS]
with open("subscription-calculator/coursegauge-annual-vs-monthly.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["Plan","Monthly price (USD)","Annual total first year (USD)","Annual renewal (USD)","Break-even months","12-month saving (USD)","Source","Prices checked"])
    for (k,name,m,a,ren,shown,note),b in zip(PLANS,bes): w.writerow([name,f"{m:.2f}",f"{a:.2f}",f"{ren:.2f}",b,f"{12*m-a:.2f}",SRC[k],"2026-10-15"])
opts="".join(f'<option value="{i}">{H.escape(d["n"])}</option>' for i,d in enumerate(data))+'<option value="custom">Another plan (enter prices)</option>'
js="""<script>
const D=%s;
const f=document.getElementById('calc'),o=document.getElementById('calcout'),c=document.getElementById('custom');
function money(x){return '$'+x.toFixed(2)}
function upd(){const sel=f.plan.value;c.hidden=sel!=='custom';let p;
if(sel==='custom'){const m=parseFloat(f.cm.value),a=parseFloat(f.ca.value);if(!(m>0&&a>0)){o.textContent='Enter a monthly price and an annual total to compare.';return}p={n:'This plan',m:m,a:a,r:a}}else p=D[+sel];
const n=Math.max(1,Math.min(36,parseInt(f.months.value)||1));
const monthly=p.m*n;const years=Math.ceil(n/12);const annual=p.a+(years-1)*p.r;const be=Math.ceil(p.a/p.m-1e-9);
const diff=Math.abs(monthly-annual);
let v=monthly<annual?`Pay monthly: it saves you ${money(diff)} over ${n} month${n>1?'s':''}.`:monthly>annual?`Choose annual: it saves you ${money(diff)} over ${n} month${n>1?'s':''}.`:'Both cost the same over this period.';
o.innerHTML=`<p><strong>${v}</strong></p><p>Monthly billing for ${n} month${n>1?'s':''}: ${money(monthly)}. Annual billing (${years} year${years>1?'s':''} paid up front): ${money(annual)}. For ${p.n}, annual costs the same or less once you use it for <strong>${be} months</strong> or more in a year.</p>`;}
f.addEventListener('input',upd);f.addEventListener('submit',e=>{e.preventDefault();upd()});upd();
</script>"""%json.dumps(data)
body=f"""<h1>Monthly or annual? Online course subscription break-even calculator</h1>
<p><strong>Short answer:</strong> on the {len(PLANS)} popular plans below, an annual subscription costs the same or less than paying monthly once you would use it for {lo} to {hi} months in a year (median {med:g} months). If you expect to study for less than about {lo} months, pay monthly and cancel; if you will learn most of the year, annual billing saves about {min(pcts)}% to {max(pcts)}% over a full year.</p>
<form id="calc"><fieldset><legend>Your plan</legend>
<label for="plan">Plan</label><br><select id="plan" name="plan">{opts}</select><br>
<div id="custom" hidden><label for="cm">Monthly price ($)</label> <input id="cm" name="cm" type="number" min="0" step="0.01" inputmode="decimal"> <label for="ca">Annual total ($)</label> <input id="ca" name="ca" type="number" min="0" step="0.01" inputmode="decimal"></div>
<label for="months">How many months will you actually use it?</label><br><input id="months" name="months" type="number" min="1" max="36" value="6" inputmode="numeric"></fieldset>
<p><button type="submit">Compare</button></p></form>
<div id="calcout" aria-live="polite"><noscript><p>The calculator needs JavaScript. The table below shows the break-even month for every plan.</p></noscript></div>
<div class="tw"><table><caption>Monthly vs annual billing on {len(PLANS)} online learning plans (US list prices, checked October 15, 2026)</caption>
<tr><th scope="col">Plan</th><th scope="col">Monthly</th><th scope="col">Annual (first year)</th><th scope="col">Annual, per month</th><th scope="col">Annual pays off from</th><th scope="col">Saving over 12 months</th><th scope="col">Source</th></tr>{"".join(rows)}</table></div>
<p><a href="coursegauge-annual-vs-monthly.csv" download>Download the data (CSV)</a> · Free to cite with a link to this page (CC BY 4.0).</p>
<h2>What the numbers show</h2>
<ul><li>The quickest payback is on discounted annual offers: DataCamp's special annual price and Domestika's first-year price both pay off within {min(be(35,168),be(33.90,164.50))} months, but both are promotional and Domestika renews at $329.</li>
<li>Codecademy and Babbel price annual billing at about half the monthly rate, so annual wins from 6 months of use.</li>
<li>Coursera Plus at $399 a year beats $59 a month from month 7.</li>
<li>Brilliant, Rosetta Stone and Pluralsight discount annual plans less (about 29% to 34% over a year), so you need 8 or 9 months of use before annual is the better deal.</li></ul>
<h2>Before you pay for a year up front</h2>
<ul><li><strong>Check the refund terms.</strong> Some annual plans are non-refundable once the trial ends (for example Pluralsight individual plans), while Coursera Plus annual has a 14-day money-back guarantee. See every policy in the <a href="../pricing-tracker/index.html">price and free-trial tracker</a>.</li>
<li><strong>Use the free trial to test your habit.</strong> If you are not using a trial most days, the monthly plan, or a free option, is probably the safer bet. Our <a href="../compare/best-free-online-course-platforms.html">guide to free course platforms</a> covers the no-cost alternatives.</li>
<li><strong>Watch renewal prices.</strong> Introductory annual prices can jump at renewal. Set a reminder a week before the renewal date.</li>
<li><strong>Prices vary.</strong> These are US list prices. Taxes, app-store billing and regional pricing change the totals, so confirm on the official page before buying.</li></ul>
<h2>Method</h2><p>Monthly price and annual total come from each platform's official pricing page on October 15, 2026 (the same figures as our <a href="../pricing-tracker/index.html">price tracker</a>). Where a platform shows annual billing as a per-month figure, we multiplied it by 12. "Annual pays off from" is the smallest whole number of months for which paying monthly costs at least as much as one year of annual billing. Platforms that only sell annual memberships (such as MasterClass) or whose US prices we could not confirm are left out rather than estimated. The calculator runs entirely in your browser and stores nothing.</p>
<p>Related: <a href="../compare/codecademy-vs-datacamp.html">Codecademy vs DataCamp</a> · <a href="../compare/coursera-vs-udemy.html">Coursera vs Udemy</a> · <a href="../compare/best-language-learning-apps.html">Best language learning apps</a> · <a href="../quiz/index.html">Platform quiz</a></p>
{js}"""
app={"@context":"https://schema.org","@type":"WebApplication","name":"CourseGauge monthly vs annual course subscription calculator","url":f"{BASE}/subscription-calculator/","applicationCategory":"FinanceApplication","operatingSystem":"Any","isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"creator":{"@type":"Organization","name":"CourseGauge"},"dateModified":"2026-10-18"}
CALC_FAQ=[
("Is an annual online course subscription worth it?",f"Only if you will keep learning most of the year. On the {len(PLANS)} plans we compared, annual billing costs the same or less than monthly once you use it for {lo} to {hi} months in a year (median {med:g} months). Below that, paying monthly and cancelling is cheaper."),
("How do I work out the break-even month myself?",f"Divide the annual price by the monthly price and round up. For Coursera Plus, $399 a year divided by $59 a month is about 6.8, so annual is cheaper from month {be(59,399)}."),
("Can I get a refund on an annual plan?",'It depends on the platform. Coursera Plus annual has a 14-day money-back guarantee, while Pluralsight individual plans are not refundable. Check every policy in our <a href="../pricing-tracker/">price and free-trial tracker</a> before paying for a year.'),
("Do introductory annual prices last?",f"Not always. Domestika Plus costs $164.50 in the first year but renews at $329, which moves break-even from {be(33.90,164.50)} months to {be(33.90,329)}. DataCamp's annual figure is also a special price, so check the renewal price before you buy."),
]
page("subscription-calculator/index.html","Monthly vs Annual Course Subscription Calculator",f"When does an annual course plan pay off? Break-even months ({lo} to {hi}) for Coursera Plus, Codecademy, DataCamp, Brilliant and more, with a free calculator.",body,app,crumbs=[("Calculator",None)],faq=CALC_FAQ)
LASTMOD[f"{BASE}/subscription-calculator/"]="2026-10-18"  # Oct 18: FAQ section added
