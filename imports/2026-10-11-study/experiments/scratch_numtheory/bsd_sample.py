"""
Random sample of rank<=1 optimal curves with conductor 5000-9999; run
prove_BSD() for each in a separate process with a hard kill timeout
(SIGALRM cannot interrupt PARI/eclib C code).
Usage: python bsd_sample.py NSAMPLE TIMEOUT OUT
"""
import sys, json, random, subprocess, time
import sage.all  # noqa
from sage.databases.cremona import CremonaDatabase

ns, tlim, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
db = CremonaDatabase()
rng = random.Random(11102026)
labels = []
while len(labels) < ns:
    N = rng.randrange(5000, 10000)
    try:
        cs = db.allcurves(N)
    except Exception:
        continue
    opt = [(k, v) for k, v in cs.items() if k.endswith('1') and int(v[1]) <= 1]
    if not opt:
        continue
    k, v = rng.choice(opt)
    labels.append(('%d%s' % (N, k), int(v[1])))
py = sys.executable
code = ("import sys,json;from sage.all import EllipticCurve;E=EllipticCurve(sys.argv[1]);"
        "r=E.prove_BSD();print(json.dumps([int(p) for p in r]))")
res = []
for lab, r in labels:
    t = time.time()
    try:
        p = subprocess.run([py, '-I', '-c', code, lab], capture_output=True, text=True, timeout=tlim)
        last = (p.stdout.strip().splitlines() or [''])[-1]
        rem = json.loads(last) if last.startswith('[') else 'error:' + (p.stderr.strip().splitlines() or ['?'])[-1][:90]
    except subprocess.TimeoutExpired:
        rem = 'timeout'
    res.append({'label': lab, 'rank': r, 'remaining': rem, 'secs': round(time.time() - t, 1)})
    with open(out, 'w') as f:
        json.dump(res, f)
proved = sum(1 for x in res if x['remaining'] == [])
openp = [x for x in res if isinstance(x['remaining'], list) and x['remaining']]
other = [x for x in res if not isinstance(x['remaining'], list)]
print('sample', len(res), 'proved', proved, 'open', len(openp), 'timeout/error', len(other))
