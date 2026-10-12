"""Falsification attempt for family 276 additivity at n=2: maximise chi(A (x) A) over ensembles of up to 8 pure
two-qubit (possibly entangled) input states, compare with 2*chi(A)."""
import numpy as np, sys
from scipy.optimize import minimize
import gad_capacity as G
def chan2(K):
    KK=[np.kron(a,b) for a in K for b in K]
    return lambda r: sum(k@r@k.conj().T for k in KK)
def vn(r):
    w=np.linalg.eigvalsh((r+r.conj().T)/2); w=w[w>1e-14]; return -(w*np.log2(w)).sum()
def run(gam,nu,m=8,starts=12,seed=0):
    A2=chan2(G.kraus(gam,nu)); rng=np.random.default_rng(seed)
    def negchi(x):
        V=(x[:8*m].reshape(m,4,2)@np.array([1,1j])); V/=np.linalg.norm(V,axis=1,keepdims=True)
        w=np.exp(x[8*m:]); w/=w.sum()
        outs=[A2(np.outer(v,v.conj())) for v in V]
        avg=sum(wi*o for wi,o in zip(w,outs))
        return -(vn(avg)-sum(wi*vn(o) for wi,o in zip(w,outs)))
    best=0
    for s in range(starts):
        x0=np.concatenate([rng.normal(size=8*m),rng.normal(size=m)*0.1])
        r=minimize(negchi,x0,method='L-BFGS-B',options={'maxiter':3000})
        best=max(best,-r.fun)
    C1=G.exact_capacity(gam,nu)[0]
    print(f"gam={gam} nu={nu}: best chi(A^2) found={best:.6f}  2*chi(A)={2*C1:.6f}  excess={best-2*C1:+.2e}",flush=True)
for gam,nu in [(0.5,0.2),(0.3,0.05),(0.7,0.1)]:
    run(gam,nu)
