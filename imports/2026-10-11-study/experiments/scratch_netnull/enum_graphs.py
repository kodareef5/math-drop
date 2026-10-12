"""Enumerate simple labeled graphs with a given degree vector and their switch neighbours.

Graphs are bitmasks over the C(n,2) vertex pairs (i<j) in lexicographic order.
"""
from itertools import combinations
from functools import lru_cache


def pair_index(n):
    idx = {}
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            idx[(i, j)] = k
            idx[(j, i)] = k
            k += 1
    return idx


def enumerate_graphs(d):
    n = len(d)
    pidx = pair_index(n)
    out = []

    def rec(i, res, mask):
        if i == n:
            if all(r == 0 for r in res):
                out.append(mask)
            return
        need = res[i]
        cands = [j for j in range(i + 1, n) if res[j] > 0]
        if need > len(cands):
            return
        for S in combinations(cands, need):
            r2 = list(res)
            r2[i] = 0
            m2 = mask
            for j in S:
                r2[j] -= 1
                m2 |= 1 << pidx[(i, j)]
            # quick feasibility: total residual even and max residual <= remaining vertices
            rem = r2[i + 1:]
            if sum(rem) % 2:
                continue
            if rem and max(rem) > len(rem) - 1:
                continue
            rec(i + 1, tuple(r2), m2)

    rec(0, tuple(d), 0)
    return out


def edges_of(mask, n):
    E = []
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if mask >> k & 1:
                E.append((i, j))
            k += 1
    return E


def switch_neighbours(mask, n, pidx):
    """Return list of neighbour masks (one per valid switch; each neighbour appears once)."""
    E = edges_of(mask, n)
    nb = []
    for (a, b), (c, d) in combinations(E, 2):
        if len({a, b, c, d}) < 4:
            continue
        rem = (1 << pidx[(a, b)]) | (1 << pidx[(c, d)])
        for (x1, y1), (x2, y2) in (((a, c), (b, d)), ((a, d), (b, c))):
            p1, p2 = pidx[(x1, y1)], pidx[(x2, y2)]
            if not (mask >> p1 & 1) and not (mask >> p2 & 1):
                nb.append((mask & ~rem) | (1 << p1) | (1 << p2))
    return nb


def is_connected(mask, n):
    adj = [[] for _ in range(n)]
    for (i, j) in edges_of(mask, n):
        adj[i].append(j)
        adj[j].append(i)
    seen = {0}
    st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                st.append(w)
    return len(seen) == n
