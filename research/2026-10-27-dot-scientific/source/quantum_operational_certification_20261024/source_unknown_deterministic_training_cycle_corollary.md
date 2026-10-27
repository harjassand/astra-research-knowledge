# Fixed twelve-state training cycles, without a random-label transcript

Status: separate stronger access-model corollary, pending independent receipt. It removes the discarded-random-label qualification by a deterministic schedule, not by claiming security against hidden memory or data correlated with program environments.

Let rho_j=|psibar_j><psibar_j| tensor E(|psi_j><psi_j|), j=1,...,12, for the exact qutrit2-design in the received labelled-training theorem. Each is prepared by one fixed known input channel call and a local known qutrit; the state index is publicly fixed. Let omega=(I3/3) tensor E(I3/3), also from one channel call. The exact source identity is
 A=(1/3)sum_(j=1)^12 rho_j-4omega=J-omega.               (1)
No access to J is assumed.

## 1. A thirteen-program controlled collision round

For A-time step h, use twelve fresh program states rho_j in a FIXED order, each with controlled partial-SWAP time h/3, followed by one fresh omega with time -4h. This consumes THIRTEEN original channel calls per round, not two. The weighted generators generally do NOT commute.

Here is a direct bound that includes their noncommutation. Regard all thirteen program registers as present initially and trace them out at the end (equivalent to discarding each after its last interaction). Put c_j=1/3 for the first twelve and c_13=-4. Let H_j=c_j |1><1| tensor SWAP_j. The joint unitary is U(h)=product_j exp(i h H_j). Since sum|c_j|=8,
 ||U'(h)||<=8, ||U''(h)||<=64
for every real h, by differentiating the finite product and using unitarity. Its induced controlled data channel F_h therefore has ||F_h''||_diamond<=256, including any untouched reference. Its first derivative after tracing the independent programs is EXACTLY i[|1><1| tensor A,.] by(1).

The ideal controlled channel exp(i h |1><1| tensor A) has second derivative diamond norm at most4 because ||A||<=1 (A is a difference of two density matrices). Both channels agree at h0 and to first order, so Taylor's integral remainder gives
 ||F_h-ideal_h||_diamond<=128h²+2h²=130h²<=256h².         (2)
Thus all noncommuting collision/Trotter effects are paid without pretending the program states commute.

Repeating N rounds for A-time t gives error at most256t²/N. This is the SAME conservative simulation bound used by the ordinary random-labelled construction, so all its classifier precision choices can be retained verbatim; only sample counts change.

## 2. Actual sample counts and inherited instruments

For the single-projector Hadamard receiver, retain eta,k,N_label from `source_unknown_classically_labelled_training_recovery_corollary.md`. It now consumes13kN_label training calls plus one data call per attempt.

For the received coherent-phase implementation with r repetitions and times t_j, retain its N_j=ceil[512t_j S/zeta]. The count becomes13r sum_j N_j, bounded by6656 S²/zeta+13rm, plus one data call.

For the nine-Bell full-throughput Hadamard receiver, retain H=9k and N from `source_unknown_nine_bell_full_throughput_recovery_theorem.md`; its count becomes13HN plus one data call. Intermediate classifier rejections remain nondestructive exactly as in that theorem.

All original full-instrument source bounds remain unchanged: zeta+2epsilon/(3p) relative to the single-outcome reduced-rate ideal, or zeta+6epsilon/p relative to the full-Bell original-rate ideal. Every assisted rate or holdout validation budget must use the corresponding thirteen-program count.

## 3. Precise access improvement and limits

The input sequence and local conjugate states are now deterministic and may be publicly known. The guarantee is for this ONE fixed circuit, not an average over an unobserved random training-label transcript. The data may be any state independent of the fresh program preparation, with an arbitrary untouched reference. There are no random training labels to condition on.

This does NOT remove the IID/memoryless channel and trusted-operation assumptions, nor does it promise security for data adversarially correlated with the quantum program/environment states. The output-register interface, quantum memory and coherent controlled SWAPs are still charged. Thirteen fresh samples are consumed on every round; the result is neither reusable classical decoder software nor a practical-cost claim. The low-dimensional holdout certificate can validate this fixed circuit with exactly the new program count.
