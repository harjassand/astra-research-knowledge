# Independent whole-review of the quantized Maxwell receiver

29 October 2026. Read-only intake of root_quantized_collision/{PROOF.md,
quantized.py,consume.py,EXECUTION.json,EQUILIBRIUM_CONTROL.md,equilibrium.py,
EQUILIBRIUM_EXECUTION.json}, together with the previously accepted direct
complex/finite-kernel derivations. No producer module or sample grid is rerun
by this review. Expected-work strengthening is treated separately below.

## Exact target and whole program

ACCEPTED analytically at the stated conditional scope: under iid fair bits
and convergent outward Arb/acb arithmetic, the program terminates almost
surely and returns exactly the integer-bin pushforward of the declared
Maxwell/covariance-mixture model at a nonnegative rational time. This is not
an exact continuous-valued machine output, empirical model acquisition or
hard-sphere receiver. It consumes the fixed rational four-rotation kernel
and the exact positive singleton program; no Haar sampler is hidden.

I checked the code and proof in full. The two initial covariance catalogs
in Receiver and consume.initial agree: cI+h E gives diag(1,21/20,11/10) or
the stated rational 2x2 block and 21/20 third entry. Transpose quadratics,
Hermitian child norms, occupied-only normalization and the Poissonized
phase/covariance constants agree with the earlier complete-law theorem.
The finite singleton applies its four exp(-left/4) coins also when left is
a computable real, not merely a rational time. Categorical denominators and
weights are exact integers; the runtime group map uses the correct transpose.

Every Uniform owns one persistent prefix. Cached coarse enclosures remain
valid after later refinement, although they can waste already acquired bits.
Normal inversion reuses its one uniform through rational-CDF bisections.
Inverse-Poisson comparisons reuse one uniform and increasing cumulative
probabilities. Fresh variables are not resampled after unresolved comparisons.
Strict upper/lower ball comparisons control every noninteger branch. Generic
integer powers were correctly replaced by polynomial multiplication, including
exact-zero components and negative powers of a strictly positive factory base.

The Huber factory preserves its multiplier-two martingale with geometrical
increment, the epsilon clamp, the threshold computed before that clamp, and
the subsequent multiplier/margin updates. Source primary: Huber1308.1562v2,
Section 2.2. The countable radial threshold/clamp equalities have zero Gaussian
proposal mass. Other fresh-uniform comparisons have zero equality probability;
Normal inversion uses countably many fixed CDF thresholds. Gaussian mixture
covariance at least I removes bin-boundary mass. These facts, plus finite ideal
genealogy/factory work, prove almost-sure termination of all strict refinements.
They do not by themselves prove finite expected bit work.

The actual seeded executions and previous failed NaN path are retained as
implementation diagnostics only. Their bounded maximum observed precision
is not a precision theorem. A diagnostic limit, when enabled, raises a
failure instead of returning a fallback value. The production path has no
such limit. No independent physical or PRNG-iid qualification is implied.

## Equally informed ordinary controls

consume.ordinary_wild has the same initial Gaussian catalog, signed quarter-
turn law and integer bins. Its stack ordering combines the two independent
children correctly. Swapping their order or R/R^T does not alter this
inversion-symmetric catalog. Its exponential leaf debt is a property of this
ordinary recursion, not a lower bound on all algorithms.

ACCEPTED analytically: EQUILIBRIUM_CONTROL.md gives a paid ordinary finite-
accuracy alternative. I reconstructed its full argument. The traceless
symmetric mean generator is self-adjoint in Frobenius norm and has gap1/4.
For a quarter-turn, A^T A and B^T B give the asserted diagonal coefficients
3/4,3/4,1/2 after averaging axes and off-diagonal coefficient1/2. Thus its
within-copy quadratic term is <=3V/4. Independent-copy cross terms cost at
most2||M||_F^2, so V_t<=9V0 exp(-t/4). No centered/fluctuation covariance is
confused with the raw D second moment here.

For Sigma,mu I>=aI, the Gaussian KL formula and the scalar Taylor estimate
with second derivative1/x^2<=1/a^2 give KL<=||Sigma-mu I||_F^2/(4a^2).
Pinsker, mixture convexity and Cauchy--Schwarz then give exactly
TV<=3sqrt(V0)/(2sqrt(2)a) exp(-t/8). Quantization contracts this TV bound.
The exact mu=157/150,V0=1/240 and conservative 1/5 prefactor are consistent.
The t>=100,epsilon=1e-6 contract therefore follows. The single-Gaussian
alternative prevents a practical long-time advantage claim based only on
the exact Wild tree's exploding leaves. It is approximate transient output,
whereas the main program's target is exact bin-law output.

## Finite mean gate

The previous almost-sure claim is accepted at its actual scope. A finite
mean proof must separately pay occupied-child conditioning, adaptive Gaussian
inversion, reused factory thresholds and final floors. EXPECTED_BITS.md
records the independent stronger analysis, with exact algebraic checks in
certify.py. Its assumptions and distinction between fair-bit consumption,
arithmetic implementation and an explicit numerical bound are retained.

## Changed evaluator intake

The original recursive arithmetic evaluator failed the finite-depth control
in DEPTH_CONTROL.json. The repaired source has been whole-read: all arithmetic
operators declare dependencies, and at(p) evaluates their postorder with an
explicit stack. Only leaf providers call their scalar subroutines. Normal
leaf evaluation invokes constant-depth Uniform/CDF comparisons and does not
reenter genealogical arithmetic depth. No unbounded arithmetic recursion
remains. The same independent1500-addition control now succeeds at recursion
limit1000; its receipt binds source SHA256
ba8202e02d8dd3e2fd85747ec726348ea78255337e2bffe6083d6d9ca6d41902.
The producer's depth10000 and unchanged-seed600-output replay remain distinct
producer evidence, not an extra independent sampling grid.

ACCEPTED after this correction at the mathematical output/conditional outward-
arithmetic scope above. Finite expected work is constructed in EXPECTED_BITS
and ELEMENTARY_INTERVAL_MODEL at the explicit polynomial elementary-interval
bit-machine scope. No numerical worst-case bound for a particular Arb build
or practical all-solver advantage is implied.
