# Independent child audit: structural fast-connector global synthesis

Reviewed 2026-10-30. Source: `GENERAL_FAST_CONNECTOR_RECURRENCE_CANDIDATE.md`.

**Verdict: the global synthesis passes this child-level audit, conditional on the two stopped-value constructions audited separately in this package.** This is not a fresh whole-package external review, a general weakly reversible recurrence theorem, or novelty clearance. The N-directed construction's prior neutral-bad and conditioning gaps were repaired and reviewed; they are not being assumed away here.

## 1. Compatible parameters and actual functions

Choose one rational 0<alpha<1 with alpha h<epsilon from the strict-power clearing bound. This satisfies both trace constructions. Their thresholds can then be increased independently. There is no cap-size/alpha or threshold circularity. Both functions are actual finite stopped costs for the same fixed-coefficient physical generator, extended by zero below their respective thresholds.

Above threshold their generator identities are exact, including fast composition jumps. The N-value has only bounded exterior leakage, from constant-rate immigration entering its fixed-width threshold band. The activity-credit value has only C AB exterior leakage, from active activation in its own h-wide threshold band. Those bands have infinite state-space support, but the displayed quantitative bounds genuinely hold uniformly in the hidden coordinates.

## 2. Residual geometry and normlikeness

Let a=(m-1)/(q-1). For B>=1 the exact formula gives

    H(B)-aB=(1-a)v,  1<=v<=q-1,

so 0<=H(B)-aB<=h, also covering B=0. Thus r differs from N-aB by at most h, and Z differs from B-N by at most h. The exact identity

    (1+a)(B-N)+2(N-aB)=(1-a)(N+B)

implies

    max(r,Z)>=(1-a)/(3+a)(N+B)-h.

Hence one residual is a positive linear fraction of total population outside a finite set.

Each first-holding lower bound is valid: before the first physical reaction, its running cost is constant, and the stopping threshold has not yet been reached. Total reaction intensity is <=C(1+N+B)^(m+q). Therefore the applicable value is at least its factorial weight divided by this polynomial. A factorial at a positive linear fraction of N+B dominates the denominator. The sum V=W_r+W_Z is consequently normlike, despite neither component being normlike by itself. It may be zero on some finite states; adding a constant if needed changes neither drift nor conclusions.

## 3. The two actual threshold leaks are absorbed

If both residuals exceed threshold, both drift terms are negative. If only one does, the other either has zero drift outside its entrance band or contributes its stated leakage. On the bounded-width Z entrance band, the geometry forces r to grow linearly with N+B; its negative factorial forcing absorbs C AB<=C(N+B)^2. On the bounded-width r entrance band, Z grows linearly and its negative factorial forcing absorbs the constant leakage. Both residuals below threshold imply bounded total population.

More quantitatively, outside a sufficiently large finite set,

    LV <= -phi(u)+C[1+(N+B)^2],

where u is at least c(N+B)-C_0. Thus LV<=-1 there. For each fixed theta>0, the same factorial comparison yields a finite K_theta and b_theta such that

    LV <= -exp(theta(N+B))+b_theta 1_{K_theta}.

No entropy selector, ignored boundary jump, or invariant capped domain enters this comparison. Arbitrary hidden compositions are covered because both value bounds and Poisson identities were proved pointwise or through actual stopping constructions.

## 4. Nonexplosion is independent, not circular

The linear localization function 1+N+B has zero fast drift. If A<m or B<q, activation contributes only a linear bound in total population. Otherwise the negative clearing term dominates C AB by a fixed multiple of A^mB^q. Hence its generator is bounded above by C(1+N+B). Finite sublevels and finite-rate localization give global nonexplosion before invoking the new sum V. Thus the stopped values are not being justified by a recurrence conclusion that in turn depends on their existence.

## 5. Closed communicating classes and positive recurrence

The fast graph and connector share the complex mA+qB, so the complete complex graph is weakly reversible. For any enabled physical reaction at x=z+y, follow a complex return path from y' to y while keeping the nonnegative residual z fixed. Every return edge is enabled at z+y_i and has positive rate. Hence each physical transition has a physical return path; every communicating class is closed. No irreducibility of the entire lattice is claimed.

The normlike drift LV<=-1 off a finite set gives finite expected hitting time of that set by stopped Dynkin. Every closed class must meet it. Finite reaction lists give finitely many possible immediate exit destinations from any finite set, all with finite V. Standard finite-set regeneration, or prescribed finite paths within a class followed by the same hitting-time bound after failed attempts, then gives finite mean return to a state in each closed irreducible class. Thus every such class is positive recurrent. Finite classes are included automatically.

## 6. Exponential moments without assuming stationary integrability of V

Fix theta and use the strengthened drift with forcing f_theta=exp(theta(N+B)). Positive recurrence supplies a finite-mean regenerative return time sigma to a chosen class state. Apply Dynkin only after finite-state/time localization and stop at sigma. Nonnegativity of V gives

    E integral_0^sigma f_theta(X_t)dt
       <= V(X_0)+b_theta E sigma < infinity.

Pass to the limit by Fatou/monotone stopping, using nonexplosion. This calculation never assumes pi(V)<infinity. The regenerative occupation formula then yields pi(f_theta)<infinity for the unique invariant probability of that irreducible class. The argument can be repeated for every fixed theta>0. It does not assert finite exponential moments for arbitrary mixtures over different class laws unless corresponding mixture bounds are separately supplied; the source correctly states the result classwise.

## Scope and final receipt

All couplings in this synthesis are valid for the stated structural family: fixed k>=2, homogeneous degree m fast graph containing every pure mX_i, common qB catalyst, q>m, and fixed positive coefficients. The conclusion is not inherited merely from the earlier explicit fixture. The constituent uncapped values and the new scalar geometry are the load-bearing mechanisms, and their child audits are separate records.

A fresh whole-package reviewer should still check the complete dependency chain independently. No further extension is made in this receipt.

Reviewed source hash:
bed8abcd3a74a23d1d8ac69784891853b6081bff67dd2b74bdb1887e4a8c780b  chemical_joint_shell_20261030/GENERAL_FAST_CONNECTOR_RECURRENCE_CANDIDATE.md

### Governing theorem statement receipt

Also read `producer-workspace/FAMILY_THEOREM.md`; the supplied hash 741a91d51b83efdd76f1440b38e34ef8098c3c114f4bbf7a3fe2f09bddf4bb30 matches the reviewed statement. Its exact graph, propensities, fixed-coefficient restriction, classwise recurrence/moment conclusions, and distinction between child audits and fresh whole-proof review agree with the audited synthesis. The stronger clearing exponent mentioned from a separate receipt is not needed for this coupling; the conservative independently checked exponent suffices.

One non-load-bearing phrase was flagged: “only the B0 excursion gains the full p power” is too strong when q-m>1. The displayed formula also gives full p for fresh phases b<=q-m. The required statement is that B0 always earns full p, while arbitrary phases require the phase-dependent bound. This does not affect the proof or theorem conclusion.

No frozen source was edited by this reviewer. Final child-level conclusion: the synthesis and stated structural scope pass, with the above wording correction; fresh independent whole-package review remains separate and pending.

### Final governing receipt after wording repair

Rechecked the current governing statement: it now says the B0 excursion earns the full p power while arbitrary phases require the phase-dependent bound. The non-load-bearing scope wording is corrected. Current SHA-256 is e14aa675f293d2f62f93e5c440daf33080c38ffb06eb8f7c029c4155c5783f17, matching the supplied receipt. Final child-level verdict: **PASS for the global synthesis and exact governing scope**, with fresh whole-package review still distinct and pending.
