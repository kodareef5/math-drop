"""Hang test: graph with a vertex adjacent to all others (ego network). Every edge
incident to the hub has no valid switch partner (any switch would create hub-x
where x is already a neighbour, or a self-loop), so persist=True loops forever."""
import sys, time
import graph_tool.all as gt
persist = bool(int(sys.argv[1]))
g = gt.random_graph(28, lambda: 3, directed=False)  # 28-vertex 3-regular (+hub = 29 vertices)
hub = g.add_vertex()
for v in range(28):
    g.add_edge(hub, g.vertex(v))
t = time.time()
nfail = gt.random_rewire(g, model='configuration', n_iter=1, persist=persist, ret_fail=True)
print('persist', persist, 'returned after', round(time.time() - t, 3), 's; failed attempts:', nfail, flush=True)
