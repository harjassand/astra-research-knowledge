# Failures avoided, actual costs, and the next unsupported operation
2026-10-30. Companion analysis; not a broader theorem than REUSABLE_FINITE_GROUP_FRAME.md.

## 1. Reset-and-switch is not a valid live native handoff
At a completed DATA target U, the live controller frame is U F_mem U^dagger, not F_mem. Resetting only a one-shot program to 0 and changing the memory generator back to its base does NOT remove that difference on busy native prefixes. The global energy counts unary DATA and bad-history flags, not the number of clean busy controllers. Thus a low-energy basin alone does not imply a sparse mismatch. The new construction avoids this entire step: G and F_mem stay fixed for all commands, and e_ab->r_b preserves the frame exactly while native registers are untouched.

## 2. Coherently merged resets have exact stale dark states
The construction uses separate channels J_ab=sqrt(kappa)|r_b><e_ab|. Replacing all channels with the same b by ONE coherent J_b=sqrt(kappa)sum_(a!=b)|r_b><e_ab| is a different and inadequate model. For two distinct a1,a2!=b and current target v!=b,

    |dark>=(|e_(a1,b)>-|e_(a2,b)>)/sqrt(2)

is annihilated by J_b and every other merged jump. The current H_v couples only r_g and e_(g,v), so it also annihilates this stale state. Its probability never reaches r_v. Therefore the uniform absorption theorem fails. Label-resolving reservoir resources are load-bearing, not a notational decomposition of a single jump.

## 3. Resource table for the concrete two-block model
Gamma=GL(2,2), m=6:
- 36 program levels per paired resource column: 6 ready +30 intermediate;
- 30 separately resolved clock-only reset channels per column, all at fixed kappa;
- 5 disjoint coherent command edges for each chosen target, each at Omega;
- one permanent G-dressed native memory generator, with no term added per command;
- grouped onsite capability for BOTH DATA bits, program and corresponding resource registers;
- external classical cumulative-target arithmetic and finite-rate control-waveform delivery;
- finite transition time plus a fixed settling time for every demanded intermediate output opportunity;
- the same ideal target-native-frame endpoint and ordinary product DATA decoder as in the theorem.

H_v has operator norm Omega because its edges are disjoint. Sum J_ab^dagger J_ab=kappa P_intermediate, so the total program generator's simple operator-norm bounds do not grow with m, although channel count and local dimension do. All calibration deviations are counted in the per-column incident JOINT generator-norm budget; resolving thirty channels does not license thirty uncharged errors. No favorable numerical threshold is asserted.

## 4. Why simply enabling an autonomous cyclic program does not solve distribution
An externally selected absorbing target is not a free-running logical clock. In the two-frame subgroup {I,CNOT}, enabling BOTH target Hamiltonians at once yields the four-state cycle r0<->e01->r1<->e10->r0. With separate resets and equal positive rates the stationary population has equal mass in the two frame classes. A deterministic late target r0 or r1 cannot have arbitrarily small unfinished probability. Independent columns then lose synchronized logical phase rather than settling to one protected instruction boundary. This is a counterexample to the specific 'run both directions forever' replacement, not a universal no-go theorem for every autonomous clock or locally coupled command distributor.

The present proof permits arbitrarily many externally delivered targets, but does not create a finite autonomous distributor that selects them, stores an unbounded instruction stream, handles feedback, or synchronizes distant block partners under noise.

## 5. Support growth for changing partners is a separate obstruction
On a block chain, successive CNOTs 1->2,2->3,... conjugate X_1 into X_1 X_2 ... X_(K+1). Tracking these transformations by permanent cumulative conjugation makes a generic memory term's DATA support grow with K. Grouping all touched blocks into one column instead makes dimension/overhead grow. The fixed-b finite-group theorem avoids this only by restricting the available partner set from the outset. It is not a proof that local error-transparent consolidation or other fault-tolerant schemes are impossible.

## 6. Ordinary equal-information baseline and consequential next bridge
If only a final output of a uniform finite-group word is required, a scheduled controller can first multiply the word to one v and execute only U_v (or adapt appropriate terminal measurements). The new theorem's lack of per-command error accumulation is not evidence of a computational speedup. Its genuine content is an actual fixed-locality, noisy finite-register realization of live physical target tracking while native QEC continues through busy controller sectors, with a single common-bath trajectory and no ideal operations between commands.

The next consequential unsupported interface is a physical measurement/resource/feedback or scalable changing-partner operation that cannot merely be collapsed into a finite uniform frame. Noisy retrieval, logical outcome generation, reinsertion/handoff to another physical apparatus, or non-Clifford resource injection would each need an actual controlled channel and a new canonical/warm-entry proof. The ordinary ideal decoder is still only a terminal mathematical interface here.
