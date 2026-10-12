# Sharp analytic constants for numerics and statistics (families 325, 374, 101, 093, 140, 119, 229, 222)

**Bottom line.** None of these eight families changes any production code path. Every applied effect is a sharper constant or exponent in a worst-case a-priori guarantee, and the software we inspected uses a-posteriori stopping rules that never read those constants. The most valuable item is in 325, the complete Crouzeix theorem. Only the drop's matrix-coefficient version gives the sharp constant 4 (previously 5.83) in the Crouzeix–Kressner bound for bivariate matrix functions and Fréchet derivatives. It also gives 2 (previously 2.414) for block and matrix-polynomial GMRES. All of this is worth a short certify note, plus a Mathlib formalization, and nothing more. On GMRES iteration counts the change is about 1%. For the matrix exponential, the classical logarithmic-norm bound already has constant 1. Of the rest: 374 gives the sharp worst-case stability exponent for semi-discrete and LOT map estimators, but its explicit constant makes any numeric certificate vacuous. 101's per-dimension 0.604-bit gap is correct and new for vectors, but the scalar case was already published. 093 is a non-explicit-constant theory result for samplers. 140, 119, 229 and 222 confirm what practitioners already assume. 229 is the one with a crisp new interpretive consequence: it pins the Jukes–Cantor ancestral-reconstruction phase transition exactly at the Kesten–Stigum point.

## What the papers actually prove

Repository pinned at openai/math `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` (permalinks below use `OM` = `https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints`).

### 325: the complete Crouzeix theorem (Lean-formalized)
- **Cor. `cor:polynomial`** ([OM/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex#L1075-L1086](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex#L1075-L1086)): for every A in M_n and every matrix polynomial P(z)=Σ B_j z^j with B_j in M_m, ‖Σ A^j⊗B_j‖ ≤ 2·max over W(A) of ‖P(z)‖. The bound is uniform in n, m and degree, and 2 is sharp (2×2 Jordan block).
- **Cor. `cor:hilbert`** ([#L1175-L1209](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex#L1175-L1209)): the same holds for bounded operators on any Hilbert space and for matrix-valued holomorphic or rational F near the closure of W(A). The closure of W(A) is a complete 2-spectral set.
- **Thm. `thm:structural`** ([#L108-L130](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex#L108-L130)): this part is constructive. Take an admissible analytic convex Ω containing W(A), with conformal map f: Ω→D. The LMI min{τ : I ⪯ H ⪯ τI, f(A)\*H f(A) ⪯ H} is attained, and its value κ² is at most 4. S = H^{1/2} makes f(SAS⁻¹) a contraction with cond(S) = κ ≤ 2. This gives a per-matrix certified constant κ(A,Ω) that is computable by SDP.
- **Status of the scalar case.** Scalar constant 2 was obtained independently by humans. Lorist–Schwenninger posted arXiv 2608.03841 on Aug 4 2026 (v2 Aug 17). Their Theorem 3 covers bounded Hilbert-space operators and rational f. Their Section 3(iv) says the commutation step in Lemma 1 does not pass to the completely bounded (matrix-coefficient) case. Jin (preprints.org 202607.1919, July 27 2026) and Luo (Aug 28) also give scalar proofs. Åhag–Czyż–Virtanen prove the complete case only for n ≤ 3. **What is unique to the drop is the complete case in all dimensions, the Lean formalization, and the optimal-similarity theorem.** One caveat: Badea–O'Loughlin–Virtanen (arXiv 2609.03637, Sept 3) prove the abstract Clouâtre–Ostermann–Ransford version. Its abstract does not say whether it yields the complete bound, so check this before claiming uniqueness publicly.

### 374: sharp one-third stability of Brenier maps (Lean-formalized statement and sharpness)
- **Thm. `main:stability`** ([OM/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/introduction.tex#L31-L41](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/introduction.tex#L31-L41)): let ρ be uniform on a compact convex body K in ℝ^d with d ≥ 2, and let the targets be any Borel probability measures on a fixed compact Y (atomic allowed). Then ‖T_μ − T_ν‖_{L²(ρ)} ≤ C(K,Y)·W₂(μ,ν)^{1/3}.
- **Explicit constant**, Cor. `gradient:finite` ([gradient.tex#L99-L111](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/gradient.tex#L99-L111)): C\* = (12dR²(1+√162)² + 28L²P_K/|K|)^{1/2}, where K ⊂ B(0,R), Y ⊂ B(0,L), R,L ≥ 1, and P_K is the sum of the coordinate-projection volumes.
- **Key intermediate step**, Prop. `finite:potentials` ([finite_stability.tex#L8-L23](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/finite_stability.tex#L8-L23)): the Brenier potentials are linearly stable, ‖u₀−u₁‖ ≤ (1+√162)R·W₂.
- **Sharpness**, Prop. `sharpness:exponent` ([sharpness.tex#L51-L61](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/sharpness.tex#L51-L61)): an explicit three-atom family on [−1,1]^d rules out every exponent above 1/3, which disproves Letrouit's conjectured square-root bound.
- **Prior target-uniform bounds:** W₁^{2/15} (Mérigot–Delalande–Chazal 2020), W₁^{1/6} (Delalande–Mérigot 2023), and a sharp W₁^{1/4} attributed to Mérigot (via Han–Zhu). There is also a W₂^{1/3} bound with atom-dependent constants (Divol–Niles-Weed–Pooladian).

### 101: sharp entropy bound and the simplex inequality (not formalized)
- **Thm. `intro:entropy`** ([OM/A-sharp-entropy-bound…/build/manuscript/introduction.tex#L75-L85](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-sharp-entropy-bound-and-the-simplex-inequality-for-isotropic-constants-October-5-2026/build/manuscript/introduction.tex#L75-L85)): every log-concave density on ℝ^m satisfies h(f) ≥ m + ½ log det Cov(f). Equality holds only for affine images of products of one-sided exponentials. There is no symmetry assumption and dependent coordinates are allowed.
- **The triage's corollary is correct.** A Gaussian with the same covariance has entropy (m/2)log(2πe) + ½ log det Cov. So D(f‖G) = h(G) − h(f) ≤ m(½log(2πe) − 1) = 0.418939·m nats = **0.604401 bits per dimension**, and this is sharp.
- **Vector consequences (my derivation, standard steps).** For additive log-concave noise Z with any covariance, C_Z(P) ≤ C_{G_Z}(P) + 0.604·m bits, where G_Z is the Gaussian with the same covariance (colored water-filling), and C_Z ≥ C_{G_Z} as usual. For MSE rate–distortion, R(D) − R_SLB(D) ≤ 0.604·m bits whenever the Gaussian of the same covariance meets its own SLB, i.e. D/m ≤ λ_min(Cov).
- **What is new and what is not.** The scalar version is not new. Melbourne–Nayar–Roberto (arXiv 2309.01840, PTRF 2026) proved h ≥ 1 + ½ log Var and stated the capacity corollary with the same ½log(2π/e) ≈ 0.42 nats gap (their Cor. 2.2). Comparing against "Marsiglietti–Kostina ~1.05 bits" therefore overstates the novelty. The vector version is new as an explicit sharp constant. Marsiglietti–Kostina's vector Theorem 4 needs symmetry and gives a per-dimension gap of ½log₂(2πe·c(n)) with c(n) = e²n²/(4√2(n+2)). That is 2.24 bits/dim at n=2, 3.77 at n=10, 7.2 at n=1000, or 2.99 bits/dim for unconditional laws. After Klartag–Lehec (2025), a dimension-free per-dimension gap followed with a non-explicit constant.

### 093: dimension-free log-Sobolev inequality for subgaussian log-concave measures (not formalized)
- **Thm. `thm:main`** ([OM/A-dimension-free-logarithmic-Sobolev…/build/sections/01-introduction.tex#L26-L36](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-dimension-free-logarithmic-Sobolev-inequality-for-subgaussian-log-concave-measures-September-23-2026/build/sections/01-introduction.tex#L26-L36)): if μ is centered log-concave with sup_θ E exp(⟨X,θ⟩²/a²) ≤ 2, then Ent(f²) ≤ C·a²∫|Df|². The corollary gives T₂ with the same C.
- **The constant is not explicit.** The proof assumes a sequence of counterexamples and derives a contradiction ([03-critical.tex#L1-L3](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-dimension-free-logarithmic-Sobolev-inequality-for-subgaussian-log-concave-measures-September-23-2026/build/sections/03-critical.tex#L1-L3); the contradiction closes in 07-observations.tex). No numerical C can be read off.
- **Previous LSI coefficients:** order n·a² (Bobkov) and √n·a² (Bizeul).

### 140, 119, 229, 222 (short)
- **140**, Thm. `h:main`: with A·d² bits of memory, recovering a unit vector needs T ≥ c_A·d·log(1/ε) noiseless Gaussian samples. The subsphere paper's Thm. `s:main` makes this explicit for o(d²) memory: T ≥ 2^{-16}·d·log₂(1/ε). Both are Lean-formalized.
- **119**: the Courtade–Kumar inequality I(f(X);Y) ≤ 1 − h(ε) is Lean-formalized. The Hellinger version (all biases) is not. **An independent computer-assisted, Lean-verified human proof** appeared earlier: Chen, Gohari, Javanmard, Lin, Mirrokni, Nair, Woodruff, arXiv 2609.24931, submitted Sept 21 2026, three days before the drop's Sept 24 paper.
- **229**:
  - Three-state symmetric channel (Thm. `thm:threshold`): reconstruction happens iff dλ² > 1, for regular b-ary trees (b ≥ 2) and Poisson trees (d > 1), for both signs of λ.
  - SBM corollary (Cor. `cor:sbm`): three symmetric communities are weakly recoverable iff (a−b)² > 3(a+2b), in O(n log n) time above the threshold.
  - Ferromagnetic four-state model (Thm. `thm:main`): non-reconstruction holds at and below dλ² = 1, for all d ≥ 2 regular and all Poisson d > 0. A companion paper gives an L³-capacity criterion on arbitrary bounded-degree trees.
  - The non-reconstruction direction is computer-assisted with exact arithmetic. Lean covers only the classical supercritical direction for three states.
- **222**:
  - Variational free-energy formulas for Ising and spherical perceptrons, for bounded potentials at positive temperature and every density. The spherical formula is Lean-formalized.
  - Certified jamming exponents γ ∈ (0.4126930, 0.4126934) and θ ∈ (0.4231063, 0.4231088).
  - The hard-constraint capacity is excluded.

## Current practice & state of the art

**Krylov methods and matrix functions.**
- Production codes stop on a-posteriori quantities, never on numerical-range bounds:
  - Krylov.jl block-GMRES stops on ‖R_k‖_F ≤ atol + rtol·‖R₀‖.
  - KrylovKit `exponentiate` uses an accumulated error estimate `normres`.
  - ExponentialUtilities uses the Niesen–Wright a-posteriori estimate.
  - funm_quad stops on update norms.
  - SciPy `expm_multiply` picks its degree and scaling from the Al-Mohy–Higham backward-error θ_m table and 1-norm estimates.
  - SciPy `expm_cond` forms the exact Kronecker Fréchet matrix.
- Field-of-values GMRES bounds are a teaching and analysis tool. Embree (*How descriptive are GMRES convergence bounds?*, arXiv 2209.01231) uses C = 1+√2. He shows the bound is sharp only for Jordan-like cases and is useless when 0 is in or near W(A).
- For convex W(A), Beckermann's Faber-polynomial route (‖F_k(A)‖ ≤ 2, C. R. Math. 2005) already gave a constant-2-type bound, with the (2+ρ_β)ρ_β^k disk-segment bound of Beckermann–Goreinov–Tyrtyshnikov.
- Crouzeix–Kressner (arXiv 2007.09784):
  - Thm. 3.1 bounds bivariate functions: ‖f{A,B}‖ ≤ (1+√2)² max over W(A)×W(B) of |f|.
  - The proof needs the complete (matrix-valued) version for one of the two variables.
  - Cor. 5.1 bounds the Fréchet derivative: ‖Df{A}‖ ≤ (1+√2)² max over W(A) of |f′|.
  - The nilpotent example A = B = J, f = xy forces a constant of at least 4.
- Kressner's bivariate Krylov paper (arXiv 1802.05759) uses M = 1+√2 (Lemma 4.2b) in prefactors 2M. It explicitly left open whether a constant like (1+√2)² works.
- Quantum eigenvalue processing (Low–Su, arXiv 2401.06240v3) has an Appendix B.2 titled "Matrix function bound with Crouzeix–Palencia theorem". I could not retrieve its body. The constant presumably sits in a normalization factor.

**Optimal-transport map estimation and LOT.**
- Practical semi-discrete solvers with a uniform convex source exist:
  - POT `solve_semidiscrete` and `semidiscrete_ot_map` offer built-in 'unif'-cube and 'ball' samplers and a hard Laguerre map when reg = 0.
  - pysdot (Newton on power diagrams) uses a unit box by default.
  - OTT-JAX has `SemidiscretePointCloud` and `SemidiscreteSolver`.
- All of them stop on marginal or weight errors and quote no map-error certificate.
- PyTransKit's `LinearOptimalTransport` uses a discrete reference point cloud with Sinkhorn/EMD and barycentric projection, so the theorem does not apply to it directly.
- Statistically, the regular-case minimax rates are much better: n^{-1/2} in the semi-discrete case (Pooladian–Divol–Niles-Weed, ICML 2023) and smoothness-dependent rates otherwise. No-assumption rates come from stability bounds: Cazelles–Pauwels–Portales (arXiv 2604.22366) give L¹ error (W₁)^{1/4}, an L² exponent of 1/5, and semi-discrete L¹ error (m/n)^{1/8}.
- LOT guarantees: Moosmüller–Cloninger give LOT ≈ W₂ up to Cε + C̄ε^{1/2} for perturbations of shifts and scalings.

**Log-concave sampling.**
- In-and-Out (Kook–Vempala–Zhang, NeurIPS 2024) states LSI-based iterations O(q·h⁻¹·C_LSI·log(log M/ε)) and Poincaré-based ones O(q·h⁻¹·C_PI·log(M/ε)) (Prop. 2).
- From a feasible cold start (Cor. 6) the cost is Õ(h⁻¹·C_LSI) with h ≈ d⁻².
- The only general geometric bound they use is C_LSI ≲ D², or ≲ D in isotropic position (Lemma 20).
- The headline theorems are stated with the covariance/Poincaré constant (KLS-type). Neither ψ₂ nor Bizeul's conjecture is mentioned.

**Information theory.**
- Marsiglietti–Kostina (Entropy 2018): scalar gap log√(πe/2) ≈ 1.05 bits. Their vector Thm. 4 needs symmetry and its constant grows with n.
- Melbourne–Nayar–Roberto (PTRF 2026): sharp scalar bound, plus the capacity corollary with gap 0.42 nats.

**Phylogenetics and community detection.**
- Steel's conjecture (O(log n) sites suffice iff branches are below the reconstruction threshold) is proved for CFN/Ising, where KS = reconstruction (Mossel 2004; Daskalakis–Mossel–Roch).
- For GTR models including JC69, O(log n) holds below KS (Roch). Above the true ancestral threshold g_ML, poly(n) sites are needed (Mossel–Roch–Sly).
- For JC, it was open whether g_ML = g_KS.
- SBM: the KS threshold was proved for q = 3, 4 only at large degree (Mossel–Sly–Sohn 2025). Large q is non-sharp (Sly 2011).

## Opportunities

### numstat-1 (325): restate the sharp numerical-range constants in docs, notes and teaching material (CERTIFY)
- **Change:** a 2–3 page note listing the constants.
  - Scalar a-priori bounds: the FOV GMRES constant becomes 2 (was 1+√2). Arnoldi f(A)b near-optimality becomes 2C = 4 (was 4.83). These are also covered by the human scalar proofs.
  - Matrix-coefficient (block) GMRES min–max over matrix polynomials: 2. Only the drop gives this.
  - Bivariate f{A,B} and Fréchet derivative (Crouzeix–Kressner Thm. 3.1 and Cor. 5.1): 4, sharp for bivariate f. Without the complete theorem one gets only 2(1+√2) = 4.83.
  - Kressner's Lemma 4.2(b) with one normal argument: M = 2.
- **Targets:**
  - The Chebfun example still says the conjecture is open with constant 11.08: [chebfun/examples linalg/Crouzeix.m#L36-L51](https://github.com/chebfun/examples/blob/f4b9ea46cfc2f52f20a844627f4a74d0bb10098c/linalg/Crouzeix.m#L36-L51). This is the only place in the cloned code where a Crouzeix constant appears at all.
  - Chebfun `fov.m` is the tool for evaluating the bounds: [chebfun fov.m#L1-L19](https://github.com/chebfun/chebfun/blob/7574c77680d7e82b79626300bf255498271a72df/fov.m#L1-L19).
  - Papers that carry the old constants: Crouzeix–Kressner (2007.09784), Kressner (1802.05759), Embree (2209.01231), Low–Su (2401.06240 App. B.2).
- **Benefit:** guarantee only. A ×0.828 factor in scalar bounds and ×0.686 in bivariate/Fréchet bounds. My experiment shows this saves about 1% of the iterations that a bound predicts (below).
- **Measurement:** the note is accepted, the Chebfun example updated, and the constants cited in the next survey or textbook edition.
- **Risks:** priority confusion with the human scalar proofs. Also, a possible complete-case result from Badea–O'Loughlin–Virtanen needs checking.
- **First step:** a PR to chebfun/examples updating Crouzeix.m. The 2×2 Jordan and A=B=J checks are in my scratch scripts.

### numstat-2 (325): the bivariate / Fréchet constant is now sharp at 4; find the true Fréchet-only constant (CERTIFY + small RESEARCH)
- **Change:** state ‖f{A,B}‖ ≤ 4·max over W(A)×W(B) of |f|, sharp by the nilpotent example (my check: ratio exactly 4.0000). Pose the open Fréchet-specific constant. Random search and the 2×2 Jordan block with f = z² give only √2 ≈ 1.41, so the sharp Fréchet constant lies in [√2, 4].
- **Who benefits:** condition-number theory for matrix functions without a semigroup structure: log, fractional powers, sign-type and rational functions. **Not the exponential.** There the logarithmic-norm (Van Loan-type) bound ‖L_exp(A)‖ ≤ e^{ω(A)} already has constant 1, and my table shows 4·e^{ω} is 4× looser.
- **Targets:** none in software. SciPy's `expm_cond` computes the exact Kronecker form ([_expm_frechet.py#L361-L420](https://github.com/scipy/scipy/blob/d1d4a8aa11723e6885f268a4106758d7917d5906/scipy/linalg/_expm_frechet.py#L361-L420)).
- **Risk:** the audience is small.
- **First step:** send a short note to Kressner and Crouzeix.

### numstat-3 (325): per-matrix certified spectral constants κ(A,Ω) via the structural LMI (RESEARCH / BENCHMARK)
- **Change:** solve min τ s.t. I ⪯ H ⪯ τI, f(A)ᵀH f(A) ⪯ H. This gives a matrix-specific constant κ ≤ 2 (often far below 2), together with a similarity certificate.
- **My SDP runs (cvxpy/SCS):** for shift matrices with Ω a disk slightly larger than W(A), κ = 1.77 (n=5), 1.44 (n=10), 1.21 (n=20), 1.08 (n=40). With a 5% larger disk, κ = 1.
- **Benefit:** tighter a-posteriori bounds for teaching and analysis.
- **Practicality:** poor. The SDP has n×n unknowns and costs O(n⁶) per solve, far more than solving the linear system. Useful only for n ≲ 100 analysis studies.
- **Risk:** the conformal map f is only easy for disks and ellipses.
- **Verdict:** monitor.

### numstat-4 (325): upstream numerical range and Crouzeix to Mathlib (FORMALIZE)
- Mathlib (checked at `d6416ab0f09d3a2e090f403fc80f37754f6181a9`) has no numerical-range definition. The drop ships a 0-sorry development: about 14k lines in `lean/OAI/Analysis/NumericalRange`, plus `DirectCrouzeix` and `HilbertCrouzeix`, on Lean v4.34.1.
- **Benefit:** formalization. It would be the first formal spectral-set library.
- **First step:** extract Toeplitz–Hausdorff convexity and W(A) basics as a Mathlib PR.

### numstat-6 (374): certify the sharp worst-case exponent for plug-in semi-discrete map estimators and LOT embeddings with a uniform convex reference (CERTIFY / REDIRECT)
- **Statements to adopt** (for ρ uniform on convex K and arbitrary compactly supported targets):
  - LOT sandwich: W₂(μ,ν) ≤ ‖T_μ − T_ν‖_{L²(ρ)} ≤ C\*·W₂(μ,ν)^{1/3}. The exponent 1/3 cannot be improved even for three-atom targets, so any uniform 1/2-type claim is false.
  - Plug-in rate: ‖T_{ν_n} − T_ν‖ ≤ C\*·W₂(ν_n,ν)^{1/3}. Jensen and Fournier–Guillin rates give E‖·‖ ≲ n^{-1/12} for d < 4 and n^{-1/(3d)} for d > 4, with no target regularity.
- **Comparison with earlier no-assumption bounds:**
  - Better than the W₁^{1/6} route for d ≥ 3.
  - Better than the W₁^{1/4} route for d ≥ 4. Tied at d = 3, and worse at d = 2 (n^{-1/12} vs n^{-1/8}), assuming that bound is in L² as the paper's comparison implies.
  - Still far below the regular-case n^{-1/2} semi-discrete rate.
- **Targets (docs only):**
  - POT semidiscrete: [samplers #L54-L82](https://github.com/PythonOT/POT/blob/604c47f28770eda10fe3cf0023c946d19c28e7ca/ot/semidiscrete.py#L54-L82), [hard map #L175-L248](https://github.com/PythonOT/POT/blob/604c47f28770eda10fe3cf0023c946d19c28e7ca/ot/semidiscrete.py#L175-L248).
  - pysdot default unit-box source: [OptimalTransport.py#L66-L78](https://github.com/sd-ot/pysdot/blob/840c92c2b144c9e779746e9a24ac44fb860cc88b/pysdot/OptimalTransport.py#L66-L78).
  - OTT `SemidiscretePointCloud`: [#L27-L47](https://github.com/ott-jax/ott/blob/36338c94707002772f2392ffa0a3acf11ab23857/src/ott/geometry/semidiscrete_pointcloud.py#L27-L47).
  - Not PyTransKit LOT, whose reference is discrete: [engine.py#L48-L105](https://github.com/rohdelab/PyTransKit/blob/aca79ee9fdf85ac3add8593e4ea5975654b725e2/pytranskit/optrans/lot/engine.py#L48-L105).
- **Benefit:** guarantee and research redirect. Stop pursuing uniform square-root stability, and state that LOT can distort small W₂ distances near fragile cell configurations.
- **Measurement:** survey or lecture-note tables updated.
- **Risk:** low impact, because practitioners do not consult these bounds.
- **First step:** a one-paragraph addition to the POT semidiscrete docstring "Notes", and a short survey note.

### numstat-8 (374): sharpen the constant (RESEARCH, monitor)
- C₀ = 162 is not optimized. On [−1,1]², C\* = 95.4, while the extremal three-atom family has ratio ‖ΔT‖/W₂^{1/3} = 0.630 ≈ 2^{-2/3} (my grid check). That gap is about 150×.
- Even with C\* = 1, the 1/6 power in any marginal-residual certificate keeps such certificates weak. So this only helps theory.

### numstat-9 (101): sharp vector log-concave entropy-gap corollaries (CERTIFY)
- **Statement:** for any log-concave noise or source vector (no symmetry, dependent coordinates allowed):
  - capacity gap to Gaussian of the same covariance ≤ 0.6044 bits/dim, sharp;
  - MSE rate–distortion gap to the Shannon lower bound ≤ 0.6044 bits/dim when D/m ≤ λ_min(Cov).
  This replaces Marsiglietti–Kostina's symmetric-only vector constants of 2.24–7.2+ bits/dim, which grow with n.
- **Tightness (my computation):** exponential noise with Gaussian input already achieves a gap of 0.6040 bits at P = 10 and 0.6044 at P ≥ 100. So the bound is attained asymptotically at high SNR.
- **Benefit:** a textbook-level guarantee. It is useful only when the noise law is unknown beyond log-concavity. For a known law, D(Z‖G) can be computed directly.
- **First step:** a 1-page note crediting Melbourne–Nayar–Roberto for the scalar case.
- **Risk:** the paper is unformalized. The exact-rational scalar certificate passes (I ran `verify_scalar.py`: ALL CHECKS PASSED), but the analytic parts are unchecked.

### numstat-11 (093): KL/Rényi mixing corollaries for ψ₂ log-concave targets (RESEARCH)
- **Corollaries to write down:**
  - In-and-Out from a feasible cold start on isotropic convex bodies with uniformly ψ₂ marginals: Õ(d²·C·a²) proper steps. Previously the only general bound was C_LSI ≲ D (Lemma 20), and D ≳ √d for isotropic bodies, so at best Õ(d^{2.5}); Bizeul's bound gave √d·a².
  - ULA/LMC in KL (Vempala–Wibisono) with κ_LSI = L·C·a² independent of d, for smooth ψ₂ log-concave potentials.
- **Practicality is limited:**
  - C is non-explicit, so no step counts can be certified.
  - Verifying ψ₂ for a given body is itself hard.
  - Cubes and products are already covered by tensorization.
  - Many practical targets (polytopes, logistic posteriors) are only ψ₁.
- **Verdict:** pursue as research, low priority.

### numstat-15 (229): exact KS thresholds as proven reference lines; Jukes–Cantor phase transition pinned (CERTIFY / RESEARCH)
- **Statement:** the four-state ferromagnetic channel P(j|i) = λ·1{i=j} + (1−λ)/4 is exactly the JC69 transition matrix, with λ = e^{−4t/3} and per-branch change probability p = 3(1−λ)/4.
  - Non-reconstruction at dλ² ≤ 1 means the deep-tree ancestral state is unrecoverable iff p ≥ (3/4)(1 − d^{−1/2}).
  - For binary trees: p\* = 0.2197, or branch length t\* = (3/8)·ln 2 = 0.2599 substitutions/site. For d = 3: p\* = 0.317, t\* = 0.412.
- **Consequence for Steel's conjecture under JC:** combined with Roch (O(log n) sites below KS) and Mossel–Roch–Sly (poly(n) sites above g_ML), this locates the transition exactly at KS for regular trees. This assumes MRS's g_ML is the regular-tree threshold, which should be checked. Previously, a window between KS and g_ML was possible.
- **SBM:** three communities are weakly recoverable iff (a−b)² > 3(a+2b) at every mean degree above 1. Previously this was proved only at large degree. Lean covers only the easy direction; the hard direction rests on shipped exact-arithmetic C++ certificates.
- **What I checked:** the four-state `small_polynomials.py` rational checks pass, including all 24 symmetry actions. The full C++ certificate needs Boost, which is unavailable here.
- **Benefit:** guarantee and interpretation for phylogenetics theory and SBM benchmark plots. Practitioners (RAxML, IQ-TREE ASR) do not operate under equal-branch JC on regular trees.
- **First step:** write the JC sequence-length corollary carefully and check MRS's definition of g_ML.

## What is NOT an opportunity here

- **numstat-5: changing any Krylov or expm code using Crouzeix constants.** No code sets a constant from Crouzeix. The codes checked:
  - SciPy `expm_multiply` uses tol = 2^-53 and the θ_m backward-error table ([#L259-L277](https://github.com/scipy/scipy/blob/d1d4a8aa11723e6885f268a4106758d7917d5906/scipy/sparse/linalg/_expm_multiply.py#L259-L277), [#L309-L312](https://github.com/scipy/scipy/blob/d1d4a8aa11723e6885f268a4106758d7917d5906/scipy/sparse/linalg/_expm_multiply.py#L309-L312)).
  - Krylov.jl block-GMRES uses residual stopping ([block_gmres.jl#L165-L186](https://github.com/JuliaSmoothOptimizers/Krylov.jl/blob/e9df3feac92c93206b688bce76fda5e46a7026a7/src/block_gmres.jl#L165-L186)).
  - KrylovKit `exponentiate` uses `normres` ([#L25-L40](https://github.com/Jutho/KrylovKit.jl/blob/fdbbc11febb97d5a56a92055bc97af8ecd3ef240/src/matrixfun/exponentiate.jl#L25-L40)).
  - ExponentialUtilities uses the Niesen–Wright estimate ([#L128-L140](https://github.com/SciML/ExponentialUtilities.jl/blob/56dba586f0c9dd2bca074859464d3a30f104f781/src/krylov_phiv_adaptive.jl#L128-L140)).
  - funm_quad uses update-norm stopping ([#L488-L503](https://github.com/guettel/funm_quad/blob/912a51586d6b7ebc1fe328f44d21c742ba2fdb7e/funm_quad/funm_quad.m#L488-L503)).
  - RKToolbox (`1e6a3c0d37a161c46c286ab9d101d043301fdee3`) has no mention of the numerical range.
  - funm_kryl and Higham's Matrix Function Toolbox could not be cloned (not publicly reachable on GitHub from here). Their published docs use a-posteriori estimates.

  On my convection–diffusion test, the FOV bound over-predicts by ~800× (1.56×10⁵ vs 193 actual iterations), whatever the constant. **The change is docs-only.**
- **Using Crouzeix–Kressner for matrix-exponential conditioning:** the classical bound with constant 1 already beats 4.
- **Quantum eigenvalue-processing speedups from 2.414→2:** this is a constant inside a normalization or log factor; nothing to implement.
- **numstat-7 (374): a-posteriori map-error certificates in semi-discrete solvers** (POT, pysdot [mass stopping #L118-L131](https://github.com/sd-ot/pysdot/blob/840c92c2b144c9e779746e9a24ac44fb860cc88b/pysdot/OptimalTransport.py#L118-L131), OTT [solver #L281-L313](https://github.com/ott-jax/ott/blob/36338c94707002772f2392ffa0a3acf11ab23857/src/ott/solvers/linear/semidiscrete.py#L281-L313)). On the unit square, C\*·(diam²·TV)^{1/6} drops below the trivial bound diam = 1.41 only when TV ≲ 10^{-11}. For a 10%-of-diameter guarantee you need W₂ ≤ 9×10⁻⁹, which is about n ≈ 10^{16} target samples in d = 2. Vacuous.
- **numstat-10 (101): advertising "1.05 → 0.604 bits" as new.** The scalar statement and the capacity corollary are Melbourne–Nayar–Roberto's.
- **numstat-12 (093): sampler code changes** (step sizes or iteration budgets in volesti, Stan, BlackJAX) based on the LSI. C is non-explicit and a is unknown. Samplers tune step sizes from acceptance rates and ESS anyway.
- **numstat-13 (140)**: the theory is clean, but no practitioner decision depends on it. The explicit 2^{-16} constant is about 9×10⁴ below the Kaczmarz upper bound (≈1.39·d·log₂(1/ε)). It covers noiseless Gaussian rows and memory fixed at A·d². Its message — sub-d²-bit learners cannot beat O(d log 1/ε) samples, and RLS-style d²·log(1/ε)-bit states are needed to do better — is already the folklore design rule.
- **numstat-14 (119)**: Courtade–Kumar confirms that forwarding one raw bit is the best one-bit summary of uniform BSC-noisy bits. The human Lean-verified proof (2609.24931) predates the drop's paper by three days. No engineering decision changes.
- **numstat-16 (222)**: the free energies are for random-label storage at positive temperature with bounded soft potentials. There is no teacher–student, generalization or capacity statement. The jamming exponents rigorously confirm Charbonneau–Kurchan–Parisi–Urbani–Zamponi's values to about 7 digits, where physics confidence was already high. Nothing changes in ML or packing practice.

## Experiment results
Scripts and outputs are in `/home/claude/work/repos/scratch_numstat/`: `crouzeix_exp.py/.out`, `crouzeix_exp2.py/.out`, `entropy_brenier_numbers.*`, `entropy_checks.*`, `brenier_rates.out`.

1. **Iteration counts predicted by the FOV bound** (tol 1e-8; C = 1+√2 vs 2):

   | ρ | C = 1+√2 | C = 2 | Saved |
   |---|---|---|---|
   | 0.9 | 184 | 182 | ≈1% |
   | 0.99 | 1921 | 1902 | ≈1% |
   | 0.999 | 19293 | 19105 | ≈1% |

   The saving is always 0.188/|log ρ| iterations.
2. **GMRES on I + 0.9·shift (n = 200, W(A) a disk):** the actual residual stays at ≈0.22 × 2ρ^k. The actual count to 1e-8 is 167, against bounds of 183 (2.414) and 182 (2).
   - On 1-D convection–diffusion (m = 200, c = 0.6), W(A) almost touches 0. GMRES actually takes 193 iterations, while the disk-FOV bound gives about 1.56×10⁵.
3. **Exact ‖L_exp(A)‖ (Frobenius-induced) vs bounds:**

   | Matrix | ‖L‖ | e^{ω} | 4e^{ω} | 5.83e^{ω} |
   |---|---|---|---|---|
   | random/√n | 3.35 | 3.55 | 14.2 | 20.7 |
   | grcar(12) | 13.2 | 14.9 | 59.6 | 86.8 |
   | strongly non-normal stable | 19.5 | 62.0 | 248 | 361 |

   The log-norm bound (constant 1) dominates in every case.
4. **Crouzeix–Kressner nilpotent example:** ratio = 4.0000, so 4 is attained. For the Fréchet-derivative ratio with f = z^k, random search found at most 1.26, and the 2×2 Jordan block with z² gives √2.
5. **Structural LMI κ for shift matrices** (cvxpy/SCS): between 1.0 and 1.77, always ≤ 2 as the theorem requires.
6. **Entropy (101):**
   - The exact-rational verifier passes.
   - Simplex slack is positive in all dimensions (→ 0.581 nats total).
   - Exponential-noise capacity gap with Gaussian input is 0.5557, 0.6040 and 0.6044 bits at P = 1, 10 and ≥100. The bound 0.6044 is tight.
7. **Brenier (374):**
   - C\* = 67.7 (unit square, centered), 95.4 ([−1,1]²), 239 (d = 10).
   - The bound beats the trivial diam bound only for W₂ ≲ 10⁻⁵.
   - Grid check of the sharpness family: ratio/W₂^{1/3} = 0.630 constant, while ratio/W₂^{1/2} grows from 1.26 to 3.02 as a goes from 0.1 to 0.003.

## Sources
- Lorist & Schwenninger, *A solution to Crouzeix's conjecture*, [arXiv 2608.03841](https://arxiv.org/abs/2608.03841) ([HTML v2](https://arxiv.org/html/2608.03841v2)); [U. Twente news, Aug 25 2026](https://new.utoday.nl/news/77075/ut-researcher-cracks-20-year-old-maths-problem); [Wikipedia: Crouzeix's conjecture](https://en.wikipedia.org/wiki/Crouzeix%27s_conjecture); Jin, [preprints.org 202607.1919](https://www.preprints.org/manuscript/202607.1919/v4); Badea–O'Loughlin–Virtanen, [arXiv 2609.03637](https://arxiv.org/abs/2609.03637).
- Crouzeix & Kressner, [arXiv 2007.09784](https://arxiv.org/abs/2007.09784); Kressner, [arXiv 1802.05759](https://arxiv.org/abs/1802.05759); Embree, [arXiv 2209.01231](https://arxiv.org/abs/2209.01231); [Extending Elman's bound for GMRES, arXiv 2312.15022](https://arxiv.org/html/2312.15022v2); Beckermann, [C. R. Math. 340 (2005)](https://comptes-rendus.academie-sciences.fr/mathematique/articles/10.1016/j.crma.2005.04.027); Low & Su, [arXiv 2401.06240](https://arxiv.org/abs/2401.06240).
- OT: Mérigot–Delalande–Chazal, [AISTATS 2020](https://proceedings.mlr.press/v108/merigot20a.html); Pooladian–Divol–Niles-Weed, [arXiv 2301.11302](https://arxiv.org/abs/2301.11302v1); Divol–Niles-Weed–Pooladian, [arXiv 2212.03722](https://arxiv.org/abs/2212.03722v2); Cazelles–Pauwels–Portales, [arXiv 2604.22366](https://arxiv.org/html/2604.22366v2); Letrouit, [arXiv 2510.13265](https://arxiv.org/abs/2510.13265); Han–Zhu, [arXiv 2602.19175](https://arxiv.org/html/2602.19175v2); Moosmüller–Cloninger, [arXiv 2008.09165](https://ar5iv.labs.arxiv.org/html/2008.09165).
- Entropy: Marsiglietti–Kostina, [arXiv 1704.07766](https://arxiv.org/abs/1704.07766) ([MDPI](https://www.mdpi.com/1099-4300/20/3/185)); Melbourne–Nayar–Roberto, [arXiv 2309.01840](https://arxiv.org/html/2309.01840v2); Bobkov–Madiman, [arXiv 1006.2883](https://arxiv.org/abs/1006.2883); Fradelizi–Marín Sola, [arXiv 2406.07406](https://arxiv.org/abs/2406.07406).
- Sampling: Kook–Vempala–Zhang, [In-and-Out, arXiv 2405.01425](https://arxiv.org/html/2405.01425v4).
- Memory: Sharan–Sidford–Valiant, [arXiv 1904.08544](https://arxiv.org/abs/1904.08544).
- Courtade–Kumar: Chen et al., [arXiv 2609.24931](https://arxiv.org/abs/2609.24931).
- Phylogenetics/reconstruction: Mossel, [Phase transitions in phylogeny, arXiv math/0304491](https://arxiv.org/abs/math/0304491v1); Daskalakis–Mossel–Roch, [arXiv math/0509575](https://arxiv.org/abs/math/0509575v2); Mossel–Roch–Sly, [arXiv 1001.3480](https://ar5iv.arxiv.org/html/1001.3480); Sly, [Reconstruction for the Potts model, AoP 2011](https://projecteuclid.org/journals/annals-of-probability/volume-39/issue-4/Reconstruction-for-the-Potts-model/10.1214/10-AOP584.pdf).
- Code (pinned): SciPy `d1d4a8aa`, Krylov.jl `e9df3fea`, KrylovKit.jl `fdbbc11f`, ExponentialUtilities.jl `56dba586`, funm_quad `912a5158`, chebfun `7574c776`, chebfun/examples `f4b9ea46`, RKToolbox `1e6a3c0d`, POT `604c47f2`, OTT-JAX `36338c94`, pysdot `840c92c2`, PyTransKit `aca79ee9`, mathlib4 `d6416ab0`.
- Note: the web-search budget ran out before I could check funm_kryl or Güttel's RKToolbox documentation pages, Low–Su Appendix B.2's body, or whether Mossel–Roch–Sly's g_ML is the regular-tree threshold. These are flagged as open checks above.
