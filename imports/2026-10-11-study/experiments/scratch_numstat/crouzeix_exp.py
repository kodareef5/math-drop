"""Quick numerical checks for family 325 (complete Crouzeix, constant 2 vs 1+sqrt2)."""
import numpy as np, scipy.linalg as sla
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(0)
K_CP = 1 + np.sqrt(2)

print("== (a) FOV-bound iteration counts: k = ceil(log(C/tol)/-log(rho)), tol=1e-8")
tol = 1e-8
for rho in [0.5, 0.9, 0.99, 0.999]:
    k_old = np.ceil(np.log(K_CP / tol) / -np.log(rho))
    k_new = np.ceil(np.log(2.0 / tol) / -np.log(rho))
    print(f"rho={rho:6}: k(1+sqrt2)={int(k_old):6d}  k(2)={int(k_new):6d}  saved={int(k_old-k_new):4d} ({100*(k_old-k_new)/k_old:.2f}%)")

def numerical_abscissa(A):
    return np.linalg.eigvalsh((A + A.conj().T) / 2).max()

def fov_boundary(A, m=720):
    pts = []
    for th in np.linspace(0, 2*np.pi, m, endpoint=False):
        H = (np.exp(1j*th)*A + np.exp(-1j*th)*A.conj().T) / 2
        w, V = np.linalg.eigh(H)
        v = V[:, -1]
        pts.append(v.conj() @ A @ v)
    return np.array(pts)

def gmres_resids(A, b, kmax):
    n = len(b); Q = np.zeros((n, kmax+1), complex); H = np.zeros((kmax+1, kmax), complex)
    beta = np.linalg.norm(b); Q[:, 0] = b / beta; res = [1.0]
    for k in range(kmax):
        w = A @ Q[:, k]
        for j in range(k+1):
            H[j, k] = Q[:, j].conj() @ w; w = w - H[j, k]*Q[:, j]
        for j in range(k+1):  # reorth
            h = Q[:, j].conj() @ w; H[j, k] += h; w = w - h*Q[:, j]
        H[k+1, k] = np.linalg.norm(w)
        if H[k+1, k] > 1e-14: Q[:, k+1] = w / H[k+1, k]
        e1 = np.zeros(k+2, complex); e1[0] = beta
        y, *_ = np.linalg.lstsq(H[:k+2, :k+1], e1, rcond=None)
        res.append(np.linalg.norm(H[:k+2, :k+1] @ y - e1) / beta)
    return np.array(res)

print("\n== (b) GMRES actual vs FOV bounds C*rho^k (W(A) a disk => min-max = rho^k exactly)")
n = 200
S = np.diag(np.ones(n-1), -1)
alpha = 0.9
A = np.eye(n) + alpha*S          # W(A) = disk(1, alpha*cos(pi/(n+1)))
rho = alpha*np.cos(np.pi/(n+1))
b = np.zeros(n); b[0] = 1.0
r = gmres_resids(A.astype(complex), b.astype(complex), 200)
for k in [10, 60, 120, 180]:
    print(f"Jordan-type alpha=0.9 k={k:3d}: actual={r[k]:.3e}  2.414*rho^k={K_CP*rho**k:.3e}  2*rho^k={2*rho**k:.3e}  ratio actual/(2rho^k)={r[k]/(2*rho**k):.3f}")
def first_below(res, t):
    idx = np.where(res < t)[0]; return int(idx[0]) if len(idx) else None
print("  iterations to 1e-8: actual", first_below(r, 1e-8), " bound(1+sqrt2)", int(np.ceil(np.log(K_CP/1e-8)/-np.log(rho))), " bound(2)", int(np.ceil(np.log(2/1e-8)/-np.log(rho))))

# convection-diffusion 1D upwind: A = tridiag(-1-c, 2, -1+c)*... nonnormal, GMRES vs FOV bound
m = 200; c = 0.6
A2 = (np.diag(2*np.ones(m)) + np.diag((-1-c)*np.ones(m-1), -1) + np.diag((-1+c)*np.ones(m-1), 1))
W = fov_boundary(A2)
# W(A2) is (nearly) an ellipse symmetric about the real axis; enclosing disk centered at cen
xmin, xmax = W.real.min(), W.real.max(); cen = (xmin + xmax)/2
rad = np.abs(W - cen).max()
rho2 = rad/abs(cen)
b2 = rng.standard_normal(m)
r2 = gmres_resids(A2.astype(complex), b2.astype(complex), 150)
print(f"conv-diff m={m} c={c}: W(A) real range [{xmin:.4f},{xmax:.4f}], enclosing-disk rho={rho2:.5f}")
print("  iterations to 1e-8: actual", first_below(r2, 1e-8), " disk-FOV bound(1+sqrt2)", int(np.ceil(np.log(K_CP/1e-8)/-np.log(rho2))) if rho2 < 1 else 'inf', " bound(2)", int(np.ceil(np.log(2/1e-8)/-np.log(rho2))) if rho2 < 1 else 'inf')

print("\n== (c) Frechet derivative of exp: exact ||L_exp(A)||_{F->F} vs bounds C*max_{W(A)}|exp'| = C*exp(omega(A))")
def frechet_exp_norm(A):
    n = A.shape[0]; Kmat = np.zeros((n*n, n*n))
    for j in range(n*n):
        E = np.zeros(n*n); E[j] = 1; E = E.reshape(n, n)
        _, L = sla.expm_frechet(A, E)
        Kmat[:, j] = L.ravel()
    return np.linalg.norm(Kmat, 2)
cases = {}
n = 12
cases['random/sqrt(n)'] = rng.standard_normal((n, n))/np.sqrt(n)
cases['grcar(12)'] = sla.toeplitz(np.r_[1, -1, np.zeros(n-2)], np.r_[1, 1, 1, 1, np.zeros(n-4)])
cases['-I + 3*shift'] = -np.eye(n) + 3*np.diag(np.ones(n-1), 1)
T = np.triu(rng.standard_normal((n, n)), 1)*2; np.fill_diagonal(T, -np.linspace(0.5, 3, n))
cases['stable triangular, strong nonnormal'] = T
print(f"{'matrix':38s} {'||L||':>10s} {'1*e^w (lognorm)':>16s} {'4*e^w':>10s} {'5.83*e^w':>10s}")
for name, A in cases.items():
    Ln = frechet_exp_norm(A); w = numerical_abscissa(A)
    print(f"{name:38s} {Ln:10.4g} {np.exp(w):16.4g} {4*np.exp(w):10.4g} {K_CP**2*np.exp(w):10.4g}")

print("\n== (d) Crouzeix-Kressner nilpotent example: A=B=[[0,1],[0,0]], f(x,y)=xy")
J = np.array([[0., 1.], [0., 0.]])
num = np.linalg.norm(np.kron(J, J), 2)   # f{A,B} acting on vec(C) ~ B (x) A
print(f"  ||f{{A,B}}|| = {num:.4f}, max_W(A)xW(B)|xy| = {0.25}, ratio = {num/0.25:.4f} (sharp constant 4; CK proved 5.83; scalar-2 + CP-complete gives 4.83)")

print("\n== (e) Frechet-derivative worst-case ratio search ||Df{A}||/max_W|f'| for f=z^k, small A (lower bound on best constant)")
def fov_max_abs_poly_deriv(A, k):
    W = fov_boundary(A, 360)   # boundary suffices for |z|^(k-1) (subharmonic)
    return (k*np.abs(W)**(k-1)).max()
def frechet_poly_norm(A, k):
    n = A.shape[0]; I = np.eye(n)
    Kmat = sum(np.kron(np.linalg.matrix_power(A.T, k-1-j), np.linalg.matrix_power(A, j)) for j in range(k))
    return np.linalg.norm(Kmat, 2)
best = (0, None)
for trial in range(400):
    nn = rng.integers(2, 4); k = rng.integers(2, 5)
    A = rng.standard_normal((nn, nn)) + 1j*rng.standard_normal((nn, nn))
    A = np.triu(A)  # Schur form
    r_ = frechet_poly_norm(A, k)/fov_max_abs_poly_deriv(A, k)
    if r_ > best[0]: best = (r_, (nn, k))
print(f"  best ratio found by random search: {best[0]:.4f} at (n,k)={best[1]}  (known upper bound now 4; earlier 5.83)")
r_J = frechet_poly_norm(J, 2)/fov_max_abs_poly_deriv(J, 2)
print(f"  2x2 Jordan, f=z^2: ratio {r_J:.4f}")
