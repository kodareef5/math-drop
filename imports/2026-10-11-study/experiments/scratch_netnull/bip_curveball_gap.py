"""Exact spectral gap of vegan's curveball (uniform pair of rows, uniform redistribution of row-unique columns)
on all binary matrices with given margins, vs the FQW26 bound 1/C(nr,2)."""
import itertools, math, json, numpy as np
from vegan_exact import int_tables, is_binary
out = []
for r, c in [((2, 2, 1), (2, 2, 1)), ((3, 2, 2, 1), (3, 2, 2, 1)), ((2, 2, 2, 1), (3, 2, 1, 1)), ((2, 2, 2, 2), (2, 2, 2, 2)),
             ((3, 3, 2, 2), (2, 2, 2, 2, 2)), ((3, 2, 2, 2, 1), (3, 3, 2, 1, 1)), ((2, 2, 2, 2, 2), (2, 2, 2, 2, 2))]:
    S = [X for X in int_tables(r, c) if is_binary(X)]
    idx = {X: i for i, X in enumerate(S)}; N = len(S); nr = len(r)
    P = np.zeros((N, N)); pairs = list(itertools.combinations(range(nr), 2))
    for (i, j) in pairs:
        fib = {}
        for X in S:
            key = tuple(X[k] for k in range(nr) if k not in (i, j)) + (tuple(X[i][q] + X[j][q] for q in range(len(c))),)
            fib.setdefault(key, []).append(idx[X])
        for mem in fib.values():
            for a in mem:
                for b in mem:
                    P[a, b] += 1 / len(mem) / len(pairs)
    ev = np.sort(np.linalg.eigvalsh(P))[::-1]
    row = dict(rows=r, cols=c, N=N, exact_gap=round(float(1 - ev[1]), 4), bound=round(1 / math.comb(nr, 2), 4), min_eig=round(float(ev[-1]), 4))
    print(json.dumps(row)); out.append(row)
json.dump(out, open("bip_curveball_gap.json", "w"), indent=1)
