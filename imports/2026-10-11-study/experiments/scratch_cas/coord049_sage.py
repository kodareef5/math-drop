# Family 049: build the explicit automorphism of C[x1..x4,w] that sends f to x1, verify it, and measure its size.
import time
from sage.all import PolynomialRing, QQ, matrix, identity_matrix, factorial
t0=time.time()
R=PolynomialRing(QQ,'p,s,u,F,J,w,P,S,U,N,Wp,x1,x2,x3,x4,L', order='degrevlex')
p,s,u,F,J,w,P,S,U,N,Wp,x1,x2,x3,x4,L = R.gens()
x = s**2-u**2+p*F
H = x**2*F-(1+2*s*x)*J-p*J**2-u
M = matrix(R,[[F,s-u],[s+u,-p]]); e=matrix(R,[[x],[-J]]); n=matrix(R,[[J],[x]])
Mp=(identity_matrix(R,2)-2*n*e.transpose())*M
Fp=Mp[0,0]; sp_=(Mp[0,1]+Mp[1,0])/2; pp=-Mp[1,1]
Q=x2**2-x4**2+x1*x3
f=x1-2*Q*(Q*(x2+x4)+x1*x4)
I=R.ideal([H])
fs=f.subs({x1:pp,x2:sp_,x3:Fp,x4:J})
print("Prop 2.1 check  f(p',s',F',J) == p  mod H :", (fs-p).reduce(I.groebner_basis())==0 if False else (fs-p) in I)
D={p:R(0),u:-p,s:2*p*x*u,F:-4*s*x*u-2*u,J:-2*x**2*u,w:R(0)}
def Delta(g): return sum(g.derivative(v)*D[v] for v in (p,s,u,F,J))
assert Delta(x)==0 and Delta(H)==p
def expwD(g):
    out=R(0); term=g; k=0
    while term!=0:
        out+=w**k*term/factorial(k); k+=1; term=Delta(term)
    return out,k
x0=s**2-u**2
Q0=2*x0*F**2+p*F**3-2*s*F*J-J**2
def to_target(g):
    g=g.subs({w:Wp-Q0})
    g=g.subs({F:4*s**2*L+(1+2*s*x0)*N, J:-(1-2*s*x0)*L+x0**2*N})
    g=g.subs({L:u-p*Wp})
    return g.subs({p:P,s:S,u:U})
print("H + p w maps to 0:", to_target(H+p*w)==0)
imgs={}
for name,g in [('x1',pp),('x2',sp_),('x3',Fp),('x4',J),('w',w)]:
    eg,k=expwD(g); tg=to_target(eg); imgs[name]=tg
    print(f"image of {name}: Delta-nilpotency index {k}, {len(tg.monomials())} terms, total degree {tg.degree()}")
fimg=f.subs({x1:imgs['x1'],x2:imgs['x2'],x3:imgs['x3'],x4:imgs['x4']})
print("phi(f) == P (first target coordinate):", fimg==P)
Jm=matrix(R,[[imgs[k].derivative(v) for v in (P,S,U,N,Wp)] for k in ['x1','x2','x3','x4','w']])
det=Jm.det()
print("Jacobian determinant of phi:", det)
print("f:", len(f.monomials()), "terms, degree", f.degree())
print("secs", round(time.time()-t0,1))
