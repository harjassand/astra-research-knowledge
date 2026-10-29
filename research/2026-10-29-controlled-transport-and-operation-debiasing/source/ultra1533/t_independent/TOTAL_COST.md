# Total acquisition and computational cost

## 1. Input and operation

The input is a supplied finite connected graph, rational q>=1, rational priors in
(0,1), integer component count r>=1, and rational output grid width delta>0.
More generally a supplied rational spanning frame and fixed PSD grounding matrix
are admitted by the theorem, although the executable specializes to a graph.
The baseline precision must be SPD. No unknown material potential is reconstructed.
There is no preparation, readout, bath or instrument oracle: this is computation
of the supplied model. It does not use N675 or any other unqualified Astra premise.

Choose a warranted rational c_bar<1 with

    r q(sqrt(q)-1)^2/8 <= c_bar.

The executable checks this inequality by a rational square comparison when the
sharpened bound is supplied. At q=1 the independent Gaussian/bit shortcut is an
ordinary faster option. Let k=n-1 be the pinned dimension.

## 2. Conditional update and arithmetic cost

After initial exact inversion, each state update uses O(k^2) rational arithmetic
for a matrix-vector contraction and Sherman--Morrison correction. The generic
implementation stores dense matrices. It does NOT turn an O(k) mesh into O(log k)
cost, use a free effective-resistance oracle, or claim optimal sparse complexity.
Graph/frame construction and inversion are charged separately in the receipt.

On a unit graph with rational q of bit length B, every possible precision has
integer-scaled entries of bit length O(B+log m). Cofactors and the determinant
bound every reduced inverse entry's bit length by O(k(B+log m+log k)). This bound
depends on the input size, not the history of rank updates. Rational Gaussian
elimination and LDL also have polynomial bit bounds via determinant minors.
For a general rational frame, replace B by its full entry bit-height; clearing
denominators and the same determinant argument still apply.

The expected state-update count is <=8L, with

    L=ceil[m(ceil(log2 m)+1)/(1-c_bar)].

The proof also gives all fixed moments of the largest window/replayed update
count bounded polynomially in L. The explicit dependence on 1/(1-c_bar) is REAL;
being extremely close to the contrast boundary is not computationally free.

## 3. Fair bits, adaptive word replay and scalar arithmetic

At a FIXED replay level, an update threshold is determined by the earlier maps;
its current uniform remains independent of it. A binary interval of width 2^-b
contains this threshold with probability <=2^-b. Resolving both extremal thresholds
therefore has a geometric requested-bit tail. Edge selection uses ordinary bounded
integer rejection, also with a geometric tail and O(log m) mean bits.

Do not condition this tail on the adaptive event that a later replay is reached.
Instead imagine each fixed-length replay unconditionally. Its total bit cost has
second moment O(poly(input)*T^2). Cauchy--Schwarz bounds its cost multiplied by the
reach event using the square root of (6). Summation over doubling levels still
converges, and gives finite, polynomially bounded expected fair-bit work in
m,k,r,input-bit-height and 1/(1-c_bar). Rational comparison (8) costs polynomially
in its input and requested bits. No separation from an algebraic threshold is
assumed; the independent uniform supplies that separation in expectation.

These are ordinary arbitrary-precision integer/rational algorithms. The executable
uses FLINT for convenience. Random.Random is a reproducible diagnostic bit source;
the iid theorem is for ideal independent fair bits, not a claim about a finite seed.

## 4. Full quantized field output

Exact rational LDL costs O(k^3) arithmetic operations after the conductance draw.
There are r*k Gaussian coordinates and O(r*k^2) elementary arithmetic contractions.
FIELD_OUTPUT proves the precision loop settles all the requested bins with finite
mean precision. A polynomial-cost elementary implementation exists: normalize U
by powers of two for log, use log via its atanh series on a fixed compact interval,
compute pi by a geometric arctangent formula, use sin/cos Taylor series on [0,2pi],
and use rational square-root bisection. These are explicitly computable operations,
not inaccessible normal/CDF oracles.

Here is the bit-height qualification behind the mean statement. Let H bound the
bit-height of every LDL coefficient, delta and its reciprocal. The field-map and
wrapped marginal-density constants in FIELD_OUTPUT have logarithms polynomially
bounded by H+k+r. Thus a starting precision p0 polynomial in these quantities pays
their constants. Beyond p0 the unresolved-depth probability decays exponentially
in p-p0. All fixed precision moments are polynomial in p0. Polynomial scalar
evaluation at these requested precisions has finite polynomial mean cost. The
normal tail also gives polynomial mean output INTEGER bit length. Binary integer
serialization is always available; no claim about unbounded decimal printing is
required. Components r are charged as output dimensions, not as log(r) work.

This is an existence/algorithmic bit-cost theorem using those constructive scalar
evaluators. It does NOT certify expected CPU bit complexity of the installed
python-flint/Arb build. Actual code uses strict outward Arb branches and finite
integer floor output. In the acquired batch all field decisions settled at32
uniform bits and256-bit interval precision; that observation is not a worst-case
precision theorem. A full continuous real is not returned as a finite string.

## 5. Acquired execution and ordinary methods

One declared batch ran23.9812 seconds, including static controls and comparators.
It returned2048 latent cycle states;64 full15-coordinate scalar fields;16 full
15-coordinate fields at q4,p99/100 (nonconvex);16 full45-coordinate vector fields;
and2 full63-coordinate fields. All full fields use quarter-grid quantization.
No actual device inputs, physical trials or paid compute were used.

For64 matched exact full-field outputs on the16-site torus:

* CFTP:1.10392 s,147342 bit queries,32768 state updates.
* Ordinary Gaussian rejection:0.100192 s,480896 bit queries,884 proposals.
* Ordinary proved-TV1/100 chain:0.727003 s,345 updates per draw. Its64-output joint
  error bound is64/100, not1/100; the per-output and joint targets are distinguished.
* Ordinary32-sweep latent-Gaussian Gibbs:0.042257 s,2048 Choleskys, but its finite
  approximation error is UNKNOWN. This faster diagnostic is not called exact.

The exact ordinary rejection method WINS the actual small-cell timing by about
11.0x. REJECTION_BOUND proves its exponential proposal barrier with volume, while
the new contraction gives a polynomial conditional-update bound. This does not
establish a crossover or a lower bound on other equally informed algorithms.
Sparse solvers, preconditioning, graph special structure and other perfect
samplers remain serious alternatives. No general practical advantage is claimed.

## 6. What changed and what did not

The changed computational question was full normalized equilibrium output rather
than only local moments, signed expansions or an unqualified equilibrium run.
The common-configuration squared-current bound pays its missing mixing premise on
ALL finite graphs, including centered nonconvex source potentials, under an explicit
contrast condition. Standard CFTP, rank-one algebra and Gaussian generation then
compose into a finite-bit observation operation.

An infinite-volume local query at volume-independent work was the initial hope;
it is NOT acquired. The conductance conditional is globally coupled, and no local
effective-resistance/inhomogeneous-background oracle was granted. Real material
fitting, physical error, arbitrary anharmonic potentials, nonzero forcing, native
large-system performance and historical priority remain separate. This result is
a finite computational principle with an executed normalized output, not a material
device or a measured civilisation-level gain.

## 7. Stronger conventional rejection, after the initial batch

LEVERAGE_REJECTION derives a positive product proposal from the SAME harmonic
leverage scores and pays its exact rejection/conditional-field output. A separate
protocol was saved before its first execution, using only the four already acquired
field source cases. No CFTP source, grid, parameters or original output were rerun.

Including both setup and sample times, its matched comparisons were:

* 16-site scalar,64 fields: .0384021 s versus CFTP1.10451 s (ordinary about28.8x faster).
* Nonconvex q4,p.99,16 fields: .00884646 s versus.140518 s (about15.9x).
* Three components,16 fields: .0114605 s versus.702329 s (about61.3x).
* 64-site scalar,2 fields: .156067 s versus20.2445 s (about129.7x).

This is a decisive practical comparator failure for prioritizing the dense CFTP
implementation on these supplied cases, and is preserved without qualification by
an easier accuracy target. BOTH methods have the same exact normalized quantized
full-field target, subject to the fair-bit/outward-primitive contract. The CFTP
general polynomial guarantee remains a distinct theorem; leverage rejection's
proved bound can still be exponential in volume. Combining them by a fixed cap
and independent fallback gives an exact operation, but no hybrid timing was run.

Both algorithms may also use the sharper contraction. GENERAL_CERTIFICATE pays
c_bar43/1000 for scalar q2: CFTP's conservative initial window becomes201 and the
ordinary TV1/100 chain's proved burn-in becomes270 (rather than256 and345).
These are theoretical cost qualifiers, not changed execution timings. For three
components at q2, c_bar13/100 is paid too. No asymmetric withholding of this input
from the ordinary method is intended.

The main batch's23.9812 s and the additional comparator's receipt are separate.
Engineering previews additionally consumed about8.45 s (one16-site latent draw,
one64-site latent draw and one16-site full-field draw). The symbolic/scalar final
consumer took .02473 s, excluding imports. Source retrieval/failed timeout and
writing are not included in those solver timings; no global wall-clock claim is
made. No paid compute or physical action occurred.
