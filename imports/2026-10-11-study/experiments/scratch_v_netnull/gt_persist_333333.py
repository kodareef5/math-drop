"""graph-tool persist=True exact law on 3-regular n=6 (70 realizations), sweep vs no-sweep."""
import sys, json
here = __file__.rsplit('/', 1)[0]; sys.path.insert(0, here)
import numpy as np
from exact_kernels import realizations, stationary, tv
from gt_persist_exact import sweep_kernel, nosweep_kernel
deg = [3] * 6
S = realizations(deg); u = np.full(len(S), 1 / len(S))
out = {'deg': deg, 'N': len(S)}
pn = stationary(nosweep_kernel(S, True)); out['nosweep_persist'] = [float(tv(pn, u)), float(pn.max() / pn.min())]
ps = stationary(sweep_kernel(S, True)); out['sweep_persist'] = [float(tv(ps, u)), float(ps.max() / ps.min())]
print(json.dumps(out)); json.dump(out, open(f'{here}/gt_persist_333333_out.json', 'w'))
