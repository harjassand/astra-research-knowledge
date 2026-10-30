# Finite bounded-species expansion

Conditional on the candidate strip theorem, consider a weakly reversible mass-action network with one distinguished count x and remaining count vector z. Supply a finite set J of bounded-population vectors such that the cylinder N_0 x J is invariant. For example, a positive conserved linear combination of all the remaining species can provide such a set. This is a substantive finiteness premise, not something inferred from deterministic permanence.

For each original reaction `(a,y)->(b,y')` and each j in J with j>=y, insert the expanded edge

    (j,a) -> (j-y+y',b), coefficient kappa (j)_y.

The coefficient is fixed and positive. This finite expanded one-hot network reproduces every rate and count jump on the supplied cylinder exactly. For an expanded edge, follow the original directed complex return path while retaining the bounded residual j-y. All intermediate populations remain nonnegative and in J by invariance. This yields an expanded complex return path. Therefore the expanded graph is weakly reversible, and the strip theorem applies after splitting mode components.

Costs: enumerate J and all available reaction-mode pairs. The number of modes can be the product of all supplied count bounds and can be enormous; no polynomial-in-binary-bounds complexity claim is made. Bounds on a chosen communicating class alone need additional argument if their full cylinder is not invariant; the present explicit reduction does not silently assume that closure.

This does not cover systems with two genuinely unbounded species. It is not the general chemical recurrence conjecture.
