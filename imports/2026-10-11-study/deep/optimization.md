# Optimization theme: hyperbolic cones, bin-packing gaps, superstrings, crossing numbers, Steinitz, L1 embeddings

Families: 095, 118, 128, 165, 097, 089. Paper sources are pinned to openai/math commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. All experiment code is in `/home/claude/work/repos/scratch_optimization/`.

**Bottom line.** None of these six families changes what an optimization practitioner does on Monday. The few real actions are small certification and benchmark items:
- **165:** the crossing numbers of K_n and K_{m,n} are now proven, so 712 graphs in published crossing-minimization benchmarks gain proven optima.
- **118:** MIRUP is now false, but the counterexamples are astronomically large, so textbooks and surveys need a one-line update. No solver needs to change.
- **095:** the explicit cone and its exact 100×100 SDP lift make a cheap, ready-made solver test instance.

On the main questions:
- **SCS vs zstd (128):** I confirmed zstd is not a fit, and measured it. Any superstring merge of zstd's dictionary segments saves at most about 1.1–1.3% of the dictionary, and plain greedy already reaches that.
- **The lower bound W (128):** on real bacterial k-mer sets, W is identical to KmerCamel's existing cycle-cover bound. It adds at most 0.3% on repeat-heavy synthetic sets, and costs about 1000× the compute.
- **097 and 089:** neither has a usable constant. The 089 planar distortion constant is about 10^(9.6×10^8), not the ~10^60 the triage recorded.

## What the papers actually prove

### 095 — Hyperbolicity cones without semidefinite lifts (3 manuscripts)

**The explicit cone** (*A Nonspectrahedral Hyperbolicity Cone*, Lean-formalized):
- **Polynomial.** `p(X,Z,y) = det((det X) Z − Φ_y(adj X))` on Sym⁴ × Sym⁴ × R³, which is 23 variables. It has degree 20 and is hyperbolic in the direction e = (I, I, 0) ([Thm 1.1, 01-introduction.tex L63-72](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Nonspectrahedral-Hyperbolicity-Cone-September-24-2026/build/sections/01-introduction.tex#L63-L72)).
- **Map.** Φ_y is built from the Choi–Lam biquadratic matrix Q(y).
- **Not spectrahedral.** Its cone K has no linear matrix inequality (LMI) representation of any size.
- **Reduced degree.** Corollary 1.2 (cor:reduced) gives q = p / det X of degree 16, as a 16×16 block determinant, with the same cone. When X ≻ 0, K is the set where Z ⪰ Φ_y(X⁻¹).

**The exact lift** (*An Exact Semidefinite Lift…*, NOT formalized):
- **Size.** Thm 1.1 ([introduction.tex L68-79](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone-October-5-2026/build/sections/introduction.tex#L68-L79)): K is the projection of a 100×100 LMI with 307 auxiliary variables.
- **How it is built.** The building blocks are explicit:
  - a 20×20 slice pencil L_θ, whose determinant equals p on the plane y = η(cosθ, sinθ, 0) + ξ(0,0,1);
  - a moment matrix H(Λ)_{(i,a),(j,b)} = Λ(f_a f_b (L_θ)_ij) with f = (1, cos θ, sin θ, cos 2θ, sin 2θ);
  - Λ ranging over the 22·15 = 330-dimensional space of trigonometric coefficients of degree ≤ 7 ([lift.tex eq. moment-matrix L46ff, size L184ff](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-Exact-Semidefinite-Lift-of-a-Nonspectrahedral-Hyperbolicity-Cone-October-5-2026/build/sections/lift.tex#L40-L207)).
- **I built it, and it is correct numerically** (see Experiments). The 307 is an upper bound, which the paper says itself. Only 204 of the 330 coefficient matrices are nonzero, so only **181 auxiliary variables actually appear**.

**The non-liftable cone** (*Hyperbolicity Cones Without Semidefinite Lifts*, NOT formalized):
- **Statement.** Thm 1.1 says some hyperbolicity cone is not a spectrahedral shadow. This disproves the Projected Lax conjecture.
- **Construction.** It is p_Q with m = 330, r = 20N − 1 and N > 10·36² ([01-introduction.tex L33-36, L138-139](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Hyperbolicity-Cones-Without-Semidefinite-Lifts-October-5-2026/build/source/01-introduction.tex#L33-L139); [02-cone.tex Prop. hyperbolic](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Hyperbolicity-Cones-Without-Semidefinite-Lifts-October-5-2026/build/source/02-cone.tex#L1-L60)).
- **Size.** With the minimum N = 12,961, the matrix size is n = r + 1 = 259,220. The ambient dimension is 2·n(n+1)/2 + 330 ≈ **6.7×10¹⁰**, and the degree n(n+1) ≈ **6.7×10¹⁰**.
- **Nature of the result.** It is an existence argument through a finite-field certificate. The paper does not claim a lower bound on lift size for any cone of usable size.

### 118 — Unbounded configuration-LP gaps in bin packing (Lean-formalized)

**What is proved:**
- **Thm 1.1 (thm:unbounded-gap).** For every c ≥ 0 there is an instance with all item sizes > 1/6 such that LP(I) = B exactly (an integer) and OPT(I) > B + c. This holds both for the Gilmore–Gomory type-configuration LP and for the individual-copy LP ([introduction.tex L87-96](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026/build/source/introduction.tex#L87-L118)). With c = 1 this refutes MIRUP (OPT ≤ ⌈LP⌉ + 1) with no ceiling ambiguity.
- **Thm 1.2.** For each fixed c, it is NP-hard to tell OPT ≤ B apart from OPT > B + c.
- **Cor 1.3.** A polynomial-time OPT + C algorithm exists if and only if P = NP.

**Instance size (galactic):**
- **Base instance.** The gap instance is the reduction applied to K₄ with k = 2 and ρ = 1/8 ([consequences.tex L9-25](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026/build/source/consequences.tex#L9-L25)).
- **Parameters.** P₀ = 100¹¹, K = 25(c+1)(1+5P₀) ≈ 2.5×10²⁴ for c = 1, and d ≥ 960K ≈ 2.4×10²⁷ ([instance.tex eq. parameters L28-45](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026/build/source/instance.tex#L28-L45)).
- **Competing-tree gadget.** It runs 2d − 1 ≈ 4.8×10²⁷ phases ([trees.tex L22-60](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026/build/source/trees.tex#L22-L60)). I computed the leaf counts: 1 → 2 → 10 → 699,050 → about 2^699050 after only 4 of those phases, so the tree depth L is a tower.
- **Item sizes.** Their denominators include [100(D*+1)]^L·3ⁿ ([instance.tex eq. encoding-denominators L387-404](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Additive-hardness-and-unbounded-configuration-gaps-in-bin-packing-September-24-2026/build/source/instance.tex#L387-L404)).
- **Consequence.** No witness can ever be written down.

**Hardness caveat.** The hardness reduction encodes sizes over denominators ~3ⁿ(R+1)^m. It therefore says **nothing about instances whose bin capacity is polynomially bounded**, which covers every BPPLIB and cutting-stock instance in practice.

### 128 — Polynomial-time 2-approximation for shortest common superstring (Lean-formalized)

**The algorithm.** Thm 1.1 gives a deterministic polynomial-time algorithm with |T| ≤ 2·OPT ([01-introduction.tex L5-10](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Polynomial-Time-2-Approximation-for-Shortest-Common-Superstring-September-24-2026/build/sections/01-introduction.tex#L5-L10)).

**The lower bound W:**
- **How the counts are built.** They are computed top-down over all distinct substrings V ([02-counts.tex L28-107](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Polynomial-Time-2-Approximation-for-Shortest-Common-Superstring-September-24-2026/build/sections/02-counts.tex#L28-L107)):
  - extension rules m(s) ≥ Σ_c m(cs) and m(s) ≥ Σ_c m(sc) (eq. extension-rules);
  - a periodicity rule using a blocking functional B_A (eq. period-rule);
  - W = Σ_c m(c) ≤ OPT (Lemma counts).
- **Status as a certificate.** W ≤ OPT is a self-contained, polynomial, checkable lower bound. The output has length ≤ 2W.

**Cost.** The paper states only "polynomial". A naive implementation of the rule enumeration is high-degree.

### 165 — Exact crossing numbers of K_n and K_{m,n} (Lean-formalized)

- **Results.** cr(K_n) = ¼⌊n/2⌋⌊(n−1)/2⌋⌊(n−2)/2⌋⌊(n−3)/2⌋ for all n, and the Zarankiewicz formula for cr(K_{m,n}) for all m, n.
- **Constructive.** The matching drawings are explicit (two-page drawings).
- **Scope.** These are ordinary, curved-arc crossing numbers. The rectilinear (straight-line) crossing number is untouched ([lean/docs/165.md](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/165.md)).

### 097 — Euclidean Steinitz–Bergström (Lean-formalized)

**What is proved.** Thm (signing/steinitz): unit-ball vectors in R^d admit one signing (or, for zero-sum families, an ordering) whose every prefix has norm ≤ C√d. This is existential: "does not supply an online rule or an efficient algorithm" ([introduction.tex L36-51](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Euclidean-Steinitz-Bergstrom-theorem-September-24-2026/build/introduction.tex#L36-L51)).

**The constant:**
- **Formula.** C = 2D*A₀/σ with σ = min{1/2, κδ/(√2π)} and κ = 1/100, δ = 1/4 ([assembly.tex L179-244](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Euclidean-Steinitz-Bergstrom-theorem-September-24-2026/build/assembly.tex#L179-L244)).
- **Partial value.** σ ≈ 5.6×10⁻⁴, so C ≥ 3554·A₀ with D* ≥ 1.
- **Unquantified part.** A₀ > c₁√C_φ (from survival.tex), and C_φ is never given a number.
- **Rough size.** If C_φ ≥ 1 then c₁ > 2.96 and C ≳ 10⁴.

### 089 — L1 embeddings of planar and bounded-treewidth graphs (Lean-formalized)

**Planar case:**
- **Distortion formula.** C = 16m/(pb) with p = 2^−(2M_pack+10) ([assembly.tex L56-60, L268-273](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Planar-Graph-Metrics-Embed-into-L1-with-Constant-Distortion-September-23-2026/build/sections/assembly.tex#L56-L273)).
- **The term M_pack.** M_pack = 2 + ⌈1600R/g⌉ ([main-packing.tex L330-339](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Planar-Graph-Metrics-Embed-into-L1-with-Constant-Distortion-September-23-2026/build/sections/main-packing.tex#L330-L339)), with R = 10⁻⁸ and g = 10⁻¹⁴ ([scale-setup.tex L30-35](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Planar-Graph-Metrics-Embed-into-L1-with-Constant-Distortion-September-23-2026/build/sections/scale-setup.tex#L30-L35)).
- **Value.** M_pack ≈ 1.6×10⁹, so **C ≥ 2^(3.2×10⁹) ≈ 10^(9.6×10⁸)**.
- **Triage correction.** The triage's "~10⁶⁰" is wrong by roughly 10⁹ orders of magnitude.

**Treewidth case.** C_k comes from a compactness argument, "without an explicit estimate".

**Flow–cut consequence.** It holds via Gupta–Newman–Rabinovich–Sinclair (GNRS) Thm 3.2, with the same constants.

## Current practice & state of the art

### Hyperbolic programming (095)

**Solvers that support it natively:**
- **DDS 3.0** (Karimi–Tunçel, MATLAB). It accepts `'HB'` constraints given as a monomial list, a straight-line program, or a determinantal pencil ([HB_Different_Formats.m L18-80](https://github.com/mehdi-karimi-math/DDS/blob/c4dc57d6b4f0435ab6ff9258ffa7e0a33cd0d6c7/Test_Examples/hyperbolic-program/HB_Different_Formats.m#L18-L80)). The solver ships as MATLAB p-code (`Solver/*.p`, closed), so I could not run it here.
- **DDS 3.0 benchmarks.** The DDS 3.0 paper (arXiv 2602.23260) benchmarks:
  - elementary-symmetric cones;
  - Vamos-like cones;
  - composite cones;
  - products of linear forms.
  These live in a public library ([LMCO/Hyperbolic Programming](https://github.com/mehdi-karimi-math/Library-for-Modern-Convex-Optimization/tree/b9a92607d160b16bd5e02d045ebb3e9cef501c62/Hyperbolic%20Programming)). Its only "SDP" baseline is the growing-size spectrahedral representation of derivative relaxations. **No concrete applications are given.** Its argument for native solvers is that SDP pencils get too large, not that SDP representations cannot exist.
- **Hypatia.jl.** No hyperbolic cone ships. It has a generic primal-barrier oracle interface (feasibility check, gradient, Hessian, third-derivative oracle `dder3`) ([Cones.jl L63-141](https://github.com/jump-dev/Hypatia.jl/blob/fcb279a246294c7198eb8af9ed1f46ded02996a3/src/Cones/Cones.jl#L63-L141)), so a hyperbolic cone could be added.
- **alfonso** (Papp–Yıldız). It takes generic barrier oracles.
- **Research first-order codes.** Renegar's hyperbolic first-order methods, and dual Frank–Wolfe projection (arXiv 2407.09213).
- **No support.** Clarabel and SCS: Clarabel's Python module exposes only the Zero, Nonnegative, SOC, Exp, Power, GenPower and PSD cones, and SCS supports no hyperbolic cone. MOSEK does not support it either.

**Known liftable classes.** Derivative relaxations of spectrahedral cones have polynomial-size SDP lifts (Saunderson–Parrilo, arXiv 1208.1443). Elementary-symmetric cones are spectrahedral (Brändén, cited in the paper). No cone that arises in practice is known to lack a lift.

### Bin packing / cutting stock (118)

**Known gaps:**
- **Largest known.** The largest known non-proper gap is 6/5. The largest known proper gap is 1.0625 (17/16) per Kartak et al., arXiv 1405.5988, raised to 1.1 (11/10) by Kartak–Ripatti (JOGO 2019).
- **Smallest non-IRUP.** Proper non-IRUP instances first appear at n = 10.
- **Status before this paper.** MIRUP was described as "still widely open" and a gap ≥ 2 was unknown.
- **Benchmarks.** Arc-flow/VPSolver work (arXiv 1310.6887) reports that most benchmark instances have IRUP and none violates MIRUP. The largest gap it found was 1.0027 (excluding the divisible case), and 5 of the 28 Hard28 instances are non-IRUP.

**How solvers use the bound.** Exact solvers use ⌈LP⌉ as a lower bound. It is always valid, and when an incumbent matches it the solver stops early. VPSolver's source has no IRUP/MIRUP logic (grep of `src/`, `pyvpsolver/` at [c01e1d3](https://github.com/fdabrandao/vpsolver/tree/c01e1d38a12ec25a6398aa36c7629bb2ceca8404)).

**Hard instances.** BPPLIB's AI/ANI classes were designed to defeat methods that exploit IRUP. A 2026 paper (arXiv 2604.05152) gives polynomial and pseudo-polynomial algorithms for those classes. 13 of the 500 AI/ANI instances were still unsolved within standard time limits.

### Superstrings and dictionaries (128)

**zstd ([49cf517](https://github.com/facebook/zstd/tree/49cf51799ea051457f57243527aa2058f999f005)) builds dictionaries for coverage, not superstrings:**
- **COVER scoring.** `COVER_selectSegment` scores each k-window as the sum of frequencies of its distinct d-mers. It then trims zero-frequency ends and zeroes the frequencies of covered d-mers ([cover.c L481-569](https://github.com/facebook/zstd/blob/49cf51799ea051457f57243527aa2058f999f005/lib/dictBuilder/cover.c#L481-L569)).
- **COVER assembly.** `COVER_buildDictionary` takes one best segment per epoch and `memcpy`s segments back to front with no overlap handling ([cover.c L751-807](https://github.com/facebook/zstd/blob/49cf51799ea051457f57243527aa2058f999f005/lib/dictBuilder/cover.c#L751-L807), memcpy at L799).
- **FASTCOVER.** Same logic over hashed d-mers ([fastcover.c L137-219](https://github.com/facebook/zstd/blob/49cf51799ea051457f57243527aa2058f999f005/lib/dictBuilder/fastcover.c#L137-L219), [L391-453](https://github.com/facebook/zstd/blob/49cf51799ea051457f57243527aa2058f999f005/lib/dictBuilder/fastcover.c#L391-L453), memcpy at L445).
- **Default trainer.** `ZDICT_trainFromBuffer` is FASTCOVER with d = 8 and steps = 4 ([zdict.c L1111-1127](https://github.com/facebook/zstd/blob/49cf51799ea051457f57243527aa2058f999f005/lib/dictBuilder/zdict.c#L1111-L1127)).
- **Legacy trainer.** It merges candidates only when they overlap at sample positions ([zdict.c ZDICT_tryMerge L356-416](https://github.com/facebook/zstd/blob/49cf51799ea051457f57243527aa2058f999f005/lib/dictBuilder/zdict.c#L356-L416)).
- **Verdict on the triage.** Confirmed: the objective is coverage under a byte budget, not superstring length.

**k-mer superstring tools:**
- **KmerCamel ([474ea89](https://github.com/OndrejSladky/kmercamel/tree/474ea890c5f09aea1bf04f5ca2b5c6f98a299e5a)).** It already ships a lower bound: `kmercamel lowerbound` computes the shortest cycle cover on the overlap graph using the greedy routine with cycle-forbidding disabled ([lower_bound.h L7-37](https://github.com/OndrejSladky/kmercamel/blob/474ea890c5f09aea1bf04f5ca2b5c6f98a299e5a/src/lower_bound.h#L7-L37); [global.h L38-133, flag at L95-97](https://github.com/OndrejSladky/kmercamel/blob/474ea890c5f09aea1bf04f5ca2b5c6f98a299e5a/src/global.h#L38-L133)).
- **ProphAsm2 ([f7b520b](https://github.com/prophyle/prophasm2/tree/f7b520b407a8de814a83fc05adf485cc210652f1)).** It computes simplitigs/SPSS (spectrum-preserving string sets), not superstrings, and has no lower-bound facility.

### Crossing numbers (165)

**OEIS A000241.** It lists terms up to n = 14; a(13) and a(14) were added in April 2024 from Aichholzer's computations. It cites Pan–Richter's bounds 0.8594·Z(n) ≤ a(n) ≤ Z(n), and has **no 2026 edit marking the formula proved**.

**OGDF ([1a40505](https://github.com/ogdf/ogdf/tree/1a40505ac00677a58ab5ce532e1dcc3bd63116e5)):**
- **Exact-value tests.** The crossing-minimizer tests assert exact values for K4–K6, K3,3, K4,3 and K4,4.
- **Heuristic tests.** Heuristics only get the assertion `actual ≥ expected`, with K10 checked at ≥ 60 ([crossing-minimizer.cpp L128-163, L172-291](https://github.com/ogdf/ogdf/blob/1a40505ac00677a58ab5ce532e1dcc3bd63116e5/test/src/planarity/crossing-minimizer.cpp#L128-L291)).

**Chimani et al. "Star-Struck" (arXiv 2108.11443).** It benchmarks on **Complete** (K₅–K₅₀, 46 graphs) and **Complete-Bip.** (K_{n1,n2} with 5 ≤ n1, n2 ≤ 40, 666 graphs). Quality is measured against the best solution found, not a known optimum. KnownCR contains no complete graphs.

**Rectilinear crossing numbers.** For straight-line drawing tools these matter, and they remain open beyond small n.

### IP proximity and sparsest cut (097, 089)

**IP proximity (097):**
- **Eisenbrand–Weismantel.** Their DP uses the ℓ∞ Steinitz bound.
- **Jansen–Rohwedder.** They reach (√m·Δ)^{2m} via discrepancy.
- **Aliev–Averkov–Jones–Oertel (arXiv 2606.13579).** They prove an asymptotically tight Euclidean proximity bound √det(AAᵀ) − 1 without any Steinitz lemma.

**Sparsest cut / partitioning (089):**
- **Production partitioners.** METIS, KaHIP and Scotch are heuristics.
- **Theory for planar graphs.** Rao's O(√log n) embedding, and quasi-polynomial (2+ε)-approximations for planar sparsest cut.

## Opportunities

### OPT-1 (095, INSTANCES): ship the explicit cone and its exact lift as a paired solver test instance

- **Proposed change.** Add the 23-variable, degree-16 cone q and its exact 100×100 lift as a paired instance in two places:
  - Karimi's hyperbolic-programming benchmark library ([LMCO/Hyperbolic Programming](https://github.com/mehdi-karimi-math/Library-for-Modern-Convex-Optimization/tree/b9a92607d160b16bd5e02d045ebb3e9cef501c62/Hyperbolic%20Programming));
  - Hypatia.jl, as a custom-cone example using the oracle interface ([Cones.jl L63-141](https://github.com/jump-dev/Hypatia.jl/blob/fcb279a246294c7198eb8af9ed1f46ded02996a3/src/Cones/Cones.jl#L63-L141)).

  It is the only known cone that is provably not spectrahedral yet has a certified exact lift, so native and lifted solves must agree exactly. That makes it a correctness test.
- **Format note.** q is not a linear determinantal form, because Q(y) is quadratic in y. DDS's `'determinant'` format therefore does not apply directly. A straight-line program needs a division-free determinant (Berkowitz, 16×16).
- **Benefit.** A correctness and conditioning test for hyperbolic solvers and moment-lift code. The lifted optimum is degenerate (rank 25 of 100), which stresses SDP solvers.
- **How to measure.** Agreement of the two objectives, iteration counts, and solver status flags. My numbers are below.
- **Risks.** The audience is one or two research groups. The instance proves nothing about scale.
- **First step.** Code is ready in `/home/claude/work/repos/scratch_optimization/hyp_cone.py` (polynomials, slice pencil, lift builder) and `bench_hyp.py`. Port it to MATLAB `.mat` files in the LMCO format.

### OPT-2 (118, REDIRECT/CERTIFY): one-paragraph updates to textbooks, surveys and benchmark docs

- **Proposed change.**
  - Williamson–Shmoys Ch. 17, Problem 3 (OPT + C algorithms): answered negatively, conditional on P ≠ NP.
  - Scheithauer–Terno MIRUP: false, and the gap is unbounded.
  - Surveys (Delorme–Iori–Martello; BPPLIB docs; VPSolver papers) that state MIRUP as an open conjecture should add a note.
- **Who benefits.** Researchers stop pursuing OPT + O(1) polynomial-time algorithms. Hoberg–Rothvoss's O(log OPT) additive bound stays the best known, and nothing rules out log-type lower bounds.
- **No solver change.** ⌈LP⌉ is still a valid bound and IRUP still holds empirically. The counterexamples cannot be written down, and the hardness needs exponentially large denominators, so it does not cover poly-capacity instances.
- **How to measure.** Errata or editions issued; citations.
- **Risks.** None. The result is Lean-checked.
- **First step.** A short note to the cutting-stock community (Scheithauer, Kartak, Rietz) and to the BPPLIB maintainers.

### OPT-3 (118, RESEARCH): find the smallest instance with OPT − LP ≥ 2

- **What it is.** Now that MIRUP is known false, "how small is the smallest witness?" is a well-posed open question. The construction gives no usable upper bound (its size is a tower).
- **Starting point.** The empirical record is 6/5 (non-proper). Kartak–Ripatti's search heuristics are the natural tool.
- **Is it a real research item?** Yes for combinatorial-optimization theory. **No** for practice: even a moderately sized witness would not change solver design, because ⌈LP⌉ is only used as a lower bound.
- **Verdict.** Pursue as research, low priority.

### OPT-4 (165, CERTIFY/INSTANCES): proven optima for crossing-number data and benchmarks

- **Proposed change.**
  - **OEIS.** Edit A000241 (and the K_{n,n}/K_{m,n} sequences) to "formula proved for all n", citing the Lean-checked theorem. I could not check the exact Zarankiewicz sequence numbers because the web-search budget ran out.
  - **Benchmarks.** In the Star-Struck "Complete" (46) and "Complete-Bip." (666) sets, report heuristic gaps to the *proven optimum*.
  - **OGDF tests.** Extend the `!IsLessThan(expected)` sanity checks to K_n and K_{m,n} for any n using Z(n). A heuristic returning fewer crossings than Z(n) now proves a bug in `verifyCrossings` or the planarization.
- **Benefit.** Certification of reference data. It is cheap and permanent.
- **Risks.** Low value. Heuristics already matched the Z(n) upper bound, and the result does not cover rectilinear crossings.
- **First step.** The OEIS edit, plus an OGDF pull request adding K₁₅/K_{10,12} lower-bound tests.

## What is NOT an opportunity here (and why)

**095:**
- **"Not every hyperbolic program compiles to SDP" does not drive solver roadmaps.** The only proven non-liftable cone has about 6.7×10¹⁰ variables and degree about 6.7×10¹⁰. Every hyperbolic cone used in practice or benchmarks is liftable, or its lift is merely large. DDS 3.0 already argues for native solvers on lift size, not existence. No one at MOSEK, Clarabel or SCS faces this decision.

**118:**
- **Using the construction as benchmark instances:** impossible; the tree depth is a tower.
- **Changing branch-and-price or arc-flow stopping rules:** nothing in them relies on MIRUP.

**128:**
- **zstd dictionary building.** Measured: superstring-merging COVER's or FASTCOVER's segments saves at most 1.06% or 1.29% of the dictionary, by a cycle-cover lower bound. Plain greedy already achieves 1.05% and 1.29%. A 2-approximation adds nothing; the objective is coverage.
- **W as a certificate in k-mer tools.** On real bacterial k-mer sets, W equals KmerCamel's existing cycle-cover bound exactly, and the period rule never raises a count. It adds at most 0.3% on subsampled repeat-heavy synthetic sets, at roughly 1000× the cost (Python prototype). Keep it only as a monitor item for extremely repetitive sequence such as satellite arrays.
- **The full 2-approximation algorithm.** Greedy is near-optimal on these instances, and a C++ implementation of all of it is a large effort.

**165:**
- **VLSI, photonic or layout design changes.** Multilayer layouts make crossings free, and straight-line drawings use the different, unsettled rectilinear crossing number.

**097:**
- **No IP-proximity or flow consequence with explicit constants.** The constant C ≳ 3.5×10³·A₀ has A₀ unquantified. An ℓ₂-ball DP beats the ℓ∞ Steinitz bound m·Δ only when √m > C·Δ₂/Δ, which means **m > C² ≳ 10⁷ constraints**, far outside where (Δm)^m DPs run. Aliev et al. 2026 already give the optimal Euclidean proximity. The result is also non-algorithmic, so it does nothing for online balancing.

**089:**
- **Flow–cut gap and partitioning.** The planar distortion is ≥ 10^(9.6×10⁸) and C_k is non-explicit. Rao's O(√log n) is smaller for every physically possible n, and production partitioners are heuristics.

## Experiment results

Note on timings: the machine has 2 cores shared with other agents (load average about 13–15), so wall times are noisy. Iteration counts are reliable.

### E1 (095) — Native barrier vs exact SDP lift

Scripts: `hyp_cone.py`, `bench_hyp.py`, `ray_test.py`, `ray_test2.py`, `slater.py`, `lift_rank.py`, `lift_cmp.py`.

**Identities hold.**
- p/(det X · q) = 1 ± 10⁻¹⁴.
- det L_θ / p = 1 ± 2×10⁻¹⁴ on random slices.
- p(e) = q(e) = 1.

**The lift as built:**
- 330 coefficient matrices, 23 output coordinates fixed.
- 204 coefficient matrices are nonzero, so only 181 of the 307 auxiliary variables appear. The trimmed version gives the same optima.
- The lift has a strictly feasible point: at x = e the best attainable minimum eigenvalue of H is 0.5.

**The lift is exact (ray tests).** I compared the boundary along random rays from interior points, using the 20×20 slice pencil with bisection as ground truth.
- 25 random rays: max relative error 1.0×10⁻⁵, median 2.6×10⁻⁷.
- 3 rays that exit through singular-X boundary points (y = 0): relative error ≤ 3×10⁻⁸.
- 3 further rays with y ≠ 0 that exit at nonsingular X: relative error ≤ 1.5×10⁻⁶.
- This is numerical support for the unformalized lift paper, including its boundary behavior at singular X.

**Benchmark setup.** 19 random instances of min cᵀx subject to tr X + tr Z = 1, three random equalities, and x ∈ K.
- **Native:** my primal barrier path-following solver with barrier −log q (barrier parameter ν = 16), using JAX autodiff for the gradient and Hessian. DDS could not be run because it needs MATLAB.
- **Lift:** the 100×100 lift solved with Clarabel 0.11.1 and SCS 3.3.1 through cvxpy 1.9.3.

| method | median iters | median solve time | status | max objective difference vs native |
|---|---|---|---|---|
| native barrier (−log q, ν = 16) | 71 Newton steps | 0.20 s | 19/19 converged, ‖Ax−b‖ ~ 1e-16 | — |
| Clarabel on 100×100 lift | 9 IPM iterations | 2.5 s | 18/19 `optimal_inaccurate` | 3.9e-7 |
| SCS on 100×100 lift | 225 | 0.74 s | 19/19 optimal | 3.1e-7 |

**Takeaways:**
- **Numerical conditioning.** At the optimum the lifted moment matrix has numerical rank 25 of 100. This degenerate optimal face is the likely reason Clarabel reports "inaccurate" while still landing within 4×10⁻⁷.
- **Speed.** At this size both routes work. The native barrier was faster here, but nothing practical hinges on it.

### E2 (128) — zstd segments: how much a superstring merge could save

Scripts: `ztrain.c` linked against a copy of zstd's lib with segment logging; `seg_overlap.py`.

**Setup.** Training corpus: 1,278 OGDF C++ source and header files (17.8 MB). Dictionary: 112,640 bytes, k = 200, d = 8.

| builder | segments | median length | contained-segment bytes | greedy-SCS saving | cycle-cover bound on any saving |
|---|---|---|---|---|---|
| COVER | 567 | 200 | 22 B | 1,164 B (1.05%) | ≤ 1.06% |
| FASTCOVER | 564 | 200 | 0 | 1,452 B (1.29%) | ≤ 1.29% |

**Conclusion.** Greedy is within 7 bytes of the bound. There is no room for a better approximation algorithm, and about 1% of the budget is the most that could ever be freed.

### E3 (128) — Greedy vs cycle-cover bound vs the paper's W on k = 31 k-mer sets

Scripts: `scs_W.py`, `kmer_exp.py`, `tiny_opt.py`, `synth_ub2.py`.

**My implementation of W.** It follows the full rule set of 02-counts.tex: extension rules, plus period rules over all periods p, all k, and the blocking functional. Validation:
- 2,342 tiny repeat-rich instances checked against exact OPT (Held–Karp): **0 violations of W ≤ OPT**.
- It reproduces the paper's a^h example (W = h).
- Without the period rule, W equals the assignment cycle-cover bound on all 1,169 test instances.
- With the period rule, W beats the cycle-cover bound on 134 of 2,342 instances (5.7%) and is never below it. W = OPT on 1,606 instances, versus 1,510 for the cycle-cover bound.

**Real data.** S. pneumoniae ATCC 700669 (NC_011900.1, bundled in KmerCamel `data/`), first 100 kb. Greedy is KmerCamel 474ea89 `compute -u`; its lower bound is `lowerbound -u`.

| set | k-mers | greedy | cycle-cover LB | W | gap greedy vs best LB | W time (Python) | cycle-cover time |
|---|---|---|---|---|---|---|---|
| 100 kb, all | 99,210 | 99,602 | 99,590 | 99,590 | 0.012% | 317 s | 0.10 s |
| 100 kb, 50% | 49,605 | 99,580 | 99,569 | 99,569 | 0.011% | 349 s | 0.48 s |
| 100 kb, 20% | 19,842 | 99,297 | 99,295 | 99,295 | 0.002% | 426 s | 0.31 s |
| 100 kb, 10% | 9,921 | 93,085 | 93,085 | 93,085 | 0% | 438 s | 0.32 s |
| synthetic tandem repeats | 4,899 | 5,705 | 5,071 | 5,071 | 12.5% | 123 s | 0.06 s |
| synthetic tandem, 30% | 1,469 | 5,135 | 4,955 | **4,969** | 3.3% | 83 s | 0.07 s |

**Findings:**
- **On genome data,** the period rule never raises a count. W equals the existing bound and costs about 1000–3000× more (in Python; C++ would narrow that, but W stays strictly heavier).
- **Incidental finding, not from the paper.** On the synthetic tandem-repeat set, OPT is pinned to [5,071, 5,072]: I built an explicit 5,072-base superstring by collapsing repeat copies. KmerCamel's greedy (5,705) is therefore **12.5% above optimum**, and greedy-ac (5,543) 9.3% above. KmerCamel's *own* cycle-cover bound already certifies this gap. It would make a useful hard-instance report to KmerCamel's authors, but the paper's W adds nothing to it.

## Sources

**Papers and preprints:**
- [Kartak, Ripatti, Scheithauer, Kurz — Minimal proper non-IRUP instances of the 1D cutting stock problem (arXiv 1405.5988)](https://arxiv.org/abs/1405.5988)
- [Kartak & Ripatti — Large proper gaps in bin packing and dual bin packing problems (JOGO 2019)](https://ideas.repec.org/a/spr/jglopt/v74y2019i3d10.1007_s10898-018-0696-0.html)
- [Brandão & Pedroso — Bin packing and related problems: general arc-flow formulation with graph compression (arXiv 1310.6887)](https://arxiv.org/pdf/1310.6887)
- [Polynomial and pseudopolynomial algorithms for two classes of bin packing instances (arXiv 2604.05152)](https://arxiv.org/abs/2604.05152)
- [Karimi & Tunçel — Efficient interior-point methods for hyperbolic programming via straight-line programs (arXiv 2602.23260)](https://arxiv.org/html/2602.23260v1)
- [Projection onto hyperbolicity cones: a dual Frank–Wolfe approach (arXiv 2407.09213)](https://arxiv.org/pdf/2407.09213)
- [Saunderson & Parrilo — Polynomial-sized semidefinite representations of derivative relaxations of spectrahedral cones (arXiv 1208.1443)](https://arxiv.org/pdf/1208.1443)
- [Papp & Yıldız — alfonso: Matlab package for nonsymmetric conic optimization (arXiv 2101.04274)](https://arxiv.org/pdf/2101.04274)
- [Clancy, Haythorpe, Newcombe — A survey of graphs with known or bounded crossing numbers (arXiv 1901.05155)](https://arxiv.org/abs/1901.05155)
- [Chimani et al. — Star-Struck by Fixed Embeddings: modern crossing number heuristics (arXiv 2108.11443)](https://arxiv.org/pdf/2108.11443v3)
- [Aliev, Averkov, Jones, Oertel — Optimal proximity bound and product function estimates in ILP (arXiv 2606.13579)](https://arxiv.org/abs/2606.13579)

**Data and tools:**
- [OEIS A000241](https://oeis.org/A000241)
- [BPPLIB](https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library)

**Code (pinned):**
- zstd [49cf517](https://github.com/facebook/zstd/tree/49cf51799ea051457f57243527aa2058f999f005)
- DDS [c4dc57d](https://github.com/mehdi-karimi-math/DDS/tree/c4dc57d6b4f0435ab6ff9258ffa7e0a33cd0d6c7)
- LMCO [b9a9260](https://github.com/mehdi-karimi-math/Library-for-Modern-Convex-Optimization/tree/b9a92607d160b16bd5e02d045ebb3e9cef501c62)
- Hypatia.jl [fcb279a](https://github.com/jump-dev/Hypatia.jl/tree/fcb279a246294c7198eb8af9ed1f46ded02996a3)
- KmerCamel [474ea89](https://github.com/OndrejSladky/kmercamel/tree/474ea890c5f09aea1bf04f5ca2b5c6f98a299e5a)
- ProphAsm2 [f7b520b](https://github.com/prophyle/prophasm2/tree/f7b520b407a8de814a83fc05adf485cc210652f1)
- VPSolver [c01e1d3](https://github.com/fdabrandao/vpsolver/tree/c01e1d38a12ec25a6398aa36c7629bb2ceca8404)
- OGDF [1a40505](https://github.com/ogdf/ogdf/tree/1a40505ac00677a58ab5ce532e1dcc3bd63116e5)

**Paper sources:** openai/math [fd4aeeb](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb), preprint directories as linked above.
