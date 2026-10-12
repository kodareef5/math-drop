"""Exact output laws of vegan's binary fixed-margin null models, from the C code in src/nestedness.c
(vegan a574546), on small margins. Ideal RNG.

swap      : each counted step = retry 2x2 draws until a checkerboard is found and swapped
            -> stationary law ~ number of checkerboard (swappable) 2x2 submatrices.
tswap     : each trial draws a 2x2 submatrix uniformly; swaps if checkerboard, else holds -> symmetric.
curveball : ordered pair of distinct rows uniform; uniform reallocation of row-unique columns -> heat bath.
quasiswap : start from r2dtable (Patefield = hypergeometric law on integer tables with the margins), apply
            quasiswap steps (uniform cell a, uniform other row, uniform other col) until binary, checking
            every `thin` steps. Absorbing chain; we compute the exact absorption law.
"""
import itertools, math, json
from fractions import Fraction
import numpy as np


def int_tables(r, c):
    """All nonnegative integer matrices with row sums r, col sums c."""
    nr, nc = len(r), len(c)
    out = []

    def rec(i, colrem, rows):
        if i == nr:
            if all(x == 0 for x in colrem):
                out.append(tuple(rows))
            return
        # compositions of r[i] bounded by colrem
        def comp(j, left, cur):
            if j == nc - 1:
                if left <= colrem[j]:
                    yield cur + [left]
                return
            for v in range(min(left, colrem[j]) + 1):
                yield from comp(j + 1, left - v, cur + [v])
        for row in comp(0, r[i], []):
            rec(i + 1, [colrem[j] - row[j] for j in range(nc)], rows + [tuple(row)])

    rec(0, list(c), [])
    return out


def hypergeom_prob(X, r, c):
    N = sum(r)
    num = math.prod(math.factorial(x) for x in r) * math.prod(math.factorial(x) for x in c)
    den = math.factorial(N) * math.prod(math.factorial(x) for row in X for x in row)
    return Fraction(num, den)


def is_binary(X):
    return all(x <= 1 for row in X for x in row)


def quasiswap_step(X):
    """Distribution over next states from one iteration of the quasiswap inner loop."""
    nr, nc = len(X), len(X[0])
    out = {}
    p0 = Fraction(1, nr * nc * (nr - 1) * (nc - 1))
    for r0 in range(nr):
        for c0 in range(nc):
            for r1 in range(nr):
                if r1 == r0:
                    continue
                a, cc = X[r0][c0], X[r1][c0]
                if a == 0 and cc == 0:
                    out[X] = out.get(X, 0) + p0 * (nc - 1)
                    continue
                for c1 in range(nc):
                    if c1 == c0:
                        continue
                    b, d = X[r0][c1], X[r1][c1]
                    Y = [list(row) for row in X]
                    if d > 0 and a > 0 and a + d - b - cc >= 2:
                        Y[r0][c0] -= 1; Y[r1][c1] -= 1; Y[r0][c1] += 1; Y[r1][c0] += 1
                    elif cc > 0 and b > 0 and b + cc - a - d >= 2:
                        Y[r0][c0] += 1; Y[r1][c1] += 1; Y[r0][c1] -= 1; Y[r1][c0] -= 1
                    Y = tuple(tuple(row) for row in Y)
                    out[Y] = out.get(Y, 0) + p0
    return out


def quasiswap_law(r, c, thin=1):
    S = int_tables(r, c)
    idx = {X: i for i, X in enumerate(S)}
    N = len(S)
    P = np.zeros((N, N))
    for X in S:
        for Y, p in quasiswap_step(X).items():
            P[idx[X], idx[Y]] += float(p)
    Pk = np.linalg.matrix_power(P, thin)
    start = np.array([float(hypergeom_prob(X, r, c)) for X in S])
    B = [i for i, X in enumerate(S) if is_binary(X)]
    T = [i for i, X in enumerate(S) if not is_binary(X)]
    Q = Pk[np.ix_(T, T)]
    R = Pk[np.ix_(T, B)]
    absorb = start[B] + start[T] @ np.linalg.solve(np.eye(len(T)) - Q, R)
    return [S[i] for i in B], absorb


def checkerboards(X):
    nr, nc = len(X), len(X[0])
    k = 0
    for r0, r1 in itertools.combinations(range(nr), 2):
        for c0, c1 in itertools.combinations(range(nc), 2):
            a, b, cc, d = X[r0][c0], X[r0][c1], X[r1][c0], X[r1][c1]
            if (a, b, cc, d) in ((1, 0, 0, 1), (0, 1, 1, 0)):
                k += 1
    return k


if __name__ == "__main__":
    cases = [((2, 2, 1), (2, 2, 1)), ((2, 1, 1), (1, 1, 1, 1)), ((3, 2, 2, 1), (3, 2, 2, 1)),
             ((2, 2, 2, 1), (3, 2, 1, 1)), ((3, 3, 2, 2), (2, 2, 2, 2, 2)), ((2, 2, 2, 2), (2, 2, 2, 2))]
    res = []
    for r, c in cases:
        Bs, law = quasiswap_law(r, c, thin=1)
        Nb = len(Bs)
        u = 1 / Nb
        cb = np.array([checkerboards(X) for X in Bs], float)
        pi_swap = cb / cb.sum()
        row = {"rows": r, "cols": c, "n_binary": Nb,
               "quasiswap_thin1_TV": round(float(0.5 * abs(law - u).sum()), 4),
               "quasiswap_thin1_max/min": round(float(law.max() / law.min()), 3),
               "swap_TV": round(float(0.5 * abs(pi_swap - u).sum()), 4),
               "swap_max/min": round(float(cb.max() / cb.min()), 3)}
        for th in (10, 100):
            _, l2 = quasiswap_law(r, c, thin=th)
            row[f"quasiswap_thin{th}_TV"] = round(float(0.5 * abs(l2 - u).sum()), 5)
        print(json.dumps(row), flush=True)
        res.append(row)
    json.dump(res, open("vegan_exact.json", "w"), indent=1)
