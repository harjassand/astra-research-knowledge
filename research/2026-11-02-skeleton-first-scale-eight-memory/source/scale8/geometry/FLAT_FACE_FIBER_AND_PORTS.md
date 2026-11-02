# Actual flat-face relative fiber: ten syndrome classes and their boundary maps

## Decisive check

Under the *naive* old-parent-face filtration, exclude old-boundary sheet edges and the vertical cylinder edges at rib endpoints. The flat doubled two-rib unit, after topological subdivision compression, has

    dim C0=8, dim C1=28, dim C2=30,
    rank δ0=8, rank δ1=20,
    H0=0, H1=0, dim H2=10.

The generator columns are the24 blue attaching triples and4 degree4 vertical-cross repetition columns. `flat_parent_face_fiber_test.py` constructs the full polygon incidence, checks δ1δ0=0, and computes these ranks. The compression is used for relative topology only; it is not declared a Hamming isometry of the full physical sheet.

Consequently one cannot simply assume a two-dimensional H2 face fiber copied from the random construction. The larger quotient does NOT imply extra logical qubits: H1 of this fiber is zero. It contains central metacheck and boundary-carry information.

## Explicit ten-dimensional dual basis

Label the nine regions of each sheet by j=(x,y), x,y=0,1,2, with central region(1,1). Let

    λ_A = sum of all nine A-sheet region faces,
    λ_j = A_j+B_j+the cylinder bands on the rib boundary of region j.

These ten rows are independent and annihilate all28 local edge columns. Their relation with the whole B sheet is

    Σ_j λ_j = λ_A+λ_B.

The central λ_(1,1) is precisely the six-face cube metacheck. It has no coupling to any boundary port. The eight outer λ_j are explicit relative boundary carries.

## Projected boundary columns

Use quotient coordinates (λ_A,λ_j). A formal single-face boundary port has projection:

* A-sheet edge adjacent to region j: e_A+e_j;
* B-sheet edge adjacent to region j: e_j;
* vertical rib endpoint between adjacent outer regions j,k: e_j+e_k.

The vertical endpoints therefore couple the eight outer region carries along their perimeter cycle. These formulas are checked column by column in `flat_fiber_boundary_projection.py`.

**Sheaf qualification:** a formal single-face boundary port is a coordinate in an old edge's incidence space. At an actual shared old edge, only combinations allowed by its inherited F_e are physical correction columns. For instance a degree3 blue edge supplies the sum of its three face ports, not independent single-face flips. The projection table must be multiplied by that actual inclusion matrix when gluing neighboring parent faces.

All32 formal boundary ports have quotient rank9. The one remaining annihilator is the central cube metacheck. Thus this local distinction between closed metachecks and boundary modes is exact, not inferred from a drawing.

## First-step consistency check with actual seed colors

In the explicitly specified reduced hashtag-cylinder realization of the source's single-square seed, take opposite y boundaries blue and opposite x boundaries red; vertical endpoints inherit those colors. The compiled complete cochain matrix has

    dim C0=16, dim C1=44, dim C2=30,
    ranks16 and27, H1 dimension1, H2 dimension3.

Thus the constructed first-step realization preserves the single logical qubit, despite having additional check relations. Of the formal boundary ports, the actual seed permits a rank7 projected subspace. Its three surviving metachecks are the three region-prism rows in the middle strip. This is a topological/reduced-complex consistency check, not a full raw geometric atlas or all-scale distance/lifetime theorem.

## Positive consequence for the next map

If a complete boundary circuit cancels all eight outer λ_j carries, then the two whole-sheet parities obey λ_A+λ_B=λ_center. On a valid global syndrome λ_center=0, so the two parities agree. This is a concrete algebraic origin for a paired check carrier. Establishing no-loss carry cancellation and consistent coarser incidence remains the real step; these equalities do not make the carries vanish automatically.

## Complete exact flat-fiber flow metric

The entire quotient has a useful graphical representation, not just selected boundary columns. Use eleven vertices: an omitted reference vertex0, the whole-sheet vertexA, and nine region verticesj. Each of the30 reduced face-syndrome bits is a graph edge:

    physical A_j: A--j,
    physical B_j: 0--j,
    cylinder band between neighboring regionsj,k: j--k.

Its binary flow boundary, omitting vertex0, is precisely the ten quotient coordinates. Each local sheet attaching correction is a triangle cycle through A or0; each vertical rib-cross correction is a four-edge region-grid cycle. Their rank20 equals the full graph cycle-space rank30−11+1, so they generate every zero-boundary flow. Therefore local syndrome coset minimum equals minimum occupied-edge count for the specified flow boundary.

`flat_fiber_flow_metric.py` computes exact shortest-path sections for all1024 quotient classes. Their minimum weights have distribution

    weight0:1, weight1:30, weight2:225,
    weight3:484, weight4:247, weight5:37.

The desired lone A charge has exact cost2, realized by any path0--j--A. No one-edge representative exists. This proves the full local factor-two terminal metric once all region carry charges are balanced, while preserving all unmatched classes instead of discarding them. The table is suitable for finite carry-potential optimization or for auditing a chosen section. It does not by itself prove global matching or logical stability of a metric decoder.
