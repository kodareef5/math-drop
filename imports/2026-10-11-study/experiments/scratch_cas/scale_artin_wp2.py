import sys, time, random, signal
sys.path.insert(0,'.')
from artin_wp import *
class TO(Exception): pass
def h(s,f): raise TO
signal.signal(signal.SIGALRM,h)
rng=random.Random(3)
def freered(w):
    out=[]
    for g in w:
        if out and out[-1][0]==g[0] and out[-1][1]==-g[1]: out.pop()
        else: out.append(g)
    return out
CAP=int(sys.argv[1]) if len(sys.argv)>1 else 30
for name,cox in [('A3 (spherical)',{(1,2):3,(2,3):3,(1,3):2}),('A~2 (affine)',{(1,2):3,(2,3):3,(1,3):3}),('(3,3,oo)',{(1,2):3,(2,3):3,(1,3):'oo'}),('A~3 (affine,rank4)',{(1,2):3,(2,3):3,(3,4):3,(1,4):3,(1,3):2,(2,4):2})]:
    Z,verts=build(cox)
    for L in [4,6,8,10,12,14,16]:
        sizes=[]; peaks=[]; ts=[]; to=0
        for _ in range(4):
            w=freered([(rng.choice(verts),rng.choice([1,-1])) for _ in range(L)])
            st={}; t=time.time()
            signal.alarm(CAP)
            try:
                is_member(Z,w,st); signal.alarm(0); ts.append(time.time()-t); sizes.append(st['final']); peaks.append(st['peak'])
            except TO:
                to+=1
        print(f"{name} random L={L}: max minimal size {max(sizes) if sizes else '-'}, max peak {max(peaks) if peaks else '-'}, max secs {max(ts) if ts else '-':.3}, timeouts({CAP}s) {to}/4" if ts else f"{name} random L={L}: all timed out", flush=True)
        if to>=2: break
    for k in range(1,12):
        w=[(v,1) for v in verts]*k
        st={}; t=time.time(); signal.alarm(CAP)
        try:
            is_member(Z,w,st); signal.alarm(0)
            print(f"{name} c^{k} (len {len(w)}): minimal size {st['final']}, peak {st['peak']}, {time.time()-t:.2f}s", flush=True)
        except TO:
            print(f"{name} c^{k}: timeout", flush=True); break
