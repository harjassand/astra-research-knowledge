# Seed-interrupted dormant section: the correct positive source

30 October 2026. Working reduction, conditional on the isolated dormant weighted Green candidate. Not a full-cycle drift proof.

Start on B=q,D=0,A>=m, with C frozen, r=C+A-H(q). Stop at the first subsequent return to B=q (after leaving the initial connector phase) or at the first true seed. A seed can occur before leaving the initial B=q phase and is then an immediate terminal event. Retain its actual B phase; do not pretend it is a section return. Let w=exp(theta r), and optionally stop on entering a fixed residual threshold.

Candidate source bound:

`E[(w_stop-w_start)_+] <= C_theta w_start (1+A_start)^-m`.    (S)

This is the source norm needed for an f_m dormant correction. It is different from integrating the raw positive physical generator, whose neutral phase cancellations have been lost.

## High incoming A mechanism

Until A falls below half its incoming value, every positive low-phase immigration race has probability at most C/A_start. A high-phase immigration has probability O(A_start^-m) before the next seed/clearing competition, uniformly in B>=q. Conditional on a seed-or-clearing event, the seed probability p=(k1+k5)/(k0+k1+k5) is fixed and positive; births cannot change that mark distribution.

Reaching the half-A boundary before a seed requires at least A_start/(2m) clearings, because only clearing can lower A on the dormant face and it lowers A by m. This has probability exp(-c A_start). Births can only increase A, so they cannot invalidate the count.

Use the exact phase height J(B)=B-(q-1)1_{B>=q}. Before m noncompulsory low immigrations or a high immigration, clearing count is bounded by a fixed constant plus (q-1) times high-activation count; low activations add no J. High activations have probability O(A_start^(1-m)) per active high phase. Each surviving seed/clearing choice has survival probability 1-p. Together these two facts give a summable event-type enumeration while A remains above half its input; no small bound on low activations is asserted.

On a path which returns to the section or stops at a seed before these designated events, r cannot increase. In particular, a low-to-high immigration wrap needs q-1>=m noncompulsory races unless a previous high activation supplied the phase, in which case the intervening downward clearing cancels the wrap. This cancellation must be verified on the full retained phase history, not by bounding each jump's positive part.

Thus positive terminal residual displacement requires m low race factors, a high immigration factor, or the exponentially rare half-A entrance. The same enumeration with a fixed exponential tilt pays subsequent wraps once A_start is large: each wrap has bounded exponential reward, whereas the required new immigration probabilities are small. This gives the proposed O(A_start^-m) source on the high-A portion.

## Finite-A head and remaining proof obligations

For bounded incoming A, f_m(A) is bounded below by a positive constant. The isolated same-exponent dormant Green, if accepted, supplies the required finite terminal w norm uniformly in C and B, so it covers that head. The exceptional half-A entrance must likewise be weighted before multiplying its exponentially small probability; an independent unweighted probability times an arbitrary terminal moment is invalid. A direct tilted block iteration, or the same-exponent Green evaluated with the actual entrance law, is required.

Two items remain uncompleted in this note:
1. A fully explicit phase-word proof that positive terminal r at a seed-interrupted stop consumes the stated m race factors, with no uncounted initial B=q seed convention.
2. The weighted half-A entrance estimate, not merely its unweighted exponential probability.

Therefore (S) is NOT yet accepted even conditionally on pointwise Green finiteness. The note records the actual source and a plausible paid mechanism, not a replacement of the missing estimate by an assumption. It also does not supply the negative useful-activation term, the seeded continuation to the section, or the global complementary residual bound.
