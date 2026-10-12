import numpy as np, cvxpy as cp, scipy.sparse as sp
from bench_hyp import make_instance, lift_problem
G, fixed, free = lift_problem()
Gf = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fixed.keys()]).T)
order = list(fixed.values())
Px = sp.csr_matrix((np.ones(23), (np.arange(23), order)), shape=(23, 23))
Gv = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in free]).T)
rng = np.random.default_rng(2026)
for it in range(3):
    c, A, b, x0 = make_instance(rng)
    x = cp.Variable(23); v = cp.Variable(len(free))
    Hexpr = cp.reshape(Gf @ (Px @ x) + Gv @ v, (100, 100), order="C")
    prob = cp.Problem(cp.Minimize(c @ x), [(Hexpr + Hexpr.T) / 2 >> 0, A @ x == b])
    prob.solve(solver=cp.CLARABEL)
    H = (Gf @ (Px @ x.value) + Gv @ v.value).reshape(100, 100); H = (H + H.T) / 2
    ev = np.linalg.eigvalsh(H)
    print(it, prob.status, "eigs of H at optimum: max %.2e, #>1e-4*max: %d, #>1e-6*max: %d" % (ev.max(), (ev > 1e-4 * ev.max()).sum(), (ev > 1e-6 * ev.max()).sum()))
