# Initial feasibility gate

Committed before the distance13 result is run/read, 2026-11-05.

- Public specified standard unrotated planar surface code, distance13, 313 physical qubits,156 ideal X checks.
- Independent Z flips with rational probability1/1000; no device/noise-acquisition claim.
- PyMatching exact minimum-weight correction with integer unit weights and its deterministic tie convention.
- Exact rational/integer canonical-witness rejection proposal, all nonbacktracking left-to-right paths of length<=55.
- 10,000 independent idealized trials, implemented with reproducible Python PRNG seed20261105. Ideal-randomness caveat retained.
- One99.9% two-sided Clopper-Pearson confidence interval, outward20-bit dyadic endpoints proved by integer binomial-CDF comparisons.
- Add exact rational Chernoff/nonbacktracking bound for omitted longer canonical witnesses.
- Record all acceptance/rejection categories and complete setup, sampling, exact-confidence time before JSON serialization.
- No advantage claim based on validity alone: compare against established splitting and importance/canonical-witness methods, including total cost and acceptance scaling. Scope and theory must survive independent review.

Existing sealed/held-out decoder data is not used. Only previously installed decoder libraries are reused.
