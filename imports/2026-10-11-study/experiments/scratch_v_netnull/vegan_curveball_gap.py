"""Spectral gap of vegan curveball kernel (exact) vs the claimed bound 1/C(r,2)."""
import sys, json, itertools
here = __file__.rsplit('/', 1)[0]; sys.path.insert(0, here)
import numpy as np
from vegan_exact import tables, key, curveball_kernel
rows = []
for nr, nc in [(3, 3), (3, 4), (4, 3), (4, 4)]:
    for rs in itertools.combinations_with_replacement(range(nc - 1, 0, -1), nr):
        for cs in itertools.combinations_with_replacement(range(nr - 1, 0, -1), nc):
            if sum(rs) != sum(cs): continue
            B = tables(rs, cs, True)
            if len(B) < 2: continue
            idx = {key(M): i for i, M in enumerate(B)}
            P = curveball_kernel(B, idx)
            ev = np.sort(np.linalg.eigvalsh((P + P.T) / 2))[::-1]
            gap = 1 - ev[1]
            bound = 1 / (nr * (nr - 1) / 2)
            rows.append(dict(rs=rs, cs=cs, N=len(B), gap=float(gap), bound=bound, ok=bool(gap >= bound - 1e-12)))
print('pairs', len(rows), 'all gap>=1/C(r,2):', all(r['ok'] for r in rows),
      'min gap/bound:', min(r['gap'] / r['bound'] for r in rows))
json.dump(rows, open(f'{here}/vegan_curveball_gap_out.json', 'w'))
