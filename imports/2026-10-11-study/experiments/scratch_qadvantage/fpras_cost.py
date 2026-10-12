"""Evaluate the explicit (galactic) parameters of the general-graph perfect-matching FPRAS
(family 113, main.tex eqs. schedule, ladder-parameters, energy-constants, ladder-lambda,
ladder-steps, statistical-parameters) and compare with exact hafnian counting
O(n^3 2^{n/2}) (Bjorklund 2012 / The Walrus).  All quantities in log10 to avoid overflow.
Lower bound on work: (#stages K+1) * (#samples S per stage) * (#chain steps s(xi)) chain steps.
Each chain step touches a product state of q(T+1) slots; we do NOT charge for that (lower bound)."""
import math, sys
L10 = math.log10
def log10_add(a, b):  # log10(10^a + 10^b)
    m = max(a, b); return m + L10(10**(a-m) + 10**(b-m))

def fpras_log10_steps(n, eps=0.1, delta=0.01):
    b = 1 + 1/n
    # K = min k>=1 : n^{n/2} b^{-k} <= eps/32
    K = max(1, math.ceil(((n/2)*math.log(n) - math.log(eps/32)) / math.log(b)))
    p = 2*K + 2
    N = n + 4*p*math.comb(n, 2)
    D0 = 1e8 * (n+1)**4
    lD = L10(100) + 2*L10(N) + L10(D0)                 # D = 100 N^2 D0
    lL = 100*(4 + L10(N) + lD)                         # L = (10^4 N D)^100
    lq = L10(32) + lL                                  # q = 32 L
    c = 1 + N**-2
    # T = min t: c^t >= max(D, 3*4^K)
    lmax = max(lD, L10(3) + K*L10(4))
    lT = L10(lmax*math.log(10)/math.log1p(float(N)**-2))  # T ~ ln(max)/ln(1+N^-2)
    lM = log10_add(lT + 2*lq, lq)                      # M = T q^2 + q
    # Lambda = 10 N q (T+1)(K + log2(ND+2) + 1)
    lLam = 1 + L10(N) + lq + lT + L10(K + (L10(N)+lD)/L10(2) + 1)
    # sigma = min(alpha/(100D), eps/(1000K)), alpha=1e-5 ; S = 10 sigma^-2 (n+K+1); xi = 1/(1000 K S)
    lsig = min(-5 - 2 - lD, L10(eps) - 3 - L10(K))
    lS = 1 - 2*lsig + L10(n+K+1)
    lxi_inv = 3 + L10(K) + lS
    # s(xi) = 20 L M (Lambda + log2(1/xi) + 1)
    ls = L10(20) + lL + lM + log10_add(lLam, L10(lxi_inv/L10(2) + 1))
    lamp = L10(math.ceil(math.log2(1/delta)))           # confidence amplification
    total = L10(K+1) + lS + ls + lamp
    return dict(n=n, K=K, N=N, log10_D=lD, log10_L=lL, log10_steps=total)

def exact_log10_ops(n):  # Bjorklund-type hafnian: ~ n^3 2^{n/2}
    return 3*L10(n) + (n/2)*L10(2)

print(f"{'n':>8} {'K':>10} {'N(enlarged)':>14} {'log10 L':>10} {'log10 FPRAS steps':>18} {'log10 exact ops':>16}")
for n in [10, 20, 40, 80, 144, 200, 400, 1000, 10**4, 10**5, 10**6]:
    r = fpras_log10_steps(n)
    print(f"{n:>8} {r['K']:>10} {r['N']:>14.3e} {r['log10_L']:>10.0f} {r['log10_steps']:>18.0f} {exact_log10_ops(n):>16.1f}")

# crossover: smallest even n where FPRAS lower-bound work < exact work
lo, hi = 10, 10**8
while hi - lo > 2:
    mid = (lo + hi)//2
    if fpras_log10_steps(mid)['log10_steps'] < exact_log10_ops(mid): hi = mid
    else: lo = mid
print(f"\nCrossover (FPRAS lower bound < exact n^3 2^(n/2)): n ~ {hi:,} vertices; "
      f"work there ~ 10^{exact_log10_ops(hi):.0f}")
