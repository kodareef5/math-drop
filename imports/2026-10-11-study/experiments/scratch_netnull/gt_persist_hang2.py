import sys
import graph_tool.all as gt
sys.path.insert(0,'.')
from enum_graphs import edges_of
E=[(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 3), (4, 5)]
for seed in range(200):
    g=gt.Graph(directed=False); g.add_vertex(6); g.add_edge_list(E)
    gt.seed_rng(seed)
    print('seed', seed, flush=True)
    gt.random_rewire(g, model='configuration', n_iter=1, edge_sweep=False, persist=True)
print('all returned')
