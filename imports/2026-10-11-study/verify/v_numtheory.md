# Independent verification: numtheory-1, numtheory-3, numtheory-4

Verifier inputs: the rows in `deep/numtheory.json` (titles, summaries, targets, permalinks only); `/root/openai-math` @ fd4aeeb; a fresh sparse clone of `sagemath/sage` develop @ 0835358 (2026-10-11); passagemath 10.8.12 (PARI 2.17.4) in `scratch_cas/venv`; system PARI/GP 2.15.4. I audited the method in the deep-dive scripts (`tatuzawa.py`, `watkins_check.py`, `x015_*.py`, `bsd_gap.py`) but re-derived every number with my own code. I read `numtheory.md` only after all checks were finished, to compare wording.

My scripts and raw outputs are in `/home/claude/work/verify/v_numtheory_scripts/`.

---

## numtheory-1: 003 (7/8 half-plane) + Tatuzawa ⇒ unconditional class-number lists beyond h = 100

**Verdict: plausible-needs-expert.**

- The number theory is sound. I can also give an independent, elementary derivation that avoids Tatuzawa's constants and is about 3× stronger.
- The reproduction claims check out, and I extended them to the whole of Watkins's table (h ≤ 100).
- The word "unconditional" depends on two things:
  1. 003 actually being a theorem: Lean-checked, but I found no independent Comparator run, and the claim is extraordinary.
  2. Correct wording for the computational range: PARI's range is *documented*, not *certified*. Mosunov–Jacobson's 2^40 run is unconditional but its per-h lists are not published.

### (a) Tatuzawa's theorem and what the exception is

I could not download the primary source (J-STAGE and IMPAN are blocked by the proxy or robots.txt). I used these secondary statements, which agree with each other.

**Elsenhans–Klüners–Nicolae (arXiv:1803.02056), Lemma 2**, citing Tatuzawa, Jap. J. Math. 21 (1951/52) 163–178, Lemma 9 and Theorem 2:

> Let 0 < ε < 1/2. There is at most one |D| ≥ max(e^{1/ε}, e^{11.2}) such that L(1,χ) ≤ 0.655 ε |D|^{−ε}. **In this case L(s,χ) has a real zero s with 1 − ε/4 < s < 1.**

**EKN Lemma 3** (take ε = 1/log|D|):

> If |D| > e^{11.2} and L(s,χ) ≠ 0 for 1 − 1/(4 log|D|) ≤ s < 1, then h(D) > 0.655/(π e) · √|D|/log|D|.

So the exception is tied to a real zero in (1 − ε/4, 1). With ε = 1/log|D| and |D| > e^{11.2}, that interval starts at 1 − 1/(4·11.2) = 0.9777 > 7/8. A zero-free half-plane Re s > 7/8 therefore excludes the exceptional case for every such D. In fact log|D| > 2 already suffices.

The one point an expert should confirm is whether "in this case L has a real zero in (1 − ε/4, 1)" is Tatuzawa's own statement, i.e. that his proof bounds each character lacking such a zero rather than using an auxiliary exceptional character. EKN state it without proof.

Supporting evidence that the single-character form is standard:

- **Hoffstein**, "On the Siegel–Tatuzawa theorem", Acta Arith. 38 (1980), Lemma 1, as quoted in arXiv:2602.03626 §3. If q > 10^6 and L(σ,χ) ≠ 0 for σ > 1 − 1/(11.657 log q), then L(1,χ) > 1.507/(11.657 log q). That gives h > 0.0412 √|D|/log|D|. It is also a per-character statement, and 1/(11.657 log q) < 1/8 as well.
- **Chen**, Acta Arith. 130 (2007), Prop. 4.3, as used in arXiv:1601.00351, gives the companion constant 0.041 = 1/(7.732π).

**Independent derivation (no Tatuzawa constants needed).** For K = Q(√D), D < 0, Hecke's integral representation is:

Λ_K(b) = (√|D|/2π)^b Γ(b) ζ_K(b) = −(h/w)/(b(1−b)) + Σ_n a_n[(αn)^{−b}Γ(b,αn) + (αn)^{b−1}Γ(1−b,αn)], where α = 2π/√|D|.

- I checked this identity to about 30 digits for D = −4, −23 and −163 (`hecke_check.gp`).
- If L(s,χ_D) ≠ 0 on (7/8, 1), then ζ_K(b) = ζ(b)L(b,χ_D) < 0 for b ∈ (7/8, 1). Every term of the sum is positive, so h ≥ w·b(1−b)·[n = 1 term] for any such b.

Results:

- **Sanity check against real class numbers.** For every fundamental D with |D| ≤ 4·10^5, the minimum of h(D)/bound is 2.65, at D = −163 (`hecke_sanity.gp`).
- **Comparison with Tatuzawa.** With b = 1 − 1/log|D|, the bound is ≥ 2.52 × Tatuzawa's 0.0767·√|D|/log|D| for every log|D| in [11.2, 700]. Asymptotically it is 1/(π√e) = 0.193. With the best b in [7/8, 1) the factor is 3.1–3.8. Restricted to Tatuzawa's own narrow window 1 − 1/(4 log|D|), the Hecke bound is 0.92–0.995 × Tatuzawa, which is consistent with 0.655/e being essentially this argument.

So the row's conclusion follows from 003 alone by a textbook argument. The Tatuzawa constant is a valid but suboptimal choice.

### (b) Does 003's Lean statement cover the needed characters?

- **Statement.** `lean/ComparatorChallenges/DirichletSevenEighths.lean` L8–12 is Mathlib-only: for all q, all `χ : DirichletCharacter ℂ q`, and Re s > 7/8, with ¬(χ = 1 ∧ s = 1), `DirichletCharacter.LFunction χ s ≠ 0`. This includes every real primitive χ_D of modulus |D|, of either parity. `docs/003.md` says the same: "every Dirichlet L-function, uniformly over all positive moduli and all characters".
- **Proof file.** `OAI/NumberTheory/DirichletL/Nonvanishing.lean` L19–25 proves the theorem with the identical signature. The config allows only propext, Quot.sound and Classical.choice, and has `enable_nanoda: false`.
- **My scan.** The OAI import closure is 2,924 files and 486,490 lines. It contains no `sorry`, `axiom`, `native_decide`, `implemented_by` or `@[extern]`. The two non-Mathlib external modules it imports (`PrimeNumberTheoremAnd.Wiener` and `RellichKondrachov…Rellich`, together with their closures) also contain no sorry or axiom.
- **Not done.** I did not build the project or run Comparator; there is no Lean toolchain here. That kernel check is the load-bearing step.

### (c) Constants and crossovers (`bnd.py`, `hecke_bound.gp`, `cov.gp`)

The constant checks: 0.655/(π e) = 0.076700, and e^{11.2} = 73,130.

Search bound B(H), the |D| beyond which the lower bound exceeds H:

| H | Tatuzawa B(H) (row) | Hecke, b = 7/8 | Hecke, best b |
|---|---|---|---|
| 10 | 3.92e6 | 1.68e5 | 1.68e5 |
| 100 | 7.06e8 | 3.73e7 | 3.73e7 |
| 457 | 1.997e10 | 1.24e9 | 1.22e9 |
| 2900 | 1.099e12 (≈ 2^40) | 8.56e10 | 7.51e10 |

Largest H whose complete list fits inside a computed range:

| Range | Tatuzawa | Hecke, b = 7/8 | Hecke, best b |
|---|---|---|---|
| \|D\| < 2e10 | 457 | 1537 | 1593 |
| \|D\| < 1e11 (JRW 2006) | 957 | 3104 | 3303 |
| \|D\| < 2^40 | 2900 | 8854 | 9887 |

The row's numbers (7.1e8, 2e10, 2^40; h ≤ 457 and h ≤ 2900) are arithmetically correct for the Tatuzawa constant. For comparison, Hoffstein's constant (|D| > 10^6) would give h ≤ 245 at 2e10 and h ≤ 1556 at 2^40.

**What "PARI-certified range" actually is.** PARI's `qfbclassno` documentation (usersch3.tex, PARI 2.15.4) says, for D < 0 and flag 0 (Shanks baby-step giant-step):

> It gives unconditionnally correct results for |D| < 2·10^10, but may give incorrect results for larger values.

This is a documented correctness range for the algorithm, not a certificate per discriminant. Sage `cm.py` L842–844 relies on it ("We do not need to certify ... under 2*10^10"). Above that range one needs `quadclassunit` plus `bnfcertify` (`quadclassunit` alone assumes GRH), or an unconditional tabulation.

**Mosunov–Jacobson (arXiv:1502.07953).**

- They tabulate all D < 0 with |D| < 2^40, unconditionally: theta-series class-number formulas for D ≢ 1 mod 8, and Eichler–Selberg trace-formula verification "to eliminate the ERH dependency" for D ≡ 1 mod 8.
- They publish divisibility, rank and p-group statistics, not counts or maxima per h. Full tables are in Mosunov's thesis, and the "soon to appear on LMFDB" remark is future tense.
- So "h ≤ 2900 from the existing 2^40 tabulation" means re-running or obtaining their data, not reading off a published list.
- Jacobson–Ramachandran–Williams (2006) went to 10^11 unconditionally.

### (d) Spot-check: reproduce Watkins from the bound

Independent PARI/GP 2.15.4 enumeration with `isfundamental` and `qfbclassno` (`wk.gp`, `w100_*.gp`):

- **To Tatuzawa B(25) = 3.17e7:** count and max|D| for every h ≤ 25 match Sage's `watkins_table` exactly (32 min CPU).
- **To the Hecke bound B(100) = 3.735e7:** all 100 entries, count and max|D| for h = 1…100, match `watkins_table` exactly, including h = 100: (1856563, 1736). No D with h ≤ 100 lies in 1.9e7 < |D| ≤ 3.735e7.

So the row's "reproduced Watkins for h ≤ 10" is confirmed and extends to h ≤ 100. Because 3.7e7 < 2e10, this rests on the documented `qfbclassno` range plus 003.

The deep-dive `watkins_check.py` does the same thing in Sage with the Tatuzawa B(10). Its method is fine; I re-ran with different code.

### Context the expert should know

- Watkins (2004) verified that L(σ,χ) ≠ 0 for all σ > 0 for odd χ with q ≤ 3·10^8 (quoted in arXiv:2602.03626). His h ≤ 100 table used that verification plus an effective tail argument. The tail |D| > B is exactly what 003 newly supplies.
- On the window [1 − 1/(4 log q), 1) alone, Bennett-type numerics (arXiv:2602.03626, Thm 1.1) verify zero-freeness only for q ≤ 10^10. That is not enough for a tail.

### What an expert must check

1. **Run Comparator on `DirichletSevenEighths.json`** (kernel replay, axioms) at the pinned Mathlib d13f23b. Everything else hinges on this, and a correct 7/8 half-plane for all Dirichlet L-functions would be a historic result.
2. **Pick the lower-bound lemma and check it.** Either:
   - confirm Tatuzawa's per-character form, i.e. that the exception is exactly a real zero in (1 − ε/4, 1), and the constants 0.655 and e^{11.2}; or
   - use Hoffstein's Lemma 1, or the Hecke-integral bound above, which takes one page.
   The Hecke bound needs rigorous (interval) evaluation of Γ(b,x) only at the cut-off, and the margin there is large.
3. **Computational backbone.** Up to 2e10, decide whether the documented `qfbclassno` range is acceptable or each value needs certification. Beyond that, use `bnfcertify` or Mosunov–Jacobson-style unconditional data.
4. **Benefit.** h ≤ ~1590 within 2e10 using the Hecke constant, versus the row's h ≤ 457.

Score suggestion: keep the row's scores. The row understates the reach (457 → ~1590 and 2900 → ~9900), but the gating risk (003) is unchanged.

---

## numtheory-3: two crash bugs in Sage `prove_BSD`

**Verdict: confirmed.** One correction: the L660 pattern is latent, not a live crash.

### Current source (sparse clone, develop @ 0835358, 2026-10-11)

- `src/sage/schemes/elliptic_curves/BSD.py` L845 and L899: `M, _, exact = BSD.curve.heegner_index_bound(D, max_height=max_height, secs_dc=secs_hi)`.
- `heegner.py` L6815: `def heegner_index_bound(self, D=0, prec=5, max_height=None) -> tuple:`. There is no `secs_dc` and no `**kwargs`. `ell_rational_field.py` L5472 binds it directly.
- History: commit 8b6a73af07 (C. Wuthrich, 2015-02-27, "pass the right argument for heegner points from bsd") turned `max_height=max_height) #, secs_dc=secs_dc)` into `..., secs_dc=secs_hi)`. `git log -S secs_dc` on `heegner.py` and `ell_rational_field.py` shows the parameter never existed in the shallow history I fetched, so this path has been broken since 2015.
- L803–807: `if p in BSD.bounds: low = BSD.bounds[p][0]; BSD.bounds[p][1] = (low, min(BSD.bounds[p][1], bd))`. `BSD.bounds[p]` is always a tuple (L498/502/662/771/773/807/871/925), so this always raises TypeError. It also has a logic slip: it assigns a pair into slot 1. The intended line is `BSD.bounds[p] = (low, min(...))`.
- L660 (`BSD.bounds[p][1] = min(...)`) has the same tuple-assignment pattern. However, at that point the only key ever in `BSD.bounds` is 2 (set at L498/L502), and the loop at L635–637 does `if p == 2: continue`. So L660 is unreachable today. It should still be fixed with the same patch.

### Reproduction (passagemath 10.8.12; its BSD.py has the same lines at 847/901/807)

```
1014e1  -> TypeError: heegner_index_bound() got an unexpected keyword argument 'secs_dc'   (BSD.py line 847)
1058d1  -> TypeError: 'tuple' object does not support item assignment                      (BSD.py line 807)
```

With the obvious two-line fix (drop `secs_dc=secs_hi`, and assign the tuple at L805), run from a patched copy (`run_patched.py`):

| Curve | Result |
|---|---|
| 1014e1, 1050c1, 1176d1, 1200b1, 1200h1 | `[]`: BSD fully proved |
| 1058d1 | `[5]` (Sha_an = 25) |
| 1200q1 | `[5]` |
| 1078m1 | timeout at 120 s |

So the fix is real and useful, not cosmetic. The deep-dive's v2 run logs 15 `secs_dc` crashes and 1 tuple crash among 659 classes with N = 1000–1200, which agrees with the curves I re-ran.

I could not search Sage's issue tracker for an existing report: GitHub search and GraphQL are blocked in this session, and a web search found nothing.

---

## numtheory-4: Caraiani–Newton covers 14 LMFDB imaginary quadratic fields

**Verdict: confirmed.**

- **Hypothesis.** arXiv:2301.10509 (v3, 2025-03-27), Thm 1.1 = Cor. 7.1.2: "Let F be an imaginary quadratic field such that the Mordell–Weil group X_0(15)(F) is finite. Then every elliptic curve E/F is modular." There are no further hypotheses on F or E; the ζ_5 and E[3]/E[5] conditions belong to the general CM-field theorem. The abstract says the same thing as "rank 0 over F".
- **Reduction.** X_0(15) = 15a1, which has rank 0 over Q and torsion of order 8. So rank X_0(15)(K) = rank 15a1(Q) + rank 15a1^{(d)}(Q) = rank 15a1^{(d)}(Q).
- **Computation (`x015.py`).** The LMFDB fields are |d| < 100 or class number 1: 31 fundamental d from −3 to −95, plus −163, for 32 fields. For each I computed the exact modular-symbol ratio L(15a1^{(d)},1)/Ω. It is nonzero for exactly −3, −4, −8, −15, −19, −20, −23, −31, −35, −47, −79, −83, −87, −91 (14 fields). By Kolyvagin these twists have rank 0, so X_0(15)(K) is finite. For the other 18 the twist has proved rank 1, or rank 2 for d = −68 and −95: d = −7, −11, −24, −39, −40, −43, −51, −52, −55, −56, −59, −67, −68, −71, −84, −88, −95, −163. Both lists match the row.
- **Cross-check.** The abstract names d = 1, 2, 3, 5, i.e. discriminants −4, −8, −3, −20, and all four are in the list.
- **LMFDB status.** The live `rcs.cande.ec` knowl (last edits by J. Cremona, 2024-02-07 and 2024-07-17) still says "Assuming modularity, the database is complete within these bounds" and never mentions Caraiani–Newton. LMFDB repo @ 009463e has no "Caraiani" anywhere, and `ecnf/main.py` L64–70 just renders that knowl. So LMFDB has not done this.
- **Why the inference is valid.** Caraiani–Newton's "modular" means L(E,s) = L(π,s) for a cuspidal parallel-weight-2 π, or E has CM. Equal L-functions with the same Γ-factors force equal conductors, so E matches a rational Bianchi newform of level equal to its conductor. LMFDB's statement "the database contains all modular curves within these bounds" then gives unconditional completeness for these 14 fields.
- **Residual caveat.** LMFDB's other assumption, the correctness of the Bianchi modular-symbol computations, is unchanged.

I raise confidence to 4. The field list is exact arithmetic, and the theorem's hypothesis is exactly as the row states.
