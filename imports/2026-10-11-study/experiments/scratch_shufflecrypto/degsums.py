# Exact reciprocal-degree sums C_u(m) = sum_{lambda |- m} (f^lambda)^{-u} for small m (sup over m),
# plus leading terms of Z_s(n) = sum_{lambda != (n),(1^n)} D^{-s} for huge n.
import math
from fractions import Fraction
def partitions(n, maxpart=None):
    if maxpart is None: maxpart=n
    if n==0: yield (); return
    for k in range(min(n,maxpart),0,-1):
        for rest in partitions(n-k,k): yield (k,)+rest
def dim(lam):
    n=sum(lam); conj=[sum(1 for r in lam if r>j) for j in range(lam[0])]
    h=1
    for i,r in enumerate(lam):
        for j in range(r): h*= (r-j-1)+(conj[j]-i-1)+1
    return math.factorial(n)//h
for u in (1,2):
    best=(0,None)
    for m in range(1,41):
        s=sum(Fraction(1,dim(l)**u) for l in partitions(m))
        if s>best[0]: best=(s,m)
    print(f"C_{u} = sup_m sum D^-{u}: {float(best[0]):.6f} at m={best[1]}")
# sums at moderately large m to show -> 2
for m in (40,):
    print("m=40: sum 1/D =", float(sum(Fraction(1,dim(l)) for l in partitions(m))))
