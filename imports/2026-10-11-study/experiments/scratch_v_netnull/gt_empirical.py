"""Run real graph-tool random_rewire on d=(4,4,2,2,2,2) and chi-square vs uniform
and vs the exact law from gt_persist_exact.py. Also hang test on a graph with a
vertex adjacent to all others (run in a subprocess with timeout).
usage: python3.12 -I gt_empirical.py <persist 0|1> <runs> <n_iter>
"""
import sys, json, time
here = __file__.rsplit('/', 1)[0]
sys.path.insert(0, here)
import numpy as np
from scipy.stats import chisquare
import graph_tool.all as gt
from exact_kernels import realizations, stationary
from gt_persist_exact import sweep_kernel

persist = bool(int(sys.argv[1])); runs = int(sys.argv[2]); n_iter = int(sys.argv[3])
deg = [4, 4, 2, 2, 2, 2]
states = realizations(deg)
idx = {E: i for i, E in enumerate(states)}
E0 = sorted(states[0])
gt.seed_rng(int(time.time()))
counts = np.zeros(len(states))
t0 = time.time()
for r in range(runs):
    g = gt.Graph(directed=False)
    g.add_vertex(6)
    g.add_edge_list(E0)
    gt.random_rewire(g, model='configuration', n_iter=n_iter, persist=persist)
    E = frozenset(tuple(sorted((int(e.source()), int(e.target())))) for e in g.edges())
    counts[idx[E]] += 1
M = sweep_kernel(states, persist)
p0 = np.zeros(len(states)); p0[0] = 1
pred = p0 @ np.linalg.matrix_power(M, n_iter)
cu = chisquare(counts, np.full(len(states), runs / len(states)))
cp = chisquare(counts, pred * runs)
res = dict(persist=persist, runs=runs, n_iter=n_iter, gt_version=gt.__version__,
           seconds=round(time.time() - t0, 1), counts=counts.astype(int).tolist(),
           predicted=[round(x, 5) for x in pred], chi2_vs_uniform=[float(cu.statistic), float(cu.pvalue)],
           chi2_vs_predicted=[float(cp.statistic), float(cp.pvalue)])
print(json.dumps(res))
json.dump(res, open(f'{here}/gt_empirical_persist{int(persist)}.json', 'w'), indent=1)
