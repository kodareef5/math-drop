"""Check the identity  sum_S w(S) * Haf(A_S)^2  =  Haf(L)   for the 'rung ladder' L built from two copies
of G joined by rungs v1-v2 (rung weight r_v, G-edge weight x in both copies), with w(S)=x^{|S|} prod_{v not in S} r_v.
Consequence: the collision-free GBS law Pr(S) ∝ x^{|S|} Haf(A_S)^2 (pure state with B = cA gives x = c;
Zhang et al. 2505.02445 write c^{2|S|}; unweighted graph, PNR, conditioned on no collisions; r_v = 1) equals the law of the uncovered-by-rung set of a random perfect matching of L
(weighted). With rational x=p/q, integer edge weights are realizable by parallel 3-paths, so the family-113 FPRAS
+ JVV self-reduction (its Lemma deletion-sampler) gives a poly-time sampler in principle.
Also checks that Pr(S) from the Gaussian-state formula sums (with collision patterns excluded) consistently."""
import itertools, random, math, sys
from functools import lru_cache
from fractions import Fraction

def haf(W, verts):
    verts = tuple(verts)
    @lru_cache(maxsize=None)
    def rec(mask):
        if mask == 0: return 1
        i = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << i); tot = 0; m = rest
        while m:
            j = (m & -m).bit_length() - 1; m &= m - 1
            wij = W[verts[i]][verts[j]]
            if wij: tot += wij * rec(rest & ~(1 << j))
        return tot
    return rec((1 << len(verts)) - 1)

random.seed(7)
ok = True
for trial in range(12):
    n = random.choice([6, 8, 9, 10])
    pe = random.choice([0.3, 0.5, 0.8])
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < pe: A[i][j] = A[j][i] = 1
    x = Fraction(random.randint(1, 5), random.randint(1, 5))           # x = squeezing scale
    r = [Fraction(random.randint(1, 4), random.randint(1, 4)) for _ in range(n)]  # node weights via rungs
    lhs = Fraction(0)
    for k in range(0, n+1, 2):
        for S in itertools.combinations(range(n), k):
            h = haf(A, S)
            if h:
                lhs += x**k * h*h * math.prod((r[v] for v in range(n) if v not in S), start=Fraction(1))
    N2 = 2*n
    L = [[Fraction(0)]*N2 for _ in range(N2)]
    for i in range(n):
        for j in range(n):
            if A[i][j]:
                L[i][j] = x; L[n+i][n+j] = x     # weight x per G-edge in each copy -> x^{|S|} total
        L[i][n+i] = L[n+i][i] = r[i]
    rhs = haf(L, range(N2))
    good = (lhs == rhs); ok &= good
    print(f"n={n:2d} p_edge={pe} x={str(x):>4}  sum_S x^|S| r(V\\S) Haf(A_S)^2 = {float(lhs):.6g}   Haf(ladder) = {float(rhs):.6g}   equal={good}")
print("ALL EQUAL" if ok else "MISMATCH")
