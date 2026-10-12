# Thorp shuffle, swap-or-not, and full-domain small-domain encryption (family 238)

**Bottom line.** Family 238 is a real theoretical milestone. It proves that the Thorp shuffle on N = 2^d cards mixes the *entire permutation* in Θ(lg N) shuffles, and the 1600·lg N statement is Lean-checked. It is not actionable for any deployed system. FF1, Ethereum's 90-round swap-or-not, and FPE libraries all stay as they are, and the literal 1600d constants are weak at FPE sizes. The most useful output is a short corollary that the triage only guessed at, which I have now checked with explicit numbers. The paper's eight-block Fourier "lift" is fully generic: its core is a Lean-proved statement about *any* law on S_N. Plugged into Hoang–Morris–Rogaway's swap-or-not bound, it gives the first fixed-round-count proof that plain swap-or-not is secure against all N queries. The cost is about 9k–16k rounds at N = 2^64 for ε = 2^-32 to 2^-64. That is roughly 3× better than mix-and-cut, the previous fixed-time full-security construction, but about 7–11× more than Sometimes-Recurse's *expected* cost. Verdict: **research lead (write the note); no engineering change anywhere.**

## What the papers actually prove

All results are for ideal round functions (independent fair coins) and N = 2^d. One "physical shuffle" is one Thorp round. In cipher terms that is one round of a maximally-unbalanced Feistel network, with one 1-bit random-function call per round, or 1/5 of an AES call using the MRS'09 5×-batching trick (which requires 32 | N).

| Result | Statement (theorem ref) | Notion | Constants | Lean |
|---|---|---|---|---|
| Main: 1600d | `Optimal-order mixing…` Thm `thm:mixing` ([main.tex L53-70](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Optimal-order-mixing-of-the-Thorp-shuffle-September-26-2026/build/main.tex#L53-L70)): ‖q_d^{*1600d} − U_N‖_TV → 0. Lower bound 1 − 2^{tN/2}/N!, so t_mix ≥ 2d − O(1). | TV of the **full permutation law on S_N**, worst start | Explicit in the proof (below), but the theorem is stated as a limit | `OAI.Thorp.main` ([Main.lean L41-53](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/ThorpShuffle/Main.lean#L41-L53)). No `sorry` in `ThorpShuffle/`. The explicit rate `fullRate` is in [EightBlocks.lean L24-26](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/ThorpShuffle/EightBlocks.lean#L24-L26). |
| Step 1: averaged marginals | Prop `prop:averaged-marginal` ([L378-391](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Optimal-order-mixing-of-the-Thorp-shuffle-September-26-2026/build/main.tex#L378-L391)): after 200d shuffles, a *random* list of k ≤ 7N/8 labels has E‖law − U_inj‖ ≤ ε_N = N^{3/2}/2·sqrt((31/32)^{198d} + 32e^{−N/256}) | q-wise (q = 7N/8), averaged over lists | explicit | yes |
| Step 2: eight-block lift | Prop `prop:orbit-lift` ([L486-539](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Optimal-order-mixing-of-the-Thorp-shuffle-September-26-2026/build/main.tex#L486-L539)): coset caps of 4×uniform for 8 blocks imply ‖ν̂(ρ)‖_op ≤ √(32C₁)·D^{−5/16}. Completion [L552-598](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Optimal-order-mixing-of-the-Thorp-shuffle-September-26-2026/build/main.tex#L552-L598): TV ≤ 8(1−M) + ½·sqrt(A^16 Σ_{ρ≠1,sgn} D^{−3} + sign term) | full law | C₁ = sup_m Σ_{λ⊢m} 1/f^λ. The paper proves it finite, gives no number | yes |
| Fixed lists (uniform over lists) | `Conditional information…` Thm `thm:first-main` and Lemma `noise:halves` ([02-first-route.tex L141-200](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Conditional-information-under-deterministic-coordinate-sweeps-September-26-2026/build/sections/02-first-route.tex#L141-L200)): any specified list of ≤ 15N/16 labels is within N^{−3/2} after 1024d shuffles. The lemma is explicit for every d: a_T ≤ (1−α/4)^{T−2d} + 4e^{−α²N/4}/α, and TV ≤ ½N^{3/2}√a_T | **q-wise, worst case over lists**, for q ≤ (1−α)N | explicit | `InformationMain` in [ThorpRemaining.lean L492](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/ThorpRemaining.lean#L492-L506) |
| Generic transfer | `From partial permutation information…` Thm `l:main` ([introduction.tex L18-35](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/From-partial-permutation-information-to-Fourier-bounds-September-26-2026/build/sections/introduction.tex#L18-L35)): for **any** measure f ≤ 1 on S_N with complementary coset caps B for b blocks, ‖f̂(ρ)‖²_HS ≤ bBC_u·D^{−1+(u+2)/b}. Plus Lemma `l:trim`, Lemma `l:plancherel`, Prop `l:amplification` ([foundations.tex L43-90](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/From-partial-permutation-information-to-Fourier-bounds-September-26-2026/build/sections/foundations.tex#L43-L90)) | full law from partial laws | explicit given C_u | `complementaryCosets_finite` ([statement](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/PartialPermutation.lean#L93-L108), [proof module](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/RepresentationTheory/PartialPermutation/Main.lean#L11)). Generic over any finite X, any b, any f. |
| 512d | `Random coordinate frames` Cor `shear:cor:512` ([L245-290](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Random-coordinate-frames-and-partial-permutation-laws-September-26-2026/build/sections/07c-transfer-applications.tex#L245-L290)) | full law | asymptotic only. Round-independent floor ≈ ½·8C₁·√2·N^{−1/8} ≈ 18.6·N^{−1/8}: vacuous (≥ 1) for N ≤ 2^32, and 0.07 at 2^64 | via `FrameMain` (32800d) |
| ½N^{−5} after P sweeps | `Random-subspace tests…` Thm `ten:lowplanes:main` ([L24-30](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Random-subspace-tests-and-trace-smoothing-for-coordinate-sweeps-September-26-2026/build/sections/introduction.tex#L24-L30)) | full law | **P absolute but not explicit** (threshold n₀ plus base cases by compactness) | `regular_trace_smoothing` (∃P) |
| Spectrum (companion read as requested) | `Compatibility entropy…` Thm `tra:duality:moment` and Cor `cor:intro-consequences` ([L45-63](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Compatibility-entropy-and-the-spectrum-of-a-Thorp-sweep-September-26-2026/build/sections/00-introduction.tex#L45-L63)): Z_N(p*) ≤ 1+1/16, s_j(T_N) ≤ j^{−1/(2p*)}, and TV → 0 for M > p* sweeps. Weighted compatibility Thm `tra:duality:weighted` has absolute L, C₀ | full law, and error decays polynomially in N per extra sweep (Cor `e:vanishing-mixing`) | **p*, L, C₀ not explicit.** The base case uses the finite-size gap Lemma `lem:finitegap` | `SpectrumMain`, `weightedCompatibility_main` (∃p) |

**The notion is the strongest one available.** These are TV bounds on the law of the *whole* permutation (an N!-point space), so no q-wise restriction applies. With ideal round functions, a TV distance of δ bounds the advantage of *any* distinguisher, even an unbounded one, making any number of adaptive forward and inverse queries. That includes all N points. So this is full-domain CCA (strong-PRP) security, and **the MRS nCPA→CCA round doubling is not needed** (the triage's "doubled for CCA" is wrong). A real instantiation adds the usual PRF term.

**Constants, re-derived (scratch `bounds.py`).** C₁ = 3.2847, attained at m = 6. This matches the triage's 3.28 and is computed exactly for m ≤ 45, after which the sum decreases toward 2. A = √(32C₁) = 10.25. At 1600d the marginal term is negligible: ε_N ≈ ½N^{−3.03}. The bound is therefore dominated by the round-independent floor ½·A^8·sqrt(Σ D^{−3}) ≈ ½·A^8·√2·N^{−3/2} = **8.6·10^7·N^{−3/2}**, which confirms the triage's ≈9e7. Values:

| N | rounds 1600d (AES calls with 5× trick) | TV, paper constants | TV, Lean `fullRate` (cruder: 96^8·ΣD^{−2}) |
|---|---|---|---|
| 2^20 | 32,000 (6,400) | 2^−3.6 | 2^+5.8 (vacuous) |
| 2^32 | 51,200 (10,240) | 2^−21.6 | 2^−6.2 |
| 2^64 | 102,400 (20,480) | 2^−69.6 | 2^−38.2 |

Adding rounds cannot push below this floor. Only more convolution factors (more blocks) can.

**Corrections to the triage.**
1. "First proof that a fixed-round shuffle cipher is secure against all N queries" is wrong. Mix-and-cut (Ristenpart–Yilek 2013) is fixed-time and fully secure with Θ(lg²N) rounds, and Morris's O(lg³N) Thorp bound already implied full security ([mix-and-cut paper](https://rist.tech.cornell.edu/papers/mixandcut.pdf)). What is new is fixed-time full security in **Θ(lg N)** rounds.
2. The cost claim of "205k PRF calls at N = 2^64" is wrong. It is 102,400 rounds, which is 20,480 AES calls with MRS batching, with no doubling.
3. The swap-or-not transfer is no longer an unchecked extrapolation. It goes through (see Opportunity 1).

## Current practice & state of the art

- **Provable small-domain encryption** (ideal round functions; rounds = PRF calls for SN, rounds/5 AES calls for Thorp):
  - MRS'09 Thorp: CCA with r(4n−2) rounds, Adv ≤ (2q/(r+1))(4nq/N)^r. This is useful only for q < N/(4 lg N) ([MRS'09](https://www.math.ucdavis.edu/static/research/infovault/morris/Lecture_Notes-5677-09.pdf), Thm 5).
  - HMR'12 swap-or-not: TV of q designated points ≤ 2N^{3/2}/(r+2)·((q+N)/2N)^{r/2+1}. This works for q ≤ (1−ε)N. The authors only *conjecture* full-domain security ([HMR'12](https://arxiv.org/abs/1208.1176)). Dai–Hoang–Tessaro tightened it ([eprint 2017/537](https://eprint.iacr.org/2017/537)); I could not retrieve the exact statement, so the tables use HMR'12.
  - Full domain:
    - Mix-and-cut: fixed time, Θ(lg²N) rounds ([RY'13](https://rist.tech.cornell.edu/papers/mixandcut.pdf)).
    - Sometimes-Recurse: expected Θ(lg N) rounds, variable time. Morris–Rogaway argue the variable time does not leak because the round count is determined by the ciphertext. Their worst case equals mix-and-cut's ([eprint 2013/560](https://eprint.iacr.org/2013/560); [slides](https://www.iacr.org/conferences/eurocrypt2014/20.pdf)). SR left open whether an oblivious shuffle reaches worst-case Θ(lg N). Family 238 answers that for Thorp, asymptotically.
- **Deployed FPE is Feistel, with no full-domain proof.**
  - NIST SP 800-38G Rev.1 2nd public draft (Feb 2025): FF1 only (10 rounds), FF3/FF3-1 removed after Beyne's attack, radix^minlen ≥ 10^6 now a requirement. NIST cites small-domain attacks (Bellare–Hoang–Tessaro 2016, Durak–Vaudenay 2017, Hoang–Tessaro–Trieu 2018, Beyne 2021) and puts single-target recovery against FF1 at domain 10^6 at ≥ 2^77 data ([2pd page](https://csrc.nist.gov/pubs/sp/800/38/g/r1/2pd), [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38Gr1.2pd.pdf)).
  - Libraries:
    - Rust `fpe` (str4d), about 2.7M downloads: FF1 only. It enforces `MIN_NS_DOMAIN_SIZE = 1_000_000` ([ff1.rs L32-41](https://github.com/str4d/fpe/blob/e2654af6072f4d83588a29064f97ccbdb04eb34e/src/ff1.rs#L32-L41)) and uses a 10-round loop ([L289](https://github.com/str4d/fpe/blob/e2654af6072f4d83588a29064f97ccbdb04eb34e/src/ff1.rs#L289)).
    - Go `capitalone/fpe`: FF1 with 10 rounds and FF3 with 8 rounds, with `feistelMin = 100` by default ([ff1.go L35-41](https://github.com/capitalone/fpe/blob/b7dcc90b924e240eac5af5ff2d4d913fbf9985f0/ff1/ff1.go#L35-L41), [ff3.go L33-39](https://github.com/capitalone/fpe/blob/b7dcc90b924e240eac5af5ff2d4d913fbf9985f0/ff3/ff3.go#L33-L39)). That default is below the Rev.1 requirement. This is a side note unrelated to Thorp.
    - Python `ff3` (mysto): FF3/FF3-1, now flagged as withdrawn ([README L18-22](https://github.com/mysto/python-fpe/blob/c51da06c72ca69af9dde1e18cfb0addfeb8bae96/README.md#L18-L22)).
  - Google Cloud Sensitive Data Protection uses FPE-FFX and recommends AES-SIV unless format preservation is required ([docs](https://docs.cloud.google.com/sensitive-data-protection/docs/pseudonymization)).
  - A crates.io search for "swap-or-not" or "thorp" found no FPE crate. I found no production FPE using Thorp or swap-or-not. The GitHub search API was unavailable in this sandbox, so this search was not exhaustive.
- **Ethereum consensus uses swap-or-not as a public-seed shuffle, not a keyed cipher.**
  - `compute_shuffled_permutation` / `compute_shuffled_index`: the pivot is SHA256(seed‖round) mod N, and the swap bit comes from SHA256(seed‖round‖pos//256) ([beacon-chain.md L1211-1245](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/specs/phase0/beacon-chain.md#L1211-L1245)).
  - `SHUFFLE_ROUND_COUNT = 90` ([L592](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/specs/phase0/beacon-chain.md#L592); [mainnet preset L11-12](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/presets/mainnet/phase0.yaml#L11-L12)).
  - Used for committees ([L1273-1284](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/specs/phase0/beacon-chain.md#L1273-L1284)), sync committees ([altair L324-344](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/specs/altair/beacon-chain.md#L324-L344)), proposer selection ([gloas L1198-1223](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/specs/gloas/beacon-chain.md#L1198-L1223)) and subnet subscription ([p2p L1820-1832](https://github.com/ethereum/consensus-specs/blob/9a8fdd0703d6ccc18e2c6c52eb08576cace262eb/specs/phase0/p2p-interface.md#L1820-L1832)).
  - Client implementations: Lighthouse ([compute_shuffled_index.rs L21-50](https://github.com/sigp/lighthouse/blob/6db6ae9382b7d6f5bd1e0ca0d349bc0dc94adba2/consensus/swap_or_not_shuffle/src/compute_shuffled_index.rs#L21-L50)) and protolambda's Go version ([shuffle.go L32-60](https://github.com/protolambda/eth2-shuffle/blob/fd840f1036c1f8f6d7625ffe6ff4d9c60f942876/shuffle.go#L32-L60)).
  - The 90 comes from HMR's "≈6 lg N rounds before CCA bounds kick in" and a "4 log₂ N" rule of thumb at about 2^22 validators ([eth2book](https://eth2book.info/latest/part2/building_blocks/shuffling/); [issue 563](https://github.com/ethereum/consensus-specs/issues/563)).
  - The relevant security notion is statistical near-uniformity of the permutation over a random-oracle seed, together with limited RANDAO grinding. There is no secret key.

## Opportunities

### 1. Full-domain swap-or-not via the generic eight-block lift (verdict on triage Q2: **SUPPORTED**)

**Why the lift is generic.** The transfer (Thm `l:main` together with Lemmas `l:trim` and `l:plancherel`) is stated and Lean-proved for an arbitrary measure on S_N and an arbitrary block partition (`ComplementaryCosetsFiniteStatement`). The Thorp-specific inputs are only three: (i) the partial-law bound, (ii) the sign mean being 0, and (iii) blocks of rounds being i.i.d. so that the law of p blocks is μ^{*p}. Swap-or-not with ideal round keys and functions satisfies all three:
- (i) HMR Thm 3 bounds the TV of *any designated* q-set, which is stronger than the averaged bound Thorp needed. So any partition works, and no 8 | N divisibility is needed.
- (ii) In each round every non-fixed pair {x, K−x} has an independent fair coin, so flipping one coin multiplies the permutation by a transposition. Hence E[sgn] = 0 exactly.
- (iii) Rounds are i.i.d.

**The resulting bound.** With b blocks, u > 0, and p blocks of r rounds each:
δ = b·HMR(N, N−⌊N/b⌋, r), and
TV(SN^{pr}) ≤ ½[pδ + sqrt((pδ)² + δ^{2p} + (bC_u)^p·Z_{p(1−(u+2)/b)−1}(N))].
Here Z_s(N) = Σ_{λ≠(N),(1^N)} D_λ^{−s} is computed exactly for defect ≤ 10, with a rigorous tail from Lemma `l:degree-basic`.

**Rounds for full-domain security ε (fixed time, all N adaptive two-sided queries), optimized over b ∈ {4,…,64}, u ∈ [0.5, 4], p ≤ 60.** Columns: (A) HMR'12 SN, CCA at q = N/2, partial domain only, for reference. (B) **SN-lift (new), q = N**. (C) Thorp-lift (new, from the paper's own fixed-list lemma), q = N, given as rounds / AES calls. (D) Mix-and-cut (RY Thm 5 / per-stage tuned). (E) SR, mean / worst. MRS'09 Thorp only reaches q < N/(4 lg N) = 2^13.7, 2^25, 2^56 respectively, so it has no full-domain entry.

| N | ε | (A) HMR q=N/2 | **(B) SN-lift** | (C) Thorp-lift rds / AES | (D) MaC | (E) SR mean / worst |
|---|---|---|---|---|---|---|
| 2^20 | 2^−32 | 535 | **13,959** | 33,000 / 6,600 | 5,440 / 5,226 | 552 / 4,181 |
| 2^20 | 2^−64 | 838 | **37,240** | 83,980 / 16,796 | 8,460 / 8,247 | 855 / 7,042 |
| 2^20 | 2^−128 | 1,447 | **113,526** | 246,840 / 49,368 | 14,560 / 14,338 | 1,464 / 12,822 |
| 2^32 | 2^−32 | 705 | **9,792** | 22,656 / 4,531 | 11,424 / 10,725 | 729 / 8,231 |
| 2^32 | 2^−64 | 1,009 | **23,220** | 52,160 / 10,432 | 16,256 / 15,576 | 1,032 / 12,915 |
| 2^32 | 2^−128 | 1,619 | **66,600** | 144,576 / 28,915 | 26,048 / 25,337 | 1,643 / 22,356 |
| 2^64 | 2^−32 | 1,161 | **8,967** | 21,056 / 4,211 | 37,440 / 33,892 | 1,194 / 24,184 |
| 2^64 | 2^−64 | 1,466 | **16,160** | 37,120 / 7,424 | 47,168 / 43,646 | 1,500 / 33,741 |
| 2^64 | 2^−128 | 2,078 | **38,794** | 85,952 / 17,190 | 66,752 / 63,220 | 2,112 / 52,966 |

FF1 does 10 Feistel rounds (≈ 10–30 AES calls) and has no full-domain proof.

How to read the table:
- **The triage's "~8× rounds" is the right order only at large N.** SN-lift divided by HMR's q = 7N/8 nCPA rounds is 3.5–8.5× at 2^64, 6.5–19× at 2^32, and 12–36× at 2^20. The lift's floor (bC_u)^{p/2}·N^{−(pγ−1)/2} forces the number of blocks p to grow like lg(1/ε)/lg N, so the cost grows roughly as lg²(1/ε)/lg N for small domains.
- **Against prior fixed-time full security** (mix-and-cut): SN-lift wins about 3–4× at N = 2^64, ties at 2^32, and loses about 2.5–8× at 2^20.
- **Thorp-lift with MRS 5× batching** is the cheapest fixed-time option in AES calls at N ≥ 2^32: about 7.4k at 2^64 / 2^−64, versus 16k for SN-lift and 44k for mix-and-cut.
- **SR's expected cost is still about 3.5–15× lower than the best fixed-time option** in each row (counting PRF/AES calls).
- Sensitivity: restricting to u = 1 (C₁, whose finiteness is Lean-checked) raises the counts by 0–25%. Using u = 0.25 (C_{1/4} ≈ 19.3, numerical) lowers the 2^64 counts by about 10–15%.

**Who benefits:** small-domain-encryption theory (HMR's conjecture is settled qualitatively), and anyone who needs a constant-time, fully secure PRP on a small domain with a citable proof. Examples: enciphering *all* identifiers in a table, or tokenization where most of the domain gets issued.

**Measurement:** a checked note with (a) the corollary statement, (b) certified bounds on C_u (currently numerical: sup at m ≤ 45), and (c) the table above reproduced by an independent script.

**Risks:**
- My bookkeeping is unreviewed.
- The C_u values need a certified tail bound.
- HMR Thm 3 is a peer-reviewed but unformalized input.
- The practical demand for provable full-domain FPE is small. FF1 users accept heuristic security at about 1000× lower cost.
- The PRF instantiation adds Adv^prf over roughly rounds × N calls.

**First step:** write the 2–3 page corollary using `bounds.py` as the worked example, and send it to the swap-or-not and SR authors (Hoang, Morris, Rogaway, Tessaro) for a sanity check.

### 2. Thorp-cipher parameter sheet: explicit partial- and full-domain bounds

The fixed-list Lemma `noise:halves` is explicit for every d and uniform over lists. It replaces MRS'09's ceiling of q < N/(4 lg N) with q ≤ (1−α)N at O(lg N/α) rounds. CCA at ε = 2^−64, using MRS doubling, gives:

| | q | Thorp rounds (AES) | MRS'09 | HMR SN |
|---|---|---|---|---|
| N = 2^64 | N/(8 lg N) | 1,802 (360) | 29,210 | 613 |
| N = 2^64 | N/2 | 3,580 (716) | n/a | 1,466 |
| N = 2^64 | 7N/8 | 14,230 (2,846) | n/a | 6,455 |

So, per AES call, Thorp now beats swap-or-not for partial-domain use when 32 | N. Full-domain Thorp-lift is column (C) above. **Benefit:** guarantees. It gives a corrected comparison for anyone who cites MRS'09, along with the cheapest fixed-time full-security option at N ≥ 2^32 in AES calls. **Risks:**
- The CCA rows need the same lemma for the inverse shuffle (reverse coordinate order). This is plausible, since the argument does not use the direction, but it is unchecked.
- Thorp natively covers only N = 2^d. Decimal domains need cycle-walking, which brings back variable time.
- **First step:** bundle with Opportunity 1 as a single note.

### 3. Make the spectral exponent p* effective (long-range research)

The Compatibility-entropy and Random-subspace companions give the *right shape* for cryptography. Each extra sweep multiplies the error by roughly N^{−c} (Cor `e:vanishing-mixing`), so there is no round-independent floor. Rounds for ε = 2^−λ would be about d·(p* + λ/(c·lg N)). But p*, P, L and C₀ are existential, coming from "sufficiently large" thresholds plus a compactness base case (Lemma `lem:finitegap`). An effective p* of, say, ≤ 10 would make fixed-time Thorp roughly competitive with SR's expected cost. **Effort:** multi-year, and the base cases for small n cannot be computed (n! states). Verdict: monitor.

## What is NOT an opportunity here (and why)

- **Ethereum `SHUFFLE_ROUND_COUNT`: nothing changes.**
  - Before and after family 238, no full-permutation uniformity bound covers 90 rounds. The support argument only requires ≳ 2 lg N ≈ 40 rounds, so 90 is not refuted either.
  - The lift would need about 14k rounds at N ≈ 2^20. That is a hard fork with roughly 150× the shuffle cost, for no practical gain.
  - At 90 rounds, HMR's existing bound already gives TV ≤ 2^−21.5 for any committee-sized set (q ≤ 2048), 2^−15 for a 10% coalition, and is vacuous for q ≥ N/2. These numbers are unchanged.
  - RANDAO last-revealer grinding dominates any residual shuffle bias.
  - Exact small-N computations (below) suggest true mixing is far faster than any proof.
- **Replacing FF1 (or reviving FF3-1) with Thorp or swap-or-not in libraries or standards: no.** Provable full-domain security costs 10^3–10^4 AES calls against FF1's ~10–30. NIST's 2025 draft addresses small-domain attacks through domain-size floors, not by changing the primitive. The Rust, Go and Python FPE targets above are untouched.
- **Using the literal 1600d / 512d / ½N^{−5} statements as cipher parameters: no.** 1600d has a round-independent floor of 8.6e7·N^{−3/2}, and Lean's certified rate is vacuous at 2^20. 512d is asymptotic (its floor of about 18.6·N^{−1/8} is vacuous up to 2^32 and still 0.07 at 2^64). The N^{−5} and spectral results have non-explicit sweep counts.
- **Oblivious shuffles (MPC, ORAM, mixnets) built from iterated Thorp/butterfly networks: no.** Routing a sampled permutation through a Beneš/Waksman network is exact at depth 2 lg N − 1. Thorp needs 1600 lg N layers (or about 10^4 by the optimized bound). Each layer costs a communication round in MPC.
- **Card shuffling / casinos: no.** Software uses PRNG plus Fisher–Yates. The Thorp result concerns a physical model.

## Experiment results

All scripts are in `/home/claude/work/repos/scratch_shufflecrypto/`.

1. **Constants** (`cu.py`, `degsums.py`): C₁ = 3.2847 (m = 6), C₂ = 2.4722 (m = 4), C_{1/2} = 5.906, C_{1/4} = 19.34. These are exact sums for m ≤ 45, after which they decrease toward 2.
2. **Literal bounds** (`bounds.py`): the table above. Floor 8.6·10^7·N^{−3/2}, giving 2^−18.6 at N = 2^30, which confirms the triage. The Lean `fullRate` floor is about 6·10^7·N^{−1}.
3. **Optimized lifts and baselines** (`bounds.py`, `extra.py`, `mac_fix.py`, `compare.py`): the main table.
   - SR and mix-and-cut reproduce the published figures: SR mean / worst 563/4411, 1048/18239, 1723/51453 rounds at 10^6, 10^16, 10^30 and ε = 10^−10, matching MR Fig. 2 exactly. Mix-and-cut needs 10,440 rounds at N = 2^30, versus "≈10,000" in RY.
   - Decimal domains at ε = 2^−32: N = 10^6 needs 15,240 SN-lift rounds (SR 552 / 4,303); N = 10^16 needs 7,819 (SR 1,037 / 17,939).
4. **Exact small-N mixing** (`exact_small.py`, `pairs.py`; exact rational-free dynamic programming over S_N):
   - Thorp at N = 8: full-permutation TV ≤ 1/4 after **5** shuffles (support lower bound 4; the theorem's 1600d = 4,800), and ≤ 2^−30 after 34.
   - Swap-or-not at N = 6–10: TV ≤ 1/4 after 4–5 rounds, ≤ 2^−30 after 38–40.
   - Two-card marginals: Thorp contracts by exactly 1/N per sweep (about ½ per shuffle) for N = 8–256. Swap-or-not contracts by about 0.51–0.56 per round, independent of N, for N = 8–256.
   - Taken together, the true constants are probably within a small factor of the support bound. The proof constants (1600; 31/32 per step) are artifacts.
   - The full-permutation computation cannot go beyond N ≈ 10 (N! states).

## Sources

- OpenAI math drop (commit fd4aeeb): main paper and companions as linked above; `lean/docs/238.md`.
- Morris, Rogaway, Stegers, *How to Encipher Messages on a Small Domain* (CRYPTO 2009): https://www.math.ucdavis.edu/static/research/infovault/morris/Lecture_Notes-5677-09.pdf ; abstract https://www.cs.ucdavis.edu/~rogaway/papers/thorp.html
- Hoang, Morris, Rogaway, *An Enciphering Scheme Based on a Card Shuffle* (CRYPTO 2012): https://arxiv.org/abs/1208.1176
- Morris, Rogaway, *Sometimes-Recurse Shuffle* (EUROCRYPT 2014): https://eprint.iacr.org/2013/560 ; full text via https://scispace.com/pdf/sometimes-recurse-shuffle-almost-random-permutations-in-5bg6y3xl0v.pdf ; slides https://www.iacr.org/conferences/eurocrypt2014/20.pdf
- Ristenpart, Yilek, *The Mix-and-Cut Shuffle* (CRYPTO 2013): https://rist.tech.cornell.edu/papers/mixandcut.pdf
- Dai, Hoang, Tessaro, chi-squared method (CRYPTO 2017): https://eprint.iacr.org/2017/537 ; Morris, Oberschelp, nCPA→CCA: https://ar5iv.labs.arxiv.org/html/2211.07896
- NIST SP 800-38G Rev.1 2pd (Feb 2025): https://csrc.nist.gov/pubs/sp/800/38/g/r1/2pd ; https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38Gr1.2pd.pdf
- Ethereum: consensus-specs @9a8fdd0 (links above); eth2book shuffling https://eth2book.info/latest/part2/building_blocks/shuffling/ ; issue 563 https://github.com/ethereum/consensus-specs/issues/563
- Google Cloud SDP pseudonymization: https://docs.cloud.google.com/sensitive-data-protection/docs/pseudonymization
- Libraries: str4d/fpe @e2654af, capitalone/fpe @b7dcc90, mysto/python-fpe @c51da06, sigp/lighthouse @6db6ae9, protolambda/eth2-shuffle @fd840f1.
- Limitation: the web-search budget ran out before I could retrieve Dai–Hoang–Tessaro's exact swap-or-not bound or survey tokenization vendors. Using their tighter bound would lower SN-lift counts by a constant factor.
