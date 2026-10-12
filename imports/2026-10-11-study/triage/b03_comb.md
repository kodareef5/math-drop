# b03_comb triage memo: Combinatorics, families 155–192

**Bottom line.** No T1. There are 2 × T2, 9 × T3 and 26 × T4. Almost everything is existence, a counterexample or an asymptotic bound. Where a result is constructive, its constants are galactic or not given. The useful actions are certification, benchmark instances and redirecting research, not faster code.

## Ranked opportunities

1. **179: No Barker code longer than 13 (T2, CERTIFY + FORMALIZE).** Yes. The circulant Hadamard theorem closes the even case; Turyn–Storer (1961) already closed the odd case. Binary Barker lengths are exactly {2,3,4,5,7,11,13}. The main theorem and the even Barker case are Lean-checked. Practice won't change: computation had excluded 13 < n ≤ 4·10³³ except one length, and designers use Barker-13, nested Barker, MPS-optimised or polyphase codes. Actions: upstream `exists_iff_order_one_or_four` to Mathlib, and update OEIS, Wikipedia and radar texts that still say "conjectured".
2. **187: Snaky in 21 moves (T2, INSTANCES).** The result has an exact, SHA-checked certificate on a 251-cell board, plus a Lean proof. Known-TRUE "Maker wins in ≤ m moves" instances would give QBFEVAL a graded hard family. Prior QBF work reached Snaky only on 5×5.
3. **165: Exact cr(K_n), cr(K_{m,n}) (T3, CERTIFY).** Lean-checked, with explicit optimal drawings. This gives ground truth for OEIS A000241 and for graph-drawing benchmarks (OGDF, KnownCR). It is not a VLSI or photonics lever: multilayer routing makes crossings free, rectilinear crossing number is still open, the old lower bound was already within 1.5%, and no heuristic ever beat Hill's drawing.
4. **180: Barnette (T3, RESEARCH/INSTANCES).** The existence proof is a nonzero signed sum over "state pairs", with a Pfaffian flavour. If the sum is computable by determinants, a polynomial-time Hamiltonian-cycle algorithm follows. Separately, plantri-generated cubic bipartite polyhedral graphs are now guaranteed YES instances.
5. **190: Ordered-matrix removal (T3, REDIRECT).** The pattern and host matrices are explicit and Lean-checked. Canonical row/column-sampling testers need exp(Ω(ε^-1/2)) samples, so property-testing work should drop polynomial testers for general 0/1 "image" patterns.
6. **158: χ(plane) ≥ 6 (T3).** A finite 6-chromatic unit-distance graph now provably exists, so SAT searches for it (Polymath16) can't be futile. Its size is unbounded.

## Channels checked and rejected

- **178 Ramanujan graphs (galactic).** Internal scales use n^{0.002a} with a = 10⁻⁴, so n₀ is astronomical. It gives no local neighbour oracle for derandomization. A random regular graph is already Ramanujan with probability ≈ 0.69, so NetworkX's sample-and-check `random_regular_expander_graph` already works. Worth taking: the exact rational test, positivity of Bᵀ(4(d−1)I − A²)B, as an exact mode for `is_regular_expander`.
- **177 coboundary expanders.** Vertex degree q^{C(2d+1,2)}, about 10³⁴. Good qLDPC codes and LTCs already exist by other routes. Theory value only.
- **174 thin trees.** The paper makes no new ATSP claim; O(1)-approximate ATSP was already known. The algorithm only does real work above a non-explicit cutoff R₀. LKH-3 and Concorde are unaffected.
- **183 k-sets.** ε is explicitly non-quantitative. Worst-case analyses improve; running times don't.
- **175, 176, 186 thresholds.** Constants 25·512⁴, 6144e⁵⁰ and 2¹⁹. The 2¹⁹ window bound is vacuous until n ≈ e⁶⁰⁰.
- **155–158 as benchmarks: no.** The 155 tile has no size bound. 156 is a continuum. 157's graphs have α ≤ 2, so colouring them is polynomial and trivial for solvers. 158's witness is not exhibited.

## Galactic or overhyped

- **160:** beats Berlekamp's bound only for k > 2^100000.
- **191:** η ≈ 4.4·10⁻⁵, so the gain n^η reaches 2 only for n > 2^22700.
- **174, 178:** "polynomial time" with unspecified exponents or cutoffs.
- **182:** the prime part depends on 003 (quasi-RH).

**Cross-links:**
- 179 ↔ 076 (binary merit factor)
- 178 ↔ 131, 219
- 174 ↔ 128
- 187 ↔ 189 (certificate-bearing proofs)
