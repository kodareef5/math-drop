"""Exact stationary laws of degree-preserving swap chains AS IMPLEMENTED, on small degree sequences.

Kernels (derived from the pinned source; see netnull.md for line refs):
  * paper / igraph rewire / NetworKit EdgeSwitching / graph-tool random_rewire(persist=False):
      every switch neighbour G' gets the same probability c per attempt, rejections hold
      -> symmetric kernel -> uniform stationary law.
  * NetworkX double_edge_swap (and rich_club_coefficient(normalized=True)):
      one counted step = "repeat attempts until one succeeds"; each switch neighbour is
      equally likely per attempt (1/m^2), so the counted-step chain is the jump chain:
      P(G,G') = 1/deg_sw(G)  ->  pi(G) proportional to deg_sw(G).
  * NetworkX random_reference(connectivity=False/True):
      one outer step = up to K=int(2m/(n-1)) counted attempts, stop at first success.
      Attempts with degenerate draws (shared vertex) are redrawn without counting, so per counted
      attempt each valid neighbour has prob 1/(2 P_disj). With s(G)=deg(G)/(2 P_disj),
      P(G,G') = (1-(1-s)^K)/deg(G) ... i.e. w(G)/(2P_disj) with w=(1-(1-s)^K)/s,
      so pi(G) proportional to s(G)/(1-(1-s(G))^K)  (variable `w` in the code is this weight).
      With connectivity=True the state space is connected realisations and deg counts only
      switches whose result is connected.
"""
import sys, math, itertools, json
import numpy as np
from enum_graphs import enumerate_graphs, switch_neighbours, pair_index, is_connected


def analyse(d, verbose=True):
    n = len(d)
    m = sum(d) // 2
    pidx = pair_index(n)
    graphs = enumerate_graphs(d)
    N = len(graphs)
    index = {g: i for i, g in enumerate(graphs)}
    nbrs = [switch_neighbours(g, n, pidx) for g in graphs]
    deg = np.array([len(x) for x in nbrs], dtype=float)
    # sanity: neighbours distinct and symmetric
    for i, g in enumerate(graphs):
        assert len(set(nbrs[i])) == len(nbrs[i])
        for h in nbrs[i]:
            assert g in switch_neighbours(h, n, pidx)
    Pdisj = math.comb(m, 2) - sum(math.comb(x, 2) for x in d)
    K = int(n * m / (n * (n - 1) / 2))
    u = np.full(N, 1.0 / N)

    def tv(p, q):
        return 0.5 * np.abs(p - q).sum()

    res = {"d": list(d), "n": n, "m": m, "N": N}
    # NetworkX double_edge_swap
    pi_des = deg / deg.sum()
    res["des_tv"] = tv(pi_des, u)
    res["des_ratio"] = deg.max() / deg.min()
    # random_reference connectivity=False
    s = deg / (2 * Pdisj)
    w = s / (1 - (1 - s) ** K)
    pi_rr = w / w.sum()
    res["K"] = K
    res["rr_noconn_tv"] = tv(pi_rr, u)
    res["rr_noconn_ratio"] = w.max() / w.min()
    # random_reference connectivity=True
    conn = np.array([is_connected(g, n) for g in graphs])
    if conn.sum() >= 2:
        C = [i for i in range(N) if conn[i]]
        degc = np.array([sum(1 for h in nbrs[i] if conn[index[h]]) for i in C], dtype=float)
        sc = degc / (2 * Pdisj)
        wc = sc / (1 - (1 - sc) ** K)
        pic = wc / wc.sum()
        uc = np.full(len(C), 1.0 / len(C))
        res["Nconn"] = len(C)
        res["rr_conn_tv"] = tv(pic, uc)
        res["rr_conn_ratio"] = wc.max() / wc.min()
        # is the connected switch graph connected (irreducible)?
        seen = {C[0]}
        st = [C[0]]
        while st:
            i = st.pop()
            for h in nbrs[i]:
                j = index[h]
                if conn[j] and j not in seen:
                    seen.add(j); st.append(j)
        res["conn_irreducible"] = len(seen) == len(C)
    # exact spectral gaps: edge-pair proposal chain with c = 1/m^2 (NetworKit/NetworkX-style draws, rejections counted)
    L = np.zeros((N, N))
    for i in range(N):
        for h in nbrs[i]:
            L[i, index[h]] -= 1
        L[i, i] = deg[i]
    ev = np.sort(np.linalg.eigvalsh(L))
    lamL = ev[1] if N > 1 else float('nan')
    res["gap_L"] = lamL
    res["gap_L_bound"] = 1.0 / (2 * n * n)
    res["gap_edgepair_exact"] = lamL / m**2
    res["gap_edgepair_bound"] = 1.0 / (2 * n * n * m * m)
    # paper's lazy 4-vertex chain: I - P = L/(12 C(n,4)), lazy
    res["gap_paper_exact"] = lamL / (12 * math.comb(n, 4))
    res["gap_paper_bound"] = 1.0 / (24 * n * n * math.comb(n, 4))
    if verbose:
        print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in res.items()}))
    return res, graphs, deg, nbrs


def curveball_gap(d):
    """Exact spectral gap of the uniform-random-pair undirected Curveball heat bath P = mean_a E_a."""
    n = len(d)
    graphs = enumerate_graphs(d)
    N = len(graphs)
    index = {g: i for i, g in enumerate(graphs)}
    pidx = pair_index(n)
    P = np.zeros((N, N))
    pairs = list(itertools.combinations(range(n), 2))
    for (a, b) in pairs:
        # fibres: fix everything except, for each w not in {a,b} with exactly one neighbour in {a,b},
        # which endpoint it attaches to. Key = graph with those singleton edges removed + counts.
        fib = {}
        for i, g in enumerate(graphs):
            key = g
            for w in range(n):
                if w in (a, b):
                    continue
                ea = g >> pidx[(a, w)] & 1
                eb = g >> pidx[(b, w)] & 1
                if ea != eb:
                    key &= ~(1 << pidx[(a, w)])
                    key &= ~(1 << pidx[(b, w)])
            fib.setdefault(key, []).append(i)
        for key, members in fib.items():
            for i in members:
                for j in members:
                    P[i, j] += 1.0 / len(members) / len(pairs)
    assert np.allclose(P.sum(1), 1) and np.allclose(P, P.T)
    ev = np.sort(np.linalg.eigvalsh(P))[::-1]
    return 1 - ev[1], ev[-1], 1.0 / math.comb(n, 2)


if __name__ == "__main__":
    seqs = [
        (3, 3, 2, 2, 2, 2),
        (3, 2, 2, 2, 2, 1),
        (4, 3, 3, 2, 2, 2),
        (3, 3, 3, 3, 2, 2),
        (2, 2, 2, 2, 2, 2, 2),
        (3, 3, 3, 3, 3, 3),
        (4, 2, 2, 2, 2, 2, 2),
        (3, 3, 3, 3, 2, 2, 2, 2),
        (4, 4, 3, 3, 2, 2, 1, 1),
        (5, 3, 3, 2, 2, 2, 2, 1),
        (6, 3, 2, 2, 2, 2, 2, 1),
    ]
    rows = []
    for d in seqs:
        r, *_ = analyse(d)
        g, lmin, gb = curveball_gap(d)
        r["cb_gap_exact"], r["cb_lmin"], r["cb_gap_bound"] = g, lmin, gb
        print("   curveball gap", round(g, 4), "lambda_min", round(lmin, 4), "bound", round(gb, 4))
        rows.append(r)
    json.dump(rows, open("exact_stationary_results.json", "w"), indent=1, default=float)
