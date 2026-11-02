# Frozen algebra, common-lift identities, and polynomial filling

2026-11-02. Scope: the DECLARED intrinsic-page, skeleton-first completion of the Section6 ell=8 geometric construction, not the unrelated random-family replacement maps. No thermal lifetime theorem is asserted here.

## 1. Exact geometric binding and scope
Use Section6 Lemma6.9/Corollary6.12 for the source's scale-eight geometric routing and bounded-density induction. Keep its physical cells and geometric maps. Resolve any unstated abstract incidence by the intrinsic-page/ordered-port convention of ATLAS_NORMALIZATION.md: inherited skeleton edge words are shared literally by incident pages; internal cells identify only within the declared page; free-cross images remain abstractly separate; the source T-book seams and glued-cross bands are identified as specified. The parent-face disk completions and tree resolutions in that note fix the relative abstract topology. All common subdivisions used for comparisons/prisms are VIRTUAL, and maps are composed back to the unchanged physical cells.

The source geometric lemma supplies routing, not algebraic exactness. The latter is proved by relative page/edge contractions, finite book templates, and the costar argument below. The missing executable integer-coordinate table is not used as an algebraic axiom: the mathematical completion uses the source routed skeleton and explicitly named intrinsic ports. A different completion with an additional internal coface or seam cycle is not covered by this theorem.

The finite chart inventory is ordinary disks/books/vertex stars, the two Figure20 book patterns and their rotated/reflected recursive versions, degree-four tree resolutions, disjoint free-cross pages, and T page deletions. The 28 relative Figure20/deletion complexes were directly compiled and have H0=H1=0. More generally their relative-boundary contractions follow from page disk subdivision and seam interval contraction. Since all such contractions fix ALL exterior ports, they glue across chart boundaries and preserve the rib graph, which avoids W0. This is why a geometrically collapsed triangle need not carry an independent hashtag.

## 2. Algebraic theorem
There are uniform finite-support cochain maps for one step, with constants independent of recursion depth:

* Blue/X: two old-level sheet projections PA,PB, each inducing an H1 isomorphism; a cochain section J of PA; a degree-minus-one h with

  1+J PA=d h+h d in degree1,
  1+J PA=d h+Q in degree2.

  Q is a bounded-local degree-two residual projector and Q d=0. Extra H2 is retained.

* Red/Z: the direct projection P2 is total parent-face parity over both sheets and bands, composed with the explicit refinement projection. P1 sums inherited seam-code labels, including the vertical inherited T seams. It has a local cochain section J and h satisfying

  1+JP=d h+h d in degrees1,2.

  Extra H0 is retained, not converted into new checks. P induces an H1 isomorphism.

Each map/homotopy is computed by fixed finite-field elimination in bounded chart/stratum blocks, followed by at most the number of cell-filtration levels (three) of homological perturbation. No global inverse or growing elimination block is used.

Proof ingredients: vertex costars L_v→⊕L_e→⊕F2 are exact below degree2 because each incident polygon has exactly two boundary edges at that vertex; edge costars are the defining inclusions L_e→F2^{faces(e)}. W0 relative normalization reduces the rib complement to these costars. Blue doubling is the unequal-endpoint mapping cylinder with actual restrictions r_a,r_b. The periodic product warp, lifted to intrinsic pages, and its cellular prism give r_b q+r_a=d t+t d and hence J_sheet(x)=(x,qx,tx). Red fixed-projection kernel has local residual homology only in TOTAL degree0: face fiber H=(1,0,1), edge fiber H=(1,1)⊗L_e, and duplicate vertex copies. The specified P removes the old-degree residual in each stratum. Equal inherited terminal ports cancel the remaining vertex-to-edge map, so finite filtered elimination contracts ker P onto degree0. The detailed proofs and matrix certificates are in RESULT.md, ATLAS_NORMALIZATION.md, RED_DIRECT.md, and boxed_relative_certificate.py/json.

A Rep4 refinement auxiliary face projects to an old pair, not a singleton. None of this theorem falsely asserts Hamming nonincrease in degree2; syndrome metrics are a separate packet-accounting ingredient.

## 3. Common blue lift WITHOUT assuming PB J=1 strictly
Keep PA J=1, as a chosen section. The source-compatible parent prism/refinement comparison gives a bounded-local L with

  1+PB J=d L+L d.

It is enough that this is a LOCAL cochain homotopy; an abstract induced H1 identity would not suffice. For a valid syndrome sigma, Q sigma=0. Define

  fA(sigma)=h2 sigma,
  K(sigma)=PB1 h2 sigma + L2 PA2 sigma,
  fB(sigma)=fA(sigma)+J1 K(sigma).

Then

  sigma+d fA(sigma)=J2 PA2 sigma,
  PA2 sigma+PB2 sigma=d K(sigma),
  sigma+d fB(sigma)=J2 PB2 sigma.

Thus both branches use the SAME lift J. The L term must be retained unless strict PBJ=1 has actually been chosen. These equations follow by applying PB to the first identity and substituting the displayed homotopy in degree2.

For closed-error filling one also needs the degree-one B homotopy, not merely the syndrome formula. Set T=PB h+L PA as a degree-minus-one map. Applying PB to the degree-one homotopy and using 1+PBJ=dL+Ld gives PA+PB=dT+Td in degree1. Therefore h_B=h+J T satisfies 1+J PB=d h_B+h_B d in degree1. All maps remain bounded-local. This supplies the B-branch filling identity explicitly without assuming a separately constructed strict PB section.

## 4. Frozen component join
Partition a valid syndrome sigma into components sigma_C only using an active dependency gate that guarantees Q sigma_C=0 and all local comparison residual equations for each restriction. Global validity does not by itself guarantee this for an arbitrary partition.

Choose branch A or B on each component, and put

  f=sum_C f_branch(C)(sigma_C),
  e_coarse=PA1 e + sum_{B-chosen C} K(sigma_C).

Then d e_coarse is exactly the mixed selected coarse syndrome, and

  e+f+J1 e_coarse = d h1 e.

Proof: the J K terms introduced by every B correction cancel the same terms in J e_coarse; linearity gives sum_C h2 sigma_C=h2 sigma. The remaining expression is the degree-one homotopy identity for e. This proves actual logical/correction consistency, including the projected correction term, for the metric branch algorithm. It does NOT establish the active gate's bounded-degree/charge estimates; those belong to the component/witness proof.

## 5. Norm-controlled physical degree-one readouts
Fix physical bases as in EDGE_BASIS_DISTANCE.md. For a Par4 split (f1,f2|f3,f4), choose old star basis anchored at f2, fine left basis {f1+f2,f2+a}, and fine right basis {f3+a,f4+a}. With P2(a)=f2, P1 sends these columns respectively to old basis vectors {b1,0,b2,b3}. For Rep4 one resolved scalar maps to the old scalar and the other to zero. Ordinary edge subdivisions and inherited T seams preserve the inherited basis. Newly born degree-four edge anchors are chosen according to their next deterministic split; no conflict with present readouts or growing cross-edge basis changes occurs.

Therefore, for blue steps,

  |PA1 e|+|PB1 e|<=|e|,

because their sheet domains are disjoint. For red steps the direct P1 has |P1 e|<=|e|. Both blue projections detect every nontrivial H1 class. Consequently d_X doubles at every blue step and does not decrease at a red step. The same argument applies independently to the orthogonal-edge-code family, where the step colors swap.

## 6. Polynomial stabilizer filling: explicit proof
Let e be an X-type stabilizer word, i.e. e in im d0, with physical weight m>=1, at any recursion level k. The desired filling is a vector a in the ACTUAL C0 basis with d0 a=e, whose generators lie within a polynomial physical distance of supp(e). Set e_k=e.

At a blue step choose whichever of PA1 e_i and PB1 e_i has smaller weight; at a red step use P1 e_i. This is an EXISTENTIAL choice on the closed error, not a purported local syndrome decoder. Denote the chosen projection by p_i and its local cochain lift/homotopy by j_i,h_i. For the blue B branch the explicit h_B below suffices; a strict section of PB is not required. Every e_i remains a coboundary because p_i is a cochain map. Thus

  e_i=j_i1 e_(i-1)+d0 h_i1 e_i,
  e_(i-1)=p_i1 e_i.

Each blue step halves weight and each red step does not increase it. Within at most r0=2(ceil(log2 m)+1) descending levels the weight is <1 and hence zero, unless the seed level is reached first. Set r=min(k,r0). If the coarse word has become zero, no terminal filling is needed. If the seed is reached, the remaining word is a seed coboundary and has a filling in the finite seed C0 space, chosen once by a lookup table.

Iterating the displayed identity expresses e as d0 of the sum of all h_i1 e_i, lifted through the corresponding products of j^0, plus the lifted terminal seed filling. This is an explicit filling algorithm. It uses only actual C0 coordinates: a j^0 image is a linear combination of the code's original X-check generators. Extra H0 residuals are kernel directions/redundant products, not additional Hamiltonian generators. No extra term is added to the physical Hamiltonian.

Uniform support bound: each p,j,h acts in a bounded number of parent charts. One coarse-to-fine step maps anchors into distance at most a fixed constant times8 at the finer scale, by the source's scale-eight routing and bounded box perturbations. Composing r steps therefore moves support by at most C sum_{j=0}^r 8^j<=C'8^r. Every h_i e_i is near an ancestor of some original occupied coordinate; its lifted checks remain in the corresponding forward-anchor neighborhood. Thus all filling generators lie in the C'8^r-neighborhood of supp(e). Since r<=2 ceil(log2 m)+2,

  radius <= C'' m^6.

The exponent6 is a convenient crude bound (8^(2 log2 m)=m^6), not claimed optimal. Map column bounds also give a polynomial bound on the number of generators if needed. When k<r0, even the finite seed filling lifts into radius O(8^k)<=poly(m). No inverse-Lipschitz embedding assumption is used. Distinct components of e may be arbitrarily far apart: before termination the support statement is a UNION of forward-anchor neighborhoods, and any seed-level connection occurs only when 8^k<=poly(m). Thus disconnected stabilizer words are included.

The empty word has empty filling. The same proof applies to the orthogonal-sheaf family's X-stabilizer words.

## 7. Physical Z distance and filling: one final-level local duality
Use the bounded-local double-complex maps F,G,H in producer-workspace/RESULT.md between A^i=C_(2-i)(X,F) and B^i=C^i(X,Fperp):

  Fd_A=d_BF, Gd_B=d_AG, 1+GF=d_AH+Hd_A.

Their hypotheses hold for this completion: closed abstract cells are connected disks/intervals/points; the strong-sheaf restriction rules commute; vertex/edge costars are exact below top degree as proved above; and the top transposed kernel is EXACTLY Fperp_sigma because each incident edge-coordinate restriction must be orthogonal to L_e, which is Eq43 for the dual sheaf. Bounded source cell stars, polygon size, and stalk bases give uniform finite double-complex blocks. Dense elimination inside each such block remains bounded-local, and the two-dimensional perturbation series has fixed length. This is an algebraic construction, not an assumption of thermal duality.

For Z distance, if e is a nontrivial A1 cycle then Fe is a nontrivial B1 cycle and |Fe|<=C|e|. Apply the independent dual-family X-distance recurrence, then divide by C ONCE at the final level. No C^k loss occurs.

For Z filling, let e be an A1 coboundary of weight m. Then Fe is a B1 coboundary of weight<=Cm. Fill it by b in B0 using §6. Since d_Ae=0,

  e=d_A( H1 e+G0 b ).

F,G,H have uniform finite range and column bounds. Hence the support of the original Z-check filling H1e+G0b lies within a polynomial neighborhood of supp(e), with constants independent of k. Again G0b and H1e are coordinates in the ACTUAL original Z-check basis C2(X,F), not new check generators. This invokes local duality once globally, not an iteration-by-iteration lifetime transfer.

## 8. Scientific boundary and resource accounting
Earned here: one-step cochain maps, H1 preservation, common-lift component identities subject to the stated component gate, physical degree-one distance growth, and polynomial X/Z stabilizer filling for the declared source-compatible completion.

Not earned by these facts alone: the metric active-component gate and its charge bound, the ANY-local-stochastic witness theorem, or any exponential memory lifetime. Those require their separate complete join.

The physical check-weight bound is a fixed constant from the actual bounded cell/stalk bases. Nothing here proves it is7. A conservative bound such as60 may be used if verified by the independent star inventory; the red flat-seed maximum6 is not an all-level proof. Extra H0/H2 residual coordinates do not justify adding a generator of smaller weight or changing the Hamiltonian.

A genuine obstruction would be an actual required external attachment contradicting the declared intrinsic port words, a closed-cell non-disk, a seam cycle not eliminated relative ports, or a failure of uniform finite chart size. None was found in the independent finite inventory audit. Merely lacking a machine-readable coordinate-route list does not negate the mathematical source-compatible completion, but should not be misrepresented as an independently compiled all-template certificate.

The filling radius can be stated for full physical CHECK SUPPORT, not just its anchor: every actual check has uniformly bounded support diameter, so enlarge C'' by the fixed check range. Likewise the duality maps' finite incidence range implies bounded geometric range because every incidence stays within a bounded-diameter physical cell star. These are forward locality statements only.
