"""Run the real library functions many times on d=[4,4,2,2,2,2] (13 labeled
realizations) and chi-square the empirical law vs uniform and vs the exact
predicted stationary law from exact_kernels.py.

usage: python3 empirical_lib.py <which> <runs> [bctpy_repo_path]
which in {nx_des, nx_rr, bct, nx_rr_sparse}
"""
import sys, json, time
import numpy as np
from scipy.stats import chisquare
here = __file__.rsplit('/', 1)[0]
sys.path.insert(0, here)
from exact_kernels import report, realizations

which = sys.argv[1]
runs = int(sys.argv[2])
deg = [4, 4, 2, 2, 2, 2]
n = len(deg); m = sum(deg) // 2
states = realizations(deg)
idx = {E: i for i, E in enumerate(states)}
E0 = states[0]


def key_of_edges(edges):
    return frozenset(tuple(sorted(e)) for e in edges)


counts = np.zeros(len(states))
rng = np.random.default_rng(12345)
t0 = time.time()
if which in ('nx_des', 'nx_rr'):
    import networkx as nx
    print('networkx', nx.__version__, nx.__file__)
    for r in range(runs):
        G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E0)
        sd = int(rng.integers(2**31))
        if which == 'nx_des':
            nx.double_edge_swap(G, nswap=60, max_tries=10**6, seed=sd)
            H = G
            pred_chain, T = 'nx_des', None
        else:
            H = nx.random_reference(G, niter=10, connectivity=True, seed=sd)
            pred_chain, T = 'nx_rr', int(2 * m / (n - 1))
        counts[idx[key_of_edges(H.edges())]] += 1
elif which == 'bct':
    sys.path.insert(0, sys.argv[3])
    import bct
    print('bct from', bct.__file__)
    A0 = np.zeros((n, n), int)
    for a, b in E0:
        A0[a, b] = A0[b, a] = 1
    for r in range(runs):
        R, eff = bct.randmio_und(A0, 10, seed=int(rng.integers(2**31)))
        E = [(a, b) for a in range(n) for b in range(a + 1, n) if R[a, b]]
        counts[idx[key_of_edges(E)]] += 1
    pred_chain, T = 'bct', int(np.round(m / (n - 1))) + 1

out, _, _, pi = report(deg, pred_chain, pred_chain == 'nx_rr', T)
exp_u = np.full(len(states), runs / len(states))
cu = chisquare(counts, exp_u)
cp = chisquare(counts, pi * runs)
res = dict(which=which, runs=runs, seconds=round(time.time() - t0, 1),
           counts=counts.astype(int).tolist(),
           predicted=[round(x, 5) for x in pi.tolist()],
           empirical=[round(x, 5) for x in (counts / runs).tolist()],
           chi2_vs_uniform=dict(stat=float(cu.statistic), p=float(cu.pvalue)),
           chi2_vs_predicted=dict(stat=float(cp.statistic), p=float(cp.pvalue)),
           emp_max_over_min=float(counts.max() / counts.min()),
           pred_TV=out['TV_stationary_vs_uniform'])
print(json.dumps(res))
json.dump(res, open(f'{here}/empirical_{which}.json', 'w'), indent=1)
