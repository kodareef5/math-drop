"""(a) Check the CatalystNetworkAnalysis INCONCLUSIVE test network
    2A+B -> C -> A+2B -> D -> 2A+B  with the siphon/P-semiflow test.
(b) Random weakly reversible networks (molecularity <= 2, linkage classes =
    random directed cycles, optional zero complex = open system): fraction for
    which the Angeli-De Leenheer-Sontag (2007) siphon test is conclusive vs
    INCONCLUSIVE, and how many of the inconclusive ones were already covered by
    earlier theorems (single linkage class: Anderson 2011 / GMS 2014;
    dim S <= 2: Pantea 2012 + CNP 2013) versus only by the new family-149 theorem.
"""
import numpy as np, itertools, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from siphons import minimal_siphons, has_psemiflow
from wr_struct_persist import conservative

rng = np.random.default_rng(42)


def ads07(dyn, edges):
    cons = conservative(dyn, edges)
    sips = minimal_siphons(dyn, edges, cap=200)
    crit = [s for s in sips if not has_psemiflow(dyn, edges, s)]
    return cons, len(sips), len(crit)


def rank_S(dyn, edges):
    di = {s: i for i, s in enumerate(dyn)}
    rows = []
    for a, b in edges:
        v = np.zeros(len(dyn))
        for s, st in b: v[di[s]] += st
        for s, st in a: v[di[s]] -= st
        rows.append(v)
    return int(np.linalg.matrix_rank(np.array(rows)))


# (a)
A, B, C, D = 'A', 'B', 'C', 'D'
edges = {((('A', 2), ('B', 1))): None}
E = [((('A', 2), ('B', 1)), (('C', 1),)), ((('C', 1),), (('A', 1), ('B', 2))),
     ((('A', 1), ('B', 2)), (('D', 1),)), ((('D', 1),), (('A', 2), ('B', 1)))]
dyn = ['A', 'B', 'C', 'D']
cons, ns, nc = ads07(dyn, {e: 1 for e in E})
sips = minimal_siphons(dyn, {e: 1 for e in E})
print('(a) CatalystNetworkAnalysis test network: conservative', cons, 'minimal siphons',
      [[dyn[i] for i in s] for s in sips], 'critical', nc, 'rank S', rank_S(dyn, E),
      '-> deficiency', 4 - 1 - rank_S(dyn, E))


# (b)
def random_complex(d, allow_zero):
    choices = []
    if allow_zero:
        choices.append(())
    for i in range(d):
        choices.append(((i, 1),)); choices.append(((i, 2),))
    for i, j in itertools.combinations(range(d), 2):
        choices.append(((i, 1), (j, 1)))
    return choices[rng.integers(len(choices))]


def random_wr(d, n_lc, max_len, open_sys):
    edges = []
    used = set()
    for _ in range(n_lc):
        L = rng.integers(2, max_len + 1)
        cyc = []
        while len(cyc) < L:
            c = random_complex(d, open_sys)
            if c not in used and c not in cyc:
                cyc.append(c)
        used |= set(cyc)
        for k in range(L):
            edges.append((cyc[k], cyc[(k + 1) % L]))
            if rng.random() < 0.5:
                edges.append((cyc[(k + 1) % L], cyc[k]))
    sp = sorted({s for e in edges for c in e for s, _ in c})
    dyn = [f'X{s}' for s in sp]
    E = [(tuple((f'X{s}', m) for s, m in a), tuple((f'X{s}', m) for s, m in b)) for a, b in edges]
    return dyn, list(dict.fromkeys(E))


stats = {}
for open_sys in [False, True]:
    for d in [4, 6]:
        cnt = dict(total=0, ads_persistent=0, inconclusive=0, inc_single_lc=0, inc_dimS_le2=0, inc_only_new=0)
        for trial in range(150):
            n_lc = int(rng.integers(1, 4))
            dyn, E = random_wr(d, n_lc, 3, open_sys)
            if len(dyn) < 2:
                continue
            cons, ns, nc = ads07(dyn, {e: 1 for e in E})
            cnt['total'] += 1
            if cons and nc == 0:
                cnt['ads_persistent'] += 1
                continue
            cnt['inconclusive'] += 1
            # linkage classes
            import networkx as nx
            G = nx.Graph(); G.add_edges_from(E)
            lc = nx.number_connected_components(G)
            rS = rank_S(dyn, E)
            if lc == 1:
                cnt['inc_single_lc'] += 1
            elif rS <= 2 or len(dyn) <= 2:
                cnt['inc_dimS_le2'] += 1
            else:
                cnt['inc_only_new'] += 1
        stats[f'open={open_sys},d={d}'] = cnt
        print(f'open={open_sys} d={d}', cnt, flush=True)
json.dump(stats, open('random_wr.json', 'w'), indent=1)
