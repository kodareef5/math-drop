import numpy as np, gad_capacity as G
# superconducting transmon-like: f=5 GHz, T_eff=50 mK -> nu = 1/(1+exp(hf/kT))
h=6.62607015e-34; kB=1.380649e-23
for Teff in [0.05, 0.08]:
    nu=1/(1+np.exp(h*5e9/(kB*Teff)))
    for gam in [1e-3, 1e-2, 0.1, 0.3]:
        C,p=G.exact_capacity(gam,nu,grid=20001)
        ug=G.fang_UG(gam,nu,nq=801,nd=300)
        kb=G.C_beta(gam,nu)
        print(f"Teff={Teff*1e3:.0f}mK nu={nu:.4f} gamma={gam:g}: C={C:.6f} p*={p:.4f} Fang-gap={ug-C:.2e} Cbeta-gap={kb-C:.2e} 1-C={1-C:.2e}")
