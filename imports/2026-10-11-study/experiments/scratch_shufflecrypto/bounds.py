"""
Explicit provable round counts for full-domain (q = N) security of shuffle ciphers.

All "TV" numbers are total-variation distance of the FULL permutation law (ideal round
functions) from uniform on S_N.  TV of the whole permutation upper-bounds the CCA
advantage of any adversary making any number of adaptive forward/inverse queries
(including all N), so no nCPA->CCA round doubling is needed for these rows.

Sources of each formula are given inline (paper + equation/lemma labels).
Everything is done in log2 to avoid underflow at N = 2^64.
"""
import math, functools, json, sys

LOG2E = 1 / math.log(2)

def lg(x):
    return math.log2(x)

def lse2(vals):
    """log2(sum 2^v) for a list of log2 values."""
    vals = [v for v in vals if v != -math.inf]
    if not vals:
        return -math.inf
    m = max(vals)
    return m + lg(sum(2 ** (v - m) for v in vals))

# ---------------------------------------------------------------- partitions / degrees
def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest

def conj(mu):
    return [sum(1 for r in mu if r > j) for j in range(mu[0])] if mu else []

def log2_f(mu):
    """log2 of number of SYT of shape mu (hook length formula)."""
    if not mu:
        return 0.0
    c = conj(mu)
    k = sum(mu)
    s = math.lgamma(k + 1)
    for i, r in enumerate(mu):
        for j in range(r):
            s -= math.log((r - j - 1) + (c[j] - i - 1) + 1)
    return s * LOG2E

def log2_D_longrow(N, mu):
    """log2 dim of S_N irrep (N-k, mu), mu |- k, computed without cancellation.
    D = N! f^mu / ( k! * prod_{first-row boxes} hook ).
    First-row hooks: box j (1..N-k): (N-k-j) + mu'_j + 1.
    For j > mu_1 these multiply to (N-k-mu_1)!; so
    D = f^mu/k! * [N!/(N-k-mu_1)!] / prod_{j<=mu_1}(N-k-j+1+mu'_j)."""
    k = sum(mu)
    m1 = mu[0] if mu else 0
    c = conj(mu)
    s = log2_f(mu) - math.lgamma(k + 1) * LOG2E
    s += sum(lg(N - i) for i in range(k + m1))
    s -= sum(lg(N - k - j + 1 + c[j - 1]) for j in range(1, m1 + 1))
    return s

def _check_small():
    # check against direct hook formula for N = 12
    N = 12
    for lam in partitions(N):
        if lam[0] >= N - 4 and lam[0] >= len(lam):
            mu = lam[1:]
            a = log2_D_longrow(N, mu)
            b = log2_f(lam)
            assert abs(a - b) < 1e-9, (lam, a, b)
_check_small()

PART_CACHE = {}
def parts_of(k):
    if k not in PART_CACHE:
        PART_CACHE[k] = list(partitions(k))
    return PART_CACHE[k]

def npart(k):
    # exact partition numbers via Euler recurrence
    p = [1] + [0] * k
    for n in range(1, k + 1):
        s, j = 0, 1
        while True:
            g1 = j * (3 * j - 1) // 2
            g2 = j * (3 * j + 1) // 2
            if g1 > n:
                break
            sg = 1 if j % 2 else -1
            s += sg * p[n - g1]
            if g2 <= n:
                s += sg * p[n - g2]
            j += 1
        p[n] = s
    return p

PNUM = npart(400)

@functools.lru_cache(maxsize=None)
def log2_Z(s, d, Kexact=10):
    """log2 of Z_s(N) = sum over lambda |- N, lambda not in {(N),(1^N)} of D^{-s}, N = 2^d.
    Exact over defect k <= Kexact (shapes (N-k,mu) and transposes); for defect k > Kexact
    an upper bound 2 p(k) C(N-k,k)^{-s} (Lemma l:degree-basic of the Fourier companion),
    valid for k <= N/3; the k > N/3 range is bounded by e^{3 sqrt N} * (2^{N/10}/N)^{-s}
    and is negligible for N >= 2^20 (included as a crude term)."""
    N = 2 ** d
    terms = []
    for k in range(1, Kexact + 1):
        for mu in parts_of(k):
            terms.append(1 + (-s) * log2_D_longrow(N, mu))  # factor 2 for transpose
    # tail k in (Kexact, N/3]: 2 p(k) C(N-k,k)^{-s}; terms decrease monotonically here, so once a
    # term is 400 bits below the max we bound the rest of the range by (N/3) x that term.
    # Rigorous version: exact-count bound 2 p(k) C(N-k,k)^{-s} for Kexact < k <= 400 (all k <= N/3),
    # then for 400 < k <= N/3 use C(N-k,k) >= 2^k and p(k) <= e^{3 sqrt k}:
    #   sum_{k>400} 2 e^{3 sqrt k} 2^{-s k}, bounded by 2 * sum_{k>400} 2^{4.33 sqrt k - s k}, which for
    #   s >= 0.25 is a decreasing sequence after k=400 with ratio <= 2^{-s/2}; bound = first term/(1-2^{-s/2}).
    # For Kexact < k <= K: 2 p(k) C(N-k,k)^{-s} with the rigorous lower bound C(N-k,k) >= (N-2k)^k / k!
    # (and C >= 2^k), p(k) exact for k <= 400 else e^{3 sqrt k}.  K = (12/s)^2 makes the remaining terms
    # 2^{1 + 4.33 sqrt k - s k} decrease with ratio <= 2^{-0.82 s}; add that geometric tail.  Requires K <= N/3.
    assert s >= 0.05
    K = max(400, math.ceil((12 / s) ** 2))
    assert K <= N / 3
    for k in range(Kexact + 1, K + 1):
        lC = max(k, k * lg(N - 2 * k) - math.lgamma(k + 1) * LOG2E)
        lp = lg(PNUM[k]) if k <= 400 else 3 * math.sqrt(k) * LOG2E
        terms.append(1 + lp - s * lC)
    first = 1 + 3 * math.sqrt(K + 1) * LOG2E - s * (K + 1)
    terms.append(first - lg(1 - 2 ** (-0.82 * s)))
    # far range (longest row/column a < 2N/3): Fourier companion Lemma l:degree-basic gives
    # D >= 2^a/(a+1) >= 2^{N/10}/(N/10+1) (a >= N/10) or D >= (5/e)^N (a < N/10); count <= e^{3 sqrt N}.
    far = 3 * math.sqrt(N) * LOG2E - s * (N / 10 - lg(N / 10 + 1))
    terms.append(far)
    return lse2(terms)

# ---------------------------------------------------------------- C_u (sup over m<=45, numerical)
CU = {0.5: 5.9061, 0.75: 4.0618, 1.0: 3.2847, 1.5: 2.7385, 2.0: 2.4722, 3.0: 2.1991, 4.0: 2.0872, 6.0: 2.0184}

# ---------------------------------------------------------------- the generic lift
def lift_tv_log2(log2_delta, p, b, u, d):
    """Fourier companion Thm l:main (isotypic, Prop l:isotypic) + Lemma l:trim (exact trimming,
    cap B=1, mass z >= 1-delta) + Lemma l:plancherel + sign mean 0:
      (sum|f^{*p}-U|)^2 <= (1-z^p)^2 + (1-z)^{2p} + (b C_u)^p Z_{p*gamma-1}(N),  gamma = 1-(u+2)/b
      TV(mu^{*p},U) <= 1/2 [ p*delta + sqrt( (p delta)^2 + delta^{2p} + (b C_u)^p Z ) ]
    Returns log2 of the TV bound."""
    gamma = 1 - (u + 2) / b
    s = p * gamma - 1
    if s < 0.05:
        return math.inf
    lz = p * lg(b * CU[u]) + log2_Z(round(s, 9), d)
    lpd = lg(p) + log2_delta
    inner = lse2([2 * lpd, 2 * p * log2_delta, lz])
    return lg(0.5) + lse2([lpd, inner / 2])

def floor_log2(p, b, u, d):
    gamma = 1 - (u + 2) / b
    s = p * gamma - 1
    if s < 0.05:
        return math.inf
    return lg(0.5) + 0.5 * (p * lg(b * CU[u]) + log2_Z(round(s, 9), d))

# ---------------------------------------------------------------- per-block marginal bounds
def hmr_q_log2(N, q, r):
    """HMR CRYPTO'12 Thm 3: TV of q designated cards after r swap-or-not rounds
    <= 2 N^{3/2}/(r+2) * ((q+N)/(2N))^{r/2+1}."""
    return 1 + 1.5 * lg(N) - lg(r + 2) + (r / 2 + 1) * lg((q + N) / (2 * N))

def thorp_list_log2(d, b, T):
    """Thorp, any fixed list of k <= (1-1/b) N labels, after T physical shuffles (T multiple of d):
    Conditional-information paper Lemma noise:halves with alpha = 1/b:
      a_T <= gamma^{T-2d} + eta/delta_h, gamma = 1-alpha/4, delta_h = alpha/2, eta = 2 exp(-alpha^2 N/4)
      TV(list) <= 1/2 N^{3/2} sqrt(a_T)  (sequential comparison, Prop noise:uniform-marginals proof)."""
    N = 2 ** d
    a = 1 / b
    g = 1 - a / 4
    l1 = (T - 2 * d) * lg(g)
    l2 = lg(2) + (-(a * a * N / 4)) * LOG2E - lg(a / 2)
    laT = lse2([l1, l2])
    return lg(0.5) + 1.5 * d + laT / 2

# ---------------------------------------------------------------- optimizers
B_GRID = [4, 8, 16, 32, 64]
U_GRID = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0]
P_GRID = list(range(2, 61))

def min_rounds_lift(d, log2_eps, kind):
    """Minimise total rounds p*r over (b,u,p,r) s.t. lift TV bound <= eps.
    kind = 'thorp' (r must be multiple of d) or 'sn' (swap-or-not, any r)."""
    N = 2 ** d
    best = None
    for b in B_GRID:
        if b > N:
            continue
        for u in U_GRID:
            gamma = 1 - (u + 2) / b
            if gamma <= 0:
                continue
            for p in P_GRID:
                if p * gamma - 1 < 0.05:
                    continue
                fl = floor_log2(p, b, u, d)
                if fl > log2_eps - 1:
                    continue
                # binary search smallest r
                def ok(r):
                    if kind == 'thorp':
                        ld = lg(b) + thorp_list_log2(d, b, r)
                    else:
                        q = N - N // b
                        ld = lg(b) + hmr_q_log2(N, q, r)
                    if ld >= 0:
                        return False
                    return lift_tv_log2(ld, p, b, u, d) <= log2_eps
                lo, hi = 1, 1
                while not ok(hi * (d if kind == 'thorp' else 1)):
                    hi *= 2
                    if hi > 10 ** 7:
                        break
                if hi > 10 ** 7:
                    continue
                while lo < hi:
                    mid = (lo + hi) // 2
                    if ok(mid * (d if kind == 'thorp' else 1)):
                        hi = mid
                    else:
                        lo = mid + 1
                r = lo * (d if kind == 'thorp' else 1)
                tot = p * r
                if best is None or tot < best[0]:
                    best = (tot, dict(b=b, u=u, p=p, r_per_block=r))
    return best

# ---------------------------------------------------------------- literal paper / Lean bounds (Thorp, 1600d)
def thorp_paper_1600d_log2(d):
    """main.tex: eps_n = n^{3/2}/2 sqrt((31/32)^{198d} + 32 e^{-n/256}); delta_n <= 8 eps_n;
    1-M <= 2 delta_n;  TV <= 8(1-M) + 1/2 sqrt( A^16 Z_3(n) + ((1-M)/M)^16 ),  A = sqrt(32 C_1)."""
    n = 2 ** d
    le = lg(0.5) + 1.5 * d + 0.5 * lse2([198 * d * lg(31 / 32), lg(32) - n / 256 * LOG2E])
    l1M = lg(16) + le
    lA16 = 8 * lg(32 * CU[1.0])
    inner = lse2([lA16 + log2_Z(3.0, d), 16 * (l1M - lg(1 - 2 ** l1M))])
    return lse2([lg(8) + l1M, lg(0.5) + inner / 2])

def thorp_lean_1600d_log2(d):
    """Lean OAI/Probability/ThorpShuffle/EightBlocks.lean fullRate with n = 2^d:
    TV <= 8 disc + 1/2 sqrt(2 (2 disc)^16 + 96^8 * sum_{defect>0} D^{-2}),
    disc <= 16 * marginalRate(d-3), marginalRate(e) = sqrt(3136((1/32)^e + (2^e)^3 (9/10)^(2^e)))."""
    e = d - 3
    lmr = 0.5 * (lg(3136) + lse2([e * lg(1 / 32), 3 * e + (2 ** e) * lg(0.9)]))
    ldisc = lg(16) + lmr
    inner = lse2([1 + 16 * (1 + ldisc), 8 * lg(96) + log2_Z(2.0, d)])
    return lse2([lg(8) + ldisc, lg(0.5) + inner / 2])

# ---------------------------------------------------------------- prior art
def sr_rounds(N, log2_eps):
    """Morris-Rogaway SR (EUROCRYPT'14), strategy p_N = floor(N/2): stage size N_i halves;
    t_{N_i} = min r with Delta_SN(N_i, ceil(N_i/2), r) <= eps/n (n = number of stages with N_i > 2), t_2 = 1.
    Returns (expected rounds for a uniform input, worst-case rounds, first-stage rounds)."""
    sizes = []
    M = N
    while M >= 2:
        sizes.append(M)
        M = M // 2
    nst = sum(1 for M in sizes if M > 2)
    tgt = log2_eps - lg(nst)
    ts = []
    for M in sizes:
        if M == 2:
            ts.append(1)
            continue
        q = -(-M // 2)
        r = 1
        while hmr_q_log2(M, q, r) > tgt:
            r += 1
        ts.append(r)
    exp_r = sum(t * (M / N) for t, M in zip(ts, sizes))
    return exp_r, sum(ts), ts[0]

def mac_rounds(N, log2_eps):
    """Ristenpart-Yilek mix-and-cut (CRYPTO'13) Thm 5 (w=1): 7 N^{3/2}/(r+2) (3/4)^{r/2+1} <= eps;
    total rounds = lg N * r (fixed time)."""
    n = math.ceil(lg(N))
    r = 1
    while lg(7) + 1.5 * lg(N) - lg(r + 2) + (r / 2 + 1) * lg(0.75) > log2_eps:
        r += 1
    return n * r, r

def mrs_max_q(N):
    """MRS CRYPTO'09 Thm 5: Adv_cca(Th[N, r(4n-2)]) <= (2q/(r+1)) (4nq/N)^r: needs q < N/(4 lg N)."""
    return N / (4 * lg(N))

if __name__ == "__main__":
    out = {}
    DS = [20, 32, 64]
    EPS = [-32, -64, -128]
    print("=== literal 1600d bounds for Thorp (full-permutation TV) ===")
    for d in DS:
        a = thorp_paper_1600d_log2(d)
        b = thorp_lean_1600d_log2(d)
        print(f"N=2^{d}: paper (main.tex, op-norm, B=4, u=1): TV <= 2^{a:.1f}   Lean fullRate: TV <= 2^{b:.1f}   rounds=1600d={1600*d}")
        out[f"literal_{d}"] = dict(paper_log2=a, lean_log2=b, rounds=1600 * d)
    print()
    print("=== 512d (Random frames Cor shear:cor:512, p=2) floor ===")
    for d in DS:
        print(f"N=2^{d}: p=2,b=8,u=1 floor TV ~ 2^{floor_log2(2, 8, 1.0, d):.1f}")
    print()
    rows = []
    for d in DS:
        N = 2 ** d
        for le in EPS:
            th = min_rounds_lift(d, le, 'thorp')
            sn = min_rounds_lift(d, le, 'sn')
            sr = sr_rounds(N, le)
            mc = mac_rounds(N, le)
            row = dict(d=d, log2_eps=le, thorp_lift=th, sn_lift=sn, sr=sr, mac=mc, mrs_max_q_log2=lg(mrs_max_q(N)))
            rows.append(row)
            print(f"N=2^{d} eps=2^{le}: Thorp-lift {th}  SN-lift {sn}  SR(exp,worst,first)={tuple(round(x,1) for x in sr)}  MaC(total,per-stage)={mc}  MRS q<2^{lg(mrs_max_q(N)):.1f}")
            sys.stdout.flush()
    out["rows"] = rows
    json.dump(out, open("bounds_out.json", "w"), indent=1)
