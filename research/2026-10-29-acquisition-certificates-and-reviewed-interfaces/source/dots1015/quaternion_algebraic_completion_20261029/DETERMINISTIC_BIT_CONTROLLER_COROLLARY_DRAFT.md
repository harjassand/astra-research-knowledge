# Deterministic bit-cost strengthening of the fixed-comparator controller

2026-10-29 — additive corollary, receiving review requested.

Dependencies: accepted EXPECTED_BIT_CONTROLLER_COROLLARY_DRAFT.md and its controller_composition receipt; accepted DETERMINISTIC_FIXED_DIRECTION_DRAFT.md and ../fixed_direction_quartic_audit_20261029/REVIEW_RECEIPT.json; the original accepted finite FTPL regret theorem. None of those files is modified.

For fixed rational probe probability p, every finite FTPL quartic query and requested additive tolerance have O(log(T+2)) rational bit length. The fixed good-direction theorem replaces the almost-sure random-retry template optimizer with a deterministic at-most6973-trial template optimizer. Consequently its mathematical worst-case bit-operation cost per edge/query is polynomial in log(T+2), with fixed potentially astronomical constants. There is no optimizer retry tail or grid-totalization dependence in this theoretical composition. FTPL itself still uses fresh private finite midpoint perturbations; the optimizer's determinism does not remove those required random choices.

Every query returns an actual rational unit quaternion with the same required global additive objective gap. Therefore the accepted fixed-comparator actual-history per-edge bound remains

 E sum_t delta_t(C_t) <= E sum_t delta_t(C*) +720 sqrt(35T/p)+720.

The persistent feedback bank remains35 rational O(log(T+2))-bit coefficients per edge; temporary solver state and current candidate precision are separately polynomial-bit resources. This is not a drifting-comparator result, a capacity claim, or a comparison against best actual encoder fidelity.

At a supplied finite deterministic implementation, a public horizon/input-bit bound could fix a worst-case mathematical work budget independently of the current private query. This strengthens the earlier theoretical padding option but does not supply a practical clock schedule, numerical constant, calibrated hardware, thermal/energy cost, control synthesis, or buffering mechanism. The present universal template is not implemented. The alternate normalized-quotient solver has accepted algebraic existence/bit-complexity arguments but is still under executable construction. No executed fast generic quantum controller or physical latency advantage is asserted. Equally informed conventional methods may reuse the same solver.
