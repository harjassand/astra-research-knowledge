# Independent check of the native atom receiving operation

**Verdict: PASS for the actual new native source, its complete normalization,
its four-action receiver, and the separate cycle/C3 branch records.**

Reviewer: `/root/cycle8_finite_gate`, 22 October 2026. The checker imports no
producer module. It reuses only its own previously authored, hash-pinned exact
receiving helpers in `../receiving/verify_receiving.py`. Importing those pure
functions does not run that module's main routine. The earlier A5 and mixed16
receivers and the finite closure gate were not rerun.

## 1. Actual sources and scope

The new input is `inputs/native_atom_9.json`, 458 bytes, SHA256
`0c0feabd40a60b8a64be468fbb62ed33d7622d51b80077c75674a21ea271c4aa`.
It supplies the original nine vertices and eleven edges, with no expression,
terminals, decomposition, or coloring. Its original vertex labels and all
eleven undirected support edges agree exactly with the receiving record.
The record's embedded original input agrees with the independently pinned
input object, not merely a summary or preparation receipt.

The receiving record is `results/native_atom_9_four_action.json`, 12,259
bytes, SHA256
`b296faff62ea21aca02f21dc36d2402557e5c534d4971cd6000e1c90a8cd4316`.
The separate branch record is `results/native_atom_branch_checks.json`,
3,014 bytes, SHA256
`f839dea60eb556a37e12c605d08c878ec3fd9d50a33cc1c9ca1401643d6d9751`.

The new checker binds those exact bytes. It does not import
`src/atom_normal_form.py`, a coloring producer, or the producer's decoder.
The literal coloring certificate's all-depth gate was completed separately;
its full search and gate are not repeated here. The saved `root_family`
identifier is not needed for this receiving check: the actual coloring is
checked directly on the original graph.

## 2. Normalization checked using actual support sets

The checker constructs each loaded node's actual vertex and edge sets from
its leaves and children. It does not accept local port counts or the saved
preparation trace as substitutes for those sets.

For a path leaf it checks all three distinct original vertices and the two
actual original edges. For an extension, the new terminal is outside the
whole child graph, the old terminal has load at most three, and the added
edge is one of the original support edges. For series, the child vertex
intersection is exactly the single identified junction. For parallel, that
intersection is exactly the two shared terminals. Every join also checks
edge disjointness, actual load sums, proper terminal identifications, and
the degree cap after the join.

At every node the two terminals are genuinely nonadjacent; all vertex
degrees are positive and at most four; and the module is connected. Each
node is used once in a rooted expression tree. At its root the vertex set
is exactly `0,...,8` and the edge set is exactly the original support. There
is no reduced-action oracle, duplicated edge, subdivision, or added edge.

The checked root terminals are `(5,2)`, with actual loads `(3,4)`. The
complete ten-node loaded result passes, including the new unequal-load
interface and its saturating parallel join. The exact vertex/edge sets,
shared vertices, loads and degree maxima for every node are retained in
`RESULT.json` under `native_normalization.node_trace`.

The recorded original-vertex suppression steps were checked separately.
Every suppressed vertex has degree exactly two in the current simple
reduction, is outside the protected edge `(0,2)`, and has exactly its saved
neighbors. The complete sequence ends at the protected edge and preserves
the degree cap. Opaque producer expression IDs and ordinary-node counts are
not used to certify the loaded expression. The final expression is checked
directly, so those labels cannot conceal a support or intersection error.

No normalization bug was found in this source. This is a validation of the
actual new normalization and reduction trace. The universal structural
theorem remains a mathematical proof obligation, rather than a conclusion
drawn from this one finite graph. The accompanying structural proof was
read for its hypotheses and triangle exception; this check does not replace
its separate all-size review.

## 3. Original graph class and star coloring

The checker independently verifies connectivity after deletion of each
vertex. It enumerates every simple cycle of this small graph and checks the
absence of every chord. There are six cycles, with lengths `4,5,6,6,7,7`.
No triangle occurs. An independently constructed fill/elimination trace
has at most two later neighbors at each step, certifying treewidth at most
two. The maximum original degree is four.

These are exact finite diagnostics. Exhaustive cycle enumeration and the
backtracking elimination search are not proposed as the preparation
algorithm or its complexity bound.

The actual four-coordinate colors are

```
[1,1,2,0,0,0,1,3,3]
```

The checker recomputes every vertex's neighbor-color multiplicity. The
arrays agree with both saved copies. The coloring is proper. For every
edge, at least one endpoint has only one neighbor of the other endpoint's
color; in this proper coloring this excludes every bichromatic length-three
path. Directly enumerated color-pair components are stars as well. Every
coordinate row has squared norm one, and all four colors are used.

The actual cycle `5-0-2-8-6-5` is present. A distinct tiny check enumerates
the `3^5=243` color assignments of C5 and confirms that no proper one is a
star-three coloring. This makes four optimal **for star-coordinate
coloring** on the new fixture. It does not exclude three arbitrary real
directions, nor other bounded-component three-coordinate designs.

## 4. Full original action and exact inverse

The matrix source exercises every free diagonal and every original support
edge with a nonzero rational coefficient. The saved noise is nonzero and
rational. Using the original support and the actual four-coordinate design,
the checker independently forms all entries of `DX`, then `DX+E`. Both
arrays agree exactly with the saved full original and observed actions.

For a bichromatic star with center data `y0` and `k` leaf data `yi`, the
checker uses the analytic least-squares formula

\[
\widehat d_i=y_i+\frac{y_0-\sum_jy_j}{k+1}.
\]

This independently derived block inverse is different code from the
producer's tree substitution. Own-color cells recover the free diagonal.
Noiseless recovery agrees exactly with all original coefficients. With
noise, all independently recovered coefficients agree with the saved output.

The full action of that output agrees with the saved projection. Every
diagonal normal equation and every edge normal equation is zero exactly.
The residual from the projected action is zero. The observed action itself
has a nonzero residual because it is projected; these two quantities must
not be conflated.

| Exact quantity | Independently checked value |
|---|---:|
| Vertices / original edges / actions | 9 / 11 / 4 |
| `||E||F^2` | `490/10201` |
| `||Dhat-D||F^2` | `26207/734472` |
| `||Y-Dhat X||F^2` | `2197/122412` |
| Residual from saved projected action | `0` |

The Frobenius error obeys the claimed squared constant two on this record.
For the operator certificate, the checker forms the complete rational matrix

\[
C=\frac32\|E\|_F^2I-(\widehat D-D)^2
\]

and computes an independent exact `LDL^T` recurrence. All nine pivots are
strictly positive, match the saved rational pivots, and reconstruct every
entry of `C` exactly. This certifies the stated operator inequality for the
actual saved noise/output without accepting a floating success flag. The
all-noise theorem still comes from the star-four/triangle-free recovery
argument, not from this one positive-definite matrix.

## 5. Distinct cycle and triangle branches

The five-cycle branch is checked from its actual five vertices and five
edges. All four loaded nodes preserve the original support, and its
terminal loads are `(2,2)`. Its actual star-four coloring and multiplicity
array pass. This is a structural and coloring branch check; the branch
record does not contain an additional matrix/noise receiving operation.

The triangle branch is exactly C3 with colors `(0,1,2)`. It has no
nonadjacent pair of terminals and is correctly kept outside the loaded
grammar. Its direct query design is `X=I3`; symmetrization of the observed
matrix gives both operator and Frobenius error at most `||E||F`. The
triangle-free `sqrt(3/2)` argument is not applied to C3. This branch likewise
contains no saved matrix/noise receiver and is not counted as one.

## 6. Scientific and computational interpretation

This source is an actual receiving use of graph preparation: the saved
native input supplies no expression, the output contains a verified
support-preserving loaded expression, and the complete original actions
are decoded afterward. It therefore tests a gap that an expression-only
fixture would leave open. It remains one small exact receiving calculation,
not a graph-recognition performance study, proof of a general algorithm's
correctness, or practical speedup.

The implementation sorts canonical edges; its actual preparation bound
includes `O(n+m log m)` work. A possible linear structural implementation
does not erase that cost in this implementation. Our finite diagnostic
enumerations are separate checking costs. The full original actions,
arithmetic precision, and downstream work remain charged.

The five-query general comparator and the four-versus-five question for
all degree-four partial two-trees are unchanged. A theorem on all
two-connected chordless atoms does not by itself stabilize arbitrary atom
gluing, triangle-containing supports, or unrestricted partial two-trees.

Historical priority, outside acceptance, application advantage and research
amplification are not established by this check. This receipt also says
nothing about Max reading or integrating the result.

## 7. Replay and dependency

From the archive root:

```
python verification/native_atom/check_native_atom.py \
  --output verification/native_atom/RESULT.replay.json
```

The checker reads its pinned original input and new receiving/branch
records and the pinned independent arithmetic helper. It deliberately
does not invoke `check_one`, the previous helper's main routine, the
coloring producer, or the finite certificate search/gate. The helper's
complete source is part of this return.

See `COSTS.md` for the measured new gate and its exclusions.
