import sys, os, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        if t in('p','div','br','li','tr','h1','h2','h3','h4','blockquote'): s.out.append('\n')
        if t=='img':
            d=dict(a); s.out.append(f"[IMG {d.get('src','')}]")
        if t=='a':
            d=dict(a)
            if d.get('href'): s.out.append(f"[LINK {d.get('href')}] ")
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
        if t in('p','div','li','tr','blockquote'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
src=sys.argv[1]; dst=sys.argv[2]
os.makedirs(dst,exist_ok=True)
for f in sorted(os.listdir(src)):
    if f.endswith('.html'):
        p=P(); p.feed(open(os.path.join(src,f),encoding='utf-8',errors='replace').read())
        t=re.sub(r'\n\s*\n\s*\n+','\n\n',''.join(p.out))
        open(os.path.join(dst,f[:-5]+'.txt'),'w').write(t)
        print(len(t), f)
