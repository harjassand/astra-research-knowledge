# Authentic measured syndrome acquisition

## Result
Acquired actual experimental Willow device measurements, not simulated samples, for Google 105Q surface-code patch `d5_at_q8_7`, logical basis label X, 50 QEC rounds, 50,000 shots. Preserved the original member bytes and names in `data/`. The full 5.7 GB ZIP was never downloaded. Every extracted member passed ZIP CRC32 and uncompressed-length validation; SHA-256 hashes are in `SHA256SUMS.json`.

Source dataset: https://zenodo.org/records/13273331 (DOI 10.5281/zenodo.13273331), published 2024-08-26, version 1.0.0, Google Quantum AI. Record metadata states CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . Attribution must accompany reuse. Publisher: https://www.nature.com/articles/s41586-024-08449-y . Record metadata is preserved. The release archive has declared MD5 `21fa6ad35b395d838ebcdbc92e364a12`; the whole-archive MD5 is NOT independently verified because only byte ranges were acquired.

## Preserved condition files
- `measurements.b8`: physical device measurement outcomes; 1,225 bits/shot, 154 bytes/shot. First 1,200 measurements are 50 ordered groups of 24 syndrome measurements; final 25 are destructive data measurements.
- `sweep_bits.b8`: 25 initialization configuration bits/shot, 4 bytes/shot; random preparation pattern, not syndrome or noise samples.
- `detection_events.b8`: 1,200 detectors/shot, 150 bytes/shot. Initial 12 boundary detectors, 49 full groups of 24, final 12 boundary detectors.
- `obs_flips_actual.b8`: one actual observable-flip bit/shot, byte-aligned, compared with the noiseless circuit's observable for that sweep configuration.
- `circuit_ideal.stim`: full expanded circuit, measurement ordering, detector references, observable parity, and coordinates.
- `circuit_noisy_si1000.stim`: explicitly MODEL-generated noise prescription; not empirical shots. Keep distinct from measurements.
- `metadata.json`: basis X, distance 5, 50 rounds, 50,000 shots, physical data/check coordinates. No timestamps or rejection flags.
- Five `decoding_results/*/obs_flips_predicted.b8` files and corresponding prior `error_model.dem` files: publisher-supplied predictions, not independently rerun decoders. DEMs are model/optimized priors, not measured fault trajectories.

All b8 files use little-endian bit order within bytes, each shot padded to a byte boundary. Row i aligns across files; chronological acquisition ordering and wall-clock gaps are NOT documented. All expected lengths and padding bits were checked. The supplied README documents formats and physical provenance. The X basis label is an arbitrary designation for the XZZX code; circuit annotations define the protected operator exactly.

## Independent consistency checks and untouched evaluator
No author software was installed or executed. Own standard-library ZIP parser and NumPy algebra only. `validate.py` parses circuit measurement indices and propagates sweep Pauli frames. `measurement_detector_observable_map.json` exposes every exact record index and sweep dependency. For each of all 1,200 detectors plus the observable, raw parity XOR propagated sweep parity XOR supplied actual flip is constant across 50,000 rows. These constant noiseless offsets are empirically inferred consistency checks, NOT an independently simulated noiseless reference. Do not train a decoder on them; the original circuit remains the normative definition.

The observable uses zero-based measurement indices [1220,1215,1210,1205,1200], sweep indices [0,5,10,15,20], and checked constant offset 1. Its physical data-qubit support follows the preserved coordinate map. A logical failure is actual flip XOR predicted flip. No decoder tuning, model selection, or fitting was performed. Original 50-round files remain byte-for-byte unchanged. Baseline-count and basic syndrome diagnostics are already exposed; treat this as an untouched evaluator for future fitting, but do not claim that these summary diagnostics were never inspected.

Baseline logical failures on these same 50,000 shots:
- Libra, RL optimized prior: 7,690 (15.380%)
- Harmony, RL optimized prior: 8,011 (16.022%)
- Harmony, SI1000 prior: 8,429 (16.858%)
- Correlated matching, RL optimized prior: 8,615 (17.230%)
- Correlated matching, SI1000 prior: 9,288 (18.576%)

These are 50-round shot failure probabilities, NOT per-round error rates. Harmony and Libra each ensemble 51 correlated-matching decoders according to the release README. Neural-network predictions are not present in this condition. Thus Libra is the strongest acquired baseline here, not a claim about the strongest decoder in the article. `validation_results.json` includes all pairwise output disagreement counts.

## Calibration subset
Also acquired the exact same device/patch/basis at r13. The source README explicitly calls 13-cycle data calibration data and says RL weights were optimized jointly for all d3 and d5 patches using it. The matched r13 condition is therefore a subset of the authors' stated calibration corpus, not an independent test and not the complete joint optimization corpus. It contains four matching/Harmony outputs; no Libra output is provided there. Calibration and evaluation differ in duration; generalization to r50 needs a predeclared protocol. Complete lineage, sample-selection provenance, and randomization chronology are unavailable.

## Limits for memory-noise and burst studies
Within-shot round order and detector geometry are explicit; temporal/spatial syndrome clusters and paired decoder decisions can be evaluated. No timestamps, absolute shot cadence, cross-condition interleaving, rejected-shot record, or documented inclusion/selection rule is supplied. Do not assume unpostselected acquisition, chronological row order, independent shots, or an unbroken memory run. No physical fault labels are supplied. Neighboring detection events share measurement records; even independent physical measurement faults create adjacent detector pairs. Observed detector correlation alone is not correlated physical noise.

This is a 2D superconducting-code experiment, not a 4D implementation. No finite-sample count establishes uniform operator-norm noise guarantees, all-subset local stochastic bounds, or transfer of a 4D toric-code theorem. Long-time/hourly burst claims require a different time-resolved dataset. No hardware jobs, outreach, spending, installs, or author-code execution occurred.

## Verified bounded acquisition totals
Downloaded HTTP range response bodies: 15,073,509 bytes, including tail, directory, local headers and compressed member data. Extracted publisher member bytes: 26,821,753. Calibration has 337 measurement bits, 312 detectors, 25 sweep bits, one observable and 50,000 rows; all lengths, padding and parity consistency checks passed.

## Intentional prior duplicates
Within each condition, SI1000 DEM bytes are identical across correlated matching and Harmony; RL-optimized DEM bytes are identical across correlated matching, Harmony, and (where present) Libra. These are shared-prior files, not additional independent evidence or duplicate experimental shot batches. `duplicate_dem_groups.json` records the exact hash groups.
