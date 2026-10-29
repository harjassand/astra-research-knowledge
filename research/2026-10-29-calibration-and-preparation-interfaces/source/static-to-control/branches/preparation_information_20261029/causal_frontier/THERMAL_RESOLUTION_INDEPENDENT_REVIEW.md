# Independent review: native thermal separation, preparation, and resolution

29 October 2026. Reviewer: producer-workspace/causal_information_frontier.
Reviewed ../THERMAL_STABILITY_DEPENDS_ON_OBSERVATIONAL_RESOLUTION.md,
especially Sections 4--6. The additional common-Maxwell-preparation argument
was independently checked from the root's explicit construction message.
This is a mathematical review, not a physical experiment or implementation.

## Conclusion

The finite-window TV separation, reversal-even witness, native-free coupling,
and stated finite-gain feedback extension are correct. The common Maxwell
initial preparation strengthens the result as claimed: it removes a stationary
preparation discrepancy and gives vanishing finite-window total physical
entropy production while retaining the fixed-resolution-free path separation.
The specific thermostat, force, initial-law and observation contracts remain
essential.

The root's adaptive Gaussian POSITION sensor bound is also correct using a
common-history latent-driver likelihood construction. I extended this to
causal convolution/momentum readouts, point-sampled velocities, continuous
Gaussian meters, and record-driven additive controls in
FINITE_RESOLUTION_TRANSCRIPT_THEOREMS.md. These are full transcript-TV
statements, not merely bounds for individual Lipschitz expectations.

Two scope cautions are substantive:

1. For adaptively chosen momentum sampling times, E[Y(tau)^2] need not equal
   the deterministic-time stationary variance. The extension uses a valid
   supremum bound instead. The O(n) precision-count obstruction proved for
   position sensors must not automatically be transferred to arbitrary
   adaptively timed point-velocity probes.
2. The simple linear-in-N bin-mismatch bound is valid for passive fixed-time
   binning. Adaptive quantizer settings/times or quantized feedback can
   condition the initially uniform phase; the same linear formula is then
   unproved. A finite decision-tree bound is supplied separately.

## 1. Full path TV witness

For S=integral F_n(q) dot (dp+gamma p dt), the stochastic integrand F_n(q)
is finite variation because q has differentiable paths, for every fixed n.
Thus Ito and Stratonovich versions coincide. Under the source,
E[S]=a^2 h/2. Under every stationary Gibbs alternative H=-grad U,

    E_U[S]=h int F_n dot H nu_q
           =h tau int F_n dot grad nu_q=0.

Periodic integration by parts and div F_n=0 justify this uniformly over U;
uniform spatial density is not being assumed for the equilibrium alternative.

The root's moment bounds follow from (A+B)^2<=2A^2+2B^2 and Ito isometry.
For arbitrary laws P,Q and a common real statistic S,

    |E_P S-E_Q S|^2 <= 2 TV(P,Q)(E_P S^2+E_Q S^2)

follows by Cauchy--Schwarz against P+Q, or a maximal coupling. Substitution
gives exactly

    TV >= a^2 h/[16((a^2+A^2)h+4 gamma tau)].

The numerical specialization a=A=gamma=tau=h=1 is 1/96. No samples or
simulation are needed for this constant.

## 2. Reversal-even witness

For the actual reversal q_t->q_(h-t), p_t->-p_(h-t), the path functional
S_even=integral F_n(q_t) dot dp_t is invariant. Its Stratonovich form makes
the time change immediate, and its Ito form is identical because the
quadratic covariation is zero. Under Gibbs equilibrium its mean vanishes:
the force term vanishes by divergence-free integration, and the friction
term by conditional Maxwell momentum symmetry.

Under the stationary source,

    E[S_even]=a^2 h/2-gamma tau sigma_n h.

For explicit uniformly bounded moments, using (A+B+C)^2<=3(A^2+B^2+C^2),
one may take

    E_n S_even^2 <= 6a^4 h^2+3 gamma^2 a^2 tau h^2
                          +6 gamma tau a^2 h,
    E_U S_even^2 <= 3a^2 A^2 h^2+3 gamma^2 a^2 tau h^2
                          +6 gamma tau a^2 h.

Here E_n w^2<=tau+a^2/gamma^2 and E_U w^2=tau. Thus the asymptotic nonzero
gap gives a genuine finite-window TV separation also through a time-even
statistic. The force-gradient sensitivity of this statistic grows with n;
the result does not give a fixed-bandwidth experiment for free.

## 3. Native free equilibrium coupling and feedback

The free comparator has the correct uniform-position Maxwell initial law:
the initial y phase is uniform independently of the entire common driver,
and the OU velocity zeta is independent of x,v. In the stationary source
w=zeta+Y. The same initial y phase then gives the exact lifted differences
delta w=Y and delta y(t)=int_0^t Y(s)ds. Stationarity and the ordinary
differential equation Y'=F_n-gamma Y give

    E[Y^2]=E[F_n Y]/gamma=tau sigma_n/gamma=:V_n.

The two coupling bounds in root (16) follow directly by Cauchy--Schwarz.
They concern a position supremum metric and momentum L2 metric; they do
not imply full path TV convergence.

For root Section 6, define delta w=Y+z. Initial z=delta y=0 is correct even
though delta w(0)=Y(0). Subtracting the two controlled equations yields
the displayed deterministic difference equations. The derivative bound
for |delta y|+|z| is conservative but valid when u is uniformly K-Lipschitz
in (y,w). Gronwall gives the stated C_h and both bounds in (18).
The comparison is the free BASELINE model run under the same controller;
it is not asserted to stay at equilibrium during actuation. Actuation on
x/v is excluded and can change the conclusion.

## 4. Same Maxwell preparation: independently checked strengthening

Start both sources from the SAME uniform-position Maxwell law mu_0, with
independent stationary OU x/v driver and independent w OU. Define

    Y^0_n(t)=int_0^t exp[-gamma(t-s)] F_n(x_s) ds.

The force covariance C_F(s) from root (3) is pointwise nonnegative. The
variance of Y^0 is the double integral of that covariance over [0,t]^2,
with positive exponential weights. Extending the domain to [0,infinity)^2
therefore gives E[(Y^0_n(t))^2]<=V_n. All coupling bounds remain valid with
Y^0, including initial delta w=0. Uniform initial y phase preserves uniform
position marginals at all times. Thus E S_n=a^2h/2 and the separation in
Section 1 remain unchanged.

Expected work on the declared particle is

    W_h = int_0^h E[F_n(x_t)Y^0_n(t)]dt
        <= h int_0^infinity exp(-gamma s) C_F(s)ds
        = tau h sigma_n.                                  (R2)

For the final distribution, condition on the full x/v driver. The w
coordinate is Gaussian of variance tau shifted by Y^0_n(h); y remains
uniform independently of all drivers. Comparing these conditional Gaussian
laws and then discarding the latent driver gives

    D(rho_h||mu_0) <= E[(Y^0_n(h))^2]/(2tau)
                    <= sigma_n/(2gamma).                  (R3)

The declared kinetic energy and bath bookkeeping give exactly

    Sigma_[0,h] = W_h/tau - D(rho_h||mu_0),
    0 <= Sigma_[0,h] <= h sigma_n.                         (R4)

This is finite-window total physical entropy production for the specified
Langevin system, bath and force work, not an assertion that the transient
instantaneous rate equals the stationary sigma_n. Preparation of the
initial Maxwell state is an explicit shared mathematical input, not an
operation acquired by this calculation. Apparatus construction or spatial
force-field generation costs are not supplied by the particle/bath model.

The force-to-free path KL remains exactly h a^2/(8 gamma tau), since the
initial laws coincide and Girsanov integrates E|F_n|^2=a^2/2. Thus the
strengthening is substantive: a stationary parity-boundary discrepancy
is not responsible for the separation.

## 5. Gaussian position sensors and ordinary bins

For root's adaptive Gaussian position sensors, place the common baseline
driver xi on an augmented probability space and compare, at the SAME
realized transcript history, the source and free conditional Gaussian
means. Query times and settings are functions of that history. The KL
chain rule then adds squared mean differences divided by twice the same
noise variance. Since every mean map is L_i-Lipschitz in position and
sum L_i^2/eta_i^2<=J holds for every history,

    D(transcript_n||transcript_0) <= J h^2 V_n/2.

Both augmented laws have the same xi marginal. Conditional counterfactual
states must be rebuilt under the common history; simply coupling two
independently evolved feedback records would not justify the calculation.
The stated construction does this correctly. Pinsker gives TV<=h sqrt(JV_n)/2.

For passive fixed sampling times and K equal bins of the y circle, the
common initial y phase is uniform independently of the coupled displacement.
The mismatch probability at time t_i is at most K E|delta y(t_i)|/(2pi).
A union bound gives the root's K/(2pi) sum_i t_i sqrt(V_n). The x bin is
identical under the coupling. Adaptive binning needs the separate treatment
in FINITE_RESOLUTION_TRANSCRIPT_THEOREMS.md.
