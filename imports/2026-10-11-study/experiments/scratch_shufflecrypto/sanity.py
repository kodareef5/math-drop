import sys; sys.path.insert(0,'.')
from bounds import *
# validate SR against Morris-Rogaway Fig 2 (N=10^16, eps=1e-10: mean ~1048-1159, worst 18239?) and MaC (N=2^30 ~10,000)
le=math.log2(1e-10)
for N in (10**6, 10**16, 10**30):
    print("SR", N, [round(x,1) for x in sr_rounds(N, le)])
print("MaC 2^30", mac_rounds(2**30, le))
# HMR examples: 64-bit, 1200 rounds, q=2^63: adv (Eq.1 CCA form) 8N^1.5/(r+4)((q+N)/2N)^(r/4+1)
N=2**64; r=1200; q=2**63
print("HMR eq1 log2 adv", 3+1.5*64-math.log2(r+4)+(r/4+1)*math.log2((q+N)/(2*N)))
# Z values
for d in (20,32,64):
    print(d, "log2 Z3", round(log2_Z(3.0,d),2), "expected ~", round(1-3*d,2), " log2 Z2", round(log2_Z(2.0,d),2))
print("tiny check Z_1(2^20)", log2_Z(1.0,20))
