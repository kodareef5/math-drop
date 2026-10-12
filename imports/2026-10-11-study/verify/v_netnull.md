# Independent verification of netnull-1, -2, -4, -5, -7

Verifier's own checks. I read the original write-up (`/home/claude/work/deep/netnull.md`) only after all of these were finished, and used it just to compare numbers and to work out which graph-tool configuration its TV table modelled.

Scripts and outputs are in `/home/claude/work/verify_repos/scratch_v_netnull/`. Fresh depth-1 clones are in `/home/claude/work/verify_repos/`:

| Repository | Commit |
|---|---|
| networkx | `6da4704c` |
| bctpy | `c28931c7` |
| vegan | `a574546b` |
| rigraph | `b4a4d338` |

These match the permalinks in the rows. Other sources:

- **MATLAB BCT:** `/home/claude/work/verify_repos/bct_matlab/`.
- **graph-tool 2.98 source:** `/home/claude/work/verify_repos/gt_src/` (Ubuntu orig tarball).

## Summary

| id | status | key numbers |
|---|---|---|
| netnull-1 | confirmed | n≤7 sweep: max TV 0.0783, max/min 2.5 (exact match). Real NX: p≈0 vs uniform, p=0.79 vs predicted law. `random_reference` is a no-op when int(2m/(n−1))=0. |
| netnull-5 | confirmed (reach ↑) | Real bctpy p=1e-38. **MATLAB BCT `randmio_und.m` has the same loop**, and run under Octave it gives p=8e-43 vs uniform, p=0.69 vs predicted. Five BCT randmio variants share the loop. |
| netnull-2 | corrected | Non-uniformity and hang confirmed on real graph-tool. The quoted TV range 0.039–0.054 is for `edge_sweep=False`; under the default `edge_sweep=True`, TV is 0.097 on 442222. |
| netnull-4 | confirmed | swap TV up to 0.078; quasiswap(thin=1) TV up to 0.072; curveball uniform with gap ≥ 1/C(r,2). Real vegan 2.6.4 agrees. vegan docs already mention the swap and quasiswap bias qualitatively. |
| netnull-7 | confirmed | R igraph `niter=100` total trials (1.6.0 and current main). 95.2% of edges survive on BA(2000). |

## netnull-1: NetworkX `double_edge_swap` / `random_reference`

### Source reading

**`double_edge_swap`** (`swap.py` L202–228):

- The proposal picks u and x with probability ∝ degree, then v and y uniformly from their neighbours. That makes each oriented edge pair uniform with probability 1/(2m)².
- `continue` on u==x or v==y does not increment `n` or `swapcount`.
- The swap succeeds iff x∉N(u) and y∉N(v).
- `swapcount` increments only on success. The output after `nswap` successes is therefore the embedded jump chain. The per-attempt kernel is symmetric, so the jump chain has π(G) ∝ s(G), the number of successful proposals.

**`random_reference`** (`smallworld.py` L79–117):

- Each of `niter*m` outer iterations makes up to T=int(2m/(n−1)) counted attempts and `break`s at the first success.
- So π(G) ∝ s/(1−(1−p)^T), where p is the per-attempt success probability. This is uniform only when T=1.
- When T=0 the outer loop does nothing.

### Exact kernels (`exact_kernels.py`, out: `exact_kernels_out.json`)

The script enumerates labeled realizations, builds the kernel as coded and solves for the stationary law. For every case:

- The per-attempt kernel is exactly symmetric.
- The stationary law matches the closed form above to ≤1.5e-15.
- The count-all-attempts chain is exactly uniform (TV 4e-16).

| d | chain | N | TV vs uniform | max/min |
|---|---|---|---|---|
| 442222 | double_edge_swap | 13 | 0.0659 | 2.00 |
| 442222 | random_reference (T=3, connected) | 13 | 0.0223 | 1.32 |
| 222222 | double_edge_swap | 70 | 0.0571 | 1.50 |
| 222222 | random_reference (T=2, connected) | 60 | 0 (only connected realizations are 6-cycles: vertex-transitive) | 1.00 |
| 3333222 | double_edge_swap | 553 | 0.0264 | 1.71 |
| 3333222 | random_reference (T=3, connected) | 552 | 0.0161 | 1.21 |

### Exhaustive sweep (`sweep_n7.py`, out: `sweep_n7_out.json`)

The sweep covers all 278 graphical sequences on 4–7 vertices that have min degree ≥1 and ≥2 realizations.

- **`double_edge_swap`:** max TV **0.0783** at d=(5,5,5,3,3,3,2) (30 realizations). Max ratio **2.5** at d=(5,5,2,2,2,2,2).
- **`random_reference`** (no connectivity filter): max TV 0.039.
- **`random_reference`** (connectivity, n≤6): max TV 0.025.

The claimed numbers (TV ≤ 0.078, ratio ≤ 2.5) reproduce exactly. The row's spot values (442222 → 0.066/2.00, 333333 → 0.057/1.50, 4333111 → 0.078/1.75) also match my sweep.

### Real-code chi-square (`empirical_lib.py`)

I ran installed networkx 3.6.1. Its `swap.py` is byte-identical to the clone. Its `smallworld.py` differs only in using `has_path` instead of `local_edge_connectivity` for the connectivity check, which is equivalent.

All runs used d=442222 from a fixed start.

| Function | Runs | Settings | χ² vs uniform | vs predicted law | Note |
|---|---|---|---|---|---|
| `double_edge_swap` | 40,000 | nswap=60 | 2590, p≈0 | p=0.79 | the graph predicted at 2× is hit 5786 times vs ≈2880 for the others |
| `random_reference` | 30,000 | niter=10, connectivity=True | p=2.8e-39 | p=0.25 | |

### No-op case

| Graph | n | m | ntries | Unchanged outputs |
|---|---|---|---|---|
| P5 + 5 isolated vertices | 10 | 4 | 0 | 200/200 |
| 4 disjoint edges + 4 isolated vertices | 12 | 4 | 0 | 200/200 |

### Docs

Neither docstring claims uniformity. The `random_reference` docstring says only "An edge is rewired approximately `niter` times".

`rich_club_coefficient(normalized=True)` calls `double_edge_swap(R, Q*E, max_tries=Q*E*10)` (`richclub.py` L111), so the default rich-club normalization uses this chain.

## netnull-5: bctpy and MATLAB BCT `randmio_und`

### bctpy

`reference.py` L1479–1557:

- max_attempts = round(n·k/(n(n−1))) = round(m/(n−1)).
- `while att <= max_attempts` allows T = max_attempts+1 attempts, with a `break` on success.

Exact law for d=442222 (T=3): TV 0.0223, max/min 1.32.

Real bctpy from the clone, 30,000 runs (itr=10): χ²=212, p=9.8e-39 vs uniform; p=0.53 vs predicted.

### MATLAB BCT

I fetched `randmio_und.m` from FieldTrip `external/bct` and from brainlife/BCT `2019_03_03_BCT`. The two are identical apart from whitespace. The official BCT sites (sites.google.com/site/bctnet, brain-connectivity-toolbox.net) are blocked by the proxy.

The header reads "Mar 2012: Limit number of rewiring attempts, count number of successful rewirings (Olaf Sporns)".

The code is the same pattern:

```matlab
maxAttempts= round(n*K/(n*(n-1)));
for iter=1:ITER
    att=0;
    while (att<=maxAttempts)
        ...
        if ~(R(a,d) || R(c,b))
            ... eff = eff+1; break;
        end
        att=att+1;
```

The same `maxAttempts`/`break` structure is in:

- `randmio_und_connected.m`
- `randmio_dir.m`
- `randmio_dir_connected.m`
- `randmio_und_signed.m`, with maxAttempts=round(n/2)

### MATLAB code under Octave

Octave 8.4 ran the FieldTrip `randmio_und.m` 30,000 times on d=442222 with ITER=10 (`bct_matlab_empirical.m`, `bct_matlab_compare.py`):

- χ²=232, **p=8.2e-43** vs uniform.
- **p=0.69** vs the predicted law.

### Reach

The MATLAB BCT is the standard network-neuroscience toolbox and is redistributed inside FieldTrip and GraphVar. Its `randmio_und` and `randmio_und_connected` drive most small-world and rich-club nulls in connectomics. Since the bias is in the original toolbox and not only the Python port, I raise reach from 3 to 4.

The effect size per graph is still small: TV 0.02 on this toy case, and the original analyst's practical estimate is ≤0.03 null-SD.

## netnull-2: graph-tool `random_rewire(persist=True)`

### Sources

- The 2.98 orig tarball (`gt_src/x/graph-tool-2.98+ds/src/graph/generation/graph_rewiring.hh`) has the main loop at L276–354, with `do { success = rewire(e, ...); } while(persist && !success);` at L339–343.
- Its diff against the installed 2.59 header (`/usr/lib/python3/dist-packages/graph_tool/include/generation/graph_rewiring.hh`) is only `graph_tool::is_directed`→`is_directed`, the sampler header rename and nmap typedef refactors.
- `python3-graph-tool` 2.59 imports under python3.12.

`RewireStrategyBase::operator()` with `RandomRewireStrategy` works as follows:

- The target slot is uniform over all m slots, and both orientations are coin-flipped.
- The move is rejected if the target slot is the same slot, if it would make a self-loop, or if it would make a parallel edge.
- a=0 for the simple configuration model, so accept probability is 1.

### Exact kernels (`gt_persist_exact.py`, out: `gt_persist_exact_out.json`, `gt_persist_333333_out.json`)

I modelled the default `edge_sweep=True` sweep exactly by tracking (graph, set of not-yet-visited edges). A random permutation is equivalent to choosing a uniform unvisited slot at each step. I also modelled `edge_sweep=False`.

| d | N | sweep, persist=False | no-sweep, persist=False | **sweep, persist=True** | no-sweep, persist=True |
|---|---|---|---|---|---|
| 442222 | 13 | TV 0 (doubly stochastic) | 0 | **0.0968 (ratio 2.52)** | 0.0535 (1.80) |
| 222222 | 70 | 0 | 0 | 0.0571 (1.50) | 0.0571 (1.50) |
| 333322 | 54 | 0 | 0 | **0.0800 (1.72)** | 0.0631 (1.42) |
| 333333 | 70 | — | — | 0.0390 (1.33) | 0.0390 (1.33) |
| 332211 | 17 | 0 | 0 | never returns (unswitchable edge) | never returns |

Notes on the table:

- The persist=False sweep is uniform because the sweep kernel is doubly stochastic. This also settles the point the original left open, that the default `edge_sweep=True` is exactly uniform.
- The analyst's TV table (0.054 for 442222, 0.039 for 333333) used `edge_sweep=False` (their `gt_persist_nosweep.py`). Under the library default `edge_sweep=True`, the bias is up to 1.8× larger: 0.097 vs 0.054 on 442222. Their own `gt_check.json` empirical TV for persist+sweep was 0.0935, which is consistent with my 0.097.
- So the row's "TV 0.039–0.054" should read "0.039–0.097 (0.097 under the default `edge_sweep=True`)".

### Real code (`gt_empirical.py`)

I ran 30,000 runs of n_iter=10, sweep=True on d=442222:

| persist | χ² vs uniform | vs exact law | Note |
|---|---|---|---|
| True | 3990, p≈0 | **p=0.89** | the over-weighted graph appears 5221/30000 vs predicted 0.1737 |
| False | p=0.55 | p=0.43 | |

### Hang (`gt_hang.py`)

The test graph is a 28-vertex 3-regular graph plus one hub adjacent to all 28 vertices.

- With `persist=False`, `random_rewire(n_iter=1)` returns in under 0.01 s with 48 failed attempts.
- With `persist=True`, the process is still running when `timeout` kills it at 45 s (exit 124).

Every hub edge is unswitchable: any switch creates a hub–neighbour duplicate or a self-loop.

### Docstring

The docstring (`__init__.py` L618–623) says persist "may improve the quality of the shuffling ... may result in many repeated attempts for certain corner-cases". It mentions neither non-uniformity nor non-termination.

## netnull-4: vegan

### Source reading (`src/nestedness.c`)

- **`swap`** (L220–267): `for(;;)` until one checkerboard swap succeeds, repeated `thin` times. It is the jump chain, so π ∝ the number of swappable 2×2 submatrices.
- **`trialswap`** (L165–213): counts every trial.
- **`curveball`** (L282–327): picks 2 distinct rows and does a uniform reshuffle of row-unique species. This is a symmetric kernel.
- **`quasiswap`** (L95–159): starts from `r2dtable` and checks `ss > mtot` only every `thin` steps. The R default thin is 1, from `simulate.nullmodel` and `oecosimu`. `permatswap(method="quasiswap", thin=1)` and `permatfull(mtype="prab")` use it.

### Exact laws (`vegan_exact.py`, `vegan_sweep.py`, `vegan_curveball_gap.py`)

The quasiswap output law is the exact absorption law from the r2dtable start, whose law is ∝ 1/∏t_ij!. The sweep covers 44 margin pairs up to 4×4.

| Model | Exact TV from uniform | Note |
|---|---|---|
| swap (stationary) | up to **0.078** (rs=3221, cs=3311) | spot cases 0.028–0.05, matching the original's "0.028–0.05 on 6 pairs"; my wider sweep found larger |
| quasiswap, thin=1 | up to **0.0720** (2222/2222, 90 tables) | matches the claimed 0.072 |
| quasiswap, thin=10 | 0.002–0.017 | |
| quasiswap, thin=100 | ≤1.6e-4 | |
| trialswap | ~1e-16 | exactly uniform |
| curveball | ~1e-16 | exactly uniform |

On all 49 margin pairs, the curveball spectral gap is ≥ 1/C(r,2). The bound is attained, with min gap/bound = 1.000.

### Real R vegan 2.6.4 (`vegan_empirical.R`, `vegan_compare.py`)

The matrix is 3×4 with rs=(2,2,2), cs=(2,2,1,1), which has 15 tables. Each model drew 60,000 samples.

| Model | χ² vs uniform | vs exact predicted law |
|---|---|---|
| quasiswap thin=1 | 1068, p=4.6e-219 | p=0.34 (TV 0.053 emp vs 0.0533 exact) |
| swap (burnin 1000, thin 25) | 974, p=5.5e-199 | p=0.21 |
| quasiswap thin=100 | p=0.65 | |
| curveball | p=0.49 | |
| tswap | p=0.45 | |

### sipoo (`vegan_sipoo_z.R`)

This is `oecosimu(..., nestednodf, "curveball", nsimul=99)` repeated 30 times:

| Settings | Run-to-run SD of NODF z |
|---|---|
| defaults (burnin=0, thin=1) | **1.04** (claimed 1.05) |
| burnin=20000, thin=500 | 0.25 |

The original's 0.16 used its own certified settings. I did not replicate those exactly.

### Already documented?

Partly. `man/commsim.Rd` says:

- `tswap` exists "because they found that ordinary swap may lead to biased sequences" (Miklós & Podani 2004).
- quasiswap "accepts thin argument ... helps in reducing or removing the bias".

So the swap bias and the quasiswap thinning bias are acknowledged qualitatively. What is new is the exact size of the bias, the fact that quasiswap's default thin=1 is biased, and the certified curveball burn-in.

I did not attempt to verify the FQW26 preprint. My curveball gap check agrees with its bound on small cases.

## netnull-7: R igraph `keeping_degseq`

### Source

- `R/rewire.R` (b4a4d338) has `keeping_degseq <- function(loops = FALSE, niter = 100)`, and `rewire_keeping_degseq` calls `rewire_impl(rewire = graph, n = niter, ...)`.
- `rewire_impl` passes `n` to `R_igraph_rewire`, then to the C `igraph_rewire(graph, n, mode)`.
- The vendored `src/vendor/cigraph/src/operators/rewire.c` runs `while (num_swaps < n)`, counting all trials, both successful and failed: "We count both successful and unsuccessful rewiring trials. This is necessary for uniform sampling." So 100 is the **total** trial count, not a per-edge count.
- The docs say only "Number of rewiring trials to perform". The r.igraph.org page for 2.3.3.9040 shows `niter = 100`.

### Contrast

- python-igraph 1.0.0 `Graph.rewire`: "The default is 10 times the number of edges".
- C `degree_sequence_game` (`games/degree_sequence.c` L747): `igraph_rewire(graph, 10 * igraph_ecount(graph), ...)`.

### Empirical

R igraph 1.6.0, installed from apt `r-cran-igraph`, also has `niter = 100`. I used `sample_pa(2000, m=2)` simplified to 3997 edges:

| Rewire | Fraction of original edges surviving |
|---|---|
| default, 5 runs | 0.9515–0.954 |
| `niter = 10*m` | 0.009–0.010 |

This matches the claimed "95–98% survive vs 1–2%".

### Limits

- I could not search the rigraph issue tracker: GitHub search and the API are blocked for non-session repos, and HTML is robots-blocked.
- The arXiv:2405.05400 abstract does not mention the igraph default. The "already flagged" remark may be in its body, which I did not check.
- Issue #103 ("Losing edge weights when rewiring") is unrelated.

## Is the principle already documented?

The principle is: count rejected proposals, or the chain is non-uniform.

**In the literature,** yes. Fosdick, Larremore, Nishimura and Ugander (SIAM Review 2018, arXiv:1608.00607), §2.3, Algorithm 1: "if edge swap would leave graph space then resample current graph", and "incorrect algorithms have a tendency to overlook the resampling step". They name no software. Artzy-Randrup & Stone 2005 and Miklós & Podani 2004 are the classic ecology and network references.

**In the libraries:**

| Library | Documented? |
|---|---|
| igraph C | Yes. Its source comment states it explicitly. |
| vegan | Qualitative bias acknowledgement in `commsim.Rd` for swap and quasiswap. |
| graph-tool | Default path is correct. The `persist` docs mention only speed. |
| NetworkX | No. Docstrings are silent, and the code comment only notes that node selection is degree-weighted. |
| bctpy | No. Docstrings are silent. |
| MATLAB BCT | No. Docstrings are silent. |

**Issue trackers:** I could not search GitHub issues for networkx, bctpy, rigraph or vegan. GraphQL and the search API are blocked for non-session repos, and github.com HTML is robots-disallowed. Web search turned up no issue reporting the bias for NetworkX or BCT. A third-party R package PR (paliocha/rcomplex#7, Sep 2026) cites the counting rule in replacing igraph's rewiring, but does not report the R default. Prior reports therefore remain **unverified**, and a human must search the trackers before filing.

## Script index

All scripts are in `/home/claude/work/verify_repos/scratch_v_netnull/`:

| Script | Purpose |
|---|---|
| `exact_kernels.py` | exact kernels for NX `double_edge_swap`, `random_reference`, BCT, and the count-all reference |
| `sweep_n7.py` | all n≤7 sequences, closed-form stationary TV |
| `empirical_lib.py` | real NetworkX and bctpy runs plus chi-square |
| `bct_matlab_empirical.m` + `bct_matlab_compare.py` | MATLAB BCT under Octave |
| `gt_persist_exact.py`, `gt_persist_333333.py` | exact graph-tool sweep and no-sweep kernels |
| `gt_empirical.py` | real graph-tool runs (python3.12) |
| `gt_hang.py` | persist hang reproduction |
| `vegan_exact.py`, `vegan_sweep.py`, `vegan_curveball_gap.py` | exact vegan laws and gaps |
| `vegan_empirical.R` + `vegan_compare.py` | real vegan runs |
| `vegan_sipoo_z.R` | sipoo z-score SD |
