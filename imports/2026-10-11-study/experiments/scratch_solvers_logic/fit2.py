"""Fit Var(H_n) = c1 n + c2 n^(2/3) (Wilson/OpenAI sqrt(n) noise + an 'intrinsic' nu=1.5 term),
and compare to the pure power law. Bootstrap standard errors."""
import json, glob, numpy as np, math
rng = np.random.default_rng(0)
data = {}
for f in glob.glob('data/H_*.jsonl'):
    L = [json.loads(l) for l in open(f)]
    if len(L) >= 150: data[L[0]['n']] = np.array([r['H'] for r in L], float)
ns = np.array(sorted(data)); V = np.array([data[n].var(ddof=1) for n in ns])
se = np.array([np.std([rng.choice(data[n], len(data[n])).var(ddof=1) for _ in range(300)]) for n in ns])
w = 1 / se ** 2
def wls(X, y, w):
    W = np.diag(w); cov = np.linalg.inv(X.T @ W @ X); b = cov @ X.T @ W @ y
    chi2 = ((y - X @ b) ** 2 * w).sum(); return b, np.sqrt(np.diag(cov)), chi2
X = np.column_stack([ns, ns ** (2 / 3)])
b, e, chi2 = wls(X, V, w)
print("n:", ns.tolist()); print("Var(H):", np.round(V, 1).tolist(), "+-", np.round(se, 1).tolist())
print(f"two-term fit Var = c1 n + c2 n^(2/3): c1={b[0]:.2f}+-{e[0]:.2f}, c2={b[1]:.2f}+-{e[1]:.2f}, chi2={chi2:.2f} on {len(ns)-2} dof")
if b[0] > 0: print(f"   crossover n* where c1 n = c2 n^(2/3): n*={(b[1]/b[0])**3:.0f}")
Xp = np.column_stack([np.log(ns), np.ones_like(ns)]); bp, ep, chi2p = wls(Xp, np.log(V), (V / se) ** 2)
print(f"power law Var ~ n^{bp[0]:.3f}+-{ep[0]:.3f} (=> sd ~ n^{bp[0]/2:.3f}, effective nu = {1/(1-bp[0]/2):.2f}), chi2={chi2p:.2f} on {len(ns)-2} dof")
for N in (1000, 10000, 100000):
    lin = b[0] * N; tot = lin + b[1] * N ** (2/3)
    print(f"   extrapolated n={N}: linear share of Var = {lin/tot:.2f}; effective local nu = ", end='')
    d = 1e-3; f = lambda x: 0.5 * math.log(b[0] * x + b[1] * x ** (2/3)); beta = (f(N * (1 + d)) - f(N)) / math.log(1 + d)
    print(f"{1/(1-beta):.2f}")
