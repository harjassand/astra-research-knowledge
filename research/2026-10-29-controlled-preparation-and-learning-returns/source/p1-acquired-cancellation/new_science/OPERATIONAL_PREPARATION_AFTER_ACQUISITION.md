# Preparing repeatable consequences after acquiring the operation representation

29 October 2026. Root new consequence prompted by the initial-preparation
counterexample in the independent review. This does NOT bootstrap the original
stationary calibration without its preparation premise.

## 1. Exact operational reset without microscopic regeneration

Use the finite/countable full-support-pi native setting of the actual-operation
theorem. Suppose a finite, label-local bounded feature family has EXACT closure
for the entire service operation menu. Its Gram matrix satisfies G>=g I, g>0.
Features f_i are genuine conditional event probabilities in[0,1], and 1 lies
in their span V. The acquired record determines each operation on V.

Let W be an ACTUALLY implementable fixed reset word that preserves pi and V.
Its reduced action on V_0={f in V:<1,f>_pi=0} has certified norm

    ||W|V_0||<=kappa<1.                                      (1)

This is acquired finite-dimensional operational contraction, not an assumed
hidden microscopic mixing bound. A deterministic baseline evolution for time
t gives kappa=exp(-lambda_V t) when its acquired restricted generator has a
positive centered gap. A product of individually common-equilibrium operations
may also satisfy(1). The word, its durations, and its operations must actually
be available; a contracting matrix alone does not execute it.

For every x and f=F c in V,

    |f(x)|<=sqrt(r/g)||f||_2.                                (2)

Indeed ||F(x)||_2<=sqrt(r), while ||Fc||_2^2=c^T Gc>=g||c||_2^2.
Full support on a countable space makes L2 identities pointwise. On a continuous
space this gives only essential-supremum control unless Feller/continuity or
another pointwise premise is supplied; arbitrary singular initial states are
not silently covered.

For any event A in any admitted finite future service program, its conditional
probability f_A(x) belongs to V by exact closure and satisfies 0<=f_A<=1.
Its centered L2 norm is at most1/2. Therefore

    sup_x |W^m f_A(x)-pi f_A|
                <=(1/2)sqrt(r/g) kappa^m.                    (3)

Taking the supremum over all service events yields a full future-record TV
bound, uniformly over admitted programs, independent of their finite horizon:

    epsilon_reset=min(1,(1/2)sqrt(r/g) kappa^m).              (4)

The guarantee concerns every consequence in the acquired operation algebra.
It does not claim convergence of the hidden microscopic state. A frozen
unobservable spectator can retain its initial state forever while(4) holds.

## 2. Old records and actual reset access

The reset word has fixed public settings and is executed WITHOUT retaining new
state observations from its interior. It can erase the influence of an arbitrary
old classical record R: conditional on R, the starting hidden law is arbitrary;
(3) applies to each possible initial state and hence its mixture. The resulting
joint law of (R,service record) is within epsilon_reset of the same R followed
by a fresh pi-initialized service under the SAME R-selected service policy.
If that policy uses R, the reference outputs may naturally depend on R; the
claim removes additional source-state dependence, not the policy itself.

Do not apply(4) to a reset that retains an unmodelled path measurement. If W is
an averaged random-clock kernel and the realized clock is retained, the acquired
average contraction need not control the conditional clock record. A fixed
deterministic-duration reset avoids that issue. Otherwise include the actual
clock/output instrument in the certified operation algebra and its contraction.
No duration, readout, randomization key, or correlated apparatus memory is erased
merely by calling the reset one operation.

For a target epsilon and 0<kappa<1, it suffices to execute

    m>=log(sqrt(r/g)/(2epsilon))/[-log(kappa)],                (5)

rounded up and at least zero. kappa=0 needs at most one word. Pay m times the
actual word duration, switching, work and clock costs. No microscopic reset
device or hidden preparation oracle is inferred. This is a REUSE construction
after successful acquisition, not a proof of free first calibration.

## 3. Finite residuals require a physical initial-law qualification

An empirical near-zero residual cannot replace exact closure in the uniform-x
claim. The independent three-state example has small L2(pi) leakage and identical
retained initial moments but a fixed response discrepancy from a rare-state
preparation. Thus moment matching alone cannot certify an approximate reset.

A sufficient finite-error version retains a warranted initial density g_0
relative to pi with ||g_0||_2<=K. Conditional reset/service guarantees require
this bound for the actual conditional initial laws, or a suitable joint bound.
Let Q_0 be the reversible baseline generator, P the label-closed projection,
A_0=P Q_0P|V its TRUE compression, and d_0=||(I-P)Q_0P||. Suppose the centered
compression has spectral gap lambda>0. This gap can be bounded from the acquired
finite matrices with their inverse-compression and numerical errors; it is not
a hidden full-state spectral gap.

After actual deterministic baseline evolution for time t, g_t=exp(tQ_0)g_0.
Both full and compressed evolutions are contractions and preserve1. Duhamel
gives ||P exp(tQ_0)-exp(tA_0)P||<=t d_0. Consequently

    ||P(g_t-1)||_2
       <=[exp(-lambda t)+t d_0] sqrt(K^2-1).                 (6)

The factor sqrt(K^2-1) follows from pi g_0=1. Also ||g_t||_2<=K.

For the subsequent service horizon T, let

    E_dyn(T)=k^2 T D exp((k-1)JT)

be the main signed path bound for true compressed operators. Comparing each
physical service law with its signed prediction and then comparing their
initial projected functionals gives

    L1(service after reset minus baseline service)
      <=(K+1)E_dyn(T)
       +k[exp(-lambda t)+t d_0]sqrt(K^2-1)exp((k-1)JT).       (7)

This is now a comparison of TWO genuine physical service laws; TV is half the
bound, clipped at1. Numerical and acquisition errors enter by the same initial/
operator terms as in the main theorem, not by pretending A_0 was directly read.

For 0<d_0<lambda, the reset factor in(6) is minimized by
t=lambda^(-1)log(lambda/d_0), with value
(d_0/lambda)[1+log(lambda/d_0)]. If d_0=0 it decays exponentially; if
d_0>=lambda this particular bound gains nothing by waiting. More waiting is
not universally a better certificate. This is an error/cost choice supported
by the acquired representation, not evidence of hidden regeneration.

## 4. Scope of the advance

Known operational-quotient contraction and standard semigroup perturbation
are the machinery. Their use here is attached to a representation whose
conditional inner products and leakage have an actual physical acquisition.
Exact finite closure can make repeatable FUTURE consequences possible even
when microscopic memory never resets. Finite-confidence reuse retains a
preparation-density/TV qualification and all acquired error terms. Initial
stationary acquisition, useful rank, conditioning, and an available contracting
word remain substantive tasks; the theorem does not certify them from a fit.
