# Local thermalization controls reversal information without erasing all memory

29 October 2026. Independent physical-source construction for Astra P1.
The root construction owns subsequent process-level consequences.

## 1. The physical information that matters

A known time for forgetting the full hidden state is unnecessary. The useful
physical condition is coercivity only on modes changed by physical reversal.
A thermal bath can supply this on momenta even when positions carry
arbitrarily persistent memory. Every hidden odd variable must be covered by
the declared bath model; coarse records do not certify this completeness.
No calibration or physical operation was performed in this research.

## 2. Exact parity-sector theorem

Let probability measure mu be invariant under an involution Theta, and let
U f=f composed with Theta. Let E be a conservative symmetric Dirichlet form
on L2(mu), invariant under U. Define

    lambda_minus = inf E(u,u)/||u||² over nonzero odd u: Uu=-u.

For h=f², f nonnegative, ||f||=1, its reflected affinity is

    A(h) = integral sqrt(h (h composed with Theta)) dmu = <f,Uf>.

**Theorem.** If lambda_minus>0 then

    2(1-A(h)) = ||f-Uf||² <= 4 E(f,f)/lambda_minus.          (1)

If a physical entropy functional obeys sigma(h)>=4E(sqrt(h),sqrt(h)),

    1-A(h) <= sigma/(2 lambda_minus),
    TV(h mu, (h mu)Theta) <= sqrt(sigma/lambda_minus).       (2)

The TV bound is truncated at one. For 0<=sigma<=2lambda_minus the sharper
bound is TV²<=sigma/lambda_minus-sigma²/(4lambda_minus²).

Proof: split f=f_plus+f_minus with f_plus/minus=(f +/- Uf)/2. The parity
subspaces are orthogonal for the Hilbert norm and for E, so E(f_minus)<=E(f).
Since f-Uf=2f_minus, the spectral definition gives (1). Cauchy--Schwarz
gives TV²<=1-A². No full spectral gap, logarithmic Sobolev inequality,
Dobrushin coefficient, or mixing of reversal-even variables is required.

### Converse and optimal constant

For bounded odd form-domain u, use the positive normalized square root

    f=(1+epsilon u)/sqrt(1+epsilon²||u||²),
    |epsilon| ||u||_infinity < 1.

Conservativity removes the constant from E, and exactly

    ||f-Uf||²/[4E(f,f)] = ||u||²/E(u,u).

Odd truncations approximate the odd-sector infimum by the Dirichlet form's
Markov contraction property. Thus 1/lambda_minus is the best constant,
even when only nonnegative square roots are tested. A uniform finite
constant in (1) for all densities is equivalent to lambda_minus>0.
This is a theorem about a specified form and all densities; it does not
make every density a stationary law of a chosen mechanical source class.

The kernel can contain all functions of position. A momentum bath may have
no mixing of the full state whatsoever and still have a positive odd gap.

## 3. Native underdamped source

Use Boltzmann constant one. Positions q lie on a torus, or in Euclidean
space with sufficient confinement and boundary integrability. Let p be
momentum, mass matrix M positive definite, inverse temperature beta>0,
and symmetric friction Gamma(q). Consider

    dq = M^{-1} p dt,
    dp = F(q) dt - Gamma(q) M^{-1}p dt
                         + sqrt(2 beta^{-1} Gamma(q)) dW.  (3)

F may be unknown and nonconservative, but is momentum independent. All
odd internal variables are p; Theta(q,p)=(q,-p). This version has no fixed
odd external parameters such as magnetic fields. Assume a positive smooth
stationary density rho, finite moments/Fisher integrals and valid
integration by parts. Supply a physically warranted rate

    Gamma(q) >= gamma_star M, gamma_star>0.                (4)

The Maxwell reference is M_beta(p) proportional to
exp[-beta p^T M^{-1}p/2]. With nu(dq)=rho_q(q)dq, set

    f=sqrt[rho/(rho_q M_beta)],
    E(f,f)=beta^{-1} integral (grad_p f)^T Gamma grad_p f
                                      rho_q M_beta dq dp. (5)

Conditional Gaussian Poincare gives lambda_minus>=gamma_star. To see this
directly, whiten momentum and diagonalize M^{-1/2}Gamma(q)M^{-1/2}.
Ornstein--Uhlenbeck eigenvalues are sums of its eigenvalues with Hermite
degrees. Every odd Hermite mode has positive odd total degree and hence
rate at least gamma_star. Integrate over rho_q. No position mixing enters.

### Physical entropy identity

The irreversible momentum current is

    j_irr = -Gamma [M^{-1}p rho + beta^{-1} grad_p rho].

For (3), the stationary entropy flow into the thermal bath is

    sigma = beta E_rho[v^T Gamma v]
                        - E_rho tr(Gamma M^{-1}), v=M^{-1}p. (6)

It equals the relative momentum Fisher information:

    sigma = beta^{-1} integral rho
        [grad_p log(rho/M_beta)]^T Gamma
        [grad_p log(rho/M_beta)] dq dp = 4 E(f,f).          (7)

This is a consequence of the declared reservoir, rather than of fitting a
visible process. Direct verification: stationary Shannon-entropy balance
gives beta^{-1} integral rho (grad log rho)^T Gamma grad log rho
= E tr(Gamma M^{-1}), because streaming (M^{-1}p,F(q)) is divergence
free. Integration by parts gives E[v^T Gamma grad_p log rho]
=-E tr(Gamma M^{-1}). Expansion of the square proves (6)--(7).
Position dependence of Gamma causes no extra momentum derivative.

**Native conclusion:**

    1 - integral sqrt[rho(q,p)rho(q,-p)] dq dp
                                     <= sigma/(2 gamma_star). (8)

This is uniform over position barriers and mixing times. Small ongoing
dissipation cannot maintain large reversal-changing preparation
distinguishability when all odd degrees are directly thermalized at a
fixed rate. It does not put positions near global equilibrium.

For constant force on a torus and scalar damping rate gamma, the stationary
momentum is shifted Maxwellian. If a is the squared mean shift in thermal
units, sigma=gamma a and affinity=exp(-a/2). The bound (8) is therefore
asymptotically sharp as a tends to zero.

## 4. Resources and failures

* The predecessor's orientation lift needs a slowly changing mode that is
  odd under Theta. A fixed positive lambda_minus excludes it. Slow even
  modes do not obstruct (8).
* Full hidden Dobrushin contraction is stronger. Even momentum OU on an
  unbounded space has Dobrushin coefficient one at every finite time:
  arbitrarily separated initial means remain distinguishable. Yet (8)
  holds. A position-preserving bath also has nontrivial invariant classes.
* If some odd variables are unthermostatted, the local form has odd zero
  modes. Hypoellipticity of the full dynamics does not supply a uniform
  gap for this local form. Another coercivity mechanism must be warranted.
* A known mass or a visible relaxation curve does not supply friction for
  all hidden momenta. The completeness of the physical class and the bath
  rate are explicit information resources, not data-acquired conclusions.
* Affinity control does not imply a bound on D(rho||rhoTheta). Smooth
  positive regularizations of one-sided Gaussian-weighted densities can
  have bounded relative Fisher information and divergent reflected KL.
  Such functional examples are not asserted to be stationary laws of (3).
* Symmetrizing stationary fluxes can produce a reversible surrogate with
  velocity-dependent momentum forces and non-Maxwell conditional density.
  That surrogate may preserve noise and kinematics while falling outside
  the same calibrated thermal class. These are distinct closure questions.

## 5. Multiple baths and physical external fields

### Coordinate baths at different temperatures

For diagonal masses and separately thermalized coordinates with
temperatures T_i and damping rates gamma_i>=gamma_star, use the product
centered Gaussian with variances m_i T_i. The current-square identity and
Hermite proof still give (8). With unequal temperatures this product is a
bath reference, not a global equilibrium of a coupled source. Physical
entropy is channel heat divided by its respective temperature.

### Several baths on the same momentum coordinates

Pointwise matrix Cauchy--Schwarz makes channel-resolved entropy dominate
the functional of summed irreversible current and summed diffusion D.
The local centered momentum OU bath has a Gaussian invariant law Mcal
whose covariance solves its Lyapunov equation. For its invariant current
velocity c, div_p(Mcal c)=0. Writing rho=h Mcal gives exactly

    integral rho |c-D grad_p log h|_{D^{-1}}²
       = 4 integral Mcal |grad_p sqrt(h)|_D²
                         + integral rho |c|_{D^{-1}}².

The cross term integrates to zero. A Gaussian Dirichlet form therefore
still lies below physical entropy. Its odd gap is the smallest eigenvalue
of Sigma^{-1/2}D Sigma^{-1/2}, where Sigma is the bath covariance. Uniform
positivity and explicit reservoir channels remain premises. A fitted
effective noise model does not identify those channels or their heat.

### Magnetic field warning with a native exact counterexample

The density-level inequality can survive Lorentz forces because they
are divergence free and do no work. But physical path reversal changes
the magnetic field. A same-field observed arrow is not thermodynamic
entropy production.

For a two-dimensional harmonic equilibrium oscillator, magnetic rotation
rate Omega, damping gamma, and J^T=-J, its Gibbs law has sigma=0. Its
position-lag covariance is

    C(t)= (T/k) I - [T/(2m)] t² I
                    + [T/(6m)] (gamma I-Omega J) t³ + O(t⁴).

Thus C(t) differs from C(t)^T for small positive t when Omega is nonzero,
despite the readout being even and the true heat dissipation being zero.
Field reversal restores the correct reciprocity. It is invalid to use
this fixed-field arrow in a same-generator heat bound.

## 6. Strong existing comparators and actual addition

Entropy-current squares, thermal heat formulas, Gaussian spectral calculus
and the restricted Poincare proof are established ingredients. With
resolved velocities and known friction, (6) already evaluates stationary
heat exactly. Harada--Sasa evaluates heat from sufficiently resolved
velocity correlations and calibrated response. Current underdamped
current/response variational methods can recover entropy under richer
interfaces. None is displaced when its required observations are present.

The proposed addition is the physical-information criterion: only the
reversal-changing sector must be quantitatively thermalized to control
preparation ambiguity. This criterion is exact at the Dirichlet-form
level, and a conventional native thermal model supplies it without global
mixing. A consequential capability must come from a process-level use of
this weaker physical input, not merely from another numerical bound.
Historical priority of the combined statement is not established.
