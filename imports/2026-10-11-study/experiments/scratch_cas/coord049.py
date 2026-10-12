# Build the explicit automorphism of C[x1..x4,w] sending f -> x1 (family 049) and measure it.
import time, sympy as sp
t0=time.time()
p,s,u,F,J,w = sp.symbols('p s u F J w')
P5,S5,U5,N5,W5 = sp.symbols('P S U N Wp')   # target coords p,s,u,N,w'
x = s**2-u**2+p*F
H = sp.expand(x**2*F-(1+2*s*x)*J-p*J**2-u)
# Prop 2.1: M' = (I-2 n e^T) M
M = sp.Matrix([[F, s-u],[s+u,-p]]); e = sp.Matrix([x,-J]); n = sp.Matrix([J,x])
Mp = (sp.eye(2)-2*n*e.T)*M
Fp = sp.expand(Mp[0,0]); sp_ = sp.expand((Mp[0,1]+Mp[1,0])/2); pp = sp.expand(-Mp[1,1])
# check: f(p',s',F',J) == p mod H
X1,X2,X3,X4 = sp.symbols('x1 x2 x3 x4')
Q = X2**2-X4**2+X1*X3
f = sp.expand(X1-2*Q*(Q*(X2+X4)+X1*X4))
fsub = sp.expand(f.subs({X1:pp,X2:sp_,X3:Fp,X4:J}, simultaneous=True))
r = sp.reduced(fsub - p, [H], p,s,u,F,J)[1] if False else None
# Use polynomial division by H, which is linear in u with coefficient -1: substitute u = H_rest
usol = sp.solve(sp.Eq(H,0),u)  # H = (...)-u where (...) contains u through x; not linear. Instead verify via rem.
def remH(g):
    q,rr = sp.div(sp.Poly(g,u,s,p,F,J), sp.Poly(H,u,s,p,F,J))
    return rr
print("f(p',s',F',J)-p reduces to 0 mod H in P? ", sp.Poly(fsub-p, p,s,u,F,J).is_zero or None)
# Derivation Delta on P (eq. con:delta)
D = {p:0, u:-p, s:2*p*x*u, F:-4*s*x*u-2*u, J:-2*x**2*u, w:0}
def Delta(g):
    return sp.expand(sum(sp.diff(g,v)*D[v] for v in (p,s,u,F,J)))
assert sp.expand(Delta(x))==0
assert sp.expand(Delta(H)-p)==0
def expwD(g, maxit=60):
    out=0; term=g; k=0
    while term!=0:
        out += w**k*term/sp.factorial(k); k+=1; term=Delta(term)
        if k>maxit: raise RuntimeError
    return sp.expand(out), k
# substitution to target coordinates
x0 = s**2-u**2
Lsym = sp.Symbol('L')
Fexpr = 4*s**2*Lsym+(1+2*s*x0)*N5
Jexpr = -(1-2*s*x0)*Lsym + x0**2*N5
Q0 = 2*x0*F**2+p*F**3-2*s*F*J-J**2
def to_target(g):  # g in P[w]
    g = g.subs({w: W5 - Q0}, simultaneous=True)
    g = g.subs({F:Fexpr, J:Jexpr}, simultaneous=True)
    g = g.subs({Lsym: u - p*W5}, simultaneous=True)
    g = g.subs({p:P5, s:S5, u:U5}, simultaneous=True)
    return sp.expand(g)
# sanity: H+pw must map to 0
print("H+pw -> 0:", to_target(H+p*w)==0)
imgs={}
for name,g in [('x1=p\'',pp),('x2=s\'',sp_),('x3=F\'',Fp),('x4=J',J),('w',w)]:
    eg,k = expwD(g)
    tg = to_target(eg)
    imgs[name]=tg
    P_ = sp.Poly(tg, P5,S5,U5,N5,W5)
    print(f"{name}: source terms={len(sp.Poly(g,p,s,u,F,J).terms())}, Delta-nilpotency={k}, image terms={len(P_.terms())}, total degree={P_.total_degree()}")
# relabel targets as x1..x4,w : P->x1,S->x2,U->x3,N->x4,Wp->w and check f -> x1
Y = sp.symbols('y1:6')
phi = {X1:imgs["x1=p'"], X2:imgs["x2=s'"], X3:imgs["x3=F'"], X4:imgs['x4=J']}
fimg = sp.expand(f.subs(phi, simultaneous=True))
print("image of f equals P (=x1)?", sp.expand(fimg-P5)==0)
Jac = sp.Matrix([[sp.diff(imgs[k],v) for v in (P5,S5,U5,N5,W5)] for k in ["x1=p'","x2=s'","x3=F'",'x4=J','w']])
t1=time.time()
det = sp.expand(Jac.det(method='berkowitz'))
print("Jacobian determinant:", det, f"(det time {time.time()-t1:.1f}s)")
print("f: terms", len(sp.Poly(f,X1,X2,X3,X4).terms()), "deg", sp.Poly(f,X1,X2,X3,X4).total_degree())
print("total secs", round(time.time()-t0,1))
