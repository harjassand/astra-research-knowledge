# What cannot be acquired from finitely many unstructured local probes

Status: new derived information-access obstruction, independently unreviewed.
It does NOT apply to the declared bounded-degree exact raw program, whose COMPLETE
coefficients are supplied and checked. It prevents interpreting that symbolic
consumer as general empirical microscopic reconstruction.

Suppose an algorithm queries F and any fixed finite number of derivatives at
finitely many configurations (y_i,z_i), adaptively if desired. Begin with an
admitted nominal F0=U(s(y)z), beta>0. Let r bound the derivative order queried and
let

    H(z)=product_i ||z-z_i||^(2r+2).

For no queries use H=1. H is smooth, nonnegative, vanishes to order at least2r+2
at every queried transverse point, and is strictly positive except a finite set.
Its leading homogeneous term is a positive power of||z||, so z.grad H is bounded
below on all R^m. Choose a smooth nonnegative bump b(y) supported in(-1/4,1/4),
with b>=b0>0 on a smaller interval I of positive length. For amplitude A>0 define

    F_A=F0+A b(y)H(z).

All queried values/derivatives through order r agree EXACTLY with F0, including
first-order dilation-defect values if those were queried. For an adaptive finite
transcript, construct H after its queries to F0; F_A gives the identical transcript.
No noisy-data or computational precision issue is needed.

The basins A_left={y<=-1/2} and B_right={y>=1/2} have unchanged unnormalized mass.
The Gibbs integral is finite since F_A>=F0. For a scalar trial changing linearly
only across I, the unnormalized capacity satisfies

    C_F_A <= [1/(beta |I|^2)] integral_I integral_R^m
                      exp(-beta F0) exp(-beta A b(y)H(z)) dz dy.

The last integral tends to0 by dominated convergence: H>0 almost everywhere and
exp(-beta F0) is integrable. Thus k_F_A tends to0, whereas k_F0>0. The upper trial
has no transverse gradient, so this conclusion holds for every fixed finite SPD
transverse mobility, not just a singular limiting diffusion.

## The alternative process is globally legitimate

Choose smooth psi(y)>=0, constant on|y|<=1/3, equal to y^2 outside|y|>=1, with
psi' having the sign of y and |psi'/(2y)| bounded by C_psi. Its second derivative
is bounded. For K=1+C_psi*kappa and any fixed SPD M use
V=1+psi(y)+K z^T M^-1 z. The F0 drift contribution is nonpositive by the same
radial calculation as the nominal Lyapunov proof. The added longitudinal drift
contributes zero, since psi'=0 on the support of b. The added transverse term is
-2K A b(y) z.grad H, bounded above by a finite constant for each fixed A because
z.grad H is bounded below. Diffusion terms are bounded. Therefore LV<=C_A and
V is coercive, proving nonexplosion. The failure does not rely on an invalid SDE,
divergent partition, singular matrix or changed basin definition.

## Consequence for this construction

A finite set of local values/defects, with no global regularity/degree/positivity
control, cannot certify a nonzero multiplicative lower conductance factor. The
robust receiver here pays for the COMPLETE exact bounded-degree rational input,
then derives global univariate inequalities. It reads microscopic coefficients;
it does not identify an unknown physical model from a few measurements. Its
information reduction avoids evaluating the partition, angular distribution,
committor or hidden mobility AFTER structural admission. Different information
interfaces—known degree with interpolation, global derivative bounds, validated
interval oracles—would need their own paid acquisition and receiving argument.
