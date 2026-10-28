# Stronger adaptive prefix acquisition on the same source

29 October 2026, Brisbane. A separate acquisition now executes the ordinary
adaptive prefix method on the same countable source as
COARSE_SWITCHING_THEORY.md. It uses independent new observations, without
the earlier receipts or lifetime pilot, and certifies the same all-word
unconditional survival accuracy with fewer source operations.

## Procedure and confidence

The source, common preparation and live/absorbed interface are unchanged.
Every trial starts from a fresh preparation. The acquisition never treats
a surviving coarse label as a restart or requests a microscopic identity.

For epsilon=1/16 and delta=1/1000, select the next word using previous
batches. Before acquiring its new observations, fix batch size

    N_j=ceil(2 epsilon^-2 log(2j(j+1)/delta)).

An upper rational logarithm rounds this paid budget safely. Form the
empirical interval [L,U]=[p_hat-epsilon/2,p_hat+epsilon/2], clipped to [0,1].
If U<=2epsilon, mark that prefix terminal and predict U/2 on it and every
extension. Otherwise predict its interval midpoint at that word and enqueue
both children. Root survival is exactly one.

Conditional on the preceding history, the selected word and sample count
are already fixed and the samples are fresh Bernoulli trials. Hoeffding
spends at most delta/[j(j+1)]. Summing this budget over all potential visit
indices gives simultaneous confidence even for a random final queue length.
This is not a retroactive allocation to prefixes selected from old data.

Branch midpoint error is at most epsilon/2. After a terminal prefix,
irreversible absorption keeps all future survival in [0,U]; the constant
prediction U/2 therefore has error at most epsilon. A complete finite tree
covers every word. The cost and almost-sure termination proof, including
rare confidence failures, is preserved in
branches/scalar/ADAPTIVE_PREFIX_COVER_COST_REVIEW.md.

## Complete executed comparison

| Resource | Balanced tapes plus paid lifetime phase | Independent adaptive route |
|---|---:|---:|
| Primitive applications | 1,086,180 | 458,449 |
| Live/absorbed reports | 1,086,180 | 458,449 |
| Fresh preparations | 540,672 | 255,220 |
| Retained prefix nodes | 84 | 38 |
| Maximum retained depth | 7 | 5 |
| Uniform absolute survival target | 1/16 | 1/16 |

The new tree has 18 branches and 20 terminal prefixes. All preparations are
paid. Confirmed deaths legitimately stop execution, and the remaining word
indicator is zero; no unobserved source duration is discarded.

Each independent acquisition has its own false-certificate bound <=.001.
No combined .001 confidence claim is made for the entire pair. The balanced
records additionally certify a two-state positive matrix model at error
.062335817204. The adaptive result certifies its finite prefix predictor;
it does not automatically validate that same matrix model. For the common
scalar-survival task at error 1/16, the adaptive method is the stronger
executed acquisition route. No universal optimality or hardware-time claim
follows.

## Interpretation

The gain uses ordinary adaptive allocation and midpoint predictions on small
survival ranges. A terminal prediction remains a small nonzero constant at
every future length even though the true source eventually absorbs. This is
appropriate for the stated absolute-error target. It does not establish a
vanishing predicted tail, relative accuracy, conditional survivor states,
or lifetime moments.

The acquired weak-Poincare envelope proves finite learning for a structural
class. The particular finite cover emitted here verifies itself through
observed prefix bounds and absorption monotonicity, without first measuring
that envelope. Its saving is therefore not attributed to a lifetime pilot
that it never used. This separates a class-level termination theorem from
instance-level finite certification.

Known prefix estimation can be the best implementation of the task. The
continuation's contribution is the explicit observation-to-composition
contract, the acquired-tail result, and the new limits on what generic coarse
access can buy. None makes prefix estimation itself a new principle.

The executable is core/adaptive_coarse_cover.py. Raw receipts, exact emitted
intervals and execution logs are under results. Private exact validation
retains eight slow blocks and bounds omitted preparation mass by 1/262144;
those parameters do not enter acquisition or inference. These are executed
software trajectories with warranted preparation and sensor access, not
laboratory calibration or equipment operation.
