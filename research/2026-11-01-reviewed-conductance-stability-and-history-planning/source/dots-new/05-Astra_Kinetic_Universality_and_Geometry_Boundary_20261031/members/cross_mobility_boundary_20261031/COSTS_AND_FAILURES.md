# Costs, exclusions, and failed shortcuts

1. The unpatched shear trial u(y-alpha z) violates the prescribed full-fiber
   basin values, even at extremely unlikely z. Its energy is NOT a valid capacity
   bound. The blended trial in PROOF.md fixes every fiber exactly before any
   limit and pays a quantified Gaussian-tail patch cost.
2. A cross-mobility matrix having a small local quadratic-form direction is not
   itself a global capacity counterexample. Full basins and tails matter. The
   exact tilted-line lower bound proves that bounded cross coefficient b prevents
   capacity collapse even if det(D)->0. This rejects that simpler shortcut.
3. The Gibbs normalization is finite but the y marginal has only y^-2 tails.
   An invariant second moment cannot be assumed. The stopped coercive Lyapunov
   argument is pointwise in the initial state and does not use that moment.
4. A Lyapunov calculation valid only for block-diagonal mobility cannot be
   imported. V_D=1+x^T D^-1x is recomputed for each full constant SPD D and exactly
   cancels the drift pairing, including the cross terms. Its Euclidean coercivity
   constants need not be uniform over the family.
5. Each matrix is finite and SPD. The proof does not replace any member by a
   singular limiting SDE or assume existence/ergodicity of that limit.
6. Fixed D_yy does not mean all physical resources are fixed: the transverse
   noise variance and cross covariance diverge while conditional y mobility
   vanishes. Eigenvalue condition number is of order k^2/epsilon. Fixed metric
   lower ellipticity, bounded cross amplitude, or bounded transverse mobility
   excludes this collapse. Whitening is not free: it changes F and the basins.
7. Fixed potential plus an unverified kinetic interface does not receive a
   physical process. Constant SPD mobility, reversibility and fluctuation-
   dissipation remain part of the exact mathematical input contract.
8. Capacity/mass is the stated equilibrium observable. Neither a committor
   formula, arbitrary-start MFPT, angular equilibration time, nor finite-time
   crossing CDF is inferred from this example.
9. The finite receiver reads all its rational matrix parameters, verifies exact
   SPD and uses deterministic rational tail bounds. Integer construction/storage
   for its explicitly expanded powers has O(k^2+input-bit-length) bits; arithmetic
   is not unit cost. Large-k expansion can be costly. No polynomial dependence
   on the binary length of k is claimed.
10. The rational certificate bounds are conservative and nonoptimal. Floats in
    check_results.json are labeled diagnostics. The proof plus exact rational
    certificate objects, not rounded decimal displays, carry the guarantee.
11. Candidate matrix values with epsilon<=0 or >=1, invalid k, noncanonical
    rationals, floating point values, booleans, unknown schema, and extra fields
    are rejected. Unrecognized potentials and nonconstant/nonreversible dynamics
    are not silently approximated.
12. No external communications, publication, equipment, purchases, or denied
    source access were needed. No permission request or failed external action
    occurred. All new files are in this directory; prior freezes were not edited.

Receiver hardening: raw JSON duplicate keys are rejected. Before constructing
expanded integer powers, the receiver enforces a configurable positive exponent
budget (default 1,000,000). A budget rejection is a declared computational limit,
not a counterexample to the analytic theorem. It occurs before large power
allocation; all displayed examples fit the default budget.
