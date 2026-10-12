# Quantum information: bosonic entropy (273), GAD capacity (276), MUBs in d=6 (266), zero-key / PPT² (272), threshold repetition (277)

**Bottom line.**
- **273 (EPnI) is the one real opportunity in this theme.** The inequality itself is Lean-checked against a comparator. Its consequence, the vacuum-port multimode constrained minimum-output-entropy bound, is exactly the missing converse ingredient for three published families of conditional theorems:
  - the Guha–Shapiro–Erkmen pure-loss broadcast region;
  - the Wilde–Hayden–Guha pure-loss trade-off regions;
  - De Palma's 2019 conditional corollaries.
  
  All of these now become unconditional (CERTIFY). The thermal-noise broadcast region is within reach: it needs one convexity lemma, which our numerics support, plus a write-up. Wiretap/private/quantum capacities of pure loss and the single-user thermal capacity were already unconditional by other means, so they gain nothing. Amplifiers, mode-dependent loss and non-degradable thermal-channel trade-offs are not unblocked.
- **276** is correct and Lean-checked. We validated it numerically. Against Khatri–Sharma–Wilde 2020 it is a large improvement: those bounds overshoot by 0.10–0.37 bits, often more than 100%. Against Fang's September 2026 converse it closes only a residual gap of 0.04–0.09 bits at low temperature (N ≤ 0.1) and under 0.003 bits for N ≥ 0.4. It is a table and reference-implementation update with no engineering consequence.
- **266:** N(6)=3 currently rests entirely on an unpublished C++ pipeline. The code, hashes manifest, runner and execution archive are absent from every public ref of openai/math. Only N(6) ≤ 5 is proved in the open: exact rational certificate plus Lean. Treat N(6)=3 as an unverified claim, and push for the release and an independent interval-arithmetic re-run.
- **272** disproves both forms of PPT² and answers "key from every entangled state?" negatively. It kills no deployed QKD result. Combined with a simple swapping identity, it actually *restores* the repeater consequence PPT² was wanted for: swap-then-distill repeaters fed with PPT states still yield zero key.
- **277** is galactic for DIQKD. CHSH needs about 10¹¹ rounds just for soundness concentration, against 1.5·10⁶ rounds in the EAT-based Nadlinger et al. 2022 experiment. It is also conceptually not a key-rate tool. Do not pursue.

All repo references are pinned to openai/math @ `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` (also the live `main` on 2026‑10‑11; `git ls-remote` checked).

---

## What the papers actually prove

### 273: The entropy photon-number inequality (Sept 24, 2026)
- **Thm `thm:epni`** ([00-introduction.tex L10-28](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/00-introduction.tex#L10-L28)). Setting:
  - two independent n-mode inputs, any finite n, finite mean energy;
  - arbitrary entanglement *within* each port;
  - a common transmissivity η ∈ [0,1] on every mode.
  
  The conclusion is g⁻¹(S(ρ_C)/n) ≥ η g⁻¹(S(ρ_A)/n) + (1−η) g⁻¹(S(ρ_B)/n), with g(t) = (t+1)ln(t+1) − t ln t. The proof is non-constructive (variational contradiction), but its consequences have explicit optimizers (thermal states, coherent-state superposition codes).
- **Cor `cor:thermal-attenuator`** ([L34-51](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/00-introduction.tex#L34-L51)). For identical thermal attenuators E_{η,N_B}^{⊗n} and *any* finite-energy n-mode input (entangled across modes), (1/n)S(out) ≥ g(η g⁻¹(S(ρ)/n) + (1−η)N_B). Product thermal inputs attain it. At N_B = 0 this is precisely Guha–Shapiro–Erkmen's "Strong Conjecture 2" and De Palma's "Conjecture 1 for the quantum-limited attenuator".
- **Cor `cor:broadcast-capacity`** ([06-broadcast.tex L28-42](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/06-broadcast.tex#L28-L42)) gives the exact two-receiver degraded pure-loss broadcast region R_B ≤ g(η_B βN̄), R_C ≤ g(η_C N̄) − g(η_C βN̄). It holds for 0 ≤ η_C < η_B and η_B + η_C ≤ 1, under a codebook-averaged photon constraint with entangled codewords allowed.
  - The converse needs the vacuum case plus convexity of φ_λ(u) = g(λg⁻¹(u)). That convexity is proved in-paper ([L119-128](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/06-broadcast.tex#L119-L128)) **only for a vacuum degrading port**.
- **Explicit scope disclaimers.** There is nothing for mode-dependent attenuations, amplifiers or additive-noise channels ([intro L63](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/00-introduction.tex#L63)). There is also nothing for noisy broadcast, wiretap, quantum capacity, feedback or cooperation ([broadcast L301-304](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/06-broadcast.tex#L301-L304)).
- **Lean.** The comparator [EntropyPhotonNumber.lean L99-106](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/EntropyPhotonNumber.lean#L99-L106) states the full inequality on untruncated Fock space ℓ²(ℕⁿ), with entropy via continuous functional calculus. The solution is [Inequality.lean L689](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/InformationTheory/PhotonNumber/Inequality.lean#L689-L695): 20 files, 21,871 lines, 0 `sorry`/`axiom` by grep. The corollaries are **not** formalized (lean/docs/273.md).
- **Triage check:** correct. One refinement: the paper's broadcast region is slightly *more* general than GSE 2007's lossless η + (1−η) = 1 split.

### 276: Classical capacity of generalized amplitude damping (Sept 24, 2026)
- **Thm `thm:main`** ([paper.tex L208-228](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Classical-capacity-and-entropy-inequalities-for-generalized-amplitude-damping-September-24-2026/build/paper.tex#L208-L228)). For all γ, ν ∈ [0,1] and all n, χ(A^{⊗n}) = nχ(A), with
  - C = (1/ln2) max_p { h((1−γ)p+γν) − g(γν(1−ν)+γ(1−γ)(p−ν)²) }, where g(u) = h((1+√(1−4u))/2);
  - attained by products of the pair √(1−p)|0⟩ ± √p|1⟩.
  
  It is fully constructive: one scalar maximization.
- **Cor `cor:partner-additivity`** ([L238-257](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Classical-capacity-and-entropy-inequalities-for-generalized-amplitude-damping-September-24-2026/build/paper.tex#L238-L257)): χ, S_min and C are additive with any finite-dimensional partner channel.
- **Lean:** the comparator [AmplitudeDamping.lean L113-122](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/AmplitudeDamping.lean#L113-L122) covers additivity at every n, the scalar maximum, operational capacity and attainment. Partner additivity is not covered.
- **Prior art in the same month.** Ordinary amplitude damping (ν=0) was solved by Tang–Zhu–Bai–Wang ([arXiv 2609.28592](https://arxiv.org/abs/2609.28592)). Fang ([arXiv 2609.14621](https://arxiv.org/abs/2609.14621)) gave a near-tight converse U_G. 276's genuinely new content is the case 0 < ν < 1, ν ≠ 1/2, outside the entanglement-breaking region.

### 266: N(6)=3 (two manuscripts, Sept 24, 2026)
- **Thm `thm:main`** ([introduction.tex L13-19](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/introduction.tex#L13-L19)) is explicitly conditional on two things:
  - the binary64/compiler conditions of the rounding appendix;
  - "the fresh complete execution documented in Section execute:observed".
- **Thm `execute:finite-theorem`** ([execution.tex L242-249](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex#L242-L249)) is the mathematical content. It says: *if* the seven named C++ files run with the listed invocations and meet the terminal conditions, *then* no 4 MUBs exist.
- **What rests on unpublished computation: the entire upper bound N(6) ≤ 3.** Specifically:
  1. The seven sources `seed.cpp`, `covout.cpp`, `ub.cpp`, `patchx.cpp`, `atlas.cpp`, `stageB.cpp` and `stageC.cpp`, together with `verification/code/extraction.json` (their SHA-256 hashes) ([execution.tex L16-21](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex#L16-L21)).
  2. The runner `proof_run.py`, `build/build-manifest.json`, `verification/REPRODUCE.md`, `verification/computation/README.md` and the execution archive `full-run-01/…` ([L380-392](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex#L380-L392)).
  3. The *applicability* of the 40-odd lemmas in seed/completion/phase-cover/refinement/exclusion and of the 74 KB rounding appendix. These analyze named routines, about 80 distinct identifiers such as `trial::certificate`, `spectralUpper` and `coverSeeds::run`. One step even relies on a disassembly check of `pow` lowering at specific addresses in the recorded binary ([L90-104](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex#L90-L104)). Without the code, nobody can check that the analysis matches what ran.
  4. What *is* published: SHA-256 hashes of 8 data files and the stage counts. The pipeline ran 249,878 seed centers, then 3,083 coarse records, 600 mid records and 22,379 fine records. 163 of the fine records hit the graph cap; these went through a 1,127-record fallback, ending with 0 unresolved. Wall time was 4,470 s on one Xeon 8573C.
  5. The paper itself says the earlier September 7 run "was not authenticated" ([L394-400](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex#L394-L400)).
- **Repo re-check (thorough).** None of the following contains a `verification/` folder for this preprint:
  - working tree, `origin/main` (fd4aeeb), and the PR ref `refs/pull/1/head` (3014888, fetched);
  - the initial commit adc7f12;
  - the PDF (`pdfdetach`: 0 embedded files);
  - any `.gitignore` (none in that dir; the repo's other ignores cover only `.build-output/`, `.verification-output/`, `*.log` etc.);
  - `lean/` (the MUB development has 3,386 files, none touching four-basis exclusion);
  - `reasoning_traces/` (11 files, none on MUBs).
  
  Contrast: other computer-assisted preprints in the same drop *do* ship code (e.g. matrix-multiplication `verification/certificate/checkers/*.cpp`, three-state reconstruction `verification/interval.cpp`). The omission is specific to 266.
- **What is proved in the open.**
  - Lower bound 3: elementary tensor construction, Lean-checked (`three_mutually_unbiased_bases`, [ThreeMain.lean L9](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/MutuallyUnbiased/Bases/ThreeMain.lean#L9)).
  - Upper bound **5**: an exact rational certificate excluding 7 MUBs, plus Weiner's completion theorem ([Exact-Fourier paper.tex L142-153](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/build/paper.tex#L142-L153)). It is Lean-checked (comparator [MUBSix.lean L56-60](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/MUBSix.lean#L56-L60)), and the triage re-ran the Python verifier (87 s).
- **Confidence assessment.**
  - N(6) ≤ 5: high (5/5).
  - N(6)=3 as a *proof*: 2/5 today. It is unreproducible, and its trust base is "binary64 plus compiler semantics" rather than interval or exact arithmetic.
  - N(6)=3 as a *fact*: very likely true. All numerics agree: Butterley–Hall 2007, Brierley–Weigert 2008, Raynal–Lü–Englert's "four most distant bases", and Prat Colomer et al. 2022 Bell-inequality searches (three methods converge to the same non-MUB quadruple).
  - The method follows a recognized certified-discretization line (Jaming–Matolcsi–Móra–Szöllősi–Weiner 2009). Once the code is released, a re-run is about 75 minutes of compute.

### 272: Entanglement without distillable key; PPT² (Sept 27, 2026)
- **Thm `thm:main-pair`** ([introduction.tex L80-89](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/build/source/sections/introduction.tex#L80-L89)) gives explicit PPT maps Φ₁, Φ₂ : M₁₀ → M₁₀ whose composite Choi matrix has product-free range, so Φ₂∘Φ₁ is not EB. This **disproves the two-map PPT² conjecture** (Christandl–Müller-Hermes–Wolf 2019, Conj. IV.1).
- **Thm `thm:main-channel`** ([L101-105](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/build/source/sections/introduction.tex#L101-L105)) gives a trace-preserving PPT channel Θ on M₂₁ with Θ∘Θ not EB. This **disproves the single-channel PPT²** (BIRS 2012 Problem G; IQOQI OQP #38).
  - Via the Choi isomorphism this also refutes OQP #38's state form: entanglement-swapping two PPT states can produce an entangled state.
  - Both theorems are Lean comparator-checked ([DimensionTenPair.lean L112-120](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/DimensionTenPair.lean#L112-L120), [DimensionTenChannel.lean L45-49](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/DimensionTenChannel.lean#L45-L49)).
- **Thm `thm:main-state` / `thm:zero-key`** ([intro L45-60](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/build/source/sections/introduction.tex#L45-L60), [secret-key.tex L121-136](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/build/source/sections/secret-key.tex#L121-L136)).
  - Every state in the "represented class" 𝒞 = {(𝓛⊗𝓜)(χχ*) : 𝓛, 𝓜 CP and co-CP} ([foundations.tex L140-152](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Entanglement-with-zero-distillable-secret-key-in-local-dimension-ten-September-27-2026/build/source/sections/foundations.tex#L140-L152)) has K_D = 0.
  - The bound is uniform: trace distance ≥ 1/10 from a secret bit, for any n and any admitted two-way protocol, with Eve holding the purification and the transcript.
  - The explicit 10×10 state is entangled and in 𝒞. This answers OQP #24 ("secret key from all entangled states?", P. Horodecki, 2005) **negatively**, within the paper's "admitted completed protocol" model.
  - This part is not a comparator statement. The in-library Lean `ZeroKey.TenDimensional.main_state` ([DimensionTen.lean L66-70](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/InformationTheory/SecretKey/DimensionTen.lean#L66-L70); 15 files, 13.6k lines, 0 `sorry`) is labelled a "finite terminal-readout model".
- **Not disproved / still open:** eventual EB of PPT maps (Θ³ or Θᵏ for k > 2); PPT² in low dimension (proved for M₃ by CMHW 2019); unital or full-rank-fixed-point cases (finite EB index proved); minimal dimensions.

### 277: Threshold parallel repetition (Sept 25, 2026)
- **Thm `thm:main`** ([00-introduction.tex L50-62](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Threshold-parallel-repetition-for-finite-dimensional-entangled-games-September-25-2026/build/sections/00-introduction.tex#L50-L62)): Pr[W_k ≥ ⌈(v+δ)k⌉] ≤ exp(−κ₀δ⁵k/(1+log d)), with κ₀ = 1/(16(4B₄)⁴) ([04-threshold.tex L223](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Threshold-parallel-repetition-for-finite-dimensional-entangled-games-September-25-2026/build/sections/04-threshold.tex#L193-L231)).
  - B₄ is a **non-explicit** universal constant imported from Song's Lemma 4.4. Song's preprint is IACR ePrint 2026/1702, unrefereed, with constants not explicit.
- **Explicit cubic bound** ([L83-88](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Threshold-parallel-repetition-for-finite-dimensional-entangled-games-September-25-2026/build/sections/00-introduction.tex#L83-L88)): exponent δ³/(16384(1+κ_μ)(1+log d)), with κ_μ = 8·max_j(|H_j|−1)/μ_{j,min}.
- **Lean:** formalizes only the δ¹³ rate, with an existential κ₀ ([EntangledGames.lean L64-74](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/EntangledGames.lean#L64-L74)).
- **Conceptual point the triage missed.** Threshold repetition bounds the probability of winning *above the entangled value v*. Honest CHSH devices never exceed v ≈ 0.854, so the theorem gives nothing directly to CHSH-based DIQKD.
  - Its DI use is indirect: soundness of guessing/"immunized" games, as in Vidick's MS_{1/8} construction, or simulation of a single round in parallel proofs.
  - Even then it yields concentration, not a min-entropy rate.

---

## Current practice & state of the art

**Bosonic capacities (273).**
- **Unconstrained minimum output entropy** (vacuum or coherent input optimal) is settled for all phase-insensitive Gaussian channels:
  - Giovannetti–García-Patrón–Cerf–Holevo, Nat. Photon. 2014 ([arXiv 1312.6225](https://arxiv.org/abs/1312.6225));
  - Giovannetti–Holevo–García-Patrón, CMP 2015;
  - majorization: Mari–Giovannetti–Holevo, Nat. Commun. 2014 ([arXiv 1312.3545](https://arxiv.org/abs/1312.3545)).
  
  Hence single-user classical capacities of thermal attenuators, amplifiers and additive-noise channels are known.
- **Constrained (fixed input entropy) minimum output entropy:**
  - one-mode: De Palma–Trevisan–Giovannetti 2016–17 ([arXiv 1605.00441](https://arxiv.org/abs/1605.00441));
  - multimode with product-basis-diagonal inputs only ([arXiv 1705.00499](https://arxiv.org/abs/1705.00499));
  - multimode *entanglement-breaking* attenuators and amplifiers: De Palma 2019 ([arXiv 1805.12469](https://arxiv.org/abs/1805.12469)).
  
  For broadcast and trade-off questions, De Palma 2019 had only outer bounds (Cor. 10, 13). The exact regions were stated "assuming Conjecture 1 for the quantum-limited attenuator".
- **Pure-loss private and quantum capacities** are unconditional via degradability, with no MOE or EPnI needed: Wilde–Qi ([arXiv 1609.01997](https://arxiv.org/abs/1609.01997)), and WHG 2012 Thm 8 for quantum capacity.
- **Practice.** Optical links operate far from Holevo limits. Broadcast/trade-off coding and joint-detection receivers exist only in theory or the lab. No mainstream software computes these regions: [thewalrus](https://github.com/XanaduAI/thewalrus/blob/54b1062e2b6759ddc733ca6bf636df580ff94968/thewalrus/quantum/entanglement.py#L59) has only Gaussian covariance entropies, and Strawberry Fields is a simulator.

**Table: published theorems conditional on the EPnI or its special cases.**

| # | Published result | Was conditional on | Already settled by other means? | Status with 273 | Missing step |
|---|---|---|---|---|---|
| 1 | Two-receiver pure-loss degraded **broadcast** region R_B ≤ g(ηβN̄), R_C ≤ g((1−η)N̄) − g((1−η)βN̄). Guha–Shapiro–Erkmen, PRA 76, 032303 (2007), [arXiv 0706.3416](https://arxiv.org/abs/0706.3416) | Strong Conj. 2 (n-mode, vacuum env, arbitrary input) | No (De Palma 2019 outer bound only) | **Unconditional**, proved in `cor:broadcast-capacity`; also covers η_B+η_C ≤ 1 | None; formalizing the corollary would raise confidence from 4 to 5 |
| 2 | **m > 2 receiver** pure-loss degraded broadcast. Guha PhD thesis, MIT 2008 ([DSpace](https://dspace.mit.edu/handle/1721.1/44413)) | SC2 | No | **Very likely unconditional** | Iterate the 273 converse layer by layer: same vacuum EPnI, φ_λ convex. Not written anywhere |
| 3 | Pure-loss **CQE trade-off** and **public/private/key trade-off** regions, η > 1/2. Wilde–Hayden–Guha PRL 108, 140501 ([1206.4886](https://arxiv.org/abs/1206.4886)); PRA 86, 062306 ([1105.0119](https://arxiv.org/abs/1105.0119)) §III G–H | SC2, applied to the channel *and* the complementary channel (beam-splitter simulation of Eve) | No | **Unconditional modulo a check.** `cor:thermal-attenuator` at N_B = 0 is SC2 for every η ∈ [0,1] and every finite-energy entangled n-mode input | Confirm WHG's converse uses SC2 only in this form; publish a short note or erratum |
| 4 | De Palma 2019 ([1805.12469](https://arxiv.org/abs/1805.12469)) §VI degraded Gaussian broadcast region and Cor. 12 triple trade-off regions of the quantum-limited attenuator | "Conjecture 1 for the quantum-limited attenuator" (multimode) | No (proved outer bounds Cor. 10, 13 only) | **Unconditional**: the hypothesis is exactly the N_B = 0 corollary. Cor. 10/13 are superseded | None |
| 5 | **Thermal-noise** (loss + thermal) broadcast region. Guha thesis 2008; Anderson–Guha–Bash, ISIT 2021 ([record](https://experts.arizona.edu/en/publications/fundamental-limits-of-bosonic-broadcast-channels/)), incl. covert broadcast | "strong MOE conjecture", thermal version, said to follow from EPnI | No | **Not yet, but within reach** | (i) convexity of φ_{λ,N′}(u) = g(λg⁻¹(u) + (1−λ)N′) for N′ > 0: 273 proves N′ = 0 only, and our grid check supports it (Experiment E2). (ii) C's channel must be a thermal attenuator of B's with an *independent* thermal environment, which needs noise ordering N′ ≥ 0. (iii) Unconstrained thermal MOE for B's codeword term (GHG 2015). Then write the converse |
| 6 | **Wiretap / private capacity** of pure loss, g(ηN̄) − g((1−η)N̄) for η > 1/2. Guha–Shapiro–Erkmen ISIT 2008, [0801.0841](https://arxiv.org/abs/0801.0841) | MOE Conj. 2 | **Yes**: Wilde–Qi [1609.01997](https://arxiv.org/abs/1609.01997) (degradability, no MOE) | No change | — |
| 7 | Energy-constrained **quantum capacity** of pure loss (claimed to follow from SC2 in 0801.0841) | SC2 | **Yes**: WHG 2012 Thm 8; Wolf–Pérez-García–Giedke 2007 (unconstrained) | No change | — |
| 8 | Single-user classical capacity of **thermal** attenuator, amplifier and additive noise. Giovannetti et al., PRA 70, 032315 (2004) Conj. 1 | MOE Conj. 1 | **Yes**: GGCH 2014, GHG 2015, MGH 2014 majorization | EPnI re-derives it (input entropy 0) | — |
| 9 | Thermal-noise bosonic **MAC**. Yen–Shapiro, [quant-ph/0506171](https://arxiv.org/abs/quant-ph/0506171) | Single-user thermal MOE | **Yes** (2014 results) | No change | — |
| 10 | **Quantum-limited amplifier** trade-off and broadcast. Qi–Wilde, [1605.04922](https://arxiv.org/abs/1605.04922) | One-mode amplifier MOE (proved) + Hadamard-channel single-letterization | The authors present it as unconditional. The De Palma et al. survey ([1803.02360](https://arxiv.org/abs/1803.02360)) still lists the amplifier trade-off converse as needing the multimode conjecture. **Sources disagree** | **No effect**: 273 disclaims amplifiers (not passive mixing) | Multimode constrained MOE for non-EB amplifiers; De Palma 2019 covers EB only |
| 11 | Thermal-channel trade-off / private / quantum capacities. WHG 2012 Thms 9–12 give achievable regions only | Capacity unknown; channel non-degradable | No | **Not unblocked** | Non-degradable channels need regularized converses; the constrained-MOE ingredient alone is insufficient |
| 12 | Wideband / **mode-dependent loss** broadcast (frequency-dependent η) | SC2 with non-identical modes | No | **Not covered**: thm and corollary assume one η for all modes | An EPnI with mode-dependent transmissivities (open) |
| 13 | FSO interference channel, very-strong-interference joint-detection region. Guha–Savov–Wilde ISIT 2011, [1102.2627](https://arxiv.org/abs/1102.2627) | "MOE conjecture of [3],[16]"; we could not identify which | ? | **Unclear** | Read the appendix. If it is the single-user thermal MOE, it was settled in 2014 |

Textbook and survey targets that may still describe rows 1–4 as conditional need to be checked; our web-search budget ran out, so their text is unverified:
- De Palma–Trevisan–Giovannetti–Ambrosio survey ([1803.02360](https://arxiv.org/abs/1803.02360)): Conj. V.1 / V.15, explicitly listed as open with broadcast and trade-off as motivation (verified).
- Khatri–Wilde, *Principles of Quantum Communication Theory* ([2011.04672](https://arxiv.org/abs/2011.04672) v2, Feb 2024): bosonic chapters.
- Holevo, *Quantum Systems, Channels, Information* (2nd ed., de Gruyter 2019): Gaussian-channel chapter.
- Serafini, *Quantum Continuous Variables*.
- Wilde's *From Classical to Quantum Shannon Theory* ([1106.1445](https://arxiv.org/abs/1106.1445) v8) is finite-dimensional, so it is an unlikely target.

**GAD capacity (276).**
- KSW 2020 ([arXiv 1903.07747](https://arxiv.org/abs/1903.07747), PRA 102, 012401) is the standard bound table: C_β = log₂(1+√(1−γ)), C_cov, C_Fil, C_EA, C_EB, lower bound χ. Its code ships as arXiv ancillary files (MATLAB/Python).
- Fang Sept 2026 is the tightest prior converse.
- Practice: GADC (the `thermal_relaxation`/`amplitude_damping_error` noise in [qiskit-aer](https://github.com/Qiskit/qiskit-aer/blob/fe964bf3ec37d27175325bb306e752d1c3cb9591/qiskit_aer/noise/errors/standard_errors.py#L351-L460)) is used to *simulate* qubit noise, not to send classical data at capacity.
- [toqito](https://github.com/vprusso/toqito/blob/4baf22e6f3da78ac9a01352de1980e2441c6cc77/toqito/channels/amplitude_damping.py#L8-L77) implements the GADC (`prob` = 1−ν) but has no capacity routines (grep: only `helstrom_holevo`).
- Side note for implementers: qiskit-aer's `amplitude_damping_error` docstring says `excited_state_population` is "the population of |0⟩" ([L449](https://github.com/Qiskit/qiskit-aer/blob/fe964bf3ec37d27175325bb306e752d1c3cb9591/qiskit_aer/noise/errors/standard_errors.py#L449)). The Kraus operators and `rho_eq` in the same function, and the sibling functions (L265, L380), all use |1⟩. So ν = `excited_state_population` (p1) and γ = `param_amp`.

**MUBs in d=6 (266): who uses them and what decisions would change.**
- **Experiments.**
  - Photonic "qusix" tests of 3 MUBs (D'Ambrosio et al., Sci. Rep. 3, 2726 (2013), [arXiv 1304.4081](https://arxiv.org/abs/1304.4081)).
  - Approximate-MUB workflows run with n = 4 in d = 6 on IBM Heron (Fatah et al., [arXiv 2607.10615](https://arxiv.org/abs/2607.10615)).
  - Bell-inequality MUB searches (Prat Colomer et al., [Quantum 6, 778 (2022)](https://quantum-journal.org/papers/q-2022-08-17-778/)).
- **Tomography and QKD.** Qubit-qutrit tomography and high-dimensional QKD already avoid d+1-MUB schemes in d=6. They use 2–3 bases, SIC-POVMs, product or overcomplete measurements, or prime-power dimensions (OAM HD-QKD survey [arXiv 2512.11286](https://arxiv.org/html/2512.11286v1)).
- **Software and lists.** toqito raises `ValueError` for d=6 ([mutually_unbiased_basis.py L56-65](https://github.com/vprusso/toqito/blob/4baf22e6f3da78ac9a01352de1980e2441c6cc77/toqito/states/mutually_unbiased_basis.py#L56-L65)). Open-problem lists: [IQOQI OQP #13](https://oqp.iqoqi.oeaw.ac.at/mutually-unbiased-bases); Horodecki–Rudnicki–Życzkowski "Five open problems", problem 2, with a prize ([arXiv 2002.03233](https://arxiv.org/abs/2002.03233)); McNulty–Weigert review ([Quantum 2026](https://quantum-journal.org/papers/q-2026-04-01-2051/)).
- **Decisions that change: essentially none operationally.** Practice already assumes no fourth MUB. The only redirect is for the small community still searching numerically for 4 MUBs in C⁶, and that redirect should wait for verification.

**Key and repeaters (272).**
- Deployed QKD proofs compute protocol-specific key rates numerically (e.g. the Lütkenhaus-group openQKDsecurity framework). Entanglement verification is a necessary precondition (Curty–Lewenstein–Lütkenhaus 2004), never a sufficient one in practice.
- Key-repeater limits for PPT states are **unconditional** (Bäuml–Christandl–Horodecki–Winter, Nat. Commun. 6, 6908 (2015), [arXiv 1402.5927](https://arxiv.org/abs/1402.5927)): K_{A↔C↔B}(ρ⊗ρ̃) ≤ K_D(ρ^Γ) ≤ min{E_R^∞(ρ^Γ), E_sq(ρ^Γ)}. Their results "support" PPT² but do not assume it.
- The OQP #38 page motivates PPT² as implying "PPT states cannot serve as a repeater resource" ([OQP #38](https://oqp.iqoqi.oeaw.ac.at/the-ppt-squared-conjecture/)). The Christandl–Ferrara repeater bound ([arXiv 1609.04696](https://arxiv.org/abs/1609.04696)) concerns private-state inputs with one-way communication.
- PPT² was known for Gaussian channels (CMHW 2019), so optical networks never had non-EB PPT links anyway.

**DIQKD (277).**
- **State of the art is EAT.** Nadlinger et al., Nature 607 (2022) ([arXiv 2109.14600](https://arxiv.org/abs/2109.14600)): 1.5·10⁶ rounds over about 8 h, CHSH S = 2.677, 95,884 secret bits at ε_snd = 10⁻¹⁰ (≈6.4% of rounds). Proof technique: Arnon-Friedman et al., Nat. Commun. 2018 ([PMC5792631](https://pmc.ncbi.nlm.nih.gov/articles/PMC5792631/)).
- **Parallel DIQKD proofs have no usable constants:**
  - Jain–Miller–Shi ([1703.05426](https://arxiv.org/abs/1703.05426)) leave their constants "for future work";
  - Vidick ([1703.08508](https://arxiv.org/abs/1703.08508)) has an Ω(δ⁹) anchored-game threshold, with no practicality claim;
  - Marwah–Dupuis 2025 ([2507.03991](https://arxiv.org/abs/2507.03991)) combine anchored-game parallel repetition with an unstructured approximate EAT.

---

## Opportunities

### qinfo-1: Make pure-loss broadcast and trade-off capacity theorems unconditional (273): CERTIFY
- **Change.** Publish a short note or erratum verifying that `cor:thermal-attenuator` (N_B = 0) discharges the conditional converses in:
  - GSE 2007 (already done by 273 for 2 receivers);
  - WHG 2012 §III G–H (CQE and public/private/key regions, η > 1/2);
  - De Palma 2019 §VI and Cor. 12;
  - the m-receiver broadcast extension.
  
  Then ask the authors and maintainers of the survey and textbooks to update their "conditional" statements.
- **Targets.** 273's [`cor:thermal-attenuator`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/00-introduction.tex#L34-L51) and [broadcast converse](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-entropy-photon-number-inequality-September-24-2026/build/sections/06-broadcast.tex#L44-L151); WHG [1105.0119](https://arxiv.org/abs/1105.0119); De Palma [1805.12469](https://arxiv.org/abs/1805.12469); survey [1803.02360](https://arxiv.org/abs/1803.02360); Khatri–Wilde [2011.04672](https://arxiv.org/abs/2011.04672).
- **Benefit.** Guarantee: about four published capacity regions for fiber and free-space channels become theorems. The beneficiaries are quantum Shannon theorists and authors of optical-communication limits; no code path changes.
- **Measurement.** Count of conditional statements removed; a WHG and De Palma author acknowledgement or erratum; textbook errata.
- **Risks.**
  - WHG's converse might use SC2 in a slightly different form, for example the complementary channel at η > 1/2 with a joint ensemble. In that case one extra lemma is needed.
  - The corollary is not Lean-formalized. The underlying inequality is.
  - All of this remains unrefereed OpenAI work.
- **First step.** Line-by-line read of WHG §III G–H against the corollary, 1–2 days.

### qinfo-2: Thermal-noise and m-receiver broadcast converses (273): RESEARCH (short)
- **Change.** Prove convexity of φ_{λ,N′}(u) = g(λg⁻¹(u) + (1−λ)N′) for N′ > 0. Then assemble the thermal broadcast converse from three pieces: thermal-attenuator degradation, `cor:thermal-attenuator` with N_B > 0, and GHG's unconstrained MOE for the strong receiver's codeword entropies. This makes the Guha 2008 and Anderson–Guha–Bash 2021 thermal (and covert) broadcast regions unconditional.
- **Evidence it works.** Our numerical check found φ_{λ,N′} convex on λ ∈ [0.05, 0.95], N′ ∈ [0,10], r ∈ [10⁻⁴, 50]. The minimum second divided difference was +5.3·10⁻⁴ (E2).
- **Benefit.** Guarantee for the physically realistic (thermal) broadcast model.
- **Risks.** Noise-ordering conditions may restrict the parameter range: degradation by an independent thermal attenuator needs N′ ≥ 0. Proving convexity analytically for N′ > 0 may be fiddly.
- **First step.** Attempt the analytic φ″ ≥ 0 computation, mirroring 273's L119-128 proof.

### qinfo-3: Exact GADC capacity as reference implementation and benchmark ground truth (276): IMPLEMENT / BENCHMARK
- **Change.** Add a `classical_capacity` routine for the GADC to toqito: next to [`amplitude_damping`](https://github.com/vprusso/toqito/blob/4baf22e6f3da78ac9a01352de1980e2441c6cc77/toqito/channels/amplitude_damping.py#L8-L77), or in `channel_metrics`. It is about 10 lines (our `gad_capacity.py::exact_capacity`), with tests against brute-force Holevo optimisation. Use it as exact ground truth to benchmark converse methods: KSW bounds, Fang's U_G, Fang–Fawzi geometric Rényi.
- **Benefit.** Capability and guarantee: exact capacity tables replace bound tables, and numerical-bound researchers get a non-trivial exact test case.
- **Measurement.** The PR merged. The tables reproduce KSW Fig. 4 with an exact curve: KSW overshoot up to 0.37 bits, Fang's ≤ 0.09 bits (E1).
- **Risks.** Small audience, and maintainers may not want a channel-specific capacity function. The value is pedagogical.
- **First step.** Open a toqito PR with the function, docstring (ν = 1 − `prob` mapping) and tests (unital midpoint closed form; ν = 0 matches Tang et al.).

### qinfo-4: N(6)=3: obtain the artifacts and re-run independently (266): CERTIFY (blocked)
- **Change.**
  1. Request that OpenAI publish `verification/code/` (7 .cpp files + `extraction.json` + `proof_run.py`), `build-manifest.json`, `REPRODUCE.md` and the execution archive.
  2. Re-run the about 75-minute pipeline on independent hardware.
  3. Check the published data hashes ([execution.tex L357-378](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex#L357-L378)).
  4. Ideally re-implement the critical inequalities in interval arithmetic (e.g. MPFI/Arb) to remove the binary64 and compiler trust base.
- **Benefit.** Turns a 2/5-confidence claim into a checkable computer-assisted theorem, which would close OQP #13 and Five-Open-Problems #2.
- **Measurement.** Artifacts released; hashes match; an independent interval re-check passes.
- **Risks.** OpenAI may not release the code. A port to interval arithmetic is weeks of work, and a failure could reveal a soundness gap.
- **First step.** File an issue on github.com/openai/math citing execution.tex L16-21 and L380-392.

### qinfo-5: Correct open-problem lists and reference wording (266, 272): CERTIFY
- **Change.**
  - [OQP #24](https://oqp.iqoqi.oeaw.ac.at/open-quantum-problems): resolved negatively, with an explicit 10×10 PPT entangled state and K_D = 0 in the admitted two-way model.
  - [OQP #38](https://oqp.iqoqi.oeaw.ac.at/the-ppt-squared-conjecture/): disproved, both the map form and the channel form (M₂₁), both Lean-checked.
  - OQP #13 and the McNulty–Weigert / Five-open-problems lists: "N(6) ≤ 5 proved (exact + Lean); N(6) = 3 claimed, computer-assisted, artifacts unpublished".
  - toqito's d=6 error message: could return the 3 tensor-product MUBs.
- **Benefit.** Accurate status for researchers.
- **Risks.** Over-stating 266. Model caveats for 272 (completed protocols; Eve holds the purification).
- **First step.** Email the OQP maintainers with the precise statements.

### qinfo-6: Swap-then-distill key repeaters: PPT inputs still give zero key (272): RESEARCH
- **Observation (ours, not in the paper).**
  - Every PPT state ρ_AB is the Choi matrix of a PPT map F (Choi isomorphism; PPT ⇔ F, T∘F CP). Likewise ρ̃_CD = J(G).
  - For any effect M on BC (including joint measurements across n copies, since ρ^{⊗n} = J(F^{⊗n})), the swapped state is σ_AD ∝ [(F†⊗G†)(M)]^T. This identity was verified numerically to 1.8·10⁻¹² relative to 10⁴ scale (E3).
  - Writing M = Σ m_r m_r* and absorbing the sum into flag registers traced by the (PPT) trace map puts σ_AD in the represented class 𝒞. So `thm:zero-key` gives **K_D(σ_AD) = 0**, even though `thm:main-pair` shows σ_AD can be entangled.
  - The same argument shows any state distributed through a composition of two PPT channels, (id⊗(Θ₂∘Θ₁)^{⊗n})(ψ), lies in 𝒞. Hence forward transmission followed by two-way distillation yields zero key over any two PPT links in series.
- **So.** The disproof kills the *separability* route to "PPT states are useless in repeaters", but the zero-key conclusion survives for swap-then-distill architectures. Fully adaptive tripartite LOCC repeaters remain open; class 𝒞 is the natural tool for them.
- **Benefit.** A redirect and guarantee for key-repeater and network-capacity theory. It does not affect deployed QKD.
- **Risks.**
  - Our derivation is unrefereed. `thm:zero-key` is not comparator-formalized, and the Lean model is a "finite terminal-readout" restriction.
  - The protocol-model details (abort handling, conditioning on the station's announced outcome) need care: the paper's Prop. on conditioning covers public events.
- **First step.** Write a 3-page note; check it against the Bäuml et al. repeater definition; test whether adaptive station measurements keep per-transcript branches in 𝒞.

### qinfo-7: Hard benchmark instance for separability software (272): INSTANCES
- **Change.** Add the explicit integer-defined 10×10 state as a known PPT-entangled test case to separability toolkits: toqito [`is_separable`](https://github.com/vprusso/toqito/blob/4baf22e6f3da78ac9a01352de1980e2441c6cc77/toqito/state_props/is_separable.py#L575-L585) and QETLAB.
- **Why it is hard** (E3). The state is PPT, rank 80 of 100, with full local ranks. Neither the CCNR criterion (‖R(ρ)‖₁ = 0.539 < 1) nor the reduction criterion (min eig +4.9·10⁻⁴) detects it. Its only certificate is the product-free-range (algebraic) argument. Toqito's full `is_separable` exhausted 7 GB RAM on it.
- **Measurement.** Tools must never return "separable". Record which criterion, if any, detects it, and how long the DPS hierarchy takes.
- **Risks.** It is mostly a stress test, with limited community uptake.
- **First step.** Publish the 100×100 matrix (built by our `zero_key_state.py` from the paper's integer pencil) and open a toqito issue.

---

## What is NOT an opportunity here

- **273 → amplifiers, mode-dependent loss, thermal wiretap, or thermal-channel quantum/private/trade-off capacities.** The paper disclaims these. The amplifier is not passive mixing. Non-degradable channels need regularization. Do not claim them as settled (table rows 10–12).
- **273 → wiretap/private/quantum capacity of pure loss and single-user thermal capacities.** These were already unconditional: Wilde–Qi 2016–18, WHG 2012, GGCH 2014, GHG 2015 and MGH 2014. The EPnI only re-derives them.
- **273 → tighter numbers for engineers.** The only new *quantitative* bounds concern exotic non-Gaussian environments, and there the EPnI improves on the qEPI-based capacity upper bound by just 0.02–0.055 bits (E2b). Real links are nowhere near these limits.
- **276 → superconducting-qubit engineering or code design.** At transmon-like ν ≈ 0.008–0.05 and per-gate γ ≈ 10⁻³–10⁻², the capacity is 0.975–0.997 bits. Prior bounds were already within 0.5–4.5·10⁻³ bits (Fang). Nobody operates qubit links as classical channels at capacity.
- **266 → redesign of d=6 tomography or QKD.** Practice already assumes no complete MUB set in d=6. Also do not cite N(6)=3 as established until the artifacts are public.
- **272 → changes to deployed QKD proofs or openQKDsecurity.** These compute protocol-specific rates, and entanglement was never treated as sufficient. PPT² was already known for Gaussian channels, so optical networks are unaffected.
- **277 → parallel DIQKD rates.** The explicit cubic rate needs ~8.7·10¹⁰ rounds (CHSH, δ = 0.1) to ~8·10¹¹ (magic square) just for 10⁻¹⁰ soundness, versus 1.5·10⁶ rounds in Nadlinger et al. with EAT. The universal δ⁵ rate has an unknown constant B₄. Threshold concentration above v also does not apply to honest CHSH devices and gives no min-entropy. Galactic.

---

## Experiment results (all in /home/claude/work/repos/scratch_qinfo/)

**E1: GADC exact capacity vs published bounds** (`gad_capacity.py`, `gad_fine.py`, `gad_two_use.py`, `gad_realistic.py`).
- **Formula validation.** At 6 points, the scalar formula matched a brute-force one-use Holevo optimization over 4-state Bloch ensembles (30 random restarts) to 10⁻¹⁵. The channel-action formula matched the KSW Kraus operators to 4·10⁻¹⁶.
- **Two-use additivity search** (8 entangled two-qubit pure states, 12 restarts, at (γ,ν) = (0.5,0.2), (0.3,0.05), (0.7,0.1)). The best χ(A⊗A) found equals 2χ(A) within 10⁻⁸, with no superadditivity. This is consistent with the theorem; a search can only falsify, not prove.
- **Max overshoot of prior upper bounds over the exact capacity** (γ grid 0.02–0.98, step 0.02, bits). KSW-min is the minimum of C_β, C_cov, C_Fil and C_EA; C_EB was also evaluated in the coarse grid and only wins inside or near the EB region.

| N (=ν) | Fang U_G max gap (at γ) | rel. | KSW-min max gap |
|---|---|---|---|
| 0.00 | 0.129 (0.50) | 27% | 0.319 (already exact via Tang et al.) |
| 0.01 | 0.092 (0.34) | 15% | 0.326 |
| 0.05 | 0.059 (0.28) | 9% | 0.343 |
| 0.10 | 0.044 (0.30) | 7% | 0.355 |
| 0.20 | 0.024 (0.36) | 4% | 0.368 |
| 0.30 | 0.011 (0.44) | 2% | 0.375 |
| 0.40 | 0.0026 (0.52) | 0.7% | 0.290 |
| 0.45 | 0.0007 (0.54) | 0.2% | 0.144 |

  - Fang − C ≥ −3.4·10⁻⁷ everywhere (grid-discretization noise), and KSW − C ≥ 0.
  - Caveats: the C_Fil sign convention was reconstructed from KSW Eq. 149. The literal "+" form went negative, so we used ½|log₂(N/(1−N))|. This only affects cells where C_Fil wins (N ≥ 0.4, mid γ). C_EA was computed from the Stinespring dilation with diagonal inputs (phase covariance). C_EB was computed by an SDP for the diamond distance to PPT (= EB for qubits) channels, plus a brute-force χ.
- **Verdict on materiality.** The improvement over KSW 2020 is large: they overshoot by 0.1–0.37 bits, often more than 100% of C. Over the September 2026 state of the art (Fang) it is modest: ≤ 0.09 bits, and only for N ≲ 0.2 at mid γ.
- **Transmon-like parameters** (5 GHz qubit, T_eff = 50–80 mK ⇒ ν = 0.008–0.047):
  - γ = 0.01: C = 0.9751 bits; Fang gap 3.5–4.5·10⁻³; C_β gap 2.1·10⁻².
  - γ = 0.1: C = 0.838–0.840; Fang gap 0.028–0.037.

**E2: EPnI side calculations** (`phi_convexity.py`, `nongauss_env_bound.py`).
- (a) φ_{λ,N′} is convex on the whole grid: min second divided difference +5.3·10⁻⁴ at λ = 0.95, N′ = 0. This supports the missing lemma for qinfo-2.
- (b) Beam splitter with a non-Gaussian Fock-mixture environment ((1−p)|0⟩⟨0| + p|1⟩⟨1|). The EPnI-based capacity upper bound improves the qEPI-based one by only 0.024–0.055 bits (η ∈ {0.5, 0.9}, N̄ ∈ {1, 10}, p ∈ {0.1, 0.3, 0.5}).

**E3: Family 272** (`zero_key_state.py`, `swap_identity.py`).
- The three shipped exact checks (`combinatorics_exact_checks.py`, `gadget_exact_check.py`, `exact_certificate.py`) reproduce byte-identically, about 1 s each.
- We rebuilt ρ = Z/tr Z from the integer pencil (eqs. explicit-matrices, L, UV, SR, phi-pair). Results:
  - tr Z = 1.302·10¹¹; PSD; PPT (min eig of ρ^{T_B} = −1.7·10⁻¹⁷);
  - rank 80; local ranks 10/10;
  - CCNR trace norm 0.539, so not detected; reduction criterion min eig +4.9·10⁻⁴, so not detected;
  - toqito `is_separable(level=1)` was killed by OOM at 7 GB, so the result is inconclusive.
- The swapping identity σ_AD = [(F†⊗G†)(M)]^T holds to 1.8·10⁻¹² (random CP maps; qinfo-6).

**E4: Family 277** (`repetition_rates.py`). Explicit cubic rate δ³/(16384(1+κ_μ)(1+ln d)):

| Game | δ | Rate per round | Rounds for 10⁻¹⁰ |
|---|---|---|---|
| CHSH (κ_μ = 96, d = 4) | 0.1 | 2.6·10⁻¹⁰ | 8.7·10¹⁰ |
| CHSH | 0.2 | — | 1.1·10¹⁰ |
| Magic square (κ_μ = 576, d = 16) | 0.1 | — | 8.2·10¹¹ |

For comparison, an i.i.d. Hoeffding benchmark needs about 1.2·10³ rounds at δ = 0.1.

**E5: Family 266 repo search.** Covered in "What the papers prove"; no artifacts exist in any public ref.

---

## Sources
- openai/math @ fd4aeeb (manuscripts and Lean as linked above); toqito @ 4baf22e; qiskit-aer @ fe964bf; thewalrus @ 54b1062.
- Guha–Shapiro–Erkmen, broadcast, PRA 76, 032303 (2007): https://arxiv.org/abs/0706.3416 ; EPnI: https://arxiv.org/abs/0710.5666 ; wiretap: https://arxiv.org/abs/0801.0841
- Wilde–Hayden–Guha: https://arxiv.org/abs/1105.0119 (PRA 86, 062306), https://arxiv.org/abs/1206.4886 (PRL 108, 140501)
- Wilde–Qi, energy-constrained private/quantum capacities: https://arxiv.org/abs/1609.01997 ; Qi–Wilde, amplifier capacities: https://arxiv.org/abs/1605.04922
- De Palma 2019: https://arxiv.org/abs/1805.12469 ; De Palma–Trevisan–Giovannetti: https://arxiv.org/abs/1605.00441 , https://arxiv.org/abs/1705.00499 ; survey: https://arxiv.org/abs/1803.02360
- Mari–Giovannetti–Holevo: https://arxiv.org/abs/1312.3545 ; Giovannetti–García-Patrón–Cerf–Holevo: https://arxiv.org/abs/1312.6225
- Guha PhD thesis: https://dspace.mit.edu/handle/1721.1/44413 ; Anderson–Guha–Bash ISIT 2021: https://experts.arizona.edu/en/publications/fundamental-limits-of-bosonic-broadcast-channels/ ; Yen–Shapiro MAC: https://arxiv.org/abs/quant-ph/0506171 ; Guha–Savov–Wilde: https://arxiv.org/abs/1102.2627
- Khatri–Sharma–Wilde: https://arxiv.org/abs/1903.07747 ; Fang 2026: https://arxiv.org/abs/2609.14621 ; Tang–Zhu–Bai–Wang 2026: https://arxiv.org/abs/2609.28592
- Khatri–Wilde textbook: https://arxiv.org/abs/2011.04672 ; Wilde textbook: https://arxiv.org/abs/1106.1445
- MUB: D'Ambrosio et al. https://arxiv.org/abs/1304.4081 ; Prat Colomer et al. https://quantum-journal.org/papers/q-2022-08-17-778/ ; McNulty–Weigert review https://quantum-journal.org/papers/q-2026-04-01-2051/ ; Five open problems https://arxiv.org/abs/2002.03233 ; OQP #13 https://oqp.iqoqi.oeaw.ac.at/mutually-unbiased-bases ; Fatah et al. https://arxiv.org/abs/2607.10615 ; Sun 2026 https://arxiv.org/abs/2610.12180 ; OAM HD-QKD survey https://arxiv.org/html/2512.11286v1
- PPT² / key: OQP #38 https://oqp.iqoqi.oeaw.ac.at/the-ppt-squared-conjecture/ ; OQP list https://oqp.iqoqi.oeaw.ac.at/open-quantum-problems ; Bäuml et al. https://arxiv.org/abs/1402.5927 ; Christandl–Ferrara https://arxiv.org/abs/1609.04696 ; Rahaman–Jaques–Paulsen https://arxiv.org/abs/1801.05542 ; An–Lee (qutrit) https://arxiv.org/abs/2607.15947
- DIQKD: Nadlinger et al. https://arxiv.org/abs/2109.14600 ; Arnon-Friedman et al. https://pmc.ncbi.nlm.nih.gov/articles/PMC5792631/ ; Jain–Miller–Shi https://arxiv.org/abs/1703.05426 ; Vidick https://arxiv.org/abs/1703.08508 ; Marwah–Dupuis https://arxiv.org/abs/2507.03991 ; Song https://eprint.iacr.org/2026/1702 ; DIQKD prospects thesis https://arxiv.org/abs/2111.11769
- Note: the web-search budget was exhausted near the end of this study. Textbook-section claims (Holevo, Serafini, Khatri–Wilde) are flagged "to check", not asserted.
