"""Exact law of graph-tool random_rewire(model='configuration', simple graph,
self_loops=False, parallel_edges=False) as implemented in graph_rewiring.hh
(graph_rewire::operator() + RewireStrategyBase + RandomRewireStrategy):

  per sweep: a uniformly random permutation of edge *slots*; for each slot e
  holding edge f: draw target slot et uniform over all m slots, random
  orientation for e and et; reject if et==e, if a self-loop would form, or if a
  parallel edge would form; otherwise swap targets (a = 0 => accept prob 1).
  persist=False: one attempt per slot.  persist=True: repeat until success.

Because the permutation is uniform, the graph-level law after one sweep depends
only on the start graph. We track states (G, U) with U = set of current edges
whose slots are still unvisited in this sweep.

Also models edge_sweep=False (one uniformly random slot per iteration).
"""
import sys, json, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from exact_kernels import realizations, stationary, tv


def k(a, b):
    return (a, b) if a < b else (b, a)


def moves_for_edge(E, f):
    """All (prob, newE, g, f_new, g_new) for primary edge f with one attempt.
    Proposal space: 2 orientations of f x m slots x 2 orientations, uniform."""
    Es = sorted(E)
    m = len(Es)
    S = set(E)
    out = []
    for (s, t) in [f, f[::-1]]:
        for g in Es:
            for (ts, tt) in [g, g[::-1]]:
                if g == f:
                    out.append((None,)); continue
                if s == tt or ts == t:
                    out.append((None,)); continue
                if k(s, tt) in S or k(ts, t) in S:
                    out.append((None,)); continue
                fn, gn = k(s, tt), k(ts, t)
                E2 = frozenset((S - {f, g}) | {fn, gn})
                out.append((E2, g, fn, gn))
    return out, 4 * m


def sweep_kernel(states, persist):
    idx = {E: i for i, E in enumerate(states)}
    N = len(states)
    M = np.zeros((N, N))
    cache = {}
    for i0, E0 in enumerate(states):
        dist = {(E0, frozenset(E0)): 1.0}
        m = len(E0)
        for step in range(m):
            nd = {}
            for (E, U), p in dist.items():
                for f in U:
                    pf = p / len(U)
                    key_ = (E, f)
                    if key_ not in cache:
                        cache[key_] = moves_for_edge(E, f)
                    mv, Z = cache[key_]
                    succ = [x for x in mv if x[0] is not None]
                    nfail = len(mv) - len(succ)
                    if persist:
                        if not succ:
                            raise RuntimeError('unswitchable edge: persist never returns')
                        w = pf / len(succ)
                    else:
                        w = pf / Z
                        if nfail:
                            st = (E, U - {f})
                            nd[st] = nd.get(st, 0.0) + pf * nfail / Z
                    for (E2, g, fn, gn) in succ:
                        U2 = U - {f}
                        if g in U2:
                            U2 = (U2 - {g}) | {gn}
                        st = (E2, frozenset(U2))
                        nd[st] = nd.get(st, 0.0) + w
            dist = nd
        for (E, U), p in dist.items():
            assert not U
            M[i0, idx[E]] += p
    return M


def nosweep_kernel(states, persist):
    idx = {E: i for i, E in enumerate(states)}
    N = len(states)
    M = np.zeros((N, N))
    for i, E in enumerate(states):
        m = len(E)
        for f in E:
            mv, Z = moves_for_edge(E, f)
            succ = [x for x in mv if x[0] is not None]
            if persist:
                if not succ:
                    M[i, i] = np.nan
                    continue
                for x in succ:
                    M[i, idx[x[0]]] += 1.0 / m / len(succ)
            else:
                M[i, i] += (len(mv) - len(succ)) / Z / m
                for x in succ:
                    M[i, idx[x[0]]] += 1.0 / m / Z
    return M


if __name__ == '__main__':
    res = []
    for deg in ([4, 4, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [3, 3, 2, 2, 1, 1], [3, 3, 3, 3, 2, 2]):
        states = realizations(deg)
        N = len(states)
        u = np.full(N, 1.0 / N)
        row = dict(deg=deg, N=N)
        for persist in (False, True):
            try:
                Ms = sweep_kernel(states, persist)
                pis = stationary(Ms)
                row[f'sweep_persist={persist}'] = dict(TV=float(tv(pis, u)), ratio=float(pis.max() / pis.min()),
                                                       rowsum_err=float(abs(Ms.sum(1) - 1).max()),
                                                       colsum_err=float(abs(Ms.sum(0) - 1).max()))
            except RuntimeError as ex:
                row[f'sweep_persist={persist}'] = str(ex)
            Mn = nosweep_kernel(states, persist)
            if np.isnan(Mn).any():
                row[f'nosweep_persist={persist}'] = 'unswitchable edge present'
            else:
                pin = stationary(Mn)
                row[f'nosweep_persist={persist}'] = dict(TV=float(tv(pin, u)), ratio=float(pin.max() / pin.min()))
        if 'TV' in str(row['sweep_persist=True']):
            np.save(f'{__file__.rsplit("/",1)[0]}/gt_pi_sweep_persist_{"_".join(map(str,deg))}.npy',
                    stationary(sweep_kernel(states, True)))
        print(json.dumps(row))
        res.append(row)
    json.dump(res, open(__file__.rsplit('/', 1)[0] + '/gt_persist_exact_out.json', 'w'), indent=1)
