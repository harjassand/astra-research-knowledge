# Exact-input Jacobi quadrature certification

## Interface and scope

`src/certified_jacobi.py` is a standalone Python-standard-library implementation.
The input is an n by n real symmetric tridiagonal matrix J with diagonal a_i/D
and positive off-diagonal b_i/D, where all a_i and b_i are integers and D is a
positive power of two (default D=2^32). Initial intended dimensions are n<=64.
The certifier and verifier do not import NumPy, SciPy or a numerical eigensolver.

`certify_jacobi(a, b, D)` returns a JSON-safe dictionary. Every root has exact
rational/dyadic lower and upper bounds in both the scaled integer coordinate and
the physical J coordinate, an exact Sturm index, and Decimal lower/upper bounds
for its e_1 spectral weight. Defaults are 140 fractional bits in the integer
coordinate and 100 Decimal significant digits. If the requested weight width
1e-28 is not achieved, both precisions are increased in bounded steps and all
attempts are charged. A cap failure raises an error rather than certifying
success. `target_weight_width=None` requests the first rigorous interval without
requiring additional tightness.

`verify_certificate(cert, expected_a, expected_b, D)` requires separately supplied
expected coefficients. It rejects a mismatched input identity, wrong root index,
invalid coordinate scaling, insufficient root width, wrong Sturm count or
unjustified weight interval. It recomputes the exact signs and directed
recurrences. Python assertions are not used. The default receiving root-width
contract is also 140 fractional bits, and can be changed explicitly.

`cms_bounds(cert, t)` returns Decimal-string lower/upper envelopes at t. A float
threshold denotes its exact represented binary rational; Fraction, Decimal and
decimal strings can express other exact intended thresholds. Consumers should
verify an untrusted certificate once before repeatedly evaluating envelopes.

## Exact root argument

Let K=D J be the integer matrix. For x=m/q, define

r_0=1,
r_1=a_0 q-m,
r_{j+1}=(a_j q-m)r_j-b_{j-1}^2 q^2 r_{j-1}.

Then r_j=q^j det(K_j-x I), where K_j is the leading j by j principal block.
All signs are computed as integer signs. Positivity of the off-diagonal entries
gives irreducibility and strict interlacing. Adjacent r_j cannot vanish: the
recurrence would force all the way back to r_0=0. At an internal zero, its two
neighbors have opposite signs, so omitting that zero gives the appropriate one
variation independent of the infinitesimal side. At a terminal zero, strict
interlacing means the sign variation count of the preceding leading block is
the number of full-matrix eigenvalues strictly below x. Thus deleting zero
sequence terms gives the strict Sturm count, including at an eigenvalue.

The diagonal entries plus adjacent off-diagonal sums give a Gershgorin enclosure.
It is enlarged to strict symmetric power-of-two integer endpoints. Exact Sturm
counts there are checked to be 0 and n. Bisection uses rational dyadic midpoints.
For root index i starting at 0, a non-singleton final interval has lower strict
count i and upper strict count i+1. A detected exact root has zero full
determinant and strict count i. These facts identify the intended ordered root.
All successive root brackets are checked not to overlap in their interiors.
Their widths are at most 2^-140 in the integer coordinate, or narrower after
adaptive refinement. Exact dyadic roots may be returned as singleton intervals.

The upper endpoint can coincide with the next root: its strict count still
counts the target root below it. This does not impair containment of the indexed
root or ordered-bracket comparisons. Every indexed root is uniquely determined
by its Sturm count and irreducibility, even if two enclosures share an endpoint.

## Weight argument and interval implementation

For a simple eigenvalue lambda of K, an eigenvector with first entry one obeys

p_0=1,
p_1=(lambda-a_0)/b_0,
p_{j+1}=((lambda-a_j)p_j-b_{j-1}p_{j-1})/b_j.

Its first entry is nonzero: otherwise the first row and positive off-diagonal
entries inductively force the entire eigenvector to vanish. Hence the spectral
weight associated with e_1 is exactly

w=1/(sum_{j=0}^{n-1} p_j(lambda)^2).

The common D cancels from this recurrence when scaled roots and integer
coefficients are used. Interval evaluation of the recurrence over each certified
root bracket therefore encloses w. Every endpoint division and arithmetic
operation uses Decimal ROUND_FLOOR or ROUND_CEILING under an explicit local
precision and wide exponent range. Squaring treats an interval containing zero
separately. Its positive reciprocal uses the already enclosed squared sum, whose
lower endpoint is at least one. Individual weights are intersected with [0,1],
and their sum is checked to enclose one.

One implementation risk was found before the first test execution and repaired:
Python's `abs(Decimal)` applies the ambient Decimal context, which can silently
round an interval endpoint inward. The final implementation uses exact
`Decimal.copy_abs()` before directed squaring. The checks intentionally set
ambient precision to nine digits while the interval engine uses its own 100-digit
contexts. The repaired module passes those checks.

## Conservative CMS envelope

For a probability measure whose leading n-step Jacobi matrix is J, let theta_i
and w_i be the exact Gaussian quadrature nodes and weights (1-based). The
Chebyshev--Markov--Stieltjes inequalities at quadrature nodes imply the following
conservative envelopes for arbitrary t:

L(t)=sum_{i=1}^{n-1} w_i,lower * 1{theta_{i+1},upper <= t},
U(t)=w_1,upper + sum_{i=2}^{n} w_i,upper * 1{theta_{i-1},lower <= t}.

These are clipped to [0,1]. The upper inequality intentionally includes equality
and can include an unnecessary extra weight at an exact node; that preserves
validity at interval boundaries. The module does not assume the underlying full
measure is supported on the small Jacobi matrix's nodes or Gershgorin interval.
Proving that a particular Krylov object has the required moment/Jacobi relation
to the intended measure is a separate obligation of the main construction.

## Tests and resource boundary

`checks/check_certified_jacobi.py` runs known one-, two- and three-dimensional
cases, including exact eigenvalues 0 and 5 with weights 4/5 and 1/5, and eigenvalues
-sqrt(2),0,sqrt(2) with weights 1/4,1/2,1/4. It checks internal and terminal Sturm
zeros, exact CMS endpoints for a larger measure, and rejection of five corrupted
certificate fields. The script is run with `python3 -O` so validation cannot
depend on Python assertions.

Separate SciPy diagnostics compare roots/weights for n=3,8,16,32,64 and test the
CMS envelope of a leading 6 by 6 block against the numerical e_1 spectral measure
of a full 20 by 20 Jacobi matrix. Numerical agreement is explicitly not used to
prove an interval. Source generation, reasoning and parent integration costs are
outside the script's measured body times.

The complete results are in `results/certified_jacobi_checks.json`, including
per-case construction/verification timings, all refinement attempts and the
runtime versions. No numerical proposal was accepted on solver status alone.

## Retained external obligations

The module certifies the exact integer matrix supplied to it. It does not itself
bound coefficient quantization from another matrix, establish a full-operator
backward error, certify orthonormality of a Krylov basis, or validate the random
probe law. These remain separately charged proof obligations. Reducible Jacobi
inputs with a zero off-diagonal are rejected and require an explicit treatment
of exact/rounded breakdown by the main construction.
