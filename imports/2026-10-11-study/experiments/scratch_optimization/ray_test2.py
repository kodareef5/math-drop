import numpy as np, json
import ray_test as R
from hyp_cone import IU, unpack
from bench_hyp import make_instance
rng = np.random.default_rng(9); errs=[]
for it in range(6):
    _, _, _, x0 = make_instance(rng, 0)
    x0[20:23] = 0.0 if it < 3 else x0[20:23]   # y=0 slice -> boundary at singular X
    d = np.zeros(23)
    w = rng.normal(size=4); w /= np.linalg.norm(w); D = -np.outer(w, w) * 3
    d[:10] = [D[i, j] for (i, j) in IU]; d[10:20] = [ (5.0 if i==j else 0.0) for (i,j) in IU]
    if it >= 3:  # y on the ray scaled so that range condition can hold: move y toward 0 too
        d[20:23] = -x0[20:23] / (np.linalg.eigvalsh(unpack(x0)[0]).min() / 3 + 1e-9) * 0
    st = R.s_true(x0, d); sl, status = R.s_lift(x0, d)
    Xb = unpack(x0 + st * d)[0]
    errs.append(abs(sl-st)/st)
    print(it, "s_true %.6g s_lift %.6g rel %.1e minEigX %.1e %s" % (st, sl, abs(sl-st)/st, np.linalg.eigvalsh(Xb).min(), status))
