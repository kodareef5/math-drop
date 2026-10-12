"""Independent exact-enumeration check of degree-preserving swap chains.

For a labeled degree sequence, enumerate every simple graph with that sequence,
build the one-step transition kernel of the chain *as the library code implements
it*, and compare its stationary law (and finite-step law from a fixed start) to
uniform.

Chains modelled (each derived from reading the source, not from any write-up):

  nx_des   : networkx.double_edge_swap, one *successful* swap per step
             (proposal: oriented edges (u,v),(x,y) each w.p. 1/(2m); `continue`
              (uncounted) if u==x or v==y; accept if x not in N(u) and y not in N(v);
              new edges u-x, v-y; loop until success).
  nx_rr    : networkx.random_reference, one outer iteration: up to
             T=int(2m/(n-1)) counted attempts, break at first success.
             Counted attempts: oriented (a,b),(c,d), all four distinct.
             Accept if d not in N(a), b not in N(c) [and connected if connectivity].
             New edges a-d, c-b.
  bct      : bctpy/BCT randmio_und, one outer iteration: up to
             T=round(m/(n-1))+1 attempts (att = 0..maxAttempts), break at first success.
             Proposal: ordered distinct edge indices with 4 distinct vertices
             (uncounted retry), e2 orientation flipped w.p. 1/2. Accept if
             not(R[a,d] or R[c,b]); new edges a-d, c-b.
  count_all: lazy chain that counts every attempt (reference: should be uniform).
"""
import itertools, sys, json
from fractions import Fraction
import numpy as np


def realizations(deg):
    n = len(deg)
    out = []
    rem = list(deg)
    edges = []

    def rec(i):
        if i == n:
            if all(r == 0 for r in rem):
                out.append(frozenset(edges))
            return
        need = rem[i]
        cands = [j for j in range(i + 1, n) if rem[j] > 0]
        if need > len(cands):
            return
        for sub in itertools.combinations(cands, need):
            for j in sub:
                rem[j] -= 1
                edges.append((i, j))
            rem[i] = 0
            rec(i + 1)
            rem[i] = need
            for j in sub:
                rem[j] += 1
                edges.pop()
    rec(0)
    return out


def adj_of(E, n):
    N = [set() for _ in range(n)]
    for (a, b) in E:
        N[a].add(b); N[b].add(a)
    return N


def connected(E, n):
    N = adj_of(E, n)
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in N[v]:
            if w not in seen:
                seen.add(w); st.append(w)
    return len(seen) == n


def key(a, b):
    return (a, b) if a < b else (b, a)


def oriented(E):
    for (a, b) in E:
        yield (a, b); yield (b, a)


def swap(E, rem1, rem2, add1, add2):
    S = set(E)
    S.discard(key(*rem1)); S.discard(key(*rem2))
    S.add(key(*add1)); S.add(key(*add2))
    return frozenset(S)


def proposals_nx_des(E, n):
    """Yield (weight, newE or None) for each equally likely proposal that is *counted*
    as an attempt... for nx_des only success matters; we return all proposals that
    survive the `continue` filters (u!=x, v!=y), each with equal weight."""
    N = adj_of(E, n)
    for (u, v) in oriented(E):
        for (x, y) in oriented(E):
            if u == x or v == y:
                continue
            if (x not in N[u]) and (y not in N[v]):
                yield swap(E, (u, v), (x, y), (u, x), (v, y))
            else:
                yield None


def proposals_4distinct(E, n, conn):
    """random_reference / bct proposal: oriented pair (a,b),(c,d) all 4 distinct;
    new edges a-d, c-b. (bct: e1 stored orientation + random flip of e2 gives the
    same multiset of outcomes per unordered pair as uniform over oriented pairs.)"""
    N = adj_of(E, n)
    for (a, b) in oriented(E):
        for (c, d) in oriented(E):
            if len({a, b, c, d}) < 4:
                continue
            if (d not in N[a]) and (b not in N[c]):
                E2 = swap(E, (a, b), (c, d), (a, d), (c, b))
                if conn and not connected(E2, n):
                    yield None
                else:
                    yield E2
            else:
                yield None


def build(deg, chain, conn=False, T=None):
    n = len(deg); m = sum(deg) // 2
    states = realizations(deg)
    if conn:
        states = [E for E in states if connected(E, n)]
    idx = {E: i for i, E in enumerate(states)}
    N = len(states)
    P = np.zeros((N, N))
    A = np.zeros((N, N))  # counted-attempt kernel (lazy), for symmetry check
    s = np.zeros(N)
    for i, E in enumerate(states):
        if chain == 'nx_des':
            props = list(proposals_nx_des(E, n))
        else:
            props = list(proposals_4distinct(E, n, conn))
        Z = len(props)
        for E2 in props:
            if E2 is None:
                A[i, i] += 1.0 / Z
            else:
                A[i, idx[E2]] += 1.0 / Z
        s[i] = 1.0 - A[i, i]
        off = A[i].copy(); off[i] = 0.0
        if chain == 'nx_des':
            P[i] = off / s[i]
        elif chain in ('nx_rr', 'bct'):
            q = (1.0 - s[i]) ** T
            P[i] = off * (1.0 - q) / s[i]
            P[i, i] = q
        elif chain == 'count_all':
            P[i] = A[i]
    return states, A, P, s


def stationary(P):
    w, v = np.linalg.eig(P.T)
    k = np.argmin(abs(w - 1))
    pi = np.real(v[:, k]); pi = pi / pi.sum()
    return pi


def tv(p, q):
    return 0.5 * np.abs(p - q).sum()


def report(deg, chain, conn=False, T=None, steps=None, start=0):
    states, A, P, s = build(deg, chain, conn, T)
    N = len(states)
    u = np.full(N, 1.0 / N)
    pi = stationary(P)
    symA = np.abs(A - A.T).max()
    if chain == 'nx_des':
        pred = s / s.sum()
    elif chain in ('nx_rr', 'bct'):
        w = s / (1 - (1 - s) ** T); pred = w / w.sum()
    else:
        pred = u
    out = dict(deg=deg, chain=chain, conn=conn, T=T, N=N,
               attempt_kernel_max_asym=float(symA),
               TV_stationary_vs_uniform=float(tv(pi, u)),
               max_over_min=float(pi.max() / pi.min()),
               max_err_vs_closed_form=float(np.abs(pi - pred).max()))
    if steps is not None:
        p0 = np.zeros(N); p0[start] = 1.0
        pk = p0 @ np.linalg.matrix_power(P, steps)
        out['steps'] = steps
        out['TV_after_steps_vs_uniform'] = float(tv(pk, u))
        out['TV_after_steps_vs_stationary'] = float(tv(pk, pi))
    return out, states, P, pi


if __name__ == '__main__':
    res = []
    cases = [
        ([4, 4, 2, 2, 2, 2], 'nx_des', False, None, 80),
        ([4, 4, 2, 2, 2, 2], 'count_all', False, None, 400),
        ([4, 4, 2, 2, 2, 2], 'nx_rr', False, int(2 * 8 / 5), 8),
        ([4, 4, 2, 2, 2, 2], 'nx_rr', True, int(2 * 8 / 5), 8),
        ([4, 4, 2, 2, 2, 2], 'bct', False, int(np.round(8 / 5)) + 1, 80),
        ([2, 2, 2, 2, 2, 2], 'nx_des', False, None, 60),
        ([2, 2, 2, 2, 2, 2], 'nx_rr', True, int(2 * 6 / 5), 6),
        ([2, 2, 2, 2, 2, 2], 'bct', False, int(np.round(6 / 5)) + 1, 60),
        ([3, 3, 2, 2, 1, 1], 'nx_des', False, None, 60),
        ([3, 3, 2, 2, 1, 1], 'bct', False, int(np.round(6 / 5)) + 1, 60),
        ([3, 3, 3, 3, 2, 2, 2], 'nx_des', False, None, 90),
        ([3, 3, 3, 3, 2, 2, 2], 'nx_rr', True, int(2 * 9 / 6), 9),
        ([3, 3, 3, 3, 2, 2, 2], 'bct', False, int(np.round(9 / 6)) + 1, 90),
    ]
    for deg, ch, conn, T, steps in cases:
        out, *_ = report(deg, ch, conn, T, steps)
        print(json.dumps(out))
        res.append(out)
    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else 'exact_kernels_out.json', 'w'), indent=1)
