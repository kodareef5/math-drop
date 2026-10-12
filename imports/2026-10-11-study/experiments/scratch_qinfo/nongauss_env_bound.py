"""Upper bound on classical capacity of a beam splitter (transmissivity eta) whose environment is an arbitrary
non-Gaussian state rho_E (iid per mode), input mean photon number N:
   C <= g(eta*N + (1-eta)*N_E) - Smin_lower,
 König-Smith qEPI (exponential, DMG 2014 any eta):  Smin >= log(eta + (1-eta) e^{S_E})
 EPnI (OpenAI 2026, thm:epni, input entropy >= 0):   Smin >= g((1-eta) g^{-1}(S_E))
Both in nats; reported in bits. Example environment: rho_E = (1-p)|0><0| + p|1><1|."""
import numpy as np
from scipy.optimize import brentq
def g(t): return 0.0 if t<=0 else (t+1)*np.log1p(t)-t*np.log(t)
def ginv(s): return 0.0 if s<=0 else brentq(lambda t:g(t)-s,0,1e9,xtol=1e-15)
def h(p): return 0.0 if p in (0,1) else -p*np.log(p)-(1-p)*np.log(1-p)
L2=np.log(2)
for eta in [0.5,0.9]:
  for N in [1.0,10.0]:
    for p in [0.1,0.3,0.5]:
        SE=h(p); NE=p
        smax=g(eta*N+(1-eta)*NE)
        ks=np.log(eta+(1-eta)*np.exp(SE)); ep=g((1-eta)*ginv(SE))
        print(f"eta={eta} N={N} p={p}: Smax={smax/L2:.4f}b  C<= {(smax-ks)/L2:.4f}b (qEPI)  C<= {(smax-ep)/L2:.4f}b (EPnI)  improvement={(ep-ks)/L2:.4f}b")
