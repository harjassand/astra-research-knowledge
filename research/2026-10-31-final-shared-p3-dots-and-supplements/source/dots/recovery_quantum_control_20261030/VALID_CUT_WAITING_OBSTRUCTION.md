# Exact active-wire waiting obstruction on fault-free valid cuts

30 October 2026. New elementary counterexample. It rejects an all-state constant-wait shortcut, not the earlier native service theorem or any established asynchronous threshold.

## Construction

Use a path of gate-clock vertices i=0,...,2m. All even vertices have the earlier layer type, all odd vertices the later type. Each incident constraint is

    n_even - n_odd in {0,1}.

Choose the valid cut

    n_i = m - ceil(i/2).

Every n_i is nonnegative. The cut is a legitimate finite down-set and is reachable from the all-zero initialization by a legal fault-free finite update ordering. Before the final update at vertex 0, replace n_0=m by m-1; this is still valid. Thus the current cut may be entered by an actual correct production event at vertex 0. Its output on the 0--1 wire is now live and awaits vertex 1's next event.

For every i<2m, vertex i's next increment requires vertex i+1 to increment first:

* if i is even, n_i-n_(i+1)=1, so incrementing i would violate the upper bound unless i+1 increments;
* if i is odd, n_(i+1)-n_i=0, so incrementing i would violate the lower bound unless i+1 increments.

Vertex 2m is initially enabled. Therefore consumption at vertex 1 requires the actual chronological chain

    2m, 2m-1, ..., 1.

These are 2m causally ordered completions. Other events and rejected attempts cannot shorten this chain. This delay has no faults, invalid clocks, repair state, missed attempts, or wrong DATA operation in it.

## A quantitative ideal-service version

Give each vertex an independent rate-lambda Poisson clock of attempted updates; an enabled attempt is instantaneous and correct, and a disabled attempt is identity. This is an especially favorable service model. After each predecessor becomes enabled, its residual Poisson waiting time is fresh exponential(lambda). Hence the live wire's consumption delay is at least a sum of 2m independent exponential(lambda) variables. In this path example its first required increments have exactly that serial dependency, so this sum is its exact delay.

In particular the expected live time is 2m/lambda. For any fixed H,

    P[consumption by H] = P[Poisson(lambda H) >= 2m] -> 0.

Even perfect local mechanics cannot give an incoming-state-uniform, computation-size-independent active-wire waiting tail from valid-cut feasibility alone. A finite native attempted-service witness cannot imply a stronger semantic statement without an additional schedule invariant.

This is not a lower bound on the probability of generating this slope under homogeneous fault-free dynamics from flat initialization by a particular time. A probabilistic theorem that controls the frequency of such cuts remains possible. It cannot replace that analysis with an all-state service claim.

## What a stronger construction must pay for

One must supply at least one of:

1. a proved tail for descending blocker depth under the ACTUAL noisy controller;
2. a bounded-skew or bounded-blocker-depth physical scheduling invariant, including its repair and root-amplification costs;
3. an independently operating protected memory on each live wire, with a valid controller-selected transfer/gate interface;
4. a timeout/error-conversion construction whose propagated missed-gate geometry has its own fault budget.

Calling m a fixed gadget constant can be legitimate only after checking the order of parameter choices. It does not remove the issue if m is the synchronization scale that must dominate a noise-overlap exponent or fault-tolerance radius.

The counterexample strengthens the existing warning that attempted service is not semantic progress. It explains why the parent's unconditional protected-transfer comparator is useful for preset transfers, while universal command-controlled computation still needs a genuine waiting/control theorem.
