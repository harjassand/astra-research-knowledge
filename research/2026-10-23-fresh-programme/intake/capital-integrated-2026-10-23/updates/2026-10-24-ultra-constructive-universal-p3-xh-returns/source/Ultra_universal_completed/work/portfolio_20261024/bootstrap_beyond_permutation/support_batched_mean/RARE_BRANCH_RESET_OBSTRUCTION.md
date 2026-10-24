# Rare-branch obstruction to finite-sample uniform reset certification

This is a bounded countermodel to the noisy-acquisition bridge in
`FIRST_CONSTRUCTION.md`. It does not challenge the exact scalar-probability
oracle algebra: with exact access, the two models below are distinguishable
in one query. The obstruction is to a finite-sample uniform guarantee from a
costly initializer when behaviorally relevant reachable branches can have
arbitrarily small probability.

## Two models with different reset feasibility

Let the hidden state be `Z in {A,B}`. Each paid initialization independently
draws

```
rho_epsilon = (1-epsilon) delta_A + epsilon delta_B,
                 0 < epsilon <= 1/2.
```

The intervention alphabet is `I`, which does nothing, and `C`. Separately,
there is a state-preserving visible test `R`; on each use it returns a
Bernoulli bit with probability `1/3` in `A` and `2/3` in `B`. The test
outcomes overlap, so they are not state labels. Tests may be repeated for
history conditioning, while reset-word mixtures are over the interventions
`I,C`; every initialization and every readout is charged.
The hidden names in this definition are for the mathematical construction
only. They are not supplied to either learner or comparator.

The two candidate controlled systems are:

* **Reset model:** `C` sends both `A` and `B` to `A`.
* **Preserve model:** `C` leaves both states fixed, like `I`.

Both are finite controlled linear observable processes of dimension two.
They have the same initializer, action/test interface, emission law, and
rank bound. A model-based comparator may be told this entire two-model class,
`epsilon`, and both emission probabilities; it is not told which transition
model is running or given a state-ID channel.

In the reset model, the one-word intervention `C` makes every predictive
state equal to `delta_A`; its observable operator is rank one and it is an
exact positive reset. In the preserve model, every legal word and every
nonnegative mixture of words preserves the hidden state. From the pure
predictive states `A` and `B`, test `R` has total-variation distance `1/3`.
Both states are in the initializer's support. Even if reachable states are
defined only by finite positive-probability observation histories, they
approach `B`: after `j` consecutive `R=1` outcomes, the posterior odds are

```
q_j/(1-q_j) = (epsilon/(1-epsilon)) 2^j,
```

so `q_j -> 1`. In the preserve model, any randomized word mixture leaves
these predictive distributions unchanged. Comparing the empty history
(posterior `epsilon`) with these histories shows that a common post-mixture
predictive law must have worst-case test error at least
`(1-epsilon)/6`; in particular, no reset with uniform error below `1/12`
exists for `epsilon <= 1/2`. The two models therefore have disjoint answers
to the question “is there a legal positive reset with uniform error below
`1/12`?”

## Finite-preparation lower bound

Couple one experimental run in the two models using the same initializer
state and the same readout randomness. If the state is `A`, every adaptive
action/test transcript is identical in the two models: `C` maps `A` to `A`
in the reset model and preserves `A` in the other. Transcripts can differ
only if that run initialized in `B`, an event of probability `epsilon`.
This remains true if the controller uses arbitrarily many within-run tests,
adapts its word to earlier outputs, or knows the two-model class.

Across `N` independent paid initializations, the models' transcript laws
therefore have total-variation distance at most

```
1 - (1-epsilon)^N <= N epsilon.
```

For any decision rule required to distinguish the two reset-feasibility
answers with error at most `delta < 1/2` under each model, the testing bound
requires

```
N >= log(1/(2 delta)) / (-log(1-epsilon))
  = Omega(epsilon^-1 log(1/delta))       as epsilon -> 0.
```

Thus no finite-sample confidence guarantee depending only on process
dimension, alphabet size, or nominal Hankel rank can certify the global
reset property uniformly over this family. The source-preparation charge
alone is at least this many times the cost of one initializer; all readouts,
word duration, computation, fitting, and reset execution are additional.
If the protocol is restricted to one Bernoulli readout per preparation after
`C`, the two means are `1/3` and `1/3+epsilon/3`, giving the familiar
`Omega(epsilon^-2 log(1/delta))` scalar-estimation cost. Allowing richer
within-run tests can improve that rate, but cannot remove the
`Omega(epsilon^-1)` rare-preparation lower bound.

With an exact scalar oracle, the query “apply `C`, then `R`” returns
probability `1/3` in the reset model and `1/3+epsilon/3` in the preserve
model, so one exact query separates them for every `epsilon>0`. The lower
bound is specifically about acquiring this distinction from finite noisy
outcomes; it is not a counterexample to the opening's exact-oracle theorem.

## What this obstruction says about a robust extension

The example keeps the state count fixed at two while the rare mass can be
arbitrarily small. A finite-sample version therefore needs a quantitative
reachability/observability promise, such as a known lower bound on the
probability of every experiment needed to expose a basis direction, plus a
conditioning margin for its Hankel basis. A finite distinguishing-depth
bound is also needed if completeness is to be established by a finite word
catalogue. The uniform reachable-state set still needs a certified enclosure;
a good residual on a signed span or on sampled histories alone is not a
uniform bound over that set.

For example, if a finite catalogue of `J` required word/test experiments
has each relevant event probability at least `p_min`, `M` independent
readouts per experiment give simultaneous additive probability accuracy
`eta` with failure at most `delta` once

```
M >= (1/(2 eta^2)) log(2 J/delta).
```

Conditional probabilities normalized by a word probability `p>=p_min` then
have errors of order `eta/p_min` (provided `eta < p_min/2`). Inverting a
Hankel basis further amplifies errors according to its smallest singular
value. A sound reset certificate would need these factors, a robust positive
mixture feasibility margin, and a validated set containing every reachable
normalized predictive state. Those are explicit supplied promises or
acquisition costs, not consequences of a small observable rank.

The competent comparator is the same rank-two model-based experiment
designer with the same initializer and noisy data. The coupling lower bound
applies to it too. A comparator given the transition matrices, a direct
`B`-preparation control, or state labels would have strictly more information
and is not matched. Conversely, after a reset has been certified, any
retaining model-based controller can use it; this construction alone makes
no comparative advantage claim. Amortization must compare all acquisition
and validation costs plus `T` executions of the learned word against the
same `T` tasks using the external initializer.
