# Orbit clustering: prior scope, costs, and a separating family

27 October 2026. This note supports the current block-orbit compiler. It is
not a claim that centroid decomposition, quotient metrics, metric clustering,
or symmetric matrix co-clustering are new. The root construction and its
independent audit contain the actual compiler and finite executions.

## 1. Closest primary ancestors actually read

**Metric local search.** Arya, Garg, Khandekar, Meyerson, Munagala and
Pandit, *Local Search Heuristics for k-Median and Facility Location Problems*,
SIAM Journal on Computing 33(3), 544–562 (2004), establish the factor-five
one-swap guarantee and the factor-(3+2/p) p-swap guarantee. The use of an
integer metric makes strict-improvement termination polynomial here. The
constant five is convenient rather than state of the art.
<https://epubs.siam.org/toc/smjcat/33/3>

**Co-clustering.** Anagnostopoulos, Dasgupta and Kumar, *A Constant-Factor
Approximation Algorithm for Co-clustering*, Theory of Computing 8(26),
597–622 (2012; preliminary PODS 2008), Theorem 3.6, converts separate
alpha-approximate row and column clusterings to a 3 alpha approximation
for matrix co-clustering. Section 2 allows the number of row and column
classes to be part of the input. This is close ancestry for the compiler's
three-term symmetric rounding. Its basic algorithm is not a new ingredient.
The paper does not give the finite-field unknown local-GL alignment or the
exact phase-reconstruction application used here.
<https://theoryofcomputing.org/articles/v008a026/v008a026.pdf>

**Sum-rank geometry.** Alfarano, Lobillo, Neri and Wachter-Zeh,
*Sum-rank product codes and bounds on the minimum distance*,
arXiv:2105.15086, Sections 2.2 and 3, studies the established sum-rank
metric and its isometries. The compiler uses its elementary matrix form:
rank is invariant under invertible left and right multiplication.
Taking a metric quotient by a finite isometry group is also standard.
<https://arxiv.org/pdf/2105.15086>

**Joint clustering and gauge synchronization.** Fan, Khoo and Zhao,
*Joint Community Detection and Rotational Synchronization via Semidefinite
Programming*, arXiv:2105.06031 (2021; SIAM Mathematics of Data Science
2022), explicitly treats clustering together with unknown vertex-wise
rotations. Its recovery theorems require an extended stochastic block
model. Clean within-community blocks are R_i R_j^T, between-community
observations are randomly drawn rotations, and graph edges are sampled
independently. The finite-field compiler instead allows an arbitrary
symmetric type kernel, adversarial errors, and approximate acquisition
followed by exact residual preservation; it need not identify the planted
classes or gauges.
<https://zhizhenz.ece.illinois.edu/Publications/JointClusterSyncSDP.pdf>

Chen, Cheng and So, *Non-Convex Joint Community Detection and Group
Synchronization via Generalized Power Method*, AISTATS 2024, gives
O(n log^2 n) exact recovery under model-parameter conditions in a related
stochastic group block model. Its proved group cases are SO(d) and O(d),
with a constant number of balanced communities. It is a stronger informed
competitor than assuming synchronization has no prior algorithm, but its
guarantee does not imply the compiler's all-input adversarial approximation.
<https://proceedings.mlr.press/v238/chen24e/chen24e.pdf>

Fan and Zhao, *Information Limits of Joint Community Detection and Finite
Group Synchronization*, arXiv:2412.16387v2, extends the stochastic model to
finite groups and establishes sharp information-theoretic recovery
thresholds. The two-community generative model remains different from
arbitrary finite-field type kernels plus adversarial sum-rank error.
<https://arxiv.org/abs/2412.16387>

The focused searches located no primary theorem stating this exact
worst-case finite-field orbit-alignment-to-phase compiler. That is not a
comprehensive priority finding. Its possible contribution is the complete
acquired representation with its gauge-invariant guarantee and counting
consequence, not any of the ingredients above in isolation.

## 2. Honest scope of the representation promise

Let n=bt and let a hidden symmetric matrix have blocks

    D_ab = L_a K_(tau(a),tau(b)) L_b^T,

where L_a is invertible b by b, tau has at most c values, and K is any
symmetric bc by bc matrix. The sum-rank error across unordered off-block
pairs is E. Arbitrary diagonal blocks cost at most n in directed rank
error. The root's acquired representation gives rank at most bc and at
most 15 b^2 (2E+n) exact residual scalar edges.

This is a restrictive structured low-rank family. Small rank by itself
allows as many as 2^(br) block-row orbits and does not imply small c.
Conversely, c is never supplied as a correct partition or as gauges; only
a budget is supplied, and the algorithm computes labels, aligning gauges,
the symmetric low-rank part and every residual coefficient.

There is no exact latent-parameter recovery claim. Two hidden models can
be observationally ambiguous. The compiler only needs an exact certified
identity and a residual-size bound relative to the best promised witness.
This distinction is why random noise, separation, and identifiable types
are unnecessary in the acquisition theorem.

## 3. Explicit cost and extension to growing or unequal blocks

For uniform blocks, all t^2 orbit distances can be computed by enumerating
GL_b(F_2), with fewer than 2^(b^2) candidates per pair. Multiplication of a
b by b gauge by a b by n row, followed by t rank computations, costs
O(b^2 n) elementary binary operations per candidate. Thus a coarse all-pair
bound is O(2^(b^2) n^3). Storing the distances and the best aligning matrices
requires polynomial space: t^2 b^2 = n^2 alignment bits.

Every orbit distance is an integer at most tb=n. A c-median objective is
at most tn<=n^2. Strict improving one-swaps therefore take at most n^2
iterations. A direct scan of all swaps and clients takes at most t^3 work
per iteration, giving the conservative O(n^5) polynomial remainder. No
claim of optimal implementation complexity is intended. Gauges can be
enumerated one at a time, so growing b does not create an exponential
space requirement.

After a blockwise linear substitution, a Boolean polynomial of degree at
most three remains of degree at most three; each width-b block has only
O(b^3) possible monomials. The nonlinear foreground therefore has
O(n b^2) fixed-locality monomials, rather than requiring an arbitrary
2^b-entry local table. For the root phase engine, one sufficient regime is

    b = n^(o(1)),  bc = o(n),  E = n^(1+o(1)).

Then enumeration costs 2^(o(n)); the exact residual and nonlinear
foreground have n^(1+o(1)) terms; and the subsequent rank-character
expansion costs 2^(bc)=2^(o(n)). This extends the representation guarantee
beyond fixed block sizes, conditional on the same local-phase theorem as
the root construction. It does not replace its proof or its arithmetic
accounting. The raw degree-three ANF still has at most O(n^3) coefficients,
and all full-ANF coordinate changes take polynomial work in that explicit
description size.

Unequal primitive block sizes also fit the metric argument. Cluster block
rows separately by row size b, with at most c_b types for each size. Column
blocks can have any sizes; the distance is the sum of ranks of rectangular
blocks. Their independent right gauges remain isometries. If beta is the
maximum block size, the same entry-error estimate uses beta^2, and the
symmetric rounded matrix has at most sum_b b c_b scalar row classes.
Consequently the sufficient regime becomes

    beta = n^(o(1)),  sum_b b c_b = o(n),  E = n^(1+o(1)).

The root subsequently implemented this extension in
work_orbit_root/heterogeneous_orbit_compiler.py and executed raw mixed-block
fixtures; its independent audit is in work_orbit_audit.

## 4. A rigorous separation from low-rank-width guarantees

Lee, Lee and Oum, *Rank-width of Random Graphs*, Journal of Graph Theory
70(3), 339–347 (2012), Theorem 1.1(ii), establishes that for
1/n << p <= 1/2 the random graph G(n,p) has rank-width n/3-o(n) with
probability tending to one. Its definition is the minimum, over all
subcubic leaf layouts, of the maximum binary adjacency cut rank.
<https://mathsci.kaist.ac.kr/~sangil/pdf/2010random.pdf>

**Elementary transfer.** If symmetric binary matrices B and S differ by
off(D), with rank(D)<=r, then each off-diagonal cut matrix differs by a
matrix of rank at most r. For every fixed rank-decomposition tree T,

    width_T(B) >= width_T(S)-r.

Taking the minimum over T gives

    rankwidth(B) >= rankwidth(S)-r.

This argument allows a nonzero diagonal in D because the cut does not
contain diagonal positions.

Choose b=3, c approximately n/(3 log n), each type used, and a full-rank
symmetric bc by bc kernel. Let U be the repeated type-coordinate
indicator matrix. Then D=U K U^T has rank r=bc approximately n/log n and
at most c block-row types. Add a scalar error graph

    S ~ G(n, log n/n).

It has M=Theta(n log n) scalar edges with high probability. For fixed b,
the unordered off-block sum-rank error E is also Theta(n log n): each
nonzero block contributes at least one and at most b rank units, and
contains at most b^2 scalar edges; within-block edges are negligible.
Therefore the root orbit compiler is in its subexponential regime, while

    r M = Theta(n^2)

lies outside the older sufficient condition r M=o(n^2). At the same time,

    rankwidth(B) >= n/3-o(n)-r = n/3-o(n).

Thus this promised family need not admit a small quadratic rank-width,
even after optimizing the scalar vertex layout in the displayed coordinates.
Add one cubic volume monomial on each triple to obtain the radical-free
nonlinear foreground and apply an arbitrary invertible affine disguise to
form a raw dense cubic input. Its affine-quadratic-leaf barrier and full
stabilizer-nullity barrier are proved in HIDDEN_CUBIC_COMPARATORS.md.

The comparison is about established guarantee parameters. It is not a lower
bound on the runtime of every simulator, or on optimally rewritten quantum
circuits, mixed stabilizer-rank methods, or arbitrary new coordinate systems.
A quadratic background alone is always exactly summable despite high
rank-width; the nonlinear foreground is essential to the counting target.
