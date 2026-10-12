"""
Experiment: on how many rank<=1 optimal curves does Sage's prove_BSD (today's
unconditional machinery) FAIL to certify BSD(E,p) at every prime?  Those are
exactly the curves where family 002 (full BSD for Selmer corank <= 1) would add
a guarantee that is not already available.

Usage: python bsd_gap.py NMIN NMAX OUTFILE [per_curve_timeout_s]
"""
import sys, time, signal, json
from sage.all import EllipticCurve, Integer
from sage.databases.cremona import CremonaDatabase

class TO(Exception):
    pass

def handler(signum, frame):
    raise TO()

signal.signal(signal.SIGALRM, handler)

nmin, nmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
tlim = int(sys.argv[4]) if len(sys.argv) > 4 else 30
db = CremonaDatabase()
res = []
t0 = time.time()
for N in range(nmin, nmax + 1):
    try:
        curves = db.allcurves(N)
    except Exception:
        continue
    # one optimal curve per isogeny class (label ending in '1')
    for key, data in curves.items():
        if not key.endswith('1'):
            continue
        label = '%d%s' % (N, key)
        ainvs, r, tors = data[0], int(data[1]), int(data[2])
        if r > 1:
            continue
        E = EllipticCurve(ainvs)
        rec = {'label': label, 'rank': r}
        signal.alarm(tlim)
        try:
            ts = time.time()
            prim = E.prove_BSD()
            rec['remaining'] = [int(p) for p in prim]
            rec['sha_an'] = int(E.sha().an())
            rec['secs'] = round(time.time() - ts, 2)
        except TO:
            rec['remaining'] = 'timeout'
        except Exception as e:  # noqa
            rec['remaining'] = 'error:' + type(e).__name__ + ':' + str(e)[:80]
        finally:
            signal.alarm(0)
        res.append(rec)
    with open(out, 'w') as f:
        json.dump(res, f)
with open(out, 'w') as f:
    json.dump(res, f)
n = len(res)
proved = sum(1 for r in res if r['remaining'] == [])
open_ = [r for r in res if isinstance(r['remaining'], list) and r['remaining']]
other = [r for r in res if not isinstance(r['remaining'], list)]
print('conductor range', nmin, nmax, 'rank<=1 optimal curves', n)
print('fully proved by prove_BSD:', proved)
print('primes left open:', len(open_), 'timeout/error:', len(other))
print('elapsed', round(time.time() - t0, 1))
