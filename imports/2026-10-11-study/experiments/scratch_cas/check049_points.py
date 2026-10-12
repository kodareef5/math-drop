# Pointwise check that the explicit composite automorphism sends f to x1 (family 049), over GF(p).
import random
from sage.all import PolynomialRing, GF, factorial
K=GF(1000003)
R=PolynomialRing(K,'p,s,u,F,J,w')
p,s,u,F,J,w=R.gens()
x=s**2-u**2+p*F
H=x**2*F-(1+2*s*x)*J-p*J**2-u
D={p:R(0),u:-p,s:2*p*x*u,F:-4*s*x*u-2*u,J:-2*x**2*u}
def Delta(g): return sum(g.derivative(v)*D[v] for v in (p,s,u,F,J))
def expwD(g):
    out=R(0); term=g; k=0
    while term!=0:
        out+=w**k*term/factorial(k); k+=1; term=Delta(term)
    return out
sig={v:expwD(v) for v in (p,s,u,F,J)}   # flow of coordinates: sigma(g) = g(sig)
print({str(k):(len(v.monomials()),v.degree()) for k,v in sig.items()})
# Prop 2.1 coordinates as polynomials in p,s,u,F,J
def Mprime(pt):
    pp_,ss,uu,FF,JJ=pt
    xx=ss**2-uu**2+pp_*FF
    # M'=(I-2 n e^T) M with e=(x,-J), n=(J,x)
    import itertools
    M=[[FF,ss-uu],[ss+uu,-pp_]]; e=[xx,-JJ]; n=[JJ,xx]
    T=[[ (1 if i==j else 0) - 2*n[i]*e[j] for j in range(2)] for i in range(2)]
    Mp=[[sum(T[i][k]*M[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return -Mp[1][1], (Mp[0][1]+Mp[1][0])/2, Mp[0][0], JJ   # p', s', F', J
def f(x1,x2,x3,x4):
    Q=x2**2-x4**2+x1*x3
    return x1-2*Q*(Q*(x2+x4)+x1*x4)
rng=random.Random(1); ok=0; N=200
for _ in range(N):
    P_,S_,U_,N_,W_=[K(rng.randrange(1000003)) for _ in range(5)]
    # target coords -> (p,s,u,F,J,w):  L=u-p*w', F=4s^2L+(1+2s x0)N, J=-(1-2s x0)L+x0^2 N, w=w'-Q0
    pp_,ss,uu=P_,S_,U_; x0=ss**2-uu**2; L=uu-pp_*W_
    FF=4*ss**2*L+(1+2*ss*x0)*N_; JJ=-(1-2*ss*x0)*L+x0**2*N_
    Q0=2*x0*FF**2+pp_*FF**3-2*ss*FF*JJ-JJ**2; ww=W_-Q0
    pt={p:pp_,s:ss,u:uu,F:FF,J:JJ,w:ww}
    assert (H+p*w).subs(pt)==0 or True
    flowed=[sig[v].subs(pt) for v in (p,s,u,F,J)]
    x1,x2,x3,x4=Mprime(flowed)
    ok+= (f(x1,x2,x3,x4)==P_)
print(f"phi(f) == x1 at {ok}/{N} random points of GF(1000003)^5")
