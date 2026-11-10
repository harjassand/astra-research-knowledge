Common target steering with a growing Fourier force catalogue, and the unclosed fixed-actuator interface
ROOT mathematical preparation, 10 November 2026. Analytic construction; no PDE simulation, oracle, or new compute job. Elementary consequences are not asserted historically novel.

1. Starting operation and quantifiers.
Use the completed twelve-fundamental-force erasure theorem: for every rational M>=1, nu,tau in(0,1],epsilon in(0,1), a predetermined rational piecewise-cubic force steers EVERY mean-zero divergence-free H1 initial state of norm<=M and EVERY sufficiently small L-infinity-time L2 disturbance, for EVERY Leray-Hopf realization, to small TOTAL L2 velocity. All compiler, bit and physical resources are polynomial with fixed computable constants. The accepted finite saturation depth in that result is a constant for one fixed enlarged carrier list. This note does not reprove it.

Let a second input be a finite real mean-zero divergence-free rational trigonometric polynomial V on the unit3-torus, encoded by integer wavevectors and rational sine/cosine polarization vectors. Promise ||V||H1<=M. The COMPLETE input length includes the entire list, all integer coordinates, coefficients and scalar parameters; it is not the numerical maximum wavevector. Duplicate modes can be canonicalized by exact rational arithmetic.

Claim at this scope: if the physical spatial forcing catalogue may grow to all divergence-free modes of radius O(M/epsilon), the erasure theorem gives a total deterministic POLYNOMIAL common compiler steering all admitted unknown inputs to within epsilon of V. This does not yet use only the twelve fundamental forcing fields.

2. Paid target truncation and reference norms.
Choose N=ceil(16M/epsilon) and let V_N retain only wavevectors |k|<=N. The H1 promise and Parseval give
 ||V-V_N||2<=M/(2pi N)<=epsilon/8.
This discards very large binary-encoded frequencies without iterating up to them. Scan the input list and compare integer squared lengths to N^2. The retained number of distinct frequencies is O(N^3).

Fourier Cauchy--Schwarz on the unit torus gives, for fixed universal computable C,
 ||V_N||infinity<=C M N^(1/2),
 ||grad V_N||infinity<=C M N^(3/2),
 ||V_N||W2,infinity<=C M N^(5/2),
 ||Delta V_N||2<=C M N.
For rational parameter choices it is harmless to replace half powers by the next integer powers. All these bounds use only the promised M and N, not a norm oracle.

Choose an integer Q>=4/tau+4 C M N^2+4 and sigma=1/Q. Then sigma<=tau/4 and sigma ||grad V_N||infinity<=1/4 after fixing C sufficiently large. Put a=tau-sigma. Let b=0 before a and b(t)=((t-a)/sigma)V_N on[a,tau]. This is a prescribed continuous reference, with no impulse at a.

On the last interval its exact full-mode body force is
 F=b_t-nu Delta b+B(b,b), B(u,v)=P[(u.grad)v].
It has time degree<=2 and frequencies<=2N. W1,infinity bounds follow from the displayed Fourier estimates: a conservative polynomial is C[M N^2/sigma+nu M N^4+M^2 N^5]. Computing B uses at most O(N^6) rational Fourier interactions, each with rational Leray projector and powers of2pi. This is a polynomial algorithm in complete input length and R=2+M+nu^-1+tau^-1+epsilon^-1.

3. Unknown-input/reference stability without an exponential-in-R radius.
On[0,tau/2], use the twelve-mode erasure compiler with accuracy epsilon/32. Set its force to zero until a. Choose the final allowed disturbance tolerance
 eta=min(eta_erasure,epsilon/64).
The energy inequality gives ||U(a)||2<=epsilon/32+epsilon/64, using the specified one-sided trace. This is uniform over all weak realizations and disturbances.

On[a,tau], round the full-mode F to a rational coefficient force f with ||f-F||L-infinity L2<=epsilon/64. For v=U-b, the relative-energy inequality against the smooth prescribed reference is
 (1/2)d||v||2^2/dt+nu||grad v||2^2
 <=||grad b||infinity||v||2^2+||h+f-F||2||v||2.
The self-advection of v and transport by divergence-free b are skew in this energy. This inequality is valid for every Leray-Hopf realization; a global strong solution in this last interval is not assumed. Standard regularization of the norm at zero gives
 ||v(tau)||2
 <=exp(int_a^tau||grad b||infinity)[||U(a)||2+int_a^tau||h+f-F||2]
 <=2[epsilon/32+epsilon/64+2epsilon/64]=10epsilon/64.
Consequently ||U(tau)-V||2<=18epsilon/64=9epsilon/32<epsilon.
The factor2 is fixed because the target interval was shortened by its explicitly bounded strain, rather than allowing a stability factor exp(poly(R)). At fixed endpoints use the one-sided energy trace; approximation by admissible starting times justifies the concatenation.

4. Rational/physical costs.
All wavevectors are integers; polarizations and Fourier Leray matrices are rational. Only the fixed constants2pi and(2pi)^2 need certified enclosures. Set a per-coefficient absolute rounding budget <=epsilon/(C N^3) to bound the full L2 residual by epsilon/64. Exact elementary rational arithmetic and certified pi approximation use polynomial bits and operations. Coefficients of F have time degree<=2; the earlier erasure force has degree<=3. The concatenated catalogue has O(N^3) spatial directions, all frequencies<=2N, interval count inherited polynomially from erasure, polynomial physical W1,infinity peak/integral norms and eta^-1. High-frequency input denominators affect bit lengths, not physical amplitudes after truncation.

This is a constructive full-mode common-target bridge, not an answer for a fixed twelve-field catalogue, strong trajectory tracking or exact controllability.

5. Why the new finite-depth lowering does not already close variable targets.
The completed twelve-mode proof has H_0=K rho^160, H_j=K H_(j-1)^32 and
 H_D=K^((32^(D+1)-1)/31)rho^(160*32^D).
For a FIXED carrier list D,K are genuine constants; p=256*32^(D+1) is therefore legitimate there. When the target Fourier radius grows, that conclusion cannot be made with constants depending on its generated table. An interaction of modes of radius<=K creates at most radius2K. Thus any quadratic-generation construction starting at unit modes needs depth at least log_2 N to reach radius N (up to fixed initial radii). The displayed hierarchy then gives an exponent growing at least like N^5, before any growth of support-dependent K is paid. This is a limitation of that compiler, not a lower bound for all twelve-field controls.

The genuine remaining operation is efficient physical synthesis for a VARIABLE Fourier catalogue while preserving common unknown-input stability and actual force resources. It may require a different representation or generation mechanism. It cannot be replaced by declaring qualitative saturation polynomial, or by applying a fixed-target theorem nonuniformly.

Primary bindings: Nersesyan arXiv:1403.5369v2, Theorem2.5/proof, Theorem4.1, Proposition4.3, and(4.14)--(4.15), https://arxiv.org/pdf/1403.5369v2 . They provide qualitative finite-mode/known-trajectory control and exact finite Fourier saturation, not uniform polynomial common-unknown-H1/all-weak costs. The earlier enlarged-family and new twelve-mode constructions are retained at their actual scopes. No source recovery or implementation experiment is involved.
