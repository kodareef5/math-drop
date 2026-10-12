# Empirical check of tensor saturation (factor 1) for D_n, and control for B_n.
# For dominant lam, mu and N=2: every nu with c_{2lam,2mu}^{2nu}>0 and lam+mu-nu in root lattice
# must have c_{lam,mu}^{nu}>0.  Uses Sage's Brauer-Klimyk WeylCharacterRing products.
import sys, time, itertools
from fractions import Fraction as Fr
from sage.all import WeylCharacterRing, QQ
def dominant(ct, n, maxc):
    out=[]
    for half in (0,1):
        rng=[Fr(2*k+half,2) for k in range(-2*int(maxc)-3,2*int(maxc)+3) if abs(Fr(2*k+half,2))<=maxc]
        rng=sorted(set(rng))
        for v in itertools.product(rng, repeat=n):
            if ct=='D':
                if all(v[i]>=v[i+1] for i in range(n-2)) and v[n-2]>=abs(v[n-1]): out.append(v)
            else:
                if all(v[i]>=v[i+1] for i in range(n-1)) and v[n-1]>=0: out.append(v)
    return out
def in_root_lattice(ct, x):
    if any(Fr(c).denominator!=1 for c in x): return False
    if ct=='D': return sum(x)%2==0
    return True  # B_n root lattice = Z^n
def run(ct, n, maxc, N=2, tlimit=600):
    W=WeylCharacterRing([ct,n])
    doms=dominant(ct,n,maxc)
    pairs=[(a,b) for i,a in enumerate(doms) for b in doms[i:] if any(a) and any(b)]
    t0=time.time(); checked=0; fails=[]; npairs=0
    for a,b in pairs:
        if time.time()-t0>tlimit: break
        P1=(W(*[QQ(x) for x in a])*W(*[QQ(x) for x in b])).monomial_coefficients()
        P2=(W(*[QQ(N*x) for x in a])*W(*[QQ(N*x) for x in b])).monomial_coefficients()
        S1=set(tuple(Fr(str(c)) for c in k.to_vector()) for k in P1)
        npairs+=1
        for k in P2:
            nu2=[Fr(str(c)) for c in k.to_vector()]
            nu=tuple(c/N for c in nu2)
            # nu must be an integral weight: all int or all half-int
            dens=set((2*c).denominator for c in nu)
            if dens!={1}: continue
            if len(set(c.denominator for c in nu))>1: continue
            diff=[a[i]+b[i]-nu[i] for i in range(n)]
            if not in_root_lattice(ct,diff): continue
            checked+=1
            if nu not in S1: fails.append((a,b,nu))
    return dict(type=f"{ct}{n}",maxc=maxc,N=N,pairs=npairs,of=len(pairs),triples_checked=checked,failures=len(fails),examples=fails[:3],secs=round(time.time()-t0,1))
if __name__=='__main__':
    ct=sys.argv[1]; n=int(sys.argv[2]); maxc=float(sys.argv[3]); N=int(sys.argv[4]) if len(sys.argv)>4 else 2
    tl=int(sys.argv[5]) if len(sys.argv)>5 else 600
    print(run(ct,n,Fr(maxc).limit_denominator(2),N,tl), flush=True)
