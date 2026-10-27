# Independent audit: acquiring a dense quadratic low-rank/sparse interface

27 October 2026. This audits the root's mixed-quadratic acquisition and
its improved short-codeword puncturing repair. All matrix arithmetic is
over F2. The asymptotic phase-counting engine is not executed here.

## Finding

The construction passes the algebraic audit and the adversarial exact
checks below. The puncture/decode repair removes the 2^O(r^2) search for
an alternating coefficient matrix. It supports the stronger regime

    r=o(n),       r M=o(n^2),

with subexponential acquisition, provided subsets are enumerated with
binomial/entropy costs rather than the unnecessarily loose n^r bound.
For the subsequent phase-counting result, the local nonlinear factor
count plus sparse residual budget must also satisfy the phase theorem's
near-linear-density condition.

One important wording correction is necessary: the cleaned column code
need only CONTAIN col(A_RR). Equality is false in general after deleting
rows and principal columns. The factorization and decoding arguments
remain valid for this proper supercode.

## 1. Clean columns exist without incoherence

Suppose an alternating observed matrix B has some decomposition B=A+S,
where A is alternating of rank at most r and S has at most M unordered
nonzero edges. The decomposition is not supplied to the algorithm.
For an integer Delta>=1, let H be the vertices whose S-degree exceeds
Delta. Then

    |H| <= floor(2M/(Delta+1)) <= 2M/Delta.

Put C=[n]\H and choose a column basis I of A_CC, so |I|<=r. Let J be
all rows in C where a column in I has an S error. Every vertex of C
has S-degree at most Delta, hence |J|<=r Delta. Set E0=H union J and
R0=[n]\E0. The observed matrix

    U0=B[R0,I]=A[R0,I]

is clean. Basis columns may lie in J, hence in E0; excluding such
column indices from the search would be incorrect.

Because A_CC[:,I] spans all columns of A_CC, restricting its rows to
R0 shows col(A_R0R0) is contained in col(U0). It need not be equal.
Discard dependent columns of U0 to obtain a full-column-rank generator.

## 2. Puncturing short words manufactures a decodable code

Repeatedly enumerate the current nonzero codewords and, if one has
weight at most 2Delta, remove all coordinates in its support. Its
nonzero preimage then lies in the kernel of the puncturing map.
Consequently the code dimension strictly decreases. There are at most
r such rounds and at most 2r Delta additional removed vertices.

At every round the punctured code still contains all columns of the
corresponding principal submatrix of A. Deleting both rows and principal
columns preserves this containment: each remaining A column is the
puncture of a formerly contained column. The code may continue to be
a proper supercode. At termination its minimum nonzero distance is
strictly greater than 2Delta.

On the final R, every column of B_RR differs from its A_RR column in
at most Delta coordinates, since H already removed every high-error
vertex. Hence it has exactly one codeword within distance Delta.
Exhaustive codeword enumeration recovers it uniquely. No assumption
about incoherence, random errors, generic rank, or error locations is
needed. The total removed set E satisfies

    |E| <= 2M/Delta+3r Delta.

Choosing Delta on the order of max(1,sqrt(M/r)) gives
|E|=O(sqrt(rM)+r). The case r=0 can be handled directly by testing
whether B itself has at most M edges; M=0 is also harmless.

## 3. Wrong candidate guesses cannot create a false certificate

The search enumerates I of size at most r and E0 up to

    a0=floor(2M/(Delta+1))+r Delta.

For each guess it uses only B, computes the observed column code,
punctures its short words, and decodes. Reject if a column has no
nearby codeword, if the assembled matrix is nonsymmetric or has a
nonzero diagonal, or if the alternating residual exceeds M edges.
An accepted decoded matrix has column rank at most the code dimension,
hence at most r. It therefore supplies a genuine certificate on its
remaining principal block, even if it is not the original hidden A.
Interactions touching E are handled directly from the actual B after
branching on E; no global recovered decomposition is required.

The distance test guarantees at most one nearby codeword, but symmetry,
alternation and total sparse-budget tests are still necessary. Exact
counterexamples exercising each rejection are included in the program.

## 4. Factorization of a proper column supercode

Let U have independent columns and contain col(A_RR). Choose any left
inverse L with LU=I and define

    K=L A_RR L^T.

Then K is alternating and A_RR=U K U^T. Indeed UL acts identically on
col(A_RR); symmetry gives the corresponding right identity. Alternation
is preserved by congruence. This computes K after decoding, without
enumerating 2^[r(r-1)/2] possibilities.

Two explicit adversarial fixtures show why containment must replace
equality. A rank-two star A, corrupted on its pivot edge, gives
rank(A_RR)=0 while rank(U)=1 after both pivot vertices are deleted.
A rank-four fixture similarly gives rank(A_RR)=2 while rank(U)=3.
Both reconstruct correctly with an alternating K. The puncture/decode
repair retains these proper supercodes when their nonzero words are
already sufficiently far apart.

## 5. Exact mixed phase reconstruction

For q_K(y)=sum_(a<b)K_ab y_a y_b, Boolean substitution gives

    q_(U K U^T)(z)=q_K(U^T z)+ell dot z,
    ell_i=q_K(U_i,*).

The linear correction is required because repeated Boolean variables
in a product reduce by x_i^2=x_i. It was checked pointwise in every
fixture.

The exact Walsh identity

    (-1)^q_K(y)=2^(-d) sum_alpha W_K(alpha)(-1)^(alpha dot y)

then converts the acquired low-rank part into a sum of dense linear
phases. Dense linear phases are just at most n unary factors. For
every assignment on E, the true B interactions crossing E become
unary phases and a known constant; the local nonlinear polynomial
restricts without increasing its monomial count or locality. Each
remaining phase sum therefore has the original local factors, at
most M sparse quadratic edges, and O(n) unary factors.

The exact character numerator is divided by 2^d only after its integer
terms have been reconstructed. No modular precision is discarded before
this division. In an asymptotic implementation characters and quadratic
Gauss sums can be processed sequentially; coefficient and accumulator
lengths are polynomial in n+r. The finite checker's leaf sums are
exhaustive and are not a fast-counter implementation.

## 6. Search and space costs

Codewords can be streamed in Gray-code order, retaining one n-bit word
and an r-bit index. Each puncture strictly reduces rank, and every
column is decoded by another streamed scan. Thus one candidate costs
poly(n)2^O(r) time and polynomial space. The search has at most

    [sum_(i<=r) binom(n,i)] [sum_(j<=a0) binom(n,j)]

candidates. For r=o(n) and rM=o(n^2), both r and a0 are o(n), and the
logarithm of this product is o(n). The same is true of branching on
the final E and the character enumeration. The bound n^r is too loose
for the full claimed regime and should not be used to justify it.

When M=O(n), every r=o(n) satisfies rM=o(n^2). If additionally the local
nonlinear factors plus M have n exp(o(log n)) density, each acquired
character instance falls under the earlier phase-product theorem,
giving the conditional subexponential original-input result.

## 7. Executed adversarial evidence

`mixed_adversarial_checks.py` manufactures 21 exact fixtures covering
concentrated star corruption, pivot indices inside E, both strict
column-containment cases, empty bases, no sparse corruption, a zero
low-rank component, a forced short-word puncture, and correlated random
examples. It verifies the clean-column witness, alternating factorization,
finite K existence, Boolean linear correction, Walsh reconstruction and
the original mixed phase sum.

`puncture_decode_checks.py` independently applies the improved acquisition
without K search to those witnesses. All 21 cases reconstructed the
actual hidden principal A after their own punctures and gave the exact
original mixed phase sum. They involved 8,060 exhaustive local phase
sums. It also passed four deliberately invalid-candidate tests:

1. An empty code with a column farther than Delta from zero.
2. A star whose observed one-column code decodes individual columns
   to a nonsymmetric matrix.
3. A complete graph with a pivot outside R whose columns decode to
   the symmetric but nonalternating all-ones matrix.
4. Unique nearby codewords whose residual exceeds the global M budget.

An empty-code valid matching residual was accepted. Nonzero short words
were actually punctured, with the rank drop and deletion budget asserted.
Proper supercodes were also retained without being mistaken for exact
column spaces.

One fixture has an observed B of full rank 12 with 54 of 66 possible
edges, although its hidden A has rank two and S has only six edges.
The acquisition leaves a nonzero rank-two component and a sparse
residual; it does not rely on B itself being low rank or sparse.

Some small fixtures puncture all variables because their Delta is large
relative to their finite length. Their exact counts still agree. They
are correctness/edge-case tests, not evidence of a finite speedup. The
asymptotic deletion guarantee uses rM=o(n^2) and r=o(n).

The fixture generator knows A,S in order to test witness existence.
The decoder receives only B, candidate index sets, Delta and M. These
programs do not benchmark the complete enumeration over all candidate
sets or execute the governing asymptotic phase solver.
