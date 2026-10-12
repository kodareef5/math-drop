"""Rounding comparison on the single-mode relaxed chirp (finite analogue of Prop. almost-signs, F=cos, H blocks)."""
import numpy as np
from seeds import relaxed_chirp, greedy_l4_round, merit
rng=np.random.default_rng(7)
N=1021; M=1<<15
def mx(x): return np.abs(np.fft.fft(x,M)).max()/np.sqrt(N)
for taper in [0.0,0.15]:
  for H in [1,2]:
    X=relaxed_chirp(N,H,rng.permutation(H),v=0.5,taper=taper)
    e=np.mean(X**2); mu=0.5*np.mean(1-np.abs(X))
    res={}
    res['sign']=np.where(X>=0,1,-1)
    rr=[np.where(rng.random(N)<(1+X)/2,1,-1) for _ in range(200)]
    Fr=[merit(s) for s in rr]
    res['greedyL4']=greedy_l4_round(X)
    print(f"taper={taper} H={H}: relaxed energy/N={e:.2f} defect mu/N={mu:.2f} relaxed max/sqrtN={mx(X):.2f} (max/sqrt(energy*N)={mx(X)/np.sqrt(e):.2f})")
    print(f"   sign: F={merit(res['sign']):.2f} max/sqrtN={mx(res['sign']):.2f} | indep. randomized rounding (200 draws): F mean={np.mean(Fr):.2f} best={max(Fr):.2f} | greedy-L4: F={merit(res['greedyL4']):.2f} max/sqrtN={mx(res['greedyL4']):.2f}")
