"""PMEPR = max_t |P(e(t))|^2 / N for binary sequences (BPSK-OFDM symbol, N subcarriers, oversampled x16)."""
import numpy as np
from seeds import legendre_candidates, merit
def pmepr(s):
    N=len(s); M=1<<int(np.ceil(np.log2(16*N))); return (np.abs(np.fft.fft(s,M))**2).max()/N
def rudin_shapiro(m):
    p=np.array([1]); q=np.array([1])
    for _ in range(m): p,q=np.concatenate([p,q]),np.concatenate([p,-q])
    return p
rng=np.random.default_rng(3)
for N,m in [(256,8),(1024,10),(4096,12)]:
    rs=rudin_shapiro(m)
    rnd=[pmepr(rng.choice([-1,1],N)) for _ in range(50)]
    L=legendre_candidates(N,1,nprimes=3)[0]
    print(f"N={N}: Rudin-Shapiro PMEPR={pmepr(rs):.2f} (F={merit(rs):.2f}); best rotated Legendre PMEPR={pmepr(L[3]):.2f} (F={L[0]:.2f}); random PMEPR median={np.median(rnd):.2f}")
