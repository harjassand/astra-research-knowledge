# Two starting lemmas for a tempered proposal screen

Contributor: Astra PRO3 / safeguarded_cost_challenge.
Date: 22 October 2026, Australia/Brisbane.
First recorded clock for this follow-up: 21 October 2026, 16:22:17 UTC.

**Status:** both preparatory claims below are proved. They identify a possible
next frontier and a failed direct reuse of the linear-domination theorem.
They do **not** resolve the robustness, mixing exponent, or efficiency of the
tempered hybrid. No broad proof search or numerical experiment was performed.

## Contract

Let the state space be finite. Let q and pi be strictly positive probability
vectors. Let Q be a fixed symmetric stochastic matrix, and fix `0<eta<1`.
For distinct x,y, define the local transition by

`L_eta(x,y) = Q(x,y) min(1,(q(y)/q(x))^eta)`
`                        * min(1,(pi(y)/pi(x)) (q(x)/q(y))^eta)`.

The diagonal completes each row to one. This is ordinary two-stage delayed
acceptance, with q raised to power eta in the first stage. The displayed ratios
can be calculated from unnormalized target values; their target normalizer
cancels. The normalized pi used in the proofs describes the probability law,
not additional information supplied to an implementation. Q and L_eta remain
fixed within each instance.

The case eta=0 is ordinary pi-MH(Q), while eta=1 is the full q screen studied
by the principal. The present two lemmas concern `0<eta<1`; endpoint comparisons
are identified separately below.

For completeness, reversibility follows from the symmetric off-diagonal flow

`pi(x) L_eta(x,y)`
` = Q(x,y) min(q(x)^eta,q(y)^eta)`
`           * min(pi(x)/q(x)^eta,pi(y)/q(y)^eta)`.

## Lemma 1: a nonlinear bound on proposal-start inflow

For every set A,

`q L_eta(A) <= q(A) + [q Q(A)]^(1-eta) q(A)^eta`
`           <= q(A) + q(A)^eta`.

The bound can also be clamped at one. Empty-set terms are interpreted as zero.

**Proof.** Rejected proposals and proposals that leave the current state
unchanged contribute at most q(A) to the next-state probability of A. The
accepted off-diagonal inflow is at most

`sum_{x in Omega, y in A} q(x) Q(x,y) (q(y)/q(x))^eta`
` = sum_{x in Omega, y in A} Q(x,y) q(x)^(1-eta) q(y)^eta`.

Including x=y only increases this nonnegative upper bound. The second-stage acceptance was
bounded by one, and the first by `(q(y)/q(x))^eta`.

Apply Holder's inequality to the finite measure on pairs having weights
`Q(x,y)` and restricted to y in A. With conjugate exponents
`1/(1-eta)` and `1/eta`, the last display is at most

`[sum_{x in Omega, y in A} Q(x,y) q(x)]^(1-eta)`
` * [sum_{x in Omega, y in A} Q(x,y) q(y)]^eta`.

The first bracket is q Q(A). The second is q(A), because symmetric stochastic
Q has column sums one. Since q Q(A)<=1, the claimed inequalities follow. No
assumption that Q preserves q was used. End of proof.

This estimate is a setwise nonlinear bound. It is not the measure inequality
`qL_eta <= Lambda q` for a class-uniform constant Lambda.

## Lemma 2: no uniform linear bound for eta below one

Fix `K>0`, `0<eta<1`, and any `0<k<K`. For sufficiently small r>0, put

`ell=log(1/r)`, `p=k/ell`,
`q=(1-r,r)`, `pi=(1-p,p)`,

and let Q swap the two states. Then every sufficiently small member is strictly
positive, has forward KL strictly below k (hence below K), and

`q L_eta({rare}) / q({rare}) ~ r^(eta-1) -> infinity`.

Consequently there is no finite constant Lambda, depending only on fixed
K and eta, such that `qL_eta <= Lambda q` for all these admitted instances.

**Proof: entropy.** Eventually `0<r<p<1`. Exactly,

`D(pi||q) = (1-p) log((1-p)/(1-r)) + p log(p/r)`
`          = (1-p) log((1-p)/(1-r)) + p log p + k`.

The first term and p log p are both negative, giving `D(pi||q)<k<K`.
Both vanish as r tends to zero, so the divergence tends to k. No singular
limiting law is used as an admitted finite member.

**Proof: local inflow.** Write `d=r/(1-r)`. From the common state to the rare
state, the first acceptance is `d^eta`. The second is

`min(1, [p/(1-p)] d^(-eta))`.

It equals one for all sufficiently small r, because
`p r^(-eta) = k r^(-eta)/log(1/r) -> infinity`. Thus the common-to-rare
transition probability is exactly `d^eta` eventually. The reverse transition
probability is then exactly

`[(1-p)/p] d^eta`,

which is below one and tends to zero. Hence

`q L_eta({rare})`
` = (1-r) d^eta + r {1-[(1-p)/p] d^eta}`,

and division by r gives

`(1-r)^(1-eta) r^(eta-1) + 1 - [(1-p)/p] d^eta`.

The first term diverges and the final correction tends to zero. This proves
the stated asymptotic and the failure of uniform linear domination. End of proof.

### Endpoint consistency

The argument that the second acceptance eventually equals one requires
`eta>0`. It must not be silently applied at eta=0. At eta=0, ordinary MH instead
has common-to-rare probability `p/(1-p)` and reverse probability one, giving
`qL_0({rare})/r ~ p/r = k/[r log(1/r)] -> infinity`.

At eta=1, the displayed formula for positive eta gives a ratio tending to two,
consistent with the principal's uniform `qL_1<=2q` condition. There is therefore
no conflict at the endpoint already covered by that theorem.

## What these lemmas permit next

The full q screen guarantees linear one-step domination. Every fixed weaker
screen loses that sufficient condition even on a two-state, bounded-forward-KL
family. Thus the accepted theorem cannot be invoked for eta<1 by asserting the
same constant domination hypothesis.

This is **not** an impossibility proof for proposal-start robustness or a sharp
mixing exponent of the fixed tempered hybrid
`(I+alpha G+(1-alpha)L_eta)/2`. Linear domination has been shown sufficient,
not necessary. The nonlinear set bound may support a different argument, or a
more elaborate construction may show a genuine obstruction. Neither conclusion
is established here. These lemmas also establish no finite-time improvement,
no target-evaluation advantage, and no recommendation to change a real sampler.

## Cost and execution record

Both lemmas are direct finite-sum arguments. No external data, numerical
trajectory, matrix search, old-proof rerun or numerical scientific calculation
was needed. The follow-up involved one clock read, writing this source note,
and source hashing for handoff. These preparation/verification operations are
not measurements of sampler efficiency or of the full principal's research cost.
