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

import time, signal
class TO(Exception): pass
def hh(s,f): raise TO
signal.signal(signal.SIGALRM,hh)
for name,cox in [('E10=T(2,3,7)',tdiag(2,3,7)),('E9=T(2,3,6) affine',tdiag(2,3,6)),('E8=T(2,3,5) spherical',tdiag(2,3,5))]:
    Z,verts=build(cox)
    for k in range(1,9):
        w=[(v,1) for v in verts]*k
        st={}; t=time.time(); signal.alarm(60)
        try:
            is_member(Z,w,st); signal.alarm(0)
            print(f"{name} c^{k} (len {len(w)}): minimal complex size {st['final']}, peak {st['peak']}, {time.time()-t:.2f}s", flush=True)
        except TO:
            print(f"{name} c^{k}: timeout 60s", flush=True); break
