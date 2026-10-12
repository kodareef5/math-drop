"""Family 276: exact classical capacity of the qubit generalized amplitude-damping
channel (GADC) vs previously published upper bounds.

Exact formula (OpenAI 2026, thm:main, paper.tex L208-228):
  C(gamma,nu) = (1/ln2) max_p { h((1-gamma)p + gamma*nu) - g(v(p)) },
  v(p) = gamma*nu*(1-nu) + gamma*(1-gamma)*(p-nu)^2,  g(u) = h((1+sqrt(1-4u))/2).
Conventions: nu = stationary excited population = N in Khatri-Sharma-Wilde (KSW, PRA 102 012401).

Upper bounds implemented:
  KSW Prop.6   C_beta  = log2(1+sqrt(1-gamma))
  KSW Eq.137   C_cov   = chi(A_{gamma,1/2}) + 2 eps + gb(eps), eps = gamma|N-1/2|
  KSW Eq.149   C_Fil   (Filippov approximate-unitality bound)
  KSW Eq.152   C_E     entanglement-assisted capacity (computed directly from Stinespring, diagonal inputs)
  KSW Eq.136   C_EB    chi(M) + 2 eps1 + gb(eps1), M = diamond-nearest EB channel (SDP), chi(M) numerically
  Fang 2026    U_G     (arXiv 2609.14621 Thm 1), lower convex envelope numerically
All capacities in bits.
"""
import numpy as np
from scipy.optimize import minimize_scalar, minimize
import sys, json, itertools

LN2 = np.log(2.0)

def h_nats(x):
    x = np.clip(x, 0.0, 1.0)
    out = np.zeros_like(np.asarray(x, dtype=float))
    with np.errstate(divide='ignore', invalid='ignore'):
        t = -x*np.log(x) - (1-x)*np.log(1-x)
    return np.where((x > 0) & (x < 1), t, 0.0)

def h2(x):
    return h_nats(x)/LN2

def gdet_nats(u):
    u = np.clip(u, 0.0, 0.25)
    return h_nats((1+np.sqrt(1-4*u))/2)

def exact_capacity(gam, nu, grid=20001):
    p = np.linspace(0, 1, grid)
    obj = h_nats((1-gam)*p + gam*nu) - gdet_nats(gam*nu*(1-nu) + gam*(1-gam)*(p-nu)**2)
    i = int(np.argmax(obj))
    # refine
    lo, hi = p[max(i-1, 0)], p[min(i+1, grid-1)]
    f = lambda q: -(h_nats((1-gam)*q + gam*nu) - gdet_nats(gam*nu*(1-nu) + gam*(1-gam)*(q-nu)**2))
    if hi > lo:
        r = minimize_scalar(f, bounds=(lo, hi), method='bounded', options={'xatol': 1e-12})
        best = max(obj[i], -r.fun); pbest = r.x if -r.fun >= obj[i] else p[i]
    else:
        best, pbest = obj[i], p[i]
    return best/LN2, float(pbest)

# ---------- channel as matrices (KSW Kraus operators) ----------
def kraus(gam, N):
    k1 = np.sqrt(1-N)*np.array([[1, 0], [0, np.sqrt(1-gam)]], dtype=complex)
    k2 = np.sqrt(gam*(1-N))*np.array([[0, 1], [0, 0]], dtype=complex)
    k3 = np.sqrt(N)*np.array([[np.sqrt(1-gam), 0], [0, 1]], dtype=complex)
    k4 = np.sqrt(gam*N)*np.array([[0, 0], [1, 0]], dtype=complex)
    return [k1, k2, k3, k4]

def apply(K, rho):
    return sum(k @ rho @ k.conj().T for k in K)

def vn_bits(rho):
    w = np.linalg.eigvalsh((rho+rho.conj().T)/2)
    w = w[w > 1e-15]
    return float(-(w*np.log2(w)).sum())

def check_channel_formula(gam, nu, trials=20, rng=np.random.default_rng(0)):
    K = kraus(gam, nu)
    err = 0
    for _ in range(trials):
        v = rng.normal(size=2)+1j*rng.normal(size=2); v /= np.linalg.norm(v)
        rho = np.outer(v, v.conj())
        q = rho[1, 1].real; z = rho[0, 1]
        t = (1-gam)*q + gam*nu
        pred = np.array([[1-t, np.sqrt(1-gam)*z], [np.sqrt(1-gam)*np.conj(z), t]])
        err = max(err, np.abs(apply(K, rho)-pred).max())
    return err

# ---------- brute-force one-shot Holevo information for a general qubit channel ----------
def bloch_state(th, ph):
    v = np.array([np.cos(th/2), np.exp(1j*ph)*np.sin(th/2)])
    return np.outer(v, v.conj())

def holevo_bruteforce(K, nstates=4, starts=30, rng=np.random.default_rng(1)):
    def negchi(x):
        th = x[:nstates]; ph = x[nstates:2*nstates]; w = np.exp(x[2*nstates:]); w /= w.sum()
        outs = [apply(K, bloch_state(th[i], ph[i])) for i in range(nstates)]
        avg = sum(w[i]*outs[i] for i in range(nstates))
        return -(vn_bits(avg) - sum(w[i]*vn_bits(outs[i]) for i in range(nstates)))
    best = 0.0
    for _ in range(starts):
        x0 = np.concatenate([rng.uniform(0, np.pi, nstates), rng.uniform(0, 2*np.pi, nstates), rng.normal(size=nstates)])
        r = minimize(negchi, x0, method='Nelder-Mead', options={'maxiter': 6000, 'xatol': 1e-9, 'fatol': 1e-12})
        best = max(best, -r.fun)
    return best

# ---------- KSW bounds ----------
def gb(x):  # bits
    if x <= 0: return 0.0
    return (1+x)*np.log2(1+x) - x*np.log2(x)

def C_beta(gam, N):
    return np.log2(1+np.sqrt(1-gam))

def C_cov(gam, N):
    eps = gam*abs(N-0.5)
    return exact_capacity(gam, 0.5)[0] + 2*eps + gb(eps)

def C_fil(gam, N):
    if N <= 0 or N >= 1:
        return np.inf
    f = gam*np.sqrt(N*(1-N)) + np.sqrt(N+(1-N)*(1-gam))*np.sqrt(1-N+N*(1-gam))
    arg = 0.5*(1-np.sqrt(1-gam)/f)
    # KSW Eq.149: 1 - h2(...) + log2 f + 1/2 log2(N/(1-N)); use symmetric form with N<=1/2 mapped via N->1-N
    val = 1 - h2(arg) + np.log2(f) + 0.5*abs(np.log2(N/(1-N)))
    return float(val)

def stinespring_iso(K):
    # V|psi> = sum_k K_k|psi> (x) |k>_E ; returns function giving (B, E) marginals
    def outputs(rho):
        dE = len(K)
        V = np.zeros((2*dE, 2), dtype=complex)
        for k, Kk in enumerate(K):
            for b in range(2):
                V[b*dE+k, :] = Kk[b, :]
        big = V @ rho @ V.conj().T
        big = big.reshape(2, dE, 2, dE)
        rB = np.einsum('ikjk->ij', big)
        rE = np.einsum('kikj->ij', big)
        return rB, rE
    return outputs

def C_EA(gam, N):
    K = kraus(gam, N); out = stinespring_iso(K)
    def negI(p):
        rho = np.diag([1-p, p]).astype(complex)
        rB, rE = out(rho)
        return -(vn_bits(rho) + vn_bits(rB) - vn_bits(rE))
    ps = np.linspace(0, 1, 401)
    vals = [-negI(p) for p in ps]
    i = int(np.argmax(vals))
    r = minimize_scalar(negI, bounds=(ps[max(i-1, 0)], ps[min(i+1, 400)]), method='bounded')
    return max(vals[i], -r.fun)

def choi(K):
    J = np.zeros((4, 4), dtype=complex)
    for i in range(2):
        for j in range(2):
            Eij = np.zeros((2, 2)); Eij[i, j] = 1
            J += np.kron(Eij, apply(K, Eij.astype(complex)))
    return J  # input (x) output, unnormalized (trace 2)

def eps_EB(gam, N):
    """(1/2)||A - M||_diamond minimised over EB qubit channels M (PPT Choi == separable for 2x2)."""
    import cvxpy as cp
    J = choi(kraus(gam, N))
    JM = cp.Variable((4, 4), hermitian=True)
    Z = cp.Variable((4, 4), hermitian=True)
    t = cp.Variable()
    def ptrace_out(X):  # trace over output (second factor)
        return cp.bmat([[X[0, 0]+X[1, 1], X[0, 2]+X[1, 3]], [X[2, 0]+X[3, 1], X[2, 2]+X[3, 3]]])
    def ptranspose_out(X):
        blocks = [[X[0:2, 0:2], X[0:2, 2:4]], [X[2:4, 0:2], X[2:4, 2:4]]]
        return cp.bmat([[blocks[0][0].T, blocks[0][1].T], [blocks[1][0].T, blocks[1][1].T]])
    cons = [JM >> 0, ptrace_out(JM) == np.eye(2), ptranspose_out(JM) >> 0,
            Z >> 0, Z - (J - JM) >> 0, t*np.eye(2) - ptrace_out(Z) >> 0]
    prob = cp.Problem(cp.Minimize(t), cons)
    prob.solve(solver='CLARABEL')
    JMv = JM.value
    # Kraus of M from its Choi matrix
    w, U = np.linalg.eigh((JMv+JMv.conj().T)/2)
    KM = []
    for k in range(4):
        if w[k] > 1e-12:
            vec = np.sqrt(w[k])*U[:, k]
            # J = sum |i><j| (x) M(|i><j|) ; vec in (in (x) out) -> Kraus K[out,in] = vec[in*2+out]
            KM.append(vec.reshape(2, 2).T)
    return float(prob.value), KM

def C_EB(gam, N):
    eps, KM = eps_EB(gam, N)
    chiM = holevo_bruteforce(KM, nstates=4, starts=12)
    return chiM + 2*eps + gb(eps), eps

# ---------- Fang 2026 U_G ----------
def fdet_bits(d):
    d = np.clip(d, 0, 0.25)
    return h2((1+np.sqrt(1-4*d))/2)

def fang_UG(gam, N, nq=801, nd=400):
    q = np.linspace(0, 1, nq)
    D = gam*((1-gam)*(q-N)**2 + N*(1-N))
    c = max(np.sqrt(1-gam) - gam*np.sqrt(N*(1-N)), 0.0)
    ell = np.empty(nq)
    for i, qi in enumerate(q):
        dmax = qi*(1-qi)
        dl = np.linspace(0, dmax, nd) if dmax > 0 else np.array([0.0])
        ell[i] = np.min(fdet_bits(D[i] + (1-gam)*dl) - fdet_bits(c**2*dl))
    # lower convex envelope of (q, ell)
    hull = []
    for i in range(nq):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (y2-y1)*(q[i]-x1) >= (ell[i]-y1)*(x2-x1):
                hull.pop()
            else:
                break
        hull.append((q[i], ell[i]))
    hx = np.array([p[0] for p in hull]); hy = np.array([p[1] for p in hull])
    gE = np.interp(q, hx, hy)
    root = np.sqrt((1-gam*(q+N))**2 + 4*gam*(1-gam)*q*N)
    pp = (1 + gam*(q-N) - root)/2; pm = (1 - gam*(q-N) - root)/2
    gB = h2(pp) + h2(pm) - fdet_bits(gam*q*(1-q))
    t = gam*N + (1-gam)*q
    return float(np.max(h2(t) - np.maximum(gE, gB)))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'grid'
    if mode == 'check':
        rows = []
        for gam, nu in [(0.1, 0.0), (0.3, 0.1), (0.5, 0.2), (0.7, 0.05), (0.9, 0.3), (0.6, 0.45)]:
            ce, p = exact_capacity(gam, nu)
            cb = holevo_bruteforce(kraus(gam, nu))
            rows.append((gam, nu, ce, cb, ce-cb, check_channel_formula(gam, nu)))
            print(f"gam={gam} nu={nu}: formula={ce:.6f} brute={cb:.6f} diff={ce-cb:+.2e} channel-formula-err={rows[-1][-1]:.1e}", flush=True)
    else:
        gams = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        Ns = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.45]
        out = []
        for N in Ns:
            for gam in gams:
                C, p = exact_capacity(gam, N)
                b = {'beta': C_beta(gam, N), 'cov': C_cov(gam, N), 'fil': C_fil(gam, N), 'EA': C_EA(gam, N)}
                eps, KM = eps_EB(gam, N)
                if 2*eps + gb(eps) < min(b.values()) - 1e-9:
                    b['EB'] = holevo_bruteforce(KM, nstates=4, starts=8) + 2*eps + gb(eps)
                ksw = min(b.values())
                ug = fang_UG(gam, N)
                row = dict(gamma=gam, N=N, C=C, p_opt=p, KSW_min=ksw, KSW_arg=min(b, key=b.get), eps_EB=eps,
                           gap_KSW=ksw-C, Fang_UG=ug, gap_Fang=ug-C, **{('ub_'+k): v for k, v in b.items()})
                out.append(row)
                print(f"N={N:.2f} g={gam:.1f} C={C:.4f} KSWmin={ksw:.4f}({row['KSW_arg']}) gapKSW={ksw-C:.4f} "
                      f"Fang={ug:.4f} gapFang={ug-C:.2e}", flush=True)
        json.dump(out, open('gad_grid.json', 'w'), indent=1)
