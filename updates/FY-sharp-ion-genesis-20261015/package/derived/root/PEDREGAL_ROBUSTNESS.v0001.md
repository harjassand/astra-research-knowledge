# Strict-separation robustness of an allowed-mold obstruction

Root derivation, 15 October 2026. Independent primary-source audit first found
an exact nonempty-image obstruction; this note proves its stability under nodal
perturbations. It does not assert a counterexample to Morrey's conjecture.
The audit packet supplies the exact Definitions 4/6 and Corollary 7.2 mapping.

Take the periodic 2-by-2 nodal mesh of spacing 1/2, anti-diagonal triangles,
and scalar nodal maps (rows ordered by y, columns by x)

    u = [[0,4],[2,3]], v = [[1,0],[0,2]].

The paper allows a j=1 mold enumerating the four vertical interfaces first,
then four horizontal interfaces in row-major order. The last two are the
interfaces at y=1/2, x=0 and x=1/2. At their first merge, the u pairs are
(2,-4),(2,-2) and (-2,2),(-2,4). The v pairs are (4,2),(4,4) and
(-4,-4),(-4,-2). Fixed pair masses in Theta_1 imply that all t-weighted
barycenters lie in the respective line segments; r has the same pair-mass
constraint. Consequently the difference vectors obey, for all feasible t,r,

    U=(4,a), -8<=a<=-4;
    V=(8,b),  4<=b<=8;
    det(U,V)=4b-8a >=48.

The necessary simultaneous parallelism at this dyad is impossible. Other
upper-tree constraints cannot repair one impossible dyad. Thus this allowed
mold has T(t)=empty for every t in Theta_1. Uniform leaf weights 1/48 are
feasible; emptiness is not an empty-domain artifact. Both maps have eight
distinct triangle gradients. The dedicated auditor verifies all these
identities and its distinct earlier witness separately.

## An open neighborhood also fails

Perturb each nodal value of each map by at most epsilon. Each triangle
gradient component is a nodal difference divided by 1/2, hence changes by
at most 4epsilon. Every normalized convex pair barycenter changes in each
component by at most 4epsilon. A difference of two such barycenters changes
by at most 8epsilon, uniformly over t and r, including boundary weights.

For epsilon<=1/10, U_x>=16/5, U_y<=-16/5, V_x>=36/5,
V_y>=16/5. The determinant therefore has the exact lower bound

    det(U,V) >= (16/5)(16/5)+(16/5)(36/5)=832/25>0.

This is a whole nodal box of strict separation. Restricting to a dense class
of maps cannot rescue nonempty images for this same allowed-mold construction.
The original u/v have distinct gradients; perturbations can be made smaller
if distinctness is additionally required. A restriction to a different mold,
selection theorem, or alternative lamination construction would be a changed
argument requiring its own proof. This note does not exclude those repairs.

The target is the actual fixed-pair-mass, fixed-mold T of Pedregal,
https://arxiv.org/html/1905.06571v5 (18 June 2026), not an arbitrary search
for laminates. A failure of this corollary/proof route is not a disproof of its
claimed ultimate ROC-to-QC conclusion. No external author has been contacted;
historical originality, external validation and formal verification UNKNOWN.
