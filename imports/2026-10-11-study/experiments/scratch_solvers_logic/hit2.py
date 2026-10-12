"""H_n sampler v2: fresh solver per query (no selector assumptions).
SAT at prefix m -> lo = first clause index falsified by the model (prefix of that length is SAT).
UNSAT at prefix m -> hi = m.  Answer H = hi where F_{hi} UNSAT and F_{hi-1} SAT."""
import sys, random, time, json
from pysat.solvers import Solver

def sample_H(n, rng, solver_name='minisat22', factor=8, start=4.26):
    M = factor * n
    clauses = []
    for _ in range(M):
        vs = rng.sample(range(1, n + 1), 3)
        clauses.append([v if rng.random() < 0.5 else -v for v in vs])
    def first_falsified(model, startj):
        val = [False] * (n + 1)
        for lit in model:
            if abs(lit) <= n: val[abs(lit)] = lit > 0
        for j in range(startj, M):
            if not any((l > 0) == val[abs(l)] for l in clauses[j]):
                return j
        return M
    lo, hi = 0, None
    nsolve = 0
    step = max(2, int(0.5 * n ** 0.5))
    mid = int(start * n)
    while hi is None or hi - lo > 1:
        if hi is not None:
            mid = (lo + hi) // 2
        elif lo >= mid:
            mid = lo + step
        nsolve += 1
        with Solver(name=solver_name, bootstrap_with=clauses[:mid]) as s:
            if s.solve():
                lo = first_falsified(s.get_model(), mid)
                if lo >= M: raise RuntimeError('factor')
                if hi is not None and lo >= hi: raise RuntimeError('inconsistent')
            else:
                hi = mid
                if hi <= lo: raise RuntimeError('inconsistent2')
    return hi, nsolve

if __name__ == '__main__':
    n = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3])
    solver = sys.argv[4] if len(sys.argv) > 4 else 'minisat22'
    out = sys.argv[5]
    rng = random.Random(seed)
    with open(out, 'a') as f:
        for i in range(N):
            t = time.time()
            H, k = sample_H(n, rng, solver)
            f.write(json.dumps({'n': n, 'seed': seed, 'i': i, 'H': H, 'nsolve': k, 't': round(time.time() - t, 3)}) + '\n')
            f.flush()
