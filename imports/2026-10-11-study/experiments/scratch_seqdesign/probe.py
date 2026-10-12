import numpy as np, time
from seeds import *
rng=np.random.default_rng(0)
for N in [257,1021,4099]:
    M=1<<int(np.ceil(np.log2(16*N)))
    for H in [1,2,4,8]:
        perm=rng.permutation(H)
        X=relaxed_chirp(N,H,perm,v=0.5)
        Q=np.abs(np.fft.fft(X,M))
        e=np.mean(X**2); mx=Q.max()/np.sqrt(N); 
        mu=0.5*np.sum(1-np.abs(X))/N
        ssign=np.where(X>=0,1,-1)
        t=time.time(); sg=greedy_l4_round(X); tt=time.time()-t
        print(f"N={N} H={H} energy/N={e:.3f} max|Q|/sqrtN={mx:.3f} mu/N={mu:.3f} F(sign)={merit(ssign):.3f} F(greedy)={merit(sg):.3f} max|P_greedy|/sqrtN={np.abs(np.fft.fft(sg,M)).max()/np.sqrt(N):.3f} t={tt:.1f}s")
    L=legendre_candidates(N,3)
    print("legendre best", [(round(a,3),b,c) for a,b,c,_ in L])
