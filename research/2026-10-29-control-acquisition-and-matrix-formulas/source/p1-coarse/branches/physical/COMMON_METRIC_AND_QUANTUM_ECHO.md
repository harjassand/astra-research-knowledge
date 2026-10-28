# Physical realization and common-metric limits for scalar echoes

28 October 2026. Focused support and challenge for the root construction.

## 1. One fixed energy metric is the load-bearing physical premise

Consider a linear heat or RC network

    C xdot = -L_i x,

with the SAME positive definite capacity matrix C for every selected mode i,
and symmetric positive semidefinite conductance matrices L_i. For dwell time
tau_i>=0,

    A_i=exp(-tau_i C^-1 L_i)

is selfadjoint and contractive in the common inner product <x,y>_C=x^T C y.
Indeed C^(1/2) A_i C^(-1/2)=exp(-tau_i C^(-1/2)L_i C^(-1/2)) is symmetric with
spectrum in[0,1]. A conservation mode at eigenvalue1 does not invalidate
contractivity.

A fixed pulse profile v injects b=C^-1v. The matched scalar readout is v^T x,
which equals <b,x>_C. Reset to equilibrium, apply the same calibrated pulse,
execute the selected sequence of modes, and read the matched port. This
physically measures f(w)=<b,A_wb>_C, up to the calibrated pulse amplitude.

Reversing the ORDER of dissipative modes implements the adjoint product because
each primitive is selfadjoint. It does not require inverse diffusion or a
thermodynamic reversal of an individual relaxation.

The construction warrants the common metric without identifying every entry
of C or L_i. It still assumes the fixed-capacity linear source law, reproducible
equilibrium reset, matched source/read profile, stable dwell times and scalar
calibration. Passive behavior alone does not warrant it. Actuation that changes
capacities, moves state coordinates or adds active feedback can violate it.
In a continuum system a point impulse may have infinite energy norm; use an
actual finite-energy source/read profile rather than a formal delta function.

## 2. Individually reversible primitives need not have a common metric

Let pi_1=(3/4,1/4), pi_2=(1/4,3/4), and A_i=1 pi_i^T. Each A_i is a reversible
Markov idempotent and an orthogonal contraction in metric diag(pi_i). But
A_1 A_2=A_2 and A_2 A_1=A_1. For b=e1 and readout b^T x, the alleged echo Gram is

    G=[[3/4,1/4],[3/4,1/4]].

It is not symmetric. Symmetrizing gives

    (G+G^T)/2=[[3/4,1/2],[1/2,1/4]],

with determinant -1/16. Thus symmetrization is not a sound repair. There is
no positive common metric making both maps selfadjoint: they would then be
orthogonal projections onto the SAME range span{1} and would have to coincide.

Passing finitely many reverse-word equalities does not establish common
selfadjointness on untested hidden directions. Such checks can falsify a
premise; a structural warrant or stronger acquisition argument is still needed.

## 3. A clean quantum family: nonselective Lueders measurements

For each chosen POVM {E_iy}, define

    Phi_i(X)=sum_y sqrt(E_iy) X sqrt(E_iy).

This is CP, trace preserving, unital and selfadjoint in the SAME Hilbert-Schmidt
inner product Tr(X^*Y), irrespective of its unknown measurement basis. It is a
Hilbert-Schmidt contraction: the Schwarz inequality for unital CP maps gives
Phi_i(X)^*Phi_i(X)<=Phi_i(X^*X), and trace preservation completes the proof.

Take b=|psi><psi|. Prepare psi, apply selected nonselective measurement channels,
then measure survival effect b. The actual Bernoulli probability is

    f(w)=Tr[b Phi_w(b)].

For a convention in which Phi_w denotes the mathematical product of primitive
maps, reversing a word gives Phi_rev(w)=Phi_w^*. Hence

    f(rev(v)w)=<Phi_v(b),Phi_w(b)>_HS.

The root's Gram/one-step/double-step construction therefore has a direct
quantum realization without microscopic process tomography. Pure-state
preparation and the matched survival test must actually be available.
Preparing a visible qubit does not prepare an inaccessible environment;
environmental memory that later re-enters invalidates a memoryless channel
description unless included in the hidden state and reproducibly reset.

Unknown bases can give noncommuting channels. Not every familiar dephasing
example does: Pauli conjugations can commute as superoperators even when their
unitaries anticommute. Check the actual superoperator commutator in examples.

Specified Lueders outcome maps X->sqrt(E_y) X sqrt(E_y) are also selfadjoint
contractions, but an outcome is not a freely selectable deterministic actuation.
Echo estimates for prescribed outcome words pay their probabilities. Conditional
prediction divides by the observed-event probability, so an unconditional joint
probability bound does not establish a relative rare-event guarantee.

Each f(w) can be estimated by survival trials. For K acquired entries, Hoeffding
plus a union bound requires O(eta^-2 log(K/delta)) repetitions per entry for
absolute accuracy eta with simultaneous confidence1-delta. Each repetition
pays reset, preparation, every primitive in the word and readout. This is an
elementary complete-cost baseline, not an optimality claim. Leakage is a
difference of measured moments and can demand much smaller eta than the
requested final probability tolerance.

For example, if a scalar word bound scales as m^2 ell^2, certifying tolerance
epsilon at horizon m asks for leakage-square resolution of order epsilon/m^2.
Independent bounded survival observations can then require order
m^4/epsilon^2 trials per moment before conditioning factors. This is a scaling
warning under this particular estimator and bound, not a universal lower bound.
An efficient query count does not supply that precision. A device realizing
the same POVM probabilities can also apply hidden post-measurement feedback;
the Lueders instrument, not merely its outcome POVM, is the warranted premise.

## 4. Thermal detailed balance is a qualified extension

Heisenberg primitive maps T_i may be selfadjoint in the common KMS product

    <X,Y>_sigma=Tr[sigma^(1/2) X^* sigma^(1/2) Y].

The SAME faithful stationary sigma must work for every primitive. Selfadjoint
Markov semigroups are contractions in this metric. Distinct thermalizations
with different Gibbs states do not automatically meet the premise.

For positive bounded probe B, the matching state is

    rho_B=sigma^(1/2) B sigma^(1/2)/Z,  Z=Tr(sigma B),

and the matching readout is B, scaled to an effect if necessary. Applying the
Schrodinger channel dual to T_w gives expectation <B,T_w B>_sigma/Z. This
thermal-sandwich preparation and its normalization are additional operations,
not consequences of merely knowing that detailed balance holds. Unknown
Gibbs states or small Z can defeat the desired cost advantage. Infinite-
temperature Lueders channels avoid this weighted-preparation issue.

## 5. Primary baselines and the actual-addition test

1. Petreczky, Bako, van Schuppen, *Realization theory of discrete-time linear
   switched systems*, Automatica2013,
   https://doi.org/10.1016/j.automatica.2013.07.022 . Noncommutative Hankel
   matrices characterize finite realization and construct states from
   input-output data.
2. Gosea, Petreczky, Antoulas, *Data-Driven Model Order Reduction of Linear
   Switched Systems in the Loewner Framework*, SISC2018,
   https://doi.org/10.1137/17M1120233 . Generalized transfer data produce reduced
   models without original system matrices; a code supplement accompanies it.
3. *A posteriori error estimation for model order reduction of parametric
   systems*,2024, https://doi.org/10.1186/s40323-024-00260-8 . Primal-dual output
   error bounds multiply primal and dual residuals. Quadratic output error
   alone is not a new generic principle.
4. *Krylov subspace methods for estimating operator-vector multiplications in
   Hilbert spaces*,2021, https://doi.org/10.1007/s13160-021-00460-4 . Data-based
   kernel Gram calculations and projected operator approximation are prior art.
5. Liu et al., *The role of randomness in unentangled quantum state
   certification*, PMLR247(2024), Fact14,
   https://proceedings.mlr.press/v247/liu24a/liu24a.pdf . Explicitly establishes
   Lueders selfadjointness, Hermiticity preservation, trace preservation and
   unitality.
6. DeBrota and Stacey, *Lueders channels and the existence of symmetric-
   informationally-complete measurements*, PRA100062327(2019),
   https://doi.org/10.1103/PhysRevA.100.062327 .
7. *Efficient Quantum Gibbs Samplers with Kubo-Martin-Schwinger Detailed Balance
   Condition*,2025, https://doi.org/10.1007/s00220-025-05235-3 . Distinguishes
   GNS/KMS metrics and defines detailed balance in the selected metric.
8. Nielsen et al., *Gate Set Tomography*, Quantum5,557(2021),
   https://arxiv.org/abs/2009.07301 and
   https://doi.org/10.22331/q-2021-10-05-557 . Linear-inversion GST already uses
   fiducial Gram matrices and single-gate insertion matrices to recover gates
   up to a gauge. The experimental data interface is a particularly close
   comparator; sufficient informational completeness is a load-bearing input.
9. Klep, Povh, Volcic, *Minimizer Extraction in Polynomial Optimization Is
   Robust*, SIOPT28(2018),3177-3207,
   https://doi.org/10.1137/17M1152061 ; author's manuscript:
   https://igorklep.codeberg.page/files/cont_gns_rev1_24may18.pdf . Section2.2
   constructs orthogonal compressed operators from a positive word-moment
   matrix; Equation2.6 is the whitened insertion-matrix formula. Section4.2
   uses a canonical flat block completion and its Schur residual without
   assuming that a nearby flat Hankel completion exists. Lemma4.3 bounds word
   mismatch within the supplied extension degree. This is very close algebraic
   prior art. The root's arbitrary-future-word claim needs to be distinguished
   by its actual finite acquisition, source contractivity and leakage bound,
   rather than by claiming a new general Gram or GNS construction.

The defensible potential addition of the root construction is the complete
experimental route from matched scalar echoes to an actual orthogonal
compression AND a PSD one-step leakage certificate, followed by a bound for
every future switched word without an assumed hidden rank cutoff. An ordinary
Hankel interpolant, a state-access Krylov method, and a known-model residual
bound are strong but differently informed comparators. No superiority follows
from restating their projected equations in different vocabulary.
