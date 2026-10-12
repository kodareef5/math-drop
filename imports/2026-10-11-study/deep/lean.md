# The Lean formalization layer: what it certifies, where it stops, and what to do with it

**Bottom line.** Inside its scope, the Lean layer is unusually clean. Across 26.1M lines (122,458 files) there are zero `sorry`, zero tactic `admit`, zero `native_decide`, zero `implemented_by`/`@[extern]`, zero `unsafe` declarations and zero custom axioms in proof code. All 416 Comparator configs permit only `propext`, `Quot.sound` and `Classical.choice`. For the application-relevant families the top line is genuinely formalized, and the earlier assumption that 003's quasi-RH still needs formalizing is wrong: ζ, every Dirichlet L and Hecke L over Q(√−3) are already zero-free for Re s > 7/8 against Mathlib-only statements. The main exception is 266: only N(6) ≤ 5 is formal, and the headline N(6)=3 rests on a binary64 run whose archive is not in the repo. Smaller gaps are 095 (no-lift), 149 (uniform permanence) and the 131 exact sampler. The real residual risks sit in the meta-layer, not the proofs:
- nobody has published a Comparator run;
- the challenge statements are agent-written with `review: unchecked`;
- 8 configs declare fully written definitions as "definition holes" that Comparator does not compare;
- 106 formalized families are missing from `formalization.yaml`.

The highest-leverage action is therefore not a new formalization. It is an independent Comparator replay plus a human statement-fidelity review of the ~20 configs behind the opportunity matrix, together with bridging the OAI theorems to the independently written formal-conjectures statements (30 files already link them). New formalization is worth funding only as infrastructure upstreams: a finite Markov chain spectral gap/mixing API seeded from 131, circulant Hadamard on Mathlib's new `Matrix.IsHadamard`, and the numerical range (Toeplitz–Hausdorff).

## What the formal layer actually proves

### Inventory (openai/math @ `fd4aeeb`, Oct 7 2026)
- **Toolchain:** `leanprover/lean4:v4.34.1`, `fixedToolchain := true`, `autoImplicit false`. Mathlib is pinned at `d13f23b7` ("bump toolchain to v4.34.1", Sep 24 2026; [lakefile L85-86](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/lakefile.lean#L85-L86)).
- **Dependencies:** 29 git requires plus 23 compatibility patches applied by Lake hooks ([lakefile L161-164](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/lakefile.lean#L161-L164)).
  - Imported by OAI code: PrimeNumberTheoremAnd (244 imports), StrongPNT, RellichKondrachov, TauCeti, FixedPointTheorems, ClassFieldTheory, SphereEversion, Schoenflies, Gromov, AbsorptionCutoff, and AINTLIB (only via `BernoulliRegular`).
  - **Required but never imported:** the 11 `lana-agents/*` packages (iut, tate-curves-theta, genl, heights, pi1, orbicurve-cores, oka, tempered-fundamental-groups, elliptic-curves, formal-schemes, belyi), plus carleson, Zeta3Irrational, leancert and PrimeCert. They add build cost and supply-chain surface for no proof content.
- **Size:**
  - `OAI/`: 122,458 `.lean` files, 26.06M lines, 1.57 GB of source (Mathlib HEAD is 8,618 files and 99 MB).
  - `ComparatorChallenges/`: 416 configs and 416 challenge files, 90.7k lines.
  - Per area (lines): Analysis 6.85M, Combinatorics 5.81M, NumberTheory 2.99M, Probability 2.25M, Geometry 2.25M, Computability 1.52M, MathematicalPhysics 1.28M; the rest are under 0.6M each.
  - Bulk is machine certificates: Ramsey 223 MB (444k kernel `decide` calls), MutuallyUnbiased 205 MB, PlanarPacking 142 MB, Progressions 58 MB.
  - **Dead code:** 7,262 files (1.21M lines) are reachable from neither `OAI.lean` nor any Comparator solution. Examples: Geometry/RCD, Probability/SLE, and 94.7k of Thomason's 160k lines.
- **Per-family map:** each of the 242 family docs maps to configs, their solution modules and the transitive OAI import closure. The full table is at `/home/claude/work/repos/scratch_lean/family_lean_map.csv`. Median closure is 34k lines and p90 is 195k. The largest are 266 (2.84M), 189 (2.80M), 159 (1.12M), 090 (0.98M) and 003 (0.56M).

### Soundness scan (static, whole library)
| Pattern | OAI/ (proof code) | ComparatorChallenges/ |
|---|---|---|
| `sorry` | **0** (not even in comments) | 539 in 415 files (expected: statements to be proved) |
| tactic `admit` | **0** (177 hits are the English word "admit" in docstrings) | 0 |
| `axiom` declarations | **0** (4 hits are docstring text) | **1**: `axiom mainStatement : MainClaim; theorem main := mainStatement` in [HarmonicGrowth.lean L100-102](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/HarmonicGrowth.lean#L100-L102) (family 361) |
| `native_decide`, `ofReduceBool`, `implemented_by`, `@[extern]`, `debug.skipKernelTC` | **0** | 0 |
| `unsafe` declarations | 0 (55 hits are identifiers such as `unsafeSet`) | 0 |
| `opaque` declarations | 1,534 in 207 files (mostly ContinuumCoulomb `Procedure` programs) | 0 |
| `run_cmd Lean.modifyEnv` (clears `auxLemmasExt`) | 11 files | 78 in 15 challenge files |
| kernel `decide` | 1.57M occurrences (sound, but expensive to check) | — |

How to read the flags:
- The HarmonicGrowth axiom sits in the challenge, not the solution. The solution proves `main` properly ([Main.lean L475](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Geometry/HarmonicGrowth/Main.lean#L475)), so Comparator is unaffected. It is still a hygiene defect: `#print axioms` on the challenge module shows a fake axiom.
- `opaque` with a typed body is sound. The `modifyEnv` calls only reset an aux-lemma cache, presumably so challenge and solution elaborate to identical auxiliary names. Neither affects kernel checking.
- Two supporting challenge files import OAI modules rather than Mathlib alone (CartierChartCompactnessSupport, CharacterVarietiesAllSeamsSupport), so their statements trust OAI definitions.
- **Dependency patches inject OpenAI-authored proofs into third-party namespaces:** +33.3k lines into PrimeNumberTheoremAnd (`Erdos970/`, `SiegelZeros/`, `ZetaFive/`, `Catalan/`), +26.2k into StrongPNT and +17k into ClassFieldTheory.
  - Upstream PNT+ `Wiener.lean`, which 003's closure imports, contains 2 `sorry`s (`prelim_decay_2/3`). The patch rewrites that file to "retain the proven declarations".
  - After applying the patches, I statically walked the external closures of the 003, Siegel, Jacobsthal and Dickman solutions (19–35 modules each) and found **no `sorry` and no axioms**. The two `axiom qc`/`hqc` hits in PNT+ `AdditiveCombination.lean` are inside a docstring example.
  - Comparator would reject `sorryAx` anyway.

### What Comparator guarantees (and what it does not)
The README ([L46-49](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/README.md#L46-L49)) and code ([Compare.lean L37-59](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/Comparator/Compare.lean#L37-L59)) guarantee three things for each `theorem_names` entry:
1. The solution constant has the same type as the challenge's. The check walks every constant used in that type and requires each non-target constant, including definition bodies, to be identical in the two environments.
2. The proof uses only the permitted axioms.
3. The Lean kernel accepts the proof.

This is real **statement matching**: a solution cannot quietly redefine a predicate the statement uses. It does **not** check that the challenge says what the paper says. The challenges are agent-written: `formalization.yaml` declares `automation: agent` and `review: status: unchecked` ([yaml L1773-1778](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/formalization.yaml#L1773-L1778)) and `scope: "Partial progress."` (L970). Only 12 of 416 challenge files define nothing of their own. Of these, 10 state theorems purely in Mathlib terms, among them QuasiRiemannHypothesis, DirichletSevenEighths, SiegelZeros and Catalan; the other 2 import OAI modules. Every other challenge carries custom definitions whose faithfulness a human has to judge.

**Definition-hole loophole.** Comparator compares only the name, type, universe levels and safety of anything listed in `definition_names`, not its body:
- [Compare.lean L63-65](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/Comparator/Compare.lean#L63-L65), and L50-52, where targets enqueue only their type's constants.
- Comparator's README says such holes "must always be checked with an additional (potentially human) verifier".
- In this repo, 10 configs use holes. In **8 of them the challenge shows a complete, non-`sorry` body**, so a reader believes the body is enforced when it is not: Brenier (12 defs, family 374), LogspaceEquality (20, family 103), KServer (9), Naimark (7), OccupiedOverlap (5, family 238), Rokhlin (4), SpinAngle (3), EuclideanFiveColor (1).
- I diffed the bodies by hand. Brenier's 12, LogspaceEquality's `step/run/spaceThrough/L`, Rokhlin `MixingOfOrder`, Naimark `IsIsomorphicToCompacts` and OccupiedOverlap `IsUnitary/relabelledUnitary` are **identical up to binder names**.
- The genuine holes (DefocusingNLS `sobolevProduct` membership proof, ElementaryPositivity witness structure) are legitimate. **No exploitation found**, but the guarantee as published is weaker than it looks.

Other gaps:
- Only 2 configs enable a second kernel (nanoda); everything else trusts the Lean kernel alone.
- The repo has **no Comparator run logs or attestations**. The Comparator layer is a checkable claim, not yet a checked one.

### Reconciling "~42% (300/719) top-line results formalized"
| Source | Count |
|---|---|
| Families with a Lean doc (`lean/docs/NNN.md`, = triage `lean=true`) | **242 / 372 (65%)** |
| Manuscripts linked from those docs | 341 (338 current; 2 point to **pre-repair** versions: docs [342](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/342.md) and 376) |
| `formalization.yaml` `sources` (manuscripts) | 173 |
| `formalization.yaml` `main_results` entries (unique configs) | 200 (189) |
| Comparator configs on disk | 416 (**227 not indexed in the yaml, covering 106 families**, including 131, 374, 266, 149, 012, 187, 317) |
| Docs whose formalization is only supporting or weaker for the headline | 14 families / 19 manuscripts: 027, 066, 095, 152, 194, 195, 212, 237, 260, 261, **266**, 280, 281, 301 |
| Docs where the headline is formalized but a headline clause is omitted | ~8 families / 13 manuscripts: 009, 087, **149**, 197, 206, 222, 229, 323 |

The figure 300 is not reproducible from any single metadata list. 341 doc-linked manuscripts minus the 19 support-only ones gives 322, and minus the partial ones gives 309. "~42%" is therefore a plausible curated manuscript-level count. At the family level, which is what the opportunity matrix uses, the headline is formalized for **~220–228 of 372 families (59–61%)**.

**Caveat for matrix builders:** `catalogue.json` sets `formalized` from yaml `sources` only (172 manuscripts). It therefore marks the 131, 374, 266, 012, 187 and 317 manuscripts as unformalized even though they have Comparator-pinned proofs. Use the doc and config mapping, not that flag.

### Key families: is the top line formalized, and does the statement match? (the confidence column)
Full machine-readable version: `/home/claude/work/deep/lean_confidence.json`. Statement files are at `lean/ComparatorChallenges/<name>.lean` @ `fd4aeeb`.

| Fam | Top line formal? | What the Lean statement says (vs paper) | Conf. |
|---|---|---|---|
| **003** | **Yes** | `riemannZeta s ≠ 0` for 7/8 < Re s ([QRH L5-7](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/QuasiRiemannHypothesis.lean#L5-L7)); `DirichletCharacter.LFunction χ s ≠ 0` for every q, χ, except the pole ([L8-12](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/DirichletSevenEighths.lean#L8-L12)). Both use **Mathlib objects only**. Hecke over Q(√−3) uses a custom L-function (22 defs, [L226-239](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/HeckeSevenEighths.lean#L226-L239)). Siegel: ∃c>0, (1−β) log q ≥ c, with c ineffective. All 4 configs are in the yaml; the closure is 556k lines. The 11/12 alternate proof is not formalized and not needed. | **5** (Hecke clause 4) |
| 011 | No (no Lean) | — | 3 |
| 012 | Yes | Joint Dickman law in natural density using Mathlib `Nat.maxPrimeFac`. ρ is defined by a delay-equation iteration in the challenge; I checked it numerically (ρ(1.5)=0.594535, ρ(2)=1−ln 2, ρ(2.5)=0.13032, all matching). Both orderings have density 1/2. Not in the yaml. | 5 |
| 021 | Yes | h(k) ≤ Ck² and ≤ Ck²/(log log 3k)². **C is existential**, so there is no usable constant for wheel/sieve code. | 5 |
| 029 | No (no Lean) | The companion is explicitly conditional on 4 stated inputs. | 3 (companion 2) |
| 095 | **Partial** | Explicit degree-20, 23-variable hyperbolic polynomial whose cone ≠ {x : L(x) ⪰ 0} for every symmetric pencil (generalized Lax disproved). The family headline, "no semidefinite lift / not a spectrahedral shadow", is **not** formalized. | 5 / **3 for no-lift** |
| 131 | Yes | The challenge kernel matches the paper exactly: ½ hold + 1/(12·C(n,4)) per proposal ([L87-94](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/SwitchChain.lean#L87-L94)). t_mix(1/4) ≤ 2n⁸, gap ≥ 1/(24n²C(n,4)), TV ≤ √\|Ω\|/2·e^{−t·gap}, connectivity ([L155-165](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/SwitchChain.lean#L155-L165)). The exact sampler is not formalized. | 5 (sampler 3) |
| 149 | **Partial** | Existence plus ε ≤ x_i(t) ≤ 1/ε, with ε depending on network, rates **and x⁰** ([L46-55](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/MassAction.lean#L46-L55)). This is boundedness plus persistence. The family headline, uniform permanence (one absorbing compact set per class, from the Oct 5 companion), is **not** formalized. | 5 / 3 |
| 165 | Yes | cr(K_n)=Hill and cr(K_{m,n})=Zarankiewicz for topological drawings (injective paths, chart-proper crossings, no triple points). The formula agrees with known cr(K_n) for n=3..12. | 5 |
| 179 | Yes | ±1 circulant Hadamard exists ⇔ n∈{1,4}; even Barker ⇒ n∈{2,4}. Odd Barker is classical and not formalized. | 5 |
| 187 | Yes | Legal 21-move Maker strategy on the infinite board; the 251-cell board claim is not formalized. | 5 |
| 238 | Yes (order only) | Θ(log N); TV→0 after **2048d** shuffles (Comparator) and 1600d (library only, [ThorpShuffle/Main L12-15](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/ThorpShuffle/Main.lean#L12-L15), not pinned). All bounds are "eventually in d" or carry an existential sweep count ([CoordinateTrace L360-367](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/CoordinateTrace.lean#L360-L367)), so **no round count is certified at any fixed N**. | 5 for order |
| 254 | Yes | Contractibility of \|nerve\| of a lifted spherical-cell preorder (`SalvettiCover`, [L54-61](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/HarmonicArtin.lean#L54-L61)) for every finite Coxeter matrix. An expert must confirm this encoding is the Salvetti cover. The CAT(0) counterexample and parabolic intersections are formal. The word/membership **algorithm** is not. | 4 (algorithm 3) |
| **266** | **No** | Formal: N(6) ≤ 5 and Fourier vanishing off Tao's class ([MUBSix L50-60](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/MUBSix.lean#L50-L60)). The headline N(6)=3 is a 4,470 s binary64 branch-and-bound. Its execution archive (`verification/computation`), which the paper cites, is **not in the repo**. formal-conjectures records only `upper_five` and keeps dim-6 "research open". | **≤5: 5; =3: 2** |
| 276 | Yes | Strong statement: the **operational** capacity is defined from codes, not by regularization. Holevo is additive and attained by phase-pair product ensembles ([L77-123](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/AmplitudeDamping.lean#L77-L123)). Additivity with an arbitrary partner channel is not formalized. | 5 (partner 3) |
| 317 | Yes | Thomason model structures for every n ≥ 1 and n = ω. The challenge is 2,473 lines with 99 defs and 11 structures, so faithfulness needs expert review. | 4 |
| 325 | Yes | ‖P[A]‖ ≤ 2·sup_{W(A)}‖P‖ for matrix polynomials and for every bounded Hilbert-space operator; 2 is sharp ([DirectCrouzeix L28-37](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/DirectCrouzeix.lean#L28-L37)). | 5 |
| 374 | Yes | ∃C, ‖T_μ−T_ν‖ ≤ C·W₂^{1/3} with the sharp exponent ([L73-103](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/Brenier.lean#L73-L103)). All 12 defs are definition holes ([Brenier.json L8-21](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/Brenier.json#L8-L21)); I verified them by hand against [Basic.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/Brenier/Basic.lean#L12-L70). The paper's explicit C* is **not** formalized. | 5 |

"5" means "Lean-formalized and statement-checked by this study, pending an independent Comparator replay".

### What the formal layer says about the drop's reliability
1. **The errors found so far avoid the formal layer.** 15 families carry withdrawn or revised manuscripts (the Oct 7 notes). Only 2 of them have Lean docs, 342 and 376, and in both the repair touched a claim outside the Lean statement:
   - 342: the cone-sum equality was corrected, while "tamed ⇒ compatible" is what Lean states.
   - 376: decay estimates were revised, while the formalized sheet/box programs and halting detector are unaffected.
   - At a 242/372 base rate one would expect ~9.8 of the 15 to have Lean docs; P(≤2) ≈ 4×10⁻⁵.
   - Per family: **13/130 unformalized families (10%) were withdrawn or repaired within two weeks, versus 2/242 (0.8%) formalized ones, with 0 errors inside a formalized statement.**
   - Selection effect: the repairs cluster in Kähler MMP, BSD and Hodge theory, where Mathlib cannot yet express the statements. This is evidence that the formal layer filters errors, not proof that it does.
2. **Lean-backed ≠ headline-backed.** 14 docs formalize only a supporting or weaker statement, and ~8 more omit a headline clause. A naive `lean=true → confidence 5` rule would overrate 266, 095 (no-lift), 149 (permanence), 195, 261, 194 and others.
3. **Statement fidelity is the open risk, not proof correctness.** One external audit is Bastounis–Circelli–Hansen (arXiv:2610.08144). It argues that an OpenAI Navier–Stokes blow-up formalization does not match its NL proof. The lemma name it cites (`norm_derivativeWord_inverse_le`) **does not occur in this repo**, and this drop's NS family (376) is about computation, not blow-up. The critique therefore appears to target a different release. I could not confirm this further because the web-search budget was exhausted.

## Current practice & state of the art
- **Comparator** (Lean FRO, built for AIMO) is the standard tool for checking untrusted AI-generated Lean. It provides a sandboxed build (landrun), `lean4export` replay, statement identity, an axiom allow-list and optional external kernels. Its own README warns that definition holes need a separate verifier. ([README](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/README.md#L88-L131))
- **Mathlib status at HEAD** (`d6416ab`, Oct 11 2026; checked with `git grep` on the commit):
  - Present: `Matrix.IsHadamard`, newly added in 2026 ([L51-54](https://github.com/leanprover-community/mathlib4/blob/d6416ab0f09d3a2e090f403fc80f37754f6181a9/Mathlib/LinearAlgebra/Matrix/HadamardMatrix.lean#L51-L54)); `Matrix.circulant`; `rowStochastic`; measure-theoretic Markov kernels with `Kernel.IsReversible`/`Invariant` ([L56-65](https://github.com/leanprover-community/mathlib4/blob/d6416ab0f09d3a2e090f403fc80f37754f6181a9/Mathlib/Probability/Kernel/Invariance.lean#L56-L65)); `SSet.modelCategoryQuillen` cofibrations and fibrations ([L36-50](https://github.com/leanprover-community/mathlib4/blob/d6416ab0f09d3a2e090f403fc80f37754f6181a9/Mathlib/AlgebraicTopology/SimplicialSet/CategoryWithFibrations.lean#L36-L50)).
  - **Absent:** a `ModelCategory SSet` instance, MarkovChain, mixing time, spectral gap, Dirichlet form, TV distance between laws, numerical range, Crouzeix, Wasserstein/OT, Dickman ρ, Jacobsthal, Barker, MUBs, reaction networks, Artin groups/Salvetti, crossing numbers, strict ω-categories, Specht modules (Mathlib has only `YoungDiagram`/`SemistandardTableau`), and quantum channels.
  - The Kan–Quillen model structure has been formalized by Joël Riou in his own development and presented at Lean Together 2026, so 317's own Kan–Quillen proof duplicates in-flight work. The Mathlib Markov-kernel paper (arXiv:2510.04070) covers kernels, disintegration and conditional independence, not mixing.
- **formal-conjectures** (DeepMind, `cd69121`) already records **36 `formal_proof` links into openai/math in 30 files**, against statements written independently with `sorry`. Examples are [circulant Hadamard](https://github.com/google-deepmind/formal-conjectures/blob/cd6912171c5a1de06905795e5533ec7120f34ddc/FormalConjectures/Arxiv/2402.13202/CirculantHadamard.lean#L58-L67), [Erdős 970/Jacobsthal](https://github.com/google-deepmind/formal-conjectures/blob/cd6912171c5a1de06905795e5533ec7120f34ddc/FormalConjectures/ErdosProblems/970.lean#L57-L71) and [MUB ≤ 5](https://github.com/google-deepmind/formal-conjectures/blob/cd6912171c5a1de06905795e5533ec7120f34ddc/FormalConjectures/OpenQuantumProblems/13.lean#L541-L554). No bridging proofs exist yet.
- **Community reading:** commentators stress that Lean checks proof versus formal statement, not formal statement versus intended problem. The "42%" figure comes from OpenAI staff (Dan Roberts) and history.md; nobody has recomputed it (redreamality, developersdigest). Quantum-information formalization lives in Physlib (formerly Lean-QuantumInfo), not Mathlib.

## Opportunities

### lean-1 · Independent Comparator replay + statement review of the ~20 application-critical configs (CERTIFY, pursue now)
- **Change:** on a workstation with the Mathlib cache (`lake exe cache get`), run `lake env comparator` under the documented `systemd-run` sandbox for the configs behind the matrix rows:
  - QuasiRiemannHypothesis, DirichletSevenEighths, HeckeSevenEighths, SiegelZeros;
  - SwitchChain, CirculantHadamard, EvenBarker, AmplitudeDamping, Brenier, MassAction, CompleteCrossing, BipartiteCrossing, DirectCrouzeix, CrouzeixHilbert, HyperbolicCones, HarmonicArtin, MUBSix, Jacobsthal, JointDickman, ThorpRemaining, SnakyTwentyOne.
  - Enable nanoda as a second kernel.
  - In parallel, have a domain expert sign off on each challenge file. Most are 30–170 lines, so expect 0.5–2 h each. HarmonicArtin's Salvetti encoding and ThomasonModelStructures (2.5k lines) need longer.
- **Benefit:** every "5" in the confidence column changes from *claimed* to *independently verified*. This is the only step that turns the formal layer into evidence a reviewer can cite.
- **Cost:** most closures are below 40k lines and should take minutes to about an hour each (estimate). 003's 556k-line closure plus patched PNT+ will take hours. MUBSix's 2.8M lines needs many hours and high `vm.max_map_count` (see the repo README mmap note).
- **Measure:** pass/fail logs, `#print axioms`, published hashes, signed review notes.
- **Risks:**
  - A build may fail on a fresh `lake update`, because 23 patches are applied by hooks.
  - The reviewer may find a mis-stated predicate. That is useful information, not a cost.
- **First step:** build `ComparatorChallenges.CirculantHadamard` and its solution (9.8k-line closure) end to end to validate the pipeline.
- I could not do this here: the proxy returns 403 for the Mathlib cache host (`lakecache.blob.core.windows.net`) and for elan's default release host. The box has 2 cores and 7 GB RAM.

### lean-2 · Bridge OAI theorems to the independently written formal-conjectures statements (FORMALIZE, pursue now)
- **Change:** for the 30 FC files that already link openai/math proofs, add a small bridging file that derives the FC statement from the OAI theorem. Examples:
  - FC `CirculantHadamard.circulant_hadamard_conjecture` (uses `Hadamard.IsHadamard'` and `Matrix.circulant`) from OAI `exists_iff_order_one_or_four` (custom `IsSignHadamard`/`IsCirculant`).
  - FC `erdos_970` from `erdos_970_quadratic`.
- **Benefit:** two independent statement authors reduces the fidelity risk to a short, human-checkable bridge. formal-conjectures can then retire `sorry` on "research solved" entries.
- **Cost:** about 20–200 lines per entry. FC's toolchain must be compatible with OAI's v4.34.1/Mathlib `d13f23b`, so pinning may require extracting the OAI closure.
- **Measure:** number of FC entries whose `sorry` is replaced by a checked bridge.
- **Risk:** version skew between FC and the OAI Mathlib pin.
- **First step:** circulant Hadamard. Its closure is small and both definitions are elementary.

### lean-3 · Repo hygiene PRs to openai/math (CERTIFY, pursue now)
- Index the 227 configs and 106 families missing from `formalization.yaml`; the yaml is the machine-readable catalogue downstream tools consume.
- Mark support-only configs in the yaml.
- Re-point docs 342 and 376 to the Oct 6 repaired manuscripts.
- Replace `axiom mainStatement` in HarmonicGrowth.lean with `sorry`.
- Make the 8 "definition-hole" configs either list only true holes or drop `definition_names`, so bodies are compared.
- Make the two support challenges self-contained (no OAI imports).
- Remove the 15+ unused `require`s (iut and others).
- Publish Comparator logs.
- Cost: days. Benefit: accurate metadata for every downstream user, including this study's catalogue. The paths are listed in the JSON targets.

### lean-4 · Harden Comparator's definition-hole semantics (IMPLEMENT, pursue now)
- **Change:** in `leanprover/comparator`, add a mode or warning for this case: a `definition_names` entry whose challenge body is not `sorry` should require body equality (or at least a warning), instead of comparing only `toConstantVal` and `safety` ([Compare.lean L63-65](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/Comparator/Compare.lean#L63-L65), [L89-104](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/Comparator/Compare.lean#L89-L104)).
- **Benefit:** closes a silent-weakening channel for every AI-proof evaluation that uses Comparator, including AIMO-style competitions. Here, 8/10 hole configs would have been caught mechanically instead of by my manual diff.
- **Measure:** the PR is merged, and rerunning the 10 configs shows which differ.
- **Risk:** legitimate uses, where the solution must supply a different body, need an explicit opt-out.

### lean-5 · Close 266's headline: publish/rerun the MUB execution archive, then certificate-check it in Lean (FORMALIZE, pursue as research)
- **Stage 1 (days):** the paper cites `verification/computation/README.md` and `REPRODUCE.md` with binaries, centers and hashes. None of these is in the repo, though 30 other manuscripts do ship `verification/`. Ask OpenAI to publish them, then rerun the 100-process pipeline (4,470 s wall on their platform).
- **Stage 2 (months):** convert the binary64 cover into kernel-checked interval certificates. LeanCert is already a pinned but unused dependency. The ≤5 development alone is 2.8M lines and 205 MB, and the ≤3 exclusion has a 12⁵ = 248,832-cell base cover plus refinements, so expect GB-scale Lean.
- **Value is modest for applications.** The QUANT design question ("no complete set of 7 MUBs, so no d+1-basis tomography or full-MUB QKD in d=6") is already settled by the formal N(6) ≤ 5. Only "can I use 4 MUBs?" depends on ≤3.
- The "≥" direction (3 MUBs exist in C⁶) is classical and a short formalization with little value.

### lean-6 · Upstream a finite Markov chain spectral-gap → TV / mixing-time API to Mathlib, seeded by 131 (FORMALIZE, pursue as research)
- **Seed:** 131's generic layer is about 800 lines that import only Mathlib: [FiniteKernelTV.lean L151-190](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Probability/SwitchChain/FiniteKernelTV.lean#L151-L190) (`matrix_tv_bound_of_gap`), FiniteKernelAlgebra, SpectralFromSquare, Energy and EnergyTransfer.
- **Gap it fills:** Mathlib has no MarkovChain, mixing time, spectral gap, Dirichlet form or TV distance. Meanwhile the OAI library re-defines `mixingTime` 15 times and TV 40 times.
- **Work:** the seed handles only symmetric, row-stochastic K with the uniform stationary law. It must be generalized to reversible π with a weighted inner product and connected to `Kernel.IsReversible`. Then add canonical paths/comparison (Diaconis–Saloff-Coste).
- **Effort:** 1–2 months by a Mathlib-fluent contributor, and the code needs rewriting to Mathlib style. Note that 30,858 OAI files `import Mathlib` wholesale.
- **Benefit:** a prerequisite for any formal MCMC guarantee (131, 238, 227, and switch/Curveball samplers).
- **Measure:** merged PRs, and 131's Comparator statement re-proved on top of them.

### lean-7 · Upstream circulant Hadamard + even Barker onto `Matrix.IsHadamard` (FORMALIZE, pursue now after lean-2)
- **Source:** 68 files and 9.5k lines with Mathlib-only imports ([Main.lean L19-22](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/LinearAlgebra/CirculantHadamard/Main.lean#L19-L22)).
- **Fit:** Mathlib now has the right definitions, so the statement becomes `(circulant v).IsHadamard → card n ∈ {1,4}` over ℝ. Much of the cyclotomic and 2-adic support (CyclotomicRings, LocalDVR, RamifiedEisenstein) probably overlaps existing Mathlib API, so expect it to shrink.
- **Effort:** weeks. Good first upstream: a classic, small and self-contained theorem.

### lean-8 · Upstream numerical range + Toeplitz–Hausdorff (from 325) (FORMALIZE, pursue now)
- Mathlib has no numerical range.
- OAI proves its convexity **four separate times**: [DirectCrouzeix/Convexity L201](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/DirectCrouzeix/Convexity.lean#L201), [NumericalRange/Convexity L324](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Analysis/NumericalRange/Convexity.lean#L324), Crouzeix/Convexity and HilbertCrouzeix/NumericalRange; 142–333 lines each.
- **Effort:** a few hundred lines, so weeks at most.
- **Next step:** Crouzeix's 2-bound is then a natural follow-up PR (~15k lines; heavier).

### lean-9 · Specht modules from 238 (FORMALIZE, monitor)
- YoungSymmetry (1.9k lines) and FiniteUnitary (3.2k lines) give unitary Specht representations.
- Representation theory of Sₙ is a long-standing Mathlib gap.
- Worth an RFC on Zulip; effort is a few months.

### lean-10 · Strict ω-categories / Street nerve from 317 (FORMALIZE, monitor)
- **Size:** the live closure is 65k lines, and 94.7k of Thomason's 160k lines are dead code.
- **What overlaps:** it contains a full Kan–Quillen `ModelCategory SSet` ([KanQuillen.lean L149-158](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/CategoryTheory/Thomason/KanQuillen.lean#L149-L158)). Mathlib lacks this, but it **duplicates Riou's in-flight work**, and weak equivalences are custom (π₀/πₙ bijections, [Definitions.lean L2347-2376](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/CategoryTheory/Thomason/Definitions.lean#L2347-L2376)).
- **What is new:** `OmegaCategory`, Steiner complexes, orientals and the Street nerve.
- **Recommendation:** offer them to Riou and the ∞-cosmos project as reference, not as a PR. Applied value is ~0.

## What is NOT an opportunity here
- **"Formalize 003's quasi-RH top line"**: already done, and against Mathlib-only statements. Spend the effort on lean-1. The 11/12 alternate proof adds nothing. The Siegel constant is ineffective, so the formal layer gives no explicit constant usable by CAS or explicit-PNT code.
- **Using `lean=true` as a confidence proxy:** this overrates 14 support-only families and ~8 partial ones (see the table). Always read the doc's scope paragraph.
- **Building or upstreaming the library wholesale:** 26M lines, 1.57 GB, 1.2M dead lines, 30,858 `import Mathlib` files and machine-certificate bulk. Verification should be per-closure (lean-1). Upstreaming should be by extraction and rewrite (lean-6/7/8).
- **Certified Thorp round counts for FPE (238):** the formal statements are asymptotic or existential. Even the explicit multipliers mean 1600d–2048d full shuffles, i.e. 51k–65k at N=2³², or 32,800d ≈ 1.05M from worst start, against the ~2d ≈ 64 lower bound. They certify nothing usable at a fixed N.
- **Formalizing explicit constants for 021/374/149 to drive applications:** the Lean statements are existential in C or ε. The papers' explicit constants (e.g. C*≈96 in 374) are too large to matter in practice, so formalizing them is effort without a user.
- **Crossing numbers (165), Brenier/W₂ (374), reaction networks (149) and the GAD channel (276) as Mathlib PRs:** each needs a missing API (graph drawings, OT, CRNT, quantum channels) and serves few users. GAD belongs in Physlib, if anywhere.
- **"N(6) ≥ 3" formalization:** classical and trivial relative to the gap. The open part is ≤3.

## Experiment results
All experiments were static, with scripts in `/home/claude/work/repos/scratch_lean/`. A full Lake build was neither attempted nor feasible.

1. **Pattern scan** (ripgrep over 122,874 files): the soundness table above.
2. **Import-closure analysis** (`closure.py`, `union.py`):
   - Per-config and per-family transitive OAI closures: `family_lean_map.csv`.
   - 7,262 files (1.21M lines) are unreachable from any target.
   - Key closures: 131 22.7k, 179 9.8k, 276 6.2k, 149 7.8k, 374 33.0k, 325 39.1k, 165 38.7k, 003 556k, 266 2.84M lines.
3. **Dependency-closure check** (`depclosure.py`): I cloned PNT+, StrongPNT, rellich-kondrachov and AbsorptionCutoff at the pinned SHAs, applied the repo patches and walked the external closures of the 003, Siegel, 021 and 012 solutions. Result: 0 `sorry`, 0 axioms; the only hit was a docstring.
4. **Definition-hole diff** (`holes2.py`, `showholes.py`): Comparator reads the bodies of 8 configs' definition holes but does not check them. Manual comparison found them identical to the solution up to binder names, or differing only in proof terms (DefocusingNLS).
5. **Dickman ρ check** (`dickman_check.py`): the challenge's delay-iteration definition reproduces ρ(1.5), ρ(2) and ρ(2.5) to 5–6 digits.
6. **Revision vs Lean association:** 2 of 15 revised/withdrawn families have Lean (9.8 expected), hypergeometric P ≈ 3.9×10⁻⁵. Restricted to the 9 Oct 7 "repaired" families: 2 of 9 (5.9 expected), P ≈ 0.01.
7. **Cached-build feasibility:**
   - The GitHub release asset for Lean v4.34.1 downloads (HTTP 200, 580 MB).
   - elan's default host and the Mathlib cache host (`lakecache.blob.core.windows.net`) return proxy 403.
   - The sandbox has 2 cores and 7 GB RAM. Building Mathlib from source here is infeasible, so **no Comparator run was possible**. This is exactly why lean-1 is the top action.
8. **Tooling note:** the shared `/home/claude/work/repos/mathlib4` clone is now a sparse checkout (≈5% of files present), apparently changed by another agent. My Mathlib searches used `git grep <sha>` on objects and are unaffected.

## Sources
- openai/math @ `fd4aeeb`: [README](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/README.md), [history.md L29-31 (300/719)](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/history.md#L29-L31), [lean/ComparatorChallenges/README.md](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/README.md), [formalization.yaml](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/formalization.yaml), [docs/266.md](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/266.md)
- leanprover/comparator @ `ca04cfc`: [README](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/README.md), [Compare.lean](https://github.com/leanprover/comparator/blob/ca04cfc72b550331658ec314bf47685281bfd4bf/Comparator/Compare.lean)
- leanprover-community/mathlib4 @ `d6416ab` (HEAD, Oct 11 2026) and the pinned `d13f23b`
- google-deepmind/formal-conjectures @ `cd69121`
- Bastounis, Circelli, Hansen, *Navier-Stokes lost in translation*, [arXiv:2610.08144](https://arxiv.org/abs/2610.08144); coverage: [AI Weekly](https://aiweekly.co/alerts/paper-flags-gap-in-openais-lean-verified-navier-stokes-proof)
- [OpenAI Math's Correction Week: What a Passing Lean Proof Actually Verifies](https://redreamality.com/blog/ai-math-verification-lean-faithfulness/)
- [OpenAI Math Repo: What the Lean Proofs Do and Don't Verify](https://www.developersdigest.tech/blog/openai-math-repo-lean-proofs-what-they-verify-2026)
- [OpenAI: Sharing AI progress in mathematics](https://openai.com/index/sharing-ai-progress-in-mathematics/)
- [Joël Riou, Formalization of homotopy theory in Lean (Lean Together 2026)](https://researchseminars.org/talk/LT2026/45/)
- [Markov kernels in Mathlib's probability library, arXiv:2510.04070](https://arxiv.org/abs/2510.04070)
- [quantumInfo / Physlib (Lean quantum information)](https://reservoir.lean-lang.org/@Timeroot/quantumInfo); [Generalized Quantum Stein's Lemma in Lean, arXiv:2510.08672](https://arxiv.org/abs/2510.08672)
- [UW AI-math projects, Fall 2026 (no Markov-mixing formalization project)](https://ai.math.uw.edu/projects/fall-2026)
