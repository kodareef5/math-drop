import sys, time, random, signal
sys.path.insert(0,'.')
from artin_wp import *
class TO(Exception): pass
def h(s,f): raise TO
signal.signal(signal.SIGALRM,h)
rng=random.Random(9)
def freered(w):
    out=[]
    for g in w:
        if out and out[-1][0]==g[0] and out[-1][1]==-g[1]: out.pop()
        else: out.append(g)
    return out
def tdiag(p,q,r):   # T_{p,q,r}: three arms of lengths p-1,q-1,r-1 from a centre, labels 3
    edges={}; c=0; nxt=1
    for L in (p-1,q-1,r-1):
        prev=c
        for _ in range(L):
            edges[(prev,nxt)]=3; prev=nxt; nxt+=1
    verts=list(range(nxt))
    cox={}
    for i in verts:
        for j in verts:
            if i<j: cox[(i,j)]=edges.get((i,j),edges.get((j,i),2))
    return cox
def rel_words(cox):
    R=[]
    for (i,j),m in cox.items():
        if m=='oo': continue
        a=([(i,1),(j,1)]*m)[:m]; b=([(j,1),(i,1)]*m)[:m]
        R.append(a+inv(b))
    return R
if __name__=="__main__":
    for name,cox in [('E10 = T(2,3,7) hyperbolic, rank 10',tdiag(2,3,7)),('T(3,3,4) hyperbolic, rank 8',tdiag(3,3,4))]:
        Z,verts=build(cox); R=rel_words(cox)
        okI=0; nI=0; okN=0; nN=0; mx=0; tmax=0
        for _ in range(30):
            w=[]
            for _ in range(2):
                c=[(rng.choice(verts),rng.choice([1,-1])) for _ in range(rng.randint(0,3))]
                r=rng.choice(R); r=r if rng.random()<.5 else inv(r)
                w=w+c+r+inv(c)
            w=freered(w)
            st={}; t=time.time(); signal.alarm(60)
            try:
                res=is_member(Z,w,st); signal.alarm(0); nI+=1; okI+=res; mx=max(mx,st['peak']); tmax=max(tmax,time.time()-t)
            except TO: pass
        for L in (6,10,14):
            for _ in range(5):
                w=freered([(rng.choice(verts),rng.choice([1,-1])) for _ in range(L)])
                st={}; t=time.time(); signal.alarm(60)
                try:
                    res=is_member(Z,w,st); signal.alarm(0); nN+=1; okN+=(not res); mx=max(mx,st['peak']); tmax=max(tmax,time.time()-t)
                except TO: pass
        print(f"{name}: identities recognised {okI}/{nI}; random words (len 6-14) declared nontrivial {okN}/{nN}; max peak complex {mx}; max time {tmax:.2f}s", flush=True)
    # CAT(0) counterexample Artin group on 116 generators (Def. def:matrix), labels in {2,3,oo}
    E=[('a','b'),('b','c'),('c','a')]
    S=['a','b','c','d','e']+[f"s{j}_{u}{v}" for (u,v) in E for j in range(3,40)]
    def blk(u,v): return [u,v]+[f"s{j}_{u}{v}" for j in range(3,40)]
    m={}
    for x in S:
        for y in S:
            if x<y: m[(x,y)]='oo'
    def setm(x,y,val):
        m[(min(x,y),max(x,y))]=val
    setm('a','b',3); setm('b','c',3); setm('c','a',3)
    for (u,v) in E:
        B=blk(u,v)
        for i in range(len(B)):
            for j in range(i+1,len(B)):
                setm(B[i],B[j],3 if j-i==1 else 2)
    for q in ('d','e'):
        for u in ('a','b','c'): setm(q,u,2)
    Z,verts=build(m)
    print("116-generator CAT(0)-counterexample group: |S| =",len(verts), flush=True)
    R=rel_words(m); ok=0; n=0; tm=0
    for _ in range(20):
        c=[(rng.choice(verts),rng.choice([1,-1])) for _ in range(3)]
        r=rng.choice(R); w=freered(c+r+inv(c)+[('d',1),('a',1),('d',-1),('a',-1)])
        t=time.time(); res=is_member(Z,w); tm=max(tm,time.time()-t); n+=1; ok+=res
    w=freered([('d',1),('e',1),('d',-1),('e',-1)])
    print(f"  conjugated relator * [d,a] recognised as identity: {ok}/{n} (max {tm:.2f}s);  [d,e] (m_de=oo) identity? {is_member(Z,w)}", flush=True)
