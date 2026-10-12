import random
import graph_tool.all as gt
rng = random.Random(1)
n = 30
E = {(0, v) for v in range(1, n)}
E |= {(u, v) for u in range(1, n) for v in range(u + 1, n) if rng.random() < 0.15}
for persist in (False, True):
    g = gt.Graph(directed=False); g.add_vertex(n); g.add_edge_list(sorted(E))
    gt.seed_rng(1)
    print('persist', persist, 'calling random_rewire ...', flush=True)
    r = gt.random_rewire(g, model='configuration', n_iter=1, persist=persist)
    print('  returned; rejected moves =', r, flush=True)
