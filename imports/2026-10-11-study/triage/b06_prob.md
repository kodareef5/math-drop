# b06_prob: probability and statistical mechanics (211–239)

**Bottom line:** 0 T1/T2, 7 T3, 22 T4. Most of this batch is landmark pure mathematics: critical percolation on Z^3 (213), Benjamini–Schramm (214), the O(3) quantum field theory (215), BKT (216), and SLE/CLE limits. It confirms physics practitioners already assume and computes no number anyone needs.

## Ranked opportunities

1. **238: Thorp shuffle mixes in Θ(log N) rounds** (T3, deep-dive, Lean).
   - **New:** the first full-security proof (all N queries) for a fixed-round, oblivious shuffle cipher. The Morris–Rogaway–Stegers Thorp bound stopped at q < N/(4 lg N), and Sometimes-Recurse needed variable time.
   - **Fewer rounds? No.** 1600·lg N shuffles are needed, plus a total-variation floor of about 9e7·N^{-3/2}. That is about 205k PRF calls for CCA at N=2^64, against about 1000 rounds for swap-or-not or Sometimes-Recurse. The floor is about 2^-19 at N=2^30, and only powers of two are covered.
   - **Unaffected:** NIST FF1/FF3-1 and Ethereum's `compute_shuffled_index`.
   - **Reusable asset:** the eight-block Fourier lift turns the image law of 7N/8 points into a full-permutation bound. With Hoang–Morris–Rogaway's swap-or-not bound as input, it appears to give full security at about 8× their rounds. That is my unchecked extrapolation.

2. **235: random k-SAT thresholds** (T3, REDIRECT).
   - **Hidden channel:** Var(H_n)=Θ(n) plus Wilson's bound gives a Θ(√n)-clause satisfiability window, i.e. ν=2. That contradicts the ν≈1.5 still quoted for random 3-SAT benchmarks; a CDCL sweep can check it.
   - **Computability is not practical.** The lower certificates (error 2^67·n^{-1/6}) say nothing until n>2^389. The upper certificates (interval-evaluated RSB trials) might beat 4.4898, but only theory cares.

3. **229: exact 3/4-state reconstruction thresholds** (T3).
   - The q=3 SBM weak-recovery threshold (a−b)²>3(a+2b) now holds at every degree.
   - **Hidden channel:** the 4-state ferromagnetic channel is Jukes–Cantor. Root-state reconstruction on deep regular trees is impossible iff p ≥ (3/4)(1−1/√d).
   - Limits: confirms existing practice, and the new direction is computer-assisted, not Lean.

4. **221 and 234: diluted Mézard–Parisi formula; invariant Ising pressure** (T3).
   - The hypotheses of 221 appear to admit the antiferromagnet, which would cover sparse Erdős–Rényi Max-Cut (needs checking).
   - 234 gives zero-temperature optima for Hopfield/Wishart QUBO and Gaussian vector balancing.
   - Possible use as reference values for Ising-machine, QAOA and AMP benchmarks (pairs with 281). Both are uncertified infima.

5. **227: SK Glauber dynamics.** Constant gap and cutoff throughout β<1, and n^{2/3} slowing at β=1. The rate λ(β) is implicit and the β>1 barriers are galactic. CERTIFY only.

6. **222: perceptron free energies and jamming exponents.** Rigorous Gardner formulas for soft losses at all densities. Capacity is excluded, so no ML practice changes.

## Overhyped or galactic

- **228:** the potential's core sits at scale e^{−t} for an unspecified large t. Not simulable, and silent on Lennard-Jones.
- **236 and 231:** no finitary coding radius (231 reads out Brownian limsups), so nothing for local, distributed or GNN algorithms.
- **239:** the exact singularity probability (about 2^-n) is not what numerical analysis or compressed sensing needs.
- **215 and 216:** the O(4) prefactor is the prediction lattice codes already use, and the XY amplitudes are not computed.
- **213:** historic, but gives no p_c, exponents or finite-size information.
- **232 and 233:** repaired on Oct 7; treat with caution.
