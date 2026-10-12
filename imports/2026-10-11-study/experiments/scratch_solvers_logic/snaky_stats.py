import sys, collections, time
sys.path.insert(0, '.')
import snaky_verify_copy as V
src = open('/root/openai-math/preprints/Snaky-in-21-Maker-moves-September-25-2026/verification/certificate.txt').read()
t = time.time()
# re-run verify but capture AA, TT, HH by monkeypatching: copy of verify logic
symbols = '0123456789ABCDEFG'
snake = [(0,0),(1,0),(2,0),(3,0),(3,1),(4,1)]
TT = [set(snake) for _ in snake]; AA = [t_ - {p} for t_, p in zip(TT, snake)]; HH = [1]*6
def point(x): return tuple(symbols.index(c) for c in x)
def reference(token):
    parts = token.split(':'); j = int(parts[0])
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
        a, t_, h = expr(it) if w == '(' else reference(w)
        aa.append(a); tt.append(t_); hh.append(h)
    return ((set.union(*aa) | set.intersection(*tt)) - {p}, set.union({p}, *tt), 1 + max(hh))
for line in src.strip().splitlines():
    words = line.replace('(', ' ( ').replace(')', ' ) ').split(); it = iter(words + [')']); next(it)
    a, t_, h = expr(it); AA.append(a); TT.append(t_); HH.append(h)
V.verify(src)
print('verified in', round(time.time()-t, 2), 's')
byh = collections.defaultdict(list)
for a, t_, h in zip(AA, TT, HH): byh[h].append((len(a), len(t_)))
print('h  #cards  |A| range   |T| range   (smallest |T| - |A| free cells)')
for h in sorted(byh):
    L = byh[h]
    print(h, len(L), (min(x[0] for x in L), max(x[0] for x in L)), (min(x[1] for x in L), max(x[1] for x in L)), min(x[1]-x[0] for x in L))
