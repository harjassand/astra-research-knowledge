# Original-face-once rank-one gradient compiler: root reconstruction

2026-10-23. Candidate reconstruction, not a priority claim. Root derived the
output-line grouping before the latest compaction, without writing or sharing
it; W43 subsequently reported the same mechanism independently and is writing
the principal frozen proof and compiler. W26 has also reconstructed the local
closedness argument. These are correlated internal reviews. The theorem below
concerns exact finite continuous piecewise-affine fields, not general Morrey.

## Statement on a flat torus, allowing affine periods

Let u:R^n -> R^m be continuous and affine on a finite periodic polyhedral
partition, with u(x+gamma)=u(x)+B gamma for gamma in a full-rank lattice.
Assume every full-dimensional cell gradient A_i has rank at most one. Let
lambda_i>0 be its normalized volume in a fundamental cell. Then

    sum_i lambda_i delta_(A_i)

is an exact finite-order laminate with barycenter B, using each original
cell once. A binary construction has at most F leaves and F-1 nontrivial
merges, where F is the number of positive-volume cells. Equal gradients may
be combined, so a smaller distinct-atom count is possible. Rank-zero merges
are allowed or redundant identical nodes can be suppressed. In particular,
rank(B)<=1. No rationality of the lattice, gradients or weights is required
for existence; an exact rational finite input gives rational arithmetic.

## 1. Closed scalar fields without target graph cuts

Group all nonzero A_i by the unoriented output line L=range(A_i). Choose a
nonzero vector v_L on each of the finitely many lines. On a cell in that
group write A_i=v_L tensor rho_i, and define the input covector field
rho_L=rho_i there and zero on every other cell. Assign zero-gradient cells
arbitrarily to one group, or keep a separate zero packet.

Across an interior codimension-one face with tangent t, continuity gives
A_i t=A_j t. If both output lines equal L, this implies
(rho_i-rho_j)t=0. If they are distinct, their intersection is {0}, so both
A_i t and A_j t vanish. Consequently the tangential jump of each extended
rho_L is zero, also when one adjacent gradient is zero. A piecewise constant
field has distributional first derivative given by these face jumps;
codimension-two intersections do not create extra terms. Hence d rho_L=0.
This holds across the periodic cell boundary because the affine period has
the same constant derivative on both sides.

## 2. Averaged wedge identity

Every periodic closed L-infinity one-form has the form
rho_L=J_L+d phi_L, where J_L is its mean and phi_L is periodic Lipschitz.
One direct proof expands in lattice Fourier modes: closedness makes each
nonzero coefficient parallel to its frequency; the zero mode is J_L.
Alternatively integrate the lift on R^n and subtract its linear periods.

For L != M the fields have disjoint supports, so rho_L wedge rho_M=0
almost everywhere. Integration by parts for the periodic potentials gives

    average(rho_L wedge rho_M)=J_L wedge J_M.

Indeed the two linear-exact cross terms have zero mean, and
d phi_L wedge d phi_M=d(phi_L d phi_M) has zero integral, componentwise.
Lipschitz potentials justify this through periodic smooth approximation.
Thus J_L wedge J_M=0 for every pair. For n>=2, all nonzero J_L lie on one
common input line. For n=1 this conclusion is automatic.

## 3. Explicit binary merges

Inside group L every matrix has output line L, so the difference of ANY two
partial weighted means has rank at most one. Merge its original faces by
any binary tree. If its total weight is p_L, its resulting mean is

    C_L = v_L tensor (J_L/p_L).

The C_L all have the same input line, or are zero. Therefore differences
between any two partial weighted means of these group means also have rank
at most one. Merge the groups by any binary tree, with their exact weights.
The root is sum_i lambda_i A_i=B. Every original face appears once; there
is no target-edge subdivision, graph cover, or duplication of its mass.
Within-group merges plus between-group merges total F-1.

## 4. Full affine Dirichlet trace; holes do not matter

Let Omega be any bounded polyhedral domain, possibly with holes, and let
u be continuous finite piecewise affine on its closure, with u=Bx+c on
EVERY boundary component and rank(B)<=1. Extend u by Bx+c outside Omega.
The same face argument applies to this global Lipschitz piecewise-affine
extension. If B!=0, choose its output line L0 and write B=v_L0 tensor b.
For L!=L0 the extended rho_L is compactly supported and distributionally
closed on R^n. For L0, rho_L0-b is compactly supported and closed.

Any compactly supported integrable closed covector field eta on R^n,
n>=2, has integral zero. For example its continuous Fourier transform
satisfies xi_i eta_hat_j(xi)-xi_j eta_hat_i(xi)=0; approach zero along two
different coordinate directions to force every component eta_hat(0)=0.
For n=1, no such conclusion holds, but every matrix has a common input
line already and the laminate construction is immediate.

Thus all nonboundary-line packet means vanish and the boundary-line packet
has mean B divided by its packet weight. When B=0 all packet means vanish.
The same two-stage merge constructs a tree with each original face once.
No simply-connectedness assumption or individual boundary-component
constant integration has been smuggled in; the full affine exterior
extension is the reason holes are harmless. Different affine traces on
different components are outside this statement.

## 5. Translation and scientific limits

The argument also applies if every A_i-C has rank<=1 for one fixed matrix
C, by applying it to u-Cx and then adding C to every node of the tree.
This translation preserves every rank-one difference. It does not assert
that arbitrary 2x2 gradients admit such a common C.

This gives an exact Jensen certificate for rank-one convex functions on
the stated laws. It does not solve Morrey, allow arbitrary finite
rank-one-supported probability measures without gradient compatibility,
or establish a comparable statement for rank-two cells, arbitrary weak
limits, approximate rank constraints, or continuum direction fields.
Priority remains UNKNOWN. The ingredients are standard Hadamard jump
compatibility, closed one-forms, null minors and elementary laminate trees.

## Verification plan

Root's independent rational fixture has 32 triangles on a 4x4 periodic
grid, two output lines, genuinely varying input covectors and nonzero
affine period B=(1,1) tensor dx. The script must derive gradients from
actual nodal values, check all face/period interfaces, derive the groups
and means, and verify every merge and every original face exactly once.
It is finite diagnostic evidence, not a replacement for this proof.
