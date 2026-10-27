# Uniformly received posterior diffusion with explicit finite null completion

## Why this avoids the posterior-face gap
Use the original eight-helper frontier of law133. In addition to normalization, impose:

1. p0=p1;
2. global F0(p)=sum_i p_i q(Y_i)-q(sum_i p_iY_i)=0;
3. F1(p)=2p4p7-3p5p6-p5p7=0.

The original three-level tree groups leaves(0,1),(2,3),(4,5),(6,7), then the first two and last two pairs. Each sibling pair has a fixed null difference. For the left four-leaf group, its unnormalized conditional q-defect is exactly(p0-p1)(15p2+17p3)/512. For the right group it is -3F1/8. Thus these constraints imply q-balance for both conditional four-leaf groups and for the whole distribution.

For positive masses, the variance identity

    F_parent = F_left+F_right+(w_left*w_right/w_parent)q(m_left-m_right)

then proves that every split between conditional child means in this SAME binary tree is null. Starting at the current mean, the updated tree with branch weights w_child/w_parent therefore gives an explicit three-level null martingale completion to the fixed eight helpers with probabilities p_i. All updated intermediate helpers are convex combinations of those strict-PD endpoints, hence stay strictly inside the physical domain. The original downstream policies at the eight fixed frontier helpers are unchanged. No global posterior revelation to a problematic simplex face is needed.

## Exact diffusion algebra
Let C(p) have rows: normalization gradient, gradient(p0-p1), gradient F0, gradient F1. A fixed four-column pivot is invertible throughout the received probability neighborhood. Set T(p) to the kernel basis with its four free rows equal to I and pivot rows -C_pivot^-1 C_free. Therefore C T=0 exactly.

Let H0=-Y^T JY and H1 be the constant half-Hessian of F1. Put h_a=T^T H_a T, G_ab=Tr(h_a h_b), b_a=Tr h_a, and

    K(p)=I-sum_a (G^-1 b)_a h_a.

Then K is symmetric and Tr(h_a K)=0 identically. The exact interval receiver verifies pivot and Gram inverses uniformly and proves K>=I/16 on ||p-p_original||_infinity<=1/32768. It also proves (YT)(YT)^T>=I/8, so mean covariance (YT)K(YT)^T>=I/128. At the center the rational matrices are included explicitly; their positive lower bounds are checked by exact leading principal minors, not floating eigenvalues.

Define the Itô diffusion dp=T(p)K(p)^(1/2)dW in the probability space, with zero drift, and stop at the first exit from the smaller neighborhood ||p-p_original||_infinity<1/65536. Coefficients are smooth there: all rational denominators are uniformly away from zero and K is uniformly positive definite. Standard local SDE existence/uniqueness applies up to this stopping time. Itô's formula preserves the linear constraints because CT=0, and preserves BOTH nonlinear constraints because the half-Hessian covariance traces vanish exactly. Hence the path remains on the completable constraint manifold. Every probability stays at least half its original positive value.

The mean is a bounded continuous martingale with covariance >=I/128 until stopping. Its quadratic-variation identity implies finite expected stopping time in this compact neighborhood (localize and pass to the bounded stopping limit); the lower covariance bound rules out indefinite residence there. Expected occupation is finite. In the four free coordinates the covariance is K>=I/16, giving a locally elliptic four-dimensional diffusion on the smooth constraint chart. The mean projection has uniformly full rank3, so its interior occupation has a positive AC component, by the local elliptic density and submersion change of variables. No explicit numerical heat-kernel/overlap lower bound is claimed here.

## Exact unchanged terminal law
At the stopped posterior, attach the explicit updated three-level null tree above, then the original downstream policy at each of the eight helpers. Since p is a bounded martingale, optional stopping gives E p_i(stop)=p_i(original). Thus the complete helper and terminal endpoint laws are EXACTLY unchanged, not merely W1-close. The incoming root component probability and outer S3 randomization are retained.

All occupation pieces are positive and J-null: the nondegenerate continuous phase, the updated conditional tree, and the unchanged downstream policies. The previous upper bound discarded the old positive line occupation, so removing that old prefix does not retract credited cancellation. Source, cubic, completion and Gram data stay fixed. This construction closes the global-completion obligation for THIS locally stopped posterior mechanism. It does not prove global revelation of an arbitrary q-balanced posterior, nor does it yet certify a material negative-mass gain; the current center's scalar field is positive, so a useful overlap test must use a suitable negative-bulk subtree or a larger received region.
