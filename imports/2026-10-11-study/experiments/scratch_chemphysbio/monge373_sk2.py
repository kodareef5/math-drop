"""Re-analyse Sinkhorn/LP plans by component pattern (branch 1 = {0,1+,1-},
branch 2 = {0,2+,2-}) rather than by exact atom; report marginal error and the
centre-atom branch split; barycentric projection restricted to centre atoms."""
import numpy as np, json
import monge373 as M
from monge373_lp import build_instance, cost_tensor, solve_lp, sinkhorn3
out = {}
for m_side, rB in [(1, 0.0), (3, 0.02)]:
    pts, A, mu, comp, src, Ys = build_instance(m_side, rB)
    n = len(mu); C = cost_tensor(A)
    res, _ = solve_lp(C, mu); P_lp = res.x.reshape(n, n, n)
    centre = [i for i in range(n) if comp[i] == '0']
    def pattern_split(P):
        b1 = b2 = oth = 0.0; per = []
        for i in centre:
            x1 = x2 = 0.0
            for j in range(n):
                for l in range(n):
                    v = P[i, j, l]
                    s = {comp[j], comp[l]}
                    if s == {'1+', '1-'}: x1 += v
                    elif s == {'2+', '2-'}: x2 += v
                    else: oth += v
            b1 += x1; b2 += x2; per.append((x1 / mu[i], x2 / mu[i]))
        tot = sum(mu[i] for i in centre)
        return b1 / tot, b2 / tot, oth / tot, per
    def bary_centre(P):
        cst = 0.0; tot = 0.0
        for i in centre:
            Pi = P[i]; mi = Pi.sum()
            T2 = np.einsum('jl,jd->d', Pi, A) / mi; T3 = np.einsum('jl,ld->d', Pi, A) / mi
            cst += mu[i] * float(M.c3(A[i], T2, T3)); tot += mu[i]
        return cst / tot
    r = {'lp_value': float(res.fun), 'lp_split': pattern_split(P_lp)[:3], 'lp_bary_centre_cost': bary_centre(P_lp)}
    sk = []
    for eps in [0.05, 0.02, 0.01]:
        P, it = sinkhorn3(C, mu, eps, iters=20000, tol=1e-13)
        marg = max(np.abs(P.sum(axis=(1, 2)) - mu).max(), np.abs(P.sum(axis=(0, 2)) - mu).max(), np.abs(P.sum(axis=(0, 1)) - mu).max())
        cost = float((P * C).sum())
        b1, b2, oth, per = pattern_split(P)
        sk.append(dict(eps=eps, iters=it, marginal_err=float(marg), cost=cost, rel_gap=(cost - res.fun) / res.fun,
                       branch1=round(b1, 4), branch2=round(b2, 4), other=round(oth, 4),
                       min_branch_share_over_centre_atoms=round(min(min(p) for p in per) / max(1e-12, max(max(p) for p in per)), 3),
                       bary_centre_cost=bary_centre(P)))
    r['sinkhorn'] = sk
    out[f'm{m_side}_r{rB}'] = r
    print(json.dumps(r, indent=1, default=float))
json.dump(out, open('monge373_sk2.json', 'w'), indent=1, default=float)
