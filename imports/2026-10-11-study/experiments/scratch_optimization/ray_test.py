"""Exactness check of the 100x100 lift (An-Exact-Semidefinite-Lift..., Thm 1.1):
for random interior x0 and random direction d, compare
  s_true = sup{s : x0 + s d in K}  (from the exact 20x20 slice pencil + bisection)
  s_lift = max{s : exists v, H(x0+s d, v) >= 0}  (Clarabel)
"""
import numpy as np, cvxpy as cp, scipy.sparse as sp, time, json
from hyp_cone import build_lift, output_index_map, unpack, IU, Phi
from bench_hyp import hyp_lambda_min, interior, make_instance

G = build_lift(); fixed = output_index_map()
free = [(l, k) for l in range(15) for k in range(22) if (l, k) not in fixed]
Gf = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fixed.keys()]).T)
order = list(fixed.values())
Px = sp.csr_matrix((np.ones(23), (np.arange(23), order)), shape=(23, 23))
Gv = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in free]).T)


def s_true(x0, d, smax=1e3):
    def inK(s):
        x = x0 + s * d
        X, Z, y = unpack(x)
        if np.linalg.eigvalsh(X).min() < -1e-12:
            return False
        return hyp_lambda_min(x) >= -1e-12
    lo, hi = 0.0, 1.0
    while inK(hi):
        lo, hi = hi, hi * 2
        if hi > smax:
            return np.inf
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if inK(mid) else (lo, mid)
    return lo


def s_lift(x0, d):
    s = cp.Variable(); v = cp.Variable(len(free))
    x = x0 + s * d
    H = cp.reshape(Gf @ (Px @ x) + Gv @ v, (100, 100), order="C")
    prob = cp.Problem(cp.Maximize(s), [(H + H.T) / 2 >> 0, s <= 1e3])
    prob.solve(solver=cp.CLARABEL)
    return s.value, prob.status


rng = np.random.default_rng(5)
rows = []
for it in range(25):
    _, _, _, x0 = make_instance(rng, 0)
    d = rng.normal(size=23)
    if it % 3 == 0:  # bias direction to make X singular first
        X0 = unpack(x0)[0]
        w = rng.normal(size=4); w /= np.linalg.norm(w)
        D = -np.outer(w, w) * 3
        d[:10] = [D[i, j] for (i, j) in IU]
    st = s_true(x0, d); sl, status = s_lift(x0, d)
    xb = x0 + st * d
    Xb = unpack(xb)[0]
    sl = float(sl); row = dict(it=it, s_true=float(st), s_lift=sl, rel_err=abs(sl - st) / max(1e-12, abs(st)), status=status,
               minEigX_at_boundary=float(np.linalg.eigvalsh(Xb).min()))
    rows.append(row); print(json.dumps(row))
errs = [r["rel_err"] for r in rows]
print("max rel err %.2e  median %.2e  ; boundary points with singular X (min eig<1e-6): %d" %
      (max(errs), np.median(errs), sum(r["minEigX_at_boundary"] < 1e-6 for r in rows)))
