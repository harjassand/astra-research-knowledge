# Mixed-animal noisy acquisition route
30 October 2026, 16:22 UTC. Explicit proof candidate, not yet audited. This refines the named noisy-reset/copy gap in STAGED_CAPTURE_RETRACTION.md. It is NOT a claim of a finished joint phase-exit/source theorem.

## A. Do not assume fresh targets independent of the old record
New layer targets may be arbitrarily dirty and correlated with the retained bath/old record. Add each target as a LEAF at its old parent in a temporary analysis graph. During preparation the actual old majority generator remains on, and each target has an actual onsite reset-to-|0> dissipator. New-layer majority and future horizontal interactions remain off. Only the old root serves the quantum read port.

Use two kinds of occupied features:
1. old disagreement-edge checks, relative to the original raw bit;
2. one target-defect check per target, occupied on |1> (relative to reset target zero).

The temporary graph has bounded degree and a bounded-fiber retraction onto the old mixed graph. It is an ANALYSIS graph, not an extra physical decoder.

For each rooted connected animal A use

 f_A=theta^(u|A|-k_old(A)) r^(k_target(A)),
 V=sum_A f_A, W=sum_A |A|f_A,

where 1<r<=theta^-1. The lower endpoint is a fixed r0=1+epsilon0, not r=1.

## B. Why the mixed drift can retain its local source
The old-majority per-move completion A->A union D adds only old edge checks. The target factor is unchanged, so the source proof's positive-increment/decrement charge is unchanged. A target reset changes one target occupied check to unoccupied; every animal containing it decreases by the factor r^-1, and no animal increases.

For aggregate coverage, partition the occupied features into old error components and singleton target-defect components. Old component containers contain only old dummy/check vertices; target singleton containers contain only their own target check. They are disjoint as check containers. The old active-density/confined-container bounds hold exactly as before, and each target defect has its own active reset with container size one. The argument needs these disjoint container/progress properties, not an artificial assertion that target defects cannot be geometrically adjacent to old errors.

A poor target singleton cannot occur: whenever an animal contains its occupied check it contains that reset's entire changed set and is directly covered. A poor OLD component is completed exactly as in the source proof, adding only old features; the target exponent again remains unchanged. The sparse-animal estimate still holds because log r<=log(1/theta).

Therefore the same bookkeeping should give, throughout the old component-safe basin,

 (L_old-majority+L_target-reset)^* V <= -gamma(theta,u,r0) W+b,   (M1)

uniformly for r in [r0,theta^-1], with b independent of total block size. The constant gamma can be tiny because r0-1 is small; reset/majority rates remain fixed and may be chosen correspondingly large. This is a finite-body atomic construction, not an unproved two-body compiler.

## C. Absorb arbitrary dirty targets at the soft endpoint
At r=r0, bound r0^(k_target)<=r0^|A| pointwise, even on arbitrary target/bath states. Choose log r0 much smaller than u log(1/theta). It consumes only a fixed fraction of the vacuum exponent. The rooted graph-retraction counting from STAGED_CAPTURE_RETRACTION then bounds this SOFT temporary V by a stronger-parameter old rooted potential, with no assumption on target state or correlations.

Thus arbitrary initially dirty targets do not impose exp(c*n_new) initial cost: their initial coefficient is deliberately too soft to defeat the animal vacuum suppression. This is not claiming the targets are physically clean yet.

## D. Ramp the penalty while actual resets clean the targets
Let r(t) increase from r0 to theta^-1. The test-observable derivative is

 partial_t V=(r'/r) sum_A k_target(A) f_A <=(r'/r) W.

Choose r'/r<=gamma_min/4 and reserve the other drift fractions for physical HP noise, quantum port reads, and logarithmic moment restoration. The ramp takes a fixed time depending on hardware constants but not block size. At its endpoint the test honestly charges target defects at full syndrome weight. This is the joint weighted reset receiving argument: it never inserts an independent-target probability assumption.

The same product Z=1+K V construction and log-sum estimate apply, now on the temporary graph. Bounded-leg remote noise still costs C eta W, since each local system leg changes only a bounded number of OLD or TARGET features. Shared bath and old-target correlations remain in the operator inequality.

## E. Noisy constant-depth copying
Ideal CNOTs copy each parent into its four new children, with fixed-depth scheduling and bounded Hamiltonian strengths. For an output edge (x',y'), its error parity is the old parity of the retracted parents XOR the involved target defects; an edge retracting to a loop has only target contributions. Thus any occupied output check is covered by a bounded number of occupied temporary input features. Each temporary feature covers only a bounded number of output checks. The retraction/completion count therefore supplies the same stronger-parameter pullback as (C1), now from the HARD temporary mixed potential rather than an assumed pure-zero target state.

A precise partial-circuit estimate is still required. The intended method is:
* reserve a stronger parameter margin before copying;
* pause the old majority and target resets for the fixed copy duration (or explicitly schedule commuting subsets);
* conjugate the test by the actual IDEAL partial copy circuit, so its derivative cancels the scheduled ideal copy Hamiltonian;
* relax the reserved animal parameters during this interval, yielding a negative multiple of W that pays ongoing read perturbations and C eta W;
* use constant-depth lightcone enlargement in the weighted-noise bound, as in the accepted source lift.

The old root is only a CNOT CONTROL, so its Z and the nominal classical read condition are not changed by ideal copying. Incorrect reads still use the full-controller comparator already discussed, not a current-bad-port approximation to delayed payloads.

This step must explicitly show that the conjugated orbit algebra and root-to-error witness survive the fixed-depth partial circuit; a handwave that all copy faults are stochastic would be invalid. The footprint enlargement is constant, so no volume or log n factor is expected, but this remains a proof obligation.

## F. What this would establish, and what remains separate
Combining old-parameter sharpening, soft target attachment, penalty ramp, bounded-depth copy, and the rooted pullback gives a fixed-duration acquisition cycle with an O(1)-source rooted/product moment bound. Repetition over O(log n) growth stages does not require unprotected transmission for log n time or a changing read port. Root logarithmic drift supplies restoration between cycles rather than adding a constant moment penalty forever.

Still separate:
* literal mixed-graph map/completion constants for the final hardware family;
* the partial-copy weighted operator estimate and finite pauses;
* global classical phase-exit control during all stages;
* one joint multirecord bad-block/local-source decomposition, rather than per-record gentle cuts;
* initial fixed seed capture and the relation between its actual raw classical outcome and source pointer conventions.

Finite reset service has an intrinsic nominal residual parameter unless its duration is chosen against the desired source accuracy. It may be made a sufficiently small fixed constant, or its fixed duration may depend on a declared physical eta benchmark to obtain an eta^a scale. Do not label a hardware-independent nominal floor O(eta) without this calibration choice. None of these resource constants grows with computation horizon.

## G. Explicit partial-copy test (16:25 refinement)
The partial-copy receiving calculation can be made exact, conditional only on the already specified mixed-feature constants. Fix theta_pre, write L_pre=log(1/theta_pre), and reserve u_a<u_b at preparation's end. During the fixed-duration copy interval [0,tau_c], pause old majority and target resets and use actual scheduled ideal unitary U(t), with U(0)=I. Define

 V_t=U(t) V_pre(theta_pre,u(t)) U(t)^dagger,
 F_t=F_Q product_j [1+K V_(j,t)],

where u(t)=u_a+(u_b-u_a)t/tau_c. The actual ideal copy Hamiltonian gives EXACT cancellation

 partial_t V_t+i[H_copy(t),V_t]
   =-L_pre u' U(t) W_pre U(t)^dagger.               (M2)

The root port Z commutes with every copy gate because every old vertex is a CONTROL and never a copy target in this stage. Hence the wrong-port projector, and the fixed-baseline native comparison structure, commute through U(t). F_Q itself acts on quantum DATA/apparatus, not record systems, so it also commutes with U(t). The bounded read perturbation is paid by (M2), using exactly the same rooted wrong-port witness.

Conjugate each ACTUAL HP noise term by the partial ideal copy circuit. It still has a constant-size system support, with constant incident cb enlargement, because the stage has fixed depth and each vertex has bounded copy incidence. In this frame V_pre is diagonal and the previous rooted orbit estimate applies. Thus its noise contribution is at most

 C_copy eta K W_pre/(1+K V_pre)

per record factor, plus the ordinary quantum DATA/apparatus incident source. Distant original legs are still distant bounded-number legs; no noise-support clique is introduced.

Choose L_pre(u_b-u_a)/tau_c larger than the required read-credit coefficient, leaving a margin for noise and log-moment restoration. This is compatible with the fixed u interval: theta may be chosen arbitrarily small FIRST, and all gate durations/strengths remain fixed. The resulting admitted eta threshold may be extremely small. At t=tau_c, the exact rooted pullback bounds the desired new-graph potential by U(tau_c)V_pre(theta_pre,u_b)U(tau_c)^dagger. Therefore replacing the comparison test by the new-graph test is nonincreasing.

This proves the intended finite-copy inequality at the ideal bounded-depth source plus arbitrary bounded-leg incident-HP level, subject to the mixed-graph pullback and full-controller relative-norm premises already stated. It does not prove the global/multirecord phase-exit marking. In particular, there is no perfect target assumption, no classical noise trajectory, and no cost proportional to n from pausing majority for this fixed interval.
