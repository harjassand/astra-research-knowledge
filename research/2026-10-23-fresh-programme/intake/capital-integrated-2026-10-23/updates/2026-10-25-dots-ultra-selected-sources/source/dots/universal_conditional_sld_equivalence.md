# Universal conditional Umegaki order equals complete equal-reference SLD order

24 October 2026. Independent verification of the saturated-reference resolvent-filter mechanism in the retained N675 extraction, Section 2, combined with the independently checked SLD reference gauge and SLD-to-BKM integral. This verifies the selected finite-dimensional analytic mechanism only. It does not validate that source's unrelated hardness or compiler claims, and it makes no external priority claim.

## Precise statement

Let P,Q be arbitrary finite-dimensional quantum channels with the same input system, and let c>=0 be finite. The following are equivalent:

(A) For every finite reference and every faithful state pair rho,sigma,

    D(P rho || P sigma)-D(rho_R || sigma_R)
      <= c [D(Q rho || Q sigma)-D(rho_R || sigma_R)].

(B) For every finite reference, faithful baseline sigma, and Hermitian H with H_R=0,

    g^S_(P sigma)(P H) <= c g^S_(Q sigma)(Q H).

Outputs are restricted to their effective support when necessary. The statement extends to boundary pairs whose displayed relative entropies are finite by the usual common faithful regularization.

Taking Q to be the identity proves that the conditional Umegaki contraction coefficient equals the complete equal-reference SLD metric coefficient for every quantum channel. It does NOT identify either with the complete equal-reference Umegaki coefficient.

## Sufficiency: (B) implies (A)

Use the common reference-score gauge H0=H-Omega_sigma(I tensor L_R), where L_R=Omega_(sigma_R)^-1(H_R). It has H0_R=0 and transforms both output conditional SLD deficits exactly to the full SLD quadratic forms of P(H0) and Q(H0). Apply (B). Integrate the untouched-reference-qubit SLD representation of BKM and then the BKM Hessian along the state-pair segment. This proves (A) with the same c.

## Necessity: saturated reference perturbations

Fix sigma,H with H_R=0. Add an auxiliary reference C having a center e0 and N leaves. Choose positive leaf weights lambda_k, a unit leaf-supported vector v, and another leaf-supported vector w. Define

    W=diag(1,lambda_1,...,lambda_N),
    tau=|v><v|,
    L=|e0><w|+|w><e0|,
    Z=Tr W,
    alpha=sigma tensor tau,
    beta(epsilon)=(sigma tensor W+epsilon H tensor L)/Z.

For sufficiently small epsilon of either sign, beta(epsilon) is faithful. Its trace is one because Tr L=0. Its reference marginal is independent of epsilon:

    alpha_RC=sigma_R tensor tau,
    beta(epsilon)_RC=sigma_R tensor W/Z.

At epsilon=0, every output channel has joint relative entropy D(tau||W/Z), equal to the reference relative entropy. Therefore its conditional relative-entropy deficit is exactly zero at the baseline. Auxiliary conjugation diag(-1,1,...,1) sends epsilon to -epsilon while leaving alpha fixed, so each deficit is even.

For a channel T, write A=T(sigma) and K=T(H), and define

    F(t)=w* (W_leaf+tI)^-1 v.

The logarithm resolvent formula yields the exact denominator Hessian

    B_T = d^2/depsilon^2 D(A tensor tau || (A tensor W+epsilon K tensor L)/Z)|_0
        = 2 sum_ij |K_ij|^2 integral_0^infinity |F(t)|^2/(a_j+a_i t) dt,

in an eigenbasis of A. The reference relative entropy has zero derivative of every positive order because its arguments are epsilon-independent. Thus B_T is also the conditional-deficit Hessian.

To check the scaling, before changing variables the ordered (i,j) contribution is

    2 |K_ij|^2 a_i integral_0^infinity
       |F(u/a_i)/a_i|^2/(a_j+u) du.

The substitution u=a_i t gives the displayed B_T without any missing factors. The normalization Z only adds a constant log Z.

Since both conditional baselines vanish, (A) implies B_P<=c B_Q. This is valid for every finite c. One cannot instead differentiate a raw-relative-entropy comparison with arbitrary c at the same construction: its nonzero common baseline would not cancel unless c=1.

## Finite resolvent filters selecting the SLD kernel

For m>=1, use the rational function

    F_m(t)=t^m / product_(j=0)^(2m) [t+1+j/m^3],
    I_m=integral_0^infinity F_m(t)^2 dt.

Its simple poles are distinct and positive, and partial fractions give a finite sum c_j/(t+lambda_j) with rational real coefficients. Such a sum is realized by uniform real v_j=1/sqrt(N) and w_j=sqrt(N)c_j. The coefficients can be large but finite, which only reduces the admissible perturbation epsilon.

Compare f_m(t)=t^m/(1+t)^(2m+1). The elementary product bound is

    exp(-2/m-1/m^2) <= F_m(t)/f_m(t) <= 1.

The normalized f_m^2 density is beta-prime with parameters (2m+1,2m+1), whose mean tends to one and variance tends to zero. The multiplicative comparison gives convergence of normalized F_m^2 to a point mass at one. Hence, for every a,b>0,

    (1/I_m) integral_0^infinity F_m(t)^2/(b+at) dt -> 1/(a+b).

There are only finitely many output eigenvalues, so

    B_T/I_m -> 2 sum_ij |K_ij|^2/(a_i+a_j) = g^S_A(K).

Taking the limit in B_P<=c B_Q proves (B).

The numerator alpha need not remain rank deficient if a formulation insists on faithfulness: replace tau by (1-zeta)tau+zeta I_C/dim C. Baseline saturation remains exact. The Hessian is linear and continuous in that numerator state, so first use the faithful inequality and then let zeta decrease to zero.

## Remaining distinction

In this construction alpha_RC and beta(epsilon)_RC are different: one auxiliary factor is tau and the other W/Z. Although the latter is independent of epsilon, the two reference marginals are not equal. The construction therefore proves a conditional statement, not complete equal-reference Umegaki realization.

For classical transmitted channels, the separate Liouville/vacuum lift repairs this gap and establishes complete Umegaki equality. For arbitrary quantum channels, that repair has not been proved. The universal remaining question is exactly whether complete equal-reference Umegaki order always equals complete equal-reference SLD order.
