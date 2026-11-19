import json, re
s=open('template_v2.html').read()
P=json.load(open('report_pages.json')); A=json.load(open('report_alpha.json')); S=json.load(open('report_stats.json')); E=json.load(open('report_extra.json'))
def dump(o): return json.dumps(o,separators=(',',':'),ensure_ascii=False)
s=s.replace('/*DATA_PAGES*/',dump(P)).replace('/*DATA_ALPHA*/',dump(A)).replace('/*DATA_STATS*/',dump(S)).replace('/*DATA_EXTRA*/',dump(E)).replace('/*DATA_META*/','{}')
out='/Users/doranchak/projects/github/misc-crypto-mysteries/oliver-twist-thrift-store/report.html'
open(out,'w').write(s)
print(len(s)//1000,'KB')
