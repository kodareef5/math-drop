import numpy as np, cvxpy as cp, scipy.sparse as sp
from bench_hyp import lift_problem
from hyp_cone import E_DIR
G, fixed, free = lift_problem()
Gf = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fixed.keys()]).T)
order = list(fixed.values())
Px = sp.csr_matrix((np.ones(23), (np.arange(23), order)), shape=(23, 23))
Gv = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in free]).T)
v = cp.Variable(len(free)); t = cp.Variable()
H = cp.reshape(Gf @ (Px @ E_DIR) + Gv @ v, (100, 100), order="C")
prob = cp.Problem(cp.Maximize(t), [(H + H.T) / 2 - t * np.eye(100) >> 0, cp.norm(v, "inf") <= 10])
prob.solve(solver=cp.CLARABEL)
Hv = (Gf @ (Px @ E_DIR) + Gv @ v.value).reshape(100, 100); ev = np.linalg.eigvalsh((Hv + Hv.T) / 2)
print(prob.status, "max min-eig of H at x=e:", t.value, " eig range", ev.min(), ev.max())
