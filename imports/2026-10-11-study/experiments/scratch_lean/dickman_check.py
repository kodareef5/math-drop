"""Replicates the Lean challenge's Dickman construction (JointDickman.lean L7-L22):
stepApprox 0 = 1; stepApprox (n+1) u = 1 - int_1^{max 1 u} stepApprox n (t-1)/max(1,t) dt;
rho u = stepApprox ceil(u) u.  Compare with known rho(2)=1-ln2, rho(3)=0.04860838829..., rho(4)=0.00491092564..."""
import math
from functools import lru_cache
H = 2e-4
def make(n):
    if n == 0:
        return lambda u: 1.0
    prev = make(n - 1)
    # tabulate on grid for speed
    grid = {}
    def f(u):
        if u <= 1: return 1.0
        N = int((u - 1) / H)
        s = 0.0
        t = 1.0
        for k in range(N):  # midpoint rule
            m = t + H / 2
            s += prev(m - 1) / m * H
            t += H
        rem = u - t
        if rem > 0:
            m = t + rem / 2
            s += prev(m - 1) / m * rem
        return 1 - s
    return f
def rho(u):
    return make(max(0, math.ceil(u)))(u)
for u, ref in [(0.5, 1.0), (1.5, 1 - math.log(1.5)), (2.0, 1 - math.log(2)), (2.5, 0.1303100)]:
    print(u, round(rho(u), 6), 'ref', round(ref, 6))
