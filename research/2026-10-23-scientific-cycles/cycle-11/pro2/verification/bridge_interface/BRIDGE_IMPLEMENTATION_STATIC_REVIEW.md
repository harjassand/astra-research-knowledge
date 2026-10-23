# Static review of the new native bridge implementation

Bounded independent bridge-interface contributor, Pro2 Cycle11, 23 October 2026.

**Verdict: PASS for the new implementation's correspondence to the proved
module conditions.** No correctness or asymptotic-complexity gap was found in
the requested branches. One nonfatal reporting limitation is recorded below.
This was source inspection only: no numerical receiver, old closure, historical
suite, or new scientific calculation was run.

## Exact inspected source

Root-owned `src/bridge_recovery.py` in
`Astra_Amplification_Cycle11_PRO2_20261023`, SHA256
`d054354fae97ca85dc225029cef023653010f292945735b2a663ca7c57a59c56`.

The inspection also compared the inherited actual implementations:

- `block_reset_recovery_legacy.py`, SHA256
  `fa28a2e59bcfd09a58ff48c0e3191cbe53b6c6700d08bd8fd8963590506380cf`;
- `coordinate_decoder.py`, SHA256
  `5e3c3f01f2297e2c8a59d4814543f4bdfa62eb6cace1320debe3fb76a1d4600f`;
- the marked normalizer and the new degree-three adapter already covered by
  the separate focused local review.

## Load-bearing checks

1. **Actual original bridge decomposition.** The iterative low-link routine
   uses the supplied simple original edge list, checks the degree-four cap,
   deletes exactly its bridges, retains isolated vertices, and orients every
   quotient-tree edge. Multiple connected components receive separate roots.
   The back-edge low-link update also sees finished descendants, which is
   harmless: their larger discovery index cannot lower the current low value.

2. **Rerooting at the actual entry.** `_reroot_atoms` requires that the actual
   entry belongs to exactly one nontrivial block, then rebuilds the atom
   parent/order/incoming/children fields from that block. All downstream marks
   therefore become the actual cuts in the newly oriented tree. It does not
   substitute a convenient terminal for the required bridge endpoint.

3. **Only one new qualification.** The degree-three oracle is called only
   when the root atom has an actual bridge entry of local degree three.
   Degree-two roots and every nonroot atom use the inherited marked oracle.
   The root permutation explicitly maps the actual root color to the assigned
   entry color and keeps the actual parent's color absent from its neighbors.
   The final module qualification checks that internal gluing preserved this
   absence. No extra independently prescribed root state is introduced.

4. **Inherited one-message rule.** The nonroot permutation test preserves
   the shared vertex color, allows at most one common channel, makes any
   common child channel unflagged, and obeys the one requested forbidden
   parent color. The code confirms that a common component is an actual
   isolated edge in that child, locates its actual other endpoint, and sends
   at most one request to its next atom. This is the Cycle10 rule, including
   collision rejection, with unchanged logical conditions.

5. **Same-entry bridge prohibition.** For each outgoing original bridge,
   `prepare_recovery` forbids the current vertex color. If its source is the
   module's actual incoming endpoint, it additionally forbids the actual
   parent endpoint color. This is exactly the omitted condition exposed by
   the triangle-chain failure. It also applies to singleton modules, whose
   only vertex is their entry, so an incoming pair cannot propagate through
   an isolated quotient vertex. At least two of four colors remain available.

6. **Isolated and disconnected input.** Empty-edge singleton modules are
   colored directly. A root singleton receives color zero; a child singleton
   receives its genuinely assigned color and uses the same reset for every
   outgoing bridge. Disconnected roots are independent. The native API
   explicitly requires n>=1; it does not claim an empty n=0 graph API.

7. **Actual resulting geometry.** The final plan is constructed on
   `form['edges']`, the full original support. Its inherited preparation
   rejects improper coloring and every bichromatic cycle. The new certificate
   checks each oriented bridge's actual child endpoint has degree one in
   its complete pair component. A nonbridge core must lie in one module,
   be connected, and pass the inherited arm-at-most-two spider check. Every
   added bridge must attach exactly one pendant leaf, with at most two per
   core vertex. Bridge-only components must be degree-four stars. These
   checks establish exactly the geometry used by the pendant-Poincare proof,
   rather than incorrectly requiring the entire component to remain a spider.

## Complexity and claim boundary

Bridge decomposition and module/atom traversals use linear arithmetic work.
There are only 24 color permutations per atom, and a child's search through
outgoing atom links occurs once per atom, so it does not introduce a hidden
quadratic depth factor. Each vertex belongs to at most two nontrivial atoms;
sorting and inherited normalization over all modules/atoms are bounded by
O(n+m log m), with fixed certificate preparation charged separately. All
component and original-action plan inspections have the same or lower bound.
Storage is O(n+m) besides fixed evidence and exact-integer bit lengths.
The code does not make rational arithmetic or action acquisition free.

The final finite checks do not recognize the advertised graph family, nor
prove successful construction on every input outside it. Their accepted
geometry is nevertheless enough to justify the same inverse on any extra
accepted support. The header states this distinction. No query-minimum,
all-real-design lower bound, optimal constant, or nonchordless all-size
guarantee is inferred from these output certificates.

## Nonfatal reporting point

In the inspected snapshot, `design['guarantee']` always records squared
constant 18, even if the bridge list is empty. This is valid but weaker than
the preserved Cycle10 `3+sqrt(5)` bound. Taking the minimum with the finite
trace/row certificates need not recover the stronger theorem. The principal
investigator was notified to retain that bridgeless bound explicitly in
conditional theorem metadata or the receiving result. No change to the
coloring or decoder is required. This review does not assert that a later
metadata correction has already occurred.

## Scope and costs

This check supplements the separate mathematical module/leaf proofs and the
18-target local review. It does not replace the independently owned exact
original-action receiver check. Static source-reading and reasoning time was
not measured; its total is unknown. Hashing binds the inspected files only
and is not scientific performance or a replay of their computations.
