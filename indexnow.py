import json,re,urllib.request
key=open(".indexnow-key").read().strip()
urls=re.findall(r"<loc>(.*?)</loc>",open("sitemap.xml").read())
base="https://coursegauge.com"
host=re.sub(r"https?://([^/]+).*",r"\1",base)
data=json.dumps({"host":host,"key":key,"keyLocation":f"{base}/{key}.txt","urlList":urls}).encode()
r=urllib.request.Request("https://api.indexnow.org/indexnow",data=data,headers={"Content-Type":"application/json; charset=utf-8"})
try: print(urllib.request.urlopen(r,timeout=30).status)
except Exception as e: print("error",getattr(e,"code",e), getattr(e,"read",lambda:b"")()[:300])
