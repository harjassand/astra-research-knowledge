# Common-seed support: an acquired sampled-core stability principle

Pure mathematical stochastic-process research. The independent full-source receipt
governs acceptance; mechanism notes and finite tests alone do not certify the code.
No operational chemistry, uploads, general weak-reversibility solution, or novelty
claim is made. Previously accepted archives are unchanged.

## Result and input class

Only `0 <-> A` changes total count. Every other channel conserves total count and
contains A in both source and target. Strip one common A, obtaining a conservative
network Q on `(A-1,B_1,...,B_m)` of maximum order p>=2. If the raw full graph is weakly
reversible and **top-order support closure from every singleton reaches shifted A**,
the theorem proves classwise positive recurrence and every finite exponential
stationary total-count moment.

The construction handles arbitrary dimension, arbitrary finite p>=2, multiple
linkages, lower-order conservative channels and arbitrary positive rates. Exact
receiving uses positive rational rates. It does not require a stationary fiber law,
a good pivot, a supplied Lyapunov function, numerical trajectories, or an ODE solver.

## Why this crosses a real boundary

In seeded states the exact internal generator is `A Q`. Time-change by `d tau=A dt`:
death becomes an independent constant-rate clock, while immigration has intensity
`lambda/A`. A finite raw support calculation plus an explicit martingale estimate
shows shifted A reaches a positive fraction of each large fixed-mass fiber quickly.
Last-window conditioning extends the bound to every later operational time, without
a mixing-law premise or an infinite-time union bound.

Both immigration-before-death and loss-of-the-last-seed probabilities are O(1/N),
with acquired constants. Observe the chain at core events and include the actual
A-zero wait/restoring immigration after seed loss. The sampled total count changes
by +1, -1 or 0. This earns t^N contraction, and a separately paid physical occupation
argument transfers recurrence and moments back to the original clock.
Its normalization is earned exactly: under embedded stationarity, each cycle's mean
birth count is `(1+p_seed_loss)/2`; the constant-rate immigration compensator gives
mean physical cycle time between `1/(2lambda)` and `1/lambda`. No unknown stationary
normalization is supplied as a premise.
Moreover each entire bundled cycle ends by its first physical immigration, so its
pointwise mean is at most `1/lambda`. The final occupation bound is simply
`pi_continuous(t^N)<=2*pi_embedded(t^N)`. The lower `1/(2lambda)` bound is a stationary
average statement, not a pointwise assertion. Earlier valid bounds remain explicit
conservative comparators in the receipt.

For example,

```
0 <-> A
A+2B <-> A+B+C <-> A+2C
A+B+C <-> 2A+B
```

passes the support test although every inverse-linear mass profile requires the
contradictory orders `w_C>w_B` and `w_B>w_C`. The executed case makes
`A+B+C -> A+2C` rate two and all other rates one, excluding classical complex balance.
The method also covers the previously reviewed mediated network that forbids every
one-step geometric Foster function F(A,N). Here **sampled** t^N drift is proved;
no one-step physical F(A,N) is asserted.

## Files and interfaces

* `SEEDED_TIME_CHANGE_THEOREM.md`: complete ordinary proof, constants, seed-failure
  cost, class communication, recurrence and physical occupation transfer.
* `seeded_time_change.py`: raw recognition, support witnesses, qualitative receiving,
  separate scalar-bound construction and semantic receiving.
* `opposing_demo.json`: acquired numerical receipt for the opposing-ray fixture.
* `exercise_time_change.py` / `exercise_results.json`: exact main controls.
* `SOURCE_SCOPE.md`: primary literature, conventional fluid/sampled/Foster credit,
  access limits and no-priority scope.
* `independent_audit/`: separate receiver, source bindings, exact killed-fiber controls
  and review receipt when staged. Its stated scope, not this file's aspiration,
  determines independent acceptance.

```python
from fractions import Fraction
from seeded_time_change import opposing_raw, qualitative, numerical

raw = opposing_raw()
q = qualitative(raw)                 # finite raw/support work only
b = numerical(raw, Fraction(2))       # explicit scalar bounds, factored powers
```

The author's semantic receivers rederive fields using its construction code. They
are not independent implementations; independent raw/support/accounting receiving
is provided separately. Neither is advertised as a hostile-input network service.
The trusted research module explicitly disables CPython's decimal-integer conversion
guard **for its interpreter process on import**, so valid scalar receipts beyond
4,300 digits can roundtrip. A four-species,
stripped-order-six regression verifies this, without expanding any Foster power.
This setting is not a memory/time safeguard and is unsuitable as an unreviewed
untrusted-input service policy.

## Honest cost boundary

Qualitative admission performs only finite raw validation, graph return checks and
support scans. It materializes no activation constants, ODE steps, fiber states,
stationary laws, scalar support powers or Foster powers. The executable degree
`p=10^50` control passes this qualitative path.

Numerical acquisition evaluates n support-level degree-p powers and rational scalar
constants. The declared `max_power_bits` only preflights the output-bit upper bound
of those support-level power products; it is **not** a total arithmetic, input,
memory or wall-time budget. A budget stop returns numerical UNKNOWN while retaining
the qualitative theorem. The huge-degree control stops before its first power.

The opposing-ray t=2 demonstration has

    delta = 1/66448438739835865555651264512
    M_cut = 2543267526313950623496479133068309573484172804713259814879233.

The head size is retained as a binomial expression and the Foster/moment powers as
exact prefactor/base/exponent expressions. **Neither the enormous head nor its
fibers are enumerated, and no power t^M_cut is expanded.** Only three degree-two
Fraction powers are executed in this numerical fixture. These are very conservative
general bounds, not useful practical tail estimates at ordinary count scales.
The earlier direct inverse-mass theorem remains much sharper numerically on its
recognized family; broader structural coverage does not make this new bound
quantitatively superior.

Main tests cover seven cases, six coordinate permutations, higher top degree,
five species, heterogeneous rates, near-one/large t, failed support with an ordinary
stable product-Poisson control, and exact malformed/tampered receipts. Independent
small-fiber killed systems are a paid conventional comparator: they do not establish
the infinite tail and are not assumed as a fiber-law oracle.

## Failure and scope semantics

Failed support means **stability UNKNOWN**. The all-unit-rate common-A lift of
`r <-> B`, `r <-> C`, `2B <-> 2C` is a stable negative control: lower-order restoration
works and classical complex balance applies, despite failed top-order support.
This theorem is sufficient, not a classification of stable common-seed networks.
Stripped p=1 and networks lacking a common A remain outside the stated receiver.

The ingredients are ordinary time change, density-dependent finite-time comparison,
support propagation, sampled-chain Foster analysis, and regenerative occupation.
The earned join is a uniform raw-acquired first-core probability estimate with all
seed loss/return and physical holding costs included. There is no general weak-
reversibility conclusion and no priority inference from earlier parser failures.

## Replay

Python 3 standard library only, from this directory:

```sh
python seeded_time_change.py > producer-workspace/seeded_time_change_demo.json
cmp opposing_demo.json producer-workspace/seeded_time_change_demo.json
python exercise_time_change.py > producer-workspace/seeded_time_change_tests.json
cmp exercise_results.json producer-workspace/seeded_time_change_tests.json
```

Final strict-allowlist packaging records independent and extracted replays. The
original preliminary `CANDIDATE_NOT_REVIEWED.md` is retained locally as development
history but is excluded from accepted delivery. Root handles all delivery.
