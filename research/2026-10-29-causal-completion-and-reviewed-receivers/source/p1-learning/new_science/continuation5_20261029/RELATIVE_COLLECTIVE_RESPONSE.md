# Local control of an entire collective relaxation time

29 October 2026. Further root construction from the selective energy
inequality. This is an equilibrium dynamical response theorem, not a
claim about arbitrary trajectory laws or a new hydrodynamic limit.
Schur complements, resolvent order and variational response theory are
established machinery. Historical novelty of this assembly is open.

## 1. The additional consequence

A uniform absolute bound on correlations cannot simply be integrated
over infinite time. Here the relative energy premise gives a different,
stronger receiver: every Laplace-transformed visible autocorrelation,
including its full integrated correlation time when finite, has a
controlled **relative** error. No inverse visible gap occurs in the
relative error budget, even though the correlation time itself diverges
as that gap closes.

This connects local acquisition and an actual selective operation to a
collective transport quantity. Its certificate does not require directly
observing the slowest relaxation or reconstructing hidden dynamics.
Preparing the declared initial equilibrium and implementing the controls
retain their actual costs.

## 2. Relative resolvent theorem

Use A=[[a,b*],[b,C]] and the premise from
GAP_FREE_SELECTIVE_AVERAGING.md. Put r=eta^2<1. For every z>0,

    (z+a)^(-1) <= P(z+A)^(-1)P
       <= [z+(1-r)a]^(-1)
       <= (1-r)^(-1)(z+a)^(-1)                     (1)

in quadratic-form order on PH. This holds for the stated finite-state
setting and the bounded-native/common-Laplacian form extension.

**Proof.** Eliminating the omitted block yields

    P(z+A)^(-1)P=[z+a-K_z]^(-1),
    K_z=b*(z+C)^(-1)b.                             (2)

K_z is nonnegative. By the energy premise and the variational formula,

    <u,K_z u>
      =sup_v [2 Re<v,bu>-<v,(z+C)v>]
      <=sup_(q>=0)[2eta sqrt(<u,au>q)-q]
      =r<u,au>.                                   (3)

The supremum is over the relevant form domain; q=<v,Cv>.
The remaining -z||v||^2 was discarded in an upper bound. Hence
z+(1-r)a<=z+a-K_z<=z+a. Invert positive operators and then use
z+(1-r)a>=(1-r)(z+a). This proves (1). QED.

No inverse of C at zero is needed in the proof. Invariant hidden
directions are allowed; the energy premise forces b to be orthogonal
to the directions where C has zero energy.

## 3. Integrated response and monotonic control

For visible f, the equilibrium Laplace correlation is

    R_A(z;f)=int_0^infinity exp(-zt)<f,exp(-tA)f> dt
            =<f,(z+A)^(-1)f>.                     (4)

Equation (1) bounds it between its averaged reference and at most
1/(1-r) times that reference. Let z decrease to zero. By spectral
monotone convergence, if <f,a^dagger f> is finite and f is orthogonal
to ker(a), then

    <f,a^dagger f> <= int_0^infinity <f,exp(-tA)f> dt
        <= (1-r)^(-1)<f,a^dagger f>.               (5)

Thus the actual integral is finite as well. Constants and other
conserved modes must be removed or handled at z>0. Centering only by
one global mean does not remove every conserved mode in a reducible
system. The particle receiver works within a fixed occupancy sector.

For A_kappa=B+kappa H, with B and H fixed and nonnegative, increasing
kappa increases A_kappa in form order. Therefore

    kappa2>=kappa1 implies
    P(z+A_kappa2)^(-1)P <= P(z+A_kappa1)^(-1)P.      (6)

For each f its integrated/Laplace response decreases toward the mean
generator response as the selected bath grows; r=J0/kappa bounds the
remaining excess when kappa>J0. This monotonicity concerns reversible
stationary response and the specified kinetic actuator. It is not a
claim that every transient correlation, mixing time or first-passage
time decreases pointwise, or that heating any device has this effect.

## 4. Consequence for a conserved many-particle density mode

In SELECTIVE_KINETIC_ANNEALING.md, a normalized nonzero density Fourier
mode F_q has mean-generator eigenvalue omega_q=s(1-cos q). Define its
actual full equilibrium integrated correlation

    tau_q=int_0^infinity E[conj(F_q(Y0))F_q(Yt)] dt.

The same supplied local bound r=M/kappa yields

    1/omega_q <= tau_q <= 1/[(1-r)omega_q].         (7)

Define the finite-volume response coefficient

    s_resp(q)=1/[(1-cos q)tau_q].                   (8)

It then satisfies

    (1-r)s <= s_resp(q) <= s                        (9)

for every N, nonzero q and permitted frozen hidden amplitude pattern.
It increases monotonically with kappa. This coefficient is explicitly
defined through integrated density response; identifying it with a
macroscopic diffusion coefficient in another convention or proving an
infinite-volume path limit would require those further statements.

For q=2pi m/N, fixed m, the relaxation time is of order N^2, yet the
relative excess is at most r/(1-r) with a fixed bath strength. To obtain
relative correlation-time tolerance epsilon it suffices to supply

    kappa >= M(1+epsilon)/epsilon.                 (10)

This sufficient per-phase strength is independent of N and omega_q.
Native-rate confidence gives M<=J_U and a mean interval for s. The same
local experiment thereby yields simultaneous intervals for every tau_q
without observing an entire diffusive relaxation. It does not erase
the cost of preparing the equilibrium, local isolation, a rate ceiling,
clock accuracy, independent actuation or retained-record conditioning.

## 5. Finite confidence and fitted response

If |mhat_i/m_i-1|<=eps uniformly, preserving the same pi, then
(1-eps)a<=ahat<=(1+eps)a. Quadratic inverse-order bounds combine with
(1) to give, for z>0 and every f,

    (1-eps)<f,(z+ahat)^(-1)f>
       <= R_A(z;f)
       <= [(1+eps)/(1-r)]<f,(z+ahat)^(-1)f>.        (11)

This is a conservative uniform-z form; the exact z-dependent sandwich
is sharper. The same bounds hold at z=0 when the reference integral
is finite off conserved directions. The simultaneous finite-data event
in FINITE_ACQUISITION_AND_RESPONSE.md supplies r and eps. It does not
give posterior success conditional on every possible calibration record.

For normalized stochastic observations, arbitrary TV contamination of
the initial law cannot be multiplied by a finite constant to control
an unbounded time integral. Equations (4)-(11) refer to the exact
declared equilibrium/operator response on the confidence event. A
finite-horizon integral pays horizon times any initial-TV error;
an infinite-horizon experimental estimator needs a tail/integrability
contract. The earlier finite-TV preparation theorem does not silently
provide that stronger contract.
