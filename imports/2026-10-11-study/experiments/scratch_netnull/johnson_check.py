"""Check numerically the sharpened comparison H <= L (i.e. Var <= <f, L f>, switch-graph gap >= 1),
obtained by replacing the paper's path bound h_a <= n^2 J_a (Lemma mix:comparison) with the exact
Johnson-graph gap N of the transposition Laplacian on a q-subset slice of N labels (so h_a <= J_a/N <= J_a/2).
Also checks the paper's H^2 >= H and Var <= <f,Hf> on the same instances."""
import itertools, json
import numpy as np
from enum_graphs import enumerate_graphs, switch_neighbours, pair_index


def operators(d):
    n = len(d)
    pidx = pair_index(n)
    gs = enumerate_graphs(d)
    N = len(gs)
    idx = {g: i for i, g in enumerate(gs)}
    L = np.zeros((N, N))
    for i, g in enumerate(gs):
        for h in switch_neighbours(g, n, pidx):
            L[i, idx[h]] -= 1
            L[i, i] += 1
    H = np.zeros((N, N))
    for (a, b) in itertools.combinations(range(n), 2):
        fib = {}
        for i, g in enumerate(gs):
            key = g
            for w in range(n):
                if w in (a, b):
                    continue
                if (g >> pidx[(a, w)] & 1) != (g >> pidx[(b, w)] & 1):
                    key &= ~(1 << pidx[(a, w)]); key &= ~(1 << pidx[(b, w)])
            fib.setdefault(key, []).append(i)
        E = np.zeros((N, N))
        for mem in fib.values():
            for i in mem:
                for j in mem:
                    E[i, j] = 1.0 / len(mem)
        H += np.eye(N) - E
    return L, H, N


if __name__ == "__main__":
    out = []
    for d in [(3, 3, 2, 2, 2, 2), (4, 4, 2, 2, 2, 2), (3, 3, 3, 3, 3, 3), (4, 3, 3, 3, 1, 1, 1),
              (5, 5, 5, 3, 3, 3, 2), (6, 3, 2, 2, 2, 2, 2, 1), (2, 2, 2, 2, 2, 2, 2), (4, 4, 3, 3, 2, 2, 1, 1)]:
        L, H, N = operators(d)
        ev_LmH = np.linalg.eigvalsh(L - H).min()
        ev_H2mH = np.linalg.eigvalsh(H @ H - H).min()
        evL = np.sort(np.linalg.eigvalsh(L))
        evH = np.sort(np.linalg.eigvalsh(H))
        n = len(d)
        row = dict(d=list(d), N=N, min_eig_L_minus_H=round(float(ev_LmH), 6),
                   min_eig_H2_minus_H=round(float(ev_H2mH), 6), gap_L=round(float(evL[1]), 4),
                   gap_H=round(float(evH[1]), 4), paper_bound_gap_L=round(1 / (2 * n * n), 5),
                   sharpened_bound_gap_L=1.0)
        print(json.dumps(row), flush=True)
        out.append(row)
    json.dump(out, open("johnson_check.json", "w"), indent=1)
