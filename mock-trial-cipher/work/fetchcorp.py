import json, urllib.request, urllib.parse, re, sys
titles=["Accounting","Embezzlement","Fraud","Bank","Money","Detective","Journal","Diary","Letter (message)","Cipher","Secret","Treasure","Trust (social science)","Business","Company","Office","Employee","Manager","Theft","Crime","Mystery","Story","Novel","Book","History of the United States","London","Paris","New York City","World War II","Science","Mathematics","Music","Art","Water","Food","Health","Computer","Internet","Weather","Family","Marriage","School","University","Law","Police","Court","Prison","Money laundering","Audit","Ledger","Financial statement","Bookkeeping","Cash","Safe","Key","Door","House","Night","Time","Memory"]
out=[]
for t in titles:
    url="https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",prop="extracts",explaintext=1,exlimit=1,titles=t,format="json",redirects=1))
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'cipher-research/1.0'})
        d=json.load(urllib.request.urlopen(req,timeout=20))
        for p in d['query']['pages'].values():
            out.append(p.get('extract',''))
    except Exception as e:
        print('fail',t,e,file=sys.stderr)
txt='\n'.join(out)
txt=re.sub(r'==+[^=]*==+',' ',txt)
open('corpus_raw.txt','w').write(txt)
print(len(txt))
