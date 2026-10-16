# Raw-state decoder prior art and incumbent input audit

Checked 2026-10-15. Read-only literature, documentation, and archive-name investigation. No measured rows inspected, no fitting, no author code run, no installation or outreach.

## Decision

Raw stabilizer outcomes, soft information, leakage-conditioned decoding, and calibrated priors are established approaches. The remaining defensible question is whether **initial ancilla signs/preparation information supply incremental, transferable predictive information beyond detectors for this measured Willow condition**, with a leakage-safe evaluation and appropriately strong comparators. Algebraic loss of raw dimensions alone answers neither usefulness nor novelty.

The strongest acquired baseline is Libra with RL-optimized prior. It is NOT the strongest published Willow decoder. No acquired baseline supplies the published neural comparator. That availability gap is a routing constraint before a SOTA or invention claim; it does not justify replacing the comparator with plain MWPM.

## Critical target-leakage restriction

The acquisition audit already identifies the actual observable flip as a deterministic parity of final data measurements, sweep bits, and a constant. Therefore a model receiving full raw M plus sweep can compute the target directly. Such apparent accuracy is not decoding progress.

For the current proposed test, use initial ancilla tags versus bulk detector statistics only, never terminal raw data-qubit outcomes. For a later decoder, retain terminal stabilizer parities rather than raw terminal data bits. Audit the feature-to-label linear span, including sweep features and any reconstructed frames. A gauge tag is a noisy observed tag, not a ground-truth state label. State-conditioned differences also need separation from readout asymmetry, preparation noise, and any uncontrolled acquisition mixing.

## Verified incumbent interfaces

### Released Willow pathways

The publisher's README states that detection-event records are decoded to predict observable flips, and describes the DEM as the configuring prior. Its worked PyMatching command takes DEM plus detection_events, whereas M and sweep enter the upstream measurement-to-detector conversion. It lists five pathways: correlated matching and Harmony under SI1000 or RL priors, plus Libra under RL prior. Harmony and Libra use 51 members in this release. RL parameters were optimized jointly using 13-cycle d3/d5 calibration data.

This supports treating the **documented released matching pathways** as detector-plus-prior algorithms. No per-shot raw M, sweep, leakage flags, analog readout, or gauge-conditioning interface is documented for them. It does not constitute a source-code audit of Google's internal experiment wrapper, so “proved never used any other input” is too strong.

Primary source: [Google Quantum AI release](https://zenodo.org/records/13273331), archive README, locally preserved under measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/README/README.md.

### Harmony / correlated matching

[Shutty, Newman, Villalonga, 2024, §§II–III](https://arxiv.org/html/2401.12434v1): the prior is a weighted error hypergraph, implemented via Stim DetectorErrorModel. Vertices are detectors; hyperedges carry probabilities and logical flips. Correlated matching uses initial matching, reweighting from inferred correlated errors, then final matching. Harmony perturbs probabilities and implied conditional probabilities and pools outputs. Thus “static DEM prior” is accurate; “all runtime weights static” is not. Runtime reweighting can be syndrome-dependent without acquiring absolute measurement signs. The paper's tensor-network comparator also takes hypergraph plus detection events.

### Libra

[Jones, 2024, §§II–IV](https://arxiv.org/html/2408.12135v1): the problem input is a weighted hypergraph and fired-detector syndrome. Matching synthesis combines local improvements from candidate error assignments consistent with that syndrome. Its surface-code implementation uses correlated-matching ensembles with perturbed priors. No extra raw-state channel appears in this defined algorithm. This is a statement about the described implementation, not a restriction preventing future externally conditioned hypergraphs.

### Reproducible open matching comparator

[PyMatching author source](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py) exposes from_detector_error_model(..., enable_correlations=True) and decode_batch(shots, ..., enable_correlations=True). Here shots are detector/syndrome vectors; model construction and decoding both need correlations enabled. Current public correlated matching is available, but is not automatically bit-identical to Google's release implementation or an ensemble replacement. No execution performed.

## Strongest competing neural prior

### AlphaQubit (Bausch et al., Nature 2024)

[Paper and Methods](https://www.nature.com/articles/s41586-024-08148-8), especially “Soft measurement inputs versus soft event inputs”, “Input ablations”, “Soft matching”, and “Code availability”:

- Inputs include stabilizer measurements and events; simulated soft/leakage variants use measurement and leakage posteriors.
- Methods explicitly discuss the missing initial measurement frame, including random off-basis signs. Under Pauli noise they remove that initial frame.
- DEM pretraining substitutes cumulative detector parity because a DEM lacks absolute initial stabilizer states.
- Soft matching updates measurement-edge probabilities per instance; correlated matching is therefore not inherently restricted to hard information.
- Terminal soft data readouts are restricted to prevent label leakage.
- The official release provides architecture pseudocode, Pauli+ data/loading documentation, and Sycamore data links; it does not offer a published checkpoint in its availability statement.

This is direct prior against claiming novelty merely for absolute outcomes or the initial-frame information distinction. It does not establish that a particular Willow initial-tag effect is useful. The exact experimental sweep-to-input transformation is not fully verified here.

### AlphaQubit 2 (Senior et al., March 2026 version)

[Primary paper](https://arxiv.org/html/2512.07737v2), §§3.4, A.1.2, A.3.5: surface-code inputs explicitly add measurement and event embeddings. On the same 105Q Willow dataset, AQ2 reports accuracy comparable to AQ1 and better than Libra. It uses a separately fitted 13-cycle DEM for initial fine-tuning, followed by two-fold cross-validation on experimental data; each training half has 19,880 fine-tuning and 5,120 development examples. Five models are ensembled for Willow.

No authoritative checkpoint, exact per-shot prediction release, or author implementation link was verified in the paper or targeted official-source searches. Absence from this search is not proof none exists. The published comparison establishes a stronger relevant competitor, not an available paired benchmark for our exact reserved shots.

## Additional established competition

- [Pattison et al., 2021](https://arxiv.org/abs/2107.13589) explicitly develops soft-information MWPM and union-find decoders, including amplitude-damping readout models. Therefore richer/readout-conditioned information is not an ML-only or new concept. Analog side information differs from the missing hard initial frame and is not present in our acquired binary files.
- [Physical Review Applied 22, 044031 (2024)](https://doi.org/10.1103/PhysRevApplied.22.044031) experimentally compares hard/soft matching and recurrent neural decoding for a superconducting d3 bit-flip surface code. Its NN soft inputs include defect probabilities and ancilla leakage flags. This supplies an experimental soft-information comparator precedent, not a result on our full Willow surface code.
- [Sivak, Newman, Klimov, 2024](https://arxiv.org/html/2406.02700v1) optimizes decoder hypergraph priors with RL-inspired calibration targeting logical error, using small sensor codes. Its priors encode heterogeneous experimental noise; this is already represented in the acquired RL baseline. Static calibration should not be conflated with conditioning on individual-shot preparation/gauge tags.

## Availability audit and stopping conclusion

Read only the existing ZIP central-directory manifest (archive_manifest.json), not compressed shot payloads. Among 9,959 entries, prediction pathways are exactly:

- 420 correlated-matching SI1000
- 420 correlated-matching RL
- 420 Harmony SI1000
- 420 Harmony RL
- 364 Libra RL

There are no neural/alphaqubit/network/checkpoint-named entries. See availability_audit.json for the machine-readable count. This verifies no neural prediction pathway in that 105Q release archive, rather than just no neural files in our acquired condition.

Searches found third-party reproductions, including [overshiki/alphaqubit-reproduce](https://github.com/overshiki/alphaqubit-reproduce), which explicitly disclaims affiliation, and [yingli-Claire/AlphaQubit-2-](https://github.com/yingli-Claire/AlphaQubit-2-), whose README describes a small execution-test dataset and random default weights. Neither is evidence of an official trained Willow baseline or fidelity to published performance. Their code was not run.

Permissible interpretation of future evidence: an initial-tag association would justify a targeted conditional-information audit, not a decoder victory. Any subsequent SOTA claim needs a defensible AQ1/AQ2 comparison or an explicit unresolved comparator limitation, and any novelty claim needs a narrower mechanism/estimator/protocol contribution. A positive comparison solely to the five archived matching predictions must be labeled exactly that.
