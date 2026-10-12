# Batch b02_tcs_b (families 122–142): triage memo

I read the TeX sources for all 20 families. Result: 1 at T2, 11 at T3, 8 at T4; nothing at T1. Almost every algorithm here is galactic or holds only in an idealized model.

## Ranked opportunities

1. **131: switch chain mixes for every degree sequence (T2, CERTIFY, deep-dive).**
   - Lean-formalized explicit constants: Var ≤ 2n²⟨f,Lf⟩, and H² ⪰ H for pair (Curveball) resampling.
   - Rescaled to chains people run:
     - a uniform-edge-pair swap chain that counts rejections has gap ≥ 1/(2n²m²);
     - undirected Curveball has gap ≥ 1/C(n,2) (observed 0.14–0.26 against bounds of 0.03–0.05).
   - **Non-obvious finding:** NetworkX `double_edge_swap` and `random_reference` loop until swaps *succeed*, so their stationary law is not uniform. Exhaustive checks on four small degree sequences give TV 0.023–0.029 from uniform and a 1.25–1.52× max/min probability ratio.
   - Action: add a lazy option to NetworkX; update the docs for NetworkX, igraph `rewire`, graph-tool and NetworKit. This affects every configuration-model null model.

2. **128: SCS 2-approximation (T3, BENCHMARK, deep-dive).**
   - The prior zstd mapping is wrong. COVER/FASTCOVER `memcpy` dmer-coverage segments chosen under a byte budget; the objective is coverage, not shortest superstring.
   - The useful artifact is the forced-occurrence lower bound W ≤ OPT (output ≤ 2W). It can certify greedy's gap on k-mer-set superstrings such as KmerCamel.
   - Feasible only for bounded-length inputs.

3. **142: deterministic F_p factoring (T3, REDIRECT only).**
   - **Not practical against Cantor–Zassenhaus.** The bound is O(((n+1)log p)^{10^12}).
   - The new curve/Jacobian machinery runs only when p > B^{200000} (primes of at least ~4.8 million bits).
   - For every prime used in practice it falls back to Berlekamp plus exhaustive search costing ~p trials, which is exponential in log p.
   - CZ's Las Vegas output is checkable, so determinism buys nothing.
   - The unconditional claim depends on the unformalized Hecke zero-free strip from family 029. The GRH-conditional polynomial bound improves on Evdokimov's quasipolynomial one.
   - Do not implement in FLINT, NTL or SymPy; fix docs and textbook statements only.

4. **140: memory–sample lower bound (T3, CERTIFY).** Streaming Kaczmarz/SGD regression is sample-optimal under o(d²) bits of memory.

5. **139, 138, 136: redirect theory communities only.**
   - 139: the dimension exponent of sampler query cost is 0, but only for condition number ≤2, with free computation between queries. Stan and BlackJAX are unaffected.
   - 138: refutes the 2^{n/2} Subset Sum hypothesis. **No crypto relevance:** attacks are average-case (~2^{0.29n}), and PQC parameters are set by lattice attacks.
   - 136: tightens Nash hardness under ETH-for-PPAD.

## Overhyped or galactic

- **130 (DFT):** the saving is (log n)^{2·10⁻¹³} ≈ 1+10⁻¹², swamped by a (log log n)⁴ overhead and 2^71-array blocks, in an exact-arithmetic model. The paper says there is "no useful crossover." **The FFTW/genfft mapping is keyword matching.** T4.
- **124:** this is Garey–Johnson OPEN8, P3|prec,p_j=1|Cmax (unit jobs, arbitrary DAG, no release dates). Runtime O(L^{150020}).
- **122:** the formalized n^{Ω(log log n)} lower bound shows uncoded worst-case reconstruction cannot be polynomial. DNA storage already uses codebooks. The decoder needs exp(C·351) traces at n=150, q=0.01.
- **133 (WL):** the unconditional exponent is 10⁻⁹k and needs k on the order of 10^6. The ETH version uses ~10^7-vertex graphs at k=4. Nothing changes for nauty or GNN practice.
- **125:** 1+2/e is tight, but the Li–Svensson enumeration n^{O(c/η)} is impractical.

## Pure (T4)

126, 129, 130, 132, 134, 135, 137, 141.
