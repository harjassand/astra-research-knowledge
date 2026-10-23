# Cycle9 result: exact, stable, and star recovery need different query counts

Pro2, 22 October 2026. Original scientific recovery contract retained.

## Main result

For fixed p>=2, consider the intrinsic connected class C_p whose actual blocks
are K_(p,k), k>=p+1, with cut vertices on the k-side and in exactly two blocks.
Block-tree depth, branching and k are unrestricted. The complete proof gives:

| Requirement within coordinate designs | Worst-case minimum actions | Uniform noise guarantee |
| --- | ---: | --- |
| Exact identification alone | p+1 | Inverse grows on long block chains |
| Uniform stable recovery | p+2 | Operator and Frobenius constant sqrt(3+sqrt(5)) |
| Star-color recovery | 2p+1 | Operator sqrt(3/2), Frobenius sqrt2 |

The stable lower also covers arbitrary signed/unequal amplitudes in one
coordinate per row. It does not cover rows mixing several coordinates.
All designs obey whole-row norm one (or at most one in the lower). All
actions use the original arbitrary supported symmetric D with free diagonal.
No matrix rounding, reduced support, coefficient prior or noise distribution
is introduced.

The p+2 construction colors all hubs with p colors and uses two alternating
middle colors down the native block tree. Every bichromatic component is a
spider with arms of length at most two. An exact two-variable Poincare
inequality bounds its incidence inverse independently of the number of arms.
Canonical LS, disjoint action cells and symmetric duplication give the stated
absolute-Frobenius-noise bound on the full matrix. This is an all-depth theorem,
not a finite palette or sampled graph extrapolation.

## The marked-root frontier changes decisively

The completed Cycle8 atom theorem survives. New support-preserving contexts
qualify a genuinely specified root: degree-three roots can be terminals;
degree-two roots are represented as the original midpoint of a path2 branch.
K_(2,3) shows why a degree-two mark cannot always be a terminal.

All 66 active-degree families in the accepted certificate have a new literal
marked-midpoint witness guaranteeing distinct root-neighbor colors and at
most one far-repeat flag. The independent new projection check passed, with
61 zero-flag and five one-flag bounds. The old closure was not rerun.

Nevertheless universal star-four gluing is FALSE. Three K_(2,4) blocks in a
path have 16 vertices, 24 edges, treewidth at most two and maximum degree four,
and are chordless. Every star-four coloring of a single block can provide its
special safe root state at only one middle vertex. The central block needs
that state simultaneously at two different attachment vertices. This is an
all-colorings contradiction, confirmed by an independent complete enumeration.

The SAME 16-vertex graph has the new stable four-action operation. In the
parameterized class, a central K_(p,2p) with p attached copies requires 2p+1
star colors; the stable design still uses p+2. Thus insisting on stars can
cost p-1 actions on a family with a fully paid uniform inverse.

For p=2, k in {3,4} is inside the original chordless, width-two, degree-four
target. For p>=3, the class remains bipartite/triangle-free and width<=p,
but is generally NOT chordless. The full arbitrary-real four-versus-five
question for all degree-four partial two-trees remains OPEN.

## Actual native receiving operations

The inputs are only original n and edge lists. The native algorithm discovers
and checks blocks, cut roles, p, depths, designs and actual component shapes.
Both operations have saved exact rational D, full DX, nonzero E, Y, recovered
coefficients, projected actions and normal equations.

| Native input | n,m | p | Stable/control actions | Squared Frobenius error/noise ratios |
| --- | --- | ---: | --- | --- |
| Original star-four obstruction | 16,24 | 2 | 4 / 5 | 404567/379652 / 39981/48425 |
| Unequal branching blocks | 27,54 | 3 | 5 / 7 | 36589043/39435200 / 157819/226350 |

Each comparison uses the SAME D and the SAME absolute Frobenius noise norm;
the control's extra noise columns are zero. These are exact implementation
checks, not statistical comparisons. All noiseless reconstructions and
projected-action residuals are exact, with residual zero. Raw observation
residuals are saved and generally nonzero.

A no-producer-import checker reconstructs the original supports and solves
Fraction normal equations independently of the producer's subtree decoder.
All four receiving operations and all 66 new marked witnesses passed. The
receiving example is an actual use of the replacement construction on the
support that defeats star-four gluing, not a claim based on archive receipt.

## Costs and controls

The native Python recognition uses O(n+m log m) comparison work because it
sorts canonical edges/blocks. Coloring, shape checking, and decoding use
O(nq+m) arithmetic/storage. The q original actions, input assembly, sparse
output, bit complexity and any floating residual are charged separately.
The exact receiver bodies together took 0.016832031 seconds; their independent
gate, including the new marked projection, took 0.105831824 seconds.
All metered bodies and unknown totals are recorded in COSTS.md. These small
execution times are not discovery or total research cost.

The first receiver failed due to a shadowed p variable; failed source and
exception are retained and its unmetered cost stays unknown. A separate
read-only review caught a quadratic list-membership issue for unbounded k;
the corrected implementation uses sets. Allowing a middle to belong to
three or more blocks breaks the proved parity invariant; a concrete family
has diverging cut balance despite component diameter four.

The matched star control has more actions and better conditioning. Classical
sparse-Hessian acyclic substitution and star recovery are established, and
their prior error analysis is explicitly acknowledged. The original three-
action forest control and full-class five-action control remain intact. No
NIST, molecular, physical-performance or total-runtime advantage is claimed.
The Cycle5 receiving squared constant remains 20, unchanged.

## Continuation decision

Retire universal star-four gluing on the connected chordless class under its
now-disproved assumptions. Retain the positive atom and marked-root theorems.
Continue the stable-recovery programme with nonstar components and simultaneous
attachment mass constraints. The next precise test is a four-coordinate
uniform inverse for block trees of chordless theta atoms with three or four
branches of arbitrary length, with all actual attachments at degree-two
interior vertices and each cut vertex in two blocks. The present theorem
settles their all-length-two K_(2,3)/K_(2,4) case; arbitrary path lengths and
multiple adjacent marked sites are not supplied for free.

Historical novelty, external acceptance, implementation usefulness and physical
performance remain separate. Source delivery is not another owner's reading,
scientific acceptance or integration. No job continues in the background.
