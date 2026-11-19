# for every fixed (verified) span: alignment cost of the claimed word vs the best dictionary alternatives; flag spans where an alternative is clearly cheaper
import sys, json, numpy as np, multiprocessing as mp
import boot, align as al, rank as rk
FS=json.load(open('fixed_spans.json'))
freq=sorted(rk.words.items(),key=lambda kv:-kv[1])[:12000]; V=[w for w,_ in freq if w.isalpha()]
LP={}
def lp_for(page,li):
    k=(page,li)
    if k not in LP: LP[k]=rk.prep(page,li)
    return LP[k]
def work(job):
    page,li,i,j,w=job
    pcs=boot.lines_of(page)[li][i:j]; sl=LP[(page,li)][i:j]
    try: c0=al.align(pcs,sl,w.upper())[1]
    except Exception: return job,None,[]
    n=j-i; alts=[]
    for a in V:
        if a.upper()==w.upper() or len(a)>1.5*len(w)+1 or len(a)<0.65*len(w)-0.5 or len(a)>1.8*n+2 or len(a)<0.5*n-1: continue
        try: c=al.align(pcs,sl,a.upper())[1]
        except Exception: continue
        alts.append((c-0.25*rk.words[a],a))
    alts.sort(); c0adj=c0-0.25*rk.words.get(w.lower(),-6)
    return job,c0adj,alts[:3]
if __name__=='__main__':
    pages=sys.argv[1:]
    jobs=[]
    for page in pages:
        for li,sp in FS[page].items():
            li=int(li); lp_for(page,li)
            for i,j,w in sp:
                if w in ('I','A','AND','THE','OF','TO','MY','IN','ON','AT','IT','IS','BE','AS','ME','SO','NO','OR','AN','UP','IF','WE','HE','DO') or j-i<2: continue
                jobs.append((page,li,i,j,w))
    print(len(jobs),'spans',flush=True)
    with mp.get_context('fork').Pool(12) as pool: res=pool.map(work,jobs,chunksize=1)
    for job,c0,alts in res:
        if c0 is None: continue
        flag='  <<<' if alts and alts[0][0]<c0-2.5 else ''
        print(job[0],job[1],job[2],job[3],job[4],round(c0,1),[(round(a,1),b) for a,b in alts],flag,flush=True)
