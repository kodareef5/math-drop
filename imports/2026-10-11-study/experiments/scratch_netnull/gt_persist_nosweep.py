import sys, json, numpy as np
from scipy.stats import chisquare
import graph_tool.all as gt
sys.path.insert(0, '.')
from enum_graphs import enumerate_graphs, pair_index
from kernels_as_implemented import row_gt, stationary
d = (4, 4, 2, 2, 2, 2); n = len(d); pidx = pair_index(n); gs = enumerate_graphs(d); idx = {g: i for i, g in enumerate(gs)}
pi, _ = stationary([row_gt(g, n, pidx, d, True) for g in gs], gs)
E0 = [(i, j) for i in range(n) for j in range(i + 1, n) if gs[0] >> pidx[(i, j)] & 1]
g = gt.Graph(directed=False); g.add_vertex(n); g.add_edge_list(E0); gt.seed_rng(9)
c = np.zeros(len(gs))
for _ in range(30000):
    gt.random_rewire(g, model="configuration", n_iter=30, edge_sweep=False, persist=True)
    m = 0
    for e in g.edges():
        u, v = int(e.source()), int(e.target()); m |= 1 << pidx[(min(u, v), max(u, v))]
    c[idx[m]] += 1
p = c / c.sum(); N = len(gs)
print(json.dumps(dict(d=d, persist=True, edge_sweep=False, TV_uniform=round(0.5*abs(p-1/N).sum(),4), exact_pred_TV=round(float(0.5*abs(pi-1/N).sum()),4),
      p_uniform=float('%.3g'%chisquare(c, np.full(N, c.sum()/N)).pvalue), p_exact_pred=float('%.3g'%chisquare(c, pi*c.sum()).pvalue))))
