# Rare total transport without identifying the frozen kinetic context

29 October 2026. Root construction, seventh continuation.

This receiving theorem uses the actual independent phase operation in
`PHASE_AVERAGING_AT_LARGE_DEVIATION_SCALE.md`. Its target is a finite-time
large-deviation law for total circulation, not a full microscopic path
law. The simple-exclusion exponent, exponential tilting and occupation
replacement are established machinery. The candidate addition is their
uniform transfer to this supplied family of unknown, possibly nonlocal
kinetic contexts. Priority of that assembled result remains unresolved.

## 1. Statement and normalization

On an N-site ring let eta_i be 0 or 1, eta^i exchange i and i+1, and z
be arbitrary frozen information. The actual physical native rates are

    r_i(eta,theta,z)=(s/2)[1+alpha_i(eta,z) cos(theta_i)],
    |alpha_i|<=a<1, alpha_i(eta^i,z)=alpha_i(eta,z).        (1)

The unknown amplitudes can vary with N, position and the entire visible
configuration. The common mean s>0 is part of the actual interface;
it cannot be inferred from invariant weights alone. Independent phase
diffusions act at physical rate kappa_N, leaving eta,z unchanged.
Observe the system for physical time N^2 T, with fixed T>0. Equivalently
its macroscopic generator is

    L_N=N^2[sum_i r_i(T_i-I)+kappa_N sum_i partial_i^2].   (2)

Assume kappa_N tends to infinity, at any rate. An alternative actual
supplier has r_i=(s/2)(1+beta_i sigma_i), |beta_i|<=a, beta_i invariant
under its own swap, with independent sign flips at physical rate
gamma_N tending to infinity. Original phases can be absorbed into beta.
This alternative requires genuine local sign-reversal actuation.

Let eta^N initially be deterministic with empirical density converging
weakly to m dx on the unit circle, where 0<m<1. Initial phases or signs
are arbitrary, as is z. The conclusion holds for every deterministic
initial sequence approaching m; the hidden-context estimates are
uniform. Uniformity over a family of initial sequences additionally
requires a common vanishing initial-profile error modulus. Mixing initial profiles with
only ordinary high probability needs a separate initial LDP.

Write J_i^N(t) for the net count of native swaps from i to i+1 by
macroscopic time t, positive when eta_i=1 and eta_(i+1)=0 immediately
before the swap. Define

    Q_N(T)=N^-2 sum_i J_i^N(T),    chi(m)=m(1-m).          (3)

The receiving result is an LDP on the real line at speed N,
with good rate function

    I_T(q)=q^2/[2 s chi(m) T].                            (4)

Thus the logarithmic probability of a small neighborhood of q tends,
as its width tends to zero after the volume limit, to -I_T(q). The
associated scaled cumulant generating function is

    lim_N N^-1 log E exp[N lambda Q_N(T)]
       =(s/2) chi(m) T lambda^2,  lambda real.            (5)

The proof below establishes the upper and moment bounds directly.
The lower bound uses the explicitly reconstructed weak-tilt density
and current law of large numbers in
`record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md`; its exact
receiving status is recorded in the final verification section.

The probabilities are those of the actual joint execution law. For
a fixed initial-profile sequence, the dynamical estimates are uniform
in pre-existing records and frozen z when the entire future conditional
native-and-actuator generator remains the declared law. Fresh actuator
noise alone is insufficient if the record exposes future native
innovations. The theorem does not
assert the same exponent after arbitrary rare future-record
conditioning, nor equivalence of apparatus or microscopic histories.

## 2. Two exponential inputs

Let delta_i=eta_i-eta_(i+1), a_i=delta_i^2, and

    H_N=sum_i r_i delta_i
       =(s/2)sum_i alpha_i delta_i cos(theta_i).          (6)

The unmodulated part telescopes exactly around the ring. The preceding
phase proof gives, for every fixed epsilon>0,

    limsup_N N^-1 log P(|int_0^T H_N dt|>epsilon)=-infinity.
                                                               (7)

The same conclusion holds for the phase part of

    B_N=(1/N)sum_i r_i a_i
       =(s/2) A_N + (s/(2N))sum_i alpha_i a_i cos(theta_i),
    A_N=(1/N)sum_i a_i.                                  (8)

It also holds under every fixed weak current comparison tilt
r_i^E=r_i exp(E delta_i/N), using the exact second-moment identity for
its likelihood. These are statements about accumulated integrals.
They do not assert that H_N is small at an individual instant.

Arbitrary continuous-phase initialization is handled by actual active
warm-up of physical duration u/kappa_N. The post-layer density is at
most (2 K_u)^N against the reversible product reference. This transfers
superexponential replacement, never a finite rate by itself. Both
the current accumulated during that layer and the density changes are
superexponentially negligible at speed N. The sign model needs no such
layer: every initial joint visible/sign law is dominated by 4^N times
its product reference.

## 3. A direct activity upper bound

Only a one-block upper estimate is needed for the LDP upper bound.
The following proof does not assume that the native rate is local.
For a block b of ell consecutive sites put

    m_b=(1/ell)sum_(i in b) eta_i,
    U_b=(1/ell)sum_(internal bonds of b) a_i,
    R_b=U_b-2 chi(m_b).                                  (9)

Under the uniform canonical measure on b with k particles,
E a_i=2k(ell-k)/[ell(ell-1)] for every internal bond. There are ell-1
such bonds, so E U_b=2 chi(k/ell) exactly. In particular R_b has zero
conditional mean given the outside configuration and block count.

For each fixed ell, the finite nearest-neighbor exchange chain in
every nontrivial canonical block sector is connected. Its Poincare
constant C_ell is finite; trivial sectors have variance zero. With
D_b^0=(1/2)sum_(internal i) E[(f(eta^i)-f(eta))^2], conditioning and
Cauchy--Schwarz imply, for ||f||_2=1,

    |<R_b,f^2>| <= 2 ||R_b||_infinity sqrt(C_ell D_b^0).
                                                               (10)

Indeed subtract the conditional mean of f, write f^2-(E_b f)^2 as
(f-E_b f)(f+E_b f), and use E_b(f+E_b f)^2<=4 E_b f^2.
No conditional independence of the actual evolving process is used.

Partition into B=floor(N/ell) full blocks and at most ell-1 unused
sites. Let R_(N,ell)=(ell/N)sum_b R_b. Summing (10), then applying
Cauchy--Schwarz across disjoint blocks, gives

    |<R_(N,ell),f^2>|
       <=2 sqrt(C_ell ell/N) sqrt(D^0(f)),               (11)

after enlarging C_ell to include ||R_b||_infinity^2 if needed.
Native ellipticity gives D_native>=c_min D^0,
c_min=s(1-a)/2. Therefore the top numerical range of
L_N+bN R_(N,ell) is at most

    b^2 C_ell ell/(c_min N).                             (12)

The Feynman--Kac bound and any exp(hN) initial density ceiling imply
that int R_(N,ell) is superexponentially concentrated near zero for
each fixed ell. One can also condition on the autonomous phase path:
the visible native generator is reversible for the same uniform law
at every time, and an arbitrary visible initial state costs only 2^N.
Thus this activity estimate itself needs no phase warm-up.

Let m_N=N^-1 sum_i eta_i, which is conserved. The bonds omitted by the
partition have fraction at most 1/ell+ell/N. Concavity of chi, adding
the leftover block with its proper weight, gives the pointwise bound

    A_N <= 2 chi(m_N)+R_(N,ell)+1/ell+ell/N.              (13)

Given epsilon>0, first choose ell so that T/ell<epsilon/4,
then let N grow and apply (12), then let the fixed exponential
multiplier b grow. It follows that

    limsup_N N^-1 log P(int_0^T A_N dt
                       >2 chi(m)T+epsilon)=-infinity.   (14)

This is an upper bound, not a two-sided local-equilibrium assertion.
It remains valid under a fixed weak current tilt by likelihood L2
transfer. The lower bound will separately need the two-sided typical
activity limit under that tilt.

## 4. The actual likelihood gives the upper bound

For a fixed real E, let P^E denote the mathematical comparison law
with native rates r_i exp(E delta_i/N) and the same phase bath and
initial state. Its likelihood relative to the actual law is

    Z_E=exp[N E Q_N(T)-C_N(E)],
    C_N(E)=int_0^T N^2 sum_i r_i(e^(E delta_i/N)-1)dt.    (15)

It is a true mean-one martingale. A uniform Taylor expansion gives

    C_N(E)/N=E int H_N dt+(E^2/2)int B_N dt+O_E(N^-1).
                                                               (16)

Define v=s chi(m)T and Lambda(E)=v E^2/2. Equations (7), (8) and
(14) imply that for every epsilon>0,

    P(C_N(E)/N>Lambda(E)+epsilon)
          is superexponentially small at speed N.       (17)

On the complement, Q_N in (q-delta,q+delta) implies
Z_E>=exp[N(Eq-|E|delta-Lambda(E)-epsilon)]. Since E Z_E=1,

    limsup_N N^-1 log P(|Q_N-q|<delta)
       <=-Eq+|E|delta+Lambda(E)+epsilon.                 (18)

Let epsilon and delta decrease, and optimize E=q/v. This proves the
local upper rate q^2/(2v). The same calculation with E positive or
negative bounds the two tails. For example,

    limsup_N N^-1 log P(Q_N>M)<=-E M+Lambda(E), E>0.      (19)

Hence the laws of Q_N are exponentially tight on the real line. A
finite cover of a compact set by the local bounds, then (19), gives
the LDP upper bound for every closed set. This argument derives the
finite rate from the actual current martingale; no initial density
ceiling is used to transfer that finite rate from another process.

## 5. The receiving lower-bound connection

For the same fixed comparison field E, the required typical statement
is

    pi_t^N -> m dx,
    int_0^T A_N dt -> 2 chi(m) T,
    Q_N(T) -> v E                                  in P^E probability.
                                                               (20)

Its reconstruction uses the following concrete inputs. Native uniform
ellipticity gives a uniform lower bound on the ordinary exchange
Dirichlet form. The weak-tilt numerical-range estimate retains half
that form and costs only O(N). The classical one-block/two-block
variational estimates therefore apply to occupation observables,
including a_i, after integrating over the spectator phases. They
require no locality of the coefficients alpha_i. The phase drift is
removed by (7) under P^E. Visible martingale quadratic variations are
O(1/N). Every limiting density path consequently solves

    partial_t rho=(s/2)partial_x^2 rho
                   -s E partial_x chi(rho), rho(0,x)=m. (21)

Uniqueness of the bounded weak solution of this uniformly parabolic
scalar equation gives rho=m. The occupation replacement then gives
the second part of (20). The current martingale decomposition is

    Q_N=M_N+int sum_i r_i e^(E delta_i/N)delta_i dt
       =M_N+int H_N dt+E int B_N dt+O_E(N^-1),          (22)

where E^E[M_N^2]<=C_E T/N. Equations (7), (8) and (20)'s activity
limit give its final current assertion. Arbitrary initial phases are
regularized only for the replacement estimates, in a vanishing
actual initial layer; the macroscopic initial profile is unchanged.

The detailed ordinary occupation/tilted-hydrodynamic connection is
saved in `record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md`. This is an adaptation of
classical weakly asymmetric exclusion, not a new hydrodynamic method.

Combining (16) and (20), under P^E,

    (1/N)log Z_E -> E(vE)-Lambda(E)=vE^2/2.             (23)

For a prescribed q choose E=q/v. Restrict the identity
P(A)=E^E[Z_E^-1 1_A] to |Q_N-q|<delta and to
|N^-1 log Z_E-I_T(q)|<epsilon. Both events have joint P^E probability
tending to one. Thus

    liminf_N N^-1 log P(|Q_N-q|<delta)
       >=-I_T(q)-epsilon.                              (24)

Let epsilon decrease. Every open set contains such a neighborhood
of each of its points, proving the open-set lower bound. No physical
weak-bias actuator is claimed: P^E is solely a proof comparison law.

## 6. Exponential moments, not merely a formal Legendre transform

For every fixed lambda, the family has a finite exponential-moment
envelope

    limsup_N N^-1 log E exp[N lambda Q_N(T)]<infinity.   (25)

To see this first under the reversible reference, use (15), (16),
the pointwise bound on B_N, Cauchy--Schwarz, the exact bound
E Z_lambda^2<=exp(C_lambda N T), and the phase Feynman--Kac estimate
for 2N lambda int H_N. The resulting exponent is at most
C_lambda N T+C_lambda' N T/kappa_N. For signs replace kappa_N by
gamma_N, with the corresponding constant.

An exp(hN) initial density ceiling preserves (25). For arbitrary
continuous phases, split off the active initial layer and use
Cauchy--Schwarz. Its jump count is dominated by a Poisson variable
with mean C N/kappa_N, and each contribution to N Q_N has magnitude
1/N. Consequently its fixed exponential moments cost O(1/kappa_N).
The unconditional endpoint law after that layer has the required
exp(hN) ceiling, so the other Cauchy--Schwarz factor is controlled.
This does not condition on a particular endpoint or discard a record.

Applying (25) at 2lambda and Cauchy--Schwarz to |Q_N|>M, followed by
exponential tightness (19), proves

    lim_(M->infinity) limsup_N N^-1 log
       E[e^(N lambda Q_N) 1_(|Q_N|>M)]=-infinity.        (26)

The bounded-domain Laplace principle from the just-proved LDP and
this tail estimate establish (5). Thus the displayed SCGF is an
actual limit; the Legendre calculation alone would not have proved it.

## 7. Consequence and limits

For this supplied conservative architecture, one common kinetic
scale s, the initial density m, and the physical observation time
N^2T determine the exponentially rare total-transport exponent.
The bounded unknown amplitudes may contain arbitrarily complex,
frozen, nonlocal kinetic information. It need not be identified or
mixed. Actual independent phase/sign agitation removes its contribution
at the speed N of these rare events.

The operation is substantial: local kinetic coordinates must be
independently addressable and selectively actuated while leaving
occupancy and z unchanged. The theorem does not supply those ports,
sensing, isolation, timing precision, homogeneous mean rates, or a
cost advantage. A conventional controller with the same operations
can implement the same law. Deterministic global cycling is a strong
alternative for bounded local contexts, as the complementary
construction proves; independent local noise is not claimed uniquely
necessary in that subclass.

This receiving result concerns a real-valued integrated current on
a fixed diffusive time horizon. Full density/current path LDPs,
nonequilibrium boundary reservoirs, arbitrary feedback policies,
singular kinetic constraints, and finite-N error rates are separate
claims. The exact SSEP current action is already established. The
newly investigated issue is robustness of that action to the stated
controlled unknown kinetics, with its actual supplier attached.

## Primary construction used

Bertini, De Sole, Gabrielli, Jona-Lasinio and Landim,
*Large deviations of the empirical current in interacting particle
systems*, https://arxiv.org/abs/math/0512394, especially Lemma 3.1,
Theorem 3.2 and the current exponential martingale, supplies the
classical density/current route and its action. Their normalization
has s=1. Kipnis--Olla--Varadhan (1989), DOI 10.1002/cpa.3160420202,
is the earlier weak-asymmetry/density large-deviation construction.
The simple quadratic target here is consistent with contraction of
that established action from a flat profile. The present proof does
not assume a new full path LDP for the modulated family.

## Receiving verification

The lower-bound dependency is now explicitly reconstructed and
reviewed in `record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md`, SHA-256
`ae8dbab399e9378a8ce8d2e8a87bac07a5f4b4c409db5329db50274e01f660f5`.
`record_geometry/RECEIVING_ACTION_REVIEW.md` preserves the actual
reviewed scalar version and its quantifier correction; final receipts
pin the corrected wording. The scalar proof is complete at its stated
interface. The stronger independent-control full spatial action is
proved separately in `CONTROLLED_MACROSCOPIC_ACTION.md`; the scalar
proof did not need to assume that theorem.
