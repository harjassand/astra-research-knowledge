# Receiving attack: adaptive hidden-ensemble information cost

30 October 2026. Existing physical-mechanism role. No new worker or fixture.

Reviewed actual input:
ADAPTIVE_INFORMATION_COST_OF_HIDDEN_ENSEMBLE_VALIDATION.md

SHA256:
2d46dca2999c651f207f8e0a3f4f4140e2e9d7defc12254d50959a54756de427

Bytes: 10034. Exact input preserved as
ADAPTIVE_INFORMATION_COST_REVIEWED_2d46dca2999c.md.

## Verdict and required interface clarification

The actual generator, density calculation, continuous-observation filter,
every-history invariant, stopped active-time information inequality and
binary-test lower bound are correct. The resulting fourth-order
precision exponent matches the elementary echo upper bound at the
specified acquisition interface. The ordinary solver is genuinely
allowed the complete parametric family, exact filter, continuous visible
jump times, adaptive switching and arbitrary computation.

Acceptance is conditional on the following explicit preparation-instrument
clarification, agreed by root for a separate binding correction:

**Every exposed preparation record, including completion time, must have
the same conditional law under the two hypotheses, and must not reveal
the previous hidden bit or the newly generated b seed. A separate
theta-independent fixed-protocol uniform initializer with hidden thermal
b-generation marks supplies this interface.**

Equality of the returned state distribution and visible label alone does
not suffice. A sampler that returns the same uniform state but encodes
theta in its clock gives a zero-active-time counterexample. A sampler
that reports the old b before replacement adds the excluded hidden
readout. These are substantive information ports, not a failure of the
four-state calculation.

If several specimens may be used simultaneously, their native noises
must be independent conditional on the fixed source hypothesis, with
fresh independent initialization at the stated conditional interface.
Alternatively the theorem can be restricted to a sequential single
specimen. Individual marginal generators alone do not define a
correlated multi-specimen bath experiment. With independent copies the
proof permits arbitrary parallelization and sums their active times.
It is a total-active-time bound, not a wall-clock lower bound against
unlimited parallel hardware.

## 1. Generator and actual preparation distance

The Walsh perturbation gives exactly the three displayed jump rates.
For theta<=1/4 the minimum off-diagonal rate is 1/8 and the maximum
3/8. The operator sends a to -a+theta b, b to -b+theta a, ab to -ab,
and constants to zero. Its gap is 1-theta>=3/4; no hidden slow-mode
assumption is being exploited.

The one-unit output from density 1+a is
1+e^(-1)[cosh(theta)a+sinh(theta)b]. The reference is
1+e^(-1)a. Writing A=cosh(theta)-1 and B=sinh(theta), one has B>A>=0.
The sign of the density difference is therefore b. Averaging its
absolute value over the four states gives
TV=e^(-1)B/2. Orthogonality of the Walsh functions gives
D=e^(-2)(A^2+B^2), and the three echo entries in the reviewed proof
reduce to that expression.

There is no erroneous conversion between visible endpoint distance
and full-state distance: the former is e^(-1)A/2, of second order.
The supplied swap/read port, if added, attains the full-state TV exactly.

## 2. Filter, including every visible jump time

At fixed current a the two hidden states have visible intensities
1/2-qa b/2. Averaging gives
lambda=1/2-qa h/2.

Unobserved b-only flips at rate 1/4 contribute -h/2 to the filtered
mean drift. The no-visible-jump update contributes
-Cov(b,lambda)=qa(1-h^2)/2. This yields the stated ODE.

At a visible flip, the b-preserving a-only event contributes h/4 to
the unnormalized new-b mean. The simultaneous a,b flip contributes
-h/4+qa/2. Their sum is qa/2 and the event probability rate is
(1-qah)/2, giving h_after=qa/(1-qah).
Observing which of those native events occurred would change this
filter and is explicitly outside the interface.

At h=+2epsilon the ODE points inward with drift at most -epsilon/2.
At h=-2epsilon it is at least epsilon/2. The jump map has magnitude
at most epsilon/(1-2epsilon^2), strictly less than 2epsilon.
Predictable switching changes neither state nor posterior
instantaneously. Fresh qualified initialization gives h=0.

Thus all visible histories generated from the stated initial interface,
including rare histories selected adaptively, obey |h|<=2epsilon and
|lambda-1/2|<=epsilon^2 u. There is no discarded timing information.
If controls are randomized, condition on the independent controller
seed; no bath or hidden preparation seed is exposed by that step.

For independent simultaneous specimens, conditioning on their complete
records fixes all realized controls. The native hidden-path likelihoods
factor by specimen, and the same bound applies to every individual
conditional intensity. Joint adaptive commands do not invalidate this
argument.

## 3. Complete observed likelihood and stopping

Under the null, visible flips have constant intensity 1/2 for every
controller command. Under the alternative, the full observed intensity
is the filtered lambda above. A fixed controller contributes the same
conditional command/seed factors under both hypotheses. The complete
theta-independent initializer contributes no relative-entropy term
under the required clarification.

The visible point-process log likelihood on a bounded observation
interval is

\[
 \ell=\int\log(\lambda/\lambda_0)\,dN
             -\int(\lambda-\lambda_0)\,dt.
\]

Taking alternative expectation gives

\[
 {\rm KL}=\mathbb E_\epsilon\int
 [\lambda\log(\lambda/\lambda_0)-\lambda+\lambda_0]\,dt.
\]

Since log z<=z-1,
the integrand is at most
(lambda-lambda_0)^2/lambda_0<=2epsilon^4 u.
During actual baseline waiting q=0, lambda=1/2 even when h is not zero,
so waiting does not reveal hidden information at zero active-time cost.

For unbounded stopping, take bounded truncations of the complete
record. Their relative entropies are uniformly bounded by
2epsilon^4 E_epsilon T_active when that expectation is finite.
Relative entropy on the increasing record sigma-fields converges to
that on the complete well-defined record; alternatively the likelihood
martingale has the corresponding uniform entropy bound. Subsequent
stopped output is a measurable function of that record.
This yields the stated inequality without assuming a fixed deterministic
trial horizon or suppressing failed/aborted attempts.

If E_epsilon T_active is infinite, the lower bound is already satisfied.
Any certification procedure still needs an actual well-defined output
decision with the declared success probabilities.

## 4. Testing lower bound and exact scope of matching

Let rejection probability be p under the alternative and q under the
null. The required p>=1-alpha and q<=alpha imply

\[
 {\rm kl}(p,q)\ge
 (1-2\alpha)\log[(1-\alpha)/\alpha].
\]

Combining with the likelihood bound proves the displayed
epsilon^(-4) active-time lower bound, with its stated alpha factor.
Since the actual full-state separation is comparable to epsilon on
(0,1/4], the precision exponent is also fourth order in that separation.

This proves a useful-certifier lower bound: exact-null acceptance
and separated-alternative rejection are both required. It does not
apply to a procedure that declines every certificate. The elementary
three-echo estimator has matching precision and confidence exponents
at bounded input ceiling and fixed word durations, although neither
constants nor complete apparatus cost are matched here.

The solver is not artificially denied a known family or an optimized
likelihood estimator. The filter-bound proof already permits both.
New hidden sensors, marked bath events, correlated extra physical
ports or a hypothesis-bearing initializer invalidate the claimed
interface and must not be silently added to either side.

## 5. Same-source operational metric: constructive proof completed

The companion SAME_SOURCE_AVAILABLE_METRIC_GAP.md proves the proposed
stronger distinction between full-state TV and the original available
future menu.

For a fixed visible transcript, the killed waiting matrix is symmetric
and the visible-jump matrix obeys J_a(q)^T=J_-a(q). Transposing its
product turns the posterior mean of the initial b into the final
mean of a normalized reversed matrix recursion. The same invariant
[-2epsilon,2epsilon] applies to that recursion.

An important detail is preserved: reversing a feedback controller does
not generally yield a causal controller. In particular, an instantaneous
post-jump command change cannot replace the original pre-jump control
inside the transposed jump matrix. The proof uses a uniform matrix
invariant for arbitrary waiting and jump control values, so it does
not need a physically implemented reversed feedback schedule.

For every permitted common future controller,

\[
 d_{\rm available}(\rho_\epsilon,\rho_0)
 \le \frac{e^{-1}}2[
 \cosh\epsilon-1+2\epsilon\sinh\epsilon].
\]

The immediate a read supplies the lower bound
e^(-1)(cosh(epsilon)-1)/2. Hence the original-menu operational distance
is Theta(epsilon^2), while full-state TV is Theta(epsilon).
The proof covers stopping and complete infinite records by conditional
expectation and bounded martingale convergence, with the complete
initializer/noise qualifications stated above.

This same-source statement compares initial states fed to one common
future controller. It does not include an exposed preparation identity
or grant repeated new copies of the unknown candidate initial law.
Those would be different statistical experiments.

## 6. Disposition

The reviewed proof is mathematically accepted under the explicit
complete-initializer and, where applicable, independent-copy conditions
above. Root has agreed to preserve the initializer correction separately.
This receipt does not silently modify the pinned input or accept an
unseen later version.

No priority, apparatus realization, universal thermodynamic lower bound,
or practical speedup is accepted. The constructive significance is the
declared physical information bottleneck and the precise objective
separation that explains it.
