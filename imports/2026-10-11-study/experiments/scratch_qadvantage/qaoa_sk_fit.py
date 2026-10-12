"""Fit the QOKit infinite-size SK QAOA energies v_p (best_SK_QAOA_parameters.json, pinned commit)
to P* - c p^{-a} and extrapolate the depth needed to reach the energy that classical
SA/greedy reaches at finite n."""
import json, math, sys
PSTAR = 0.763166
d = json.load(open(sys.argv[1]))
pts = sorted((int(k), v['energy']) for k, v in d.items())
for p, e in pts:
    pass
# least squares on log(P*-v) = log c - a log p, using p >= 10
xs = [math.log(p) for p, e in pts if p >= 10]
ys = [math.log(PSTAR - e) for p, e in pts if p >= 10]
m = len(xs); xb = sum(xs)/m; yb = sum(ys)/m
a = -sum((x-xb)*(y-yb) for x, y in zip(xs, ys))/sum((x-xb)**2 for x in xs)
c = math.exp(yb + a*xb)
print(f"fit (p>=10): P* - v_p ~ {c:.3f} * p^-{a:.3f}")
for p, e in pts:
    if p in (1, 2, 5, 11, 20, 40, 60, 80):
        print(f"  p={p:3d}  v_p={e:.4f}  ratio v_p/P*={e/PSTAR:.4f}")
for target in (0.70, 0.74, 0.75, 0.755, 0.76):
    p = (c/(PSTAR-target))**(1/a)
    print(f"  depth to reach {target:.3f} ({target/PSTAR:.3f} of P*): p ~ {p:,.0f}")
