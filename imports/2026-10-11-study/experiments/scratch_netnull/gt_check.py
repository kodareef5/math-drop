"""Run graph-tool's actual random_rewire (Ubuntu python3-graph-tool 2.59, same rewiring code as 2.98 modulo
cosmetic renames) on small degree vectors; compare empirical law with uniform.
Run with: python3.12 gt_check.py <samples>"""
import sys, json, random
import numpy as np
from scipy.stats import chisquare
import graph_tool.all as gt
sys.path.insert(0, '.')
from enum_graphs import enumerate_graphs, pair_index

SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 20000


def run(d, persist=False, sweep=True, n_iter=3):
    n = len(d)
    pidx = pair_index(n)
    gs = enumerate_graphs(d)
    index = {g: i for i, g in enumerate(gs)}
    E0 = [(i, j) for i in range(n) for j in range(i + 1, n) if gs[0] >> pidx[(i, j)] & 1]
    g = gt.Graph(directed=False)
    g.add_vertex(n)
    g.add_edge_list(E0)
    gt.seed_rng(7)
    c = np.zeros(len(gs))
    for _ in range(SAMPLES):
        gt.random_rewire(g, model="configuration", n_iter=n_iter, edge_sweep=sweep, persist=persist)
        mask = 0
        for e in g.edges():
            u, v = int(e.source()), int(e.target())
            mask |= 1 << pidx[(min(u, v), max(u, v))]
        c[index[mask]] += 1
    N = len(gs)
    p = c / c.sum()
    row = dict(d=list(d), persist=persist, edge_sweep=sweep, n_iter=n_iter, N=N,
               TV_uniform=round(0.5 * abs(p - 1 / N).sum(), 4),
               p_uniform=float('%.3g' % chisquare(c, np.full(N, c.sum() / N)).pvalue))
    print(json.dumps(row), flush=True)
    return row


if __name__ == "__main__":
    out = []
    for d in [(4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3)]:
        out.append(run(d, persist=False, sweep=True, n_iter=3))
        out.append(run(d, persist=False, sweep=False, n_iter=30))
    out.append(run((4, 4, 2, 2, 2, 2), persist=True, sweep=True, n_iter=3))
    json.dump(out, open("gt_check.json", "w"), indent=1)
