# A dynamical information record for heat and equilibrium explanation

29 October 2026. Root construction extending the shear result to an autonomous
equilibrium driver. The compressed-resolvent formulation was independently
suggested and derived in physical_frontier/SPECTRAL_HEAT_PRINCIPLE_INDEPENDENT_REVIEW.md.
This note develops the exact native projection and a complete acquisition
contract for a finite force family. No native record has been acquired.

## 1. Consequence and physical interface

The objective is to identify which reusable dynamical information determines
both the heat of a driven system and whether an equilibrium model explains its
trajectories well. The same information can justify a simpler predictor for
specified coarse consequences. These are distinct tasks and have distinct norms.

An autonomous equilibrium kinetic driver has positions X on a compact connected
torus, momenta P, unit masses, temperature tau>0, symmetric positive friction
matrix Gamma, and force -grad U(X):

    dX=P dt,
    dP=[-grad U(X)-Gamma P]dt+sqrt(2tau Gamma)dW_d.

Its stationary Gibbs law is mu_d, position marginal nu. All driver momenta
are odd under the physical reversal; positions are even. No odd external field
is present. Let L be its stationary Markov generator. U and hidden driver
coordinates need not be reconstructed to USE the observable record below,
but the equilibrium/bath/source-class contract must be warranted.

Couple a transverse circle coordinate y and momentum w by

    dy=w dt,
    dw=[f(X)-gamma w]dt+sqrt(2gamma tau)dW_r, gamma>0.      (1)

The receiver noise is independent. The coupling is one way: changing f leaves
the driver law unchanged. Physically f is an applied work force relative to
the specified stationary bath, not an uncharged equilibrium reciprocal
interaction or a carrier-fluid velocity under a different reversal contract.
This directionality, the thermostat and the calibrated force family are
substantive inputs. A fitted passive record does not establish them.

For bounded f, use a two-sided stationary driver and an independent stationary
OU zeta of variance tau:

    Y_f(t)=integral_0^infinity exp(-gamma s) f(X_(t-s))ds,
    w(t)=zeta(t)+Y_f(t).

An independent uniform y phase makes the full source stationary. Its position
marginal is nu(X) times uniform y, and its full driver marginal is exactly mu_d.

## 2. The exact heat form

Define the compressed resolvent on position observables by

    H_gamma=P_X (gamma-L)^(-1) P_X,
    <f,H_gamma g>_nu
      =integral_0^infinity exp(-gamma t) E_mu_d[f(X_0)g(X_t)]dt. (2)

Here P_X is conditional expectation onto functions of driver position.
The physical equilibrium identity U_Theta L U_Theta=L* and evenness of
position observables imply that H_gamma is selfadjoint. For u=(gamma-L)^(-1)f,

    <f,H_gamma f>=gamma ||u||^2-Re<u,Lu> >=gamma||u||^2.

The stationary Markov semigroup is an L2 contraction, so its generator is
dissipative and its resolvent norm is at most 1/gamma. Consequently

    0 < <f,H_gamma f> <= ||f||_nu^2/gamma for f!=0.        (3)

Strict positivity for each nonzero f does NOT give a positive uniform lower
spectral bound on an infinite force space. The shear example has eigenvalues
decaying like inverse spatial frequency.

Stationarity of Y'=f-gamma Y gives E(fY)=gamma E Y^2. The driver has zero
mean thermal entropy flow, while the receiver contributes its excess kinetic
heat. Thus total stationary physical entropy production is exactly

    sigma[f]=<f,H_gamma f>/tau,
    E Y_f^2=tau sigma[f]/gamma.                          (4)

This is exact at every allowed force amplitude, because the driver is unchanged.
It is not a weak-driving approximation. Individual driver/receiver probability
currents in the joint density need not separately have zero entropy-square
terms; (4) concerns the total stationary physical heat balance.

## 3. The exact nearest equilibrium within the same thermal class

Compare the driven source with EVERY stationary equilibrium model on the same
coordinates, temperature and friction matrices, with arbitrary smooth periodic
potential V(X,y). Write V=U+R. Girsanov gives the stationary path-KL rate

    I(f,V)= ||f||_nu^2/(4gamma tau)
       +(1/(4tau)) E_(nu times uniform)
             [|grad_X R|_(Gamma^-1)^2+gamma^-1 |partial_y R|^2]. (5)

The only possible cross term is proportional to E[f(X) partial_y R], which
vanishes by periodic y integration. Therefore the exact best native equilibrium
is the original driver with a free receiver, denoted P_0 with law mu_0.
For every finite horizon h,

    D(P_f^rho_f[0,h]||P_V^mu_V[0,h])
       =D(P_f^rho_f||P_0^mu_0)+D(P_0^mu_0||P_V^mu_V),    (6)
    inf_V D(P_f^rho_f||P_V^mu_V)
       =D(rho_f||mu_0)+h ||f||_nu^2/(4gamma tau).        (7)

The initial Pythagorean step holds because source and reference have the SAME
position marginal, and equilibrium likelihood ratios differ only through
position potentials. The dynamic step is (5).

A latent Gaussian-shift comparison supplies

    D(rho_f||mu_0)<=E Y_f^2/(2tau)=sigma[f]/(2gamma).      (8)

Condition on the driver history, compare the shifted independent receiver
Gaussian with its unshifted version, then discard the history. The driver
and y marginals already agree. No independence of Y_f from the current
driver state is assumed.

Hence the rate cost of native equilibrium explanation is the ORDINARY force
norm, while heat is the COMPRESSED-RESOLVENT force norm. The first is a
likelihood/model cost, not a second thermodynamic entropy rate.

## 4. The exact structural condition

On an allowed closed position-force subspace S, a uniform bound

    I_native[f]<=C sigma[f] for all f in S

holds if and only if H_gamma restricted to S has a positive lower spectral
bound kappa, with best C=1/(4gamma kappa):

    <f,H_gamma f> >= kappa ||f||_nu^2.                  (9)

For a finite family f_alpha=sum_(i=1)^r alpha_i phi_i(X), define

    G_ij=E[phi_i(X_0)phi_j(X_0)],
    H_ij=integral_0^infinity e^-gamma t
                              E[phi_i(X_0)phi_j(X_t)]dt.

Then

    sigma(alpha)=alpha^T H alpha/tau,
    I_native(alpha)=alpha^T G alpha/(4gamma tau).         (10)

If the features are independent in L2(nu), G and H are positive definite,
and kappa=lambda_min(G^-1/2 H G^-1/2)>0. Small kappa is an information and
precision cost; its positivity is not a uniform quantitative bound. One-time
feature data supplies G but generally not H. Actual eliminated dynamics is
contained in the lagged record.

For the free spatial driver, Fourier modes diagonalize H, reproducing the
negative-half-Sobolev theorem. Known bandwidth or regularity restricts the
directions in which the two physical questions can separate.

## 5. Constructive acquisition from actual dynamical pairs

The following is a declared source-access protocol, NOT a claim that its
physical gates were acquired during this research. Suppose independent driver
preparations in mu_d are genuinely available, the bounded features can be
read without changing the driver dynamics, and |phi_i|<=B_i is warranted.
Sensor uncertainty and actual preparation error must be charged separately.

Draw S from an independent exponential clock of rate gamma, let the actual
driver evolve for S, and read the feature vectors at zero and S. Then

    G_sample = phi(X_0) phi(X_0)^T,
    H_sample = [phi(X_0)phi(X_S)^T+phi(X_S)phi(X_0)^T]/(2gamma)

are unbiased for G and H. No hidden-state reconstruction or numerical time
derivative is required. The time pair is essential; a frozen configuration
does not provide the second matrix.

### A bounded physical clock

To cap each trajectory at T_c, replace H_sample by zero when S>T_c and stop
that trajectory no later than T_c. Its expectation is the truncated integral
H^(T_c), not H. Stationary Cauchy--Schwarz gives the operator-norm tail bound

    ||H-H^(T_c)||_op <= (sum_i B_i^2) exp(-gamma T_c)/gamma. (11)

H^(T_c) itself need not be positive semidefinite: equilibrium underdamped
correlations can oscillate. Use (11), not an unjustified positivity claim.
The mean capped evolution time is at most
(1-exp(-gamma T_c))/gamma and its worst case is T_c. Drawing the censoring
event before execution can reduce this cost but is unnecessary for the bound.

### Finite confidence, precision and reuse

Use N truly independent such preparations. There are M=r(r+1) independent
ENTRY TYPES across the two symmetric matrices (their errors within a trial
can be correlated). A union bound and bounded Hoeffding inequality give,
with probability at least 1-delta, all entry errors at once:

    |Ghat_ij-G_ij| <= B_i B_j sqrt[2 log(2M/delta)/N],
    |Hhat_ij-H^(T_c)_ij|
           <= (B_i B_j/gamma) sqrt[2 log(2M/delta)/N].    (12)

Only independence ACROSS prepared trials is used. Conservative spectral
error bounds are

    eta_G=(sum_i B_i^2) sqrt[2 log(2M/delta)/N],
    eta_H=(eta_G+(sum_i B_i^2)exp(-gamma T_c))/gamma.      (13)

Known deterministic measurement/calibration and arithmetic errors must be
added. For example, errors epsilon_i on each feature change a product by at
most B_i epsilon_j+B_j epsilon_i+epsilon_i epsilon_j; dividing by gamma
gives the corresponding H-product error. Counting a readout does not acquire
that precision. Common sensor noise must not be treated as independent.

A verified numerical/interval calculation that establishes

    Ghat-eta_G I > 0,
    Hhat-eta_H I >= kappa_cert (Ghat+eta_G I), kappa_cert>0, (14)

then proves H>=kappa_cert G on the entire calibrated force family. The same
event simultaneously gives

    |sigma(alpha)-alpha^T Hhat alpha/tau|
                                      <= eta_H ||alpha||_2^2/tau, (15)
    I_native(alpha)<=sigma(alpha)/(4gamma kappa_cert).

The certificate is uniform in coefficients, so choosing alpha after examining
the calibration record does not spend a new statistical failure probability.
SERVICE still needs the stipulated stationary driver preparation independently
of the data used for adaptive selection. Choosing a force based on the current
unreset driver history changes the preparation law and is not covered merely
by (14). Redundant features need a warranted quotient or a restriction to a
strictly certified positive Gram subspace; finite noise does not prove exact
zero directions.

### Full task costs and conventional comparison

Acquisition requires N independent physical equilibrium preparations, up to
2rN calibrated scalar feature readings (or 2N vector acquisitions only when
such a vector sensor really exists), at most N T_c elapsed driver evolution,
mean evolution at most N/gamma, and the actual sensor/reset costs. Computing
the two outer-product averages costs O(Nr^2) elementary arithmetic and stores
O(r^2) numbers, in addition to the raw record if retained. The robust generalized
eigenvalue/semidefinite certificate is ordinary dense matrix work; its bit and
conditioning costs grow as the desired margin shrinks. Each later scalar
quadratic evaluation costs O(r^2), with input calibration and preparation still
required for physical execution. Simultaneous independent preparations can
alter elapsed time but require those additional physical copies.

These are not free capabilities of a generic coarse source. In particular,
equilibrium appearance, visible correlation decay, or a short fitted model do
not prove the required independent preparations, one-way coupling, bath law,
feature readout or force regularity. No such native apparatus was accessed here.

The strongest equally informed route uses the same correlation/Gram estimation
and ordinary linear algebra. The covariance calculation is standard linear
filtering/Green--Kubo machinery; no computational speedup is claimed. The proposed
addition is the exact two-metric physical interpretation, native equilibrium
projection, coercivity criterion and compatible acquisition-to-consequence
assembly. Familiar methods can directly adopt it.

## 6. What this record does and does not predict

G,H determine all stationary heat and native equilibrium KL-rate costs in (10).
They also bound a useful approximate predictor. Coupling to the original driver
with a free receiver gives

    E integral_0^h |w_f-w_0|^2dt=h tau sigma[f]/gamma,
    E sup_(t<=h) d(y_f(t),y_0(t))^2<=h^2 tau sigma[f]/gamma. (16)

The complete noisy-transcript theorems in causal_frontier/ therefore apply
with V=tau sigma[f]/gamma for stationary use, including the stated allowed
sensor/actuation contracts. The reference retains the original equilibrium
driver; it is not a claim that all hidden dynamics can be discarded.

Two-time correlations do NOT specify the exact nonlinear/non-Gaussian receiver
path law, higher cumulants, arbitrary first-passage means, or interventions that
backact on the driver. Those require additional dynamical information or a
different guarantee. Equation (16) controls the consequences it names.

### Common thermal preparation: the oscillatory-correlation correction

For a general equilibrium driver, C_f(t) may be negative. The shear proof's
nonnegative-covariance argument MUST NOT be transferred unchanged. With the
common thermal initial state, use the exact identity

    Y_f^0(t)=Y_f(t)-exp(-gamma t)Y_f(0).

Stationarity and Cauchy--Schwarz imply

    E(Y_f^0(t))^2 <= (1+exp(-gamma t))^2 V <=4V,
    V=tau sigma[f]/gamma.                               (17)

Thus all fixed-horizon coupling/noisy-transcript bounds survive with 4V.
The Gaussian-shift comparison gives D(rho_f(h)||mu_0)<=2sigma[f]/gamma.
The receiver energy equation gives nonnegative total input work

    W(h)=gamma integral_0^h E(Y_f^0(t))^2dt
                           + E(Y_f^0(h))^2/2
         <=tau sigma[f](4h+2/gamma).                    (18)

Physical total entropy is W/tau-D(rho_f(h)||mu_0), hence is also bounded by
the right side of (18) divided by tau. The stronger shear constants require
its nonnegative correlations. After turning the coupling off, the residual
shift decays as exp(-gamma r), giving the corresponding Gaussian preparation
recovery bound. Exact fresh independence at finite r is still not supplied.

All thermodynamic statements concern the declared particles and thermal bath
channels. They do not include unmodeled actuation, sensing, controller or
field-generation dissipation. Similar equations with a different physical
reversal or reservoir interpretation are not automatically interchangeable.
