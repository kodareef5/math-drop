# Chemistry / physics / biology theme: reaction-network permanence, Kohn–Sham and SCE representability, Coulomb QMA-hardness, lattice/torus/ionization certificates

Families: 149, 278, 373, 275, 090, 354, 263. Paper sources are pinned to openai/math commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` (dated 2026-10-07). Experiment code and outputs are in `/home/claude/work/repos/scratch_chemphysbio/`.

**Bottom line**

- **149 is the only one of the seven with a concrete software action.**
  - **What is new.** Every weakly reversible, mass-action network with fixed positive rates is bounded and persistent, and also permanent class by class. This holds for any number of linkage classes, any deficiency and any dimension, and the boundedness/persistence half is Lean-checked.
  - **Where it lands.** The right target is not `Catalyst.isweaklyreversible`. It is `CatalystNetworkAnalysis.ispersistent`, which today returns `:INCONCLUSIVE` for every weakly reversible network outside the Angeli–De Leenheer–Sontag siphon test. The repo's own TODO lists "permanence in networks".
  - **How often it matters.** In a scan of 702 curated BioModels, the existing siphon test was inconclusive on 177 of the 236 structurally weakly reversible networks, and every one of those 177 is non-conservative.
  - **Caveat.** Only 21 of the 236 have kinetics that verify as pure mass action. All 21 that the new theorem would decide were already decided by the siphon test, or are single-linkage or deficiency-zero.
  - **Verdict.** A cheap, correct structural rule worth a PR now, but its value is documentation and API completeness, not a new result on curated models.
- **278 (Kohn–Sham) and 373 (Monge/co-motion) are "stop assuming" results.**
  - 278's instance is an H₂⁺-like two-centre, three-electron molecule with Z specified only through a non-numeric supremum, using D = 10²⁰⁰.
  - 373's discrete instance is easy to build. I built it: an exact LP and multi-marginal Sinkhorn both recover the forced 50/50 branch split. The barycentric "read off a co-motion map" step overshoots by 13.8–41%, and the Hu–Chen–Liu product ansatz is not exact (+1.4% on 5 atoms, +0.4% on 35 atoms).
- **275 is a framing citation for quantum-advantage debates.** The instances have polynomially many unit nuclei, but the exponent is enormous, and the result only removes the fixed-basis loophole in O'Gorman et al.
- **090, 354 and 263 are certify-and-cite only.**

## What the papers actually prove

### 149 — Weakly reversible mass-action systems: boundedness, persistence, permanence (2 manuscripts; Lean: boundedness/persistence only)

**Boundedness and persistence** ([Thm 1.1, 01-introduction.tex L40-51](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Boundedness-and-persistence-of-weakly-reversible-mass-action-systems-September-25-2026/build/sections/01-introduction.tex#L40-L51)):
- **Statement.** Take any finite network, any d, any number of linkage classes, weak reversibility, and positive *constant* rates. For every x⁰ > 0 the solution is global, and ε ≤ xᵢ(t) ≤ 1/ε for all t ≥ 0.
- **The bound depends on x⁰.** ε depends on the network, the rates and x⁰.
- **Geometric form.** Each x⁰ lies in a compact convex forward-invariant polytope K ⊂ ℝ^d_{>0} ([Prop polytope, 03-dynamics.tex L327-333](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Boundedness-and-persistence-of-weakly-reversible-mass-action-systems-September-25-2026/build/sections/03-dynamics.tex#L327-L333)).
- **Corollaries:**
  - A positive equilibrium exists in every positive stoichiometric class. This re-proves Boros 2019 ([Cor positive-equilibrium L408](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Boundedness-and-persistence-of-weakly-reversible-mass-action-systems-September-25-2026/build/sections/03-dynamics.tex#L408-L435)).
  - **Global Attractor Conjecture (GAC) for complex-balanced systems.** Complex balance implies weak reversibility. Trapping in K ∩ (x⁰+S), the Horn–Jackson entropy and LaSalle then give convergence to the unique positive equilibrium ([Remark complex-balanced convergence, L437-461](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Boundedness-and-persistence-of-weakly-reversible-mass-action-systems-September-25-2026/build/sections/03-dynamics.tex#L437-L461)).
  - **So yes: the GAC (fixed rates) follows.** The paper presents it as recovering the conclusion "see also Craciun 2026".
- **Lean.** The trajectorywise statement is formalized as `global_bounded_persistent_solution`, with 71 files and 0 `sorry` ([Main.lean L73-84](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/MassAction/Main.lean#L73-L84); comparator statement [MassAction.lean L46-54](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/MassAction.lean#L46-L54)).

**Uniform permanence** ([Thm 1.1, introduction.tex L43-60](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/introduction.tex#L43-L60)):
- **Statement.** For every positive class P there is a compact convex forward-invariant set K_P ⊂ P that absorbs every trajectory starting in P. This gives a class-uniform ε_P with ε_P ≤ xᵢ(t) ≤ 1/ε_P after a transient that depends on x⁰.
- **Also on unbounded classes.** The result covers unbounded classes, i.e. open systems with inflow ∅→X, which matters below.
- **Not formalized.** This paper has no Lean formalization.
- **Constructive?** Only in form. h_P is chosen "sufficiently small" through an induction and compactness argument (trapping.tex L80-94), so no computable ε_P is given and no certificate size is stated.
- **Scope limits:**
  - Fixed rates only. Bounded time-varying rates are *not* claimed, whereas Gopalkrishnan–Miller–Shiu (GMS) 2014 and Craciun–Nazarov–Pantea (CNP) 2013 allow them.
  - Mass action only.

**Comparison with prior work:**
- **Craciun, arXiv 1501.02860.** v1 was posted in 2015; v3, dated 23 Sep 2026, proves that *bounded* trajectories of weakly reversible toric differential inclusions persist, and from that the GAC ([arXiv abstract](https://arxiv.org/abs/1501.02860)). The general weakly reversible persistence statement there *assumes* a trajectory bound.
- **What is new in 149.**
  - Boundedness for multi-linkage-class weakly reversible networks.
  - Unconditional persistence.
  - Classwise permanence.
- **Earlier partial results:**
  - Single linkage class: Anderson 2011 proved boundedness, and GMS 2014 (Gopalkrishnan, Miller and Shiu) proved permanence.
  - Two species: Craciun, Nazarov and Pantea 2013 (CNP 2013).
  - dim S = 2: Pantea 2012 proved persistence of bounded trajectories, and the GAC for dim S = 3.
  - The 2024 literature still described the GAC as conjectured, with only the single-linkage case proven ([arXiv 2409.04802](https://arxiv.org/pdf/2409.04802v1)).
- **Status of the GAC.** It now has two independent claimed proofs, Craciun v3 and 149's Remark. Neither is peer-reviewed. 149's boundedness half is machine-checked.
- **Prior error found.** The paper also points out a gap in the August–Barahona 2010 boundedness proof, with an explicit counter-example to an intermediate claim (01-introduction.tex L115-128).

**Triage check.** The triage was correct, with two corrections:
- The Lean formalization covers only the trajectorywise theorem, not permanence.
- The concrete engineering hook is `ispersistent` in CatalystNetworkAnalysis.jl, not `isweaklyreversible`.

### 278 — A Coulomb ground-state density with no Kohn–Sham ensemble representation (1 manuscript, not formalized)

- **Instance** ([Thm 1.1, main.tex L131-150](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Coulomb-Ground-State-Density-without-Kohn-Sham-Ensemble-Representation-September-25-2026/build/main.tex#L131-L150)):
  - 3 electrons and two equal nuclei of integer charge Z at ±(D/Z)e_z, with D = 10²⁰⁰. This is a 3D, full Coulomb system.
  - The absolute ground state sits in the S_z = 1/2 sector.
- **The claim.** No v ∈ L^{3/2} + L^∞ (real, spin-independent) and no ground-state ensemble of H_s(v) of any degeneracy reproduces its density.
- **The charge is not numeric.** Z = 2 + ⌈sup_{t∈(0,1]} t⁻¹ 𝟙_𝓑(t)⌉ ([Def exact-charge, 06-parameters.tex L268-278](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Coulomb-Ground-State-Density-without-Kohn-Sham-Ensemble-Representation-September-25-2026/build/sections/06-parameters.tex#L268-L278)). It is finite, but no numerical bound is given.
- **Why it is unphysical.** In scaled units this is a "stretched H₂⁺ plus one electron" system at separation 2·10²⁰⁰ Bohr/Z with weak electron repulsion λ = 1/Z.
- **Mechanism.** The leading Dyson (removal) amplitude has a nodal *median plane*. The ionic-channel coupling gives the density a slower λ·A(r)·r⁻⁴ tail on that plane.
  - Any representing local potential is forced to equal Δg/(2g) up to a constant.
  - If that potential were in L^{3/2}+L^∞, the plane trace of g would have to decay faster than it actually does. That is the contradiction.
- **Reusable fixed-density obstruction** ([Thm obstruction, 05-plane-obstruction.tex L358-372](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Coulomb-Ground-State-Density-without-Kohn-Sham-Ensemble-Representation-September-25-2026/build/sections/05-plane-obstruction.tex#L358-L372)). Its hypotheses are an odd angle θ with a weighted gap, the two orbital equations, and plane-tail asymptotics.
  - These are stated as fixed-parameter hypotheses, so in principle they can be checked for another density.
  - But they need exact asymptotics of the *exact* density on the nodal plane, which no numerical density supplies.
- **Functional consequence** ([Cor hxc-first-variation, 07-functional-consequence.tex L41-53](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Coulomb-Ground-State-Density-without-Kohn-Sham-Ensemble-Representation-September-25-2026/build/sections/07-functional-consequence.tex#L41-L53)):
  - T_ens has an empty 𝒱-subdifferential at this density.
  - E_Hxc has no local-potential first variation along all segments.
- **Not excluded:**
  - distributional potentials;
  - spin-dependent (spin-DFT) potentials;
  - nonlocal operators;
  - Moreau–Yosida regularized densities.

### 373 — Nonattainment of the three-marginal Coulomb Monge problem (1 manuscript; Lean: 3D Coulomb case)

- **Statement** ([Thm 1.1, introduction.tex L29-45](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/introduction.tex#L29-L45)):
  - There is a density ρ ∈ C_c^∞ with √ρ ∈ C_c^∞ whose three-marginal Coulomb optimum is attained by a Kantorovich plan. No pair of measure-preserving Borel maps attains it.
  - The Monge and Kantorovich infima are equal (Section infima).
  - The Riesz extension covers every s > 0 and every d ≥ 2 ([Thm riesz](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/riesz.tex#L16-L39)).
- **Construction.** Five small balls sit at 0, ±e₁, ±e₂. The certificate potential u satisfies c ≥ u⊕u⊕u, with equality exactly on two branch families (0, a_k, −a_k) ([Lemma local L21-46](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/local.tex#L21-L46), [Prop certificate L9-31](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/certificate.tex#L9-L31)).
- **The mass imbalance that blocks maps.** The centre carries mass 1/3 and each outer ball 1/6, so any map from the centre must split.
- **Constructive and explicit?** Yes: explicit up to "sufficiently small" radii and the choice of K. My numerical check shows K = 3 and radii up to about 0.1 work (Experiment C).
- **Physical status.** It is a member of the physical density class D₃ (n = 3ρ, √n ∈ H¹). It is *not* asserted to be the density of any molecule or external potential.
- **Prior status.** Friesecke stated the question open in Jan 2026; the paper cites this at introduction.tex L91.

### 275 — QMA-hardness of continuum Coulomb energy (2 manuscripts; Lean: both, including the source CMP hardness, 0 `sorry`)

- **Statement** ([Thm main, introduction.tex L91-100](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026/build/introduction.tex#L91-L100); input model [Table L62-83](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026/build/introduction.tex#L62-L83)). Deciding E₀ ≤ a vs E₀ ≥ b is QMA-hard under deterministic poly-time reductions, for:
  - the clamped-nuclei electronic Hamiltonian,
  - with all nuclear charges equal to 1,
  - at rational positions,
  - with N given in unary,
  - with E₀ the infimum over the *full spinful antisymmetric continuum*,
  - and thresholds separated by at least 1.
- **What is not claimed:**
  - QMA membership;
  - neutrality, binding, or any spectral gap.
- **What is new relative to prior work:**
  - Schuch–Verstraete 2009 needed local magnetic fields and designed potentials; their DFT corollary concerns the universal functional.
  - O'Gorman–Irani–Whitfield–Fefferman ([PRX Quantum 3, 020322 (2022)](https://arxiv.org/abs/2103.08215)) needed a *supplied finite orbital basis*. The present result removes the basis.
- **Galactic scales:**
  - Planar-mode scale k = ⌈C·n^A⌉ and dilation λ = 8k³/ρ, with A and C "sufficiently large absolute" constants ([implementation.tex L21](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026/build/sections/implementation.tex#L17-L24)).
  - Box half-width H = ⌈λ⁵⌉ ([density.tex L14](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/QMA-hardness-of-continuum-Coulomb-energy-with-unit-nuclear-charges-September-24-2026/build/sections/density.tex#L14)).
  - The background slab of density ρ is discretized into unit nuclei, each of mass 1/λ. The nucleus count is about ρ·|Ω|·λ ≳ λ¹¹·S ≈ n^{33A}.
  - So the instances are "hydrogen clouds", polynomial but astronomically large. Most nuclei form a background slab; they are not chemically meaningful sites.
  - **Hugely cationic.** There are only N = m electrons, one per encoded site, so the cluster carries total nuclear charge about n^{33A}. Nothing about it resembles a molecule.

### 090, 354, 263 — certificates

- **090.**
  - **Universal optimality of the triangular lattice in 2D** for all completely monotone functions of r² ([Thm universal, 01-uniform-gaussian-theorem.tex L31-41](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/build/sections/01-uniform-gaussian-theorem.tex#L31-L41)).
  - **Renormalized Coulomb energy:** the Sandier–Serfaty Abrikosov conjecture ([Thm main, L64-72](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Triangular-minimality-for-planar-Coulomb-renormalized-energy-September-23-2026/build/sections/01-introduction.tex#L64-L72)).
  - **BHS linear term for the sphere's log-energy** ([Cor bhs, L105-127](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Triangular-minimality-for-planar-Coulomb-renormalized-energy-September-23-2026/build/sections/01-introduction.tex#L105-L127)). The error is o(n) with no rate; the paper says explicitly that it gives no construction or algorithm.
  - **Verification.** Rigorous interval-arithmetic verifiers are shipped. I ran them (Experiment D).
- **354.**
  - The isoperimetric profile of the unit cubic 3-torus is min{(36π)^{1/3}v^{2/3}, 2√(πv), 2}, with v = min(V, 1−V) ([Thm intro:main, paper.tex L56-82](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-Isoperimetric-Conjecture-for-the-Cubic-Flat-Three-Torus-September-24-2026/build/paper.tex#L56-L82)).
  - Transitions are at 4π/81 ≈ 0.1551 and 1/π ≈ 0.3183, and the minimizers are completely classified. It is Lean-formalized.
- **263.**
  - **Molecular excess charge:** a molecule with M nuclei binds at most Z + C·M electrons, with C universal but **not numerical** ([Thm main, L34-43](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-excess-charge-for-Coulomb-molecules-and-the-outer-radius-of-neutral-atoms-September-24-2026/build/sections/01-introduction.tex#L34-L43)).
  - **Atoms:** universal two-sided bounds on the first ionization energy and on the radius of neutral atoms ([Cor first-ionization L80-90](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-excess-charge-for-Coulomb-molecules-and-the-outer-radius-of-neutral-atoms-September-24-2026/build/sections/01-introduction.tex#L80-L90)).
  - **Asymptotics:** Thomas–Fermi asymptotics for removing m electrons (Lean).

## Current practice & state of the art

**Reaction-network tools (149):**
- **Catalyst.jl** (`SciML/Catalyst.jl` @ `e9162784`):
  - **Weak reversibility.** `isweaklyreversible` checks strong connectivity of each linkage class ([network_analysis.jl L810-837](https://github.com/SciML/Catalyst.jl/blob/e9162784b4fc463af2ae250ecb09debf185365d8/src/network_analysis.jl#L810-L837)).
  - **Deficiency theorems.** `satisfiesdeficiencyzero` and `satisfiesdeficiencyone` ([L1349-1383](https://github.com/SciML/Catalyst.jl/blob/e9162784b4fc463af2ae250ecb09debf185365d8/src/network_analysis.jl#L1349-L1383)).
  - **Complex balance.** `iscomplexbalanced` uses the van der Schaft matrix-tree test ([L1126-1159](https://github.com/SciML/Catalyst.jl/blob/e9162784b4fc463af2ae250ecb09debf185365d8/src/network_analysis.jl#L1126-L1159)).
  - **Docs.** The CRNT docs page states the deficiency-zero theorem only as *local* asymptotic stability, and says nothing about boundedness, persistence or global convergence ([crn_theory.md L210-280](https://github.com/SciML/Catalyst.jl/blob/e9162784b4fc463af2ae250ecb09debf185365d8/docs/src/network_analysis/crn_theory.md#L210-L280)).
  - **Docstring bug.** The `isweaklyreversible` docstring example builds `sir` and then calls `subnetworks(rn)` (L817-822).
- **CatalystNetworkAnalysis.jl** (`SciML/CatalystNetworkAnalysis.jl` @ `cac50dd8`, "not quite release-ready"):
  - **The persistence test.** `ispersistent` implements only the Angeli–De Leenheer–Sontag 2007 test: conservative and no critical siphon gives `:PERSISTENT`; everything else is `:INCONCLUSIVE` ([persistence.jl L24-37](https://github.com/SciML/CatalystNetworkAnalysis.jl/blob/cac50dd89b5f2baf4d0d689ba3b4b58501382a45/src/persistence.jl#L24-L37)).
  - **Open TODO.** The file header lists "endotactic networks / permanence in networks" as TODO ([L1-4](https://github.com/SciML/CatalystNetworkAnalysis.jl/blob/cac50dd89b5f2baf4d0d689ba3b4b58501382a45/src/persistence.jl#L1-L4)).
  - **Test fixture.** The test suite pins `:INCONCLUSIVE` for the weakly reversible network 2A+B→C→A+2B→D→2A+B ([test/persistence.jl L64-76](https://github.com/SciML/CatalystNetworkAnalysis.jl/blob/cac50dd89b5f2baf4d0d689ba3b4b58501382a45/test/persistence.jl#L64-L76)).
  - **Message bug.** `networksummary` prints "This reaction network is persistent" for `:NOT_PERSISTENT` ([steadystates.jl L116-117](https://github.com/SciML/CatalystNetworkAnalysis.jl/blob/cac50dd89b5f2baf4d0d689ba3b4b58501382a45/src/steadystates.jl#L112-L120)).
- **CRNT4SBML** (PNNL @ `20406f45`, last commit Aug 2021):
  - Checks weak reversibility via networkx strong connectivity ([c_graph.py L872-896](https://github.com/PNNL-Comp-Mass-Spec/CRNT4SBML/blob/20406f452863f35f766b504fe2b3f3ab034b62fe/crnt4sbml/c_graph.py#L872-L896)).
  - Its deficiency-zero report prints only "precisely one equilibrium" ([low_deficiency_approach.py L94-141](https://github.com/PNNL-Comp-Mass-Spec/CRNT4SBML/blob/20406f452863f35f766b504fe2b3f3ab034b62fe/crnt4sbml/low_deficiency_approach.py#L94-L141)).
  - Its focus is multistationarity.
- **CoNtRol** (Donnell, Banaji, Johnston, Pantea):
  - Runs siphon-based persistence conditions and a mixed-integer linear program (MILP) for strong endotacticity ([Johnston–Pantea–Donnell, arXiv 1412.4662](https://arxiv.org/abs/1412.4662)).
  - Its wiki was last edited in 2015 ([reaction-networks.net/wiki/CoNtRol](https://reaction-networks.net/wiki/CoNtRol)).
- **CRNToolbox and ERNEST.** I did not inspect their code: CRNToolbox is a Windows binary, and ERNEST is a MATLAB toolbox. Both are deficiency- and multistationarity-oriented.
- **BioModels / ODEbase.** ODEbase computes deficiency and a mass-action heuristic for 662 of the then-1044 curated models, but does not report weak reversibility ([ODEbase, PMC9710575](https://pmc.ncbi.nlm.nih.gov/articles/PMC9710575)). I found no published count of weakly reversible curated models, so I made one (Experiment A).

**DFT representability (278):**
- **Numerical failures of noninteracting v-representability:**
  - Trushin–Erhard–Görling ([PRA 110, L020802 (2024)](https://cris.fau.de/publications/327055796)) inverted full-CI and coupled-cluster densities of open-shell p-block atoms.
  - Except for N and P, the inversion converged only to *Aufbau-violating* occupations.
  - Erhard–Trushin–Görling ([JCP 162, 034116 (2025)](https://cris.fau.de/publications/334083596)) found that only the fully (space- and spin-) symmetrized formalism avoids Aufbau violations in all their cases.
  - Their cases are *atoms*. The obstruction there is symmetry and occupation pattern, not a nodal-plane tail.
- **Nodal-plane asymptotics.** The asymptotic mechanism was proposed by Gori-Giorgi–Gál–Baerends ([arXiv 1109.2204](https://arxiv.org/abs/1109.2204)) and Gori-Giorgi–Baerends 2018 ([arXiv 1804.00475](https://arxiv.org/abs/1804.00475)).
  - Either the density decays differently on a HOMO nodal plane, or the KS potential is irregular or divergent there.
  - Della Sala–Görling ([JCP 116, 5374 (2002)](https://cris.fau.de/publications/108574884)) found direction-dependent asymptotic limits of the exact-exchange potential in molecules.
- **Inversion software.**
  - n2v (Wasserman group @ `64592d1b`, last commit 2022) uses Aufbau occupation: `diagonalize` occupies the lowest `ndocc` orbitals ([inverter.py L197-225](https://github.com/wasserman-group/n2v/blob/64592d1bf56b77c5035b79d92198f33b24b55624/n2v/inverter.py#L197-L225)).
  - On non-convergence it raises "try a different initial guess" ([wuyang.py L56-60](https://github.com/wasserman-group/n2v/blob/64592d1bf56b77c5035b79d92198f33b24b55624/n2v/methods/wuyang.py#L56-L60)).
- **Who relies on ensemble v-representability:**
  - Gross–Oliveira–Kohn (GOK) ensemble DFT for excited states ([Gould, Kronik, Pittalis and collaborators; Cernatic et al., arXiv 2109.04943](https://arxiv.org/abs/2109.04943)).
  - Fractional-occupation and ensemble methods: REKS/SSR (in [DFTB+](https://dftbplus-recipes.readthedocs.io/en/stable/reks/introduction.html), TeraChem, GAMESS) and ensemble-KS.
  - Exact-functional and density-inversion studies.
  - The review by Penz et al. ([arXiv 2211.16627](https://arxiv.org/abs/2211.16627)) treats 3D ensemble v-representability as open; 278 settles it negatively for the L^{3/2}+L^∞ potential class.

**Multi-marginal Coulomb optimal transport (OT) / strictly correlated electrons (SCE) numerics (373):**
- **Mainstream SCE.** SCE functionals use co-motion functions (a Monge ansatz). These are exact in 1D and for N = 2 ([Seidl et al., arXiv 1702.05022](https://arxiv.org/abs/1702.05022)).
- **Kantorovich-dual solvers.** Mendl–Lin solve the Kantorovich dual ([arXiv 1210.7117](https://arxiv.org/abs/1210.7117)). Benamou–Carlier–Nenna use multi-marginal Sinkhorn ([chapter](https://cvgmt.sns.it/media/doc/paper/3102/chapter_DFT_Benamou_Carlier_Nenna.pdf)).
- **Sparsity-based solvers.** Friesecke–Schulz–Vögler's genetic column generation (GenCol) exploits the O(ℓN) sparsity of Kantorovich plans ([arXiv 2103.12624](https://arxiv.org/abs/2103.12624)).
- **The Monge-like product ansatz.** Hu–Chen–Liu ([SISC, doi 10.1137/21M1455164](https://arxiv.org/abs/2110.07352)) parametrize γ = (ρ/N)·γ₂(r₁,r₂)···γ_N(r₁,r_N), i.e. conditionally independent given r₁. They state that it is *unknown* whether Coulomb MMOT has a minimizer of this form, and they recover maps by barycentric averaging.
- **POT.** POT (@ `604c47f2`) has only a 1D Monge multi-marginal solver, `dmmot_monge_1dgrid_loss` ([dmmot.py L60](https://github.com/PythonOT/POT/blob/604c47f28770eda10fe3cf0023c946d19c28e7ca/ot/lp/dmmot.py#L60-L64)). No Coulomb MMOT solver ships there.

**Quantum-chemistry complexity (275):**
- **The prevailing view.** [Lee et al., Nat. Commun. 14 (2023)](https://research.google/pubs/evaluating-the-evidence-for-exponential-quantum-advantage-in-ground-state-quantum-chemistry/) found no evidence of *generic* exponential quantum advantage for ground-state chemistry.
- **Prior hardness results.**
  - Schuch–Verstraete ([arXiv 0712.0483](https://arxiv.org/abs/0712.0483), Nat. Phys. 5, 732 (2009)): Hubbard model with fields, with a DFT-functional corollary.
  - O'Gorman et al. 2022: hardness in a fixed basis.
- **Guided local Hamiltonian results** (Gharibian–Le Gall, [arXiv 2111.09079](https://arxiv.org/abs/2111.09079)) show that BQP-completeness *with a good guiding state* is where quantum advantage claims actually live.

**Lattices, tori, atoms (090/354/263):**
- **090.** Cohn–Kumar–Miller–Radchenko–Viazovska proved universal optimality in dimensions 8 and 24 ([Annals 2022](https://annals.math.princeton.edu/2022/196-3/p03)). Dimension 2 was open until 090.
- **The BHS constant.** Bétermin–Sandier showed it is equivalent to triangular minimality of the renormalized energy ([arXiv 1404.4485](https://arxiv.org/abs/1404.4485)).
- **354.** Prestipino et al. derived the 4π/81 and 1/π droplet → cylinder → slab crossovers by comparing three candidate shapes. They classified other shapes found in simulation as metastable ([arXiv 1509.02324](https://arxiv.org/abs/1509.02324), PRE 92, 022141).

## Opportunities

### chemphysbio-1 — Add a weak-reversibility/mass-action branch to `CatalystNetworkAnalysis.ispersistent` (and a permanence flag)

- **Proposed change** in `CatalystNetworkAnalysis.jl/src/persistence.jl`, inside `ispersistent` ([L24-37](https://github.com/SciML/CatalystNetworkAnalysis.jl/blob/cac50dd89b5f2baf4d0d689ba3b4b58501382a45/src/persistence.jl#L24-L37)), before the `:INCONCLUSIVE` return:
  ```julia
  if all(r -> ismassaction(r, rs), reactions(rs)) && isweaklyreversible(rs, subnetworks(rs))
      return :PERSISTENT   # bounded + persistent + classwise permanent for all positive constant rates
  end
  ```
  - Document the reference: OpenAI 2026 "Boundedness and persistence…" (Lean-checked) plus "Uniform permanence…".
  - State the limit: it holds for constant rates only, not time-varying rates.
  - Optionally add `ispermanent(rs)` returning `:PERMANENT` under the same condition. That fills the "permanence in networks" TODO (L3).
  - Fix the swapped `:NOT_PERSISTENT` message in `steadystates.jl` (L116-117).
- **Catalyst.jl docs.** Add one paragraph to `crn_theory.md` after L280.
  - Weak reversibility plus mass action implies bounded, persistent and permanent dynamics, for all rates.
  - With deficiency zero, the deficiency-zero equilibrium is *globally* attracting within its class: GAC, with the citations to Craciun 1501.02860v3 and 149.
  - Fix the `isweaklyreversible` docstring (`sir` vs `rn`, L817-822).
- **Changed tests.**
  - Flip the fixture at `test/persistence.jl` L64-76 (2A+B→C→A+2B→D→2A+B) from `:INCONCLUSIVE` to `:PERSISTENT`, but only if the rates are mass action, which they are in the DSL.
  - My siphon check confirms this network is conservative with two critical siphons {B,C,D} and {A,C,D}, deficiency 0. ADS07 *cannot* decide it.
  - Note it is single-linkage and deficiency-zero, so it was already persistent by Anderson 2011 / GMS 2014. The new theorem is not needed for this particular fixture.
- **New test, decided only by 149.** I found this by random search (Experiment B):
  `0 → X1+X2 → X0+X1 → 0`, `2X1 → 2X2 → X0 → 2X1`.
  - Two linkage classes, deficiency 1, dim S = 3, open (non-conservative), so ADS07 is inconclusive.
  - Simulation at 30 random log-uniform rate sets and initial states stays in [2.6·10⁻², 1.9·10³] for t ∈ [1500, 3000].
- **Benefit (guarantee, not speed).**
  - Users of Catalyst's network-analysis stack get a correct, rate-independent persistence/permanence verdict for a large structural class that currently returns `:INCONCLUSIVE`.
  - It also replaces "locally asymptotically stable" with "globally attracting in class" for deficiency-zero networks.
- **Measurement:**
  - Fraction of `:INCONCLUSIVE` verdicts eliminated on a benchmark set.
  - Correctness spot checks by simulation.
  - On BioModels the structural effect is large (177 of 236 weakly reversible networks are ADS07-inconclusive), but the mass-action-qualified effect is about zero (Experiment A).
- **Risks:**
  1. The theorem is unrefereed, and the permanence half is unformalized. Cite the Lean-checked boundedness/persistence as the conservative claim and permanence as "claimed".
  2. `ismassaction` in Catalyst is syntactic. It returns true for any rate that does not depend on species ([reactionsystem_conversions.jl L358-394](https://github.com/SciML/Catalyst.jl/blob/e9162784b4fc463af2ae250ecb09debf185365d8/src/reactionsystem_conversions.jl#L358-L394)), but time-dependent rates are already excluded there (L381-383). Good.
  3. Constant and boundary species are filtered from complexes ([filter_constspecs L27](https://github.com/SciML/Catalyst.jl/blob/e9162784b4fc463af2ae250ecb09debf185365d8/src/network_analysis.jl#L27-L30)). That matches the theorem's convention: they act as rate multipliers.
  4. Maintainers may prefer to wait for refereeing.
- **First step.** Open an issue on CatalystNetworkAnalysis.jl with the two-line rule, the two test networks and the citations. Then send the PR together with the message-bug fix.

### chemphysbio-2 — BioModels scan: report weak reversibility and the persistence/GAC certificate in curated-model metadata (ODEbase-style)

- **What I measured (Experiment A).**
  - About 40% of curated reaction networks are *structurally* weakly reversible: 236 of 597, or 194 with rate-law-aware reversibility.
  - But the theorem needs mass action. Only 21 weakly reversible models verify as pure mass action, and 13 of those are also free of events and rules.
  - For curated systems-biology models the certificate is therefore mostly inapplicable as written. Michaelis–Menten/Hill rate laws dominate.
- **Possible value:**
  - ODEbase/BioModels could add a "WR + mass-action → permanent, GAC if δ = 0" flag, which is cheap.
  - Molecular-programming compilers (DNA strand displacement) emit exact mass-action CRNs, where the certificate is directly applicable.
- **Who benefits:** model curators and ODEbase.
- **Measurement:** the number of models flagged.
- **Risk:** the low applicable count (about 3% of networks).
- **Verdict:** monitor or low priority.

### chemphysbio-3 — 373 as a regression instance for multi-marginal Coulomb OT solvers, and a warning on the "Monge-like" product ansatz and barycentric map extraction

- **Proposed change.** Ship the five-ball instance as a small, exactly solvable test case.
  - **Known values.** The exact LP value equals the certificate dual 3·Σμᵢu(pᵢ). The optimum splits each centre atom 50/50 between the two branches.
  - **Test content:**
    - (a) Kantorovich solvers (LP, Sinkhorn, GenCol) must reproduce the value and the split.
    - (b) Map-based or product-ansatz solvers must be documented as giving strictly higher energy on it.
    - (c) "Co-motion functions" read off by barycentric projection must be flagged as non-optimal.
- **Targets:**
  - the Hu–Chen–Liu global-optimization code (SISC 2023);
  - GenCol (Friesecke group);
  - multi-marginal Sinkhorn implementations;
  - POT has no Coulomb MMOT yet, so a POT example or test is a natural home.
- **Evidence (Experiment C):**
  - LP = dual certificate to 4·10⁻¹⁶.
  - Sinkhorn at ε = 0.01 reproduces the 0.5/0.5 split.
  - The product ansatz bottoms out 1.4% above optimum on 5 atoms and 0.4% on 35 atoms.
  - Barycentric maps cost +13.8% from the LP plan and +41% when restricted to the centre atoms.
- **Benefit:** guarantee and instances. Solver authors get a certified non-Monge benchmark in 3D.
- **Risks:**
  - SCE practitioners care about atoms and molecules. The SCE *energy* (the infimum) is unaffected, and the bad instance is artificial: no known external potential realizes it.
  - Impact is limited to method-validation sections of papers.
- **First step.** Release the 60-line instance builder (`monge373_lp.py`) and the result JSON. Contact the Friesecke, Nenna and Hu–Chen–Liu groups.

### chemphysbio-4 — 278: redirect inversion and ensemble-DFT practice (documentation-level), plus a research test of the nodal-plane mechanism in real open-shell systems

- **Proposed change.** Add a note to density-inversion tools that non-convergence or Aufbau violation can be genuine non-representability, not a bad initial guess.
  - n2v raises "try a different initial guess" (wuyang.py L56-60) and assumes Aufbau occupation (inverter.py L197-225).
  - Suggested remedies to document:
    - symmetrized inversion (Erhard–Trushin–Görling 2025);
    - Moreau–Yosida regularization;
    - reporting the regularization-dependence of v_xc.
- **Benefit:** redirect. Fewer wasted inversion runs, and correct interpretation of reference v_xc potentials used to train ML functionals.
- **Research part.** Do real molecules with a HOMO nodal plane extending to infinity satisfy the obstruction's hypotheses?
  - Candidates: π-radicals such as the allyl or benzene cation, and the B or O p-shell atoms in a reduced-symmetry ensemble.
  - The needed input is the exact-density tail on the plane, which requires full-CI-quality densities with correct asymptotics. That is hard, and is the reason this remains research.
- **Risks:**
  - The certified instance is unphysical (D = 10²⁰⁰, non-numerical Z).
  - It covers L^{3/2}+L^∞ only; practical inversions on finite bases always return *some* potential.
  - The TEG24 atomic failures have a different mechanism (symmetry and occupation), so 278 does not explain them.
- **Verdict:** pursue as research, low priority.

### chemphysbio-5 — 275: cite in quantum-advantage and complexity framing (REDIRECT, documentation)

- **Change.** In reviews and resource-estimation papers, cite 275 as the basis-free, unit-charge, all-spin-sector version of electronic-structure QMA-hardness. Generic ab initio ground-state energy estimation, even for clouds of protons in the continuum, is QMA-hard.
- **What it does *not* change.**
  - Lee et al.'s argument is about *typical* chemistry and state preparation, not worst-case complexity.
  - The hard instances have about n^{33A} unit nuclei, mostly a background slab, with only polynomially many electrons. They are hugely cationic, so no chemist will meet them.
- **Benefit:** it closes a frequently raised loophole ("hardness only arises from the basis truncation").
- **Risk:** over-reading it as evidence against quantum advantage for real molecules.
- **Verdict:** monitor or cite.

### chemphysbio-6 — 090/354/263 certificate citations

- **090.**
  - 2D colloid, Wigner, Abrikosov and Yukawa simulations can cite a ground-state theorem for completely monotone potentials (Gaussian core, Yukawa, Coulomb-renormalized).
  - Point-set designers can use C_BHS as the asymptotic target. My L-BFGS-optimized point sets approach it: gap 0.0056 → 0.0024 from n = 100 to n = 1600.
  - The verifier runs cleanly (37,310 Bernstein checks plus 10 tail checks, 15 minutes).
  - No algorithmic gain.
- **354.**
  - Finite-size coexistence studies in *cubic* boxes can cite the sphere/cylinder/slab sequence and the 4π/81, 1/π crossovers as exact for the isotropic sharp-interface model.
  - Production slab simulations use elongated boxes, which are not covered.
- **263.**
  - The constant C is not numerical, so there is no engineering consequence.
  - Cite in mathematical-physics surveys only.

## What is NOT an opportunity here

- **Faster CRN analysis from 149.** There is no algorithm and no computable ε_P. The trapping polytope is not a usable certificate output, because h_P is chosen by compactness.
- **Implementing a "persistence certificate" object** (a polytope) in Catalyst. Do not pursue: there is no effective construction.
- **"149 settles BioModels dynamics."** It does not. Only about 3.5% of curated networks (21 of 597) are both weakly reversible and pure mass action. For all 13 clean ones, the classical ADS07 siphon test or older theorems already give persistence.
- **Using 278's instance as a DFT benchmark.** D = 10²⁰⁰ and Z is non-numerical. No quantum-chemistry code can represent it. Instead, the mechanism (a nodal-plane tail) should be tested on real open-shell π systems.
- **Telling ensemble-DFT (GOK, REKS) users their methods are invalid.** Their working equations do not need exact representability of *every* Coulomb density: they work with approximate functionals in finite bases. 278 removes only the exact-theory guarantee.
- **Replacing co-motion SCE functionals** for atoms and molecules. The SCE energy is the infimum and is unaffected. Radial SCE solutions for spherical atoms are a separate question already studied by Seidl et al.
- **275 as a statement about real molecules or about BQP.** It is worst-case, membership is not shown, and the instances are galactic.
- **090/354/263 as algorithmic or design inputs.** The sphere result is asymptotic with no rate. 354 is cubic-only. 263's C is not numerical.

## Experiment results

All code is in `/home/claude/work/repos/scratch_chemphysbio/`. Python 3.13, libsbml 5.21, SciPy 1.18 HiGHS.

**A. BioModels weak-reversibility scan** (`scan_wr.py`, `wr_struct_persist.py`, `cb_check.py`, `wr_kinetic.py`).
- **Data.** Curated SBML from the sys-bio/temp-biomodels mirror @ `6a09daf4`: 702 models, BIOMD0000000001–0734. The EBI API was unreachable from this sandbox.
- **Conventions.** Boundary and constant species were dropped. SBML `reversible` flags were used for directions.

| quantity | count |
|---|---|
| models with a reaction network | 597 |
| structurally weakly reversible (SBML flags) | 236 (39.5%) |
| weakly reversible with rate-law-aware directions (reverse term present) | 194 |
| all reactions verified mass action (symbolic check) | 76 |
| weakly reversible **and** mass action | 21 (13 with no events or rules) |
| …complex-balanced at curated rates | 10 of 21 (all deficiency 0; the 5 models with assignment rules could not be checked reliably) |
| weakly reversible networks where the ADS07 siphon test is conclusive | 59 of 236 |
| ADS07-inconclusive (all because non-conservative) | 177 |
| …of which multi-linkage, deficiency > 0 (only 149 decides) | 34 structurally (19 rate-law-aware) |
| …of those 34, verified mass action | **0** (max mass-action fraction 48%) |

All 8 mass-action, weakly reversible, multi-linkage clean models are conservative and pass ADS07: BIOMD 002, 038, 085, 086, 500, 501, 629 and 692.

**B. Random weakly reversible networks** (`random_wr2.py`, 591 networks; 4–6 species, molecularity ≤ 2, 1–3 cyclic linkage classes, closed and open). This is a synthetic-population view of what each theorem decides:

| covered by | share |
|---|---|
| ADS07 siphon test (conservative, no critical siphon) | 24.0% |
| single linkage class (Anderson / GMS) | 13.9% |
| dim S ≤ 2 (Pantea / CNP) | 6.1% |
| multi-linkage deficiency 0 (bounded by Horn–Jackson; persistence = GAC, Craciun v3) | 40.4% |
| **only the new 149 theorem** (multi-linkage, δ > 0, dim S ≥ 3) | **15.6%** |

- **Minimal example and the existing fixture.** The minimal example is the chemphysbio-1 test network. The CatalystNetworkAnalysis INCONCLUSIVE fixture has 2 critical siphons and δ = 0.

**C. 373 five-ball instance** (`monge373.py`, `monge373_lp.py`, `monge373_sk2.py`, `product_ansatz373*.py`).
- **Lemma local with K = 3.** The sampled supporting inequality c − u⊕u⊕u ≥ 0 holds for all radii ≤ 0.10 and fails at 0.15. "Sufficiently small" therefore means about 0.1 in units where the centre-to-outer distance is 1.
- **Results:**

| atoms | LP optimum | dual certificate | branch split | Sinkhorn ε=0.01 (gap, split) | barycentric map cost | product ansatz best |
|---|---|---|---|---|---|---|
| 5 | 2.500000 | 2.500000 | 0.5/0.5 | −4e-6, 0.5/0.5 | 2.845 (+13.8%); centre-only 3.536 (+41%) | 2.5345 (+1.38%) |
| 35 | 2.499666 | 2.499666 | 0.5/0.5 all 7 centre atoms | +3.2e-4, 0.5/0.5 | 2.845 (+13.8%) | 2.5096 (+0.40%) |
| 40 | 2.499637 | 2.499637 | 0.5/0.5 all 8 | +3.4e-4 | 2.845 (+13.8%) | not run |

- **Why the product ansatz loses.** It forces the two outer electrons to be conditionally independent given the centre, so it puts mass on mismatched (0, a₁, −a₂) triples, which cost 2 + 1/√2 > 5/2.
- **Discrete Monge maps.** On 5 atoms the best measure-preserving discrete map costs 334.6. The atom masses make every map collide, which is the discrete shadow of the theorem.

**D. 090 verifiers** (copied to `tri090/`, python-flint 0.9.0).
- `arithmetic_bounds.py`: "All scalar assertions certified" (0.7 s).
- `numeric_balls.py`: 37,310 Bernstein comparisons plus 10 tail comparisons certified with strict Arb balls (885 s).
- **Sphere log-energy** (`sphere_log.py`). (E − lead)/n for L-BFGS-optimized points was −0.04999 (n=100) → −0.05323 (n=1600), against C_BHS = −0.055605. The gap shrinks slowly (0.0056 → 0.0024), consistent with the theorem and with its o(n) error having no rate.

**Not run:**
- No Julia toolchain was available, so the Catalyst PR was not executed. The decision logic was emulated in Python with identical rules.
- 278 and 275 instances cannot be computed: Z is non-numerical and the nucleus counts are galactic.

## Sources

- openai/math @ `fd4aeeb2` (papers and Lean, as linked above).
- [Craciun, Toric differential inclusions and a proof of the GAC, arXiv 1501.02860 (v3 23 Sep 2026)](https://arxiv.org/abs/1501.02860)
- [Anderson, A proof of the GAC in the single linkage class case, arXiv 1101.0761](https://arxiv.org/pdf/1101.0761)
- [Pantea, On the persistence and global stability of mass-action systems, arXiv 1103.0603](https://arxiv.org/abs/1103.0603)
- [Craciun–Nazarov–Pantea, Persistence and permanence of mass-action and power-law systems, arXiv 1010.3050](https://arxiv.org/pdf/1010.3050)
- [Johnston–Pantea–Donnell, computational approach to persistence/permanence/endotacticity, arXiv 1412.4662](https://arxiv.org/abs/1412.4662)
- [Angeli–De Leenheer–Sontag, Petri net approach to persistence, arXiv q-bio/0608019](https://arxiv.org/pdf/q-bio/0608019)
- [Realizations through weakly reversible networks and the globally attracting locus, arXiv 2409.04802](https://arxiv.org/pdf/2409.04802v1)
- [CoNtRol wiki](https://reaction-networks.net/wiki/CoNtRol)
- [ODEbase, PMC9710575](https://pmc.ncbi.nlm.nih.gov/articles/PMC9710575)
- [Catalyst CRNT docs](https://docs.sciml.ai/Catalyst/dev/network_analysis/crn_theory/)
- [Trushin–Erhard–Görling, PRA 110 L020802 (2024)](https://cris.fau.de/publications/327055796)
- [Erhard–Trushin–Görling, JCP 162 034116 (2025)](https://cris.fau.de/publications/334083596)
- [Gori-Giorgi–Gál–Baerends, arXiv 1109.2204](https://arxiv.org/abs/1109.2204)
- [Gori-Giorgi–Baerends, arXiv 1804.00475](https://arxiv.org/abs/1804.00475)
- [Della Sala–Görling, JCP 116 5374 (2002)](https://cris.fau.de/publications/108574884)
- [Penz et al., structure of density–potential mapping, arXiv 2211.16627](https://arxiv.org/abs/2211.16627)
- [Ensemble DFT of neutral and charged excitations, arXiv 2109.04943](https://arxiv.org/abs/2109.04943)
- [DFTB+ REKS recipes](https://dftbplus-recipes.readthedocs.io/en/stable/reks/introduction.html)
- [n2v Wu–Yang docs](https://n2v.readthedocs.io/en/latest/invert/wu_yang.html)
- [Friesecke–Schulz–Vögler, Genetic column generation, arXiv 2103.12624](https://arxiv.org/abs/2103.12624)
- [Hu–Chen–Liu, Global optimization approach for Coulomb MMOT, arXiv 2110.07352 / SISC](https://arxiv.org/abs/2110.07352)
- [Benamou–Carlier–Nenna, DFT chapter](https://cvgmt.sns.it/media/doc/paper/3102/chapter_DFT_Benamou_Carlier_Nenna.pdf)
- [Mendl–Lin, Kantorovich dual for SCE, arXiv 1210.7117](https://arxiv.org/abs/1210.7117)
- [Seidl et al., SCE functional for spherically symmetric systems revisited, arXiv 1702.05022](https://arxiv.org/abs/1702.05022)
- [O'Gorman–Irani–Whitfield–Fefferman, arXiv 2103.08215 (PRX Quantum 3 020322)](https://arxiv.org/abs/2103.08215)
- [Schuch–Verstraete, arXiv 0712.0483 (Nat. Phys. 5 732)](https://arxiv.org/abs/0712.0483)
- [Lee et al., Evaluating the evidence for exponential quantum advantage, Nat. Commun. 14 (2023)](https://research.google/pubs/evaluating-the-evidence-for-exponential-quantum-advantage-in-ground-state-quantum-chemistry/)
- [Gharibian–Le Gall, Dequantizing QSVT, arXiv 2111.09079](https://arxiv.org/abs/2111.09079)
- [Cohn et al., Universal optimality of E8 and Leech, Annals 2022](https://annals.math.princeton.edu/2022/196-3/p03)
- [Bétermin–Sandier, arXiv 1404.4485](https://arxiv.org/abs/1404.4485)
- [Prestipino et al., Shapes of a liquid droplet in a periodic box, arXiv 1509.02324](https://arxiv.org/abs/1509.02324)
- Code pins:
  - [SciML/Catalyst.jl @ e9162784](https://github.com/SciML/Catalyst.jl/tree/e9162784b4fc463af2ae250ecb09debf185365d8)
  - [SciML/CatalystNetworkAnalysis.jl @ cac50dd8](https://github.com/SciML/CatalystNetworkAnalysis.jl/tree/cac50dd89b5f2baf4d0d689ba3b4b58501382a45)
  - [PNNL CRNT4SBML @ 20406f45](https://github.com/PNNL-Comp-Mass-Spec/CRNT4SBML/tree/20406f452863f35f766b504fe2b3f3ab034b62fe)
  - [wasserman-group/n2v @ 64592d1b](https://github.com/wasserman-group/n2v/tree/64592d1bf56b77c5035b79d92198f33b24b55624)
  - [PythonOT/POT @ 604c47f2](https://github.com/PythonOT/POT/tree/604c47f28770eda10fe3cf0023c946d19c28e7ca)
  - [sys-bio/temp-biomodels @ 6a09daf4](https://github.com/sys-bio/temp-biomodels/tree/6a09daf46af1bb89e4857436b623a7b8720863ad)
- Note: the web-search budget ran out late in the task. The CRNToolbox and ERNEST internals and the GOK production-code inventory were not checked further.
