"""Discrete instance of the family-373 construction + exact 3-marginal LP
and multi-marginal Sinkhorn.  Run after monge373.py (reuses its functions).

Instance: centre atoms x_j on a small grid in a ball B (radius rB) around 0,
weights nu_j (smooth bump, normalised), centre mass nu_j/3, outer atoms
Y_k(x_j), W_k(x_j) (k=1,2) with mass nu_j/6.  All three marginals = mu.
Checks:
  (1) LP optimum == 3 * sum_i mu_i u(p_i)  (duality with the paper's
      certificate potential u)  -> certificate numerically tight
  (2) support of the LP plan lies on the two branch families, and every
      centre atom is split 50/50 between branch 1 and branch 2
  (3) multi-marginal Sinkhorn at decreasing eps converges to the same split
  (4) barycentric-projection map (used to read co-motion functions off a
      Kantorovich plan) evaluated on this instance: cost vs optimum
"""
import numpy as np, itertools, json, time
from scipy.optimize import linprog
from scipy import sparse
import monge373 as M

rng = np.random.default_rng(1)


def build_instance(m_side=2, rB=0.02):
    # centre grid points inside ball radius rB
    g = np.linspace(-rB, rB, m_side) if m_side > 1 else np.array([0.0])
    pts = np.array([p for p in itertools.product(g, g, g) if np.linalg.norm(p) <= rB * 1.0001])
    if len(pts) == 0:
        pts = np.zeros((1, 3))
    w = np.exp(-np.sum(pts ** 2, axis=1) / (rB ** 2 + 1e-12))
    w /= w.sum()
    atoms, mass, comp, src = [], [], [], []
    Ys = {}
    for j, x in enumerate(pts):
        atoms.append(x); mass.append(w[j] / 3); comp.append('0'); src.append(j)
        for k in range(2):
            y, z = M.solve_given_x(x, k)
            Ys[(j, k)] = (y, z)
    for k in range(2):
        for j, x in enumerate(pts):
            atoms.append(Ys[(j, k)][0]); mass.append(w[j] / 6); comp.append(f'{k+1}+'); src.append(j)
            atoms.append(Ys[(j, k)][1]); mass.append(w[j] / 6); comp.append(f'{k+1}-'); src.append(j)
    return pts, np.array(atoms), np.array(mass), comp, src, Ys


def u_of_atom(p, cmp):
    if cmp == '0':
        return float(M.u0(p))
    k = int(cmp[0]) - 1
    if cmp[1] == '+':
        return float(M.w_k(p, k)[0])
    return float(M.vk(p, k))


def cost_tensor(A):
    n = len(A)
    D = np.linalg.norm(A[:, None, :] - A[None, :, :], axis=-1)
    with np.errstate(divide='ignore'):
        Inv = np.where(D > 0, 1.0 / D, 1e6)
    C = Inv[:, :, None] + Inv[:, None, :] + Inv[None, :, :]
    return C


def solve_lp(C, mu):
    n = len(mu)
    N = n ** 3
    c = C.reshape(-1)
    rows, cols = [], []
    idx = np.arange(N).reshape(n, n, n)
    for ax in range(3):
        for i in range(n):
            sl = [slice(None)] * 3; sl[ax] = i
            ids = idx[tuple(sl)].reshape(-1)
            rows.append(np.full(ids.size, ax * n + i)); cols.append(ids)
    rows = np.concatenate(rows); cols = np.concatenate(cols)
    A = sparse.csr_matrix((np.ones(rows.size), (rows, cols)), shape=(3 * n, N))
    b = np.concatenate([mu, mu, mu])
    t = time.time()
    res = linprog(c, A_eq=A, b_eq=b, bounds=(0, None), method='highs')
    return res, time.time() - t


def sinkhorn3(C, mu, eps, iters=5000, tol=1e-12):
    # log-domain multi-marginal Sinkhorn with three (equal) marginals
    n = len(mu)
    f = [np.zeros(n) for _ in range(3)]
    logmu = np.log(mu)
    Cs = C / eps
    from scipy.special import logsumexp
    for it in range(iters):
        old = [x.copy() for x in f]
        # update f0
        S = f[1][None, :, None] + f[2][None, None, :] - Cs
        f[0] = logmu - logsumexp(S, axis=(1, 2))
        S = f[0][:, None, None] + f[2][None, None, :] - Cs
        f[1] = logmu - logsumexp(S, axis=(0, 2))
        S = f[0][:, None, None] + f[1][None, :, None] - Cs
        f[2] = logmu - logsumexp(S, axis=(0, 1))
        if max(np.abs(a - b).max() for a, b in zip(f, old)) < tol:
            break
    logP = f[0][:, None, None] + f[1][None, :, None] + f[2][None, None, :] - Cs
    P = np.exp(logP)
    return P, it


def analyse_plan(P, comp, src, mu, A):
    """for each centre atom: mass going to branch-1 vs branch-2 triples (any order)."""
    n = len(mu)
    centre = [i for i in range(n) if comp[i] == '0']
    out = []
    tot_on_branches = 0.0
    for i in centre:
        # plan with first coordinate = i (symmetrise over coordinate roles)
        Pi = P[i] + 0.0
        b = {1: 0.0, 2: 0.0, 'other': 0.0}
        for j in range(n):
            for l in range(n):
                v = Pi[j, l]
                if v <= 0:
                    continue
                cj, cl = comp[j], comp[l]
                if {cj, cl} == {'1+', '1-'} and src[j] == src[i] and src[l] == src[i]:
                    b[1] += v
                elif {cj, cl} == {'2+', '2-'} and src[j] == src[i] and src[l] == src[i]:
                    b[2] += v
                else:
                    b['other'] += v
        out.append((i, b[1] / mu[i], b[2] / mu[i], b['other'] / mu[i]))
    return out


if __name__ == '__main__':
    results = {}
    for m_side, rB in [(1, 0.0), (3, 0.02), (4, 0.03)]:
        pts, A, mu, comp, src, Ys = build_instance(m_side, rB)
        n = len(mu)
        # potential certificate value
        uvals = np.array([u_of_atom(A[i], comp[i]) for i in range(n)])
        dual_val = 3 * float(np.dot(mu, uvals))
        C = cost_tensor(A)
        res, tlp = solve_lp(C, mu)
        P = res.x.reshape(n, n, n)
        stats = analyse_plan(P, comp, src, mu, A)
        split = [s for s in stats if s[1] > 1e-6 and s[2] > 1e-6]
        offb = max(s[3] for s in stats)
        # barycentric projection of the LP plan from marginal 1 (centre atoms)
        bary_cost = 0.0
        for i in range(n):
            Pi = P[i]
            mi = Pi.sum()
            if mi <= 0:
                continue
            T2 = np.einsum('jl,jd->d', Pi, A) / mi
            T3 = np.einsum('jl,ld->d', Pi, A) / mi
            bary_cost += mu[i] * float(M.c3(A[i], T2, T3))
        r = dict(n_centre=len(pts), n_atoms=n, lp_value=float(res.fun), dual_certificate_value=dual_val,
                 lp_minus_dual=float(res.fun) - dual_val, lp_seconds=round(tlp, 2),
                 centre_atoms_split=len(split), centre_atoms=len(stats),
                 max_offbranch_fraction=float(offb),
                 example_split=[(round(s[1], 4), round(s[2], 4)) for s in stats[:3]],
                 barycentric_projection_cost=bary_cost,
                 barycentric_rel_error=(bary_cost - float(res.fun)) / float(res.fun))
        # Sinkhorn
        sk = []
        for eps in [0.05, 0.02, 0.01]:
            Pk, it = sinkhorn3(C, mu, eps)
            costk = float((Pk * np.where(C < 1e5, C, 0)).sum())
            st = analyse_plan(Pk, comp, src, mu, A)
            sk.append(dict(eps=eps, iters=it, cost=costk, rel_gap=(costk - float(res.fun)) / float(res.fun),
                           branch_split_first=(round(st[0][1], 3), round(st[0][2], 3), round(st[0][3], 3))))
        r['sinkhorn'] = sk
        print(json.dumps(r, indent=1))
        results[f'm{m_side}_r{rB}'] = r
    json.dump(results, open('monge373_lp.json', 'w'), indent=1)
