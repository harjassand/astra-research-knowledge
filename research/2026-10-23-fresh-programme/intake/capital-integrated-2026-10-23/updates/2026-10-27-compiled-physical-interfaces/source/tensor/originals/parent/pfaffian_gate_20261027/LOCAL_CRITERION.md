# Candidate local determinant recognition reduction

Root independently attacks the outstanding compiler's global-field gate.
This is a proposed algebraic reduction, not an accepted compiler, historical
novelty or new counting complexity claim. The worker is separately checking it.

Suppose each rational trivalent binary tensor has a nondegenerate rank-two CP
decomposition T_v=sum_(s=0,1) tensor_(legs e) u_(v,e,s), with component weights
absorbed into the factors. For each neighboring leg define the RATIONAL
quadratic form

    q_(w,e)(x)=det(T_w contracted with x on leg e).

The other two factor matrices at w are invertible by nondegeneracy. Taking
the2x2 determinant shows q_(w,e)(x)=C_(w,e)
(x^T u_(w,e,0))(x^T u_(w,e,1)), with C nonzero. Therefore the squared local
field balance obtained from the binary edge matrices M_e[a,b]=u_(v,e,a)^T
u_(w,e,b) is precisely

    beta_v=product_(e=vw) q_(w,e)(u_(v,e,1))
                             /q_(w,e)(u_(v,e,0)).

Assume every edge entry is nonzero. This expression is in ONLY v's quadratic
CP field, because every neighboring q has rational coefficients. Neighboring
root embeddings are not needed. Component rescalings with product1 across
the three factors cancel because each q is homogeneous of degree2. Flipping
v's component labels inverts beta_v, so the test beta_v=1 is label-invariant.

Indeed choose edge row/column factors r_e,s_e with
r_e²=M10 M11/(M00 M01), s_e=M11/(M00 r_e). Dividing rows/columns by
diag(1,r_e),diag(1,s_e) makes the edge matrix [[a,b],[b,a]]. Vertex spin1
gets g_v=product incident r_e or s_e; g_v²=beta_v. When beta_v=1 each g_v
is±1, not an arbitrary algebraic field. Edge square-root sign flips toggle
the two incident g's. Their signs can all be made positive iff their product
on each connected component is positive.

The component product is R=product_e M11/M00, and R²=product_v beta_v=1.
Flipping a vertex's CP labels changes R by1/beta_v=1 (the analogous column
formula holds at the opposite edge orientation); factor normalizations cancel
globally. Consequently R is fixed by the actual Galois group and is rational,
so R=±1. If R=-1, after edge symmetrization an odd number of residual vertex
weights[1,-1] makes the component partition function change sign under global
spin flip; it is exactly ZERO. It need not be rejected as an unsolved sign case.
If R=+1, an incidence-system sign assignment removes all vertex fields.

For rational input the CP factors can be obtained in a local quadratic field
by a2x2 matrix-pencil decomposition, choosing a nonsingular rational slice.
Local determinant-quadratic tests therefore avoid even a multi-neighbor star
field. A finite-field implementation still needs prime/denominator controls,
branch consistency for all tensor identities, and a correct planar Ising or
Pfaffian evaluator. Those algorithmic/bit/completeness requirements are not
proved by this local note. Degenerate vertices, zero edge entries and general
algebraic inputs are not silently included.

Independent exact K4 diagnostics are in check_local.py/LOCAL_CHECK.json. A
dense rational hidden-gauge even-parity network has beta_v=1 at all four
vertices and original contraction2600; replacing one vertex by odd parity has
the same local beta tests, R=-1 numerically, and exact contraction0. Adding
one parity-breaking entry fails the local tests while still having contraction
2600, because its odd contribution is killed by the other even tensors. Thus
failure of this sufficient representation test is NOT a hardness claim or a
failure of every exact contraction method. Global R was only numerically
evaluated in this diagnostic; the zero contraction was checked exactly by64
edge assignments. No complete finite-field/Pfaffian compiler was executed.

Two useful consequences also avoid global fields. An edge has ALL four CP
entries nonzero iff q_(w,e)(u_(v,e,0)) and q_(w,e)(u_(v,e,1)) are both
nonzero. Thus even this hypothesis can be checked in v's quadratic field.
The local two-slice matrix pencil has distinct eigenlines; any other rank-two
decomposition must diagonalize that same pencil, proving the needed uniqueness
up to component permutation and leg scalings whose componentwise products are1.
This supplies the Galois-permutation premise rather than assuming unrelated
algebraic roots have one prescribed global embedding.

## Standard Fisher normalization as a separate diagnostic

For a closed trivalent graph, vertex count V is even. Once edge gauges give
M_e=[[a_e,b_e],[b_e,a_e]] and all vertex fields are neutralized, orthogonal
Hadamard on each leg gives vertex(1/sqrt2)*even-parity and edge weights
w0=a+b,w1=a-b. Its overall vertex factor is the RATIONAL2^(-V/2).
Every CP leg matrix is invertible, hence each M_e is invertible and w0,w1
are both nonzero under these assumptions.

Replace a vertex by a triangle with internal dimer weights1. An original
state0 edge is SELECTED as an external dimer edge; original state1 is not.
At a vertex, an even number of active/state1 edges leaves an even number of
triangle vertices for internal matching. There is exactly one such internal
matching (none or one edge), so this is a bijection. External weights are
w0/w1, giving

  Z=2^(-V/2) product_e(w1_e) Z_dimer(Fisher graph).

The known all-external perfect matching fixes the Pfaffian orientation sign
once a valid planar Pfaffian orientation is supplied. No additional sqrt2
field extension is needed. Fisher's mapping/Pfaffian evaluation is established
prior: https://doi.org/10.1063/1.1704825 . This note does not invent it.
check_fisher_normalization.py independently enumerates spin and triangle-dimer
partitions on two rational K4 cases, including signed weights; both exact
normalizations pass in FISHER_CHECK.json. It implements no general orientation
or Pfaffian solver and establishes no asymptotic or novelty claim by itself.
