# Finite bits to stored Gaussian probes: operation, proof, and scope

Local module for the PRO2 spectral distribution construction, 21 October 2026.
This module supplies one missing computational boundary: an explicit coupling
between an ideal Gaussian probe block and a reproducible stored rational block.
It does not establish the matrix quadrature certificate, choose a benchmark, or
verify the entropy of the device supplying random bits.

## 1. Contract and returned object

The module is `src/gaussian_bits.py`. Its public entry points are

```python
ints, denominator, certificate = generate_probe_block(n, s, directory)
receipt = verify_probe_block(directory,
    expected_n=n, expected_s=s, expected_bits_sha256=bits_digest)
```

Here `ints` is an n by s `int64` array, `denominator = 2**40`, and the stored
probe matrix is exactly `ints / denominator`. The directory contains the saved
raw bits, the NumPy integer file, and a JSON certificate:

* `gaussian_bits.bin`
* `gaussian_probe_ints.npy`
* `gaussian_probe_certificate.json`

For reproducible tests only, the optional `seed` argument uses Python's
deterministic generator and records that no probabilistic coverage is claimed.
The actual experiment uses one call to `os.urandom`, persists its output before
inspecting it, and never silently redraws or overwrites an existing bit file.

The probability model is explicit: all 64-bit words are independent uniform
words. `os.urandom` is the chosen implementation of that assumption; neither the
mathematical proof nor replay establishes that a particular operating system
actually supplied independent physical entropy. The deterministic certificate
is valid for the saved words regardless of their origin. Distributional
conclusions require the stated model.

The relevant certificate fields are exact rational objects with decimal-string
`numerator` and `denominator` fields. In particular:

* `global_normalized_cdf_slack` is a simultaneous perturbation bound for the
  aggregate-normalized spectral distribution of the block.
* `per_column_normalized_cdf_slack` contains simultaneous perturbation bounds
  for each individually normalized column. Their arithmetic mean is a bound
  for the equal-weight spherical-probe average.
* `excluded_cell_failure_bound` equals `ceil(n*s/2) / 2**64`.
* The Frobenius radius, column radii, norm lower bound, and largest pair error
  are also retained, so the calculation can be inspected rather than inferred
  from a rounded displayed decimal.

The aliases `normalized_cdf_slack`, `column_cdf_slacks`, and
`exception_probability_upper` are retained for the earlier interface. Replay
checks the aliases too; disagreeing duplicates are rejected.

## 2. Exact bit-cell coupling

Set N = 2^64. Parse consecutive little-endian 64-bit word pairs (j,h). For each
pair the implementation evaluates the Box--Muller transform at the cell
midpoints

    U0 = (j+1/2)/N,       V0 = (h+1/2)/N,
    r0 = sqrt(-2 log U0), theta0 = 2 pi V0,
    z0 = (r0 cos theta0, r0 sin theta0).

To define the proof coupling, extend the probability space with independent
continuous Uniform(0,1) variables R and S, independent across pairs and of all
words. Put

    U = (j+R)/N,         V = (h+S)/N,
    z = sqrt(-2 log U) (cos(2 pi V), sin(2 pi V)).

Under the iid uniform-word model, U and V are independent continuous uniform
variables. The usual change of variables is elementary: r=sqrt(-2 log U) has
density r exp(-r^2/2) on r>0, the angle has density 1/(2 pi), and the Cartesian
Jacobian is r. Thus z has density

    (2 pi)^(-1) exp(-(x^2+y^2)/2),

so its two coordinates are independent standard Gaussians. Distinct pairs use
independent random inputs, hence all coordinates are jointly independent.
Flatten consecutive coordinates into row-major n by s storage. Every column is
therefore an independent N(0,I_n) vector. If n*s is odd, discard the last
coordinate; Gaussian independence is preserved.

There are M=ceil(n*s/2) pairs. If any radial word j is zero, the algorithm
persists the bits and a failure record, then aborts without a probe block.
The union bound gives

    Pr{some radial word is zero} <= M/N.

The exact value is 1-(1-1/N)^M, but the rational union bound is simpler and
sufficient. This event is tested explicitly, not silently conditioned away.

The proof of the ideal Gaussian law uses the entire uniform distribution,
including the excluded cells. One must not reason that the ideal probes remain
exactly Gaussian after conditioning on no zero cell. The valid reasoning is to
intersect the usual ideal-Gaussian concentration event with the successful
coupling event, then charge the excluded event by a union bound if needed.

The module also refuses a stored column of zero norm. That is a declared abort,
not a falsely certified interval. The conservative statistical statement used
for integration is an *unconditional bound on an incorrect returned result*
under the stated bit model, not coverage conditional on generation succeeding.
A statement guaranteeing successful output as well as coverage would need to
charge any additional abort event. In fact, when all aborts produce no interval,
the no-false-output argument can omit their probabilities; retaining M/N is
conservative. No conditional-on-success confidence claim is made here.

## 3. Integer interval arithmetic

All proof-relevant transcendental calculations use intervals with a common
scale Q=2^112. An integer pair (a,b) represents the closed real interval
[a/Q,b/Q]. Python arbitrary-precision integer arithmetic is used. Rational
scaling, products, and division round outward using integer floor and ceiling.
An interval product takes all four endpoint products. For a nonnegative
interval, square root uses

    [ floor(sqrt(a Q)), ceil(sqrt(b Q)) ] / Q.

The ceiling is checked by the integer square. Thus these operations enclose
the corresponding exact real operations without a floating rounding model.
NumPy is used only to store, shape, hash, and compare integer arrays. Its
floating linear algebra is not part of this module's verifier.

### 3.1 Pi

The code encloses

    pi = 16 arctan(1/5) - 4 arctan(1/239)

using 48 terms of each alternating arctangent series. The absolute remainder is
at most the magnitude of the next term,

    1 / ((2L+1) q^(2L+1)),  L=48, q in {5,239}.

For completeness, if a=arctan(1/5), tangent doubling gives tan(2a)=5/12 and
tan(4a)=120/119. With b=arctan(1/239), the tangent subtraction formula gives
tan(4a-b)=1. The elementary bounds 0<4a-b<pi/2 select pi/4 as that angle,
establishing the identity. The interval arithmetic encloses every series
coefficient and the stated remainder.

### 3.2 Logarithm

For midpoint U0=p/2^65 with p=2j+1, choose the power of two T satisfying
T<=p<2T, write U0=2^(-k) z with z=p/T in [1,2), and set

    x=(z-1)/(z+1)=(p-T)/(p+T),  0<=x<1/3.

Then

    log U0 = 2 atanh(x) - k log 2,
    2 atanh(x) = 2 sum_{a>=0} x^(2a+1)/(2a+1).

The first L=48 terms are enclosed by integer intervals. For x<=1/3, the
remaining positive tail is bounded by

    2 x^(2L+1) / ((2L+1)(1-x^2))
        <= 9 / (4(2L+1) 3^(2L+1)).

The same formula at x=1/3 encloses log 2. Although the outward-rounded upper
endpoint of the *argument interval* can exceed 1/3 by at most one interval
unit, the actual rational argument is known from construction to be at most
1/3. Polynomial interval evaluation encloses that actual argument, and the
tail bound applies to it. `_two_atanh` is an internal helper whose contract
includes this exact-argument restriction; it is not advertised as an enclosure
for arbitrary real arguments just above 1/3.

Multiplication by -2 and integer interval square root now enclose r0. At the
largest admitted radial word j=N-1, -2 log U0 is small but still many orders of
magnitude larger than the accumulated interval uncertainty. The implementation
checks that its square-root lower endpoint is nonnegative, and otherwise
refuses the operation rather than assuming success.

### 3.3 Sine and cosine

Using exact integer arithmetic on h, choose the nearest integer multiple
q*pi/2 to theta0 and reduce to

    x = pi * (2h+1-q*N/2) / N,    |x| <= pi/4 < 1.

The pi enclosure is propagated through this expression; the implementation
also checks its interval lies in [-1,1]. Horner interval evaluation gives the
degree-36 cosine polynomial and degree-37 sine polynomial. Taylor's theorem
(or the alternating-series remainder on this range) supplies the respective
absolute remainders

    1/38!,  1/39!.

Cosine's degree-37 Taylor polynomial is the same as its degree-36 polynomial;
sine's degree-38 polynomial is the same as its degree-37 polynomial. This
explains why the displayed next orders are valid. Quadrant identities then
recover cos(theta0) and sin(theta0), with all signs and interval endpoints
transformed explicitly.

Multiplying these intervals by the radial interval encloses both coordinates
of z0. The rational centre of each interval is rounded to a multiple of
2^(-40), with ties to even. The distance to the more distant interval endpoint
is a rigorous upper bound e_x or e_y for its exact midpoint error. These
include both transcendental enclosure width and final stored quantization.

## 4. From the full continuous cell to the stored pair

For admitted j>=1, U is in [j/N,(j+1)/N] and |U-U0|<=1/(2N). Let r(u) denote
sqrt(-2 log u). The square-root Holder inequality and the mean value theorem
for logarithm imply

    |r(U)-r(U0)|
      <= sqrt(2 |log U-log U0|)
      <= 1/sqrt(j).                                      (1)

This bound remains valid in the last cell ending at U=1, where a direct radial
derivative bound would become singular. If b=(j+1)/N<1, the derivative also gives

    |r'(u)| = 1/[u sqrt(-2 log u)]
             <= N/[j sqrt(2(1-b))],

because u>=j/N, -log u>=-log b>=1-b. Therefore

    |r(U)-r(U0)| <= 1/[2j sqrt(2(1-b))].                  (2)

The implementation takes the smaller of the outward-rounded (1) and (2),
omitting (2) when b=1. It computes a lower integer bound on the denominator
sqrt(2(1-b)) before taking the reciprocal, so the derivative bound is rounded
in the correct direction.

For the angle, |2 pi V-theta0|<=pi/N. The unit-circle parametrization has
Lipschitz constant one in Euclidean norm. With R_j an upper bound for the radial
cell error and r0_hi an upper bound for r0,

    || r(U) e(theta)-r0 e(theta0) ||_2
      <= |r(U)-r0| + r0 ||e(theta)-e(theta0)||_2
      <= R_j + r0_hi*pi_hi/N = C_jh.

Combining with midpoint quantization gives

    ||z-z_stored||_2 <= C_jh + sqrt(e_x^2+e_y^2),
    |z_x-z_stored_x| <= C_jh + e_x,
    |z_y-z_stored_y| <= C_jh + e_y.                       (3)

These are the exact quantities, outward-rounded at scale Q, returned by
`_pair`. The angular term deliberately uses r0 rather than r(U); the displayed
decomposition justifies that choice.

For the full matrix, sum squared pair bounds from (3) and take an outward
integer square root to obtain R with ||G-G_stored||_F<=R. If the final pair has
an unused component, retaining its full pair bound is conservative. For each
column, sum the squares of the coordinate bounds assigned to that column,
then take an outward square root. This gives R_l with
||g_l-g_stored_l||_2<=R_l. No omitted Gaussian coordinates or correlations need
to be enumerated to apply the transfer.

## 5. Uniform transfer of normalized spectral measures

Let a and b be nonzero vectors in any finite real inner-product space. Suppose
||a-b||<=R. For every orthogonal projector P,

    | a^T P a/||a||^2 - b^T P b/||b||^2 |
        <= min(1, R/||b||).                              (4)

Proof: put u=a/||a|| and v=b/||b||. The nonzero eigenvalues of the trace-zero
matrix uu^T-vv^T are plus and minus sqrt(1-(u^T v)^2), as follows by restricting
it to span(u,v) and calculating its trace and squared trace. The absolute
projector trace against that matrix is at most its positive eigenvalue.
The distance from b to the line spanned by a is exactly
||b|| sqrt(1-(u^T v)^2) and is at most ||b-a||. This proves (4); the trivial
bound one covers R>=||b||.

Apply (4) to the flattened blocks, with the orthogonal projector P(t) acting
on every column. In row-major flattening this projector is P(t) tensor I_s.
If `norm_lower` is a positive exact lower bound for ||G_stored||_F, the returned
global slack is

    min(1, R / norm_lower).

The column slacks apply (4) separately using R_l and a lower bound for the
stored column norm. The lower norm bounds come from integer squared norms of
the stored numerators and integer square roots; no floating norm is trusted.
The arithmetic mean of column slacks bounds the difference between the ideal
equal-weight spherical-probe CDF and its stored-column counterpart.

All these perturbation bounds hold simultaneously for every orthogonal
projector. Consequently they cover every spectral threshold of every fixed
matrix and may be added to the corresponding Gaussian concentration radius.
The separate Gaussian concentration theorem still requires the matrix to be
fixed independently of these probes, and its sample-count assumptions still
apply. Computing the perturbation radius from the observed words causes no
additional probability penalty, because the deterministic coupling bounds
hold for every point of every admitted cell.

## 6. Replay, identity, and trusted boundary

Verification reconstructs the probes and all exact radius fields from the
saved words, checks every supplied deterministic certificate field, checks the
integer array's shape and dtype, compares every integer, and checks hashes of
the bits and probe file. It refuses incorrect aliases as well as understated
radii. The receiver may pin n, s, and the bit-source SHA256 externally.

An unpinned verifier can establish that a self-consistent bundle is valid; it
cannot establish that it is the exact previously agreed experimental bundle.
Use the receiving manifest's pinned hash to establish the latter. Hashes also
do not prove that the source was unpredictable or independent. Verification
does not independently establish the code's correctness, the Python integer
implementation, SHA256, or the mathematical concentration theorem; those are
part of the ordinary trusted software and proof boundary and are disclosed.
It does remove dependence on floating transcendental or Gaussian-generator
accuracy from the probe-to-stored-matrix transfer.

## 7. Bounded tests, failures, and costs

`notes/check_gaussian_bits.py` evaluates 172 deliberately difficult and
deterministically selected word pairs at 120-digit Decimal precision. It uses
Gauss--Legendre pi and a direct un-reduced trigonometric series as independent
diagnostic references. Across each pair's midpoint and four cell corners,
860 reference vectors lay within the certified pair and coordinate bounds.
This numerical test does not replace the all-interior proof in Section 4.
The hardest ratio was approximately 0.9999999999996483, attained near a
last-cell boundary; the bound was not merely tested far from its edge.

Exact replay passed. Tests rejected a changed raw bit source, an altered
integer probe even after updating its file hash, an understated global slack,
a receiver dimension mismatch, and a receiver hash mismatch. The discarded
coordinate in an odd-sized block was tested. A mock radial zero cell caused
a persisted failure record with no probe output, and rerunning generation in
that directory was rejected. Existing valid files were also left unchanged
after attempted regeneration.

The final diagnostics receipt is `notes/gaussian_bits_diagnostics.json`.
Its measured body cost was 0.3511342189995048 seconds wall,
0.924377268 seconds process CPU, and 29,470,720 bytes peak process RSS on this
Linux environment. The shell runner observed 0.388217128 seconds for that
process. CPU and wall differ because the process's numerical dependencies can
have background threads; these are observations rather than complexity claims.

Two 12 by 8 deterministic fixtures were constructed while stabilizing the JSON
interface. The initial fixture, retained as `notes/gaussian_bits_fixture`, used
0.007452714000464766 seconds measured generation wall and
0.07140795899999997 seconds CPU, with peak process RSS 23,552,000 bytes. The
interface-final fixture in `notes/gaussian_bits_fixture_v1` used
0.0074656220003817 seconds wall and 0.07141455799999996 seconds CPU, with peak
process RSS 23,560,192 bytes. Their saved bits and probe integers are identical;
the second construction added the receiving interface aliases and was not a
search for favorable random probes. The old JSON lacks those final aliases and
is an explicitly retained preliminary fixture, not an admitted final-schema
certificate. Final-fixture replay cost 0.007573643000796437 seconds wall,
0.06931927999999998 seconds CPU, with peak process RSS 23,699,456 bytes.

An attempted optional diagnostic import of `mpmath` failed because that package
was absent. No installation was attempted. Decimal diagnostics replaced it;
the production verifier was unaffected. This attempt is retained here so the
reported path does not imply a dependency that was available or used.

The body resource counters begin after module import; they exclude interpreter
startup, NumPy import, and construction of the constant pi/log-two intervals
at import time. Whole-experiment elapsed cost must include those startup costs
and all checks, not sum these internal body receipts as if they were total
programme costs. Peak RSS is a process high-water mark and cannot be summed
over sequential calls. The parent actual n=1074,s=8 generation and replay
receipts, rather than an extrapolation from these fixtures, supply the actual
experiment's cost.

No construction failure was observed in the final interval algorithm or its
adversarial tests. The only nonproduction failure above is the missing optional
diagnostic package; the expected rejection tests are successful checks of the
documented failure behavior. No full-scale duplicate probe experiment was
launched by this local task.

## 8. Result and remaining limitation

This module gives a reproducible exact-integer bridge from a stated iid-bit
model to stored dyadic probe vectors, with explicit uniform-CDF perturbation
allowances and a same-input allowance for the equal-weight sphere comparator.
The integrated scientific result still depends on the parent's matrix input
binding, concentration theorem, quadrature certificate, and actual measured
cost comparison. This module establishes none of those independently and
claims no improvement in physical entropy generation or universal advantage
over existing stochastic spectral methods.
