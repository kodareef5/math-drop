import sys, time, random
sys.path.insert(0,'.')
from ncpit2 import *
from flint import nmod_poly, nmod
import math
rng=random.Random(5)
# exact deterministic evaluation (first column only), and cost to certify a ZERO formula (needs all d coefficients)
rows=[]
for name,f,n in [('[x1,x2]',comm(X(1),X(2)),2),
                 ('ZERO (x1+x2)^2-(x2+x1)^2',sub(power(add(X(1),X(2)),2),power(add(X(2),X(1)),2)),2),
                 ('[[x1,x2],x1]',comm(comm(X(1),X(2)),X(1)),2),
                 ('ZERO (x1+x2)^3-(x2+x1)^3',sub(power(add(X(1),X(2)),3),power(add(X(2),X(1)),3)),2),
                 ('ZERO (x1+x2+x3)^2-(x3+x2+x1)^2',sub(power(add(add(X(1),X(2)),X(3)),2),power(add(add(X(3),X(2)),X(1)),2)),3)]:
    s=size(f); d=2*n*s*s
    t=time.time(); o=hit(f,n,d); dt=time.time()-t
    B=3+math.ceil(math.log2(d+1))+d*math.ceil(math.log2(n+1))
    print(f"{name}: n={n} s={s} d={d} entry-bits<= {B}  ord_0={o}  exact first-column eval {dt:.2f}s", flush=True)
# randomized baseline: random k x k matrices mod p=2^61-1, k = floor(s/2)+1 (Amitsur-Levitzki), error <= deg/p
import numpy as np
P=(1<<61)-1
def matmul(A,B):
    k=len(A); return [[sum(A[i][l]*B[l][j] for l in range(k))%P for j in range(k)] for i in range(k)]
def evm(f,Ms,k):
    t=f[0]
    if t=='x': return Ms[f[1]]
    if t=='c': c=int(f[1].p)*pow(int(f[1].q),-1,P)%P; return [[(c if i==j else 0) for j in range(k)] for i in range(k)]
    a=evm(f[1],Ms,k); b=evm(f[2],Ms,k)
    if t=='+': return [[(a[i][j]+b[i][j])%P for j in range(k)] for i in range(k)]
    return matmul(a,b)
for name,f,n in [('S_4 standard polynomial',standard_poly([X(i) for i in range(1,5)]),4),('ZERO (x1+x2)^10-(x2+x1)^10',sub(power(add(X(1),X(2)),10),power(add(X(2),X(1)),10)),2)]:
    s=size(f); k=3 if 'S_4' in name else 6
    Ms={i:[[rng.randrange(P) for _ in range(k)] for _ in range(k)] for i in range(1,n+1)}
    t=time.time(); V=evm(f,Ms,k); dt=time.time()-t
    nz=any(V[i][j] for i in range(k) for j in range(k))
    d=2*n*s*s
    print(f"randomized {name}: s={s}, {k}x{k} mod 2^61-1: nonzero={nz} in {dt*1000:.1f} ms; deterministic point would need d={d}, entries up to ~{d*math.ceil(math.log2(n+1))} bits")
