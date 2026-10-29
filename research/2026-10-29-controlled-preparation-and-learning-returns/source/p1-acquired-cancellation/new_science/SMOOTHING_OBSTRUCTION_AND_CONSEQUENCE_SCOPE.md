# Smoothing prevents exact finite closure of a nontrivial sharp readout

29 October 2026. Root next attack after the acquisition and preparation theorems.
This is an ordinary proof of a consequential limitation of the proposed native
diffusion specialization, not a claimed new historical theorem about smoothing.
It changes which receiving consequence is justified. Approximate acquisition and
prediction survive; exact finite rank is not a generic property of diffusion.

## 1. Injective smoothing obstruction

Let X be a connected metric state space with a full-support probability pi.
Let T be an actual Markov kernel with these properties:

* T induces an injective bounded operator on L2(pi).
* For every bounded measurable v, Tv has a continuous version (strong Feller).

There is NO finite-dimensional subspace V of bounded measurable functions,
viewed modulo pi-null sets, that is T-invariant and contains 1_A for any A with
0<pi(A)<1.

Proof. Injectivity makes T|V one-to-one. A one-to-one endomorphism of a finite
dimensional space is onto. Therefore 1_A=Tu in L2(pi) for some bounded u in V.
The strong Feller property supplies a continuous version f of Tu. Since
f=1_A pi-a.e., f takes values in {0,1} pi-a.e. If its value at any point lay
outside {0,1}, continuity would give a nonempty open set of such values, of
positive pi mass by full support. Thus f takes values in {0,1} everywhere.
A continuous map from a connected space to {0,1} is constant, contradicting
0<pi(A)<1. QED.

The statement requires just ONE smoothing injective operation. A large menu,
controlled feature expansion, or a clever finite coordinate basis cannot
remove the obstruction while preserving that operation and the sharp readout.
It does not forbid a finite invariant span of smooth observables that excludes
the sharp observation effects. Such a span answers a different question.

## 2. Reversible diffusion and randomized-time operations

For a self-adjoint nonpositive Markov generator Q, T_t=exp(tQ), t>0, is
injective on L2(pi): its spectral multiplier exp(t lambda) is strictly positive
at every finite spectral value lambda. No bounded inverse on the full Hilbert
space is asserted or needed. A reversible diffusion whose actual positive-time
kernel is strong Feller therefore meets the obstruction whenever pi has full
support on a connected space.

The exponential-clock resolvent S=alpha(alpha I-Q)^(-1) is injective for the
same reason. If T_t is strong Feller for every t>0, S maps bounded functions to
continuous functions: omit the interval [0,epsilon], whose sup-norm contribution
is at most (1-exp(-alpha epsilon))||f||_infinity; the remaining integral is
continuous by bounded convergence. The uniform limit as epsilon decreases to
zero is continuous. Thus randomizing the duration does not cure finite closure.

In particular the zero-defect condition in COMMON_EQUILIBRIUM_OPERATION_ACCESS
cannot be met by any finite label-local dictionary for a nontrivial sharp
partition of such a diffusion. It remains a valid conditional theorem, and
the SAME acquired matrices still measure a nonzero approximation defect.

There is no contradiction with the finite/countable jump constructions, with
disconnected native state spaces, with a physically implemented noninjective
reset kernel, or with approximate finite-state diffusion models. Nor does this
prove impossibility of every conceivable nonlinear or infinite representation.
Its target is the finite linear effect space used in this tranche.

## 3. Explicit circle calculation: the measured defect is positive

Take Brownian diffusion on the circle with generator Q=d^2/dx^2 and uniform
pi=dx/(2pi). The actual kernel T_t is convolution with the periodic heat kernel.
Its Fourier multipliers exp(-n^2 t) are nonzero and its kernel is smooth, so the
previous theorem applies without any hidden regularity assumption.

Let A=(0,pi), ignore the two pi-null boundary points, and let
f=1_A-1_(A-complement). Then ||f||_2=1, pi f=0, and

    f(x)=(4/pi) sum_(n>=1 odd) sin(n x)/n      in L2(pi).

For V=span{1,f}, define

    a(t)=<f,T_t f>=(8/pi^2) sum_(n>=1 odd) exp(-n^2 t)/n^2.

The exact acquired centered leakage is

    ||(I-P)T_t f||_2^2 = a(2t)-a(t)^2 > 0,       t>0.

Indeed w_n=8/(pi^2 n^2), n odd, are positive and sum to1. The displayed
difference is the variance of exp(-n^2 t) under w. Keeping the pair n=1,3
in the identity Var(Z)=sum_(n<m)w_n w_m(Z_n-Z_m)^2 gives the explicit bound

    a(2t)-a(t)^2 >= [64/(9pi^4)](exp(-t)-exp(-9t))^2 > 0.

The defect can become small for a long actual wait; its strict positivity
does not imply a fixed error floor over all durations or dimensions. Waiting
changes the experiment, its actual time and the service interface. Infinite
future rank and useful finite-accuracy prediction are compatible.

## 4. Soft sensing is not automatically an exact-rank repair

Suppose a nondemolition sensor, when called without intervening state evolution,
has a conditional outcome probability p(x). Repeated calls have fresh independent
sensor noise conditional on the unchanged state. Their effect map is
M_p:v -> p v. If a finite-dimensional V contains1 and is invariant under M_p,
then 1,p,p^2,... belong to V. Some nonzero polynomial therefore obeys
P(p(x))=0 pi-a.e. Hence p has only finitely many essential values.

If p is continuous and nonconstant on connected full-support X, this is
impossible: continuity and full support imply P(p(x))=0 everywhere, while a
continuous nonconstant image of a connected space is not a finite set.

This proof concerns the DECLARED repeated sensor interface. It does not cover
a sensor with back-action, correlated noise, a mandatory intervening evolution,
or only a bounded number of readings. Those change the physical instruments
and must be analyzed as such. Softening a threshold while retaining arbitrary
fresh repeated sensing does not alone make exact finite closure available.

## 5. Receiving consequence and strong conventional comparison

The useful diffusion destination is acquired APPROXIMATE completeness for a
declared program class and accuracy, with observation/preparation costs attached.
The kernel-level finite-program defect bounds remain applicable. The exact
uniform-in-initial-state preparation theorem cannot be imported by calling a
small measured residual zero. A density/TV qualification, a genuine additional
reset operation, or a stronger acquired error geometry is needed.

Finite-state diffusion approximation is already a strong established route.
Kontoyiannis and Meyn, *Approximating a diffusion by a finite-state hidden Markov
model*, Stochastic Processes and their Applications127 (2017), 2482-2507,
DOI10.1016/j.spa.2016.11.004, prove a finite-state approximation under their
regularity/reachability and Lyapunov conditions. The author version's Theorem1.2
gives weighted-norm resolvent approximation and a uniform-in-time semigroup
estimate for smooth compactly supported test functions with a D^2g term. It
does not state the sharp-readout exact closure ruled out here, and its supplied
microscopic conditions are not automatically acquired from a coarse fit.
The proposed addition remains observable acquisition of the residual information,
not invention of finite-state approximation or semigroup reduction.

Primary author version read (28 November2016), pp1-6, especially Proposition1.1
and Theorem1.2:
https://www.dpmms.cam.ac.uk/~ik355/PAPERS/HMM.pdf

The ordinary proof above is self-contained. The primary paper is a comparator
and confirms the strong-Feller hypothesis in its stated diffusion setting;
none of its unseen technical lemmas is silently imported as a new dependency.

## 6. Research decision changed by this failure

Common equilibrium remains valuable: it removes the acquired word's growing
importance weights. It does NOT remove predictive rank or conditioning. For
connected smoothing diffusions, the immediate objective is now a controlled
finite-accuracy consequence, not an exact closing dictionary. A new physical
operation might alter injectivity or the observation instrument; its preparation
and execution would be part of the invention. For warranted jump sources, exact
operation closure and the prepared-law construction remain live possibilities.
