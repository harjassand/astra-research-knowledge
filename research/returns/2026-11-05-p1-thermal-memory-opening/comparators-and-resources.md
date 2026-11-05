# Thermal-memory sampler comparisons, calibration and full physical bill

The [selected opening](README.md) is accountable to the strongest existing way to achieve the same write/hold/read operation. The [source audit](package/source_audit.json), [Code Swendsen-Wang comparison](package/csw_bdl_comparison.md), and consolidated [report](package/selection_brief.tex) retain unresolved comparisons rather than claiming exclusion.

## Comparators that can defeat novelty

Ground-state Clifford encoding is already available; a comparable ground-start lifetime theorem would answer the selected question without thermal loading. The thermal-start lifetime statement alone does not grant that theorem. Sector-mixing methods have additional metacheck/redundancy hypotheses, whose target applicability must be checked.

Code Swendsen-Wang may work if the actual physical-check matrices have sufficiently small graphic/cographic defect. One criterion uses a graph incidence matrix g on the same check coordinates with `ker(h^T) subset ker(g^T)` and defect `d=dim ker(g^T)-dim ker(h^T)`. Dependence `2^O(d) poly(N)` means d=O(log N) can suffice; the graph need not preserve physical geometry. One logical qubit or large metachecks do not settle that defect. The included [synthetic obstruction check](package/verify_matroid_obstruction.json) refutes that shortcut, not applicability to the target family.

Regular-matroid Ising approximation is a broader competitor than graphicness. The opening derives a counting-to-sampling self-reduction and binary-kernel lift. If both relevant physical-check matroids satisfy the required regularity, this can supply a polynomial approximate syndrome sampler. That actual regularity remains unresolved. Polynomial dependence on inverse accuracy is adequate; exponential holding does not require excluding a competitor merely for lacking logarithmic accuracy dependence.

Two October 2026 decoding-based preparation papers were available only at primary abstract level to the producer. Their theorem-level applicability was not excluded. The source record distinguishes full-text access, abstract-only access and failed retrieval. No completed priority determination is claimed.

## Fixed positive coupling variation and calibration

Using the same admissible decoder for history and protected logical frame, nonzero base syndrome forces a component whose size grows with hierarchy depth. Rooted polymer counting supplies stretched-exponentially small bad mass at sufficiently low fixed temperature. This uses actual positive couplings in activities and J_min for the bound, uniformly over fixed coefficients in [J_min,J_max].

For dimensionless lambda_a=beta J_a and sampler estimates lambda_hat,

```text
TV(p_lambda,p_lambda_hat)<=min(1,0.25 sum_a |lambda_a-lambda_hat_a|).
```

Average coefficient precision O(epsilon/N) suffices for an O(epsilon) loading term. Contractivity prevents a holding-time multiplier for that initial discrepancy. Changed check operators, extra logical terms, temporal drift and general noncommuting fabrication errors are outside this result; a direct general perturbation bound can grow as `t ||Delta H||`.

## Physical resources remain substantive

The operation assumes an explicit stabilizer description and recorded embedding, access to the stipulated commuting interactions, reset/product ancillas, classical randomness and memory. Polynomial classical compilation and O(N^2) Clifford gates are before routing. A supplied polynomial-size local control network adds paid routing. Two-body/material implementation is additional work.

Writing and reading need isolation or switching of the holding Hamiltonian/bath, or a proved compensation procedure. For G circuit locations, the sufficient hybrid bound sums their errors into the control budget; inverse-polynomial gate errors suffice in this accounting, but no constant-noise fault-tolerant preparation threshold is established. Fresh ancillas do not repair errors suffered by the unknown bare input before encoding.

Syndrome metrology, correction in the protected frame, inverse encoding, calibration, reset and fresh samples are required on reuse. Holding pays at least Nt spacetime volume and cooling power times t. The source's random-embedding scale around 5.4e24 and density bound around 6.6e10 are fixed but severe; independence from N does not make them practical. Fixed-positive commuting variation is not robustness to arbitrary hardware error over exponential time.

## Versions and unselected notes

The report consolidates the selected construction. [Quantum construction notes](package/quantum_new.md), [independent challenge](package/learning_challenge.md), [strict-AT alternative](package/learning_new.md), and [independent selection audit](package/independent.md) preserve their own conditions.

The [conditional thermal-transport note](package/conditional_thermal_repair.tex) is an unselected reusable derivation, not a completed Gibbs sampler. It assumes outcome-conditioned repair maps that it does not construct and did not receive the same independent audit as the selected sampler. It must not be promoted to an attained physical operation by reading its conditional equations alone.

The earlier equilibrium-inference, quantum companion, partial-SWAP compressor and acquisition-loss results remain unchanged at their earned scopes. The unrestricted joint receiver memory/processing law remains open. P1's nomination is a constructive opening for challenge, with existing samplers, source-specific assumptions and physical significance still capable of defeating the selection.
