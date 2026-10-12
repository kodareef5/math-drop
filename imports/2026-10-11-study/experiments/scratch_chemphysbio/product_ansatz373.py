"""Best value of the Hu-Chen-Liu (SISC 2023) 'Monge-like' product ansatz
  gamma(r1,r2,r3) = mu(r1) X2[r1,r2] X3[r1,r3]
(X_i row-stochastic, mu^T X_i = mu) on the 5-atom family-373 instance,
versus the exact Kantorovich LP optimum (2.5).
The objective is bilinear in (X2, X3): we use alternating exact LPs
(fix X3 -> LP in X2; fix X2 -> LP in X3) from many random starts, plus
an exhaustive search over all pairs of deterministic couplings (permutation-
like vertices), which are vertices of each LP block.
Note: the product form has marginal 3 equal to mu^T X3 and marginal 2 equal to
mu^T X2 by construction, so it is a feasible Kantorovich plan.
"""
import numpy as np, json, itertools
from scipy.optimize import linprog
from monge373_lp import build_instance, cost_tensor, solve_lp

rng = np.random.default_rng(7)


def block_lp(Cmat, mu):
    """min sum_ij mu_i X_ij Cmat_ij s.t. rows of X sum to 1, mu^T X = mu, X>=0."""
    n = len(mu)
    c = (mu[:, None] * Cmat).ravel()
    A = []; b = []
    for i in range(n):
        a = np.zeros(n*n); a[i*n:(i+1)*n] = 1; A.append(a); b.append(1)
    for j in range(n):
        a = np.zeros(n*n)
        for i in range(n):
            a[i*n+j] = mu[i]
        A.append(a); b.append(mu[j])
    r = linprog(c, A_eq=np.array(A), b_eq=np.array(b), bounds=(0, None), method='highs')
    return r.x.reshape(n, n), r.fun


def value(C, mu, X2, X3):
    return float(np.einsum('i,ij,il,ijl->', mu, X2, X3, C))


def random_feasible(mu):
    n = len(mu)
    # random cost -> LP vertex, then mix two vertices
    X, _ = block_lp(rng.random((n, n)), mu)
    Y, _ = block_lp(rng.random((n, n)), mu)
    t = rng.random()
    return t*X + (1-t)*Y


if __name__ == '__main__':
    pts, A, mu, comp, src, Ys = build_instance(1, 0.0)
    C = cost_tensor(A)
    Cf = np.where(C < 1e5, C, 1e3)
    res, _ = solve_lp(C, mu)
    best = np.inf
    for s in range(300):
        X2 = random_feasible(mu); X3 = random_feasible(mu)
        prev = np.inf
        for it in range(50):
            X2, _ = block_lp(np.einsum('il,ijl->ij', X3, Cf), mu)
            X3, _ = block_lp(np.einsum('ij,ijl->il', X2, Cf), mu)
            v = value(Cf, mu, X2, X3)
            if prev - v < 1e-13:
                break
            prev = v
        best = min(best, v)
    # exhaustive over deterministic maps T: atoms -> atoms that preserve mu (Monge plans)
    n = len(mu)
    monge_best = np.inf
    for T2 in itertools.product(range(n), repeat=n):
        m2 = np.zeros(n)
        for i, j in enumerate(T2):
            m2[j] += mu[i]
        if np.abs(m2 - mu).max() > 1e-12:
            continue
        for T3 in itertools.product(range(n), repeat=n):
            m3 = np.zeros(n)
            for i, j in enumerate(T3):
                m3[j] += mu[i]
            if np.abs(m3 - mu).max() > 1e-12:
                continue
            v = sum(mu[i]*Cf[i, T2[i], T3[i]] for i in range(n))
            monge_best = min(monge_best, v)
    out = dict(n_atoms=n, masses=[round(float(m), 4) for m in mu], kantorovich_opt=float(res.fun),
               product_ansatz_best=float(best), product_rel_gap=float((best-res.fun)/res.fun),
               discrete_monge_best=float(monge_best), monge_rel_gap=float((monge_best-res.fun)/res.fun))
    print(out)
    json.dump(out, open('product_ansatz373.json', 'w'), indent=1)
