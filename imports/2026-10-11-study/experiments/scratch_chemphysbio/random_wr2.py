"""Same generator as random_wr.py; classify ADS07-inconclusive WR networks:
  single LC (Anderson 2011 / GMS 2014), dim S<=2 (Pantea 2012 / CNP 2013),
  multi-LC & deficiency 0 (complex balanced for all rates: bounded by Horn-Jackson
  Lyapunov fn; persistence = GAC, claimed by Craciun 1501.02860v3),
  multi-LC & deficiency>0 & dim S>=3 (only family 149 covers)."""
import numpy as np, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random_wr as RW
from scan_wr import deficiency
RW.rng = np.random.default_rng(2026)
out = {}
for open_sys in [False, True]:
    for d in [4, 6]:
        c = dict(total=0, ads_persistent=0, single_lc=0, dimS_le2=0, multi_def0=0, only_149=0)
        for t in range(150):
            dyn, E = RW.random_wr(d, int(RW.rng.integers(1, 4)), 3, open_sys)
            if len(dyn) < 2: continue
            c['total'] += 1
            cons, ns, nc = RW.ads07(dyn, {e: 1 for e in E})
            if cons and nc == 0: c['ads_persistent'] += 1; continue
            nodes = sorted({x for e in E for x in e})
            dfc, lc, rk = deficiency(E, nodes, dyn)
            if lc == 1: c['single_lc'] += 1
            elif rk <= 2: c['dimS_le2'] += 1
            elif dfc == 0: c['multi_def0'] += 1
            else: c['only_149'] += 1
        out[f'open={open_sys},d={d}'] = c; print(f'open={open_sys} d={d}', c, flush=True)
json.dump(out, open('random_wr2.json', 'w'), indent=1)
