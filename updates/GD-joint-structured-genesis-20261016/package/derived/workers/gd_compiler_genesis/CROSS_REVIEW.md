# Separate review of the actual-rotation compiler and invariant floor

16 October 2026. This review was explicitly requested by the root investigator **after** this worker's genesis artifacts were sealed. It did not influence the sealed genesis proofs. Reviewed source: `gd_compiler_adversary/PROOFS.md`, SHA-256 `a978f58856c505125a0c8c1ae64ae8cb9ab787db16cc3eb2fd41a34df3e80101`, operative Sections 4 and 5. The whole proof file was viewed as context. No peer scientific script or check output was read or executed, and no peer artifact was changed.

**Disposition:** both core results reconstruct correctly under their exact assumptions. This is same-team internal review, not external validation or a historical-priority finding. The physical actuator/predicate promises and the memory receiver remain conditional.

## Section 4: actual correction-rotation minimax

The actual channels are CPTP because the rotation preserves the active rate operator: `A_theta,u† A_theta,u = Pi`. Together with the exact inactive jump `I-Pi`, the rate operator is identity. Thus the signed difference is a difference of completed correction channels, and its active coefficient matrix is genuinely the jointly constrained rank-one difference `kappa(ww^T-e0e0^T)`. It is not an arbitrary independent coefficient box.

I independently reconstructed the attaining floor. On the span of `e0,u`, its active matrix is

\[
\begin{pmatrix}
\alpha-\kappa q&\kappa\sin\theta\cos\theta\\
\kappa\sin\theta\cos\theta&\beta+\kappa q
\end{pmatrix},\qquad q=\sin^2\theta.
\]

The stated endpoint choices give determinant `kappa(q0-q)(kappa+beta-alpha)`. For `q0<=1/(m+1)`, the final factor is nonnegative: `alpha-beta-kappa` increases from `-kappa` to zero. Both diagonals and the `m-1` transverse eigenvalues `beta` are nonnegative. Real symmetric cross coefficients contribute zero to the adjoint-product sum because `A†B_j+B_j†A=0` and the selected Pauli axes anticommute. The inactive term supplies the complement, giving scalar total rate `Lambda I`. This establishes CP and TP, including the singular endpoint. At larger angle intervals, `N=C0`, `Lambda=kappa` is an immediate attaining channel.

The lower bound against **every fixed CPTP center** is sound. Restricting the input to `Pi` is a legal isometric input restriction of a channel and preserves trace preservation on that restricted input. Its normalized Choi matrix has trace one. The restricted active Choi vectors of `A,B_j` have unit norm and are orthogonal, using the stated actual two-check Pauli support. A full-patch Choi vector instead has an active-rank factor; dropping that factor without restricting the input would have been invalid. The source performs the restriction correctly.

Projecting the restricted Choi matrix of an arbitrary center only decreases its trace, so output leakage cannot evade the lower bound. Sign/permutation averaging is performed on the projected necessary matrix feasibility problem. It need not be physically implementable as a covariance of the original center: invariance of the complete uncertainty family suffices to retain feasibility and trace. It reduces the problem to `diag(a,b I_m)` and the exact convex objective

\[
mb+\kappa q_0+
\frac{\kappa^2q_0(1-q_0)}{b+\kappa q_0}.
\]

Its interior minimizer is `b=kappa(t0/sqrt(m)-q0)` precisely until `q0=1/(m+1)`. The resulting value equals the proposed rate. For a larger uncertainty interval, the included critical angle forces the lower bound `kappa`. This matches the attaining construction. I found no mathematical gap in this minimax argument.

The exact norm comparison also reconstructs. The restricted-input error Choi matrix is the difference of two unit vectors with overlap `cos(theta)`, giving trace norm `2kappa|sin(theta)|`. The unitary-channel difference composed with the active trace-nonincreasing CP action gives the matching diamond upper bound for `|theta|<=pi/2`. No ambient-patch dimension factor remains.

## Section 5: same common actuator error

For all three axes, the active part of `(C0+C1+C2+C3)/4` is complete depolarization on the written face applied to `A rho A†`. Conjugation of that output by any **face-only** unitary leaves it invariant. Consequently four completed conditional-action streams of equal rate retain the claimed average floor when their active branches all inherit the same postrotation. Their inactive branches must remain exactly the specified complement.

The proposal positivity proof is also correct. In the displayed active family its matrix is `(nu/4)I_4+kappa(ww^T-e0e0^T)`. The difference has eigenvalues `+kappa|sin(theta)|,-kappa|sin(theta)|,0,0`. Thus `nu=4kappa sin(theta0)` is sufficient throughout `0<theta0<=pi/2`; trace preservation follows from the completed channels and trace-annihilating difference. At `theta0=0`, apply the already stated zero-clock convention: omit the floor and clock, rather than evaluate the displayed quotient `E/nu`.

The invariance requires one common face-only postrotation on every active action at the generator level. It does not cover command-dependent rotations, unknown memory–bath unitaries, faulty predicates, leakage or faulty inactive branches. The source states the first implementation exclusions, and the face-only scope is explicit in its formula. No optimum under the additional invariant-floor constraint was claimed or established.

## Independent finite checks and scope

`check_cross_review.py` constructs a fresh three-qubit algebra with two independent commuting predicates and one written face; it does not import peer code. The actual 11-qubit trace orthogonality follows separately from the source's Pauli support statement. `CROSS_REVIEW_CHECKS.json` records:

* Sixty actual rotation cases for one, two and three axes, across both rate branches, their boundary and realized zero angle. Maximum channel/Kraus difference is `6.67e-16`, and the scalar-rate error is `4.45e-16`.
* The restricted-input Choi formula agrees within `6.21e-17`; the independent endpoint-dual rate evaluation agrees within `7.78e-17`.
* Eight arbitrary common face-rotation checks preserve the averaged floor within `1.12e-16`. Twelve invariant-floor proposal checks are CP to floating-point precision.
* A command-dependent rotation deliberately outside the model changes the average by `0.1525293182`, confirming that the common-actuator assumption matters.
* The reviewed source and every original genesis artifact still match their recorded hashes.

These finite checks support the analytic sign, normalization, singular-case and scope review. They do not establish the classical memory tail, geometry incidence counts, hardware qualification, a useful threshold or historical novelty. Those topics were not part of this cross-review. No source change is requested for the core proofs; explicitly applying the zero-angle convention in Section 5 would be a minor presentation clarification.
