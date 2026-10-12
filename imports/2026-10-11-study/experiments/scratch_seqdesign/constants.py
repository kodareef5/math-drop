"""Explicit constants implied by the 076 rounding lemma (rounding.tex) and the final bound
limsup m_N <= K_delta + 2 C sqrt(delta log(20/delta)) (reduction.tex)."""
import math
S=sum(2**(-h/2)*math.sqrt(1+h/4) for h in range(2000))
C0=8*S                      # Lemma rounding-matrix: 4 sqrt(sL) S with L<=4 log(2R/s)
pref=2*math.sqrt(2)/(1-math.pi*math.e/20)
C=pref*max(1.0, C0/(math.sqrt(2)-1))
print(f"S={S:.4f}  C0={C0:.2f}  C(rounding lemma)={C:.1f}")
def bound(d): return math.sqrt((1+d)**3/(1-d)) + 2*C*math.sqrt(d*math.log(20/d))
for target_F in [6.34, 9.0, 12.32]:
    m=math.sqrt(1+1/target_F)
    lo,hi=1e-300,0.04
    if bound(hi)<m: print('easy'); continue
    for _ in range(2000):
        mid=math.sqrt(lo*hi)
        if bound(mid)<m: lo=mid
        else: hi=mid
    print(f"F>={target_F}: need m_N<={m:.4f}; the paper's bound needs delta<={lo:.2e}")
# energy recursion bound: M_j >= M_{j-1} + (1-M_{j-1})^2/8  => 1-M_d <= ~8/d
for dl in [1e-2,1e-4,1e-8,1e-12]:
    print(f"delta={dl:g}: paper's recursion guarantee needs d ~ 8/delta = {8/dl:.0e} torus variables")
