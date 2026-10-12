import numpy as np, json, math
import product_ansatz373 as P
from monge373_lp import build_instance, cost_tensor, solve_lp
out = {}
for m_side, rB, starts in [(3, 0.02, 25)]:
    pts, A, mu, comp, src, Ys = build_instance(m_side, rB)
    C = cost_tensor(A); Cf = np.where(C < 1e5, C, 1e3)
    res, _ = solve_lp(C, mu)
    best = np.inf
    for s in range(starts):
        X2 = P.random_feasible(mu); X3 = P.random_feasible(mu); prev = np.inf
        for it in range(60):
            X2, _ = P.block_lp(np.einsum('il,ijl->ij', X3, Cf), mu)
            X3, _ = P.block_lp(np.einsum('ij,ijl->il', X2, Cf), mu)
            v = P.value(Cf, mu, X2, X3)
            if prev - v < 1e-13: break
            prev = v
        best = min(best, v)
    out[f'm{m_side}'] = dict(n_atoms=len(mu), kantorovich_opt=float(res.fun), product_best=float(best),
                             rel_gap=float((best - res.fun) / res.fun),
                             independent_branch_prediction=float(res.fun + (1/math.sqrt(2) - 0.5) / 6))
    print(out[f'm{m_side}'], flush=True)
json.dump(out, open('product_ansatz373b.json', 'w'), indent=1)
