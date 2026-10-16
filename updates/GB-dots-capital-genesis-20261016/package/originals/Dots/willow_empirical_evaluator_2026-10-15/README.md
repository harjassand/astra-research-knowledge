# Willow empirical evaluator packet

## What this delivers
An authentic, runnable measurement interface for Google Quantum AI's 105Q Willow patch d5_at_q8_7, logical basis X: 50,000 50-round evaluation shots and the matched 50,000-shot 13-round calibration subset. Original selected publisher files are preserved byte-for-byte. This is an evaluator and reproducibility package, not a new decoder, a decoder advantage, a causal discovery, or a hardware theorem.

### Results at a glance
- Independent circuit/reference reconstruction exactly reproduces all 75.6 million supplied detector bits and 100,000 observable bits across both conditions.
- Five published r50 baselines reproduce; Libra/RL is strongest **among acquired predictions**, with 7,690 failures / 50,000 shots. AlphaQubit 2 is a stronger relevant published Willow comparator; authoritative matching checkpoints/per-shot predictions were not verified available here. No SOTA comparison is possible from this packet alone.
- A fixed 9,288-pair structural-DEM independence diagnostic, using only the diagnostic half, has 0 rejections at its prespecified 1% familywise threshold (minimum adjusted p 0.0131265). Nonrejection does not validate independence or the full model.
- Calibration-only initial-tag tests show 80/264 adjusted associations. The necessary control-design qualification is substantial: only ten distinct preparation strings, repeated 5,000 times each; finite-support parity aliases prevent causal identification of a specific preparation feature. Read CONTROL_DESIGN_AUDIT.md alongside those results.
- The missing initial syndrome frame is real, but raw-state inputs, soft decoding, adaptive ancilla mapping, and physical-feedback-versus-frame distinctions have prior art. No novelty or net hardware benefit is established.

## Start here
1. Read this README, HANDOFF.md, and LICENSES_AND_PROVENANCE.md.
2. Read measured_syndrome_audit/REPORT.md for exact bit layout, independent reference checks, frozen split, and raw-state information loss.
3. Read measured_noise_independence/REPORT.md for the fixed diagnostic result.
4. Read calibration_state_response/REPORT.md **together with** CONTROL_DESIGN_AUDIT.md and the source clarification below.
5. Read raw_state_decoder_prior_art/REPORT.md and PHYSICAL_CONTROL_PRIOR.md before interpreting an input or feedback idea as new.

## Read-only replay
Supported/tested environment: Python 3.12 on Linux, NumPy 2.3.5, SciPy 1.17.0. The statistics scripts use the Unix resource module; Windows requires a Linux environment such as WSL. No publisher analysis code is needed or executed. No network access is needed. Dependencies are listed in requirements.txt; the runner does not install anything.

From this extracted directory run:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python replay.py

The runner first checks the complete manifest, copies the packet to a disposable temporary directory, reproduces six analyses there, compares saved scientific outputs, verifies original data remained unchanged, rechecks the source packet, and deletes temporary output. It reads all rows solely for the permitted measurement/parity/integrity/published-baseline audit; its new diagnostic statistics read only frozen diagnostic rows, while calibration scripts read r13. No new reserved-half statistics are computed. It needs roughly 50 MB disk for a temporary copy; peak analysis memory is below 1 GiB. It does not train a decoder or perform a reserved confirmation test.

Actual recorded replay status is in REPLAY_STATUS.txt. Scripts are portable adapted copies; PORTABILITY_CHANGES.json records hashes and precise changes. Original research workspace files were not modified. Run through replay.py: running component scripts directly overwrites their output files beside the script.

## Holdout and leakage
The diagnostic/reserved split is frozen, deterministic, and exact. Prior broad full-dataset summaries and published baseline counts existed before the split, so this is prospective reservation, not pristine retroactive blinding. See HANDOFF.md for the exact split contract. Reserved labels are retained only inside the byte-identical original source streams, and must not be used to choose models or hypotheses.

Full raw measurements plus sweep bits directly determine the target observable flip through a final-data parity. Giving a decoder those raw terminal data bits would leak the answer. Initial ancilla tags and terminal stabilizer parities are different inputs; every future feature set needs an explicit target-span audit.

## Source clarification and interpretation hierarchy
The matched r13 subset is not the complete joint d3/d5 RL calibration corpus, and is not an unseen test. The publisher README does not describe sweep selection, but the Willow supplementary information §V/Fig. S12 does: five random bitstrings and their complements, 5,000 repetitions each. Thus the control audit's statement that selection is undocumented refers specifically to the supplied README; the physical-control prior-art report supplies the broader source. Neither source establishes acquisition chronology, per-shot randomization/interleaving, absent rejection, or causal identification. File-index contiguity is not proof of drift.

The 2026 Author Correction concerns repetition-code Figure 3a labeling/legend attribution, with no stated surface-code dataset or decoder-metric change; see the audit report's scoped source note. No correction PDF is redistributed.

The packet contains binary **measurement data** (.b8), which are indispensable original inputs. It contains no executables, compiled libraries, unused archive blobs, private notes, credentials, or downloaded paper PDFs. Saved research reports may retain original analysis-time hashes/provenance; the root manifest governs this portable packet, and portable code hashes differ as documented.
