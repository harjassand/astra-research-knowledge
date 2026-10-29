# Independent review — original ideal-idle noisy storage calculation

28 October2026. **PASS as a deterministic floating numerical calculation of the specified closed finite-tile model.** The later clocked successor is expressly outside this review. Original program, results and governing source were not edited.

## Independent reconstruction and replay

`check.py` separately reconstructs the parity/flag gate schedule, embeds gates using explicit computational-basis indexing rather than the author's tensor-axis updater, forms prepared-ancilla isometries and measured-outcome Kraus operators, and composes all193 adaptive terminal branches. Correction tables come from the earlier independent word-Pauli reconstruction, not the author's flag tables. Conditional physical correction pulses and the total weight-one fallback are included. Different classical measurement outcomes are summed incoherently after their actual corrections; no branch is postselected.

All ten signed angles in the original dataset were independently reconstructed, including zero and both signs at .001,.01,.03. Full instruments are trace preserving to floating accuracy. The ideal-angle instrument agrees with the complete ideal EC superoperator on all physical operators, not only encoded test states. Independent and author Kraus arrays agree within2e-16; largest independent TP entry residual is below1.2e-14.

For each angle the reviewer encodes the four logical Pauli operators once and propagates32-dimensional physical operators through every native/local-inverse map and every noisy EC map. Those actual operators are retained between rounds. Terminal logical PTMs at T=1,2,8,32,128 match the preserved result to below5e-13. Diagnostic decoding of a copy never updates the persistent state. All five fixed-control unencoded baselines were independently replayed at every saved horizon.

The naive decoded-one-round power is demonstrably different. At T128 the maximum PTM discrepancy is approximately .006936 for eta+.01 and .009370 for eta−.01; at eta±.03 it is approximately .064824 and .063471. This is retained physical-state feedback, not a modified fit. At eta0 the difference is numerical roundoff, consistent with actual ideal syndrome reset.

## Provenance and actual model

The selected calibration count4096/site is read from the original pilot selection record. The same saved learned frame matrices are used unchanged at each round. Their exact file hashes and the source-generator hash match the preserved result. The simulation knows source Kraus parameters as scorer; it does not give them to a new learner or fit a new receiver. There are zero new sampled acquisition/holdout records. The earlier pilot's complete acquisition cost remains paid, not just the selected bank.

This model has stationary product native channels, freshly discarded source environments, actual noisy adaptive EC, and physically applied conditional corrections. Native and learned-inverse operation is followed by EC; old records are discarded. Coherent gate errors have the same signed angle at all specified operations and all cycles. Ancilla preparation and measurement basis errors are included. Idles, readout bits, classical controller, and additional learned-inverse implementation error are ideal. This is a deliberately incomplete hardware model, not an unmentioned source of perfect timing control.

All193 terminal records have a defined correction. Sixty-four syntactic branches invoke the fallback (32 check/syndrome combinations, each with two flagged syndrome-readout possibilities); the fallback is fixed before evolution and not selected using results. Its higher-order success is not assumed. The101 potential noisy-operation count is consistent with56 flagged,40 fresh-pass and5 conditional correction operations;751 remains the broader potential location accounting, many of which are ideal in this noise family.

## Metrics and comparison limits

Entanglement infidelity and normalized Choi trace distance are calculated from the terminal PTM. A normalized Choi trace distance is not a diamond distance. The stated qubit lower/upper bounds and common-label Stinespring inequality are mathematically valid, but floating eigenvalues and Gram norms have no outward-rounded error certificate. We accept them only as diagnostics, not certified norm bounds or statistical confidence intervals. This numerical calculation does not inherit an experimental noisy-round fidelity certificate from the original pilot holdout.

The unencoded comparison uses the same fixed learned inverse and the same number T of native applications per physical site. It is neither equal wall-clock storage time nor equal total resources: an encoded logical round uses five native sites plus recovery, while each listed unencoded channel uses one site. “Time steps” in the original prose must be read as discrete native-use rounds, not elapsed physical time. These are not optimal horizon-specific unencoded decoders and do not establish superiority to every equally informed adaptive baseline. Source-informed terminal optimization remains a separate question.

Small favorable signed-control interference in some runs is a model-specific numerical effect, not a general benefit of noise. No noise threshold, new code, hardware demonstration, arbitrary returning bath protection, injection/readout implementation, or clocked-idle advantage is established. The later separately authored clocked model requires its own audit and is not approved by this receipt.
