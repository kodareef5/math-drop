"""Quantify the 076 auxiliary polynomial p_j (spreading.tex eq. binary-recursion):
p_j = p_{j-1} + (1 - p_{j-1}^2)/2 * cos(2 pi y_j).  M_j = E[p_j^2] (Monte Carlo), |supp p_j| (exact, small j)."""
import numpy as np
from collections import defaultdict
rng=np.random.default_rng(1)
S=400000
p=np.zeros(S); Ms={}
for j in range(1,4001):
    y=rng.random(S)
    p=p+(1-p*p)/2*np.cos(2*np.pi*y)
    if j in (1,2,3,4,5,8,10,20,50,100,200,500,1000,2000,4000):
        Ms[j]=np.mean(p*p)
for j,m in Ms.items(): print(f"j={j:5d}  M_j={m:.5f}  1-M_j={1-m:.5f}  j*(1-M_j)={j*(1-m):.3f}")
# exact Fourier support sizes via dict polynomials
def mul(A,B):
    C=defaultdict(float)
    for a,ca in A.items():
        for b,cb in B.items():
            C[tuple(x+y for x,y in zip(a,b))]+=ca*cb
    return {k:v for k,v in C.items() if abs(v)>1e-15}
P={}  # p_0 = 0 in dimension 0
dim=0
for j in range(1,6):
    # lift P to dim j
    P={k+(0,):v for k,v in P.items()}
    sq=mul(P,P) if P else {}
    one_minus={ (0,)*j:1.0 }
    for k,v in sq.items(): one_minus[k]=one_minus.get(k,0)-v
    half={k:v/2 for k,v in one_minus.items() if abs(v)>1e-15}
    new=dict(P)
    for k,v in half.items():
        for s in (1,-1):
            kk=k[:-1]+(s,)
            new[kk]=new.get(kk,0)+v/2
    P={k:v for k,v in new.items() if abs(v)>1e-15}
    print(f"j={j}: |supp p_j|={len(P)}  M_j(exact)={sum(v*v for v in P.values()):.5f}")
