# Number theory and logic: quasi-RH, BSD in Selmer corank ≤ 1, Bianchi modularity, Artin, H10(Q)

Families: **003** quasi-RH and Landau–Siegel; **002** BSD for Selmer corank ≤ 1; **030** modularity of elliptic curves over imaginary quadratic fields; **029** Artin's conjecture and a uniform cyclotomic Hecke strip; **004** Hilbert's tenth problem over ℚ; **142** deterministic polynomial factorization (only as a dependent of 029); **011/012/021** briefly.

**Pinned versions**
- openai/math `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`
- SageMath `0835358cba62dc19fccdff54f32e52fded9f22b0` (11.0.beta2, Oct 11 2026)
- LMFDB `009463ed27b5dda4516c446bff5c618a17a42076` (Oct 2 2026)
- OSCAR.jl `539415e4edb9dbc3e2397787a2eccb4c76e80eaa`
- FLINT `a4c9750d0d3d67bb01cf6d18c187591b313451c3`
- OpenSSL `5188e2f0405b7cd4e5ee1c458403fb4c6d4a37c7`
- Mathlib `d6416ab0f09d3a2e090f403fc80f37754f6181a9`

Experiments are in `/home/claude/work/repos/scratch_numtheory/`. They were run with passagemath 10.8.12, a pip-installed SageMath with PARI, eclib and the Cremona database up to N ≤ 9999.

**Bottom line**
- **Pursue now: 003 makes Sage's class-number tables certifiable well past h = 100.**
  - 003's Lean-formalized 7/8 half-plane removes the only hypothesis in Tatuzawa's explicit Siegel bound. That bound (in Elsenhans–Klüners–Nicolae's form) is h(D) > 0.0767·√|D|/log|D| for every fundamental D < 0 with |D| > e^11.2.
  - So every imaginary quadratic field of class number ≤ H has |D| ≤ B(H), with a numerical B(H) and no exception left over. This is a much stronger corollary than the papers' own "effective, constant uncomputed" h(D) remark.
  - I re-derived Watkins's unconditional table for h ≤ 10 by brute force from this bound alone, in 5 minutes. Counts and maximal |D| match exactly.
  - B(457) < 2·10^10, which is PARI's certified `qfbclassno` range. The Mosunov–Jacobson unconditional tabulation to 2^40 covers h ≤ 2900. Sage's `cm.py` hard-stops at h = 100 and says larger h is only "easy conditional on GRH".
  - This is a real IMPLEMENT/CERTIFY item. The proof input is Lean-checked, and Tatuzawa (1951) is classical, though its constants deserve an expert check.
- **002 (full BSD for Selmer corank ≤ 1) is the biggest database item, and the right action is to prepare, not to flip flags.**
  - 86.1% of LMFDB's 3,824,372 curves over ℚ have rank ≤ 1. For all of them, "Ш_an" would become "#Ш".
  - Sage's `prove_BSD` already certifies most small-conductor curves. My sweeps found it proved 254/279 (91%) of rank-≤1 isogeny classes with N ≤ 200 and 567/640 (89%) with 1000 ≤ N ≤ 1200, and 27/30 in a random sample with 5000 ≤ N < 10000. The residual is almost entirely p = 3, plus 17 crashes from two real bugs I found in `prove_BSD`.
  - 002 is an extraordinary claim: about 340 pages across 3 unformalized manuscripts, plus a 130-page Goldfeld/2-converse paper, and Mathlib has no Selmer groups or Ш at all. So the only defensible action now is an expert review request and a gated "pending review" code path.
- **The triage's key negative stands, with one correction.**
  - 003 does not touch the GRH in PARI `bnfinit`/`quadclassunit`, Magma `ClassGroup`, Sage `proof=False`, FLINT `qfb_exponent_grh` or CSI-FiSh.
  - The triage's "029 transfers to class-group characters of quadratic fields by Artin factorization" is **false** in general. A ring or Hilbert class field of an imaginary quadratic field is generalized dihedral over ℚ, so its characters are Hecke characters of K, not of any cyclotomic field. 029 covers only the genus subfield. Even where it did apply, (log|d|)^{10^6} only beats Minkowski above 5·10^7-bit discriminants.
- **Everything else is docs-level or "do not pursue".**
  - 003 square roots and Miller's test: 10^19–10^94 times worse than Bach at 2048 bits.
  - 030: completes LMFDB's imaginary quadratic tables. I show 18 of the 32 LMFDB "complete-range" fields (|d| < 100 or class number 1) are not covered by Caraiani–Newton, but the result is a single unformalized 30-page paper.
  - 004: OSCAR's `is_realizable` makes no ℚ claim to retract. Tensor rank over ℚ becomes undecidable via Schaefer–Štefankovič.
  - 029/142: galactic.

## What the papers actually prove

### 003: quasi-Riemann hypothesis and Landau–Siegel (3 manuscripts; Lean: yes)
- **Theorem `thm:main`** (paper.tex L106–111, Sep 30): every finite-order Hecke L-function over F = ℚ(√−3), and every Dirichlet L-function including ζ, is zero-free in Re s > 7/8. The principal pole is allowed.
  - The Dirichlet case follows from factoring L_F(s, χ∘N) = L(s, χ)·L(s, χχ₋₃).
  - So the result covers exactly two families: **Dirichlet characters, and Hecke characters of the single field ℚ(√−3)**.
- **Cor. `cor:nonresidues-square-roots`** (L325–361): n(p) ≤ C(log p)^A with A = 32 via BIMS Thm 6.7. The weak GRH there is Dirichlet-only, with exponent 4/(1−2ε) = 32 at ε = 7/16. C is not computed. The corollary also gives deterministic poly-time square roots mod p (scan 2, 3, … then Tonelli–Shanks).
- **Companion paper** (Oct 5, paper2.tex):
  - L73 gives the 11/12 half-plane by an independent route.
  - Cor. `cor:primes-ap` (L84–95) gives the error term x^{11/12} log x in the prime number theorem for arithmetic progressions, effective but not explicit.
  - L113–125 claim the effective bound h(D) ≫ √|D|/log log|D| and completeness of Euler's 65 idoneal numbers, via EKN Theorem 2.
- **Siegel paper** (Oct 1, `thm:main` L66–73): (1−β) log q ≥ c for an ineffective c.
  - This adds nothing to 7/8 for real zeros. 7/8 already excludes every real zero above 7/8, uniformly and with no constant.
- **Lean.**
  - The `QuasiRiemannHypothesis` and `DirichletSevenEighths` challenges state the theorems with Mathlib objects only (`riemannZeta`, `DirichletCharacter.LFunction`). See [L8–12](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/DirichletSevenEighths.lean#L8-L12).
  - The Hecke clause uses a custom `Character` and `LFunction` ([L217–239](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/HeckeSevenEighths.lean#L217-L239)).
  - All four configs allow only the standard axioms. The companion Lean audit (`deep/lean.md`) walked the 556k-line closure and the patched PNT+ externals and found no `sorry` and no axiom.
  - **Confidence: 5 for the Dirichlet 7/8 statement.**

### 002: full BSD formula when some full p^∞-Selmer corank is ≤ 1 (3 manuscripts + dependencies; Lean: no)
- **Main theorem** (exact-bsd `thm:main`, 01-introduction.tex L47–62): s_q(E) ∈ {0, 1} for some prime q implies r = a = s_q, Ш is finite, and the full leading-term formula holds at every prime, with no extra hypotheses. The normalizations are a minimal model, the Néron differential, Ω over all of E(ℝ), and Tamagawa numbers c_ℓ.
- **Dependency chain** (all OpenAI, unformalized):
  - exact-bsd (94 pp.) rests on [C] the Selmer converse at every prime (82 pp., Thm 1.1 at L25–37) and [B] the 2-primary formula (164 pp., Thm 1.1 at L54–71).
  - Both rest on 006's Goldfeld/2-converse paper (130 pp.), which uses Smith's Selmer distribution.
  - The B, C and Goldfeld papers cite one another.
- **Revision history.** The Oct 7 revision of exact-bsd deleted the citation `\cite{Dv}` from "the starting constructions" (L134). The Oct 3 source never defined a `Dv` bibitem. The other revisions update citations only.
- **What is new for the databases.**
  - Analytic rank ≤ 1 already gives r = a and #Ш < ∞ (Gross–Zagier–Kolyvagin).
  - What 002 adds for all of them is the **exact integer** #Ш = Ш_an, including at p = 2 and p = 3 and at additive and reducible primes. Those are exactly the cases where Kolyvagin/Kato/Skinner–Urban bounds fail.
  - It is an identity, not an algorithm. Per-curve use still needs a certified analytic rank ≤ 1 (or s_p ≤ 1 from a descent) and exact L^{(r)}(E,1)/Ω.
- **Mathlib:** has `WeierstrassCurve` and an L-function definition but no Selmer group, Tate–Shafarevich group or modularity. Formalizing 002 is a multi-year effort.

### 030: modularity over imaginary quadratic fields (1 manuscript, 30 pp.; Lean: no)
- `thm:main` (introduction.tex L17–43): every E/K over every imaginary quadratic K is modular, with full local–global compatibility.
- It uses Caraiani–Newton's lifting theorem plus a new geometric prime switch through cyclic covers.
- Prior state: CN prove modularity for every E/K when X₀(15)(K) is finite (L94–103), which covers ℚ(√−d) for d = 1, 2, 3, 5 and infinitely many others.
- Not constructive, but databases need only the existence statement.

### 029: Artin infinitude and a uniform cyclotomic Hecke strip (1 + 1 conditional manuscripts; Lean: no)
- **`thm:primitive-root`** (01-introduction.tex L17–24): ≥ c_a x/(log x)² primes p in (x, 2x) have primitive root a. c_a and x_a are not explicit.
- **`thm:hecke-zero-free`** (L38–45): L_F(s, η) ≠ 0 for Re s > 1 − 10⁻⁶, for every finite-order Hecke character η of every cyclotomic F ⊇ μ₁₂.
- 142 uses this strip (10-analytic.tex L9–18, L91–158) through abelian factorization of ζ_M for M = ℚ(μ₁₂q, p^{1/q}). M/K is a Kummer extension of a cyclotomic field. That is legitimate, and gives O(((n+1)log p)^{10^12}).

### 004: H10(ℚ) is undecidable (2 manuscripts; Lean: no)
- `thm:main` (01-introduction.tex L7–11) gives undecidability.
- Cor. `thm:degree-normal-form` (07-consequences.tex L8–21): Turing degree 0′, still 0′ restricted to total degree ≤ 4 or to sums of squares of quadrics.
- It depends on the pointwise 2-converse (004/006 chain) and 2-adic Fontaine–Mazur (010).

### 011/012/021 (brief)
- These are asymptotic laws or existence bounds with no rates (011/012) or with ineffective C (021).
- The triage verdicts stand: no CAS, crypto or sieve guarantee changes.

## Current practice and state of the art

**Elliptic curves over ℚ (002).**
- LMFDB holds 3,824,372 curves: rank 0 is 36.73%, rank 1 is 49.34% ([stats](https://www.lmfdb.org/EllipticCurve/Q/stats)).
- The reliability knowl ([rcs.rigor.ec.q](https://www.lmfdb.org/knowledge/show/rcs.rigor.ec.q)) says:
  - r_an is rigorous only for r_an ≤ 3 and N ≤ 500k.
  - Rank-0 Ш_an is exact (modular symbols for N ≤ 500k, Stein's algorithm above).
  - Rank-1 Ш_an is exact only for N < 5000.
  - It never claims Ш_an = #Ш.
- The [ec.analytic_sha_order](https://www.lmfdb.org/knowledge/show/ec.analytic_sha_order) knowl presents Ш_an as the BSD-predicted value, and [ec.q.bsdconjecture](https://www.lmfdb.org/knowledge/show/ec.q.bsdconjecture) states BSD with no proven cases.
- LMFDB issue [#5872](https://github.com/LMFDB/lmfdb/issues/5872) (open) concerns the "exact" tag for rank 0.
- Curve-by-curve full-BSD verification: Miller proved BSD for 16714 of the 16725 rank-≤1 curves with N < 5000 ([arXiv:1010.2431](https://arxiv.org/abs/1010.2431)). Banwait–Huang (2026) identify curves with infinitely many BSD-verified twists, only about 0.1% of the N < 500k curves ([arXiv:2601.16044](https://arxiv.org/html/2601.16044v1)).
- PARI's `ellbsd` documentation describes the formula as what BSD "predicts" ([PARI EC docs](https://pari.math.u-bordeaux.fr/dochtml/html/Elliptic_curves.html)).

**Imaginary quadratic fields (030).**
- LMFDB lists 455,002 curves over imaginary quadratic fields ([browse](https://www.lmfdb.org/EllipticCurve/browse/2/0/)).
- The completeness knowl [rcs.cande.ec](https://www.lmfdb.org/knowledge/show/rcs.cande.ec) says that, because modularity has not been proved in general, the database is complete only *assuming modularity*. It covers fields with |d| < 100 or class number 1, within the Bianchi level bounds.
- Caraiani–Newton prove modularity for ℚ(√−d), d = 1, 2, 3, 5, and whenever X₀(15)(K) is finite ([arXiv:2301.10509](https://arxiv.org/abs/2301.10509)). Extensions cover 87.5% of the expected primes p for ℚ(√−p) ([arXiv:2405.09337](https://arxiv.org/abs/2405.09337)).

**GRH in class-group software (003/029).**
- PARI's `bnfinit` result is "conditional on the GRH" unless certified by `bnfcertify` ([PARI docs](https://pari.math.u-bordeaux.fr/dochtml/html/General_number_fields.html)).
- FLINT `qfb_exponent_grh` uses a GRH generator bound of 6 log²|n| ([qfb.rst](https://github.com/flintlib/flint/blob/a4c9750d0d3d67bb01cf6d18c187591b313451c3/doc/source/qfb.rst#L209-L214), [exponent_grh.c L35–38](https://github.com/flintlib/flint/blob/a4c9750d0d3d67bb01cf6d18c187591b313451c3/src/qfb/exponent_grh.c#L35-L38)).
- CSI-FiSh *assumes* its prime ideals generate the class group, which "follows from GRH" ([ePrint 2019/498](https://eprint.iacr.org/2019/498)).
- Mosunov–Jacobson tabulated class groups unconditionally for |Δ| < 2^40 ([arXiv:1502.07953](https://arxiv.org/abs/1502.07953)).
- Watkins solved the class number problem unconditionally for h ≤ 100. Holmin et al. extend it to odd h ≤ 10^6 *on GRH* ([arXiv:1510.04387](https://ar5iv.labs.arxiv.org/html/1510.04387)).
- Cremona–Sutherland's HCP test is correct unconditionally, with only its running time GRH-dependent; their Algorithm 1 needs GRH for its "false" answers ([arXiv:2301.11169](https://arxiv.org/html/2301.11169v4)).

**Least non-residue (003).**
- Bach (GRH): n(p) ≤ 2 log² p. Lamzouri–Li–Soundararajan (GRH): n(p) < log² p for p ≥ 5 ([arXiv:1309.3595](https://ar5iv.labs.arxiv.org/html/1309.3595)).
- Unconditional: Norton 4.7 p^{1/4} log p; Treviño 0.9/1.1 p^{1/4} log p; Burgess–Vinogradov p^{1/(4√e)+ε} (non-explicit). These are cited in [arXiv:1412.3062](https://arxiv.org/pdf/1412.3062).
- BIMS Thm 6.7 (weak GRH ⇒ n(p, r) = O((log p)^{4/(1−2ε)})) ([paper](https://cse.iitk.ac.in/users/nitin/papers/irred-and-rth-root.pdf)).

**Rational decision problems (004).**
- Sturmfels showed that matroid realizability over ℚ is equivalent to Diophantine solvability over ℚ. The OSCAR matroid paper quotes this and says decidability "is not known" ([arXiv:2311.08792](https://arxiv.org/pdf/2311.08792), §3).
- Schaefer–Štefankovič give a polynomial-time many-one reduction from the existential theory of any field F to tensor rank over F. Their Figure 1 lists tensor rank over ℚ as ∃ℚ-complete with upper bound ∅′ ([arXiv:1612.04338](https://arxiv.org/pdf/1612.04338)).
- Shitov proves the same for integral domains ([arXiv:1611.01559](https://arxiv.org/abs/1611.01559)).

## Opportunities

### numtheory-1: Extend Sage's unconditional class-number tables beyond h = 100 using 003 + Tatuzawa (IMPLEMENT/CERTIFY)
**The math.**
- Tatuzawa's explicit Siegel theorem, as stated by Elsenhans–Klüners–Nicolae ([arXiv:1803.02056](https://arxiv.org/pdf/1803.02056), Lemmas 2–3), says:
  - Assume |D| > e^{11.2} and L(s, χ_D) ≠ 0 on [1 − 1/(4 log|D|), 1).
  - Then h(D) > (0.655/(πe)) √|D| / log|D|.
- 003 gives L(s, χ) ≠ 0 for Re s > 7/8 for every Dirichlet χ, and 1 − 1/(4 log|D|) > 7/8 as soon as log|D| > 2. So the hypothesis holds **for every D**, with no exceptional discriminant and no uncomputed constant.
- Hence h(D) ≤ H implies |D| ≤ B(H), where B is explicit:

| H | B(H) |
|---|---|
| 100 | 7.06·10^8 |
| 457 | 2.0·10^10 |
| 1000 | 1.10·10^11 |
| 2900 | 2^40 |

- **This is far stronger than what the papers advertise.** They advertise h(D) ≫ √|D|/log log|D| with "computable constant" and stop there.
- B(H) is about 50× larger than the GRH bound Cremona–Sutherland use (1.4·10^7 at h = 100), but it is finite and unconditional.

**Validation (experiment E1).**
- With `watkins_check.py`, I enumerated all fundamental D with |D| ≤ B(10) = 3.92·10^6 using PARI `qfbclassno`, which is certified below 2·10^10.
- Counts and largest |D| for each h = 1..10 match Watkins's table in Sage exactly ([cm.py L539–583](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/cm.py#L539-L583)), for example h = 10: 87 fields, max |D| = 13843.
- Sanity check: on all 281,731 fundamental D in (−10^6, −73130), min h·log|D|/√|D| = 0.83 (D = −111763), well above 0.0767.

**Targets.**
- [`largest_fundamental_disc_with_class_number`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/cm.py#L609-L654) and [`largest_disc_with_class_number`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/cm.py#L657-L716): their docstrings say h > 100 is "easy … conditional on the GRH, but much harder … unconditional", and they raise `NotImplementedError` for h > 100.
- [`discriminants_with_bounded_class_number`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/cm.py#L797-L804) raises "if hmax>100 you must specify a discriminant bound B". The fix could supply B(H) automatically.
- Downstream: `cm_orders`, `cm_j_invariants(K)` for [K:ℚ] > 100, and the CM j-invariant certification paths. The proof flag is turned off below 2·10^10 at [L842–844](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/cm.py#L842-L844), which is consistent with PARI's documented certified range.
- LMFDB CM and class-number data, and anyone citing "Watkins h ≤ 100" as the unconditional frontier.

**Benefit.** guarantee and capability. Unconditional complete lists:
- for h ≤ 457, compute-bound only (all fundamental |D| < 2·10^10);
- for h ≤ 2900, if Mosunov–Jacobson's unconditional 2^40 tabulation is reused.

**Cost.** Enumerating to 2·10^10 with `qfbclassno` is about 5·10^9 fundamental discriminants. Extrapolating my 291 s run to 3.9·10^6, a single core needs roughly 4 CPU-days per 10^8 at small |D|, rising with |D|. This is a cluster-scale job, or reuse Mosunov–Jacobson's data.

**Risks.**
- (i) Tatuzawa's 1951 constants: EKN restate them (Lemma 2), and Hoffstein revisited the theorem in "On the Siegel–Tatuzawa theorem" (Acta Arith. 38). An expert must confirm 0.655 and e^{11.2} before certification.
- (ii) The bound is only as good as 003. That risk is small because it is Lean-formalized against Mathlib's `DirichletCharacter.LFunction`.
- (iii) Practical value is modest: who needs h = 101..457 complete lists? CM-point and isogeny-class-in-degree-d searches, Heegner-point work and LMFDB.

**First step.** Write a 2-page note giving the bound, the constants and the h ≤ 10 replication. Ask Watkins/Klaise or another expert to check the Tatuzawa constants. Then open a Sage PR that adds an optional unconditional bound B(h) with a citation, gated on that check.

### numtheory-2: Prepare LMFDB/Sage for 002 without asserting it: "Ш_an = #Ш (pending review)" (CERTIFY, gated)
**What would change if 002 holds.**
- [`Sha.an`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/sha_tate.py#L299-L456) returns "the Birch and Swinnerton-Dyer conjectural order" (L301). Its code comment "rank > 0 (Not provably correct)" (L436) refers to the analytic computation. With 002, for r ≤ 1 the value is #Ш outright, given rigorous L′.
- [`prove_BSD`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/BSD.py#L246-L462) returns the primes where "BSD(E,p)" is unproven (L249–255). With 002 it would return `[]` for every rank ≤ 1 curve once `rank == analytic_rank` is certified (L534–535).
- [`Sha.an_numerical`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/sha_tate.py#L208-L227) docstring.
- LMFDB:
  - [`ec-curve.html` L262–349](https://github.com/LMFDB/lmfdb/blob/009463ed27b5dda4516c446bff5c618a17a42076/lmfdb/elliptic_curves/templates/ec-curve.html#L262-L349): "BSD invariants", "Analytic order of Ш", "BSD formula".
  - [`web_ec.py` L705](https://github.com/LMFDB/lmfdb/blob/009463ed27b5dda4516c446bff5c618a17a42076/lmfdb/elliptic_curves/web_ec.py#L705) (`sha_is_exact = rank == 0`, issue #5872).
  - [L813–815](https://github.com/LMFDB/lmfdb/blob/009463ed27b5dda4516c446bff5c618a17a42076/lmfdb/elliptic_curves/web_ec.py#L813-L815): the formula is already rendered with "=" for r_an < 2 and "≟" otherwise. That "=" is today a statement about Ш_an, and would become a theorem about #Ш.
  - Knowls `ec.analytic_sha_order`, `ec.q.analytic_sha_value`, `ec.q.bsdconjecture`, `rcs.rigor.ec.q`. These live in the knowl DB, not the repo.
- Reach: 3,291,642 curves (86.1%), but 93.7% of them have Ш_an = 1.
- Also Cremona's `ecdata` sha column, Magma `ConjecturalSha`, PARI `ellbsd` docs, and the arithmetic-statistics papers that condition on BSD.

**What is already proven today (experiment E2, `bsd_gap.py`).** I ran Sage `prove_BSD()` on every rank-≤1 optimal curve (label …1) in two conductor windows:

| window | classes | fully proved | primes left open | crash/timeout |
|---|---|---|---|---|
| N = 11–200 | 281 | 254 (91% of 279 completed) | 25 (all p = 3 or 5; all Ш_an = 1) | 2 (env; both proved on rerun) |
| N = 1000–1200 | 659 | 567 (89% of 640 completed) | 73 (p = 3: 68, p = 5: 3, p = 2: 1, p = 7: 1) | 19 (15 `secs_dc` bug, 1 tuple bug, 3 timeouts at 30 s) |
| random 30, 5000 ≤ N < 10000 | 30 | 27 | 2 (both p = 3) | 1 (`secs_dc` bug) |

- So the gap 002 closes is concentrated at p = 3 and at reducible or additive primes. For almost all of these curves Ш_an = 1. Only 1 of the 100 open curves across all three runs has Ш_an > 1 (1058b1, Ш_an = 4, p = 2 open).
- At large conductor the analytic inputs (Heegner index, L-ratio) dominate the cost, not the theory.

**Bugs found in `prove_BSD`** (independent of 002, worth fixing now; this is row numtheory-3):
- (a) [BSD.py L845](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/BSD.py#L845) and [L899](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/BSD.py#L899) call `heegner_index_bound(..., secs_dc=secs_hi)`. The [signature](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/heegner.py#L6815) has no `secs_dc`, so rank-0 curves reaching the "try harder" branch crash with TypeError. Seen on 15 curves, e.g. 1014e1 and 1050c1.
- (b) [BSD.py L805](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/BSD.py#L805) does `BSD.bounds[p][1] = (low, …)` on a tuple, raising TypeError (1058d1). It should be `BSD.bounds[p] = (low, min(...))`. The same pattern appears at L660.

**Benefit.** guarantee. It removes "assuming BSD" from Ш for 3.3M curves and from downstream statistics, such as the distribution of Ш and Delaunay-heuristic tests.

**Confidence.** **1–2.**
- Full BSD in rank ≤ 1 at all primes was open.
- The claim rests on about 340 pages in 3 interlocking unformalized OpenAI manuscripts plus the 130-page 006 paper, and uses ultralimit/"admissible cochain" constructions (Selmer-converse §1 L159).
- In the formalization audit, BSD sits among the clusters with repairs, and 10% of unformalized families were repaired within two weeks.
- No Lean is possible soon: Mathlib has no Selmer group or Ш.

**Measurement.**
- (1) Number of independent expert reports on [B], [C] and exact-bsd.
- (2) Once accepted, the share of LMFDB rank-≤1 pages carrying a "proven" Ш tag. This needs rank-1 exact L′(E,1) beyond N = 5000, which is a computation LMFDB has not run.

**First step.**
- Now: file the two Sage bug fixes.
- Open an LMFDB discussion issue proposing a knowl sentence: "a 2026 unrefereed preprint claims Ш_an = #Ш for r ≤ 1; not used for any flag". Keep it display-only.
- Ask the LMFDB editorial board to commission review.
- Do **not** change `sha_is_exact` semantics or `prove_BSD` output until refereed.

### numtheory-4: LMFDB imaginary-quadratic completeness qualifier (030) (CERTIFY; the CN part now, the 030 part gated)
**Targets.**
- The knowl `rcs.cande.ec` (served by [ecnf/main.py L64–70](https://github.com/LMFDB/lmfdb/blob/009463ed27b5dda4516c446bff5c618a17a42076/lmfdb/ecnf/main.py#L64-L70)), with its "assuming modularity" completeness.
- Bianchi modular form pages.
- [`ecnf-curve.html` L361–386](https://github.com/LMFDB/lmfdb/blob/009463ed27b5dda4516c446bff5c618a17a42076/lmfdb/ecnf/templates/ecnf-curve.html#L361-L386) (the "conditional on BSD" footnote concerns rank, not modularity, and is unaffected).

**Experiment E3 (`x015_twists.py`, `x015_exact.py`).**
- Of the 32 fields with |d| < 100 or class number 1, 14 are already covered unconditionally by Caraiani–Newton: d = −3, −4, −8, −15, −19, −20, −23, −31, −35, −47, −79, −83, −87, −91. X₀(15)(K) is finite there, certified by exact L(15a1^{(d)}, 1)/Ω ≠ 0.
- The other 18 have X₀(15)(K) infinite, so they need 030 or a different CN residual argument: −7, −11, −24, −39, −40, −43, −51, −52, −55, −56, −59, −67, −68, −71, −84, −88, −95, −163.
- These include 2.0.7.1, which has 70,927 curves.
- LMFDB could today replace its blanket caveat with "complete (unconditionally) for the 14 fields above". That is a no-risk docs fix that needs no preprint.

**Confidence.** 2: a single 30-page unformalized paper, with CN's lifting theorem as essential input.

**First step.** File an LMFDB issue with the 14/18 split now (CN-based, independent of 030). Mention 030 only as "claimed".

### numtheory-5: Textbook/doc note — unconditional deterministic square roots and Miller test (CERTIFY, docs only)
- **Targets: docs only, with no code change.**
  - Galbraith §2.9, Crandall–Pomerance, Cohen GTM 138, Wikipedia (Tonelli–Shanks, Miller–Rabin).
  - FLINT's [`flint_mpn_sqrtmod` doc](https://github.com/flintlib/flint/blob/a4c9750d0d3d67bb01cf6d18c187591b313451c3/doc/source/mpn_extras.rst#L1342-L1351), which says a prime with least non-residue > 2^20 is a "negligible probability" event. The cap itself is at [sqrtmod.c L170–188](https://github.com/flintlib/flint/blob/a4c9750d0d3d67bb01cf6d18c187591b313451c3/src/mpn_extras/sqrtmod.c#L170-L188).
  - OpenSSL's `BN_mod_sqrt` tries 2..21 and then random y up to 82 tries ([bn_sqrt.c L176–216](https://github.com/openssl/openssl/blob/5188e2f0405b7cd4e5ee1c458403fb4c6d4a37c7/crypto/bn/bn_sqrt.c#L176-L216)). It is randomized, so it is unaffected.
- **Numbers (E4, `bounds.py`).**
  - 2^20 covers primes up to 1045 bits under Bach and 1477 bits under LLS. Unconditionally, Treviño only covers 59 bits, and 003 with C = 1 covers about 20 bits for A = 32.
  - So FLINT's "negligible probability" wording is a heuristic or GRH statement. 003 does not make the cap provably safe at any cryptographic size.
- **Benefit.** A "guarantee" for theory statements only. **Practicality 1.**

### numtheory-6: Coding-theory "under Artin's conjecture" audit (029) (CERTIFY, docs)
- Asymptotic double-circulant, four-circulant, LCD and hull results are still stated "under Artin's conjecture" in 2024–25. An example is arXiv:2401.07017, which needs primes m with q primitive mod m.
- 029 supplies infinitely many such m for each non-square q ≠ −1. That is all an asymptotic-existence argument needs, but only for prime moduli and with x/log²x density.
- Results that need positive density stay conditional.
- Confidence 2–3 (unformalized, 92 pp.).
- First step: sort the literature into "infinitude-only" and "density" results. BIKE/HQC parameters are unaffected.

## What is NOT an opportunity here (and why)

JSON rows numtheory-7, -8, -9 and -11 are "do not pursue". numtheory-10 (004) is "monitor" at docs level.


- **"003 removes GRH from class-group computations" (PARI `bnfinit`/`quadclassunit`, Magma `ClassGroup`, Sage `proof=False`, FLINT `qfb_exponent_grh`, CSI-FiSh): false.**
  - Bach's bound for generators of Cl(K) needs GRH for ζ_K and the Hecke L-functions of class-group characters of K.
  - For an imaginary quadratic K, those are L(s, χ_D) times L-functions of non-genus class-group characters. 003 controls only the first factor, and Hecke characters of ℚ(√−3).
  - A zero-free region also cannot by itself give a polylog bound. The Bach-type exponent is 1/(1−θ)-ish, so 7/8 would give (log|d|)^{O(8)} with uncomputed constants. That is still not 6 log²|d|.
  - Sage's `proof=False` hooks ([number_field.py L4385–4386](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/rings/number_field/number_field.py#L4385-L4386)) stay as they are.
- **"029's cyclotomic strip transfers by Artin factorization to class-group characters of quadratic fields" (the triage's non-obvious channel): wrong as stated.**
  - Artin factorization writes ζ_M for M/F abelian as a product of Hecke L-functions *of F*. 029's theorem is about Hecke characters of cyclotomic F.
  - So it covers L-functions of finite abelian extensions of cyclotomic fields, which is how 142 legitimately uses Kummer extensions of ℚ(μ₁₂q). By the Kronecker–Weber theorem, that includes every abelian extension of ℚ.
  - The Hilbert class field H of K = ℚ(√D) is Galois over ℚ with Gal(H/ℚ) = Cl(K) ⋊ C₂, a generalized dihedral group, which is non-abelian once Cl(K) has exponent > 2.
  - So H is **not** contained in any cyclotomic field. A non-genus class-group character of K is a character of K, not the restriction of a Hecke character of any cyclotomic F through a norm compatibility.
  - Base change to F = K(μ₁₂) does not help either. η∘N_{FK/K} is a Hecke character of FK, and FK is not cyclotomic, because it contains K and K ⊄ ℚ(μ_n) in general.
  - The Artin L-function of the 2-dimensional induced representation Ind_K^ℚ ψ is a dihedral (CM-form) L-function, which 029 does not cover.
  - **The strip covers exactly the genus characters** (χ_{d₁}·χ_{d₂} with d₁d₂ = D), which give the 2-rank and nothing beyond it.
  - Even granting a transfer, the bound (log|d|)^{10^6} beats Minkowski's √|d| only once |d| has more than 5.0·10^7 bits. It would beat subexponential Hafner–McCurley only beyond 4.5·10^{13} bits (E4).
- **"Square roots / Miller test / factoring without GRH" as a speed claim (003, 142).**
  - At 2048 bits, 003's bound with C = 1 is 10^{18.6}, 10^{43.8} or 10^{94.3} times Bach's for A = 8, 16 or 32.
  - It beats explicit Treviño/Norton only above 200/509/1205 bits and Burgess–Vinogradov above 435/996/2237 bits, before the unknown C.
  - Real primes have mean n(p) ≈ 3–4: across 560 random 256–2048-bit primes the maximum was 23.
  - 142's exponent 10^{12} is galactic.
- **"No Siegel zeros" as a usable explicit bound.** The Siegel paper's c is ineffective (contradiction argument), and the Lean statement is ∃c > 0. What is actually useful is the 7/8 half-plane (numtheory-1), not the Siegel paper.
- **Idoneal-numbers completeness (003 companion claim): fine, but no software uses it.**
  - EKN's hypothesis (no real zero in [1 − 1/(4 log|D|), 1)) follows from 7/8.
  - OEIS A000926 still says "conjectured complete" and could be footnoted. That is docs only.
- **004 → OSCAR `is_realizable`: nothing to retract.**
  - The docstring ([realization_space.jl L79–92](https://github.com/oscar-system/Oscar.jl/blob/539415e4edb9dbc3e2397787a2eccb4c76e80eaa/experimental/MatroidRealizationSpaces/src/realization_space.jl#L79-L92)) only claims to decide realizability over *some* field of characteristic 0 (algebraically closed reasoning via minimal primes, [L100–111](https://github.com/oscar-system/Oscar.jl/blob/539415e4edb9dbc3e2397787a2eccb4c76e80eaa/experimental/MatroidRealizationSpaces/src/realization_space.jl#L100-L111)) or over GF(p) or GF(q).
  - `realization_space(…; ground_ring=QQ)` ([L296–306](https://github.com/oscar-system/Oscar.jl/blob/539415e4edb9dbc3e2397787a2eccb4c76e80eaa/experimental/MatroidRealizationSpaces/src/realization_space.jl#L296-L306)) returns the ideal over ℚ but makes no claim about ℚ-points.
  - At most, add one sentence noting that ℚ-realizability is undecidable (Sturmfels + 004), mirroring the existing "undecidable in general" notes in `SimplicialComplexes.jl` L477/L496/L515.
  - Tensor rank over ℚ: Schaefer–Štefankovič's reduction makes it undecidable given 004. No tool claims to decide it.
  - The SMT channel (QF_NRA is decidable over ℝ, NIA was already undecidable) is unaffected.
- **011/012/021**: no rates or explicit constants at 2^256-scale, so no generator or sieve code changes. The triage verdicts stand.

## Experiment results

All code and outputs are in `/home/claude/work/repos/scratch_numtheory/`.
- **E1 — 003 + Tatuzawa class-number bound** (`tatuzawa.py`, `watkins_check.py`):
  - Constant 0.0767 above e^{11.2} = 73130.
  - Empirical minimum of h·log|D|/√|D| over 281,731 discriminants is 0.83.
  - B(10) = 3.92·10^6, B(100) = 7.06·10^8, B(457) ≈ 2·10^10, and |D| < 2^40 covers h ≤ 2900.
  - Brute-force re-derivation of Watkins h ≤ 10 matched all 10 rows exactly (291 s).
- **E2 — `prove_BSD` gap** (`bsd_gap.py`, `out_11_200.json`, `out_1000_1200_v2.json`): see the table in numtheory-2.
  - The first 1000–1200 run had 72 extra crashes from a missing `passagemath-symbolics`. That was environmental, and fixed in v2.
  - The remaining crashes reproduce two genuine Sage bugs (BSD.py L845/L899 `secs_dc`; L805 tuple assignment).
  - In a random sample of 30 rank-≤1 classes with 5000 ≤ N < 10000 (`bsd_sample.py`, `out_sample_5k_10k.json`, 45 s hard timeout per curve in a subprocess), 27 were fully proved, 2 were left open at p = 3, and 1 hit the `secs_dc` crash.
- **E3 — Caraiani–Newton coverage of LMFDB imaginary quadratic fields** (`x015_*.py`): 14 of 32 covered, 18 need 030 (lists above).
- **E4 — Least non-residue and class-group bounds** (`bounds.py`, `bounds_out.txt`): crossover table above; empirical mean n(p) of 3.2–4.0 for random primes.

## Sources
- openai/math preprints and lean (commit fd4aeeb): 003 paper.tex L106–111, L325–361; paper2.tex L73–125; Siegel paper.tex L66–73; 002 exact-bsd 01-introduction.tex L47–62, L134 (Oct 3 vs Oct 7); Selmer converse L25–37; 2-primary L54–71; 029 L17–45; 142 00-introduction L27–38, 10-analytic L9–158; 030 introduction L17–43, L91–103; 004 L7–11, 07-consequences L8–21.
- LMFDB stats: https://www.lmfdb.org/EllipticCurve/Q/stats ; knowls rcs.rigor.ec.q, ec.analytic_sha_order, ec.q.analytic_sha_value, ec.q.bsdconjecture, rcs.cande.ec; issue https://github.com/LMFDB/lmfdb/issues/5872 ; IQ browse https://www.lmfdb.org/EllipticCurve/browse/2/0/
- Miller, arXiv:1010.2431; Banwait–Huang, arXiv:2601.16044
- Caraiani–Newton, arXiv:2301.10509; X₀(15) over ℚ(√−p), arXiv:2405.09337
- Elsenhans–Klüners–Nicolae, arXiv:1803.02056 (Lemmas 2–3, Thm 2); OEIS A000926
- Mosunov–Jacobson, arXiv:1502.07953; Holmin et al., arXiv:1510.04387; Cremona–Sutherland, arXiv:2301.11169
- Lamzouri–Li–Soundararajan, arXiv:1309.3595; Treviño, arXiv:1412.3062; BIMS, https://cse.iitk.ac.in/users/nitin/papers/irred-and-rth-root.pdf
- PARI docs: General_number_fields.html, Elliptic_curves.html
- CSI-FiSh, https://eprint.iacr.org/2019/498
- OSCAR matroids, arXiv:2311.08792; Schaefer–Štefankovič, arXiv:1612.04338; Shitov, arXiv:1611.01559
- Double/four-circulant codes under Artin, arXiv:2401.07017
- Code: Sage BSD.py, sha_tate.py, cm.py, heegner.py, number_field.py; LMFDB web_ec.py, ec-curve.html, ecnf/WebEllipticCurve.py, ecnf-curve.html, ecnf/main.py; OSCAR realization_space.jl; FLINT sqrtmod.c, mpn_extras.rst, qfb.rst, exponent_grh.c; OpenSSL bn_sqrt.c (all pinned above).

LMFDB filtered-count queries (rank 0–1 with Ш ≥ 2; N > 500000) could not be read because the fetch proxy rate-limited them (HTTP 429). The rank split above comes from the stats page instead.
