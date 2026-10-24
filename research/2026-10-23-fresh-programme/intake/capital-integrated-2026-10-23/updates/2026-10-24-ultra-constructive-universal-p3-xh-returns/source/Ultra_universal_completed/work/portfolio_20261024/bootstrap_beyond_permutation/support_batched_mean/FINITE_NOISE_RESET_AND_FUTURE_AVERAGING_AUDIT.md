# Rank-two reset certificate and dependent future-program audit

This note audits the specified finite-noise rank-two certificate and future
validation stream. It gives a conditional theorem and identifies the gates
that must be explicit. It is not an experiment result.

## The rank-two uniform-error formula

Let `x_0,x_1` be two actual normalized predictive preparations. Suppose the
**full controlled Hankel rank is at most two**, and the two rows span that
space. For a binary event `G`, write

```
g = x_1(G) - x_0(G) != 0.
```

Every reachable normalized predictive row `x` then has a unique affine
coordinate

```
x = x_0 + alpha (x_1-x_0),
alpha = (x(G)-x_0(G))/g,
|alpha| <= 1/|g|,
```

because `x(G), x_0(G)` are probabilities in `[0,1]`. This is a positive
reachability bound derived from the event range; it does not require the two
preparations to be endpoints of the reachable convex set.

Let each candidate reset word `u` be an unconditional, normalization-
preserving controlled operation. Its linear predictive operator maps the
one-dimensional zero-normalization contrast into itself, so

```
(x_1-x_0) M_u = d_u (x_1-x_0).
```

For any future binary program/event `F`,

```
Delta_u(G) = x_1 M_u G - x_0 M_u G = d_u g,
|x_1 M_u F - x_0 M_u F| = |d_u| |x_1(F)-x_0(F)| <= |d_u|.
```

For a fixed nonnegative mixture `lambda` with sum one, set
`S=sum_u lambda_u M_u`. Then for every reachable normalized `x`,

```
|x S F - x_0 S F|
   <= |sum_u lambda_u Delta_u(G)| / |g|^2.
```

The first factor `1/|g|` bounds the input's affine coordinate; the second
comes from using `G` to read out the post-word contrast. The same bound holds
for total variation over a future transcript by taking the supremum over
events `F`. It remains valid when the physical hidden state persists between
trials, provided every resulting predictive row is in the same rank-two
controlled space and every reset word is in that controlled family.

This proof depends on the *global* rank-two promise, normalization-preserving
reset words, a true gap `g != 0`, and use of actual preparations that span the
controlled observable space. Nine calibration settings alone do not verify
that no third predictive direction exists or that a new target program lies
in the same controlled family. If the rank bound is only empirically guessed,
the certificate is conditional on it. A postselected/abortive word is not
normalization-preserving; its state-dependent success probability must be
modeled and paid separately.

## Simultaneous calibration and data-dependent mixture selection

Suppose the finite library of candidate words and the nine raw Bernoulli
settings are fixed before data collection. Each setting receives 50,000
independently initialized shots, and `w=0.01` is the desired two-sided
absolute error. Hoeffding plus a union bound gives

```
P(any raw mean misses its interval) <= 9 * 2 exp(-2*50,000*0.01^2)
                                      = 18 exp(-10)
                                      ~= 0.0008172 < 0.001.
```

This is 450,000 initialized setting-shots in total. If the preparations,
word controls, or readouts have extra drift or non-Bernoulli noise, that is
not covered by this bound.

If every raw mean used in the prep gap and macro contrasts is in its
simultaneous interval, then a prep-gap estimate `g_hat` gives

```
|g| >= g_L := |g_hat| - 2w.
```

Require `g_L>0`; otherwise the data have not certified a spanning basis.
Each contrast formed as a difference of two raw means has error at most
`2w`. If the **actual selected rational** `lambda` is nonnegative, sums to
one, and exactly cancels the empirical contrasts, then despite its
data-dependent selection,

```
|sum_u lambda_u Delta_u(G)| <= 2w,
uniform future-event reset error <= 2w / g_L^2.
```

There is no extra selection penalty over a continuum of simplex weights:
on the simultaneous event, the convex weighted sum of coordinate errors is
at most their maximum. This argument does require that the candidate word
library and the nine settings were fixed in advance and that all means used
by the optimizer are among those nine. If the solver leaves empirical
residual `r_LP`, replace `2w` by `2w+|r_LP|`. If weights are rounded, include
the residual of the rounded, renormalized nonnegative weights; do not quote
the unrounded LP solution as the executed intervention.

The error scale is not automatically small: since `|g|<=1`, the stated
`w=0.01` certificate is at least `0.02` even in the best-gap limit, and is
larger when `g_L<1`. To certify requested tolerance `epsilon_reset`, require
`2w+|r_LP| <= epsilon_reset*g_L^2`; otherwise report the numerical gate as
failed. The empirical LP can also fail to find a useful simplex mixture;
no reset is certified in that case.

For experiment planning, if a justified lower bound `g>=g0>0` is supplied
and the LP residual is zero, setting `w<=epsilon_reset*g0^2/2` is sufficient.
The nine-setting Hoeffding design then needs at least
`M >= 2/(epsilon_reset^2*g0^4) * log(18/alpha)` shots per setting to make
the simultaneous source failure at most `alpha`. This conditioning penalty
is paid in addition to the fixed 50,000-shot illustration.

The formula certifies a reset relative to the chosen actual reference
`x_0 S` and all events in the globally promised rank-two continuation
space. A previously unmeasured future program can be tested without
reusing its target outcomes in the calibration LP. The held-out check does
not enlarge the calibrated model class: arbitrary new programs or
unbounded word lengths require the global rank/closure promise (or their own
coverage and precision budget). Exact rational LP arithmetic on empirical
counts is possible, but its bit lengths, fitting runtime, stored data,
control random bits, and the length/cost of every chosen word are still
paid.

## Future validation with retained hidden state

Let `C` be the calibration sigma-field. On its good event, freeze the
selected `lambda`, let `S` be its predictive operator, and let a fixed,
previously unmeasured future program return `Y_i in [0,1]` on trial `i`.
Each trial must draw a **fresh independent** word `U_i~lambda` after the
past, then run the same fixed future program. Let `F_{i-1}` contain all
previous observed outcomes and any information used to choose the next
trial, but not the fresh word draw. If the current predictive row is any
reachable `x_i`, the uniform reset certificate gives

```
| E[Y_i | F_{i-1}, C] - p_* | <= epsilon_reset,
p_* := x_0 S(F).
```

The conditional expectation averages over the fresh `U_i`. The outcome
`Y_i` itself need not be independent of earlier outcomes: the hidden state
may be retained and changed by each future program. Set
`D_i=Y_i-E[Y_i|F_{i-1},C]`. These are martingale differences with conditional
range length at most one. Therefore, conditional on the calibration good
event,

```
P(|mean(Y_i)-p_*| > epsilon_reset + tau | C)
    <= 2 exp(-2 N tau^2).
```

Unconditionally, add the source failure probability, so the bound is at
most `18 exp(-10) + 2 exp(-2 N tau^2)`, subject to the stated gates. This is
a martingale concentration result, not an iid or independent joint-law
claim. It applies to every conditional history because the reset error
bound is uniform over reachable predictive rows; a merely marginal source
average would not suffice.

The fresh-word requirement matters. If one word `U~lambda` is drawn once
and then reused for all `N` trials, take two words with constant outcomes
zero and one and equal weights. The mixture target is `p_*=1/2`, but the
sample average is always zero or one, so it does not concentrate around
`1/2`. A hidden, unobserved draw is still not a fresh draw. The fixed target
program must also be declared before its target outcomes are examined; if
programs are adaptively selected from a large family, either the uniform
rank-two theorem must cover every selected event or a separate selection
bound is needed.

## Fair comparison and cost boundary

The matched retaining comparator is a rank-two model-based system
identifier/controller given the same two actual preparations, the same nine
settings and 50,000 shots per setting, the same global rank promise, and the
same future-program contract. It may retain all counts, fit the two-state
predictive model, and run the same LP if that helps its later task. A method
with exact transition matrices, state labels, or direct preparation of the
rare hidden component has extra information and is not matched.

The source ledger already contains 450,000 independent preparations and
readouts, plus exact/finite-precision fitting, rational-weight storage,
verification, and execution of a sampled raw word on every use. A useful
amortization comparison must include

```
C_reset_route = C_9settings + C_fit + C_validation
                + T * E_{u~lambda}[C_word(u)],
C_retain_route = C_same_acquisition + C_model/target + T*C_external_prep.
```

Without measured costs for the initializer and each raw word, this audit
certifies neither savings nor a learning advantage. After a reset is
validated, the retaining comparator can use it too. The earlier rare-branch
lower bound still applies whenever a required span/prep is reachable only
with arbitrarily small probability; this rank-two calculation does not
remove that floor for general systems.
