# Sequence design: Barker / circulant Hadamard (179) and unbounded binary merit factor (076)

**Bottom line.** Both results are real and Lean-checked at the headline level. Neither changes what an engineer builds. Family 179 settles the circulant Hadamard conjecture (orders 1 and 4 only), and with the classical odd-length theorem this gives binary Barker lengths of exactly {2,3,4,5,7,11,13}. The right action is CERTIFY: Wikipedia, OEIS A091704, MathWorld, MATLAB docs and formal-conjectures still say "conjectured", "open" or "maximum known". A Mathlib/Archive upstream is a worthwhile medium-effort FORMALIZE project. Family 076 disproves Turyn's bounded-merit-factor conjecture, so Golay's 12.32 is no longer a defensible "asymptotic limit". The only action is a wording REDIRECT in LABS and quantum-benchmark papers that still quote it. The construction gives no N0 and no algorithm, and the explicit constants (rounding constant 196608 in Lean) are galactic. Our seeding experiment (N = 101 to 4099) confirms that a finite analogue of the pipeline loses clearly to classical Legendre seeds for N ≥ 257, so do not pursue it as a code generator. Binary-OFDM PMEPR is not a real channel.

## What the papers actually prove

### Family 179: "The circulant Hadamard conjecture" (Sept 23, 2026; unchanged by the Oct 7 repair)
- **Thm `thm:main`** (introduction.tex L21-24): a real ±1 circulant Hadamard matrix of order n exists **iff n ∈ {1,4}**. Witness for 4: first row `+++-`.
- **Cor `cor:barker`** (introduction.tex L43-50; proof in contradiction.tex L196-240): for n > 1, a binary Barker sequence (|C_a(t)| ≤ 1 for all t ≥ 1) exists **iff n ∈ {2,3,4,5,7,11,13}**.
  - The *even* case is new. For even n > 2, Barker forces n ≡ 0 mod 4 and all periodic autocorrelations to be 0, so the sequence is a circulant Hadamard row and n = 4 (the Turyn-Storer 1961 implication).
  - The *odd* case is **classical and not new**: Turyn-Storer 1961, with a cleaner proof in Schmidt-Willms 2016 (Des. Codes Cryptogr.; [arXiv 1501.06035](https://arxiv.org/abs/1501.06035)), an elementary run-structure/parity argument of a few pages.
- Method: the classical reduction to n = 4u², u odd (Turyn), then a new alternating product of character values Δ(x) over the prime divisors of u. Δ is shown to be an algebraic integer of absolute value 1 under all embeddings, so a root of unity by Kronecker, and of odd order. A 2-adic "binary coefficient identity" then yields a contradiction. There are no constants or regimes; this is an exact classification.
- **Triage check:** correct. One nuance: the triage text "Logan-Mossinghoff excluded every length 13<n≤4e33 except one" conflates two results. That exclusion is Borwein-Mossinghoff 2014 for *Barker* lengths ([arXiv 1306.0045](https://arxiv.org/abs/1306.0045): only n = 3979201339721749133016171583224100 survived below ~4·10³³). Logan-Mossinghoff 2017 left 4,489 candidate *circulant Hadamard orders* ≤ 4·10³⁰ (introduction.tex L98-103).

**Lean status (verified by reading the files, repo @ `fd4aeeb`).**
- `OAI.CirculantHadamard.exists_iff_order_one_or_four` ([Main.lean L19-34](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/LinearAlgebra/CirculantHadamard/Main.lean#L19-L34)) is checked against the comparator statement [ComparatorChallenges/CirculantHadamard.lean L24-26](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/CirculantHadamard.lean#L24-L26). Permitted axioms are `propext`, `Quot.sound` and `Classical.choice`.
- The statement is the honest one: real n×n matrix, entries ±1, H·Hᵀ = n·I, literally circulant.
- `OAI.CirculantHadamard.Barker.even_length_eq_two_or_four` ([Barker/Main.lean L63-73](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/LinearAlgebra/Barker/Main.lean#L63-L73)), with comparator EvenBarker.json.
- **The odd-length Barker classification is NOT in Lean** (lean/docs/179.md says so explicitly). The full Corollary `cor:barker` is therefore Lean-checked only for even n; the odd part rests on peer-reviewed classical work.
- I grepped all 68 + 5 files for `sorry`, `axiom`, `admit`, `native_decide`, `implemented_by`, `extern` and `set_option maxHeartbeats`. There are **no hits**.
- I did not re-run the build or the comparator. Lake cache hosts are blocked by the egress proxy, so a from-source Mathlib build was not attempted on 2 cores.

**Upstreamability.**
- Size: ~9,500 lines in 68 files for the circulant theorem plus 277 lines in 5 files for Barker.
- Dependencies: Mathlib only (pinned `d13f23b`, Lean v4.34.1). No other OAI library and none of the lakefile's third-party packages are imported; only one file imports all of `Mathlib`.
- Mathlib (`d6416ab`, 2026-10-11) already has much of what is needed:
  - `Matrix.circulant` ([Circulant.lean L48-52](https://github.com/leanprover-community/mathlib4/blob/d6416ab0f09d3a2e090f403fc80f37754f6181a9/Mathlib/LinearAlgebra/Matrix/Circulant.lean#L48-L52)).
  - A 2026 `Matrix.IsHadamard` with `four_dvd_card` ([HadamardMatrix.lean L51-54](https://github.com/leanprover-community/mathlib4/blob/d6416ab0f09d3a2e090f403fc80f37754f6181a9/Mathlib/LinearAlgebra/Matrix/HadamardMatrix.lean#L51-L54)).
  - Kronecker's theorem `NumberField.Embeddings.pow_eq_one_of_norm_eq_one` ([Embeddings.lean L137-140](https://github.com/leanprover-community/mathlib4/blob/d6416ab0f09d3a2e090f403fc80f37754f6181a9/Mathlib/NumberTheory/NumberField/InfinitePlace/Embeddings.lean#L137-L140)), which the OAI wrapper already calls ([Kronecker.lean L19-44](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/LinearAlgebra/CirculantHadamard/Kronecker.lean#L19-L44)).
- The bulk is custom group-ring (`AddMonoidAlgebra R (ZMod n)` with a star), cyclotomic localization and DVR plumbing.
- Verdict: upstreamable, but as a multi-PR project. Restate against `Matrix.IsHadamard` and `Matrix.circulant`, land the theorem in `Archive/` (precedent: `Archive/Sensitivity.lean`), and split the reusable algebra into separate PRs. This is weeks of work, not days.

### Family 076: real ultraflat Littlewood polynomials (three manuscripts)
- **Sept 23 paper, Thm `thm:main`** (introduction.tex L22-33): m_N := min over ±1 words of ‖P‖_∞/√N → 1 through *all* N. Lean: `OAI.AsymptoticallyMinimalLittlewood.main` ([Main.lean L187-232](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/Littlewood/Main.lean#L187-L192)), 27 files, ~9.6k lines, 0 sorry, comparator `AsymptoticallyMinimalLittlewood.json`.
- **Cor `cor:merit`** (merit-morse.tex L22-36): max_A F(A) → ∞ through all N, from F(A_N) ≥ 1/(m_N² − 1). This disproves Turyn's (= Erdős's L⁴) bounded-merit-factor conjecture. The corollary is a two-line consequence of the Lean-checked theorem; it is not itself a comparator statement.
- **Oct 5 papers.** "Ultraflat real Littlewood polynomials" Thm 1.1 gives the two-sided bound (1−ε)√N ≤ |P| ≤ (1+ε)√N; it is *not* Lean-formalized. "Nearly minimal maxima ..." gives √N/16 ≤ |P| ≤ (1+η)√N.
- **Constructive? Existential only.** The paper says no useful convergence rate or efficient signing algorithm is asserted ([introduction.tex L34-39](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotically-minimal-maxima-of-real-Littlewood-polynomials-September-23-2026/build/introduction.tex#L34-L39)). The Lean doc repeats this.

**The pipeline, step by step, and what is implementable at finite N:**

1. **Auxiliary torus polynomial** (spreading.tex Prop `prop:auxiliary`, recursion L127-135). p_j = p_{j−1} + (1−p_{j−1}²)/2 · cos(2πy_j). The guaranteed energy gain is M_j ≥ M_{j−1} + (1−M_{j−1})²/8, so 1 − M_d ≲ 8/d.
   - Monte Carlo: M_20 = 0.86, M_50 = 0.990, M_100 = 0.9998. In practice d ~ 50-100 suffices for δ ~ 10⁻²-10⁻⁴.
   - The exact Fourier support grows doubly exponentially: |supp p_j| = 2, 8, 54, 700, 17358 for j = 1..5. The box bound at d = 20 is 10⁶⁴.
   - Each support vector is then spread by quadratic oscillations into a box of B^D frequencies, with D = |supp|/2.
   - **Not instantiable** beyond d ≈ 4.
2. **Signed interval packing** (packing.tex Lemma `lem:signed-packing`): a prime q → ∞, a random slot hypergraph, and a Pippenger-Spencer near-perfect matching giving H ≈ q/(2L) blocks. This is randomized-algorithmic in principle, but q and H are astronomically large for the support above.
3. **Sampling** (sampling.tex eq. `sampling-coefficients`, [L152-157](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotically-minimal-maxima-of-real-Littlewood-polynomials-September-23-2026/build/sampling.tex#L152-L157)): X_{N,k} = Σ_h χ_h(k/N) F(kθ_h + (N/2)v(k/N − x_h*)²). These are real values in [−1,1] built from chirp-sampled torus coordinates. **This step is directly implementable at any N** once F, θ_h and v are fixed.
4. **Defect-sensitive rounding** (Lemma `lem:rounding`; rounding.tex): dyadic Lovett-Meka partial colouring on a 40N-row Fourier grid. The error is ≤ C(1 + √(μ log(80N/μ))). **Implementable** (Lovett-Meka and Gram-Schmidt walk are polynomial-time), but the constant is enormous: Lean proves C = **196608** ([Rounding.lean `defect_rounding` L1225-1230](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/Littlewood/Rounding.lean#L1225-L1230)). My own tally of the TeX constants gives C ≈ 400. Either way the guarantee is vacuous at any feasible N.
5. **Quantitative consequence of the constants** (my computation, `constants.py`). The final bound is limsup m_N ≤ K_δ + 2C√(δ log(20/δ)). To certify F > 6.34 one needs m_N < 1.076, which requires δ < 3.6·10⁻¹⁰ with C = 404, or **δ < 1·10⁻¹⁵ with the Lean constant**. Beating 12.32 needs δ < 3·10⁻¹⁶. With 1 − M_d ~ 8/d, that means d ~ 10¹⁶ torus variables. **Galactic.**

**Triage check:** correct. "Galactic", T2, REDIRECT is right. The triage's suggested 2-3-day BENCHMARK was run here and came out negative (below).

## Current practice and state of the art

**Barker / pulse compression.**
- Practice stopped at Barker-13 decades ago. IEEE 802.11b DSSS uses the 11-chip Barker code at 1-2 Mb/s and CCK above ([Wikipedia 802.11b](https://en.wikipedia.org/wiki/IEEE_802.11b-1999)). MATLAB's `comm.BarkerCode` and `phased.PhaseCodedWaveform` only accept lengths 2-13 ([MathWorks](https://www.mathworks.com/help/comm/ref/comm.barkercode-system-object.html)).
- Longer codes are minimum-PSL binary codes, nested Barker, mismatched filters (e.g. Levanon-Scharf 2009 on Barker-13 and MPSL-51), or polyphase codes.
- The classification changes none of this. It only removes a hypothetical.

**Where 179 is still listed as open (Oct 2026):**
- **Wikipedia "Barker code":** "It is conjectured that no longer sequence exists"; the even case is described as unresolved ([link](https://en.wikipedia.org/wiki/Barker_code)).
- **Wikipedia "Hadamard matrix":** the circulant Hadamard conjecture is presented as open ("verified for all but 26 values of u < 10⁴") ([link](https://en.wikipedia.org/wiki/Hadamard_matrix)).
- **OEIS A091704** (Barker counts): "It is conjectured that there are no Barker codes of length > 13", plus the Borwein-Mossinghoff exceptional-length comment ([link](https://oeis.org/A091704)).
- **MathWorld "Barker Code":** "it is conjectured that no longer Barker codes exist" ([link](https://mathworld.wolfram.com/BarkerCode.html)).
- **MATLAB doc:** "The maximum known Barker code length is 13." This is technically true but should say "maximum possible".
- **google-deepmind/formal-conjectures @ `cd69121`:**
  - `barker_conjecture` is still tagged `research open` ([BarkerSequence.lean L48-51](https://github.com/google-deepmind/formal-conjectures/blob/cd6912171c5a1de06905795e5533ec7120f34ddc/FormalConjectures/Arxiv/2104.00502/BarkerSequence.lean#L48-L51)).
  - `circulant_hadamard_conjecture` is **already** tagged `research solved` with a link to the OAI Lean proof ([CirculantHadamard.lean L55-66](https://github.com/google-deepmind/formal-conjectures/blob/cd6912171c5a1de06905795e5533ec7120f34ddc/FormalConjectures/Arxiv/2402.13202/CirculantHadamard.lean#L55-L66)). The two entries are inconsistent.
- **Radar textbooks** (Levanon-Mozeson, Richards, Skolnik) typically say only that "13 is the longest known Barker code" (Jedwab's 2008 survey: the conjecture "remains unproven"). I could not access textbook full text. Any change happens at the next edition and should say "longest possible (odd: Turyn-Storer 1961; even: circulant Hadamard theorem, 2026)".

**LABS / merit factor records (finite N).**
- Exact optima are known for N ≤ 66 (Packebusch-Mertens 2016, [arXiv 1512.02475](https://arxiv.org/abs/1512.02475); OEIS [A102780](https://oeis.org/A102780)), and skew-symmetric optima for N ≤ 119.
- Best known values:
  - F ≈ 9.5 for N ≤ 225 (git_labs skew table; best for N > 200 is 9.54 at N = 213).
  - 7-8 for N = 227-401.
  - 6.52 at N = 449 in the 2018 table.
  - Up to **7.78 at N = 455** and new records for all N = 450-527 (Pšeničnik et al., [arXiv 2409.07222](https://arxiv.org/abs/2409.07222)).
  - "F = 6.367 at N = 1010" is quoted by Zhang et al. 2025 as the largest reported experiment.
- The best proven asymptotic families give 6.342 (Jedwab-Katz-Schmidt rotated/appended Legendre).
- The classical solvers (Gallardo-Cotta-Fernández MA/TS, `lssOrel`) all start from **uniform random** sequences: [LABS.c L40-44](https://github.com/borkob/git_labs/blob/1aa123407636e48630174e0bf122037e369c1d68/solvers/lMAts-lRRts/src/LABS.c#L40-L44), [GA.c L161-173](https://github.com/borkob/git_labs/blob/1aa123407636e48630174e0bf122037e369c1d68/solvers/lMAts-lRRts/src/GA.c#L161-L173), [sequence.cpp L83-89](https://github.com/borkob/git_labs/blob/1aa123407636e48630174e0bf122037e369c1d68/solvers/lssOrel/src/sequence.cpp#L83-L89).

**Who still quotes a finite asymptotic optimum (Q3). Exact text to change:**

| Source | What it says now | Change to |
|---|---|---|
| Shaydulin et al., *Sci. Adv.* 2024 ([arXiv 2308.02342v2](https://arxiv.org/abs/2308.02342)), main text "Problem statement" | the best-known merit factor drops for large N, "whereas the asymptotic limit predicts that the merit factor should stay approximately constant" (no number, no citation) | "...whereas the optimal merit factor is now known to grow without bound as N→∞ (OpenAI 2026, Lean-checked; no effective rate), so the decline reflects heuristic failure." |
| Same, Supplementary S1 | "The conjectured asymptotic limit of F → 12.32 as N → ∞ was derived using arguments from statistical mechanics (Golay 1982)"; also "explicit sequences asymptotically achieving F ≈ 6.34 are known" | Keep 6.34. Replace 12.32 with "Golay's 12.32 is a heuristic (ergodicity-postulate) estimate for long sequences; the optimal merit factor is unbounded (Turyn's conjecture is false), with no known rate." |
| Zhang, Shen, Kumar, Pistoia (JPMorgan), [arXiv 2504.00987](https://arxiv.org/abs/2504.00987), Sec. II.A + footnote | no known method can reach "the asymptotic merit factor of F_N ≈ 12.3248 as N→∞ ... as proposed by Golay"; N = 1010 at 6.367 is "a significant departure from Golay's postulate" | Drop "the asymptotic merit factor"; call 12.3248 Golay's heuristic estimate, and note that the true optimum diverges. |
| Sciorilli et al. 2025, [arXiv 2506.17391](https://arxiv.org/abs/2506.17391) | asymptotics of the optimal merit factor "remains an open question"; Golay's "asymptotic upper bound F_N ≲ 12.3248/(8πN)^{3/(2N)}" | It is no longer open in the bounded/unbounded sense, and the "upper bound" is false asymptotically. |
| Packebusch-Mertens 2016, Sec. 2 | "The common belief is that ... F_N is bounded by some constant"; "an open problem to prove (or disprove) that F_N is bounded" | Disproved (Turyn's conjecture false). Mertens' 1996 extrapolation "F > 9" ([cond-mat/9605050](https://arxiv.org/abs/cond-mat/9605050)) is still consistent. |
| Bošković-Brglez-Brest 2014/2017 ([arXiv 1406.5301](https://arxiv.org/abs/1406.5301)) | "conjectured asymptotic value of F = 12.3248" | Same correction. |
| Wikipedia "Littlewood polynomial" | ultraflat ±1 sequences listed as "a central open question"; "determining the optimal asymptotic merit factor" listed as a major open problem | Unboundedness and ultraflatness resolved (preprint + Lean); the *rate* and constructive versions remain open. |
| erdosproblems.com #1150 (last edited Jan 2026) | "open" | Disproved. formal-conjectures already tags `erdos_1150` as solved with a Lean link. |
| AlphaEvolve problem 28 "Golay's Merit Factor" ([problems/28.html L214-232](https://github.com/google-deepmind/alphaevolve_repository_of_problems/blob/8f447457957deac61e28bf1676746f0753b3b2f8/problems/28.html#L214-L232)) | asks for the asymptotic behaviour of C⁺(n) and C⁴(n) | C⁺(n)→1 and max merit → ∞ are now known; the open part is the rate. |

- The newer quantum papers (Kipu/NVIDIA QE-MTS, [arXiv 2511.04553](https://arxiv.org/abs/2511.04553); Quantinuum/JPMC 2026, [arXiv 2603.04584](https://arxiv.org/abs/2603.04584)) **do not quote** an asymptotic merit factor. Nothing needs to change there.
- None of the quantum *claims* (time-to-solution scaling at N ≤ 40-50) depend on the asymptotic constant.

**Binary OFDM PMEPR (Q4).**
- For one BPSK-OFDM symbol on N subcarriers, PMEPR = max_t |P(e(t))|²/N, so ultraflat Littlewood would mean PMEPR → 1. My check (`pmepr.py`, ×16 oversampling):

| Family | N | PMEPR |
|---|---|---|
| Rudin-Shapiro / Golay | 256, 1024, 4096 | 2.00 |
| Best rotated Legendre | 256-4096 | 2.4-2.7 |
| Random words (median) | 256 | 6.5 |
| Random words (median) | 4096 | 9.3 |

- Real channels carry data. Schmidt's covering-radius lower bound ([cs/0611161](https://arxiv.org/abs/cs/0611161)) and the Davis-Jedwab Golay/Reed-Muller coset framework ([1999](https://scholarship.richmond.edu/mathcs-faculty-publications/137)) govern the rate/PMEPR trade-off.
- 5G NR does PAPR control via π/2-BPSK with DFT-s-OFDM and FDSS, plus Zadoff-Chu reference signals ([arXiv 1907.05692](https://arxiv.org/abs/1907.05692), [arXiv 2509.19064](https://arxiv.org/abs/2509.19064)).
- A single fixed binary word with PMEPR near 1 would serve at most as a preamble or pilot, a role CAZAC/Zadoff-Chu sequences already fill (constant envelope). 076 gives no way to compute one. **Not a real channel.**

## Opportunities

### seqdesign-1: CERTIFY the Barker/circulant classification in reference works (pursue now)
- **Change:** Update Wikipedia "Barker code" (Conjecture section) and "Hadamard matrix" (circulant section), OEIS A091704 (comment, and keyword `fini`/`full` status), and MathWorld. Ask MathWorks to change "maximum known" to "maximum possible" in the `comm.BarkerCode` and `phased.PhaseCodedWaveform` docs.
- **Citation package:** OAI preprint, the Lean theorem permalink above, the comparator file, and Schmidt-Willms 2016 for the odd case.
- **Benefit:** guarantee for students and engineers; ends residual searches. Impact is low but nearly free.
- **Measure:** pages updated; edits survive review.
- **Risks:** Wikipedia's reliable-source rules may require peer review. Five earlier complete proofs have been claimed (Oh-Hashi 2016, Orozco-López 2019, Morris 2023, Gallardo 2024, Manjhi-Kumar 2025; introduction.tex L115-116) without acceptance. The Lean check, against a comparator statement I read and found faithful, is the strongest argument.
- **First step:** Wikipedia talk-page post with the Lean link, plus an OEIS edit.

### seqdesign-7: REDIRECT computational searches and fix formal-conjectures (pursue now)
- **Change:** Re-tag `barker_conjecture` in formal-conjectures as solved. It is inconsistent with the already-solved `circulant_hadamard_conjecture` in the same repo.
- A fully formal proof additionally needs the odd case. Schmidt-Willms is short and elementary, a good Lean target of days to weeks.
- Wieferich-pair and field-descent searches for circulant Hadamard orders or even Barker lengths (Logan-Mossinghoff style) can stop.

### seqdesign-2: FORMALIZE: upstream 179 to Mathlib / Archive (pursue as research)
- **Change:** Restate the theorem using Mathlib's `Matrix.IsHadamard` and `Matrix.circulant`, put the main theorem in `Archive/`, and upstream the reusable algebra separately: cyclic group-ring star, local DVR lemmas at primes over 2 and p in cyclotomic adjoins, alternating character products.
- **Size:** ~9.8k lines total.
- **Benefit:** formalization. formal-conjectures can point to Mathlib instead of a third-party repo, and the algebra is reusable for difference-set results.
- **Measure:** PR(s) merged.
- **Risks:** review burden of AI-generated, non-idiomatic Lean; version drift from `d13f23b`.
- **First step:** Port Barker/Main.lean plus the matrix bridge, with the main theorem as an Archive entry referencing the OAI development.

### seqdesign-3: REDIRECT "Golay 12.32 / bounded merit factor" wording (pursue now)
- **Change:** the text edits in the table above, sent as errata or email to the authors of the Shaydulin et al. and Zhang et al. JPMorgan papers, plus edits to Wikipedia "Littlewood polynomial" and erdosproblems #1150.
- **Benefit:** correct framing in benchmark literature. Impact is small; it removes a false "ceiling" narrative.
- **Measure:** revised versions; new LABS papers stop citing 12.32 as the limit.
- **Risk:** overcorrection into "high merit factors are reachable". The note must say: *unbounded, but no rate, no algorithm, and nothing changes at N ≤ 10⁴*.

## What is NOT an opportunity here

- **seqdesign-4, 076 pipeline as a LABS seed generator: do not pursue.**
  - The proof's auxiliary polynomial cannot be instantiated: d ~ 8/δ variables, doubly exponential support, then B^D spreading.
  - A faithful finite analogue (chirp waveform plus sign or greedy rounding) gives seeds at F ≈ 3.5-4.2. After tabu search it ends at ≈ 4.5-5.9, below Legendre seeds (6.3-6.4) at every N ≥ 257 (results below).
  - The rounding constant 196608 makes the guarantee vacuous at any N.
- **seqdesign-5, better binary radar/CDMA codes or quantum-advantage implications: do not pursue.** The result is existential with no N0; at practical N (≤ 10⁴) the bar is set by search, and quantum LABS work lives at N ≤ ~50 where exact optima are known.
- **seqdesign-6, binary OFDM PMEPR → 1: do not pursue** (see Q4 above).
- **179 for radar design: no change.** Barker-13 was already the ceiling in every design flow. The classification does not create codes, and minimum-PSL or mismatched-filter design is unaffected.
- **No link between 076 and 179 in practice.** The "approximately Hadamard circulant" line (Steinerberger) is what flat Littlewood polynomials give. 179 says exact circulant Hadamard rows do not exist beyond n = 4. Both are now settled and neither yields a design tool.

## Experiment results

All code and logs are in `/home/claude/work/repos/scratch_seqdesign/` (`tabu.c`, `seeds.py`, `run_exp.sh`, `summarize.py`, `results_table.md`, `results_raw.log`, `constants.py`, `aux_recursion.py`, `probe*.py`, `pmepr.py`).

**Setup**
- **Local search:** restarted tabu search, a faithful re-implementation of the Gallardo-Cotta-Fernández TS component used inside MA/TS: random walk length in [N/2, 3N/2], tabu tenure maxIter/10 + U[0, maxIter/50], aspiration, O(N) incremental flip evaluation.
- **Restarts:** cycle through each family's seed list.
- **Budget:** fixed per N in TS flip-steps (each step scans all N flips). Budgets were 400k, 200k, 100k, 30k, 8k and 4k steps for N = 101, 257, 509, 1021, 2053 and 4099.
- **Runs:** 3 independent runs per (N, family), on 2 CPU cores.

**Seed families**
- (a) **pipeline:** a relaxed waveform from sampling.tex with F = cos(2πy) (a single ±mode, an exact signed packing: H ∈ {1,2,3,4,6,8} blocks whose chirp sweeps tile [0,1/2] and its reflection), v ∈ [0.44, 0.5], random phase. It is then rounded by a greedy coordinate-wise L⁴-minimizing rounding, a cheap stand-in for discrepancy rounding. The best K = budget/N + 2 of 3K candidates are kept.
- (a′) **pipe_sign:** the same waveform, with the sign of X_k used directly (hard-limited chirp).
- (b) **random:** uniform ±1.
- (c) **legendre:** Legendre sequences for the 6 primes nearest N/1.058, all rotations, periodically appended to length N; the best K are kept (the Jedwab-Katz-Schmidt family).

**Best merit factor after search, range over 3 runs (best seed F in parentheses):**

| N | random | Legendre rot.+app. | pipeline (greedy-L4) | pipeline (sign) |
|---|---|---|---|---|
| 101 | 5.63-5.84 (2.24) | 5.84-6.03 (5.46) | **6.17-6.24** (4.97) | 5.97-6.17 (4.13) |
| 257 | 5.00-5.13 (1.53) | **6.27** (6.27) | 5.48-5.88 (4.68) | 5.44-5.67 (3.85) |
| 509 | 4.73-4.82 (1.36) | **6.38** (6.38) | 5.05-5.36 (4.27) | 5.16-5.41 (3.54) |
| 1021 | 4.61-4.73 (1.18) | **6.33** (6.33) | 4.97-5.10 (4.03) | 4.95-5.17 (3.08) |
| 2053 | 4.49-4.53 (1.06) | **6.35** (6.34) | 4.55-4.81 (3.50) | 4.71-4.76 (2.51) |
| 4099 | 4.39-4.50 (1.05) | **6.34** (6.34) | 4.52-4.74 (3.56) | 4.67-4.93 (2.58) |

**Reference values (not comparable budgets):**
- Best known (skew-restricted, git_labs 2018 table): 8.82 at N = 101 and 7.38 at N = 257. Exact optimum at N = 101 is unknown; skew-optimal is 8.82.
- N ≈ 509: 2024 records in the 6.5-7.8 range ([arXiv 2409.07222](https://arxiv.org/abs/2409.07222)).
- N = 1010: 6.367.

**Reading**
- The pipeline-style seed is a better *starting point* than random everywhere: seed F of 3.5-5 versus about 1, and after search +0.1 to +0.6 over random.
- At N = 101 it slightly beat Legendre seeds under this budget, but the margin is small, there are only 3 runs, and both are about 2.6 below the known best of 8.82. **Do not read anything into it.**
- At **every N ≥ 257 it loses clearly to Legendre seeding** (by 0.5-1.8).
- At N ≥ 1021 the TS budget is too small to move Legendre seeds much: the final F is essentially the seed's 6.33-6.35, while random and pipeline seeds end around 4.5-5.
- Diagnostics:
  - The relaxed chirp has energy/N ≈ 0.50 and defect μ/N ≈ 0.18. The paper needs both to be o(1), which requires the full multi-variable auxiliary polynomial.
  - The relaxed maximum is ≈ 0.94-1.0 √N, or about 1.33 times √(energy·N).
  - After rounding, the sign word's maximum is ≈ 1.8-1.9 √N.
  - Independent randomized rounding (E[ε_k] = X_k) is much worse: F ≈ 1.3.
  - Saturating the waveform (tanh) raises energy to 0.9 but does not improve post-rounding F beyond ≈ 4.0-4.3.
- **Caveats:**
  - These are small runs on 2 cores; the budgets were cut once (first schedule took about 7 min per run at N = 4099).
  - Our TS is not the full memetic MA/TS.
  - Our "pipeline" is a single-mode simplification with greedy rounding, not Lovett-Meka.
  - The negative result is about this finite analogue. Together with the constants analysis it is enough for a "do not pursue" decision, but it is not a proof that no relax-and-round seed could ever help.

**Constants calculation (`constants.py`):**
- To certify F > 6.34 (m_N < 1.076) from the paper's bound needs δ < 3.6·10⁻¹⁰ with C ≈ 404 (my tally from TeX), or δ < 1.0·10⁻¹⁵ with Lean's C = 196608.
- At any N, Lean's rounding error bound with μ/N = 0.01 is ≈ 6·10⁴·√N, versus a target error of about 0.07·√N.

## Sources
- OpenAI math repo @ `fd4aeeb` (preprints and Lean cited above); lean/docs/179.md, lean/docs/076.md.
- [Barker code - Wikipedia](https://en.wikipedia.org/wiki/Barker_code); [Hadamard matrix - Wikipedia](https://en.wikipedia.org/wiki/Hadamard_matrix); [Littlewood polynomial - Wikipedia](https://en.wikipedia.org/wiki/Littlewood_polynomial); [IEEE 802.11b - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.11b-1999)
- [OEIS A091704](https://oeis.org/A091704); [OEIS A102780](https://oeis.org/A102780); [MathWorld Barker Code](https://mathworld.wolfram.com/BarkerCode.html); [MATLAB comm.BarkerCode](https://www.mathworks.com/help/comm/ref/comm.barkercode-system-object.html); [MATLAB phased.PhaseCodedWaveform](https://www.mathworks.com/help/phased/ref/phased.phasecodedwaveform-system-object.html)
- Borwein-Mossinghoff, [Wieferich pairs and Barker sequences II, arXiv 1306.0045](https://arxiv.org/abs/1306.0045); Schmidt-Willms, [Barker sequences of odd length, arXiv 1501.06035](https://arxiv.org/abs/1501.06035); Jedwab, [What can be used instead of a Barker sequence? (2008)](https://www.sfu.ca/~jed/Papers/Jedwab.%20Barker%20Sequence%20Alternatives.%202008.pdf)
- [google-deepmind/formal-conjectures @ cd69121](https://github.com/google-deepmind/formal-conjectures/tree/cd6912171c5a1de06905795e5533ec7120f34ddc); [erdosproblems.com/1150](https://www.erdosproblems.com/1150); [erdosproblems.com/230](https://www.erdosproblems.com/230); Erdélyi, [arXiv 2608.00744](https://arxiv.org/abs/2608.00744)
- [mathlib4 @ d6416ab](https://github.com/leanprover-community/mathlib4/tree/d6416ab0f09d3a2e090f403fc80f37754f6181a9) (HadamardMatrix.lean, Circulant.lean, Embeddings.lean)
- Shaydulin et al., [arXiv 2308.02342](https://arxiv.org/abs/2308.02342) (Sci. Adv. 2024); Zhang et al., [arXiv 2504.00987](https://arxiv.org/abs/2504.00987); Sciorilli et al., [arXiv 2506.17391](https://arxiv.org/abs/2506.17391); Gomez Cadavid et al., [arXiv 2511.04553](https://arxiv.org/abs/2511.04553); Perlin et al., [arXiv 2603.04584](https://arxiv.org/abs/2603.04584)
- Packebusch-Mertens, [arXiv 1512.02475](https://arxiv.org/abs/1512.02475); Mertens, [cond-mat/9605050](https://arxiv.org/abs/cond-mat/9605050); Bošković-Brglez-Brest, [arXiv 1406.5301](https://arxiv.org/abs/1406.5301); [borkob/git_labs @ 1aa1234](https://github.com/borkob/git_labs/tree/1aa123407636e48630174e0bf122037e369c1d68); Pšeničnik et al., [arXiv 2409.07222](https://arxiv.org/abs/2409.07222); Dimitrov et al., [arXiv 2011.00068](https://arxiv.org/abs/2011.00068)
- [AlphaEvolve repository of problems @ 8f44745](https://github.com/google-deepmind/alphaevolve_repository_of_problems/tree/8f447457957deac61e28bf1676746f0753b3b2f8) (problem 28, flat_polynomials notebook); Balister et al., [Flat Littlewood polynomials exist, arXiv 1907.09464](https://arxiv.org/abs/1907.09464)
- Levanon-Scharf, [Range sidelobes blanking ... mismatched filters (IET RSN 2009)](https://www.nadavlevanon.sites.tau.ac.il/_files/ugd/dfbcdc_b69b0e6b772649a8ba725061326ccbac.pdf)
- Davis-Jedwab 1999, [Peak-to-mean power control in OFDM ...](https://scholarship.richmond.edu/mathcs-faculty-publications/137); K.-U. Schmidt, [arXiv cs/0611161](https://arxiv.org/abs/cs/0611161); [arXiv 1907.05692](https://arxiv.org/abs/1907.05692); [arXiv 2509.19064](https://arxiv.org/abs/2509.19064)
