# Shared rubric for the OpenAI math-drop opportunity study

Repo: /root/openai-math (cloned from github.com/openai/math). 372 result families, 719 manuscripts.
Each manuscript dir is `/root/openai-math/preprints/<dir>/` with `paper.pdf` (or other pdf name), `README.md`, and TeX sources under `build/` (read `build/sections/00-introduction.tex`, `build/main.tex`, `build/paper.tex` etc. — grep for `\begin{theorem}` to find main statements). `pdftotext` is installed if TeX is missing.
Lean formalizations: /root/openai-math/lean (formalization.yaml lists formalized papers). A family marked lean=true has a Lean doc.
Three manuscripts were WITHDRAWN on Oct 7 2026 (sign error in Weil-classes eightfold paper + two dependents); 14 others were repaired. Treat all results as claims of an unreleased model, not peer-reviewed.

GROUND RULE: "Taking the math as true" is not enough. For every applied claim, check (a) is the result constructive / does it give an algorithm or explicit object, (b) are constants explicit or galactic, (c) what regime does it improve and does anyone actually operate in that regime, (d) what does current practice already do (often heuristics already beat the theory). A sub-n·log n algorithm with exponent saving 2^-182 is GALACTIC: zero practical speedup. Say so bluntly.

## Axis 1 — discipline (given): the 17 catalogue subjects.

## Axis 2 — impact channel (use these codes; a family can have several)
- ALGO   algorithms & data structures (new or faster algorithm, approximation scheme, sampler, construction)
- CPLX   complexity / hardness / impossibility that redirects practitioner effort (stop searching, use heuristics)
- CRYPTO cryptography & security (parameters, proofs of security, primality, class groups, isogenies, FPE, randomness)
- CAS    computer algebra & exact computation (number fields, polynomials, L-functions, groups, certification of GRH-conditional computations)
- NUM    numerical analysis & scientific computing (linear algebra, Krylov, PDE solvers, FFT, quadrature)
- OPT    optimization & operations research (LP/SDP/IP, scheduling, packing, matching, routing)
- STAT   statistics, ML, sampling/MCMC, learning theory, high-dimensional inference
- COMM   coding theory, information theory, sequence design (radar/sonar/CDMA), compression, DNA storage
- QUANT  quantum computing / quantum information / QKD / quantum error correction
- PHYS   physics, chemistry, materials, fluids, plasma, DFT, condensed matter numerics
- NET    networks, graphs, network science, distributed/online algorithms, mechanism design / markets
- GEO    computational geometry, graphics, imaging, inverse problems, optimal transport, metric embeddings / sketching
- BIO    biology: bioinformatics, systems biology, chemical reaction networks, DNA
- VERIF  formal methods, logic, type theory, proof assistants, SMT, decidability
- FOUND  foundational only — no credible applied channel within ~10 years

## Axis 3 — tier
- T1 DIRECT: gives an implementable algorithm/construction/explicit object/explicit bound for an operation real software or real practitioners perform, in a regime they operate in.
- T2 ENABLING: changes guarantees or decisions without new code paths being faster — certifies existing practice (e.g. proves a heuristic MCMC mixes), makes conditional computations unconditional, settles a design question engineers face (e.g. "no Barker code > 13 exists"), provides hard benchmark instances, or tells a field to stop pursuing something.
- T3 INDIRECT: plausible transfer via theory to an applied field, but requires further research steps.
- T4 PURE: no credible applied channel.

## Scores (integers 1–5) — used to build the opportunity matrix
- impact: value if it works (size of improvement × number of users/stakes). 5 = industry-wide or field-redirecting.
- reach: how many people/systems are touched. 5 = ubiquitous software / whole engineering discipline.
- directness: 5 = the paper itself specifies the procedure/object; 1 = needs new research to even define the application.
- practicality: 5 = works at realistic sizes/constants; 1 = galactic or astronomically large parameters.
- confidence: proof confidence. 5 = Lean-formalized top-line + short/clean argument; 3 = unformalized but plausible; 1 = depends on withdrawn/repaired work or extraordinary claim with no formalization.
- effort: engineering/research effort to first measurable result. 5 = days; 3 = a few weeks; 1 = multi-year program.
- time_to_value: 5 = < 1 month; 1 = > 3 years.

## Action types
IMPLEMENT (code change in a named project) · BENCHMARK (empirical test vs current practice) · CERTIFY (update docs/guarantees/remove conditional caveats) · REDIRECT (stop/redirect R&D effort, update textbooks/standards) · INSTANCES (counterexample → test/benchmark instances) · FORMALIZE (Lean/Mathlib contribution) · RESEARCH (follow-on research program) · NONE
