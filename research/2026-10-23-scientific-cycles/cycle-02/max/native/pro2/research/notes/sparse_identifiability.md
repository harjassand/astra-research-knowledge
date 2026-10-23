# Original graph structure changes the common-operator class

Later update: the initial7--9 identification bracket in this chronological
record has been superseded. The root's84-vertex core dimension argument,
independently checked in `notes/eight_probe_obstruction_challenge.md`, rules
out every eight-direction block. Combined with the nine-column certificate
below, the exact identification minimum for this symmetric support is9.
The no9-clique result and failed clique-based necessity route remain valid.

This is a critical scope test of the common-action completion result, using
the original exact-decimal NIST support and the already saved integer basis.
No eigenvalue solve, matrix reconstruction, new probe, precision sweep, or
repeat of the single-probe moment calculation was performed.

## Exact result

For the 1074-dimensional bcsstk08 pattern, expand the original symmetric
coordinate records and interpret every decimal as an exact rational. There
are 7017 lower-triangular records, no exact-zero records, and 12960 expanded
nonzero entries. Row5 (zero based) has 339 allowed entries, the maximum;
the minimum row support is1.

Take the saved basis integers `basis[ell,i,depth]`, in order of increasing
depth followed by increasing probe index. The fixed prefix length is

    q = max_i |support(row i)| = 339.

Thus columns0 through335 contain all eight probes at depths0 through41,
and columns336 through338 contain probes0,1,2 at depth42. The common basis
denominator is2^29; it does not affect row rank.

Every one of the1074 row-restricted matrices

    X[support(row i), 0:339]

has full row rank over the rationals and over the reals. This is certified by
a nonzero square minor modulo the explicit prime2147483647. One fixed prime
and one fixed prefix were tried, and all rows passed. No failed primes or
prefixes were discarded.

Consequently, if two real matrices C and B both obey the original support
pattern and satisfy `C X=B X`, then `C=B`. Symmetry is not needed for this
339-column uniqueness statement.

This demonstrates that the large dense-completion ambiguity is created in
part by omitting available graph information. It cannot be called an
impossibility for the fully specified sparse NIST input. A subsequently
authorized symmetry-aware test below reduces the actual sufficient prefix
to9 already stored directions. The339-column result and all its costs are
preserved as the first construction.

## Proof

Let D=C-B. Its i-th row is supported on the known set S_i. The i-th row of
`D X=0` is

    D[i,S_i] X[S_i,:] = 0.

Since X[S_i,:] has full row rank, its rows are linearly independent. The only
linear combination giving zero is the zero coefficient vector. Thus
`D[i,S_i]=0` for each i, and hence D=0.

To prove the row-rank claim, the certificate supplies |S_i| selected columns
and the determinant of the corresponding integer square minor reduced modulo
p. A nonzero determinant modulo p implies that the integer determinant is
nonzero, so that minor is nonsingular over the rationals and reals. There is
no floating-point rank threshold.

The modulus p=2147483647 is checked prime by exact trial division through its
integer square root. The modular array kernels multiply at most two residues
before reduction and never accumulate a dot product. Since `(p-1)^2<2^63`,
every signed int64 product and subtraction used there is representable; this
guard is checked explicitly. Modular inverses are Python exact integers.

## Source binding and independent minor replay

The exact original parser is `restore_pro2/src/exact_residual.py:read_mm_exact`.
The checker pins the SHA256 digests of that parser, the original gzip input,
and `witnesses/lanczos.npz`. It obtains the support from original nonzero
decimal coefficients and symmetric expansion, not from a rounded-operator
nonzero filter. Positive diagonal mass scaling preserves this original
pattern for the actual generalized operator A.

The construction performs rectangular elimination to select each minor.
The separate replay path forms only the declared square minor, applies the
declared row permutation, and verifies all recorded pivots and determinant
by square Schur elimination. It performs no new minor selection or rank
search. Both paths use exact modular arithmetic. This is an independent
algebraic replay path inside the same source file, not a theorem-prover
formalization or independent software stack.

Files:

- `checks/check_sparse_identifiability.py`
- `results/sparse_identifiability_certificate.json`
- `results/sparse_identifiability.json`
- `results/sparse_identifiability_replay.json`

Certificate size421302 bytes; SHA256
`b501e7bd03383db941e468721fc12ea859316ede00030471965a320cc90b8e1f`.

Reproduce with the already supplied owner source directory:

    python checks/check_sparse_identifiability.py --verify --owner OWNER_ROOT

The `--construct` mode refuses to overwrite the existing certificate.

## A symmetry-aware structural clue and the initial stopping boundary

The root identified a stronger conditional elimination argument. Let the
off-diagonal original pattern be an undirected graph. Eliminate vertices in
some order. At a current vertex i, suppose the rows of X indexed by i and its
remaining neighbors are independent. All entries incident to previously
eliminated vertices are already zero by symmetry. Therefore the same local
argument forces the remaining entries in row i of a symmetric D to vanish;
symmetry then eliminates them from the corresponding columns.

If the graph has degeneracy d_graph, a minimum-degree peeling order has at
most d_graph remaining neighbors at every step. Generic `d_graph+1` columns
therefore suffice for symmetric identifiability: each of finitely many
required row minors is a nonzero polynomial for independently generic X.
This generic statement does not certify a particular stored X.

For the actual original graph, deterministic minimum-current-degree peeling
(ties resolved by the smallest zero-based vertex index) gives

    degeneracy = 8,    generic sufficient column count = 9.

The full order and remaining degrees are preserved in
`results/sparse_degeneracy_preliminary.json`. An exact replay in
`checks/check_sparse_degeneracy.py` verifies each removal was minimum degree,
and identifies the suffix induced subgraph at which the minimum reaches8.
That subgraph proves the matching lower bound on degeneracy. Thus this graph
quantity is not an estimate from the maximum row degree.

The initially requested conditional branch was to test the saved eight initial columns
only if the sufficient count was at most8. It was9, so no nine-column test or
automatic extension was performed at that checkpoint. The root then explicitly
selected the distinct bounded nine-column test described below. The change
was authorized and prospective, rather than silently widening a failed run.

## Actual nine-column symmetry-aware result

The root's subsequent fixed experiment takes precisely the first9 stored
columns in the same depth-then-probe order: the eight saved starting columns,
followed by probe0's depth1 column. All nine already occur in the old512-column
stored transcript. No new random probe or Krylov step is generated.

Along the saved degeneracy8 peeling order, every one of1074 matrices

    X[{current vertex} union {remaining neighbors}, 0:9]

has full row rank, certified by a nonzero minor modulo the same fixed prime
2147483647. One attempt passes every step. Therefore, for SYMMETRIC matrices
supported on the original pattern, the action on these nine exact stored
directions is injective.

Proof: induct on the elimination order. Before handling vertex i, all rows
of D at previously removed vertices have been shown to be zero. Symmetry
therefore makes all entries in their columns zero as well. The only possible
nonzero entries of row i are at i and its remaining neighbors. Its equation
`D[i,:] X=0`, together with the verified local full row rank, forces this row
to zero. The induction ends with D=0.

This is a finite exact certificate for the actual stored directions, not just
a generic-random-matrix assertion. It identifies exact action information
which already lies within the span considered by the dense completion
calculation. The support prior can therefore collapse that ambiguity even
though each separately retained scalar Jacobi moment class remains broad.

Files:

- `checks/check_symmetric_sparse_identifiability.py`
- `results/symmetric_sparse_identifiability_certificate.json`
- `results/symmetric_sparse_identifiability.json`
- `results/symmetric_sparse_identifiability_replay.json`

Certificate size316470 bytes; SHA256
`cb0fc199f108511d857f74de98602c26aa243258314ddd56c921fb6d7230360e`.
The replay independently checks all declared local minors and the entire
deterministic minimum-degree order against the original source support.

Reproduce with:

    python checks/check_symmetric_sparse_identifiability.py --verify --owner OWNER_ROOT

### Failed sharpness route: there is no9-clique

The requested clique obstruction would make9 necessary: on a9-clique, any
eight query columns admit a nonzero vector z supported on that clique with
`z^T X=0`, and `D=z z^T` is then a nonzero symmetric pattern-supported
perturbation satisfying `D X=0`. A sufficiently small multiple preserves any
strict spectral enclosure around a compatible interior operator.

But the actual graph contains no9-clique. This was checked completely without
an exponential search. Every9-clique has an earliest vertex in the peeling
order. It would have eight later clique neighbors; since the peeling order
has at most eight remaining neighbors at every step, that vertex's full
remaining-neighbor set would have to be exactly those eight vertices and be
a clique. The code checks every such size9 local set, and none is complete.
This also excludes any larger clique, consistently with degeneracy8.

Consequently9 is a verified sufficient direction count, not a proven optimum.
An elementary dimension lower bound gives7: the space of symmetric matrices
on the original pattern has dimension7017, while six matrix-vector actions
have at most6*1074=6444 scalar outputs, leaving a nonzero kernel for every
choice of six directions. This argument also applies transcriptwise to
deterministic adaptive queries: a perturbation annihilating all queried
directions reproduces the same responses and hence the same chosen queries.
Small perturbations can preserve strict support bounds. At this chronological
checkpoint, the exact minimum was bracketed between7 and9 for unrestricted
exact directions. The later induced-core dimension proof cited at the top
resolves this uncertainty in favor of9; the original dimension-bound and
failed clique attempt are preserved here.

Neither this identification lower bound nor the failed clique route is a
lower bound for approximate CDF estimation. The rank-one clique construction,
even if present, would not by itself imply a macroscopically wide count band.

## Limits that matter

1. Identifiability is not stable recovery. These exact integer row ranks can
   be supported by extremely small singular directions. No lower singular
   value bound, reconstruction error, noisy-action tolerance or condition
   number has been certified.
2. The proof assumes exact joint action Y. Saved scalar Jacobi coefficients
   or separately completed per-probe moment sequences do not provide that
   action for one common operator.
3. The exact source A and its dyadic surrogate barA have different actions.
   This result applies separately to either exact action if supplied. It
   does not silently identify `A X` with `barA X`, or remove the prior
   operator-norm input allowance.
4. No entries of A were reconstructed here and no eigenvalue counts were
   computed. This is not a spectral speedup, and it does not reverse the
   prior dense-computation cost defeat.
5. The rowwise339 condition is sufficient even for nonsymmetric matrices.
   The actual nine-column construction uses symmetry. Its optimality was
   initially open between7 and9 and is established by the later independent
   core dimension challenge cited above; this record preserves that sequence.

## Observed costs and attempts

The first support-only inspection found q339. It was exploratory source
reading, not the measured constructor. The constructor and replay each
include their own source digest checks, exact source parsing, basis loading,
prefix creation and primality check. Their timers start before Python library
imports (but after interpreter start). CPU can exceed wall time during
multithreaded library initialization.

| Stage | Wall seconds | Process CPU seconds | Peak RSS bytes |
| --- | ---: | ---: | ---: |
| Construction including imports |0.8737865520|1.701295866|57819136|
| Separate minor replay including imports |0.6392257280|1.399327785|57868288|

Nested construction source/prefix work0.278790595s; exact modular rank work
0.512123679s; primality check0.001366745s. Nested replay source/prefix work
0.249710451s; declared-minor checking0.302573876s; primality check0.001244203s.
These subsets are not additional to their enclosing totals.

The separate initial parse-plus-peeling body took0.030234011s and is additional.
Its replay took0.511630065s wall /1.242296362 CPU including imports, peak RSS
47542272 bytes; the minimum-degree8 lower-bound witness is an84-vertex induced
suffix starting at elimination step990.

The subsequent nine-column construction took0.566901561s wall /1.394368577 CPU
including imports, peak RSS57499648 bytes. The separate replay took0.541821593s
wall /1.373152500 CPU including imports, peak RSS57569280 bytes. Nested
construction/order checks took0.154714693s and replay checks0.144580738s.
Source/prefix loading took0.321728475s and0.289917835s respectively. The shared
loader still materializes339 columns before slicing9; its entire actual cost
is included. The no9-clique check is included in both bodies. These are one
new fixed construction and one replay, not a q/precision search, and their
costs are additional to the339-column experiment.

Code/proof development,
the first support inspection, tool startup and model inference are additional
and not fully metered. There was one prescribed modular construction attempt,
zero failed rank rows, and no prime/prefix search in each of the two separately
specified constructions. The lack of a9-clique is a failed proposed necessity
mechanism, retained rather than reinterpreted as a sharp result.
