# A data-exposure counterexample to update-index noise transfer

2026-10-29. Scope: rigorous counterexample for the **independent-Poisson marching-soldier scheduler**, which is the continuous-time comparator in arXiv:2601.20818. It is NOT a theorem that the guarded finite-kappa clocks have the same law, NOT a failure theorem for the particular concatenated code in that paper, and NOT a no-go for physical-time fault-cluster thresholds.

## Primary comparators checked first

Terhal–Burkard, https://arxiv.org/abs/quant-ph/0402104, and Aliferis–Gottesman–Preskill, https://arxiv.org/abs/quant-ph/0504218, establish conventional retained-bath threshold frameworks. Their relevant currency is a joint norm bound on specified faulty locations, not independence or marginal mean waiting times. The independent-Poisson construction and its claimed mean-speed-to-local-fault conversion are in https://arxiv.org/html/2601.20818v1, IV.2, especially the paragraphs following its noise model. That paper explicitly leaves general nonunitary Lindbladian noise open. The p-bounded contract in https://arxiv.org/html/2412.19803v2, Definition 3.11, quantifies over **every finite specified set**, so the set below is an admissible test.

## Scheduler and exact dependency coordinates

On a d-dimensional cubic lattice, d>=2, initially all successful-update counters are zero. A vertex can perform its next update only when its count is no larger than every neighbor's count. Independent rate-one Poisson attempts give the exact deferred-clock representation

    T(v,k)=max_{u in N[v]} T(u,k-1)+E(v,k),
    T(v,0)=0,  E(v,k) iid Exp(1).

Let z=|N[v]|=2d+1 and fix an origin o. Set s>0,

    R=floor(s/[8 log(2z)]),
    V_R={v: 1<=dist(v,o)<=R},  r=|V_R|=Theta(R^d),
    k_v=dist(v,o).

The fixed selected UPDATE locations are the intervals preceding update (v,k_v+1), for v in V_R. These are specified in advance; they are not adaptively selected from a trajectory.

Define A={E(o,1)>s}, of probability e^{-s}. The dependency path from (o,1) to (v,k_v+1) gives

    A implies T(v,k_v+1)>s  for all v in V_R.

Conversely, T(v,k_v) does not depend on E(o,1): a directed dependency path of k_v vertices can traverse at most k_v-1 graph edges. Therefore the event

    B={T(v,k_v)<=s/2 for every v in V_R}

is independent of A. Expanding the recurrence into at most z^{k_v-1} paths and using E exp(E/2)=2 gives

    Pr[T(v,k_v)>s/2] <= (2z)^{k_v} exp(-s/4) <= exp(-s/8).

Thus Pr(B)>=1-r exp(-s/8). On A intersect B, **every selected interval contains the entire physical-time interval [s/2,s]**. All selected sites are idle throughout that interval. This is the crucial joint exposure, absent from a mean-progress calculation.

## Actual bounded local nonunitary data damage

At each vertex put a data qubit. Its successful update resets it to |0>; this is a perfectly valid one-site CPTP update, with the usual neighboring counter eligibility test. Updates of other vertices do not touch this data qubit. Between updates apply independent local noise with Lindblad operator

    L_v=sqrt(lambda) |1><0|_v.

This is genuine nonunitary noise, with local generator diamond norm <=2 lambda, and is a subcase of bounded local noise with an arbitrary retained bath (take an inert bath). Given its most recent reset at t_v, the qubit is in state

    exp[-lambda(s-t_v)] |0><0| + (1-exp[-lambda(s-t_v)]) |1><1|.

On A intersect B, every t_v=T(v,k_v)<=s/2 and no further reset occurs before s. Conditional on the scheduler, the noises and output Z measurements are independent. Hence the physically observable event that **all r selected data qubits are wrong at time s** has probability at least

    exp(-s) [1-r exp(-s/8)] [1-exp(-lambda s/2)]^r.             (1)

Each wrong output witnesses a data fault in its specified interval preceding update (v,k_v+1). There is no ambiguity from a controller flag or a mere absence of updates: these are actual incorrect data values. Noise does not touch the counters.

Take s=a/lambda for any fixed a>0. If the induced update-index data-fault process were q(lambda)-bounded, (1) would force

    q(lambda) >= [1-exp(-a/2)] exp(-s/r)
                 [1-r exp(-s/8)]^(1/r).

For d>=2, r=Theta(s^d), so s/r ->0. Therefore

    liminf_{lambda->0} q(lambda) >= 1-exp(-a/2).

Since a can be any fixed positive constant, **no q(lambda)->0 interval-exposure contract exists; in fact any uniform all-times/all-volumes local-stochastic parameter for those exposures must be q>=1**. The same construction with independent unitary X Poisson noise yields a lower limiting bound approaching 1/2 through odd-jump parity; it already defeats a parameter tending to zero within the comparator's narrower noise class.

The reset-to-zero example is intentionally a minimal channel instance, not a proposed quantum code. It disproves a generic schedule-to-update-index fault-law transfer. It does not imply that a specific code cannot tolerate these extended, very rare exposure cones through a different geometric cluster argument.

## Retained coherent bath version of the interval fault obstruction

Instead of the Lindblad noise, take H_SB=h sum_v X_v tensor Z_B, with one common retained bath qubit, initially in a Z_B eigenstate. Every interaction term has norm h and one-site system support. On a long idle interval the local data undergoes a rotation of angle h times its physical duration; its channel deviation is not O(h) uniformly over the selected successful-update intervals. This provides a bounded retained-bath exposure witness, but (1) is the stronger fully quantified joint data counterexample. No assumption that a common bath generates independent faults is made or needed.

## Consequence for the root guarded-channel architecture

The root exact-channel and controller results do not justify replacing physical-time exposure by one small fault parameter per successful correction update. The root no-emission theorem concerns recorded **attempted CPTP channels**; for a marching-soldier channel a completed attempt may only test eligibility and do nothing. It does not bound the waiting time between successful counter increments. A region can receive abundant recorded resets while its data correction is stalled by a distant dependency bottleneck.

The guarded finite-kappa clocks are correlated, so the iid E representation above must NOT be imported into them. The rigorous conclusion is a decisive failure of the proposed generic transfer already for the simpler primary comparator. To finish the guarded-clock architecture one must retain physical-time cells / dependency cones and prove the chosen code corrects that fault model, or change the scheduler to bound such exposure. This document does not claim that either task has been completed.

## Operational caveat and explicit completed-instrument variant (root audit)

A reset can erase all earlier data damage. Therefore the preceding proof must **not** be quoted as saying that the subsequent reduced-data reset channel is faulty: reset-to-zero composed with any trace-preserving pre-noise is still reset-to-zero. The bound refutes a local-stochastic law for actual **interval noise exposures / pre-update data faults**, and establishes simultaneous physical data readout damage at time s. It is not by itself a witness against every possible equivalent fault representation after erasing updates.

There is an explicit way to retain the witness if the claimed contract includes the completed channel's measurement output. Implement each successful update as the ordinary two-outcome instrument

    K_0=|0><0|, K_1=|0><1|,

and retain its classical outcome along with its location and update index. It measures the incoming data bit and then resets it. In the exact guarded-Kraus compiler these are precisely the two downward-reset Kraus labels, so the result can be carried by the actual emitted reset record; it is not inferred from an occupancy flag. Equivalently supply a fresh initialized output bit for each update, copy the computational-basis value to it, then reset the data. That latter realization explicitly consumes one fresh output bit per recorded update and needs its physical output/storage interface; it is not free fixed-space hardware.

Because amplitude-raising noise leaves |1> invariant, on the wrong-data event at s each site's first later successful update (v,k_v+1) emits outcome 1. The clean instrument emits outcome 0 at every update. Therefore exactly the same lower bound (1) applies to a joint set of **observable faulty completed measurement outputs**, even though the post-reset data are clean. For the usual CPTP map that discards those outcomes, only the earlier interval-exposure statement is claimed. A threshold theorem may legitimately exploit such erasure; the counterexample is not a proof against that theorem.

The Poisson-X variant is safest stated as a joint bound on the independent noise **increments during the disjoint per-site intervals**, not the cumulative already-corrupted data. For operational output errors use the monotone nonunitary amplitude-raising construction above; it avoids cancellation before the eventual recorded update.
