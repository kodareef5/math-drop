# b05_alggeo: algebraic and complex geometry (032–069, 36 families)

**Bottom line:** 34 families are T4/FOUND, 2 are weak T3, and none are T1 or T2. I checked every requested channel against the actual theorems. Each one fails on one of these points:

- the "very general" hypothesis
- non-explicit constants
- a galactic object
- the result was already known in the regime that matters

## Ranked (all weak)

1. **037 ODP volume gap (T3, PHYS).** The bound nvol ≤ 2(n−1)^n is sharp and explicit. Through the Martelli–Sparks–Yau / Li–Xu dictionary, the n=4 case says every Sasaki–Einstein 7-manifold other than round S^7 has Vol ≤ Vol(V_{5,2}) = (81/128)Vol(S^7). That gives a universal large-N gap F_{S^3} ≥ 1.257·F_{S^7} for M2-brane SCFTs. This is a curiosity for hep-th and changes no computation.
2. **055 corrected BMT inequality on every threefold (T3, PHYS).** Rigorous GV/PT/rank-0 DT computations (Feyzbakhsh–Thomas; Alexandrov–Feyzbakhsh–Klemm–Pioline–Schimannek) need BMT, which is proven only for X5 and X_{4,2}. This paper proves ch3 ≤ (a²/6+k)H²ch1 everywhere, but k and R_* come from a Frobenius spreading-out argument (constant C_0) and are never computed. Making them explicit for X6/X8 would be real but multi-year research.
3. **047/049 explicit counterexamples (T4, Lean-verified).** These polynomials could be regression instances for Singular/Macaulay2 LND routines. No applied user needs them.

## Requested channels: rejected

- **039 Nagata (Lean-verified) → splines, interpolation, AG codes: no.**
  - Nagata only says fat-point systems with d ≤ m√r vanish at *very general* points.
  - Spline dimension (via inverse systems) needs SHGH non-speciality, and SHGH was already verified for m ≤ 11.
  - Mesh and grid points are not very general. My exact mod-p check found 0-dimensional systems at random points but 6–91-dimensional ones for points on a conic.
  - Hansen's AG-code distance bound needs the Seshadri constant at F_q-rational points, while the char-p result covers only the generic tuple.
- **032 → isogeny crypto: no.** SQIsign, CSIDH, 2D isogeny attacks, CM/Igusa and pairings use only Tate's 1966 theorem and Honda–Tate. Higher-codimension Tate classes appear in no algorithm.
- **041/065 → strings: no.** 041 is structural only. Virasoro for CY complete intersections was already known (Getzler), and GV computations do not use it.
- **CAS, resolution, MMP software: no.**
  - 034's effective-Iitaka degree m(d) is existential.
  - 056: no software runs 4-fold MMP.
  - 059: resolution uses algebraic multiplicity, so nothing changes.
  - 064 makes Singular's μ a triviality certificate, but nobody needs it.

## Withdrawal flag

**032 has confidence 1.** I diffed its versions and found no direct citation of the withdrawn eightfold or K3 papers; the only OpenAI citation is family 001. However:

- The CM theorem in effect claims split Weil classes on CM abelian varieties are algebraic (via André's reduction), the same object as the withdrawn claim.
- The withdrawn K3 papers extended this family's Kuga–Satake work.
- Two sibling papers rest on the CM theorem.
- The consequences (Tate for all abelian varieties over F_q, Hodge standard) are extraordinary and unformalized.

Family 001 uses the CM theorem only for a corollary, not for its main theorem.

## Overhyped or galactic

- **053 Pixton counterexample:** genus 10^60. admcycles `generating_indices` assumes Pixton completeness, but feasible computations stop around g ≈ 5, so no output can change.
- **054:** the discriminant threshold is ineffective.
- **034/036/056/066 abundance/MMP chain:** it rests on one unformalized root (033), and six Kähler-MMP manuscripts were repaired on Oct 7, so I gave it confidence 1–2.

No family in this batch needs a deep dive.
