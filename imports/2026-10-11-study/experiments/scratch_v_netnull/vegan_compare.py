"""Compare vegan_empirical_out.txt (R vegan 2.6.4) with exact laws from vegan_exact.py
for rs=(2,2,2), cs=(2,2,1,1)."""
import json, sys
import numpy as np
from scipy.stats import chisquare
here = __file__.rsplit('/', 1)[0]
sys.path.insert(0, here)
from vegan_exact import analyse
r = analyse((2, 2, 2), (2, 2, 1, 1), thins=(1, 100))
order = [''.join(map(str, o)) for o in r['_order']]
pred = {'swap': np.array(r['_swap_law']), 'quasiswap_thin1': np.array(r['_quasiswap_law_thin1'])}
res = {}
for line in open(f'{here}/vegan_empirical_out.txt'):
    if ':' not in line: continue
    nm, *kv = line.split()
    d = dict(x.split(':') for x in kv)
    c = np.array([int(d.get(k, 0)) for k in order], float)
    n = c.sum()
    u = chisquare(c, np.full(len(c), n / len(c)))
    row = dict(n=int(n), chi2_uniform=float(u.statistic), p_uniform=float(u.pvalue),
               emp_TV=float(0.5 * abs(c / n - 1 / len(c)).sum()))
    if nm in pred:
        p = chisquare(c, pred[nm] * n)
        row.update(chi2_pred=float(p.statistic), p_pred=float(p.pvalue),
                   exact_TV=float(0.5 * abs(pred[nm] - 1 / len(c)).sum()))
    res[nm] = row
    print(nm, json.dumps(row))
json.dump(res, open(f'{here}/vegan_compare_out.json', 'w'), indent=1)
