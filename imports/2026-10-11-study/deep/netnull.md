# Degree-preserving null models: switch-chain mixing (131), contingency tables (115), exact Ramanujan test (178)

**Bottom line.** Pursue now:

- A small correctness patch to NetworkX, submitted by a human contributor.
- Two bug reports: graph-tool and bctpy.
- A "certified burn-in" helper for vegan's curveball null model.

Do not pursue: anything from 115, the 178 construction, or using 131's bounds as defaults.

I recomputed the stationary law of each library's chain exactly, as implemented, and ran the actual library code (chi-square tests) to check:

- **Not uniform:** NetworkX `double_edge_swap` and `random_reference`, which feed `rich_club_coefficient(normalized=True)` (on by default), `sigma` and `omega`. Also bctpy `randmio_und`, vegan `swap`, vegan `quasiswap` at its default `thin=1`, and graph-tool `random_rewire(persist=True)`. The last one also never terminates on any graph that has an unswitchable edge, for example one with a vertex adjacent to all others.
- **Exactly uniform:** igraph `rewire`, NetworKit `EdgeSwitching`/`Curveball`/`GlobalCurveball`, graph-tool's default `random_rewire`, and vegan `tswap`/`curveball`.

The underlying principle (rejected switches must count as holding steps) is old and widely published. What is new is this library-by-library audit. The practical bias on real graphs is small: it shifts any null mean by at most 0.03 null SDs on the graphs tested. This is a correctness fix, not a result-changing one.

131's Lean-checked spectral bounds sit 10^5–10^20× above the usual 10m–100m swap budgets once m ≥ 10^4. They neither justify nor contradict those defaults. Their real practical value is cheap *certified* budgets for small instances, especially Curveball:

- On an ecology matrix (sipoo), a certified curveball burn-in takes 30 ms.
- vegan's defaults give NODF z-scores with run-to-run SD 1.05, against 0.16 with the certified budget.

## What the papers actually prove

### Family 131 — switch chain, every graphical degree sequence (Lean-formalized top line)

**Main result** ([Thm 1.1](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/introduction.tex#L32-L39)). The theorem covers a *lazy* chain: hold with probability 1/2, pick a uniform 4-set, then pick one of 6 ordered matching pairs, with rejections held. For that chain:

- t_mix(1/4) ≤ 2n^8.
- The spectral gap is ≥ 1/(24 n² C(n,4)).

This is Lean-checked with no `sorry` or `axiom` under `lean/OAI/Probability/SwitchChain*`: [Main.lean L18-L33](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/SwitchChain/Main.lean#L18-L33).

**Constructive?** Yes: the chain itself is the algorithm, and the constants are explicit. The exact sampler ([Cor. exact-sampling](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/introduction.tex#L42-L49)) is a different matter:

- It enumerates all 2^{C(n,2)} adjacency strings on a branch taken with probability 2^{-4B-10} ([exact-sampling.tex L40-L46, L100-L101](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/exact-sampling.tex#L40-L46)).
- Its polynomial running time holds only in expectation.
- It is not formalized.

**The intermediate inequalities that matter for practice** ([mixing.tex](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/mixing.tex#L92-L203)). Both are also Lean theorems:

- (a) **Cor. mix:poincare: Var(f) ≤ ⟨f,Hf⟩**, where H = Σ_a (I − E_a) sums the undirected Curveball pair resamplings over all vertex pairs. In Lean: [`uniformVariance_le_generator`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/SwitchChain/PairPoincare.lean#L29-L73).
  - The Curveball chain that picks a uniform random pair has P = I − H/C(n,2).
  - **So its gap is ≥ 1/C(n,2).** This is an immediate corollary that the paper does not state.
- (b) **Lemma mix:comparison and eq. mix:L-poincare: Var(f) ≤ 2n²⟨f,Lf⟩**, where L is the unnormalized switch-graph Laplacian. In Lean: [`generator_energy_le_switchLaplacian_unconditional`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/SwitchChain/PairComparisonEndpoint.lean#L12-L18).
  - Any chain that gives every valid switch the same probability c per attempt and holds on rejection has gap ≥ c/(2n²).
  - For igraph, c = 1/(m(m−1)). For degree-weighted node draws (NetworKit, NetworkX-style), c = 1/m².

**Sharpened constant (my derivation, not in the paper).** The paper bounds h_a ≤ n²J_a by a path argument ([L146, L176-L177](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/mixing.tex#L143-L177)). The bound can be tightened:

- On a q-subset slice of N labels, the transposition Laplacian J_a has spectral gap exactly N (the Johnson-scheme eigenvalues are j(N+1−j)).
- So h_a ≤ J_a/N ≤ J_a/2, which gives **H ≤ L and Var(f) ≤ ⟨f,Lf⟩** — a factor 2n² better.
- I checked L − H ⪰ 0 numerically on 8 degree sequences (minimum eigenvalue 0 up to rounding).
- It still needs a written proof.

**How loose the bounds are, on exact small cases:**

| Quantity | Exact | Paper bound | Paper is loose by |
|---|---|---|---|
| gap(L), 11 sequences with n ≤ 8 | 4.6–11.8 | 1/(2n²) | 380–1500× |
| gap(L), same sequences | 4.6–11.8 | Sharpened bound: 1 | 5–12× |
| Curveball gap | 0.12–0.33 | 1/C(n,2) = 0.036–0.067 | 3–5× |

**Scope.** The theorem covers simple undirected graphs only. It does *not* cover:

- the connected-graph state space (`connectivity=True`, `connected_double_edge_swap`);
- directed graphs;
- multigraphs;
- `GlobalCurveball`, whose pairs trade simultaneously over a random matching.

The bipartite / 0-1 matrix case is **Fu–Qin–Wang 2026** ([arXiv:2606.22636](https://arxiv.org/abs/2606.22636)). It is an external preprint, not part of this drop, and its abstract says the proof was generated by ChatGPT 5.5 Pro. Its bounds:

- swap-chain gap ≥ [C(r,2)C(c,2)]^{-1};
- row-pair Curveball gap ≥ 1/C(r,2).

131 re-proves FQW's three-row variance inequality, and that inequality is Lean-checked: [`row_variance_bound`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/SwitchChain/RowVarianceAssembly.lean#L103). The full bipartite theorem is not in this drop's Lean.

**Triage check.** The triage's numbers reproduce exactly:

- Its four sequences give TV 0.0250 / 0.0284 / 0.0293 / 0.0232 and ratios 1.43 / 1.25 / 1.52 / 1.50.
- Its rescalings (gap ≥ 1/(2n²m²) for NetworkX-style draws, and Curveball ≥ 1/C(n,2)) are correct.

The triage was wrong to label the bipartite case "FQW26/115". 115 concerns integer tables; the 0-1 case is FQW26 alone.

### Family 115 — contingency tables with arbitrary margins (Lean-formalized)

- **[Thm main](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/introduction.tex#L18-L32):** uniform sampling of nonnegative *integer* tables, poly(m, n, log N), in two forms:
  - exact, in expected time;
  - 2^{-k}-approximate, on every run.
- **The chain analysed is an auxiliary one.** It runs on a padded "small-cell" state space, weighted by completion counts ([Prop. small-chain](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/algorithms.tex#L51-L66), inverse gap ≤ d^160). It is not the 2×2 ±1 swap or Diaconis–Gangolli chain that people run.
- **Constants are galactic:**
  - d = 10+(m+1)(n+1), L = d^12, U = d^20 ([model-and-graph.tex L16-L20](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/model-and-graph.tex#L16-L20)).
  - T = d^200(k+b)² steps ([L105-L107](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/algorithms.tex#L105-L107)), so a 2×2 table already needs more than 10^256 steps.
  - Exact correction costs 2^{500db} ([L221-L225](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/algorithms.tex#L221-L225)).
  - The FPRAS companion uses H = O(L^11 ε^{-2}) ([algorithm.tex L534](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-FPRAS-for-Cell-Bounded-Contingency-Tables-September-24-2026/build/sections/algorithm.tex#L534)), and the paper itself calls its bounds "deliberately generous".
- The triage was right: T3, galactic.

### Family 178 — deterministic nonbipartite Ramanujan graphs (not formalized)

- **[Thm main](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Deterministic-nonbipartite-Ramanujan-graphs-in-every-fixed-degree-September-23-2026/build/sections/introduction.tex#L24-L34):** there are constants n_0(d), k_d with no explicit values. The scales use a = 10^{-4} ([setup.tex L55](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Deterministic-nonbipartite-Ramanujan-graphs-in-every-fixed-degree-September-23-2026/build/sections/setup.tex#L55)), so this is galactic.
- **The only practical by-product** is the exact certificate ([algorithm.tex L99-L116](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Deterministic-nonbipartite-Ramanujan-graphs-in-every-fixed-degree-September-23-2026/build/sections/algorithm.tex#L99-L116)):
  - With B = [e_i − e_n], test B^T(4(d−1)I − A²)B ≻ 0 by exact rational inertia.
  - This is classical Sylvester-inertia linear algebra, not a new idea.

## Current practice and state of the art

- **Counting rejections is long-known to be necessary for uniformity:**
  - Milo et al. count failed switches "to insure detailed balance" and suggest Q·m switches with Q = 100 ([cond-mat/0312028](https://arxiv.org/abs/cond-mat/0312028)).
  - Carstens & Horadam 2017 (Ex. 2.2–2.3, Def. 2.5) show that the chain which skips rejections is biased, and prescribe 1/M per switch plus a self-loop ([J. Complex Netw. 5(3)](https://doi.org/10.1093/comnet/cnw027)).
  - Fosdick, Larremore, Nishimura & Ugander 2018 build "swap and hold" into their algorithm (§2.3, Alg. 1). They give no software audit, and say mixing time is open, recommending diagnostics instead (§2.5) ([arXiv:1608.00607](https://arxiv.org/abs/1608.00607)).
  - Coolen et al. call the bias "mobility" ([arXiv:1203.0877](https://arxiv.org/abs/1203.0877)).
  - vegan's own docs say Miklós & Podani found ordinary swap biased ([commsim.Rd L126-L132](https://github.com/vegandevs/vegan/blob/a574546bee7a03f7ea034fe259dd42818eea43ac/man/commsim.Rd#L118-L155)).
  - I did not verify Artzy-Randrup & Stone 2005 or Rao–Jana–Bandyopadhyay 1996; see the search limits below.
- **Libraries that already do it right, and say why:**
  - igraph's C loop comments that it counts unsuccessful trials "for uniform sampling" ([rewire.c L74-L187](https://github.com/igraph/igraph/blob/912f99d59134a70ebe26eafe804a7af62d4868d4/src/operators/rewire.c#L74-L187)).
  - The NetworKit header cites Carstens–Horadam ([EdgeSwitching.hpp L21-L50](https://github.com/networkit/networkit/blob/5f03e17cec0918add08f0f7c00c103ee0119da5b/include/networkit/randomization/EdgeSwitching.hpp#L21-L50)).
- **Budgets people use:**

  | Library / function | Default budget |
  |---|---|
  | igraph Python `rewire` | 10m trials |
  | igraph C `degree_sequence_game` edge-switching | 10m trials ([degree_sequence.c L712-L722](https://github.com/igraph/igraph/blob/912f99d59134a70ebe26eafe804a7af62d4868d4/src/games/degree_sequence.c#L712-L722)) |
  | **R igraph `keeping_degseq`** | **100 trials total** ([rewire.R L77-L83](https://github.com/igraph/rigraph/blob/b4a4d3381d5a37e2d4678c6bc29319fd1bd1351a/R/rewire.R#L77-L83)) |
  | NetworKit `EdgeSwitching` | 10 per edge |
  | NetworKit `GlobalCurveball` | 20 global rounds |
  | graph-tool `random_rewire` | 10 sweeps |
  | NetworkX `rich_club_coefficient` | Q = 100 successful swaps per edge |
  | NetworkX `random_reference` | `niter=1` |
  | NetworkX `sigma` / `omega` | niter = 100 / 10 |
  | vegan `oecosimu` / `permatswap` | burnin = 0, thin = 1 |

  A 2024 tool comparison recommends about 100m and warns that igraph's default trial count is too low ([arXiv:2405.05400](https://arxiv.org/abs/2405.05400)).
- **Ramanujan practice:** random regular graphs are Ramanujan with probability about 0.69 (Huang–McKenzie–Yau, cited in 178's intro). NetworkX samples and then checks with a floating-point `eigsh` ([expanders.py L359-L502](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/generators/expanders.py#L359-L502)).

**Search limits (disclosed).** The shared WebSearch budget ran out after three queries. The NetworkX and igraph issue trackers could not be searched: GitHub HTML is robots-blocked and the API is restricted to this session's repositories.

As a fallback I scanned about 3,000 recent NetworkX commits ([`git log`](https://github.com/networkx/networkx/commits/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985)). None mentions uniformity or rejection counting for `swap.py` or `smallworld.py`. The 2022 "bug fix" commits 247231f0 and 9d5e11f2 only touched argument checks.

**Someone must search the issue tracker before filing.** NetworkX's AGENTS.md requires it.

## Q1 — which implementations are uniform? (exact kernels as implemented, plus the real code)

I wrote each library's per-step randomness exactly, from the pinned source, enumerated every labeled realization, and solved for the stationary law. Script: `kernels_as_implemented.py`. Cells show exact TV from uniform, with the max/min probability ratio in parentheses.

| d (labeled realizations) | NX `double_edge_swap` | NX `random_reference` | igraph `rewire` | NetworKit `EdgeSwitching` | graph-tool (default) | graph-tool `persist=True` |
|---|---|---|---|---|---|---|
| 332222 (54) | 0.032 (1.27) | 0.012 (1.10) | 0 | 0 | 0 | **hangs** |
| 442222 (13) | 0.066 (2.00) | 0.022 (1.32) | 0 | 0 | 0 | 0.054 (1.80) |
| 333333 (70) | 0.057 (1.50) | 0.025 (1.21) | 0 | 0 | 0 | 0.039 (1.33) |
| 4333111 (30) | 0.078 (1.75) | 0.018 (1.16) | 0 | 0 | 0 | **hangs** |
| 2222222 (465) | 0.040 (1.24) | 0.028 (1.17) | 0 | 0 | 0 | 0.041 (1.24) |
| 63222221 (145) | 0.041 (1.50) | 0.010 (1.10) | 0 | 0 | 0 | **hangs** |

**Why each chain lands where it does:**

- **NetworkX `double_edge_swap`** ([L202-L228](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/algorithms/swap.py#L202-L228)):
  - `swapcount` only increments on success (L221), so the stationary law is π(G) ∝ deg_sw(G).
  - deg_sw(G) = 2P_disj − Σ_{uv∈E}(d_u−1)(d_v−1) + 3·triangles + 2·C4, a closed form I verified by brute force.
  - **The bias favors graphs with many triangles and 4-cycles and with low degree-degree product sums.**
  - Exhaustive over all 278 degree vectors on 7 vertices: max TV 0.078, max ratio 2.5.
- **NetworkX `random_reference`** ([L79-L117](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/algorithms/smallworld.py#L79-L117)):
  - It makes up to K = int(2m/(n−1)) attempts and `break`s at the first success (L115).
  - So π ∝ s/(1−(1−s)^K), with s = deg_sw/(2P_disj). This is exactly uniform only when K = 1 (verified).
  - **When K = 0 (average degree below about 1) it returns G unchanged:** n=1000, m=400 gave 0 edges changed.
- **igraph** counts every trial, with an ordered pair, a coin flip and rejections held. Its kernel is symmetric, so the law is uniform.
- **NetworKit** `EdgeSwitching` ([L26-L48](https://github.com/networkit/networkit/blob/5f03e17cec0918add08f0f7c00c103ee0119da5b/networkit/cpp/randomization/EdgeSwitching.cpp#L26-L48)) has a symmetric kernel. `Curveball` ([CurveballImpl.cpp L382-L511](https://github.com/networkit/networkit/blob/5f03e17cec0918add08f0f7c00c103ee0119da5b/networkit/cpp/randomization/CurveballImpl.cpp#L382-L511)) is an average of conditional-expectation projections, so it is reversible to uniform.
- **graph-tool** ([2.98 source](http://archive.ubuntu.com/ubuntu/pool/universe/g/graph-tool/graph-tool_2.98+ds.orig.tar.xz); git.skewed.de is blocked from here, so no permalink):
  - `src/graph/generation/graph_rewiring.hh` L276-L354 is the sweep loop, with `do{...}while(persist && !success)` at L339-L343. L505-L590 is the acceptance step, which has a = 0 for simple configuration.
  - The default `persist=False` holds on rejection, so it is uniform.
  - The exact table models single uniform-edge moves (`edge_sweep=False`). For the default `edge_sweep=True` (each edge visited once in a random order), I did not derive an exact kernel; edge-slot bookkeeping makes the symmetry argument non-trivial. The real-code chi-square tests do not reject uniformity (p = 0.76 and 0.57).
  - `persist=True` loops until the same edge succeeds. That is non-uniform, and it **loops forever** if that edge has no valid partner, which is true of every edge at a vertex of degree n−1.
  - I reproduced the hang on a 30-vertex graph with a universal vertex: no return in 60 s, while `persist=False` returns at once.
  - The docstring (`__init__.py` L618-L623) only warns of "many repeated attempts".
- **vegan** ([nestedness.c](https://github.com/vegandevs/vegan/blob/a574546bee7a03f7ea034fe259dd42818eea43ac/src/nestedness.c#L95-L327)):
  - `swap` (L220-L267) retries until it finds a checkerboard, so π ∝ #checkerboards. Exact TV 0.028–0.05 on 6 margin pairs.
  - `trialswap` (L165-L213) and `curveball` (L282-L327) are uniform.
  - `quasiswap` (L95-L159) starts from r2dtable and is absorbing. With `thin=1` its absorption law has TV 0.027–0.072 and ratio up to 2.36. With `thin=100` TV is ≤ 1e-5.
  - It is the default for `permatswap` and for `permatfull(mtype="prab")` ([permatfull.R L20](https://github.com/vegandevs/vegan/blob/a574546bee7a03f7ea034fe259dd42818eea43ac/R/permatfull.R#L20)).
  - The C kernels are identical in vegan 2.6-4, which is the installed CRAN version.
- **bctpy `randmio_und`** ([reference.py L1479-L1557](https://github.com/aestrivex/bctpy/blob/c28931c70222ab8d2ed78de29d47bff6c513f6ec/bct/algorithms/reference.py#L1479-L1557)) has the same stop-at-first-success pattern as `random_reference`. I did not inspect the MATLAB BCT original.

**Real-code confirmation.** I ran each pinned or installed library and recorded thinned states. Code: `confirm_actual_code.py`, `gt_check.py`, `vegan_actual.R`, `bct_check.py`, `rr_actual_check.py`. Chi-square p-values:

| Implementation | p vs uniform | p vs predicted biased law |
|---|---|---|
| NX `double_edge_swap` | ≈0 / 2e-127 | 0.47 / 0.62 |
| NX `random_reference` | 2e-47 / 1e-13 | 0.70 / 0.35 |
| bctpy `randmio_und` | 5e-34 / 4e-6 | 0.045 / 0.36 |
| graph-tool `persist=True` | 4e-254 | 0.80 |
| igraph `rewire` | 0.60 / 0.68 | — |
| NetworKit `EdgeSwitching` | 0.91 / 0.52 | — |
| NetworKit `GlobalCurveball` | 0.46 / 0.39 | — |
| NetworKit `Curveball` | 0.98 / 0.12 | — |
| graph-tool default (four configurations) | 0.43–0.80 | — |
| vegan `tswap` | 0.71 | — |
| vegan `curveball` | 0.86 | — |
| vegan `quasiswap(thin=100)` | 0.22 | — |
| vegan `swap` | 6e-174 | — |
| vegan `quasiswap(thin=1)` | ≈0 | — |
| NX `connected_double_edge_swap` | 0.98 / 0.12 | — |

`connected_double_edge_swap` counts every attempt and shows no bias at this resolution, but it is not proved uniform.

**How much it matters** (`practical_bias.py`, `cv_hard.py`):

- For any statistic, the shift of its null mean under the NetworkX law is at most CV(deg_sw) null SDs, by Cauchy–Schwarz.
- Measured CV(deg_sw) across 12 graphs ranges from 0.0004 (wheel) to 0.030 (karate). That set includes dense, hub-dominated and power-law graphs.
- Directly reweighting uniform samples gives z-score shifts of at most 0.029 SD on karate, and at most 0.01 SD on les_mis, Davis, BA(200) and power-law-cluster(500), for assortativity, transitivity, clustering and rich-club.
- **Conclusion:** the bias is real and fixable, but no published z-score is likely to change by more than a few hundredths of an SD. The worst cases are tiny or dense toy graphs.

## Q3 — the bounds as swap counts

Budgets are for TV ≤ 1/4, from the worst-case start, using log|Ω| ≤ log C(C(n,2), m). Code: `budgets.py`, `certified_small.py`; igraph runs about 1.2×10^6 attempts/s.

| Graph | Lean 4-set chain (steps) | igraph edge-pair, paper constant (per edge) | igraph, sharpened constant (per edge) | Undirected Curveball, certified (pair trades) | Defaults |
|---|---|---|---|---|---|
| karate (n=34, m=78) | 1.4e11 | 2.0e7 (22 min) | 8.6e3 (0.6 s) | 6.3e4 | 10–100 per edge |
| les_mis (77, 254) | — | 1.3e9 (3 days) | 1.1e5 (23 s) | 1.3e6 | 10–100 per edge |
| n=1e3, m=1e4 | 2.4e22 | 4.9e14 | 2.5e8 (23 days) | 1.2e10 (about 7 h in NetworKit) | 10–100 per edge; 20 global rounds |
| n=1e5, m=1e6 | 4.8e36 | 9.5e22 | 4.8e12 | 2.4e16 | 10–100 per edge |
| n=1e6, m=1e7 | 5.9e43 | 1.2e27 | 5.9e14 | 3.0e19 | 10–100 per edge |

**Verdict.** For m ≥ 10^4 the bounds say nothing useful about the 10m–100m defaults: they are 10^6–10^20× larger. They neither justify nor contradict those defaults, and should not be used to set them.

They are useful in two narrow places:

1. **Small graphs.** For m up to a few hundred, the sharpened edge-pair budget takes seconds.
2. **Curveball.**
   - The certified burn-in is affordable once, up to n ≈ 1000.
   - The certified decorrelation time is cheap: P = mean of projections is positive semidefinite, so every statistic's autocorrelation is ≤ (1 − 1/C(n,2))^t. That gives ρ ≤ 0.01 after C(n,2)·ln 100 trades, about 4.7 s at n = 1000.

**Some defaults are contradicted, by a separate lower-bound check, not by 131.** The fraction of original edges that survive should match its stationary value (`overlap_lb.py`):

| Run | Original edges retained, BA(2000) / power-law(2000) | Stationary value |
|---|---|---|
| R igraph default `keeping_degseq()` (100 trials total) | 95% / 98% | 1.2% / 1.9% |
| NetworkX `random_reference(niter=1)` | 14% / 15% | 1.2% / 1.9% |

Both defaults are clearly unmixed.

## Opportunities

### netnull-1 — NetworkX: count rejected swaps (correctness fix; pursue now via a human contributor)

**Proposed change.** The patch is drafted, tested and saved at `/home/claude/work/repos/scratch_netnull/networkx_count_rejected.patch`. It is applied, uncommitted, on branch `count-rejected-swaps` in `/home/claude/work/repos/networkx` (base 6da4704c).

1. **`double_edge_swap(..., *, count_rejected=False)`.**
   - The new keyword is backward compatible: the default is unchanged.
   - When True, a failed parallel-edge check still counts. This is the only code change:
     ```python
             swapcount += 1
     +   elif count_rejected:
     +       swapcount += 1  # a rejected attempt is a holding step of the chain
     ```
   - Degenerate draws (`ui == xi`, `v == y`) are still redrawn. Their probability is the same for every realization, Σ d_u²/(2m)² + Σ d_v(d_v−1)/(4m²), so the kernel stays symmetric (verified exactly).
   - The Notes section explains the bias and cites Carstens–Horadam, Havel and Fosdick et al.
2. **`random_reference`.** Replace "up to K attempts, stop at first success" with "one counted attempt per iteration, `niter·m` attempts". This also fixes the K = 0 no-op.
   - This is a **behavior change**: there are fewer successful swaps per `niter`, and seeded outputs change.
   - Maintainers may prefer a new `niter` default or a deprecation path.
   - `sigma` and `omega` ([L296-L298](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/algorithms/smallworld.py#L246-L298), L377-L386) inherit the fix.
3. **Follow-up PR (not in the patch): `rich_club_coefficient(normalized=True)`** ([richclub.py L103-L114](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/algorithms/richclub.py#L103-L114)) should pass `count_rejected=True`.
   - This changes seeded outputs, and `test_rich_club_zero_division_error` depends on the stream for seed 4. I tried the change and that test failed, so I kept it out of the first PR.
   - `Q` would become attempts per edge rather than successes.

**Verification.**

- Exact kernels of the patched `double_edge_swap` and `random_reference` are symmetric with TV = 0 on 5 and 4 sequences respectively.
- Patched real code on d = 442222: max/min ratio 1.08 against 2.01 unpatched.
- `random_reference` chi-square p = 0.80 / 0.79 / 0.10, the last with `connectivity=True`.
- 48 existing swap, smallworld and richclub tests pass, plus 2 new tests.

**Issue/PR content outline.** NetworkX policy forbids AI-written text in issues and PR descriptions and requires disclosure of AI tool use ([contribute.html](https://networkx.org/documentation/latest/developer/contribute.html)). A human must write the text in their own words; this outline is input to that.

- (i) Title: *`double_edge_swap` and `random_reference` do not sample uniformly: rejected swaps are not counted.*
- (ii) Mechanism: the loop at swap.py L202-L228 only counts successes; smallworld.py L115 breaks at the first success. So π(G) ∝ #valid swaps, or s/(1−(1−s)^K).
- (iii) Minimal reproduction: d = [4,4,2,2,2,2] has 13 labeled realizations. Run `double_edge_swap(G, nswap=5)` 20,000 times: frequencies range 2.0× between realizations (TV 0.066), where uniform gives 1.0.
- (iv) Impact is small on real graphs (≤ 0.03 null-SD on karate, les_mis and others). Still, normalized rich-club, sigma and omega are documented as degree-preserving uniform nulls.
- (v) Fix as above, and note that igraph and NetworKit already count rejections.
- (vi) Also: `random_reference` is a no-op when 2m < n−1, and `niter=1` leaves about 14% of original edges in place.
- (vii) State AI assistance.

**Benefit.** A correctness guarantee for the most-used Python network library's null models. Now that 131 exists, the fixed chain has a theorem behind it; the current one targets the wrong law.

**Measurement.** Exact-enumeration unit test (13 realizations), and the z-shift table above.

**Risks.** Maintainers may see the bias as negligible, which is fair given ≤ 0.03 SD. Seeded-output changes break downstream reproducibility. Under `count_rejected`, dense graphs need far more attempts: 4% acceptance at p = 0.8.

**First step.** A human contributor searches NetworkX issues for existing reports, opens a short issue with the reproduction, then submits PR 1 (the keyword-only option and docs).

### netnull-2 — graph-tool `random_rewire(persist=True)`: non-uniform and can hang (bug report; pursue now)

- The hang reproduces on 2.59, and the 2.98 loop source is unchanged.
- Any graph with a vertex adjacent to all others hangs; ego networks always qualify.
- Proposed fix:
  - document that `persist=True` is non-uniform;
  - cap retries per edge, or skip edges with no valid partner;
  - or deprecate the option for `model="configuration"`.
- First step: an upstream report with the 30-vertex reproduction (`gt_persist_hub.py`) and the exact TV table.

### netnull-3 — certified budgets from 131 for uniform-law samplers (CERTIFY; docs now, numbers as research)

- **Docs** for igraph `rewire`, NetworKit `EdgeSwitching`/`Curveball` and graph-tool `random_rewire` can now state: polynomial mixing for **every** degree sequence, simple undirected case, with explicit gap ≥ c/(2n²) (and ≥ 1/C(n,2) for random-pair Curveball). They must also be explicit that the defaults are heuristics.
- **A `certified_budget(n, m, eps)` helper** is worth adding only for small graphs and for Curveball (see the Q3 table).
- **The sharpened H ≤ L constant** needs a short written proof before anyone cites it.
- **Risks:** users may read "certified" as a recommendation for large graphs; directed, connected and multigraph variants are not covered; `GlobalCurveball` is not covered.

### netnull-4 — vegan: certified burn-in and thinning for `curveball` (pursue now)

- **The chain matches the theorem.** vegan's `curveball` picks a uniform random pair of rows and redistributes uniformly ([nestedness.c L282-L327](https://github.com/vegandevs/vegan/blob/a574546bee7a03f7ea034fe259dd42818eea43ac/src/nestedness.c#L282-L327)). That is exactly FQW26's row-pair heat bath, with gap ≥ 1/C(r,2).
  - Exact gaps on 7 margin pairs: 0.16–0.33 against bounds 0.10–0.33, tight on 3×3.
- **Proposed rule:**
  - burn-in = ⌈C(r,2)(½ log|Ω| + log 2)⌉, with log|Ω| ≤ min(Σ_i log C(c, r_i), Σ_j log C(r, c_j));
  - thin = ⌈C(r,2) ln(1/ρ)⌉.
- **Sipoo** (18×50): burn-in = 22,394 and thin = 705 trades, which take milliseconds.
- **Measured effect on oecosimu NODF z-scores** (`vegan_defaults.R`), 20 replicates of 99 simulations:

  | Settings | Mean z | Run-to-run SD |
  |---|---|---|
  | Defaults (`burnin=0`, `thin=1`) | −0.98 | 1.05 |
  | Certified rule | −1.38 | 0.16 |

  The defaults are unmixed. vegan already documents that sequential methods need burn-in and thinning; the new part is a *certified, cheap* number.
- **Benefit:** a guarantee, for a large ecology user base (oecosimu and nestedness tests).
- **Risks:** FQW26 is an unrefereed, AI-generated preprint whose full theorem is not in this drop's Lean, though its key lemma is via 131. Pairing columns instead would need the column bound.
- **First step:** a vegan issue proposing `burnin="certified"`, or a helper, with the sipoo table.
- **Same issue, second point: `quasiswap`'s default `thin=1` is not uniform.** Exact TV is up to 0.072; with `thin=100` it is ≤ 1e-5.
  - On sipoo the effect is negligible: NODF mean within 0.03–0.04 SD of long-run curveball.
  - So a default `thin` of 100 is cheap insurance, not a fix for wrong results.

### netnull-5 — bctpy `randmio_und` (bug report; pursue now, low effort)

- It uses the same stop-at-first-success law as `random_reference` (real-code p = 5e-34 vs uniform).
- This matters in connectomics, where small-worldness and rich-club nulls are common.
- First step: a report with the reproduction. The MATLAB BCT original still needs checking.

### netnull-7 — R igraph `keeping_degseq(niter = 100)` default (doc/default fix; pursue now, not from the papers)

- The R default is 100 trials *total*, regardless of graph size ([rewire.R L77-L83](https://github.com/igraph/rigraph/blob/b4a4d3381d5a37e2d4678c6bc29319fd1bd1351a/R/rewire.R#L77-L83)). Python igraph and the C `degree_sequence_game` use 10m.
- On BA(2000) and power-law(2000), 95–98% of the original edges survive; the stationary value is about 1–2%.
- Proposed fix: default `niter = 10 * ecount(graph)`, or at least a documentation warning. The 2024 tool comparison already flagged this ([arXiv:2405.05400](https://arxiv.org/abs/2405.05400)).
- First step: check the rigraph issue tracker, then file an issue.

### netnull-6 — NetworkX `is_regular_expander`: deterministic boundary handling (small issue; the full exact mode is not worth it)

**Two bugs found** ([L419-L426](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/generators/expanders.py#L419-L426)):

1. **Answers flip on boundary spectra.** Graphs with a nontrivial eigenvalue exactly at ±2√(d−1) get answers that depend on ARPACK's random start and on node order.
   - C₈ on the same object: True in 13 of 30 calls.
   - Petersen×C₄ (d=5, eigenvalue −4): True in 2 of 40 relabelings.
2. **Bipartite graphs always return False**, because `min(lams)` returns −d. That includes bipartite Ramanujan graphs such as Heawood and K₃,₃. The docstring claims a Ramanujan test without saying which definition it uses.

**The exact test is too slow as a general mode.** It is 178's test, written in integers as n(4(d−1)I − A²) + d²J ≻ 0 and checked by fraction-free Bareiss elimination:

| n | Exact test | Float test |
|---|---|---|
| 100 | 0.33 s | 0.008 s |
| 200 | 8 s | 0.009 s |
| 400 | 244 s | 0.022 s |

**Worth it only as a fallback:** use the exact test when the floating-point |λ| lies within a tolerance band of 2√(d−1). Also fix the docstring and the bipartite handling.

**Value: low.** Random samples almost never land on the boundary.

## What is NOT an opportunity

- **Using 131's bounds to set or defend default swap counts.** At m ≥ 10^4 they are 10^6–10^20× too large; heuristics plus diagnostics remain the state of the art.
- **131's exact sampler.** Its correction branch enumerates 2^{C(n,2)} graphs; its running time is polynomial only in expectation.
- **115 for ecology or statistics.**
  - It analyses an auxiliary padded chain, not the swap or Diaconis–Gangolli chains people run.
  - Its constants are galactic (d^200; more than 10^256 steps for a 2×2 table).
  - Fisher-type tests need the hypergeometric law (r2dtable), not the uniform one.
  - vegan's count models also fix fill, a different state space; vegan itself warns its `swap_count` "seems to be biased".
  - The 0-1 ecology case is FQW26, not 115.
- **178's deterministic construction**, which is galactic and gives no local neighbour oracle.
- **An `exact=True` mode in NetworkX**, which costs O(n^4+) in big integers.
- **Claiming 131 "certifies" NetworkX.** The NetworkX chains target a different law; the fix rests on old principles, and 131 only adds that the corrected chain provably mixes.
- **Certifying connected or directed variants**, which 131 does not cover.

## Experiment results (all in `/home/claude/work/repos/scratch_netnull/`)

| Script | What it found |
|---|---|
| `kernels_as_implemented.py` | Exact as-implemented kernels and stationary laws (the table above) |
| `exhaustive_small.py` | All degree vectors with n ≤ 7, closed-form deg_sw verified; max TV 0.078, ratio 2.5 |
| `confirm_actual_code.py` | Actual-code chi-square tests |
| `gt_check.py` | Actual graph-tool chi-square tests |
| `rr_actual_check.py` | Actual NetworkX `random_reference` chi-square tests |
| `bct_check.py` | Actual bctpy chi-square tests |
| `cdes_check.py` | Actual `connected_double_edge_swap` chi-square tests |
| `nk_curveball_check.py` | Actual NetworKit `Curveball` chi-square tests |
| `gt_persist_hub.py` | graph-tool `persist=True` hang |
| `exact_stationary.py`, `johnson_check.py` | Exact gaps against bounds; H ≤ L check |
| `bip_curveball_gap.py` | Bipartite Curveball exact gaps |
| `vegan_exact.py`, `vegan_actual.R` | vegan exact and actual laws |
| `vegan_sipoo.R`, `vegan_defaults.R` | z-score stability under default vs certified settings |
| `practical_bias.py`, `cv_hard.py` | Real-graph impact |
| `budgets.py`, `certified_small.py`, `curveball_timing.py`, `overlap_lb.py` | Budgets, timings, default-mixing lower-bound check |
| `patched_kernel.py`, `rr_patched_check.py` | Patch verification |

## Sources

- Fosdick, Larremore, Nishimura & Ugander, *Configuring random graph models with fixed degree sequences*, SIAM Rev. 2018 — https://arxiv.org/abs/1608.00607
- Carstens & Horadam, *Switching edges to randomize networks: what goes wrong and how to fix it*, J. Complex Netw. 2017 — https://doi.org/10.1093/comnet/cnw027
- Milo, Kashtan, Itzkovitz, Newman & Alon, *On the uniform generation of random graphs with prescribed degree sequences* — https://arxiv.org/abs/cond-mat/0312028
- Coolen et al., *Controlled Markovian dynamics of graphs* (mobility bias) — https://arxiv.org/abs/1203.0877
- *Comparative analysis of graph randomization: tools, methods, pitfalls, and best practices* (2024) — https://arxiv.org/abs/2405.05400
- Fu, Qin & Wang, *Spectral Gap for the Binary Fixed-Margin Swap Chain* (2026) — https://arxiv.org/abs/2606.22636
- NetworkX automated-contributions policy — https://networkx.org/documentation/latest/developer/contribute.html
- Pinned code: networkx 6da4704c, igraph 912f99d5, rigraph b4a4d338, networkit 5f03e17c, vegan a574546b, bctpy c28931c7, graph-tool 2.98+ds (Ubuntu orig tarball), openai/math fd4aeeb2
