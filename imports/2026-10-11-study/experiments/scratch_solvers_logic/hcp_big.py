import sys, time, numpy as np, networkx as nx
sys.path.insert(0, '.')
from barnette_hcp import random_map, flag_graph, hcp_lkh
rng = np.random.default_rng(11)
for npts in (60, 120):
    for rep in range(3):
        G, pos = random_map(npts, 0.4, rng); F = flag_graph(G, pos)
        for runs in (1, 10, 30):
            dt, bad, ok = hcp_lkh(F, runs=runs)
            print(f"flag |V|={F.number_of_nodes()} rep={rep} runs={runs}: {dt:.1f}s non-edges={bad}", flush=True)
            if bad == 0: break
