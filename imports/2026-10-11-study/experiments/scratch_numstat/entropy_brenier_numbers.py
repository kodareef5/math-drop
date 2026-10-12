import math, numpy as np
LN2 = math.log(2)
print("== Family 101: entropy gap to Gaussian with same covariance (per dimension)")
gap_new = 0.5*math.log(2*math.pi*math.e) - 1.0          # nats, from h >= m + 1/2 logdet Cov
print(f"new vector bound (OAI 101): {gap_new:.6f} nats = {gap_new/LN2:.6f} bits per dim (sharp, any log-concave vector)")
mnr = 0.5*math.log(2*math.pi/math.e)
print(f"Melbourne-Nayar-Roberto scalar (h>=1+1/2 log Var): {mnr:.6f} nats = {mnr/LN2:.6f} bits (identical; scalar only)")
mk_scalar = 0.5*math.log(math.pi*math.e/2)
print(f"Marsiglietti-Kostina scalar (h>=1/2 log(4 Var)): {mk_scalar:.6f} nats = {mk_scalar/LN2:.6f} bits")
print("Marsiglietti-Kostina Thm 4 vector (symmetric log-concave only): per-dim gap 1/2 log(2 pi e c(n))")
for n in [2, 3, 5, 10, 100, 1000, 10**6]:
    c_gen = math.e**2*n**2/(4*math.sqrt(2)*(n+2))
    g_gen = 0.5*math.log2(2*math.pi*math.e*c_gen)
    g_unc = 0.5*math.log2(2*math.pi*math.e*math.e**2/2)
    print(f"  n={n:>7}: general symmetric {g_gen:6.3f} bits/dim   unconditional {g_unc:6.3f} bits/dim   new {gap_new/LN2:.3f}")
# sanity: simplex isotropic constant vs 1/e (uniform measures => entropy bound gives L_K <= 1/e)
for n in [1,2,3,10,100,1000]:
    LK = math.exp((math.lgamma(n+1))/n)/((n+1)**((n+1)/(2*n))*math.sqrt(n+2))
    print(f"  simplex L_K(n={n}) = {LK:.6f}  (< 1/e = {1/math.e:.6f}: {LK < 1/math.e})")
# examples of h - (m + 1/2 logdet Cov) >= 0
ex = {
 'Gaussian':      0.5*math.log(2*math.pi*math.e) - 1,
 'Laplace':       (1+math.log(2)) - (1+0.5*math.log(2)),
 'uniform':       0.0 - (1+0.5*math.log(1/12)),
 'exponential':   1 - (1+0),
 'logistic':      2 - (1+0.5*math.log(math.pi**2/3)),
}
for k,v in ex.items(): print(f"  per-dim slack h-(1+1/2 log Var) for {k:12s}: {v:+.5f} nats")

print("\n== Family 374: explicit constant C* = sqrt(12 d R^2 (1+sqrt162)^2 + 28 L^2 P_K/|K|)")
def Cstar(d, R, L, PK, volK):
    return math.sqrt(12*d*R**2*(1+math.sqrt(162))**2 + 28*L**2*PK/volK)
for d in [2,3,5,10,50]:
    # unit cube source and unit cube target, both centered; convention R,L >= 1
    R = max(1.0, math.sqrt(d)/2); L = max(1.0, math.sqrt(d)/2)
    C = Cstar(d, R, L, PK=d, volK=1.0)
    diam = math.sqrt(d)
    w_thresh = (diam/C)**3
    print(f"  d={d:3d}: C*={C:8.1f}; trivial bound diam(Y)={diam:.3f}; C*W2^(1/3) < diam iff W2 < {w_thresh:.2e} (= {w_thresh/diam:.2e} x diam)")
print("  For L2-map error eps=0.1*diam need W2 <= (0.1*diam/C*)^3:")
for d in [2,3,10]:
    R = max(1.0, math.sqrt(d)/2); L=R; C = Cstar(d,R,L,d,1.0); diam=math.sqrt(d)
    print(f"    d={d}: W2 <= {(0.1*diam/C)**3:.2e}; with E W2(mu_n,mu) ~ n^(-1/max(d,2)) (ignoring logs/consts) => n ~ {((0.1*diam/C)**3)**(-max(d,2)):.1e}")
print("\n  exponent comparison for plug-in semi-discrete estimator T_{mu_n} (uniform convex source, compact target):")
for d in [2,3,5,10]:
    print(f"    d={d:2d}: DM23 W1^(1/6): n^-{1/(6*max(d,2)):.4f}  Merigot W1^(1/4): n^-{1/(4*max(d,2)):.4f}  OAI W2^(1/3): n^-{1/(3*max(d,2)):.4f}")

print("\n  sharpness family check (K=Y=[-1,1]^2): closed-form scaling")
for a in [1e-1,1e-2,1e-3,1e-4,1e-5]:
    b = a/2
    W2 = math.sqrt(a*b*b)       # central cell mass a (rho=1/4 on square), atom 0 -> b e2
    # symmetric difference of central cells: |x1| between a and a+b x2 => area = 2*int_{-1}^{1} |b x2| dx2 = 2*b ; normalized by 4
    sd = 2*b/4*2   # both sides x1>0 and x1<0 counted: 2 * (int |b x2| dx2 = b) / 4
    L2 = math.sqrt(sd*1.0)      # map jump |e1 - 0| ~ 1 on switched set (ignoring b e2 term)
    print(f"    a={a:.0e}: W2={W2:.3e}  ||T-T'||~{L2:.3e}  ratio/W2^(1/3)={L2/W2**(1/3):.3f}  ratio/W2^(1/2)={L2/W2**0.5:.1f}")
