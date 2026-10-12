import sys, math; sys.path.insert(0,'.')
from bounds import hmr_q_log2, thorp_list_log2, lg
def thorp_ncpa_rounds(d, frac_avail, le):
    b = 1/frac_avail  # alpha = 1/b
    T = 2*d
    while thorp_list_log2(d, b, T) > le: T += 1
    return T
def hmr_cca_rounds(N,q,le):
    r=1
    while 3+1.5*lg(N)-lg(r+4)+(r/4+1)*lg((q+N)/(2*N))>le: r+=1
    return r
def mrs_cca(N, q, le):
    # MRS Thm 5: Th[N, r(4n-2)] CCA <= 2q/(r+1) (4nq/N)^r
    n=int(round(lg(N)))
    if 4*n*q>=N: return None
    r=1
    while lg(2*q/(r+1)) + r*lg(4*n*q/N) > le: r+=1
    return r*(4*n-2)
print("Partial-domain CCA rounds (and AES calls) at eps=2^-64")
print("N, q | MRS'09 Thorp CCA | new Thorp fixed-list (nCPA x2 for CCA via MPR) rounds / AES(5x) | HMR SN CCA rounds=AES")
for d in (20,32,64):
    N=2**d
    for name,q,fa in (("N/(8 lgN)",N//(8*d),None),("N/2",N//2,0.5),("7N/8",N-N//8,0.125)):
        m = mrs_cca(N,q,-65) if q< N/(4*d) else None
        if fa is None: fa = 1 - q/N
        t = thorp_ncpa_rounds(d, fa, -65)
        h = hmr_cca_rounds(N,q,-64)
        print(f"2^{d}, {name}: MRS {m} | Thorp {2*t} rounds / {2*t/5:.0f} AES | SN {h}")
# Ethereum committee-level: rounds for HMR Thm 3 (nCPA = TV of q designated points) <= 2^-40
for d in (20,21):
    N=2**d
    for q in (128, 2048):
        r=1
        while hmr_q_log2(N,q,r) > -40: r+=1
        print(f"Eth2 N=2^{d} q={q}: TV bound at r=90: 2^{hmr_q_log2(N,q,90):.1f}; rounds for 2^-40: {r}")
