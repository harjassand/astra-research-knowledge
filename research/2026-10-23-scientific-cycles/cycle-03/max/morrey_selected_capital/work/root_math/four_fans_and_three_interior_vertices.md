# Four-face fans and arbitrary vector-valued triangular layer maps

22 October 2026. Root's independent analytic reconstruction and extension.
This is a finite binary laminate result for the precise mesh classes below,
not a resolution of Morrey. Historical priority is UNKNOWN. The generic
annular capacity argument was independently developed with WS10; its
coordinate verification and independent audits are separate evidence.

All triangulations below are genuine straight, nonoverlapping,
positive-area, conforming triangulations. Nodal maps are continuous and
affine on each face. Areas are physical areas, never freely chosen weights.
A finite binary laminate here permits repeated occurrences of the same
matrix, subsequently coalesced, and zero/coincident rank-one splits.

## 1. An arbitrary four-face fan is a binary laminate at its own mean

Let a simple quadrilateral with cyclic vertices P0,...,P3 be triangulated
by joining one interior vertex O to all four vertices. Let U be ANY
R^2-valued nodal map, with arbitrary values also on the boundary. Its four
face gradients are M0,...,M3 with positive areas t0,...,t3. Consecutive
gradients are rank-one connected by continuity across their shared edge.

There are three noncollinear boundary vertices. Fit an affine vector map
Lx+b to U at these vertices, and write the fourth boundary discrepancy
as v. Choose a scalar P1 function f equal to 1 at the fourth vertex and
0 at the other three boundary vertices, with any value at O. Then

    U = Lx+b+v f+R,       R|boundary=0.

The mean gradient of R is zero. The determinant null Lagrangian for
continuous P1 maps gives

    mean det DU = mean det(L+v tensor Df)
                = det(L+v tensor mean Df) = det(mean DU).       (1)

The middle equality uses the affine determinant formula for a rank-one
perturbation of the fixed L. It makes no convexity assumption on the
quadrilateral. All that is needed is the stated valid fan.

Group the two consecutive pairs (M0,M1) and (M2,M3), with their physical
weights, and call their means X,Y. Each pair is a rank-one binary split,
so determinant is affine on that split. Equation (1), applied to the two
group means, therefore says

    mass(X)*mass(Y)*det(X-Y)=0.

Both masses are positive; hence rank(X-Y)<=1. This supplies a complete
three-split binary tree at the actual mean of U.

Equivalently, the determinant variance identity and the four consecutive
rank-one connections give the useful exact identity

    t0*t2*det(M0-M2)+t1*t3*det(M1-M3)=0.                    (2)

This is a law-level statement. The mean affine map usually does NOT
have the original quadrilateral boundary values. It gives no permission
to replace the fan by that affine map inside a larger actual map.

## 2. Generic seven-face annulus: no restriction on the output values

Let W0,W1,W2 be a triangle strictly inside V0,V1,V2, indexed cyclically.
Require their matched connecting edges and the chosen annular diagonals
to yield an actual seven-face triangulation (six annular faces plus the
inner triangle). Prescribe U=0 at each outer vertex, arbitrary vector
values at the three inner vertices, and interpolate. The inner affine
map is U(x)=Cx+b, with C an ARBITRARY 2x2 matrix.

In a consistent cyclic diagonal pattern label the three outer-edge
faces Ai (areas ai), the three inner-edge faces Bi (areas bi), and the
inner face C (area c). Ai denotes a matrix here. It has determinant zero,
because its map vanishes on the whole corresponding outer edge. The
physical shared-edge connections are

    C--Bi,    Ai--Bi,    Ai--B(i-1).

For adjacent Bi,Bj and their shared exterior Ak, the four actual faces
C,Bi,Ak,Bj form a four-face fan. Thus (2) gives

    det(Bi-Bj) = -ak*c/(bi*bj)*det(C-Ak).                  (3)

This includes singular C and zero diagonal determinants. It follows
solely from geometry and continuity, with NO scalar roof assumption.

Write zi=bi det Bi, zC=c det C. The zero exterior boundary implies

    sum ai Ai+sum bi Bi+c C=0,     z0+z1+z2+zC=0.         (4)

If at least one zi is nonzero, select two zi of the same weak sign,
not both zero. Such a pair exists among three real numbers; relabel it
z0,z2, leaving z1. Put

    q0=z0/(z0+z2),    q2=z2/(z0+z2),    q0+q2=1.

Both q are nonnegative. If all three zi vanish, then zC=0 by (4),
and choose q0=q2=1/2 instead.

The first four-leaf module has terminal masses

    A1:a1,    B0:b0,    B1:q0*b1,    C:q0*c.

The second has

    A2:a2,    B2:b2,    B1:q2*b1,    C:q2*c.

For positive q, first merge C with B0 and A1 with B1 in module 0.
Both differences are rank one. Their two means X,Y satisfy

    (mC+m0)(mA+m1) det(X-Y)
      =mC*mA det(C-A1)+m0*m1 det(B0-B1)=0,

by (3) and the literal product equality

    (q0*c)*a1 = [a1*c/(b0*b1)]*b0*(q0*b1).

Thus the top split is rank one too. The same calculation applies to
module 2. Their determinant charges are

    z0+q0*(z1+zC)=0,       z2+q2*(z1+zC)=0,

by (4); both module roots have determinant zero. When a q is zero,
the module prunes to its physical pair Ak,Bi. Then zi=0, each leaf
has determinant zero, and their physical shared edge is rank one;
the same conclusion holds without a limiting argument.

The modules use exactly all B and C masses, A1,A2, and no A0.
The remaining A0 has determinant zero. These three roots have positive
weights and total mean zero by (4).

Any three determinant-zero matrices R0,R1,R2 with positive weights
alpha0+alpha1+alpha2=1 and mean zero form a binary laminate: since

    det(alpha0 R0+alpha1 R1)=alpha2^2 det R2=0,

the determinant variance identity implies det(R0-R1)=0. Their mean is
proportional to R2, so the last split is rank one as well. The two-root
and one-root cases are immediate. Thus the seven-face actual law is a
finite binary laminate at zero. Reflection handles the other consistent
cyclic pattern.

## 3. The six mixed diagonal patterns for generic C

On every outer-edge face Ai one has Ai=vi tensor pi, where vi is the
vector value at its inner apex, and the physical normal balance is
sum ai pi=0. A mixed pattern has two such faces with the same inner
apex, hence the same vi. Merge them. Their weighted normal is parallel
to the third normal, by the balance identity. Their mean is therefore
rank-one connected to the third Ai. The whole A group has a binary
collapse to a rank-one matrix MA.

On an inner-edge face Bi, subtract the inner affine map Cx+b:
Bi=C+wi tensor ri, where wi is the residual vector value at its exterior
apex, and sum bi ri=0. The other transition of a mixed pattern gives two
equal wi. The identical two-merge argument collapses the B group to
MB=C+rank-one matrix. Hence MB and C are rank-one connected.

Merge MB with the physical cap C. The resulting mean is proportional
to -MA because the full actual mean is zero. It is rank-one connected
to MA. This completes the binary tree, with no assumption on det C.

Every diagonal assertion is subject to actual nonoverlap and positive
areas. An algebraically named diagonal outside a concave quadrilateral
is not an admissible triangulation.

## 4. Arbitrary vector nodal data on nested triangular layers

For finitely many strictly nested triangles with admissible annular
triangulations as above, arbitrary vector values on every layer's three
vertices and at an optional final center, and affine data on the outer
boundary, the full gradient law is a finite binary laminate at the
outer affine gradient.

Induct from the center. A three-face fan in a triangle has affine
boundary values; after subtracting that affine map its nodal map is a
fixed output vector times a scalar hat, so all differences lie in one
rank-one linear plane. Collapse it by binary splits. At each outer
step, the collapsed inner map supplies its affine trace Cx+b. Subtract
the affine map matching the next three outer vertices, and apply the
generic annulus theorem. Replacing the cap leaf by its existing finite
tree gives the next finite tree. No inner boundary trace is discarded.

## 5. Every triangular mesh with at most three interior vertices

Take a nondegenerate conforming triangulation of a triangle whose ONLY
boundary vertices are its three corners, with at most three interior
vertices, and ANY vector P1 map with affine boundary trace. Its full
gradient law is a finite binary laminate at its affine boundary gradient.

An interior degree-three vertex has a triangular patch. Collapse its
three gradients to the affine map matching that patch's three boundary
vertices as in section 4. This is an actual boundary-preserving
coarsening, and its finite tree can later be substituted back.

If I interior vertices remain and j edges join two interior vertices,
Euler's formula gives 3I internal edges. Their total interior degree
is 3I+j, with j<=I*(I-1)/2. For I=1,2 this is less than 4I, hence some
interior vertex has degree three. For I=3, if none has degree three,
then j=3 and all interior degrees are four. The three interior vertices
form their central triangle; all six remaining faces form its annulus
with the outer triangle. To check the precise annular topology, every
inner vertex has two interior and two exterior neighbors. Each exterior
vertex has at least one inner neighbor. If it had exactly one, its two
boundary-edge faces would force that inner neighbor to connect to all
three exterior corners, a contradiction. Thus the exterior cross-degrees
are all two as well. The six cross-edges form a simple bipartite six-cycle.
Its alternating perfect matchings give the noncrossing connectors and
the cyclic strip diagonals. This is exactly the seven-face case above.
Undoing the coarsenings yields the asserted finite binary tree.

For every finite globally rank-one convex F and every affine background
B, each claimed law therefore satisfies its exact Jensen inequality
by repeated rank-one convexity. No differentiability, generic-position
of output values, or strict determinant sign is required.

These finite mesh classes do not supply a dense class of all gradient
tests. In particular, a four-face fan's mean collapse need not preserve
its quadrilateral trace. Degree-four interior vertex elimination is an
unresolved stronger operation; silently using it would invalidate a
purported proof of the full conjecture.
