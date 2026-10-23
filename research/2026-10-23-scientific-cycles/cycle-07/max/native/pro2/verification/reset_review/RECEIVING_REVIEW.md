# Final source-bound receiving check and focused graph-proof review

Reviewer: `cut_balance_challenge`, Cycle6 PRO2. This is the requested final
fixed-input verification gate. It does not replay the producer, old Cycle5
fixtures, or any application benchmark.

## Verdict

The first and only independent receiving-check run passed all three supplied
records. The executable is `verify_receiving.py`; exact results and input hashes
are in `RECEIVING_RESULT.json`. No producer module is imported. The producer's
source was read for the record format and deterministic labeling convention;
this is independently implemented verification, not a claimed blind review.

| Exact saved input | n | m | Degree | Largest bichromatic tree | Result |
|---|---:|---:|---:|---:|---|
| Base paths, odd series and forks | 359 | 484 | 4 | 9 | Three-query row certificate C^2=17 |
| Arbitrary paths, odd series and forks | 218 | 245 | 4 | 11 | Three-query row certificate C^2=19 |
| Failed even-series rotation Q8 | 1788 | 2042 | 3 | 256 | Exact inverse lower squared16383/256 |

## What was actually verified

The checker independently reconstructs the labeled support and colors from
the supplied expression, using recursive grammar semantics instead of the
producer's iterative builder. Repeated node IDs are copied as declared.
The fixed examples have expression depths7,5 and16. This checker is for these
saved inputs; it does not replace the production builder's all-depth iterative
implementation or claim an unlimited Python-recursion execution interface.

It then checks the materialized graph independently: canonical simple edges,
connectedness, proper three-coloring, maximum degree, degree-one distinct
terminals, absence of bichromatic cycles and terminal transmission, actual
boundary profiles and root symbolic graph counts. It checks the supplied
adjacent-degree-four witnesses on both positive supports.

For all bichromatic trees, it recomputes component sizes, every edge's exact
cut mass, M, independently chosen centroid orientations, row certificates,
and the inherited Frobenius certificate. In both positive cases the recorded
winning constant is the exact graph-specific row certificate:17 and19.
Thus the check establishes an all-noise bound for each fixed graph and seed,
not merely success on the saved noise vector.

All actual matrices, actions and noise are checked with `fractions.Fraction`.
The checker recomputes the complete sparse symmetric product DX, including
all free diagonal entries, adds the saved full three-column noise, and matches
every observed entry. It constructs the orthogonal action-range projection
independently by signing each pair component and subtracting its mean.
The recovered supported symmetric matrix has action equal to that projection
entry for entry. Forest injectivity makes it the unique projected-action
solution. No independent floating eigenvalue calculation or solver status is
used. The noiseless product is also checked to lie exactly in the signal range.

The exact saved quantities reproduced were:

| Input | Noise squared Frobenius norm | Error squared Frobenius norm | Error maximum absolute row sum | Projected residual |
|---|---|---|---|---|
| Base paths | 86167/994009 | 1473287741/16102945800 | 65/997 | 0 |
| Arbitrary paths | 52374/994009 | 111049929367/2386859141205 | 6859/98703 | 0 |

The error row sums satisfy their certified operator budgets. These are
conservative operator bounds, not claims that a row sum equals the spectral
norm or that the uniform theorem constants are sharp.

For Q8, all nonzero witness matrix edges are checked against the original
support. Direct multiplication reproduces the complete stored sparse action,
including the absence of extra nonzero cells. Removing the selected edge from
the256-vertex boundary tree independently gives cut sizes127 and129. The
signed action is constant on each side, with opposite signs and magnitudes
1/127 and1/129. The cut coefficient has absolute value one. Hence

    ||DX||F^2 = 1/127+1/129 = 256/16383,
    ||D||op >= 1,
    rho^2 >= 16383/256.

This is a verified failure of the recorded three-color design. No all-design
graph obstruction is inferred.

## Focused review of the new graph-property assertions

The main path-leaf grammar's chordlessness and two-connectivity assertions
are correct. The full argument is worth stating explicitly:

1. Every vertex lies on a simple terminal path. This holds for a path leaf.
   In a series production, extend a selected child terminal path through
   arbitrary paths in the other children. In a parallel production, extend
   a selected child's terminal path through the two new exterior stubs.

2. Every simple terminal path is induced. A series path traverses its children
   in order, with no inter-child edges except their shared junction. A parallel
   terminal path traverses exactly one child: switching children would revisit
   one of the shared terminals. Its only additional edges are the exterior
   stubs; there is no direct edge between the parallel join vertices.

3. Any cycle crossing parallel children consists of one terminal path in each
   of two children. The paths are induced, there are no cross-interior edges,
   and there is no edge between the shared endpoints. Thus no such cycle has
   a chord. All other cycles lie in a child. A series join cannot make a new
   cycle across its cut vertex. Since every child terminal path has length at
   least two, a new parallel cycle has length at least four. This proves both
   chordlessness and triangle-freeness for all path-leaf instances.

4. Remove the two exterior degree-one vertices of a P_b node. The remaining
   graph is the union of at least two child networks on shared endpoints a,z.
   If an internal vertex v is removed, choose a different intact child to
   connect a and z. Every surviving vertex w in the affected child still
   connects to at least one endpoint: take a simple a-z path through w and
   use its segment from w to the endpoint lying on the side away from v.
   If a itself is removed, the segment from w to z on such a path avoids a;
   deleting z is symmetric. Thus deleting any one vertex leaves a connected
   graph, proving two-connectivity of this core.

5. A clique cutset in this triangle-free two-connected core cannot have size
   one or at least three. If an adjacent pair a,z were a cutset, every component
   after its removal would meet both a and z, by two-connectivity. Paths through
   two distinct components would form a cycle on which edge az is a chord.
   This contradicts chordlessness. Hence the core is a chordless atom with no
   clique cutset. Exterior stubs remain present in the actual recovery input;
   the full graph with degree-one terminals is not asserted two-connected.

The optional arbitrary-path leaves retain all these properties. The more
abstract supplied-module *coloring* extension in Section4 does not itself
imply graph degree, series-parallel structure or chordlessness: corresponding
structural hypotheses on those supplied modules must be retained if those
additional claims are made. This qualification does not affect either actual
positive input or the main theorem.

## Remaining proof and scope assessment

The all-depth odd-series invariant and path-leaf enlargement in the actual
root PROOF.md agree with the earlier focused review. At an odd series junction,
only one boundary component from each neighboring child can meet, because
no child transmits. Low and high profile slots are not exchanged. The length-
three optional leaf word and the periodic longer-leaf rule are proper,
separated and have bichromatic runs of at most four vertices. Therefore the
stated beta=K0=4 and K=31 extension is valid.

The principal result remains conditional on a supplied admitted grammar.
Recognition of arbitrary supports, the full four-versus-five question,
historical priority and physical/application speedup are not established by
this checker. The source explicitly charges expression reading, full actions,
preparation, exact arithmetic and the residual boundary.

## Replay and observed cost

From the archive root, a receiving agent may run

    python verification/reset_review/verify_receiving.py --input-directory results --output /tmp/pro2_cycle6_receiving_check.json

This leaves the frozen saved result unchanged. The first actual run here had:

- Body wall0.07819296499656048s, including input reads and verification.
- Body CPU0.078194209s.
- Peak process RSS15,859,712 bytes.
- Output serialization and process startup excluded from that body timer.

Proof reading, checker authoring, mathematical review, messages, service and
integration are additional and unmetered, not zero. No numerical tuning,
failed first run, broad sweep, producer rerun, package install, external
write, or paid computation occurred in this final verification task.
