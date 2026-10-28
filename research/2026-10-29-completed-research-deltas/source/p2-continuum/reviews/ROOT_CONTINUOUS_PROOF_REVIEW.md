# Root review of the continuous residual and temporal-span obstruction

28 October 2026. Actual independent proof reading of the solver contributor's new result. No claim of an independent interval replay of its floating continuous solver.

Accepted mathematical scope: for a fixed temporal one-particle span W, a differentiable normalized trial constrained to Fock(W), a unitary Pauli source, and the single displayed sine vertex, the omitted factor gives residual at least |A|(1-exp(-tau))/sqrt(2). I independently derived the even/odd decomposition. The nonvacuum cosine variance is (1-exp(-tau))²/2, the sine norm squared is (1-exp(-2tau))/2, and these sectors are orthogonal. Their smaller coefficient times sin²+cos² proves the floor. Other retained generators and the trial derivative cannot cancel its exterior component.

The full continuous residual uses H² in the complete space, not the square of projected H. Orthogonal exterior and in-span time-freezing components add as positive matrices before the square root. The floating integrated values, finite-coordinate exponentials, conditioning and quadrature discrepancy do not establish numerical certified channel bounds. They do establish useful diagnostics under the stated mathematical formulas. The temporal floor bounds this residual-certificate strategy, not the actual endpoint channel distance.

## Root extension: nonunitary source exposure

For a bounded self-adjoint source S commuting with the bath, and a proposed input isometry V inside the fixed span, the same calculation gives the exact exterior input matrix

    R_out†R_out=A² V† S² [a sin²B_W+b cos²B_W] V,
    a=(1-exp(-tau))²/2, b=(1-exp(-2tau))/2.

Since b>=a, this implies

    ||R|| >= |A|(1-exp(-tau))/sqrt(2) * ||S V||.

This is a new root-authored immediate extension, not part of the contributor's independently authored proof. It is useful for the actual source sine: no uniform unit lower factor can be assumed when S has arbitrarily small singular values. For several exterior vertices, interference may invalidate summing separate lower bounds. A moving temporal span requires its derivative/transport term. Neither extension is silently included in the Pauli numerical example.
