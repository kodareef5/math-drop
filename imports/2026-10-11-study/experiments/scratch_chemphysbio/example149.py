"""Hand-built WR mass-action network for a proposed CatalystNetworkAnalysis test:
   0 <-> A,  A + B <-> C,  2C <-> B + D,  D <-> 2A  (4 linkage classes? check)
Report: WR, linkage classes, deficiency, rank S, conservative, siphons, ADS07 verdict,
then simulate with random positive rates (sanity check only, not proof)."""
import numpy as np, itertools, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from siphons import minimal_siphons, has_psemiflow
from wr_struct_persist import conservative
from scan_wr import scc_ok, deficiency
from scipy.integrate import solve_ivp
cands = {
 'N1': [((), (('A',1),)), ((('A',1),('B',1)), (('C',1),)), ((('C',2),), (('B',1),('D',1))), ((('D',1),), (('A',2),))],
 'N2': [((), (('A',1),)), ((('A',1),('B',1)), (('C',1),)), ((('C',1),), (('D',1),)), ((('B',1),('D',1)), (('A',2),))],
}
for name, half in cands.items():
    E = []
    for a, b in half:
        E += [(a, b), (b, a)]
    dyn = sorted({s for e in E for c in e for s, _ in c})
    nodes = sorted({c for e in E for c in e})
    d, lc, rk = deficiency(E, nodes, dyn)
    cons = conservative(dyn, {e: 1 for e in E})
    sips = minimal_siphons(dyn, {e: 1 for e in E})
    crit = [s for s in sips if not has_psemiflow(dyn, {e: 1 for e in E}, s)]
    print(name, 'species', dyn, 'WR', scc_ok(E, nodes), 'LC', lc, 'rankS', rk, 'deficiency', d,
          'conservative', cons, 'siphons', [[dyn[i] for i in s] for s in sips], 'critical', len(crit),
          '-> ADS07', 'PERSISTENT' if cons and not crit else 'INCONCLUSIVE')
    # simulate
    di = {s: i for i, s in enumerate(dyn)}
    Y = lambda c: np.array([dict(c).get(s, 0) for s in dyn], float)
    rng = np.random.default_rng(3)
    mins, maxs = [], []
    for trial in range(20):
        k = np.exp(rng.uniform(-3, 3, len(E)))
        src = np.array([Y(a) for a, b in E]); net = np.array([Y(b) - Y(a) for a, b in E])
        f = lambda t, x: (k * np.prod(np.maximum(x, 0)[None, :] ** src, axis=1)) @ net
        x0 = np.exp(rng.uniform(-4, 4, len(dyn)))
        sol = solve_ivp(f, (0, 2000), x0, method='LSODA', rtol=1e-8, atol=1e-12)
        tail = sol.y[:, sol.t > 1000]
        mins.append(tail.min()); maxs.append(tail.max())
    print('   20 random rate sets/initial states, t in [1000,2000]: min conc', f'{min(mins):.3e}', 'max conc', f'{max(maxs):.3e}')
