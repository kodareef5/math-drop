import json, glob, numpy as np, math
rng = np.random.default_rng(0)
rows = []
for f in sorted(glob.glob('data/H_*.jsonl'), key=lambda s: int(s.split('_')[1].split('.')[0])):
    L = [json.loads(l) for l in open(f)]
    n = L[0]['n']; H = np.array([r['H'] for r in L], dtype=float)
    def stats(H):
        q = np.quantile(H, [0.1, 0.25, 0.5, 0.75, 0.9])
        return H.mean(), H.std(ddof=1), q[4] - q[0], q[3] - q[1], q[2]
    m, s, w1090, iqr, med = stats(H)
    B = np.array([stats(rng.choice(H, len(H))) for _ in range(400)])
    se = B.std(axis=0)
    rows.append((n, len(H), m, s, w1090, iqr, med, se))
print(f"{'n':>4} {'N':>5} {'E[H]/n':>8} {'sd(H)':>7}±   {'sd/sqrt n':>9} {'W10-90':>7}±  {'W/sqrt n':>8} {'IQR':>6}  {'alpha_50%':>9}")
for n, N, m, s, w, iqr, med, se in rows:
    print(f"{n:>4} {N:>5} {m/n:8.4f} {s:7.2f}±{se[1]:4.2f} {s/math.sqrt(n):9.3f} {w:7.1f}±{se[2]:3.1f} {w/math.sqrt(n):8.3f} {iqr:6.1f}  {med/n:9.4f}")
# power-law fits sd ~ n^beta (beta = 1/2 <=> nu = 2 in clause count: density window ~ n^{beta-1} = n^{-1/nu})
ns = np.array([r[0] for r in rows], float)
for name, col, secol in [('sd(H)', 3, 1), ('W10-90', 4, 2)]:
    y = np.array([r[col] for r in rows]); e = np.array([r[7][secol] for r in rows])
    wts = (y / e) ** 2
    A = np.vstack([np.log(ns), np.ones_like(ns)]).T
    W = np.diag(wts)
    beta, c = np.linalg.solve(A.T @ W @ A, A.T @ W @ np.log(y))
    cov = np.linalg.inv(A.T @ W @ A)
    print(f"fit {name} ~ n^{beta:.3f} (±{math.sqrt(cov[0,0]):.3f})  => density-window exponent {beta-1:.3f}, nu = 1/(1-beta) = {1/(1-beta):.2f}")
    # local slopes
    for i in range(len(ns) - 1):
        b = math.log(y[i+1] / y[i]) / math.log(ns[i+1] / ns[i])
        print(f"   local slope {int(ns[i])}->{int(ns[i+1])}: beta={b:.3f}  nu={1/(1-b):.2f}")
