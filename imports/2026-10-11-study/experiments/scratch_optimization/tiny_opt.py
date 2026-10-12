"""Tiny k-mer sets with tandem repeats: exact OPT (Held-Karp) vs greedy vs cycle-cover LB vs W (family 128)."""
import random, sys, os
import numpy as np
from scipy.optimize import linear_sum_assignment
sys.path.insert(0, os.path.dirname(__file__))
from scs_W import compute_W, opt_scs, greedy_scs, ov


def cycle_cover_lb(strs):
    strs = [s for s in set(strs) if not any(s != t and s in t for t in strs)]
    n = len(strs)
    C = np.array([[len(strs[j]) - ov(strs[i], strs[j]) if i != j else len(strs[i]) - self_ov(strs[i])
                   for j in range(n)] for i in range(n)])
    r, c = linear_sum_assignment(C)
    return int(C[r, c].sum())


def self_ov(s):
    for o in range(len(s) - 1, 0, -1):
        if s.endswith(s[:o]):
            return o
    return 0


rnd = random.Random(11)
stats = {"n": 0, "W>cc": 0, "W<cc": 0, "W=OPT": 0, "cc=OPT": 0, "best=OPT": 0, "greedy=OPT": 0}
ratios = []
for trial in range(3000):
    k = rnd.choice([5, 6, 7, 8])
    p = rnd.randint(1, 4)
    unit = "".join(rnd.choice("ACGT") for _ in range(p))
    s = "".join(rnd.choice("ACGT") for _ in range(rnd.randint(2, 6))) + unit * rnd.randint(2, 6) + \
        "".join(rnd.choice("ACGT") for _ in range(rnd.randint(2, 6)))
    if rnd.random() < 0.5:
        unit2 = "".join(rnd.choice("ACGT") for _ in range(rnd.randint(1, 3)))
        s += unit2 * rnd.randint(2, 6) + "".join(rnd.choice("ACGT") for _ in range(rnd.randint(1, 4)))
    km = sorted({s[i:i + k] for i in range(len(s) - k + 1)})
    if rnd.random() < 0.5 and len(km) > 3:
        km = rnd.sample(km, max(2, int(len(km) * rnd.uniform(0.3, 0.8))))
    if len(km) > 14 or len(km) < 2:
        continue
    O = opt_scs(km); G = greedy_scs(km); W = compute_W(km); CC = cycle_cover_lb(km)
    assert W <= O and CC <= O, (km, W, CC, O)
    stats["n"] += 1
    stats["W>cc"] += W > CC; stats["W<cc"] += W < CC
    stats["W=OPT"] += W == O; stats["cc=OPT"] += CC == O; stats["best=OPT"] += max(W, CC) == O
    stats["greedy=OPT"] += G == O
    ratios.append((G / O, O / max(W, CC), O / CC, O / W))
R = np.array(ratios)
print(stats)
print("max greedy/OPT %.3f  mean %.4f" % (R[:, 0].max(), R[:, 0].mean()))
print("max OPT/max(W,cc) %.3f mean %.4f | max OPT/cc %.3f | max OPT/W %.3f" % (R[:, 1].max(), R[:, 1].mean(), R[:, 2].max(), R[:, 3].max()))
