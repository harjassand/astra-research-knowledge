# One logical protected token: first-hub clock comparison

Status: separate mathematical derivation and exact local comparison, not yet bound by an independent whole-review receipt. Prior accepted source files are unchanged. This does not replace the simultaneous multi-hub coverage table.

The parent proposed retaining one logical token rather than one token per inactive phase. Its state is0 (absent), one inactive phase i, or the absorbing hub set. When absent, accept each raw immigration at its rate lambda_i; an arrival to a hub absorbs. While present at i, ignore other arrivals, use conversion rates k_ij, and use death rate d_i to return to0. Conversion into a hub absorbs.

Couple this token to the actual core as follows. If the token is at i, split the actual linear conversion rate k_ij y_i into protected rate k_ij and remainder k_ij(y_i-1), and similarly split death. Protected events move/remove the logical token; other events leave it unchanged. A positive-count-preserving nonlinear reaction can remove individuals at its own population-dependent rate, but leaves at least one indistinguishable survivor in that phase; relabel that survivor as the protected token. This is not an independent immutable particle lineage. Starting with the token absent is valid for every actual population state.

The logical token's rates are autonomous and finite. Strong connectivity of the raw monomolecular graph through0 gives absorption on a hub in finite mean. Its killed matrix has |I|+1 states. Actual hub activation occurs no later than token absorption. Thus the solved mean from0 supplies a uniform first-hub activation bound.

The protected Dirichlet constructor uses this bound only in the one-sided excess and conservative termination witness. Its actual trial radii, finite head equations and exact fringe acceptance tests do not depend on the clock mean. The local comparison therefore checks every returned patch/Foster datum for literal equality after substituting the single-token acquisition; only activation-clock, termination-witness and clock-work metadata are excluded from that equality check.

Executed comparisons:

- Frozen five-species positive-cycle example: binary4 states, mean24; single token3 states, mean24. Exact same R4/head10, all patch/Foster data identical; both conservative scalar radii40.
- Parallel-arrival example: two inactive phases independently receive rate1 immigration and each converts to the sole hub at rate1; the hub has rate1 death and a reversible satellite star. Binary4 states, mean5/4; single token3 states, mean3/2. Exact same R17/head153, all patch/Foster data identical; both conservative scalar radii17.

The second example shows why reducing clock dimension is not automatically improving its mean bound. The mathematical termination proof remains valid with either positive finite bound. Costs include the actual head search, not merely clock size. A one-token state cannot certify simultaneous occupancy of multiple required hubs; the later coverage-support theorem uses a different target.

`compare_clock.py` imports the unchanged frozen-family constructor from the adjacent `stochastic_protected_boundary_20261031` directory and temporarily substitutes only its activation-clock function in memory. This is a pending research comparison, not a hardened standalone certificate verifier or a change to the accepted constructor.
