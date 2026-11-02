# Direct red projection and stratified H1 argument

2026-11-02. This note addresses red doubling itself, not the tree-resolution refinement. It specifies the exact incidence hypotheses that a source-compatible atlas must realize. It does not replace those incidence checks by coincident geometric coordinates.

## Direct projection in degrees 1 and 2
Give every fine sheet or cylinder face its old parent-face ID. A cylinder band follows a rib arc inside that parent face. For a fine face basis vector q define P2(q)=its parent face.

For a fine edge e and a local codeword u in F_e, aggregate its face coordinates by parent-face ID. For each parent face f, set a_f=sum_{q incident e,parent(q)=f}u_q.

* On an internal new red edge, every incident face has the same parent f and the local parity constraint gives a_f=0. Thus P1(e,u)=0.
* On an ordinary inherited edge descendant, the incident face IDs are exactly the old incident faces and the inherited local code identifies the aggregate a with an element of the old F_E. Set P1(e,u)=a at E.
* On a T-cylinder vertical seam, the inherited old code gives exactly the same identity map into F_E. Include this contribution; omitting vertical seams is incorrect.
* At a free cross, separate parent-ID surfaces and their edges; no aggregate may mix coincident pages.

Summing these maps over fine edges gives the EXACT column identity

    P2 d_new^1 = d_old^1 P1.                      (R1)

It is independent of choices of local bases, and holds for arbitrary inherited Rep/Par codes. In particular a new red attaching or glued-cross parity column disappears because its two (or even many) occupied face entries have the SAME parent ID. This is not the blue cone formula.

For refinement auxiliary faces, compose this map with the separately earned refinement projection. A Rep4 auxiliary then maps to an old pair, not to a singleton; R1 persists, but Hamming nonincrease does not. This is the packet-metric issue recorded by root.

## Degree-zero map
Along each old edge, the fine seam-type edges (both sheet descendants plus inherited vertical T seams) form an abstract graph with coefficients in F_E. At each internal graph vertex the strong sheaf equations and the new red parity restrictions make the sum of its incident seam labels vanish. Hence P1 d_new^0 receives contributions only at graph terminals over old vertices. Sum the restrictions of those terminal vertex labels to define P0. When the source W0 region has no cylinder, this is the sum of the two sheet old-vertex labels. Then

    P1 d_new^0 = d_old^0 P0.                      (R0)

This assertion requires the seam network to have the correct old endpoints and no unrecorded terminal. It is a concrete port condition, checkable from abstract incidence; it is not inferred from the drawing.

## Why the red map should preserve H1 (precise stratified argument)
Split the fine complex by the smallest old stratum supporting its parent-ID incidence; transfer each local relative fiber by Gaussian elimination. For an ordinary parent completion, the fibers are:

1. Old vertex: no bands in its neighborhood; two copies of F_v in degree 0.
2. Old edge: the two sheet intervals with two rib rungs. After factoring inherited F_E, this is the one-dimensional parity-sheaf graph relative its four external endpoints. Its H1 is F_E, represented by total edge-label sum; any extra cohomology is H0. For the two-rung ladder the dimensions per scalar coefficient are (H0,H1)=(1,1). The relative vertex spaces are even-parity spaces at internal trivalent vertices. The incidence image is the global-even subspace because the graph is connected: use paths to generate every pair of edges. This proves H1 directly; rank-nullity gives H0.
3. Old face: two disk pages joined along a connected hashtag graph. Its relative red fiber has H2=F2, represented by total face parity, H1=0, and H0=F2 for the single hashtag cycle. A direct finite certificate for the compacted two-rib fiber already exists at explicit_memory_witness_20261102/flat_red_face_fiber_results.json: (C0,C1,C2)=(32,60,30), ranks=(31,29), yielding (1,0,1). Ordinary parent-ID disk subdivisions add only elementary exact pairs and preserve this result. More general routed pages need an explicit subdivision/homeomorphism to this disk-band model, not merely bounded size.

The induced degree-one and degree-two maps between the surviving old edge and face coordinates are exactly the old restriction maps, by R1. The vertex-to-edge map is the sum of the two old vertex restrictions, by R0. Splitting (u,v) into u+v and v leaves one old vertex copy plus an extra degree-zero coordinate. All additional local residual coordinates lie in TOTAL degree zero; they cannot create a degree-one class through maps to face fibers because face H1=0. There can, however, be transferred maps from residual vertex-degree-zero coordinates to neighboring edge H1 unless the two sheet terminal maps are shown equal. The endpoint-sum construction and the same parent-ID port matching prove their equality for the ordinary model. With that condition, the transferred complex is the old complex plus a complex concentrated in degree zero. Thus P induces an H1 isomorphism and retains extra H0 rather than falsely claiming full cohomology equivalence.

## Exact remaining recursive obligation
A boxed W0 region containing several collapsed old cells need not be a SINGLE old-vertex fiber. Its two sheet copies must be reduced by the explicitly given parent-ID page subdivision/tree-resolution contraction BEFORE the above stratum transfer. If that reduction is relative to all its boundary ports, its two endpoint maps agree and the same proof goes through. Bounded density alone is insufficient: it bounds matrix sizes but does not prove their relative H1 vanishes. This note gives the direct red maps and the complete ordinary-fiber argument; it does not claim to have enumerated the collapsed recursive patch ports.

## Useful immediate certificate target
For every actual bounded boxed patch, assemble D0,D1 and the candidate P0,P1,P2 from parent IDs, then check R0,R1. Compute the mapping-cone homology in degree1, retaining degree0 residuals. This checks the proposed map itself, not just equality of encoded-qubit counts. The finite sheaf compiler already computes D0,D1 from complete polygon cofaces and colors.

## Executed direct-map seed certificate
`red_seed_projection_test.py` uses the complete abstract compacted first-step fixture with inherited opposite blue/red boundary sides and NEW RED attaching/cross junctions. It constructs the actual sheaf D0,D1 and the direct P1 above, checks both cochain identities, and checks that a fine cocycle maps to the nonzero old logical vector (11). Results: dimensions (48,76,30), ranks (45,30), H=(3,1,0), and P induces an H1 isomorphism. P2 is total parity of all thirty fine faces. This tests the map, not only the equality k=1. The three retained H0 classes match the ordinary-stratum prediction: one face residual plus one residual for each of the two blue old boundary-edge stalks; the seed's old vertex stalks vanish.

For an ordinary two-rib completion the residual-count prediction is dim extra H0 = sum_v dim F_v + sum_e dim F_e + number_of_old_faces, with the qualification that all endpoint/residual transfer maps have been checked as described above. This is also consistent with the local dual-costar Euler dimensions, but the direct seed certificate does not require importing blue decoder maps.

## Fixed-projection local homotopy (parent-agent completion)
The direct P above need NOT be replaced by an arbitrary homological-perturbation projection. It is degreewise surjective and respects the vertex→edge→face filtration. Take K=ker P with that filtration. On each ordinary stratum P removes exactly its old-degree residual: one vertex F_v in degree0, edge F_e in degree1, and face F2 in degree2. Consequently the local homology of K is concentrated in TOTAL degree0. The extra vertex summand has zero transferred map to edge H1 because the two actual terminal restrictions are identical by the ordered inherited port convention. Edge and face residual H0 summands have no possible total-degree1 target in K.

Choose a local coordinate splitting of the prescribed P, cancel the stratum-local exact pairs, and transfer connecting maps. The filtration has three levels, so the perturbation expansion has uniformly bounded length. Since the residual target is concentrated in degree0, its transferred differential is zero. Reinsert the uncanceled old summands to obtain a cochain section J with PJ=1 and a bounded-local h such that

    1-JP = d h+h d    in degrees 1 and 2.

A degree-zero residual projector remains and must not be omitted. This proves H1(P) is an isomorphism and supplies the correction identity while retaining the literal parent-parity P2 and inherited-seam-sum P1. It is not merely an equality of logical dimensions.

For the constructed intrinsic-page atlas in ATLAS_NORMALIZATION.md, boxed W0 charts first contract RELATIVE all named exterior ports, and these contractions do not touch ribs. The ordinary fiber argument therefore applies after normalization, and composing the relative chart maps supplies the claimed fixed-P homotopy on the constructed physical completion. Degree-four tree resolution is composed separately and preserves its explicitly specified P2 auxiliary column; it is handled by packet metric rather than falsely called face parity.
