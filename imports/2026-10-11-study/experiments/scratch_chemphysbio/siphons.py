"""Enumerate minimal siphons (ILP with no-good cuts, HiGHS via scipy.milp) and
check the Angeli-De Leenheer-Sontag (2007) structural persistence criterion:
a conservative network is persistent if every (minimal) siphon contains the
support of a semipositive conservation law (P-semiflow). Networks with a
'critical' siphon are not covered by that classical certificate.
Usage: python3 -I siphons.py <final_dir> ID [ID ...]
"""
import sys, os, glob
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cb_check import extract


def minimal_siphons(dyn, edges, cap=500):
    n = len(dyn)
    di = {s: i for i, s in enumerate(dyn)}
    A, lb, ub = [], [], []
    for (a, b) in edges:
        reac = [di[s] for s, _ in a]
        for s, _ in b:
            row = np.zeros(n); row[di[s]] = 1
            for j in reac:
                row[j] -= 1
            A.append(row); lb.append(-np.inf); ub.append(0)  # s_i <= sum reactants
    # nonempty
    A.append(np.ones(n)); lb.append(1); ub.append(np.inf)
    found = []
    while len(found) < cap:
        cons = LinearConstraint(np.array(A), lb, ub)
        res = milp(c=np.ones(n), constraints=cons, integrality=np.ones(n), bounds=Bounds(0, 1))
        if res.status != 0:
            break
        s = np.round(res.x).astype(int)
        sup = np.flatnonzero(s)
        found.append(sup)
        # exclude supersets of this siphon: sum_{i in sup} x_i <= |sup|-1
        row = np.zeros(n); row[sup] = 1
        A.append(row); lb.append(-np.inf); ub.append(len(sup) - 1)
    return found


def has_psemiflow(dyn, edges, sup):
    n = len(dyn); di = {s: i for i, s in enumerate(dyn)}
    rows = []
    for (a, b) in edges:
        v = np.zeros(n)
        for s, st in b: v[di[s]] += st
        for s, st in a: v[di[s]] -= st
        rows.append(v)
    S = np.array(rows)
    bounds = [(0, None) if i in set(sup) else (0, 0) for i in range(n)]
    A_eq = np.vstack([S, np.ones((1, n))]); b_eq = np.concatenate([np.zeros(S.shape[0]), [1]])
    res = linprog(np.zeros(n), A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    return res.status == 0


if __name__ == '__main__':
    final = sys.argv[1]
    for i in sys.argv[2:]:
        f = glob.glob(os.path.join(final, i, i + '*.xml'))[0]
        dyn, edges, _, _ = extract(f)
        sips = minimal_siphons(dyn, edges)
        crit = [s for s in sips if not has_psemiflow(dyn, edges, s)]
        print(i, 'minimal siphons', len(sips), 'critical (no P-semiflow inside)', len(crit),
              '-> ADS07 certifies persistence' if not crit else '-> NOT covered by ADS07 siphon criterion',
              [[dyn[j] for j in s] for s in crit][:3])
