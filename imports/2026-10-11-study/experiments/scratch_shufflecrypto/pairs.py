# Exact law of the ordered positions of 2 cards (a lower bound for full-permutation TV) under
# (a) Thorp coordinate sweeps (d layers = d physical shuffles), (b) swap-or-not rounds (random K in Z_N, fair F).
import numpy as np, math, json, sys
def thorp_layer(P, i):
    N = P.shape[0]; e = 1 << i
    idx = np.arange(N); fl = idx ^ e
    G = (P + P[fl, :] + P[:, fl] + P[fl][:, fl]) / 4.0
    # targets on the same i-edge: (a, a^e)
    same = (P[idx, fl] + P[fl, idx]) / 2.0
    G[idx, fl] = same
    return G
def tv2(P):
    N = P.shape[0]; U = 1.0 / (N * (N - 1))
    M = P.copy(); np.fill_diagonal(M, U)  # diagonal excluded
    return 0.5 * (np.abs(M - U).sum())
out = {}
print("Thorp: 2-card TV after v sweeps (start cards at 0 and 1; translation-invariant chain)")
for d in range(3, 11):
    N = 2 ** d
    worst = []
    starts = [1, N - 1, N // 2 + 1] if N > 8 else list(range(1, N))
    res = None
    for c in starts:
        P = np.zeros((N, N)); P[0, c] = 1.0
        tvs = []
        for v in range(1, 9):
            for i in range(d):
                P = thorp_layer(P, i)
            tvs.append(tv2(P))
        res = tvs if res is None else [max(a, b) for a, b in zip(res, tvs)]
    out[f"thorp_{N}"] = res
    rates = [res[k + 1] / res[k] for k in range(3, 6) if res[k] > 1e-300]
    print(f"N=2^{d}: " + " ".join(f"{t:.2e}" for t in res) + f" | per-sweep ratio ~ {np.mean(rates):.3g}, 1/N = {1/N:.3g}")
    sys.stdout.flush()
print("\nSwap-or-not: 2-card TV after r rounds (worst start over a few pairs)")
def sn_round(P):
    N = P.shape[0]; acc = np.zeros_like(P); idx = np.arange(N)
    for K in range(N):
        part = (K - idx) % N
        fixed = part == idx
        # generic: each card independently moves to partner w.p. 1/2 (stays if fixed point)
        A = 0.5 * (P + P[part, :]); A = 0.5 * (A + A[:, part])
        # correct targets (a, b) with b = partner(a) (same pair): law = (P(a,b)+P(b,a))/2
        same = (P[idx, part] + P[part, idx]) / 2.0
        A[idx, part] = np.where(fixed, A[idx, part], same)
        acc += A
    return acc / N
for N in (8, 16, 32, 64, 128, 256):
    res = None
    for c in (1, N // 2, N - 1):
        P = np.zeros((N, N)); P[0, c] = 1.0
        tvs = []
        for r in range(1, 61):
            P = sn_round(P); tvs.append(tv2(P))
        res = tvs if res is None else [max(a, b) for a, b in zip(res, tvs)]
    out[f"sn_{N}"] = res
    def first(th): return next((r for r, v in enumerate(res, 1) if v <= th), None)
    rate = (res[49] / res[29]) ** (1 / 20) if res[49] > 0 else float('nan')
    print(f"N={N}: rounds to 2-card TV<=2^-10: {first(2**-10)}, <=2^-20: {first(2**-20)}, <=2^-30: {first(2**-30)}; asymptotic per-round ratio {rate:.4f}")
    sys.stdout.flush()
json.dump(out, open('pairs_out.json', 'w'))
