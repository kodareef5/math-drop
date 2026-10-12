import sys, math, json; sys.path.insert(0,'.')
import bounds
from bounds import *
bounds.U_GRID=[0.25,0.5,0.75,1.0,1.5,2.0]
bounds.CU[0.25]=19.3374
def mac_tuned(N, le):
    n=math.ceil(lg(N)); tot=0
    for i in range(n):
        Ni=N/2**i
        if Ni<2: break
        r=1
        while lg(7)+1.5*lg(Ni)-lg(r+2)+(r/2+1)*lg(0.75) > le-lg(n): r+=1
        tot+=r
    return tot
def sn_lift_generalN(N, le):
    # same optimizer but for arbitrary N (not power of 2): Z_s computed at d = log2 N rounded down (Z_s decreasing in N)
    d=int(math.floor(lg(N)))
    best=None
    for b in [4,8,16]:
        for u in bounds.U_GRID:
            g=1-(u+2)/b
            if g<=0: continue
            for p in range(2,61):
                if p*g-1<0.05: continue
                if floor_log2(p,b,u,d)>le-1: continue
                def ok(r):
                    ld=lg(b)+hmr_q_log2(N, N-N//b, r)
                    return ld<0 and lift_tv_log2(ld,p,b,u,d)<=le
                lo,hi=1,1
                while not ok(hi): hi*=2
                while lo<hi:
                    m=(lo+hi)//2
                    if ok(m): hi=m
                    else: lo=m+1
                if best is None or p*lo<best[0]: best=(p*lo,dict(b=b,u=u,p=p,r=lo))
    return best
res=[]
for name,N in [("10^6",10**6),("2^20",2**20),("10^9 (SSN)",10**9),("2^32",2**32),("10^16 (PAN)",10**16),("2^64",2**64)]:
    for le in (-32,-64):
        sl=sn_lift_generalN(N,le); sr=sr_rounds(N,le); mc=mac_rounds(N,le)[0]; mct=mac_tuned(N,le)
        th=None
        d=lg(N)
        if abs(d-round(d))<1e-9:
            th=min_rounds_lift(int(round(d)),le,'thorp')
        row=dict(N=name,log2_eps=le,sn_lift=sl,sr_mean=round(sr[0],1),sr_worst=sr[1],mac_thm5=mc,mac_tuned=mct,thorp_lift=th)
        res.append(row); print(row); sys.stdout.flush()
json.dump(res,open('extra_out.json','w'),indent=1)
