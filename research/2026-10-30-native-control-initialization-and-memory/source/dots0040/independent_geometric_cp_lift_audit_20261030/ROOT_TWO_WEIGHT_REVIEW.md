# Independent root review of the two-weight CP-dressed basin repair
2026-10-30 00:24 UTC.

Reviewed DRESSED_BARRIER_COMPARISON_REPAIR.md, SHA-256 0d5ed927ac819ae14e8915eb39d6247f947ad9c9bb3a847a605d729b2aa7384b. This review concerns the new comparison/composition, not a fresh audit of the preceding clock commutator theorem.

Verdict: the comparison and killed-basin handoff are valid at the stated FULL-TENSOR DIRECT fresh-K scope, conditional on the cited clean drift and canonical boundary theorem. No new native one-site-reset or transactional dirty-sector conclusion follows.

Checks:
1. Use the STRUCTURAL backward causal cone, not a cone inferred after cancellations. Selecting no-jump summands inside it can expose extra clock dependence, but that dependence remains inside the recursively defined structural cone. Outside unital circuit gates still cancel. The cone has O(|A|) gates at fixed circuit depth and bounded range.
2. Each selected no-jump Kraus is clock-only because the complete reset bundle has sum K_s^dagger K_s=I. Ordered products need not commute; minimum singular values multiply from below. Thus the exact positive summand gives T(f_A)>=exp(-C t|A|) f_A with no volume-sized gate count.
3. Two nearby exponents are genuinely available: choose both c values in the open weighted-progress parameter region before choosing sufficiently small theta and t. The a_+-a_0 margin pays the local dressing loss, while V_0 retains the high-boundary estimate and V_+ supplies the clean drift. This is not a global constant comparison T(V)>=cV.
4. On the V_0 basin, accepted local correction moves neither raise V_0 nor leave component safety below the canonical-edge threshold. Thus each Schrödinger dressing channel preserves the basin, allowing a basin-restricted operator inequality to be pushed through its adjoint.
5. Basin preservation alone would not remove off-diagonal blocks. The additional covariance argument is correct: every K_s=F_s Pi_s has a definite stabilizer character, and the clock factors commute with all data stabilizers. The full CP dressing therefore preserves the stabilizer fixed algebra, which is block diagonal in the full syndrome. The syndrome-defined basin projector commutes with T(V_+) exactly.
6. The dressed-noise inequality and T(W_+)>=T(V_+) give a uniform killed moment. Since T(V_+)>=V_0, high-V_0 exit-source mass is controlled, and the existing local-boundary Duhamel argument applies with the same polynomial prefactor. Initial vacuum gives O(N) dressed moment; N>=N0 and fixed logical-independent clock/bath initialization are retained.

No physical projection onto the basin, physical implementation of the proof-only CP dressing, or observation of its no-jump record is required. The actual final recovery and all model/noise support assumptions remain those of the preceding theorem.
