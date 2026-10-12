import sys, time, random
sys.path.insert(0,'.')
from artin_wp import *
rng=random.Random(3)
def freered(w):
    out=[]
    for g in w:
        if out and out[-1][0]==g[0] and out[-1][1]==-g[1]: out.pop()
        else: out.append(g)
    return out
for name,cox in [('A3 (spherical)',{(1,2):3,(2,3):3,(1,3):2}),('A~2 (affine)',{(1,2):3,(2,3):3,(1,3):3}),('(3,3,oo)',{(1,2):3,(2,3):3,(1,3):'oo'}),('A~3 (affine,rank4)',{(1,2):3,(2,3):3,(3,4):3,(1,4):3,(1,3):2,(2,4):2})]:
    Z,verts=build(cox)
    row=[]
    for L in [4,8,12,16,20,24]:
        sizes=[]; peaks=[]; ts=[]
        for _ in range(5):
            w=freered([(rng.choice(verts),rng.choice([1,-1])) for _ in range(L)])
            st={}; t=time.time()
            try:
                is_member(Z,w,st); ts.append(time.time()-t); sizes.append(st['final']); peaks.append(st['peak'])
            except Exception as e:
                ts.append(float('nan'))
            if time.time()-t>60: break
        row.append((L,max(sizes),max(peaks),round(max(ts),2)))
        if max(ts)>60: break
    print(name,'random words: (len, max minimal-complex size, max peak, max secs) =',row, flush=True)
    # positive word: powers of Coxeter element c = s1 s2 ... sn
    row=[]
    for k in range(1,9):
        w=[(v,1) for v in verts]*k
        st={}; t=time.time(); is_member(Z,w,st); dt=time.time()-t
        row.append((len(w),st['final'],round(dt,2)))
        if dt>60: break
    print(name,'Coxeter-element powers c^k: (len, minimal-complex size, secs) =',row, flush=True)
