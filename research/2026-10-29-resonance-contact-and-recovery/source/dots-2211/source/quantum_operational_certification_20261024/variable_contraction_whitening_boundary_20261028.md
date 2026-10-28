# Failure of pooled whitening when contraction and spectator record co-vary

28 October 2026. Root candidate boundary; separate independent review pending. This is an exact channel construction with a floating matrix diagnostic, not acquired source data.

Take two physical qubits and true mixer V=I. Select a private fair classical branch a. On qubit1 apply amplitude damping of rate9/25, along z if a=0 and along u=(3/5,0,4/5) if a=1. Replace qubit2 with |a><a|. This is a valid mixture of product CPTP channels. Each own-qubit Bloch contraction is positive definite:

    T0=diag(4/5,4/5,16/25),
    T1=(4/5)I-(4/25)uu^T.

Actual signed contrasts for input qubit1 are

    C_j=(1/4) sum_(a=0,1) [sum_k T_a[k,j] sigma_k] tensor |a><a|.

The affine offsets cancel exactly. The Gram matrix is

    G=(T0^2+T1^2)/8 >0.

Whitening yields two blocks proportional to sigma dot T_a G^(-1/2)e_j. Their signs are the unit vectors in these block-dependent directions, not the common true sigma_j. Even the X/Z signs need not anticommute. In general G fixes the SUM of the two block inner products, not each block separately. A positive global Gram and positive sign gaps therefore cannot certify the missing common-factor premise.

The accompanying reproducible floating check obtains sign errors approximately0.05000 and0.06189 for X/Z and X/Z anticommutator norm approximately0.21475, while the smallest whitened sign gap exceeds0.4795. These values illustrate the analytic distinction; they are not statistical confidence claims. The branch can be reset independently each call, so the problem does not require an adversarial continuing memory.

This defeats applying the fixed-T/common-R whitening proof to arbitrary mixtures of differently oriented contractions correlated with spectator factors. It does not prove a general impossibility of learning that mixture: one could exploit its accessible flag or a richer representation. The existing fixed-product and fixed-T conditional-contrast theorems remain unaffected.
