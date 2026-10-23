# Independent Cycle10 receiving review

## Verdict and exact scope

PASS for all three saved NEW original-action operations in
`results/RECEIVING.json`: the 57-vertex theta support under the main block-reset
construction and the explicit theta construction, and the 30-vertex mixed
non-theta/cycle/triangle support under the main block-reset construction.
The same exact D and same exact absolute Frobenius noise are used by the
two theta operations. No historical suite, old closure or producer receiving
program was re-executed.

The verifier imports only Python's standard library. In particular, it does
not import `coordinate_decoder`, `block_reset_recovery`, `marked_atom`,
`theta_hub_split`, or any inherited producer module. It reads their bytes
only to bind the exact saved source identities.

## What was independently checked

1. Each input is a connected original simple support, degree at most four.
   An independent articulation-deletion algorithm reconstructs its maximal
   blocks. The source's low-link decomposition is not called. Each cut has
   exactly two actual blocks and degree two in both.
2. Complete original-cycle enumeration on these small blocks checks
   chordlessness; a successful degree-at-most-two fill elimination supplies
   explicit width-two bags. Fill edges appear only in this verification
   witness, never in a queried action.
3. All actual four-color rows are proper and all bichromatic components are
   trees. Every saved center/arm witness reconstructs its exact component,
   with disjoint arms of length one or two. Original edge support is retained.
4. In both main-construction operations, every local block record is bound
   to the original edge list and original vertex IDs. Independent expansion
   of the saved path/L/R/S/P expressions checks their exact support. The
   restored marked vertex is the actual stated degree-two root.
5. Raw and permuted local colors are checked directly for the star property.
   Actual root neighbor supports, far flags and multiplicities are recomputed.
   The saved permutation, parent support, shared channel and optional
   forbidden channel are verified. The code's deterministic minimum valid
   permutation is checked using the actual saved raw coloring, without
   reconstructing it from the old certificate table.
6. The non-theta operation actually exercises its compulsory message:
   the incoming edge is (6,11), the outgoing cut is vertex 11, its forbidden
   color is 3, and the receiving child block is 5. Its actual root-neighbor
   colors omit 3. This is not merely a nonempty message counter.
7. Every free diagonal and supported edge coefficient, every nonzero rational
   noise cell, all original noiseless actions DX, all observations DX+E and
   every output coefficient are reconstructed exactly.
8. The independent inverse solves Fraction normal equations for each actual
   unsigned-incidence component. It does not use producer subtree sums.
   Both noiseless and noisy outputs match. All projected actions, normal
   equations and raw residuals match exactly. The projected numerical
   residual is zero, while the raw observation residual is nonzero.
9. Squared matrix Frobenius errors and absolute action-noise norms are
   recomputed, and the bound against 3+sqrt(5) is checked by rational
   inequalities. Cut balances and maximum component sizes also match.

The scientific argument supplies the all-size bound. These finite independent
checks support the actual realization and full original-action receiving use;
they are not a substitute for the proof or a new application benchmark.

## Proof reading and one scope clarification

The current main proof preserves the previously reviewed one-message invariant.
It no longer assumes independently realizable profiles at several roots of
one block. The optional request constrains the next child and is always one
actual parent channel. Every inherited component is an isolated child edge,
and its endpoint message blocks another generation. The global result is a
base star with at most one pendant extension at each original vertex, including
extensions at the center and the base-single-edge case.

The native code is explicitly not advertised as a complete chordlessness
recognizer on all possible inputs. Coverage is proved on the stated class;
an accepted actual support is additionally certified by its returned coloring
and spider shapes. The proof makes this distinction correctly.

One wording correction was requested and accepted during this review:
"connected bridgeless graph" can include a single isolated vertex, whereas
the native main entry point requires a nontrivial block. The advertised
coverage should say "with at least one edge"; the isolated vertex has trivial
one-query recovery separately. This is a scope clarification, not a failure
of the nontrivial graph theorem or either receiver. No receiver was changed
or rerun because of it. The exact proof hash read by the executable gate is
recorded in `VERDICT.json`; later wording changes should be bound separately.

No remaining mathematical gap was identified in the all-depth gluing argument
within its degree-two, two-block-incidence hypotheses. Bridges, nonchordless
atoms and the full arbitrary-real four-query problem remain outside this
checkpoint. This review does not certify historical priority, external
acceptance, physical utility or all-source asymptotic implementation bounds.

## Observed cost

`COSTS.json` records the complete independent checking body, including native
source/input binding, both support checks, all three rational reconstructions
and serialization of `VERDICT.json`:

* Wall: 0.037147830000321846 seconds.
* CPU: 0.037145443 seconds.
* Peak process RSS: 13,570,048 bytes.

The final cost-receipt serialization, source reading, reasoning, authoring,
proof-review drafting and integration are excluded; their totals remain
unknown. There was no failed execution of this independent gate. Its first
recorded execution passed. The final code hash, verdict hash and exact source
bindings are in the machine-readable files.

Run the checker on an unchanged copy if another implementation check is needed:

    python verification/independent_receiving/verify_receiving.py

It overwrites only its own verdict/cost files. This command is a receiving
instruction, not a request to repeat the check merely for another receipt.
