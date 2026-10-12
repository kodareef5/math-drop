"""Sweep small margins (3x3, 3x4, 4x4 with all entries 0/1 feasible, >=2 binary tables)
for exact TV from uniform of vegan swap (stationary) and quasiswap (thin=1) output laws."""
import itertools, json, sys
here = __file__.rsplit('/', 1)[0]; sys.path.insert(0, here)
from vegan_exact import analyse, tables
best = {'swap': (0, None), 'quasiswap1': (0, None), 'quasiswap100': (0, None)}
cnt = 0
for nr, nc in [(3, 3), (3, 4), (4, 3), (4, 4)]:
    for rs in itertools.combinations_with_replacement(range(nc - 1, 0, -1), nr):
        for cs in itertools.combinations_with_replacement(range(nr - 1, 0, -1), nc):
            if sum(rs) != sum(cs): continue
            B = tables(rs, cs, True)
            if len(B) < 2: continue
            if len(tables(rs, cs, False)) > 400: continue
            r = analyse(rs, cs, thins=(1, 100)); cnt += 1
            for k, v in [('swap', r['swap']['TV']), ('quasiswap1', r['quasiswap']['thin=1']['TV']),
                         ('quasiswap100', r['quasiswap']['thin=100']['TV'])]:
                if v > best[k][0]: best[k] = (v, (rs, cs, len(B)))
print('margin pairs:', cnt); print(json.dumps(best))
json.dump(dict(n=cnt, best=best), open(f'{here}/vegan_sweep_out.json', 'w'))
