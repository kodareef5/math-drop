"""Replay the exact instances behind data/H_*.jsonl and regress H on extensive 'disorder'
statistics of the prefix with m0 = round(4.267 n) clauses. Each statistic is a sum over
variables (sd ~ sqrt n), so the variance it explains is the sqrt(n)-scale (nu = 2) component
predicted by Wilson-type arguments. Residual = everything else (the 'intrinsic' window).
Out-of-sample R^2 via 5-fold CV guards against overfitting."""
import json, glob, random, numpy as np, math, collections, sys
def replay(n, seed, count, M_factor=8):
    rng = random.Random(seed); out = []
    for _ in range(count):
        M = M_factor * n; cl = []
        for _ in range(M):
            vs = rng.sample(range(1, n + 1), 3)
            cl.append([v if rng.random() < 0.5 else -v for v in vs])
        out.append(cl)
    return out
def feats(cl, n, m0):
    pos = np.zeros(n + 1); neg = np.zeros(n + 1)
    for c in cl[:m0]:
        for l in c:
            if l > 0: pos[l] += 1
            else: neg[-l] += 1
    pos, neg = pos[1:], neg[1:]; deg = pos + neg
    imb = (pos - neg) ** 2
    return [imb.sum(),                  # sign imbalance
            (deg ** 2).sum(),           # degree heterogeneity
            (deg <= 8).sum(),           # low-degree variables
            (np.minimum(pos, neg) <= 2).sum(),  # nearly-pure variables
            (np.abs(pos - neg) ** 3).sum()]
names = ['imb2', 'deg2', 'deg<=8', 'minpn<=2', 'imb3']
rows = []
files = sorted(glob.glob('data/H_*.jsonl'), key=lambda s: int(s.split('_')[1].split('.')[0]))
for f in files:
    L = [json.loads(l) for l in open(f)]
    if len(L) < 60: continue
    n = L[0]['n']; m0 = round(4.267 * n)
    byseed = collections.defaultdict(list)
    for r in L: byseed[r['seed']].append(r)
    H, X = [], []
    for seed, rs in byseed.items():
        rs.sort(key=lambda r: r['i'])
        for r, cl in zip(rs, replay(n, seed, len(rs))):
            H.append(r['H']); X.append(feats(cl, n, m0))
    H = np.array(H, float); X = np.array(X, float)
    Z = (X - X.mean(0)) / X.std(0)
    A = np.column_stack([np.ones(len(H)), Z])
    coef, *_ = np.linalg.lstsq(A, H, rcond=None)
    fit = A @ coef
    # 5-fold CV
    idx = np.arange(len(H)); np.random.default_rng(1).shuffle(idx); folds = np.array_split(idx, 5); pred = np.zeros_like(H)
    for k in range(5):
        te = folds[k]; tr = np.setdiff1d(idx, te)
        c, *_ = np.linalg.lstsq(A[tr], H[tr], rcond=None); pred[te] = A[te] @ c
    r2cv = 1 - ((H - pred) ** 2).sum() / ((H - H.mean()) ** 2).sum()
    vH = H.var(ddof=1); vexp = max(r2cv, 0) * vH; vres = vH - vexp
    # single strongest predictor
    cors = [np.corrcoef(Z[:, j], H)[0, 1] for j in range(Z.shape[1])]
    rows.append((n, len(H), vH, r2cv, vexp, vres, cors))
    print(f"n={n:4d} N={len(H):5d} Var(H)={vH:7.1f}  CV-R2={r2cv:5.3f}  explained/n={vexp/n:6.3f}  resid/n^(2/3)={vres/n**(2/3):6.2f}  resid/n={vres/n:5.2f}  corr: " + ' '.join(f"{nm}={c:+.2f}" for nm, c in zip(names, cors)), flush=True)
