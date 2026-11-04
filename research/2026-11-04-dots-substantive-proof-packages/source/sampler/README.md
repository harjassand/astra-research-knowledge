# Positive latent-Ising compiler: review packet

Status: mathematical construction complete at its explicit scope; independent verification pending. This is not an accepted Astra result, a production sampler, a novelty claim, or a demonstrated scientific speedup.

## Main deliverable
PROOF.md gives a raw-rational-tensor -> positive CP reconstruction -> global gauge/field certification -> polynomial-bit approximate partition/sampling operation. It applies to an explicit class on arbitrary simple cubic graphs, including nonplanar graphs and nonzero hidden fields. It includes a condition-preserving coupling-range reduction, original-variable sampling kernels, precision accounting, an explicit annealing FPRAS reduction, and an optional noisy-entry contract with statistical acquisition costs.

## Sources
SOURCES.md records the pinned N1077 source hash and strongest ordinary comparators. N1077_SOURCE.md is the exact source proof, recovered read-only from local revision 7d48e3de2106712b790d07d50de9edd1a20db365. No stale index rebuild or remote repository mutation was performed.

## Executed exact checks
- audit.py / results.json: heterogeneous positive raw tensors on K3,3; exact partition and all nine original-edge marginals; nonzero-field compatibility invariants.
- irrational_audit.py / irrational_results.json: raw integer signature [40,20,20,90], recovered irrational positive CP factors, and exact global rational cancellation.
- coarsening_audit.py / coarsening_results.json: 2,187 exact strong-edge probability checks, a counterexample if field consistency is removed, and the subdivision identity.

Run each with Python and SymPy. The examples are constructed finite audits, not learned scientific inputs or performance benchmarks.

## Independent review priorities
1. Is the normalization/sign test complete for strict positive rank-two CP decompositions at nonzero hyperdeterminant?
2. Do signed-graph balancing and positive symmetrization exhaust the declared latent ferromagnetic/consistent-field representations?
3. Is the strong-edge probability proof valid and does deletion/contraction/subdivision preserve both partition and TV error budgets?
4. Do local bounded-degree algebraic expressions avoid a global compositum and support the claimed exact comparisons/precision costs?
5. Does the published parameter-dependent mixing bound, after preprocessing, yield genuinely polynomial expected BIT complexity?
6. Does original-variable reconstruction use a positive stochastic kernel rather than an invalid arbitrary gauge interpretation?
7. Does the annealing argument avoid pinning-induced inconsistent fields and charge all independent approximate samples?
8. Are prior work, synthetic input provenance, lack of production implementation and absence of comparative advantage sufficiently explicit?

A successful review would support the scoped acquired-operation theorem only. It would not certify novelty, broad applicability, or the user's transformative-consequence bar.
