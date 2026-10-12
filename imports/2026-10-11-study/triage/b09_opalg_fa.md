# b09_opalg_fa (operator algebras 285–303, functional analysis 322–332): triage memo

I read the theorem statements of all 30 families and read the TeX in depth for 300, 325, 329, 330 and 332. Result: 1 at T2, 2 at T3, 27 at T4. This batch is pure mathematics. The landmark results are Lean-formalized (287, 288, 296) but have no applied consumer.

## Ranked opportunities

1. **325, complete Crouzeix (T2, CERTIFY).**
   - Sharp constant 2, Lean-formalized, with matrix coefficients.
   - Gain over 1+√2: scalar a-priori bounds get 17% tighter. The GMRES field-of-values bound goes 2.414→2 and the Arnoldi f(A)b constant 4.83→4. That saves about 0.19/|log ρ| iterations, roughly 1%.
   - The scalar constant 2 was also proved by humans in Aug 2026 (Lorist–Schwenninger 2608.03841, Jin, Luo). Only the complete version is unique to the drop.
   - Where the complete version matters: the Crouzeix–Kressner bivariate f{A,B} / Fréchet-derivative bound goes 5.83 (published) → 4.83 (human results) → 4, which is sharp; block-GMRES bounds with matrix polynomials also improve.
   - Targets: Low–Su App. B.2, and textbooks and docs.
   - Production codes are unaffected; they stop on a-posteriori estimates.

2. **332, metric Markov cotype of ℓ1 (T3, RESEARCH). Non-obvious channel.**
   - Makarychev–Makarychev (FOCS 2010, Cor 5.9) showed that a positive answer to Ball's question e(ℓ2,ℓ1)<∞ gives cut sparsifiers of quality O(√log k · log log k) on k terminals. This paper's Corollary is that answer.
   - Result: the existential bound improves from O(log k/log log k) to within (log log k)² of the Ω(√log k/log log k) lower bound. The paper does not notice this.
   - Caveats: existential only; galactic (log k ≳ 5500 before the unknown constant K); not Lean-formalized.

3. **329, metric-entropy duality counterexample (T3, REDIRECT).**
   - Lean-formalized.
   - It shows that the scale-dependent loss in Hu–Peale–Reingold's outcome-indistinguishability duality (ALT 2022) cannot become universal.
   - The bodies are tower-sized (h ≈ 10^477 at a=1), so they are useless as benchmark instances.

## Checked and rejected

- **300, paving.** The finite-dimensional content (frames, sparsification) was settled by MSS 2015 and Ravichandran–Srivastava 2017. This paper uses RS17 as a black box with a worse constant (5·10⁸ε⁻²) and extends it to diffuse masas, with only a strongly-small compression. Existential. The algorithmic Kadison–Singer work is in separate human preprints. T4.
- **330, Lipschitz-free / EMD.** For a finite metric the free space is finite-dimensional, and the identity is a norm-1 finite-rank map, so EMD sketching and embedding are unaffected. T4.
- **327, 331.** Qualitative statements about infinite-dimensional spaces. No new distortion number for any finite metric. T4.
- **324.** Infinite-dimensional; irrelevant to embeddings. T4.
- **288.** The universal constant is about 1.2·10⁶. The finite-dimensional cases used in quantum information were known with much better constants. T4.
- **296.** Baire-category argument; no explicit generator. T4.
- **328.** Zorn's-lemma proof by contradiction; Hilbert-space splitting methods were already covered. T4.
- **285.** Physics K-theory uses amenable groups, for which Baum–Connes is a theorem. Unformalized extraordinary claims. T4.
- **302.** Mean-dimension signal embeddings are untouched. T4.

## Overhype watch

- "Paving → frames" (300) and "Lipschitz-free → EMD" (330) are keyword matches with no content behind them.
- "Crouzeix → faster GMRES/expm" (325) is false. It tightens bound constants only, and the scalar half was also done by humans.
