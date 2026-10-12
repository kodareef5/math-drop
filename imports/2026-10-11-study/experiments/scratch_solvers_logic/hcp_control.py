import sys, time, numpy as np, networkx as nx, elkai
sys.path.insert(0, '.')
from barnette_hcp import random_map, flag_graph, hcp_lkh
rng = np.random.default_rng(7)
def planted_cubic(n, rng):
    # random Hamiltonian cycle + random perfect matching of chords (simple graph), cubic, Hamiltonian by construction
    while True:
        perm = rng.permutation(n); G = nx.cycle_graph(n); G = nx.relabel_nodes(G, {i: int(perm[i]) for i in range(n)})
        p = rng.permutation(n); ok = True
        for i in range(0, n, 2):
            u, v = int(p[i]), int(p[i+1])
            if G.has_edge(u, v): ok = False; break
            G.add_edge(u, v)
        if ok: return G
for npts, frac in [(120, 0.4), (120, 0.4)]:
    G, pos = random_map(npts, frac, rng); F = flag_graph(G, pos); N = F.number_of_nodes()
    for runs in (1, 5):
        dt, bad, ok = hcp_lkh(F, runs=runs)
        print(f"Barnette flag graph |V|={N} planar={nx.check_planarity(F)[0]} runs={runs}: {dt:.1f}s non-edges={bad}", flush=True)
    P = planted_cubic(N, rng)
    for runs in (1, 5):
        dt, bad, ok = hcp_lkh(P, runs=runs)
        print(f"planted random cubic   |V|={N} runs={runs}: {dt:.1f}s non-edges={bad}", flush=True)
