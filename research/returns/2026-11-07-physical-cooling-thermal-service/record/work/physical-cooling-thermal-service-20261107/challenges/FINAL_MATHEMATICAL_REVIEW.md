# Version-bound hostile mathematical review

Reviewed file: `outputs/PHYSICAL_COOLING_THERMAL_SERVICE_RESEARCH_DOSSIER.md`.
Reviewed SHA-256:
`d7e25afde8da5874136adb99d0dd0ad7fbdb74329dabc7b756124423951e9a7e`.
Review date: 7 November 2026, Brisbane. Reviewer: the same hostile mathematical
auditor as the frozen independent initial; no additional agents were used.

**Verdict:** the substantive cooling/source/module argument passes at its stated
model. Two small quantitative/quantifier clarifications below are required before
calling this version final. There is no newly identified counterexample to the
claimed fixed-local-precision finite-round theorem. The review does not close the
explicitly open refrigerator, generic-bank-noise, noisy-universal-port, geometry,
numerical-threshold or advantage claims.

I checked Sections 1-10 in full, the optional reset calculation in Section 11
against the cached primary Merkli text, and the status/resource boundaries in
Sections 13-15. The exact bath/source interfaces, deterministic contraction,
output-cone proof, canonical operator-module factorization and CP/TNI repair were
checked against the earlier capital and my separately frozen constructive proof.
The source-pair spectrum/marginal/work formulas were already independently
verified in `auditor/FINITE_THERMAL_PAIR_RESERVE.md` and the pinned finite algebra
checks. No additional algebra script was needed for this review.

## Required fix 1: count every restoring round in the service error

Lines 448 and 467-471 currently admit two readings of K. The operation describes
K cooling sweeps **and** a fixed restoring number after each of G gates, whereas
the bound contains only `2K delta_round`. Make the accounting unambiguous.

Either define K to be the **total number of cooling rounds**, including every
post-gate restoring round (and state separately whether the fixed entry rounds
are included or absorbed into the displayed entry term), or use

    2(K_hold+r_restore*G) delta_round

for a uniform restoring count r_restore, plus the already declared entry cost.
If gate types have different counts, use their actual sum. The same convention
must govern the source/control counts in Sections 8 and 13. One can alternatively
absorb the restoring errors into a *new explicitly defined* gate-service error;
they cannot silently disappear into the native gate tail `delta_gate`.

This does not change the exponential-service conclusion: r_restore is fixed.

## Required fix 2: state the finite-size lower bound for local neutrality

Lines 33-37 give the strict asymptotic margin `2C0 u_c<delta`, while lines 130-131
also charge the fixed catalog support `wt(P_a)`. State the theorem for admitted
code lengths `n>=n0`, where n0 is large enough for

    2C0 u_c n+q_cat<delta n,

with q_cat the largest catalog Pauli support; also include any other fixed-support
bootstrap bounds used by the imported canonical frame/gates. A sufficiently
large fixed n0 exists by the stated strict margin. A separately proved
all-finite-size bound may replace this qualification, but it is not written in
this version. No asymptotic lifetime or fixed-precision conclusion is lost.

## Requested source-preparation clarification: permissible precise addition

The current exact product Gibbs-pair reserve is valid as written. To allow fixed
local preparation errors without demanding exponentially accurate preparation of
the entire large reserve, the following is a valid extension:

> Prepare the private source pairs independently in states tildeomega_j with
> `||tildeomega_j-omega_j||1<=epsilon_src`. Let each private waiting channel be
> CPTP and fix omega_j. If all waiting-environment outputs are permanently
> excluded from future accesses, contractivity gives the same error bound at
> every delivery time. Independent private waiting channels preserve the product
> structure. The local delivered-pair preparation difference from the ground-pair
> reference then has complete norm at most `2p_bad+epsilon_src`; this fixed
> per-pair amount is included in the local expansion budget, with no requirement
> that the whole-reserve trace distance be small.

Here a fixed prescribed delivery schedule suffices. If scheduling depends on
external controls, the actual delivered preparation must have the same complete
local bound; reduced marginal estimates are not a substitute.

The permanent-output exclusion is essential to this particular inference.
An arbitrary CPTP waiting channel fixing the **reduced** pair state can correlate
the pair with its physical environment. If those modes later enter accessible B,
the bound `2p_bad+epsilon_src` does not follow from reduced contractivity alone.
Require the full joint delivered-source bound, or rederive a conservative joint
gentle-projection bound (generally of square-root order) and pay it. This is the
same future-access boundary correctly stated for the optional bosonic reset.

For correlated classical fluctuations in commuting N,V amplitudes, exact omega_j
is fixed on every trajectory, so the product remains exact. With imperfect
initial private pairs, the unconditional delivered state need not remain product.
A conditional product expansion plus uniform local trace-norm error bounds can
still yield a signed all-subset expansion after averaging; claim that argument
explicitly if used. The simpler independent-private-channel extension above is
sufficient and avoids needing this extra argument.

No other mathematical correction is required by this review at the stated
physical and port premises. In particular, U is clearly diagnostic in the
powered two-body representation, future source isolation is explicit, the
optional reset does not reuse reduced-channel accuracy as a joint-bath estimate,
and the finite reserve's O(nK) hardware is distinguished from O(n) active cells.

## Final delta-check and acceptance

Final dossier SHA-256:
`92cd3cf466b669f39ae9bab6e845330d46470a7280d7519fcc4d9a00216ceb1b`.

**PASS at the stated mathematical and physical-model premises.** I checked the
revised finite-size qualification, K_tot definition and its error/time/hardware
uses, and the new imperfect-source preparation paragraph against the requirements
above. Both required fixes are resolved. The source extension correctly requires
independent private CPTP waiting that fixes omega and permanent exclusion of its
waiting-environment outputs; the per-pair `2p_bad+epsilon_src` budget is valid.
No required mathematical correction remains from this review. The expressly
open physical/capability claims remain open and are not promoted by this PASS.
