# Triangular semantic-defect energy: a proposed continuous-noise bridge
2026-10-30. Root working lemma and concrete target, not a new accepted LOCC threshold. The purpose is to replace a fault-parent record argument with an operator energy on the actual apparatus, if the required semantic predicates can be earned.

## Failure that motivates the representation
A physical fault can dirty an Alice engine; its actual dirty retirement can change Alice DATA much later. A Bob reply/cache that was valid after the original fault may then become false. Thus 'only primitive faults create semantic marks' is false. In a Poisson-instrument proof one can retain depth-two ancestry. Arbitrary continuous joint noise does not provide such a literal fault record, so that argument cannot simply be imported.

## Finite-type operator reset lemma
Let E=U+Σ_h R_type(h) B_h, where all local raw-energy terms and binary defect projectors commute. Assume a source-normalized local reset instrument Φ_h has summed source effect B_h and:
1. Its output has B_h=0.
2. It can change only a declared bounded set of other flags J_h and a declared local part of U whose spectral range is K_h.
3. All unaffected terms commute its Kraus legs and factor through it. The source B_h commutes E.
4. On the output, only types strictly below type(h) in a fixed finite acyclic dependency graph may be newly created. Already-present affected lower flags are included in the same worst-case set J_h.

Choose weights recursively so

  R_type(h) > K_h + Σ_(j∈J_h) R_type(j) + δ,

with δ>0. Fixed graph depth and bounded fanout give finite weights independent of system size (possibly very large). After factoring unaffected energy, the source local exponential is at least e^(sR_h) times the common lower bound and the output local exponential at most e^(s[K_h+Σ_jR_j]) times it. Completeness of the reset on its source and positivity then yield

  Φ_h*(e^(sE)) ≤ e^(−sδ) B_h e^(sE).

This is an operator bound on the complete instrument, retaining reference/bath coefficients. It does not require that individual output Kraus legs be monomial in syndrome, that a measurement of the semantic flags occurs, or that different faults are independent. It is the same bounded-local-spectral-range logic as the accepted dirty-reset envelope, now paying explicitly for lower-tier semantic flags.

If the source effect is a positive local rate times B_h rather than B_h itself, normalize the complete source instrument and retain the rate bounds in the controller service calculation. A reset that merely SOMETIMES heals B_h is not covered by this simple lemma; its actual killed resolvent/service must be supplied.

## Concrete Alice-to-Bob hypothesis to construct, not assume
Candidate types are dirty Alice history, false Bob cache/program, and dirty Bob local execution. A false cache can be defined mathematically by comparing its stored stabilizer-check bits with the CURRENT Alice stabilizer syndrome. These are actual commuting observables only after the correct local forest representation and measured classical registers have been specified.

An Alice dirty retirement may alter a bounded set of Alice checks and hence create boundedly many false Bob dependencies. Bob does not change Alice. However one must still prove that a dirty Bob retirement cannot corrupt another clean Bob engine's locked snapshot; full raw-read locks and actual-owned-resource support are the proposed mechanism. If this fails, a cyclic semantic dependency may appear and the triangular weight construction is unavailable.

A cache that is stale in time but equals the current syndrome can be semantically correct. Conversely, FIFO epoch consistency alone does not prove syndrome truth. The energy should use operationally relevant false-value flags rather than inaccessible fault history, but every flag-free commit must then be shown logically safe. Flushing must actually heal all flags counted in its service event, including delayed held messages; this is precisely the difficult protocol obligation.

## What this would and would not buy
If those operator predicates, actual reset/healing service, local supports, and clean useful action are proved, the global exponential native compiler has a plausible route to continuous joint-noise LOCC correction without literal Poisson fault ancestry. The finite-type weighted reset lemma only pays local defect propagation. It does not establish the required predicates, a common invariant history algebra, readiness/service, a local CP similarity, or a complete quantum threshold.

A directed cycle with unit or greater defect reproduction cannot be paid by strictly decreasing scalar type weights. That is a limitation of this representation, not an impossibility theorem for the physical protocol. A cyclic route would require a quantitative contraction mechanism or a different potential rather than silently increasing weights.

This elementary potential construction is useful machinery only if it closes the actual delayed-retirement obstruction; no novelty, practical gain or civilisation-scale result is claimed for the abstract lemma alone.
