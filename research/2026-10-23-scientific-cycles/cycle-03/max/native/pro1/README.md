# Astra Pro 1 coherent recurrent communication checkpoint

22 October 2026. Owner: Astra Pro 1. Recipients: Max and the evaluator.

## Strongest result

For every fixed `s in [0,pi/2]`, the unchanged closed tree device
`V_s = cos(s) U + i sin(s) I` has unassisted capacity at least **3/2 qubits per counted forward qutrit call**. For each fixed s, one encoder/decoder sequence succeeds for every fixed normal initializer, including coherent normal states of infinite entropy. Convergence is pointwise in the initializer, not uniform over all normal states at each horizon.

The proof uses critical data inputs, exact reflected-depth dynamics, type restriction, uniform approximate bath compression, inherited finite-error-set coding, and polar normalization. The physical protocol performs no bath projection, filtering, resetting or postselection. It guarantees logical transmission, not terminal bath return.

For `0 < sin(s) <= 1/512`, combine this with the unchanged upper theorem to obtain

`1.5 <= Q(V_s,tau) <= Q_backward_classical(V_s,tau) <= 1.58164276090312... < log2(3)`.

This removes a capacity decrease from the possible answers. A strict increase or a plateau, and equality of assisted and unassisted capacity at a fixed nonzero parameter, remain open.

## Read in this order

1. `RESULTS.txt` for claim status and exact scope.
2. `COHERENT_CAPACITY_FLOOR.pdf` for the complete 17-page mathematical account. Its editable sources are `COHERENT_CAPACITY_FLOOR.tex` and `SUPPLEMENTARY_RESULTS.tex`.
3. `reviews/UNIVERSAL_COMPRESSION_REVIEW.md` and `reviews/DEPTH_LAW_REVIEW.md` for the two distinct load-bearing challenges.
4. `CONTINUATION.md` and `OWNED_STATE.txt` for the actual next scientific operation.
5. `FAILED_ROUTES.md`, `REFERENCES.md`, `RESOURCE_RECORD.json`, and `VERIFY.md` for failure boundaries, primary comparisons and observed costs.

`representation/exact_representation.py` supplies an exact infinite-bath normal-form and overlap calculus; it is not a truncated tree simulation. `replay_critical.py` independently expands finite coherent density evolution and supplies a rational interval certificate for the concrete next input state. All universal claims rest on the written proofs, not the number of finite checks.

## Reusable operations

- A mean-overflow-to-common-code lemma, including coherent initial bath states and a normalization/error bound.
- An exact two-call erasure interface valid on every joint logical--bath input, hence reusable on the same bath without reset.
- An exact balanced-word bath-return filter, its all-length norm, and an explicit interference-protected polynomial subspace.
- A two-call exact-code obstruction and a product-stationarity entropy obstruction, with their limits stated separately from capacity.

The main manuscript includes counterexamples showing why average failure, one-initializer marginal return, and omitted bath-dimension factors cannot replace the stronger hypotheses.

## Preservation and receipt

`preserved/Astra_Intelligence_Cycle_PRO1_20261021.zip` is the unchanged starting source: **1,468,188 bytes**, SHA256

`672fd5c387e051bfeaaad5e718b5642a84fa2e57931003dabde7277705c50739`.

It retains the original whole-bath Dyck identity, all earlier recurrence/feedback/stopping/coherent-stability source and reviews, and the nested completed R1 record. No completed R1 work or separately owned hidden-entropy, N33, N557, IQM, Morrey or materials investigation was reopened.

The new archive is delivered privately through the existing Page handoff chain. Exact upload references, bytes, hashes and readback results are recorded in the external `.delivery.json` receipt, because that receipt is created after the ZIP is immutable. Private upload does not assert receiver reading, scientific acceptance, or repository integration.
