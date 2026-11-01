# Population service-level construction — new, unreviewed

The constructive result is an acquired-local-model to finite-population task
join, not a new mean-field algorithm or acquisition superiority result.

For 1,000,000 conditionally independent simulator workers, 24 stages and the
explicit original initial law, the ordinary exact Bellman policy has coarse
terminal readiness .624537981679. The received same-prefix local error is
.0109739142345. A scalar tail certificate gives readiness at least .610323697095
with deployment failure probability <=1e-9, **conditional on a valid learning
event with confidence .999**. Unconditional joint bad-event bound is .001000001,
not 1e-9. The stronger finite-class adaptive broadcast-table comparator pays
eta=.006873863543; expected-regret bound is about .0356956. No microscopic
policy, physical sensor, worker independence or PRNG truth is inferred.

The execution fixture actually made 24,000,000 worker updates and map/action
lookups (plus 1,000,000 initial draws), observing readiness .623714. This one
realization does not empirically test a 1e-9 tail. Policy learning used 768 exact
Bellman products; partition storage, model, source receiving and source costs
are separate. `PROOF.md` spells out all joins and counterexamples.

## Strong ordinary baseline wins the one-goal task

Discovery-only retained counts independently produce the EXACT SAME policy.
250,000 fresh single-worker episodes (6,000,000 updates) plus empirical Bernstein
certify population readiness at least .616328951748. Prospective total is
37,588,352 source calls, versus 2,535,588,352 for the reusable local certificate.
This baseline requires no acquired leakage certificate and is retained as an
ordinary win. It proves one-policy/one-goal feasibility, not the all-adaptive-
population-policy regret claim. A terminal-distribution confidence region can
answer many future linear utility queries for the SAME policy at no new
observation cost; task count alone is not a fair amortization argument.

`retained_policy_scout.py/json` is separately labelled exploratory, not a source
certificate: 2,000 reward queries yielded 313 distinct table policies; four basis-
goal policies lost up to .04245 in COARSE utility. This neither establishes a
representative workload nor counts semantic equivalence of policies, and does
not infer true value from the cheap coarse model. It is outside the core freeze
unless expressly included later.

## Reproduction
From this directory with existing Python/numpy/sympy:

    python -c 'import check_population as c; print(c.run())'

Nonmutating run replays current tagged acquisition twice, regenerates 30 million
worker/MC updates, checks exact adaptive-counterfactual and Bellman examples,
and rejects 12 malformed/substituted tasks. Main entry points write saved files;
prefer run. `population.py` planner takes an externally supplied query digest
and receives the source task/horizon/actions/confidence. It always uses B and
E from the SAME admitted prefix. The core source input dependencies live in
`../two_rate_operator_acquisition_20261031/tagged_pool_retention/`.

All old and new acquisition attempts remain actually paid. A prospective early
stopping bill is not a refund. The prototype's block-label sensor is a simulator
interface; no equipment was operated. Current artifacts have author checks,
not an independent review. Existing accepted archives are untouched.
