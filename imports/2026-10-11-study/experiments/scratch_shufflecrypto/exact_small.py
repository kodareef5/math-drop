# Exact full-permutation TV distance from uniform for (a) Thorp (coordinate-sweep form) on N=8,
# (b) swap-or-not with ideal independent round keys/functions on N=6..10.
import itertools, math, sys, numpy as np, json
def build(N):
    perms = np.array(list(itertools.permutations(range(N))), dtype=np.int8)  # row j: g as tuple g[label]=position
    M = len(perms)
    # rank via mixed radix Lehmer code (lexicographic order = itertools order)
    def rank(P):
        P = P.astype(np.int64); n = P.shape[1]; r = np.zeros(len(P), dtype=np.int64)
        for i in range(n):
            smaller = (P[:, i+1:] < P[:, i:i+1]).sum(axis=1)
            r = r * (n - i) + smaller
        return r
    assert (rank(perms) == np.arange(M)).all()
    tmap = {}
    for a in range(N):
        for b in range(a+1, N):
            Q = perms.copy()
            ma = perms == a; mb = perms == b
            Q[ma] = b; Q[mb] = a
            tmap[(a, b)] = rank(Q).astype(np.int32)
    return M, tmap
def layer(P, pairs, tmap):
    for (a, b) in pairs:
        if a == b: continue
        a, b = min(a, b), max(a, b)
        Pt = np.empty_like(P); Pt[tmap[(a, b)]] = P   # mass at g moves to tau o g
        P = 0.5 * (P + Pt)
    return P
def tv(P, M): return 0.5 * np.abs(P - 1.0 / M).sum()
res = {}
# Thorp N=8 (d=3): coordinate sweeps
N, d = 8, 3
M, tmap = build(N)
P = np.zeros(M); P[0] = 1.0
th = []
for t in range(1, 121):
    i = (t - 1) % d
    pairs = [(x, x ^ (1 << i)) for x in range(N) if not (x >> i) & 1]
    P = layer(P, pairs, tmap)
    th.append(tv(P, M))
res['thorp_8'] = th
print("Thorp N=8 TV by physical shuffle:", [f"{t}:{v:.2e}" for t, v in enumerate(th, 1) if t in (3,6,9,12,15,18,24,30,45,60,90,120)])
for N in (6, 7, 8, 9, 10):
    M, tmap = build(N)
    P = np.zeros(M); P[0] = 1.0
    sn = []
    for r in range(1, 151):
        acc = np.zeros(M)
        for K in range(N):
            pairs = sorted({(min(x, (K - x) % N), max(x, (K - x) % N)) for x in range(N)})
            acc += layer(P, pairs, tmap)
        P = acc / N
        sn.append(tv(P, M))
        if sn[-1] < 1e-12: break
    res[f'sn_{N}'] = sn
    def first(th): 
        return next((r for r, v in enumerate(sn, 1) if v <= th), None)
    print(f"SN N={N}: rounds to TV<=1/4: {first(0.25)}, <=2^-10: {first(2**-10)}, <=2^-20: {first(2**-20)}, <=2^-30: {first(2**-30)}  (lg N = {math.log2(N):.2f})")
    sys.stdout.flush()
    del tmap
def firstt(th):
    return next((t for t, v in enumerate(res['thorp_8'], 1) if v <= th), None)
print(f"Thorp N=8: shuffles to TV<=1/4: {firstt(0.25)}, <=2^-10: {firstt(2**-10)}, <=2^-20: {firstt(2**-20)}, <=2^-30: {firstt(2**-30)}")
json.dump(res, open('exact_small.json', 'w'))
