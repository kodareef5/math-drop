# b10_alg_group: algebra (193–210) and group theory (246–259), 32 families

**Bottom line:** 28 T4, 3 T3, 1 T2, no T1. This is a deeply foundational batch: the explicit objects are random, astronomically large, or defined via Busy Beaver constants.

## Ranked opportunities

1. **254 Artin groups (T2, CAS/ALGO, CERTIFY, deep dive).**
   - *Software touchpoint.* The K(π,1) theorem is Lean-formalized (the OAI ArtinGroups tree has no `sorry`). GAP HAP's `ResolutionArtin(D)` is documented as valid only "in those cases where the conjecture is known to hold". SageMath's `sage.groups.artin` still lists torsion-freeness, the center, word problem and K(π,1) as conjectures. All of these become theorems.
   - *Non-obvious find.* Cor. `cor:membership` gives the first uniform algorithm for the word problem and parabolic membership in every finite-rank Artin group: exact Gaussian elimination over a Temperley–Lieb–Jones fusion algebra over Q(ζ_N).
   - *Limits.* No complexity bound, and likely exponential. Garside, Holt–Rees and the A3/B3-free algorithms stay faster where they apply. The gain is decidability for non-FC diagrams, which currently fall to generic fp-group methods. Braid crypto (spherical type) gains nothing.

2. **204 Spin(2n) saturation (T3, ALGO).**
   - *Unstated consequence.* With saturation factor 1, type-D tensor-multiplicity positivity reduces to Berenstein–Zelevinsky polytope LP feasibility, so it is in P.
   - *Why new.* GCT3 said its argument "does not generalize" to types B, C, D.
   - *Limits.* Small audience (LiE, Sage `WeylCharacterRing`), and it decides positivity only.

3. **200 EGH / lex-plus-powers (T3, CAS).**
   - *What it gives.* A characteristic-0 realizability criterion for Hilbert functions of ideals containing a regular sequence, plus a priori Betti bounds.
   - *Software touchpoint.* Macaulay2 `LexIdeals` (`LPP`, `isLPP`, `generateLPPs`) still says "conjectured", so this is a documentation note.
   - *Coding channel rejected.* Complete-intersection evaluation-code bounds need F_q; the proof is characteristic 0 only.

4. **258 Gersten dichotomy (T3, weak).** A two-sided search (kbmag/walrus versus Baumslag–Solitar witnesses) might decide one-relator hyperbolicity and settle Cashen–Hoffmann census entries. This is my inference; the paper is unformalized and about 760 KB.

## Requested channels rejected

- **Test instances (196, 197, 247, 253).** Presentations are unusable: 2^{10000h} alphabets (247), unbounded sizes (253), 16,516 letters with about 5×10^8 vertices (196). 197 is "not executed" and its odd-characteristic field is built from (C(1200,600)!)²+1. None can stress-test ACE, kbmag or SAT searches.
- **248 Thompson F.** Clean and Lean-formalized, but F-based crypto was already broken. It confirms the cogrowth extrapolation (≈15 < 16) and gives no explicit spectral gap.
- **255, 256.** Not algorithmic. 256 gives solutions only in an unspecified overgroup.
- **205 Saxl, 210 Foulkes.** Positivity results, while GCT needs vanishing, which Bürgisser–Ikenmeyer–Panova already ruled out. 210 answers Landsberg's Problem 7.19 but gives no lower bound. The quantum marginal problem is unaffected.
- **206 lattice undecidability.** No complete decider exists, but small lattices stay representable, so UACalc-style searches are unaffected.
- **193, 194, 195, 199.** No Macaulay2, Singular or QPA computation depends on them. 199 is explicit but needs transcendental parameters.
- **252.** Being nonlinear helps crypto only in principle; the group is not explicit.

## Overhyped, galactic or caution

- **Galactic or existential-only:** 196, 197, 247, 250, 253, 257. 206's minimal lattice is defined via Busy Beaver.
- **Extraordinary and unformalized:** 202 proves Alperin's weight conjecture without the classification of finite simple groups. 203 (Donovan) depends on 202.
- **No withdrawal dependencies found.**
