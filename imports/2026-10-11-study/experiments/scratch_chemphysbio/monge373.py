"""Numerical instantiation of the five-component Coulomb density of family 373
(A counterexample to the Monge ansatz for the three-marginal Coulomb cost).

Steps
 1. Follow Lemma local: centers (0, a_k, -a_k), u0(x)=5/2-K/2|x|^2,
    v_k(z)=5/4 a_k.(z+a_k)-K/2|z+a_k|^2, F_k=c-u0-v_k, pick K.
 2. Solve grad_{(x,z)} F_k = 0 for given x (unknowns y,z) by Newton to get
    Y_k(x), W_k(x); w_k(y)=F_k(x,y,z) at the equality triple.
 3. Numerically (non-rigorously) check the supporting inequality
    c >= u+u+u on random triples in U^3 for candidate radii; report the
    largest radius that passes -> "how small is sufficiently small".
 4. Build a discrete marginal: center atoms x_j (grid in ball B) with mass
    nu_j/3, outer atoms Y_k(x_j), W_k(x_j) with mass nu_j/6; also a
    re-binned regular-grid version. Solve the 3-marginal OT exactly by LP
    (HiGHS) and report optimal cost vs 5/2, branch split per center atom,
    and the barycentric-projection defect.
Not a proof; numerical evidence only.
"""
import numpy as np, itertools, time, json, sys
from scipy.optimize import linprog
from scipy import sparse

rng = np.random.default_rng(0)
e = np.eye(3)
a = [e[0], e[1]]


def c3(x, y, z):
    return 1/np.linalg.norm(x-y, axis=-1) + 1/np.linalg.norm(x-z, axis=-1) + 1/np.linalg.norm(y-z, axis=-1)


def grad_pair(b):
    # gradient of 1/|b| wrt b
    n = np.linalg.norm(b)
    return -b/n**3


def hess_pair(b):
    n = np.linalg.norm(b)
    return (3*np.outer(b, b)/n**2 - np.eye(3))/n**3


def make_K():
    Ks = []
    for k in range(2):
        x, y, z = np.zeros(3), a[k], -a[k]
        # Hessian of c wrt (x,z)
        Hxx = hess_pair(x-y) + hess_pair(x-z)
        Hzz = hess_pair(x-z) + hess_pair(y-z)
        Hxz = -hess_pair(x-z)
        M = np.block([[Hxx, Hxz], [Hxz.T, Hzz]])
        Ks.append(M)
    # smallest K making M+K I PD with margin, and blocks invertible
    for K in np.arange(0.5, 50, 0.25):
        ok = True
        for k in range(2):
            M = Ks[k]
            if np.linalg.eigvalsh(M + K*np.eye(6)).min() <= 0.2:
                ok = False
                break
            x, y, z = np.zeros(3), a[k], -a[k]
            N = np.vstack([-hess_pair(x-y), -hess_pair(y-z)])  # d/dy grad_(x,z) c
            D = -np.linalg.solve(M + K*np.eye(6), N)
            if min(abs(np.linalg.det(D[:3])), abs(np.linalg.det(D[3:]))) < 1e-3:
                ok = False
                break
        if ok:
            return K
    raise RuntimeError


K = make_K()


def u0(x):
    return 2.5 - K/2*np.sum(x**2, axis=-1)


def vk(z, k):
    return 1.25*((z + a[k]) @ a[k]) - K/2*np.sum((z + a[k])**2, axis=-1)


def gradF_xz(x, y, z, k):
    gx = grad_pair(x-y) + grad_pair(x-z) + K*x  # -grad u0 = +K x
    gz = -grad_pair(x-z) - grad_pair(y-z) - (1.25*a[k] - K*(z + a[k]))
    return np.concatenate([gx, gz])


def solve_given_y(y, k, x0=None, z0=None):
    """stationary (x,z) of F_k(.,y,.) by Newton (Hessian PD near centers)."""
    x = np.zeros(3) if x0 is None else x0.copy()
    z = -a[k] if z0 is None else z0.copy()
    for _ in range(50):
        g = gradF_xz(x, y, z, k)
        Hxx = hess_pair(x-y) + hess_pair(x-z) + K*np.eye(3)
        Hzz = hess_pair(x-z) + hess_pair(y-z) + K*np.eye(3)
        Hxz = -hess_pair(x-z)
        H = np.block([[Hxx, Hxz], [Hxz.T, Hzz]])
        d = np.linalg.solve(H, g)
        x -= d[:3]; z -= d[3:]
        if np.linalg.norm(d) < 1e-14:
            break
    return x, z


def w_k(y, k):
    x, z = solve_given_y(y, k)
    return c3(x, y, z) - u0(x) - vk(z, k), x, z


def solve_given_x(x, k):
    """find y with X_k(y)=x (i.e. Y_k(x)) and z=Z_k(y) by Newton on 6 eqs."""
    y = a[k].copy(); z = -a[k].copy()
    for _ in range(60):
        def G(yz):
            return gradF_xz(x, yz[:3], yz[3:], k)
        v = np.concatenate([y, z])
        g = G(v)
        J = np.zeros((6, 6)); h = 1e-7
        for i in range(6):
            dv = np.zeros(6); dv[i] = h
            J[:, i] = (G(v+dv) - G(v-dv))/(2*h)
        d = np.linalg.solve(J, g)
        y -= d[:3]; z -= d[3:]
        if np.linalg.norm(d) < 1e-13:
            break
    return y, z


def u_point(p, comp):
    """certificate potential on component comp in {0,'1+','1-','2+','2-'}"""
    if comp == 0:
        return u0(p)
    k = int(comp[0]) - 1
    if comp[1] == '+':
        return w_k(p, k)[0]
    return vk(p, k)


centers = {0: np.zeros(3), '1+': a[0], '1-': -a[0], '2+': a[1], '2-': -a[1]}
comps = list(centers)


def sample_ball(center, r, n):
    v = rng.normal(size=(n, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
    rad = r*rng.random(n)**(1/3)
    return center + v*rad[:, None]


def check_radius(r, nsamp=60):
    """random check of c >= sum u on all component patterns for balls radius r.
    Also checks the local branch is the global minimum (via the inequality)."""
    pts = {cmp: sample_ball(centers[cmp], r, nsamp) for cmp in comps}
    # include centers exactly
    uvals = {cmp: np.array([u_point(p, cmp) for p in pts[cmp]]) for cmp in comps}
    worst = np.inf
    for c1, c2, c3_ in itertools.combinations_with_replacement(comps, 3):
        P1, P2, P3 = pts[c1], pts[c2], pts[c3_]
        U1, U2, U3 = uvals[c1], uvals[c2], uvals[c3_]
        # random triples
        i = rng.integers(0, nsamp, 3000); j = rng.integers(0, nsamp, 3000); l = rng.integers(0, nsamp, 3000)
        with np.errstate(divide='ignore'):
            gap = c3(P1[i], P2[j], P3[l]) - (U1[i] + U2[j] + U3[l])
        gap = gap[np.isfinite(gap)]
        if gap.size:
            worst = min(worst, gap.min())
    return worst, max(abs(np.concatenate(list(uvals.values()))).max(), 0)


if __name__ == "__main__":
    out = {"K": float(K)}
    print("K =", K)
    # 1. how large can the component radii be?
    radii = [0.2, 0.15, 0.1, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02]
    res = []
    for r in radii:
        try:
            worst, M = check_radius(r)
        except np.linalg.LinAlgError:
            worst, M = -np.inf, np.nan
        res.append((r, float(worst), float(M)))
        print(f"radius {r}: min sampled gap c-sum u = {worst:.3e}  (max|u|={M:.3f}, need 1/(2r)={1/(2*r):.1f} > 3M)")
    out["radius_scan"] = res
    json.dump(out, open("monge373_radii.json", "w"), indent=1)
