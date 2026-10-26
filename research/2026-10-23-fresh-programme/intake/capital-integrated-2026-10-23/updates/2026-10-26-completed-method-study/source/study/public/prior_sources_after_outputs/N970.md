# Binary classical inputs: no quantum-reference advantage in global relative order

24 October 2026. Parent's SLD-superoperator argument independently checked. Historical novelty has not been established. The conclusion optimizes over all priors; it is not a fixed-input-prior assertion.

Let K be any finite-output stochastic channel with input alphabet {0,1}. Write k_y0=K(y|0), k_y1=K(y|1), delta_y=k_y0-k_y1. Then its ordinary classical Umegaki contraction coefficient, complete equal-reference Umegaki coefficient, and conditional Umegaki coefficient with arbitrary finite quantum references all equal

    sup_(0<t<1) t(1-t) sum_y delta_y^2/[k_y1+delta_y t].

Endpoint limits are included through the supremum. Delete identically zero output rows. A constant channel has coefficient zero.

## Positive-superoperator reduction

Take arbitrary faithful cq baseline blocks sigma0,sigma1 on a finite quantum reference and an equal-reference tangent with blocks H,-H. On the real Hilbert space of Hermitian reference matrices, let

    A=Omega_(sigma0), B=Omega_(sigma1), T=A+B,
    S=T^-1/2 A T^-1/2,  h=T^-1/2 H,

where Omega_sigma(X)=(sigma X+X sigma)/2. These are positive definite self-adjoint superoperators, with 0<S<I. This is a congruence and coordinate change for the SLD quadratic form. It is not a physical reference filter and makes no BKM-whitening claim.

Input SLD metric is exactly

    <h,[S^-1+(I-S)^-1]h>.

Output y has tangent delta_y H and covariance

    Omega_(sigma_y)=k_y0 A+k_y1 B
       =T^1/2[k_y1 I+delta_y S]T^1/2.

Consequently the total output metric is

    <h,[sum_y delta_y^2 (k_y1 I+delta_y S)^-1]h>.

All middle operators are scalar functions of the SAME self-adjoint contraction S. Spectral calculus bounds their ratio by the supremum of the scalar ratio on (0,1), namely the displayed formula. No operator commutativity of sigma0 and sigma1 was assumed.

Conversely choose a one-dimensional reference, sigma0=t, sigma1=1-t, and a nonzero scalar H. This realizes the scalar ratio for every t. Thus the complete equal-reference SLD coefficient is exactly the ordinary scalar supremum. The universal conditional-Umegaki-to-complete-SLD bound gives the upper bound for the conditional coefficient. Ordinary classical infinitesimal pairs give the reverse lower bound, and complete equal-reference pairs lie between ordinary and conditional classes.

## Two arbitrary binary-input channels

For another channel L with the same binary input, define

    F_K(t)=sum_y [K(y|0)-K(y|1)]^2/
                    [K(y|1)+(K(y|0)-K(y|1))t],

and F_L similarly. A uniform complete SLD inequality for the channel pair is equivalent to

    F_K(t)<=c F_L(t) for every 0<t<1.

The same single-S superoperator reduction proves sufficiency, and scalar reference states prove necessity. Classical Hessian integration and infinitesimal pairs identify this with the ordinary classical relative-entropy comparison. The all-classical Liouville theorem, or its conditional-SLD upper direction combined with scalar lower bounds, gives the identical complete and conditional comparisons with arbitrary quantum references.

If L is nonconstant, F_L(t)>0 throughout (0,1). If L is constant and K nonconstant, no finite upper relative constant exists. If both are constant, both sides vanish and impose no restriction. Writing inequalities rather than ratios handles all degeneracies.

## Scope

The result covers arbitrary numbers of output symbols and arbitrary quantum-reference dimensions, but the transmitted input alphabet has exactly two symbols. Together with the known ternary quantum-reference construction, it identifies three input symbols as the smallest cardinality at which the global classical-channel reference advantage can occur.

For a prescribed input prior, the spectrum of S need not equal that prior. Thus the proof must not be promoted to a fixed-prior no-advantage theorem. It also does not cover generic quantum-input channels merely because their Hilbert-space dimension is two.
