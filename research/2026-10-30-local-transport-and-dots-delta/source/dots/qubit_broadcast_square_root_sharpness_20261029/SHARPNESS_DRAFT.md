# The square-root broadcast-loss exponent is necessary
2026-10-29. Root analytic construction; independent review pending. This is a lower-bound example for the EB-comparator objective, not a claim about historical novelty.

Fix 0<e<1. Take the four equiprobable qubit states with Bloch vectors +e X,-e X,+e Z,-e Z. Their mean is I/2. Let the physical broadcaster measure Z and prepare two copies of its classical outcome |0> or |1>. Each marginal is the qubit Z-dephasing channel.

Define g(e)=ln(2)-h((1+e)/2), with natural-log binary entropy. Input Holevo information is g(e). The Z pair retains its information, while both X states map to I/2, so each marginal Holevo information is g(e)/2. Each loss is delta=g(e)/2=e^2/4+O(e^4).

We prove that the minimum average trace distance from the ensemble to its image under ONE common EB qubit channel is exactly e/4.

Every EB qubit channel has a measure/prepare representation with effects E_j=p_j(I+m_j.sigma), sum p_j=1, sum p_j m_j=0, |m_j|<=1, and prepared Bloch vectors r_j with |r_j|<=1. Its affine Bloch matrix is T=sum p_j r_j m_j^T. Therefore its nuclear norm is <=sum p_j |r_j||m_j|<=1. The translation is t=sum p_j r_j.

For the +/- pair along axis a, the sum of their Euclidean output deficits is
 |e(I-T)a-t|+|-e(I-T)a-t| >=2e |(I-T)a|.
Trace distance is half Bloch distance. Averaging all four states gives
 error >= e/4 [|(I-T)e_x|+|(I-T)e_z|]
       >= e/4 [2-T_xx-T_zz]
       >= e/4.
The last step uses T_xx+T_zz<=||T||_*<=1. This also covers arbitrary translations and arbitrary finite POVMs.

The EB channel F=(dephase_X+dephase_Z)/2 has T=diag(1/2,0,1/2), t=0 and attains error e/4 for all four states. Thus the bound is exact.

Consequently error/sqrt(delta) ->1/2 as e->0. No uniform bound o(sqrt(delta)) is possible, even for an actual two-output classical broadcaster, a maximally mixed prior, no quantum reference, and four states. This matches the exponent of the separate slow-mode upper construction if that construction passes receiving review. It does not make that construction's large constant tight, nor establish a computationally cheap acquisition procedure.
