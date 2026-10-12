import sys, time, random
sys.path.insert(0,'.')
from artin_wp import *
# Affine A~2: triangle of 3s
cox={(1,2):3,(2,3):3,(1,3):3}
Z,verts=build(cox)
def P(*xs): return [(abs(x), 1 if x>0 else -1) for x in xs]
cases=[('s1s2s1 = s2s1s2', P(1,2,1,-2,-1,-2), True),
       ('s1s2 = s2s1', P(1,2,-1,-2), False),
       ('s3(s1s2s1)s3^-1 = s3(s2s1s2)s3^-1', P(3,1,2,1,-2,-1,-2,-3), True),
       ('s1 = s2', P(1,-2), False),
       ('s1^5 s2 s1^-5 = s2 ?', P(1,1,1,1,1,2,-1,-1,-1,-1,-1,-2), False),
       ('(s1s2s3)^3 commutation test with s1s2s1', P(1,2,3,1,2,3,1,2,3, 1,2,1, -3,-2,-1,-3,-2,-1,-3,-2,-1, -1,-2,-1), None)]
for name,w,exp in cases:
    st={}; t=time.time(); r=is_member(Z,w,st)
    print(f"A~2  {name}: identity? {r} (expected {exp})  peak {st['peak']} final {st['final']}  {time.time()-t:.3f}s")
# large type (4,4,4) not supported (label 4 needs Temperley-Lieb fusion data); use (3,3,oo) and (oo,oo,oo)
cox2={(1,2):3,(2,3):3,(1,3):'oo'}
Z2,_=build(cox2)
for name,w,exp in [('s1s2s1=s2s1s2',P(1,2,1,-2,-1,-2),True),('s1s3=s3s1',P(1,3,-1,-3),False),('s2s3s2=s3s2s3',P(2,3,2,-3,-2,-3),True)]:
    st={}; r=is_member(Z2,w,st); print(f"(3,3,oo) {name}: {r} (exp {exp}) final {st['final']}")
