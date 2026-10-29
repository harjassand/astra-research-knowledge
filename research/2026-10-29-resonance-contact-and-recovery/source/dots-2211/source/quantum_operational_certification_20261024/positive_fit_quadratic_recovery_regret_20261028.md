# A quadratic native-recovery certificate from a positive fitted algebra

28 October 2026. Root candidate corollary; independent review pending. This concerns one logical qubit's entanglement fidelity, NOT complete-memory process distance. It can remain useful when a much stronger operator-inverse target is not met.

## 1. Fixed actual channel: sound without true block positivity

Let the actual qubit-input channel N have full accessible physical output dimension d. Put C_j=N(sigma_j/2). For any CPTP decoder R define A_R,j=R†(sigma_j). Then

    Fe(R composed N)=[1+sum_j Tr(A_R,j C_j)]/4.

The input is a Bell pair independent of the actual source memory defining this channel. This is neither a collective multi-logical nor a complete retained-memory objective. A local-envelope measurement only licenses optimization over that same local output.

Suppose a known physical Pauli triple A and a known symmetric own-commutant coefficient block S>=kappa I have been fitted, giving Ctilde_j=sum_k A_k S_kj. The fitted Ctilde need not itself be a physical channel. Its positive block nevertheless gives the received convex dual/curvature inequality for ALL unital-CP proposals Phi:

    F_Ctilde(A)-F_Ctilde(Phi) >=(kappa/2)D^2,
    D^2=sum_j ||Phi(sigma_j)-A_j||F^2.

Let e be any certified bound on ||C-Ctilde||_(sum F^2), for example the full observed fit residual plus sqrt(3d)a on simultaneous operator-confidence intervals. Then

    max_(R CPTP) Fe(R N)-Fe(R_A N) <= min(1,e^2/(8kappa)). (1)

Proof: at any proposal Phi, its true unscaled objective advantage over A is at most eD-kappa D^2/2, whose scalar maximum is e^2/(2kappa). Divide by4. R_A is the actual extraction channel associated with the exact physical Pauli triple A. The proof does not assume any true positive-block representation, and does not certify the source belongs to one. A positive fitted model is a robustness witness around the actual measured contrasts.

Data-dependent candidate/fit selection is permitted on the simultaneous confidence event. Failed fitting or nonpositive candidate gaps lead to abstention or no nontrivial certificate. Statistical failure probability and actual gate/calibration/readout discrepancies are paid separately; implementation errors need not preserve the nominal dual identity. Record-averaged versus conditional guarantees retain their actual acquisition contract.

This certificate is for the SAME actual channel (or precisely specified averaged test channel) whose contrasts were acquired. It must not be carried to a different future retained-memory state merely because it fits the observed bank. It is a native fidelity-regret guarantee, not a diamond bound.

## 2. A different future channel in the SAME positive-algebra family

Now impose the stronger actual structural promise of the received positive-operator acquisition theorem. The calibration channel and every future channel share the same true Pauli triple B, while their positive operator blocks T may change. The acquired fit certificate gives

    D_AB=(sum_j||A_j-B_j||F^2)^(1/2)<=2e/kappa.

For ANY future one-qubit channel satisfying the full-output positive-block contract, B is its full-CPTP native entanglement-fidelity oracle by the same dual. Also

    Fe(R_B N_future)-Fe(R_A N_future)
      =(1/8)sum_jk Tr[(A_j-B_j) T_future,jk (A_k-B_k)].

Here Tr T_future=sum_j Tr T_future,jj=F_Cfuture(B)<=3 because its entanglement fidelity is at most1. Positivity therefore bounds this loss by

    (3/8) sum_j||A_j-B_j||op^2
       <=(3/8) D_AB^2
       <=min(1,3e^2/(2kappa^2)),                  (2)

where the final right-hand side is understood capped at1. This bound is uniform across unknown future block coefficients and actual conditional source-memory states satisfying that same promise. It does not require refitting the changing noise. True block positivity is indispensable for this second scope; it was not needed in(1).

Neither(1) nor(2) bounds coherent complete-memory deviations. The received coherent-error-flag example shows small Bell loss can coexist with square-root complete error. Entangled input/source-memory, joint feedback comparisons and reuse costs must use their separate complete-operation theorems. No generic code threshold or collective decoder optimum follows.

## 3. Practical question and fair baseline

A pilot may fail the uniform inverse guard2e/kappa yet yield a meaningful(1) or(2); this must be calculated, not asserted. The strongest equally informed ordinary approach is the same channel-recovery SDP and ordinary fidelity certification. This note contributes a curvature-based quadratic certificate and explicit separation of its two source scopes, not an invented superiority over that comparator. No acquisition speed claim follows until real confidence bounds, fit quality, noise gap and control costs are evaluated.
