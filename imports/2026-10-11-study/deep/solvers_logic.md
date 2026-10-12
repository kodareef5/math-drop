# Solvers & logic: random-SAT windows, Snaky, quasipolynomial games, Barnette, PTS normalization

**Bottom line.** None of the five families gives a deployable speed-up. The one claim the triage flagged as a practitioner redirect (#235: "ν = 2, not 1.5, so fix generator docs") is mathematically correct, but it is **not new**. Wilson already proved ν ≥ 2 in 2000–2002, and the new Θ(n) variance upper bound only adds the matching side. My experiment (11.8k exact hitting times, n = 50–300) shows the practical picture is unchanged at every n anyone uses. The window scales like n^0.34 (ν_eff ≈ 1.5). The Θ(n) disorder component is measurable (≈ 1.2n, from regression on sign-imbalance statistics) but is outweighed by an ≈ 28n^0.58 term until n ~ 3×10³, so ν_eff is only ~1.75 even at n = 10⁴. Do **not** pursue a docs or generator redirect. Two small INSTANCES opportunities are real and cheap:
- **Snaky (#187):** a certificate-backed TRUE/FALSE QBF family with tunable hardness. CAQE already times out at 15 free cells and height 8.
- **Barnette (#180):** guaranteed-Hamiltonian cubic instances. Hamiltonicity was previously guaranteed only to ~84 vertices, and some are surprisingly hostile to single-run LKH.

The mean-payoff/stochastic algorithm (#104) is a genuine theory advance: the first deterministic quasipolynomial bound in binary input length for MPG, SSG and MPPG. My prototype of its recursion is correct on tiny games but makes about 4.6×10^4 calls on a 4-vertex game, so it is useless as a solver. Oink cannot host it anyway, because Oink is parity-only. Worth monitoring, not implementing. #245 (WN ⇒ SN for all PTS, Lean-checked, β only) changes nothing operational for Coq/Lean/Agda: none of them is a PTS with β-only conversion, and no kernel termination proof routes through weak normalization.

---

## What the papers actually prove

Repo: `openai/math` @ `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. All are unrefereed claims of an unreleased model.

### #235: Limiting random SAT thresholds, sharp variance, computability (4 manuscripts)
Model throughout: proper 3-clauses (distinct variables, fair signs), i.i.d. **with replacement**. H_n = first m at which F_m is UNSAT.
- **Linear Variance of the Random 3-SAT Hitting Time** (Oct 5), `main.tex` Thm `thm:main` (L61–70): Var(H_n) ≤ Cn for all n ≥ 3, and ≥ cn for n ≥ n_0. C and c are unspecified absolute constants.
  - **Only the upper bound is new.** The lower bound is a short deduction from Wilson 2002, Cor. 4, restated as Thm `thm:wilson` (L647–655).
  - Cor. `cor:window` (L682–704): for each fixed η ∈ (0, ½), r_n(η) − r_n(1−η) = Θ_η(√n), where r_n(p) is the clause count at which P(SAT) first drops to p.
  - The paper itself notes (L706–709) that this is about fluctuation **around the finite-size mean E H_n**. It gives no rate for E H_n/n → α.
  - Proof: Efron–Stein with clause omission, plus a new potential P_d(S) built from random 2-clause kill probabilities. Not Lean-formalized. The Lean comparator `SATVariance.lean` L54–66 states only the O(n log n) bound for k = 3.
- **Variance of the Random k-SAT Hitting Time** (Sep 27), Thm `thm:variance`: Var(H_n) = Θ_k(n) for k ≥ 4, and O(n log n) for k = 3. Lean-formalized (per `lean/docs/235.md`).
- **A Limiting Satisfiability Threshold for Every Fixed Clause Size** (Sep 25), Thm `thm:main`: P_n(⌊cn⌋) → 1 for c < α_k and → 0 for c > α_k. Lean-formalized. Priority is explicitly credited to **Carenini (ECCC TR26-229 and Oct 5 follow-up)**, whose window bound is O(n^{1/2+1/k}).
- **Computing the Random 3-SAT Threshold** (Sep 27), Thm `thm:main` (introduction L22–33): α_3 is a computable real.
  - The lower certificate carries error 2^67 n^{−1/6} (`assembly.tex` L10), which is nontrivial only for n ≳ 2^389. **Galactic.**
  - The paper computes no digits of α_3.

**Is the triage's logic right?** Mostly yes, with two corrections.
1. **The variance result is for the right quantity, and it does imply the window width.** P(F_m SAT) = P(H_n > m), so the satisfiability curve *is* the survival function of H_n. Var = O(n) plus Chebyshev gives an O(√n) clause window (upper side). Wilson gives Ω(√n) (lower side). In density, the window is Θ(n^{−1/2}), so ν = 2 in the convention where width ∝ n^{−1/ν}.
2. **The ν = 2 part is not news.** Wilson proved ν ≥ 2 (when well-defined) for all three standard ensembles in 2000/2002. His abstract already says this contradicts the experimental ν_3 = 1.5 ± 0.1 ([arXiv math/0005136](https://arxiv.org/abs/math/0005136v2)). Wilson's mechanism is "bystander" clauses: a constant fraction of clauses contain a variable that occurs only once, and each added clause can move P(SAT) by at most O(1/√m).

   Leone, Ricci-Tersenghi and Zecchina (2001) had already explained, in the statistical-physics literature, that the generation noise of the random formula forces ν = 2 asymptotically, while an intrinsic smaller exponent governs moderate N. They fitted w(N) = A·N^{−1/ν} + B·N^{−1/2} ([cond-mat/0103200](https://arxiv.org/abs/cond-mat/0103200)). The general disordered-systems version, that a ν_FS = 2/d noise scale is separate from the intrinsic ν, is Pázmándi–Scalettar–Zimányi 1997 ([cond-mat/9704155](https://arxiv.org/abs/cond-mat/9704155)).

   So the new paper upgrades "ν ≥ 2" to "ν = 2 exactly for the full variance". That closes a 25-year-old gap mathematically, but it does not change what experimenters should believe at n ≤ 10^3.

### #187: Snaky in 21 Maker moves
- `introduction.tex` Thm `thm:main` (L25–33): on empty ℤ², one Maker policy completes a copy of Snaky (6 cells, all 8 symmetries) within 21 Maker claims against every Breaker play.
- `strategy.tex` Cor. `cor:finite-board` (L64–71): the same holds on the 251-cell support T_727 and on the 17×17 board.
- **Constructive and certificate-backed.** `verification/certificate.txt` holds 722 lines, giving 728 "cards" (A, T, h): Maker owns A, Breaker owns nothing in T, Maker wins within h moves (Def. `def:claim`, `templates.tex` L9–19). Each card is a pivot cell plus placed references to earlier cards. The checker `verify_certificate.py` (119 lines, pure Python) recomputes all cards in **0.3 s**; I ran it and it passed. Lean: `SnakyTwentyOne.lean` theorem `snaky_winning_strategy_21_with_legal_states` (L45). The formalization is 94 files, 71k lines, 0 `sorry`.
- Card statistics (my tabulation):

  | Height h | Cards | Smallest number of free cells |T∖A| |
  |---|---|---|
  | 2 | 42 | 3 |
  | 5 | 100 | 9 |
  | 8 | 51 | 15 |
  | 12 | 20 | 28 |
  | 16 | 5 | 72 |
  | 21 | 1 | 251 |

  The certificate is therefore a **graded ladder of TRUE finite game positions**.
- Caveat: the paper claims neither optimality of 21 nor that h is tight for any card. My QBF runs found at least one card (290) where h−1 also suffices.

### #104: Quasipolynomial algorithms for mean-payoff / stochastic / parity games (4 manuscripts)
- **Deterministic MPG** (Sep 25), `01-introduction.tex` Thm `thm:main` (L34–51): computes the zero-threshold winning set in 2^{C (log₂(L+2))²} bit operations, where L is the **binary** input length (weights arbitrary signed binary). Values, optimal positional strategies and minimum energy credits follow (Sections 7–8). Not formalized.
- **Randomized MPG** (Sep 25): the same bound, correct with probability ≥ 7/8. **Lean-formalized** as a Turing-machine statement (`RandomizedMeanPayoff.lean` L123). The appendix contains a Lean-checked counterexample to Truffet's arXiv:2603.26423v4 strongly-polynomial tropical rule.
- **Mean-payoff parity** (Oct 5), Thm `thm:main` (L33): deterministic quasipolynomial time via 2^{O(log² n)} calls to the MPG solver.
- **Turn-based stochastic MPG** (Oct 5), Thm `thm:main` (L50): deterministic quasipolynomial time in binary L. This includes Condon's simple stochastic games (value ≥ ½) by an explicit reduction. **This is the headline novelty.** Previously the best results were randomized subexponential (Ludwig 1995 and successors), pseudopolynomial with a fixed number of chance nodes, or quasipolynomial only for bounded treewidth (Chatterjee et al. 2023).
- **The algorithm is fully specified.** Procedure `Label(A, D, a, b)` (`04-algorithm.tex` L21–85) works on integer boxes [A, A+D]^V with rational masses a, b. Steps:
  1. Base case on mass (a_i b_i > 1) or width (D < 4096 → plain clipped value iteration `Basic`).
  2. Downward pivot pass with width-D/128 children at masses (a, 4/3·b).
  3. Upward pass with width-D/128 children at (4/3·a, b).
  4. A provisional width-D/2 child.
  5. A continuation child at the same width with masses multiplied by 4/5 and 8/5 (product ×32/25).

  Initial box: D_0 ≥ 64(n+1)(W+1) after the weight bias ŵ = (n+1)w + 1 (`02-boxes.tex` L13–17, L92–95). Call bound: (H+1)(B_0+1)(1+Hs)^{B_0} with s = 2048n+3 and B_0 = 1 + ⌊log_{32/25} n²⌋ (`06-complexity.tex` L28–37).
- **Is it different from existing quasipolynomial parity solvers?** Structurally it is a cousin of Parys's reduced-precision recursion and Lehtinen–Parys–Schewe–Wojtczak; the paper says so (`06-complexity.tex` L53–58). It differs in two ways:
  1. The "precision" is a rational mass budget on supports of integer potential vectors, not a dominion-size bound.
  2. It operates on **numeric potentials** (value-iteration operator F), not attractor decompositions.

  It is not Calude et al.'s play-summary automaton, nor Jurdziński–Lazić succinct progress measures, nor Fearnley et al.'s QPT; those are what Oink's QPT/SSPM implement. Restricted to parity games via Jurdziński's reduction, it would give nothing beyond Calude et al. 2017: parity games are already quasipolynomial. **Its novelty is entirely in the binary-weight MPG / stochastic setting**, which universal-graph methods provably cannot reach. Fijalkow–Gawrychowski–Ohlmann give an N^{1−1/n} lower bound for that approach ([arXiv 1812.07072](https://arxiv.org/pdf/1812.07072)).

### #180: Barnette's conjecture
- `paper.tex` Thm `thm:main` (L79–82): every cubic, bipartite, planar, 3-connected graph is Hamiltonian.
- Thm `thm:partition` and Cor. `cor:edge-avoidance` (L794): the cycle can avoid any chosen edge.
- Cor. `cor:pfaffian-paths` (L812): every 3-edge path in a cubic 3-connected Pfaffian bipartite graph lies on a Hamiltonian cycle.
- **Not constructive.** The proof shows that a finite signed exponential sum over Tutte state pairs is nonzero. The paper explicitly says (L168–170) that it gives no polynomial-time construction.
- Lean: `OAI/Combinatorics/Hamiltonian/Main.lean` L47 `theorem main`, 31 files, ~8.9k lines, 0 `sorry`. **High confidence.**

### #245: WN ⇒ SN in pure type systems
- `introduction.tex` Thm `thm:main` (L117): for every PTS (arbitrary sorts, non-functional axioms/rules, reduction inside annotations, open contexts), system-wide weak β-normalization implies system-wide strong β-normalization.
- It is the **β instance** of Geuvers' 1993 conjecture. The paper is explicit that it says nothing about βη (L135–138), and that it is a system-wide statement, not per-term.
- Lean: `ComparatorChallenges/TypeSystemNormalization.lean` L116; proof in `OAI/Computability/TypeSystem/` (33 files, ~29.5k lines, 0 `sorry`, uses `Classical`).
- The proof is a reducibility-candidates construction plus a relational Hurkens-paradox argument that excludes the bad profile graph. It is non-effective: it gives **no bound** on reduction lengths and no algorithm.

## Current practice & state of the art

- **Random 3-SAT generation (#235).**
  - SATLIB's uf/uuf sets use n = 20…250 at m ≈ 4.26n and note that the transition sharpens with n. They do not cite an exponent. SATLIB rejects tautologies and repeated literals; its page does not say whether duplicate clauses are allowed ([SATLIB RND3SAT](https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/RND3SAT/descr.html)).
  - CNFgen's `RandomKCNF` samples clauses **without** repetition ([cnfgen randomformulas.py L82–88](https://github.com/MassimoLauria/cnfgen/blob/24e633bdbed0d0998493bee99c42faf480c7dc96/cnfgen/families/randomformulas.py#L82-L88)). This is a different ensemble from the paper's, but asymptotically equivalent at this scale.
  - No generator I checked hard-codes a window exponent; users calibrate the 50% point empirically per n.
  - The physics literature has treated ν_3 ≈ 1.5 as an *effective/intrinsic* exponent with an asymptotic ν = 2 noise floor since 2001 (Leone et al.). Lee et al. 2010 ([PRE 82, 061109](https://arxiv.org/abs/1005.0251)) work on algorithmic-transition FSS and warn of strong finite-size effects for N ≲ 10³.
- **Positional-game QBF (#187).**
  - Shaik, Mayer-Eichberger, van de Pol and Saffidine (2023) encode Hex and Harary's tic-tac-toe in QBF ([arXiv 2301.07345](https://arxiv.org/pdf/2301.07345)). On 5×5 HTTT, all polyominoes up to 4 cells solve in under 10 s and "Z" solves at depth 11 in about 8 minutes; the other polyominoes, Snaky included, time out at depth 15 with a 3 h budget. Best pipeline: Bloqqer + CAQE.
  - Encoder: Q-sage ([github.com/irfansha/Q-sage](https://github.com/irfansha/Q-sage)); HTTT GDDL models in `Benchmarks/SAT2023_GDDL/GDDL_models/httt/`.
  - The annual QBF evaluation continues as **QBF Gallery 2026** (Seidl, Peyrer, Pulina; JKU Linz; with SAT 2026 at FLoC). It has PCNF, Crafted, Random, 2QBF, non-CNF and DQBF tracks, and asks for application formulas that are hard for current solvers, in QDIMACS/QCIR with redistributable licenses. The 2026 benchmark deadline (May 17) has passed, so the next window is 2027 ([QBF Gallery 2026](https://qbf.pages.sai.jku.at/gallery26/), [QBF Gallery 2023 report](https://arxiv.org/abs/2604.16153)). Neither page mentions positional-game families.
  - Boucher & Villemaire (2025) cover strong achievement games (cited in the Snaky paper).
- **Parity / mean-payoff / stochastic games (#104).**
  - Oink ([github.com/trolando/oink](https://github.com/trolando/oink)) is the reference parity suite. It already ships Parys / Lehtinen et al. recursive quasipolynomial solvers (ZLKQ; ZLKPP-WAW and ZLKPP-LIV by Parys), QPT ordered progress measures (Fearnley et al.), succinct SPM (Jurdziński–Lazić) and their bounded variants. Its own README says fixpoint iteration and Zielonka are among the fastest in practice.
  - For simple stochastic games, practice is value iteration, strategy iteration or quadratic programming in PRISM-games, per Křetínský, Ramneantu, Slivinskiy and Weininger ([arXiv 2008.09465](https://arxiv.org/abs/2008.09465)).
  - MPG/energy solvers use Brim et al. value iteration (pseudopolynomial) or strategy improvement.
- **Hamiltonian cycle (#180).**
  - Barnette's conjecture was verified computationally to 84 vertices by Aldred, Brinkmann and McKay, using plantri and about 3 CPU-years mostly spent finding cycles ([Mohar problem page](https://users.fmf.uni-lj.si/mohar/Problems/P4BarnetteConjecture.html)). Wikipedia states < 86.
  - HCP benchmarking: the FHCP Challenge Set has 1001 known-Hamiltonian graphs from structural families (GP(n,2), uniquely-Hamiltonian, Stedman triples, …), chosen because at least 2 of Concorde, LKH and SLH found them hard. Coudert and Cohen solved 985 ([FHCP paper](https://ar5iv.arxiv.org/html/1902.10352)). There is no Barnette family.
  - Hamiltonicity of 2-connected cubic bipartite planar graphs is NP-complete (Akiyama–Nishizeki–Saito 1980, as cited on Wikipedia). Feder–Subi showed that, had Barnette been false, the 3-connected case would be NP-complete too.
- **Proof-assistant metatheory (#245).**
  - MetaRocq (formerly MetaCoq) assumes strong normalization as its only axiom. It is stated as well-foundedness of reduction on well-typed terms ([PCUICSN.v L12–50](https://github.com/MetaRocq/metarocq/blob/c8cd46054518193103c3bb33aa6e15c7f489e72c/pcuic/theories/PCUICSN.v#L12-L50); [Touring MetaCoq, §4.1](https://arxiv.org/pdf/2107.07670)).
  - Lean 4's kernel has no termination proof at all. Abel & Coquand showed that normalization *fails* for impredicative Prop with proof-irrelevant equality ([LMCS 2020](https://arxiv.org/abs/1911.08174)).

## Opportunities

### solvers_logic-1: Snaky certificate → graded known-truth QBF family (INSTANCES, #187)
**Proposed change.** Publish a generator plus a fixed suite of QDIMACS instances: "Maker to move, owning A, wins within h moves on board T" for certificate cards (A, T, h), at h (TRUE by the certificate) and at h−1 (truth known only when a solver decides it). Add whole-board instances on T_727 (251 cells) and on 17×17 at h = 21 (TRUE). Submit to the QBF Gallery Crafted track in 2027 and contribute the generator to Q-sage.

**How hard is emitting it?** Easy; I did it. `snaky_qbf.py` (≈150 lines) parses the certificate with the paper's own reference semantics and emits a QDIMACS prefix ∃M₁∀B₁∃M₂…∃M_h∃gates. It uses log-encoded move indices; occupied or out-of-range moves act as passes, which is sound by monotonicity of Maker–Breaker games.
- Restricting Breaker to T is sound for TRUE answers: Breaker stones outside T are irrelevant to every child envelope (Def. `def:claim`). For FALSE answers it is a statement about the finite game on T only.
- I also produced Q-sage `bwnib` encodings for Snaky on 7×7 and 17×17 boards with a hand-written GDDL `#blackgoal` listing the 8 orientations. These work out of the box (838 vars on 7×7 at depth 9; 3,690 vars on 17×17 at depth 41).

**Measured (Bloqqer + CAQE 4.0.1, from Q-sage's bundled binaries).**

| Card | h_cert | Free cells | Snaky copies | Vars / clauses | Result at h | Result at h−1 |
|---|---|---|---|---|---|---|
| 6 | 2 | 3 | 2 | 37 / 100 | TRUE 0.04 s | FALSE 0.02 s |
| 16 | 3 | 5 | 3 | 95 / 277 | TRUE 0.11 s | FALSE 0.04 s |
| 27 | 4 | 7 | 4 | 174 / 525 | TRUE 0.5 s | FALSE 0.1 s |
| 81 | 5 | 9 | 5 | 286 / 934 | TRUE 1.1 s | FALSE 0.9 s |
| 167 | 6 | 11 | 6 | 415 / 1382 | TRUE 6.3 s | FALSE 2.5 s |
| 290 | 7 | 13 | 7 | 568 / 1918 | TRUE 16.7 s | **TRUE** 10.3 s |
| 405 | 8 | 15 | 15 | 752 / 2598 | timeout 150 s | timeout |
| 443 | 9 | 17 | 14 | 968 / 3583 | timeout 150 s | timeout |
| 727 | 21 | 251 | 1419 | 32,622 / 165,720 | not attempted | |

Q-sage Snaky on 7×7 at depths 9 and 11, and on 17×17 at depth 41: CAQE timed out at 300 s (100 s for 7×7 after Bloqqer).

So difficulty rises smoothly with height and crosses the current-solver frontier near h = 8. That is exactly the shape a benchmark family needs. Every TRUE instance has an independently checkable certificate: the card's winning strategy, Lean-verified for the whole certificate.

**Who benefits.** QBF solver developers (CAQE, DepQBF, Qute, …) and the QBF Gallery Crafted track. Strategy/certificate extraction research, since a Skolem-function certificate for TRUE instances can be compared with the card strategy. Q-sage users.

**Measurement.** Number of instances (by h) solved within 1 h by each Gallery solver. Whether any solver reproduces h = 21 on T_727 (very unlikely). Whether solvers certify the FALSE side at h−1, which would give new *lower bounds* the paper does not claim.

**Risks.**
- The family is narrow: one game, one shape.
- Gallery curators may down-weight "crafted puzzle" families.
- Above h ≈ 10 everything times out, so the useful range is about h = 5…12.
- FALSE labels at h−1 rest on my encoding, not on the paper; card 290 shows h is not always tight.

**First step.** Emit cards for h = 2…14 (about 5 per height, smallest |T∖A| first) at both h and h−1. Cross-check small ones against Q-sage's independent `bwnib` encoding with the init position set to A. Package with a README and the certificate SHA256 (`3fa12d36…`). Email the QBF Gallery organizers (Seidl) ahead of the 2027 call.

### solvers_logic-2: Barnette graphs as guaranteed-YES HCP instances (INSTANCES, #180)
**Can plantri do it?** Yes, directly. `plantri -bd n` emits exactly the duals of 3-connected eulerian triangulations, i.e. the 3-connected cubic bipartite planar graphs ([plantri-guide.txt L346–352](https://github.com/mishun/plantri/blob/09745aeb09819bf200cfc77617f000258dba0a49/plantri-guide.txt#L346-L352); mirror of plantri 4.5). `-c4` gives the cyclically 4-connected subclass.
- Counts (my run): orders 36, 40 and 44 give 15,374, 171,168 and 2,024,119 graphs, at about 1.2 µs per graph.
- plantri caps the triangulation at 64 vertices, i.e. 124-vertex cubic graphs (the cap is configurable via MAXN ≤ 255 in the source).
- For larger, non-exhaustive instances I used flag graphs (omnitruncations) of random planar maps. These are always cubic, bipartite and planar; I checked 3-connectivity explicitly (κ = 3 on all 416–852-vertex instances tested).

Before this theorem, Hamiltonicity of a Barnette graph above ~84 vertices was guaranteed only by finding the cycle. Now every such instance, at any size, is a certified YES.

**Is it useful? Measured (LKH-2 via `elkai`, HCP as 0/1 TSP).**

| Instances | Single LKH run fails | 10 runs fail | 30 runs fail |
|---|---|---|---|
| plantri Barnette, 84 vertices (30 graphs) | 11/30 | 0/30 | |
| plantri Barnette, 124 vertices (30 graphs) | 21/30 | 2/30 | |
| Flag graphs, ~420 vertices (3 graphs) | 3/3 | 0/3 | |
| Flag graphs, ~850 vertices (3 graphs) | 3/3 | 3/3 | 0/3 (130–165 s) |
| Planted-Hamiltonian random cubic graphs, 848 vertices (2 graphs) | 0/2 | | |

Control: general 3-connected cubic planar duals (`plantri -d`) of the same orders failed even more often (84 vertices: 28/30 at 1 run, 22/30 at 10; 124 vertices: 30/30, 26/30). But those are not known to be Hamiltonian, so failures there are uninformative.

So planar cubic structure makes LKH work hard, and Barnette graphs give you that hardness **with a YES guarantee at every size**. Only the FHCP-style hand-built families offered that before.

**Who benefits.** HCP/TSP heuristic developers (LKH, Concorde-HCP, SLH) and FHCP-style benchmark curators. It is also a natural test family for SAT/ILP Hamiltonicity encodings, since planar subtour structure is a known pain point.

**Measurement.** Time-to-tour vs n for LKH, Concorde and SAT encodings on (a) Barnette flag graphs, (b) plantri random samples at 124 vertices, (c) planted random cubic graphs. Report failure rate per restart budget.

**Risks.**
- Instances may be "hard for LKH but easy for exact HCP solvers". The FHCP challenge showed that structure-exploiting decompositions crack many families.
- Not a large community.
- The theorem guarantees existence only; there is no polynomial algorithm and no planted cycle to compare against.

**First step.** Release a generator (flag-graph construction plus 3-connectivity check, or plantri random sampling with `res/mod`) and a 200-instance suite at 100–5,000 vertices. Send it to the FHCP maintainers (Haythorpe, Flinders).

### solvers_logic-3: Correct the record on 3-SAT window scaling (REDIRECT, #235): do not pursue as a docs or practice change
**What the triage proposed.** Measure the window, then correct generator documentation that quotes ν ≈ 1.5.

**What I found.**
1. No generator I inspected (SATLIB, CNFgen) quotes ν. The ν ≥ 2 vs 1.5 tension has been explained in print since 2001 (finite-size crossover from an intrinsic exponent to a ν = 2 noise floor).
2. **The experiment shows ν_eff ≈ 1.5 throughout the practical range.** Detailed below: sd(H_n) ∝ n^{0.34}, and a two-term fit gives a linear coefficient indistinguishable from zero.

Telling practitioners "the window shrinks as n^{−1/2}" would therefore be *wrong* at every n they use. At 50 ≤ n ≤ 300 the window shrinks as n^{−0.66}. Extrapolating the measured linear-variance component (≈ 1.2n), ν_eff reaches only ~1.62 at n = 10³ and ~1.75 at n = 10⁴. The correct practical statement is unchanged: calibrate the 50% point and the window width empirically per n.

What the paper does give a careful theorist: (i) a rigorous Θ(√n) asymptotic window, and (ii) Var(H) = Θ(n), so ν = 2 is the true asymptotic exponent of the full variance. The "1.5" is now provably a pre-asymptotic effective exponent. That belongs in a review footnote, not in code.

**Verdict:** do not pursue as an engineering redirect. Optional: one paragraph in a survey or wiki noting that Wilson's bound is now matched.

### solvers_logic-4: Implement the quasipolynomial Label recursion in Oink or a game solver (IMPLEMENT/BENCHMARK, #104): do not pursue
**Where it would go.**
- Oink solvers implement `pg::Solver::run()` ([solver.hpp L32–69](https://github.com/trolando/oink/blob/8fbf0a7c3e5b0baa254cb4516258c5c42fa99db1/include/oink/solver.hpp#L32-L69)).
- They are registered in the `Solvers::Solvers()` table ([solvers.cpp L48–85](https://github.com/trolando/oink/blob/8fbf0a7c3e5b0baa254cb4516258c5c42fa99db1/src/solvers.cpp#L48-L85)) and listed in CMake ([CMakeLists.txt L79–105](https://github.com/trolando/oink/blob/8fbf0a7c3e5b0baa254cb4516258c5c42fa99db1/CMakeLists.txt#L79-L105)).
- The template to copy is the QPT solver ([qpt.hpp L24–77](https://github.com/trolando/oink/blob/8fbf0a7c3e5b0baa254cb4516258c5c42fa99db1/src/solvers/qpt.hpp#L24-L77)).
- **But Oink's `Game` stores only priority and owner per vertex** ([game.hpp L478–481](https://github.com/trolando/oink/blob/8fbf0a7c3e5b0baa254cb4516258c5c42fa99db1/include/oink/game.hpp#L478-L481)): no weights, no chance nodes. A port would run the algorithm only on parity games via Jurdziński's reduction (weights n^p), which is exactly the case where it brings nothing new. Oink already has the Parys/LPSW family (ZLKQ, ZLKPP-WAW/LIV).

**Measured cost.** I implemented `Label` as written (`mpg_label.py`, exact Fractions) and checked it against brute-force positional-strategy enumeration: **12/12 random games with n = 2–4 correct.** The cost on these toy games:

| n | W | D_0 | Calls | Width-base calls | Value-iteration evaluations | Time (Python) |
|---|---|---|---|---|---|---|
| 3 | 3 | 2^12 | 4.6×10³ – 9.3×10³ | | | |
| 3 | 20 | 2^15 | 3.7×10⁵ | | ~8.5×10⁵ | ~20 s |
| 4 | 5 | 2^14 | 2.3×10⁵ | | 1.3×10⁶ | 22 s |

A direct Brim et al. value iteration solves these in about nW ≈ 100 sweeps.

The input-independent *minimum* call count (each pivot pass stopping after one call) is already 5×10⁹ for n = 100, W = 1, and 8.8×10³⁰ for n = 100, W = 2^62. The paper's worst-case bound at n = 100 is about 10^272.

The constants (D < 4096 base case, ×4/3 and ×32/25 mass steps, pivot step D/4096) make the recursion depth large even when nothing is hard. **Practicality = 1.** A C++ port gains about 100× but not the 10^5–10^20 needed.

**Who could still care.** Theory groups working on SSG/MPG complexity. The deterministic SSG result may be the most significant theory item in this theme. Tool builders (PRISM-games, Storm) should keep value/strategy iteration.

**Verdict:** do not pursue implementation. Monitor for a practical variant (e.g. using the stationary-pivot certificate as a value-iteration acceleration heuristic) as research.

### solvers_logic-5: Deterministic quasipolynomial SSG/MPG as a theory redirect (RESEARCH, #104): monitor
**What it gives.** This is the first deterministic 2^{O(log² L)} algorithm in the *binary* input length for mean-payoff, mean-payoff parity and turn-based stochastic mean-payoff games, including Condon's simple stochastic games. The randomized MPG version is Lean-checked as a Turing-machine statement ([RandomizedMeanPayoff.lean L113–123](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/RandomizedMeanPayoff.lean#L113-L123)).

**What it changes.** It moves SSG from "NP ∩ coNP, best deterministic bound exponential" to "quasipolynomial". It also shows a route around the universal-graph lower bounds. The appendix counterexample to Truffet's strongly-polynomial tropical rule is a small, concrete redirect for anyone evaluating that claim.

**What to do.** Watch peer review of the unformalized deterministic and stochastic papers. Do not expect tool impact.

### solvers_logic-6: Barnette → polynomial-time algorithm via Pfaffians (RESEARCH, #180): monitor only
The triage suggested checking whether the paper's state-pair sum Z(x) is a Pfaffian or determinant, which with self-reducibility would give a polynomial algorithm. The paper uses double-dimer-style regrouping and Temperley-type correspondences but proves non-vanishing by asymptotic cancellation at a parameter → 0. Making that effective needs a new idea, and it is a legitimate open question. No action beyond flagging it to the planar-algorithms community.

### solvers_logic-7: Proof-assistant metatheory (#245): no operational change
- **What changes:** for the PTS fragment, a proof of weak normalization now suffices for strong normalization. Metatheory papers that prove WN by a normalization-by-evaluation (NbE) argument for a PTS can now cite this to get SN.
- **Does it help MetaRocq?** Its single axiom is SN, as well-foundedness of `cored` on well-typed terms ([PCUICSN.v L44–50](https://github.com/MetaRocq/metarocq/blob/c8cd46054518193103c3bb33aa6e15c7f489e72c/pcuic/theories/PCUICSN.v#L44-L50)). PCUIC is **not** a PTS: it has inductives, fixpoints with a guard condition, cumulativity, η, let, and so on. The theorem covers β only, and WN of PCUIC is no easier to prove than SN anyway.
- **Lean:** the kernel does not normalize, and Abel–Coquand's counterexample shows its theory is not normalizing.
- **Agda:** the type theory is not a PTS either (η, inductive families, sized types).

The result is a Lean-checked theorem and a FORMALIZE-type deliverable already done by OpenAI. The only residual action is citing it in type-theory surveys. Note the proof uses `Classical` and gives no bound on reduction lengths, so it cannot be "run".

## What is NOT an opportunity here (and why)

- **"ν = 2, fix the generators" (#235).** Already proved as a lower bound by Wilson in 2002, already explained physically in 2001, and empirically irrelevant at practical n. My data give ν_eff = 1.52 ± 0.04 at n ≤ 300, extrapolating to ~1.6 at 10³. Nobody hard-codes ν.
- **Computing α_3 from the computability paper (#235; JSON row solvers_logic-8).** The lower certificate's error 2^67 n^{−1/6} becomes < 1 only for n > 2^402. No digits. Galactic.
- **Running the Label algorithm in any tool (#104).** About 10^5 calls on 3-vertex games, and a minimum of 10^9–10^30 calls at n = 100. Oink cannot even represent MPG/SSG inputs.
- **Using #104 to speed up parity games.** Parity is already quasipolynomial (Calude et al., in Oink as QPT/SSPM/ZLKQ), and those are themselves slower than Zielonka/FPI on practical games per Oink's documentation.
- **A Barnette Hamiltonian-cycle *algorithm* (#180).** Existence only. The paper says outright that it gives no polynomial-time construction.
- **Changing MetaRocq/Lean/Agda trust bases on account of #245.** Wrong calculus (they are not PTS), wrong reduction (βη, ι, δ), and they do not assume WN.
- **h = 21 on 251 cells as a "hard but solvable" QBF.** At 32,622 variables and 21 quantifier blocks (|T| = 251, 1,419 Snaky copies), it is far beyond current QBF solvers, which already fail at 15 free cells. Useful only as an aspirational TRUE instance.

## Experiment results

All code, data and logs: `/home/claude/work/repos/scratch_solvers_logic/`.

### E1 (#235). Exact hitting times H_n for random 3-SAT (proper clauses, with replacement: the paper's model)
**Method.** For each instance I draw 8n clauses and find H_n exactly by bisection with model-guided jumps: a SAT model at prefix m certifies SAT up to its first falsified clause. Engines: `minisat22` via PySAT for n ≤ 100; march (look-ahead, built from [marijnheule/march-SAT-solver @ b5c365a](https://github.com/marijnheule/march-SAT-solver), with `-fgnu89-inline -fcommon` build flags) for n ≥ 150. Every SAT model is verified against the prefix.
- Cross-check: CaDiCaL, Glucose and MiniSat give identical H on shared seeds.
- Cost: about 0.03 s per sample at n = 100, 0.25 s at 200, 7 s at 250, 26 s at 300, and **~1000 s at n = 400**, where I stopped (one sample).

| n | N | E[H]/n | 50% point α | sd(H) | sd/√n | 10–90% width (clauses) | width/√n |
|---|---|---|---|---|---|---|---|
| 50 | 4000 | 4.396 | 4.360 | 18.07 ± 0.23 | 2.56 | 46 | 6.5 |
| 100 | 3000 | 4.309 | 4.290 | 22.81 ± 0.36 | 2.28 | 58 | 5.8 |
| 150 | 2000 | 4.287 | 4.273 | 26.46 ± 0.48 | 2.16 | 66 | 5.4 |
| 200 | 2000 | 4.277 | 4.270 | 29.44 ± 0.51 | 2.08 | 76 | 5.4 |
| 250 | 600 | 4.277 | 4.268 | 31.4 ± 0.9 | 1.99 | 83 | 5.2 |
| 300 | 210 | 4.261 | 4.253 | 30.7 ± 1.6 | 1.77 | 76 | 4.4 |

Total: 11,811 exact samples. n = 400 costs about 1000 s per sample with march and was dropped.

- **Weighted power-law fit:** Var(H) ∝ n^{0.684 ± 0.025}, so sd ∝ n^{0.342} and the density window ∝ n^{−0.66}. That gives **ν_eff = 1.52**, exactly the Kirkpatrick–Selman value. sd/√n is still *falling* at n = 300; under ν = 2 asymptotics it must eventually level off.
- **Two-term fit** Var = c₁n + c₂n^{2/3}: c₁ = 0.18 ± 0.38, c₂ = 23.5 ± 1.8. The Θ(n) term the theorem guarantees is real asymptotically but **numerically small**, and a global fit cannot resolve it at n ≤ 300. The direct regression estimate below (c₁ ≈ 1.2) is better.
- **Mechanism check.** I replayed every instance and regressed H on extensive "disorder" statistics of the prefix at m = 4.267n: literal-sign imbalance Σ_v (pos_v − neg_v)², degree moments, low-degree counts. These fluctuate on the √n scale, so they carry the Wilson/ν = 2 component.
  - Cross-validated R² is 0.19 to 0.37, rising with n.
  - The variance they explain is ≈ 1.1–1.3 × n at every n. That is a **genuinely linear-in-n component**, as the theorem says.
  - The residual ("intrinsic") variance ∝ n^{2/3} carries the rest at these sizes.
  - Sign imbalance alone predicts SAT vs UNSAT at the 50% point with AUC 0.705 (n = 50) to 0.748 (n = 250).

  So the √n-scale disorder contribution is real and measurable. But its coefficient (≈ 1.2 n) is ~20× smaller than the n^{2/3} term until n is in the thousands.

  The regression captures the Wilson component directly, while the two-term fit cannot resolve the linear term at these n. The direct estimate is the more trustworthy of the two. Taking Var = 1.16n + 27.6n^{0.584} (linear part from the regression, residual fitted), the model's effective ν is:

  | n | Linear share of Var | ν_eff |
  |---|---|---|
  | 300 | 31% | 1.55 |
  | 10³ | 43% | 1.62 |
  | 10⁴ | 66% | 1.75 |
  | 10⁵ | 83% | 1.87 |
  | 10⁶ | 93% | 1.94 |

  So the theorem's ν = 2 is approached only logarithmically slowly. Practice at n ≤ 10³ sees ν ≈ 1.5–1.6. This extrapolation assumes the residual keeps its fitted power law; treat it as indicative.

### E2 (#187). Snaky QBF
Certificate verified in 0.3 s. Card ladder encoded, results in the table under solvers_logic-1. CAQE 4.0.1 with Bloqqer solves h ≤ 7 (13 free cells) in ≤ 17 s and times out at h = 8, 9 (150 s). Card 290 is winnable in 6 moves, not the certified 7. Q-sage `bwnib` Snaky instances (7×7 at depths 9 and 11; 17×17 at depth 41) time out at 100–300 s.

### E3 (#180). Barnette graphs vs LKH
Results in the table under solvers_logic-2. All flag-graph instances verified cubic, bipartite, planar and 3-connected (networkx `node_connectivity`).

### E4 (#104). Label prototype
12/12 correct against brute force on n ≤ 4. Call counts 4.6×10³ – 3.8×10⁵. The analytic minimum-call model gives 5×10⁹ calls at n = 100, W = 1, and 9×10³⁰ at W = 2^62. Paper bound at n = 100: about 10^272. (`mpg_calls.out`)

## Sources
- Wilson, *On the critical exponents of random k-SAT*, RSA 2002: https://arxiv.org/abs/math/0005136v2
- Leone, Ricci-Tersenghi, Zecchina, *Phase coexistence and finite-size scaling in random combinatorial problems*, 2001: https://arxiv.org/abs/cond-mat/0103200
- Pázmándi, Scalettar, Zimányi, *Revisiting the theory of finite size scaling in disordered systems*, 1997: https://arxiv.org/abs/cond-mat/9704155
- Lee, Ha, Jeon, Jeong, *Finite-size scaling in random K-SAT problems*, PRE 2010: https://arxiv.org/abs/1005.0251
- SATLIB uniform random 3-SAT: https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/RND3SAT/descr.html
- CNFgen RandomKCNF: https://github.com/MassimoLauria/cnfgen/blob/24e633bdbed0d0998493bee99c42faf480c7dc96/cnfgen/families/randomformulas.py#L82-L88
- Shaik, Mayer-Eichberger, van de Pol, Saffidine, *Implicit State and Goals in QBF Encodings for Positional Games*, 2023: https://arxiv.org/pdf/2301.07345 ; Q-sage: https://github.com/irfansha/Q-sage (commit 08177212dbca5605f84c86d702fc06e4ecce5cc8)
- QBF Gallery 2026: https://qbf.pages.sai.jku.at/gallery26/ ; QBF Gallery 2023 report: https://arxiv.org/abs/2604.16153
- Oink: https://github.com/trolando/oink (commit 8fbf0a7c3e5b0baa254cb4516258c5c42fa99db1)
- Fijalkow, Gawrychowski, Ohlmann, *The complexity of mean payoff games using universal graphs*: https://arxiv.org/pdf/1812.07072
- Křetínský, Ramneantu, Slivinskiy, Weininger, *Comparison of algorithms for simple stochastic games*: https://arxiv.org/abs/2008.09465
- Barnette's conjecture computational status (Mohar): https://users.fmf.uni-lj.si/mohar/Problems/P4BarnetteConjecture.html ; Wikipedia: https://en.wikipedia.org/wiki/Barnette%27s_conjecture
- FHCP Challenge Set: https://ar5iv.arxiv.org/html/1902.10352
- plantri 4.5 mirror: https://github.com/mishun/plantri (commit 09745aeb09819bf200cfc77617f000258dba0a49)
- MetaRocq PCUICSN.v: https://github.com/MetaRocq/metarocq/blob/c8cd46054518193103c3bb33aa6e15c7f489e72c/pcuic/theories/PCUICSN.v#L12-L50 ; Sozeau et al., *Touring the MetaCoq project*: https://arxiv.org/pdf/2107.07670
- Abel & Coquand, *Failure of normalization in impredicative type theory with proof-irrelevant propositional equality*: https://arxiv.org/abs/1911.08174
- march SAT solver: https://github.com/marijnheule/march-SAT-solver (commit b5c365a2176a4480050bae92415c9c8c00bdf49b)
- OpenAI math drop: https://github.com/openai/math (commit fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb)

Note: the web-search budget was exhausted near the end. I could not re-verify Boufkhad et al. on regular/balanced random k-SAT, or whether any current generator documentation quotes ν explicitly; the claim that "no generator I checked quotes ν" rests on SATLIB and CNFgen only.
