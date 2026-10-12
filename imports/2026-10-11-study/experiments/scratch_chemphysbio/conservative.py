"""Check whether WR mass-action BioModels networks are conservative
(exists w>0 with w.(y'-y)=0 for all reactions) -> all classes bounded."""
import sys, json, glob, os
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cb_check import extract
final = sys.argv[1]
ids = sys.argv[2:]
for i in ids:
    f = glob.glob(os.path.join(final, i, i + '*.xml'))[0]
    dyn, edges, _, _ = extract(f)
    di = {s: k for k, s in enumerate(dyn)}
    rows = []
    for (a, b) in edges:
        v = np.zeros(len(dyn))
        for s, st in b: v[di[s]] += st
        for s, st in a: v[di[s]] -= st
        rows.append(v)
    S = np.array(rows)
    # maximize min w_i subject to S w = 0, w<=1 : variables (w, t), max t
    n = len(dyn)
    c = np.zeros(n + 1); c[-1] = -1
    A_eq = np.hstack([S, np.zeros((S.shape[0], 1))])
    A_ub = np.hstack([-np.eye(n), np.ones((n, 1))])  # t - w_i <= 0
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(n), A_eq=A_eq, b_eq=np.zeros(S.shape[0]),
                  bounds=[(0, 1)] * n + [(0, 1)], method='highs')
    print(i, 'species', n, 'conservative' if res.status == 0 and -res.fun > 1e-9 else 'NOT conservative (some class unbounded or open system)', round(-res.fun, 6))
