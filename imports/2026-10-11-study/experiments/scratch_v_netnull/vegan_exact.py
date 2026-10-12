"""Exact laws of vegan's binary null models as implemented in src/nestedness.c
(read from vegandevs/vegan@a574546) for small margins.

swap      : per step, loop until one successful 2x2 swap (proposal: cell a uniform
            over nr*nc, second row uniform among others, second col uniform among
            others). Sequential; we compute the stationary law.
quasiswap : start from r2dtable (law prop. to 1/prod t_ij!), then blocks of `thin`
            quasiswap steps; stop at the first block end with all entries <= 1.
            Non-sequential: we compute the exact output law.
curveball : two distinct rows uniformly; shuffle the row-unique species.
trialswap : `thin` single trials, rejections counted (reference).

usage: python3 vegan_exact.py
"""
import itertools, json, sys
from math import factorial, comb
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from exact_kernels import stationary, tv


def tables(rs, cs, binary):
    nr, nc = len(rs), len(cs)
    out = []
    def rec(i, colrem, rows):
        if i == nr:
            if all(c == 0 for c in colrem):
                out.append(tuple(rows))
            return
        hi = 1 if binary else None
        def rowrec(j, left, row):
            if j == nc:
                if left == 0:
                    rec(i + 1, [colrem[k] - row[k] for k in range(nc)], rows + [tuple(row)])
                return
            top = min(left, colrem[j]) if hi is None else min(left, colrem[j], 1)
            for v in range(top + 1):
                rowrec(j + 1, left - v, row + [v])
        rowrec(0, rs[i], [])
    rec(0, list(cs), [])
    return [np.array(t) for t in out]


def key(M):
    return M.tobytes()


def swap_step_targets(M):
    """list over all proposals (a, row1, col1) of resulting matrix (or None)."""
    nr, nc = M.shape
    res = []
    for r0 in range(nr):
        for c0 in range(nc):
            for r1 in range(nr):
                if r1 == r0: continue
                for c1 in range(nc):
                    if c1 == c0: continue
                    a, b, c, d = M[r0, c0], M[r0, c1], M[r1, c0], M[r1, c1]
                    if a == d == 1 and b == c == 0 or (b == c == 1 and a == d == 0):
                        N = M.copy()
                        N[r0, c0], N[r0, c1], N[r1, c0], N[r1, c1] = 1 - a, 1 - b, 1 - c, 1 - d
                        res.append(N)
                    else:
                        res.append(None)
    return res


def qswap_step(M):
    """exact one-step distribution of a quasiswap step, as dict key->(prob, matrix)."""
    nr, nc = M.shape
    out = {}
    pa = 1.0 / (nr * nc)
    for r0 in range(nr):
        for c0 in range(nc):
            for r1 in range(nr):
                if r1 == r0: continue
                p1 = pa / (nr - 1)
                if M[r1, c0] == 0 and M[r0, c0] == 0:
                    k = key(M); out[k] = (out.get(k, (0, M))[0] + p1, M); continue
                for c1 in range(nc):
                    if c1 == c0: continue
                    p = p1 / (nc - 1)
                    a, b, c, d = M[r0, c0], M[r0, c1], M[r1, c0], M[r1, c1]
                    N = M.copy()
                    if d > 0 and a > 0 and a + d - b - c >= 2:
                        N[r0, c0] -= 1; N[r1, c1] -= 1; N[r0, c1] += 1; N[r1, c0] += 1
                    elif c > 0 and b > 0 and b + c - a - d >= 2:
                        N[r0, c0] += 1; N[r1, c1] += 1; N[r0, c1] -= 1; N[r1, c0] -= 1
                    k = key(N); out[k] = (out.get(k, (0, N))[0] + p, N)
    return out


def curveball_kernel(B, idx):
    nr = B[0].shape[0]
    P = np.zeros((len(B), len(B)))
    npairs = nr * (nr - 1)  # ordered pairs (I2RAND)
    for i, M in enumerate(B):
        for r0 in range(nr):
            for r1 in range(nr):
                if r0 == r1: continue
                u0 = [j for j in range(M.shape[1]) if M[r0, j] == 1 and M[r1, j] == 0]
                u1 = [j for j in range(M.shape[1]) if M[r1, j] == 1 and M[r0, j] == 0]
                if not u0 or not u1:
                    P[i, i] += 1.0 / npairs; continue
                U = u0 + u1
                combos = list(itertools.combinations(U, len(u0)))
                for S in combos:
                    N = M.copy()
                    for j in U:
                        N[r0, j] = 1 if j in S else 0
                        N[r1, j] = 0 if j in S else 1
                    P[i, idx[key(N)]] += 1.0 / npairs / len(combos)
    return P


def analyse(rs, cs, thins=(1, 10, 100)):
    B = tables(rs, cs, True)
    idx = {key(M): i for i, M in enumerate(B)}
    n = len(B)
    u = np.full(n, 1.0 / n)
    res = dict(rs=rs, cs=cs, n01=n)
    # swap
    Ps = np.zeros((n, n)); A = np.zeros((n, n)); sw = np.zeros(n)
    for i, M in enumerate(B):
        tg = swap_step_targets(M)
        succ = [N for N in tg if N is not None]
        sw[i] = len(succ)
        for N in succ:
            Ps[i, idx[key(N)]] += 1.0 / len(succ)
            A[i, idx[key(N)]] += 1.0 / len(tg)
        A[i, i] += 1 - len(succ) / len(tg)
    pis = stationary(Ps)
    res['swap'] = dict(TV=float(tv(pis, u)), ratio=float(pis.max() / pis.min()),
                       closed_form_err=float(abs(pis - sw / sw.sum()).max()),
                       swappable_counts=sorted(set(sw.astype(int).tolist())))
    res['trialswap'] = dict(TV=float(tv(stationary(A), u)))
    # curveball
    Pc = curveball_kernel(B, idx)
    pic = stationary(Pc)
    res['curveball'] = dict(TV=float(tv(pic, u)), kernel_asym=float(abs(Pc - Pc.T).max()))
    # quasiswap: exact output law
    T = tables(rs, cs, False)
    tidx = {key(M): i for i, M in enumerate(T)}
    nT = len(T)
    K = np.zeros((nT, nT))
    for i, M in enumerate(T):
        for k_, (p, N) in qswap_step(M).items():
            K[i, tidx[k_]] += p
    N_ = sum(rs)
    p0 = np.array([np.prod([factorial(x) for x in rs]) * np.prod([factorial(x) for x in cs])
                   / factorial(N_) / np.prod([factorial(int(x)) for x in M.ravel()]) for M in T])
    assert abs(p0.sum() - 1) < 1e-12
    is01 = np.array([M.max() <= 1 for M in T])
    tr = np.where(~is01)[0]; ab = np.where(is01)[0]
    res['quasiswap'] = {}
    for th in thins:
        Bk = np.linalg.matrix_power(K, th)
        Q = Bk[np.ix_(tr, tr)]; R = Bk[np.ix_(tr, ab)]
        out = p0[ab] + p0[tr] @ np.linalg.solve(np.eye(len(tr)) - Q, R)
        # reorder to B order
        law = np.zeros(n)
        for jj, j in enumerate(ab):
            law[idx[key(T[j])]] = out[jj]
        res['quasiswap'][f'thin={th}'] = dict(TV=float(tv(law, u)), ratio=float(law.max() / law.min()),
                                             sum=float(law.sum()))
        if th == 1:
            res['_quasiswap_law_thin1'] = law.tolist()
    res['_swap_law'] = pis.tolist()
    res['_order'] = [M.ravel().tolist() for M in B]
    return res


if __name__ == '__main__':
    allres = []
    for rs, cs in [((2, 2, 1, 1), (2, 2, 1, 1)), ((2, 1, 1), (2, 1, 1)), ((3, 2, 2, 1), (3, 2, 2, 1)),
                   ((2, 2, 2), (2, 2, 1, 1)), ((3, 2, 1, 1), (2, 2, 2, 1))]:
        r = analyse(rs, cs)
        print(json.dumps({k: v for k, v in r.items() if not k.startswith('_')}))
        allres.append(r)
    json.dump(allres, open(__file__.rsplit('/', 1)[0] + '/vegan_exact_out.json', 'w'))
