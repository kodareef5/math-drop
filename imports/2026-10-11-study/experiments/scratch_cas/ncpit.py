# Prototype of the char-0 hitting point of family 116 (One-Rational-Matrix-Hitting-Point, thm:main).
# T_i is the matrix of a(z) -> int_0^z a(t)/(t+i) dt on F[[z]]/(z^d), d = 2 n s^2.
# Key observation: f(T)e_0 = pi_d(h_f) can be computed with s "matrix-vector" products,
# and each T_i v is an O(d) recurrence (divide by (z+i), then integrate), not an O(d^2) product.
import random, time, itertools, math
from flint import fmpq, fmpz_mat, fmpq_mat
def Tv(i, v):
    d=len(v); b=[fmpq(0)]*d; prev=fmpq(0)
    for r in range(d):           # b = v/(z+i):  i*b_r + b_{r-1} = v_r
        prev=(v[r]-prev)/i; b[r]=prev
    c=[fmpq(0)]*d               # integrate: c_r = b_{r-1}/r
    for r in range(1,d): c[r]=b[r-1]/r
    return c
# formulas: ('x',i) | ('c',q) | ('+',A,B) | ('*',A,B)
def size(f): return 1 if f[0] in 'xc' else 1+size(f[1])+size(f[2])
def ev(f, v):
    t=f[0]
    if t=='x': return Tv(f[1], v)
    if t=='c': return [f[1]*a for a in v]
    if t=='+':
        a=ev(f[1],v); b=ev(f[2],v); return [x+y for x,y in zip(a,b)]
    return ev(f[1], ev(f[2], v))   # (A*B)v = A(Bv)
def hit(f, n, d):
    e0=[fmpq(1)]+[fmpq(0)]*(d-1)
    h=ev(f,e0)
    nz=[k for k,a in enumerate(h) if a!=0]
    return (nz[0] if nz else None)
def X(i): return ('x',i)
def add(a,b): return ('+',a,b)
def mul(a,b): return ('*',a,b)
def neg(a): return ('*',('c',fmpq(-1)),a)
def sub(a,b): return add(a,neg(b))
def comm(a,b): return sub(mul(a,b),mul(b,a))
def rand_formula(s, n, rng):
    if s<=1: return X(rng.randint(1,n)) if rng.random()<0.8 else ('c',fmpq(rng.randint(-3,3)))
    k=rng.randint(1,s-2) if s>=3 else 1
    op = '+' if rng.random()<0.4 else '*'
    return (op, rand_formula(k,n,rng), rand_formula(max(1,s-1-k),n,rng))
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
        tot = term if tot is None else add(tot,term)
    return tot
if __name__=='__main__':
    rng=random.Random(1)
    print("== structured nonzero formulas: actual ord_0(h_f) vs guaranteed bound d-1 = 2ns^2-1")
    tests=[('[x1,x2]',comm(X(1),X(2)),2),
           ('[[x1,x2],x1]',comm(comm(X(1),X(2)),X(1)),2),
           ('[[x1,x2],[x1,x2]]... [ [x1,x2], x3 ]',comm(comm(X(1),X(2)),X(3)),3),
           ('S_4(x1..x4) (vanishes on 2x2 matrices)',standard_poly([X(1),X(2),X(3),X(4)]),4),
           ('S_6(x1..x6) (vanishes on 3x3 matrices)',standard_poly([X(i) for i in range(1,7)]),6),
           ('(x1+x2)^8 - (x2+x1)^8 + [x1,x2]', add(sub(eval("mul("*7+"add(X(1),X(2))"+",add(X(1),X(2)))"*7), eval("mul("*7+"add(X(2),X(1))"+",add(X(2),X(1)))"*7)), comm(X(1),X(2))),2)]
    for name,f,n in tests:
        s=size(f); d=2*n*s*s
        t=time.time(); o=hit(f,n,d); dt=time.time()-t
        print(f"{name}: n={n} size s={s} d=2ns^2={d}  ord_0(h_f)={o}  eval {dt:.2f}s")
    print("== identically-zero formula: (x1+x2)^8 - (x2+x1)^8 must give zero vector")
    z = sub(eval("mul("*7+"add(X(1),X(2))"+",add(X(1),X(2)))"*7), eval("mul("*7+"add(X(2),X(1))"+",add(X(2),X(1)))"*7))
    s=size(z); print(" size",s," ord:",hit(z,2,2*2*s*s))
    print("== random formulas: time for one deterministic evaluation (vector form) and max observed ord_0")
    for n,s in [(3,15),(3,31),(5,63),(5,127),(8,255)]:
        d=2*n*s*s; mx=0; t=time.time(); cnt=0; zeros=0
        for _ in range(5):
            f=rand_formula(s,n,rng); o=hit(f,n,d); cnt+=1
            if o is None: zeros+=1
            else: mx=max(mx,o)
        print(f" n={n} s={s} d={d}: avg eval {(time.time()-t)/cnt:.2f}s, max ord_0 seen {mx}, zero formulas {zeros}/{cnt}")
