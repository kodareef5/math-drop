import sys, math, json; sys.path.insert(0,'.')
from bounds import *
rows=json.load(open('bounds_out.json'))['rows']
def hmr_partial_rounds(N, q, le, cca=True):
    # cca: HMR eq.(1) 8N^1.5/(r+4) ((q+N)/2N)^(r/4+1); ncpa: Thm3 2N^1.5/(r+2)((q+N)/2N)^(r/2+1)
    r=1
    while True:
        if cca: v=3+1.5*lg(N)-lg(r+4)+(r/4+1)*lg((q+N)/(2*N))
        else: v=hmr_q_log2(N,q,r)
        if v<=le: return r
        r+=1
print("d  log2eps | SN-lift(fixed) | HMR cca q=N/2 | HMR ncpa q=7N/8 | lift/HMR(7N/8) | Thorp-lift rounds, AES(/5) | MaC | SR mean/worst")
tab=[]
for R in rows:
    d,le=R['d'],R['log2_eps']; N=2**d
    h2=hmr_partial_rounds(N,N//2,le,True); h78=hmr_partial_rounds(N,N-N//8,le,False)
    sn=R['sn_lift'][0]; th=R['thorp_lift'][0]
    tab.append(dict(d=d,le=le,sn=sn,sn_par=R['sn_lift'][1],th=th,th_par=R['thorp_lift'][1],th_aes=th/5,hmr_half_cca=h2,hmr_78_ncpa=h78,mac=R['mac'][0],sr_mean=R['sr'][0],sr_worst=R['sr'][1]))
    print(f"{d:2d} {le:5d} | {sn:7d} | {h2:6d} | {h78:6d} | {sn/h78:5.1f}x | {th:7d}, {th/5:8.0f} | {R['mac'][0]:6d} | {R['sr'][0]:.0f}/{R['sr'][1]}")
json.dump(tab,open('compare_out.json','w'),indent=1)
# Ethereum: N ~ 2^20..2^21 active validators, r=90
for d in (20,21,22):
    N=2**d
    print(f"Eth2 N=2^{d}, r=90: HMR Thm3 q=N/2 TV bound 2^{hmr_q_log2(N,N//2,90):.1f}; q=1000 committee: 2^{hmr_q_log2(N,1000,90):.1f}; rounds for HMR q=N/2 ncpa <=2^-32: {hmr_partial_rounds(N,N//2,-32,False)}; support lower bound rounds ~ {math.ceil((math.lgamma(N+1)/math.log(2))/(N/2))}")
# p=2 (asymptotic isotypic corollary) and p=8 op-norm floor for SN at b=8,u=1
for d in (20,32,64):
    print(f"N=2^{d}: lift floor p=2,b=8,u=1: 2^{floor_log2(2,8,1.0,d):.1f}; p=4: 2^{floor_log2(4,8,1.0,d):.1f}; p=8: 2^{floor_log2(8,8,1.0,d):.1f}")
