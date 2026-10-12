import time
from sage.all import *
from cysignals.alarm import alarm, cancel_alarm, AlarmInterrupt
def run(label, A, tests):
    for name,x,y in tests:
        t=time.time()
        try:
            alarm(30); r = (x==y); cancel_alarm()
            print(label, name, r, round(time.time()-t,3),'s', flush=True)
        except AlarmInterrupt:
            print(label, name, 'TIMEOUT 30s', flush=True)
B = ArtinGroup(['B',3]); a,b,c = B.gens()
run('B3(finite, Garside)', B, [('braid rel', b*c*b*c, c*b*c*b), ('false', a*b, b*a)])
L = ArtinGroup(CoxeterMatrix([[1,4,4],[4,1,4],[4,4,1]])); x,y,z = L.gens()
run('large-type (4,4,4)', L, [('braid rel', x*y*x*y, y*x*y*x), ('false', x*y, y*x)])
