# Independent receiving check

**Status: PASS, first execution.** This review is source informed: the producer's
saved JSON schema and graph-label convention were read. The checker imports only
Python's standard library. It does not import or execute the producer's graph
builder, port algebra, generic incidence decoder, receiving script, or old
scientific experiment.

The preceding independent finite-certificate gate remains the all-depth proof
input. This receiving check concerns the three actual saved applications of that
construction and the exact inherited Q8 witness.

## Operation checked

`verify_receiving.py` parses each original supplied expression into independent
immutable syntax trees. It decomposes a path of length at least two into length
two and possibly one length three, and associates all series joins. It compares
that syntax with the saved normalized expression. A separate recursive uncolored
graph builder then reconstructs the exact saved vertex labels and edge order.
Repeated expression IDs expand to disjoint copies except at declared terminals.

The checker verifies connectedness, simplicity, the two distinct nonadjacent
degree-one terminals, maximum degree at most four, and every saved family count
and root signature. It checks the actual coloring both by excluding a
bichromatic four-vertex path and by constructing every nontrivial bichromatic
component and verifying that it is a star. No bounded-size sample is used to
infer the general coloring theorem; the earlier 200-witness gate and local port
lemma supply that theorem.

All matrix and action computations use exact `Fraction` arithmetic. The input
diagonal and every supported edge are arbitrary prescribed nonzero rationals,
and all four original full-support action columns are explicitly recomputed.
The saved nonzero rational noise is then added and compared cell by cell with
the saved observation. There is no reduced-support action oracle.

## Independent least-squares formula and error proof

For one bichromatic star with center `c`, leaf set `L`, and `d=|L|`, let
`y_c` be the center observation in the leaves' color and `y_l` the leaf
observation in the center's color. The unsigned-incidence least-squares solution
is

\[
 \delta=\frac{y_c-\sum_{\ell\in L}y_\ell}{d+1},\qquad
 \widehat w_{c\ell}=y_\ell+\delta.
\]

This follows directly from the normal equations: if
`s=sum_l w_(c,l)`, then `w_(c,l)=y_l+y_c-s`, and summation gives the formula.
The case of one edge gives the average of its two observations; either endpoint
can be chosen as center. The free diagonal is read from each vertex's own-color
action cell. Every other unused action cell is discarded.

This is a different implementation from the producer's signed-incidence mean
projection followed by subtree summation. The independent formula reproduces
every saved output coefficient exactly. The checker also verifies the separate
normal equations in action coordinates: diagonal residuals vanish, and the two
action residuals incident to each edge sum to zero. Since the action map is
injective on the supported symmetric matrices, these equations uniquely identify
the orthogonal projection of the observation onto its range. Consequently the
stored **projected-action residual** is zero. The raw observation residual need
not be zero because arbitrary noise can have a component outside that range.

For a star, its unsigned-incidence Gram matrix is
`B^T B = I + 11^T`, so its smallest eigenvalue is at least one. Its least-squares
inverse contracts Euclidean coefficient noise by at most one. Distinct star
blocks use disjoint action cells, and the diagonal cells are separate. Therefore

\[
 \|\widehat D-D\|_F^2
 =\|\Delta d\|_2^2+2\|\Delta w\|_2^2
 \le 2\|E\|_F^2,
 \qquad
 \|\widehat D-D\|_{\rm op}\le\sqrt2\|E\|_F.
\]

This all-noise bound is independent of graph size and uses the original absolute
Frobenius action-noise convention. Each coordinate query row is a unit vector.
The squared constant two is supplied by this Gram argument, not a larger generic
tree row-sum estimate and not an empirical ratio on the saved noise.

## Saved applications

| Saved application | Vertices | Edges | Maximum degree | Maximum bichromatic star order | Noise Frobenius norm squared | Actual matrix error Frobenius norm squared |
|---|---:|---:|---:|---:|---|---|
| `star_three_obstruction_17` | 17 | 20 | 4 | 3 | `1632/1018081` | `9395/9162729` |
| `arbitrary_paths_and_both_parities` | 59 | 72 | 4 | 4 | `5531/1018081` | `142603/36650916` |
| `same_saved_Q8_support` | 1788 | 2042 | 3 | 3 | `171549/1018081` | `586391/6108486` |

For each row, noiseless reconstruction is exact, the saved noisy output agrees
with independent least squares, and the exact actual error satisfies the
all-noise squared bound two. The 59-vertex input includes path length seven,
series arity five, binary series, and all four guaranteed state families. This
is a receiving use of the final path-leaf extension, not merely a port response
test. The 17-vertex use is the same grammar expression whose star-three
obstruction was separately checked; this receiving gate does not repeat that
enumeration.

## Q8 provenance and inherited witness

The native Cycle6 archive is authenticated at 168,937 bytes and SHA256
`1c45c5708be5f277f6ae881f3d2e7e0598fe9b79cd943d8afcc42a3e404041cb`.
Its `results/failed_even_series_rotation.json` member is compared byte for byte
with the supplied selected copy, which has 136,415 bytes and SHA256
`18dcb6f78241dd5b89c7048b74e3e883cd674db5f75dc12f69d21aa0bd1bba3a`.
The new Q8 graph has exactly the same labeled edge set and original expression.

The new receiving witness has the identical native nonzero supported matrix
coefficients, zero diagonal, and native unit edge `(2,5)`. Recomputing its new
four-column action gives

\[
 \|W X_{\rm new}\|_F^2=\frac{2499892216}{268402689},
\]

and the independent star inverse recovers that witness exactly. The old
three-column action norm squared `256/16383` and old inverse lower bound squared
`16383/256` are authenticated received values. They are deliberately **not
recalculated** in this check.

This establishes an actual transfer of the same matrix witness and support to
the new stable four-query operation. It repairs the specified failed coloring
with one more query. It does not prove an arbitrary-real three-query lower on
Q8, compare matched query counts, establish historical priority, or imply an
application runtime or physical-performance gain.

## Replay and limits

Run from the return directory:

```text
python verification/receiving/verify_receiving.py
```

The unchanged native Cycle6 archive belongs in `sources/`; the checker also
accepts the exact same pinned file beside the working directory for the original
authoring layout. A later portability-only change added this preferred packaged
location; it did not alter any calculation, and no second scientific run was
performed. All numerical inputs and saved outputs remain unchanged.

The source hashes and exact gate output are in `RESULT.json`. This review and
the executable support internal correctness of the stated operation. They do
not establish external acceptance, graph recognition outside the supplied
grammar, a complete four-query theorem for degree-four partial two-trees, or
historical novelty. Costs below exclude unknown discovery and authoring totals.
