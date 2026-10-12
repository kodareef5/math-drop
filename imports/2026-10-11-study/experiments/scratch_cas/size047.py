import time
from sage.all import PolynomialRing, QQ, factorial
t0=time.time()
R=PolynomialRing(QQ,'p,s,u,F,J,w')
p,s,u,F,J,w=R.gens()
x=s**2+u**3+p**2*F
H=x**2*F-(1+2*s*x)*J-p**2*J**2-p*u
print("047 H: terms",len(H.monomials()),"degree",H.degree(), flush=True)
D={p:R(0),u:-p**2,s:-3*p**2*x*u**2,F:(6*s*x+3)*u**2,J:3*x**2*u**2}
def Delta(g): return sum(g.derivative(v)*D[v] for v in (p,s,u,F,J))
print("Delta x == 0:",Delta(x)==0," Delta H == p^3:",Delta(H)==p**3, flush=True)
def expmwD(g):   # Phi^{-1} = exp(-w Delta)
    out=R(0); term=g; k=0
    while term!=0:
        out+=(-w)**k*term/factorial(k); k+=1; term=Delta(term)
    return out,k
x0=s**2+u**3
M_=(1-2*s*x0)*F+4*s**2*J
L_=x0**2*F-(1+2*s*x0)*J
# e_0 = -w - p F(L)^3 - Q1(L) h  with F,J as functions of L,M; we use F,J directly (same element of P[w])
Q=2*x0*F**2-2*s*F*J-J**2
# C = Q at L=0: F=(1+2 s x0)M, J=x0^2 M where M=M_
C=Q.subs({F:(1+2*s*x0)*M_, J:x0**2*M_})
Q1=(Q-C)//L_ if (Q-C)%L_==0 else None
print("Q1 polynomial in P:", Q1 is not None, flush=True)
h=u-p*Q-p**3*F**3-p**2*w
e0=-w-p*F**3-Q1*h
for name,g in [('p',p),('s',s),('u',u),('M',M_),('e0',e0)]:
    t=time.time(); im,k=expmwD(g)
    print(f"047 coordinate Phi^-1({name}): Delta-nilpotency {k}, {len(im.monomials())} terms, degree {im.degree()}, {time.time()-t:.1f}s", flush=True)
