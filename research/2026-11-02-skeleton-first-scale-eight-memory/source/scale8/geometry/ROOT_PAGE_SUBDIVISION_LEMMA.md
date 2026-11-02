# Root constructive completion: relative page subdivision

2026-11-02. This specifies an abstract subdivision realization, not an inference that every coface omitted from a rendered source figure is absent. Its compatibility with the complete recursive geometry remains a separate check.

## Explicit parent-face convention
Each refined face carries its PARENT abstract face ID. New internal cells are identified only within that parent face. Distinct parent faces are glued only along their prescribed inherited boundary cells; equal embedding coordinates never identify abstract cells. Internal subdivision edges therefore have exactly two incident face pieces and repetition/parity code span(11). Old branching-edge segments retain their inherited sheaf code and incidence labels.

For source Figure20 left, the three displayed groups form disks after their listed shared edges are identified:
- above: internal RQ; exterior cycle O-R-A0-A1-Q-P;
- right: internal PD0; exterior O-P-Q-C1-C0-D0;
- below: internal PD1; exterior O-P-Q-D1-B1-B0.
Their common inherited seam is O-P-Q. D0,D1 remain different abstract vertices even if their images coincide.

For the right panel:
- above: internal PA1; exterior O-A0-A1-R-Q-P;
- right: internal PC0,QC1; exterior O-P-Q-R-C3-C2-C1-C0;
- below: internal PB1,QB2,QB4; exterior O-P-Q-R-B5-B4-B3-B2-B1-B0.
Their common inherited seam is O-P-Q-R. These boundary cycles follow by cancelling internal edges over F2, not by coordinate-based gluing. Every within-page dual adjacency graph here is a tree.

This gives an explicit three-page-book subdivision with the same face words as the displayed source portion. It resolves the finite conditional compression test for THIS realization. One must still verify that each page has the intended parent face and that its exterior boundary matches every neighboring recursive gadget; do not promote it to a completed source-family incidence reconstruction.

## Exact syndrome compression lemma
Take any parent page partitioned into finitely many faces whose internal degree-two dual adjacency graph is connected. Let P2 sum all its fine face-syndrome bits mod2. Choose one anchor face and define I2 to put the parent bit there. A fixed spanning tree of the dual graph supplies a linear correction h: route each non-anchor syndrome bit to the anchor using the associated physical internal-edge qubit columns (each flips its two adjacent fine faces). Then

 sigma + delta_fine h(sigma) = I2 P2 sigma,
 |P2 sigma| <= |sigma|,
 P2 I2=I.

The correction depends only on the page, has bounded support for a bounded-size page, and vanishes on zero. The final weight is nonincreasing; individual sequential moves need not be monotone. A deterministic bag containing the full page plus its correction columns makes the operation component-compatible.

Across a branching inherited edge, sum the fine segment labels in its fixed local code F_e to define P1. Internal-edge labels project to zero. Since F_e is linear and every boundary segment has the same inherited incidence pattern, one has the exact cochain identity

 P2 delta_fine = delta_parent P1.

This holds for either repetition or parity sheaf, including degree-one and degree-two subcases. The affine quotient of fine syndromes by internal-edge corrections is therefore exactly the parent face-bit space with its original inherited-edge columns. Its quotient Hamming cost equals the parent Hamming cost: parity gives the lower bound, one-anchor realization the upper bound. No extra factor is charged for degenerate geometric faces, because they remain ordinary abstract faces in the cochain complex.

For a chosen parent-edge insertion, its fine boundary face endpoints can be moved to anchors with h, yielding an explicit corrected lift I1 and delta_fine I1=I2 delta_parent. This is the syndrome/correction part of a chain contraction. Full C0/stabilizer/cohomology identification still requires the corresponding vertex-stalk maps or elementary cell-subdivision argument; it is not asserted merely from the C1-to-C2 identity.

## Why this helps and what remains
The lemma supplies an exact bounded-support, weight-nonincreasing lift of the reduced three-page transfer algebra when a genuine parent-face realization has been supplied. It does not create the global coarse map, paired-copy contraction, vertex carry constraints, or physical-Z decoder. Those are still the substantive gates. It avoids treating a missing raw incidence table as either a proved degree-two fact or an insurmountable obstruction: the abstract subdivision can be constructed explicitly and tested against the actual boundary attachments.
