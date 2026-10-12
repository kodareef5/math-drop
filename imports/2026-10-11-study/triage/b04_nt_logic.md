# b04: Number theory 001–031 and logic 240–245, triage memo

**Bottom line:** 28 of 37 families are T4, and none is T1. No PARI, FLINT, OpenSSL or GMP code gets faster or newly correct. The value is removing "assuming GRH / Artin / modularity / BSD" caveats from textbooks and databases.

## Ranked opportunities

1. **003 Quasi-RH (T2 CERTIFY).** The 7/8 half-plane and the Landau–Siegel gap are Lean-formalized (standard axioms). Corollary: n(p) ≤ C(log p)^A (A=32 via BIMS). So deterministic Tonelli–Shanks / square roots mod p and Miller's test become unconditional polynomial time; also effective h(D) ≫ √|D|/loglog|D|.
   - **Galactic.** (log p)^16–32 is 10^46–10^91 at 1024 bits. It beats Burgess only above about 1000–2200 bits, and C is never computed. OpenSSL `BN_mod_sqrt` stops after about 80 tries.
   - **Key negative:** the GRH dependence in PARI `bnfinit`/`quadclassunit`, Magma `ClassGroup` with `Proof:="GRH"`, Sage `proof=False`, Buchmann's algorithm and CSI-FiSh/CSIDH concerns Hecke L-functions of the field. 003 covers Dirichlet L-functions and Q(√−3) only, so those caveats stay.
2. **002 Full BSD for Selmer corank ≤ 1 (T2, deep dive).** This is the most practically certifiable result here. For all rank-0/1 curves (most of Cremona/LMFDB), the analytic order of Sha becomes the proven order, and Sage `prove_BSD()` could return `[]`. It is an extraordinary claim in three unformalized manuscripts, so hold any change until expert review.
3. **029 Artin, infinitude part (T2).** Coding-theory existence results stated "under Artin's conjecture" (quasi-cyclic, double-circulant codes) become unconditional where only infinitely many primes are needed. Density-dependent results stay open, because x/log²x is density zero. BIKE/HQC parameters never needed the conjecture.
   - **Non-obvious channel:** its uniform strip Re s > 1−10⁻⁶ for Hecke L-functions of cyclotomic fields transfers by Artin factorization to every abelian field, including class-group characters of quadratic fields. That would be the first unconditional, effective Bach-type bound. The exponent is about 10⁶, so it is galactic, like 142's O(n^{10^12}) factorization. Deep dive to document, not to implement.
4. **030 Modularity over imaginary quadratic fields (T2).** LMFDB states completeness of its imaginary-quadratic elliptic-curve tables only "assuming modularity". This would remove the caveat (single unformalized paper).
5. **243 CPT ≠ PTIME (T3 INSTANCES).** Explicit F₃-linear-consistency structure pairs defeat choiceless symmetric computation. They are candidate hard instances beyond CFI graphs for GNN-expressivity benchmarks such as BREC.
6. **004 H10 over Q (T3 REDIRECT).** Via Sturmfels's equivalence this makes rational matroid realizability undecidable, which affects OSCAR `is_realizable`. Exact tensor rank over Q is likely undecidable via Shitov; check the reduction. The SMT impact is thin: real nonlinear arithmetic (QF_NRA) is untouched and integer nonlinear arithmetic was already undecidable.

## Checked and rejected

- **021 Jacobsthal:** C is not explicit and exact values are tabulated for k ≤ 43–50. OpenSSL `probable_prime` and `mpz_nextprime` depend on prime gaps and restart when the step bound is exceeded.
- **011/012 smoothness laws:** asymptotic only, with no error term at 2^256. They support Pollard p−1 and twin-smooth heuristics only in the limit (T3, practicality 1).
- **017 π exponent:** the threshold is ineffective, so it is useless for libm argument reduction.
- **015 torus packets:** totally real fields with no rate; not the cyclotomic setting lattice crypto uses.
- **245 WN ⇒ SN:** β-only pure type systems. The Rocq, Lean and Agda kernels are not PTSs, so this is research at most.
- **242 single-fold:** the polynomial is not explicit.

## Overhyped

- **"Square roots and factoring without GRH" (003, and 142 via 029):** clean theory, numerically useless.
- **"No Siegel zeros":** the constant c is non-explicit (proof by contradiction). The effective h(D) bound comes from the 7/8 half-plane and its constant is still uncomputed.
