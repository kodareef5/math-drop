"""Chi-square of Octave-run MATLAB BCT randmio_und.m outputs vs uniform and vs exact law."""
import sys, json
import numpy as np
from scipy.stats import chisquare
here = __file__.rsplit('/', 1)[0]; sys.path.insert(0, here)
from exact_kernels import realizations, report
deg = [4, 4, 2, 2, 2, 2]; n = 6; m = 8
states = realizations(deg); idx = {E: i for i, E in enumerate(states)}
c = np.zeros(len(states))
for line in open(f'{here}/bct_matlab_keys.txt'):
    E = frozenset((int(t[0]), int(t[1])) for t in line.strip().strip(',').split(','))
    c[idx[E]] += 1
T = int(np.round(m / (n - 1))) + 1
_, _, _, pi = report(deg, 'bct', False, T)
N = c.sum()
u = chisquare(c, np.full(len(c), N / len(c))); p = chisquare(c, pi * N)
res = dict(runs=int(N), counts=c.astype(int).tolist(), chi2_uniform=[float(u.statistic), float(u.pvalue)],
           chi2_pred=[float(p.statistic), float(p.pvalue)])
print(json.dumps(res)); json.dump(res, open(f'{here}/bct_matlab_compare_out.json', 'w'), indent=1)
