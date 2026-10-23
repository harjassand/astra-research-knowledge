# Comparison for the owner's recursive parallel/series networks

## Frozen object and outcome

The owner supplied a terminal network grammar: a length-two path; parallel composition of two or three terminal-degree-one children, followed by one fresh stub at each end; optional odd series compositions with at least three children; arbitrary uneven recursion; and a further version allowing arbitrary path leaves.

This check sought an established coloring theorem matching that grammar. **None was identified in the inspected primary sources.** This is a bounded retrieval outcome, not a historical novelty claim. The root's proposed three-color, bounded-bichromatic-component proof was not independently reviewed by this literature task. Its uniform component bound and noise consequence must rest on the root proof/checker.

## Closest named construction: Laakso graphs, but different recursion

Sofiya Ostrovska and Mikhail I. Ostrovskii, *Nonexistence of embeddings with uniformly bounded distortions of Laakso graphs into diamond graphs*, Definition 1.2 and Figure 2:

https://facpub.stjohns.edu/ostrovsm/OstrovskV2.pdf

The primary definition starts with an edge and replaces every edge at each stage by a six-edge diamond with one stub at each terminal. The first replacement is exactly the owner's binary parallel operation applied to two base paths. Subsequent replacements also expand the stub edges. This differs from the owner's recursive operation that adds fresh, unexpanded stubs around parallel children. The full definitions and figure description were accessed; no metric-embedding theorem is used as a coloring result.

For the homogeneous binary owner subfamily, the edge recurrence is e_0=2 and e_(d+1)=2e_d+2, hence e_d=4*2^d-2. Standard Laakso graphs have 6^d edges. The shared six-edge first gadget therefore does not justify identifying the families at higher levels (14 versus 36 edges at the next level).

The same source defines ordinary diamond graphs by replacing every edge with a four-cycle. Those have no terminal stubs and terminal degrees grow. That family also does not identify the owner's bounded-degree grammar. “Laakso-like recursive terminal networks” is a descriptive analogy only; the explicit grammar is the scientific contract.

## A nearby coloring paper is about a different family

C. Renuga, D. Meiyappan, S. Prabhu, and M. Arulperumjothi, *Acyclic and star coloring parameters of fractal cubic networks* (2025):

https://www.nature.com/articles/s41598-025-96645-9

The primary construction starts from C4. At each stage it takes four disjoint copies and adds a cycle through one specified vertex of each copy. Its acyclic-three / star-four claims concern that construction. The exact graph definition was read to test applicability; the coloring proofs were not audited because the graph family does not match.

Directly from that definition, its cycles are joined at cut vertices. The owner's ternary first core contains K_(2,3), and even the binary second level contains a theta subdivision, so it is not a cactus family. The word “fractal” or “recursive” supplies no transfer.

## Strongest comparisons that remain applicable

- Generic partial-two-tree acyclic-three coloring is an exact identification comparator. It does not control the size of bichromatic trees, so it does not give the owner's dimension-independent stability claim.
- The already inherited general five-real-query operation remains an applicable stable comparator on treewidth at most two / maximum degree at most four. The inherited six-color star construction is the broad coordinate-color comparator. This narrow literature check did not improve either result.
- Wood's established exact-one-subdivision star-three result applies to the exact-one-subdivision subclass. Adjacent vertices of degree at least three exclude an exact-one-subdivision representation, so it cannot be invoked for the full supplied grammar. The stronger “every edge subdivided at least twice” star-four theorem also requires a separate valid representation; none was supplied here.
- The root's claimed gain is consequently a uniform error guarantee for a precisely specified recursive family using three queries, rather than a new generic acyclic-three query count. No application performance follows from this literature comparison.

## Search scope and costs

Four web calls; fourteen search entries and three open entries. Queries focused on Laakso/diamond graphs, glued or doubled trees, recursive series-parallel star coloring, and the closest returned fractal coloring paper. No matching primary all-size coloring theorem emerged. The PMC request was blocked by a browser challenge; the publisher's primary HTML supplied the actual construction. Unrelated modular-product “diamond,” historical circular “star coloring,” edge-coloring, and quantum-walk results were excluded.

Measured awaited web-call time: **21.527 seconds**. Complete mathematical assessment/authoring cost was not separately metered. No numerical run, old replay, package installation, paid resource, or external write.

Source retrieval refs for receiving lookup: `turn190view0` (Laakso/diamond definitions), `turn191view0` (fractal-network construction), `turn190view1` (PMC challenge). Detailed calls are in RECURSIVE_COMPARISON_CALLS.json.

