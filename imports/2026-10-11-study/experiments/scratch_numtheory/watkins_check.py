"""
Re-derive Watkins' unconditional class-number table for h <= H using only
003 (Lean-formalized 7/8 zero-free half-plane) + Tatuzawa's explicit lemma:
for fundamental D<0 with |D| > e^11.2, h(D) > 0.655/(pi e) sqrt|D|/log|D|.
So every fundamental D with h(D) <= H has |D| <= B(H); enumerate them all.
Compare count and largest |D| per h with Watkins' table (Sage cm.py).
"""
import math, sys, time
from sage.all import pari, Integer
from sage.schemes.elliptic_curves.cm import largest_fundamental_disc_with_class_number as watkins

H = int(sys.argv[1])
C = 0.655 / (math.pi * math.e)


def B(h):
    lo, hi = math.e ** 2, 1e40
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if C * math.sqrt(mid) / math.log(mid) <= h:
            lo = mid
        else:
            hi = mid
    return max(lo, math.exp(11.2))


Bmax = int(B(H)) + 1
t0 = time.time()
cnt = {h: 0 for h in range(1, H + 1)}
mx = {h: 0 for h in range(1, H + 1)}
for n in range(3, Bmax + 1):
    D = -n
    if n % 4 not in (0, 3):
        continue
    if not Integer(D).is_fundamental_discriminant():
        continue
    h = int(pari(D).qfbclassno())
    if h <= H:
        cnt[h] += 1
        mx[h] = n
print('H=%d, search bound B(H)=%d, time %.0fs' % (H, Bmax, time.time() - t0))
ok = True
for h in range(1, H + 1):
    wD, wn = watkins(h)
    match = (wD == mx[h] and wn == cnt[h])
    ok &= match
    print('h=%3d  003-derived: count=%5d max|D|=%8d   Watkins: count=%5d max|D|=%8d  %s' % (
        h, cnt[h], mx[h], wn, wD, 'OK' if match else 'MISMATCH'))
print('ALL MATCH' if ok else 'SOME MISMATCH')
