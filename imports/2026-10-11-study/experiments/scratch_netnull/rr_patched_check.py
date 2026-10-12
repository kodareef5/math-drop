import json, random, numpy as np, networkx as nx
from scipy.stats import chisquare
from enum_graphs import enumerate_graphs, pair_index, is_connected
out = []
for d, conn in [((4, 4, 2, 2, 2, 2), False), ((3, 3, 3, 3, 3, 3), False), ((4, 4, 3, 3, 2, 2, 2), True)]:
    n = len(d); pidx = pair_index(n)
    gs = [g for g in enumerate_graphs(d) if (is_connected(g, n) or not conn)]; idx = {g: i for i, g in enumerate(gs)}
    E0 = [(i, j) for i in range(n) for j in range(i + 1, n) if gs[0] >> pidx[(i, j)] & 1]
    G = nx.Graph(E0); rng = random.Random(8); c = np.zeros(len(gs))
    for _ in range(15000):
        G = nx.random_reference(G, niter=1, connectivity=conn, seed=rng)
        m = 0
        for u, v in G.edges(): m |= 1 << pidx[(min(u, v), max(u, v))]
        c[idx[m]] += 1
    N = len(gs); p = c / c.sum()
    r = dict(d=list(d), connectivity=conn, N=N, patched_TV_uniform=round(0.5 * abs(p - 1 / N).sum(), 4),
             p_uniform=float('%.3g' % chisquare(c, np.full(N, c.sum() / N)).pvalue))
    print(json.dumps(r)); out.append(r)
json.dump(out, open("rr_patched_check.json", "w"), indent=1)
