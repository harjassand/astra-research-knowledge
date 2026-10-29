# Preparing one reusable operational state without assuming a hidden stationary reset

29 October 2026. New construction found during the independent preparation
review. Author ordinary proof; not part of the reviewed root version. The
construction uses exact acquired operation closure and does not infer it from
finite noisy near-closure. It does not bootstrap the first stationary calibration.

## 1. Intended consequence

An actually executable word can prepare repeatable future consequences even
when it does not preserve the original microscopic equilibrium pi. What needs
to contract is its acquired action on predictive effects modulo constants.
Its limiting operational preparation is itself determined by finite matrices.
The law bounds control bounded event/payoff consequences. They do not by
themselves bound an unbounded mean lifetime without a tail or moment condition.

This removes a full hidden-stationarity requirement from the exact reset theorem.
If the target is specifically the OLD baseline pi service, an acquired bias
floor must remain. If repeatability under the chosen physical word is the target,
that bias defines a new prepared law rather than an error to be ignored.

## 2. Exact source/interface conditions

Use the finite/countable full-support pi setting and the exact finite service
effect space V from the actual-operation theorem. Let F=(f_1,...,f_r), with
0<=f_i<=1, G>=gI, 1 in V, and put C=sqrt(r/g). Hence

    |v(x)|<=C ||v||_(L2(pi)),   v in V, every native state x.       (1)

The continuous-state alternative needs an explicit pointwise/Feller version
condition, as in the root preparation theorem. Pure L2 identities do not cover
arbitrary pi-null initial states.

Let W be an ACTUAL fixed physical kernel word preserving V and constant1. Its
restricted action is acquired through the declared observation/preparation
interface, for example by the weighted adjoint-word construction. We do NOT
assume pi W=pi. Its internal outcomes, clock realization and randomization
variables are not retained for later service unless their full joint instrument
has been included in the operation representation and reset analysis.

Let ell(v)=pi(v), P0 v=v-ell(v)1, and V0=ker ell. Define the FINITE acquired maps

    A=P0 W|V0,       b=ell W|V0.

Assume certified true bounds

    ||A||_(L2(pi))<=kappa<1,       ||b||_(V0^*)<=delta.           (2)

Unlike W|V0, A is defined even when W does not preserve V0. Use the Gram-metric
operator norm, not just an eigenvalue modulus. Kappa need not be small for a
single call. If a verified finite power has norm <1, that power is an available
longer word and its actual cost is charged.

## 3. Exact finite-dimensional decomposition

Write f=ell(f)1+v, v=P0f. Since W1=1,

    Wf=[ell(f)+b(v)]1+A v,
    W^m f=[ell(f)+sum_(j=0)^(m-1) b A^j v]1+A^m v.          (3)

This is an elementary block-triangular operator identity; it does not use
microscopic mixing, positivity of predictive coordinates, or reversibility
of the product word. Define

    ell_*(f)=ell(f)+b(I-A)^-1P0 f.                           (4)

The inverse exists with norm <=1/(1-kappa). Formula (4) is determined by the
acquired finite representation. It satisfies ell_*(1)=1 and ell_*W=ell_*.

For a service event effect f_A, 0<=f_A<=1 and ||P0f_A||_2<=1/2. Equations
(1)--(3) yield the uniform baseline-relative estimate

    sup_x |W^m f_A(x)-ell(f_A)|
      <=(1/2)[C kappa^m+delta(1-kappa^m)/(1-kappa)].          (5)

Thus if the goal remains baseline service, the limiting certificate is the
acquired floor delta/[2(1-kappa)], rather than an invented equilibrium reset.
When b=0, this recovers the root theorem even if pi W=pi is NOT known outside V.
Only predictive stationarity ell W=ell on V is then required.

Subtracting (4) instead gives

    W^m f-ell_*(f)1
         = A^m P0f - [b A^m(I-A)^-1P0f]1.

Therefore

    sup_x |W^m f_A(x)-ell_*(f_A)|
       <=(1/2)[C+delta/(1-kappa)] kappa^m.                  (6)

The same bound works for EVERY event in EVERY admitted finite future program.
This is a horizon-independent operational reset to the word's own prepared
law. It does not assert convergence of the hidden microscopic distribution.

## 4. The prepared service laws are positive probability laws

Although (4) uses signed predictive coordinates, positivity is not assumed.
For each actual initial x and service program, W^m followed by service is a
genuine probability law. Equation (6), uniformly over all service events,
makes these laws Cauchy in total variation. The space of finite measures is
complete in total variation, so the limit is a genuine probability law with
event values ell_*(f_A). It is independent of x.

Consistency under restriction of records and common postprocessing is inherited
from the actual finite-m service laws. The same finite functional therefore
supports all the admitted programs, not a separately chosen limit for each
payoff. No r-state positive Markov realization is asserted or required.

In a finite hidden space a microscopic W-stationary distribution exists, but
the theorem does not need to identify or prepare it. In a more general kernel
interface the proof does not assume microscopic stationary-measure existence.
The supplied native source class may have stronger properties; none is borrowed
for the operational statement. A frozen hidden spectator can retain arbitrary
old information while every admitted service consequence converges as above.

## 5. Old records and reuse

For an arbitrary retained old record R, condition on R=r and allow the actual
hidden starting law to depend arbitrarily on r. Let the subsequent service
policy use that same r in both the physical and reference experiments. Every
joint event induces a bounded effect f_(A,r) in V. Integrating (6) over its
conditional starting law and the SAME marginal law of R gives

    TV(joint old record and actual service,
       same old record and ell_*-initialized service)
       <= min(1,(1/2)[C+delta/(1-kappa)]kappa^m).            (7)

The reference service may depend on R through the chosen policy. The reset
removes dependence carried additionally by the source state. The actual word
must not retain new reset information outside the declared service interface;
averaged random clocks do not imply a conditional guarantee given their
realized times or random seeds.

For desired epsilon, choose m large enough that the right side of (7) is at
most epsilon, using the certified kappa,delta,g and actual word costs. For
kappa=0 one word suffices. Switching, durations, work, measurement/erasure,
precision and numerical execution are not supplied by matrix contraction.

## 6. What is actually acquired and what remains assumed

The finite record determines ell, the restricted W, A and b; a certified Gram
floor converts their numerical enclosures into the norm bounds in (2). Thus
the contraction and any baseline bias are finite operational properties rather
than hidden microscopic mixing assumptions. If (2) is not certified, the word
has not earned this guarantee. Another operation or a longer word may help,
but existence of a suitable word is not promised.

For exact V closure, finite statistical/numerical uncertainty in these maps can
be handled by bounds rather than exact equality tests. For example, if Ahat,bhat
approximate A,b with ||A-Ahat||<=e_A, ||b-bhat||<=e_b, ||Ahat||<=kappahat<1,
then their stationary correction rows obey

    ||b(I-A)^-1-bhat(I-Ahat)^-1||
       <= e_b/(1-kappa)
          +||bhat|| e_A/[(1-kappa)(1-kappahat)].             (8)

Any additional error in ell, the Gram geometry or the constant-coordinate map
must also be propagated. Formula (8) is not a replacement for those errors.
Errors in service operators retain their own complete-consequence bounds.

EXACT operation/effect closure remains a structural hypothesis of the uniform-x
result. Small L2 leakage alone cannot control rare-state initializations; the
root's density-qualified approximate theorem and the preserved three-state
counterexample still apply. No first-calibration iid source or bath reset is
manufactured by a finite reduced fit. This is a new reuse construction after
the needed information has genuinely been acquired.

## 7. Mathematical ancestry and claimed addition

Block-triangular iteration, finite-dimensional contraction and resolvent inversion
are standard. The useful connection is to an acquired physical operation algebra:
one may certify and execute a predictable preparation WITHOUT establishing a
microscopic reset or preserving the original hidden equilibrium. This is a
conditional foundational construction, not a practical speedup or a claim of
historical priority. No device or physical acquisition was performed here.
