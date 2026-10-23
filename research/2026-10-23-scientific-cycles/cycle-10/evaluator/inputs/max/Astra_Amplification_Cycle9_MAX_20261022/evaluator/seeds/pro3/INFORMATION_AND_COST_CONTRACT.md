# Information, operations, and costs

## Scientific class

The principal theorem fixes K>0 and alpha in (0,1). At horizon n the public
policy supplies 0<eta_n<1, finite kappa_n>=0, and a finite A_n>=0.
The actual native Q is target-independent, row-stochastic and reciprocal,
with max |log(Q_yx/Q_xy)|<=A_n. The target and proposal are strictly positive
on a finite labelled space and share one supplied population D(pi||q)<=K.
Support size varies over the supremum. The chain starts from q.

The sampler uses exactly the screen
S_xy=(q_y/q_x)^eta (Q_yx/Q_xy)^kappa and the second factor completing the
target Hastings ratio. G, Q, eta, kappa and all mixture probabilities are
fixed throughout a run. The actual rejection diagonal and lazy random
mixture are retained.

## Honest access

q sampling and q-value evaluation are allowed at their actual costs.
An unnormalized target evaluation and an evaluable forward/reverse Q pair
suffice for the ratio calculations. No target normalizer or complete target
table is supplied free. Full caching is allowed, with lookup and storage
charged. K is a population promise, not a statistic inferred from sampled
target values or empirical training loss. A_n is a genuine public proposal
promise, not an estimated maximum over visited edges.

There are no off-support or hidden-support restrictions on the recipient.
If complete analytic target structure is actually known, direct sampling
or enumeration remains a legitimate comparator. The proof's normalized
tables, low/high weight sets, anchor, and absorbed process are verifier
objects, not new free operations available to a sampler.

## Actual operations counted by the law

The theorem counts deterministic actual transitions of C. Each step chooses
I, G, or L with probabilities 1/2, alpha/2, and beta/2. A global step draws
one proposal-q candidate. A local step draws a native Q proposal and
evaluates its forward/reverse probabilities and the required target/q
ratios, subject to available cache. Rejections count as steps. No optional
attempt count is replaced by its mean.

The absorbed first-hit operator is used only in a mathematical bound.
Original C resumes after each first hit in the upper decomposition.
The lower selects a conservative event in the original random choices;
marking all global attempts as failures before capture does not alter C.
The entire terminal union, including global moves among its states, is
retained when calculating escape.

## Resource size of adverse inputs

For M=ceil(exp A_n) and a fixed depth J on a bad subsequence, the new
construction has 1+sum_{i=0}^J M^i native states. Vertex indices can require
J ceil(log_2 M)+O(log J) bits. Exact probability magnitudes involve
J(V+log M), where V is approximately |kappa-eta|A/eta.

An implicit tree representation avoids explicit enumeration but still pays
for indices, native child selection, arithmetic, target evaluations, reverse
Q evaluation, and cache. Exact arbitrary-real exp(A), its ceiling, and
very small masses are part of the ideal mathematical model. No uniform
fixed-word implementation is claimed. Very large supports are required
for some tiny mismatch budgets; this does not itself demonstrate floating
point instability.

The new exact checks materialize only five-state and fourteen-state
fixtures. They are not implementation benchmarks for the large-support
asymptotic inputs.

## Comparator and scope

Pure proposal-start IMH uses the same actual target, proposal, access and
K promise, with its own native cost accounting. Its general minimax
amplitude is K. On the new mismatch lower family its TV tends to zero
while the hybrid retains a positive error lower bound. Deterministic
j/n->t>0 comparisons are law comparisons, not a claim that j global
evaluations cost the same as n hybrid steps.

The strong matched-screen control uses identical q,pi,Q and changes only
kappa to eta in the finite checks. No finite-time ordering or speedup is
inferred. Direct analytic sampling remains available for disclosed
analytic fixtures.

## Explicit exclusions

No adaptive within-run Q or screen policy, deterministic LG/GL schedule,
nonreversible target kernel, empirical KL certificate, noisy target
estimator, general independently chosen edge error, or finite-precision
acceptance theorem is included. The upper energy argument happens to
allow real negative kappa, but the stated exact criterion is for the
requested nonnegative-kappa class. No extension is silently asserted.

Inference, token, monetary, and total discovery costs are unavailable.
Measured Python body time and archive replay time are recorded separately.
No spending, paid compute, hardware, public sharing or outreach occurred.

