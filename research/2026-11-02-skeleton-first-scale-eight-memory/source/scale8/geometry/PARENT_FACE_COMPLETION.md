# Constructive repair: an explicit parent-face subdivision realization

Root proposed this repair to the incidence evidence gap. The construction below specifies a local realization instead of treating missing coface lists as known. It proves the polygon compression for **this realization**. It does not assert that every unstated identification in the original paper has been independently recovered, or that all recursive gadget boundaries have now been joined.

## Definition

Start from a three-page book. Its pages are parent faces U,R,L. Their only shared edges are the inherited old seam. Every other parent boundary incidence is retained as a port for gluing to the surrounding complex. Introduce the exact source Example6.8 polygons within each page, tagging every cell by its parent-page identity except for cells on the inherited shared seam. Glue only:

1. the explicitly paired subdivision edges *within the same parent face*;
2. the inherited parent seam/boundary incidences.

No two abstract cells are identified because their embedded images coincide. In particular the distinct source labels P,D0,D1 and P,C0 or Q,C1 remain distinct where the source uses them to resolve a geometric coincidence.

### Left realization

Upper-page internal edge RQ; parent boundary O–R–A0–A1–Q–P.
Right-page internal edge PD0; parent boundary O–P–Q–C1–C0–D0.
Lower-page internal edge PD1; parent boundary O–P–Q–D1–B1–B0.
The inherited seam is O–P–Q.

### Right realization

Upper-page internal edge PA1; parent boundary O–A0–A1–R–Q–P.
Right-page internal edges PC0 and QC1; parent boundary O–P–Q–R–C3–C2–C1–C0.
Lower-page internal edges PB1,QB2,QB4; parent boundary O–P–Q–R–B5–B4–B3–B2–B1–B0.
The inherited seam is O–P–Q–R.

The code `parent_face_subdivision_certificate.py` checks every page is a disk: the polygon dual graph is a tree, each added polygon glues along one internal edge, the remaining boundary is a single cycle, and V−E+F=1. Thus this is an honest cellwise subdivision of the declared three-page book. All internal edges have physical face degree2 **by this specification**, and the inherited seam retains its original F. The 64/512-pattern coset-cost computations in `recursive_t_polygon_certificate.py` consequently become unconditional algebraic certificates for this specified realization.

## Embedding compatibility that is actually established

Use the source's vertex placements and face maps for these exact polygon words. The construction changes no polygon image, adds no face, and changes no boundary edge image. Canceling a paired internal edge only identifies the abstract parent disk; it does not delete or move its physical subdivision cells. Hence the visible local boundary embedding agrees with the source panel, and the local face-density bound is not worsened by this completion. Degenerate embedded polygons are allowed; the abstract disks remain nonsingular.

What remains to be checked globally is that each parent boundary port attaches to the intended neighboring gadget with consistent parent IDs and inherited sheaf restrictions. This is a port-identification check, not a reason to allow arbitrary third cofaces on the internal subdivision edges. In particular the completion must not silently override an actual external attachment specified elsewhere; if such an attachment exists, that port must be represented in the parent subdivision rather than ignored.

## Exact syndrome reduction

For each parent page, take the parity of its child face syndromes. Internal degree2 correction columns span exactly the even-parity subspace on that page, so a chosen anchor realizes the parity with minimum possible physical syndrome weight. After this compression the old seam acts by F on the three anchors. Thus the local coset minimum is exactly

    min_{f∈F} |(parity_U,parity_R,parity_L)+f|.

This proves no-loss final syndrome reduction and an explicit bounded-support correction for the specified parent realization. It handles arbitrary incoming syndrome on the local polygons; no clean-boundary assumption is used. It does not on its own eliminate boundary carry or establish a full coarse-chain identity.

## Model honesty

This is a fully specified, source-compatible local completion of the refinement sketch, not evidence that a conditional result about an invented unrelated toy has solved the original family. To promote it to a complete ell=8 family one must give the remaining parent-face/port atlas, check all gadgets use this subdivision consistently, retain the two shifted rib maps, and prove the global decoder/witness properties. Those are still open in this construction record.
