# Independent audit: positive unfiltered reference-filter score

**PASS — 26 October 2026.** Governing note: `qutrit_reset_unfiltered_reference_score_positive_theorem.md`, with the coordinate-score spectral-floor, own-zero and companion-zero receivers. This is an unfiltered tangent theorem, not finite noisy-direction filter order.

## Actual score, covariance, and floor reduction

The previously received source-block formula has the correct input/reference/WH coefficients. Differentiating reference congruence yields the displayed Hermitian Q. At a singular source, congruence preserves the ranks of source, reference and output, so the derivative uses the continuous XlogX expression rather than an unavailable support-opening logarithm.

Matched physical/reference unitary covariance diagonalizes A without changing the maximally entangled seed. Matched diagonal phase invariance makes Q diagonal in that basis. Thus strict positivity of all coordinate scores implies Tr(PQ)>0 for every nonzero PSD P, including perturbations not commuting with A.

Adding a scalar reset floor b translates the coordinate integral and leaves the factor t-b. Its first and second derivatives are exactly those stated. At b>0 they are locally dominated and convergent. The boundary score is continuous by the finite-dimensional XlogX expression. Before the kernel's sole upward crossing the score is concave; at and beyond the crossing it is strictly positive from the tail integral. The chord bound therefore receives all faithful scores from their singular boundary scores, including strictness when that boundary is the pure zero-reset point. This is a second-derivative/chord reduction, not generic reset monotonicity.

## Own-zero boundary

The exact central entropy entries give `kappa+g3(b,c)-g2(2b)-g2(2c)` with the stated half-output scaling constants. Their individual convergent resolvent expressions use h_s. Its scalar concavity gap J is increasing in each variable; `v/(2-v)<=v<=1` and the analogous w inequalities yield the stated pointwise compensation. With finite nonzero noise at least one inequality is strict for every s>0. The pure endpoint has exact zero score. This analytical proof suffices without the optional positive-polynomial corroboration.

## Companion-zero boundary and exact certificate

For a,b>0 the actual kernel is negative near zero and positive at s=1. Its acquired zero geometry gives a unique theta in (0,1). The rescaled crossing equation has positive leading and linear coefficients and one positive root v. Both rational root bounds follow from the exact substitutions in the certificate.

The fresh self-contained SymPy script was rerun. It reacquires the actual source ratio, baseline integral zero, crossing quadratic, derivative numerator and pseudo-remainder. The degree-seven to degree-two pseudo-division uses the positive factor A^6; therefore it preserves the relevant sign on the crossing variety. Its remainder is `(z-1)^2 T`, linear in v. Bounding positive-v monomials at the lower root bound and negative-v monomials at the upper bound is legitimate coefficientwise on u,w,z>=0. The resulting lower polynomial has exactly 4066 strictly positive coefficients. The surviving monomial `45097156608*u*z^6` proves strictness for actual u>0,z>0, including possible w=0 limits.

The ratio singularity at z=1 is removable because the actual numerator kernel has a simple crossing. Away from one its derivative is strictly positive; its continuous extension is therefore strictly increasing. It has finite large-z limit, and the source and pure baseline integrals converge. Subtracting R(1) times the zero-integral baseline gives a strictly positive score. This is a genuine signed-integral compensation, not a sign inference from a single crossing alone. The remaining a=0 and b=0 endpoints use the separately received own-zero and equal-companion axis cases.

## Conclusion and scope

For every nonzero A>=0 and d>0, Q is positive definite. For A=0 it is zero. Homogeneity correctly gives TrQ=D(X), but no finite noisy-filter iteration follows: after such a filter the seed need not remain maximally entangled. The result does not establish finite anchored order, accepted-only GLS monotonicity, or arbitrary filtered-source score positivity.
