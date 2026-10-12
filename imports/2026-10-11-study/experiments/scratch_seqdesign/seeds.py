"""Seed generators for the LABS experiment (theme seqdesign, family 076).

Families:
  random    : uniform +/-1 sequences
  legendre  : rotated + periodically appended Legendre sequences (Jedwab-Katz-Schmidt family);
              best-F candidates over primes p in [N/1.15, N] and all rotations
  pipeline  : finite analogue of the 076 pipeline: a relaxed real-valued quadratic-phase
              waveform X in [-1,1]^N (Prop. almost-signs with F = cos on T^1, H blocks with a
              packed set of chirp intervals) followed by sequential "defect-aware" rounding to
              signs that greedily minimises the L4 norm of the partially rounded polynomial.
  pipe_sign : same relaxed waveform, naive rounding eps_k = sign(X_k) (hard-limited chirp)
Usage: python3 -I seeds.py FAMILY N K rngseed out.txt
"""
import sys
import numpy as np


def merit(s):
    s = np.asarray(s, dtype=float)
    N = len(s)
    M = 1 << int(np.ceil(np.log2(2 * N)))
    S = np.fft.rfft(s, M)
    c = np.fft.irfft(np.abs(S) ** 2, M)[1:N]
    return N * N / (2.0 * np.sum(np.round(c) ** 2))


def merit_batch(A):
    """A: (B, N) array of +/-1 rows."""
    B, N = A.shape
    M = 1 << int(np.ceil(np.log2(2 * N)))
    S = np.fft.rfft(A, M, axis=1)
    c = np.fft.irfft(np.abs(S) ** 2, M, axis=1)[:, 1:N]
    return N * N / (2.0 * np.sum(np.round(c) ** 2, axis=1))


def primes_upto(n):
    sv = np.ones(n + 1, bool)
    sv[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sv[i]:
            sv[i * i::i] = False
    return np.nonzero(sv)[0]


def legendre_seq(p):
    q = np.zeros(p, int)
    q[(np.arange(1, p) ** 2) % p] = 1
    s = np.where(q == 1, 1, -1)
    s[0] = 1
    return s


def legendre_candidates(N, K, nprimes=6, batch=256):
    """Appended rotated Legendre sequences (Jedwab-Katz-Schmidt): for the nprimes primes p
    closest to N/1.058 (p <= N), take all p rotations of the Legendre sequence of length p,
    periodically extended to length N; return the K best by merit factor."""
    ps = [int(p) for p in primes_upto(N) if p >= 3]
    ps.sort(key=lambda p: abs(p - N / 1.058))
    out = []
    for p in ps[:nprimes]:
        L = legendre_seq(p)
        for r0 in range(0, p, batch):
            rs = np.arange(r0, min(p, r0 + batch))
            idx = (np.arange(N)[None, :] + rs[:, None]) % p
            A = L[idx]
            F = merit_batch(A)
            for j in np.argsort(-F)[:K]:
                out.append((F[j], p, int(rs[j]), A[j].copy()))
        out.sort(key=lambda x: -x[0])
        out = out[:K]
    return out


def relaxed_chirp(N, H, perm, v=0.5, phi=0.0, taper=0.0):
    """Prop. almost-signs with F(y)=cos(2 pi y): A={+1,-1}, c=1/2, lambda=+-v.
    Block h covers [(h-1)/H, h/H); its chirp has centre theta_h and sweeps an interval of
    width v/H. With v=1/2 the H positive intervals tile [0,1/2] and their reflections tile
    [1/2,1], i.e. the signed-interval packing of Lemma signed-packing is exact."""
    k = np.arange(N)
    x = k / N
    h = np.minimum((x * H).astype(int), H - 1)
    xs = (h + 0.5) / H
    centres = (np.arange(H) + 0.5) / (2 * H) * (2 * v)  # tile [0, v]
    theta = centres[np.asarray(perm)[h]]
    ph = k * theta + 0.5 * N * v * (x - xs) ** 2 + phi
    X = np.cos(2 * np.pi * ph)
    if taper > 0:
        u = (x * H) - h  # position within block in [0,1)
        w = np.clip(np.minimum(u, 1 - u) / taper, 0, 1)
        X = X * (0.5 - 0.5 * np.cos(np.pi * w))
    return X


def greedy_l4_round(X, order=None):
    N = len(X)
    M = 1 << int(np.ceil(np.log2(4 * N)))
    t = np.arange(M) / M
    G = np.fft.fft(X, M).conj()  # G(t) = sum X_j e(j t) on the grid (conj of numpy's e(-jt))
    eps = np.empty(N)
    if order is None:
        order = range(N)
    w = np.exp(2j * np.pi * t)
    ek = np.ones(M, complex)
    seq = list(order)
    sequential = all(int(a) == i for i, a in enumerate(seq))
    for k in seq:
        if sequential:
            if k > 0:
                ek = ek * w
        else:
            ek = np.exp(2j * np.pi * k * t)
        Gp = G + (1 - X[k]) * ek
        Gm = G + (-1 - X[k]) * ek
        if np.sum(np.abs(Gp) ** 4) <= np.sum(np.abs(Gm) ** 4):
            G = Gp
            eps[k] = 1
        else:
            G = Gm
            eps[k] = -1
    return eps.astype(int)


def pipeline_candidates(N, K, rng, rounding="greedy"):
    out = []
    Hs = [1, 2, 3, 4, 6, 8]
    tries = 0
    target = 3 * K if N < 2000 else K
    while len(out) < target and tries < 6 * K:
        tries += 1
        H = Hs[tries % len(Hs)]
        perm = rng.permutation(H) if H > 1 else [0]
        v = rng.uniform(0.44, 0.5)
        phi = rng.uniform(0, 1)
        X = relaxed_chirp(N, H, perm, v=v, phi=phi)
        if rounding == "greedy":
            order = np.arange(N) if (N >= 2000 or rng.random() < 0.5) else rng.permutation(N)
            s = greedy_l4_round(X, order)
        else:
            s = np.where(X >= 0, 1, -1)
        out.append((merit(s), H, float(v), s))
    out.sort(key=lambda x: -x[0])
    return out[:K]


def to_str(s):
    return "".join("+" if v > 0 else "-" for v in s)


if __name__ == "__main__":
    fam, N, K, seed, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = np.random.default_rng(seed)
    if fam == "random":
        cands = [(None, rng.choice([-1, 1], N)) for _ in range(K)]
        seqs = [c[1] for c in cands]
    elif fam == "legendre":
        cands = legendre_candidates(N, K)
        seqs = [c[3] for c in cands]
    elif fam == "pipeline":
        cands = pipeline_candidates(N, K, rng, "greedy")
        seqs = [c[3] for c in cands]
    elif fam == "pipe_sign":
        cands = pipeline_candidates(N, K, rng, "sign")
        seqs = [c[3] for c in cands]
    else:
        raise SystemExit("unknown family")
    Fs = [merit(s) for s in seqs]
    with open(outp, "w") as f:
        for s in seqs:
            f.write(to_str(s) + "\n")
    print(f"{fam} N={N} K={len(seqs)} seedF_max={max(Fs):.4f} seedF_mean={np.mean(Fs):.4f}")
