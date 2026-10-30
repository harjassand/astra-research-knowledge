# Exact finite-halo interface for a truncated one-unbounded-coordinate corner

Status: repaired version passed child adversarial check (see INDEPENDENT_HALF_FACTORIAL_HALO_AUDIT.md); no whole-project independent review. This is a local adjoint statement, not a claim that the physical corner is invariant.

Let one species count n be unbounded and let j denote all other species counts. Fix ANY finite corner set J of bounded-coordinate values. Write an original complex as y=(a_y,b_y), where a_y is its unbounded-coordinate count. Define the finite residual set

    Z={j−b_y : j∈J, y a complex, j≥b_y coordinatewise}.

For every z∈Z, include the ENTIRE original complex graph translated in the bounded coordinates. Its lifted complexes are

    (phase z+b_y, unbounded order a_y).

An original edge y→y' gets lifted coefficient

    k_yy' (z+b_y)_(b_y)>0,

and shifts the unbounded count by a_y'−a_y. Identical lifted edges are retained with their coefficients added. The union is a finite-phase weakly reversible reaction graph, because every retained translated linkage is complete. Its finite phase alphabet is the halo H={z+b_y:z∈Z,y a complex}.

The lifted finite-phase generator agrees with the physical generator on EVERY outgoing edge from a phase in J. It also includes EVERY physical incoming edge to a phase in J: for a target j∈J and target complex y', its residual is z=j−b_y'≥0, which belongs to Z, and the predecessor phase is z+b_y∈H. Conversely retained labeled edges are genuine original mass-action edges with the exact bounded-coordinate falling-factorial coefficient.

Therefore, for any positive function mu defined on the halo,

    L_physical^* mu(n,j)=L_halo^* mu(n,j), j∈J,

where the physical expression uses the halo values on every incoming predecessor. Values outside H are irrelevant to this equality. No closed-cylinder assumption is made.

## Receiving application: split nontrivial, neutral, and absorbing components

The full halo graph can have projected components with all residual increments delta=0. The earlier blanket application of the nontrivial phase theorem to every halo state was invalid and is replaced here.

1. On a projected component with some delta≠0, apply the universal half-factorial extension at the already fixed alpha∈(0,1/2).
2. On an all-delta-zero component, the residual r=n+beta_j is conserved EXACTLY. If its phase set is wholly contained in J, its residual classes are closed finite PHYSICAL classes, because all physical outgoing edges from J are included. These classes are already positive recurrent and are excluded from a strict-drift assertion.
3. Otherwise restrict this neutral component to I=J intersect its phase set. Its finite phase generator Q_I(r), killed at H\J, is transient for all sufficiently large r: the full projected component is irreducible and every retained edge is then enabled. Set the exterior halo values to Gamma(r+1)^(−alpha). After dividing by Gamma(r+1)^(−alpha), their normalized incoming forcing is g(r)=Q_(O,I)(r)^T 1, where O is the exterior phase set in this component. It is an explicit nonnegative polynomial vector. Define

       v_I(r)=(−Q_I(r)^T)^−1 [1+g(r)].

   Positive killed-chain forest formulas make v_I positive rational. With mu_I=Gamma(r+1)^(−alpha)v_I, the EXACT local adjoint equals−Gamma(r+1)^(−alpha) on I. No count-shift error occurs because delta=0. This is an actual interior-killing solve, not a claim that the full neutral halo has negative drift.
4. A j∈J absent from H enables no bounded-coordinate part of any complex. For all sufficiently large n it is absorbing, and weak reversibility also prevents incoming edges. It is a closed singleton physical class, not a state at which strict negative adjoint is claimed.

Thus on each fixed infinite physical communicating class, all sufficiently large-count states in J receive a local strict adjoint certificate with the prescribed alpha. Already closed finite classes are handled separately. The union of all finite classes across different residual values need not be finite, and no such assertion is used.

The physical process may leave J and H; the local certificate does not prevent that and is not itself a stationary law. The remaining global task is to match these earned halo values with bulk/joint-shell values on overlaps and absorb outgoing feedback. That task is not declared solved. The construction removes the false prerequisite that a truncated corner itself be weakly reversible or closed, and the common-alpha extension prevents choosing its width from silently changing the factorial exponent.
