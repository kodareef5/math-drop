import numpy as np, cvxpy as cp, scipy.sparse as sp, collections
from bench_hyp import make_instance, lift_problem
G, fixed, free = lift_problem()
nz = np.abs(G).sum(axis=(2, 3)) > 0
Gf = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fixed.keys()]).T)
order = list(fixed.values())
Px = sp.csr_matrix((np.ones(23), (np.arange(23), order)), shape=(23, 23))
res = collections.defaultdict(list)
for name, fr in [("full307", free), ("trim181", [(l, k) for (l, k) in free if nz[l, k]])]:
    Gv = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fr]).T)
    rng = np.random.default_rng(2026)
    for it in range(12):
        c, A, b, x0 = make_instance(rng)
        x = cp.Variable(23); v = cp.Variable(len(fr))
        H = cp.reshape(Gf @ (Px @ x) + Gv @ v, (100, 100), order="C")
        prob = cp.Problem(cp.Minimize(c @ x), [(H + H.T) / 2 >> 0, A @ x == b])
        prob.solve(solver=cp.CLARABEL)
        if it: res[name].append((prob.status, prob.solver_stats.num_iters, prob.solver_stats.solve_time, prob.value))
for name, r in res.items():
    print(name, collections.Counter(s for s, *_ in r), "median iters", np.median([x[1] for x in r]), "median solve %.2fs" % np.median([x[2] for x in r]))
print("max |obj full - trim| %.1e" % max(abs(a[3] - b[3]) for a, b in zip(res["full307"], res["trim181"])))
