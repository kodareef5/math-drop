"""
030 marginal value: Caraiani-Newton already prove modularity of every elliptic
curve over an imaginary quadratic field K when X_0(15)(K) is finite, i.e. when
rank 15a1(K) = rank 15a1(Q) + rank 15a1^(d_K)(Q) = 0.  For the LMFDB
'complete' imaginary quadratic fields (|d| < 100 or class number one), list
which fields are already covered and which need 030.
"""
from sage.all import EllipticCurve, QuadraticField, Integer, fundamental_discriminant

E = EllipticCurve('15a1')
fields = sorted({d for d in range(-3, -100, -1) if Integer(d).is_fundamental_discriminant()}
                | {-3, -4, -7, -8, -11, -19, -43, -67, -163}, reverse=True)
covered, need030 = [], []
for d in fields:
    Et = E.quadratic_twist(d)
    eps = Et.root_number()
    ar = Et.analytic_rank()
    try:
        r = Et.rank(only_use_mwrank=False)
    except Exception:
        r = None
    tot = E.rank() + ar
    (covered if tot == 0 else need030).append((d, eps, ar, r))
print('LMFDB IQ fields checked:', len(fields))
print('covered by Caraiani-Newton (twist rank 0):', [c[0] for c in covered])
print('NOT covered (X_0(15)(K) infinite) -> need 030:', [(c[0], 'eps', c[1], 'ar', c[2]) for c in need030])
