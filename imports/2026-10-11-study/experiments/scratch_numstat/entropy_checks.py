import math, numpy as np
from scipy import integrate, special
LN2 = math.log(2)
print("== 101 sanity: uniform on standard simplex in R^n, slack h - (n + 1/2 logdet Cov) (total nats)")
for n in [1,2,3,5,10,100,1000]:
    h = -math.lgamma(n+1)
    logdet = -(n+1)*math.log(n+1) - n*math.log(n+2)
    slack = h - (n + 0.5*logdet)
    print(f"  n={n:5d}: slack={slack:.5f} nats total, {slack/n:.5f} per dim (>=0 required; -> 3/2 - log(2pi)/2 = {1.5-0.5*math.log(2*math.pi):.4f})")

print("\n== 101 tightness: additive exponential noise (var 1), Gaussian input power P: I(X;X+Z) - 1/2 log2(1+P)  vs bound 0.6044 bits")
def h_sum(P):
    s = math.sqrt(P)
    # density of X+Z, X~N(0,P), Z~Exp(1)-1 (centered): exponentially modified Gaussian
    def f(y):
        t = y + 1.0
        return 0.5*math.exp(0.5*P - t)*special.erfc((P - t)/(math.sqrt(2)*s)) if True else 0
    def logf(y):
        t = y + 1.0
        return 0.5*P - t + special.log_ndtr((t - P)/s)
    lo, hi = -12*s - 5, 12*s + 40
    mass, _ = integrate.quad(lambda y: math.exp(logf(y)), lo, hi, limit=400, points=[0.0])
    val, _ = integrate.quad(lambda y: -math.exp(logf(y))*logf(y), lo, hi, limit=400, points=[0.0])
    assert abs(mass-1)<1e-6, mass
    return val
for P in [1, 10, 100, 1e3, 1e4]:
    I = (h_sum(P) - 1.0)/LN2          # h(Z)=1 nat for Exp(1)
    CG = 0.5*math.log2(1+P)
    print(f"  P={P:8g}: I_gauss-input={I:.4f} bits, C_Gauss={CG:.4f}, gap={I-CG:.4f} bits (upper bound 0.6044)")
