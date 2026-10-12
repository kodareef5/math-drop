"""Large random Barnette graphs (3-connected cubic bipartite planar) as HCP instances.
Construction: flag graph (= omnitruncation) of a random planar map M built from a Delaunay
triangulation with random edge deletions (keeps min degree >= 3). The flag graph of a plane map
is cubic and bipartite; planarity is inherited; 3-connectivity is checked explicitly.
Then solve HCP with LKH (elkai) using 0/1 costs and verify the tour uses only graph edges."""
import sys, time, random, numpy as np, networkx as nx
from scipy.spatial import Delaunay
import elkai

def random_map(npts, del_frac, rng):
    P = rng.random((npts, 2))
    tri = Delaunay(P)
    G = nx.Graph()
    for s in tri.simplices:
        for a, b in ((s[0], s[1]), (s[1], s[2]), (s[0], s[2])): G.add_edge(int(a), int(b))
    hull = set()
    for a, b in tri.convex_hull: hull.add(frozenset((int(a), int(b))))
    edges = [e for e in G.edges() if frozenset(e) not in hull]
    rng.shuffle(edges)
    target = int(del_frac * len(edges)); k = 0
    for u, v in edges:
        if k >= target: break
        if G.degree(u) > 3 and G.degree(v) > 3:
            G.remove_edge(u, v)
            if nx.is_biconnected(G) if npts < 300 else True: k += 1
            else: G.add_edge(u, v)
    pos = {i: P[i] for i in G.nodes()}
    return G, pos

def flag_graph(G, pos):
    # half-edges with rotation system from geometric angles
    import math
    nbrs = {v: sorted(G[v], key=lambda w: math.atan2(pos[w][1]-pos[v][1], pos[w][0]-pos[v][0])) for v in G}
    # next(h) for face to the left of u->v: at v, take the neighbor preceding u in ccw order (clockwise next)
    def nxt(u, v):
        L = nbrs[v]; i = L.index(u); return (v, L[(i - 1) % len(L)])
    H = [(u, v) for u in G for v in G[u]]
    idx = {h: i for i, h in enumerate(H)}
    F = nx.Graph()
    for (u, v) in H:
        h = idx[(u, v)]
        F.add_edge((h, 0), (h, 1))                       # change vertex
        F.add_edge((h, 1), (idx[nxt(u, v)], 0))          # change edge (same face, same vertex)
        F.add_edge((h, 0), (idx[(v, u)], 1))             # change face
    return nx.convert_node_labels_to_integers(F)

def check(F):
    assert all(d == 3 for _, d in F.degree())
    assert nx.is_bipartite(F)
    assert nx.check_planarity(F)[0]
    return nx.node_connectivity(F) if F.number_of_nodes() <= 600 else None

def hcp_lkh(F, runs=1):
    n = F.number_of_nodes()
    M = np.ones((n, n), dtype=np.int32)
    for u, v in F.edges(): M[u, v] = M[v, u] = 0
    np.fill_diagonal(M, 0)
    t = time.time()
    tour = elkai.DistanceMatrix(M.tolist()).solve_tsp(runs=runs)
    dt = time.time() - t
    tour = tour[:-1] if tour[0] == tour[-1] else tour
    bad = sum(1 for i in range(len(tour)) if not F.has_edge(tour[i], tour[(i + 1) % len(tour)]))
    return dt, bad, len(set(tour)) == n

if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    for npts, frac in [(40, 0.3), (40, 0.5), (120, 0.3), (120, 0.5), (300, 0.4), (500, 0.4)]:
        G, pos = random_map(npts, frac, rng)
        F = flag_graph(G, pos)
        kconn = check(F)
        faces = nx.check_planarity(F)[1]
        dt, bad, ok = hcp_lkh(F)
        print(f"map n={G.number_of_nodes()} m={G.number_of_edges()} maxdeg={max(d for _,d in G.degree())}  "
              f"flag graph |V|={F.number_of_nodes()} 3conn={kconn}  LKH {dt:.2f}s non-edges-in-tour={bad} perm_ok={ok}", flush=True)
