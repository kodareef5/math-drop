# b11: analysis (071–086), convex/metric geometry (087–101), dynamics (143–154)

**Bottom line:** no T1s. 5 T2, 7 T3, 31 T4. Nearly everything is existential, and constants are missing or astronomically large.

## Ranked opportunities

1. **149, permanence for weakly reversible reaction networks (T2, CERTIFY).** With mass-action kinetics and any fixed positive rates, concentrations neither blow up nor go to zero. Tools already check the hypothesis (Catalyst.jl `isweaklyreversible`, CRNToolbox) but report no dynamics, so they can add a certificate valid for all rates. Lean-formalized (per-trajectory version). Caveats: bounds not explicit; check overlap with Craciun's GAC preprint.

2. **076, binary merit factors are unbounded (T2, REDIRECT; deep dive).** Turyn's conjecture is disproved, but the result is galactic:
   - the paper says "no useful convergence rate or efficient signing algorithm";
   - N0(η) is unspecified, so it beats no record (LABS optima N ≤ 66; F > 9 to N ≈ 250; 6.34 for explicit families).
   - **Action:** tell LABS/QAOA benchmark authors and radar/CDMA surveys to stop quoting a finite asymptotic optimum (Golay's 12.3).
   - **Side experiment:** use the proof's waveform-then-round pipeline as a solver seed at N = 10³–10⁴.

3. **101, sharp entropy bound for log-concave laws (T2, CERTIFY).** h ≥ m + ½ log det Cov gives a sharp 0.604 bits/dimension gap to Gaussian, for both noise capacity and the rate-distortion gap (previously ~1.05 bits). These corollaries are my own derivation and need checking.

4. **095, hyperbolicity cones without SDP lifts (T2, INSTANCES; deep dive).** An explicit 23-variable cone is not an SDP in its own variables but has an explicit 100×100 lift. Benchmark: native DDS/Hypatia solve vs the lift in MOSEK/Clarabel. Also a redirect: compiling every hyperbolic program to SDP is impossible. The truly non-liftable cone is enormous.

5. **090, triangular lattice is energy-optimal (T2, CERTIFY).** Proofs ship interval-arithmetic certificates. Sphere point-set benchmarks can quote the proven constant C_BHS, and vortex/Coulomb-crystal work can cite a theorem instead of numerics. All of this was already believed.

6. **T3s:**
   - **093:** a dimension-free log-Sobolev constant, giving Langevin-sampler mixing guarantees; constant not explicit.
   - **097:** Euclidean Steinitz O(√d) could shrink integer-programming dynamic programs, but C is not explicit, there is no algorithm, and existing bounds are comparable.
   - **089:** planar flow–cut gap is O(1), but the constant is about 10⁶⁰ or more; theory only.
   - **099, 098, 096:** "stop" results for theory; 096 depends on family 102.
   - **143:** at most 2 limit cycles when damping degree ≤ 4, so birhythmic models need degree ≥ 6.

## Non-obvious channels

- 076 → binary OFDM peak power (non-constructive).
- 101 → capacity and rate-distortion bounds.
- 095 → solver benchmark instances.
- 143 → oscillator modeling rule.

## Overhyped or galactic

- **094:** dimension exp((log n)^γ), no algorithm. p-stable sketches already do better; no effect on nearest-neighbour search.
- **092:** irrelevant to vector quantization; codes need only 2^{o(n)} covering density.
- **146:** k0 not given; physicists know the chaotic regime numerically.
- **Harmonic analysis (073–075, 077–080, 082, 083, 086):** pure. Kakeya and restriction are unformalized.

No family here depends on withdrawn or repaired manuscripts.
