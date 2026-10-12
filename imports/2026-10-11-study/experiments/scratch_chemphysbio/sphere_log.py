"""Family 090 corollary (Brauchart-Hardin-Saff linear term, now a theorem):
E_log(n) = (1/2 - log 2) n^2 - (n/2) log n + C_BHS n + o(n),
C_BHS = 2 log 2 + (1/2) log(2/3) + 3 log(sqrt(pi)/Gamma(1/3)).
Experiment: locally optimise n points on S^2 (start: Fibonacci/spiral points),
report the normalised linear coefficient (E - lead terms)/n vs C_BHS.
Energy convention: sum over ORDERED pairs i != j of -log|y_i - y_j| (as in the paper).
"""
import numpy as np, json, math
from scipy.optimize import minimize

C_BHS = 2*math.log(2) + 0.5*math.log(2/3) + 3*math.log(math.sqrt(math.pi)/math.gamma(1/3))


def fib(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2*i/n)
    th = math.pi*(1 + 5**0.5)*i
    return np.stack([np.cos(th)*np.sin(phi), np.sin(th)*np.sin(phi), np.cos(phi)], 1)


def energy_grad(flat, n):
    X = flat.reshape(n, 3)
    nr = np.linalg.norm(X, axis=1, keepdims=True)
    Y = X / nr
    D = Y[:, None, :] - Y[None, :, :]
    r2 = np.sum(D**2, -1)
    np.fill_diagonal(r2, 1.0)
    E = -0.5*np.sum(np.log(r2)) * 1.0  # ordered pairs: sum_{i!=j} -log r = -0.5*sum log r^2
    G = -2*np.sum(D / r2[:, :, None], axis=1)  # dE/dY (ordered pairs, both i,j terms)
    # chain rule through normalisation
    GY = G - np.sum(G*Y, 1, keepdims=True)*Y
    GX = GY / nr
    return E, GX.ravel()


def lead(n):
    return (0.5 - math.log(2))*n*n - 0.5*n*math.log(n)


out = {"C_BHS": C_BHS, "rows": []}
for n in [100, 200, 400, 800, 1600]:
    x0 = fib(n).ravel()
    E0, _ = energy_grad(x0, n)
    r = minimize(energy_grad, x0, args=(n,), jac=True, method='L-BFGS-B', options={'maxiter': 3000, 'gtol': 1e-9})
    E1 = r.fun
    row = dict(n=n, fib_coeff=(E0 - lead(n))/n, opt_coeff=(E1 - lead(n))/n, gap_to_CBHS=(E1 - lead(n))/n - C_BHS,
               iters=r.nit)
    out["rows"].append(row)
    print(row, flush=True)
print("C_BHS =", C_BHS)
json.dump(out, open("sphere_log.json", "w"), indent=1)
