import csv,html as H
P=json.load(open("data/pricing.json"))
COLS=["Monthly","Annual","Free trial","Free tier","Refund / money-back","Certificate"]
SEE="see official pricing"
os.makedirs("pricing-tracker",exist_ok=True)
with open("pricing-tracker/coursegauge-pricing-tracker.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["Platform"]+COLS+["Source","Last checked"])
    for row in P: w.writerow([R[row[0]]["name"]]+[SEE if x=="SEE" else x for x in row[1:7]]+[row[7],"2026-10-15"])
def cell(x,src): return f'<a href="{src}" rel="nofollow noopener">{SEE}</a>' if x=="SEE" else H.escape(x)
rows="".join(f'<tr><th scope="row"><a href="../reviews/{r[0]}.html">{R[r[0]]["name"]}</a></th>'+"".join(f"<td>{cell(x,r[7])}</td>" for x in r[1:7])+f'<td><a href="{r[7]}" rel="nofollow noopener">Source</a><br><small>Checked 2026-10-15</small></td></tr>' for r in P)
body=f"""<h1>Online course platform price and free-trial tracker</h1>
<p><strong>Short answer:</strong> the cheapest ways to learn are fully free options (Khan Academy, Alison, edX audit, Duolingo's free tier). Among paid subscriptions, annual billing is almost always cheaper per month than monthly billing. Watch renewal prices and refund windows. Prices below are US list prices taken from each platform's official pages.</p>
<p><a href="coursegauge-pricing-tracker.csv" download>Download the data (CSV)</a> · Free to cite with a link to this page.</p>
<div class="tw"><table><caption>Plan prices, trials, free tiers, refunds and certificates for 20 platforms (US, checked October 15, 2026)</caption><tr><th scope="col">Platform</th>{"".join(f'<th scope="col">{c}</th>' for c in COLS)}<th scope="col">Source</th></tr>{rows}</table></div>
<h2>Method</h2><p>Each figure was read on the platform's own pricing page, plan page or help centre on the date shown. Where we could not confirm a figure on an official page, we show "see official pricing" with a link instead of estimating. Promotional prices are labelled. Prices vary by region, taxes and app-store billing. A script re-fetches every source and flags changes for us to review, so we re-check pages whenever they change.</p>
<p>Found an outdated figure? <a href="../contact.html">Tell us</a>.</p>"""
ds={"@context":"https://schema.org","@type":"Dataset","name":"CourseGauge online course platform price and free-trial tracker","description":"US list prices, free trials, free tiers, refund policies and certificate availability for 20 online learning platforms, each with an official source link.","url":f"{BASE}/pricing-tracker/","dateModified":"2026-10-15","license":"https://creativecommons.org/licenses/by/4.0/","creator":{"@type":"Organization","name":"Joshua Israel Ventures LLC"},"isAccessibleForFree":True,"distribution":[{"@type":"DataDownload","encodingFormat":"text/csv","contentUrl":f"{BASE}/pricing-tracker/coursegauge-pricing-tracker.csv"}]}
page("pricing-tracker/index.html","Online Course Price and Free-Trial Tracker 2026","Current prices, free trials, refund policies and certificates for 20 online course platforms, each with an official source and check date.",body,ds)
Q=[("goal","What's your main goal?",[("career","Change or grow my career"),("hobby","Creative hobby or personal interest"),("school","School subjects or fundamentals"),("language","Learn a language"),("curious","Be inspired and learn broadly")]),
("budget","What's your budget?",[("free","Free only"),("low","Low, a few dollars a month"),("any","I'll pay for the right fit")]),
("format","How do you like to learn?",[("video","Watching video lessons"),("hands","Hands-on practice and projects"),("structured","Structured courses with graded work")]),
("cert","Do you need a certificate?",[("yes","Yes, one employers recognise"),("nice","Nice to have"),("no","No")]),
("subject","Which subject?",[("tech","Coding, data or IT"),("business","Business and soft skills"),("creative","Art, design or crafts"),("academic","Maths, science or humanities"),("lang","Languages")])]
qs="".join(f'<fieldset><legend>{i+1}. {t}</legend>'+"".join(f'<label><input type="radio" name="{k}" value="{v}" required> {l}</label><br>' for v,l in o)+'</fieldset>' for i,(k,t,o) in enumerate(Q))
names={k:v["name"] for k,v in R.items()}
quizjs="""<script>
const N=%s;
const S={
coursera:{goal:{career:3},cert:{yes:4,nice:1},format:{structured:3},subject:{business:2,tech:1,academic:1},budget:{any:1,low:1},why:"university and industry certificates with graded work"},
edx:{goal:{career:1,school:1},budget:{free:2,low:1},cert:{yes:2},format:{structured:2},subject:{academic:2},why:"free audit track with an optional paid verified certificate"},
udemy:{goal:{career:2},budget:{low:2},format:{video:2},cert:{no:1,nice:1},subject:{tech:2,business:1},why:"buy a single practical course and keep it"},
skillshare:{goal:{hobby:3},format:{hands:2,video:1},subject:{creative:3},cert:{no:1},why:"short project-based creative classes"},
domestika:{goal:{hobby:2},format:{hands:1,video:1},subject:{creative:3},why:"in-depth creative courses you can own"},
masterclass:{goal:{curious:4},format:{video:3},cert:{no:2},budget:{any:1},why:"polished lessons from famous practitioners"},
"great-courses-plus":{goal:{curious:3},format:{video:2},subject:{academic:2},cert:{no:1},why:"long-form lectures on history, science and more"},
codecademy:{goal:{career:2},format:{hands:3},subject:{tech:3},budget:{free:1,low:1},why:"interactive coding with a free Basic tier"},
datacamp:{goal:{career:2},format:{hands:2},subject:{tech:3},cert:{nice:1},why:"hands-on data and AI skills"},
pluralsight:{goal:{career:2},subject:{tech:3},cert:{yes:1},budget:{any:1},why:"tech skills, labs and certification prep"},
"linkedin-learning":{goal:{career:2},subject:{business:3},format:{video:1},cert:{nice:1},why:"business and software skills bundled with Premium"},
"khan-academy":{goal:{school:4},budget:{free:4},subject:{academic:3},cert:{no:1},why:"completely free, nonprofit fundamentals"},
brilliant:{goal:{school:2,curious:1},format:{hands:2},subject:{academic:2,tech:1},cert:{no:1},why:"interactive problem solving in maths and science"},
alison:{budget:{free:3},cert:{nice:2},goal:{career:1},why:"free courses with optional certificates"},
duolingo:{goal:{language:3},budget:{free:3,low:1},subject:{lang:3},why:"free daily language practice"},
babbel:{goal:{language:3},format:{structured:2},subject:{lang:3},budget:{low:1,any:1},why:"structured conversation-focused lessons"},
"rosetta-stone":{goal:{language:2},format:{hands:1},subject:{lang:2},budget:{any:1},why:"immersion-style learning across many languages"},
futurelearn:{goal:{career:1,school:1},format:{structured:2},cert:{nice:1,yes:1},subject:{academic:1,business:1},why:"short university courses"},
udacity:{goal:{career:2},subject:{tech:2},cert:{yes:1},budget:{any:2},format:{hands:2},why:"intensive project-based tech programs"}};
const PAID_ONLY=["masterclass","udacity","pluralsight","linkedin-learning","babbel","rosetta-stone","great-courses-plus","futurelearn","domestika","skillshare","datacamp","brilliant","coursera","udemy"];
document.getElementById('quiz').addEventListener('submit',e=>{e.preventDefault();const f=new FormData(e.target);const a={};for(const[k,v]of f)a[k]=v;
const sc=Object.entries(S).map(([k,s])=>{let t=0;for(const q in a){t+=(s[q]&&s[q][a[q]])||0}if(a.budget==='free'&&PAID_ONLY.includes(k))t-=5;return[k,t]}).sort((x,y)=>y[1]-x[1]).filter(x=>x[1]>0).slice(0,3);
const out=document.getElementById('result');out.innerHTML='<h2>Your matches</h2>'+(sc.length?'<ol>'+sc.map(([k])=>`<li><a href="../reviews/${k}.html">${N[k]}</a>: ${S[k].why}.</li>`).join('')+'</ol>':'<p>No strong match. Browse <a href="../reviews/index.html">all reviews</a>.</p>')+'<p>Check current prices in the <a href="../pricing-tracker/index.html">price tracker</a>.</p>';out.focus();});
</script>"""%json.dumps(names)
nos='<noscript><h2>Quick guide without JavaScript</h2><ul><li>Career certificates: <a href="../reviews/coursera.html">Coursera</a>, <a href="../reviews/edx.html">edX</a></li><li>Free: <a href="../reviews/khan-academy.html">Khan Academy</a>, <a href="../reviews/alison.html">Alison</a></li><li>Creative hobbies: <a href="../reviews/skillshare.html">Skillshare</a>, <a href="../reviews/domestika.html">Domestika</a></li><li>Coding: <a href="../reviews/codecademy.html">Codecademy</a>, <a href="../reviews/datacamp.html">DataCamp</a></li><li>Languages: <a href="../reviews/duolingo.html">Duolingo</a>, <a href="../reviews/babbel.html">Babbel</a></li><li>Inspiration: <a href="../reviews/masterclass.html">MasterClass</a></li></ul></noscript>'
body=f"""<h1>Which online course platform fits you?</h1><p>Answer five questions to get one to three matches with reasons. Your answers stay in your browser: nothing is stored or sent.</p>
<form id="quiz">{qs}<p><button type="submit">Show my matches</button></p></form><div id="result" tabindex="-1" aria-live="polite"></div>{nos}{quizjs}
<p><small>Matches are our editorial judgement based on each platform's features as described in our reviews.</small></p>"""
page("quiz/index.html","Which Online Course Platform Fits You? Quiz","Five quick questions to match you with the online course platform that suits your goal, budget, format and need for a certificate.",body)
