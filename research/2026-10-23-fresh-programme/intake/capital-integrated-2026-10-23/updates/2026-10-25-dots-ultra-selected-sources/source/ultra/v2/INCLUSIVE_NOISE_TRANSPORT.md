# Inclusive heat response of a bounded nonlinear mechanical contact

25 October 2026. This is the owned derivation following FIRST_CONSTRUCTION.md.
The earlier conditional support calculations remain unchanged. The result
below closes the inelastic-current and finite-common-mass gates under an
explicit equilibrium scattering contract. It does not yet identify a full
continuous double-well Hamiltonian with the Toulouse scaling model.

## 1. Physical contract and observable

Two identical, lossless, semi-infinite scalar leads have impedance Z>0 at
their ACTUAL terminal planes. Each endpoint has mass M/2, M>0. The only
interaction between endpoints is a time-independent stable potential V(Y),
where Y=u_R-u_L; it need not be harmonic or weak. There is no ground, hidden
heat port, drive or velocity-dependent interaction. Lead thermal fields are
Gaussian. The common displacement U=(u_L+u_R)/2 and the relative coordinate
have kinetic energy

    T = M Udot^2/2 + (M/4) Ydot^2/2.

The lead dissipation is 2Z Udot^2+(Z/2)Ydot^2. Thus the bare relative mass is
B=M/4 and its Ohmic friction is Z/2. These are derived from the two terminal
coordinates, not parameters inferred from a two-state truncation.

The theorem concerns the stationary LINEAR heat conductance about a common
temperature T>0, theta=k_B T/hbar. Take the steady-state limit first. Assume
an equilibrium KMS scattering state with canonical incoming/outgoing fields
and no nonmixing bound modes retaining an initial population. Equivalently
one may take a regulated thermal scattering limit in which the identities
below hold. Absolute common position has no Gibbs state on the infinite
line; use the translation quotient for positions and the asymptotic field
algebra for flux. No absolute-position variance is used. These are actual
assumptions, not a proof of asymptotic completeness for every nonlinear V.

Let chi_Y(omega) be the FULL bath-dressed equilibrium retarded response to a
force coupled as -F Y, with time dependence exp(-i omega t). Its imaginary
part is nonnegative for omega>0. The measured total connected variance is
Var_T(Y), including zero point motion.

## 2. Exact mechanical parity mapping

Use a_e=(a_L+a_R)/sqrt(2), a_o=(a_R-a_L)/sqrt(2), and the same convention for
outgoing fields b. The corresponding terminal coordinates are q_e=sqrt(2)U
and q_o=Y/sqrt(2). For either parity terminal the exact lead force is
2Z v_in-Z qdot, while v_out=qdot-v_in. The even terminal is a free mass
M/2, hence

    S_e(omega) = (2Z+i M omega)/(2Z-i M omega),  |S_e|=1.

For the odd coordinate the driving force conjugate to Y is
sqrt(2)Z v_in,o. Taking the coherent response in the full interacting system
therefore gives

    S_o(omega) = -1-i omega Z chi_Y(omega).                  (1)

For nonlinear V this is a coherent small-signal amplitude. It is NOT the
whole one-phonon probability, and |t_elastic|^2 is not the inclusive heat
transmission. All internal and frequency-changing processes are retained in
the response and output field used next.

## 3. Quantum covariance insertion and inclusive current

Normalize fields so <a_alpha^dagger(omega)a_beta(omega')> equals
2pi delta(omega-omega') N_alpha,beta. The parity input covariance of two
independent physical thermal leads is

    N = [[n,c],[c,n]],  n=(n_L+n_R)/2,  c=(n_R-n_L)/2.

For a symmetric infinitesimal bias about T, n=n_T+O(Delta T^2). Only c
changes to first order. Thus the marginal state of each parity bath, and in
particular that of the nonlinear odd subsystem, has no first-order change.

Here is the quantum step explicitly. Regularize by frequency bins and let
A=a_o, E=a_e, B_out=b_o in one bin of frequency omega, with equilibrium
occupation n>0. The Gaussian input density matrix obeys

    partial_c rho|_0 = rho_0(E^dagger A+A^dagger E)/[n(n+1)].

The even mode is dynamically independent of the complete odd output. Its
thermal contraction therefore gives

    partial_c <E^dagger B_out>|_0 = <A^dagger B_out>_eq/n.

Incoming A and outgoing B_out are frequency-omega annihilation operators for
the same equilibrium Hamiltonian. KMS implies

    <B_out A^dagger> = exp(hbar omega/k_B T)<A^dagger B_out>.

Consequently <[B_out,A^dagger]>=<A^dagger B_out>/n. Displacing the input
coherently changes <B_out> by this commutator times the input amplitude;
this is exactly S_o from (1). The anomalous response has the opposite
frequency and vanishes in a stationary frequency-preserving linear response.
Taking the bin limit yields

    delta< b_e^dagger b_o > = S_e^* S_o delta c.

The odd-only output occupation, INCLUDING all inelastic redistribution, has
zero first-order change: tracing the cross insertion over the independent
even channel gives zero. The same holds for the even-only occupation.
Transforming back to physical outputs then gives

    I_L = (hbar/2pi) int_0^infinity omega [n_L-n_R]
                       T_eff(omega) d omega + o(Delta T),
    T_eff = [1-Re(S_e^* S_o)]/2.                             (2)

This is an inclusive linear-response identity. Inelastic energy is not
discarded; its directed first-order effect is the equilibrium input/output
cross correlator. At finite bias the marginal odd state changes and (2) is
not asserted. For a harmonic V both parity amplitudes have unit modulus,
and (2) reduces to |(S_e-S_o)/2|^2, the ordinary full transmission.

## 4. Contractivity and a UNIFORM finite-mass error

KMS and outgoing CCR give <B_out^dagger B_out>=n, just as for A. Cauchy--
Schwarz now yields |<A^dagger B_out>|<=n. Thus

    |S_o|<=1,  0<=T_eff<=1.                                  (3)

This does not assume that nonlinear coherent scattering is unitary. It uses
unitarity/canonical normalization of the COMPLETE asymptotic output.
Combining (1) and (3) also imposes the useful optical disk constraint

    chi_Y''(omega) >= (Z omega/2)|chi_Y(omega)|^2.             (4)

Arbitrary positive spectral measures need not satisfy (4). In particular an
undamped isolated TLS line is not the full response of this coupled port.

Define g_theta(omega)=[x/sinh x]^2, x=omega/(2theta),

    J = int g_theta T_eff d omega,  K = k_B J/(2pi),
    J_Q = int g_theta d omega = pi^2 theta/3,
    J_0 = int g_theta [1-Re S_o]/2 d omega.

Since |S_e-1|<=M omega/Z, (3) gives, uniformly over retuned nonlinear V,

    |J-J_0|/J_Q <= c_M M theta/Z,
    c_M = 9 zeta(3)/pi^2 = 1.0961444541... .                  (5)

Indeed the pointwise kernel error is <=M omega/(2Z) and
int omega g_theta d omega=6 zeta(3)theta^2. No pointwise smallness of chi,
no real-part bound, and no exchange of a retuned susceptibility limit with
an uncontrolled integral is needed. The finite common mass is therefore
harmless for the LEADING cold fraction when M theta/Z->0. It is retained
exactly by (2) at other temperatures.

## 5. Total equilibrium motion and sharp spectral cost

Equation (1) gives the exact auxiliary loss

    J_Q-J_0 = (Z/2) int omega g_theta chi_Y'' d omega.          (6)

The equilibrium fluctuation--dissipation theorem gives

    Var_T(Y) >= (hbar/pi) int coth(omega/(2theta)) chi_Y''
                                            d omega.         (7)

Equality holds for a mixing confined coordinate without a separate static
zero-frequency covariance. A conserved zero-frequency covariance is an
additional nonnegative contribution and does not weaken the bounds below.

Let u_*>0 solve u_* coth u_*=3 and set

    kappa = (3/(4pi)) max_(u>0) u^3/sinh u
          = 0.6434518924787489... .

The maximum follows by one derivative; u coth u increases from 1 to infinity.
Comparing the two positive weights in (6)--(7) gives

    delta_0=(J_Q-J_0)/J_Q <= kappa (Z/hbar) Var_T(Y).

For the ACTUAL deficit delta=(J_Q-J)/J_Q, (5) therefore proves

    Var_T(Y) >= (hbar/(kappa Z))
                    [delta-c_M M theta/Z]_+ .                (8)

The coefficient 1/kappa=1.5541177385... is sharp only over unrestricted
positive spectral measures, which is a RELAXATION of the physical class
because of (4), sum rules and microscopic realization constraints. It is
not claimed to be an attained mechanical optimum. Its consequence is that
the inclusive equilibrium identities alone impose a constant motion floor,
rather than the stronger logarithm proved for positive harmonic networks.

There is still a compliance cost. If the retarded static susceptibility is
C=(2/pi)int chi_Y''/omega, then

    delta_0 <= (3 psi_*/pi) Z C theta,
    psi_* = max_(x>0) x^4/sinh^2 x = 1.2202580156... .         (9)

Thus a fixed cold deficit requires C of order at least 1/theta, even when
motion need not grow by this spectral argument. For the FULL canonical
coordinate, the double-commutator sum rule is

    int omega chi_Y'' d omega = pi/(2B)=2pi/M.                (10)

A TLS low line with fixed dipole and frequency O(theta) carries only
O(theta) of this moment. A physical double well must retain high intrawell
transitions; (10) is not supplied by a standalone spin Hilbert space.

## 6. A finite-window equilibrium-noise operation

Let S_Y(omega) be the symmetrized connected displacement spectrum with
Var=(1/pi)int_0^infinity S_Y d omega. Away from a static atom,
S_Y=hbar coth(omega/(2theta))chi_Y''. Put

    W_theta(omega)=omega g_theta tanh(omega/(2theta))
                 =theta w(omega/theta),
    w(z)=z^3/(2sinh z).

Then (6) is exactly

    delta_0 = Z/(2hbar J_Q) int W_theta S_Y d omega.           (11)

This specifies what an equilibrium displacement-noise measurement must
acquire to infer inclusive heat loss, rather than using periodic band counts
or an elastic probability. Suppose a measured spectrum S_hat on [l,h] has
certified integrated absolute error E, and total Var<=d_max^2 is known.
Its inferred value delta_hat obeys the explicit certificate

    |delta-delta_hat| <= c_M M theta/Z
       + Z/(2hbar J_Q) [ E sup_[l,h] W_theta
                        +pi d_max^2 sup_outside[l,h] W_theta ]. (12)

This follows by positivity and contains all unmeasured spectral weight.
It is an acquisition specification, not a measurement performed here. A
window [epsilon theta,R theta] gives temperature-independent relative-tail
control as epsilon->0 and R->infinity. Resolving a fixed fraction of that
thermal window requires observation time at least of order 1/theta, with
additional sampling/error costs dependent on the actual sensor and noise.
Neither a free spectral oracle nor free analytic continuation is assumed.

## 7. Conventional explanation and the remaining actual operation

The inclusive equilibrium-response kernel is close conventional ancestry:
Yamamoto, Glazman & Houzet, arXiv:2403.13552, Eqs. (2)--(8), derive it for
one active Josephson series channel including inelastic outputs. Yeyati et
al., arXiv:2403.13526v2, Eqs. (17)--(20), retain a matrix-Keldysh inelastic
term at finite bias. Our mechanical mapping, the KMS derivation, and the
uniform finite-M correction specify the present contract; this is not a
claim to invent the nonlinear current/admittance relation.

Primary links:
https://arxiv.org/html/2403.13552
https://arxiv.org/html/2403.13526

The strongest candidate bounded-coordinate operation is conventional
dissipative tunnelling. The exact Toulouse spin-boson scaling model supplies
a finite positive deficit with Var(Y)=d^2, but identifying that model with a
continuous massive port requires a controlled projection, bath cutoff,
physical splitting retuning, and all high-frequency transitions. A hard-wall
bounded-coordinate family can bound total range exactly, but does not by
itself prove its low-energy response. Those gates remain open here. No
material, hardware, novelty or nonzero heat-suppression claim for such a
microscopic family follows just from (1)--(12).
