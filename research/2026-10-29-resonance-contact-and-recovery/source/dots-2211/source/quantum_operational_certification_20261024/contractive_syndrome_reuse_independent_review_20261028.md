# Independent review: contractive syndrome reuse and actual reset interface

28 October 2026. **PASS at the stated closed-register, complete-map scope.** Governing recurrence: `contractive_syndrome_reuse_20261028.md`. Governing adaptive circuit identity: `flagged_faultfree_all_operator_reset_20261028.md`. Receipt binds exact versions and the current gadget-source amendment. No historical novelty, global threshold or hardware claim is accepted here.

## General time-varying theorem

The proof is valid for arbitrary CPTP references A_t satisfying P A_t=A_t=A_t P, not only A_t=P or constant channels. P is a CPTP idempotent; Q=I-P is only a linear decomposition, with diamond norm at most two. Setting T_t=E_t...E_1 P, S_t=P T_t and G_t=Q T_t gives exact recurrences. In particular, A_t G_(t-1)=0, since A_t=A_t P, while Q A_t=0. Also S_t is an actual CPTP composition and has norm one. These facts establish

    g_t = 2 epsilon_t (1+g_(t-1)), g_0=0,
    final half-diamond <= sum_t[b_t + epsilon_t g_(t-1)/2].

The comparison to A_t...A_1 P is a telescoping recurrence contracted by CPTP A_t. It never bounds the actual past by a product of perturbation norms. If every epsilon_t<=epsilon<1/2, g_t<=2epsilon/(1-2epsilon); the cross term vanishes at t=1. Hence the uniform bound is sum b_t+(T-1)epsilon²/(1-2epsilon), capped at one. The separate author's constant-round estimate with T rather than T-1 is weaker but valid. There are no physically inserted intermediate P maps in this argument.

## Independent nontrivial exact fixture

`contractive_syndrome_reuse_independent_check_20261028.py` imports none of the author routines. It represents maps on a logical qubit and syndrome qubit as exact rational 16-by-16 superoperators. P preserves the logical qubit and resets syndrome to |0>. A_t combines this reset with a different nonidentity logical Z rotation each round. Actual E_t applies coherent Z-logical/X-syndrome rotations both before and after the reset; their angles vary with t. Thus a coherent residual from one round interacts with the next round before the next real reset. The example is not a product of independently decoded cycles.

For eight successive rounds the program verifies complete-map recurrences exactly, CPTP Kraus completeness, P A_t=A_t=A_t P, and the complete final map. The final map is an exact dephasing mixture relative to the reference unitary product, so its half-diamond distance is exactly its dephasing probability, not merely a sampled-state lower bound. Certified epsilon_t bounds come from exact unitary distances and channel hybrids; b_t is exact. All errors lie below the finite recurrence bound. At T=2 the true error is about .010858, demonstrating feedback beyond simply adding the two individually decoded dephasing probabilities.

A separate exact negative control removes actual reset and verifies error sin²(T theta), rather than a linear sum of sin²(theta). At theta=0 the identity channel is full diamond distance two from P, witnessed by syndrome |1>; this family is outside the small-complete-map hypothesis. It is not a counterexample to the accepted theorem.

## Equality of the fault-free physical gadget to P

The full-operator argument is correct. Each native data parity coupling commutes with the flag-to-syndrome CX because the controls are disjoint and the syndrome-target X actions commute. The two flag CXs cancel, also for the explicitly compiled H-CX-H coupling. On arbitrary data, the fault-free flag remains unentangled and trivial, while syndrome readout implements the stabilizer's exact projectors.

For each nonzero joint syndrome s, exactly one early-exit prefix—the first nonzero bit—occurs. Its projector followed by the complete fresh pass equals the joint projector Pi_s. The physically applied weight-one correction yields Kraus E_s Pi_s. The zero branch yields Pi_0. The resulting Kraus family is trace preserving, has range in the code and acts as identity there; therefore P²=P on all physical operators, including off-diagonal syndrome operators and reference extensions. This is not inferred merely from the 16 code-error test states. The author's supplementary exact dyadic fixture was inspected and rerun; its 256 Kraus composition checks agree with the algebra.

For a full frame/receiver round, the ideal relation Ad(V†) Ad(V)=id must hold on every physical input operator, not merely clean code states. With that architecture it holds algebraically. The audit does not certify a different receiver's unproved action on syndrome sectors. A_t may include other retained slow registers only when the two-sided absorption identities are actually established on that enlarged space.

## Scoped amendment to earlier physical-gadget review

The clarified mathematical unrolling uses 751 potential locations: 424 flagged, 292 conditional fresh-pass, and 35 conditional single-qubit-correction/idle locations. This corrects the interpretation of 737, which is the maximum executed branch cost, not the number of potential controlled slots. Disabled slots are zero-duration identity bypasses. Bounds are uniform over enabled branches; real waiting intervals require additional actual idle locations and checks. This provides a legitimate bounded ordered-instrument hybrid and fault expansion with trusted classical control. The 424 clean trajectory and 737 executed-path counts remain correct.

The independent gadget simulator was rerun against the amended files and still verifies all 1,528 clean-input single-fault records, the 16 correctable-input cases and 1,024 arbitrary-Pauli fault-free cases. Its previous output was preserved under a `pre751` filename before re-binding. This review supersedes only the earlier receipt's source bindings and potential-slot interpretation, not its scientific single-gadget conclusions or negative controls.

## Load-bearing boundaries

Both epsilon_t and b_t are obligations; one-cycle fidelity alone supplies neither a complete retained-register epsilon nor a reset theorem. All old records must be retired or explicitly retained in the modeled persistent register. Shared baths, record-responsive sources, or initially correlated external memory cannot be omitted when asserting a closed E_t. Full-map local-instrument error contracts and actual reset interfaces are required. Fixed coherent control errors and repeated use of the same learned program are allowed; they are not equivalent to an arbitrary unmodeled bath.

The result closes the deterministic coherent-reuse step for a proved closed finite tile near its full reset reference, with small full-channel epsilon and quadratic projected error b. It does not give a scalable array threshold: epsilon can grow with tile size and all 751 potential locations plus receiver/native operations must be paid. Initial input injection and final physical readout remain separate error budgets. The final P in the stated metric is an analysis endpoint, not an implemented free decoder. No hardware calibration bounds or general source-memory protection were generated by this audit.
