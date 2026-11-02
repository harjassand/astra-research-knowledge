# Root's blue-cross packet metric: local obstruction repair and operation inventory

This tests a positive metric proposal from root. It is not yet a complete explicit-family decoder theorem.

## The hard packet test

The complete reduced first-step seed permits no single auxiliary syndrome after Rep4 tree resolution. However an adjacent-arm resolution at each of the four central crosses admits a **valid two-auxiliary diagonal packet**. The program solves an explicit physical Pauli-column witness for it. Its minimum coarse weight among the two local resolution sections is4, although its fine syndrome weight is2. Opposite-arm resolution has different behavior. See `rep4_aux_packet_test.py/results`.

This invalidates a raw columnwise Hamming-nonincreasing refinement claim. It is not a logical low-energy path or a lifetime no-go: no repeating hierarchy cycle or nontrivial logical class was established.

## A uniform finite packet norm

For physical X-syndrome face coordinates, allow atoms consisting of:

1. any single face;
2. any two faces incident on the same CURRENT blue degree4 edge.

Allowing all six pairs avoids needing the exact arm grouping to define the metric. Let μ(σ) be minimum atom count whose XOR is σ. Then

    |σ|/2 ≤ μ(σ) ≤ |σ|.

The lower bound follows because every atom has at most two coordinates. The upper bound uses singletons. This is a decoder metric, not a Hamiltonian modification.

Equivalently μ is the minimum number of unmatched occupied vertices plus matched pairs in the allowed pair graph induced on supp(σ). To see why intermediate canceled vertices do not improve it, decompose any chosen pair-edge subgraph into paths between odd-degree vertices and cycles. Replace each path of length≥2 by its two singleton endpoints at no greater cost; length1 paths are disjoint matching edges. Cycles can be discarded.

## Exact elementary projection

For a Rep4 edge replaced by two Rep3 edges, in coordinates four old faces plus auxiliary a, take

    g1=(1100,1), g2=(0011,1),
    P2(a)=1100, P2(old faces)=identity.

The projected auxiliary has packet cost1. The code verifies P1, inclusion I1, and homotopy h2, including 1+IP=hd in degree1. For a Par4 edge resolved into two Par3 edges choose P2(a)=1000; this has ordinary cost1. Both32-syndrome tests pass, without restricting to admissible syndromes. See `degree4_packet_projection.py/results`.

Thus the diagonal valid auxiliary packet above has coarse packet cost2, not4. The raw obstruction is repaired without assuming an unseen extra energy defect.

## Timing and geometric inventory to verify globally

The source's refinement resolves old degree4 glued crosses into degree3 junctions. Its other listed refined structures are T junctions (degree3), distinct free-cross edges (degree2), and recursive T-derived overlapping but abstractly separate edges. New degree4 edges are created by doubling at glued crosses; they are vertical cylinder edges, blue in RX and red in RZ. T seams retain old color but have degree3.

Under that actual operation inventory:

* RX: every current fine blue-pair atom is entirely in the new cylinder, so both first-sheet syndrome projections kill it. A fine sheet singleton projects through ordinary subdivision or a Par4 resolution to at most one old face. Consequently the sum of the two coarse packet costs is at most fine packet cost, atom by atom.
* RZ: there are no new blue4 pair atoms; old blue4 edges were resolved. A fine singleton projects through a Rep4 resolution to one allowed old pair, or through ordinary cells to one old face. Thus the total-parity projection is packet-nonincreasing, if the actual red cochain projection has these declared columns.

The proposed RX min-copy decoder would therefore contract μ by1/2, while RZ would not increase it. This does not depend on the actual Rep4 split selecting adjacent or opposite arms.

## Locality

A current degree4 glued cross lies inside one old parent face's hashtag. Its pair atoms use only that face's cylinder bands; a degree3 T seam does not create pair adjacency to another parent face. Hence this new packet adjacency has bounded degree and, for the declared gadget atlas, bounded per-parent-face component size. It introduces no intended hierarchy-dependent discount. Charged decoder components should include allowed-pair adjacency and the input preimages needed for coarse packet ownership.

## Exact remaining obligations

1. Verify the degree4 timing inventory for every actual recursive box, not only the standard pictures.
2. Supply globally consistent parent-cell projections including all degree4 tree resolutions and shifted rib endpoints; check the atomwise column list against those matrices.
3. Prove the red physical-X cochain projection is the proposed total-parent-face parity map, including edge/vertex fibers.
4. Establish common-lift alignment and charged-component logical stability/witness growth.
5. Handle the opposite physical error sector with actual bounded dual maps, not an unproved lifetime-duality assertion.

The metric repair is a promising concrete mechanism and survives the explicit valid auxiliary-packet test. It has not yet certified the full practical-scale memory family.
