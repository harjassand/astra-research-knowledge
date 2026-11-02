# Explicit-family cochain fibers: a constructed parent-ID completion

Date: 2026-11-02. Independent derivation from arXiv:2605.10943v1 §§2.3, 2.4, 6.2, not from the random replacement complex. Primary source: https://arxiv.org/html/2605.10943v1#S6.SS2 . This is a proved algebraic construction for the parent-ID completion specified below, NOT a claim that every incidence hidden in source figures has been independently reconstructed.

## Result and exact scope
For a bounded-size, regular-polygon parent-ID refinement whose rib complement has the chamber structure below, blue/X doubling admits bounded-local cochain maps J,P with PJ=1 and an H^1 isomorphism. There is a bounded-local h giving

    e + JP e = d h e + h d e                         (1)

for every degree-one e. Consequently f(sigma)=h sigma gives

    e + f(de) + J P e in im d^0.                    (2)

The same identity descends through a bounded-local subdivision contraction to the OLD complex. This proves an actual logical/correction identity, not merely a metric cleaning inequality. It does NOT prove the weight inequality |P sigma| <= |sigma|/2; a different nonlinear cleaning rule may be needed for that. There are extra degree-two cohomology classes, so demanding a cochain equivalence in every degree is the wrong target.

The red/Z operation is blue/X for the orthogonal edge-code sheaf followed by cellular sheaf duality; a bounded-local construction of that duality is described below, but a source-gadget incidence implementation has not been produced here. No lifetime theorem is asserted.

## 1. Local exactness requiring no random-family input
Write V_f=F2 and L_e subset F2^{faces(e)} for the prescribed repetition/parity edge code. At a vertex v define L_v by the strong sheaf axiom. Assume every polygonal face incident to v has exactly two DISTINCT incident boundary edges, with incidences retained abstractly even if their geometric images coincide.

The local costar complex is

    L_v -> direct_sum_{e containing v} L_e -> direct_sum_{f containing v} F2.

The first arrow consists of restrictions. It is injective. A vector in the kernel of the second arrow has equal values on the two boundary edges of each face. Those common face values satisfy every incident edge constraint, hence define a unique element of L_v. Thus local H^0 and H^1 vanish. At an edge the local complex L_e -> F2^{faces(e)} is its defining inclusion, so H^1 vanishes. The face costar is F2 in degree 2.

This verifies the actual local acyclicity condition of §2.4 for a regular polygonal completion, including mixed red/blue vertices. Geometric collapsed triangles are harmless if their three abstract vertices/edges remain distinct. If the intended figure instead identifies two abstract boundary vertices, its incidence must be supplied and this proof must be replaced by a direct rank check.

## 2. Explicit subdivision completion
Keep separate parent IDs for all old faces, edges, vertices: never identify cells solely because their embedded coordinates coincide. Give each face a disk parameterization and each edge an interval parameterization, compatible on boundaries. Subdivide by the source's lattice routes, retaining an abstract disk tiling even for collapsed images. Interior new edges carry repetition-2; old edge descendants carry L_e. Vertex stalks are computed, not guessed, from the strong axiom.

A standard cellular subdivision contraction can be computed independently inside old face disks relative their boundaries, then inside old edge intervals relative endpoints. For a disk relative boundary its residual is F2 in degree 2; for an interval relative endpoints its residual is L_e in degree 1; for a vertex its residual is L_v in degree 0. Gaussian elimination in each constant-sized block gives i,p,h. The transferred differential is exactly the old restriction differential: boundary incidences count once modulo two; restrictions to a face are the same coordinate maps. Finite two-dimensional filtration means at most boundedly many parent stars are used. The embedding can be the source's perturbed piecewise-cellular map; the algebra never depends on injectivity of that map.

If a degree-four junction is resolved into two degree-three junctions separated by a new strip, use this explicit tree resolution (a constructed completion of the incidence):
* Rep4: two Rep3 spaces with coordinates (a,a,t=a) and (b,b,s=b), and differential to the new strip coordinate t+s. Kernel is Rep4 and cokernel is zero.
* Par4: two Par3 spaces (a,b,t=a+b), (c,d,s=c+d), differential t+s. Kernel projects bijectively to Par4 on (a,b,c,d), and cokernel is zero.
Tensor this transverse elementary cancellation with the edge subdivision. This supplies the missing algebraic guarantee for a split junction without falsely treating a degree-four to two degree-three split as a literal homeomorphism. It remains necessary to verify the source Figure 24 uses this incidence and no additional identifications.

## 3. Rib graph A and relative fibers
In each old face use two parallel ribs in each direction, forming a hashtag. Each rib runs to the boundary; old edge parameterizations identify the two intersection markers on all incident faces. At free crosses retain separate graph points; at glued crosses identify them. At a junction of d old sheets, the rib graph has a vertex stalk L_e and each incident rib arc has stalk F2. At an ordinary glued cross its vertex stalk is F2. This graph sheaf is the restriction of the refined sheet sheaf.

Two shifted sheets use different parameter positions for their rib markers. Match ordered marker 1 to marker 1 and marker 2 to marker 2; piecewise interval homeomorphisms, extended over parent disks, identify the abstract rib graphs. If the two actual cellulations differ, pass through their common bounded subdivision. This is essential: geometric equality of coordinates is NOT the sheet-copy map.

The components of the complement of A are:
* a corner neighborhood for each old vertex, collecting the face corners glued across old edges;
* a middle strip neighborhood for each old edge, between its two rib markers;
* a central face chamber for each old face.
The closure of each chamber is taken relative to its boundary in A. Each relative complex is a subdivision of the corresponding costar complex in §1. Therefore

    H^0(X',A;F)=H^1(X',A;F)=0.                     (3)

All chambers have bounded combinatorial size per iteration (ell=8 and bounded parent star size), so these vanishings come with bounded-local linear contractions, not merely an abstract existence argument. Gaussian elimination is performed separately on chamber matrices. H^2 is retained as a residual vector space, not discarded.

This is the exact geometric obligation needed from the perturbation gadgets: the cut chamber incidence must be parent-vertex/edge/face costars, or have a demonstrated elementary contraction to them. The source's interior hashtag, T-junction bands, inherited O-P-Q code and distinct free-cross surfaces agree with this completion. The unlisted boundary incidences of all refinement gadgets are not checked here. A claim for the literal entire source family remains conditional on that finite check.

## 4. Actual blue doubling complex
Let C=C(X',F), B=C(A,F|A), and R:C->B be the restriction cochain map. In compatible cellular coordinates R is a degreewise coordinate projection. The product bands give the mapping-cylinder double

    D^k = C^k + C^k + B^{k-1},
    d_D(x,y,b) = (dx,dy, db + R(x+y)).            (4)

Here B^{-1}=B^2=0. New repetition junctions identify sheet and band values. At a T-junction, the inherited old edge code on the vertical O-P-Q line gives precisely the B-vertex stalk L_e. At a glued cross it is Rep4=F2; at a free cross the two bands remain independent. Thus the strong-sheaf stalk equations yield (4), after bounded subdivisions of the routed bands. This is a source-specific use of its code assignments, not an imported replacement map.

Define J(x)=(x,x,0), P(x,y,b)=x. These are explicit cochain maps, PJ=1. Under (x,y,b)->(x,z=x+y,b), D splits as C plus

    K^k=C^k + B^{k-1}, d_K(z,b)=(dz, db+Rz).

Since R is surjective, K is the relative complex E=ker R plus elementary contractible pairs. One can see this without invoking a theorem: choose the coordinate inclusion s:B->C, write z=u+s a with u in E, and cancel the a↔b unit pivots. The remaining differential is d on E. These cancellations only touch a rib's adjacent cells. By (3), K has no H^0,H^1 and only degree-two residuals. Hence H^1(D)=H^1(C), and a contraction of K onto its H^2 residual gives (1). The maps J,P,h are bounded-local because all cancellation blocks are bounded rib/chamber stars.

Compose with refinement i:C_old->C and p:C->C_old, with 1+ip=dh_ref+h_ref d. Then J_old=Ji, P_old=pP, and

    H = h_D + J h_ref P

satisfies 1+J_old P_old=dH+Hd in degree 1. For syndrome sigma, f(sigma)=H sigma gives the old-level version of (2). In particular a fine cycle has the same logical class as its old-level projection, and a cycle with zero old logical class is a fine coboundary.

## 5. Why full cohomology preservation is false
Even two ordinary disks doubled along one connected hashtag have an extra H^2: the hashtag has one cycle and the union is homotopy equivalent to its suspension. H^1 remains zero. More generally H^2(K)=H^2(X',A;F) consists of bounded local residuals. No globally valid identity 1-JP=dh+hd on degree 2 exists unless these residuals are included in the target. A valid all-degree target is C_old direct_sum V[2], with V the local residual spaces.

## 6. Red/Z and duality: what is and is not supplied
Orthogonalizing every edge code exchanges Rep and Par (Rep2=Par2). Thus the red operation for F is the blue operation for F-perp. To turn its maps into maps on the original code, form a common barycentric subdivision and use the costar resolutions of §1 to identify the cellular dual complex with C(X,F-perp). Each local resolution is exact below degree 2. Eliminating the local exact pairs and transferring the incidence maps over the dimension-2 cell filtration is a finite Gaussian-elimination algorithm for the duality maps; its support stays within a bounded parent star. Transpose the blue maps and homotopy and conjugate by these local duality maps. The degree-one homotopy identity and logical-class identity then transfer. Extra degree-two residuals become degree-zero residuals.

This is a constructive algorithm under the regular-cell/chamber hypotheses, not an explicit list of matrices for every source gadget. Merely citing the H^1 isomorphism of Theorem 2.2 would NOT establish locality of the decoder; the local resolutions and finite transfer are necessary. I have not supplied a full machine-checked implementation of these duality matrices, so the blue result is substantially more explicit than the red result.

## 7. Remaining finite obligations and nonclaims
1. Enumerate parent-ID face boundaries of all source refinement gadgets, including recursive T boxes and degenerate triangles/pentagons; verify regular polygon incidence or directly rank-test exceptions.
2. Verify every rib-complement chamber contracts to the asserted old costar, and verify the two sheet rib graphs are matched without permutation/monodromy of parent face coordinates.
3. Verify the Figure-24 split equals the transverse tree resolution above.
4. Implement/check local duality matrices for red if explicit matrix output is required.
5. Separately establish the nonlinear syndrome weight reduction and thermal witness argument. Equations (1)-(2) alone do not establish exponential lifetime.

These are precise local algebraic obligations, not a claim that source geometry or a theorem for a different random family supplies the missing maps.

## 8. Amendment after independent comparison: unequal endpoint restrictions
The shorthand r_a=r_b in §4 is justified only after constructing the parent-preserving identification, not by setting physical coordinates equal. Here is a version that keeps the actual restrictions throughout.

Let C_a,C_b be the two actual sheet complexes and r_a:C_a->B, r_b:C_b->B their different restrictions. Construct bounded-local q:C_a->C_b and a degree-minus-one t:C_a->B satisfying

    r_b q + r_a = d_B t + t d_a.                 (5)

Then the actual formula is

    Jx=(x,qx,tx),    P(x,y,b)=x.

It is a cochain section because (5) is exactly its third-component cochain equation. In coordinates (x, y+qx, b+tx), D splits as C_a plus Cone(r_b). Thus the local relative-costar contraction of the SECOND sheet alone proves the same H^1 preservation and correction identity, without equating endpoint restriction matrices. The first sheet need not be identified cell-for-cell with the second.

Constructing (5): use ordered rib markers on each inherited parent edge. A piecewise-linear interval isotopy carries the two markers of side a to the two markers of side b while fixing old vertices. Extend it on each abstract parent disk, carrying its two-by-two grid of proper arcs to the other grid; since both arc systems have the same nine chambers and boundary order, the extension exists by mapping the nine disk closures compatibly. Glue extensions only along inherited parent-ID seams. Distinct free-cross pages remain separate. Give the sweep prism the inherited edge codes; integrating cochains across its interval factor is the cellular prism homotopy t. The identity boundary(prism)=endpoint_a+endpoint_b+prism(boundary) proves (5). Common-subdivide each bounded parent disk to make both maps cellular; ordinary subdivision contractions return to the original two cellulations. This q,t has bounded support in one parent star.

This argument proves (5) for the constructed parent-ID completion precisely when the actual two cut systems have the stated chamber combinatorics. It does not settle the finite verification that a folded recursive source page has that cut system. In particular, an extra rib loop, a reversed pairing on one seam, or a rib ending inside a page would break the premise and must not be silently ignored. This is the concrete topological test for the source gadgets.

The parent's flat relative fiber H^2 dimension 10 is consistent with the absolute H^2=1 disk example in §5: the former retains external relative boundaries, adding boundary-carry classes. No dimension-2 residual is removed by the argument here.

## 9. Explicit finite elimination recipe (no unspecified global inverse)
For each chamber E^0 --a--> E^1 --b--> E^2, compute bases over F2 by fixed lexicographic Gaussian elimination. Exactness proved above says a is injective and ker b=im a. Extend the columns of a to a basis [a,L] of E^1. Then b restricted to L is injective; extend its image to a basis [bL,Z] of E^2. Define h^1(a u+L v)=u and h^2(bL v+Z w)=L v. The residual projection sends bL v+Z w to w. These matrices satisfy

    h^1 a=1,    a h^1+h^2 b=1,    b h^2+Z pi^2=1.

Thus the degree-one identity is computed within each chamber, and the only uncanceled coordinates are its explicitly retained Z basis. Apply the same unit-pivot elimination to the rib coordinate-inclusion pairs of Cone(R). No global linear solve is used, and the maximal matrix size is bounded by one ell=8 parent star. This establishes bounded input/output influence, not a numerical Hamming contraction constant.

## 10. Connecting any weight-controlled cleaning to the logical identity
Choose the split contraction with hJ=0 and Ph=0 (the direct-sum construction above has these properties). Suppose a separate metric cleaning algorithm, possibly nonlinear, supplies c(sigma) with

    sigma+d c(sigma)=J^2 tau.

For an error e of syndrome sigma put e'=e+c(sigma). Then Pe' has syndrome tau and

    e'+J Pe'=d h e',

because h d e'=h J tau=0. Therefore the cleaned error has exactly the logical class of the lifted coarse error Pe'. This is the correct bridge from syndrome cleaning to logical preservation. The coarse error is P(e+c), not automatically Pe: the correction may change its coarse component. Either impose Pc=0 or explicitly include Pc in the recorded coarse correction. A claim that syndrome cleaning alone proves logical equivalence omitting this term is incomplete.
