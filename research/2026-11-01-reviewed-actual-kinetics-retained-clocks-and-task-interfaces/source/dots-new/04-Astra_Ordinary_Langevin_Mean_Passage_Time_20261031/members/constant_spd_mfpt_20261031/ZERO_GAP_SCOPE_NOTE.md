# Why a spectral-gap number is not merely missing here

Separate exact observation; not a new numerical certificate. With fixed finite
alpha and kappa, q(y)=v(y)^(-alpha) is comparable to |y|^(-4alpha) in either tail.
Let psi be a nonzero smooth function supported in(1,2), and h_R(y,z)=psi(-y/R).
For large R this is supported inside A and has zero trace on the target B.
Its full-state norm and Dirichlet energy, after the same normalized conditional
fiber integration, obey

    ||h_R||^2 ~ R^(1-4alpha),
    E(h_R) ~ beta^-1 R^(-1-4alpha).

The constants are positive and independent of R; the fiber gradient is zero for
any constant SPD transverse matrix. Thus the Rayleigh quotient tends to zero
like R^-2, proving that the target-killed operator has spectral bottom zero.
For the full invariant measure, alpha>1/4 also implies
(mean h_R)^2/||h_R||^2=O(R^(1-4alpha))->0, so the global Poincare gap is zero too.

The finite mean proved in the main construction is therefore source-specific
inverse-generator information in a setting with no bounded global inverse.
This does not contradict the gap-based primary bounds: their positive-gap
premise is absent. It also does not prove any new assertion about medians,
exponential moments, arbitrary-point means or finite-bit initialization.
