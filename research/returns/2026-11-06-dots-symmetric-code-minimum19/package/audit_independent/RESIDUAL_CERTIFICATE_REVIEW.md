# Review of residual-bounded dual certificate plan

The proposed approach is mathematically valid, subject to the checks below. A numerical positive slack, particularly with optimal_inaccurate, remains only a candidate until this certificate is verified.

## Sign convention and exact target

Discard the auxiliary slack variable by evaluating all constraints at epsilon=0. Write equalities as A(x)=b, scalar inequalities as q_i(x)>=0, and PSD inequalities as F_i(x)>=0. For arbitrary real equality multipliers y, nonnegative scalar multipliers z_i, and PSD matrix multipliers Z_i, form

L(x)=y·(A(x)-b)-sum_i z_i q_i(x)-sum_i Tr(Z_i F_i(x)).

For every true feasible x, L(x)<=0. Expand the SAME expression as

L(x)=c+r_a·a+sum_i Tr(r_i X_i).

Here c=-y_a0-(D/2)y_sum if these are the only inhomogeneous constraints, with the corresponding equalities written a0-1=0 and sum(a)-D/2=0. Do not rely on a solver's generic dual-objective sign; compute this expansion explicitly. No epsilon-stationarity equation is required for a zero-slack infeasibility certificate. Consequently clipping scalar duals and lifting matrix duals is permitted, as long as all residuals and the constant are recomputed afterward.

## Compactness bound

The enumerator has a>=0 and sum a=D/2, so |r_a·a| <= (D/2)||r_a||_infinity.

For each J, define W_sym=Qs^T Qs and W_std=Qp^T Qp+Qm^T Qm. The marginal constraints and exact identity 1^T M diag((-1)^l)=D e0^T give sum_l w_l=4 and therefore

sum_J (2J+1)[Tr(W_sym A_J)+Tr(W_std B_J)]=8.

If W_i>=g_i I with rigorously positive g_i, then the PSD parameter matrices obey sum_i dim(J_i) g_i Tr(X_i)<=8. Hence

|sum_i Tr(r_i X_i)| <= 8 max_i ||sym(r_i)||op/[dim(J_i) g_i].

This proves infeasibility when c exceeds the enumerator bound plus this block bound. A single common minGram is safe but weaker. The standard factor 2 is justified only after establishing Qm^T Qm=Qp^T Qp; alternatively certify W_std directly. Empty blocks are omitted. Gram matrices close to I or 2I admit especially easy certified lower bounds using Gershgorin or an infinity-norm deviation bound.

## Required validity checks

1. The projected seed matrices must span all intended symmetric and standard-plus multiplicity spaces. Full column rank alone is not enough if too few columns were selected. Verify exact projector ranks, or exact character-derived dimensions, and positive Gram lower bounds at those dimensions. The S3 intertwiners must satisfy their exact representation relations. With full spanning, every real feasible Schur block has PSD parameter matrices in these nonorthonormal coordinates.
2. Real blocks still cover the unrestricted complex-code problem by averaging a hypothetical feasible solution with its complex conjugate. This uses the reality of all exact constraints.
3. Use original mathematical coefficients, including values numerically smaller than 1e-15. Sparse coefficient dropping may be bounded as an error, but cannot silently become part of the exact certificate.
4. Residuals for symmetric matrix variables must use the full trace pairing. Off-diagonal coefficients in a scalar polynomial count twice in Tr(rX). Computing residual matrices by analytic matrix adjoints, then symmetrizing, avoids a vectorization mismatch.
5. Symmetrize and rationalize each numeric PSD dual, add a rational diagonal lift, then verify PSD by an exact rational LDL decomposition or another exact argument. If an LDL pivot is zero, use a correct semidefinite procedure or increase the lift to positive definiteness; division through zero is invalid.
6. Rational scalar clipping and matrix lifting are harmless only when the resulting exact multipliers, not pre-rounding ones, enter the residual calculation.
7. Every radical/6j/projector entry and every bound must be exact algebraic or enclosed by directed-rounding intervals. Standard floating-point residuals are not rigorous enclosures. The constant also needs a certified lower bound; residual norms and inverse Gram factors need certified upper bounds.
8. A Frobenius bound or maximum absolute row-sum bound on symmetric residual matrices is sufficient in place of an exact operator norm. For interval entries use upper bounds on absolute values. These simpler certified norms may be adequate given a 6.9e-5 candidate margin.
9. The SDP duals on X+epsilon I and on all complement/PPT constraints are valid at epsilon=0. Include every such dual once, with its correct adjoint map. Redundant constraints do not invalidate a certificate.
10. Preserve a reproducible verifier independent of CVXPY and the optimization solver. Its output should provide lower(c), upper(residual budget), the positive difference, and exact PSD/nonnegativity and spanning checks.

The n=19 control is a useful bug detector, but neither its numerical success nor failure replaces the above certificate. No optimization jobs were rerun for this review.
