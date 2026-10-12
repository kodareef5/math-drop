import sys, importlib.util, traceback, signal
from sage.all import EllipticCurve
spec = importlib.util.spec_from_file_location('BSD_patched', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM, h)
for lab in sys.argv[2:]:
    E = EllipticCurve(lab)
    signal.alarm(120)
    try:
        r = m.prove_BSD(E)
        print(lab, 'patched result:', r, 'sha_an', E.sha().an())
    except TO:
        print(lab, 'TIMEOUT 120s')
    except Exception as e:
        tb=[f for f in traceback.extract_tb(e.__traceback__) if 'BSD_patched' in f.filename]
        print(lab, 'EXC', type(e).__name__, str(e)[:120], 'line', tb[-1].lineno if tb else '?', tb[-1].line if tb else '')
    finally:
        signal.alarm(0)
