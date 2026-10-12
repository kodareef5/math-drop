"""Family 272: build the explicit 10x10 zero-key state rho = Z/tr Z (paper eqs. explicit-matrices, L, UV, SR, phi-pair)
numerically and check basic properties + what standard detectors see.
  - PSD, trace 1, PPT (partial transpose PSD)
  - rank of Z, product-free range is the paper's certificate (not re-proved here)
  - realignment (CCNR) criterion value: >1 detects entanglement
  - range dimension vs 100
"""
import numpy as np, itertools, json

M0 = np.array([[6,0,0,0],[0,6,0,0],[0,0,6,0],[0,0,0,6],[0,0,0,0],[0,0,0,0]],float)
M1 = np.array([[-12,0,0,0],[0,-6,0,0],[0,0,6,0],[0,0,0,12],[-6,0,6,6],[-6,-6,6,0]],float)
M2 = np.array([[0,6,-2,0],[6,6,0,2],[-2,0,10,0],[0,2,0,24],[0,0,0,6],[0,-6,6,-6]],float)
M3 = np.array([[0,0,-4,-3],[0,-2,-3,-4],[-4,-3,11,6],[-3,-4,6,25],[6,6,0,0],[0,-6,6,6]],float)
Ms = [M0,M1,M2,M3]
# check block symmetry M_i^T M_j = M_j^T M_i
assert all(np.allclose(Ms[i].T@Ms[j], Ms[j].T@Ms[i]) for i in range(4) for j in range(4))
# L(A) = sum_r Q_r A Q_r^*, Q_r has i-th column = (row r of M_i)^T
Q = [np.column_stack([Ms[i][r,:] for i in range(4)]) for r in range(6)]
def L(A): return sum(q@A@q.conj().T for q in Q)
def Ladj(Y): return sum(q.conj().T@Y@q for q in Q)
# check L(E_ij) = M_i^T M_j
for i in range(4):
    for j in range(4):
        E=np.zeros((4,4));E[i,j]=1
        assert np.allclose(L(E), Ms[i].T@Ms[j])
# U: C^10 -> C^4 (x) C^4 (symmetric), V: C^6 -> antisymmetric
sym=[(i,j) for i in range(4) for j in range(i,4)]
asym=[(i,j) for i in range(4) for j in range(i+1,4)]
def e(k,n=4): v=np.zeros(n); v[k]=1; return v
U=np.zeros((16,10)); V=np.zeros((16,6))
for c,(i,j) in enumerate(sym):
    U[:,c]= np.kron(e(i),e(j)) if i==j else (np.kron(e(i),e(j))+np.kron(e(j),e(i)))/np.sqrt(2)
for c,(i,j) in enumerate(asym):
    V[:,c]=(np.kron(e(i),e(j))-np.kron(e(j),e(i)))/np.sqrt(2)
def LL(X):  # (L (x) L) on 16x16 via Kraus
    return sum(np.kron(q1,q2)@X@np.kron(q1,q2).conj().T for q1 in Q for q2 in Q)
def LLadj(Y):
    return sum(np.kron(q1,q2).conj().T@Y@np.kron(q1,q2) for q1 in Q for q2 in Q)
# K signed permutation on C^6
comp={ (0,1):((2,3),+1),(0,2):((1,3),-1),(0,3):((1,2),+1),(1,2):((0,3),+1),(1,3):((0,2),-1),(2,3):((0,1),+1)}
K=np.zeros((6,6))
for c,(ij) in enumerate(asym):
    kl,s=comp[ij]; K[asym.index(kl),c]=s
def S(A): return V.T@LL(U@A@U.T)@V
def Sadj(Y): return U.T@LLadj(V@Y@V.T)@U
def Radj(Y): return Sadj((K.T@Y@K).T)
Emb=np.zeros((10,6)); Emb[:6,:6]=np.eye(6)
def Phi1(A): return Emb@S(A.T)@Emb.T
def Phi2(B): return Radj(Emb.T@B@Emb)
Z=np.zeros((100,100),complex)
for i in range(10):
    for j in range(10):
        Eij=np.zeros((10,10)); Eij[i,j]=1
        Z+=np.kron(Eij, Phi2(Phi1(Eij)))
Z=(Z+Z.conj().T)/2
tr=np.trace(Z).real
rho=Z/tr
w=np.linalg.eigvalsh(rho)
def ptranspose(X,d=10):  # partial transpose on second factor
    return X.reshape(d,d,d,d).transpose(0,3,2,1).reshape(d*d,d*d)
wpt=np.linalg.eigvalsh((ptranspose(rho)+ptranspose(rho).conj().T)/2)
def realign(X,d=10):
    return X.reshape(d,d,d,d).transpose(0,2,1,3).reshape(d*d,d*d)
ccnr=np.linalg.svd(realign(rho),compute_uv=False).sum()
rank=int((w>1e-10*w.max()).sum())
out=dict(trace_Z=float(tr), min_eig=float(w.min()), rank=rank, min_eig_PT=float(wpt.min()),
         ccnr_trace_norm=float(ccnr), ccnr_detects=bool(ccnr>1+1e-9),
         purity=float(np.trace(rho@rho).real))
# Purity-based / reduction criterion: rho_A (x) I - rho >= 0 ?
rA=np.trace(rho.reshape(10,10,10,10),axis1=1,axis2=3); rB=np.trace(rho.reshape(10,10,10,10),axis1=0,axis2=2)
out['reduction_min_eig']=float(np.linalg.eigvalsh(np.kron(rA,np.eye(10))-rho).min())
out['local_ranks']=[int(np.linalg.matrix_rank(rA,1e-10)),int(np.linalg.matrix_rank(rB,1e-10))]
print(json.dumps(out,indent=1))
np.save('zero_key_rho.npy',rho)
