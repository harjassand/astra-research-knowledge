# Executed finite-bank intervention learning

29 October 2026. Execution of the established KT/importance-sampling
route in CONTROLLER_COMPLEXITY_AND_REAL_EXPERIMENTS.md. Synthetic
samples, not a physical experiment or an apparatus precision budget.

## The learner's actual interface

There are two operations, one controller context and 64 calls per
episode. An unobserved z in {0,1,2} is drawn independently at each
warranted preparation and frozen within that episode. Hidden state
x in {0,...,6} starts at zero. Native operations are

    A0: x <- 2x+z+1 modulo 7,
    A1: x <- 3x+2z+1 modulo 7.

They do not commute. For z=0, equal-count words 01 and 10 end at
states 4 and 3. A terminal binary sensor has mean 19/20 if the A1
count lies between 44 and 52 and the endpoint lies in {0,1,3};
otherwise its mean is 1/20. The model is used by the generator and
an independent population auditor, not by policy selection.

The bank has 131,072 episodes under the rational KT selector. The
learner receives action counts and terminal bits. Packed chronological
actions are retained and their counts checked. No hidden state,
parameter or target rollout is given to the learner. Simulator-private
random draws are not part of the compared service transcript.

## Selection and confidence

All 4,097 row probabilities p=m/4096 are evaluated on this bank. The
selected policy is

    p_hat = 3086/4096 = 0.75341796875.

With C_T=2 sqrt(65) and the prespecified beta=0.01:

| Quantity | Value |
|---|---:|
| Certified global regret against every p in [0,1] | <= 0.133619738 |
| Certified improvement over p=1/2 | >= 0.191929786 |
| Population selected value, audit only | 0.361465221 |
| Population best grid value, audit only | 0.361507473 |
| Population regret on grid, audit only | 0.0000422529 |
| Population p=1/2 value, audit only | 0.0507116166 |
| Population deterministic p=0 and p=1 values | 0.05 each |
| Largest grid estimation error in this seeded run | 0.00414535318 |

The first two statements share one event with probability at least
0.99 under the declared sampling model. Population numbers are not
inputs to that event. The global certificate includes the continuous
grid approximation T/4096.

A separate fresh deployment used 65,536 newly prepared episodes.
Its observed mean was 0.3605041504, with a separate 99% Hoeffding
radius 0.00635790481. Both events hold jointly with at least 98%
confidence by a union bound. This does not license reusing the final
calibration hidden state as the deployment initialization.

## Costs and ordinary comparator

Bank plus fresh deployment used 196,608 preparations, 12,582,912
native calls and action selections, and 196,608 terminal readings.
Finite integer RNG calls are recorded, not counted as single random
bits. Physical timing, sensor error and actuation error are not
supplied by this synthetic experiment.

The fair incumbent is the same established KT/reusable-policy method,
which ties the execution. Uniform actions have worst path ratio
2^64, while the KT ceiling is about 16.125, but this contrast is not
a novelty or practical-superiority claim. A conventional mixture of
deterministic policies covers that subclass at constant cost; those
policies cannot attain the much better randomized value in this
one-context class. An ordinary adaptive optimizer may exploit this
particular specimen more cheaply than the worst-case theorem.

## Checks and reproducibility

The checker verifies binary KT domination with exact fractions for
horizons through 64. It checks lower-bound packing at horizons
4,096 through 262,144, with 4,8,16,32 disjoint boxes respectively;
center-policy box masses exceed 0.97 against the analytic 0.75
requirement. These finite checks do not substitute for the proof.

The equal-count ordering witness, exposed-key support failure and
frozen-repeat variance failure are retained. The population auditor
uses a separate conditional-count recursion, then integrates against
binomial probabilities; this is not an acquired hidden-state model.

Reproduce with `python3 check_controller_learning.py`. Raw records
and hashes are listed in CONTROLLER_LEARNING_CHECKS.json. Proof,
generator, learner, population auditor and actual internal review
remain distinct assets.

## Exact arithmetic receipt

`certify_controller_bank.py` independently reloads the saved bank and
compares all 4,097 importance estimates as rational numbers with a
common integer denominator. It confirms the same selected policy.
A rational exponential partial sum certifies the logarithm ceiling;
integer-square inequalities certify the Bernstein radius ceiling
58997369/10^9. It verifies the displayed outward-rounded global
regret and improvement bounds exactly. The receipt is
EXACT_CONTROLLER_CERTIFICATE.json. This uses no further trials and
does not change the physical sampling assumptions. The original
floating-point population checks remain diagnostic evidence.
