# Total, classical and thermal-excess displacement conventions

The range cap in QUANTUM_ACOUSTIC_COVERAGE.md is on TOTAL quantum Gibbs position variance, including zero-point motion. Its temperature-independent coverage bound is unchanged. The classical proof in ACOUSTIC_RANGE_THEOREM.md applies to classical Gibbs variance and also follows as a weaker bound for total quantum variance.

An earlier chat shorthand, echoed in a support note, incorrectly suggested that an excess-only quantum cap could simply retain the classical k_B T/omega^2 lower-bound argument. That shorthand is corrected here and in the support note; no governing proof used it.

For a fixed network at the specified T, the mode coefficients are

c_total(omega)=hbar/(2omega)coth[omega/(2theta)],
c_ground(omega)=hbar/(2omega),
c_excess(omega)=c_total-c_ground
              =hbar/[omega(exp(omega/theta)-1)],
theta=k_B T/hbar.

They obey c_total>=k_B T/omega^2, while c_excess<=k_B T/omega^2. Thus an upper bound on quantum thermal excess does not supply the earlier classical covariance lower floor. The ground-state subtraction must use the SAME network, including the same tuning at that T; subtracting the covariance of a different reference network need not leave a positive quadratic form.

A separate valid bound is available. The excess covariance is positive and has decreasing mode coefficient c_excess. If every internal relative EXCESS variance is at most d^2, the same positive quadratic form F in ACOUSTIC_RANGE_THEOREM.md obeys V_F,excess<=12M d^2. The L2/seminorm triangle is valid because the excess covariance is positive. On the soft-mode wave-number set,

V_F,excess>=c_excess(a)/36.

Hence, whenever a<=Omega_aff/4,

a[exp(a/theta)-1]>=hbar/(432M d^2).

If rho_ex solves equality, a>=min{Omega_aff/4,rho_ex}, and the same intrinsic Bose-tail lower-transport bound applies using that cutoff. In dimensionless variables,

u[exp(u)-1]=hbar^2/(432M d^2 k_B T),
u=rho_ex/theta.

This cutoff is DIFFERENT from the total-variance equation rho tanh[rho/(2theta)]=hbar/(864M d^2). It does not give a T-independent coverage floor. No classical or total-quantum conclusion is promoted across these variance definitions.
