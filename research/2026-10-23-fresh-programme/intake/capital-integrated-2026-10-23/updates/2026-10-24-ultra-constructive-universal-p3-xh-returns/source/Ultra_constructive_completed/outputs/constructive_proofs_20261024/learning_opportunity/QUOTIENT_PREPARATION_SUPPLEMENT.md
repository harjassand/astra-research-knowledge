# A stronger acquired preparation operation

24 October 2026. Mathematical supplement; **not the core-table implementation measured in the executable runs**. Luna batched_mean supplied the quotient-rejection observation. I independently verified it and derived the strict-prefix inversion bypass and finite timeout accounting, with root's checks. Source/comparator/priority limitations from `PROOF.md` remain in force.

## Balanced quotient, with exact rejection cost

Use the exact acquired prefix Fₜ and the notation of `PROOF.md`: Lₜ has dimension n−rₜ; Aₜ:Lₜ→F₂ᵗ is linear of rank aₜ. Set

    sₜ=t−aₜ.

Let πₜ be the quotient map modulo im Aₜ. For a complement Rₜ to Lₜ, the acquired map

    Gₜ(z)=πₜ Fₜ(Rₜz),      z∈F₂^rₜ,

has sₜ output bits. The prefix balance calculation already proved shows

    |Gₜ⁻¹(q)|=2^(rₜ−sₜ),   for every quotient value q.       (1)

Thus 0≤sₜ≤rₜ, and Gₜ is a balanced surjection. Draw uniform z, accept iff Gₜ(z)=πₜy, then sample a uniform affine lift v solving Aₜv=y+Fₜ(Rₜz). The accepted core is uniform on the correct quotient fibre, and every accepted core has the same number of lifts. The output Rₜz+v is therefore **exactly uniform** on Fₜ⁻¹(y).

Acceptance probability is exactly 2^(-sₜ), independent of y. Preparation takes 2^sₜ core evaluations in expectation, polynomial linear algebra, and polynomial memory; it need not enumerate 2^rₜ cores. The expected fresh-bit use per accepted object is

    rₜ 2^sₜ + (n−rₜ−aₜ).                                  (2)

When sₜ=0 this is exactly n−t bits. For sₜ>0 the extra failed-proposal bits are paid. This is an exact sampler, with its random running time exposed; there is no hidden conditional-preparation oracle.

The important acquired parameter is

    κ(Q)=max_(0≤t<n) sₜ.

It is computed stage by stage from acquired coordinates, not supplied. κ≤b(Q), but can be much smaller. If κ is large, the rejection cost remains exponential. There is no theorem here that generic quadratic inversion is efficient or hard.

## Inverse rank without building the final core table

The t=n radical is unnecessary. Given the requested complete output y, prepare an exact uniform point in the acquired (n−1)-bit prefix fibre. This fibre has exactly two points. Evaluate the acquired final polynomial and retain the point iff Qₙ(x)=yₙ. Exactly one of the two matches, so acceptance is 1/2 and the returned point is the unique inverse.

This inverse takes two strict-prefix preparations in expectation, hence expected work bounded by poly(n)·2^(s_(n−1)+1). It uses no comparisons after acquisition and no final 2^b(Q) table. A finite cap on the two-point rejection gives UNKNOWN with its explicit failure probability.

The same two-point fact also makes acquisition of Qₙ simpler: draw from the known (n−1)-prefix fibre until both distinct inputs have appeared (three draws expected), compare them once, and identify the queried x by raw-vector equality. The smaller point has final bit 0, the larger has final bit 1. These exact last-bit labels can be interpolated directly. Neither this acceleration nor the rejection inverse is represented as executed by `acquire_quadratic_order.py`.

## A strict separation from the final polar-rank cost

Let n=2m+1 and consider the quadratic shear

    Qᵢ(x)=xᵢ                     (i=1,…,n−1),
    Qₙ(x)=xₙ+sum_(j=1)^m x_(2j−1)x_(2j).

It is a bijection: the last coordinate is inverted by the identical shear. Its final polar form has rank n−1, so b(Q)=n−1. But every strict prefix is linear with Aₜ onto: rₜ=sₜ=0 for every t<n, and κ(Q)=0. Conditional preparation, all-coordinate acquisition and the inverse bypass are polynomial for this family even though a final-common-radical table would be exponential. This family is also inside the older complete-triangular comparator's class; this is a cost correction and a broader parameterization, not superiority to N780 on its overlap.

Invertible affine *input* hiding preserves the argument (strict-prefix coordinates remain independent affine forms). Arbitrary affine output mixing can move the nonlinear bit into earlier significance positions and increase κ; no output-invariant κ claim is made.

## Short fibres and finite caps

The fresh-median proof enumerates fibres of size N≤64 to repair discrete ties. A quotient-only implementation cannot silently pay 2^rₜ to enumerate them. Instead draw exact uniform points from the prefix fibre until all **known N** distinct inputs have been collected. The stopping condition is certified by raw equality and the known fibre size. The expected number of accepted preparations is N H_N≤64 H_64<304; sorting those N objects then gives the exact midpoint. This uses constant expected preparation overhead, not a free exact enumeration primitive.

Neither an erroneous acquired prefix nor a broken class promise may be allowed to make rejection run forever. Here is a finite capped construction, stated for the fresh-median learner. Let δ_a be its interpolation-error allocation; set R as in the main theorem with δ_a and

    L=7 nDₙR,
    J_N=N ceil(log₂(N L/η₂)),
    M=L max(511,J_64).

L bounds the total weak-label requests. Cap each short-fibre collection after J_N accepted preparation calls. On a correct prefix, a union bound over N unseen objects gives failure at most

    N exp(−J_N/N) ≤ η₂/L.

Thus all collections succeed except with probability η₂. M then bounds the total requested conditional preparations, including large-fibre medians. For each such preparation at acquired stage t, permit at most

    Bₜ=2^sₜ ceil(log₂(M/η₁))

uniform-core proposals, then return UNKNOWN if none succeeds. On a correct prefix its failure is at most

    (1−2^(-sₜ))^Bₜ ≤ exp(−Bₜ2^(-sₜ)) ≤ η₁/M.

The dyadic ceilings are finite integer calculations; no exact-real logarithm oracle is needed. Every branch now has a finite timeout, including an erroneous learned prefix with an empty quotient fibre. Since computed sₜ≤t<n, an all-branch exponential upper cap still exists.

Couple this implementation to the ideal uncapped correct-prefix sampler on the same random tapes. Until a first interpolation error or timeout the experiments coincide. A first-error/timeout union bound gives

    P[correct completion with all caps respected] ≥1−δ_a−η₁−η₂.           (3)

On this simultaneous event the classical work is 2^κ(Q) times an explicit polynomial in n and the logarithmic confidence factors; memory can be polynomial. Outside it, acquired parameters can be worse than their true-prefix values, so (3) must not be promoted to an unconditional expected FPT bound. One can additionally impose a uniform user resource budget and return UNKNOWN on exceeding it.

This coupling also avoids conditioning the statistical proof on accepted/capped histories, which could otherwise bias later offsets. No failed preparation, rejected core, timeout or source work is hidden from the resource ledger.

## Status

This is a stronger proved-in-model preparation/inverse construction, not an executed large-instance acquisition, an independently accepted theorem, a novelty-cleared primitive, or a civilisation-level result. Any equally informed conventional learner may use this same operation after acquiring the same polynomials. The useful unresolved boundary is efficient exact acquisition when the *acquired strict-prefix quotient deficit* κ is large; replacing it with a latent sampler would merely assume the central difficulty away.
