"""Actual (unpatched, pinned) networkx.random_reference(connectivity=False): chi-square vs uniform and vs the
predicted law pi ~ s/(1-(1-s)^K). Each sample = one call with niter=3 (3m outer iterations)."""
import json, math, random, numpy as np, networkx as nx
from scipy.stats import chisquare
from enum_graphs import enumerate_graphs, pair_index, switch_neighbours
out = []
for d in [(4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3)]:
    n = len(d); pidx = pair_index(n); gs = enumerate_graphs(d); idx = {g: i for i, g in enumerate(gs)}
    m = sum(d) // 2; K = int(n * m / (n * (n - 1) / 2)); Pd = math.comb(m, 2) - sum(math.comb(x, 2) for x in d)
    deg = np.array([len(switch_neighbours(g, n, pidx)) for g in gs], float); s = deg / (2 * Pd)
    w = s / (1 - (1 - s) ** K); pred = w / w.sum()
    E0 = [(i, j) for i in range(n) for j in range(i + 1, n) if gs[0] >> pidx[(i, j)] & 1]
    G = nx.Graph(E0); rng = random.Random(17); c = np.zeros(len(gs))
    for _ in range(30000):
        G = nx.random_reference(G, niter=3, connectivity=False, seed=rng)
        msk = 0
        for u, v in G.edges(): msk |= 1 << pidx[(min(u, v), max(u, v))]
        c[idx[msk]] += 1
    N = len(gs); p = c / c.sum()
    r = dict(d=list(d), lib="networkx.random_reference(conn=False) [pinned, unpatched]", K=K, TV_uniform=round(0.5 * abs(p - 1 / N).sum(), 4),
             pred_TV=round(float(0.5 * abs(pred - 1 / N).sum()), 4), p_uniform=float('%.3g' % chisquare(c, np.full(N, c.sum() / N)).pvalue),
             p_pred=float('%.3g' % chisquare(c, pred * c.sum()).pvalue))
    print(json.dumps(r)); out.append(r)
json.dump(out, open("rr_actual_check.json", "w"), indent=1)
