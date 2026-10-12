import json, random, numpy as np, networkit as nk
from scipy.stats import chisquare
from enum_graphs import enumerate_graphs, pair_index
out=[]
for d in [(4,4,2,2,2,2),(3,3,3,3,3,3)]:
    n=len(d); pidx=pair_index(n); gs=enumerate_graphs(d); idx={g:i for i,g in enumerate(gs)}
    E0=[(i,j) for i in range(n) for j in range(i+1,n) if gs[0]>>pidx[(i,j)]&1]
    nk.engineering.setSeed(21, False); rng=random.Random(21)
    G=nk.Graph(n)
    for u,v in E0: G.addEdge(u,v)
    c=np.zeros(len(gs))
    for _ in range(15000):
        cb=nk.randomization.Curveball(G)
        cb.run([tuple(rng.sample(range(n),2)) for _ in range(12)])
        G=cb.getGraph()
        m=0
        for a,b in G.iterEdges(): m|=1<<pidx[(min(a,b),max(a,b))]
        c[idx[m]]+=1
    N=len(gs); p=c/c.sum()
    r=dict(d=list(d),lib="networkit.Curveball uniform trades",samples=int(c.sum()),TV_uniform=round(0.5*abs(p-1/N).sum(),4),p_uniform=float('%.3g'%chisquare(c,np.full(N,c.sum()/N)).pvalue))
    print(json.dumps(r)); out.append(r)
json.dump(out,open("nk_curveball_check.json","w"),indent=1)
