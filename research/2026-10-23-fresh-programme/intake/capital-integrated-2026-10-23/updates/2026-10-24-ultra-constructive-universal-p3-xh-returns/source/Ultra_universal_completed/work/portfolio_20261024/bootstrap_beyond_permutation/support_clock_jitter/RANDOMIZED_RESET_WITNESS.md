# Exact all-size randomized behavioural reset: cycle witness and limits

2026-10-24. Source-free mathematical support for the frozen construction. This
is an existence example and cost audit, not an acquired experiment, novelty
claim, or general reset theorem.

## Family and observable interface

For each integer `n >= 2`, take phases `s in Z_n`, one raw control `R` with
`s -> s+1 mod n`, and a visible binary test `E` that returns one exactly at
phase zero. The analysis uses phases only to specify the family; the learner's
interface is the scalar controlled-experiment probability `h(wE)`. The
initializer for those experiments is phase zero. The rank bound is `n`.

For `i,j=0,...,n-1`, use preparation words `b_i=R^i` and tests
`t_j=R^j E`. Directly from the scalar oracle,

    H_ij = h(b_i t_j) = 1{i+j = 0 mod n},
    (H_R)_ij = h(b_i R t_j) = 1{i+j+1 = 0 mod n}.

Thus `H` is an invertible permutation matrix. The usual observable-operator
recovery gives `M_R=H^{-1}H_R`; it is similar to the phase-cycle permutation.
The normalization column is `c=H^{-1}1`, since `Hc=1`. This is a full
reachable/observable basis for the stated rank-`n` family, so checking the
operator on these rows covers every predictive state in the family.

## Randomized reset, and why no fixed word can do it

Choose a fresh `L` uniformly from `{0,...,n-1}` and execute `R^L`, then discard
the choice/control record before the continuation. From any starting phase
`s`, the nonselective post-operation phase law is `s+L`, exactly uniform on
`Z_n`. Therefore every finite continuation experiment has the same law,
independent of the starting phase. In phase coordinates the nonselective
operation is

    S = (1/n) sum_(k=0)^(n-1) P^k = J_n/n = 1_col v,
    v = (1/n) 1_row,

where `P` is the cycle permutation and `J_n` is the all-ones matrix. It has
rank one and preserves normalization. Conjugating by the Hankel basis leaves
rank one, so in the learned predictive coordinates it has exactly the form
`c v'` required by the construction. No hidden phase estimate is needed to
apply it.

Every deterministic raw word is `R^k`, a bijection on phases. The tests
`R^j E` distinguish any two phases (choose `j=-s mod n`), so no such word
equalizes future behavior. More strongly, if a randomized word has length `L`
and its post-state law is to be independent of every initial phase, then
`L mod n` must be uniform: the output law from phase `s` is the shift by `s`
of that residue law. This also shows the uniform target is the unique common
post-state law obtainable from mixtures of these words; in particular this
operation does not reproduce the point initializer `s=0`.

## Tight word-cost bound

Count one application of `R` as one unit. Any valid randomized word must give
each residue `j` probability `1/n`; among nonnegative lengths with residue
`j`, the shortest is `j`. Hence

    E[L] >= sum_(j=0)^(n-1) j/n = (n-1)/2.

The uniform choice among the shortest representatives `0,...,n-1` attains
this bound, has worst-case length `n-1`, and uses exactly `n` possible words.
The worst-case bound is tight too, since a word producing residue `n-1` has
length at least `n-1`. Exact uniform randomization has entropy at least
`log2(n)` bits; the length distribution above attains that entropy. For
non-power-of-two `n`, an exact sampler can use rejection from fair bits; its
random-bit cost is additional to pulse cost.

These are reset-episode costs only. If execution time is visible, the chosen
length leaks `L`; if the control transcript or random seed is retained, then
conditioning on it leaves the state at a known rotation rather than at the
common uniform law. The rank-one claim is for the **nonselective** randomized
operation after its record is hidden/discarded. Erasing/hiding that record is
not free by implication. One can instead pad all choices to `n-1` clock slots
with a non-disturbing hold, but that requires such a hold and charges its
elapsed time; the reset conclusion applies only if the downstream interface
does not observe the private pulse schedule. If downstream policy may use the
record or timing, this example is not a conditional reset.

## Acquisition and matched controls

Under the exact scalar-probability interface and a supplied rank bound `n`, a
generic operator route can acquire `H` and `H_R` with `2 n^2` raw `h` queries.
Each query is deterministic in this family, so one actual run gives its exact
zero/one value. Each query uses one initializer and one readout. Across all
entries, the `H` words use `n^2(n-1)` `R` pulses; the `H_R` words use `n^3`;
the total is `2 n^3-n^2` pulses, plus `2 n^2` initializer and readout costs.
Then exact linear algebra and the `n` powers of `M_R` produce the uniform
mixture without further probability queries. If `n` is unknown, a
nondemolition `E` read after each step of one orbit from phase zero reveals
the first positive return at step `n`; this takes `n` rotations/readouts and
one initializer. If each return test instead requires a fresh initializer,
the separate-query pulse total is `n(n+1)/2`, with `n` initializations.

The strongest matched conventional control is already the same cyclic-group
average: after learning the period, sample `L` uniformly and execute `R^L`.
It gets the identical reset with the same optimal `((n-1)/2)` expected pulse
cost and `n-1` worst-case pulse cost, without constructing all `n^2` Hankel
entries. Thus the operator LP is a valid representation-level way to discover
the intervention, but this family gives it no acquisition or runtime advantage
over a controller that recognizes the cycle. A generic stochastic-mixing
baseline that uses a less efficient random walk is not the relevant strongest
comparison.

For an external reset, let `C_v` be the full paid cost of preparing the same
uniform predictive law (including any readout, randomization, and disposal of
the preparation record). Reusing the word-mixture costs
`C_acq + T[(n-1)c_R/2 + C_rand + C_hide]` over `T` preparations, versus `T C_v`
for the external operation. It is cheaper only when

    T(C_v - ((n-1)c_R/2 + C_rand + C_hide)) > C_acq.

Here `C_acq` includes initializer, pulse, readout, computation, and validation
costs; the generic Hankel count above is one explicit upper bound, while the
single-orbit conventional learner is much cheaper on this family. A reset to
the original point law is not a matched comparator target: the cycle controls
cannot make that law common to all starting phases. If the downstream task
requires the original point initializer, replacing it by `v` changes the task
and the proposed reset is inapplicable.

## Scope boundary

This proves an all-size separation between deterministic words and
nonselective randomized words, with a tight expected and worst-case duration
bound. It does not show that a reset is learnable for arbitrary finite
controlled systems, that noisy finite samples certify the exact LP, or that
the random record can be hidden at zero cost. The family is a group-twirl
control whose strongest same-data competitor already reproduces the operation;
the useful content is the exact existence/cost/record boundary, not an
advantage claim for observable-operator learning.
