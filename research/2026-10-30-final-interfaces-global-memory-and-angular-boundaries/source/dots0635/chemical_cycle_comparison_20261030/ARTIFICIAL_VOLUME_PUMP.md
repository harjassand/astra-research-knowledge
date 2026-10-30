# Exact mass-action counterexample to arbitrary cycle-preserving-volume comparison

Status: internally derived, unreviewed. This is a counterexample to a proposed approximation/comparison principle, not to recurrence of the full process.

Fix R>1. On two species include four disjoint reversible linkages:

    10A <-->11A,   20A <-->21A,
    10B <-->11B,   20B <-->21B.

For both species choose lower-channel forward/backward constants R,1; higher-channel constants1,R. The all-unit reference constants balance every linkage and give mu0(a,b)=1/(a!b!). The actual full process is a product of independent birth–death chains; on its unbounded closed classes it is positive recurrent. Indeed in one coordinate its birth/death ratio is asymptotic to1/[R(n+1)], so its stationary tail is factorial up to exponential factors.

Now take any finite nearest-neighbor self-avoiding path x0,...,xM entirely in a,b≥21. Retain just one complete reversible residual layer for each path edge: for an increasing coordinate edge use the lower channel, and for a decreasing edge use the higher channel. Both directions of each retained layer are kept. All other residual layers are discarded. Thus this is a legitimate finite cycle-preserving truncation of the fixed mass-action graph.

For each oriented path edge the exact reference flux equality is

    mu0(x_i) q0(x_i,x_(i+1))
    =mu0(x_(i+1)) q0(x_(i+1),x_i)=1/z_i!.

By the chosen channel, the actual forward/backward conductance ratio is R, regardless of whether the spatial step increases or decreases its coordinate. The finite path stationary distribution is therefore exactly

    pi(x_i) ∝ R^i mu0(x_i).

The tree density is T_(x_i)/T_(x0)=R^i. A square snake of side n has M of order n² while all |x_i| are O(n). Consequently the hoped-for volume-uniform exponential-distance tree-density bound fails even for truncations of this fixed, elementary, genuinely recurrent weakly reversible mass-action network. At the end of the snake the density distortion is exp(O(n²)), which overwhelms factorial weight exp(−O(n log n)). Reference factorial confinement and chemical cycle preservation alone do not rule this out.

This also explains why arbitrary exhaustions are dangerous: a core can be enlarged and its omitted channels later restored, while newly added remote path corridors create increasingly severe finite-volume pumping. No such construction is needed to refute the uniform claim, and no assertion about a particular exhaustion's limit is used here.

## Required repair
Any useful finite-volume tree argument must use a canonical geometrically complete residual cutoff (for example, every residual layer whose full linkage is contained in a box) or explicitly control channel omissions. The exact tree identity remains valid. The desired density comparison is still unproved for canonical cutoffs; this example does not refute it there.

This is a stronger diagnostic than a generic Markov perturbation counterexample: all retained rates are exact falling-factorial mass action, rate constants come from one fixed finite WR network, and each retained chemical cycle is complete. What fails is treating layer completeness as adequate geometric control.
