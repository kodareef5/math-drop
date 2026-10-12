import sys, random
sys.path.insert(0,'.')
from artin_wp import *
def freered(w):
    out=[]
    for g in w:
        if out and out[-1][0]==g[0] and out[-1][1]==-g[1]: out.pop()
        else: out.append(g)
    return out
def tdiag(p,q,r):
    edges={}; c=0; nxt=1
    for L in (p-1,q-1,r-1):
        prev=c
        for _ in range(L):
            edges[(prev,nxt)]=3; prev=nxt; nxt+=1
    verts=list(range(nxt)); cox={}
    for i in verts:
        for j in verts:
            if i<j: cox[(i,j)]=edges.get((i,j),edges.get((j,i),2))
    return cox
from sage.all import ArtinGroup, CoxeterMatrix, identity_matrix
rng=random.Random(21)
cox=tdiag(2,3,7); Z,verts=build(cox)
cm=[[1 if i==j else cox[(min(i,j),max(i,j))] for j in verts] for i in verts]
A=ArtinGroup(CoxeterMatrix(cm)); G=A.gens()
agree=0; n=0; burau_triv=0
for L in (4,8,12):
    for _ in range(10):
        w=freered([(rng.choice(verts),rng.choice([1,-1])) for _ in range(L)])
        if not w: continue
        el=A.one()
        for g,e in w: el=el*G[verts.index(g)]**e
        bm=el.burau_matrix(); triv=(bm==identity_matrix(bm.base_ring(),bm.nrows()))
        mine=is_member(Z,w); n+=1; burau_triv+=triv
        agree+= (mine==triv) if not triv else 1
print(f"E10 random words: prototype verdict consistent with generalized Burau on {agree}/{n} (Burau trivial on {burau_triv})")
