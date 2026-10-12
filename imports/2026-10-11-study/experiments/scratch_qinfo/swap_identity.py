"""Check: for CP maps F: M_a->M_b, G: M_d->M_c and effect M on BC,
sigma_AD = Tr_BC[(J(F)_AB (x) J'(G)_CD)(1_A (x) M_BC (x) 1_D)] equals [(F^dag (x) G^dag)(M)]^T (on A (x) D).
If F,G are PPT this writes sigma_AD in the paper's represented class C (Def. represented-class) => K_D = 0 by Thm zero-key."""
import numpy as np
rng=np.random.default_rng(3)
a,b,c,d=2,3,3,2
def rk(n,m,k): return [rng.normal(size=(m,n))+1j*rng.normal(size=(m,n)) for _ in range(k)]
KF=rk(a,b,3); KG=rk(d,c,2)
F=lambda X: sum(k@X@k.conj().T for k in KF); Fd=lambda Y: sum(k.conj().T@Y@k for k in KF)
G=lambda X: sum(k@X@k.conj().T for k in KG); Gd=lambda Y: sum(k.conj().T@Y@k for k in KG)
def E(n,i,j): e=np.zeros((n,n),complex); e[i,j]=1; return e
JF=sum(np.kron(E(a,i,j),F(E(a,i,j))) for i in range(a) for j in range(a))          # A(x)B
JG=sum(np.kron(G(E(d,i,j)),E(d,i,j)) for i in range(d) for j in range(d))          # C(x)D
X=rng.normal(size=(b*c,b*c))+1j*rng.normal(size=(b*c,b*c)); M=X@X.conj().T          # effect on BC (unnormalised)
big=np.kron(JF,JG)                                   # A B C D
op=np.kron(np.kron(np.eye(a),M),np.eye(d))
T=(big@op).reshape(a,b,c,d,a,b,c,d)
sigma=np.einsum('ibcjkbcl->ijkl',T).reshape(a*d,a*d)
# (F^dag (x) G^dag)(M) via Kraus
FG=sum(np.kron(k1,k2).conj().T@M@np.kron(k1,k2) for k1 in KF for k2 in KG)
print('max|sigma - [(Fd x Gd)(M)]^T| =', np.abs(sigma-FG.T).max(), ' scale', np.abs(sigma).max())
