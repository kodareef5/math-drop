import sys, time, random, statistics
sys.path.insert(0,'.')
from artin_wp import *
from sage.all import BraidGroup, ArtinGroup, CoxeterMatrix, matrix, identity_matrix
rng=random.Random(7)
def freered(w):
    out=[]
    for g in w:
        if out and out[-1][0]==g[0] and out[-1][1]==-g[1]: out.pop()
        else: out.append(g)
    return out
def check_d2(Z,E):
    # verify d^2 = 0 on the complex
    out={}
    for (s,t),y in E.D.items(): out.setdefault(s,{})[t]=y
    for s in out:
        acc={}
        for t,y in out[s].items():
            for u_,y2 in out.get(t,{}).items():
                for b,c in Z.mul(y,y2).items():
                    acc[(u_,b)]=acc.get((u_,b),0)+c
        if any(c!=0 for c in acc.values()): return False
    return True
# 1) Type A3 (braid group B4) vs Sage Garside normal form, random words
cox={(1,2):3,(2,3):3,(1,3):2}
Z,_=build(cox)
B=BraidGroup(4)
agree=0; n=0; ntrue=0; t0=time.time()
for trial in range(300):
    L=rng.randint(1,10)
    w=freered([(rng.randint(1,3), rng.choice([1,-1])) for _ in range(L)])
    # half of the trials: make an identity by w * (braid-relation-rewritten w)^-1
    if trial%2==0:
        # rewrite w by applying random braid relations on positive/negative subwords via Sage's normal form word
        b=B([g*e for g,e in w]) if w else B.one()
        w2=[(abs(x), 1 if x>0 else -1) for x in b.Tietze()]
        w=freered(w+inv(w2))
    truth = (B([g*e for g,e in w])==B.one()) if w else True
    E=act(Z,w)
    assert check_d2(Z,E)
    mine = len(E.S)==1 and list(E.S.values())[0]==('f',0,0)
    n+=1; agree+=(mine==truth); ntrue+=truth
print(f"A3/B4 vs Sage Garside: {agree}/{n} agree ({ntrue} identities)  {time.time()-t0:.1f}s")
# 2) affine A~2 and (3,3,oo), (oo,oo,oo): identities from relator insertion must test True;
#    non-identities: cross-check with generalized Burau (Sage burau_matrix) -- if Burau != I then must be False.
def rel_words(cox):
    R=[]
    for (i,j),m in cox.items():
        if m=='oo': continue
        a=[(i,1),(j,1)]*m; a=a[:m]
        b=[(j,1),(i,1)]*m; b=b[:m]
        R.append(a+inv(b))
    return R
def rand_identity(cox, gens, k, L):
    R=rel_words(cox); w=[]
    for _ in range(k):
        c=[(rng.choice(gens),rng.choice([1,-1])) for _ in range(rng.randint(0,L))]
        r=rng.choice(R); r = r if rng.random()<0.5 else inv(r)
        w=w+c+r+inv(c)
    return freered(w)
for name,cox in [('A~2',{(1,2):3,(2,3):3,(1,3):3}),('(3,3,oo)',{(1,2):3,(2,3):3,(1,3):'oo'}),('(oo,oo,oo) free',{(1,2):'oo',(2,3):'oo',(1,3):'oo'}),('A~3 square',{(1,2):3,(2,3):3,(3,4):3,(1,4):3,(1,3):2,(2,4):2})]:
    Z,verts=build(cox)
    gens=verts
    mat=[[1 if i==j else (0 if cox.get((min(i,j),max(i,j)),2)=='oo' and False else 0) for j in verts] for i in verts]
    cm=[[1 if i==j else (-1 if cox.get((min(i,j),max(i,j)))=='oo' else cox.get((min(i,j),max(i,j)),2)) for j in verts] for i in verts]
    A=ArtinGroup(CoxeterMatrix(cm))
    ok_id=0; nid=0; peaks=[]
    for _ in range(40 if rel_words(cox) else 0):
        w=rand_identity(cox,gens,rng.randint(1,3),3)
        st={}; r=is_member(Z,w,st); nid+=1; ok_id+=r; peaks.append(st['peak'])
    ok_non=0; nnon=0; burau_nontriv=0
    for _ in range(60):
        w=freered([(rng.choice(gens),rng.choice([1,-1])) for _ in range(rng.randint(1,8))])
        if not w: continue
        r=is_member(Z,w)
        gg=A.gens(); el=A.one()
        for g,e in w: el=el*gg[verts.index(g)]**e
        if hasattr(el,'burau_matrix'):
            bm=el.burau_matrix(); nontriv = (bm != identity_matrix(bm.base_ring(), bm.nrows()))
        else:
            nontriv = (el != A.one())
        nnon+=1; burau_nontriv+=nontriv
        ok_non += (not (nontriv and r))
    print(f"{name}: relator-insertion identities recognised {ok_id}/{nid} (max peak {max(peaks) if peaks else 0}); random words consistent with Burau {ok_non}/{nnon} (Burau nontrivial on {burau_nontriv})")
# 3) parabolic membership in A~2 with X={1}
cox={(1,2):3,(2,3):3,(1,3):3}
Z1,_=build(cox,X=(1,))
tests=[([(1,1)]*5,True),([(1,1),(2,1)],False),([(2,1),(1,1),(2,-1)],False),([(1,-1),(1,-1),(1,1)],True)]
print("A~2 parabolic membership in A_{1}:", [is_member(Z1,w)==e for w,e in tests])
