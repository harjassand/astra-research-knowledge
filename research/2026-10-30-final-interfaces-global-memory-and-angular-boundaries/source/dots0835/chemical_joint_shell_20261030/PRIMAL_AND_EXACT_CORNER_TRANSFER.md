# Primal certificates and an actual nonlocal corner transfer operator

Status: personally derived; child adversarial check passed (see INDEPENDENT_HALF_FACTORIAL_HALO_AUDIT.md), not a global recurrence review. No global feedback contraction is asserted.

## Primal bulk companion
For the same alpha as the fractional-factorial bulk theorem, put

    V(x)=product_i(x_i!)^alpha.

The exact forward ratio V(x+nu)/V(x), multiplied by k(x)_y, equals the same ideal mixed-power expression k a_y^(1−alpha)a_y'^alpha up to relative O(1/min x). Therefore the finite killed-generator inequality proves

    LV/V≤−c sum_y(x)_y

in the same classwise high-count bulk region. This supplies an earned Foster function there, not merely a summable adjoint measure.

## Primal finite-phase companion
In UNIVERSAL_HALF_FACTORIAL_PHASE_EXTENSION.md take the RIGHT inverse

    u(r)=(−G(r))^−1 1>0,
    V(r,j)=Gamma(r+1)^alpha u_j(r).

Its univariate rational-Puiseux shift ratios are1+O(1/r), and the fixed positive inflation2^|delta| absorbs forward as well as backward shifts. Thus LV≤−Gamma(r+1)^alpha outside a finite set. Multiplying by any fixed power r^s preserves an eventual version of the inequality after reserving a second fixed inflation factor, since its shift ratios are again1+O(1/r). No phase-width-dependent reduction of alpha is required.

## Exact physical corner exit kernel
Construct the finite WR halo for a finite corner J as in FINITE_HALO_EXACT_CORNER_INTERFACE.md. The physical and halo processes agree UNTIL the first exit tau from J, not just in their frozen generators. On each halo communicating class that intersects the complement of J, tau has finite expectation from every state because the halo chain is positively recurrent by the earned finite-phase theorem. Classes wholly contained in J are already solved closed physical classes and are separated from the transfer construction.

Define the ACTUAL exit kernel

    K_J(x,y)=P_x[X(tau)=y], y outside J.

No coordinate is frozen along this excursion; all count changes, phase changes and their stochastic dependence are retained.

On a nontrivial halo component, let V be the primal finite-phase certificate. On an all-delta-zero component exiting J, use instead the exact killed-phase right-resolvent construction: prescribe exterior V=Gamma(r+1)^alpha and solve Q_I u=−1−Q_(I,out)1, then set V_I=Gamma(r+1)^alpha u. This gives exact negative drift in J because r is conserved. Closed finite physical classes and absorbing phases are separated as in the repaired halo note. In either case, its positive drift is supported in a finite set F. By the strong Markov property at the first visit to F, expected time spent in F before tau is bounded uniformly over starting states by a finite constant (take the maximum expected exit time over F in the relevant class). Stopped Dynkin, localization, and Fatou therefore give

    sum_y K_J(x,y)V(y) ≤ V(x)+C,
    E_x[tau]≤C'(V(x)+1).

The constants come from a proved recurrent auxiliary finite-phase system, not an assumed recurrence of the full physical network. They can be very large; no uniformity over widening J is asserted.

Hence for any explicit nonnegative boundary datum g(y)≤cV(y), the Dirichlet extension

    H_g(x)=E_x[g(X(tau))]

is finite, nonnegative, and solves the actual killed-corner harmonic equation LH_g=0 in J, with the prescribed boundary values. Adding a nonnegative running cost bounded by the earned drift integrand gives the corresponding finite Poisson extension. Polynomially modified factorial boundary data can be admitted by the preceding multiplier observation, or by choosing a slightly larger exponent still below1/2.

This is a genuine joint, nonlocal corner transfer mechanism. It does not assume instantaneous equilibration or replace the exit law by a frozen stationary average.

## Remaining receiving obligation
Extending an outer bulk/joint-shell function harmonically into the corner can increase its values at states reached by jumps from the outer region. Those return values feed back into the outer generator. The bound above does NOT prove that this feedback is dominated by the outer negative margin, and it does not claim a global Lyapunov function. That is the remaining contraction/matching problem.
