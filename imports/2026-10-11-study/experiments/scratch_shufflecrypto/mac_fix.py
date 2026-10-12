import math
lg=math.log2
def mac_perstage(N, le):
    # Ristenpart-Yilek accounting: stage i has 2^{i-1} tweaked SN instances on N_i=N/2^{i-1} points, each a 2-PRS
    # with advantage <= HMR Thm3 at q=N_i/2: 2 N_i^{1.5}/(r+2) (3/4)^{r/2+1}. Stage total 2^i N_i^{1.5}/(r+2)(3/4)^{r/2+1}.
    n=math.ceil(lg(N)); tot=0
    for i in range(1,n+1):
        Ni=N/2**(i-1)
        if Ni<2: break
        r=1
        while i+1.5*lg(Ni)-lg(r+2)+(r/2+1)*lg(0.75) > le-lg(n): r+=1
        tot+=r
    return tot
for name,N in [("10^6",10**6),("2^20",2**20),("10^9",10**9),("2^32",2**32),("10^16",10**16),("2^64",2**64)]:
    print(name, {le: mac_perstage(N,le) for le in (-32,-64,-128)})
