# Current owned question: fixed-parameter coherent tree capacity

This checkpoint supersedes the former open feedback and endpoint-stability questions. The scientific mission remains active.

## Precise target

For V_s=cos(s)U+i sin(s)I on the same tree and stationary tau_pi, exhibit a reliable rate above 3/2 at one fixed 0<sin(s)<=1/512, or prove a converse ruling out that target on a nonzero interval. Capacity could increase, remain on a plateau, or decrease. Equality of unassisted and backward-classical capacities at a fixed nonzero s is also unproved.

One s and one normal initializer are fixed throughout every capacity code sequence. Use fixed-n unassisted or noiseless backward-classical communication with every forward qutrit and outcome counted. No reset, bath access, preshared entanglement, backward quantum wire or forward timing channel. Preserve arbitrary reference entanglement asymptotically. Terminal bath return is not imposed on this perturbed capacity problem; adding it would be a new operational contract.

## Why this boundary matters

The permutation endpoint has a strict capacity deficit controlled by compatible tree walks, and exact Dyck return subspaces attain that exponential rate. Coherent no-move amplitude changes the complete process while keeping the same bath, port dimension and faithful product stationary state. Its capacity tests whether the deficit survives for a structural reason beyond exact permutation ranks. Stationarity alone cannot decide that dynamical question.

Endpoint continuity now rules out an immediate jump to full qutrit capacity. It does not decide a small gain, plateau or loss.

## Established starting objects

U is labeled edge reversal, U*=U and U^2=I, on C^3 tensor ell2(V(T_3)). Root ports are child ports 0,1,2; nonroot parent is 0 and children 1,2. eta=diag(3/4,1/8,1/8), pi(root)=1/3 and pi(child)=pi(parent)*eta_a/(3/4). Both U and every V_s preserve eta tensor tau_pi exactly.

At s=0, both capacities equal 3/2. At s=pi/2, the device is identity up to phase and has capacity log2 3.

For 0<theta<1/2, theta>sin(s)/(cos(s)+sin(s)), and

    h2(theta)+(1-theta)log2 cos(s)+theta log2 sin(s)<0,

the feedback capacity is at most

    B(theta)=3/2+h2(theta)+theta(log2 3-3/2).

theta=1/100 gives the strict upper bound 1.58165<log2 3 for 0<sin(s)<=1/512. theta=sqrt(sin(s)) gives the endpoint upper limit.

The lower construction uses a fixed exact Dyck block, identity on the entire bath, followed by an outer code for sparse coherent errors. It requires no bath reset and yields full-diamond error <=4 times the omitted-history amplitude. It proves the matching lower limit uniformly over bath states. Both capacities converge to 3/2 at zero. Its lower semicontinuity actually holds against arbitrary unitary operator-norm perturbations of U on the same space; the upper bound remains specific to the coherent family.

## Actual bottleneck and chosen next step

The upper proof sums amplitude norms and ranks, discarding cancellations. The outer lower code treats deviations as errors. Neither can decide whether their coherent information-carrying contribution raises the rate above 3/2.

Next analyze the exact block operator on superpositions of balanced words with a controlled number of unmatched move/stay alternatives, retaining their final-bath overlaps. Seek a block family with a provably approximately correctable subspace of dimension exponent above 3/2 and an error estimate that remains uniform over the bath through concatenation. The needed evidence is an all-horizon construction, not a small-block rank increase.

A useful negative route is an invariant of the coherent block channel that replaces raw individual-Kraus rank and bounds its asymptotic Choi entanglement at 3/2. Full Kraus ranks appearing after adding I do not by themselves show that communication reaches those ranks.

Retire a method if it requires horizon-dependent s, fresh baths, a stochastic replacement for coherent histories, or lacks reference-uniform error control. Those failures do not retire the broader question.

## Source map and preserved boundaries

The complete current proof is Section 7 of FEEDBACK_AND_STOPPING.tex. Focused reviews are COHERENT_HISTORY_REVIEW.md, HISTORY_EXPONENT_REVIEW.md and LOWER_STABILITY_REVIEW.md. The older COHERENT_STABILITY_LITERATURE.md proposed the lower route; its gap is now resolved by the completed proof and dedicated review.

The unchanged owner ZIP supplies the exact Dyck identity and finite-error-set coding lemma. Feedback and expected-cost questions for U are closed under their stated assumptions. The separate LOCC R1 programme remains completed. Hidden-entropy, N33, N557, IQM and others' programmes remain with their owners.
