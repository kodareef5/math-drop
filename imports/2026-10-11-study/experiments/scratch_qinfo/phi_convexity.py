"""Check convexity of phi_{lam,N}(u) = g(lam*g^{-1}(u) + (1-lam)*N) in u >= 0 for N >= 0 (g = bosonic entropy, nats).
Needed (with Cor. thermal-attenuator of the EPnI paper) for a thermal-noise degraded broadcast / Jensen step."""
import numpy as np
from scipy.optimize import brentq
def g(t): t=np.asarray(t,float); return np.where(t>0,(t+1)*np.log1p(t)-t*np.log(np.where(t>0,t,1)),0.0)
def ginv(s):
    if s<=0: return 0.0
    return brentq(lambda t: float(g(t))-s, 0, 1e9, xtol=1e-14, rtol=1e-14)
worst=np.inf; arg=None
for lam in [0.05,0.2,0.4,0.6,0.8,0.95]:
    for N in [0.0,0.01,0.1,0.5,1,3,10]:
        r=np.geomspace(1e-4,50,400)          # photon numbers -> u=g(r)
        u=g(r)
        phi=np.array([float(g(lam*x+(1-lam)*N)) for x in r])
        # second divided differences on nonuniform grid
        d1=(phi[1:]-phi[:-1])/(u[1:]-u[:-1])
        d2=(d1[1:]-d1[:-1])/((u[2:]-u[:-2])/2)
        m=d2.min()
        # relative to scale
        if m<worst: worst=m; arg=(lam,N)
        print(f"lam={lam} N={N}: min 2nd diff = {m:.3e}  (slope range {d1.min():.4f}..{d1.max():.4f})")
print("worst",worst,arg)
