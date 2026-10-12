import time
from sage.all import *
from cysignals.alarm import alarm, cancel_alarm, AlarmInterrupt
A = ArtinGroup(CoxeterMatrix([[1,3,3],[3,1,3],[3,3,1]]))  # affine A~2
print(type(A))
s1,s2,s3 = A.gens()
tests = [('braid rel (true)',s1*s2*s1, s2*s1*s2),
         ('non-rel (false)',s1*s2, s2*s1),
         ('conj braid rel (true)',s3*s1*s2*s1*s3**-1, s3*s2*s1*s2*s3**-1),
         ('s1 vs s2 (false)', s1, s2)]
for name,x,y in tests:
    t=time.time()
    try:
        alarm(60)
        r = (x==y)
        cancel_alarm()
        print(name, r, round(time.time()-t,2),'s', flush=True)
    except AlarmInterrupt:
        print(name, 'TIMEOUT 60s', flush=True)
