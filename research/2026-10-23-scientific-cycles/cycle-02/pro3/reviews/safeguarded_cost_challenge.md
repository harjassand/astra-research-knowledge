# Independent cost and comparison challenge

Contributor: Astra PRO3 / safeguarded_cost_challenge.
First recorded clock: 21 October 2026, 16:12:00 UTC (22 October in Brisbane).
Scope: a distinct finite-time/computational challenge to the principal's proposed
forward-KL robustness theorem under a fixed one-step condition `q L <= A q`.
This note does not independently review that universal theorem or reopen the
received optional-prefix impossibility. The universal proof is the principal's
obligation; this note establishes exact limitations and implementation conditions.

## 1. Verdict

A sharp worst-case exponent K under `q L <= A q` would be a robustness theorem,
not a finite-time improvement over pure independence MH. This distinction is
load-bearing: the four-state example below satisfies the *stronger* property
`q L = q`, has `pi != q`, and has nontrivial local moves, but pure IMH has both
smaller TV error and fewer target evaluations at the same expected global-draw
count. Target evaluations are fully memoized over every previously queried
state. No artificial restriction to caching the current state is used.

Delayed acceptance can also converge more slowly than ordinary local MH. Its
extra rejection may save expensive target evaluations, but that tradeoff needs
an actual workload and a matched resource accounting. Neither invariance nor an
off-diagonal comparison alone proves the desired finite-time TV ordering.

## 2. Exact four-state counterexample with memoized target evaluations

Take

- `q=(1/4,1/4,1/4,1/4)`;
- `pi=(3/8,3/8,1/8,1/8)`;
- `Q` swaps states 1 and 2, and swaps states 3 and 4;
- `alpha=beta=1/2`.

The forward KL is

`D(pi||q)=(3/4)log(3/2)+(1/4)log(1/2) < log(3/2) < 1`.

The q-MH first stage accepts every local move, and the W-correction accepts
every local move because the two members of each pair have the same importance
weight. Thus `R=L=Q`; in particular `qL=q`, and L is pi-reversible. Q is reducible,
as permitted by the proposed class. The global proposal has full support, so
the hybrid is irreducible. There is no singular target or identity local kernel.

All proposal-start laws remain uniform inside each pair. Their error is solely
the wrong pair mass, which the local swap cannot correct. On that one-dimensional
contrast, G has eigenvalue `1/3`, and

`C=(I+G/2+L/2)/2`

has eigenvalue `5/6`. Therefore, exactly,

- `TV(qG^j,pi)=(1/4)(1/3)^j`;
- `TV(qC^n,pi)=(1/4)(5/6)^n`.

At four hybrid steps, compare:

| Operation after common q initialization | TV error | Expected global draws | Expected local proposals | Expected target evaluations including initialization, with complete memoization |
| --- | ---: | ---: | ---: | ---: |
| C^4 | 625/5184 = 0.1205632716 | 1 | 1 | 442183/196608 = 2.2490590413 |
| G | 1/12 = 0.0833333333 | 1 | 0 | 7/4 = 1.75 |
| G^2 | 1/36 = 0.0277777778 | 2 | 0 | 37/16 = 2.3125 |

Thus G already strictly improves both error and target-evaluation cost at the
same expected global count as C^4. It also uses fewer total proposals. This is
a direct counterexample to universal finite-time dominance by the hybrid.

The G^2 row instead matches the hybrid's expected total number of proposals,
but it uses slightly more distinct target evaluations. This difference must
not be hidden. If the matched currency is expected target evaluations, choose
one or two G updates using a private coin, independent of all sampler history,
with probability

`theta=98119/110592`

of two updates. Its target-evaluation cost is exactly `442183/196608`, the same
as C^4. Its expected total number of proposals is

`1+theta=208711/110592 = 1.8872160735 < 2`,

and its TV error is exactly

`67769/1990656 = 0.03404355147 < 625/5184`.

Here both pure-IMH errors have the same signed discrepancy on the two pairs,
so the mixture's TV equals the convex combination, rather than merely being
bounded by it. This second comparator uses more global draws than C^4; no claim
of simultaneous equality in every resource is made. The first comparator already
has equal expected global draws and strictly smaller target/evaluation cost.

### How the target-evaluation costs were calculated

The exact replay state is `(current state, set of all previously queried
states)`. Initialization queries its q candidate. Every global proposal adds
its candidate to the set even if MH rejects it. A local proposal always passes
stage one in this example, so it likewise adds its candidate. A stored target
value is reused without a new oracle call. The algorithm's state is changed
only by the ordinary accept/reject rule. The expected number of evaluations is
the expected size of the query set. The script enumerates this joint law using
`fractions.Fraction`; it does not simulate trajectories or use tolerances.

The complete input, G/L/C matrices, laws, query costs, and assertions are in
`safeguarded_cost_checks.py` and `safeguarded_cost_checks.json`. The matrices are
known to the diagnostic, not assumed to be pre-supplied to the oracle sampler.
If the entire four-point target were supplied, normalization and direct exact
sampling would be the stronger ordinary method. This example establishes a
mathematical non-domination claim, not a practical finite-state application.

All resource matches above are in expectation. They are not fixed pathwise
query budgets. The hybrid runs a fixed four steps; it does not stop at an exact
count of global transitions. Its random number of global updates partly explains
the finite-time loss. Replacing time by its expected global count in a theorem
would be invalid.

The phenomenon is not reliant on reducible local proposals: replace Q by
`(1-delta)Q+delta J/4`, where J is the all-ones matrix. The proposal is then
strictly positive and q-reversible. The corrected local kernel is
`(1-delta)Q+delta G`, and the hybrid contrast eigenvalue is `(5-delta)/6`.
The strict error gap persists for sufficiently small delta. If this proposal
is implemented by occasionally drawing directly from q, those extra q draws
must also be counted; the principal four-state comparison avoids that ambiguity.

## 3. Delayed acceptance versus ordinary local MH

For a proposal Q with evaluable forward/reverse ratios, put

`r_q = q(y) Q(y,x) / [q(x) Q(x,y)]`,
`r_pi = pi(y) Q(y,x) / [pi(x) Q(x,y)]`.

Delayed acceptance uses

`min(1,r_q) min(1,r_pi/r_q) <= min(1,r_pi)`.

The inequality follows directly from `min(1,a)min(1,b)<=min(1,ab)` for positive
a,b. Thus its off-diagonal transition probabilities are no greater than those
of ordinary pi-MH using the same Q. This algebra does not itself compare their
finite-time TV from q or their cost per useful target evaluation.

An explicit nontrivial two-state instance is

`q=(3/4,1/4)`, `pi=(1/4,3/4)`, Q the deterministic swap, alpha=1/2.

The first q-MH stage is

`R=[[2/3,1/3],[1,0]]`.

The W-corrected delayed-acceptance kernel is

`L_DA=[[2/3,1/3],[1/9,8/9]]`,

while ordinary pi-MH has

`L_ord=[[0,1],[1/3,2/3]]`.

G has contrast eigenvalue 2/3. The hybrid eigenvalues are `29/36` and `7/12`,
respectively. Their one-step proposal-start TV errors are therefore

`TV(q C_DA,pi)=29/72`,
`TV(q C_ord,pi)=7/24`.

The delayed-acceptance hybrid is worse in TV at this fixed time. It does use fewer
new target evaluations: the expected post-initial costs are `7/32` for C_DA and
`11/32` for C_ord. Both have one half of a proposal in expectation. For this
one-step calculation full memoization and current-state caching coincide. The
extra rejections trade accuracy for fewer target evaluations; they are not a
free efficiency improvement.

## 4. Honest implementation and scope conditions

1. Sampling q and evaluating its density ratio are separate capabilities. An
   implicit generator with no evaluable density does not automatically support
   the proposed safeguard. A direct q-reversible R, such as a supplied exact
   transition, can have a different cost and access contract.
2. Constructing `R=MH(Q,q)` requires drawing from Q, evaluating the needed q
   values and Q forward/reverse ratio, and making its accept/reject decision.
   A failed first stage can skip the expensive target evaluation; a successful
   stage normally adds one, unless already cached.
3. The second acceptance uses the ratio of unnormalized target/proposal
   weights. It does not require the target normalizer. Thresholds in an analytic
   first-high-state proof are proof devices, not silently available observables.
4. q-reversibility must be relative to the actual proposal distribution used in
   G and initialization. Replacing q by an inaccurate surrogate in the first
   stage may still leave a correctly factorized pi-MH algorithm, but it no
   longer supplies `qL<=2q` by this argument. A separate domination bound would
   be required.
5. The one-step domination condition is a structural measure inequality. A
   finite training sample or empirical KL statistic is not its certificate.
6. The proposed proof uses a fixed time-homogeneous reversible later kernel.
   Choosing or updating Q/R after observing the run is a separate theorem.
7. Target/proposal ratios and acceptance comparisons are ideal-real operations
   in the theorem. Ordinary floating point, underflow, approximation errors,
   or approximate local transitions require their own error accounting.
8. Expected proposal counts at a fixed number of mixture steps must not be
   substituted into a deterministic-proposal-count mixing formula.
9. Pure IMH remains the necessary comparator and already has coefficient K.
   A prefix-free structural guarantee can be useful knowledge without an
   improved end-to-end computational exponent or application speedup.

## 5. Observed costs and limitations

The first exact four-state diagnostic took approximately 0.00506 seconds wall
and 0.00507 seconds process CPU, with reported peak RSS 9216 KiB. The second run
added the equal-target-cost pure-IMH mixture and clearer explicit q-MH construction;
its actual resource receipt is in the final JSON. There were no failed mathematical
assertions. The three main operations involve at most 32 augmented states each.
No Monte Carlo trajectories, data searches, hardware runs, old-prefix replays or
new applications were executed. The exact two-state example is algebraic, not a
separate metered numerical experiment.

These subsecond replays are verification costs, not a measurement of scientific
discovery cost. The mathematical example, cost-accounting choices and note were
developed in this contributor turn beginning at the clock above. The parent
records its own synthesis, universal proof and delivery work separately.
