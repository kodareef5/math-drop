"""Sample the random 3-SAT hitting time H_n (first unsatisfiable prefix) for the
proper-clause-with-replacement model of the OpenAI 'Linear Variance' paper.
Uses one incremental solver per instance with selector literals; SAT answers
advance the lower bound to the first clause falsified by the model, UNSAT answers
pull the upper bound to the max index in the assumption core."""
import sys, random, time, json
from pysat.solvers import Solver

def sample_H(n, rng, solver_name='cadical195', factor=8):
    M = factor * n
    clauses = []
    for _ in range(M):
        vs = rng.sample(range(1, n + 1), 3)
        clauses.append([v if rng.random() < 0.5 else -v for v in vs])
    sel = [n + 1 + j for j in range(M)]           # selector for clause j (0-based)
    s = Solver(name=solver_name)
    for j, c in enumerate(clauses):
        s.add_clause(c + [-sel[j]])
    lo, hi = 0, None      # F_lo is SAT (lo clauses); F_hi is UNSAT
    guess = int(4.2 * n)
    nsolve = 0
    def first_falsified(model, start):
        val = [False] * (n + 1)
        for lit in model[:n]:
            if abs(lit) <= n: val[abs(lit)] = lit > 0
        for j in range(start, M):
            if not any((l > 0) == val[abs(l)] for l in clauses[j]):
                return j          # 0-based index of first falsified clause
        return M
    while hi is None or hi - lo > 1:
        if hi is None:
            mid = max(lo + 1, guess) if lo < guess else min(M, lo + max(1, n // 10))
        else:
            mid = (lo + hi) // 2
        nsolve += 1
        if s.solve(assumptions=sel[:mid]):
            j = first_falsified(s.get_model(), mid)
            lo = j                 # clauses 0..j-1 satisfied => F_j SAT
            if lo >= M:
                raise RuntimeError('increase factor')
        else:
            core = s.get_core()
            hi = max(x - n - 1 for x in core) + 1 if core else 0
            # core lits are selectors; index+1 = prefix length
    s.delete()
    return hi, nsolve

if __name__ == '__main__':
    n = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3])
    solver = sys.argv[4] if len(sys.argv) > 4 else 'cadical195'
    out = sys.argv[5] if len(sys.argv) > 5 else f'H_n{n}_s{seed}.jsonl'
    rng = random.Random(seed)
    with open(out, 'a') as f:
        for i in range(N):
            t = time.time()
            H, k = sample_H(n, rng, solver)
            f.write(json.dumps({'n': n, 'H': H, 'nsolve': k, 't': round(time.time() - t, 3)}) + '\n')
            f.flush()
