"""Exhaustive bias of NetworkX double_edge_swap / random_reference over ALL labelled graphs on n<=7 vertices.

Uses the closed form (checked against brute force in check_formula()):
  #valid switches  deg_sw(G) = 2*P_disj - S2(G) + 3*T(G) + 2*C4(G)
  P_disj = C(m,2) - sum_v C(d_v,2)        (unordered vertex-disjoint edge pairs; degree-determined)
  S2     = sum_{uv in E} (d_u-1)(d_v-1)   (assortativity numerator; varies with G)
  T      = #triangles, C4 = #4-cycles
NetworkX double_edge_swap stationary law  pi(G) ~ deg_sw(G)                 (retry-until-success)
NetworkX random_reference  stationary law  pi(G) ~ s/(1-(1-s)^K), s=deg_sw/(2 P_disj), K=int(2m/(n-1))
"""
import itertools, math, sys
import numpy as np
from collections import defaultdict
from enum_graphs import enumerate_graphs, switch_neighbours, pair_index


def stats_batch(A):
    # A: (B, n, n) int64 adjacency
    d = A.sum(2)
    m = d.sum(1) // 2
    A2 = A @ A
    T = np.einsum('bij,bji->b', A2, A) // 6
    dm1 = d - 1
    S2 = np.einsum('bij,bi,bj->b', A, dm1, dm1) // 2
    n = A.shape[1]
    iu = np.triu_indices(n, 1)
    co = A2[:, iu[0], iu[1]]
    C4 = (co * (co - 1) // 2).sum(1) // 2
    Pdisj = m * (m - 1) // 2 - (d * (d - 1) // 2).sum(1)
    degsw = 2 * Pdisj - S2 + 3 * T + 2 * C4
    return d, m, Pdisj, degsw


def check_formula():
    seqs = [(3, 3, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3), (4, 3, 3, 2, 2, 2), (3, 3, 3, 3, 2, 2, 2, 2), (5, 3, 3, 2, 2, 2, 2, 1)]
    for dseq in seqs:
        n = len(dseq)
        pidx = pair_index(n)
        gs = enumerate_graphs(dseq)
        A = np.zeros((len(gs), n, n), dtype=np.int64)
        for b, g in enumerate(gs):
            k = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if g >> k & 1:
                        A[b, i, j] = A[b, j, i] = 1
                    k += 1
        _, _, _, degsw = stats_batch(A)
        brute = np.array([len(switch_neighbours(g, n, pidx)) for g in gs])
        assert (brute == degsw).all(), dseq
    print("closed-form deg_sw formula verified on", len(seqs), "degree sequences")


def exhaustive(n):
    pairs = list(itertools.combinations(range(n), 2))
    P = len(pairs)
    total = 1 << P
    groups_des = defaultdict(list)
    groups_rr = defaultdict(list)
    B = 1 << 16
    for start in range(0, total, B):
        masks = np.arange(start, min(total, start + B), dtype=np.int64)
        A = np.zeros((len(masks), n, n), dtype=np.int64)
        for k, (i, j) in enumerate(pairs):
            bit = (masks >> k) & 1
            A[:, i, j] = bit
            A[:, j, i] = bit
        d, m, Pdisj, degsw = stats_batch(A)
        for b in range(len(masks)):
            key = tuple(d[b])
            if list(key) != sorted(key, reverse=True):
                continue  # labelled degree vectors: restrict to non-increasing ones (law is permutation invariant)
            groups_des[key].append(degsw[b])
            groups_rr[key].append((degsw[b], Pdisj[b], m[b]))
    out = []
    for key, w in groups_des.items():
        w = np.array(w, dtype=float)
        N = len(w)
        if N < 2 or w.min() == 0:
            # w.min()==0 => some realisation has no switch; the switch graph would be disconnected unless N==1
            if N >= 2 and w.min() == 0:
                print("WARNING zero-switch realisation", key)
            continue
        pi = w / w.sum()
        tv = 0.5 * np.abs(pi - 1.0 / N).sum()
        rr = groups_rr[key]
        Pd, mm = rr[0][1], rr[0][2]
        K = int(2 * mm / (n - 1))
        s = w / (2 * Pd)
        if K >= 1:
            wr = s / (1 - (1 - s) ** K)
            pr = wr / wr.sum()
            tvr = 0.5 * np.abs(pr - 1.0 / N).sum()
        else:
            tvr = float('nan')
        out.append((tv, w.max() / w.min(), tvr, K, key, N))
    out.sort(reverse=True)
    return out


if __name__ == "__main__":
    check_formula()
    for n in (5, 6, 7):
        res = exhaustive(n)
        tvs = np.array([r[0] for r in res])
        tvr = np.array([r[2] for r in res if not math.isnan(r[2])])
        print(f"n={n}: {len(res)} non-increasing degree vectors with >=2 realisations")
        print(f"   double_edge_swap TV: max {tvs.max():.4f}, median {np.median(tvs):.4f}; max ratio {max(r[1] for r in res):.3f}")
        print(f"   random_reference TV: max {np.nanmax(tvr):.4f}, median {np.median(tvr):.4f}")
        for r in res[:5]:
            print("     worst:", r[4], "N=", r[5], "TV_des=%.4f ratio=%.3f TV_rr=%.4f K=%d" % (r[0], r[1], r[2], r[3]))
