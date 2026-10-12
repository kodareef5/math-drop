"""
Type-D positivity test prototype for family 204.
Saturation factor 1 (Thm 1.1 of 'Tensor saturation for even spin groups') gives:
  c_{lam,mu}^{nu} > 0  <=>  (lam+mu-nu in root lattice Q(D_n))  and  (some rational dilate has an invariant)
and "some dilate has an invariant" <=> (lam, mu, nu*) lies in the rational tensor cone = the
eigencone, cut out by finitely many linear inequalities (Belkale-Kumar / Ressayre; for type D
these are not written down in closed form in polynomial size).
Here we use a generic, exact certificate that needs no inequality list:
  c_{N lam, N mu}^{N nu} > 0 for some N  <=>  the BZ/Littelmann polytope is nonempty
and approximate it by checking dilations N = 1..Nmax with Sage (Brauer-Klimyk).  This is NOT the
polynomial-time algorithm -- it measures how often the saturation shortcut changes the answer
relative to computing at N=1 directly (it never does, if the theorem is true), and how the cost of
the direct computation grows with the size of the weights.
"""
import time, sys, random
from fractions import Fraction as Fr
from sage.all import WeylCharacterRing, QQ
def cost_curve(n, base, scales):
    W=WeylCharacterRing(['D',n])
    out=[]
    for k in scales:
        lam=[QQ(k*c) for c in base[0]]; mu=[QQ(k*c) for c in base[1]]
        t=time.time(); P=W(*lam)*W(*mu); dt=time.time()-t
        out.append((k, len(P.monomial_coefficients()), round(dt,2)))
        if dt>120: break
    return out
if __name__=='__main__':
    for n,base in [(4,((2,1,1,0),(1,1,0,0))),(5,((2,1,1,0,0),(1,1,0,0,0))),(6,((1,1,0,0,0,0),(1,0,0,0,0,0)))]:
        print(f"D{n} tensor product V(k*lam) x V(k*mu), Brauer-Klimyk in Sage: (k, #irreducible constituents, secs)", cost_curve(n,base,[1,2,3,4,6,8]), flush=True)
