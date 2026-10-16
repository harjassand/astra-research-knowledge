# Separate additive private-sign Fourier lemma

This is an audit of an additional algebraic construction. It is separate from the clean stroboscopic Pauli/Choi bridge in REPORT.md. It does not establish that any unspecified correction-interleaved physical model has the required additive form.

## Exact sufficient model
After conditioning on any other randomness, assume the joint Hamiltonian has precisely

 H_f,eta(t)=Hbase(t)+sum_{i in S} (-1)^f_i xi_i(t) A_i(t),

where independent uniform binary f_i are independent of all other randomness and input; independent telegraph xi_i start at +1 with rate gamma_i; and Hbase, A_i are independent of every selected f_i and selected xi_i path. The A_i are Hermitian with ||A_i(t)||<=J_i and supported in known time intervals I_i of lengths tau_i. Piecewise prescribed ideal unitary operations may enter the Hbase propagator only if they too are independent of all selected bits and clocks. No term carries a product of two selected signs. Bath operators and all terms may otherwise fail to commute.

For an arbitrary finite-dimensional joint input space, let U_f,eta be the resulting propagator and define the Walsh coefficient

 K_S,eta=2^(-|S|) sum_f (-1)^(sum_i f_i) U_f,eta.

The uniform bit-average channel has a positive Kraus expansion in all Walsh coefficients. There is no presumption yet that a Walsh label is a spatial Pauli fault.

## Uniform effect bound
Pass to the Hbase interaction picture. Its unitary is independent of selected bits/clocks, preserves A_i norm bounds, and cancels in K_S^dagger K_S. In the absolutely convergent Dyson expansion, Walsh projection forces an odd number of A_i insertions for every selected i. Both bra and ket have this odd constraint. For each i the combined 2m_i insertion times have telegraph expectation

 exp[-2 gamma_i sum_r(u_(2r)-u_(2r-1))].

This is nonnegative. Bounding quantum matrix elements by products of operator norms and summing ket/bra odd colorings gives the same factor 2^(2m_i-1) as the supplied independent endpoint proof. Interleavings partition the product of the per-species ordered simplices, so there is no additional multinomial penalty even if the A_i and bath operators do not commute.

All A_i insertion times lie inside I_i. The paired-gap integral is invariant under translating I_i and bounded by the interval-length expression. Consequently, uniformly in every normalized joint input,

 E_eta K_S,eta^dagger K_S,eta <= product_i B(J_i,gamma_i,tau_i) I,

with B the finite-rate positive majorant from REPORT.md, section 10. If the physical rate or amplitude profile differs outside I_i, it is irrelevant because A_i vanishes there; selected clocks must retain the specified independent telegraph law within I_i.

If there are additional independent initial bits h, summing squared full Walsh coefficients over all unselected Fourier labels equals E_h of the selected-bit coefficient effect, by Parseval. Thus the same uniform bound constrains the event “selected Fourier bits are all odd,” with no penalty for the remaining labels. Applying an ordinary positive union bound to possible detecting coordinates gives the corresponding product of sums of B factors.

## Required separation from physical claims
This lemma tolerates arbitrary persistent bath and arbitrary selected-randomness-independent unitary background, but its algebraic independence conditions are substantive. They are not implied solely by words such as ideal correction, local pulse, private randomness, or tracked frame.

In particular, a correction selected using the same seed, an ideal core whose toggling frame depends on the selected bits, a noise term proportional to a product of two selected signs, or direct clock leakage invalidates this decomposition or this proof. Grouping interacting signs can change the resulting rate or locality factors. Physical support/completion properties of the resulting Walsh Kraus operators require a separate theorem before interpreting them as local faults. The Choi bridge and coloring theorem in REPORT.md remain valid independently within their narrower verified clean-interval scope.
