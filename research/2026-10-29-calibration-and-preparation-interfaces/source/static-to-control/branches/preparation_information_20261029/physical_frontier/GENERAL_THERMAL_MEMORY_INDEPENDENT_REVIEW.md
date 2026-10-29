# Independent review of the general thermal memory record

29 October 2026. Reviewed root's GENERAL_THERMAL_MEMORY_METRICS.md through
its acquisition, costs, common-preparation correction and thermodynamic
scope. Read-version SHA256:

    0d452d6a839b7609341ee73e825f550d95ac8ce2a1e7bd133a3d1f98727a8121

Also read causal_frontier/FINITE_RESOLUTION_TRANSCRIPT_THEOREMS.md to
check the new use of its variance-based consequences. This is an ordinary
internal proof review, not an external validation or a native acquisition.

## 1. Verdict

The exact heat form, selfadjoint positive compressed resolvent, native
equilibrium projection, finite-window Pythagorean identity, Gaussian
preparation bound, paired acquisition, simultaneous matrix confidence,
and corrected common-preparation factors check under the declared source
and observation contract. No substantive gap was found in those claims.
The strongest additional preparation consequence is proved in Section 6
below: the same acquired heat record controls the time needed to prepare
the coupled stationary law from the common independent thermal state.

The physical gates remain genuine inputs. In particular, the source uses
a one-way applied work force, independent receiver noise, a fixed bath,
an equilibrium autonomous driver, and actual independent preparations.
The record cannot establish these premises by fitting itself.

## 2. Exact native projection and initial preparation

The driver marginal is its original Gibbs law, while an independent
uniform receiver phase makes the position marginal nu(X) times uniform y.
For any comparison potential V=U+R, the squared Girsanov drift discrepancy
is the root's equation (5). Its only cross term integrates to zero in y:

    integral f(X) partial_y R(X,y) dy = 0.

The remaining driver and receiver gradient terms are nonnegative, and
the potential U(X) with a free receiver attains equality. The comparison
allows arbitrary smooth periodic coupling potentials V on the same
coordinates; it does not silently allow altered baths, new coordinates,
velocity forces, odd external fields or latent states.

The finite-window Pythagorean statement is stronger than the rate result
and is correct. At initial time,

    log(mu_0/mu_V)=R(X,y)/tau+constant

depends only on positions. Source and mu_0 have identical position
marginals, so

    D(rho_f||mu_V)=D(rho_f||mu_0)+D(mu_0||mu_V).

At positive times the same position-marginal identity makes the gradient
cost under the driven stationary source equal to its cost under mu_0.
Combining both identities proves the full path-KL Pythagorean equation.

For the preparation bound, condition on the entire driver history. The
receiver momentum is N(Y_f(0),tau), whereas the reference is N(0,tau).
The underlying history law is identical in the augmented comparison.
Gaussian KL is Y_f(0)^2/(2tau); discard the driver history except its
current state, and use the independent uniform receiver phase. Thus

    D(rho_f||mu_0)<=E Y_f^2/(2tau)=sigma/(2gamma).

Y_f is generally correlated with the current driver state. The proof
correctly avoids asserting independence. The rate and full-path costs
are information-theoretic explanation costs, not another heat definition.

## 3. Operator and finite-family qualifications

For position features, actual physical equilibrium gives
L*=Theta L Theta and Theta phi_i=phi_i. Hence the compressed resolvent is
selfadjoint. Its positivity follows from dissipativity of L, and strict
positivity holds for every nonzero L2 feature because the resolvent is
injective. These facts do not supply a uniform lower spectral bound.

For a closed force space S, the intended operator in the criterion is
the quadratic-form compression P_S H_gamma P_S; invariance of S under
H_gamma is unnecessary. The operator-level criterion is meaningful on
L2. Physical applications should continue to use admissible bounded
forces, or separately justify any unbounded force extension. The finite
bounded-feature family in the acquisition theorem has no such issue.

Linear independence in L2(nu) gives G,H positive definite. A finite
confidence certificate can establish a quantitative positive margin.
It cannot establish an exact nullspace from small noisy eigenvalues.
The root explicitly retains this distinction and the conditioning cost.

## 4. Acquisition and confidence audit

For S sampled independently from Exp(gamma),

    E[sym(phi_0 phi_S^T)/gamma]
      =integral_0^infinity exp(-gamma t) C(t)dt=H.

The initial outer product has expectation G. Every trial requires two
time points from one actual evolving preparation; replacing the second
with an identical frozen sample would change H. Actual independence is
needed across trials, not across feature entries within a trial.

With censoring at T_c, the estimate targets H^(T_c). The omitted tail can
have either sign because kinetic equilibrium correlations can oscillate.
The root's operator-norm bias bound therefore has the correct two-sided
use. In particular H^(T_c) need not be positive semidefinite.

There are r(r+1) upper-triangular entry types across both symmetric
matrices. Each G entry lies in an interval of length at most 2B_iB_j;
each censored H entry lies in one of length at most 2B_iB_j/gamma.
Bounded Hoeffding plus a union bound gives equation (12) with
log[2r(r+1)/delta], including correlated within-trial entries.

If |E_ij|<=a B_iB_j, then for every vector z,

    |z^T E z|<=a (sum B_i|z_i|)^2
                  <=a (sum B_i^2)||z||².

This proves the root's spectral error conversion. Adding the censored
tail and warranted deterministic calibration errors gives valid eta_G
and eta_H. The lower/upper Loewner bounds then imply H>=kappa_cert G.
The same event is uniform over all coefficients alpha, including those
selected after reading the calibration record.

This does not cover selecting alpha from the current unreset driver
history: that conditions the service preparation. Nor does selecting the
feature basis after seeing the same data inherit the finite predeclared
family's confidence guarantee without a further uniform/held-out analysis.

The declared lag clock is exact and independent. A finite-resolution
implementation must also charge its timing error. Small timing error
alone does not uniformly control arbitrary bounded discontinuous feature
correlations. A calibrated correlation-continuity bound or a feature
regularity argument can supply the error; the ideal protocol does not
make instrument timing precision free. Likewise the receiver gamma and
temperature calibration are inputs to the formulas.

Reuse is across the stated alpha family for the fixed driver and receiver
gamma. Changing the driver, temperature or receiver relaxation kernel
changes H and does not inherit reuse merely from retaining the same G.

## 5. Common thermal preparation and transcript transfer

The correction is necessary and sufficient for the stated second-moment
bounds. In general C_f(t) can be negative, so monotonicity of filtered
variance cannot be assumed. The exact identity

    Y_f^0(t)=Y_f(t)-exp(-gamma t)Y_f(0)

and Cauchy--Schwarz give

    E(Y_f^0(t))² <= (1+exp(-gamma t))²V <=4V,
    V=tau sigma/gamma.

The receiver energy equation then yields

    W(h)=gamma integral_0^h E(Y_f^0(t))²dt
                                      +E(Y_f^0(h))²/2
         <=tau sigma(4h+2/gamma).

Initial mu_0 is the Gibbs state of the original driver plus free receiver.
Its finite-time Gibbs relative entropy obeys
D(rho_f(h)||mu_0)<=E(Y_f^0(h))²/(2tau)<=2sigma/gamma.
Since delta S=delta E/tau-D(rho_f(h)||mu_0), total physical entropy is
W/tau-D, as stated. The displayed work bound is for the force f itself;
additional feedback actuation in a separate experiment has its own work.

The transcript proofs read from causal_frontier depend on: a common
driver law; identical source/free conditional sensor histories; the
receiver difference being the same filtered force; variance control;
and specified sensor/actuator contracts. They do not otherwise require
the free spatial driver or a sine. Thus their extension is valid with V
for stationary use and 4V for the common thermal preparation. For their
adaptive point-momentum bound, replace the sine amplitude a by the actual
bound A_f=||f||_infinity: |Y|<=A_f/gamma and |Y'|<=2A_f still hold.

Any state-feedback extension must retain its stated uniform Lipschitz
and actuator assumptions. The work bound above must not be transferred
to arbitrary added feedback commands. Full hidden dynamics is not
discarded: the comparison retains the same autonomous driver.

## 6. Additional constructive preparation theorem

The same record also supplies a preparation-time bound for the coupled
stationary law. It removes a need to supply an entire stationary forcing
history, while retaining the genuine independent thermal-driver gate.

**Preparation.** Start the driver in its actual equilibrium law, the
receiver momentum in an independent N(0,tau), and its circle coordinate
in an independent uniform phase. Apply the fixed force f for time b.
Let rho_f^warm(b) be the resulting full state law, and let rho_f^stat be
the stationary coupled law.

For the same two-sided stationary driver history, the warm forcing shift
at time b is

    Y_f^0(b)=Y_f(b)-exp(-gamma b)Y_f(0).

In an augmented comparison conditioned on that history, both receiver
momenta have variance tau and their conditional means differ by
exp(-gamma b)Y_f(0). The driver-history law is identical. Therefore
Gaussian KL and marginalization give BOTH directions:

    D(rho_f^warm(b)||rho_f^stat)
       <= exp(-2gamma b) sigma[f]/(2gamma),               (P1)
    D(rho_f^stat||rho_f^warm(b))
       <= exp(-2gamma b) sigma[f]/(2gamma).               (P2)

The independent uniform receiver phase is needed for the full state-law
claim. The source can be constructed from the finite forward history
[0,b]; no past-history oracle is used in execution. The two-sided history
is only a proof coupling.

For any subsequent finite horizon with the same source dynamics, initial
data processing gives the same KL bound on future path laws. Hence

    TV(future_warm,future_stationary)
                    <=exp(-gamma b) sqrt[sigma/(4gamma)]. (P3)

This controls every bounded future path decision under the declared
source. It does not control an unbounded lifetime mean without additional
integrability. A common subsequent causal experiment is also a kernel of
the initial state, so its complete transcript obeys the same preparation
error bound if its conditional dynamics and policy are the same in both
comparisons.

**Scope clarification, added after the finite-clock review:** the common
kernel must include apparatus initialization and any retained controller
memory. Fresh common apparatus initialization, or discarding the warm-up
transcript, is sufficient. A warm-up transcript correlated with the driver
history is extra initial information; retaining it requires a bound on
the augmented prepared-state/transcript law, which (P1)--(P3) do not supply
by themselves. This clarification preserves the reviewed root version
hash above and the original Gaussian state-law proof.

The acquired upper bound

    sigma_up(alpha)=max(0,[alpha^T Hhat alpha
                                  +eta_H||alpha||²]/tau)

is valid simultaneously for all alpha on the calibration event. It may
therefore be inserted in (P1)--(P3) for a force selected independently of
the fresh service driver state. For example, TV target epsilon is met by

    b >= max(0, gamma^-1 log[sqrt(sigma_up/(4gamma))/epsilon]). (P4)

When sigma_up=0 use b=0. The common-preparation work bound supplies the
additional particle/bath input-work budget

    W(b) <= tau sigma_up(4b+2/gamma).                     (P5)

This construction does not prepare independent driver equilibrium samples
or pay for the actuator, force profile, uniform receiver preparation or
thermal receiver preparation. Those remain explicit physical gates and
costs. It does make the subsequent coupled stationary preparation error
quantitative using the acquired dynamical record, instead of assuming a
hidden joint-system mixing time.

## 7. Review limits and conventional comparison

Paired equilibrium correlations, Gaussian mixture KL, matrix concentration,
linear filtering and Girsanov are conventional tools. An equally informed
existing method can acquire the same matrices and evaluate the same
quadratic forms at the same leading task cost. The addition under review
is the precise physical consequence and compatible native projection,
preparation and reuse theorem, not a numerical speedup.

All heat and work in this note concern the declared degrees of freedom and
thermal baths. An implementation of nonreciprocal forcing may dissipate
additional energy in external fields, sensors or controllers. No such
apparatus was constructed or operated; the mathematics does not charge
its missing engineering cost as zero.
