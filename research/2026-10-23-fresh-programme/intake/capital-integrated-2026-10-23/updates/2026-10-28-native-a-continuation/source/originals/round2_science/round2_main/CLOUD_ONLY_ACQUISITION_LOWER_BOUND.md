# A quantitative obstruction to cloud-only hidden-center acquisition

27 October 2026. This concerns an intermediate oracle, NOT the original
N687 value-query problem. It rules out a tempting universal replacement for
source-preserving gauges and identifies information a richer representation
must retain.

## Contract and theorem

A fixed, possibly completely known conservative scalar source g is available
through unlimited values. An unknown center theta enters only through at
most n independent samples N(theta,tau^2). Auxiliary randomness, adaptive
computation and evaluations of this fixed g are unrestricted. The output
must approximate N(E g(theta+rG),S^2) uniformly over theta. No retained data
with additional theta information are supplied.

Let 0<kappa=Lr/S<=1. There is a globally L-Lipschitz C-infinity conservative
source for which uniform TV error epsilon<=kappa/32 requires

    n >= tau^2 / [2 r^2 log(12/kappa)].                 (1)

This counts Gaussian center observations even when g is known completely.
It does not lower-bound original g-value calls in N687.

Choose g(x)=Lr cos(x/r), potential F(x)=Lr^2 sin(x/r). Then

    m(theta)=Lr exp(-1/2) cos(theta/r).

For n Gaussian center observations their sample mean N(theta,tau^2/n) is
sufficient: the residual observations are independent of both it and theta.
Every allowed algorithm is therefore a positive Markov kernel from this
mean. Pad a bounded adaptive stopping rule to n observations.
The n=0 case is impossible separately: a theta-independent output has zero
nonconstant Fourier coefficients, violating (2) at the requested accuracy.

For a kernel receiving N(theta,eta^2), uniform TV epsilon from
N(a cos(theta/r),S^2) implies the bounded-characteristic-test inequality

    exp(-1/2)|J_1(a/S)|
       <= exp(-eta^2/(2r^2))+2epsilon.                 (2)

This follows by taking long-interval Fourier coefficients at frequency 1/r
of the output characteristic function at argument 1/S. The conditional
characteristic function has modulus at most one. Gaussian convolution
attenuates its coefficient by exp(-eta^2/(2r^2)); translating the averaging
interval leaves a boundary term tending to zero. Uniform TV changes the
coefficient by at most 2epsilon. No periodicity of the kernel, output-tail
assumption, or finite-moment certification is used. The companion
round2_positive/GAUSSIAN_SHIFT_REUSE_OBSTRUCTION.md gives the full argument.

Here a/S=kappa exp(-1/2)<=1. The alternating Bessel series gives
J_1(z)>=z/2-z^3/16>=7z/16 on [0,1]. Thus the left side of (2) is at least
(7/(16e))kappa>7kappa/48. With 2epsilon<=kappa/16,

    exp[-tau^2/(2nr^2)] >= kappa/12.

Taking logarithms proves (1).

## Consequence for the proposed mechanism

For the ideal Gaussian target, its maximum local Fisher information divided
by the information in one center observation is tau^2 L^2/(e S^2) for this
cosine source. The generic Lipschitz upper scale is
tau^2 L^2/S^2=(tau^2/r^2)kappa^2. This local comparison is weaker than the
uniform nonlinear acquisition bound by order 1/[kappa^2 log(1/kappa)].
It is not a separate approximate-TV theorem.

For L=S=tau=1 and r=kappa, error kappa/32 requires
n >= 1/[2kappa^2 log(12/kappa)], although the Fisher scale is one. Thus a
universal small-amplitude nonlinear mean channel cannot obtain small relative
law error from a fixed noisy center using only polylogarithmically many
independent repeats as kappa tends to zero.

This does not contradict the affine value-only channel, whose mean is
affine. It does not contradict R16, which pays for center precision and
retains source-query transformations. It does not apply to N687 at a
supplied fixed center, or to an algorithm retaining additional source-coupled
data about its center. Fixed-g values cannot add theta information here;
in the original problem source values and intermediate centers can be tied.

The next representation should consequently preserve the query-visible
Gaussian program and its constructed reserve, rather than discard everything
except a Gaussian sample labeled by an unknown mean. The joint-absorption
and normal-form theorems construct those properties. The remaining task is
a nonlinear law correction exploiting this retained information with the
required dimension and total-cost bounds.

## Executed certification

check_cloud_only_bound.py verifies integer observation-count obstructions
at dyadic kappa. Decisive comparisons use rational exponential enclosures.
The bounded-test proof supplies the law inequality; no scalar calibration,
source-query experiment, empirical moments, or fitted model are used.
