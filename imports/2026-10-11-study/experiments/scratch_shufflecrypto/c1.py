# Compute reciprocal-degree sums sum_{lambda |- s} (f^lambda)^{-u} via hook-length formula
import math, sys
from functools import lru_cache
def partitions(n, maxpart=None):
    if maxpart is None: maxpart=n
    if n==0: yield (); return
    for k in range(min(n,maxpart),0,-1):
        for rest in partitions(n-k,k): yield (k,)+rest
def logdim(lam):
    n=sum(lam); conj=[sum(1 for r in lam if r>j) for j in range(lam[0])] if lam else []
    lh=0.0
    for i,r in enumerate(lam):
        for j in range(r):
            lh+=math.log(r-j-1 + conj[j]-i-1 + 1)
    return math.lgamma(n+1)-lh
best=(0,0)
for s in range(1,61):
    tot=sum(math.exp(-logdim(l)) for l in partitions(s))
    if tot>best[0]: best=(tot,s)
    if s<=14 or s%10==0: print(s, round(tot,6))
print("sup so far C1 =",best)
