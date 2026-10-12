# b08 Mathematical physics (260–284) and PDE (362–377): triage memo

**41 families: 0 T1, 8 T2, 10 T3, 23 T4.** Nothing here gives faster code. The value is in certified formulas, settled design questions and hardness results.

## Ranked opportunities
1. **273 Entropy photon-number inequality (T2, CERTIFY, deep-dive).** Proves a 2007 conjecture behind a family of conditional bosonic capacity theorems. It makes the multimode thermal-attenuator minimum output entropy and the pure-loss broadcast region unconditional. The paper does not claim wiretap or trade-off capacities, so the deep-dive should list every "conditional on EPnI" theorem (Guha–Shapiro–Erkmen, Wilde–Hayden–Guha) and check which ones close.
2. **276 Generalized amplitude-damping capacity (T2, CERTIFY).** Closed one-variable formula, Lean-formalized. It replaces the bounds in Khatri–Sharma–Wilde and Fang, and shows entangled inputs cannot help against thermal relaxation. Roughly a day of work.
3. **266 N(6)=3 MUBs (T2, CERTIFY, deep-dive).** Settles a design question for d=6 tomography and qudit QKD. **Provenance gap:** the cited `verification/code/` C++ sources and run archive are missing from the repo, and Lean proves only N(6)≤5. I ran the exact ≤5 verifier (87 s, output matches the paper). First get the pipeline and rerun it.
4. **374 Sharp W₂^{1/3} Brenier stability (T2, CERTIFY).** Fully formalized and sharp. It is the right worst-case guarantee for linearized-OT embeddings and Monge-map estimators (PyTransKit, pysdot, POT, OTT-JAX). The constant (about 96 on unit squares) certifies the exponent only.
5. **373 Coulomb Monge nonattainment (T2, INSTANCES).** SCE-DFT solvers cannot assume co-motion maps when N≥3. A discretized density makes a test case for multi-marginal Sinkhorn and GenCol.
6. **275 Continuum Coulomb QMA-hardness (T2, REDIRECT).** Worst-case ab initio energies are hard even with protons only and full continuum minimization. Useful for framing quantum-advantage claims in chemistry; no effect on codes.
7. **278 Kohn–Sham ensemble non-representability (T2, REDIRECT, deep-dive).** Analytic backing for observed density-inversion failures. The instance is unphysical (D=10^200), but the nodal-plane mechanism is generic. Check whether it applies to real open-shell atoms.
8. **274 Parity ∉ QAC⁰ (T2, REDIRECT).** Native multi-controlled-Z gates cannot replace fanout, so constant-depth GHZ needs feedforward or global-MS gates.

## Non-obvious channels
- 368: the proof shows injective piecewise-affine tetrahedral maps are dense, relevant to injectivity-constrained elasticity FEM. Energy convergence is not covered.
- 365: rough-conductivity nonuniqueness shows regularity priors are necessary in 3D EIT and ERT. The same-patch uniqueness result matches real electrode geometry.
- 281's companion makes Montanari's *classical* SK optimizer unconditional, so QAOA gains no advantage.
- 272: the PPT² disproof may unblock key-repeater no-go assumptions.

## Overhyped or galactic
- **265 2D area law and PEPS:** existence-only. Tensors are not constructible, the exponent is large and unspecified, and there is no efficient 2D algorithm. A deep-dive should look for an approximate-ground-state-projector (AGSP) route, not code.
- **277:** for CHSH at δ=0.1 the rate needs about 10¹¹ rounds for 10⁻¹⁰ soundness. Irrelevant to DIQKD, where entropy-accumulation (EAT) proofs rule.
- **279, 283:** nothing for Qiskit, tket or BQSKit. 279 disclaims practicality; 283's oracle is not constructed and its error is 1/2.
- **376:** the tape lives in exact reals, so there is no CFD undecidability. The box-transport paper was repaired on Oct 7.
- **268, 269:** confirm known physics. The Haldane bound is about 100× below the DMRG gap. No MBQC or topological-QC consequence.
- **362–364:** 362 only removes an assumption from convergence proofs (one species). 363 needs singular data that DSMC never meets.
- **262, 263:** no DFT consequence. The 3D γ=1 constant is unchanged, and C is not effective.
