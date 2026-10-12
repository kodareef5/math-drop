"""Explicit 23-variable nonspectrahedral hyperbolicity cone (family 095) and its
100x100 / 307-aux exact SDP lift, built from the formulas in
  A-Nonspectrahedral-Hyperbolicity-Cone-September-24-2026 (eq. form, phi, polynomial, reduced-polynomial)
  An-Exact-Semidefinite-Lift-...-October-5-2026 (eq. U, slice-pencil, moment-matrix, Thm 1.1)
Coordinates: x = (upper-tri X lexicographic (10), upper-tri Z (10), y1,y2,y3).
"""
import numpy as np

IU = [(i, j) for i in range(4) for j in range(i, 4)]  # 10 upper-tri index pairs


def sym_from_vec(v):
    M = np.zeros((4, 4), dtype=np.result_type(v, float))
    for k, (i, j) in enumerate(IU):
        M[i, j] = v[k]
        M[j, i] = v[k]
    return M


def vec_from_sym(M):
    return np.array([M[i, j] for (i, j) in IU])


def unpack(x):
    return sym_from_vec(x[:10]), sym_from_vec(x[10:20]), np.asarray(x[20:23])


def Qmat(y):
    y1, y2, y3 = y
    return np.array([[y1**2 + y2**2, -y1 * y2, -y1 * y3],
                     [-y1 * y2, y2**2 + y3**2, -y2 * y3],
                     [-y1 * y3, -y2 * y3, y3**2 + y1**2]])


def Phi(y, W):
    Q = Qmat(y)
    a, r, T = W[0, 0], W[1:, 0], W[1:, 1:]
    out = np.zeros((4, 4))
    out[0, 0] = np.trace(Q @ T)
    out[0, 1:] = -r @ Q
    out[1:, 0] = -Q @ r
    out[1:, 1:] = a * Q
    return out


def adj(X):
    return np.linalg.det(X) * np.linalg.inv(X)


def p_poly(x):
    X, Z, y = unpack(x)
    return np.linalg.det(np.linalg.det(X) * Z - Phi(y, adj(X)))


# reduced degree-16 polynomial q via the 16x16 block determinant (Cor. reduced)
Kmats = []
for i in range(3):
    K = np.zeros((4, 4))
    K[0, 1 + i] = 1.0
    K[1 + i, 0] = -1.0
    Kmats.append(K)
Cbig = np.hstack(Kmats)  # 4 x 12


def q_matrix(x):
    X, Z, y = unpack(x)
    top = np.hstack([np.kron(np.eye(3), X), Cbig.T])
    bot = np.hstack([Cbig @ np.kron(Qmat(y), np.eye(4)), Z])
    return np.vstack([top, bot])


def q_poly(x):
    return np.linalg.det(q_matrix(x))


def in_interior(x, tol=0.0):
    X, Z, y = unpack(x)
    ev = np.linalg.eigvalsh(X)
    if ev.min() <= tol:
        return False
    S = Z - Phi(y, np.linalg.inv(X))
    return np.linalg.eigvalsh((S + S.T) / 2).min() > tol


def hyp_eigs(x):
    """roots of t -> p(t e - x): eigenvalues of X (x4) and of Z - Phi_y(X^{-1}) shifted...
    computed generically by fitting the degree-16 univariate q(t e - x)."""
    ts = np.cos(np.pi * (np.arange(40) + 0.5) / 40) * 50
    e = np.zeros(23); e[[0, 4, 7, 9]] = 1; e[[10, 14, 17, 19]] = 1
    vals = np.array([q_poly(t * e - x) for t in ts])
    coef = np.polynomial.chebyshev.chebfit(ts / 50, vals, 16)
    r = np.polynomial.chebyshev.chebroots(coef) * 50
    return np.sort(r.real)


E_DIR = np.zeros(23); E_DIR[[0, 4, 7, 9]] = 1; E_DIR[[10, 14, 17, 19]] = 1


# ---------------- slice pencil L_theta (20x20) ----------------
def U_theta(th):
    w = np.exp(1j * th); c, s = np.cos(th), np.sin(th)
    return (1 / np.sqrt(2)) * np.array([[-1 / w, -w],
                                        [s / w**2, s * w**2],
                                        [c / w**2, -c * w**2]])


V0 = (1 / np.sqrt(2)) * np.array([[0, 0], [1j, 1j], [1, 1]])


def realify(F):
    return np.column_stack([F[:, 0].real, F[:, 0].imag, F[:, 1].real, F[:, 1].imag])


def Bof(r):
    B = np.zeros((4, 4))
    B[0, 1:] = r
    B[1:, 0] = -r
    return B


def L_theta(th, X, Z, eta, xi):
    F = realify(eta * U_theta(th) + xi * V0)
    Bs = np.vstack([Bof(F[:, j]) for j in range(4)])  # 16x4
    top = np.hstack([np.kron(np.eye(4), X), Bs])
    bot = np.hstack([Bs.T, Z])
    return np.vstack([top, bot])


# ---------------- the 100x100 lift ----------------
# coordinates of the 22 slice variables: 10 X, 10 Z, eta, xi
# trig basis of T_7: g_0=1, g_{2l-1}=cos(l th), g_{2l}=sin(l th), l=1..7  (15 functions)
NS = 32
THS = 2 * np.pi * np.arange(NS) / NS


def trig_coeffs(vals):
    """vals: (..., NS) samples of a trig poly of degree<=7 -> (..., 15) coefficients."""
    F = np.fft.rfft(vals, axis=-1) / NS
    out = np.zeros(vals.shape[:-1] + (15,))
    out[..., 0] = F[..., 0].real
    for l in range(1, 8):
        out[..., 2 * l - 1] = 2 * F[..., l].real
        out[..., 2 * l] = -2 * F[..., l].imag
    return out


def slice_basis_pencils(th):
    """22 matrices: L_theta evaluated at unit coordinate (linear in slice vars)."""
    mats = []
    for k in range(10):
        v = np.zeros(10); v[k] = 1
        mats.append(L_theta(th, sym_from_vec(v), np.zeros((4, 4)), 0, 0))
    for k in range(10):
        v = np.zeros(10); v[k] = 1
        mats.append(L_theta(th, np.zeros((4, 4)), sym_from_vec(v), 0, 0))
    mats.append(L_theta(th, np.zeros((4, 4)), np.zeros((4, 4)), 1, 0))
    mats.append(L_theta(th, np.zeros((4, 4)), np.zeros((4, 4)), 0, 1))
    return np.array(mats)  # 22 x 20 x 20


def build_lift():
    """Return list G of 330 sparse-ish 100x100 coefficient matrices, indexed by (ell, coord),
    so H(Lambda) = sum_{ell,c} lam[ell,c] G[ell,c]."""
    Ls = np.array([slice_basis_pencils(th) for th in THS])  # NS x 22 x 20 x 20
    f = np.array([np.ones(NS), np.cos(THS), np.sin(THS), np.cos(2 * THS), np.sin(2 * THS)])  # 5 x NS
    # entry (i,a),(j,b) with row index i*5+a
    G = np.zeros((15, 22, 100, 100))
    for a in range(5):
        for b in range(5):
            prod = f[a] * f[b]  # NS
            vals = Ls * prod[:, None, None, None]  # NS x 22 x 20 x 20
            co = trig_coeffs(np.moveaxis(vals, 0, -1))  # 22 x 20 x 20 x 15
            co[np.abs(co) < 1e-12] = 0.0
            # place into G[ell, c, i*5+a, j*5+b]
            for i in range(20):
                G[:, :, i * 5 + a, b::5] = np.moveaxis(co[:, i, :, :], -1, 0)
    return G


# output coordinates (fixed by x): ell=0 (const) with X/Z coords; eta*cos -> (ell=1, c=20); eta*sin -> (ell=2, c=20); xi -> (ell=0, c=21)
def output_index_map():
    fixed = {}
    for k in range(10):
        fixed[(0, k)] = k            # X_k
        fixed[(0, 10 + k)] = 10 + k  # Z_k
    fixed[(1, 20)] = 20  # y1 = Lambda(eta cos)
    fixed[(2, 20)] = 21  # y2 = Lambda(eta sin)
    fixed[(0, 21)] = 22  # y3 = Lambda(xi)
    return fixed


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    # 1. check p = det X * q and slice identity det L_theta = p
    for _ in range(3):
        x = rng.normal(size=23)
        X, Z, y = unpack(x)
        th = rng.uniform(0, 2 * np.pi)
        eta, xi = rng.normal(), rng.normal()
        yy = np.array([eta * np.cos(th), eta * np.sin(th), xi])
        xx = np.concatenate([x[:20], yy])
        print("p/(detX*q) =", p_poly(xx) / (np.linalg.det(X) * q_poly(xx)),
              " detL/p =", np.linalg.det(L_theta(th, X, Z, eta, xi)) / p_poly(xx))
    print("p(e) =", p_poly(E_DIR), " q(e) =", q_poly(E_DIR))
    G = build_lift()
    nz = np.count_nonzero(np.abs(G).sum(axis=(2, 3)))
    print("lift: 15x22=330 coordinate matrices, nonzero ones:", nz, "  size", G.shape[2:])
    # 2. evaluation functional at a point gives H = sum_ell g_ell(th0) * L-basis ... check H psd for a K point
    fixed = output_index_map()
    print("fixed coords:", len(fixed), "-> aux:", 330 - len(fixed))
