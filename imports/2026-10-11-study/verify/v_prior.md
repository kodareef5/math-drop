# Independent verification of the prior "do not pursue" claims

Sources: TeX in `/root/openai-math/preprints/<dir>/build/`, with dirs found via `/home/claude/work/catalogue.json`. zstd was cloned at depth 1 into `/home/claude/work/verify_repos/zstd` (HEAD `49cf51799ea0`, 2026-10-05). Rerun scratch files are in `/tmp/claude-0/-home-claude/9ecfe579-5c26-592b-b10c-fed627312cde/scratchpad/`.

| # | Claim | Status |
|---|-------|--------|
| 1 | 121 edit distance: exact DP unless ell >= 2^1000 | confirmed |
| 2 | 107 omega <= 9/4 is non-constructive; companions have no crossover | confirmed |
| 3 | 109 kappa = 2^-182, d >= 2 only at n >= 2^(2^(2^75)), multitape TM | confirmed |
| 4 | 142 factoring exponent 10^12, p > B^200000, about p trials otherwise, depends on 029 | confirmed |
| 5 | 130 DFT saving (log n)^(2·10^-13), no useful crossover | confirmed (wording nit) |
| 6 | 128 vs zstd: COVER/FASTCOVER optimize coverage under a budget, merge saves <=1.06%/1.29% | confirmed (1.06% is really 1.053% of dictionary bytes) |
| 7 | 003 does not cover class-group Hecke L-functions | confirmed (029 caveat) |

---

## 1. Family 121, almost-linear edit distance

`An-Almost-Linear-Approximation-Scheme-for-Edit-Distance-September-24-2026/build/sections/02-geometry.tex`

- Parameters (subsection "Uniform access to the accuracy input"): "define $H$ as the least power of two at least $\lceil\log_2(N+2)\rceil$, and $\ell$ as the least power of two at least $\max(1,\log_2 H)$."
- Line 99: "Use exact dynamic programming also if $\ell<2^{1000}$ or $\ell\varepsilon<10$. It uses $O((N+1)^2)$ word operations and can store only two rows."
- Line 155: the slack inequalities "follow at $\ell\ge2^{1000}$".
- `01-introduction.tex` `thm:main`: "For every fixed rational $\varepsilon$, its worst-case expected running time ... is $N^{1+o(1)}$". The threshold "may depend on $\varepsilon$."

What this means: ell >= 2^1000 requires log2 H > 2^999, so H > 2^(2^999). That gives ceil(log2(N+2)) > 2^(2^999), i.e. N > 2^(2^(2^999)) roughly. The second condition, ell·eps >= 10, makes it stricter still. The prior statement is exact.

## 2. Family 107, omega <= 9/4 and its companions

`Matrix-Multiplication-Nine-Fourths-October-2-2026/build/paper.tex`

- sec:intro: "Theorem~\ref{thm:main} concerns the asymptotic arithmetic exponent; its proof does not specify a competitive finite matrix size."
- End of the proof in sec:growth: "The definition of $\nu$ supplies a fixed integer $u\geq2$ and an exact rank decomposition of $T_u$ of length $r<u^{9/4+\delta}$." Here $\nu=\inf_n\log_n R(T_n)$ (eq:mm). The decomposition exists only through the infimum, and none is exhibited.
- The bound $\nu\le 9/4$ comes from `lem:existence` (Detecting characters), whose proof "uses finite dimensional separation, compactness, and a fixed-point theorem" (Appendix sec:existence). This is an existence argument over Strassen's asymptotic spectrum.
- The closing remark notes only that the coefficients can be taken algebraic, by the Nullstellensatz.

Companions:

- `Staggered-extraction-...-September-24-2026/build/sections/introduction.tex`, `thm:main`: $\omega_F<2.371054886006746$. It adds: "the counting arguments and parameter choices do not give bit-complexity or practical crossover estimates."
- `Complex-Matrix-Multiplication-Below-2.258-.../build/introduction.tex`, `thm:main`: $\omega<1129/500=2.258$, proved via Schönhage's asymptotic sum inequality on Coppersmith–Winograd-type tensors.
  - `rectangular/08-comparison.tex`: "It does not claim a practical crossover size".
  - `tex/conclusion.tex`: "It does not estimate the size of a useful finite implementation or its numerical stability".
  - `tex/reproducibility.tex`: "do not claim a practical matrix-multiplication implementation".
  - `cor:characteristic-transfer` "selects two fixed exact rank schemes" that are not exhibited.

## 3. Family 109, integer multiplication below n log n

`Integer-multiplication-below-n-log-n-September-23-2026/build/sections/`

- `00-introduction.tex`, `thm:main`: "one deterministic Turing machine $A$, with a fixed finite alphabet and a fixed finite number of one-dimensional tapes ... $T_A(n)=O(n(\lg n)^{1-\kappa}),\ \kappa=2^{-182}$." It continues: "The constants and thresholds in the construction are extremely large".
- `08-assembly.tex`, eq:fixed-parameters: "$C_1=20,\ \epsilon=2^{-75},\ \kappa=2^{-182}$".
- Sizes: "$b=\lceil\log_2n\rceil,\ p=6b,\ d=\lfloor b^\epsilon\rfloor$". Also: "$d=\lfloor b^{2^{-75}}\rfloor$ is found by binary search using exact comparisons $d^{2^{75}}\le b$".
- Line ~1002: "Fix one cutoff beyond all the size, precision, margin and layout conditions, and use schoolbook multiplication below it."

What this means: d >= 2 iff b >= 2^(2^75), i.e. n > 2^(2^(2^75) - 1). This matches the prior's n >= 2^(2^(2^75)).

## 4. Family 142, deterministic factoring over F_p

`Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/build/sections/`

- `00-introduction.tex`, `thm:factorization`: "$O\bigl(((n+1)\lceil\log_2p\rceil)^{10^{12}}\bigr)$ bit operations". eq:B defines $B=20+(n+1)(L+1)$.
- `08-driver.tex`: "Call the characteristic \emph{small} when $p\le B^{200000}$." In that case Step 5 reads: "Test $\gcd(h,b-a)$ for $a=0,\ldots,p-1$". Also: "Scalar enumeration in the small case costs at most $B^{200000}$ trials per call."
- `09-complexity.tex`: "In the branch $p\le B^{200000}$, no auxiliary table or curve is used. The extra scalar loop ... has length at most $p$". The small-prime branch costs $O(B^{201000})$.
- Computed: the large branch needs log2 p >~ 200000·log2 B. That is about 4.63M bits at n=1 and about 5.83M bits at n=100.
- `10-analytic.tex`, Theorem `analytic:hecke` = "[OpenAIPrimitive26, Theorem~1.2]". It gives a zero-free region $\Re s>1-10^{-6}$ for every finite-order Hecke character of cyclotomic $K\supseteq\mu_{12}$, and the paper says: "Its proof is not part of this paper". The same section notes that GRH alone suffices.
- The cited result is family 029's `thm:hecke-zero-free` (`Primitive-roots-for-every-admissible-integer-base-October-4-2026/build/sections/01-introduction.tex`). The catalogue has `lean: false` for both 029 and 142.

## 5. Family 130, exact DFT below n log n

`An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/`

- `introduction.tex`, eq:main-constants: $m=10^6$, $W_*=2^{71}$, $\Delta=6871402692000000$, $\theta=\log_m(m-\Delta/W_*)$.
- `thm:main`: $O(n(\log n)^\theta(\log\log n)^{4-\theta})$. `cor:decimal`: $O(n(\log n)^{1-10^{-13}})$.
- The paper says: "The constants in the algorithm are enormous, so these are asymptotic existence and explicitness results, with no useful crossover estimate. ... does not assert a corresponding improvement for stable floating-point FFTs or for bit complexity."
- Recomputed with mpmath: θ = 0.99999999999978936, so 1−θ = 2.106·10⁻¹³ (`all-lengths.tex`: "$\theta<1-2\cdot10^{-13}$"). At log2 n = 64, (log n)^(1−θ) − 1 ≈ 8.8·10⁻¹³.
- `network.tex`, `net:tensor-bound`: for k < K = m·72 = 7.2·10⁷ the factors are applied directly. W_* = 2^71 is the number of arrays batched together, not a block length. The prior's phrase "2^71-element blocks" is a wording slip; it does not change the verdict.
- The companion `Finite-tensor-savings-...` `thm:main` is a nonuniform liminf existence result: "The coefficients are chosen separately for each resulting circuit; their preparation is outside this model."

## 6. Family 128 (SCS) vs zstd dictionary builder

The code reviewed is `/home/claude/work/verify_repos/zstd/lib/dictBuilder/{cover.c,fastcover.c,zdict.c}`.

- cover.c:483-490 (FASTCOVER at fastcover.c:140-147 is the same, with hashed dmers): "Score(S) = F(S_1) + F(S_2) + ... + F(S_{k-d+1}) ... Once the dmer d is in the dictionary we set F(d) = 0." So this is greedy max-coverage.
- `COVER_buildDictionary` (cover.c:754-806) and `FASTCOVER_buildDictionary` (fastcover.c:395-450) both run `for (epoch = 0; tail > 0; ...)`, set `segmentSize = MIN(segment.end - segment.begin + parameters.d - 1, tail)`, then call `memcpy(dict + tail, ...)`. They concatenate back to front ("to allow the best segments to be referenced with the smallest offsets") until the byte budget is used up. Neither has a merge or overlap step.
- COVER trims zero-frequency heads and tails (cover.c:547). FASTCOVER does not.
- `ZDICT_trainFromBuffer` (zdict.c:1111) calls `ZDICT_optimizeTrainFromBuffer_fastCover` with d=8 and steps=4.
- Only the legacy trainer has an overlap merge: `ZDICT_tryMerge`, zdict.c:356.

Conclusion: the objective is coverage under a byte budget, not superstring length. Confirmed.

### Measurement re-check

The scripts are in `/home/claude/work/repos/scratch_optimization/`.

- Instrumentation: the diff against upstream shows only one `fprintf(SEGLOG, begin, segmentSize)` line after each `memcpy` (plus stdio/stdlib includes). Training used `ztrain.c` with dictionary capacity 112,640, k=200, d=8 and f=20 for FASTCOVER, at level 3. The input was 1,278 files listed in `/tmp/claude-0/samples.txt`, 17,785,822 bytes in total.
- Rerun: the instrumented trainer gave segment logs and a corpus concat that are byte-identical to the stored `seg_cover.log`, `seg_fastcover.log` and `samples_concat.bin`. The segment sizes sum to exactly 112,640 for both modes.
- `seg_overlap.py` rerun, about 12 s:
  - COVER: 567 segments, 22 B contained, greedy saves 1,164 B (1.05%).
  - FASTCOVER: 564 segments, 0 B contained, greedy saves 1,452 B (1.29%).
- Independent upper bound (my `ub.py`/`ub2.py`): I removed contained and duplicate segments, then took a max-weight assignment (cycle cover) over the pairwise suffix-prefix overlap matrix. That gives 1,186 B = **1.053%** for COVER and 1,452 B = **1.289%** for FASTCOVER. So the greedy result is optimal for both.
- The overlaps are tiny. The largest pairwise overlap in COVER is 7 B; FASTCOVER has two outliers of 113 B and 166 B.
- The method is sound. A max-weight cycle cover bounds the overlap of any single superstring order from above, so it is a valid bound on the savings. The prior's "1.06%" equals 1186/111454, which divides by the merged length rather than the dictionary size. Against dictionary bytes the figure is 1.053%; the conclusion is unchanged.
- Limitation: there is one corpus, of C++ sources. The bound also covers only the bytes that merging would free; refilling those bytes with more segments would have marginal coverage value.

## 7. Family 003 and class-group computations (PARI bnfinit/quadclassunit)

- `The-Quasi-Riemann-Hypothesis-September-30-2026/build/paper.tex`, `thm:main`: "Every finite-order Hecke $L$-function over $F=\mathbb Q(\sqrt{-3})$ has no zero in $\Re s>7/8$. The same holds for every Dirichlet $L$-function, including $\zeta(s)$."
  - The Dirichlet case is derived from the Hecke one, via eq:hecke-dirichlet-factorization: $L_F^{S}(s,\chi\circ N)=L^{S}(s,\chi)L^{S}(s,\chi\chi_{-3})$.
- `The-Quasi-Riemann-Hypothesis-October-5-2026/build/paper2.tex`, `thm:main`: the same scope with $11/12$.
  - Its listed class-group consequences are for *imaginary quadratic class numbers*: an effective $h(D)\gg\sqrt{|D|}/\log\log|D|$ and the idoneal-number list. These come via Dirichlet's class-number formula, which only involves Dirichlet $L(1,\chi_D)$.
- `Uniform-exclusion-of-Landau-Siegel-zeros-October-1-2026/build/paper.tex`, `thm:main`: covers real zeros of primitive real **Dirichlet** characters only.

Reasoning:

- GRH-conditional class-group algorithms (Bach's bound, as used in PARI `bnfinit`/`quadclassunit`, Magma `Proof:="GRH"`) need zero-free information for $\zeta_K$ and $L_K(s,\psi)$, where $\psi$ runs over characters of $\mathrm{Cl}(K)$. These are Hecke characters of $K$.
- For a quadratic $K$ of discriminant $d$:
  - Genus (order-2) characters give $L_K(s,\psi)=L(s,\chi_{d_1})L(s,\chi_{d_2})$, which 003 covers.
  - For $\psi$ of order at least 3, $L_K(s,\psi)=L(s,\mathrm{Ind}_K^{\mathbb Q}\psi)$ is an irreducible 2-dimensional dihedral Artin L-function. It is not a product of Dirichlet L-functions. It is not a Hecke L-function over $\mathbb Q(\sqrt{-3})$ either, apart from order-4 ($D_4$) cases where the representation happens to also be induced from $\mathbb Q(\sqrt{-3})$.
- So 003 does not remove GRH from these computations. Confirmed.

Caveat, which is not part of the claim being checked: family 029 `thm:hecke-zero-free` covers all finite-order Hecke characters of any cyclotomic $F\supseteq\mu_{12}$ (width $10^{-6}$, unformalized).

- Take $F=\mathbb Q(\mu_{\mathrm{lcm}(12,|d|)})\supseteq K$. Then $L_F(s,\psi\circ N_{F/K})=\prod_{\omega}L_K(s,\psi\omega)$, with $\omega$ running over characters of $\mathrm{Gal}(F/K)$, so the strip transfers to $L_K(s,\psi)$.
- The result is an unconditional but galactic Bach-type bound of order $(\log|d|)^{O(10^6)}$. This matches the triage note in `/home/claude/work/triage/b04_nt_logic.json`.
- So the practical "keep the GRH caveats" conclusion holds whichever family is cited.
