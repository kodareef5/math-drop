import numpy as np, cvxpy as cp, importlib.util, sys
spec = importlib.util.spec_from_file_location("ce", "crouzeix_exp.py")
# reuse gmres_resids/fov_boundary without re-running experiments: copy definitions
src = open("crouzeix_exp.py").read()
defs = src[src.index("def numerical_abscissa"):src.index('print("\\n== (b)')]
exec(defs)
rng = np.random.default_rng(1)
m = 200; c = 0.6
A2 = (np.diag(2*np.ones(m)) + np.diag((-1-c)*np.ones(m-1), -1) + np.diag((-1+c)*np.ones(m-1), 1))
b2 = rng.standard_normal(m)
r2 = gmres_resids(A2.astype(complex), b2.astype(complex), 200)
idx = np.where(r2 < 1e-8)[0]
print("conv-diff m=200 c=0.6: actual GMRES iterations to 1e-8:", int(idx[0]) if len(idx) else None, "; disk-FOV bound predicts ~1.56e5 (C=2) / 1.58e5 (C=2.414)")

print("\nPer-matrix optimal similarity constant kappa (Thm structural LMI) for Omega=disk(0,r), T=A/r:")
for n in [5, 10, 20, 40]:
    S = np.diag(np.ones(n-1), 1); w = np.cos(np.pi/(n+1))
    for fac in [1.001, 1.05, 1.5]:
        r = fac*w; T = S/r
        H = cp.Variable((n, n), symmetric=True); tau = cp.Variable()
        cons = [H >> np.eye(n), tau*np.eye(n) - H >> 0, H - T.T @ H @ T >> 0]
        prob = cp.Problem(cp.Minimize(tau), cons); prob.solve(solver=cp.SCS, eps=1e-7, max_iters=200000)
        print(f"  shift n={n:3d}, r={fac}*w(A): kappa = {np.sqrt(tau.value):.4f}  (theorem: <= 2)")
