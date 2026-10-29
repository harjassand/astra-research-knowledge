# Which implementation errors preserve the rare-transport consequence?

29 October 2026. Root follow-on construction. This file distinguishes
structural approximation, statistical confidence and actual directional
bias. It supplements `RARE_TRANSPORT_WITHOUT_KINETIC_IDENTIFICATION.md`.

## 1. Vanishing reversible rate errors need no 1/N accuracy

Allow the actual physical native rates to be

    r_i=(s/2)[1+alpha_i(eta,z)cos(theta_i)
                       +e_(i,N)(eta,theta,z)],          (1)

where alpha_i satisfies the preceding assumptions and

    e_(i,N)(eta^i,theta,z)=e_(i,N)(eta,theta,z),
    sup_(i,eta,theta,z)|e_(i,N)|<=d_N ->0.               (2)

The error may depend on every occupancy and phase coordinate. Assume
a+d_N<=a'<1 for all sufficiently large N. The complete generator is
still reversible for the uniform product reference, at each fixed z,
and D_native>=c_*D^0 with c_*=s(1-a')/2. The phase bath is autonomous.

The same finite-time total-current LDP and SCGF hold when kappa_N
tends to infinity and d_N tends to zero independently. In particular
there is no requirement N d_N ->0 for these reversible errors.

Here is the additional estimate. Let F_i be fixed bounded spatial
coefficients and

    R_N=(s/2)sum_i F_i e_(i,N)(eta_i-eta_(i+1)).          (3)

Own-swap invariance and change of variables under eta -> eta^i give

    <R_N,f^2>
       =(s/4)sum_i <F_i e_(i,N)delta_i, f^2-(f^i)^2>.
                                                               (4)

For ||f||_2=1, weighted Cauchy--Schwarz using the actual positive
native rates, followed by ||f+f^i||_2<=2, yields

    |<R_N,f^2>|
       <= [s ||F||_infinity/sqrt(2c_*)]
                              d_N sqrt(N D_native(f)). (5)

To check the constant, write each term of (4) with weights r_i/2
and its reciprocal. The first square sum is D_native; the second
is at most 2 sum_i||(s/2)F_i e_i||_infinity^2/c_*.

The phase part separately has bound
s a ||F||_infinity sqrt(N D_theta(f)). Completing the square against
-N^2 D_native-N^2 kappa_N D_theta proves

    log E_mu exp[bN int_0^T (phase drift+R_N)dt]
       <= C b^2 N T (1/kappa_N+d_N^2).                 (6)

Consequently the entire unwanted accumulated current is
superexponentially negligible at speed N. The weak-tilt L2 likelihood
transfer remains valid for the actual rates (1). The error in the
quadratic mobility compensator is bounded pointwise by s d_N/2.
Uniform ellipticity still supplies occupation replacement. Thus every
step of the receiving proof is preserved. Arbitrary phase initial
laws are covered by the same active initial layer; signs have the
same proof with their sign Dirichlet form.

Uniformly vanishing bond-mean errors are included in (1), as are
many reciprocal actuation errors. This is a population structural
statement. Establishing the uniform bound (2) from measurements is
a separate acquisition problem and cannot be asserted from a few
equilibrium measurements.

## 2. A directional error of order 1/N changes the capability

The reciprocal condition in (2) matters. Even without hidden phases,
consider the actual rates

    r_i=(s/2) exp[c(eta_i-eta_(i+1))/N], c nonzero.        (7)

Their absolute deviation from s/2 is O(1/N), tending to zero. Their
forward/reverse ratio is not one. From a macroscopically flat density
m, the ordinary weakly asymmetric exclusion limit gives

    Q_N(T) -> s chi(m)cT,                               (8)

rather than zero. Thus the original zero-centered rare-current law
cannot hold. A small amplitude bound alone is inadequate: a weak
directional bias accumulates over diffusive time. For this homogeneous
error family, suppressing its unintended macroscopic field requires
the physical directional exponent to be o(1/N), or its field must be
explicitly included and controlled as part of the target.

Equation (7) is an actual counterexample, not a purported free actuator
for the main construction. The same mathematical weak tilt is used
as a comparison measure in the receiving proof; those two roles must
remain separate. A general biased density/current action can have
additional structure and is not claimed here from the simple shift
of the typical current alone.

## 3. Ordinary calibration can erase an exponential assertion

Suppose the true model is in the admitted family only on a calibration
coverage event C_N, with probability at least 1-beta_N. A bound of the
form P(A_N)<=exp[-N I+o(N)]+beta_N gives no positive exponent when
beta_N is a fixed confidence failure probability. Retaining a record
of the calibration does not remove that probability or convert a
frequentist coverage event into a posterior guarantee.

An explicit mixture shows this is substantive. Let a calibration
branch select a system with mean s_0 with probability 1-beta and a
different mean s_1>s_0 with probability beta>0. Both means can have
the actual selectively controlled architecture. For q nonzero,

    P(|Q_N-q|<delta)
      =(1-beta) P_(s_0)(|Q_N-q|<delta)
         +beta P_(s_1)(|Q_N-q|<delta).                  (9)

As the neighborhood narrows after N grows, its exponent is

    min{q^2/[2s_0 chi(m)T], q^2/[2s_1 chi(m)T]},        (10)

which is the less costly s_1 branch, however small fixed beta is.
If beta_N=exp[-N J+o(N)], the two competing costs instead are
I_(s_0)(q) and J+I_(s_1)(q). A speed-N error budget needs to be compared
with the actual rare-event cost; a universal transfer of all
superexponential events needs a superexponential budget.

Useful honest alternatives are: a population theorem for a warranted
operation family; an explicitly conditional-on-coverage statement;
a deterministic robust interval of actions for every admitted s;
or acquisition whose actual failure exponent is carried into the
deployment claim. For s in [s_-,s_+], the pointwise population action
lies in [q^2/(2s_+chi(m)T),q^2/(2s_-chi(m)T)]. This interval does not
itself establish any conditional law of a calibration-selected device.

The preceding phase/current bounds are pointwise uniform in frozen z
and pre-existing records if future random inputs retain their stated
conditional laws and the admitted structural bounds hold. That
uniformity is useful, but it does not warrant those bounds for an
unmeasured selected device or repair an incorrect confidence budget.

## 4. Cost and physical scope

For N bonds, physical horizon N^2T and independent kicks at rate
gamma_N, the expected number of kick events is gamma_N N^3 T.
Native rates of order one give order N^3 T attempted native events
(the accepted count depends on occupancy). Arbitrarily slow divergence
of gamma_N is a mathematical limit, not a claim of negligible control
work or laboratory feasibility. Diffusion ports have their own energy,
bandwidth, isolation and noise costs, not a discrete-kick count unless
an actual implementation identifies one.

Sensing a signed current, guaranteeing reciprocal errors, calibrating
the common mean, keeping the desired conserved initial density and
maintaining independent local actuation are all actual suppliers.
Neither the rare-event theorem nor its conventional mathematical
comparison laws provide them free of charge.

Primary reference for (7)--(8): Bertini et al.,
https://arxiv.org/abs/math/0512394, Lemma 3.1, in the s=1 normalization;
Kipnis--Olla--Varadhan, DOI 10.1002/cpa.3160420202, is the earlier
weakly asymmetric hydrodynamic construction.
