import numpy as np, json, gad_capacity as G
res={}
for N in [0.0,0.01,0.02,0.05,0.1,0.2,0.3,0.4,0.45,0.49]:
    best=(0,None); bestK=(0,None); relK=(0,None)
    for g in np.linspace(0.02,0.98,49):
        C=G.exact_capacity(g,N,grid=4001)[0]
        ug=G.fang_UG(g,N,nq=401,nd=200)
        k=min(G.C_beta(g,N),G.C_cov(g,N),G.C_fil(g,N) if N>0 else np.inf,G.C_EA(g,N))
        if ug-C>best[0]: best=(ug-C,g,C)
        if k-C>bestK[0]: bestK=(k-C,g,C)
        if (k-C)/C>relK[0]: relK=((k-C)/C,g)
    res[N]=dict(fang_maxgap=best[0],fang_at_gamma=best[1],C_there=best[2],ksw_maxgap=bestK[0],ksw_at_gamma=bestK[1],ksw_max_rel=relK[0])
    print(f"N={N:.2f}: Fang max gap {best[0]:.4f} bits at gamma={best[1]:.2f} (C={best[2]:.4f}, rel {best[0]/best[2]:.1%}); "
          f"KSW(no-EB) max gap {bestK[0]:.4f} at gamma={bestK[1]:.2f}; KSW max rel {relK[0]:.0%}",flush=True)
json.dump(res,open('gad_fine.json','w'),indent=1)
