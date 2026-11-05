# Imported recovery and compatibility with the actual burst source

[Operation guide](README.md) · [Complete source proof](P2_AUTONOMOUS_CLASSICAL_BURST_20261106_RETURN.txt) · [Boundary and costs](availability-boundary-and-costs.md)

## A finite initialized germ, rather than unproved self-organization

The construction uses Gacs's deterministic damage, computation, initialized hierarchy and output clauses. It does not claim that the burst process satisfies the imported paper's stronger stochastic-trajectory hypotheses. Scales obey `B_k=exp(Theta(k^2))` and `T_k=B_k exp(O(k log k))=B_k^(1+o(1))` up to a fixed base period.

Paid noisy known-word startup installs a sufficiently large germ and neighboring guards. The task fits within its first computation stage, before growth/shrinkage/lifting. The guard needs a minimum observation-to-commit delay; an update-count bound alone would permit a rapid staggered chain. No random-germ theorem, permanently trusted freeze bit or continuing external scheduler is introduced.

Physical counters, state and snapshot buffers are all corruptible. Fixed physical attempt-count tiles certify lower/upper cycle time and snapshot-to-commit delay. A damaged phase, stale buffer, fast cycle or stall receives an explicit damage/halo charge; a complete subsequent good cycle overwrites the stale information. These are fixed-window source estimates, not products inferred from random waiting-time marginals.

Startup writes the intended symbols with finite local reset attempts while execution may already run. Missing/late resets and preparation-time bursts count as initial damage, retaining burst correlations. The parameter order is defect budget, finite clock/preparation constants, then sufficiently small positive intensity, all before `C,W`. Ending the one-time preparation interval remains part of the supplied startup premise.

## Arbitrary CPTP values reduce only because the operation is classical

Condition on actual mark geometry and ideal attempt clocks. Expand ideal basis observations and arbitrary faults into branches. Every branch admits a classical faulty-history witness whose deviations are confined to actual fault supports and declared preparation/timing halos. Fault-created coherence is assigned a basis value at its next ideal observation; assignments can be correlated and depend on the whole branch.

The deterministic recovery guarantee applies to every such faulty-value assignment, then averaging gives the CPTP guarantee. This is a support argument, not a new iid noise model. The same reduction would destroy quantum coherence and does not solve the preceding universal quantum-processing task.

## Retain one large burst hitting several witnesses

The circular tube layout has bounded spacing/neighbor links. For arc length `L`, duration `u` and marks of radius at least `b`, the actual source bound is `c lambda u(L b^(-r-1)+b^-r)`, including centers outside the installed device.

Damage surviving to level `k+1` supplies separated lower-level witnesses. The stated recurrence is

```
p_(k+1) <= A_k p_k^2 + ell_k
A_k = O((Q_k U_k)^2)
ell_k <= c lambda (T_(k+1)+tau_in+s_0)(Q_k+1) B_k^-r.
```

For a separated pair, small-mark witnesses depend on disjoint original source sets and disjoint clock tiles; their probabilities multiply there. The omitted large marks are charged by `ell_k`, without conditioning them absent to manufacture independence.

Nearly linear recovery makes large-mark forcing scale as `lambda B_k^(1-r)` up to subpowers. For `0<b<r-1`, the source derives `p_k<=M vartheta B_k^-b` and a summable `sum_k Q_k U_k p_k`, paying for both the top operation and downward physical-output windows. No independent effective decoder-fault law or random shared-service shortcut is imported.
