# Acquired physical operations and the complete programs they support

29 October 2026. Root formulation after the kinetic-prefactor challenge.
This is the main consequence-level principle. Canonical energy-family
completion remains a stronger conditional corollary.

## 1. Actual operations remove an unjustified kinetic extrapolation

Rates (2,1/2) and (2a,a/2), a>0, have the same two-state biased Gibbs law
but different dynamics. An energy change does not determine barrier kinetics.
Acquire actual operations, certify a common predictive representation, and
compose THOSE operations into arbitrary causal programs. No canonical relation
between different operations is needed for this consequence.

## 2. Native menu and known reversible weights

On one finite or countable hidden space, observe only label Y in{1,...,k}.
Baseline Q_0 is reversible for probability pi. Actual operation j in a finite
menu has conservative generator Q_j, supplied exit ceiling Lambda_j, and
detailed balance in pi(x) w_j(Y(x)). Each positive label weight w_j is known;
w_0=1. Kinetic prefactors, including internal same-label rates, may differ
arbitrarily and be unknown. No hidden-state-count bound is imposed.

The physical switching interface changes generators without an extra unmodelled
state kick or memory update. If switching does such a thing, its actual map
needs separate acquisition. Neither this interface, hidden reversibility,
stationary preparation nor the rate ceiling follows from a visible fit.

Let H_j=M_sqrt(w_j), r_j=max sqrt(w_j)/min sqrt(w_j). For an independent
exponential clock of rate alpha_j,

    S_j=alpha_j(alpha_j I-Q_j)^(-1),
    spec(S_j) in [a_j,1], a_j=alpha_j/(alpha_j+2Lambda_j).

The space is L2(pi w_j). Choosing alpha_j=2Lambda_j>0 gives a_j>=1/2.
The zero-rate case can use any alpha_j.

## 3. Hidden conditional moments have a chronological acquisition

Use bounded controlled future-word features f_i=O_i1. Words contain actual
forward pulse resolvents and label projections. Make the dictionary label-local
and include all label indicators; then V=span{f_i} contains1 and is invariant
under every visible multiplication. Require a nonsingular acquired Gram matrix.
Its baseline projection P is orthogonal in every weighted space.

    S_j*=M_(w_j) S_j M_(w_j)^(-1) in L2(pi),
    <f_i,T f_l>_pi=<1,O_i* T O_l1>_pi.                    (1)

The adjoint word uses the SAME forward pulses, reversed in order, with visible
endpoint weights w_j(Y_before)/w_j(Y_after). It starts from baseline pi.
It is not a physical reversal, microscopic copy, or new stationary preparation.
Weight range grows by at most r_j^2 per adjoint stage and is charged.

Center weight w_j with zero, one, or two independent clock stages acquires

    G_j=<F,w_j F>, K_j=<F,w_j S_j F>, D_j=<F,w_j S_j^2 F>,
    R_j=D_j-K_jG_j^(-1)K_j
       =<(I-P)S_jF,w_j(I-P)S_jF> >=0.                   (2)

Two fresh independent clocks are essential; doubling one random duration is
different. Censored/digital clocks approximate these operators with paid error.

## 4. Exact operation-algebra theorem

All R_j vanish iff V is invariant under every Q_j. The resolvent is boundedly
invertible; its restriction to finite V is invertible, proving the equivalence.

    L_j=alpha_j[I-(G_j^(-1)K_j)^(-1)]=Q_j|V.             (3)

Together with label projectors, initial expectation and constant1, these
matrices determine ALL complete visible path laws from baseline pi under any
well-posed predictable program selecting j from visible history and external
randomness. Arbitrary durations and switching are allowed. Measurable convex
mixtures are represented when actually implemented; matrices do not implement
an unavailable physical mixture. Uniform exit ceiling prevents explosion.

Proof: within-label killed generators and cross-label jump operators preserve
V. Their chronological products reproduce every visible path density for a
fixed history-selected program. Integrate jump times and external randomization.
One record is chosen before the policy. Hidden-state feedback, new physical
operations, and arbitrary unacquired microscopic preparations are excluded.

Predictive coordinates can be signed. Exact probabilities have the native
source as a positive realization; no r-state physical simulator is claimed.

## 5. Complete visible-path error from approximate closure

Let epsilon_j^2 be the largest normalized defect eigenvalue, c_j the minimum
compression eigenvalue. Weighted generator leakage is bounded by

    d_j=alpha_j epsilon_j/(a_j c_j),

or safely alpha_j epsilon_j/a_j^2. Use finite-data upper/lower confidence
bounds, not the empirical plug-in values. Put

    D=max_j r_j d_j,      J=max_j r_j Lambda_j.

Against the SIGNED prediction from true compressed generators PQ_jP,

    L1(visible-path error)<= k^2 T D exp((k-1)JT).        (4)

Within a label, w_j is constant, so Q_j's killed generator is self-adjoint
nonpositive in baseline L2(pi). Its propagator and block-diagonal compression
are contractions. Their difference over time t is <=tD. A jump a->b has
operator E_aQ_jE_b, norm<=Lambda_j sqrt(w_j(b)/w_j(a))<=J, and discrepancy
from block-diagonal compression <=D. The latter follows by conjugating the
self-adjoint weighted omitted block with H_j; all label projections commute.

For m jumps, chronological telescoping bounds a path-density error by
T D J^m+mD J^(m-1). There are k(k-1)^m label words and a time simplex of
volume T^m/m!. Summing proves(4). At m=0 omit the second term. Along each
visible prefix, feedback chooses the same deterministic operation program on
both sides, so no policy derivative or hidden mixing estimate is needed.

If numerical/compression killed-block errors are <=zK, jump-block errors <=zJ,
and initial functional error on V in dual L2(pi) is <=e_init, the same proof gives

    E_T=k[e_init+T(D+zK+(k-1)(D+zJ))]
                 exp([zK+(k-1)(J+zJ)]T).                (5)

Consistent label blocks are needed. Estimated killed propagators have norm
<=exp(zK t); jump norms are <=J+zJ. Every bounded visible-path payoff g has
error <=||g||_infinity E_T, uniformly over the actual program class. Clipping
a scalar prediction to its known range cannot worsen scalar error, but does
not create a single positive model law. Only with a positive realization is
half the L1 bound a TV distance between laws. The conservative exponential
horizon factor is retained; infinite-time lifetime error is not inferred.

## 6. Two distinct completion scopes

For the actual finite menu, no fixed kinetic-prefactor assumption relates
operations. If the stronger canonical law q^h=q h(Y_j)/h(Y_i) is warranted,
the main finite-pulse note additionally completes every unmeasured amplitude
from baseline and k-1 biases. That is a separate physical corollary.

There is also a kernel-only version WITHOUT a source rate ceiling. Suppose
the actual operations are fixed-duration reversible Markov kernels T_j with
known weights w_j. Use T_j and two successive calls T_j^2 directly in(1)-(2).
Zero defect certifies invariance and all causal programs of those exact calls
and visible endpoint measurements. No generator inverse, exponential clock,
or hidden spectrum floor is then needed. This controls the specified endpoint
record, not unobserved between-call paths, arbitrary durations or a clock side
record that was discarded. For a fixed m calls the elementary telescoping
bound has explicit k^m and operator-norm factors; no favorable m scaling is
claimed. It is a different, smaller execution interface rather than an inferred
microscopic clock bound.

## 7. Addition and limits

Invariant spaces, observable-operator models, Schur residuals, resolvent learning
and reduced solvers are established machinery. The candidate addition is the
actual acquisition of hidden conditional inner products and leakage through
weighted reversible operations; controlled tests can expose and add directions
absent from complete passive prediction. No same-hidden-state batched futures
are assumed. Weighted depth, preparations, clocks, conditioning, and numerical
execution are charged. No practical speedup or physical experiment is claimed.
