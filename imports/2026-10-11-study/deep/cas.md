# Computer algebra: Artin groups (K(π,1), word problem), EGH/lex-plus-powers, type-D saturation, noncommutative identity testing, explicit counterexamples

Families covered: 254, 200, 204, 116, 047, 049, 196, 197, 201, 248, 255.

Pinned versions:
- **Paper sources:** openai/math commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- **Code targets:**
  - GAP HAP `415d3655c99f1e0aa95e042b20b80b8eb404b4e1` (HAP 1.79, 2026-10-05)
  - SageMath `0835358cba62dc19fccdff54f32e52fded9f22b0` (2026-10-11)
  - Macaulay2 `stable` `1a37f6fe95badb1e5f99707a485503d213fd9d49`. The text cited is identical on `development` `84e5bd65`.
  - NCAlgebra `4156ae48f9540dc1547b8a42df4ac89cce15d814`
  - Singular `4d253ff427cae6718de42b81149e3c3953f8e866`
- **Experiment code:** `/home/claude/work/repos/scratch_cas/`.
- **Software used:** passagemath 10.8.12 (pip-installed SageMath), Macaulay2 1.22, GAP 4 with HAP 1.62 (Ubuntu packages).

**Bottom line**
- **Pursue now:** two small documentation changes, both resting on the Lean-formalized Artin K(π,1) theorem (254).
  - GAP HAP's `ResolutionArtinGroup` pages and SageMath's `ArtinGroup` docstring still call K(π,1), torsion-freeness, the center and the word problem conjectural "except in known cases".
  - A one-paragraph change, with hedged citation, makes HAP's integral-homology output an unconditional Artin-group invariant for every finite-rank diagram.
  - A separate cleanup can be done regardless of the preprint: HAP has stale wording ("depends on K(π,1) for spherical type" is Deligne 1972) and names a non-existent `ResolutionArtin`.
- **Worth a small Sage contribution: the uniform word-problem algorithm (Cor. cor:membership) is implementable.**
  - I built a ~200-line prototype for labels in {2,3,∞} and validated it. It agrees with Sage's Garside normal form on 300/300 braid-group words, recognises 200/200 relator-insertion identities across six non-spherical groups, and never contradicts the generalized Burau representation.
  - Sage's generic `ArtinGroup ==` today does not terminate even on the defining relation of affine Ã₂.
  - The catch: complex size grows exponentially with word length outside spherical/affine type (×≈5.9 per Coxeter-element power for diagram (3,3,∞)). It is therefore a terminating fallback. It does not replace the polynomial algorithms for spherical, large and no-A₃/B₃ type.
- **Monitor or do not pursue:**
  - The Macaulay2 LexIdeals doc change (200): its claim is char 0 only and unformalized, so wait for refereeing.
  - LP positivity for type D (204): real, but niche, and no implementation of the needed type-D polytope inequalities exists.
  - Deterministic noncommutative identity testing (116): infeasible beyond formula size ≈25, and no real software works black-box.
  - 196/197/201/248/255: no computational channel at all.
  - 047/049: tiny explicit polynomials, but only their easy half is machine-checkable.

## What the papers actually prove

### 254 — Artin groups (3 manuscripts; all of the top lines are Lean-formalized)

**K(π,1) theorem** ([Thm 1.1 (thm:main), introduction.tex L22-30](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Harmonic-heights-and-the-Artin-K-pi-1-conjecture-September-23-2026/build/sections/introduction.tex#L22-L30)):
- For every Coxeter matrix on a finite set, the universal cover of the standard Salvetti complex is contractible.
- Scope: arbitrary finite labels, ∞ labels, and disconnected diagrams. Infinite-rank diagrams are excluded.
- Lean: `OAI.HarmonicArtin.salvetti_cover_contractible` ([comparator statement L57-61](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/HarmonicArtin.lean#L57-L61)). Only the axioms propext, Quot.sound and Classical.choice are allowed, and none of the 881 Artin Lean files contains `sorry`.

**Corollaries** (Cor. cor:artin-structural, [consequences.tex L23-37](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Harmonic-heights-and-the-Artin-K-pi-1-conjecture-September-23-2026/build/sections/consequences.tex#L23-L37)). These are not in Lean; the Lean doc says "later corollaries … are not included".
- A is torsion-free (short argument from the finite K(π,1)).
- Z(A) ≅ ℤᵏ, where k is the number of irreducible *spherical* components. This uses Jankiewicz–Schreve, which assumes K(π,1).
- BA⁺ ≃ BA, via Dobrinskaya and Ozornova.
- Boyd homological stability for braid-tail families.

**Parabolic intersections** ([Thm thm:main, Cor. cor:arbitrary-intersections, 01_intro.tex L21-48](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Parabolic-intersections-in-Artin-groups-September-23-2026/build/sections/01_intro.tex#L21-L48)):
- For every finite-rank Artin group, the intersection of two parabolics is parabolic. Any family's intersection is already the intersection of at most |S| members, and every subset has a parabolic closure.
- Lean ([comparator L96-129](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/ArtinParabolicIntersections.lean#L96-L129)) covers four statements: pairwise, arbitrary, closure, and acylindrical hyperbolicity / weak malnormality in the non-clique case.
- The proof does not use the K(π,1) theorem.

**Word and parabolic-membership problems** ([Cor. cor:membership, 01_intro.tex L59-66](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Parabolic-intersections-in-Artin-groups-September-23-2026/build/sections/01_intro.tex#L59-L66); algorithm in [08_stabilizers.tex §sec:algorithms L221-311](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Parabolic-intersections-in-Artin-groups-September-23-2026/build/sections/08_stabilizers.tex#L221-L311)). This part is **NOT in Lean**.

*How the algorithm works:*
- **Input.** Enlarge S by a frame colour f, which commutes with X and has label 3 to S∖X.
- **Algebra.** Build a finite graded zigzag-type algebra Z over K = ℚ(e^{2πi/N}), where N = lcm{2m : finite labels m ≥ 4}, or K = ℚ when no such label exists.
  - Labels ≥ 4 use a Temperley–Lieb–Jones fusion factor per edge (simples F₀…F_{m−2}).
  - Label 3 contributes a single arrow pair; ∞ contributes 1⊕1, i.e. two arrow pairs ([02_category.tex L130-170](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Parabolic-intersections-in-Artin-groups-September-23-2026/build/sections/02_category.tex#L130-L170)).
- **Action.** Generators act by the evaluation cones B_i = Cone(⊕P_α⊗e_αE → E) ([Prop cat:action, L392-427](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Parabolic-intersections-in-Artin-groups-September-23-2026/build/sections/02_category.tex#L392-L427)).
- **Test.** Compute B_w P_{f,𝟏}, cancel invertible scalar differential entries by Gaussian elimination, and test whether the minimal complex is P_{f,𝟏} in placement (0,0).

*Status:* constructive, exact arithmetic, terminating. **The paper asserts no complexity bound.** The intro also notes that parabolic membership was already decidable *given* any word-problem solution, by Charney–Paris convexity plus brute force.

**CAT(0) counterexample:** an explicit Artin matrix on 116 generators with labels in {2,3,∞} admits no geometric CAT(0) action ([Def def:matrix, assembly.tex L10-37](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-Artin-group-with-no-geometric-CAT-0-action-September-23-2026/build/sections/assembly.tex#L10-L37)). It is Lean-formalized and has no computational consequence.

**Triage check:** correct. One refinement: the algebra in the word-problem algorithm needs Temperley–Lieb fusion only when some label is ≥ 4. For labels in {2,3,∞} it is an ordinary zigzag algebra over ℚ, which is what made a quick prototype possible.

### 200 — Eisenbud–Green–Harris (EGH) / lex-plus-powers (LPP), 2 manuscripts, NOT formalized

**Main theorem** ([Thm thm:main L41-53](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/build/sections/01-introduction.tex#L41-L53)):
- **Hypotheses.** Work over ℂ with degrees 2 ≤ a₁ ≤ … ≤ aₙ. Let I contain a homogeneous regular sequence of degrees aᵢ.
- **Conclusion.** The LPP prescription J has the same Hilbert function as I and β_{p,j}(S/J) ≥ β_{p,j}(S/I) for all p, j.

**Char-0 corollary** ([Cor cor:characteristic-zero L68-94](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/build/sections/01-introduction.tex#L68-L94)):
- Extends to any char-0 field and to regular sequences of any length c ≤ n, including non-Artinian quotients.
- Uses the Caviglia–Maclagan and Caviglia–Kummini reductions.

**Constructive?** The extremal object J is explicit; the proof is existential (a division algebra over a finitely generated extension of ℂ). **Positive characteristic stays open.**

### 204 — tensor saturation for Spin(2n), NOT formalized

**Theorem** ([Thm thm:main L33-42](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Tensor-Saturation-for-Even-Spin-Groups-September-24-2026/build/sections/01-introduction.tex#L33-L42)): let λ, μ, ν be dominant with λ+μ+ν ∈ Q(Dₙ). If (V(Nλ)⊗V(Nμ)⊗V(Nν))^G ≠ 0 for some N ≥ 1, then the invariant already exists at N = 1.

**Algorithmic consequence (not stated in the paper):**
1. Check that λ+μ+ν lies in the root lattice.
2. Test feasibility of any rational polytope whose lattice points count the multiplicity and which dilates with the weights, for example the Berenstein–Zelevinsky (BZ) polytope.

Together these decide type-D tensor positivity. This is exactly the GCT3 template, which was conditional for B, C, D (see below); type D becomes unconditional.

### 116 — matrix hitting points for noncommutative (NC) formulas

**Char 0** ([Thm thm:main L24-42](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/introduction.tex#L24-L42)):
- The hitting tuple T_{n,s} ∈ Mat_d(ℚ)ⁿ, with d = 2ns², detects every nonzero NC formula of size ≤ s in n variables.
- The matrices are explicit ([eq:explicit-matrices](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/construction.tex#L14-L31)): T_i is the operator a(z) ↦ ∫₀ᶻ a(t)/(t+i) dt on ℚ[[z]]/(zᵈ).
- Entries have up to ≈ d·log₂(n+1) bits.

**Char p version** ([Thm L26-44](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-Matrix-Hitting-Points-in-Every-Positive-Characteristic-October-4-2026/build/sections/introduction.tex#L26-L44)): d = O(n³s⁶), with unspecified absolute constants C, k.

**Rational formulas** ([Thm L20-24](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026/build/sections/introduction.tex#L20-L24)): a polynomial-size hitting *list*, with exponent unspecified.

**Lean:** the hitting properties are formalized; the size/bit bounds are not.

### 047 / 049 — explicit affine-geometry counterexamples (Lean-formalized)

**047** ([eq:example + Thm, 01-introduction.tex L49-70](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026/build/sections/01-introduction.tex#L49-L70)):
- The defining polynomial is H = x²F − (1+2sx)J − p²J² − pu with x = s²+u³+p²F, in ℂ[p,s,u,F,J] (12 terms, degree 7).
- Results: A = P/(H) satisfies A[w] ≅ ℂ^[5] but A ≇ ℂ^[4].

**049** ([Thm L8-16](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/build/source/sections/01-introduction.tex#L8-L16)):
- The polynomial is f = x₁ − 2Q(Q(x₂+x₄) + x₁x₄) with Q = x₂² − x₄² + x₁x₃ (16 terms, degree 5).
- Results: f is a coordinate of ℂ[x₁..x₄, w] but not of ℂ[x₁..x₄].

**What is constructive:** the "yes" halves, i.e. the stabilizations, are explicit. The "no" halves are proofs, not algorithms.

### 196 / 197 / 201 — group-ring and division-ring counterexamples

**196:**
- The construction is random: PG(2,128) labels with |T| = 16516 letters and 8258 generators.
- Graphs live on n vertices, where n is a multiple of 2·16513² = 545,358,338 and must be "sufficiently large". The required size is ineffective ([types.tex L14-30](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Torsion-Free-Group-Algebra-with-Zero-Divisors-September-23-2026/build/sections/types.tex#L10-L30)).

**197:**
- The odd-characteristic version uses p = least prime factor of (m!)²+1 with m = C(1200,600) ≈ 10^359.6. (m!)² therefore has about 10^362 digits, and p is uncomputable in practice ([L13-20](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-Odd-Characteristic-September-26-2026/build/sections/01-introduction.tex#L13-L20)).
- The characteristic-two prescription "has not been executed" and "need not be computationally practical".
- The torsion-free F₂ version inherits 196's random sizes.

**201:** built by a countable diagonal scheduling. It is not explicit at all.

### 248 — Thompson's group F is nonamenable (Lean-formalized)

- Proposition avg:boundary ([finite-proof.tex L194-200](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Thompsons-group-F-is-nonamenable-September-23-2026/build/sections/finite-proof.tex#L194-L200)) gives the Følner-defect bound (δ²/L² − 4/D)/(4(1−1/D)), with δ = 1/2.
- The bound is for a transport set S that depends on D; L and D are never instantiated.
- **There is no spectral-radius or cogrowth bound for the standard generators x₀, x₁.**

### 255 — quasi-isometric recognition of virtually polycyclic groups

A quasi-isometric rigidity theorem, Lean-formalized. It contains no algorithm.

## Current practice & state of the art

### Artin-group word problem

**What is known**
- The general case is listed as open in Boyd's 2026 survey (arXiv:2601.08658, §1.1, §3.1).
- Solved classes, each with its own algorithm:
  - spherical type, by Garside normal forms (Brieskorn–Saito, Deligne; quadratic);
  - right-angled;
  - FC type (Altobelli; Charney–Davis);
  - large type, by shortlex automatic structures (Holt–Rees 2012);
  - Euclidean type (McCammond–Sulway, arXiv:1312.7770);
  - 3-free diagrams, in quadratic time (arXiv:2204.03523);
  - diagrams with no A₃/B₃ subdiagram, by quadratic-time rewriting to geodesics (Blasco-García, Cumplido, Holt, Morris-Wright, Rees, arXiv:2412.12195).
- Godelle–Paris (arXiv:1007.1365) reduce K(π,1) and the word problem to the free-of-∞ parabolics.

**What SageMath actually does**
- `ArtinGroup(...)` dispatches ([artin.py L615-623](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/artin.py#L615-L623)) as follows:
  - all labels ∞ → `RightAngledArtinGroup`, which has a normal form;
  - type A → `BraidGroup`;
  - other finite types → `FiniteTypeArtinGroup`, which compares by left normal form ([L318-350](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/artin.py#L318-L350));
  - **everything else → plain `ArtinGroup`**.
- The plain `ArtinGroupElement` ([L42-58](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/artin.py#L42-L58)) has no comparison of its own. It inherits libGAP's fp-group `_richcmp_` ([libgap_wrapper.pyx L638-656](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/libgap_wrapper.pyx#L638-L656)), which may never terminate.
- The module TODO still asks for affine-type support ([L14-18](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/artin.py#L14-L18)).
- **Measured (Experiment E1):**
  - affine Ã₂, `s1*s2*s1 == s2*s1*s2`: **timeout at 60 s**, as do `s1*s2 == s2*s1` and two more trivial tests;
  - large type (4,4,4): **timeout at 30 s** on the defining relation;
  - B₃ (finite type): 0.024 s.

**What the Sage docs say** ([artin.py L526-536](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/artin.py#L526-L536)):
- Torsion-freeness, the center, the solvable word problem and K(π,1) are listed as "conjectured", known for finite type "and a number of other cases".
- The center statement is also imprecise for reducible diagrams. It says infinite type ⇒ trivial center, but A(A₁) × A(Ã₂) has center ℤ.

**What GAP HAP does**
- `ResolutionArtinGroup(D,n)` ([resArtin.gi](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/lib/ArtinCoxeter/resArtin.gi#L44-L50)) builds the Salvetti/Squier complex: one free generator per spherical subset ([L44-50](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/lib/ArtinCoxeter/resArtin.gi#L44-L50)). Spherical diagrams go to a separate routine ([L22-26](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/lib/ArtinCoxeter/resArtin.gi#L22-L26)).
- It sets `homotopy:=fail` and returns the group as a bare fp group ([L164-176](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/lib/ArtinCoxeter/resArtin.gi#L164-L176)).

The documentation conditions correctness on K(π,1) in five places:
- [manual entry, newResolutions.xml L18](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/doc/newResolutions.xml#L18): R is a resolution for the Artin *monoid* and "conjectured" to be one for the group, "known to hold in certain cases". It also says the group comes "without any method for solving the word problem".
- [aboutArtinGroups.html L292-307](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/www/SideLinks/About/aboutArtinGroups.html#L292-L307): X_D "is conjectured" to be contractible, and the command is usable "in those cases where the conjecture is known to hold". This page names the command `ResolutionArtin(D)`, which does not exist; the function is `ResolutionArtinGroup(D,n)`.
- [tutorialResolutions.xml L276-280](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/tutorial/tutorialResolutions.xml#L276-L280): for B₇, exactness "depends on the solution to the K(π,1) Conjecture for Artin groups of spherical type". That case has been a theorem since Deligne 1972, so the wording is stale regardless of the new paper.
- [tutorialGroupCohomology.xml L342](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/tutorial/tutorialGroupCohomology.xml#L342)
- [aboutCohomologyRings.html L259-263](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/www/SideLinks/About/aboutCohomologyRings.html#L259-L263)

### EGH / LPP in software

- Macaulay2's `LexIdeals` (v1.2, 2008) ships `LPP`, `generateLPPs` and `isLPP`.
  - The `LPP` doc node still says LPP ideals "are conjectured to play a role analogous" to lex ideals ([LexIdeals.m2 L870-872](https://github.com/Macaulay2/M2/blob/1a37f6fe95badb1e5f99707a485503d213fd9d49/M2/Macaulay2/packages/LexIdeals.m2#L870-L872)).
  - `LPP` requires a full-length power sequence: it returns `null` unless #powers = #variables ([L246-277](https://github.com/Macaulay2/M2/blob/1a37f6fe95badb1e5f99707a485503d213fd9d49/M2/Macaulay2/packages/LexIdeals.m2#L246-L277), check at L250).
- Prior known cases are listed in the paper's introduction:
  - Clements–Lindström (ideals already containing the powers);
  - Mermin–Peeva–Stillman (squares);
  - Mermin–Murai (monomial regular sequences);
  - Caviglia–Maclagan and Caviglia–De Stefani (fast-growing degrees, any field);
  - Caviglia–Sammartano (char-0 Betti numbers under a growth condition).

### Tensor-product positivity

**Type A:**
- Littlewood–Richardson positivity is in P via Knutson–Tao saturation plus LP (Mulmuley–Sohoni GCT3, arXiv:cs/0501076).
- It can also be done combinatorially by max-flow (Bürgisser–Ikenmeyer, DMTCS proc. AK 2009).

**Types B, C, D:**
- The journal GCT3 (Mulmuley–Narayanan–Sohoni, JACo 2012, Thm 1.2) decides positivity in strongly polynomial time **assuming** a positivity/stretching conjecture.
- Remark 1.4 there needs only "c = 0 ⇒ c(n) = 0 for odd n", which saturation factor 1 implies. The LP is over the BZ polytope.
- De Loera–McAllister (arXiv:math/0501446) count lattice points with LattE plus Maple-generated BZ inequalities. For type D they report D₄ only: LattE ≈ 2.5–4.5 min vs LiE up to > 60 min.
- **No public library I found exposes type-D BZ (i-trail) inequalities.** Littelmann's explicit string-cone descriptions cover types A and C; types B and C come by folding.
- SageMath's `WeylCharacterRing` multiplies characters by Brauer–Klimyk ([weyl_characters.py L490-513](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/combinat/root_system/weyl_characters.py#L490-L513)). Its cost grows polynomially in the weights, with high degree (E5).

### NC identity testing in software

- **NCAlgebra** (Mathematica) represents NC polynomials as sparse sums of words. Zero testing is a coefficient check (`NCPolyPossibleZeroQ`, [NCPoly.m L167-169](https://github.com/NCAlgebra/NC/blob/4156ae48f9540dc1547b8a42df4ac89cce15d814/NCPoly/NCPoly.m#L167-L169)).
- NC rational functions are handled white-box through realizations: `NCMinimalRealization` ([NCRealization.m L607-640](https://github.com/NCAlgebra/NC/blob/4156ae48f9540dc1547b8a42df4ac89cce15d814/NCAlgebra/NCRealization.m#L607-L640)). A rational expression is zero exactly when its minimal realization is trivial.
- Deterministic white-box algorithms already exist: Raz–Shpilka for formulas and algebraic branching programs; noncommutative-rank algorithms for rational expressions.
- **No software I found works black-box**, which is the only setting where a hitting point helps.

### Thompson's group F in cryptography and computation

- The Shpilrain–Ushakov key exchange on F was broken twice:
  - Matucci (arXiv:math/0607184): efficient private-key recovery;
  - Ruinskiy–Shamir–Tsaban (arXiv:cs/0607079): length-based attacks with significant success rates.
- Elvey Price and Guttmann (arXiv:1706.07571) estimate the cogrowth constant at ≈ 15 < 16, numerically supporting nonamenability.

*(Web-search budget ran out mid-task; a few attributions, e.g. Altobelli for FC type, come from the Boyd survey and the paper's own literature review rather than primary sources.)*

## Opportunities

### cas-1 — HAP: drop the K(π,1) caveat on `ResolutionArtinGroup`, fix stale wording (254) — **CERTIFY, pursue now**

**Proposed change**, two-stage.

*(a) Uncontroversial now:*
- In `tutorialResolutions.xml` L279-280, say exactness for B₇ "follows from Deligne's theorem (1972)".
- In `aboutArtinGroups.html` L303, rename `ResolutionArtin(D)` to `ResolutionArtinGroup(D,n)`.

*(b) Hedged update* across the five pinned locations. Draft for `aboutArtinGroups.html` L300-307 and the manual entry at newResolutions.xml L18:

> The space X_D is contractible for every finite Coxeter diagram D; this is the Artin K(π,1) conjecture, classically known for spherical (Deligne), FC-type and 2-dimensional (Charney–Davis), affine (Paolini–Salvetti) and several further classes, and claimed for all finite-rank diagrams in a 2026 preprint (OpenAI, "Harmonic heights and the Artin K(π,1) conjecture") whose top-level statement is machine-checked in Lean 4 (`OAI.HarmonicArtin.salvetti_cover_contractible`). Consequently `ResolutionArtinGroup(D,n)` returns n terms of a free ZA_D-resolution for every D, and `Homology(TensorWithIntegers(R),k)` is the integral homology of the Artin group A_D. The contracting homotopy is not implemented, and `R!.group` is returned as a finitely presented group without a word-problem solver.

**Benefit:** guarantee. Every homology computation HAP already does for a non-spherical, non-FC, non-affine diagram becomes a statement about the group rather than the monoid. Examples:
- the Artin group of E₁₀ = T(2,3,7): HAP computes H₁ = ℤ, H₂ = ℤ/2 in 29 s;
- the compact-hyperbolic [5,3,3,3]: H₁..H₄ = ℤ, ℤ/2, ℤ/2⊕ℤ, ℤ² (E3).

To my knowledge, neither lies in any class covered in the paper's literature review (FC, dimension ≤ 3, affine, or all spherical parabolics of type A/B/I₂). Both are non-FC. E₁₀ has dimension 9 and contains E₈; [5,3,3,3] has dimension 4 and contains H₄. Charney–Davis 1995 also treated some hyperbolic-reflection-group cases, so check whether [5,3,3,3] was already covered before citing it as new.

**Beneficiaries:** HAP users computing Artin-group cohomology, and geometric group theorists using HAP for examples (Ellis is himself an author on K(π,1) cases).

**Measurement:** merged documentation change. As a sanity check, Euler characteristics from HAP cells agree with the computed Betti numbers (verified for [5,3,3,3]: 1−5+10−10+5 = 1 = 1−1+0−1+2).

**Risks:** the maintainer may wait for refereeing. Corollaries such as BA⁺ ≃ BA are not in Lean; the resolution statement needs only the formalized theorem.

**First step:** open an issue or PR on gap-packages/hap with part (a), and part (b) as hedged text. I could not search existing HAP or Sage issues: the GitHub search API is blocked in this sandbox.

### cas-2 — SageMath: rewrite the `ArtinGroup` "conjectured properties" docstring and warn about `==` (254) — **CERTIFY, pursue now**

**Proposed change** to [artin.py L526-536](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/groups/artin.py#L526-L536). Draft:

> Artin groups `A_M` of finite rank have the following properties. The Salvetti complex (equivalently `H_{W_M}/W_M`) is a `K(A_M,1)` [Del1972]_ for finite type, [CD1995]_ for FC type, [PS2021]_ for affine type; for all finite-rank `M` this is claimed in a 2026 preprint with a Lean-formalized top-level statement. Consequently `A_M` is torsion free, and `Z(A_M) \cong \ZZ^k` where `k` is the number of irreducible components of finite type. The word problem is solvable for finite type (Garside normal form, implemented here), right-angled (implemented), large type, Euclidean type and diagrams without `A_3`/`B_3` subdiagrams; a uniform algorithm for all finite-rank `M` is given in a 2026 preprint.
>
> .. WARNING:: For Coxeter data that is not finite type or right-angled, element comparison falls back to GAP's finitely-presented-group methods and may not terminate (e.g. affine type `\tilde{A}_2`).

**Benefit:**
- removes a false impression that these properties are open in general;
- fixes the center statement for reducible diagrams;
- documents a real hang users will hit.

**Measurement:** merged PR, with doctests marked `# not tested` for the hang.

**Risks:** Sage reviewers may require published references. The warning and the center correction are independent of the preprint and should be split into their own PR.

### cas-3 — SageMath: opt-in uniform word / parabolic-membership test via the categorical action (254) — **IMPLEMENT, pursue now (narrow scope)**

**Proposed change:** an explicit method, e.g. `ArtinGroupElement.is_one(algorithm='categorical')` and `ArtinGroup.parabolic_membership(w, X, u)`. It would be used only for Coxeter data where Sage has no normal form, and would not replace `==` or `__hash__`. The suggested route:
1. Dispatch to known fast algorithms where they apply.
2. Use the categorical test as the terminating fallback.

**What I built** ([`artin_wp.py`](/home/claude/work/repos/scratch_cas/artin_wp.py), ~170 lines):
- Zigzag algebra on S∪{f} for labels in {2,3,∞}, bounded complexes of graded projectives, B_i / B_i⁻¹ cones, and Gaussian-elimination minimization over ℚ.
- The frame vertex o can be dropped: it never enters a complex built by colours of S, and Hom spaces among the remaining projectives are unchanged.
- Validation results are in E2.

**Comparison with existing algorithms:**
- Spherical: Garside normal form, polynomial. The categorical algorithm is slower.
- Large type: Holt–Rees shortlex, quadratic.
- No A₃/B₃ subdiagram: quadratic.
- Euclidean type: McCammond–Sulway.
- **Gap filled:** for diagrams outside all these classes — e.g. hyperbolic E₁₀, [5,3,3,3], non-FC diagrams with A₃ subdiagrams, and the 116-generator CAT(0) counterexample group — this is the only implementable general procedure. Even in classes where algorithms exist, none is in Sage today.

**Cost (measured, E2):**
- Spherical A₃ and affine Ã₂/Ã₃: polynomial growth. Ã₂ c^k: minimal complex 818 summands at word length 33, 1.9 s.
- Hyperbolic E₁₀: 1254 summands at length 80, 1.4 s.
- Diagram (3,3,∞), Coxeter-element powers: sizes 9, 65, 393, 2305, i.e. ×≈5.9 per power. This matches the spectral radius 5.83 of the Coxeter element in the reflection representation. c⁵ (length 15) did not finish in 30 s.
- One random length-14 word in (3,3,∞) reached 9052 summands (14.7 s).
- **Expect exponential cost in word length whenever the Coxeter element has spectral radius > 1.**

**Labels ≥ 4 need extra work:** Temperley–Lieb–Jones fusion over ℚ(ζ_N), via Jones–Wenzl idempotents and trace-pairing quotients, all exact linear algebra as in §sec:algorithms. Sage already has cyclotomic fields and `TemperleyLiebAlgebra`.

**Benefit:** capability, namely termination where Sage currently hangs. There is no speed gain where any specialised algorithm exists.

**Beneficiaries:** a small number of geometric group theorists experimenting with Artin groups in Sage.

**Measurement:**
- agreement with Garside / RAAG normal forms on random words;
- relator-insertion identities;
- Burau-certified nontrivial words;
- a timing table vs word length per diagram class.

**Risks:**
- The algorithmic corollary is not formalized. Mitigation: the prototype's cross-checks.
- Exponential blow-up limits it to short words.
- Reviewers may want a published reference.

**First step:** port `artin_wp.py` into a Sage ticket for labels {2,3,∞} with doctests, then add Temperley–Lieb–Jones labels.

### cas-4 — Macaulay2 LexIdeals: document char-0 EGH/LPP; `LPP(R,h,a) =!= null` is an exact realizability test in char 0 (200) — **CERTIFY, monitor**

**Proposed change** to the LPP doc node ([L838-880](https://github.com/Macaulay2/M2/blob/1a37f6fe95badb1e5f99707a485503d213fd9d49/M2/Macaulay2/packages/LexIdeals.m2#L838-L880)). Replace "are conjectured to play a role" (L871) with:

> In characteristic zero this is claimed in a 2026 preprint (OpenAI, "The Artinian Lex-Plus-Powers Betti Theorem"): if I contains a homogeneous regular sequence of degrees a_1 ≤ … ≤ a_c (each ≥ 2), the a-LPP ideal with the Hilbert function of I exists and has graded Betti numbers ≥ those of I. In positive characteristic this remains open.

One could add that, in characteristic 0, a Hilbert function h is realized by some S/I with I ⊇ regular sequence of degrees a exactly when `LPP(R,h,a)` is non-null. The LPP ideal itself contains x_i^{a_i}, so non-null always implies realizable; EGH gives the converse.

**Status:** demonstrated in Macaulay2 1.22 (E8). Random instances over ℚ all satisfy the Betti inequality (36/36 in Sage/Singular plus an M2 example). Generic ideals are weak evidence, so this is a sanity check, not support.

**Benefit:** guarantee, char 0 only.

**Risks:** unformalized; a long two-paper proof of a 30-year-old conjecture. Example coefficient rings in the docs are `ZZ/32003`, i.e. positive characteristic, where the claim says nothing. Coding-theory and Gröbner-cryptanalysis applications live over F_q, which the result does not reach.

**First step:** after acceptance or independent verification, a three-sentence doc PR. An optional extension of `LPP` to c < n power sequences needs a non-Artinian Hilbert-function interface and is not worth doing now.

### cas-5 — Type-D tensor positivity by root-lattice check + LP (204) — **RESEARCH, monitor**

**Proposed change:** implement `is_positive(λ,μ,ν)` for Dₙ as "λ+μ+ν ∈ Q(Dₙ)" plus LP feasibility of the BZ (i-trail) polytope. This is the GCT3 template, now unconditional in type D.

**Evidence:**
- I verified saturation factor 1 empirically on 8,481 triples across D₄ (N = 2, 3), D₅, D₆ and D₇ (partial), with 0 failures. B₂/B₃ controls fail as expected (1/71 and 4/210), so the check is sensitive (E4).
- The cost of today's practice grows fast with weight size. Sage's full decomposition takes 51 s for D₄ and 413 s for D₅ at scale k = 8 (E5). An LP would take milliseconds.

**Why only monitor:**
- No library exposes type-D BZ inequalities. Writing i-trail inequalities for a reduced word of w₀ in Dₙ is a real (if routine) project.
- The paper does not state the algorithm.
- Users mostly want multiplicities at small weights: LieART, physics model building, Sage. There Brauer–Klimyk is fine.
- GCT and quantum-marginal work centre on GL/Kronecker/plethysm coefficients, not Spin(2n) tensor products.

**First step if pursued:** generate BZ inequalities for D₄ from De Loera–McAllister's Maple notebook or Littelmann cones. Check LP feasibility ⇔ positivity against `WeylCharacterRing` on the E4 triples.

### cas-6 — 047/049 as test instances for polynomial-automorphism / locally-nilpotent-derivation (LND) code — **INSTANCES, monitor (low value)**

**Sizes (E7):**
- 049: f has 16 terms, degree 5. As a *composite of three elementary maps*, the stabilizing automorphism of ℂ[x₁..x₄,w] is small: exp(wΔ) sends p,s,u,F,J to polynomials with 1/7/2/27/13 terms. Expanded, the five coordinate images have 561 / 24,356 / 212,512 / 3,137 / 79 terms (degrees 24/56/88/37/13).
- 047: H has 12 terms, degree 7. The five explicit coordinates of A[w] have 1 / 10 / 2 / 669 / 128,842 terms (degrees 1/12/3/58/211); they take 2.7 s to compute.

**Verification:** symbolic identities verified (Prop. 2.1 and H + pw ↦ 0). φ(f) = x₁ was checked at 200/200 random points over GF(1000003).

**Limitations:**
- Only the stabilization (the "yes" half) is checkable.
- Neither Singular (`algebra.lib` [`is_surjective`/`is_bijective`](https://github.com/Singular/Singular/blob/4d253ff427cae6718de42b81149e3c3953f8e866/Singular/LIB/algebra.lib#L676-L760)) nor M2 nor Sage has a routine that decides coordinate-hood or "is affine space". The hard half is therefore not a regression test for anything.
- The most concrete use is minor: Δ on ℂ[p,s,u,F,J] with Δ(H) = p (049) or p³ (047) is a 5-variable LND whose kernel could be fed to Singular's [`ainvar.lib` `invariantRing`](https://github.com/Singular/Singular/blob/4d253ff427cae6718de42b81149e3c3953f8e866/Singular/LIB/ainvar.lib#L500).

## What is NOT an opportunity here (and why)

- **116, deterministic black-box NC identity testing in CAS: do not pursue.**
  - The prototype works. It needs no d×d matrices: f(T)e₀ = π_d(h_f) is computed with s series operations.
  - Cost is the problem. d = 2ns² and the rationals grow to ≈ d·log₂(n+1) bits. Size 25 in 3 variables already takes 12–23 s, and certifying a *zero* formula is exactly the case that needs all d coefficients.
  - The standard polynomial S₄ (size 215) would need d = 369,800 with ~10⁶-bit entries. A random 3×3 evaluation mod 2⁶¹−1 detects it in 0.7 ms, with failure probability ≤ deg/p.
  - Observed orders ord₀(h_f) were 3–6 against guaranteed bounds of 323–3749, so the bound is very loose.
  - Every real NC system (NCAlgebra, NCSOStools, free-probability linearization codes) has the expression in hand and uses white-box methods. The triage's T3/low score stands.
- **Using the categorical word-problem algorithm for braid-group (spherical) cryptography or speed: do not pursue.** Garside normal forms are polynomial. The categorical complex grows at least linearly even for A₃ Coxeter powers, and exponentially for pseudo-Anosov-like words (cf. Khovanov–Seidel).
- **196 / 197 / 201 as test instances: do not pursue.** None is a concrete object:
  - 196 requires n ≥ 5.45×10⁸ with ineffective "sufficiently large", over a random 8258-generator presentation;
  - 197 (odd characteristic) needs the least prime factor of ((C(1200,600))!)²+1;
  - 201 is a countable diagonal construction.

  Gardam-style SAT searches for small-support units and zero divisors gain nothing.
- **248, Thompson's F: do not pursue.**
  - The Shpilrain–Ushakov scheme was already broken twice (Matucci; Ruinskiy–Shamir–Tsaban).
  - Nonamenability implies linear drift of random-walk normal-form length. That is consistent with length-based attacks working, so it neither revives nor newly breaks anything.
  - The proof gives no spectral-radius or cogrowth constant for x₀, x₁, so numerical group theory gains only a confirmed sign (growth constant 15 < 16, Elvey Price–Guttmann).
- **255, QI recognition of virtually polycyclic groups: do not pursue.** There is no algorithm, and being virtually polycyclic is not decidable from finite presentations (an Adian–Rabin property). GAP Polycyclic starts from pc presentations.
- **200 for coding theory / Gröbner cryptanalysis: do not pursue.** Char 0 only, while those applications live over F_q.
- **204 for GCT / quantum marginals: do not pursue as stated.** Those need Kronecker/plethysm or GL moment polytopes, not Spin(2n) tensor positivity.
- **254 CAT(0) counterexample: no computational content.** The 116-generator group is handled trivially by the prototype (E2), and no software decides CAT(0)-ness.

## Experiment results

All code is in `/home/claude/work/repos/scratch_cas/`.

**E1 — Sage today** (`t_artin.py`, `t_artin2.py`):
- Generic `ArtinGroup` equality, affine Ã₂: 4/4 tests time out at 60 s, including the defining braid relation.
- Large type (4,4,4): 2/2 time out at 30 s.
- B₃ (Garside): 0.024 s.

**E2 — categorical word-problem prototype** (`artin_wp.py`, `validate_artin_wp.py`, `hyperbolic_wp.py`, `e10_burau.py`, `scale_artin_wp2.py`, `e10_growth.py`):
- **Correctness on A₃ (B₄ braids):** 300/300 random words agree with Sage's Garside normal form (153 identities), in 1.0–1.4 s total; d² = 0 checked on every complex.
- **Non-spherical identities and Burau consistency:**

  | Group | Relator-insertion identities recognised | Burau-nontrivial words declared nontrivial |
  |---|---|---|
  | Ã₂ | 40/40 | 57/57 |
  | (3,3,∞) | 40/40 | 57/57 |
  | Ã₃ | 40/40 | 58/58 |
  | free (∞,∞,∞) | — | 57/57 nontrivial |
  | E₁₀ | 30/30 | 30/30 (random words) |
  | T(3,3,4) | 30/30 | — |

- **Parabolic membership** in Ã₂ for A_{1}: 4/4 correct.
- **116-generator CAT(0) group:** 20/20 conjugated-relator identities in ≤ 0.02 s; [d,e] (m = ∞) correctly nontrivial.
- **Growth of the minimal complex for Coxeter-element powers c^k:**

  | Group | Sizes | Note |
  |---|---|---|
  | A₃ | 7…55 (k ≤ 11) | linear |
  | Ã₂ | 8, 28, 62, …, 818 (k = 11, 1.9 s) | quadratic |
  | Ã₃ | …1292 (k = 11, 4.4 s) | |
  | E₈ | …683 (k = 8) | |
  | E₉ | …979 (k = 8) | |
  | E₁₀ | 36, 96, 185, 302, 450, 656, 922, 1254 (k = 8, 1.4 s) | successive ratios fall to 1.36 by k = 8; cannot yet tell polynomial growth from slow exponential growth (Coxeter spectral radius = Lehmer's number 1.176) |
  | (3,3,∞) | 9, 65, 393, 2305 | ratio → 5.87 vs Coxeter spectral radius 5.83; k = 5 timed out at 30 s |

- **Random words (3,3,∞):** worst case 9052 summands at length 14 (14.7 s).

**E3 — HAP (1.62) homology, now unconditional group homology** (`gap/*.g`):

| Group | Homology | Cells | Time |
|---|---|---|---|
| E₁₀ = T(2,3,7) | H₁ = ℤ, H₂ = ℤ/2 | 1, 10, 45, 120 | 29 s |
| [5,3,3,3] | H₁..H₄ = ℤ, ℤ/2, ℤ/2⊕ℤ, ℤ² | 1, 5, 10, 10, 5 | 3.1 s |
| Ã₂ | H₁ = ℤ, H₂ = ℤ, H₃ = 0 | | |
| (3,3,∞) | H₁ = ℤ, H₂ = 0 | | |

**E4 — saturation factor 1, empirical** (`sat_check.py`):

| Case | Triples checked | Failures |
|---|---|---|
| D₄, N = 2 | 835 | 0 |
| D₄, N = 3, |coords| ≤ 2 | 5,209 | 0 |
| D₅ | 1,779 | 0 |
| D₆ | 275 | 0 |
| D₇ (50/55 pairs) | 383 | 0 |
| B₂ (control) | 71 | 1 |
| B₃ (control) | 210 | 4, e.g. V(ω₁)⊗V(ω₁) ∌ V(ω₁) but the doubles contain it |

**E5 — cost of current practice**, Sage Brauer–Klimyk V(kλ)⊗V(kμ), as (k, constituents, s):
- D₄: (1, 13, 0.02) … (8, 6831, 51)
- D₅: … (8, 15017, 413)
- D₆ small weights: (8, 95, 52)

**E6 — NC hitting point** (`ncpit2.py`, `ncpit3.py`):

| Formula | Matrix dim d | ord₀(h_f) | Time |
|---|---|---|---|
| [x₁,x₂] (s = 9) | 324 | 3 | 0.03 s |
| [[x₁,x₂],x₁] (s = 25) | 2500 | 6 | 2–5 s |
| [[x₁,x₂],x₃] (s = 25, n = 3) | 3750 | 5 | 12–23 s |
| zero formulas (s = 17, 25, 25) | — | correctly all-zero | 0.25 / 3.0 / 11.9 s |
| S₄ (s = 215), deterministic | would need 369,800 | — | infeasible |
| S₄ (s = 215), randomized 3×3 mod 2⁶¹−1 | — | — | 0.7 ms |

**E7 — 047/049 objects** (`size047.py`, `coord049_v2.py`, `check049_points.py`): sizes and verification as given under cas-6. The full symbolic composite check for 049 was stopped after 18 minutes, once all five images had been computed.

**E8 — LPP sanity** (`lpp_check.py`, `m2/lpp.m2`):
- 36/36 random char-0 instances satisfy HF equality and the Betti inequality.
- M2 1.22 example: I = (2 quadrics, 2 cubics) in ℚ[a,b,c]. LPP = (a², b², c³, abc). Total Betti numbers 1,4,5,2 ≤ 1,4,6,3.
- `LPP(R,{1,3,4,4},{2,2})` returns `null` (unsupported c < n).

## Sources

- Boyd, *An introduction to the geometric and combinatorial group theory of Artin groups*, [arXiv:2601.08658](https://arxiv.org/html/2601.08658v1): open status of the word problem; class list.
- Blasco-García, Cumplido, Holt, Morris-Wright, Rees, *Rewriting in Artin groups without A₃ or B₃ subdiagrams*, [arXiv:2412.12195](https://arxiv.org/abs/2412.12195).
- *The word problem is solvable for 3-free Artin groups in quadratic time*, [arXiv:2204.03523](https://arxiv.org/html/2204.03523v4).
- Godelle–Paris, *K(π,1) and word problems for infinite type Artin–Tits groups*, [arXiv:1007.1365](https://arxiv.org/abs/1007.1365).
- McCammond–Sulway, *Artin groups of Euclidean type*, [arXiv:1312.7770](https://arxiv.org/abs/1312.7770).
- Mulmuley–Sohoni, GCT3, [arXiv:cs/0501076](https://arxiv.org/abs/cs/0501076); Mulmuley–Narayanan–Sohoni, J. Algebraic Combin. 36 (2012), [full text](https://emis.univie.ac.at/journals/JACO/Volume36_1/rg1w9655642r84t8.fulltext.pdf).
- De Loera–McAllister, *On the computation of Clebsch–Gordan coefficients and the dilation effect*, [arXiv:math/0501446](https://arxiv.org/abs/math/0501446).
- Bürgisser–Ikenmeyer, *A max-flow algorithm for positivity of Littlewood–Richardson coefficients*, [DMTCS proc. AK](https://dmtcs.episciences.org/2749/pdf).
- Berenstein–Zelevinsky, *Tensor product multiplicities, canonical bases and totally positive varieties*, [arXiv:math/9912012](https://arxiv.org/abs/math/9912012).
- *On combinatorics of string polytopes in types B and C*, [arXiv:2306.11242](https://ar5iv.labs.arxiv.org/html/2306.11242): type A/C explicit string cones, type D not covered.
- Matucci, *Cryptanalysis of the Shpilrain–Ushakov protocol in Thompson's group*, [arXiv:math/0607184](https://arxiv.org/abs/math/0607184).
- Ruinskiy–Shamir–Tsaban, *Length-based cryptanalysis: the case of Thompson's group*, [arXiv:cs/0607079](https://arxiv.org/abs/cs/0607079).
- Elvey Price–Guttmann, *Numerical studies of Thompson's group F and related groups*, [arXiv:1706.07571](https://arxiv.org/abs/1706.07571).
- Code: [gap-packages/hap@415d365](https://github.com/gap-packages/hap/tree/415d3655c99f1e0aa95e042b20b80b8eb404b4e1), [sagemath/sage@0835358](https://github.com/sagemath/sage/tree/0835358cba62dc19fccdff54f32e52fded9f22b0), [Macaulay2/M2@1a37f6f](https://github.com/Macaulay2/M2/tree/1a37f6fe95badb1e5f99707a485503d213fd9d49), [NCAlgebra/NC@4156ae4](https://github.com/NCAlgebra/NC/tree/4156ae48f9540dc1547b8a42df4ac89cce15d814), [Singular/Singular@4d253ff](https://github.com/Singular/Singular/tree/4d253ff427cae6718de42b81149e3c3953f8e866).
- Papers: [openai/math@fd4aeeb](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb) (manuscripts and `lean/`).
