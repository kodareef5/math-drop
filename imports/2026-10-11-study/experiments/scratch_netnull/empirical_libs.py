"""Run the ACTUAL library code (NetworkX, python-igraph C core, NetworKit) as a long chain on small degree
sequences, record the labelled graph after every step, and compare the empirical occupation law with
(a) uniform and (b) the predicted law pi ~ deg_sw for retry-until-success.

Usage: python3 empirical_libs.py <steps>
"""
import sys, time, json, math, random
import numpy as np
import networkx as nx
import igraph as ig
import networkit as nk
from enum_graphs import enumerate_graphs, switch_neighbours, pair_index

STEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 100000


def mask_of(edges, pidx):
    m = 0
    for u, v in edges:
        m |= 1 << pidx[(u, v)]
    return m


def setup(d):
    n = len(d)
    pidx = pair_index(n)
    gs = enumerate_graphs(d)
    index = {g: i for i, g in enumerate(gs)}
    deg = np.array([len(switch_neighbours(g, n, pidx)) for g in gs], float)
    E0 = []
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if gs[0] >> k & 1:
                E0.append((i, j))
            k += 1
    return n, pidx, gs, index, deg, E0


def report(name, counts, deg, extra=None):
    N = len(counts)
    p = counts / counts.sum()
    u = np.full(N, 1 / N)
    pr = deg / deg.sum()
    tvu = 0.5 * np.abs(p - u).sum()
    tvp = 0.5 * np.abs(p - pr).sum()
    # noise floor: TV of a multinomial sample from the predicted law of the same size (iid), rough guide
    row = {"lib": name, "TV_to_uniform": round(tvu, 4), "TV_to_deg_sw_law": round(tvp, 4),
           "corr(freq,deg_sw)": round(float(np.corrcoef(p, deg)[0, 1]), 3)}
    if extra:
        row.update(extra)
    print(json.dumps(row), flush=True)
    return row


def run_networkx_des(d, seed=1):
    n, pidx, gs, index, deg, E0 = setup(d)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E0)
    rng = random.Random(seed)
    c = np.zeros(len(gs))
    for _ in range(STEPS):
        nx.double_edge_swap(G, nswap=1, max_tries=10**6, seed=rng)
        c[index[mask_of(G.edges(), pidx)]] += 1
    return report("networkx.double_edge_swap", c, deg)


def run_networkx_rr(d, seed=2):
    n, pidx, gs, index, deg, E0 = setup(d)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E0)
    m = len(E0)
    rng = random.Random(seed)
    c = np.zeros(len(gs))
    # niter=1 means m outer iterations; we want one outer iteration per recorded state, so call with a
    # graph whose niter*nedges... instead we record after each call with niter=1 (m outer iterations):
    # stationary law is unaffected by sub-sampling.
    for _ in range(STEPS // m):
        G = nx.random_reference(G, niter=1, connectivity=False, seed=rng)
        c[index[mask_of(G.edges(), pidx)]] += 1
    # predicted law for random_reference
    Pd = math.comb(m, 2) - sum(math.comb(x, 2) for x in d)
    K = int(n * m / (n * (n - 1) / 2))
    s = deg / (2 * Pd)
    w = s / (1 - (1 - s) ** K)
    N = len(gs)
    p = c / c.sum()
    return report("networkx.random_reference(conn=False)", c, deg,
                  {"K": K, "TV_to_rr_law": round(0.5 * np.abs(p - w / w.sum()).sum(), 4),
                   "pred_TV_rr_vs_uniform": round(0.5 * np.abs(w / w.sum() - 1 / N).sum(), 4)})


def run_igraph(d, seed=3):
    n, pidx, gs, index, deg, E0 = setup(d)
    random.seed(seed)
    ig.set_random_number_generator(random)
    g = ig.Graph(n=n, edges=E0)
    c = np.zeros(len(gs))
    for _ in range(STEPS):
        g.rewire(n=1, allowed_edge_types="simple")
        c[index[mask_of(g.get_edgelist(), pidx)]] += 1
    return report("igraph.Graph.rewire (C igraph_rewire)", c, deg)


def run_igraph_adjlist(d, seed=4):
    """n>=10 triggers the adjacency-list code path; record every 10 trials."""
    n, pidx, gs, index, deg, E0 = setup(d)
    random.seed(seed)
    ig.set_random_number_generator(random)
    g = ig.Graph(n=n, edges=E0)
    c = np.zeros(len(gs))
    for _ in range(STEPS // 10):
        g.rewire(n=10, allowed_edge_types="simple")
        c[index[mask_of(g.get_edgelist(), pidx)]] += 1
    return report("igraph.Graph.rewire n=10 (adjlist path)", c, deg)


def nk_graph(n, E):
    G = nk.Graph(n)
    for u, v in E:
        G.addEdge(u, v)
    return G


def run_networkit_es(d, seed=5):
    n, pidx, gs, index, deg, E0 = setup(d)
    nk.engineering.setSeed(seed, False)
    G = nk_graph(n, E0)
    m = len(E0)
    es = nk.randomization.EdgeSwitchingInPlace(G, 1.0 / m)  # ceil(m * 1/m) = 1 attempt per run()
    c = np.zeros(len(gs))
    for _ in range(STEPS):
        es.run()
        c[index[mask_of(((min(u, v), max(u, v)) for u, v in G.iterEdges()), pidx)]] += 1
    return report("networkit.EdgeSwitchingInPlace", c, deg)


def run_networkit_cb(d, seed=6):
    n, pidx, gs, index, deg, E0 = setup(d)
    nk.engineering.setSeed(seed, False)
    rng = random.Random(seed)
    G = nk_graph(n, E0)
    c = np.zeros(len(gs))
    cb = nk.randomization.Curveball(G)
    steps = STEPS // 5
    for _ in range(steps):
        u, v = rng.sample(range(n), 2)
        cb.run([(u, v)])
        H = cb.getGraph()
        c[index[mask_of(((min(a, b), max(a, b)) for a, b in H.iterEdges()), pidx)]] += 1
    return report("networkit.Curveball (uniform random pair trades)", c, deg)


def run_networkit_gcb(d, seed=7):
    n, pidx, gs, index, deg, E0 = setup(d)
    nk.engineering.setSeed(seed, False)
    G = nk_graph(n, E0)
    c = np.zeros(len(gs))
    for _ in range(STEPS // 20):
        g = nk.randomization.GlobalCurveball(G, 1, False, False)
        g.run()
        G = g.getGraph()
        c[index[mask_of(((min(a, b), max(a, b)) for a, b in G.iterEdges()), pidx)]] += 1
    return report("networkit.GlobalCurveball (1 global trade)", c, deg)


if __name__ == "__main__":
    seqs = [(4, 3, 3, 3, 1, 1, 1), (4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3)]
    out = {}
    for d in seqs:
        print("== degree sequence", d, "N =", len(enumerate_graphs(d)), flush=True)
        rows = []
        for f in (run_networkx_des, run_networkx_rr, run_igraph, run_igraph_adjlist, run_networkit_es,
                  run_networkit_cb, run_networkit_gcb):
            t = time.time()
            r = f(d)
            r["sec"] = round(time.time() - t, 1)
            rows.append(r)
        out[str(d)] = rows
    json.dump(out, open(f"empirical_libs_{STEPS}.json", "w"), indent=1)
