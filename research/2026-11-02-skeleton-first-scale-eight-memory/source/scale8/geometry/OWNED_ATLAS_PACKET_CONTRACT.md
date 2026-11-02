# Packet projection contract for the explicitly specified local template atlas

This records what can be owned as a construction, rather than claiming unknown source incidence. The atlas consists of ordinary cellwise subdivisions, the parent-ID three-page subdivisions in PARENT_FACE_COMPLETION.md, the explicit Rep4/Par4 tree resolutions, and the specified new blue/red attaching and crossing junctions. A complete recursive architecture must still match their external ports and verify its embedding, chamber structure, and logical maps.

## Cochain/metric columns for each owned template

### Ordinary parent-face and three-page subdivision

P2 sends each child face to its unique parent face. Internal degree2 pair columns project tozero. An inherited seam code vector f∈F_e projects to the same vector on its parent-face ports. Thus syndrome parity projection is a cochain map at C1→C2 and each child singleton has singleton cost. The full displayed three-page realization is independently checked by its disk/parent-ID construction, not by assuming unseen cofaces.

### Degree4 tree resolution

Rep4 is resolved by columns(1100,a),(0011,a). P2 fixes old coordinates and maps a→1100. Par4 is resolved by the two even-parity three-face spaces; P2 may map a→1000. The code computes P1,I1,h2 and verifies the transverse contraction identities. Hence the Rep auxiliary is one allowed blue packet, while the Par auxiliary is one singleton. All32 syndromes in both cases satisfy the packet inequality.

### New blue attaching/crossing junctions

At a blue attaching edge the column has two sheet-side faces in the same refined parent face and one cylinder face. First-sheet projection gives two identical parent labels, hencezero; the other sheet projection giveszero too. New degree4 vertical crossing columns lie entirely in cylinder faces and both sheet projections kill them. Inherited old-edge columns on a chosen sheet project by the original F_e inclusion. These are the local C1→C2 identities for P_A,P_B.

### New red attaching/crossing junctions

Each allowed column at a new red junction has even parity among faces of one refined parent face. Total-parent-face parity therefore sends it tozero, including the new Par4 crossing. At an inherited T seam, the actual F_e acts on different parent-face ports and projects to that same inherited F_e vector. This includes degree1 blue/red boundaries and degree2 sub-T cases. Composing with the refinement tree maps retains these identities.

These C1→C2 column checks do not alone establish the C0 map or a logical homotopy; those require the bounded chamber/costar construction. No such inference is hidden here.

## Alternating packet inequalities

Use all pairs incident on a current blue degree4 edge as permitted cost-one atoms. If the recursive timing inventory has all old degree4 edges resolved before doubling and only new cylinder glued crosses of degree4, then:

* RX fine pair-atoms are cylinder-only and are killed by both sheet projections. Every other fine atom is a singleton in one sheet or the cylinder, and its two projected costs sum to at mostone. In RX the previous new crossings are red, so any degree4 auxiliary in the refinement projects to a singleton via the Par4 map. Therefore

        μ_old(P_Aσ)+μ_old(P_Bσ) ≤ μ_fine(σ).

* RZ fine has no blue degree4 pair-atoms. Every singleton under total-parent parity plus refinement projects to a singleton or a cost-one blue Rep4 pair. Therefore

        μ_old(P_totalσ) ≤ μ_fine(σ).

These statements hold atomwise, even for inadmissible syndrome vectors; no unproved admissibility cancellation is used. The exact diagonal-auxiliary valid packet consequently causes no failure of these μ inequalities.

## Packet lookup and component ownership

On one hashtag, four glued crosses generate24 allowed pair atoms on12 cylinder-band vertices; the maximum pair degree is6. `packet_matching_certificate.py` checks all4096 patterns: XOR-atom minimum equals occupied-vertex matching minimum, and |σ|/2≤μ≤|σ|.

For charged-component decoding, include in the static input dependency graph:

1. all local linear-map/residual-row dependencies;
2. a clique on each fine packet block (at most12 faces);
3. for every coarse packet block, a clique on ALL fine input coordinates influencing that block through either P_A or P_B (or P_total).

Each preimage has bounded size by the actual bounded projection matrices. This ensures every fine packet block and every possible coarse packet block has a unique active component owner, regardless of which sheet is selected. Thus μ is component-additive and min-copy selection gives a componentwise factor1/2 in RX. The added edges do not create unbounded degree or pretend that the minimum-copy choice itself is constant-radius.

## What is still not a family theorem

The atomic maps and inequalities are verified for the specified templates. The all-family join still needs the external port atlas, source-compatible degree4 timing, shifted-rib alignment/chamber homotopies, red C0/logical maps, and the recursive logical-failure witness theorem. The physical Hamiltonian is unchanged by choosing μ; using an explicit completion of source incidence must be declared as such and globally embedded before claiming the requested architecture.
