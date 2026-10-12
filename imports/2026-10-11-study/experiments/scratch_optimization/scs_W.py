"""Forced-occurrence lower bound W <= OPT for shortest common superstring
(family 128: A-Polynomial-Time-2-Approximation-for-Shortest-Common-Superstring-September-24-2026,
 build/sections/02-counts.tex: extension rules eq. (extension-rules), period rule eq. (period-rule),
 blocking functional eq. (block-functional), W eq. (W), Lemma counts).

Specialised to inputs that are all the same length k (k-mer sets), but the recursion is the general one.
"""
import sys, time
from collections import defaultdict

SIGMA = "ACGT"


def build_levels(strings):
    k = max(len(s) for s in strings)
    levels = {k: set(s for s in strings if len(s) == k)}
    assert all(len(s) == k for s in strings), "k-mer sets only in this prototype"
    for l in range(k, 1, -1):
        nxt = set()
        for t in levels[l]:
            nxt.add(t[1:]); nxt.add(t[:-1])
        levels[l - 1] = nxt
    return k, levels


def periods(v):
    """all periods p < |v| of v (via KMP border chain)."""
    n = len(v)
    f = [0] * n
    j = 0
    for i in range(1, n):
        while j and v[i] != v[j]:
            j = f[j - 1]
        if v[i] == v[j]:
            j += 1
        f[i] = j
    out = []
    b = f[-1]
    while b:
        out.append(n - b)
        b = f[b - 1]
    return out


def blocking(s, P, m, Vlev, kmax):
    """B_A(s; m) for the periodic text A with period word P (A(i)=P[i mod p]); requires s = A[0:|s|)."""
    p = len(P)
    ls = len(s)
    A = lambda i: P[i % p]
    tot = 0
    a = 0
    left = ""  # A[-a:0)
    while True:
        core_l = left + s
        if len(core_l) > kmax - 2 or core_l not in Vlev[len(core_l)]:
            break
        xbad = A(-a - 1)
        interior = core_l
        b = 0
        while len(interior) <= kmax - 2 and interior in Vlev[len(interior)]:
            ybad = A(ls + b)
            for x in SIGMA:
                if x == xbad:
                    continue
                for y in SIGMA:
                    if y == ybad:
                        continue
                    tot += m.get(x + interior + y, 0)
            interior = interior + ybad
            b += 1
        left = A(-a - 1) + left
        a += 1
    return tot


def compute_W(strings, use_period=True, stats=None):
    k, V = build_levels(strings)
    m = {s: 1 for s in V[k]}
    pending = defaultdict(dict)  # level -> {(w,P): kmult}
    n_rules = n_trig = n_raised = 0

    def emit(l):
        nonlocal n_rules, n_trig
        for v in V[l]:
            for p in periods(v):
                P = v[:p]
                n_rules += 1
                if m[v] > blocking(v, P, m, V, k):
                    n_trig += 1
                    kk = 1
                    while kk * p < l:
                        w = v[: l - kk * p]
                        d = pending[len(w)]
                        if d.get((w, P), 0) < kk:
                            d[(w, P)] = kk
                        kk += 1

    if use_period and k >= 2:
        emit(k)
    for l in range(k - 1, 0, -1):
        left = defaultdict(int); right = defaultdict(int)
        for t in V[l + 1]:
            mt = m[t]
            left[t[1:]] += mt   # t = c s
            right[t[:-1]] += mt  # t = s c
        for s in V[l]:
            m[s] = max(left[s], right[s])
        if use_period:
            for (w, P), kk in pending[l].items():
                val = blocking(w, P, m, V, k) + kk + 1
                if val > m[w]:
                    m[w] = val
                    n_raised += 1
            pending.pop(l, None)
            if l >= 2:
                emit(l)
    W = sum(m.get(c, 0) for c in SIGMA)
    if stats is not None:
        stats.update(dict(V=sum(len(x) for x in V.values()), rules=n_rules, triggered=n_trig, raised=n_raised))
    return W


# ---------------- exact OPT (tiny instances) and greedy for validation ----------------
def ov(a, b):
    for o in range(min(len(a), len(b)) - 1, 0, -1):
        if a.endswith(b[:o]):
            return o
    return 0


def opt_scs(strs):
    strs = [s for s in set(strs) if not any(s != t and s in t for t in strs)]
    n = len(strs)
    O = [[ov(strs[i], strs[j]) if i != j else 0 for j in range(n)] for i in range(n)]
    INF = 10**9
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = len(strs[i])
    for S in range(1 << n):
        for i in range(n):
            if dp[S][i] >= INF or not (S >> i) & 1:
                continue
            for j in range(n):
                if (S >> j) & 1:
                    continue
                v = dp[S][i] + len(strs[j]) - O[i][j]
                if v < dp[S | 1 << j][j]:
                    dp[S | 1 << j][j] = v
    return min(dp[(1 << n) - 1])


def greedy_scs(strs):
    strs = [s for s in set(strs) if not any(s != t and s in t for t in strs)]
    while len(strs) > 1:
        best = (-1, 0, 1)
        for i in range(len(strs)):
            for j in range(len(strs)):
                if i != j:
                    o = ov(strs[i], strs[j])
                    if o > best[0]:
                        best = (o, i, j)
        o, i, j = best
        new = strs[i] + strs[j][o:]
        strs = [s for t, s in enumerate(strs) if t not in (i, j)] + [new]
        strs = [s for s in strs if not any(s != t and s in t for t in strs)]
    return len(strs[0])


if __name__ == "__main__":
    import random
    rnd = random.Random(1)
    # paper's example: a^h alone -> W = h
    for h in (2, 5, 9):
        print("a^%d: W=%d (W_ext=%d)" % (h, compute_W(["A" * h]), compute_W(["A" * h], use_period=False)))
    bad = 0; worst = 0
    for trial in range(400):
        k = rnd.choice([3, 4, 5, 6])
        alph = rnd.choice(["AC", "ACG", "ACGT"])
        n = rnd.randint(2, 8)
        base = "".join(rnd.choice(alph) for _ in range(rnd.randint(k + 2, 3 * k + 6)))
        kmers = list({base[i:i + k] for i in range(len(base) - k + 1)})
        kmers = rnd.sample(kmers, min(n, len(kmers)))
        W = compute_W(kmers); We = compute_W(kmers, use_period=False)
        O = opt_scs(kmers); G = greedy_scs(kmers)
        if W > O:
            bad += 1
            print("VIOLATION", kmers, W, O)
        worst = max(worst, G / W)
        assert We <= W
    print("validation: 400 random tiny k-mer sets, W<=OPT violations:", bad, " max greedy/W = %.3f" % worst)
