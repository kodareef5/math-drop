# Verification: quantum / chem-bio / solvers rows (repo fd4aeeb)

Method: I checked each row against its primary sources before opening any theme write-up. These were the manuscript TeX under `preprints/*/build/` and the Lean comparator statements and solution modules. For the solution modules I wrote a transitive-import scanner (`deps.py` in the scratchpad) that looks for `sorry`, `admit`, `axiom`, `native_decide` and `implemented_by`. I also used the cited arXiv papers (via WebFetch, since direct arXiv downloads were blocked by the proxy) and fresh clones in `/home/claude/work/verify_repos/` (CatalystNetworkAnalysis.jl and Catalyst.jl at the pinned SHAs, mishun/plantri at 09745ae, toqito at 4baf22e). I ran code where I could: the Snaky verifier, my own brute-force Maker-Breaker solver, and plantri, which I compiled and checked with networkx.

| id | status |
|---|---|
| qinfo-1 | confirmed |
| qinfo-5 | confirmed (one wording caveat) |
| qadvantage-1 | confirmed |
| qadvantage-5 | corrected |
| chemphysbio-1 | confirmed (minor nuance) |
| solvers_logic-1 | confirmed (QBF timings not reproduced) |
| solvers_logic-2 | corrected |

## qinfo-1: EPnI vacuum corollary discharges GSE Strong Conjecture 2 (confirmed)

- **TeX:** `00-introduction.tex` L13-36 (thm:epni) states the EPnI for finite-energy n-mode states with arbitrary internal entanglement. L34-51 (cor:thermal-attenuator) gives, for E_{eta,N_B}^{(x)n}, the bound S/n >= g(eta g^{-1}(S(rho)/n) + (1-eta)N_B), with the thermal input attaining it. `06-broadcast.tex` L53-63 says the N_B=0 case "supplies the finite-block vacuum-port inequality required from Strong Conjecture 2 in [GSE2007, App. A]". L28-151 gives the full converse plus achievability for 0 <= eta_C < eta_B, eta_B + eta_C <= 1.
- **GSE 2007 (0706.3416):** Strong Conjecture 2 has "input modes a in their vacuum states, the entropy of b is ng(K) ... product thermal minimizes output entropy", which is n-mode with a vacuum port. The converse ends with "completes proof of the converse, given that strong conjecture 2 is true." This is an exact match.
- **WHG PRA 86 062306 (1105.0119):** The paper says the region is "optimal whenever eta >= 1/2 provided that a longstanding minimum output entropy conjecture is true". Sec. III G says "both proofs require Strong Conjecture 2 from Refs. [24,25]", and it notes "Strong Conjecture 2 holds if the entropy photon-number inequality is true". The thermal and amplifier sections are achievable regions only, so the row correctly limits unconditionality to pure loss with eta > 1/2. The PRL (1206.4886) says "If eta >= 1/2 and the minimum-output entropy conjecture is true, then ... capacity region".
- **De Palma 2019 (1805.12469):** Conjecture 1 is stated for E^{(x)n}_{eta,E} of identical one-mode attenuators. Sec. VI ("Assuming Conjecture 1 for the quantum-limited attenuator, the capacity region ... coincides with (60)") uses E^{(x)n}_{(1-eta)/eta}, which is exactly the corollary's setting. Sec. VII / Cor. 12 are conditional in the same way.
- **Lean:** The `EntropyPhotonNumber.lean` comparator (L99-106) is the EPnI with untruncated Fock space, finite energy, and gInv. The solution `OAI.InformationTheory.PhotonNumber.Inequality` has 26 modules, all clean. `lean/docs/273.md` says "The thermal-attenuator minimum-output-entropy and broadcast-capacity consequences in the paper are outside this selected inequality." The row says only that "the EPnI itself is Lean-checked", which is accurate.
- **Not checked:** the "very likely Guha m-receiver" claim (MIT thesis, hedged in the row) and the Khatri-Wilde wording.

## qinfo-5: 272 disproves PPT², answers OQP #24 within its protocol model (confirmed, one caveat)

- **TeX** (`introduction.tex` L45-105):
  - thm:main-state: an explicit entangled rho on C^10 (x) C^10 with no product vector in its range, K_D(rho)=0, and an unhalved trace-norm gap >= 1/5 (halved, 1/10) for every admitted completed bit protocol.
  - thm:main-pair: PPT maps Phi1, Phi2 on M_10 whose composition is not EB, refuting CMHW2019 Conj. IV.1.
  - thm:main-channel: a trace-preserving PPT channel Theta on M_21 with Theta∘Theta not EB, answering BIRS 2012 Problem G.
  - L107-113: dimensions are not claimed minimal.
- **Lean:** `DimensionTenChannel.lean` L45-49 (`exists_channel_fin21`: PPT, TracePreserving, ¬EntanglementBreaking(Θ∘Θ)) and `DimensionTenPair.lean` L112-120 (`main_pair`: explicit phiOne/phiTwo, PPT, Z ≠ 0, no product vector in the range, not EB). The solution modules (148 and 129 modules) are clean.
- **Caveat:** the K_D=0 / 1/10-gap statement is not Lean-checked. docs/272.md: "The paper's zero-distillable-secret-key statement is outside these two selected Comparator statements." The row's "both Lean comparator-checked" refers to the two PPT² forms, which is correct, but a reader could think the OQP #24 answer is formal.
- **OQP pages:**
  - The list shows #13 MUBs, #24 "Secret key from all entangled states" and #38 "The PPT-squared conjecture".
  - #24's model is "(finitely many) rounds of local operations and public communication" with Eve overhearing. 272's admitted model includes "ordinary finite protocols", so the answer is negative within its model, as the row says.
  - #38 is stated only in the state form: sigma_AD after a yes/no POVM on BC of two PPT states is separable. The Choi/entanglement-swapping refutation is standard (Choi states of Phi1 and Phi2 plus a projection onto the maximally entangled state give J(Phi2∘Phi1) up to transposes), but the paper never cites OQP #38. That step is the row's inference.
- **266 status line:** The catalogue headline is "Proves N(6)=3". docs/266.md says the Lean proves only "at most five members". The 266 TeX `execution.tex` refers to a `verification/code/` directory (seed.cpp, covout.cpp, stageB/C.cpp) that is not in the drop (find returns nothing). The row's status line is accurate.
- **toqito:** `mutually_unbiased_basis.py` L56-65 @4baf22e raises ValueError for non-prime-power d. Confirmed.

## qadvantage-1: Max-Cut hardness via deterministic classical reduction, so a quantum ratio above alpha_GW implies NP ⊆ BQP (confirmed)

- **TeX:** thm:main (L39-42) states that for every fixed alpha in (alpha_GW, 1] approximation is NP-hard on simple unweighted graphs. thm:gap (L52-61) is the YES/NO gap (1+t)/2 - eps vs (1+B(t))/2 + eps.
- **Determinism:** `conclusion.tex` L40-55 says "the test is a deterministic polynomial-size graph construction ... computable in deterministic polynomial time". `preliminaries.tex` L163-164 says prop:affine-games is "deterministic and has polynomial running time". `affine_games.tex` L570 says "deterministic polynomial reduction". `unweighted.tex` L17/L28 describes a deterministic conversion (deterministic prime search). The randomized labelers in `decoding.tex` are analysis only, and L361-365 fixes the shared randomness.
- **Lean:** The `OptimalMaxCut.lean` comparator L133-149 is a GapReduction with `Turing.TM2ComputableInPolyTime` from binary 3SAT, noBound < alpha*yesBound, and completeness/soundness. The solution `OAI.Computability.MaxCut.Main` has 372 modules, all clean. The UG theorem comparator also uses TM2ComputableInPolyTime, and its solution (478 modules) is clean, which supports the row's Raghavendra/CSP extension.
- **Logic:** A Karp reduction composed with a BQP algorithm for the gap problem decides 3SAT in BQP. An algorithm whose worst-case ratio is >= alpha with bounded error, or whose expected ratio is >= alpha' > alpha_GW, gives the gap decision after Markov plus repetition and choosing t, eps so that the gap fits between alpha_GW and alpha'. So NP ⊆ BQP. The reduction blows up to |X|^T 2^{2^{(n+1)T}} vertices, which is polynomial but galactic. That does not affect the implication.

## qadvantage-5: Companion makes EAMS unconditional, so the Basso et al. "QAOA beats unconditional classical" claim is obsolete (corrected)

- **Confirmed core:** The companion `algorithm-application.tex` L13-35 cor:algorithm gives a randomized C(eps)n^2-operation algorithm with H_n(sigma) >= max - eps n w.h.p. Its proof says "Theorem full-support gives a strictly increasing minimizer in U, exactly the no-overlap-gap hypothesis in [EAMS2021, Assumption 2]". EAMS Assumption 2 is "exists gamma_* in U strictly increasing in [0,1)" with Cor. 2.2 / Thm. 3 complexity C(eps)(chi+N) + N chi_1. Lean (`SKFullSupport`, 135 modules, clean) proves full support conditional on a minimizer; docs/281.md says it is "conditional on the order parameter being a minimizer". The QAOA thm:main L111-119 and the L131-133 disclaimer ("no quantitative finite-size estimate, depth bound, or efficient procedure for choosing the angles") match the row.
- **Correction 1 (wrong model):** In Basso-Farhi-Marwaha-Villalonga-Zhou (2110.14206), "p=11 QAOA beats all classical algorithms (known to the authors) that are free of unproven conjectures" is about Max-Cut on large-girth D-regular graphs (nu_11 = 0.6408 vs the 2/pi ≈ 0.6366 benchmark), not SK. The algorithm they set aside is El Alaoui-Montanari-Sellke, footnoted with "assuming ... no overlap gap". The regular-graph algorithm (EAMS 2023 RSA, 2111.06813) has Thm 1.7 "If Assumption 1 holds" with Assumption 1 "gamma_* strictly increasing", which is the same zero-temperature fact. So the claim is now obsolete for regular graphs too, but by inference: 281's companion only invokes the SK theorem EAMS2021.
- **Correction 2 (priority):** Montanari 2019 (1812.10897) assumes a positive-temperature interval support (Assumption 1, beta > beta_0). Lopatto (2607.11756, Jul 2026) settled that, as the QAOA paper's own positive-temperature route notes. Chen (2607.18032, submitted Jul 20 2026) proved zero-temperature full support before the Sep 27 companion, which itself cites "Chen [Thm 1.3] proves the same". The SK optimizer was therefore already unconditional by Chen/Lopatto; 281's companion is an independent reproof. Write "Chen 2026 (and independently 281's companion)".
- **Not checked:** the SA experiment (3 s at n=1000 matching p≈240) and the QOKit file lines.

## chemphysbio-1: Weakly reversible mass-action is bounded and persistent; CatalystNetworkAnalysis gaps (confirmed)

- **TeX:** The 149 boundedness paper `01-introduction.tex` L40-53 thm:main covers finite C, weakly reversible R, and positive constant rates. Every positive x0 has a global solution and an eps in (0,1) with eps <= x_i(t) <= 1/eps; "every positive trajectory is bounded and persistent". The permanence paper `introduction.tex` L43-60 is the classwise version with a compact convex absorbing K_P and is unformalized; catalogue family 149 is marked lean=true, with the Lean doc covering only the boundedness paper. `03-dynamics.tex` L437-461 rem:complex-balanced-convergence covers GAC for complex-balanced systems and deficiency-zero weakly reversible networks.
- **Lean:** `Main.lean` L73-84 `global_bounded_persistent_solution` matches the comparator `MassAction.lean`, where WeaklyReversible is TransGen reachability per reaction and the rates are constants κ: Reaction → ℝ. The solution has 71 modules, all clean. There is no linkage-class or deficiency restriction.
- **Code (fresh clone, HEAD = cac50dd89b5f...):**
  - `src/persistence.jl` L1-4 has the TODO list ("endotactic networks / permanence in networks / ...").
  - L24-37 `ispersistent`: if conservative, all non-critical siphons give `:PERSISTENT` and not-consistent gives `:NOT_PERSISTENT`; otherwise it returns `:INCONCLUSIVE`. The row says "only implements the Angeli-De Leenheer-Sontag siphon test", which is accurate in substance; there is also a consistency branch.
  - `test/persistence.jl` L65-76 is a conservative weakly reversible two-cycle network (2A+B<->C<->A+2B<->D<->2A+B) for which the test expects `:INCONCLUSIVE`, although thm:main says it is persistent.
  - `src/steadystates.jl` L116-117: the `:NOT_PERSISTENT` branch prints "This reaction network is persistent. It possess steady states ...". The bug is confirmed.
  - Catalyst.jl @e916278: the `isweaklyreversible` docstring builds `sir` but calls `subnetworks(rn)` (confirmed). The `crn_theory.md` deficiency-zero section says only "asymptotically stable" (confirmed). `ismassaction` returns false on iv-dependence (confirmed).
- **Not checked:** the "15.6% of random WR networks" statistic.

## solvers_logic-1: Snaky certificate cards as known-truth QBF instances (confirmed)

- I ran `python3 -I -B verification/verify_certificate.py`. Output: `{"status":"PASS","certificate_sha256":"3fa12d36a6d4dbb185e3f2808c8dfde13d85ee309afbca030d6ad17ae9fe3d04","numbered_cards":728,"final_support_cells":251,"final_height":21,...}` in 0.15 s. The certificate has 722 lines (cards 6..727 plus the six bases, 728 in total).
- **Format:** each line has the form `j pivot child...`. A child is `k:sUV` (a signed permutation s plus a translation UV over the alphabet 0-G) or a parenthesized subexpression. The cards combine as T = {p} ∪ ⋃T_i, A = (⋃A_i ∪ ⋂T_i) \ {p}, h = 1 + max h_i (templates.tex lem:combination).
- **Semantics** (templates.tex def:claim): (A,T,h) is valid if, at any position with Maker to move, A ⊆ M and B ∩ T = ∅, Maker wins within h further moves. Lean has a per-card `row_works_j : Template HasSnaky h required_j envelope_j` (1626 row_works theorems), where Template means ∀ M B disjoint, A ⊆ M, B ∩ H = ∅ → WinsIn h. The solution has 94 modules, all clean. Lean's `required_290` matches my parsed A(290).
- **Independent check:** I wrote a memoized minimax over the cells of T only, with only those snake placements contained in T as targets. Breaker moves outside T are irrelevant because the game is monotone.

  | card | h | free cells | TRUE at h | TRUE at h-1 |
  |---|---|---|---|---|
  | 0 | 1 | 1 | yes | no |
  | 6 | 2 | 3 | yes | no |
  | 7, 8 | 3 | 7 | yes | no |
  | 10, 50 | 4 | 9 | yes | no |
  | 16, 20 | 3 | 5 | yes | no |
  | 30, 40 | 2 | 3 | yes | no |
  | 60 | 4 | 7 | yes | no |
  | 100 | 5 | 11 | yes | yes |
  | 290 | 7 | 13 | yes | yes |

  Card 290's h-1 result matches the row. So heights are upper bounds, and "querying h-1 gives unknown-truth instances" is correct. Free-cell ranges per height are wide (h=8: 15..42), so "h=8 (15 free cells)" refers to the smallest h=8 cards.
- **Not reproduced:** the Bloqqer/CAQE timings (no QBF solver is installed).

## solvers_logic-2: Barnette proved; plantri -bd generates the class (corrected)

- **TeX:** `paper.tex` L79-82 thm:main: "Every finite simple undirected graph that is cubic, bipartite, planar, and 3-vertex-connected has a Hamiltonian cycle."
- **Lean:** `BarnetteHamiltonian.lean` MainStatement uses IsRegularOfDegree 3, IsBipartite, topological `Planar` (PlaneEmbedding into ℝ² with Path arcs), ThreeVertexConnected (>= 4 vertices, connected after deleting any <= 2 vertices) and HasHamiltonianCycle (a single spanning cycle). `Main.lean` L47 `theorem main`; the solution has 31 modules, all clean.
- **plantri** (mishun mirror 09745ae, v4.5): plantri-guide L346-352 says "-b but not -p: Select eulerian triangulations ... -c3 (default) 3-connected eulerian planar triangulation. The dual is a 3-connected bipartite cubic graph." L297 says "-d causes the dual graph to be written". L196-201 says n triangulation vertices give a dual with 2n-4 vertices. I compiled it: `plantri -bd -g 14` produced 32 graphs on 24 vertices and `-bd 16` produced 185 graphs on 28 vertices. networkx confirms all are cubic, bipartite, planar and 3-connected, and a DFS found a Hamiltonian cycle in all 217.
- **Correction 1:** "before, only orders up to ~84 had been checked" is out of date. Brinkmann-Goedgebeur-McKay (arXiv 2101.00943) state "Barnette's conjecture is true up to at least 90 vertices", using plantri plus cubhamg and about 37 CPU-years. Aldred-Brinkmann-McKay had reached 84.
- **Correction 2:** "plantri -bd generates them exhaustively up to 124 vertices" confuses the MAXN=64 compile limit (64 triangulation vertices give a 124-vertex dual) with feasible exhaustive generation. Counts of `plantri -bu n` for n = 12..24 are 8, 32, 185, 1543, 15374, 171168, 2024119 (about 10x per step). Exhaustive generation is hopeless far below 124 vertices, which is why BGM stopped at 90. 124-vertex instances must be res/mod slices or random samples. This does not invalidate the benchmark idea.
- **Not checked:** the LKH failure rates and the flag-graph construction.
