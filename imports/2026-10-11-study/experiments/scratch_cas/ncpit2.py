# Faster prototype: series arithmetic with FLINT (fmpq_poly), same semantics as ncpit.py.
import random, time, itertools, sys
from flint import fmpq_poly, fmpq
sys.setrecursionlimit(100000)
_inv={}
def inv_series(i,d):
    k=(i,d)
    if k not in _inv:
        # 1/(z+i) = sum (-1)^a z^a / i^(a+1)
        _inv[k]=fmpq_poly([fmpq((-1)**a, i**(a+1)) for a in range(d)])
    return _inv[k]
def Tv(i,v,d):  # pi_d( int_0^z v(t)/(t+i) dt )
    return v.mul_low(inv_series(i,d), d).integral().truncate(d) if hasattr(v,'mul_low') else None
def ev(f,v,d):
    t=f[0]
    if t=='x': return Tv(f[1],v,d)
    if t=='c': return v*f[1]
    if t=='+': return ev(f[1],v,d)+ev(f[2],v,d)
    return ev(f[1],ev(f[2],v,d),d)
def size(f): return 1 if f[0] in 'xc' else 1+size(f[1])+size(f[2])
def ordz(p):
    c=p.coeffs()
    for k,a in enumerate(c):
        if a!=0: return k
    return None
def hit(f,n,d): return ordz(ev(f,fmpq_poly([1]),d))
def X(i): return ('x',i)
def add(a,b): return ('+',a,b)
def mul(a,b): return ('*',a,b)
def neg(a): return ('*',('c',fmpq(-1)),a)
def sub(a,b): return add(a,neg(b))
def comm(a,b): return sub(mul(a,b),mul(b,a))
def power(a,k):
    r=a
    for _ in range(k-1): r=mul(r,a)
    return r
def rand_formula(s,n,rng):
    if s<=1: return X(rng.randint(1,n)) if rng.random()<0.8 else ('c',fmpq(rng.randint(-3,3)))
    k=rng.randint(1,s-2) if s>=3 else 1
    return ('+' if rng.random()<0.4 else '*', rand_formula(k,n,rng), rand_formula(max(1,s-1-k),n,rng))
def standard_poly(xs):
    tot=None
    for perm in itertools.permutations(range(len(xs))):
        sgn=1
        for a in range(len(perm)):
            for b in range(a+1,len(perm)):
                if perm[a]>perm[b]: sgn=-sgn
        term=xs[perm[0]]
        for j in perm[1:]: term=mul(term,xs[j])
        if sgn<0: term=neg(term)
        tot=term if tot is None else add(tot,term)
    return tot
if __name__=='__main__':
    rng=random.Random(1)
    print("== structured formulas: ord_0(h_f) actually reached vs guaranteed d=2ns^2", flush=True)
    tests=[('[x1,x2]',comm(X(1),X(2)),2),
           ('[[x1,x2],x1]',comm(comm(X(1),X(2)),X(1)),2),
           ('[[x1,x2],x3]',comm(comm(X(1),X(2)),X(3)),3),
           ('S_4 standard poly (zero on M_2)',standard_poly([X(i) for i in range(1,5)]),4),
           ('S_5 standard poly',standard_poly([X(i) for i in range(1,6)]),5),
           ('[x1,x2]^4 (Hall-type, zero on M_1 only)',power(comm(X(1),X(2)),4),2),
           ('(x1+x2)^10-(x2+x1)^10 + [x1,x2]', add(sub(power(add(X(1),X(2)),10),power(add(X(2),X(1)),10)),comm(X(1),X(2))),2),
           ('ZERO: (x1+x2)^10-(x2+x1)^10', sub(power(add(X(1),X(2)),10),power(add(X(2),X(1)),10)),2)]
    for name,f,n in tests:
        s=size(f); d=2*n*s*s
        t=time.time(); o=hit(f,n,d); dt=time.time()-t
        print(f" {name}: n={n} s={s} d={d}  ord_0={o}  eval {dt:.2f}s", flush=True)
    print("== random formulas", flush=True)
    for n,s in [(3,31),(5,63),(5,127),(8,255),(8,511)]:
        d=2*n*s*s; mx=0; t=time.time(); cnt=0; zeros=0
        for _ in range(3):
            f=rand_formula(s,n,rng); o=hit(f,n,d); cnt+=1
            if o is None: zeros+=1
            else: mx=max(mx,o)
        print(f" n={n} s={s} d={d}: avg eval {(time.time()-t)/cnt:.2f}s  max ord_0 {mx}  zero {zeros}/{cnt}", flush=True)
