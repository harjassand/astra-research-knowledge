# Finite physical-star closure without a global coordinate generator

2026-11-02. Independent geometry derivation for the **declared intrinsic-page, skeleton-first completion** of the ell=8 family. This uses the source's admitted box/edge closure (Section 6.2, Lemma 6.9 / Claim 6.11) and the named-port convention in `ATLAS_NORMALIZATION.md`. It is not a claim about every unspecified alternative cellulation of the drawings. It does not assume that coordinate coincidence identifies vertices.

## Main result

Every actual physical vertex belongs to one of two closed classes:

1. **Outside every exceptional box:** the sum Q_v of dimensions of its incident physical edge stalks is at most 12.
2. **Inside an exceptional box:** the finite actual stars below have Q_v at most13, attained only at the raw doubled-T Q in the conservative all-parity dimension count. Their vertex-stalk dimensions are at most4 by the exact finite matrices.

Therefore **Q_v<=13 and w_X<=13 in EVERY edge basis and EVERY vertex-generator basis**. No Hamiltonian generator is multiplied or replaced to obtain this bound. Combined with a globally fixed path basis on each red edge stalk, the ordinary face bound gives w_Z<=10. The edge-basis change is a Clifford acting on at most three qubits in that one stalk and conjugates every original Hamiltonian term individually; it preserves the full spectrum and the entire Gibbs state under conjugation. No added physical qubit, changed cell image or thermal cold penalty is required at the stabilizer level. Native recompilation and physical noise admission still require their separately charged constants.

The optional optimized vertex bases in Part C strengthen w_X to12, but changing the vertex-generator basis changes the Hamiltonian and needs separate thermal accounting. The governing strongest baseline is now **K<=15 with no change whatsoever to the source Hamiltonian or physical data bases**, since the existing Z weight is at most15. K<=13 is an optional exact-Gibbs edge re-encoding; see ../UNTOUCHED_K15_AND_NATIVE_DICTIONARY.md.

The stronger proposed K10 exterior classification is NOT used: injectivity of spatial directions among abstract edge germs is unnecessary for the capacity bound and is not silently assumed.

## A. Exterior capacity lemma

For a lattice unit segment outside the exceptional boxes, the source's simple-structure invariant allows only:

- one abstract edge, incident to at most three faces; its stalk dimension is at most two;
- two abstract edges with the same segment image, each incident to at most two faces; their TOTAL stalk dimension is at most two.

The second case remains safe even if the two abstract germs share an endpoint. At a fixed lattice vertex there are six incident unit-segment directions. Therefore

 Q_v=sum_(e incident v) dim F_e <=6*2=12.

No zero-length edge lies outside the boxes: the exceptional T polygons and their residual recursive features are precisely the boxed degeneracies. The boxes have noninteger boundary coordinates, so a lattice vertex outside every box has a sufficiently small neighborhood disjoint from all boxes. The local classification applies to every incident punctured germ, even if its far endpoint lies in a box. Edge-face incidence is constant along an open abstract edge.

This also handles all ordinary boundaries: degree-one blue has dimension1, degree-one red dimension0. A missing page cannot increase the per-direction capacity.

A finite ordinary overclass is obtained by recording six direction bins, each containing one degree<=3 germ or two degree<=2 germs, the face incidence, and Rep/Par colors. Each direction bin has at most four total face-edge incidences (one degree≤3 germ or two degree≤2 germs). Six bins therefore have at most24 incidences; each regular abstract face corner uses two distinct edge germs, so there are at most12 incident face coordinates. No injectivity of face images is needed. Thus this is genuinely a finite local-state closure, not an unbounded family of unknown vertex matrices. Its analytic capacity bound makes exhaustive enumeration unnecessary.

## B. Exact exceptional-box inventory

All coordinates below are the local integer coordinates used in source Example6.8/Figure20; translations, coordinate permutations/reflections and inherited page labels do not change the star calculation. The declared atlas treats the other recursive T box as the prescribed rotated/reflected copy, retaining its complete exterior words.

### B1. Newly doubled T box

The box is

 (-2/7,9/7) x (-2/7,2/7) x (-2/7,9/7).

Its actual abstract vertices are exactly

 O=(0,0,0), P=(1,0,0), Q=(1,0,1), R=(0,0,1),
 D0=(1,0,0), D1=(1,0,0).

P,D0,D1 remain three DIFFERENT abstract vertices. All other named polygon vertices have x=2 or z=-1,2 and lie outside this box. The listed polygons have no hidden interior lattice subdivision vertices.

Complete the cylinder pages with their actual original and copied ordinary sheet books. The attachment paths are:

| page | original sheet | copied sheet |
|---|---|---|
| upper | O-R-A0 | Q-A1 |
| right | O-D0-C0 | Q-C1 |
| lower | O-B0 | Q-D1-B1 |

For each path segment there are exactly two incident sheet-side faces, one on each side of the attaching rib. At O or Q their transverse seam germs are shared across all retained pages. This is the ordinary edge-book collar at the interior of the scaled old edge, not an invented extra boundary closure. The cylinder seam O-P-Q retains the OLD edge code; attaching ribs carry the iteration's NEW code.

The resulting complete links are:

- O: K_(3,d), d in {1,2,3} retained pages;
- Q: K_(3,d), with the upper-cylinder incidence edge subdivided once when the upper page is retained (the extra node is germ QR);
- P: a theta/book link with page-path lengths (1,2,2), deleting absent pages;
- R,D0,D1 when present: K_(2,3), the two attaching-rib germs and three transverse germs.

The added subdivision at Q is essential; omitting it would undercount one physical edge qubit. The exact parent polygons, not their geometric overlap, determine these links.

### B2. Recursive T-derived residual box

The box is

 (-2/7,16/7) x (-2/7,2/7) x (-2/7,2/7),

in its own translated/rotated coordinates. Its abstract vertices are exactly

 O=(0,0,0), P=(1,0,0), Q=(2,0,0),
 C0=(1,0,0), C1=(2,0,0).

P and C0, and Q and C1, remain distinct. In particular R=(2,0,1) and B4=(2,1,0) are OUTSIDE the box. There is no need to guess a second sheet attachment or a global endpoint identification at R in order to certify the boxed vertices.

The ordinary sheet attachment paths meeting the box are

 upper: O-A0; right: O-C0-C1-C2; lower: O-B0.

These receive the same two sheet-side faces per segment as in B1. All other needed cofaces at the five listed vertices are already in the explicit right-hand Figure20 polygon list. Their complete links are:

- O: K_(3,d), with old-code seam germs and new-code attaching ribs;
- P: page-path lengths (2,2,2);
- Q: page-path lengths (1,2,3);
- C0,C1 when the right page is retained: K_(2,3).

Deleting pages gives all boundary subcharts, retaining degree-one blue/red distinctions. The right chart's exterior continuation is governed by the ordinary exterior capacity lemma; no unearned complete-star claim is made about a truncated port.

### B3. Newly doubled glued-cross box

Its transverse width is 4/7 and its longitudinal extent is (-2/7,9/7), so its only integer vertices are the endpoints O,P of the new degree-four cylinder edge. The underlying original/copied sheet is locally one ordinary face. Each endpoint link is the wheel graph consisting of a C4 sheet link plus the vertical edge-germ node joined to all four outer nodes. Every non-degree-two stalk has the new iteration color.

The following refinement resolves the degree-four edge and leaves **no residual box**. Its output vertices therefore fall under the source's exterior simple-structure invariant and Part A. A separate guessed partial-wheel classification of the split-cross endpoint is not required for this bound.

### B4. Newly doubled free-cross box

The source specifies two disjoint cylinder surfaces with chains A0-B0-B1-A1 and C0-D0-D1-C1. Their images overlap in one unit square, but the declared atlas keeps their abstract vertices, edges and faces separate. The four geometric corner positions of that square each contain independent ordinary single-rib attachment vertices. Each individual abstract star is K_(2,3), with the two attaching-rib germs colored by the new iteration and the other germs degree2.

The subsequent free-cross refinement leaves no residual box and again falls under Part A. Identifying the overlapping free-cross vertices would change this construction and is not covered.

## C. Executable certificate and basis robustness

`boxed_link_geometry_certificate.py` extracts partial links directly from the two literal polygon lists and adds only the sheet collars listed above. It checks all seven nonempty page subsets, both inherited seam colors and both iteration colors. It also includes the two glued-cross and two free-cross colors: **252 cases** total.

For each link it enumerates the exact vertex-stalk code F_v and chooses a minimum-bottleneck spanning basis using a robust local cost:

- nonzero repetition/degree2 restriction costs1;
- nonzero Par3 restriction costs at most2;
- nonzero Par4 restriction costs at most3.

These costs upper-bound restriction coordinates in EVERY choice of basis for that edge stalk. Thus the selected F_v basis is safe simultaneously for any globally fixed edge bases; independently choosing conflicting bases at opposite endpoints is not part of the proof.

Results:

| box class | cases | maximal robust X weight | maximal dim F_v | maximal Q_v |
|---|---:|---:|---:|---:|
| doubled T |132|9|4|13|
| recursive T residual |116|8|4|12|
| doubled glued cross |2|7|4|11|
| doubled free cross |2|6|2|7|

The starred Q_v=13 at the raw doubled-T Q explains why the exterior capacity lemma must not be naively applied inside every box. Its actual optimized generator bound9 is nevertheless below12.

## D. Closure argument across every level

The source invariant says boxes are disjoint; outside boxes all structures are simple. Refinement of types1/2 creates only type2 residual boxes. Refinement of types3/4 leaves no residual box. Doubling creates only the named T/glued/free boxes, while W0 has no ribs and preserves the inherited type2 boxes separately in the two copies.

The declared atlas fixes literal Figure20 page words inside the T boxes, their rotations/reflections and page-deletion subcharts, and fixes inherited external port identities. Therefore the finite boxed list B1-B4 repeats without any new abstract vertex identification. Everything not in the boxed list satisfies Part A. This closes the two-class induction from the single-square seed.

This is a **bounded local physical-star proof**, not a full global integer-coordinate renderer and not a replacement of the source geometric admission. Its only imported geometric facts are the already admitted box/edge closure and the actual named finite gadgets. Any custom optimization that adds faces, changes port gluing, introduces a zero-length exterior edge, or identifies free-cross IDs must repeat this check.


## E. Uniform vertex-stalk rank and qubit incidence

Let A be uniform on the binary vertex stalk F_v. For each incident abstract edge germ e, restrict A to the face coordinates incident on e. Every incident polygon face has exactly two distinct boundary edge germs at v (including the declared degenerate embedded triangles/pentagons). Shearer's entropy inequality therefore gives

 2 dim(F_v) = 2 H(A) <= sum_e H(A|_e) <= sum_e dim(F_e)=Q_v.

Consequently Q_v<=13 implies **dim F_v<=6** without requiring a simple link graph. In any actual basis of F_v, an edge qubit appears in at most dim F_v generators at either endpoint. Thus **q_X<=12**. Since any edge has at most four incident faces, **q_Z<=4**. With the path-basis w_Z<=10 and the basis-independent w_X<=13, total qubit incidence is at most16 and the check-overlap count including itself is at most

 D <= 1+13(16-1)=196.

These are conservative uniform certificates for the actual declared generator coordinates. They do not assume that a convenient sparse vertex basis was already the Hamiltonian's chosen basis.
