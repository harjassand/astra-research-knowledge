# Narrow Fig.20 incidence-completeness audit

2026-11-02. Independently inspected `T_polygons.png` and primary source arXiv:2605.10943v1, Example6.8, Fig.20 caption, general figure conventions and refinement/doubling prose.

## Verdict

The six-/nine-face polygon-list computations are exact relative algebra for those lists. This pass does NOT independently certify that every apparently degree2 shared edge has physical face degree2 in the complete recursive patch. Keep this qualification until an explicit coface/subdivision receipt closes it.

The prose introduces the lists as faces in the displayed portion incident to path O–P–Q. It does not expressly give a closed star for each transverse shared edge. Fig.20 says that vertex positions are distorted to expose overlaps. General conventions also distinguish actual edges from mere thin visual guides. Thus neither coordinate coincidence nor apparent absence of a third rendered face is a completeness proof.

The left patch is strongly consistent with subdivisions of the three individual cylinder surfaces described exhaustively near O–P–Q in Fig.26. In particular RQ has the intended interpretation as an internal diagonal of the upper cylinder surface. To turn this into a certificate for all three edges RQ, PD0, PD1, explicitly map each listed polygon to that abstract cylinder surface and check that the shared edge lies in its relative interior, rather than an attaching boundary. Geometric degeneracy of PD0/PD1 makes coordinate-only checking inadequate.

For the right recursive box, the analogous needed checks concern PA1, PC0, QC1, PB1, QB2, QB4. Refinement preserves the underlying topology and inherits sheaf data, which can establish degree2 once an edge is identified as an internal subdivision edge of a single old face. The source excerpt does not provide that explicit subdivision map for these named edges. Some nearby original-sheet faces are visually present but omitted from the O–P–Q list; their abstract distinction must be preserved rather than guessed from coordinates.

## Exact missing representation

Supply either:

1. the full abstract coface list for each of the three/six tested shared edges, including any sheet/cylinder attaching faces; or
2. a source-faithful subdivision map assigning each listed polygon and shared edge to an old abstract face and proving that each tested edge is interior to that face, with no new doubling attachment on it at this stage.

This is a finite incidence audit, not a request for a global decoder theorem. No counterexample or actual extra third face was found; the conclusion is that the present evidence is insufficient to independently promote conditional algebra to a complete physical-incidence certificate.
