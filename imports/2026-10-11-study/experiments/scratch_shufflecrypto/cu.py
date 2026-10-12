# C_u = sup_m sum_{lambda |- m} D_lambda^{-u}; report sup over m<=45 and argmax, to check where sup is attained
import math, json
def partitions(n, maxpart=None):
    if maxpart is None: maxpart=n
    if n==0: yield (); return
    for k in range(min(n,maxpart),0,-1):
        for rest in partitions(n-k,k): yield (k,)+rest
def logdim(lam):
    n=sum(lam); conj=[sum(1 for r in lam if r>j) for j in range(lam[0])]
    lh=0.0
    for i,r in enumerate(lam):
        for j in range(r): lh+=math.log((r-j-1)+(conj[j]-i-1)+1)
    return math.lgamma(n+1)-lh
logs={m:[logdim(l) for l in partitions(m)] for m in range(1,46)}
out={}
for u in [0.25,0.5,0.75,1,1.5,2,3,4,6]:
    vals={m:sum(math.exp(-u*x) for x in logs[m]) for m in logs}
    mbest=max(vals,key=vals.get)
    out[u]=(vals[mbest],mbest,vals[45])
    print(f"u={u}: sup_(m<=45) = {vals[mbest]:.4f} at m={mbest}; value at m=45: {vals[45]:.4f}")
json.dump({str(k):v for k,v in out.items()},open('cu.json','w'))
