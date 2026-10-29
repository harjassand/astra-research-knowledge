# Selective kinetic averaging at the scale of rare macroscopic histories

29 October 2026. Root construction, seventh continuation. Earlier files
are unchanged. Feynman--Kac, entropy, weak tilts and exclusion
hydrodynamics are established machinery. Priority of the assembled
physical family and consequence is unresolved.

## 1. Actual family

On an N-site ring, eta_i is 0 or 1, theta_i is one circle coordinate
per bond, and z is arbitrary frozen microscopic information. Write
eta^i for exchange of sites i and i+1. Physical native rates are

    r_i=(s/2)[1+alpha_i(eta,z) cos(theta_i)],
    alpha_i(eta^i,z)=alpha_i(eta,z), |alpha_i|<=a<1, s>0.    (1)

The unknown amplitudes can be N-dependent and nonlocal in the full
configuration. Their mean s is independent of z; it must be supplied
or acquired, not inferred from equilibrium weights. The actual added
operation is independent phase diffusion, leaving eta,z unchanged.
On macroscopic diffusive time,

    L_N=N^2[sum_i r_i Delta_i+kappa_N sum_i partial_i^2].    (2)

Each fixed-z sector is reversible for
mu_N=Ber(1/2)^N times uniform circles. The measure mixes the conserved
particle sectors. The phases have fresh independent driving noises;
z never mixes or resets. Bounded jump intensities and autonomous
circle diffusions give a well-defined process.

Independent actual pi kicks are a second supplier: absorb original
phase offsets into bounded beta_i(eta,z), use native rates
(s/2)(1+beta_i sigma_i), and flip each sign at physical rate gamma_N.
This needs genuine sign-reversal access, not merely diffusion access.

## 2. Finite-N exponential estimate

For deterministic time-dependent v_i(t,eta,z), independent of theta,
put V_N=sum_i v_i cos(theta_i) and A_N^2=sum_i ||v_i||_infinity^2.
Circle integration by parts, for normalized f in the form domain,
gives

    |<V_N,f^2>| <=2 A_N sqrt(D_theta(f)),
    D_theta(f)=sum_i ||partial_i f||_2^2.                   (3)

No configuration derivative of alpha occurs. The native Dirichlet
form is nonnegative. Completing the square and applying the
time-dependent Feynman--Kac energy estimate yields

    log E_mu exp[lambda int_0^tau V_N(t)dt]
      <=lambda^2/(N^2 kappa_N) int_0^tau A_N^2(t)dt.        (4)

Indeed <f,L_N f>+lambda<V_N,f^2> is at most the integrand on
the right. All potentials are bounded at fixed N, so form
approximation justifies the calculation without eta/z regularity.

For independent signs,

    <v_i sigma_i,f^2>
      =(1/2)<v_i sigma_i,(f-f^i)(f+f^i)>

gives sqrt(2) A_N sqrt(D_sign), with
D_sign=(1/2)sum_i E[(f^i-f)^2]. The right side of (4) is then
lambda^2 int A_N^2/(2N^2 gamma_N). Thus all following statements
also hold for gamma_N tending to infinity.

## 3. Macroscopic hidden-current replacement

For a smooth externally prescribed field E, the hidden current drift is

    V_N^E=(s/2)sum_i E(t,i/N)(eta_i-eta_(i+1))
                              alpha_i(eta,z)cos(theta_i). (5)

Here A_N^2<=C_E N, C_E=(s a ||E||_infinity/2)^2. With lambda=bN,

    log E_mu exp[bN int_0^tau V_N^E dt]
       <= b^2 C_E N tau/kappa_N.                          (6)

For every delta>0 and any kappa_N tending to infinity,

    limsup_N (1/N)log P_mu(|int_0^tau V_N^E dt|>delta)
       =-infinity.                                       (7)

First fix b, apply exponential Markov and let N grow. The divided
log bound is -b delta+o(1); then let b grow. There is no required
power-law growth of kappa_N.

The density drift uses E_i=N[G((i+1)/N)-G(i/N)]. Quadratic weak-tilt
compensators have phase coefficients of order 1/N and satisfy the
same replacement, with stronger constants. For fixed fields,
suprema of the integrated residual over t<=tau also satisfy (7):
the residual is deterministically Lipschitz with constant C N;
a grid of O(N/delta) points costs only o(N) in its log probability.
This does not allow arbitrary fields chosen from future observations.

## 4. Arbitrary microscopic initialization without a native hold

Run the actual native-plus-bath process for physical time u/kappa_N,
where u>0 is fixed. Its autonomous phase marginal, conditional on
any old record and frozen z, has density at most K_u^N relative to
uniform phases. K_u is the finite one-circle heat-kernel maximum.
This holds for singular and correlated initial phases.

Each eta's joint density is bounded by that phase marginal; mu_N
assigns eta mass 2^-N. The complete post-warm-up density is therefore
at most (2K_u)^N relative to mu_N. Multiplication by this exponential
factor preserves (7). No exact phase equilibrium or hidden reset is
assumed.

The warm-up takes u/(kappa_N N^2) macroscopic time. A smooth density
test or integrated current changes by at most C/N^2 per swap. Total
native calls in the warm-up are dominated by a Poisson variable of
mean CNu/kappa_N. A fixed macroscopic discrepancy needs order N^2
calls, whose Poisson tail is superexponentially small at speed N.
The integrated drift residual during warm-up is deterministically
O(1/(kappa_N N)).

For the sign-kick supplier, any initial joint law of eta and signs
has density at most 4^N against their uniform product. No initial
sign randomization, forgotten key, continuous-phase warm-up or
native hold is needed. Future kick clocks still need their actual
fresh conditional law.

Conditional on a retained old record, the entire future native-and-bath
generator must remain the declared law, including its native innovations.
Fresh actuator noise alone does not imply that stronger condition.
These assertions concern the actual joint probability law. They do
not promise validity after arbitrary rare future-record conditioning,
or TV equivalence of all microscopic/apparatus histories.

## 5. Weak current tilts: mathematical comparison laws

For a smooth deterministic field E, define comparison rates

    r_i^E=r_i exp(xi_i),
    xi_i=(eta_i-eta_(i+1)) E(t,i/N)/N.                     (8)

No physical implementation of (8) is inferred from the actual menu.
It is a change of measure for proving rare-event properties of the
original process. The phase bath is unchanged. Its likelihood is

    Z_E=exp[sum_(swap times) xi_i
             -int_0^tau N^2 sum_i r_i(e^xi_i-1)dt].        (9)

Finite rates and bounded fields make these true martingales. Exactly,

    Z_E^2=Z_(2E) exp[int N^2 sum_i r_i(e^xi_i-1)^2dt].     (10)

Since |xi_i|<=||E||/N, the integral is at most C_E' N tau.
Thus E Z_E^2<=exp(C_E' N tau) for any common initial law.
Cauchy--Schwarz transfers every speed-N superexponential event to
the weakly tilted comparison law. Tilted stationarity is not needed.

Equivalently, an energy estimate can absorb half the reversible
native Dirichlet form, retaining a C_E' N potential bound. The
second-moment identity is sufficient for the transfers used here.

## 6. Receiving scope

The hidden current and quadratic compensators can be removed at
the exponential scale of rare macroscopic trajectories. Typical-path
hydrodynamics is a weaker consequence. Native uniform ellipticity
r_i>=(s/2)(1-a)>0 supplies the form comparison for conventional
occupation replacement.

A full density/current path LDP additionally needs occupation
replacement, exponential tightness, current-path topology and
lower-bound hydrodynamics under (8). This estimate alone does not
declare those steps complete. Their construction and scope belong
in the receiving action theorem. Fixed-confidence calibration error
also cannot simply be added to exponentially small probabilities.

## Primary context

Kipnis--Olla--Varadhan, Hydrodynamics and large deviation for simple
exclusion processes (1989), DOI 10.1002/cpa.3160420202, supplies
the classical weak-asymmetry framework. Bertini et al., Large
deviations of the empirical current in interacting particle systems,
https://arxiv.org/abs/math/0512394 , supplies the established SSEP
action target. Redig--Saada--Sau, Symmetric simple exclusion process
in dynamic environment: hydrodynamics (2020), DOI 10.1214/20-EJP536,
is a close dynamic-conductance alternative; its self-duality route
does not automatically cover arbitrary configuration-dependent rates.
These methods and the SSEP action are not claimed as inventions.
