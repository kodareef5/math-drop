"""Exact transition kernels obtained by enumerating every random choice each library's code makes in one
step (ideal RNG), on all labelled graphs with a small degree vector. Then exact stationary law vs uniform.

Per-attempt enumerations (line refs in netnull.md):
 NX_DES   networkx double_edge_swap, nswap=1: (ui,xi) iid degree-weighted; ui==xi -> redraw; v,y uniform
          neighbours; v==y -> redraw; if x!~u and y!~v -> {ux,vy}; else failed attempt; loop until success.
 NX_RR    networkx random_reference(connectivity=False), one outer iteration: up to K=int(2m/(n-1)) counted
          attempts, degenerate draws redrawn uncounted; new edges {ad, cb}; stop at first success.
 IG       igraph_i_rewire, one trial: e0 uniform, e1 uniform != e0; with prob 1/2 flip (c,d); checks; {ad, cb}.
          Edge storage orientation (a,b) is taken as stored (i<j). The adjlist path can flip stored orientations
          over time; this does not matter: for each unordered edge pair, each of its two switches gets
          probability 2 * 1/(m(m-1)) * 1/2 = 1/(m(m-1)) whatever the stored orientations are.
 NK_ES    NetworKit EdgeSwitchingInPlace, one attempt: s1,s2 iid degree-weighted; t1,t2 uniform neighbours;
          reject s2==t1 or s2~t1 or t1==t2 or s1==t2 or s1~t2; else {s1 t2, s2 t1}.
 GT       graph-tool random_rewire(model='configuration', edge_sweep=False, persist=False), one iteration:
          e uniform; et uniform (et==e fail); coins for orientation of e and et; reject s==tt or ts==t,
          or s~tt or ts~t; else {s tt, ts t}  (acceptance a=0 for simple undirected configuration model).
 GT_P     same with persist=True: repeat (et, coins) for the same e until success.
"""
import itertools, math, json, sys
from fractions import Fraction
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from enum_graphs import enumerate_graphs, pair_index, edges_of


def adjsets(mask, n):
    A = [set() for _ in range(n)]
    for i, j in edges_of(mask, n):
        A[i].add(j); A[j].add(i)
    return A


def apply(mask, pidx, rem, add):
    for (u, v) in rem:
        mask &= ~(1 << pidx[(u, v)])
    for (u, v) in add:
        mask |= 1 << pidx[(u, v)]
    return mask


def row_nx_des(mask, n, pidx, d):
    A = adjsets(mask, n)
    D = sum(d)
    out = {}
    for u in range(n):
        for x in range(n):
            if u == x or d[u] == 0 or d[x] == 0:
                continue
            pux = Fraction(d[u], D) * Fraction(d[x], D)
            for v in A[u]:
                for y in A[x]:
                    if v == y:
                        continue
                    p = pux / (d[u] * d[x])
                    if x not in A[u] and y not in A[v]:
                        g2 = apply(mask, pidx, [(u, v), (x, y)], [(u, x), (v, y)])
                        out[g2] = out.get(g2, 0) + p
    tot = sum(out.values())
    return {g: p / tot for g, p in out.items()}  # retry until success


def attempt_rr(mask, n, pidx, d):
    """One counted attempt of random_reference conditional on a non-degenerate draw."""
    A = adjsets(mask, n)
    D = sum(d)
    succ = {}
    tot = 0
    for a in range(n):
        for c in range(n):
            if a == c or d[a] == 0 or d[c] == 0:
                continue
            pac = Fraction(d[a], D) * Fraction(d[c], D)
            for b in A[a]:
                for dd in A[c]:
                    if b in (a, c, dd) or dd in (a, b, c):
                        continue
                    p = pac / (d[a] * d[c])
                    tot += p
                    if dd not in A[a] and b not in A[c]:
                        g2 = apply(mask, pidx, [(a, b), (c, dd)], [(a, dd), (c, b)])
                        succ[g2] = succ.get(g2, 0) + p
    return {g: p / tot for g, p in succ.items()}


def row_nx_rr(mask, n, pidx, d, K):
    succ = attempt_rr(mask, n, pidx, d)
    s = sum(succ.values())
    if K == 0:
        return {mask: Fraction(1)}
    reach = 1 - (1 - s) ** K
    out = {g: p / s * reach for g, p in succ.items()}
    out[mask] = out.get(mask, 0) + (1 - reach)
    return out


def row_igraph(mask, n, pidx, d):
    E = edges_of(mask, n)
    m = len(E)
    A = adjsets(mask, n)
    out = {}
    for i0 in range(m):
        for i1 in range(m):
            if i0 == i1:
                continue
            for flip in (0, 1):
                p = Fraction(1, m * (m - 1) * 2)
                a, b = E[i0]
                c, dd = E[i1]
                if flip:
                    c, dd = dd, c
                ok = not (a == c or b == dd) and (a != dd and b != c)
                if ok and dd not in A[a] and b not in A[c]:
                    g2 = apply(mask, pidx, [(a, b), (c, dd)], [(a, dd), (c, b)])
                else:
                    g2 = mask
                out[g2] = out.get(g2, 0) + p
    return out


def row_nk(mask, n, pidx, d):
    A = adjsets(mask, n)
    D = sum(d)
    out = {}
    for s1 in range(n):
        for s2 in range(n):
            if d[s1] == 0 or d[s2] == 0:
                continue
            for t1 in A[s1]:
                for t2 in A[s2]:
                    p = Fraction(d[s1], D) * Fraction(d[s2], D) / (d[s1] * d[s2])
                    if s2 == t1 or t1 in A[s2] or t1 == t2 or s1 == t2 or t2 in A[s1]:
                        g2 = mask
                    else:
                        g2 = apply(mask, pidx, [(s1, t1), (s2, t2)], [(s1, t2), (s2, t1)])
                    out[g2] = out.get(g2, 0) + p
    return out


def gt_edge_attempts(mask, n, pidx, e, E, A):
    """For fixed edge index e: outcomes over et uniform and 2 coins; returns dict g2->prob incl. holding."""
    m = len(E)
    out = {}
    for et in range(m):
        for ce in (0, 1):
            for ct in (0, 1):
                p = Fraction(1, 4 * m)
                if et == e:
                    out[mask] = out.get(mask, 0) + p
                    continue
                s, t = E[e] if not ce else E[e][::-1]
                ts, tt = E[et] if not ct else E[et][::-1]
                if s == tt or ts == t or tt in A[s] or t in A[ts]:
                    out[mask] = out.get(mask, 0) + p
                    continue
                g2 = apply(mask, pidx, [E[e], E[et]], [(s, tt), (ts, t)])
                out[g2] = out.get(g2, 0) + p
    return out


def row_gt(mask, n, pidx, d, persist=False):
    E = edges_of(mask, n)
    m = len(E)
    A = adjsets(mask, n)
    out = {}
    for e in range(m):
        r = gt_edge_attempts(mask, n, pidx, e, E, A)
        if persist:
            hold = r.get(mask, 0)
            if hold == 1:
                return None  # infinite loop: edge e has no valid partner
            r = {g: p / (1 - hold) for g, p in r.items() if g != mask}
        for g, p in r.items():
            out[g] = out.get(g, 0) + p / m
    return out


def stationary(rows, graphs):
    N = len(graphs)
    idx = {g: i for i, g in enumerate(graphs)}
    I, J, V = [], [], []
    for i, r in enumerate(rows):
        for g, p in r.items():
            I.append(i); J.append(idx[g]); V.append(float(p))
    P = sps.csr_matrix((V, (I, J)), shape=(N, N))
    assert np.allclose(np.asarray(P.sum(1)).ravel(), 1)
    # solve pi (P - I) = 0, sum pi = 1
    M = (P.T - sps.identity(N)).tolil()
    M[0, :] = 1
    b = np.zeros(N); b[0] = 1
    pi = spla.spsolve(M.tocsc(), b)
    sym = abs(P - P.T).max()
    return pi, sym


def run(d):
    n = len(d)
    m = sum(d) // 2
    pidx = pair_index(n)
    graphs = enumerate_graphs(d)
    N = len(graphs)
    K = int(n * m / (n * (n - 1) / 2))
    res = {"d": list(d), "N": N, "m": m}
    impls = {
        "networkx.double_edge_swap": lambda g: row_nx_des(g, n, pidx, d),
        "networkx.random_reference(conn=False)": lambda g: row_nx_rr(g, n, pidx, d, K),
        "igraph_rewire": lambda g: row_igraph(g, n, pidx, d),
        "networkit.EdgeSwitching": lambda g: row_nk(g, n, pidx, d),
        "graph-tool random_rewire (persist=False)": lambda g: row_gt(g, n, pidx, d, False),
        "graph-tool random_rewire (persist=True)": lambda g: row_gt(g, n, pidx, d, True),
    }
    for name, f in impls.items():
        rows = [f(g) for g in graphs]
        if any(r is None for r in rows):
            res[name] = "HANGS (an edge with no valid switch partner; persist loops forever)"
            continue
        pi, sym = stationary(rows, graphs)
        tv = 0.5 * np.abs(pi - 1 / N).sum()
        res[name] = {"TV": round(float(tv), 5), "max/min": round(float(pi.max() / pi.min()), 4),
                     "kernel_symmetric": bool(sym < 1e-12)}
    print(json.dumps(res), flush=True)
    return res


if __name__ == "__main__":
    seqs = [(3, 3, 2, 2, 2, 2), (4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3), (3, 3, 3, 3, 1, 1),
            (2, 2, 2, 2, 2, 2, 2), (4, 3, 3, 3, 1, 1, 1), (5, 5, 5, 3, 3, 3, 2), (6, 3, 2, 2, 2, 2, 2, 1)]
    allres = [run(d) for d in seqs]
    json.dump(allres, open("kernels_as_implemented.json", "w"), indent=1)
