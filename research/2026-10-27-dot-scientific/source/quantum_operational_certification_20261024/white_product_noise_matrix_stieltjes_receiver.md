# Exact 3x3 matrix-Stieltjes receiver for a pure main plus white physical product noise

Consider the actual source A=I3 tensor tau+|psi><psi|, with arbitrary finite reference, tau>=0, and no normalization needed. Put V for the 3-by-reference coefficient matrix of psi, K=VV*, and

 M(s)=V(tau^T+sI)^(-1)V*, g(s)=TrM(s).

Here V_ij are the coefficients of psi in a fixed product basis; the transpose on tau is necessary with that convention. Equivalently V acts from the conjugate reference space, where the conjugate noise operator is used. Every physical baseline I3 tensor tau is fixed by N=W3 tensor id and E=I3/3 tensor Tr_phys, so its deficit is zero.

The input rank-one correction, the three antisymmetric Kraus columns, and the nine depolarizing Kraus columns have exact determinant corrections

 d_I(s)=log(1+g),
 d_N(s)=logdet[I3+(gI3-M)/2],
 d_E(s)=3logdet(I3+M/3).

For d_N, the weighted main vector has physical marginal M; the antisymmetric Stinespring complement is again WH3, so its three-column Gram is (gI-M^T)/2. For d_E, the nonzero weighted reference-marginal spectrum equals that of M, with three copies and factor1/3.

Thus the full exact homogeneous deficit is

 Delta(A)=integral_0^infinity F(M(s)) ds,
 F(M)=2logdet[I3+(TrM I3-M)/2]-log(1+TrM)-3logdet(I3+M/3).  (1)

All unrestricted reference structure is retained in the ACTUAL matrix Stieltjes function M(s), not in arbitrary independent positive matrices at different s.

## Paid differential constraint

The common Gram representation gives, on ranK,

 -M'(s)=V(tau^T+sI)^(-2)V* >= M(s) K^+ M(s).                 (2)

Indeed the 2-by-2 block Gram with entries K,M,-M' is PSD, and its Schur complement gives (2). The covariance remainder is positive and may be nonzero when the main's Schmidt support is not tau-invariant. Also sM(s)->K at infinity. K, its rank and the remainder must not be discarded in an integral-transport argument.

If K=kappa I3, every eigenvalue m_i(s) satisfies -m_i'(s)>=m_i(s)^2/kappa wherever differentiable. Equivalently its effective shift kappa/m_i(s)-s is nondecreasing. This is a necessary scalar consequence, not a proof that arbitrary curves satisfying it are realizable or safe.

## Essential failures to retain

Pointwise positivity in (1) is false. For M=(g/3)I3,

 F=6log(1+g/3)-log(1+g)-9log(1+g/9),

which tends to minus infinity as g->infinity. The entropy must be paid after integration.

Even replacing tau by its direct compression to the main Schmidt support is not a monotone value reduction: the exact already-safe isotropic example in flat_product_noise_schmidt_core_deletion_obstruction.md lowers Delta when a hidden reference component is added, including when K is scalar. Thus the covariance remainder in (2) is not automatically a nonnegative entropy correction. The proven finite-Krylov theorem instead pays an explicit approximation error.

This is a genuinely finite physical-matrix representation of the remaining value problem, not a positivity theorem or a free reference-dimension reduction.

## No unrestricted convexity or concavity in the noise

Even the scalar ray tau=tI3 with normalized maximally entangled main disproves both global assertions. Its exact deficit is

 h(t)=(t+1)log(t+1)-4tlogt
       -6(t+1/3)log(t+1/3)+9(t+1/9)log(t+1/9).

It satisfies h(0)=0, h(1/9)=(10/9)log(5/4)>0, and h(t)=2/(9t)+O(t^(-2)) as t->infinity. A convex function with h(0)=0 and one positive value cannot decay to zero at infinity; a concave function with a positive value and limit zero must eventually have a negative secant slope, which by concavity forces divergence to minus infinity. Thus neither unrestricted tau-convexity nor tau-concavity can justify reduction to extreme noise. This does not rule out a separately proved fixed-trace or source-constrained convexity statement.
