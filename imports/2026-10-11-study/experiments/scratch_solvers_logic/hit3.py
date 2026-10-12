"""H_n sampler v3: same bisection as hit2 but the engine is pluggable:
 'minisat22'/'cadical195' via pysat, or 'march' via subprocess (look-ahead, strong on random UNSAT)."""
import sys, random, time, json, subprocess, os, tempfile
from pysat.solvers import Solver
MARCH = '/home/claude/work/repos/march/march_nh'
TMP = os.environ.get('HTMP', '/tmp/claude-0')

def solve(clauses, n, engine):
    if engine == 'march':
        fd, path = tempfile.mkstemp(suffix='.cnf', dir=TMP)
        with os.fdopen(fd, 'w') as f:
            f.write(f'p cnf {n} {len(clauses)}\n')
            for c in clauses: f.write(f'{c[0]} {c[1]} {c[2]} 0\n')
        out = subprocess.run([MARCH, path], capture_output=True, text=True).stdout
        os.unlink(path)
        if 's UNSATISFIABLE' in out: return False, None
        if 's SATISFIABLE' not in out: raise RuntimeError('march: ' + out[-300:])
        model = []
        for line in out.splitlines():
            if line.startswith('v '): model += [int(x) for x in line[2:].split() if x != '0']
        return True, model
    with Solver(name=engine, bootstrap_with=clauses) as s:
        if s.solve(): return True, s.get_model()
        return False, None

def sample_H(n, rng, engine, factor=8, start=4.26):
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
            if not any((l > 0) == val[abs(l)] for l in clauses[j]): return j
        return M
    lo, hi, nsolve = 0, None, 0
    step = max(2, int(0.5 * n ** 0.5))
    mid = int(start * n)
    while hi is None or hi - lo > 1:
        if hi is not None: mid = (lo + hi) // 2
        elif lo >= mid: mid = lo + step
        nsolve += 1
        sat, model = solve(clauses[:mid], n, engine)
        if sat:
            # verify model really satisfies the prefix
            j = first_falsified(model, 0)
            if j < mid: raise RuntimeError('bad model')
            lo = first_falsified(model, mid)
            if lo >= M: raise RuntimeError('factor')
        else:
            hi = mid
        if hi is not None and hi <= lo: raise RuntimeError('inconsistent')
    return hi, nsolve

if __name__ == '__main__':
    n = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3]); engine = sys.argv[4]; out = sys.argv[5]
    rng = random.Random(seed)
    with open(out, 'a') as f:
        for i in range(N):
            t = time.time(); H, k = sample_H(n, rng, engine)
            f.write(json.dumps({'n': n, 'seed': seed, 'i': i, 'H': H, 'nsolve': k, 'engine': engine, 't': round(time.time() - t, 3)}) + '\n'); f.flush()
