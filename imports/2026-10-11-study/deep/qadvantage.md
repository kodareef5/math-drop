# What the OpenAI math drop does to quantum-advantage claims and quantum-algorithm roadmaps

Theme `qadvantage`. Families: 102 (UGC / optimal approximation thresholds), 113 (FPRAS for perfect matchings in general graphs), 281 (QAOA reaches the SK optimum, plus its full-support companion), 274 (Parity is not in QAC0), 275 (QMA-hardness of continuum Coulomb energy), 284 (optimal quartic R-vs-Q query separation), 265 (2D area law and polynomial PEPS), 279 (exact quantum factoring), 283 (unitary synthesis from a Boolean oracle), 076 (LABS merit factor, only as a QAOA benchmark).

Repo pinned at openai/math `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Every result is an unreviewed model-generated claim.

**Bottom line.**
- **No new speedup.** Nothing in this theme gives a quantum or classical algorithm anyone should implement. The two algorithmic results (the 113 FPRAS and the classical SK optimizer that 281's companion makes unconditional) either have running times of degree about 6,500 or were already known to practice.
- **Value is redirection.** A short note to quantum-optimization and GBS groups is worth doing now. It should make three points:
  - **Max-Cut and Max-CSPs.** A polynomial-time quantum algorithm (QAOA, annealing, hybrids) whose worst-case or expected ratio beats Goemans–Williamson on Max-Cut, or beats the basic SDP on any Max-CSP, would now imply NP ⊆ BQP, with no UGC caveat.
  - **GBS on unweighted graphs.** The complexity-theoretic basis for GBS graph applications is gone, both for perfect-matching counting and, through an elementary ladder-graph reduction we checked exactly, for the ideal collision-free sampling law itself. Classical practice does not change: the FPRAS needs about 10^13155 steps at n = 10.
  - **QAOA on SK.** QAOA provably reaches the SK optimum. The classical competitor is now unconditional and linear in the input size at fixed ε. Any advantage can only lie in the unproven ε-scaling, and in our experiment 3 s of simulated annealing at n = 1000 matches QAOA depth p ≈ 240.
- **The rest.** 274, 275 and 265 confirm consensus and are existence or asymptotic results. 279, 283, 284 and 076 change nothing for roadmaps.

---

## What the papers actually prove

| Fam | Statement (theorem ref) | Constructive? | Constants / regime | Formal status |
|---|---|---|---|---|
| 102 | **Thm `thm:ugc`.** For all fixed ε, δ there is a deterministic poly-time reduction from 3SAT to unweighted, simple, bipartite Unique Games over F_2^s with translation constraints ([00-introduction.tex L22–39](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Unique-Games-Theorem-September-23-2026/build/sections/00-introduction.tex#L22-L39)). **Direct Max-Cut Thm `thm:main`/`thm:gap`.** For every α > α_GW = 0.878567 it is NP-hard to approximate Max-Cut within α on simple unweighted graphs, with completeness (1+t)/2 − ε against soundness (1+B(t))/2 + ε and B(t) = (2/π)·arcsin t ([introduction.tex L39–61](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Direct-Proof-of-Optimal-Max-Cut-Hardness-September-23-2026/build/sections/introduction.tex#L39-L61)). The reduction is a deterministic poly-time Karp reduction ([conclusion.tex L40–57](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Direct-Proof-of-Optimal-Max-Cut-Hardness-September-23-2026/build/sections/conclusion.tex#L40-L57)). Corollaries make Raghavendra's SDP-optimality for every Max-CSP, the factor-2 bound for Vertex Cover, ordering CSPs and others unconditional (07-consequences.tex, `cor:raghavendra-consequence` L64). | Yes, as reductions. | Galactic: the vertex count \|X\|^T·2^{2^{(n+1)T}} has a constant but astronomical factor. Worst case over all graphs only. | Lean: [`OptimalMaxCut.lean` L133–149](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/OptimalMaxCut.lean#L133-L149) states a poly-time `TM2` gap reduction from binary 3SAT with only the standard axioms. The solution tree `OAI/Computability/MaxCut` (372 files) has no `sorry`. I did not build it. |
| 113 | **Thm `thm:main`.** A uniform classical randomized algorithm approximates #PM(G) of any finite simple graph to (1±ε) with probability 1−δ, in worst-case time poly(input, 1/ε, log 1/δ), and returns exactly 0 when #PM = 0 ([main.tex L132–143](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex#L132-L143)). It gives samplers through JVV deletion (`lem:deletion-sampler` L3203) and counting for prescribed-degree subgraphs and size-k matchings (`cor:prescribed-degree` L3098). The companion gives a deterministic N(G)/512^n ≤ A ≤ N(G) for nonnegative integer multiplicities ([01-introduction.tex L201–212](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026/build/sections/01-introduction.tex#L201-L212)). | Yes, explicit chain. | Explicitly galactic: L = (10^4·N·D)^100 ([L1592–1597](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex#L1592-L1597)), q = 32L ([L2249–2253](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/build/main.tex#L2249-L2253)). The authors say the constants are "for transparent estimates rather than practical efficiency" (L300–303). Our computed degree is about 6,500 (see Experiments). | [`lean/docs/113.md`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/113.md) describes an FPRAS formalization (`MatchingFPRAS.lean`; `OAI/Combinatorics/MatchingCount`, 415 files, no `sorry`). The catalogue and `formalization.yaml` list only the entropy companion as formalized, so the listing is inconsistent. |
| 281 | **Thm `thm:main`.** For zero-field SK, lim_{p→∞} Q_p = P* ≈ 0.763166, where Q_p is the supremum over angles of the n→∞ limit of expected energy per spin. For each ε there exist a finite p and deterministic angles, independent of n and J, reaching P* − ε ([01-introduction.tex L111–119](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/QAOA-attains-the-SK-ground-state-energy-in-the-thermodynamic-first-limit-September-25-2026/build/sections/01-introduction.tex#L111-L119)). The paper itself says it gives "no quantitative finite-size estimate, depth bound, or efficient procedure for choosing the angles" (L131–133). The angle word may contain inverse gates and very large angles. **Cor `cor:regular-maxcut`.** On (D+1)-regular graphs of girth > 2p+1 the cut fraction is ≥ 1/2 + (P*−η)/√D, taking n→∞ and then D→∞ (L218–255). **Companion Thm `thm:full-support`.** Every zero-temperature Parisi minimizer has support [0,1) ([main.tex L119–131](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Full-support-of-the-zero-temperature-Sherrington-Kirkpatrick-order-parameter-September-27-2026/build/main.tex#L119-L131)). It then follows (**Cor `cor:algorithm`**) that the El Alaoui–Montanari–Sellke message-passing algorithm reaches max H − εn with probability → 1 using C(ε)·n² operations, with no assumption ([algorithm-application.tex L13–35](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Full-support-of-the-zero-temperature-Sherrington-Kirkpatrick-order-parameter-September-27-2026/build/algorithm-application.tex#L13-L35)). | QAOA: no (existence of p and angles). Classical: yes, but C(ε) is not quantified. | Thermodynamic limit first, then depth. No rate. | `lean/docs/281.md`: Lean covers the Parisi value identities and full support (`OAI/Probability/SKSupport`, 135 files, no `sorry`), **not** QAOA convergence. |
| 274 | **Thm `thm:parity`.** Fix depth d, c ≥ 1 and ε > 0. For all large n, no circuit of depth ≤ d on ≤ n^c qubits built from arbitrary 1-qubit gates and unbounded-arity Toffoli gates computes parity with advantage ε, with no mid-circuit measurement, postselection or fanout gate ([introduction.tex L22–35](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Product-projection-localization-and-the-QAC0-parity-lower-bound-September-24-2026/build/sections/introduction.tex#L22-L35)). The proof works in the larger model of layers of **product-state reflections I − 2A**, which covers C^kZ/C^kX in any local basis ([localization.tex L32–50](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Product-projection-localization-and-the-QAC0-parity-lower-bound-September-24-2026/build/sections/localization.tex#L32-L50)). **Cor `cor:state-preparation`.** Every prepared n-qubit state has felinity < n^{−a}, so no inverse-polynomial weight sits on both a string and its complement (this rules out GHZ/cat states). Dicke states with n^δ ≤ k ≤ n/2 cannot be reached within trace distance 1/(80k) ([consequences.tex L35–49](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Product-projection-localization-and-the-QAC0-parity-lower-bound-September-24-2026/build/sections/consequences.tex#L35-L49)). | No (lower bound). | Asymptotic only, with no explicit n₀. | Lean-formalized (`QACParity`, listed in `formalization.yaml`). |
| 275 | **Thm `thm:main`.** Approximating the ground-state energy of the 3D continuum electronic Hamiltonian is QMA-hard. This holds with unit-charge nuclei at distinct rational positions, a unary electron count, the full spinful antisymmetric continuum, and threshold separation ≥ 1, under deterministic classical poly-time Karp reductions. QMA membership is not asserted ([introduction.tex L91–108](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026/build/introduction.tex#L91-L108)). | Yes, as a reduction. | Instances are hydrogen clusters stretched polynomially, with k = ⌈C·n^A⌉ and λ = 8k³/ρ for "sufficiently large absolute" A and C (`sections/implementation.tex` L19–23). | `lean/docs/275.md` describes a formalization (`OAI/MathematicalPhysics/ContinuumCoulomb`, no `sorry`); it is not listed in `formalization.yaml`. |
| 265 | **Thm `thm:area`.** A unique ground state with global gap Δ of a finite-range Hamiltonian on any induced square-lattice domain satisfies S(A) ≤ C(q,R,J,Δ)·\|∂A\| ([00-introduction.tex L39–53](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/build/sections/00-introduction.tex#L39-L53)). **PEPS Thm `thm:main`.** On an open L×L grid there is a PEPS with bond dimension C·L^c and global error L^{−1}. The paper explicitly makes "no claim that its tensors can be found or contracted efficiently" ([PEPS 00-introduction.tex L36–66](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-PEPS-approximation-of-gapped-square-grid-ground-states-September-24-2026/build/sections/00-introduction.tex#L36-L66)). **Prop `prop:positive`.** There are quasi-local 0 ≤ k_i ≤ I with k_iΩ = 0, Σk_i ≥ g(I − P_Ω), and tails e^{−c·l^α} ([03-quasilocal.tex L220–246](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/build/sections/03-quasilocal.tex#L220-L246)). Building them requires the **ground-state expectation ⟨Ω,h_iΩ⟩** as the centering constant (L250–256). | No (existence). | c is unspecified and large: internal errors of L^{−60} and patch ranks e^{C_Q(1+u)}. | Not formalized. |
| 279 | Polynomial-size uniform circuits over a fixed finite gate set factor every N with probability exactly 1 ([01-introduction.tex L10–13, L44–50](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-quantum-factoring-over-a-fixed-finite-gate-set-September-25-2026/build/sections/01-introduction.tex#L10-L50)). The paper says its "large polynomial parameters are not intended as practical resource improvements". | Yes. | Large polynomials. | Lean doc present. |
| 283 | A fixed poly-size oracle circuit approximates any n-qubit unitary to diamond error 1/2 for a suitably chosen Boolean oracle. That oracle may have an unrestricted truth table, and no efficient way to construct it is given ([01-introduction.tex L46–65](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/01-introduction.tex#L46-L65)). | Not for the oracle. | Error 1/2. | Not formalized. |
| 284 | α_tot = 4: R(f) = O((1+Q)^4) is tight, via total functions with Q ≤ C·√m·polylog and R ≥ c·m^{2−1/k}/log² ([01-introduction.tex L29–42](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Nearly-Quartic-Separation-Between-Randomized-and-Quantum-Query-Complexity-October-5-2026/build/sections/01-introduction.tex#L29-L42)). | Explicit but contrived functions. | Polylog losses. | Not formalized. |
| 076 | max_A F(A) → ∞ over all lengths N ([merit-morse.tex L22–36](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotically-minimal-maxima-of-real-Littlewood-polynomials-September-23-2026/build/merit-morse.tex#L22-L36)). The paper gives "no useful convergence rate or efficient signing algorithm" (introduction.tex L36–39). | No. | No N₀. | Lean-formalized. |

**Where the triage was off.**
- **102.** The triage was correct, and its conclusion is stronger than it stated:
  - **Expected ratio is enough.** An *expected*-ratio guarantee E[cut] ≥ α·OPT with α > α_GW also implies NP ⊆ BQP. Markov's inequality on OPT − cut gives a constant success probability at some α′ ∈ (α_GW, α), and repetition amplifies it. The resulting quantum decider for 3SAT has one-sided error, because in the NO case no cut exceeds the threshold.
  - **Every Max-CSP.** The same holds for every Max-CSP against Raghavendra's SDP threshold.
  - **Quantum Max-Cut.** UG-based hardness for Quantum Max-Cut loses its UGC hypothesis. HNPTW's 0.956 still needs their vector-valued Borell conjecture. The product-state 0.9859 hardness in arXiv:2306.03912 becomes ordinary NP-hardness, provided its quantifier order matches `thm:ugc`, which should be checked.
- **113.** The triage understated the result:
  - **Weighted case.** It said nonnegative weights are covered only by the weak 512^n factor. In fact, weights that are polynomially bounded rationals reduce to the unweighted FPRAS with the standard gadget of w parallel 3-edge paths.
  - **GBS sampling.** It said GBS sampling arguments are untouched. The random-complex-matrix hardness arguments are indeed untouched. The **ideal collision-free GBS law on an unweighted graph**, however, is exactly a perfect-matching law of a ladder graph (verified below), so 113 together with JVV gives a classical polynomial-time sampler in principle.
- **281.** The triage read the result as "a statement of no advantage", which is only half right:
  - **The main theorem favours QAOA.** It proves that QAOA *can* reach the optimum, which the conjecture of Basso et al. had left open.
  - **The "no advantage" reading comes from the companion,** which makes the classical optimizer unconditional. Chen (arXiv:2607.18032, July 2026) had already obtained the same full-support theorem independently, so this is not new to the drop.
  - **Neither paper bounds rates.** Neither p(ε) nor C(ε) is bounded.
- **265.** The triage was correct. Add two points. Polynomial-time algorithms for this class are ruled out unless NP = RP, as shown below. The AGSP idea based on `prop:positive` is circular, because the centering constant is the ground-state local energy.

---

## Current practice and state of the art

**Max-Cut and quantum optimization (102).**
- **Worst-case benchmarks before the drop.** α_GW was optimal only under UGC (KKMO 2007), and the unconditional NP-hardness bound was 16/17 (Håstad plus TSSW gadgets).
- **"Beats GW" claims are instance-specific.**
  - Tate et al. (Quantum 7, 1121, 2023, [arXiv:2112.11354](https://arxiv.org/abs/2112.11354)) report that warm-started QAOA beats GW empirically on 1,148 graphs with ≤ 11 nodes at p = 8. Their provable p = 0 ratios are 0.658 and 0.585, both below GW.
  - Wurtz & Lykov ([arXiv:2107.00677](https://arxiv.org/abs/2107.00677)) say that, under their numerical fixed-angle conjecture, QAOA at p ≥ 11 has a larger guarantee than GW **on 3-regular graphs**. That class already has a classical 0.9326 algorithm (Halperin–Livnat–Zwick 2004, J. Algorithms), which they do not compare against.
- **Local-algorithm limits.** Barak & Marwaha ([arXiv:2106.05900](https://www.arxiv.org/abs/2106.05900)) show that 1-local algorithms are bounded away from the optimum on high-girth graphs. A classical local algorithm reaches 1/2 + (2/π)/√D.
- **Annealing.** The scaling-advantage claims for annealing are ensemble time-to-ε results on spin-glass instances (Munoz-Bauza & Lidar, PRL 2025, [arXiv:2401.07184](https://arxiv.org/html/2401.07184v1)), so they are average-case.
- **Code.** Qiskit Optimization ships GW only as a baseline and warm-start presolver:
  - `GoemansWilliamsonOptimizer._solve_max_cut_sdp`, documented as ".878-approximation" ([L237–246](https://github.com/qiskit-community/qiskit-optimization/blob/65ce191a4c3ed48f203d8dd6eea476d0deea9e71/qiskit_optimization/algorithms/goemans_williamson_optimizer.py#L237-L246));
  - `WarmStartQAOAOptimizer(pre_solver=…)` ([L202–224](https://github.com/qiskit-community/qiskit-optimization/blob/65ce191a4c3ed48f203d8dd6eea476d0deea9e71/qiskit_optimization/algorithms/warm_start_qaoa_optimizer.py#L202-L224)).
- **Quantum Max-Cut.**
  - Hardness is UGC-conditional: HNPTW ([arXiv:2111.01254](https://arxiv.org/abs/2111.01254v2)) and arXiv:2306.03912 (0.9859 for product states under UGC, with a vector-Borell inequality proved in a restricted range).
  - Crosta et al. ([arXiv:2606.27224](https://arxiv.org/abs/2606.27224)) claim a *conditional* 0.651 ratio using Rydberg annealing plus SDP, against 0.614 for SDP alone.

**GBS graph applications (113).**
- **Hardness basis.** GBS hardness rests on |Haf|² of random complex Gaussian matrices (Hamilton et al. 2017, [arXiv:1612.01199](https://arxiv.org/pdf/1612.01199)). Graph applications embed a *nonnegative* adjacency matrix, so for an unweighted graph Pr(S) ∝ c^{\|S\|}·#PM(G[S])².
- **Application papers.**
  - Brádler et al. (PRA 98, 032310, 2018, [arXiv:1712.06729](https://arxiv.org/abs/1712.06729v1)) claim GBS can estimate #PM of arbitrary graphs "significantly faster" than a classical computer. Their estimator uses the all-ones event, whose probability they acknowledge decays exponentially. No classical runtime comparison is given.
  - Arrazola & Bromley (PRL 2018, [arXiv:1803.10730](https://arxiv.org/abs/1803.10730)) on dense subgraphs and Schuld et al. (PRA 2020, [arXiv:1905.12646](https://arxiv.org/abs/1905.12646)) on graph similarity motivate GBS by the hafnian–matching link. They do not prove hardness: Schuld et al. call the computation "possibly even intractable".
  - Jiuzhang graph experiments (Deng et al., PRL 130, 190601, 2023, [arXiv:2302.00936](https://arxiv.org/abs/2302.00936)) report empirical enhancement only.
- **Dequantization already under way.**
  - Oh, Fefferman, Jiang, Quesada (PRX Quantum 5, 020341, 2024, [arXiv:2302.00536](https://arxiv.org/abs/2302.00536)) give a classical sampler ∝ Haf and find "the advantage from GBS is not significant in general". They note nonnegative-hafnian approximation is only known to lie in BPP^NP.
  - Solomons et al. ([arXiv:2301.13217](https://arxiv.org/abs/2301.13217)) find at most a polynomial speedup for dense subgraph finding.
  - Zhang et al. ([arXiv:2505.02445](https://arxiv.org/abs/2505.02445)) give MCMC sampling of the GBS law, provably poly-time **only for dense graphs**. They name uniform PM sampling on non-bipartite graphs, whose mixing time is open, as the bottleneck. **113 removes exactly this obstacle, in principle.**
- **Code.**
  - The Walrus exact hafnian is O(n³·2^{n/2}) (docs, algorithms.rst). Its only approximate method is Barvinok's estimator for nonnegative matrices: `hafnian(approx=True)` → `hafnian_approx` ([_hafnian.py L801–808, L1069–1085](https://github.com/XanaduAI/thewalrus/blob/54b1062e2b6759ddc733ca6bf636df580ff94968/thewalrus/_hafnian.py#L1069-L1085)). That estimator can need exponentially many samples (Uvarov & Vinichenko, [arXiv:2312.10143](https://arxiv.org/abs/2312.10143)).
  - The docs state that approximate PM-counting methods target real or positive weighted graphs ([algorithms.rst L35](https://github.com/XanaduAI/thewalrus/blob/54b1062e2b6759ddc733ca6bf636df580ff94968/docs/algorithms.rst#L35)).
  - Strawberry Fields `apps` builds the dense-subgraph and similarity tools on these papers ([subgraph.py L14–19](https://github.com/XanaduAI/strawberryfields/blob/162125d8ad5fd5488322a30c520253189596adf5/strawberryfields/apps/subgraph.py#L14-L19), [similarity.py L14–21, L98–106](https://github.com/XanaduAI/strawberryfields/blob/162125d8ad5fd5488322a30c520253189596adf5/strawberryfields/apps/similarity.py#L98-L106)). The last commit (Jan 2026) decommissioned Xanadu's quantum cloud.

**QAOA on SK (281).**
- **Infinite-size analyses.**
  - FGGZ (Quantum 6, 759, 2022, [arXiv:1910.08187](https://arxiv.org/abs/1910.08187)) computes infinite-size QAOA on SK up to p = 12. At p = 11 it beats the standard SDP, and the authors "hope to match" Montanari.
  - Basso et al. (TQC 2022, [arXiv:2110.14206](https://arxiv.org/abs/2110.14206)) go to p = 20. They claim p = 11 beats "all known classical algorithms free of unproven conjectures" on large-girth regular graphs, and conjecture convergence to Parisi.
- **The classical algorithm was conditional.** Montanari ([arXiv:1812.10897](https://arxiv.org/abs/1812.10897), SICOMP) and EAMS (Ann. Probab. 2021; RSA 2023 local MaxCut, Thm 1.7) rest on a no-overlap-gap assumption (the minimizer γ* is strictly increasing). That assumption was proved in July 2026 by Chen (zero temperature, [arXiv:2607.18032](https://arxiv.org/abs/2607.18032)), building on Lopatto's positive-temperature full-RSB result ([arXiv:2607.11756](https://arxiv.org/abs/2607.11756)), and again by the drop's companion.
- **Current quantum claims.**
  - Boulebnane et al. (JPMC/Argonne, [arXiv:2505.07929](https://arxiv.org/abs/2505.07929)) reach p = 160 with ε ≲ 2.2% (energy 0.7461, with angles extrapolated from p = 80). They give numerical depth scaling O(n/ε^{1.13}) and claim a "potential polynomial speedup", calling Montanari's C(ε) exponential in 1/ε.
  - Sels & Morone ([arXiv:2607.08708](https://arxiv.org/abs/2607.08708), "Absence of quantum advantage for approximate spin glass optimization") find that a semiclassical truncated-Wigner version matches or slightly beats spin-1/2 QAOA, converging like log p/p. I read only the abstract and a news summary.
- **Code.** QOKit ships the fixed SK angles and infinite-size energies for p ≤ 80 ([`best_SK_QAOA_parameters.json`](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/assets/best_SK_QAOA_parameters.json#L449): p = 11 → 0.6408; [L1242](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/assets/best_SK_QAOA_parameters.json#L1242): p = 80 → 0.7397). They are loaded by [`_get_sk_gamma_beta` L193–222](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/parameter_utils.py#L193-L222), which extrapolates in Fourier space beyond p = 80.

**Shallow circuits and hardware (274).**
- **Native multi-qubit gates.** Neutral atoms provide CZ/CCZ by Rydberg blockade (Levine et al. PRL 2019, [arXiv:1908.06101](https://arxiv.org/abs/1908.06101); Evered et al. Nature 2023, [arXiv:2304.05420](https://arxiv.org/abs/2304.05420)).
- **Long-range entanglement.** IBM produces it with dynamic circuits, using mid-circuit measurement and feedforward (Bäumer et al., [arXiv:2308.13065](https://arxiv.org/abs/2308.13065): 101-qubit CNOT teleportation and GHZ preparation).
- **Ions.** Trapped ions use global Mølmer–Sørensen and Ising gates; Maslov & Nam ([arXiv:1707.06356](https://arxiv.org/abs/1707.06356)) show global interactions reduce entangling-gate counts.
- **Prior QAC0 lower bounds** all needed ancilla or depth restrictions: Rosenthal 2021; Anshu–Dong–Ou–Yao 2025; Fenner et al. 2025 ([arXiv:2504.06433](https://arxiv.org/abs/2504.06433)).

**2D ground states (265).**
- **Practice.** People use iPEPS with small bond dimension D and 2D DMRG on cylinders, whose bond dimension grows exponentially in the width.
- **Provable algorithms.**
  - 1D gapped systems have the Landau–Vazirani–Vidick polynomial-time algorithm ([arXiv:1307.5143](https://ar5iv.arxiv.org/html/1307.5143)) and its RRG successors.
  - In 2D, the best result covers frustration-free, locally gapped systems and runs in time exp(n^{1/2+o(1)}) (Abrahamsen, [arXiv:2004.02850](https://arxiv.org/abs/2004.02850)). The same paper shows polynomial time is impossible unless NP = RP, even for *classical* frustration-free 2D instances with a unique ground state and gap 1, via planar 3SAT and Valiant–Vazirani.
  - Anshu–Arad–Gosset (STOC 2022, [arXiv:2103.02492](https://arxiv.org/abs/2103.02492)) prove a 2D area law for frustration-free, locally gapped systems.

**Chemistry (275).**
- **Prior hardness.** O'Gorman–Irani–Whitfield–Fefferman ([arXiv:2103.08215](https://arxiv.org/abs/2103.08215)) prove QMA-completeness of electronic structure in a fixed basis. Schuch–Verstraete 2009 did the continuum with designed potentials.
- **Assessments.** Lee et al. (Nat. Commun. 14, 2023, [link](https://ideas.repec.org/a/nat/natcom/v14y2023i1d10.1038_s41467-023-37587-6.html)) find exponential advantage unlikely for generic problems. The positive case rests on guided or structured instances (Gharibian–Le Gall, [arXiv:2111.09079](https://arxiv.org/abs/2111.09079)).

**Roadmap items (279, 283, 284, 076).**
- **Factoring.** Resource estimates are driven by Gidney 2025, under one million noisy qubits for RSA-2048 ([arXiv:2505.15917](https://arxiv.org/abs/2505.15917v1)).
- **Superquadratic speedups.** Babbush et al. argue error-corrected advantage needs better than quadratic speedups (PRX Quantum 2021, [arXiv:2011.04149](https://arxiv.org/abs/2011.04149)).
- **LABS.**
  - The QAOA-on-LABS scaling paper (Shaydulin et al., Sci. Adv. 2024, [arXiv:2308.02342](https://arxiv.org/abs/2308.02342v2)) measures time to the **exact optimum** at N ≤ 40: QAOA+QMF scales as 1.21^N against 1.34^N for memetic tabu.
  - Its motivation contrasts falling best-known merit factors with an asymptotic limit that "predicts the merit factor should stay approximately constant".
  - QOKit's [`true_optimal_mf`](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/labs.py#L15-L17) tabulates exact optima from Packebusch–Mertens.

---

## Claim → what the drop now implies → strength

| # | Claim currently made (industry / literature) | What the drop implies | Strength |
|---|---|---|---|
| 1 | A QAOA, annealer or Ising machine could beat GW's 0.878 for Max-Cut (worst case, poly time). | Impossible unless **NP ⊆ BQP**, even for expected-ratio guarantees, because the reduction is a classical deterministic Karp reduction. Before the drop this would only have refuted UGC. | **Strong** formally (Lean-formalized). Low practical stakes, because few papers make an explicit worst-case claim. |
| 2 | "Beats GW" on small graphs, 3-regular graphs or fixed-angle instances is evidence of advantage (Tate et al. 2023; Wurtz–Lykov 2021). | GW is the wrong yardstick. On general graphs nothing beats it in the worst case. On restricted classes the classical baselines are stronger (0.9326 on cubic graphs; PTAS for dense graphs; exact on planar graphs). Compare instance by instance against GW plus local search and strong heuristics. | **Moderate** (redirects framing). |
| 3 | The basic SDP is optimal for every Max-CSP only under UGC. | Now under P ≠ NP (Raghavendra corollary). Quantum worst-case ratios above the SDP threshold imply NP ⊆ BQP for *every* Max-CSP. | **Strong**, practically low. |
| 4 | Quantum Max-Cut hardness is UGC-conditional (HNPTW; arXiv:2306.03912). | The UGC hypothesis drops. 0.956 still needs vector-valued Borell. The product-state 0.9859 becomes NP-hard, pending a quantifier check. Conditional quantum ratios such as 0.651 are not affected. | **Moderate**, needs expert check. |
| 5 | GBS estimates #PM of arbitrary graphs faster than classical computers (Brádler et al. 2018). | A classical **FPRAS** exists (113), while the GBS estimator needs exponentially many samples in general. The complexity-theoretic claim is reversed. The practical picture is unchanged: exact O(n³·2^{n/2}) beats the FPRAS below n ≈ 2.8×10⁵. | **Strong** (complexity); none (practice). |
| 6 | Sampling GBS on graphs is classically hard, which underpins dense-subgraph, max-hafnian and similarity applications. | For **unweighted** graphs, and for weights that are polynomially bounded positive rationals, the ideal lossless collision-free PNR law is a perfect-matching law of a ladder graph. FPRAS plus JVV then gives a classical poly-time sampler in principle. Lossy, threshold-detector, complex and negative-weight cases are not covered. This reinforces existing dequantizations (Oh et al. 2024; Zhang et al. 2025). | **Moderate–strong** in principle; none in practice. |
| 7 | GBS random-matrix advantage experiments (Jiuzhang, Borealis) rest on hafnian hardness. | Untouched: they use complex Gaussian matrices, which are not nonnegative. | **None**. |
| 8 | p = 11 QAOA beats every classical algorithm free of unproven conjectures (Basso et al. 2022). | **Obsolete.** The EAMS local algorithm reaches P* (1/2 + P*/√D on large-girth graphs) **unconditionally** (Chen 2026; drop companion), against 0.6408 for p = 11 QAOA. | **Strong**, narrow. |
| 9 | QAOA on SK may give a polynomial quantum speedup (Boulebnane et al. 2025). | Precondition proven: QAOA converges to P* in the thermodynamic-first limit. No depth bound. The classical competitor is now unconditional with O(n²) cost, linear in the input at fixed ε. Any advantage must come from ε-scaling, which neither paper addresses. Practically, 3 s of simulated annealing at n = 1000 equals p ≈ 240 (Experiment 3). | **Neutral** on the speedup claim; **strong** that advantage is only possible in ε-dependence. |
| 10 | Native C^kZ/Toffoli gates (Rydberg, ions) enable constant-depth GHZ, fanout or parity. | False for large n without measurement plus feedforward or a multi-target or global (fanout-type) gate. Dicke states are also obstructed. No explicit n₀. | **Moderate** (asymptotic). |
| 11 | An area law means 2D gapped ground states are classically easy (PEPS). | Existence only: a polynomial-bond-dimension PEPS exists but is neither constructed nor contracted. The class contains NP-hard instances (unless NP = RP), so neither classical nor quantum computers can solve it in poly time in the worst case. Practice is unchanged. | **Strong** against "easy"; weak for practice. |
| 12 | Quantum computers will solve electronic structure (ground-state energies) in general. | The continuum problem with protons only is QMA-hard, so a generic efficient quantum algorithm would imply QMA ⊆ BQP. This closes the basis-set loophole in O'Gorman et al. Advantage must come from structure (guided states, good initial overlap). | **Moderate** (confirms consensus). |
| 13 | Superquadratic or quartic query speedups are a roadmap target (Babbush et al.). | Quartic is the maximum for total functions, and it is attained by contrived functions. No practical problem follows. | **Weak / none**. |
| 14 | Exactness or retries matter for factoring resource estimates. | Exact poly-size factoring exists, but its polynomials are large. No change to Gidney-style estimates. | **None**. |
| 15 | Unitary synthesis implies efficient compilation of arbitrary unitaries. | It needs an exponential-size oracle and achieves error only 1/2. | **None**. |
| 16 | The LABS optimal merit factor is asymptotically bounded or constant (benchmark motivation). | Max merit factor → ∞, but non-constructively and with no rate. Benchmarks of time to the exact optimum at N ≤ 66 are unaffected. | **Weak** (wording only). |

---

## Opportunities

### qadvantage-1: Note to quantum-optimization groups on worst-case-ratio framing (102). REDIRECT, pursue now
- **Proposed change.** Publish a 2–3 page note stating the following:
  - **Max-Cut and Max-CSPs.** For general graphs, any poly-time quantum algorithm whose worst-case or expected approximation ratio exceeds α_GW on Max-Cut would imply NP ⊆ BQP. The same holds against the Raghavendra SDP threshold for any Max-CSP. The reduction is the deterministic Karp reduction of `thm:gap`.
  - **Worst-case ratio is not a target.** It cannot be beaten. Compare against GW plus local search and best-in-class heuristics on fixed instance families, and use class-specific baselines on restricted classes: 0.9326 on cubic graphs, PTAS on dense graphs, exact algorithms on planar graphs.
  - **Optional docs PR.** Add one sentence to Qiskit's GW docstring ([L237–246](https://github.com/qiskit-community/qiskit-optimization/blob/65ce191a4c3ed48f203d8dd6eea476d0deea9e71/qiskit_optimization/algorithms/goemans_williamson_optimizer.py#L237-L246)): "optimal worst-case ratio for poly-time algorithms unless P = NP (2026)".
- **Beneficiaries.** Quantum-optimization benchmarking groups, reviewers, and vendor marketing teams that compare against GW.
- **Measurement.** Track how often new QAOA and annealing papers cite "beats GW" without an instance-family qualifier, and whether the docstring PR is accepted.
- **Risks.**
  - Results are unreviewed; mitigated because the top-line statement is Lean-formalized.
  - Low marginal value, since the community already assumed UGC.
  - Restricted graph classes and non-polynomial (annealing-time) regimes fall outside the statement.
- **First step.** Draft the note around rows 1–4 of the table, citing `thm:gap` and `OptimalMaxCut.lean`.

### qadvantage-2: Quantum Max-Cut hardness without UGC (102). CERTIFY, monitor
- **Claim to check.** HNPTW (arXiv:2111.01254) and arXiv:2306.03912 use standard UG reductions. If their parameter order matches `thm:ugc` (errors fixed before the alphabet), their UG-hardness becomes NP-hardness:
  - product-state Quantum Max-Cut at 0.9859, unconditionally;
  - 0.956+ε, conditional only on vector-valued Borell.
- **Action.** Ask the HNPTW authors or a UG expert to confirm, then update survey tables. The value is low but cheap to realize.

### qadvantage-3: Retire the GBS perfect-matching-counting advantage claim (113). REDIRECT, pursue now
- **Proposed change.** A short comment or blog post on the Brádler et al. 2018 claim. Classical approximate counting of PMs in unweighted general graphs is now in FPRAS. The GBS estimator's sample cost grows exponentially for general graphs, so there is no complexity-theoretic quantum advantage for this task, and in fact a reversal. In practice, exact counting (The Walrus, O(n³·2^{n/2})) wins at every feasible size.
- **Docs PR.** Optionally update The Walrus [algorithms.rst L35](https://github.com/XanaduAI/thewalrus/blob/54b1062e2b6759ddc733ca6bf636df580ff94968/docs/algorithms.rst#L35) with one sentence on the 2026 FPRAS and its galactic degree.
- **Risk.** The FPRAS is unreviewed. A Lean formalization is described, but the listing is inconsistent.

### qadvantage-4: Complexity status of ideal unweighted-graph GBS sampling, via the ladder reduction (113). RESEARCH/REDIRECT, pursue as research
- **Observation, verified exactly (Experiment 2).** Let G be a graph with adjacency A. Build a ladder: two copies of G, plus a rung of weight r_v joining the two copies of each vertex v, and give every G-edge weight x in both copies. Then

  Σ_S x^{|S|}·Π_{v∉S} r_v·Haf(A_S)² = Haf(ladder).

  The set of vertices not covered by rungs in a random perfect matching of the ladder therefore follows exactly the collision-free GBS law Pr(S) ∝ x^{|S|}·Haf(A_S)².
- **Why this yields a sampler.** Rational x and r become unweighted graphs by the parallel-path gadget. The 113 FPRAS plus JVV self-reduction (`lem:deletion-sampler`) then gives a **classical polynomial-time approximate sampler** for the ideal lossless, collision-free, PNR GBS distribution on unweighted graphs. This is the step Zhang et al. 2025 could only do for dense graphs.
- **Deliverable.** A 4-page technical note:
  - extend the reduction to collision patterns (blow-up graphs, since Haf(A_n) counts PMs of a vertex-replicated graph) and to node weights (`waw_matrix`);
  - state exactly which GBS application claims lose their hardness basis;
  - state what remains: loss, threshold detectors (Torontonian), and complex or negative weights.
- **Benefit and measurement.** Theory redirect. Measure by acceptance and citation in the GBS-applications literature.
- **Risks.**
  - The construction may be folklore.
  - It inherits the galactic degree of about 6,500, so it has zero practical consequence.
  - Collision handling needs care.

### qadvantage-5: Classical-side time-to-ε benchmark for SK and large-girth Max-Cut (281). BENCHMARK + REDIRECT, pursue now
- **Proposed change.** Write a benchmark and short note for the QAOA-on-SK advantage discussion (JPMC/Argonne, MIT and Google groups):
  1. **Retire the Basso et al. claim.** The "p = 11 QAOA beats all unconditional classical algorithms" statement is obsolete, because EAMS and IAMP are now unconditional (Chen 2026, independently the drop's companion).
  2. **Report time-to-ε curves on the same instances.** Use QAOA p(ε) (from QOKit's infinite-size table, [JSON L449/L1242](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/assets/best_SK_QAOA_parameters.json#L1242)), IAMP with numerically solved Parisi γ, and SA/PT heuristics, at n = 10³–10⁵.
  3. **Count resources fully.** Report gate count p·n(n−1)/2 per shot for QAOA against wall-clock time for the classical methods.
- **Experiment 3 already shows the scale.** QAOA needs depth p ≈ 240 (about 1.2×10⁸ ZZ gates per shot) to match 3 s of single-core SA at n = 1000.
- **Targets.** QOKit [`parameter_utils._get_sk_gamma_beta` L193–222](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/parameter_utils.py#L193-L222) and [`sk.py` L13–23](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/sk.py#L13-L23), which uses the same normalization as the paper.
- **Measurement.** A fitted C(ε) for IAMP and SA. Determine whether a polynomial-in-1/ε classical scaling with exponent ≤ 1.13 is observed, which would remove the claimed speedup, or whether IAMP really blows up exponentially.
- **Risks.**
  - IAMP needs an accurate Parisi γ near t → 1.
  - Finite-n energies sit below P*, so comparisons must use the same n.
  - SA is a heuristic without guarantees, so a theorem-level comparison needs IAMP.
- **First step.** Port an IAMP implementation for SK, which needs only a discretized Parisi PDE, and reproduce the n ≈ 10⁴ curve.

### qadvantage-6: Architecture note on the multi-control vs multi-target distinction (274). REDIRECT, monitor
- **What is ruled out.** In the model of 1-qubit gates plus product-state reflections (C^kZ/C^kX in any local basis, which is the Rydberg-blockade native gate), constant-depth circuits on polynomially many qubits cannot compute parity or fanout, and cannot prepare GHZ-like or Dicke(k ≥ n^δ) states, for large n.
- **Routes that remain open.** The theorem does **not** cover:
  - mid-circuit measurement plus feedforward (IBM dynamic circuits);
  - one-control/many-target gates (fanout-type "mesoscopic" Rydberg gates);
  - global MS/Ising gates on ions;
  - multi-controlled phases other than π.
- **Resource estimates.** Estimates should therefore budget either log depth, dynamic circuits, or a fanout-type primitive.
- **Why only monitor.** No explicit n₀ is given, nobody currently designs constant-depth GHZ from C^kZ, and Dicke-state circuits in use (e.g. QOKit [`dicke_state_utils.dicke_simple` L205–215](https://github.com/jpmorganchase/QOKit/blob/a00cc72adc29ef72d04e7f72272431e641f7d1eb/qokit/dicke_state_utils.py#L205-L215)) are already linear or log depth. Fold this into the qadvantage-1 note as one paragraph.

### qadvantage-7: Continuum electronic-structure QMA-hardness in advantage assessments (275). CERTIFY/REDIRECT, pursue now (citation-level)
- **What to update.** Assessments of chemistry advantage and resource-estimation papers. Worst-case ab initio ground-state energy is QMA-hard **in the continuum with protons only**, so neither classical nor quantum computers can solve it generically unless QMA ⊆ BQP. Advantage claims must name the structural assumption they rely on (initial-state overlap, adiabatic gap, guided input).
- **Why it matters.** It removes the "artifact of a finite basis" objection to O'Gorman et al. 2022.
- **Cost and risk.** One paragraph in the note. The instances are polynomially stretched hydrogen clusters, irrelevant to real molecules, and the paper does not assert QMA membership.

### qadvantage-8: Provable subexponential algorithm for frustrated, globally gapped 2D systems (265). RESEARCH, low priority
- **What is possible.** Polynomial time is impossible (see below). The meaningful target is an exp(Õ(L)) = exp(Õ(√n)) algorithm for open L×L grids. That would match Abrahamsen's frustration-free bound and the rETH lower bound, and would rigorously justify 2D DMRG with bond dimension exponential in the width for the frustrated case.
- **Existence side.** The PEPS theorem gives snake-MPS existence with bond dimension (C·L^c)^{L+1} = exp(O(L log L)) at error 1/L. The open problem is the *search*.
- **Obstacle.** The positive operators of `prop:positive` need ⟨Ω,h_iΩ⟩ as their centering constant (L250–256), so they cannot be built without already knowing the ground state's local energies. A self-consistent or bootstrapped estimation scheme would be new research.
- **Scores.** Effort 1, time to value 1.

---

## What is NOT an opportunity here

- **Implementing the 113 FPRAS** for GBS benchmarking, hafnian estimation, or anything else. The lower bound on chain steps is 10^13155 at n = 10 and 10^20792 at n = 144 (Jiuzhang's mode count), with running-time degree about 6,500. It beats exact O(n³·2^{n/2}) only beyond n ≈ 282,000, where both cost about 10^42519. This is galactic, and Barvinok-type estimators and exact solvers remain the tools.
- **Using 281 to choose QAOA angles or depths.** The construction is an existence proof. Its word uses seed simulation, echoes, inverse gates and very large angles, with no bound on p. QOKit's numerically optimized and extrapolated angles are strictly more useful.
- **Treating 281 as evidence *for* a QAOA speedup.** It proves only what the classical algorithm already achieves: reaching P* − ε. At fixed ε the classical cost is C(ε)·n², linear in the n² couplings, so no polynomial-in-n quantum speedup is possible. Only the ε-dependence is open.
- **A poly-time "2D LVV" algorithm built on the area law or PEPS (265).** The theorem's class contains classical, frustration-free, gap-1, unique-ground-state planar instances. Finding their ground states solves Unique-SAT, so it is NP-hard under randomized reductions (Abrahamsen 2020). Neither classical nor quantum computers can do this unless NP ⊆ RP or NP ⊆ BQP. The area law changes representability, not computability.
- **Claiming PEPS bond-dimension guidance from 265.** The exponent c is unspecified and plausibly huge (internal L^{−60} errors), so practitioners' D ≈ 4–20 choices get no guidance.
- **Using 274 as a compiler depth bound at n ≈ 100.** The result is asymptotic with no n₀.
- **279 for resource estimates.** Exact factoring has larger polynomials than Gidney-style circuits, and hardware noise dominates any gain from exactness.
- **283 for unitary compilers** (Qiskit, tket, BQSKit). The oracle is the entire difficulty, and error 1/2 is useless.
- **284 as roadmap evidence for superquadratic speedups.** The functions are artificial pointer and cheat-sheet constructions, and R = O(Q⁴) was already known. Nothing in Babbush et al.'s analysis changes.
- **076 for QAOA-on-LABS.** Time-to-exact-optimum benchmarks at N ≤ 40–66 are untouched. The only fix is to stop calling the asymptotic merit factor "approximately constant" in motivating text.
- **Claiming GBS random-matrix supremacy is weakened (113).** It is not, because those experiments use complex matrices.

---

## Experiment results

All files are in `/home/claude/work/repos/scratch_qadvantage/`.

**1. Explicit FPRAS cost (`fpras_cost.py`, `fpras_cost.out`).**
- **Method.** Transcribe the paper's parameters (`eq:schedule`, `eq:ladder-parameters`, `eq:energy-constants`, `eq:ladder-steps`, `eq:statistical-parameters`) with ε = 0.1 and δ = 0.01. Count only Markov-chain steps, as (K+1) × S × s(ξ) × ⌈log₂(1/δ)⌉, which is a lower bound on the work.

| n | log10(FPRAS steps) | log10(exact n³·2^{n/2}) |
|---|---|---|
| 10 | 13,155 | 4.5 |
| 144 | 20,792 | 28.1 |
| 1,000 | 26,388 | 159.5 |
| 10⁶ | 46,114 | 150,533 |

- **Crossover.** n ≈ 282,382 vertices, where both cost about 10^42,519.
- **Effective polynomial degree.** About 6,550.

**2. GBS ladder identity (`gbs_ladder_identity.py`, `.out`).**
- **Method.** Exact rational arithmetic on 12 random graphs (n = 6–10, edge densities 0.3–0.8, random rational x and r_v).
- **Result.** Σ_S x^{|S|}·Π_{v∉S} r_v·Haf(A_S)² = Haf(ladder) held in all 12 cases. This is the identity behind qadvantage-4.

**3. QAOA-SK depth vs simulated annealing (`sk_sa.c`, `qaoa_sk_fit.py`, `*.out`).**
- **QAOA fit.** QOKit's infinite-size energies for p ≥ 10 fit P* − v_p ≈ 0.928·p^{−0.842}, consistent with Boulebnane et al.'s ε ∝ p^{−0.88}. The stored values are 0.6408 at p = 11 and 0.7397 at p = 80.
- **SA results.** Single-core C simulated annealing plus greedy descent, normalized as in the paper. Mean energy per spin:

| n | Sweeps | Energy per spin | Fraction of P* | Time |
|---|---|---|---|---|
| 1000 | 10³ | 0.7489 | 98.1% | 0.29 s |
| 1000 | 10⁴ | 0.7539 | 98.8% | 3.0 s |
| 2000 | 10³ | 0.7496 | 98.2% | 1.7 s |
| 2000 | 10⁴ | 0.7578 | 99.3% | 20 s |

- **Equivalent QAOA depth** to match these energies: p ≈ 142, 238, 151 and 455 respectively. That is 0.7–9×10⁸ ZZ gates per shot, noiseless.
- **Caveats.**
  - SA has no guarantee. Finite-n optima lie below P*, so the SA fractions are conservative.
  - The QAOA values are n→∞ limits, extrapolated beyond p = 80.
  - A further batch at n = 4000 with 10⁴ sweeps was **stopped by the background time limit** and is not reported.

**Not run.** IAMP (EAMS) itself. It needs a numerical Parisi γ solver, and porting one exceeds the 30-minute budget. That is qadvantage-5's first step.

**Note on sources.** The web-search budget was exhausted near the end. Claims about specific coherent-Ising-machine and D-Wave Max-Cut comparisons are therefore not made here, and the Sels–Morone result is cited from its abstract and a news summary.

---

## Sources

- **Drop manuscripts and Lean:** github.com/openai/math @ fd4aeeb (permalinks inline).
- **Max-Cut, UGC and Quantum Max-Cut:**
  - Tate et al. [arXiv:2112.11354](https://arxiv.org/abs/2112.11354)
  - Wurtz & Lykov [arXiv:2107.00677](https://arxiv.org/abs/2107.00677)
  - Barak & Marwaha [arXiv:2106.05900](https://www.arxiv.org/abs/2106.05900)
  - Marwaha [arXiv:2101.05513](https://arxiv.org/abs/2101.05513)
  - HNPTW [arXiv:2111.01254](https://arxiv.org/abs/2111.01254v2)
  - [arXiv:2306.03912](https://export.arxiv.org/abs/2306.03912v2)
  - Crosta et al. [arXiv:2606.27224](https://arxiv.org/abs/2606.27224)
  - Munoz-Bauza & Lidar [arXiv:2401.07184](https://arxiv.org/html/2401.07184v1)
  - Halperin–Livnat–Zwick "MAX CUT in cubic graphs" ([TAU record](https://cris.tau.ac.il/en/publications/max-cut-in-cubic-graphs-2/))
- **GBS:**
  - Hamilton et al. [arXiv:1612.01199](https://arxiv.org/pdf/1612.01199)
  - Brádler et al. [arXiv:1712.06729](https://arxiv.org/abs/1712.06729v1)
  - Arrazola & Bromley [arXiv:1803.10730](https://arxiv.org/abs/1803.10730)
  - Schuld et al. [arXiv:1905.12646](https://arxiv.org/abs/1905.12646)
  - Oh–Fefferman–Jiang–Quesada [arXiv:2302.00536](https://arxiv.org/abs/2302.00536)
  - Solomons et al. [arXiv:2301.13217](https://arxiv.org/abs/2301.13217)
  - Zhang et al. [arXiv:2505.02445](https://arxiv.org/abs/2505.02445)
  - Deng et al. [arXiv:2302.00936](https://arxiv.org/abs/2302.00936)
  - Uvarov & Vinichenko [arXiv:2312.10143](https://arxiv.org/abs/2312.10143)
- **SK and QAOA:**
  - FGGZ [arXiv:1910.08187](https://arxiv.org/abs/1910.08187)
  - Basso et al. [arXiv:2110.14206](https://arxiv.org/abs/2110.14206)
  - Montanari [arXiv:1812.10897](https://arxiv.org/abs/1812.10897)
  - EAMS [arXiv:2001.00904](https://arxiv.org/abs/2001.00904)
  - EAMS local MaxCut [arXiv:2111.06813](https://arxiv.org/abs/2111.06813)
  - Chen [arXiv:2607.18032](https://arxiv.org/abs/2607.18032)
  - Lopatto [arXiv:2607.11756](https://arxiv.org/abs/2607.11756)
  - Boulebnane et al. [arXiv:2505.07929](https://arxiv.org/abs/2505.07929) ([ALCF summary](https://www.alcf.anl.gov/science/case-studies/evidence-qaoa-optimizes-sherrington-kirkpatrick-model-efficiently-average-case))
  - Sels & Morone [arXiv:2607.08708](https://arxiv.org/abs/2607.08708) ([summary](https://quantumzeitgeist.com/large-spin-qaoa-balances-flatiron-institute/))
- **Shallow circuits and hardware:**
  - Fenner et al. [arXiv:2504.06433](https://arxiv.org/abs/2504.06433)
  - Levine et al. [arXiv:1908.06101](https://arxiv.org/abs/1908.06101)
  - Evered et al. [arXiv:2304.05420](https://arxiv.org/abs/2304.05420)
  - Bäumer et al. [arXiv:2308.13065](https://arxiv.org/abs/2308.13065)
  - Maslov & Nam [arXiv:1707.06356](https://arxiv.org/abs/1707.06356)
- **2D ground states:**
  - Abrahamsen [arXiv:2004.02850](https://arxiv.org/abs/2004.02850)
  - Anshu–Arad–Gosset [arXiv:2103.02492](https://arxiv.org/abs/2103.02492v2)
  - LVV [arXiv:1307.5143](https://ar5iv.arxiv.org/html/1307.5143)
- **Chemistry:**
  - O'Gorman et al. [arXiv:2103.08215](https://arxiv.org/abs/2103.08215)
  - Lee et al. Nat. Commun. 2023 ([record](https://ideas.repec.org/a/nat/natcom/v14y2023i1d10.1038_s41467-023-37587-6.html))
  - Gharibian–Le Gall [arXiv:2111.09079](https://arxiv.org/abs/2111.09079v2)
- **Roadmaps:**
  - Gidney [arXiv:2505.15917](https://arxiv.org/abs/2505.15917v1)
  - Babbush et al. [arXiv:2011.04149](https://arxiv.org/abs/2011.04149)
  - Shaydulin et al. [arXiv:2308.02342](https://arxiv.org/abs/2308.02342v2)
- **Code (pinned):**
  - qiskit-optimization @65ce191
  - thewalrus @54b1062
  - strawberryfields @162125d
  - QOKit @a00cc72
