# Independent review of the frozen v1 certified qubit projections

2026-10-29. This review recovers and extends the existing `independent_collective_review` rather than replacing it. `check_exact_v1.json` binds reviewed files by SHA-256. The independent checker imports neither the proposal nor repair implementation.

## Accepted at actual scope

For each of the 192 recorded N64 updates, the supplied output is an exactly rational qubit POVM, and its weighted squared Frobenius objective is within the requested `xi=1/1048576` of the optimum. Every record-driven input and unseen-label split is replayed exactly, including all 64 times for each of the three seeds. The records equal the earlier unmodified N64 bank. Maximum exact-certified gap, displayed approximately, is 9.416514393020858e-15. This is stronger than float feasibility but not evidence of improved recovery performance.

Four separate extreme-multiplicity certificates, K=2^60, 2^120, 2^512 and 2^2048, pass the same independent rational primal/dual test with gaps below 1e-7. These are single instances of one fixed overloaded-center family, not coverage of arbitrary weighted inputs.

## Governing argument

Write a Hermitian matrix as v0 I+v1 X+v2 Y+v3 Z. It is PSD exactly when v0>=0 and v0^2>=v1^2+v2^2+v3^2. Its squared Frobenius norm is twice the squared Euclidean coefficient norm. Aggregate unseen effects use weight 1/K, correctly representing K identical per-label effects.

For objective sum_i w_i ||E_i-Y_i||_F^2, add Tr[L(sum_i E_i-I)]. Completing squares and minimizing each PSD block gives the dual function

    -Tr L + sum_i w_i ||Y_i||_F^2
             - sum_i Tr[(2 w_i Y_i-L)_+^2]/(4 w_i).

No constraint on L is required. For a coefficient vector v, the two eigenvalues are v0 +/- sqrt(sum_{j>0} vj^2). Exact integer square-root bracketing gives upper bounds v0+hi and v0-lo for these eigenvalues. Squaring their nonnegative parts gives an upper bound on the subtracted quantity, hence a genuine LOWER dual value. Every primal value, dual lower value, gap and feasibility predicate is recomputed using rational arithmetic. Weak duality is sufficient for certification; optimizer convergence or float eigenvalue accuracy is not assumed.

The repair procedure rounds to rational coefficients, lifts each block by an upper bound on its spectral negativity, scales their sum below I using an upper bound on its largest eigenvalue, and adds the exact PSD residual to the last block. The construction and independent feasibility test agree. These operations can increase the objective, but the final gap includes the increase.

## Limits and required corrections

`project_certified` v1 is fail-closed: it raises if its final exact gap is too large. Its float Dykstra proposal has a fixed iteration cap and no accepted worst-case termination or complexity guarantee. It converts multiplicities to floats and cannot handle K=2^2048 on its public route. The extreme-K script instead uses a distinct seen-only limiting-dual candidate factory; the exact finite-K term remains in the certificate. Therefore extreme-K certificate validity must not be advertised as generic public-solver coverage. Author was notified to integrate safe routing separately.

The N4096 log alone contains two completed-seed announcements, not a completed output bank or certificates. It is excluded from this acceptance. Source dynamics, Born probabilities and diagnostic scores remain floating simulations. No hardware acquisition, complete source model identification, arbitrary flag-dimension solver, performance advantage, novelty or end-to-end scalable architecture is certified here. The earlier negative baseline comparison remains in force.
