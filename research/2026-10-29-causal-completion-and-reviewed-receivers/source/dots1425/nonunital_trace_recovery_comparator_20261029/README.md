# Direct actual-prior trace comparison — 2026-10-29

Independent receiving acceptance: ../nonunital_trace_recovery_audit_20261029/REVIEW_RECEIPT.json (SHA256 bbf32be16645d563b483bff942c779094c7a743bcd0321575b6fd160df595f5b).

For Φ=X∘ADγ, γ≥1/2 (γ<1), and any ensemble with a diagonal actual barycenter, the explicit computational-basis measure/reprepare channel obeys e_avg≤(2+√2)√δ, where δ is the actual Holevo loss. No stationarity or additive barycenter penalty is required. The stationary case has coefficient≤2. The reference extension assumes a product barycenter; the map is EB on A, not on an untouched reference.

The proof uses actual averaged rotated-Petz recovery and direct trace projection. It bypasses both zero EB CP-mixture weight and an exact failure of entropy-comparator bounds demonstrated in ../nonstationary_coverage_obstruction_20261029. Generic universal recovery is prior machinery, not a novelty claim.

Reproduce: python check.py; python check_biased.py; python check_actual_prior.py. Scripts use NumPy/SciPy. Governing proofs, scoped check outputs, and immutable hashes are in SHA256SUMS.txt, BIASED_SHA256SUMS.txt, ACTUAL_PRIOR_SHA256SUMS.txt. No unrestricted N371, arbitrary coherent-barycenter, tensorization, or hardware claim is made. A separate coherent-prior finite certificate is under independent review in ../prior_adapted_trace_comparator_20261029.
