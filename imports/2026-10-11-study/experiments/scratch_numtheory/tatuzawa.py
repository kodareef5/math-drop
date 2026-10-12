"""
003 + Tatuzawa => explicit unconditional class-number lower bound.

Tatuzawa (as stated in Elsenhans-Kluners-Nicolae, arXiv:1803.02056, Lemma 2/3):
  if |D| > e^11.2 and L(s,chi_D) != 0 on [1 - 1/(4 log|D|), 1) then
      h(D) > 0.655/(pi e) * sqrt|D| / log|D|.
003 (Lean-formalized) gives L(s,chi) != 0 for Re s > 7/8 for every Dirichlet
character, and 1 - 1/(4 log|D|) > 7/8 once log|D| > 2.  So the bound holds for
every fundamental D < 0 with |D| > e^11.2 ~ 73130, with no exceptional D.

(a) sanity check of the inequality against PARI class numbers;
(b) B(h): largest |D| allowed for class number <= h;
(c) largest h whose complete list needs only |D| < 2^40 (Mosunov-Jacobson's
    unconditional tabulation range).
"""
import math, sys
from sage.all import pari, Integer

C = 0.655 / (math.pi * math.e)
LO = math.exp(11.2)
print('constant 0.655/(pi e) = %.5f ; e^11.2 = %.0f' % (C, LO))

# (a) empirical check
Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
worst = (9e9, None, None)
cnt = 0
for n in range(int(LO) + 1, Nmax + 1):
    D = -n
    if not Integer(D).is_fundamental_discriminant():
        continue
    h = int(pari(D).qfbclassno())
    ratio = h * math.log(n) / math.sqrt(n)
    cnt += 1
    if ratio < worst[0]:
        worst = (ratio, D, h)
print('(a) fundamental D in (-%d, -%d): %d discriminants; min h*log|D|/sqrt|D| = %.4f at D=%d (h=%d); bound %.4f holds: %s'
      % (Nmax, int(LO), cnt, worst[0], worst[1], worst[2], C, worst[0] > C))


def B(h):
    # largest x with C sqrt(x)/log(x) <= h  (monotone for x > e^2)
    lo, hi = math.e ** 2, 1e40
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if C * math.sqrt(mid) / math.log(mid) <= h:
            lo = mid
        else:
            hi = mid
    return max(lo, LO)


watkins_max = {1: 163, 10: 13843, 50: 389467, 100: 1856563}
print('(b) h, B(h) from 003+Tatuzawa, Watkins actual max |D| (unconditional, h<=100)')
for h in (1, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 100000):
    print('    h=%-7d B(h)=%.3e  log2=%.1f  Watkins max=%s' % (h, B(h), math.log2(B(h)), watkins_max.get(h, '-')))
lim = 2.0 ** 40
hmax = int(C * math.sqrt(lim) / math.log(lim))
print('(c) |D| < 2^40 covers every class number h <= %d' % hmax)
