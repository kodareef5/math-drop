"""Benchmark: native hyperbolic-barrier IPM vs exact 100x100 SDP lift (Clarabel, SCS)
on   min c^T x  s.t.  A x = b,  x in K   (K = 23-dim nonspectrahedral hyperbolicity cone, family 095).
"""
import sys, time, json
import numpy as np
import jax, jax.numpy as jnp
jax.config.update("jax_enable_x64", True)
import cvxpy as cp
from hyp_cone import (unpack, sym_from_vec, IU, L_theta, build_lift, output_index_map, E_DIR, q_poly, p_poly)

# ---------- trace inner product weights: <x,x'> = tr(XX') + tr(ZZ') + y.y' ----------
WTS = np.array([1.0 if i == j else 2.0 for (i, j) in IU] * 2 + [1, 1, 1])


def hyp_lambda_min(x):
    """smallest root of t -> p(te - x) via the exact 20x20 slice pencil (Lemma slice)."""
    X, Z, y = unpack(x)
    eta = np.hypot(y[0], y[1]); th = np.arctan2(y[1], y[0]); xi = y[2]
    L = L_theta(th, X, Z, eta, xi)
    return np.linalg.eigvalsh((L + L.T) / 2).min()


# ---------- native barrier F(x) = -log q(x) = -3 logdet X - logdet(Z - Phi_y(X^{-1})), nu = 16 ----------
iu = np.array(IU)


def jsym(v):
    M = jnp.zeros((4, 4))
    M = M.at[iu[:, 0], iu[:, 1]].set(v)
    M = M.at[iu[:, 1], iu[:, 0]].set(v)
    return M


def jQ(y):
    y1, y2, y3 = y
    return jnp.array([[y1**2 + y2**2, -y1 * y2, -y1 * y3],
                      [-y1 * y2, y2**2 + y3**2, -y2 * y3],
                      [-y1 * y3, -y2 * y3, y3**2 + y1**2]])


def jPhi(y, W):
    Q = jQ(y)
    a, r, T = W[0, 0], W[1:, 0], W[1:, 1:]
    top = jnp.concatenate([jnp.array([jnp.trace(Q @ T)]), -r @ Q])
    bot = jnp.concatenate([(-Q @ r)[:, None], a * Q], axis=1)
    return jnp.concatenate([top[None, :], bot], axis=0)


def F(x):
    X = jsym(x[:10]); Z = jsym(x[10:20]); y = x[20:23]
    Xi = jnp.linalg.inv(X)
    S = Z - jPhi(y, Xi)
    return -3.0 * jnp.linalg.slogdet(X)[1] - jnp.linalg.slogdet(S)[1]


gF = jax.jit(jax.grad(F))
hF = jax.jit(jax.hessian(F))
Fj = jax.jit(F)
NU = 16.0


def interior(x):
    X, Z, y = unpack(x)
    if np.linalg.eigvalsh(X).min() <= 0:
        return False
    return hyp_lambda_min(x) > 0


def native_solve(c, A, b, x0, eps=1e-8, mu=20.0, verbose=False):
    """Primal barrier path-following (long-step), feasible start x0, null-space parametrisation x = x0 + N z
    so A x = b holds to machine precision. Returns x, newton_steps, time."""
    import scipy.linalg as sla
    t0 = time.perf_counter()
    N = sla.null_space(A)
    x = x0.copy(); t = 1.0; steps = 0
    while True:
        for _ in range(200):
            g = N.T @ (t * c + np.asarray(gF(x))); H = N.T @ np.asarray(hF(x)) @ N
            dz = -np.linalg.solve(H, g); lam2 = float(-g @ dz)
            steps += 1
            if lam2 / 2 < 1e-10:
                break
            dx = N @ dz
            s = 1.0
            phi0 = t * c @ x + float(Fj(x))
            while True:
                xn = x + s * dx
                if interior(xn) and t * c @ xn + float(Fj(xn)) <= phi0 - 0.25 * s * lam2:
                    break
                s *= 0.5
            x = xn
        if NU / t < eps:
            break
        t *= mu
    return x, steps, time.perf_counter() - t0


def lift_problem():
    G = build_lift()  # 15 x 22 x 100 x 100
    fixed = output_index_map()
    free = [(l, k) for l in range(15) for k in range(22) if (l, k) not in fixed]
    return G, fixed, free


def lift_solve(c, A, b, G, fixed, free, solver, eps=1e-8):
    x = cp.Variable(23)
    v = cp.Variable(len(free))
    # H = sum fixed G * x + sum free G * v ; build as sparse linear maps over the 100x100 matrix
    import scipy.sparse as sp
    Gf = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in fixed.keys()]).T)  # 10000 x 23(ordered by dict)
    order = list(fixed.values())
    Px = sp.csr_matrix((np.ones(23), (np.arange(23), order)), shape=(23, 23))
    Gv = sp.csr_matrix(np.array([G[l, k].ravel() for (l, k) in free]).T)
    Hvec = Gf @ (Px @ x) + Gv @ v
    H = cp.reshape(Hvec, (100, 100), order="C")
    cons = [(H + H.T) / 2 >> 0, A @ x == b]
    prob = cp.Problem(cp.Minimize(c @ x), cons)
    t0 = time.perf_counter()
    if solver == "CLARABEL":
        prob.solve(solver=cp.CLARABEL)
    else:
        prob.solve(solver=cp.SCS, eps_abs=1e-6, eps_rel=1e-6, max_iters=200000)
    wall = time.perf_counter() - t0
    st = prob.solver_stats
    return x.value, prob.value, wall, st.solve_time, st.num_iters, prob.status


def make_instance(rng, m_extra=3):
    """Random c; constraints: <e,x>=1 (trace normalisation) + m_extra random equalities through a
    random interior point x0 (so a strictly feasible start exists)."""
    # random interior point: X pd, Z = Phi_y(X^-1) + pd
    from hyp_cone import Phi
    while True:
        Xr = rng.normal(size=(4, 4)); X = Xr @ Xr.T / 4 + 0.3 * np.eye(4)
        y = rng.normal(size=3)
        Zr = rng.normal(size=(4, 4)); Z = Phi(y, np.linalg.inv(X)) + Zr @ Zr.T / 4 + 0.3 * np.eye(4)
        x0 = np.concatenate([[X[i, j] for (i, j) in IU], [Z[i, j] for (i, j) in IU], y])
        if interior(x0):
            break
    a0 = E_DIR * WTS  # tr X + tr Z
    A = np.vstack([a0] + [rng.normal(size=23) for _ in range(m_extra)])
    s = a0 @ x0
    x0 = x0 / s
    b = A @ x0
    c = rng.normal(size=23)
    return c, A, b, x0


if __name__ == "__main__":
    n_inst = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    rng = np.random.default_rng(2026)
    G, fixed, free = lift_problem()
    # warm up jax
    _ = gF(E_DIR); _ = hF(E_DIR)
    rows = []
    for it in range(n_inst):
        c, A, b, x0 = make_instance(rng)
        xn, steps, tn = native_solve(c, A, b, x0)
        fn = c @ xn
        row = dict(inst=it, native_obj=fn, native_newton=steps, native_time=tn,
                   native_lmin=hyp_lambda_min(xn), native_feas=float(np.abs(A @ xn - b).max()))
        for solver in ["CLARABEL", "SCS"]:
            try:
                xl, fl, wall, stime, iters, status = lift_solve(c, A, b, G, fixed, free, solver)
                row[solver] = dict(obj=fl, wall=wall, solve_time=stime, iters=iters, status=status,
                                   lmin=hyp_lambda_min(xl) if xl is not None else None,
                                   obj_diff=(fl - fn) if fl is not None else None)
            except Exception as ex:
                row[solver] = dict(error=str(ex)[:200])
        rows.append(row)
        print(json.dumps(row, default=float))
        sys.stdout.flush()
    json.dump(rows, open("bench_hyp_results.json", "w"), default=float, indent=1)
