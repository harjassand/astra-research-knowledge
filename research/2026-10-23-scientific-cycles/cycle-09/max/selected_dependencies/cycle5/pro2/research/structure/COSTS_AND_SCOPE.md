# Scope, actual evidence, unsuccessful reasoning and observed costs

The new contribution is the all-size long-triangle-strip elimination and
arbitrary-end-color extension theorem in PROOF.md. It uses the unchanged
Cycle4 classification of genuine degree-four 2-trees and its period-nine
bichromatic-component lemma as dependencies. Those old calculations were not
replayed or counted as new research. The new finite tests concern144 boundary
transitions and a two-strip/square receiving operation.

## Actual exact diagnostic

`check_strip_extension.py` verifies all144 length-six ordered-pair transitions,
then every prescribed pair of endpoint colors for each strip length30,...,38
(1296 tests). This is a diagnostic over all core-length residues and all end
states; the proof, not increasing tested size, covers arbitrary strip length.
Every saved test was proper and acyclic, had no bichromatic component meeting
both ends, and observed maximum component size9 (the theorem uses16).

The new mixed fixture has99 vertices and194 edges: two triangle strips of
orders60 and39 connected along their end edges by a square. Removing long
strip interiors gives8 vertices and6 edges. All original edges, strip orders,
reduced and extended colors are saved in RESULT.json. It demonstrates the
actual receiving interface; it is not a new extremal lower, an all-graph
coloring solver, or a numerical performance benchmark.

## Recorded script executions, including authoring verification

| Run | Purpose / change since preceding run | Body wall s | Body CPU s | Peak process RSS bytes |
|---|---|---:|---:|---:|
| 1 | Initial boundary table and new mixed-fixture check | 0.09500449200277217 | 0.095007124 | 10,354,688 |
| 2 | Triangle extraction changed from union/find to direct incidence traversal | 0.0952649940008996 | 0.095253532 | 9,437,184 |
| 3 | Removed repeated global edge scans and unnecessary component sorting | 0.09130077699956018 | 0.091255850 | 10,354,688 |

All three passed; there was no failed numerical run or precision tuning.
Total observed diagnostic body wall is0.281570263003232s. The saved RESULT.json
is run3. Earlier metrics are retained here because overwriting the finite
result does not erase the cost of authoring verification.
The measured body excludes Python startup/import and the fixed transition
table construction performed at import; these were not separately timed.
A later optional `--output PATH` interface allows a receiving replay to leave
the frozen saved result unchanged. This argument-parsing-only edit was not
counted as another scientific run.

Two additional tiny authoring snippets enumerated reachable-state cardinalities
and printed the twelve canonical boundary words. Their body times were not
instrumented; tool outer wall was below0.001s each. They are not zero-cost.
Two focused primary-literature search calls reported rounded outer latencies
2.4s and2.1s. They did not establish a new theorem used in this proof or historical
priority. They returned broad acyclic/star-coloring material but did not settle
the four-color bounded-component question. No downloads or paid computation.

Proof discovery, source reading, note authoring, contributor/reviewer exchange,
total inference/CPU/wall across services, cost in money and energy are unknown
or unmetered, not zero. The small script times are not the cost of discovery.

## Operation cost and error boundary

For a degree-four support, triangle enumeration, component traversal, validated
strip ordering, reduction and extension take O(n+m) set/arithmetic work and
storage under ordinary unit-cost vertex indexing. The fixed144 transition
table is independent of input size. Actual integer bit cost and input reading
remain chargeable. The graph's treewidth is a mathematical premise, not a
certificate manufactured by this extractor. The implementation verifies the
actual strip pattern, degree cap and internal saturation used by the transfer.

The unresolved coloring of the reduced graph is an explicit input; its discovery
cost is not counted free. After extension, the *original* graph and coloring
go to the global coordinate decoder. Original action cells cannot be treated
as independent reduced-graph observations. Four matrix actions, observation
reading, decoder arithmetic and any rigorously bounded residual have their
usual costs. There is no application timing, NIST advantage or molecular claim.

## Failed or insufficient premises retained

1. A bounded tree-partition or a low-degree elimination order alone does not
   prove four-color bounded components: two alternating palettes can propagate
   bichromatic paths/trees through arbitrarily many bags. That route was not
   promoted into a global stability theorem.
2. Maximum-degree-four does not make every triangle component bounded. Squared
   paths are arbitrarily long; the operation therefore removes them through
   explicit boundary resets instead of assuming bounded pieces.
3. The clique-attachment lemma alone does not control a mixed square/long-cycle
   hierarchy. It is structural capital, not the missing whole-class coloring.
4. A supplied reduced coloring is not automatically the original operator's
   recovery plan. The full-support global decoder is essential.

Historical originality is unassessed. The focused independent reviewer may
record a proof review separately. A finite check and an internally accepted
proof are not external scientific acceptance.
