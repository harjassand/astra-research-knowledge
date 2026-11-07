# Nonlinear closure: exact operations and the remaining gate

These are final constructive attacks, not a complete finite-N prediction theorem. Discrete primitives, Fourier regularization and nongradient fluctuation corrections have established predecessors; no historical novelty is asserted.

## Exact primitive without a Taylor remainder

For a length-L block with endpoint bits a,b and core count k, define F_L(s)=sum_(j=1)^s D(j/L). Counts in the overlapping length-(L-1) windows are m_x=k+a and m_(x+1)=k+b. Exactly,

    D((k+a+b)/L)(b-a)=F_L(m_(x+1))-F_L(m_x).

If a=b both sides vanish; otherwise a+b=1 and the single summand between neighboring counts is D((k+1)/L). Spatial summation by parts is therefore exact. The normalized F_L/(L-1) approximates the constitutive primitive with a paid Riemann/coefficient modulus error. No unknown D' is needed for this operation. It does not replace a nonlinear microscopic window-density function by its macroscopic counterpart.

## Rough-height obstruction

The constructor independently found this exact failure of the unregularized energy shortcut. On an N-ring, p=N^(-1)sum eta_i, take mean-zero H with H_(i+1)-H_i=(eta_i-p)/N and current j_i=eta_i-eta_(i+1). Then

    sum_i H_(i+1)j_i
       =sum_i(H_(i+1)-H_i)eta_i=p(1-p).

Under Bernoulli(rho), its expectation is rho(1-rho)(1-1/N). An internally invariant block coefficient times its endpoint difference instead has conditional mean zero. Replacing the former by the latter without a compensator is false, even for SSEP with zero constitutive residual. This is the order-one current/noise cancellation in the rough height energy. It does not refute the separately proved same-expression invariant-weight pressure bound.

## Explicit smoothing repair

Use piecewise-constant lattice density eta_N in [0,1] on the unit torus, and retain 0<|k|<=M in its H^(-1) error energy against a prescribed u in [0,1]. A single exchange changes the k-th Fourier coefficient by at most 2pi|k|/N^2; the cell-integration factor can only lower it. Its jump-quadratic energy is therefore <=2M/N^4. At diffusive speed N^2 and rates <=lambda per bond, the full Itô term is <=2lambda M/N. The discarded energy is deterministically <=||eta_N-u||_2^2/[4pi^2(M+1)^2]<=1/[4pi^2(M+1)^2]. Thus smoothing removes the specific order-one rough-height obstruction.

Finite Fourier height kernels have computable spatial derivative bounds, with a loose choice C_M=10pi(M+1)^3. Their own-block oscillation is O(C_M L^2/N^2), so the pressure approximation costs O(T C_M L B/N). For a smooth coefficient, centered spatial block averaging cancels the first moment and costs O(lambda C_M L^2/N) after summing rates. These quantities vanish for fixed M,L before N grows.

## What is still unproved

The exact primitive leaves a nonlinear small-window density function. Smoothing controls observable martingale and block-oscillation costs. Neither controls its difference from the same nonlinear function of the macroscopic density. The local-equilibrium/one- or two-block replacement, corrector time-boundary terms, nonlinear stability and compatible growing-scale choices still require a complete proof. An alternative is to compute conditional state-weighted means and prove their cancellation with the corrector/noise energy. Neither full operation is completed here. Finite-N service and arbitrary-force driving remain OPEN.
