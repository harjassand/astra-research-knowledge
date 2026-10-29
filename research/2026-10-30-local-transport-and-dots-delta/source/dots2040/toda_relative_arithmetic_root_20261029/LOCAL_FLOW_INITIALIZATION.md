# Local continuous-flow initialization on the unchanged spectral curve

2026-10-29. Root working derivation, submitted for review. This closes neither the full arithmetic implementation nor any novelty claim. It uses the classical local Abel inversion followed by doubling strategy, credited in `latent_integrable_geometry/LAX_DECODER_FRONTIER.md` to Couveignes–Edixhoven and Mascot.

## The missing interface

Numerically advancing the physical Toda variables and recomputing a spectral curve is not an acceptable shortcut: rounding changes conserved spectral data, and long-time phase errors then grow. Instead initialize on the original exact rational reduced spectral curve throughout.

Let theta0 be the initial physical degree-g divisor, A the Abel map in the unnormalized monomial differential basis, and v=(0,...,0,-2) the reduced Toda translation velocity. The closed-gap cancellation and velocity are separately checked in the governing notes. For g=0 the physical isospectral set is a singleton and no integration is needed.

Use the existing uniform estimates ||J^-1||<=K, ||D²A||<=L_H on a complex angle ball of radius rho. Define

    r = min(rho/2, 1/(4 K L_H)), eta = r/(2K).

For real tau with 2|tau| <= eta/4, seek h in the r-ball satisfying

    A(theta0+h)-A(theta0) = tau v.

Writing R(h)=A(theta0+h)-A(theta0)-J h, the map

    Phi(h)=J^-1[tau v-R(h)]

has derivative norm <=K L_H r<=1/4. Moreover ||Phi(0)||<=K eta/4=r/8. It maps the r-ball strictly inside itself. Starting h0=0, exact iteration converges geometrically to a real h*. The resulting curve points define D(tau) on the ORIGINAL spectral curve. Realness follows because all local coefficients and the target are real and the contraction is unique. There is no supplied global period matrix, no long-time ODE solver, and no favorable pivot promise.

## Quantitative evaluation rather than an integral oracle

Each component of the Abel displacement is a sum over gaps of one-dimensional integrals

    integral_0^{h_j} -mu_j(theta0_j+s)^(k-1) / sqrt(-F_excluded,j(mu_j(theta0_j+s))) ds.

Within |s|<=rho, the excluded factors stay at least Delta/2 from zero. Each integrand is holomorphic with an explicit bound U_J whose logarithm is polynomial in g, log M, log(1/Delta). On |h_j|<=rho/2, the Taylor series about zero has a geometrically decaying integrated tail: truncation degree q gives error <=2 rho U_J 2^(-q) per entry. Thus q=O(p+log g+log(rho U_J+1)) terms suffice for p output bits. Powers, sine/cosine series and the square-root recurrence compute these coefficients with polynomially many operations. The square-root initial denominator is bounded below by (Delta/2)^g, so working precision is polynomially larger than p and the input size. Square roots and initial sine/cosine need not be represented in their composite algebraic number field: certified rational intervals for each value suffice.

J can be inverted with rational interval elimination or an approximate rational inverse plus a residual test. ||J^-1||<=K charges conditioning; it does not assume an individual fixed pivot is large. One concrete route is rounded J, exact rational matrix inversion, and the Neumann bound ||J^-1 (J-Jhat)||<=1/2, obtained by entrywise precision below 1/(2gK). This ensures Jhat is nonsingular, bounds its inverse, and controls multiplication errors.

An inexact contraction with per-iteration Euclidean error <=zeta obeys

    ||h_l-h*|| <= (1/4)^l ||h*|| + (4/3) zeta.

Choose l=O(p+log(r+1)), zeta<=min(2^(-p-3),r/8). The exact map sends the r-ball into the 3r/8-ball, so the inexact iteration stays inside the r/2-ball; the precision floor log(1/r) is charged even when requested p is modest. Every evaluation therefore uses polynomial bit work in g, input coefficient size and p. Evaluation of the elementary functions above must use certified series/interval algorithms, not floating quadrature alone. This note gives the reduction and explicit convergence bounds, not a certified implementation receipt.

## Binary time scaling and error budget

For rational target time T choose an integer m>=0 such that tau=T/2^m satisfies 2|tau|<=eta/4. Then

    m = O(log(2+|T|)+log(1/eta)).

Given the existing physical conditioning bounds, log(1/eta) is polynomial in the rational input size. Initialize D(tau), then apply the relative operation E~2D-D0 m times, always keeping D0 and the curve fixed. This is time doubling because A(D(tau))-A(D0)=tau v; divisor doubling without this initialization is not.

Let kappa_dec bound conversion from sufficiently small direct Abel error to the requested physical output error, including the inverse-spectral decoder. Set per-call direct error

    delta <= epsilon / [4 kappa_dec 2^m].

Let J_forward be an explicit upper bound on the complex Abel derivative norm in the collar, for example g (2M)^g (2/Delta)^g. Obtain angle error <=delta/(2 max(1,J_forward)) by adding log2(max(1,J_forward)) to the initializer precision; charge rounding of the initial divisor and final initialization coordinates separately within delta. Thus initialize with direct error <=delta. The recurrence e_(j+1)<=2 e_j+delta yields e_m<2^(m+1) delta<=epsilon/(2 kappa_dec). Remaining rounding receives the other half of the budget. Precision p=O(m+log(1/epsilon)+log kappa_dec) suffices before the separately charged O(g)-exponent residual-to-zero conversion in each arithmetic call. No g^m precision growth follows from this direct-error invariant.

## Scope and stopping boundary

This is a quantitative composition of established inverse-spectral and Jacobian methods. It would yield a useful end-to-end polynomial-bit theorem only after the all-input relative-arithmetic proof and certified implementation interfaces are complete. It supplies no advantage over a conventional algorithm allowed the same exact equations, exact initial data, spectral geometry and methods. Exact hidden-Toda recognition is separately matched by a linear self-adjoint polar-kernel comparator.

The computation does not acquire exact physical initial conditions. A measured model/state with uncertainty in frequencies can have phase uncertainty of order |T| times that uncertainty. Logarithmic runtime dependence on |T| for an exact mathematical instance is not logarithmic experimental acquisition cost, robustness to unknown perturbations, or a general fast-forwarding principle.

## Review correction, 19:25 UTC

Independent audit identified and repaired two omissions: inexact contraction tolerance must also be below r/8, and angle accuracy must be converted to direct Abel accuracy using the forward derivative bound. Neither changes polynomial bit complexity. See the separate review note for its precise scope.
