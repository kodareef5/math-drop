"""At the empirical median clause count m* (P(SAT) ~ 1/2), how well does the formula's literal-sign
imbalance sum_v (pos_v - neg_v)^2 alone predict SAT vs UNSAT? (SAT iff H > m*)."""
import json, glob, random, numpy as np, collections
def replay(n, seed, count):
    rng = random.Random(seed); out = []
    for _ in range(count):
        cl = []
        for _ in range(8 * n):
            vs = rng.sample(range(1, n + 1), 3)
            cl.append([v if rng.random() < 0.5 else -v for v in vs])
        out.append(cl)
    return out
def auc(score, label):
    s1 = score[label == 1]; s0 = score[label == 0]
    r = np.argsort(np.argsort(np.concatenate([s1, s0]), kind='mergesort')) + 1
    return (r[:len(s1)].sum() - len(s1) * (len(s1) + 1) / 2) / (len(s1) * len(s0))
for f in sorted(glob.glob('data/H_*.jsonl'), key=lambda s: int(s.split('_')[1].split('.')[0])):
    L = [json.loads(l) for l in open(f)]
    if len(L) < 150: continue
    n = L[0]['n']; H = np.array([r['H'] for r in L]); mstar = int(np.median(H))
    byseed = collections.defaultdict(list)
    for r in L: byseed[r['seed']].append(r)
    imb, lab = [], []
    for seed, rs in byseed.items():
        rs.sort(key=lambda r: r['i'])
        for r, cl in zip(rs, replay(n, seed, len(rs))):
            pos = np.zeros(n + 1); neg = np.zeros(n + 1)
            for c in cl[:mstar]:
                for l in c:
                    if l > 0: pos[l] += 1
                    else: neg[-l] += 1
            imb.append(((pos - neg) ** 2).sum()); lab.append(int(r['H'] > mstar))
    imb, lab = np.array(imb), np.array(lab)
    print(f"n={n:4d} N={len(L):5d} m*={mstar} (alpha={mstar/n:.3f}) P(SAT at m*)={lab.mean():.2f}  AUC(sign-imbalance -> SAT)={auc(imb, lab):.3f}", flush=True)
