import sys, math; sys.path.insert(0,'.')
import bounds
from bounds import *
def sn_lift_N(N, le):
    d=int(math.floor(lg(N))); best=None
    for b in [4,8,16]:
        for u in [0.5,1.0]:
            g=1-(u+2)/b
            if g<=0: continue
            for p in range(2,121):
                if p*g-1<0.05: continue
                try:
                    if floor_log2(p,b,u,d)>le-1: continue
                except AssertionError:
                    continue
                def ok(r):
                    ld=lg(b)+hmr_q_log2(N,N-N//b,r)
                    return ld<0 and lift_tv_log2(ld,p,b,u,d)<=le
                lo,hi=1,1
                while not ok(hi): hi*=2
                while lo<hi:
                    m=(lo+hi)//2
                    if ok(m): hi=m
                    else: lo=m+1
                if best is None or p*lo<best[0]: best=(p*lo,dict(b=b,u=u,p=p,r=lo))
    return best
for N in (10**4, 10**5, 10**6, 2**24):
    print(N, {le: sn_lift_N(N,le) for le in (-32,)}, "SR", [round(x) for x in sr_rounds(N,-32)][:2], "table bytes", N*math.ceil(lg(N)/8))
