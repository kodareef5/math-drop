"""Exact kernel of the PATCHED networkx double_edge_swap(count_rejected=True), one counted attempt:
(ui,xi) iid degree-weighted, v,y uniform neighbours; ui==xi or v==y -> redraw (uncounted);
success -> {ux, vy}; failure -> hold.  Check: symmetric kernel, uniform stationary law."""
import json
from fractions import Fraction
import numpy as np
from enum_graphs import enumerate_graphs, pair_index
from kernels_as_implemented import adjsets, apply, stationary

def row(mask, n, pidx, d):
    A = adjsets(mask, n); D = sum(d); out = {}; tot = 0
    for u in range(n):
        for x in range(n):
            if u == x or d[u] == 0 or d[x] == 0: continue
            for v in A[u]:
                for y in A[x]:
                    if v == y: continue
                    p = Fraction(1, D * D); tot += p
                    g2 = apply(mask, pidx, [(u, v), (x, y)], [(u, x), (v, y)]) if (x not in A[u] and y not in A[v]) else mask
                    out[g2] = out.get(g2, 0) + p
    return {g: p / tot for g, p in out.items()}

for d in [(4,4,2,2,2,2),(3,3,3,3,3,3),(4,3,3,3,1,1,1),(6,3,2,2,2,2,2,1),(2,2,2,2,2,2,2)]:
    n=len(d); pidx=pair_index(n); gs=enumerate_graphs(d)
    pi, sym = stationary([row(g,n,pidx,d) for g in gs], gs)
    print(json.dumps(dict(d=list(d), N=len(gs), TV=round(float(0.5*abs(pi-1/len(gs)).sum()),12), kernel_symmetric=bool(sym<1e-12))))
