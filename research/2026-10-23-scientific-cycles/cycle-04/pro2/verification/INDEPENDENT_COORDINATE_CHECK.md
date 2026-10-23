# Independent exact receiving check

The checker `independent_coordinate_check.py` was written without reading or
importing the producer implementation in `src/coordinate_decoder.py`. It reads
only the saved data `results/coordinate_operations.json`, reconstructs the
coordinate action directly, discovers bichromatic components by a separate
breadth-first traversal, and solves each incidence normal equation by exact
Gauss–Jordan elimination. Mathematical input arithmetic uses Python
`fractions.Fraction` exclusively. The largest linear system has order four.
No floating matrix solver or large dense matrix is used.

The one execution passed. Its complete machine-readable record is
`independent_coordinate_result.json`. The checked input has 284,861 bytes and
SHA-256
`86c3ae6ad78a6cb5ba5f5b5069a99601d040b560581fead5a197fb7b048ec2d5`.

## Checked obligations

- The support edges and coefficient records are complete and unique, and the
  coordinate colors are proper. Every probe row therefore has norm exactly one;
  free diagonal coefficients occupy their own color cells.
- Every noiseless reconstruction equals its source diagonal and off-diagonal
  coefficients. Every saved noisy output equals the independently solved output.
  The saved Frobenius noise and error squared norms match exactly.
- Every period-nine component in both supplied bandwidth-two fixtures is a
  path with at most five vertices. The full fixture has exactly the support of
  the squared path. The second fixture is a bandwidth-two subsupport.
- The five-query comparator has matching components. No coefficient action
  cells collide: diagonal entries appear once and off-diagonal entries twice.
  This verifies Frobenius isometry on the supplied support, not merely on the
  chosen coefficient values.
- The good four-query prism seed has star components of at most three vertices.
- For each fixed graph/seed, the checker verifies the prescribed all-noise
  Frobenius bound, in addition to the particular saved noise. If `G=B^T B` is
  the incidence Gram matrix of a component and the squared advertised constant
  is `c2`, the exact Schur-complement test checks `(c2/2) G - I` is positive
  semidefinite. This implies `2 ||B^+||^2 <= c2`. The action blocks and diagonal
  cells are disjoint, so their inequalities combine by summing squares. The
  squared constants checked are `16/3`, `16/3`, `1`, and `2`, respectively.
  The rational `16/3` bound is weaker than the analytically sharp path-block
  constant `3+sqrt(5)`; this check does not replace that analytic argument.
- The witness support is independently reconstructed as two copies of the
  saved 127-vertex rooted tree with matching rungs. It has 254 vertices, 379
  edges and maximum degree four. The cut `(0,2)` independently separates the
  loaded layer into sizes 63 and 64. Its coefficient has absolute value one.
  The bad-seed action has magnitude `1/63` or `1/64` on each vertex of the
  corresponding side, and vanishes on the unloaded layer. Direct sparse action
  evaluation gives exactly `127/4032` squared norm. The same matrix under the
  good seed gives exactly `3167639/451584`. Thus the saved explicit bad-seed
  inverse lower squared ratio is `4032/127`. This is not a graph hard for every
  design: the good four-query seed on that same graph is also checked.
- The bicolored four-cycle is rejected by the forest decoder. Its supplied
  nonzero symmetric matrix has Frobenius squared norm eight and exactly zero
  action. Proper coloring and bounded component size alone do not suffice.

## Cost and scope

Exactly one verification run was executed; it passed without corrective reruns.
Body wall time was **0.052666757997940294 seconds**, process CPU time was
**0.052668796000000004 seconds**, and observed peak process RSS was
**13,099,008 bytes**. These body measurements include loading and checking the
input and exclude process startup, JSON schema inspection, checker authoring,
prior literature work, parent integration and private delivery. Those additional
costs were not individually timed and are not zero. The prior literature costs
are recorded separately in `research/literature/COSTS.md`.

This is independent concrete-data and fixed-graph block-norm verification.
It does not by itself establish the universal coloring theorems, historical
originality, a four-query result on every degree-four partial two-tree, or an
application speed advantage.

Receiving invocation from the checkpoint root:

```sh
python verification/independent_coordinate_check.py
```

The default input and output paths are relative to the checker's own location,
so that invocation remains valid after relocating the complete checkpoint.
Use `--output PATH` to direct a receiving replay outside the frozen result.
That command-line option was added after the first passing run without changing
the mathematical checker or rerunning it. The original receipt is unchanged.
