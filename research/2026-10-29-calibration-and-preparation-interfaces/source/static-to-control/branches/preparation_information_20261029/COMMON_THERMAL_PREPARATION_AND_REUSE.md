# The ambiguity survives a common thermal preparation

29 October 2026. Root continuation of the native shear construction.
This closes a preparation loophole in an existence/counterexample theorem;
it does not claim an acquired laboratory initialization or free actuation.

## 1. Identical initial source and comparator states

Use the same two-torus, unit masses, friction gamma and temperature tau as
THERMAL_STABILITY_DEPENDS_ON_OBSERVATIONAL_RESOLUTION.md. At time zero,
prepare BOTH the driven source and free comparator in the known free Gibbs law

    mu_0 = uniform_(x,y) tensor N(0,tau)_(v,w).

Activate F_n=(0,a sin(nx)) only in the source. No biased orientation or
source-specific stationary state is needed. Couple the Brownian motions,
the initial momenta and both uniform position phases. Then exactly

    w_n(t)-w_0(t)=Y_n^0(t)
       = integral_0^t exp[-gamma(t-s)] a sin(n x_s) ds,
    y_n(t)-y_0(t)=integral_0^t Y_n^0(s)ds.                 (1)

The x,v driver remains stationary free kinetic motion. Its force correlation
C_n(s) is positive at every lag and is given in the preceding root proof.
The y phase remains uniform independently of the driver at every fixed time.

## 2. Finite-time energy, information and dissipation

Let sigma_n denote the stationary entropy rate calculated there. Positivity
of C_n and inclusion of integration domains imply, for every t>=0,

    E(Y_n^0(t))^2 <= tau sigma_n/gamma.                    (2)

Proof: the double integral for the left side uses past lags in [0,t]^2;
the stationary expression uses [0,infinity)^2 with the same nonnegative
kernel. Likewise

    E[F_n(x_t) w_n(t)]
      = integral_0^t exp(-gamma s) C_n(s)ds <= tau sigma_n.

Therefore the mean applied mechanical work up to h satisfies

    0 <= W_n(h) <= tau h sigma_n.                         (3)

The final physical state is also close to the SAME free Gibbs preparation:

    D(rho_n(h)||mu_0) <= E(Y_n^0(h))^2/(2tau)
                                      <= sigma_n/(2gamma). (4)

To prove (4), condition on the entire driver history. The independent thermal
w component is a Gaussian of variance tau and its shift is Y_n^0(h).
The x,v marginal is the free equilibrium marginal; y is an independent
uniform phase. Augment the comparison by the same hidden driver history,
compare shifted versus unshifted Gaussians, then discard the augmentation.
Joint convexity/data processing gives (4). This is an ordinary preparation
comparison, not a statement that a hidden path was measured.

There is no potential-energy change from the applied position-dependent work
force in this declared model. Its bookkeeping is an external mechanical work
channel acting against a stationary equilibrium bath. With k_B=1, the physical
total entropy production from the equilibrium initial state is

    Sigma_n[0,h] = W_n(h)/tau - D(rho_n(h)||mu_0),
    0 <= Sigma_n[0,h] <= h sigma_n ->0.                   (5)

This is the standard nonequilibrium free-energy balance, not the raw KL of a
stationary path with its naive reversal. It assumes the stated first law,
thermal reservoir and force interpretation. Implementation cost of making
or switching the spatial force field is not included or claimed to vanish.
If the same generator is interpreted as advection by a moving medium, the
physical heat/reversal contract can differ; one must not transfer (5) by
generator resemblance alone.

## 3. The stronger path-model obstruction remains

Uniform position at every time preserves the force/gradient orthogonality.
Against a stationary Gibbs equilibrium model with potential U, the full path
KL over [0,h] is

    D(P_n^mu0 || P_U^nuU)
      = D(mu_0||nu_U)
          + h[ a^2/(8gamma tau)
                       + E_uniform |grad U|^2/(4gamma tau)].

Free equilibrium is the exact minimizer, including the preparation term:

    inf_U D(P_n^mu0 || P_U^nuU) = h a^2/(8gamma tau).      (6)

This is independent of n, while (5) tends to zero. The finite-window TV
separation against a common bounded-force equilibrium class also survives:
the score integral F_n dot (dp+gamma p dt) still has source mean a^2h/2,
equilibrium mean zero and the same second-moment bounds. Hence the earlier
lower bound a^2h/[16((a^2+A^2)h+4gamma tau)] remains valid.

Thus the distinction is not paid for by an unknown stationary preparation,
an initial reversed-state KL boundary, or a hidden weakly thermalized bit.
It lies in the force's growing spatial frequency and the strength of the
observation metric. The source itself is still a mathematical constructed
family with supplied force, bath and complete degrees of freedom.

## 4. Passive recovery of the preparation after the experiment

Turn the applied force off at h and allow the same free thermostat to act
for a further time r. In the above coupling the residual shifted momentum
is exactly exp(-gamma r)Y_n^0(h). The x,v law stays stationary free and the
y phase stays uniform. The same latent Gaussian comparison gives

    D(rho_n(h+r)||mu_0)
                  <= exp(-2gamma r) sigma_n/(2gamma).     (7)

To make this KL at most epsilon_p, the sufficient recovery time is

    r >= max(0, (1/(2gamma)) log[sigma_n/(2gamma epsilon_p)]).

For a required TV tolerance delta_p it is enough to set epsilon_p=2delta_p^2
and apply Pinsker. The force must actually be turned off, the bath model
must cover the declared complete momenta, and the initial free Gibbs preparation
must be warranted. Formula (7) does not provide exact iid fresh runs at finite
r, and accumulated preparation error in repeated use must be budgeted.
An externally assisted preparation can have different costs; none is assumed.

## 5. Consequential prediction and observation budget

Bounds (2) and (1) imply the same position-sup/momentum-L2 coupling bounds as
the stationary construction, with inequality in place of its momentum equality.
Thus the free baseline remains accurate for the declared bounded-sensitivity
consequences, despite the full-path obstruction (6).

For adaptive noisy position measurements the appropriate finite resource is
the sum of squared sensor sensitivity divided by noise variance, together
with the horizon and admitted control gain. A complete chain-rule proof is
preserved in causal_frontier/. Exact differentiation of an unlimited continuous
position path is a different interface and is not supplied by that budget.

No measurement, thermal preparation, force field or reset was physically
acquired here. The theorem removes a loophole from the counterexample by
constructing the full preparation/execution/recovery law, while leaving the
actual hardware, calibration, bandwidth, energy and time of realization explicit.
