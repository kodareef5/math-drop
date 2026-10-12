"""Prototype of Procedure Label (OpenAI 'Deterministic quasipolynomial-time mean-payoff games',
04-algorithm.tex L21-85; parameters 03-translations.tex L13-16; reduction 02-boxes.tex).
Exact integers + Fractions. Verified against brute-force positional-strategy enumeration.
Purpose: (1) sanity-check the specification is implementable as written, (2) count calls."""
import sys, random, itertools, time
from fractions import Fraction as Fr
sys.setrecursionlimit(100000)

class Game:
    def __init__(s, n, owner, edges):   # owner[i] in {'max','min'}; edges: list of (i,j,w)
        s.n, s.owner, s.edges = n, owner, edges
        s.out = [[] for _ in range(n)]
        for i, j, w in edges: s.out[i].append((j, w))

def solve_label(g, stats):
    n = g.n
    W = max(abs((n + 1) * w + 1) for _, _, w in g.edges)
    wh = [[(j, (n + 1) * w + 1) for j, w in g.out[i]] for i in range(n)]
    D0 = 1
    while D0 < 64 * (n + 1) * (W + 1): D0 *= 2
    def F(z):
        r = []
        for i in range(n):
            vals = [w + z[j] for j, w in wh[i]]
            r.append(max(vals) if g.owner[i] == 'max' else min(vals))
        return r
    def basic(A, u):
        p = list(A)
        while True:
            fz = F(p)
            q = [min(u[i], max(A[i], fz[i])) for i in range(n)]
            stats['basic_evals'] += 1
            if q == p: return p
            p = q
    def label(A, D, a, b, depth=0):
        stats['calls'] += 1
        stats['maxdepth'] = max(stats['maxdepth'], depth)
        if all(a[i] * b[i] > 1 for i in range(n)):
            stats['mass_base'] += 1
            return ['+' if b[i] > 1 else '-' for i in range(n)]
        if D < 4096:
            stats['width_base'] += 1
            u = [A[i] + D for i in range(n)]
            z = basic(A, u)
            return ['+' if 2 * z[i] > 2 * A[i] + D else '-' for i in range(n)]
        P = D // 32
        c = [A[i] + D // 2 for i in range(n)]; M = D // 8; q = D // 128; p = q // 32
        # downward pass
        k = list(c); b43 = [Fr(4, 3) * x for x in b]
        while True:
            lab = label([k[i] - q // 2 for i in range(n)], q, a, b43, depth + 1)
            new = [max(c[i] - M, k[i] - p) if lab[i] == '-' else k[i] for i in range(n)]
            if new == k: break
            k = new
        Iminus = {i for i in range(n) if k[i] < c[i] - P}
        # upward pass
        a43 = [Fr(4, 3) * x for x in a]
        while True:
            lab = label([k[i] - q // 2 for i in range(n)], q, a43, b, depth + 1)
            new = [min(c[i] + M, k[i] + p) if lab[i] == '+' else k[i] for i in range(n)]
            if new == k: break
            k = new
        Iplus = {i for i in range(n) if k[i] > c[i] + P}
        # provisional
        lam0 = label([k[i] - D // 4 for i in range(n)], D // 2, a, b, depth + 1)
        ab = [(Fr(4, 5) * a[i], Fr(8, 5) * b[i]) if lam0[i] == '+' else (Fr(8, 5) * a[i], Fr(4, 5) * b[i]) for i in range(n)]
        out = label(A, D, [x for x, _ in ab], [y for _, y in ab], depth + 1)
        out = list(out)
        for i in range(n):
            if i in Iminus: out[i] = '-'
            elif i in Iplus: out[i] = '+'
        return out
    res = label([0] * n, D0, [Fr(1, n)] * n, [Fr(1, n)] * n)
    return {i for i in range(n) if res[i] == '+'}, D0

def brute(g):
    # Max wins from v iff exists positional sigma s.t. for all positional tau, cycle reached has mean >= 0
    n = g.n
    maxv = [i for i in range(n) if g.owner[i] == 'max']; minv = [i for i in range(n) if g.owner[i] == 'min']
    best = [False] * n
    for sig in itertools.product(*[range(len(g.out[i])) for i in maxv]):
        s = dict(zip(maxv, sig))
        ok = [True] * n
        for tau in itertools.product(*[range(len(g.out[i])) for i in minv]):
            t = dict(zip(minv, tau))
            for v in range(n):
                seen = {}; path = []; x = v
                while x not in seen:
                    seen[x] = len(path); j, w = g.out[x][s[x] if x in s else t[x]]; path.append(w); x = j
                cyc = path[seen[x]:]
                if sum(cyc) < 0: ok[v] = False
        for v in range(n): best[v] = best[v] or ok[v]
    return {v for v in range(n) if best[v]}

def random_game(n, outdeg, W, rng):
    owner = [rng.choice(['max', 'min']) for _ in range(n)]
    edges = []
    for i in range(n):
        for j in rng.sample(range(n), min(outdeg, n)):
            edges.append((i, j, rng.randint(-W, W)))
    return Game(n, owner, edges)

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    cfgs = [(2, 2, 3), (3, 2, 3), (3, 2, 20), (4, 2, 5)]
    for n, d, W in cfgs:
        for rep in range(3):
            g = random_game(n, d, W, rng)
            st = {'calls': 0, 'basic_evals': 0, 'mass_base': 0, 'width_base': 0, 'maxdepth': 0}
            t = time.time(); U, D0 = solve_label(g, st); dt = time.time() - t
            B = brute(g)
            print(f"n={n} W={W} D0=2^{D0.bit_length()-1}: correct={U == B} calls={st['calls']:.3e} width_base={st['width_base']} "
                  f"basic_evals={st['basic_evals']} depth={st['maxdepth']} time={dt:.1f}s", flush=True)
