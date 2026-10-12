import numpy as np
def cubic_rate(delta,kappa,d): return delta**3/(16384*(1+kappa)*(1+np.log(d)))
games={'CHSH (4 uniform qs, d=4)':(96,4),'Magic square (9 uniform qs, d=16)':(8*8/(1/9),16)}
for name,(kap,d) in games.items():
    for delta in [0.01,0.05,0.1,0.2]:
        r=cubic_rate(delta,kap,d)
        k=np.log(1e10)/r
        print(f"{name}: kappa_mu={kap:.0f} delta={delta}: rate={r:.3e}/round, k for 1e-10 = {k:.2e} rounds")
# Hoeffding-type benchmark for an i.i.d. adversary (what one would get without coherent attacks)
for delta in [0.01,0.05,0.1]:
    print(f"iid Hoeffding benchmark delta={delta}: k={np.log(1e10)/(2*delta**2):.2e}")
