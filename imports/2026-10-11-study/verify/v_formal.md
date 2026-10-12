# Verification: formal and CAS rows (lean-1, lean-4, seqdesign-1, seqdesign-3, cas-1, cas-2, optimization-3)

Repo `/root/openai-math` @ fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb. Fresh clones were made in `/home/claude/work/verify_repos/`:

| Repo | Commit | Notes |
|---|---|---|
| comparator | ca04cfc72b55 | matches the permalinks |
| hap | 415d3655c99f | matches; PackageInfo version 1.79 |
| sage | 0835358cba62 | sparse checkout of `src/sage/groups`; matches |
| vpsolver | c01e1d38a12e | matches |

I made all my own checks before opening the theme `.md` files. I opened `cas.md` and `seqdesign.md` only at the end, to reconcile the E10 timing and to see how the merit-factor Lean status was worded.

---

## lean-1: confirmed (minor caveats)

**Soundness scan** (ripgrep, `-t lean`, over `lean/OAI`: 122,458 files, 26,060,031 lines):

- `\bsorry\b` in OAI: **0**. All 539 matches are in `ComparatorChallenges/*.lean`, as expected for challenge files.
- `\badmit\b` in OAI: 178 matches. Every one is English prose ("…admit a …") inside doc comments. The 3 lines that *start* with `admit` (MaskedCoordinates.lean L25, FiniteDustCover.lean L11, CartanPathTupleLifts.lean L27) are comment continuation lines. Searches for tactic-position forms (`by admit`, `· admit`, `<;> admit`, `; admit`) found 0.
- `native_decide`, `@[extern`, `implemented_by`, `unsafe def`, `ofReduceBool`, `debug.skipKernelTC`: **0** each.
- `axiom` declarations: the only real one is `ComparatorChallenges/HarmonicGrowth.lean:100: axiom mainStatement : MainClaim`, followed by `theorem main : MainClaim := mainStatement`. The other three hits (Printer.lean:43, HookModel.lean:274, LocalRecords.lean:298) are wrapped doc-comment lines ("…axiom is used/needed"). The HarmonicGrowth axiom does not weaken anything: `HarmonicGrowth.json` lists `theorem_names: [OAI.HarmonicCounterexample.main]`, and Comparator requires the solution's `main` to use only the three permitted axioms.
- `run_cmd modifyEnv` in OAI: 11 files. They only add entries to `LibrarySuggestions.nameDenyListExt` or reset `auxLemmasExt`, so they create no declarations.
- `lean/patches/*.patch` (23 dependency patches applied by lakefile hooks): no added `sorry`, `axiom`, `admit` or `native_decide`. Upstream dependency sources themselves were not scanned. Mathlib and Lean core appear in every closure checked; the circulant Hadamard and Artin closures import only Mathlib/Lean/Std plus OAI.

**Configs:** 416 `*.json`. Every one has `permitted_axioms` = {propext, Quot.sound, Classical.choice}. Only 2 set `enable_nanoda: true` (TraceIdealTransportSupport, ArtinParabolicIntersections), and none use `external_kernels`. I found no Comparator run log or attestation anywhere in the repo.

**Permalinks:**

| Link | Content | Status |
|---|---|---|
| Comparator README L46-49 | the three guarantees (same statement, permitted axioms, kernel-accepted) | ✓ |
| formalization.yaml L1773-1778 | `automation: methods: - method: agent` / `review: status: unchecked` | ✓ |
| QuasiRiemannHypothesis.lean L5-7 | `riemannZeta_ne_zero_of_seven_eighths_lt_re`, Mathlib-only statement | ✓ |
| SwitchChain.lean L155-165 | `switch_chain_main`, `switch_chain_tv_bound`, `switch_connectivity` | ✓ |
| HarmonicArtin.lean L54-61 | `SalvettiCover` defined as the realization of the nerve of the lifted-cell preorder; `salvetti_cover_contractible` | ✓ |

The HarmonicArtin encoding is a bespoke poset model (`LiftedFace` with reduced-word and minimal-coset conditions). The row's "needs expert check" is fair.

**Minor:** the row's first_step says the CirculantHadamard closure is "9.8k-line". I count 9,564 lines across its 73 OAI modules, so about 9.6k.

## lean-4: confirmed

**Comparator source** @ca04cfc:

- `Compare.lean` L63-65: `definitionHoleMatches` is `challengeHole.toConstantVal == solutionHole.toConstantVal && challengeHole.safety == solutionHole.safety`. `ConstantVal` holds name, levelParams and type, so the value is never compared.
- L89-104: for each definition target, check it is `defnInfo` on both sides, then `definitionHoleMatches`, then `worklist.push solutionConst.name`.
- L50-52: when the worklist reaches a definition or theorem target, it adds only `solutionConst.type.getUsedConstants`. The body's constants are not compared against the challenge. Axiom use and kernel replay still apply to the whole solution.
- README L88-138 ("Definition Holes"): guarantees only axioms, kernel acceptance, and "name, type, universe levels and safety levels". It says "To establish a definition hole, the challenge must provide it as a sorried definition" and that hole solutions "**must** always be checked with an additional (potentially human) verifier".

**The 10 configs with non-empty `definition_names`** (65 names in total):

| Config | # names | Bodies in the challenge file |
|---|---|---|
| Brenier | 12 | all complete (`E`, `uniformMeasure`, …, `HasExactlyThreeAtoms`; Brenier.json L8-21) |
| KServer | 9 | all complete |
| LogspaceEquality | 20 | all complete |
| Naimark | 7 | all complete |
| OccupiedOverlap | 5 | all complete |
| Rokhlin | 4 | all complete |
| SpinAngle | 3 | all complete |
| EuclideanFiveColor | 1 | complete |
| DefocusingNLS | 3 | `sobolevProduct` has a `by sorry` proof field (L105-107); `schrodingerFlow` and `sobolevOddPower` are complete |
| ElementaryPositivity | 1 | true sorry hole (`elementaryPositivityWitness … := by sorry`) |

So "8 of 10 hole configs show complete non-sorry bodies" and "all 12 Brenier OT definitions" are correct. Counting names, 63 of 65 are complete.

**Exploitation check.** I compared each challenge hole body with the solution body found in the solution module's import closure:

- Naimark, LogspaceEquality, SpinAngle, Brenier, Rokhlin, EuclideanFiveColor and OccupiedOverlap are textually identical up to binder names and `omit … in` decorations.
- KServer differs only by variable renaming (`requests`↔`σ`, `labels`↔`j`).
- DefocusingNLS differs only in the membership proof terms inside subtypes.

Nothing was weakened, which confirms "a manual diff found no exploitation".

Context: no file in `lean/docs` or the ComparatorChallenges README mentions that the hole bodies are type-checked only. GitHub issue search on leanprover/comparator was not possible (GraphQL is blocked), so I could not rule out an existing issue.

## seqdesign-1: confirmed

**TeX** (`The-circulant-Hadamard-conjecture-September-23-2026/build/sections/introduction.tex`):

- L21-24, thm:main: "a real circulant Hadamard matrix of order n exists if and only if n∈{1,4}".
- L35-40: the odd case is credited to Turyn–Storer 1961, with Schmidt–Willms 2016 for the exact list; even length >2 forces vanishing periodic autocorrelations.
- L43-49, cor:barker: n>1 Barker ⇔ n∈{2,3,4,5,7,11,13}.

**Lean:**

- `OAI/LinearAlgebra/CirculantHadamard/Main.lean` L19-34: `exists_iff_order_one_or_four (n) (hn : 0 < n) : ExistsRealCirculantHadamard n ↔ n = 1 ∨ n = 4`.
- `ComparatorChallenges/CirculantHadamard.lean`: the definitions (`IsSign`, `IsCirculant` with `H i j = h (j - i)` over `Fin n`, `IsSignHadamard` with `H * Hᵀ = n • 1`) match the TeX definition.
- `Barker/Main.lean` L63-73, `even_length_eq_two_or_four`, matches `EvenBarker.lean`.
- The closure is Mathlib/Lean plus 73 OAI modules with no sorry.
- lean/docs/179.md: "The paper's classification of odd Barker lengths is outside this selected additional statement." This is consistent with the row.

**Live references (WebFetch, 2026-10-11):**

- Wikipedia "Barker code": "It is conjectured that no longer sequence exists"; "the possible existence of an even Barker sequence longer than 4 remains open". No 2026 proof is mentioned.
- Wikipedia "Hadamard matrix": "The circulant Hadamard matrix conjecture, however, asserts that, apart from the known 1 × 1 and 4 × 4 examples, no such matrices exist. This was verified for all but 26 values of u less than 10^4."
- OEIS A091704: "It is conjectured that there are no Barker codes of length > 13", plus the Borwein–Mossinghoff 2014 window (n = 3979201339721749133016171583224100 or n > 4·10^33). Last modified Oct 11 2026; no proof is mentioned.
- MathWorld: "it is conjectured that no longer Barker codes exist."
- MATLAB comm.BarkerCode: "The maximum known Barker code length is 13."
- formal-conjectures @cd69121 BarkerSequence.lean L48-51: `@[category research open, AMS 5 11 94] theorem barker_conjecture … : a.length ≤ 13 := by sorry`.

## seqdesign-3: corrected ("Lean-checked consequence" is overstated)

**TeX.** cor:merit is in the **Sept-23** preprint `Asymptotically-minimal-maxima-of-real-Littlewood-polynomials-September-23-2026/build/merit-morse.tex` L22-36: "F_N = max F(A) → +∞ … through all integer lengths". The proof (L37-50) is 1/F(A_N) = ‖P‖₄⁴/N² − 1 ≤ m_N² − 1 → 0 by thm:main (m_N → 1), matching the row's mechanism. introduction.tex L100-109 names Turyn's/Erdős's L⁴ conjecture and states the disproof. The Oct-5 "Ultraflat" companion is also listed under family 076 in CONTENTS.md.

**Lean status.** lean/docs/076.md formalizes only (i) the max modulus ≤ (1+η)√N for all large N (`AsymptoticallyMinimalLittlewood.lean`) and (ii) finite-exponent L^p flatness. "merit" (case-insensitive) occurs **nowhere** in `lean/OAI` or `ComparatorChallenges`. The corollary is therefore a short, valid deduction from a Lean-checked theorem, but it is not itself Lean-checked. The row's summary ("a Lean-checked consequence") and its suggested replacement texts ("OpenAI 2026, Lean-checked") should say "follows in three lines from a Lean-checked theorem". The underlying math claim stands.

**Targets:**

| Target | Status | What it says |
|---|---|---|
| Shaydulin et al. (arXiv 2308.02342v2, DOI 10.1126/sciadv.adm6761 = Sci. Adv.) | ✓ | Main text: "whereas the asymptotic limit predicts that the merit factor should stay approximately constant." Supp. S1: "The conjectured asymptotic limit of F → 12.32 as N → ∞ was derived using arguments from statistical mechanics in Ref. (54)." |
| Zhang–Shen–Kumar–Pistoia (2504.00987), §II.A | ✓ | "the asymptotic merit factor of F_N ≈ 12.3248 as N → ∞ as proposed by Golay using the ergodicity postulate" |
| Sciorilli et al. (2506.17391) | ✓ | "Golay conjectured based on the ergodicity postulate the asymptotic upper bound F_N ≲ 12.3248/(8πN)^{3/(2N)}" |
| Packebusch–Mertens (1512.02475) | ✓ (body, not abstract) | "It is an open problem to prove (or disprove) that F_N is bounded." / "The common belief is that no such sequences exist and that F_N is bounded by some constant." |
| Wikipedia "Littlewood polynomial" | ✓ | "The existence or nonexistence of an ultraflat Littlewood sequence remains a central open question"; "determining the optimal asymptotic merit factor" listed among major problems |
| AlphaEvolve problems/28.html L214-232 | ✓ | Asks for the behaviour of C⁻, C⁺, C^w, C⁴ as n→∞ |
| git_labs README @1aa1234 | partly checked | It frames the BKV chase. I did not verify the "solvers seed randomly" part of the label; the README does not mention seeding. |

## cas-1: corrected (timing claim and one permalink range)

**Theorem scope.** `Harmonic-heights…/build/sections/introduction.tex` L22-30 says: "For every Coxeter matrix on a finite set S, the universal cover of X(W,S) is contractible … allows arbitrary finite labels, infinite labels, and connected or disconnected diagrams."

**Lean.**

- `ComparatorChallenges/HarmonicArtin.lean` L57-61: `salvetti_cover_contractible [Finite S] (M : CoxeterMatrix S) : ContractibleSpace (SalvettiCover M)`.
- The solution `OAI.Topology.ArtinGroups.Main` also proves `standard_salvetti_universal_cover_contractible`: `sourceSalvettiProjection` is a covering map and surjective, and the cover is simply connected and contractible.
- The closure is 660 OAI modules plus Mathlib, with no sorry.
- lean/docs/254.md: "Later corollaries in the manuscript are not included." So the center and monoid corollaries are not formalized, as the row's risks note says.

**HAP lines @415d365:**

| File and lines | Content | Status |
|---|---|---|
| doc/newResolutions.xml L18 | ResolutionArtinGroup returns a resolution for the "Artin monoid"; "It is conjectured that R is also a free resolution for the Artin group G. The conjecture is known to hold in certain cases."; "The contracting homotopy on R has not yet been implemented!" | ✓ |
| www/SideLinks/About/aboutArtinGroups.html L292-307 | "It is conjectured that X_D is always contractible. In those cases where the conjecture is known to hold the command ResolutionArtin(D) can be used…" | ✓ |
| same page | `ResolutionArtin` does not exist; only `ResolutionArtinGroup` and `ResolutionArtinGroup_spherical` are declared (lib/hap.gd L310-311) | ✓ |
| tutorial/tutorialResolutions.xml L276-280 | "Exactness of the resolution depends on the solution to the K(π,1) Conjecture for Artin groups of spherical type" (stale since Deligne 1972) | ✓ |
| tutorial/tutorialGroupCohomology.xml L342 | "…in thoses cases such as the spherical cases where the K(π,1)-conjecture is known to hold…" | ✓ |
| aboutCohomologyRings.html L259-263 | "…Artin groups where the K(pi,1) conjecture is known to hold" | ✓ |
| lib/ArtinCoxeter/resArtin.gi L44-50 | generators are the spherical subsets | ✓ |
| same file | `homotopy:=fail` | at **L168**, outside the cited L44-50 range |

**Measured timing (local GAP 4.12.1 + HAP 1.62, 2 cores).** The installed `resArtin.gi` is byte-identical to the clone's.

- [5,3,3,3]: H₀..H₅ in 3.0 s total, giving H₁ = ℤ, H₂ = ℤ/2, H₃ = ℤ/2⊕ℤ, H₄ = ℤ². This matches "seconds".
- E10 = T(2,3,7): `ResolutionArtinGroup(D,5)` took **67 s** to build, after which H₀..H₄ took well under 1 s (H₁ = ℤ, H₂ = ℤ/2, H₃ = ℤ/2, H₄ = ℤ/2⊕ℤ/6).
- E10 with `ResolutionArtinGroup(D,11)` (full homology) **did not finish within 5 minutes**.

The theme write-up reports 29 s for E10 H₁, H₂. Either way, E10 is tens of seconds for low degrees and much longer for the full range, not "seconds". The HAP doc claims themselves are all correct.

## cas-2: confirmed

**Docstring.** Sage @0835358 `src/sage/groups/artin.py` L526-536 reads verbatim:

> "Artin groups are conjectured to have many nice properties: torsion free; Finite type Artin groups have Z(A_M) = ZZ and infinite type Artin groups have trivial center; solvable word problems; H_W/W is a K(A_M,1)-space … These conjectures are known when the Artin group is finite type and a number of other cases."

The center statement is wrong for reducible diagrams. For example, A₁×A₁ = ℤ² has center ℤ² (finite type), and A₁ × Ã₂-type products are infinite type with nontrivial center. Family 254's cor:artin-structural (consequences.tex L23-36) gives Z(A) ≅ ℤ^k, where k counts the irreducible spherical components.

For the word problem, family 254's companion `Parabolic-intersections…/01_intro.tex` L64-65 states that "the word problem is decidable for every finite-rank Artin group". That is a different preprint in the same family, so it is consistent with the row's plan to cite "the preprints".

**Dispatch.** L615-623: all-∞ labels go to `RightAngledArtinGroup`, `not coxeter_data.is_finite()` goes to the generic `ArtinGroup` (`super().__classcall__`), type A goes to `BraidGroup`, and everything else to `FiniteTypeArtinGroup`.

**Comparison.**

- `ArtinGroupElement` (L42-58) defines only `_latex_`, `exponent_sum`, `coxeter_group_element` and `burau_matrix`. The `_richcmp_` at L322 belongs to `FiniteTypeArtinGroupElement`.
- The generic element therefore inherits `ElementLibGAP._richcmp_` (libgap_wrapper.pyx L638-656), which is `richcmp(left._libgap, right._libgap, op)`, i.e. GAP fp-group equality.

**Hang reproduction.** Sage is not installed here, so I ran the same GAP comparison directly (GAP 4.12.1, 60 s `timeout`):

- Affine Ã₂ (three m=3 relations), `G.1*G.2*G.1 = G.2*G.1*G.2`: killed at 60 s with no output.
- Large type (4,4,4), `(G.1*G.2)^2 = (G.2*G.1)^2`: killed at 60 s.

This matches the row's measurement, with the caveat that it was tested through GAP rather than through Sage itself.

## optimization-3: confirmed (one wording nuance)

**TeX** (`Additive-hardness…/build/source/introduction.tex`):

- L87-96, thm:unbounded-gap: for every c ≥ 0 there is a finite rational instance I and integer B with all sizes > 1/6, LP(I) = B and OPT(I) > B + c; this also holds for the individual-copy configuration LP.
- L98-102: c = 1 disproves MIRUP (L72-77: OPT ≤ ⌈LP⌉+1, Scheithauer–Terno).
- L106-112, thm:additive-hardness: NP-hard to distinguish packing into B from not packing into B+c, sizes > 1/6.
- L114-118, cor:complexity-equiv: a polynomial OPT+C algorithm exists iff P = NP.
- L12-14: Williamson–Shmoys Ch. 17 Problem 3 is cited as the constant-additive question.

**Lean.** `ComparatorChallenges/BinPackingGap.lean` `main_results` (L356-372) states:

- ∀c ∃I B, `I.n = 5B`, sizes in (1/6, 1), `B + c < opt I`, `individualLP I = B`, `typeLP I = B`;
- ∀c `PackingGapNPHard c` (polytime TM2 reductions from every NP language);
- `(∃c, Nonempty (AbsoluteAdditiveAlgorithm c)) ↔ PEqualsNP`;
- under P = NP, an exact algorithm exists.

The solution `OAI.Computability.BinPacking.Main` has a 284-module OAI closure with no sorry, and its JSON permits only the standard axioms.

**Witness sizes:**

- instance.tex L34-35: P₀ = 100^11, K = 25(c+1)(1+5P₀), d ≥ max{72K, 120K/ρ}. With ρ = 1/8 (consequences.tex L10) and c = 1, d ≥ 2.4×10^27 (c = 0 gives 1.2×10^27).
- trees.tex L56: 2d−1 phases, each phase adding N levels where N is the current leaf count, so the size is tower-like in d.
- instance.tex L392-397: denominators are D_geom = 160(R+1)^m[100(D*+1)]^L and D_size = 10^9·P₀·3^n·D_geom. These are exponential in n (bit length O(n + m log n)), so "exponentially large denominators" is correct.

**VPSolver** @c01e1d3: case-insensitive grep for irup, mirup and round-up finds nothing.

**Williamson–Shmoys.** I could not open the book PDF (proxy 403 on curl; WebFetch returned only front matter). Secondary sources characterize Problem #3 as "whether the Gilmore-Gomory LP has a constant integrality gap" (Hoberg–Rothvoss, arXiv 1503.08796 §1.1) and say Rothvoss 2013 "partly solves problem #3" (arXiv 1301.4010). If that characterization is right, the **unconditional** thm:unbounded-gap answers Problem 3 negatively, while the P≠NP conditional is needed only for the algorithmic OPT+C question. The paper itself frames Problem 3 as the algorithmic question. The row's "closes … Problem 3 (conditionally on P≠NP)" is therefore defensible under the paper's framing but may undersell it.

Rothvoss 1301.4010 also says MIRUP is "conjectured in [ST97]" and "known to be true for instances that contain at most 7 different item sizes", which supports "surveys still state MIRUP as conjecture".
