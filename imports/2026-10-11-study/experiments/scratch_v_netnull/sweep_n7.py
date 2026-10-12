"""Sweep all graphical degree sequences (sorted, n<=7, no isolated vertices required? no:
all sequences with min degree >=1) and compute exact stationary TV-from-uniform for
  nx_des (stationary prop. to s(G)),
  nx_rr  (no connectivity requirement; prop. to s/(1-(1-p)^T), T=int(2m/(n-1))),
  nx_rr_conn (connected realizations only, explicit connectivity check),
  bct    (prop. to s/(1-(1-p)^T), T=round_half_even(m/(n-1))+1).
s(G) = number of successful oriented proposals = trace(A B A B), B = J - I - A.
The closed forms are justified because the per-attempt kernel is symmetric
(checked exactly in exact_kernels.py)."""
import itertools, json, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from exact_kernels import realizations, connected


def graphical(seq):
    s = sorted(seq, reverse=True)
    if sum(s) % 2:
        return False
    n = len(s)
    for k in range(1, n + 1):
        if sum(s[:k]) > k * (k - 1) + sum(min(d, k) for d in s[k:]):
            return False
    return True


def tv(p):
    u = 1.0 / len(p)
    return 0.5 * np.abs(p - u).sum()


def conn_success_count(E, n):
    """oriented successful proposals with the post-swap connectivity check"""
    N = [set() for _ in range(n)]
    for a, b in E:
        N[a].add(b); N[b].add(a)
    cnt = 0
    oriented = [(a, b) for a, b in E] + [(b, a) for a, b in E]
    for (a, b) in oriented:
        for (c, d) in oriented:
            if len({a, b, c, d}) < 4:
                continue
            if d in N[a] or b in N[c]:
                continue
            S = set(E)
            S.discard(tuple(sorted((a, b)))); S.discard(tuple(sorted((c, d))))
            S.add(tuple(sorted((a, d)))); S.add(tuple(sorted((c, b))))
            if connected(S, n):
                cnt += 1
    return cnt


def main(nmax=7, do_conn_upto=7):
    rows = []
    for n in range(4, nmax + 1):
        for seq in itertools.combinations_with_replacement(range(n - 1, 0, -1), n):
            seq = list(seq)
            if not graphical(seq):
                continue
            m = sum(seq) // 2
            if m < 2:
                continue
            R = realizations(seq)
            if len(R) < 2:
                continue
            s = []
            for E in R:
                A = np.zeros((n, n))
                for a, b in E:
                    A[a, b] = A[b, a] = 1
                B = 1 - A - np.eye(n)
                s.append(np.trace(A @ B @ A @ B))
            s = np.array(s)
            Z4 = (2 * m) ** 2 - 4 * m - 4 * sum(d * (d - 1) for d in seq)  # oriented pairs, 4 distinct
            p = s / Z4
            row = dict(seq=seq, n=n, m=m, N=len(R))
            pi = s / s.sum()
            row['nx_des'] = (tv(pi), pi.max() / pi.min())
            T = int(2 * m / (n - 1))
            row['T_rr'] = T
            if T >= 1:
                w = s / (1 - (1 - p) ** T); w /= w.sum()
                row['nx_rr'] = (tv(w), w.max() / w.min())
            Tb = int(np.round(m / (n - 1))) + 1
            row['T_bct'] = Tb
            w = s / (1 - (1 - p) ** Tb); w /= w.sum()
            row['bct'] = (tv(w), w.max() / w.min())
            if n <= do_conn_upto and T >= 1:
                C = [E for E in R if connected(E, n)]
                if len(C) >= 2:
                    sc = np.array([conn_success_count(E, n) for E in C], float)
                    pc = sc / Z4
                    w = sc / (1 - (1 - pc) ** T); w /= w.sum()
                    row['nx_rr_conn'] = (tv(w), w.max() / w.min(), len(C))
            rows.append(row)
    return rows


if __name__ == '__main__':
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    rows = main(nmax, do_conn_upto=int(sys.argv[2]) if len(sys.argv) > 2 else 6)
    json.dump(rows, open(f'sweep_n{nmax}_out.json', 'w'), indent=0)
    for ch in ['nx_des', 'nx_rr', 'nx_rr_conn', 'bct']:
        rr = [r for r in rows if ch in r]
        bt = max(rr, key=lambda r: r[ch][0])
        br = max(rr, key=lambda r: r[ch][1])
        print(ch, 'nseq', len(rr), 'maxTV', round(bt[ch][0], 4), bt['seq'], 'N', bt['N'],
              '| max ratio', round(br[ch][1], 3), br['seq'], 'N', br['N'])
