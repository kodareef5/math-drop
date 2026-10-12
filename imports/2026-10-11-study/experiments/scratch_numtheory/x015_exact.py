from sage.all import EllipticCurve
E = EllipticCurve('15a1')
cov = [-3, -4, -8, -15, -19, -20, -23, -31, -35, -47, -79, -83, -87, -91]
for d in cov:
    Et = E.quadratic_twist(d).minimal_model()
    print(d, 'root_number', Et.root_number(), 'L(E_d,1)/Omega =', Et.lseries().L_ratio(), 'rank(Q)=', E.rank(), '+', Et.rank())
