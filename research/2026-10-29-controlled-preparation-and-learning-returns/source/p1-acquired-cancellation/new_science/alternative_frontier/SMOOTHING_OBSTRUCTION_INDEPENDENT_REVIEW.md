# Independent ordinary review: smoothing obstruction and consequence scope

29 October 2026. PASS at the source snapshot below. No substantive correction
is required. This is a review of the new obstruction, not of earlier fixtures,
the quantitative approximation companions, or the indexed literature comparator.

Reviewed source: `../SMOOTHING_OBSTRUCTION_AND_CONSEQUENCE_SCOPE.md`.

SHA256: `3de09bbffb02238cc676ec00f862ced2d4e12864d5f1260319b3408f320672d5`.

The reviewed version states that X is a connected METRIC state space. All
continuous-version and initial-support qualifications below refer to that
version. A frozen copy is retained in `reviewed_versions/`.

## 1. The finite sharp-readout obstruction passes

Injectivity of T makes its endomorphism on finite-dimensional invariant V onto.
Thus the sharp effect 1_A has a preimage u in V. The stipulated boundedness of
the features lets strong Feller smoothing give a continuous version f of Tu.
If f were outside {0,1} at any point, continuity would produce a nonempty open
set on which it stays outside {0,1}. Full support makes that set have positive
pi measure, contradicting f=1_A almost everywhere. Hence f is globally
{0,1}-valued; connectedness makes it constant, contradicting 0<pi(A)<1.

There is no loophole from modifying an indicator on a pi-null boundary, or from
choosing a different continuous version. Full support makes two continuous
versions agreeing almost everywhere agree everywhere.

Even an unbounded-coordinate change does not evade this particular obstruction
if it proposes a finite T-invariant L2 space containing 1_A. The cyclic subspace
span{T^n 1_A:n>=0} lies inside it, is finite dimensional and T-invariant, and
consists of bounded functions because T is Markov. The reviewed bounded-space
argument applies to that subspace. This is an optional strengthening, not a
dependency needed by the source proof.

One such operation is enough. Additional operations, coordinates or adaptive
feature choices cannot produce common exact finite closure while retaining the
same smoothing operation and sharp effect.

## 2. Reversible semigroup and exponential-clock corollaries pass

For a self-adjoint nonpositive generator, the spectral multipliers exp(t lambda)
and alpha/(alpha-lambda) are strictly positive at every finite spectral value.
Their squared spectral integrals can vanish only for the zero vector. This proves
injectivity without asserting a spectral floor or a bounded inverse. The
unbounded negative spectrum of a diffusion causes no exception to this argument.

On a metric space, the stated bounded-convergence argument for the resolvent is
valid for the actual measurable Markov semigroup: along x_n -> x, the positive-
time strong-Feller versions converge for each time, and the Markov bound supplies
domination. The omitted initial time interval has uniformly vanishing mass.

A useful version-safe proof of the same conclusion is

    S_epsilon f = exp(-alpha epsilon) T_epsilon S f,
    ||S f-S_epsilon f||_infinity
        <= (1-exp(-alpha epsilon)) ||f||_infinity.

Here S_epsilon is the resolvent integral restricted to times at least epsilon.
It has a continuous version because S f is bounded and T_epsilon is strong
Feller. If only almost-everywhere versions are being used, differences of these
continuous versions have the same supremum and essential supremum by full
support. They are therefore uniformly Cauchy and converge to a continuous
version of S f. This avoids any unnoticed assumption of joint continuity in
time and state. The actual exponential-clock operation still presupposes an
ordinary measurable transition semigroup, as the physical formulation does.

Consequently a randomized duration does not remove the obstruction. Conversely,
these statements do not provide the positive spectral floor used by earlier
bounded-generator error estimates. The source correctly directs diffusion work
to the applicable kernel-level finite-program bounds.

## 3. The circle variance and explicit lower bound are exact

For Q=d^2/dx^2 and uniform circle measure, the displayed square-wave Fourier
series has coefficients 4/(pi n) on odd sine modes. Since each sine has squared
L2 norm 1/2, its spectral weights are w_n=8/(pi^2 n^2), summing to1.
The constant mode vanishes. Projection of T_t f onto span{1,f} is therefore
a(t)f, while ||T_t f||_2^2=a(2t). The residual is exactly

    a(2t)-a(t)^2 = Var_w(exp(-n^2 t)).

The nonnegative pairwise variance identity applies to the countable weights.
Keeping n=1 and n=3 gives precisely

    [64/(9 pi^4)] [exp(-t)-exp(-9t)]^2,

which is strictly positive for every finite t>0. The pi-null endpoints of the
half-circle do not alter the L2 calculation or the no-go. No numerical evidence
or unverified regularity lemma is required.

There is no duration-independent positive lower bound: the displayed residual
tends to zero for long waits, and also for t decreasing to zero. Thus strict
nonclosure does not imply that a fixed-accuracy task is difficult or expensive.

## 4. Repeated soft sensing is correctly scoped

For a nondemolition sensor with unchanged hidden state and fresh conditionally
independent noise, the all-success effect of m calls is p^m. Invariance under
M_p and inclusion of1 therefore put all powers of p into V. Finite dimension
gives a nonzero polynomial relation P(p)=0 almost everywhere. Its finitely many
real roots contain the essential range of p.

If p is continuous, full support upgrades that polynomial identity to every
point. A continuous nonconstant image of connected X cannot be finite. This
establishes the soft-sensor obstruction independently of any dynamical smoothing.

The physical qualifications in the source are essential and correctly retained:
back-action, correlated sensor noise, mandatory source evolution between calls,
or a bounded reading budget change the effect algebra. In particular, replacing
a deterministic threshold by a noisy continuous response does not resolve exact
rank while unlimited fresh repetitions on an unchanged state remain available.

## 5. Initial support and actual access do not yield an unmentioned escape

Full support is substantive. For example, on connected X=[0,1], take
pi=(delta_0+delta_1)/2 and

    T f(x)=(1-x)f(0)+x f(1).

This kernel is strong Feller and is the identity on the two-dimensional L2(pi),
hence injective there. A nontrivial sharp endpoint label has exact finite
closure. The example is excluded because pi does not have full support; its
effective supported state space is disconnected. A connected ambient coordinate
space alone would therefore be insufficient. The reviewed source includes the
needed full-support hypothesis.

The theorem concerns a finite invariant effect space that includes the declared
sharp readout. It is not a general impossibility claim about predicting one
stationary marginal, a prescribed bounded list of outputs, or every possible
nonlinear representation. Density/TV restrictions can help control approximate
service error; they do not magically make a common finite effect space satisfy
the theorem's unchanged exact hypotheses.

A reset can enable preparation or a smaller program class. Simply adding an
optional noninjective reset does not permit common finite closure if the old
injective smoothing call and sharp observation remain available. Making reset
mandatory, replacing a call by a reset-containing composite, or changing the
instrument changes the actual operation family. Section1 already states the
scope that prevents an incorrect interpretation of the later reset discussion.

Finally, the result needs only the sharp observation at an allowed endpoint; it
does not assume that the thresholded diffusion has finitely many label jumps or
a bounded-jump path representation. Such a representation must not be imported
from finite-rate CTMCs. The source's stated kernel-program receiving consequence
keeps this distinction.

## Decision

The obstruction justifies changing the connected smoothing-diffusion destination
from an exact closing dictionary to a declared finite-accuracy consequence, or
to a genuinely changed physical interface. It does not invalidate the exact
conditional acquisition theorem for other source classes, or its nonzero
measured residual as information about approximation. The literature comparator
was not re-audited here; the reviewed ordinary proofs are self-contained.
