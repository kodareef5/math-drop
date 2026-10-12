import sys, traceback
from sage.all import EllipticCurve
for lab in sys.argv[1:]:
    E = EllipticCurve(lab)
    print('==', lab, E.ainvs(), 'rank', E.rank(), 'sha_an', E.sha().an())
    try:
        r = E.prove_BSD(verbosity=1)
        print('RESULT', r)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        last = [f for f in tb if 'BSD.py' in f.filename]
        print('EXC', type(e).__name__, str(e)[:200])
        for f in last[-2:]:
            print('   at BSD.py line', f.lineno, ':', f.line)
