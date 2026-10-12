"""
Prototype of the uniform word/parabolic-membership algorithm of
'Parabolic intersections in Artin groups' (OpenAI, Sep 2026), Cor. cor:membership, Sec. 8,
restricted to Coxeter matrices with labels in {2,3,oo}.  For these labels the fusion
category is Vec (no label >= 4), so the algebra Z is the zigzag algebra of the graph
S + {f} (label 3 -> one arrow pair, oo -> two arrow pairs, 2 -> none); f joins S minus X by label 3.
(The auxiliary frame vertex o never enters the computation: twists by colours of S never
create P_o summands.)  B_i = Cone(P_i (x) e_i E -> E), D_i = inverse (coevaluation) twist.
Test: w in A_X  <=>  minimal complex of B_w P_f is P_f<0>[0].
"""
from fractions import Fraction
import itertools, random, time, sys

class Zigzag:
    def __init__(self, mult):
        self.mult = mult            # dict (i,j) -> 0/1/2, symmetric
        pass
    def m(self,i,j): return self.mult.get((i,j),0) if i!=j else 0
    def basis(self,i,j):
        if i==j: return [('e',i),('t',i)]
        return [('a',i,j,k) for k in range(self.m(i,j))]
    @staticmethod
    def deg(b): return {'e':0,'a':1,'t':2}[b[0]]
    def dual(self,b):   # tau(b * dual(b)) = 1, dual(b) in e_j Z e_i
        if b[0]=='e': return ('t',b[1])
        if b[0]=='t': return ('e',b[1])
        return ('a',b[2],b[1],b[3])
    def mulb(self,b1,b2):  # product of basis elements (path order) -> basis elt or None
        if b1[0]=='e': return b2
        if b2[0]=='e': return b1
        if b1[0]=='t' or b2[0]=='t': return None
        # arrow*arrow
        if b1[2]==b2[1] and b2[2]==b1[1] and b1[3]==b2[3]: return ('t',b1[1])
        return None
    def mul(self,x,y):   # dict elements
        out={}
        for b1,c1 in x.items():
            for b2,c2 in y.items():
                b=self.mulb(b1,b2)
                if b is not None:
                    out[b]=out.get(b,0)+c1*c2
        return {b:c for b,c in out.items() if c!=0}

class Cx:
    """complex of graded projectives: summands {id:(vertex, cochain, shift)}, D {(src,tgt): elt}"""
    def __init__(self): self.S={}; self.D={}; self.n=0
    def add(self,v,c,a): self.n+=1; self.S[self.n]=(v,c,a); return self.n

def twist(Z,E,i,inverse=False):
    N=Cx(); emap={}; ymap={}
    for s,(j,c,a) in E.S.items():
        emap[s]=N.add(j,c,a)
    for s,(j,c,a) in E.S.items():
        for z in Z.basis(i,j):
            if inverse: ymap[(s,z)]=N.add(i,c+1,a+Z.deg(z)-2)
            else:       ymap[(s,z)]=N.add(i,c-1,a+Z.deg(z))
    sgnE = 1
    sgnY = -1
    for (s,t),y in E.D.items():
        N.D[(emap[s],emap[t])]=dict(y)
        j=E.S[s][0]
        for z in Z.basis(i,j):
            prod=Z.mul({z:1},y)
            for z2,cf in prod.items():
                key=(ymap[(s,z)],ymap[(t,z2)])
                N.D[key]={('e',i):sgnY*cf}
    for s,(j,c,a) in E.S.items():
        for z in Z.basis(i,j):
            if inverse: N.D[(emap[s],ymap[(s,z)])]={Z.dual(z):1}   # coevaluation E -> Y
            else:       N.D[(ymap[(s,z)],emap[s])]={z:1}            # evaluation Y -> E
    return N

def minimize(Z,E):
    S=E.S; D=E.D
    out={}; inn={}
    for (s,t),y in D.items():
        out.setdefault(s,{})[t]=y; inn.setdefault(t,{})[s]=y
    changed=True
    while True:
        found=None
        for (s,t),y in list(D.items()):
            v=S[s][0]
            lam=y.get(('e',v),0) if S[t][0]==v else 0
            if lam!=0: found=(s,t,Fraction(lam)); break
        if not found: break
        b1,b2,lam=found
        inv=Fraction(1)/lam
        srcs=[x for x in inn.get(b2,{}) if x!=b1]   # delta_x : x -> b2
        tgts=[y for y in out.get(b1,{}) if y!=b2]   # gamma_y : b1 -> y
        for x in srcs:
            dx=inn[b2][x]
            for yv in tgts:
                gy=out[b1][yv]
                corr=Z.mul(Z.mul(dx,{('e',S[b2][0]):inv}),gy)
                cur=dict(D.get((x,yv),{}))
                for b,cf in corr.items():
                    cur[b]=cur.get(b,0)-cf
                cur={b:cf for b,cf in cur.items() if cf!=0}
                if cur:
                    D[(x,yv)]=cur; out.setdefault(x,{})[yv]=cur; inn.setdefault(yv,{})[x]=cur
                else:
                    D.pop((x,yv),None); out.get(x,{}).pop(yv,None); inn.get(yv,{}).pop(x,None)
        for b in (b1,b2):
            for t in list(out.get(b,{})): D.pop((b,t),None); inn.get(t,{}).pop(b,None)
            for s in list(inn.get(b,{})): D.pop((s,b),None); out.get(s,{}).pop(b,None)
            out.pop(b,None); inn.pop(b,None); S.pop(b)
    return E

def act(Z,word,f='f',minimize_each=True,stats=None):
    E=Cx(); E.add(f,0,0)
    peak=1
    for g in reversed(word):          # B_w = B_{g1}...B_{gk}; rightmost acts first
        i,e = (g,1) if not isinstance(g,tuple) else g
        E=twist(Z,E,i,inverse=(e<0))
        peak=max(peak,len(E.S))
        if minimize_each: E=minimize(Z,E)
    E=minimize(Z,E)
    if stats is not None: stats['peak']=peak; stats['final']=len(E.S)
    return E

def build(coxeter, X=()):
    """coxeter: dict (i,j)->m with m in {2,3,'oo'} for i<j over vertex list"""
    mult={}
    verts=sorted({v for e in coxeter for v in e})
    for (i,j),m in coxeter.items():
        k={2:0,3:1,'oo':2}[m]
        if k: mult[(i,j)]=k; mult[(j,i)]=k
    for v in verts:
        if v not in X: mult[(v,'f')]=1; mult[('f',v)]=1
    return Zigzag(mult), verts

def is_member(Z,word,stats=None):
    E=act(Z,word,stats=stats)
    return len(E.S)==1 and list(E.S.values())[0]==('f',0,0)

def inv(w): return [(g,-e) for (g,e) in reversed(w)]
def W(*gs): return [(g,1) if not isinstance(g,tuple) else g for g in gs]
