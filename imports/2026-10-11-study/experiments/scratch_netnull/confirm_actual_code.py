"""Long runs of the ACTUAL library code on d=(4,4,2,2,2,2) (13 labelled realisations) and d=(3,3,3,3,3,3) (70),
with chi-square goodness-of-fit tests against (a) uniform and (b) the predicted law pi ~ deg_sw.
Successive states are correlated, so we thin: record every THIN steps (THIN chosen >> relaxation time,
which is ~1/0.08 = 12 attempts for these instances, see exact_stationary results)."""
import sys, json, random, math, time
import numpy as np
from scipy.stats import chisquare
import networkx as nx
import igraph as ig
import networkit as nk
from enum_graphs import enumerate_graphs, switch_neighbours, pair_index

SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
THIN = 60


def setup(d):
    n = len(d)
    pidx = pair_index(n)
    gs = enumerate_graphs(d)
    index = {g: i for i, g in enumerate(gs)}
    deg = np.array([len(switch_neighbours(g, n, pidx)) for g in gs], float)
    E0 = [(i, j) for i in range(n) for j in range(i + 1, n) if gs[0] >> pidx[(i, j)] & 1]
    return n, pidx, gs, index, deg, E0


def mask_of(edges, pidx):
    m = 0
    for u, v in edges:
        m |= 1 << pidx[(u, v)]
    return m


def test(name, c, deg):
    N = len(c)
    exp_u = np.full(N, c.sum() / N)
    exp_d = deg / deg.sum() * c.sum()
    pu = chisquare(c, exp_u).pvalue
    pd = chisquare(c, exp_d).pvalue
    p = c / c.sum()
    row = dict(lib=name, samples=int(c.sum()), TV_uniform=round(0.5 * abs(p - 1 / N).sum(), 4),
               TV_degsw=round(0.5 * abs(p - deg / deg.sum()).sum(), 4), p_uniform=float('%.3g' % pu),
               p_degsw=float('%.3g' % pd))
    print(json.dumps(row), flush=True)
    return row


def main(d):
    n, pidx, gs, index, deg, E0 = setup(d)
    out = []
    # NetworkX double_edge_swap: THIN successful swaps between records
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E0)
    rng = random.Random(11)
    c = np.zeros(len(gs))
    for _ in range(SAMPLES):
        nx.double_edge_swap(G, nswap=THIN // 4, max_tries=10**7, seed=rng)
        c[index[mask_of(G.edges(), pidx)]] += 1
    out.append(test("networkx.double_edge_swap", c, deg))
    # igraph rewire: THIN trials between records
    random.seed(12); ig.set_random_number_generator(random)
    g = ig.Graph(n=n, edges=E0)
    c = np.zeros(len(gs))
    for _ in range(SAMPLES):
        g.rewire(n=THIN, allowed_edge_types="simple")
        c[index[mask_of(g.get_edgelist(), pidx)]] += 1
    out.append(test("igraph rewire", c, deg))
    # NetworKit EdgeSwitchingInPlace: THIN attempts between records
    nk.engineering.setSeed(13, False)
    H = nk.Graph(n)
    for u, v in E0:
        H.addEdge(u, v)
    m = len(E0)
    es = nk.randomization.EdgeSwitchingInPlace(H, THIN / m)
    c = np.zeros(len(gs))
    for _ in range(SAMPLES):
        es.run()
        c[index[mask_of(((min(a, b), max(a, b)) for a, b in H.iterEdges()), pidx)]] += 1
    out.append(test("networkit EdgeSwitching", c, deg))
    # NetworKit GlobalCurveball: 2 global trades between records
    nk.engineering.setSeed(14, False)
    H = nk.Graph(n)
    for u, v in E0:
        H.addEdge(u, v)
    c = np.zeros(len(gs))
    for _ in range(SAMPLES):
        gc = nk.randomization.GlobalCurveball(H, 2, False, False)
        gc.run()
        H = gc.getGraph()
        c[index[mask_of(((min(a, b), max(a, b)) for a, b in H.iterEdges()), pidx)]] += 1
    out.append(test("networkit GlobalCurveball", c, deg))
    return out


if __name__ == "__main__":
    res = {}
    for d in [(4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3)]:
        print("==", d, flush=True)
        res[str(d)] = main(d)
    json.dump(res, open("confirm_actual_code.json", "w"), indent=1)
