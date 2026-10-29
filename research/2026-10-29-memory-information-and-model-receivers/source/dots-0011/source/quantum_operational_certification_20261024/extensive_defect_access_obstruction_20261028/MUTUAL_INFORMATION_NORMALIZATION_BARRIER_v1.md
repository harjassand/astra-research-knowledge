# Typical full-reference normalization pays an exponential mutual-information scale

28 October 2026. New exact per-sector bound and asymptotic consequence, pending independent review. This is a lower bound for the code-oblivious error-row block interface, **not** a lower bound for all recovery algorithms.

## Exact sector statement

Take a universal Schur sector lambda,mu and a selected environmental irrep nu with nonzero Kronecker multiplicity g_(lambda,mu,nu). Let d_lambda,d_mu,d_nu be their Specht dimensions. The complete selected reference space has dimension N>=d_nu because it contains at least one full copy of nu. The normalization identity from NORMALIZATION_AND_STRUCTURED_CODE_v1.md therefore gives

    alpha_full^2 >= d_lambda N/d_mu
                    >= d_lambda d_nu/d_mu.             (1)

Here alpha_full is the normalization of a block access interface for the complete unencoded row [F_1 ... F_N], not the normalized channel's Stinespring isometry and not the code-restricted row. Changing basis or using a redundant Parseval frame cannot change this norm. A coherent rather than enumerated coefficient register can reduce classical compilation cost but cannot violate (1).

For a partition theta of k with at most r rows, standard hook/type estimates give

    2^[k H(theta/k)]/(k+r)^[b(r)] <= d_theta
        <=2^[k H(theta/k)],
    b(r)=(r−1)(r+2)/2.

Consequently (1) implies the finite lower bound

    log2 alpha_full >= (k/2)[H(lambda/k)+H(nu/k)−H(mu/k)]
                       −[b(r_A)log2(k+r_A)
                          +b(r_E)log2(k+r_E)]/2.         (2)

If the right side is negative the ordinary contraction lower bound alpha_full>=||B|| still applies; no spurious positive obstruction is inferred.

## Iid finite-local-dimension interpretation

For a purification |psi>_ABE of a fixed finite-dimensional bipartite state rho_AB, perform the actual commuting local Schur sector measurements on k copies. Each marginal spectrum concentrates at its own reduced-state spectrum. A union bound over the three marginal concentration statements suffices; independence of lambda,mu,nu is unnecessary. Entropy continuity then gives jointly, with probability tending to one,

    H(lambda/k)=S(A)+o(1),
    H(mu/k)=S(B)+o(1),
    H(nu/k)=S(E)+o(1).

Any triple occurring with nonzero physical probability has nonzero invariant coupling, hence g_(lambda,mu,nu)>0. If the chosen universal reference includes its environmental nu, equations (1)–(2) imply

    alpha_full >= 2^[k I(A:E)/2 − o(k)],
    I(A:E)=S(A)+S(E)−S(B).

Thus for fixed sources with positive A–environment mutual information, a high-mass complete reference interface built before code restriction carries an exponential normalization even when the coherent information S(B)−S(E) is positive and a positive communication/distillation rate is possible. At a code rate near coherent information, d_lambda/K itself has exponential rate I(A:E), explaining the sqrt(d/K) gap between full-row and potentially near-isometric encoded-row normalization.

For any fixed tiny positive rate slack, the same conclusion holds with the corresponding entropy slack in the exponent. This statement concerns a selected sector whose actual nu is included. A reference omitting all typical nu evades the bound only by losing the physical mass it was supposed to recover.

## What is and is not removed

This identifies a genuine cost of the *code-oblivious row interface* which is not merely the (k)_j enumeration artifact of the fixed-defect construction. It does not prove a universal query lower bound: efficient code-aware compilation can avoid the full-row interface altogether, as the explicit flag-dephasing example proves. Nor does a supplied normalized Stinespring oracle automatically implement the transposed error row at unit scale.

A hierarchical reference algorithm must therefore demonstrate how its final effective encoded block normalization avoids the mutual-information scale, not only how it stores or traverses error labels in logarithmic space. A structured Young-compatible code would need to produce that code-aware contraction while maintaining the required recovery guarantee; preserving a literal common prefix under the entire conjugated algebra is too strong and generally fails. These are the next load-bearing construction obligations, not solved steps.
