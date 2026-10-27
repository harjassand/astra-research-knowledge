# Independent receipt: pure-physical, mixed-logical reset

Status: PASS, 2026-10-26. Governing proof: `pure_physical_mixed_logical_reset_value_theorem.md`. Actual class: E(rho)=p rho tensor sigma+q Tr(rho) P_u tensor eta, arbitrary finite density matrices sigma,eta, without a commutation assumption. Output isometries preserve the result. This does not receive arbitrary physically mixed or correlated reset states.

## Actual source identity

By matched covariance u may be set to physical output label 0. Write S=p sigma/3, Q=q eta/3. The normalized Choi input is Phi3 tensor 3S plus I3 tensor P0 tensor Q. Only the physical |00> reset sector overlaps the maximally entangled success sector, with squared overlap 1/3; the other two reset sectors are orthogonal. Its coupled logical block has Gram G_(1/3)(3S,Q), equivalently the displayed T after a physical basis change.

The reference success marginal has logical weight S on each qutrit coordinate, and reset weight 3Q on coordinate 0. Thus its sole overlap is L_1(S,3Q). The normalized WH image of Phi3 is the antisymmetric projection divided by 3, so success weight is S in each of its three sectors. Exactly two of these have overlap 1/2 with the reset physical column, whose weight is Q. Their contribution to the deficit is -2 times two copies L_(1/2)(S,Q), hence the factor -4, not -2. The remaining sectors are orthogonal. The unscaled output block has the displayed L up to an irrelevant sign unitary on one physical basis vector. Orthogonal-reference success/reset baseline has zero deficit even for mixed logical sigma and eta. These facts give equation (1) exactly, with no measurement of logical eigenvectors.

## Noncommuting series and integration

The determinant ratio for G_c versus diag(X,Y) is det(I-c P_X P_Y). P_X P_Y has the nonnegative spectrum of a positive sandwich (zero eigenvalues included), and for every s>0 its spectral radius is strictly below one. Trace equality cancels the resolvent entropy subtraction terms, giving the positive logarithm series (2). This argument remains valid for singular X,Y at positive s. Each L_c is finite; Tonelli and the finite entropy integral justify its series, including c=1. In the finite signed combination the absolute sum of terms is dominated by the sum of the three finite positive L integrals, so separating n=1 from n>=2 loses no convergence term.

For n>=2, P_(3Q)>=P_Q, hence P_S^(1/2)P_(3Q)P_S^(1/2)>=P_S^(1/2)P_Q P_S^(1/2). Eigenvalue monotonicity gives the trace-power inequality for each integer n; no false operator monotonicity of matrix powers is needed. Since 4/2^n<=1, these orders are pointwise nonnegative.

The integrated n=1 term uses separate spectral bases and weights |<i|j>|², retaining all noncommutativity. J(a,b)=a psi(log(a/b)); therefore (1/3)J(3a,b)+J(a,3b)-2J(a,b) is exactly a times the centered psi difference with step log3. The displayed second derivative is correct. Its numerator bracket has second derivative z exp(z)>0 for z>0 and vanishing value/first derivative at zero. Reflection psi(-z)=psi(z)+z and psi''(0)=1/6 give strict convexity on the whole real line. Thus the integrated linear term is strictly positive for every positive-eigenvalue overlap.

Zero eigenvalues contribute zero to J by continuous extension. Alternatively compress or regularize and use finite entropy continuity for the nonnegative result; strictness itself follows directly from positive spectral overlaps, not from an invalid strict-limit argument. Consequently equality holds exactly for S Q=0, namely pq=0 or sigma eta=0. This includes all singular support configurations.

## Lineage and replay

The old physically flat reset has physical factor I3/3, not P_u. Its identity-baseline operator-bath lifting theorem does not directly apply to the present baseline I3 tensor P_u. The general coherent-star theorem does not directly receive a mixed noncommuting logical success/reset pair either. This is a distinct internally received class; no historical-priority assertion is made and no convex-mixture inference to arbitrary physical reset is used.

Replayed `pure_physical_mixed_logical_reset_check.py` in its required working directory: PASS, 60 complex noncommuting cases, maximum actual-source/coherence-formula discrepancy 3.52e-15. The analytic argument above, rather than that finite test, is the sign and equality proof. No correction to the governing manuscript was required.
