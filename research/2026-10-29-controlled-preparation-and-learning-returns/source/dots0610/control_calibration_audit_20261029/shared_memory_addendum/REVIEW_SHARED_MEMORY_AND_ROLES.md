# Separate independent addendum: shared-memory obstruction and role allocation

2026-10-29 04:51 UTC. The prior calibration receipt is unchanged. Verdict: **accepted at stated scope** for SHARED_MEMORY_COUNTEREXAMPLE_v3.md and the algebra in OPTIMIZED_MODULAR_ROLE_ALLOCATION_v4.md. These are respectively an exact counterexample and a conditional optimization calculation, not experiments.

## Counterexample

All maps have a full CPTP completion. The encoder Kraus operators V tensor |0><f| sum to identity on logical-plus-flag input. The decoder code-sector Kraus operators Z^f V† tensor |0><f|, together with the two equally weighted replacement outputs for each physical-complement basis vector and flag value, sum to identity on the complete physical-plus-flag input. The source I_data tensor X_flag is unitary. Thus no trace-decreasing postselection is hidden.

Algebraically the endpoint round trip is id_logical tensor Reset_flag. The source-included service is Ad_Z tensor Reset_flag. The encoder reset makes these identities hold for arbitrary initial flag state, including correlations with the logical input or an external reference. The author program checked basis flag states; this review additionally compared both COMPLETE logical/flag superoperators on all matrix units, covering their off-diagonal and correlated-input action. Maximum discrepancy was 4.45e-16. Trace preservation and the author fixtures were rerun in a separate copied folder.

Every physical source input is unchanged, so all matching tests pass regardless of the flag. Membership passes because V lands in spin zero. A fresh round trip resets the flag before using it and therefore also passes. Repeating/interleaving these tests cannot distinguish the construction from correct service. Physical permutation inverses cancel exactly because the source is identity on data. Logical Pauli conjugation preserves Ad_Z up to an irrelevant sign, as independently checked for all four pads. Full-path computational/Hadamard testing instead fails with probability 1/2.

There is no explicit matching, pad or role-key input to a component map. Nevertheless the shared physical flag records that the source was invoked; the decoder can act differently on that state. This is a component-memory channel, not gratuitous classical metadata leakage. A stronger physical isolation assumption forbidding it excludes the example. The example does not refute the accepted theorem, which expressly assumes such isolation. Its consequence is precise: fresh modular test success cannot by itself establish the missing endpoint/source isolation or justify replacing D(id tensor B)E by id tensor B.

## Role allocation

For positive c_i,w_i,lambda_i with sum lambda_i=1, weighted Cauchy gives the stated linear majorant. Choosing a_i=s c_i/(R lambda_i), R>0, makes R times the aggregate test-failure hazard exactly the upper majorant for the service-bad hazard. The stated normalization enforces s+sum a_i=1.

The unweighted ratio is minimized by lambda_i proportional to sqrt(c_i). The weighted per-generated-service test cost sum_i w_i c_i/(R lambda_i) is minimized by lambda_i proportional to sqrt(w_i c_i). This follows directly from Cauchy, with equality at those vectors. It is not a minimization of acceptance-conditioned payload cost, total latency, or source exposures; the manuscript correctly separates native source calls from endpoint calibration calls. Independent arithmetic checked 200 positive-weight cases against 2,000 other simplex points. The asymptotic unweighted coefficient is 30.388761398760714, consistent with 30.39. The full-path coefficient-2 comparison remains valid under its own reference/privacy assumptions.

Files in this addendum are independently hash-bound in REVIEW_RECEIPT.json. The earlier three-axis/triangle/control-debit acceptance is neither overwritten nor silently extended to shared-memory endpoints.
