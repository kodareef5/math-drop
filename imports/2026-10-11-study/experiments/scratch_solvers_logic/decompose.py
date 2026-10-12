"""Replay the exact instances behind data/H_*.jsonl (deterministic RNG) and decompose Var(H)
into the part explained by Wilson-type global 'bystander' statistics (which fluctuate on the
sqrt(n) scale) and a residual.  Statistics on the prefix of m0 = round(4.267 n) clauses:
  S1 = # clauses containing a variable that occurs exactly once in the prefix (Wilson's partially free clauses)
  S0 = # variables that do not occur at all in the prefix
"""
import json, glob, random, numpy as np, math, collections
def replay(n, seed, count):
    rng = random.Random(seed); out = []
    for _ in range(count):
        M = 8 * n; cl = []
        for _ in range(M):
            vs = rng.sample(range(1, n + 1), 3)
            cl.append([v if rng.random() < 0.5 else -v for v in vs])
        out.append(cl)
    return out
res = []
for f in sorted(glob.glob('data/H_*.jsonl'), key=lambda s: int(s.split('_')[1].split('.')[0])):
    L = [json.loads(l) for l in open(f)]
    n = L[0]['n']
    if len(L) < 50: continue
    byseed = collections.defaultdict(list)
    for r in L: byseed[r['seed']].append(r)
    H, S0, S1 = [], [], []
    m0 = round(4.267 * n)
    for seed, rs in byseed.items():
        inst = replay(n, seed, len(rs))
        for r, cl in zip(rs, inst):
            cnt = collections.Counter(abs(l) for c in cl[:m0] for l in c)
            S0.append(n - len(cnt))
            S1.append(sum(1 for c in cl[:m0] if any(cnt[abs(l)] == 1 for l in c)))
            H.append(r['H'])
    H, S0, S1 = map(lambda a: np.array(a, float), (H, S0, S1))
    X = np.column_stack([np.ones_like(H), S0 - S0.mean(), S1 - S1.mean()])
    beta, *_ = np.linalg.lstsq(X, H, rcond=None)
    fitted = X @ beta; resid = H - fitted
    vH, vexp, vres = H.var(ddof=1), fitted.var(ddof=1), resid.var(ddof=1)
    res.append((n, len(H), vH, vexp, vres, beta[1], beta[2], S0.std(), S1.std()))
print(f"{'n':>4} {'N':>5} {'Var H':>8} {'explained':>9} {'resid':>8} {'R2':>5} {'expl/n':>7} {'resid/n^(2/3)':>13} {'resid/n':>8}  coef(S0) coef(S1)  sd(S0)/sqrt n sd(S1)/sqrt n")
for n, N, vH, ve, vr, b0, b1, s0, s1 in res:
    print(f"{n:>4} {N:>5} {vH:8.1f} {ve:9.1f} {vr:8.1f} {ve/vH:5.2f} {ve/n:7.3f} {vr/n**(2/3):13.3f} {vr/n:8.3f}  {b0:8.3f} {b1:8.3f}  {s0/math.sqrt(n):12.3f} {s1/math.sqrt(n):12.3f}")
