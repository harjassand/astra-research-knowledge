# Selective sources and mechanism choice

28 October 2026. Source reading for bounded-error acquisition of an entire
positive-energy intervention law, including baseline-dark controls. No
equipment, external writes, purchases, or outreach occurred.

## Current Astra sources actually used

The current repository revision supplied by the parent is
`ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2`. The following cards were read
directly there; their current copies are saved alongside this note.

- [N1082 current card](https://github.com/harjassand/astra-research-knowledge/blob/ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2/frontier/cards/N1082-observable-centered-gram-response-compiler.json).
  The governing `ASTRA_PRO3_GLOBAL_RESPONSE_ACQUISITION.md` was read directly
  from its local saved source, whose SHA-256 is
  `aebe53e9e530bc6bb3e1f30446ff4f942b9849303e992abaf5222f44a4a6a042`, matching
  the current card. Its leverage is the fixed affine-SPD rank-one class and
  the observable response quotient. Its exact acquisition divides by
  nonzero source-port couplings; a generic reference supplies almost-sure
  illumination, not a finite-grid noise-conditioning guarantee. Historical
  programme/result archives remain unacquired. The reported 510 calls are
  not newly executed evidence.
- [N1090 current card](https://github.com/harjassand/astra-research-knowledge/blob/ca9174c0692d6e2ee77a9a1cb3e65573bfeaf9c2/frontier/cards/N1090-matrix-concave-scalar-audit-and-excitation-limits.json).
  Its governing `ASTRA_PRO3_MATRIX_CONCAVE_CLASS_AUDIT.md` was fetched and
  read directly. The saved source has SHA-256
  `0fbfd812cecf613c61a2b77e77a6feb1eff563ef70de2c8a6136c057e0ebeb8a`, matching
  the current card. It already contains live finite-difference audits,
  task-directed line searches, and hidden-excitation failures. Repeating
  those operations would not establish full response transfer after the
  source becomes unavailable. Its nonlinear matrix-concavity premise is
  independently warranted, not inferred from passivity or finite data.

The current cards do not expose an independent whole-proof audit. Their
versioned scoped reviews and source-reported executions retain their actual
limits. No missing historical producer code has been reconstructed and
silently relabeled as original.

## Primary mathematical sources and existing implementations

### Positive resolvents and rational approximation

[Braess and Hackbusch, *On the approximation of Stieltjes functions by
exponential sums and rational functions with applications to partial
differential equations*, Numerische Mathematik 158 (2026),
doi:10.1007/s00211-025-01523-1](https://link.springer.com/article/10.1007/s00211-025-01523-1).
Read the integral representation, interpolation discussion, and stated
stability distinction. Positive-measure Stieltjes functions admit strong
rational approximation theory. The paper explicitly distinguishes algorithms
that preserve/use this positivity from generic AAA behavior. Its exact
function-approximation results do not supply a bounded raw-noise acquisition
certificate for the present multivariate source.

[Nakatsukasa, Sète and Trefethen, *The AAA Algorithm for Rational
Approximation*, SIAM J. Sci. Comput. 40 (2018),
doi:10.1137/16M1106122](https://epubs.siam.org/doi/10.1137/16M1106122).
Barycentric rational fitting with adaptively selected support points is
established prior machinery. The [baryrat implementation
documentation](https://baryrat.readthedocs.io/en/latest/) was inspected;
it exposes evaluation, poles/residues, derivatives, and numerator/denominator
conversion. An accurate sampled fit is not automatically a rigorous
all-dose bounded-error enclosure.

[Gosea and Güttel, *Algorithms for the rational approximation of
matrix-valued functions*, MIMS preprint (2021)](https://eprints.maths.manchester.ac.uk/2809/).
The authors compare AAA variants, RKFIT, vector fitting and Loewner-based
methods, including noisy data. Their reported noise sensitivity distinguishes
interpolation from approximation. This is a strong conventional comparison
family, not evidence that the present source has a known latent rank.

Official [pyMOR Loewner documentation](https://docs.pymor.org/2025-1-0/autoapi/pymor/reductors/loewner/index.html)
accepts sampled transfer-function values and constructs reduced models.
The [parametric AAA implementation](https://docs.pymor.org/2026-1-1/autoapi/pymor/reductors/aaa/index.html)
supports multivariate barycentric approximation but explicitly warns that its
assembled Loewner matrix has a product of per-variable sample counts in its
row dimension. These implementations exist; none was run or instrumented in
this continuation. Their fit tolerances are not substituted for deterministic
certificates.

### Positive measures and certified outer families

[de Klerk and Laurent, *A survey of semidefinite programming approaches to
the generalized problem of moments and their error analysis* (2018)](https://optimization-online.org/wp-content/uploads/2018/11/6924.pdf).
Read the compact-support measure programme, dual nonnegative-function
certificate, and finite atomic solution statements. This provides a
conventional rigorous framework for a noisy scalar Stieltjes ray: retain all
positive measures compatible with acquired intervals, rather than choose
unverified poles. The conditions for strong duality and atomic extrema need
to be checked for the actual constraint formulation.

[Drake's official sum-of-squares tutorial](https://drake.mit.edu/tutorials/sum_of_squares_optimization.html)
and [SumOfSquares.jl constraint documentation](https://jump.dev/SumOfSquares.jl/stable/reference/constraints/)
show existing polynomial nonnegativity/PSD modelling machinery. Clearing
positive rational denominators on a one-dimensional spectral interval turns
ray dual inequalities into univariate polynomial nonnegativity. Floating
SDP output still needs verified residual/PSD bounds or an exact dual
certificate before becoming an outward response guarantee.

### Determinantal structure

[Kulesza and Taskar, *Determinantal Point Processes for Machine Learning*,
arXiv:1207.6083v4](https://arxiv.org/html/1207.6083v4), Sections 2.2–2.4,
provides the classical positive principal-minor expansion and spectral
Bernoulli cardinality identity. Those identities led to the new determinant
tail derivation. The proof here independently spells out the required
coupling and does not import a stochastic detector model.

[Brylawski, *A Determinantal Identity for Resistive Networks*, SIAM J.
Appl. Math. 32 (1977), doi:10.1137/0132036](https://epubs.siam.org/doi/10.1137/0132036).
The accessible primary abstract states the classical relation between
conductance and positive tree-generating polynomial ratios. The full article
was not obtained or used as a missing proof step. Determinant positivity is
proved directly in the saved new argument; priority for the representation
itself is not claimed.

### Simplex interpolation

[Tobin Isaac, *Recursive, Parameter-Free, Explicitly Defined Interpolation
Nodes for Simplices*, SIAM J. Sci. Comput.,
doi:10.1137/20M1321802](https://epubs.siam.org/doi/10.1137/20M1321802)
describes symmetric simplex node constructions and links the
[recursivenodes implementation](https://tisaac.gitlab.io/recursivenodes).
The source treats the Lebesgue constant as a meaningful comparison, rather
than judging interpolation only by sample count. This is relevant to any
finite continuation of the determinant representation. There is no claim
that its low-dimensional node comparisons solve high-dimensional physical
acquisition or deterministic noise amplification here.

## Ray mechanism: useful, but insufficient for the full mission

For a fixed complete mixed command direction w>=0 with sum w_i=1,
diagonalizing K_w=diag(sqrt(w)) B diag(sqrt(w)) gives

    J(sw)=c0+integral_[0,kappa] s/(1+s lambda) dnu_w(lambda),
    nu_w>=0, nu_w([0,kappa])<=G^2.

Every calibrated raw scalar observation on that ray imposes a linear
constraint on the unknown positive measure and c0. Optimizing a later
response over all compatible measures gives an honest set-membership
enclosure without identifying weak poles or taking derivatives. Its dual
uses rational functions nonnegative over [0,kappa]; multiplying by the
known positive denominators gives a univariate polynomial certificate.
This is a plausible way to close a reusable one-parameter capability,
including mixtures containing dark controls.

It does not acquire angular dependence. Even complete noiseless curves on
fewer than n independent directions fail to identify all sources in the
simple B=0 subclass. The separate `inference_ray_obstruction.md` gives an
adaptive exact-query witness. Arbitrary-order sparse sign twins supply a
different obstruction when every complete actual command has limited
support. A dense shifted reference must be counted in that actual support.

## Selected stronger opening

The saved `inference_determinant_tail_theorem.md` treats the entire
multivariate response. It replaces the weak-coupling normalized Gram by

    F=N/D,
    D=det(I+B U),
    N=det(I+(B+gg^T)U)-D,

whose coefficients are nonnegative. Simultaneously truncating their total
degrees gives a globally valid rational function F_r satisfying

    0<=F-F_r<=F H_r(q),
    H_r(q)=(q^r/r!)/(sum_(j=0)^r q^j/j!), q=delta*kappa.

This rational, one-sided bound decays factorially for every fixed finite q,
admits dark couplings and arbitrary hidden rank, and is dimension-uniformly
sharp for this particular truncation. It removes the earlier small-q
convergence obstruction and gives positive linear constraints for an
acquired coefficient outer family. A second theorem bounds ambiguity after
ideal complete k-sparse information by `delta G^2 Pr(Poisson(2q)>=k)`.

The remaining obstruction is acquiring a narrow family economically.
Truncated coefficient storage grows as `sum_(j=0)^r binom(n,j)`; a direct
full interpolation design can still be prohibitively large and amplify
noise. Neither coefficient availability nor a globally successful adaptive
design is assumed. The parent's finite lattice/Bernstein route can use this
representation result where it helps; the present work does not substitute
an unexecuted acquisition theorem for that practical construction.

## Equally informed conventional comparison and complete costs

The strongest comparator is allowed the same calibrated scalar intervals,
source/actuator bounds, mixed-action interface, positivity, and retained
data. It can use Stieltjes moment bounds, robust rational fitting, positive
determinant coefficients, and exactly the same truncation/LP certificates.
It therefore ties the mathematical operation. Generic unverified AAA is
not the only permitted comparator, and there is no demonstrated practical
or historical-priority advantage.

Any future implementation must charge every new source reaction, baseline
and calibration standard, failed or exploratory query, complete command
support and writes, preparation/settling/reset, instrument resolution,
readout energy, elapsed time, coefficient storage, bit growth, and verified
optimization. A finite approximation degree is a precision decision, not
an acquired exact rank or exact source-class certificate. The warrant for
kappa remains essential: the retained raw-response saturation obstruction
rules out a scale-uniform finite-query guarantee without such information.
