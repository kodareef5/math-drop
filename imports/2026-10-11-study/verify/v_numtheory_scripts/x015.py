from sage.all import EllipticCurve, QuadraticField, Integer, kronecker
X = EllipticCurve('15a1')
print('X0(15) =15a1?', X.ainvs(), 'conductor', X.conductor(), 'rank(Q)', X.rank(), 'torsion', X.torsion_order())
fields = sorted([d for d in range(-3,-100,-1) if Integer(d).is_fundamental_discriminant()]+[-163], reverse=True)
print(len(fields), fields)
cov=[]; notcov=[]
for d in fields:
    Et = X.quadratic_twist(d)
    Lr = Et.lseries().L_ratio()   # exact via modular symbols
    eps = Et.root_number()
    if Lr != 0:
        cov.append(d)
    else:
        try:
            r = Et.rank(proof=True)
        except Exception as e:
            r = 'err'
        notcov.append((d, eps, r))
print('covered (L(X^d,1)!=0 => rank X(K)=0 by Kolyvagin):', cov, len(cov))
print('not covered (d, root number, proved rank of twist):', notcov, len(notcov))
