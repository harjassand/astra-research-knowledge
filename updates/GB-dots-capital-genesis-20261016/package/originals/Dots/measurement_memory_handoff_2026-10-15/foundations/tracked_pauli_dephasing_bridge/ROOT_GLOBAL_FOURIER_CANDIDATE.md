# Global private-character telegraph bound: construction to audit

Date 2026-10-15. Root construction, awaiting independent reconstruction. It is a candidate strengthening of the existing additive private-pulse Fourier effect theorem, not a claim that arbitrary hardware supplies this interface.

## Algebraic model
For a finite selected set S, condition on every unselected classical seed/clock. Let
H_f,xi(t)=H_base(t)+sum_(i in S) (-1)^f_i xi_i(t) A_i(t),
where f_i are independent fair bits, xi_i are independent rate-gamma_i telegraph signs starting +1 at each pulse's start, A_i is Hermitian, ||A_i(t)||<=J_i and supported in an interval of length tau_i. Both H_base and every A_i are independent of every selected f_i and xi_i. They may contain arbitrary noncommuting bath terms, arbitrary finite reservoirs/reference dilations and interleaved ideal operations. No physical commutation among A_i or with H_base is assumed. Selected intervals may overlap or recur on the same memory coordinates.

For fixed xi let K_odd(xi)=E_f (-1)^(sum_i f_i) U_f,xi. More generally retain the complete Fourier Kraus family for all initial frame coordinates and sum squared effects over labels nonzero in the selected bits. The effect is the L2 Fourier-projection norm squared, with unselected coordinates averaged by Parseval.

Candidate exact bound:
E_xi K_odd(xi)^dagger K_odd(xi) <= product_i B(J_i,gamma_i,tau_i) I,
B={exp(-gamma tau)[cosh(d tau)+(gamma/d)sinh(d tau)]-1}/2,
d=sqrt(gamma^2+4J^2),
B <= {exp(2J^2 tau/gamma)-1}/2.

## Proof mechanism
Expand only selected interactions in the interaction picture of H_base. Odd Fourier extraction retains words with an odd count of each selected species. In K^dagger K, each species therefore has an odd count on each branch and an even combined count 2m_i. Its averaged telegraph moment is the nonnegative paired-gap kernel exp[-2gamma_i sum_(r=1)^m_i(u_(2r)-u_(2r-1))], with times ordered within that species's own support interval. Operator word norms are bounded by product J_i^(2m_i), without commuting any bath operators. Branch shuffles contribute 2^(2m_i-1), and summing all interspecies time orderings partitions the product of ordered simplices. Exact sums yield B; extending pair-gap integrals yields the exponential majorant. Taking operator norm of the positive final effect establishes the Loewner bound. Arbitrary input bath/reference states are covered by the operator inequality.

## Application to full Pauli pulse frames
In the additive private-pulse interface, each pulse i has its own independent full initial Pauli frame, affecting only that pulse's interaction. Pick one generator bit f_i and its independent Poisson updates. Split the pulse's frame-conjugated interaction into even/odd parts under that generator. The even part is independent of this bit and its update process; the odd part is (-1)^f_i xi_i times an operator of norm <= the original pulse norm. Condition on all other generator seed/update processes. This realizes the algebraic model if the complete physical dilation really has the requisite private-coordinate dependence.

If pulse i's nonzero character is detected by any of m_i generator bits, union over one detecting bit for every selected pulse yields the global nonzero-character effect bound product_i[m_i B_i]. Individual factors may be capped at one by dropping large-factor pulse selections and using the same unconditional theorem. For an n-qubit full Pauli frame, m_i=2n. The Kraus record also retains continuous update histories and all other physical outcomes; all outcomes must be summed for the effect bound. Seeds must remain private and be coarse-grained before claiming a Pauli-diagonal averaged channel.

This route does not rely on a simultaneous endpoint parity observable, so should permit the earlier completion-support argument on clean isolated pulse patches even when a memory patch is reused at later times. This last composition remains to be checked against the exact prior theorem.

## Physical scope
Ideal instantaneous tracked Pauli controls; initial seed independent of initial joint state; final inverse exact; lab interaction independent of control seed except stipulated conjugation; no direct bath access to controller/clock reservoirs. Noise during finite-duration randomizer pulses is not included. Clean identity-noise intervals after exact correction are the immediate candidate interface. Randomizer changes during a nontrivial noisy Clifford core need a separate compiler and control-noise qualification; the prior fixed-core theorem cannot silently supply it. This is not the autonomous untracked stabilizer-dephasing model.
