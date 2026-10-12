import numpy as np, cvxpy as cp, scipy.sparse as sp, json, time, collections
from bench_hyp import make_instance, lift_problem, native_solve, hyp_lambda_min
G, fixed, free = lift_problem()
nz = np.abs(G).sum(axis=(2, 3)) > 0
free_t = [(l, k) for (l, k) in free if nz[l, k]]
Gf = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fixed.keys()]).T)
order = list(fixed.values())
Px = sp.csr_matrix((np.ones(23), (np.arange(23), order)), shape=(23, 23))
Gv = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in free_t]).T)
rng = np.random.default_rng(2026)
st = collections.Counter(); its = []; ts = []; diffs = []
for it in range(20):
    c, A, b, x0 = make_instance(rng)
    xn, _, _ = native_solve(c, A, b, x0)
    x = cp.Variable(23); v = cp.Variable(len(free_t))
    H = cp.reshape(Gf @ (Px @ x) + Gv @ v, (100, 100), order="C")
    prob = cp.Problem(cp.Minimize(c @ x), [(H + H.T) / 2 >> 0, A @ x == b])
    prob.solve(solver=cp.CLARABEL)
    if it == 0: continue
    st[prob.status] += 1; its.append(prob.solver_stats.num_iters); ts.append(prob.solver_stats.solve_time); diffs.append(prob.value - c @ xn)
print("trimmed lift: aux vars", len(free_t), "statuses", dict(st), "median iters", np.median(its), "median solve %.2fs" % np.median(ts), "max |dobj| %.1e" % max(map(abs, diffs)))
