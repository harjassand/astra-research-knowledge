# Ordinary methods and matched scientific comparison

The strong general comparator is proposal-start pure independence MH, using
the same q and positive unnormalized target. Under the same certified population
budget D(pi||q)<=K, its minimax TV risk has exact amplitude K/log n. The complete
accepted coupling upper and two-state matching lower are preserved verbatim in
sources/selected_cycle5/COMPARATOR.md and inside the unchanged original ZIP.
They are a received comparison, not a new Cycle6 claim.

The new theorem never improves that leading general minimax amplitude. Its
value is the exact robustness penalty and transport/information mechanism.
For r0>=1 the hybrid amplitude is max{K,B_K exp(-s)}, where
B_K=(beta/alpha)(exp(K)-1). This equals K only when the capture contribution
does not dominate. It exceeds K at sufficiently negative critical offsets.

Cycle6 additionally proves a SAME-INSTANCE separation: on the explicit
three-state family, the hybrid has error ~B_K exp(-s)/log n and pure IMH
has error ~(log n)^-4 for any deterministic m~t n, t>0. Taking
m=floor(alpha n/2) matches expected global proposals. The exact finite
sandwiches and the proof are in GLOBAL_BOUNDARY_THEOREM.md Sections 7-8.

This is an exact-law comparison. It does not equate target evaluations,
uniform generation, q-ratio arithmetic, cache misses or memory. Full caching
is admitted to both methods. For a known three-state support, paying for three
target evaluations permits direct normalization and exact categorical sampling
under the ideal-real oracle; that natural ordinary option is not forbidden.
No practical runtime advantage is claimed for any screened mixture here.

At a future implementation stage all native operations must be charged,
including initialization, full cache operations, q and Q proposal/evaluation
cost, both acceptance stages and numerical precision. The absorbed process,
normalized proof tables and test-dependent bad set are not free sampler inputs.
The present result does not certify finite-precision or empirical-KL behavior.
