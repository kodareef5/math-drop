"""Emit QDIMACS for 'Maker (to move) completes a Snaky copy within h Maker moves' on the
finite board T of a certificate card (A,T,h) from the OpenAI Snaky-in-21 certificate.
Card semantics (templates.tex Def. valid claim): if Maker owns A and Breaker owns nothing in T,
Maker wins within h moves. Maker's certified strategy only plays inside T and every target used
lies inside T, so restricting both players to T (Breaker moves outside T are passes for Maker's
purposes; extra Breaker stones never help Maker) yields a TRUE finite instance.
Encoding: binary move indices; out-of-range index or an occupied cell = pass (dominated move,
does not change the game value by monotonicity of Maker-Breaker games). Ownership gates:
  MO_t(c) = MO_{t-1}(c) | (m_t(c) & ~BO_{t-1}(c)),  BO_t(c) = BO_{t-1}(c) | (b_t(c) & ~MO_t(c)).
Win = OR over Snaky copies W inside T of AND_{c in W} MO_h(c).  Prefix: e M1 a B1 e M2 ... e Mh e gates."""
import sys, math, itertools
symbols = '0123456789ABCDEFG'
SNAKE = [(0,0),(1,0),(2,0),(3,0),(3,1),(4,1)]
def load_cards(path):
    TT = [set(SNAKE) for _ in SNAKE]; AA = [t - {p} for t, p in zip(TT, SNAKE)]; HH = [1]*6
    def point(x): return tuple(symbols.index(c) for c in x)
    def reference(tok):
        parts = tok.split(':'); j = int(parts[0])
        if len(parts) == 1: s = dx = dy = 0
        else: s = int(parts[1][0]); dx, dy = point(parts[1][1:])
        def put(P):
            Q = set()
            for x, y in P:
                if s & 2: x = -x
                if s & 4: y = -y
                if s & 1: x, y = y, x
                Q.add((x + dx, y + dy))
            return Q
        return put(AA[j]), put(TT[j]), HH[j]
    def expr(it):
        p = point(next(it)); aa, tt, hh = [], [], []
        while True:
            w = next(it)
            if w == ')': break
            a, t, h = expr(it) if w == '(' else reference(w)
            aa.append(a); tt.append(t); hh.append(h)
        return ((set.union(*aa) | set.intersection(*tt)) - {p}, set.union({p}, *tt), 1 + max(hh))
    for line in open(path).read().strip().splitlines():
        words = line.replace('(', ' ( ').replace(')', ' ) ').split(); it = iter(words + [')']); next(it)
        a, t, h = expr(it); AA.append(a); TT.append(t); HH.append(h)
    return AA, TT, HH
def copies(T):
    out = set()
    for s in range(8):
        P = []
        for x, y in SNAKE:
            if s & 2: x = -x
            if s & 4: y = -y
            if s & 1: x, y = y, x
            P.append((x, y))
        for (cx, cy) in T:
            for (px, py) in P:
                dx, dy = cx - px, cy - py
                W = frozenset((x + dx, y + dy) for x, y in P)
                if W <= T: out.add(W)
    return out
class Enc:
    def __init__(s): s.nv = 0; s.cl = []
    def var(s): s.nv += 1; return s.nv
    def AND(s, lits):
        if not lits: return s.TRUE
        if len(lits) == 1: return lits[0]
        g = s.var()
        for l in lits: s.cl.append([-g, l])
        s.cl.append([g] + [-l for l in lits]); return g
    def OR(s, lits):
        if not lits: return -s.TRUE
        if len(lits) == 1: return lits[0]
        g = s.var()
        for l in lits: s.cl.append([g, -l])
        s.cl.append([-g] + list(lits)); return g
def encode(A, T, h, out):
    F = sorted(T - A)              # free cells
    W = [w for w in copies(T)]
    nb = max(1, math.ceil(math.log2(len(F))))
    e = Enc(); blocks = []
    mbits, bbits = [], []
    for t in range(h):
        mb = [e.var() for _ in range(nb)]; mbits.append(mb); blocks.append(('e', mb))
        if t < h - 1:
            bb = [e.var() for _ in range(nb)]; bbits.append(bb); blocks.append(('a', bb))
    first_gate = e.nv + 1
    e.TRUE = e.var(); e.cl.append([e.TRUE])
    def dec(bits, i):
        return e.AND([bits[k] if (i >> k) & 1 else -bits[k] for k in range(nb)])
    MO = {c: (e.TRUE if c in A else -e.TRUE) for c in T}
    BO = {c: -e.TRUE for c in T}
    for t in range(h):
        for i, c in enumerate(F):
            mt = dec(mbits[t], i)
            MO[c] = e.OR([MO[c], e.AND([mt, -BO[c]])])
        if t < h - 1:
            for i, c in enumerate(F):
                bt = dec(bbits[t], i)
                BO[c] = e.OR([BO[c], e.AND([bt, -MO[c]])])
    win = e.OR([e.AND([MO[c] for c in w]) for w in W])
    e.cl.append([win])
    with open(out, 'w') as f:
        f.write(f"c Snaky Maker-Breaker: |A|={len(A)} |T|={len(T)} free={len(F)} h={h} copies={len(W)}\n")
        f.write(f"p cnf {e.nv} {len(e.cl)}\n")
        for q, vs in blocks: f.write(q + ' ' + ' '.join(map(str, vs)) + ' 0\n')
        f.write('e ' + ' '.join(map(str, range(first_gate, e.nv + 1))) + ' 0\n')
        for c in e.cl: f.write(' '.join(map(str, c)) + ' 0\n')
    return len(F), len(W), e.nv, len(e.cl)
if __name__ == '__main__':
    cert = '/root/openai-math/preprints/Snaky-in-21-Maker-moves-September-25-2026/verification/certificate.txt'
    AA, TT, HH = load_cards(cert)
    import json
    sel = json.loads(sys.argv[1]) if len(sys.argv) > 1 else None
    print(len(AA), 'cards loaded')
