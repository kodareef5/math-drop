# b01_tcs_a: triage memo (families 102–121, theoretical computer science)

I read the TeX sources for all 20 families. There are no T1 or T2 results: every algorithm is either galactic or non-constructive.

## Ranked opportunities (all modest)
1. **104, mean-payoff / stochastic / parity games (T3, BENCHMARK, deep-dive).** The only fully specified exact-arithmetic recursion here without astronomical parameters built in. It is the first deterministic quasipolynomial algorithm for simple stochastic games and binary-weight mean-payoff games. Benchmark it as a robust fallback against Zielonka and strategy iteration in Oink, PRISM-games and Storm. The worst-case call bound is still about 10^300 at n=100.
2. **118, bin packing, MIRUP disproved (T3, REDIRECT).** Settles the cutting-stock conjecture, and fixed-additive approximation is NP-hard. The gap instances are astronomical (P0=100^11, d ≥ 2.4·10^27 for c=1). Solvers that use ceil(LP) are unaffected and there are no usable benchmark instances. Update textbooks, and point small-instance search at the smallest instance with gap ≥ 2.
3. **119, Courtade–Kumar (T3, CERTIFY).** A sharp closed-form converse, 1−h(ε), for one-bit summaries of noisy bits. Practical, but the model is stylized.
4. **113, general-graph perfect-matching FPRAS (T3, REDIRECT).** The algorithm is unusable (replica count 32·(10⁴ND)^100). Non-obvious channel: it removes the complexity-theoretic case for Gaussian boson sampling applications that estimate perfect-matching counts of unweighted graphs.
5. **115, contingency tables (T3, RESEARCH).** The sampler is galactic: d^200 steps with d=(m+1)(n+1)+10, about 10^256 for a 2×2 table. It targets the uniform law, while Fisher's exact test (R `fisher.test`, `r2dtable`) needs the hypergeometric law, which Patefield already samples exactly. The real use is fixed-margin null models (vegan `permatswap`). Open question: can the analysis certify the standard swap chain, as 131 does for edge switches?
6. **116, noncommutative identity testing (T3).** An explicit 2ns²-dimensional rational hitting point. Easy to prototype in SageMath or NCAlgebra, but niche.
7. **102, UGC (T3).** A worst-case ratio above α_GW (Max-Cut) or below 2 (Vertex Cover) from a quantum heuristic now implies NP ⊆ BQP. This changes how advantage claims are framed, nothing more.

## Audit of the prior analysis (all three claims rejected)
- **107, ω ≤ 9/4 → FLINT `nmod_mat_mul`: wrong.** The proof is non-constructive. It bounds Strassen's asymptotic spectrum and then takes "a fixed u and an exact rank decomposition of T_u", which is never computed. The paper says it "does not specify a competitive finite matrix size". The constructive companions (2.371055 over every field, 2.258 over ℂ) are laser-method constructions with N→∞ and "no practical crossover estimates". Do not feed 9/4 into crypto cost estimators either; conservative ones already use w=2.
- **109, integer multiplication → GMP, OpenSSL, CPython: wrong.** κ=2^-182. The parameter d=⌊(log n)^{2^-75}⌋ reaches 2 only at n ≥ 2^(2^(2^75)). The speedup at n=2^(2^64) bits is 1+10^-53. The model is a multitape Turing machine, and the result is not Lean-formalized.
- **121, edit distance → RapidFuzz: wrong.** It runs exact Wagner–Fischer dynamic programming whenever ℓ < 2^1000 (ℓ ≈ log log N). The approximation branch never runs for N < 2^(2^(2^999)), so a faithful implementation is just the quadratic dynamic program. RapidFuzz's bit-parallel Myers algorithm, edlib and WFA already dominate.
- **120, almost-linear general matching: galactic.** The o(1) term "has no convergence rate", and it inherits the never-implemented almost-linear max-flow machinery. LEMON, Boost and Blossom V are unaffected. It is not formalized.

## Other galactic or vacuous results
111 (prophet ratio 2^-310, no efficiency claim); 110 (k-server existential, computable version has an "enormous" additive term); 114 (U=N^61000); 103 (white-box simulation, no pseudorandom generator, compiler constant 2^{(u+100)²}). 105, 106, 108, 112 and 117 are pure hardness or lower-bound results.
