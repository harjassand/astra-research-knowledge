# Independent constructor review of the mixed-gas analytic consumer

2026-11-02. PASS for the analytic interface reviewed, not a claim of historical novelty or practical constants.

Reviewed file: thermal_perturbation/MIXED_GAS_ANALYTIC_CONSUMER.md
SHA256: 3077290b18531e15c9cf10ee4afe18c8e611db56cfe788c8a7a0e38a840c0654.

Bound exact representation: EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md
SHA256: d6c5c78066af317d3c3e75fcdff64c3a9f6d77446c348140c23cbc8702d8f238.

## Checks

1. Primitive source activity goes to zero at fixed beta and native parameters. Full-column rod charge is finite and proportional to distinct-label count, so mixed KP can absorb sources by choosing sufficiently small fixed perturbations. Source-label counting anchored at possible interaction labels justifies the geometric G(q0) sum; multiple anchors only overcount.
2. Exact scaling eta^(number of V events) applies to trajectory-level activities and every selected Mayer cluster. It therefore gives a single O(v) prefactor to all source-containing clusters. This avoids assuming differentiability of a spatially local operator logarithm or bounding global Gibbs-state distance.
3. Source syndrome dependence consists of its own marked clock fluxes PLUS its closed-Pauli stabilizer filling. The polynomial anchor count is paid by the spare exponential source-size weight, not by an exponential in filling volume.
4. Any remaining changed character has a winding rod on the flipped check. Marking that rod and using the rooted >=2 cluster bound is valid: a selected mixed cluster also contains a source, hence cannot be the singleton. Overcounting source-free clusters after extracting the actual source-scaling factor is safe.
5. A nontrivial logical source requires distinct-label support at least d/b_D; arbitrary repeats do not increase support. The scalar pinned-ratio lemma supplies a RELATIVE matrix remainder, avoiding an extensive partition-function lower-bound loss.
6. Memory OR native-clock labels anchor exceptional sources, because clock-only native errors may acquire a data Pauli after U. Bath-only components remain scalar regardless of size. Thus the remainder is O(n) anchored rather than total bath-volume anchored.
7. Positive actual projected Gibbs weights are compared to the modulus of the nonzero scalar background, with controlled 1±r_n factors. No positivity of individual signed polymers is assumed.

The optional stronger doubled-charge calculations in MIXED_KP_PARAMETER_ADMISSION.md are unnecessary for this cleaner eta-scaling consumer and must not be presented as an extra premise of it.

Conclusion: no new gap found between exact source representation and the static perturbed-Gibbs witness-ratio input. The existing exact physical-time logical-twirl consumer still requires its stated equilibrium initialization, local-correctability, and actual-Hamiltonian hypotheses to be joined separately.
