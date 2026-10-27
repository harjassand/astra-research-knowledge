# Independent audit of the block-orbit extension

27 October 2026. The root construction generalizes raw row clustering to blocks whose internal coordinates have unknown invertible binary gauges. This audit checks that construction; it does not claim generic block-diagonal low-rank completion.

## Metric and gauge orientation

For fixed block width b, a block row X is a list of b by b matrices. Set

    rho(X,Y)=sum_j rank(X_j-Y_j),
    d([X],[Y])=min_(G in GL_b(F_2)) rho(GX,Y).

The rank sum is a metric on block rows, and simultaneous left multiplication by an invertible matrix is an isometry. Therefore the quotient distance is a pseudometric satisfying symmetry and the triangle inequality. The right gauge on column block j also preserves each summand's rank. This is exactly why unknown block-column gauges do not have to be learned before the metric is computed.

Given a cluster assignment a -> f(a), choose G_a with rho(G_a B_a,B_f(a))=d([B_a],[B_f(a)]). Let G be their block-diagonal direct sum. After congruence B'=GBG^T, a valid row model repeats the RAW facility block row B_f(a), multiplied on the right by G^T. It does not generally repeat the corresponding block row of B', since that row has its own left gauge. This orientation was independently implemented and tested.

If the metric clustering objective is kappa, the directed entrywise Hamming error A of this row model satisfies A<=b^2 kappa: a b by b matrix has at most b^2 nonzero entries for each nonzero rank unit. This bound is loose but valid and sufficient for b=n^{o(1)}.

## Hidden error accounting

Suppose the hidden gauged block matrix has at most c block-row orbit types. If at most M unordered OFF-DIAGONAL BLOCK pairs are corrupted, the total directed rank discrepancy T of the raw matrix from this witness is at most 2bM+n. Arbitrary unknown diagonal blocks contribute at most b each, hence n total. If instead M counts scalar off-diagonal entry errors, use T<=2M+n. The two M conventions must not be mixed.

The standard input-center argument gives metric optimum at most 2T, and classical one-swap local search gives kappa<=10T. The metric values are integers of polynomial magnitude, so exact strict-improvement local search terminates after polynomially many swaps. Computing distances by enumerating GL_b costs poly(n)2^{b^2}; for b=n^{o(1)} this is 2^{o(n)}. The raw block partition is assumed to be the parent's separately acquired centroid partition, not a supplied decomposition.

## The root's improved symmetric rounding constant is valid

Fix a pair of cluster labels and within-block coordinate positions. This defines a binary rectangular matrix Y indexed by original blocks. Let v_j be its row-model constant, and let u_i be its transposed column-model constant. Choose a uniformly random column j0 and fill the whole rectangle with v_j0. For every entry,

    [Y_ij != v_j0]
      <= [Y_ij != u_i] + [u_i != Y_i,j0] + [Y_i,j0 != v_j0].

Summing i,j and averaging j0 gives candidate constant error at most twice the column-model error plus once the row-model error. The raw majority bit does no worse. Summing ordered rectangles gives directed majority error at most 3A, because symmetry makes the global row- and column-model errors equal. Transposed rectangles choose the same majority, including the diagonal cases, so the resulting C is symmetric. Its off-diagonal residual has at most 3A/2 unordered edges.

The scalar row partition consists of pairs (cluster label, internal coordinate), at most bc classes. Therefore C has an explicit indicator factorization of rank at most bc. Combining the bounds gives residual edges at most 15b^2 T, hence at most 15b^2(2bM+n) under the corrupted-block-pair convention.

An earlier two-coordinate argument using a random raw Y entry gives only 4A. The stronger root argument above uses the model bit v_j0 and correctly saves one term. There is no conflict in the two bounds.

## Exact phase and locality accounting

The congruence changes quadratic phases by an additional unary correction. If x=G^T y, then

    q_B(x)=q_(GBG^T)(y) + ell.y,
    ell_j=q_B(row_j(G)).

This correction cannot be discarded. Because G is block diagonal, an originally block-local cubic remains block-local and of degree at most three after Boolean multilinear reduction. If blocks have width at most b, expanding these polynomials contributes O(nb^2) cubic-or-lower monomials. The raw acquired completion's sparse residual is retained exactly. A later Walsh expansion of the rank-bc symmetric completion produces only unary modifications, as in the saved fourth-root compiler.

This does not prove acquisition for every rank-r matrix plus unknown block diagonal. The condition is small block-row ORBIT diversity, which can be much stronger than small rank. The complete equivalence-class partition and gauges are nonetheless manufactured from raw block rows, not assumed known.

## Executed independent checks

`block_orbit_audit.py` tested six independently generated hidden-gauge fixtures with block widths two and three, including arbitrary diagonal-block changes and corrupted off-block pairs. It checked quotient-metric symmetry and all triangle inequalities, compared one-swap local costs with exact facility optima, verified hidden error bounds, aligned raw block rows, and checked the exact symmetric acquired representation. The largest fixture has 18 variables in six blocks, with GL_3 containing 168 elements.

The program also verified 5,952 pointwise quadratic coordinate-change identities, five exact mixed phase sums, and 35,200 exhaustive rectangular rounding inequalities. All assertions passed. These checks validate the identities and real finite implementation; no asymptotic phase-engine execution or practical speedup is asserted.
