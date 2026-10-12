# Family 200: check the char-0 LPP Betti inequality on random instances (sanity / regression data, not proof).
import random, itertools, time, sys
from sage.all import PolynomialRing, QQ, GF, ZZ
rng=random.Random(11)
def betti(I):
    F=I.graded_free_resolution()
    out={}
    for i in range(0,len(F)+2):
        try: b=F.betti(i)
        except Exception: break
        for deg,v in b.items():
            if v: out[(i,deg)]=v
    return out
def hilb(I,R,top):
    Q=R.quotient(I) if False else None
    hs=I.hilbert_series()
    t=hs.parent().gen()
    ps=hs.numerator()*0
    # expand series
    from sage.all import PowerSeriesRing
    S=PowerSeriesRing(QQ,'z',default_prec=top+1); z=S.gen()
    num=hs.numerator(); den=hs.denominator()
    ser=S(num(z))/S(den(z))
    return [int(ser[d]) for d in range(top+1)]
def lpp(R,a,h,top):
    n=R.ngens(); x=R.gens()
    gens=[x[i]**a[i] for i in range(len(a))]
    P=R.ideal(gens)
    for d in range(1,top+1):
        mons=sorted(R.monomials_of_degree(d), reverse=True)  # lex order? use explicit lex key
        mons=sorted(R.monomials_of_degree(d), key=lambda m: m.exponents()[0], reverse=True)
        outside=[m for m in mons if m not in P]
        dimP=len(mons)-len(outside)
        q=(len(mons)-h[d])-dimP
        if q<0 or q>len(outside): return None
        gens+=outside[:q]
    return R.ideal(gens)
def run(n,a,extra,trials,char0=True):
    K=QQ
    R=PolynomialRing(K,'x',n,order='lex')
    x=R.gens(); res=[]
    for tr in range(trials):
        def rf(d):
            return sum(K(rng.randint(-3,3))*m for m in R.monomials_of_degree(d))
        reg=[rf(d) for d in a]
        ex=[rf(d) for d in extra]
        I=R.ideal(reg+ex)
        top=sum(ai-1 for ai in a)+1 if len(a)==n else 8
        h=hilb(I,R,top)
        J=lpp(R,a,h,top)
        if J is None: res.append(('LPP undefined',h)); continue
        hJ=hilb(J,R,top)
        bI=betti(I); bJ=betti(J)
        ok=(h==hJ) and all(bI.get(k,0)<=bJ.get(k,0) for k in set(bI)|set(bJ))
        res.append((ok,h,sum(bI.values()),sum(bJ.values())))
    return res
t=time.time()
for n,a,extra in [(3,[2,2,2],[2]),(3,[2,2,3],[3,3]),(3,[2,3,3],[3]),(4,[2,2,2,2],[2,3]),(4,[2,2,3,3],[3,3]),(3,[2,2],[3,3])]:
    r=run(n,a,extra,6)
    print(f"n={n} a={a} extra={extra}: ", [(x[0],x[2],x[3]) if len(x)>2 else x for x in r], f"{time.time()-t:.1f}s", flush=True)
