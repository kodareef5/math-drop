"""Minimum (input-independent) number of Label calls executed by the deterministic
quasipolynomial MPG algorithm (OpenAI 'Deterministic quasipolynomial-time mean-payoff games',
Sec. 4 Procedure Label, Sec. 6). Structure (04-algorithm.tex L21-85, 03-translations L13-16):
  base: all a_i b_i > 1 (mass) or D < 4096 (width)
  else: down pass >=1 call at width D/128, masses (a, 4/3 b)
        up pass   >=1 call at width D/128, masses (4/3 a, b)
        provisional: width D/2, same masses
        continuation: width D, every product times (4/5)(8/5) = 32/25
All products start at 1/n^2 (a_i=b_i=1/n) and are multiplied uniformly, so the mass base case
fires exactly when (4/3)^x (32/25)^y > n^2 along the path: input independent.
Minimum = each pass stops after its first (stationary) call. Maximum per pass = 1024n+1 calls.
"""
import math, sys
from functools import lru_cache
from fractions import Fraction

def count(n, W, per_pass=1):
    Wt = (n + 1) * W + 1          # transformed weight bound, 02-boxes.tex eq:bias
    D0 = 1
    while D0 < 64 * (n + 1) * (Wt + 1): D0 *= 2
    d0 = D0.bit_length() - 1
    target = Fraction(n * n)
    @lru_cache(maxsize=None)
    def f(d, x, y):   # width 2^d, x pass-multiplications (4/3), y continuation mults (32/25)
        prod = Fraction(4, 3) ** x * Fraction(32, 25) ** y
        if prod > target: return 1, 1            # (calls, base calls)
        if d < 12: return 1, 1                    # D < 4096
        c1, b1 = f(d - 7, x + 1, y)               # one narrow child per pass, width D/128
        c2, b2 = f(d - 1, x, y)                   # provisional, width D/2
        c3, b3 = f(d, x, y + 1)                   # continuation, same width
        return 1 + 2 * per_pass * c1 + c2 + c3, 2 * per_pass * b1 + b2 + b3
    return d0, f(d0, 0, 0)

B0 = lambda n: 1 + math.floor(math.log(n * n) / math.log(32 / 25))
print(f"{'n':>6} {'W':>12} {'log2 D0':>8} {'B0':>4} {'min calls':>12} {'min base calls':>14}  paper bound (H+1)(B0+1)(1+Hs)^B0")
for n in [2, 5, 10, 20, 50, 100, 1000]:
    for W in [1, 100, 10**6, 2**30, 2**62]:
        d0, (c, b) = count(n, W)
        H = d0 + B0(n); s = 2048 * n + 3
        bound_log10 = math.log10(H + 1) + math.log10(B0(n) + 1) + B0(n) * math.log10(1 + H * s)
        print(f"{n:>6} {W:>12} {d0:>8} {B0(n):>4} {c:>12.3e} {b:>14.3e}  10^{bound_log10:.0f}")
