# Whole mathematical challenge of coherent fault admission

29 October 2026. Verdict: **ACCEPTED at the explicit model and receiver
scopes below.** This is a whole analytical challenge, not an extrapolation
from the finite consumer. No further model, trajectory, bath, or numerical
parameter case was run by this reviewer.

The reviewed final inputs are:

| Root input | SHA256 |
| --- | --- |
| PROOF.md | 216c08b8573205aca5db516dc07f24d0a689b7533bbc1af6776e380075ec5828 |
| MW_RECEIVER.md | 1f022e6f006d3f052e50f62d15f884051913745780165261c4f71e40d58ce18b |
| ASYNC_GAUSSIAN.md | bc81c307442eb5f1dec4ae1afa2bb84fe00be495ebb072b7e5f158aa1bfa9b24 |
| consume.py | a00a62b886a2dea175e6d97be67a41e2d4a330a106648983c77fcf748fb2e2e4 |

They are under `../../root_coherent_admission/`. The final physical-model
paragraphs were reread after the last amendment. The separate nominal CLOCK
environment and the independent free Gaussian DATA baths are now explicit
tensor factors. The nominal Hamiltonian acts trivially on those DATA baths;
it does not hide additional check-conditioned couplings to the same fields.
That distinction is necessary for the specified free-correlation Wick proof.

## 1. What was reconstructed

The following checks are theorem-level; the finite diagnostic is separate.

**Boolean cancellation and asynchronous enumeration.** For nonempty R the
Mobius coefficient of the large-component event is the negative coefficient
of its good indicator. The latter factorizes over the induced components of
H[R]. Any component smaller than d supplies the zero nonempty coefficient
of a constant function. Thus all surviving components have size at least d,
and the coefficient bound 2^|R| is valid without positive fault flags.

I supplied the explicit deferred-decision proof in
[BFS_AND_POLYMERS.md](BFS_AND_POLYMERS.md). Its load-bearing invariant is that
every revealed read flag has its entire check/block occupation row exposed.
Previously observed failure runs cannot then hide new children. With all
forced roots queued initially, conditional scan bounds and the tower
property give E[4^Y|past] <= 1024/793 < 2. The queue supermartingale yields
E 2^|cluster(S)| <= 4^|S| for multiple prescribed roots, even when scans overlap
and clusters merge. Root-set enumeration is performed inside the expectation;
it does not use the false inequality E exp(X) <= exp(E X). Consequently

    E ||bad map|| <= exp[4 N theta (2 epsilon/theta)^d] - 1,
    theta = 1/(64 b K),  2 epsilon <= theta.

Only independent exogenous Poisson OCCURRENCE flags are averaged in this
argument. A flag is not a Born measurement result or a certificate of read
correctness. Every Born record remains unnormalized in the quantum process.
The inclusive strategy-norm bound is uniform for each complete fixed
exogenous schedule before averaging it.

**Correctness of the asynchronous conclusion.** Small components support
only a zero-syndrome Pauli of weight below the code distance, hence a
stabilizer. With the specified nominal Pauli-times-check record algebra,
the good sum is invariant under logical Pauli twirling. This proves distance
at most twice the bad-map bound to SOME positive logical Pauli channel.
It neither bounds that channel's nonidentity weight nor supplies memory
persistence. A generic minimum-weight decoder is not justified by this
component criterion: its corrections can introduce additional support.

**Static minimum-weight receiver.** I reconstructed the forced/forbidden
identity

    H(T,Z) = sum_(U subset Z) (-1)^|U| Bad(T union U),
    ||H(T,Z)|| <= epsilon^|T| (1+epsilon)^|Z|.

It is a finite linear identity for ONE consistent family, with no
independence, commutation, or positivity assumption on its maps. The
encoded-support property is a separate premise and does not follow from an
inclusive norm bound alone.

For a syndrome subset Omega, the summed corrected decoder R_Omega is CP
and trace nonincreasing: the sum of its Kraus adjoint-products is the
syndrome projector for Omega. Its complete norm is therefore at most one,
independently of the number of syndromes. This controls correlated complex
environment coefficients; no norm is taken separately for every syndrome.

The relevant components contain BOTH the declared fault support and the
chosen correction. Minimum weight implies at least half the sites of every
nonzero component lie in the declared fault support. Fixing forced labels
inside each component and forbidding labels on its boundary leaves all
outside faults resummed. Thus the stated general bound is paid:

    L = 2^D (1+epsilon)^[D(1+Delta)] epsilon^[1/(2q)],
    Xi = sum_(connected K, |K|>=d_code) L^|K|,
    ||Lambda_MW-id||_diamond <= min{2, 2[exp(Xi)-1]}.

The cancellation of all small terms into a scalar identity, followed by
trace preservation to control that scalar, is valid even though the
individual fault maps are not channels. D is TOTAL experiment incidence,
not instantaneous incidence. Perfect final syndrome extraction and global
minimum-weight correction remain explicit inputs, with their implementation
and computational cost unpaid here.

## 2. Physical admission and the constructive strengthening

I contributed [HEREDITARY_HYBRID.md](HEREDITARY_HYBRID.md), subsequently
incorporated and credited in the root source. This portion is not a separate
external audit of my own result. Root independently challenged the earlier
Gaussian resummation on which it relies. The current review discloses that
author/reviewer overlap while checking the combined interfaces.

For the static receiver, one label denotes an independent Gaussian DATA
bath over the whole finite storage window. After first disabling every
forbidden seed, the mixed finite difference over the forced seeds is again
a physical Gaussian correlation-variation comparison. Each selected pair
belongs to one seed, so r forced seeds require at least r pairs. Exact
reference evolution retains every other bath and the strong nominal clock
environment. The same estimate holds uniformly for every disabled set:

    ||H(T,Z)|| <= epsilon^|T|,
    epsilon = e eta <= 1,
    eta = 8 alpha^2 sup_j integral_[0,Twin]^2 |C_j(t,s)| dt ds.

This hereditary estimate removes the forbidden-boundary factor for this
physical model: L_phys = 2^D epsilon^[1/(2q)]. These comparison experiments
are a proof construction, not an acquired exponential collection of channel
outputs. Propagation by the check-diagonal, logical-identity nominal
Hamiltonian preserves source Pauli labels. On encoded input, tracing its
fixed environment gives the required scalar Pauli-pair coefficients, even
though interaction-picture operators need not be spatially local.

For the asynchronous receiver, a label instead denotes a complete
seed/time-slot coupling switch. The SAME free bath is reused between its
active slots. The reference has all data couplings off on the marked slots,
so within-slot data disturbances are marked as well as cross-slot memory.
Selected pairs touching a marked slot INCLUDE pairs with both endpoints
in that slot. At least ceil(r/2) pairs cover r slots; the row estimate

    eta <= 8 alpha^2 tau M0,
    M0 = sup_j integral_R |C_j(u)| du,
    epsilon = sqrt(2 e eta),  eta <= 1/2

therefore admits the actual full-slot-toggle family to the asynchronous
theorem. The final partial-block convention only extends the auxiliary
exogenous flag process. Its last-block flag cannot cut between actual
slots, because endpoint flags are ignored. No additional physical
evolution or bath reset is inferred.

The accepted fixed passive band gives M0 <= 16 A0^2 uniformly at inverse
temperature at least one. The rational overpayments 384 alpha^2 Twin A0^2
for the static epsilon and 28 alpha A0 sqrt(tau) for the asynchronous epsilon
follow. The static code/delta rule in the final source correctly pays the
animal count and exp(Xi)-1. None of these conservative constants has been
qualified as a useful physical rate.

## 3. Strong conventional comparison

[Han et al., 2609.20537v1](https://arxiv.org/html/2609.20537v1) already prove
constant code-capacity coherent/local-CPTP qLDPC thresholds, including
minimum-weight decoding with perfect final syndrome extraction. Appendix C's
component/correction density argument, CP syndrome selectors and
large-component resummation are controlling prior here. The root package
does not invent generic coherent qLDPC thresholding. Its distinct input is
the inclusive-only nonfactorizing family, the stronger actual hereditary
Gaussian hybrid, and the specified annealed read graph; historical priority
for those extensions is UNKNOWN.

[AGP, quant-ph/0504218v3](https://arxiv.org/pdf/quant-ph/0504218v3) supplies
ordinary coherent fault-path norm methods. [Composable Quantum
Fault-Tolerance, 2508.08246v2](https://arxiv.org/html/2508.08246v2) is a strong
comparison for complete norms and cluster/decoder support costs. Liu--Lu
2408.04009v3 Lemma 1 and Ng--Preskill 0810.4953 supply the established Gaussian
variation/fault-path mechanisms; the prior frozen packet pays their stated
well-defined dynamics and correlation premises.

An equally informed bounded-Hamiltonian route is stronger when applicable:
mixed Duhamel differences for full source/environment seed operators of
norm at most alpha give the hereditary bound (2 alpha Twin)^|T|, without
Gaussianity or independent baths. The r! orders cancel the simplex volume
denominator; no extra factor e is needed. The Gaussian operation addresses
unbounded fields, correlation-based inputs and zero-mean quadratic weak
coupling, rather than defeating that ordinary bounded-operator method.

## 4. Execution, resources and remaining gates

The root consumer was whole-code read, not rerun. Its saved exact diagnostics
cover 1099 graphs, 6504 graph/threshold cases, 202012 Boolean coefficients,
729 disjoint forced/forbidden specifications on six labels, and a five-block
one-check read-graph diagnostic. The separate standard non-CSS [[5,1,3]]
example correctly warns against identifying small fault components with MW
correctness. The current root consumer took 0.17169816700334195 seconds;
its earlier saved version took 0.15061508301005233 seconds. Those are root
implementation diagnostics, not a second execution by this reviewer or
proofs of the all-size theorems. There were no random draws or physical
trajectories. This review added analytical derivations and transport hashes;
the human/model analysis cost was not metered.

The actual surviving operation is a complete-norm admission theorem for
finite-horizon coherent correlated noise with explicitly preserved source
labels, including an independent unbounded Gaussian-data-bath realization.
Static recovery gives logical correctness with a perfect final global MW
receiver. Asynchronous recovery gives Pauliization only. Neither supplies
positive physical fault flags, a causal Markov Pauli process, autonomous
decoding, calibrated noisy readout, an arbitrary-time fixed-noise memory,
or a bounded-density 3D reservoir apparatus.

Factorization at the initial source/DATA-bath time is a genuine physical
gate. The bath after a window can be source correlated, so the static
one-window result cannot be restarted as if it had fresh independent baths.
A finite closed reservoir also lacks an all-time integrable absolute
correlation norm. The asynchronous continuum theorem is uniform in its
finite horizon given that actual kernel premise; it does not acquire
indefinite finite hardware, entropy export, or a microscopic implementation
of the nominal ideal operations. The full source check algebra must remain
exact; arbitrary physical Hamiltonian perturbations are not silently
included in the nominal check-diagonal model.

There is no remaining substantive correction requested at these scopes.
This is an internal mathematical acceptance, not historical novelty,
practical advantage, physical validation or a storage-lifetime claim.
