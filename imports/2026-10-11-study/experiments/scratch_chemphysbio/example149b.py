"""Search small WR networks (<=4 species, molecularity<=2) for a minimal test case
that (i) has >=2 linkage classes, (ii) deficiency >= 1, (iii) dim S >= 3,
(iv) ADS07 siphon test INCONCLUSIVE -> covered only by the family-149 theorem.
Then simulate it at random rates (sanity check)."""
import numpy as np, sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random_wr as RW
from scan_wr import scc_ok, deficiency
from scipy.integrate import solve_ivp
import networkx as nx
rng = np.random.default_rng(11); RW.rng = rng
best = None
for t in range(4000):
    dyn, E = RW.random_wr(3, 2, 3, True)
    if len(dyn) < 3: continue
    nodes = sorted({c for e in E for c in e})
    d, lc, rk = deficiency(E, nodes, dyn)
    if lc < 2 or d < 1 or rk < 3: continue
    cons, ns, nc = RW.ads07(dyn, {e: 1 for e in E})
    if cons and nc == 0: continue
    if best is None or len(E) < len(best[1]):
        best = (dyn, E, d, lc, rk, cons, nc)
dyn, E, d, lc, rk, cons, nc = best
fmt = lambda c: ' + '.join((f'{m}{s}' if m > 1 else s) for s, m in c) or '0'
print('species', dyn, 'LC', lc, 'deficiency', d, 'rankS', rk, 'conservative', cons, 'critical siphons', nc)
for a, b in E: print('  ', fmt(a), '->', fmt(b))
Y = lambda c: np.array([dict(c).get(s, 0) for s in dyn], float)
src = np.array([Y(a) for a, b in E]); net = np.array([Y(b) - Y(a) for a, b in E])
mins, maxs = [], []
for trial in range(30):
    k = np.exp(rng.uniform(-3, 3, len(E)))
    f = lambda t, x: (k * np.prod(np.maximum(x, 0)[None, :] ** src, axis=1)) @ net
    x0 = np.exp(rng.uniform(-4, 4, len(dyn)))
    sol = solve_ivp(f, (0, 3000), x0, method='LSODA', rtol=1e-9, atol=1e-14)
    tail = sol.y[:, sol.t > 1500]
    mins.append(tail.min()); maxs.append(tail.max())
print('30 random rate sets/initial states, t in [1500,3000]: min conc %.3e  max conc %.3e' % (min(mins), max(maxs)))
