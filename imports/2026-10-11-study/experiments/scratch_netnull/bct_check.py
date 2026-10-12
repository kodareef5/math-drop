"""Actual bctpy randmio_und (port of BCT randmio_und.m) on d=(4,4,2,2,2,2): one outer iteration = up to
round(m/(n-1))+1 counted attempts, stop at first success. Predicted law pi ~ s/(1-(1-s)^K')."""
import json, math, numpy as np
from scipy.stats import chisquare
import bct
from enum_graphs import enumerate_graphs, pair_index, switch_neighbours
out = []
for d in [(4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3)]:
    n = len(d); pidx = pair_index(n); gs = enumerate_graphs(d); idx = {g: i for i, g in enumerate(gs)}
    deg = np.array([len(switch_neighbours(g, n, pidx)) for g in gs], float)
    m = sum(d) // 2
    Pd = math.comb(m, 2) - sum(math.comb(x, 2) for x in d)
    K = int(np.round(n * m / (n * (n - 1)))) + 1
    s = deg / (2 * Pd); w = s / (1 - (1 - s) ** K); pred = w / w.sum()
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if gs[0] >> pidx[(i, j)] & 1: A[i, j] = A[j, i] = 1
    c = np.zeros(len(gs)); rs = np.random.RandomState(3)
    for _ in range(20000):
        A, _ = bct.randmio_und(A, 2, seed=rs)
        msk = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j]: msk |= 1 << pidx[(i, j)]
        c[idx[msk]] += 1
    N = len(gs); p = c / c.sum()
    r = dict(d=list(d), lib="bctpy.randmio_und", K_attempts=K, TV_uniform=round(0.5 * abs(p - 1 / N).sum(), 4),
             p_uniform=float('%.3g' % chisquare(c, np.full(N, c.sum() / N)).pvalue),
             pred_TV_uniform=round(0.5 * abs(pred - 1 / N).sum(), 4),
             p_pred=float('%.3g' % chisquare(c, pred * c.sum()).pvalue))
    print(json.dumps(r)); out.append(r)
json.dump(out, open("bct_check.json", "w"), indent=1)
