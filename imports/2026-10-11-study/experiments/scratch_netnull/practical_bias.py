"""How much does the retry-until-success bias move null-model means on real small networks?

Draw near-uniform samples with igraph's rewire (rejections counted; uniform stationary law) and reweight by the
exact stationary density of the NetworkX chains (importance weights, unbiased in the limit):
   double_edge_swap  : w(G) = deg_sw(G)
   random_reference  : w(G) = s/(1-(1-s)^K),  s = deg_sw/(2 P_disj), K=int(2m/(n-1))  [connectivity=False law]
deg_sw(G) = 2 P_disj - S2 + 3 T + 2 C4 (verified exactly in exhaustive_small.py).
Report shift of null mean in units of null SD (= change in the z-score the user would report).
"""
import sys, json, random, math
import numpy as np
import networkx as nx
import igraph as ig

SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 2000


def degsw_terms(A, d):
    m = int(d.sum() // 2)
    A2 = A @ A
    T = np.trace(A2 @ A) / 6
    S2 = ((A * np.outer(d - 1, d - 1)).sum()) / 2
    co = A2[np.triu_indices(len(d), 1)]
    C4 = (co * (co - 1) / 2).sum() / 2
    Pd = m * (m - 1) / 2 - (d * (d - 1) / 2).sum()
    return 2 * Pd - S2 + 3 * T + 2 * C4, Pd


def rich_club(A, d, k):
    idx = np.where(d > k)[0]
    Nk = len(idx)
    if Nk < 2:
        return np.nan
    Ek = A[np.ix_(idx, idx)].sum() / 2
    return 2 * Ek / (Nk * (Nk - 1))


def observables(g, d, ks):
    A = np.array(g.get_adjacency().data, dtype=float)
    obs = {"assortativity": g.assortativity_degree(directed=False),
           "transitivity": g.transitivity_undirected(),
           "avg_clustering": g.transitivity_avglocal_undirected(mode="zero")}
    for k in ks:
        obs[f"rich_club_k{k}"] = rich_club(A, d, k)
    return A, obs


def run(name, G):
    G = nx.convert_node_labels_to_integers(nx.Graph(G))
    G.remove_edges_from(nx.selfloop_edges(G))
    n, m = G.number_of_nodes(), G.number_of_edges()
    g = ig.Graph(n=n, edges=list(G.edges()))
    d = np.array(g.degree(), dtype=float)
    ks = sorted(set(int(x) for x in np.percentile(d, [80, 90, 95])))
    K = int(n * m / (n * (n - 1) / 2))
    random.seed(1)
    ig.set_random_number_generator(random)
    g.rewire(n=100 * m)  # burn-in
    W1, W2, OBS = [], [], []
    for _ in range(SAMPLES):
        g.rewire(n=10 * m)
        A, obs = observables(g, d, ks)
        w, Pd = degsw_terms(A, d)
        s = w / (2 * Pd)
        W1.append(w)
        W2.append(s / (1 - (1 - s) ** K) if K >= 1 else 1.0)
        OBS.append(obs)
    W1, W2 = np.array(W1), np.array(W2)
    res = {"network": name, "n": n, "m": m, "samples": SAMPLES, "K": K,
           "deg_sw_CV": round(float(W1.std() / W1.mean()), 4)}
    for key in OBS[0]:
        x = np.array([o[key] for o in OBS], dtype=float)
        ok = ~np.isnan(x)
        x, w1, w2 = x[ok], W1[ok], W2[ok]
        mu, sd = x.mean(), x.std()
        if sd == 0:
            continue
        mu1 = (x * w1).sum() / w1.sum()
        mu2 = (x * w2).sum() / w2.sum()
        # Monte Carlo SE of the shift, by batch means on (x*w/wbar - x)
        res[key] = {"null_mean_uniform": round(float(mu), 4), "null_sd": round(float(sd), 4),
                    "shift_double_edge_swap_in_sd": round(float((mu1 - mu) / sd), 3),
                    "shift_random_reference_in_sd": round(float((mu2 - mu) / sd), 3)}
    print(json.dumps(res), flush=True)
    return res


if __name__ == "__main__":
    nets = [("florentine_families", nx.florentine_families_graph()),
            ("karate_club", nx.karate_club_graph()),
            ("les_miserables", nx.les_miserables_graph()),
            ("davis_southern_women(projected-free bipartite)", nx.davis_southern_women_graph()),
            ("barabasi_albert_n200_m2", nx.barabasi_albert_graph(200, 2, seed=3)),
            ("powerlaw_cluster_n500", nx.powerlaw_cluster_graph(500, 3, 0.3, seed=4))]
    out = [run(nm, G) for nm, G in nets]
    json.dump(out, open("practical_bias.json", "w"), indent=1)
