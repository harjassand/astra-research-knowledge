# Independent measured-syndrome interface audit

## Verdict
PASS for preserved member integrity, dimensions, bit layout, all-row measurement-to-detector/observable identity, and published baseline counts. No decoder or noise-model fitting, installations, author-code execution, hardware calls, or new reserved-row statistics were performed.

Source: Google Quantum AI, *Data for “Quantum error correction below the surface code threshold”*, Zenodo 13273331, version 1.0.0, published 2024-08-26, DOI https://doi.org/10.5281/zenodo.13273331 . Dataset license CC BY 4.0; retain attribution. The preserved source README explicitly identifies measurements.b8 as actual device-collected measurements. Noisy SI1000 circuit and DEM files are model artifacts; decoder predictions are published derived outputs. Integrity/consistency checks cannot independently establish physical provenance beyond the publisher's source attribution.

## Independently reproduced checks
- All 33 preserved original members, including the source README: recomputed SHA256 matches saved acquisition hashes; recomputed CRC32 and byte lengths match a fresh direct parse of the preserved ZIP central directory. Checks cover 26,821,753 original bytes. Whole-archive MD5 remains unverified because only selected ranges were acquired. CRC and hashes verify these preserved members, not an independently signed archive.
- r50: 50,000 rows, 1,225 measurements, 1,200 detectors, 25 sweep bits, one observable. Measurement, detector, sweep, observable row strides are 154, 150, 4, 1 bytes.
- r13: 50,000 rows, 337 measurements, 312 detectors, 25 sweep bits, one observable. Row strides are 43, 39, 4, 1 bytes.
- All b8 padding is zero; bits unpack little-endian within each byte, and each row is byte aligned. Published predictions also have valid one-bit rows and zero padding.
- Fresh circuit parser identifies ordered measurement references, and propagates each sweep bit as a Pauli frame through resets, H, and CZ. Fixed X/Y gates affect the separate noiseless reference.
- A from-scratch pure-Python stabilizer simulator independently computes a valid noiseless measurement record with all sweep bits zero. It tracks full Pauli phases, updates projective measurements, and handles resets. Detector and observable offsets come solely from circuit simulation, never from experimental outcomes. Its reference parities are stable for four additional random measurement branches and, for every one of the 25 individual sweep inputs, agree with the independently propagated symbolic sweep mask, at both circuit lengths (58 circuit self-check runs).
- Using raw experimental measurement parity XOR symbolic sweep parity XOR independent noiseless reference offset gives EXACTLY the supplied detection/observable flips: zero mismatches among 75,600,000 detector bits and 100,000 observable bits across both conditions.
- The r50 observable uses zero-based measurements [1220,1215,1210,1205,1200], sweep bits [0,5,10,15,20], and noiseless offset 1. The r13 measurement indices are [332,327,322,317,312], with the same sweep support and offset.

This strengthens the acquisition's earlier constant-offset consistency check: those earlier offsets were inferred empirically; this audit derives them from the ideal circuit independently. The simulator is an independent implementation, not a formal proof or cross-package certification.

## Published baseline outputs
Recomputed full-r50 failures, prediction XOR actual:
- Libra / RL: 7,690 / 50,000 = 15.380%
- Harmony / RL: 8,011 / 50,000 = 16.022%
- Harmony / SI1000: 8,429 / 50,000 = 16.858%
- Correlated matching / RL: 8,615 / 50,000 = 17.230%
- Correlated matching / SI1000: 9,288 / 50,000 = 18.576%

These are 50-round shot failure fractions, not per-round rates. Decoders were not rerun. No neural-network outputs were acquired; the best acquired baseline is not necessarily the best decoder in the article.

Byte identities: within each condition, both SI1000 prior files are identical. All three r50 RL priors are identical; both r13 RL priors are identical. These are shared models, not distinct physical samples. Full hashes/groups and the four r13 baseline counts are in audit_results.json.

## Calibration scope
Source README says RL priors were optimized jointly for all distance-3 and distance-5 patches using 13-cycle calibration data. The acquired r13 condition is only the matched d5_at_q8_7/X subset of that calibration corpus, not the whole joint corpus and not an independent unseen test. It has four matching/Harmony outputs and no Libra output. Calibration use must be separately declared; equal patch/basis does not establish equal temporal conditions or duration transfer.

## Frozen prospective split
Before the diagnostic worker read measured detector rows, all original r50 zero-based indices were sorted by the raw SHA256 digest of ASCII `astra-willow-split-v1:` concatenated with unpadded decimal index. First 25,000 are diagnostic; remaining 25,000 are reserved. Lists retain hash order, with one decimal index and LF per line.
- diagnostic_indices.txt SHA256: 80d49493e16e51d3f2cfe8574ec3316ded74e0a51ae49865165e9def979ee2ae
- reserved_indices.txt SHA256: 3353cbe6f4b1c6ad12045e77b1e0e9d93a01e04e676007580d9f86f621abdbf0

No new model statistics may use reserved rows. All-row integrity, parity, and publisher-baseline checks are permitted. r13 is separately available for calibration. This is a prospective holdout contract, NOT retroactive blinding: acquisition had already exposed broad full-r50 descriptive summaries and published baseline performance. The split is reproducible, not a guarantee of IID samples, temporal independence, or absent acquisition leakage.

## Independent diagnostic-family structural check
Independently regenerated all 9,288 same-spatial-check temporal-bulk detector pairs with both times 1..49 and lag 2..10; these exactly match the diagnostic worker's frozen_family.json. Both DEMs match circuit detector coordinates. Each has 20,039 error instructions. For each instruction, all detector targets across all '^' decomposition separators are XORed as ONE mechanism support. Every selected pair has zero common incident error-line mechanisms in BOTH models. Thus each pair is independent under a fixed independent-Bernoulli mechanism model on either support, for arbitrary fixed probabilities. This does not establish independence under arbitrary independent physical noise or under unobserved mixtures/drift. Details: independent_dem_pair_audit.json. No experimental statistics were used for this structural audit.

## Limits and correction record
No acquisition timestamps, absolute shot cadence, guaranteed chronological row order, interleaving, rejection flags, documented postselection/inclusion rule, or physical fault labels are supplied in these condition files. Row alignment and within-shot circuit order are usable; cross-shot chronology and independent samples are not established. Adjacent detectors share raw measurement records, so their correlation alone cannot identify correlated physical faults. Classical detector observations do not determine unique physical mechanisms or quantum process norms.

This 2D superconducting-code experiment does not implement or certify a 4D toric-code theorem. Finite data do not establish uniform operator-norm hypotheses or all-subset local-stochastic bounds. Long-time/hourly burst claims are unsupported here.

The coordinating reviewer checked the 2026 Author Correction, https://www.nature.com/articles/s41586-026-10559-8.pdf (primary indexed text; direct PDF opening redirected), also indexed as PMC13171424. Its stated changes concern the repetition-code Figure 3a x-axis label and legend attribution; no surface-code dataset or decoder-metric change is stated. This audit did not independently retrieve the correction and does not broaden that review's scope. The correction's license is distinct from the dataset license.

## Reproduction artifacts
Run audit.py with the already-installed NumPy to reproduce the integrity checks, circuit maps, all-row parity tests, reference self-checks, and baseline counts. Run audit_dem_pairs.py for the independent structural-pair check. Both are original audit code and execute no publisher code. audit_results.json, r50_independent_map.json, r13_independent_map.json, reference_self_checks.json, and split_contract.json retain machine-readable details.

## Structural extension: raw readout signs and preparation/gauge mixtures
A second symbolic stabilizer implementation tracks each intrinsic projective-measurement random variable, in addition to its fixed phase and affine sweep dependence. This is circuit-only analysis; it opens no experimental b8 files.

For both circuit lengths, the first 24 syndrome readouts contain 12 intrinsically random outcomes at zero-based measurement positions [2,4,6,7,9,11,12,14,16,17,19,21]. The other 12 are determined affine functions of the 25 sweep bits. The initial random signs persist in later rounds: exactly half of all noiseless ancilla readouts depend on these signs (600 of 1,200 at r50; 156 of 312 at r13). Later syndrome rounds introduce no fresh randomness in the noiseless circuit. Final data readout introduces a further 12 independent random variables. Every annotated detector and logical observable cancels all intrinsic random variables.

Every ideal raw measurement has the form constant XOR selected sweep bits XOR selected intrinsic random signs. Exact masks are recorded for each measurement in r50_raw_reference_structure.json and r13_raw_reference_structure.json. Sweep-controlled X gates occur only in initialization, yet their affine influence can persist throughout the ancilla readouts. Cancellation in a detector does not mean the underlying physical readout state is independent of the preparation or the initial random sign.

For fixed sweep inputs, the raw measurement-to-detector linear map has rank 1,200 out of 1,225 at r50 (312 out of 337 at r13): D+sweep alone leaves 25 raw-bit degrees of freedom unresolved. Adding the actual observable label raises the rank by one and leaves 24 unresolved, corresponding in the noiseless reference to the 12 initial syndrome-sign variables and 12 additional final-readout variables. These rank counts are algebraic properties for arbitrary raw bit records, not empirical entropy estimates. The actual observable label is evaluation truth, not a decoder input.

Consequently D+sweep retains syndrome changes and known preparation configuration, but not the full absolute raw readout state or the randomly selected initial syndrome signs. Detector marginals can mix distinct preparation/readout-state contexts. A model with state-dependent physical measurement errors can create long-lag marginal detector association without establishing a non-Markovian bath or temporally correlated microscopic noise. The current fixed-DEM independence family does not distinguish those possibilities, and its nonrejection does not validate them either. No mechanism is inferred here. In experimental records, an early raw readout is itself noisy and cannot simply be equated to a known latent ideal sign. Any conditioning or stratified test would require a separate fixed protocol and must preserve the reserved split.
