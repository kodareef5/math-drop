# b07 — Differential geometry (333–361) and topology (304–321): triage memo

**Verdict:** 42 of 47 families are T4/FOUND. One is T2, four are T3, none is T1. None gives an algorithm with explicit constants.

## Ranked opportunities

1. **354, isoperimetric profile of the cubic 3-torus: T2 CERTIFY.**
   - Exact closed-form profile. Sphere, then cylinder, then slab, switching at exactly 4π/81 and 1/π; no other shape ever wins. Lean-formalized.
   - Finite-size coexistence analysis in periodic MC/MD boxes (Binder/MacDowell; Prestipino et al. PRE 2015) already uses these values, found by comparing only the three candidate shapes.
   - New: no other morphology (e.g. gyroid/Schwarz) can minimize area in a cubic cell.
   - Modest value. Elongated slab boxes, fluctuations and anisotropy are not covered. Not the Kelvin foam problem.

2. **360, weak MTW gives regular OT on manifolds: T3. Overhyped for applications.**
   - Squared-distance cost only. Exponent from a compactness argument, not explicit (paper says so). No algorithm.
   - Does not cover reflector-antenna or refractor costs, whose MTW theory is separate and older. Industrial freeform design does not use it.
   - Sphere, SO(3), tori and sphere products were already covered by Loeper, Loeper–Villani and Figalli–Kim–McCann. Gain at most for mixed products such as S²×T^k: one literature check.

3. **317, Thomason model structures: T3 FORMALIZE.** Not HoTT (strict, not weak, categories). The asset is about 160k lines of Lean 4 on Mathlib's `SSet.modelCategoryQuillen`, which could be upstreamed to Mathlib or infinity-cosmos with months of refactoring.

4. **312, Grothendieck homotopy hypothesis: T3.** No effect on Coq-HoTT, Cubical Agda or Lean. Niche channel: coherator type theories (CaTT, Brunerie), if their coherator fits the Ara–Henry convention. Only the elementary-expansion step is formalized.

5. **357, bi-Lipschitz charts at RCD regular points: T3, weak.** Like eigenfunction charts in manifold-learning theory, but chart radius unquantified and constant from compactness, so no sample-complexity statement.

## Requested checks that came back T4

- **343, symplectic packing.** In dimension ≥6 only volume and Gromov's two-ball bound constrain packing, so there is less rigidity. Applied phase-space work uses single-ball non-squeezing only.
- **346 (varifolds) and 355 (MCF).** Surface Evolver, varifold shape metrics and mesh smoothing do not depend on these regularity results.
- **350, nodal bounds.** Surface constant not explicit; 3–5D counterexamples need non-analytic, finely tuned metrics. Mesh segmentation and Laplacian encodings in GNNs work where √λ scaling was already known.
- **356/357, RCD spaces.** Not the graph Ricci curvatures used in ML.
- **307, coarse assembly.** Congruence SL₃(ℤ) graphs: no new expander, no TDA link.
- **337, CAT(0) fillings.** Phylogenetic tree space and robot cube complexes use geodesics and means, not isoperimetric constants.

## Geometric deep learning, mesh processing and robotics

Nothing actionable:
- **333/334, isometric immersions:** graphics and morphing sheets work in C¹ or analytic regimes.
- **351, Ricci flow:** applied versions are 2D discrete or graph flows.
- **Topology (304–321):** nothing touches configuration spaces or topological complexity.

## Overhyped or galactic

- **360:** the most "applied" title, but a non-quantitative theorem for a cost optics does not use.
- **347:** counterexamples in dimensions 22 and 3332.
- **340:** needs an unspecified large N.
- **Chromatic families (308, 309, 311, 313, 314, 316, 318, 319):** no applied reach.

**Repairs:** 342 (cone-equality claim corrected) and 341 (dependency removed) were revised on Oct 7. Neither is applied.
