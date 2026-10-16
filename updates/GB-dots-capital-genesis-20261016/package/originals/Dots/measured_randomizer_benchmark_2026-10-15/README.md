# Measured randomized-control benchmark

## Result

**Use Ware et al., _Experimental Pauli-frame randomization on a superconducting qubit_, PRA 103, 042604 (2021), as the strongest openly obtainable matched randomized-control foothold found here.** Its released counts support a reproducible comparison of randomized and unrandomized implementations of the same logical circuits with the same physical pulse budget. It does **not** measure the cost/benefit of adding more physical randomizer pulses at fixed task duration.

- [Primary paper](https://arxiv.org/abs/1803.01818), [published DOI](https://doi.org/10.1103/PhysRevA.103.042604)
- [Primary dataset release, Zenodo v1.2](https://zenodo.org/records/4609459)
- [Pinned source/data repository](https://github.com/matthewware/RGST-analysis/tree/9afedca174dbcb14d52c245cf7504a834816fc39)

All acquisition was public and read-only. No author software was run, no dependencies installed, no accounts created, and no contact made. `validate_counts.py` is newly written standard-library-only parsing/arithmetic, not a re-execution of the author's analysis.

## Physical and acquisition contract

The paper describes one fixed-frequency superconducting transmon. Every Clifford uses two 50 ns physical X(pi/2) pulses and up to three virtual Z-frame updates. Random Paulis are merged with adjacent Cliffords, leaving circuit duration unchanged. This changes driven rotation phases; it is more than measurement relabeling, but adds no physical pulses.

Ten single-shot randomized variants alternate with ten baseline shots, repeated 100 times. Seven full runs take about one hour each, with initial calibration. This deliberate interleaving mitigates drift; aggregate release files cannot establish shot-level stationarity or remove arbitrary drift confounding.

The published incumbent uses long-sequence GST, testing a saturated per-sequence binomial model against fixed-operation and Clifford-plus-stochastic-Pauli models. Its reported noise-shaping and reconstructed diamond-distance improvements are stronger analyses than the descriptive return-count audit below. Those fits do not identify a joint system–bath norm or certify a CP fault-process bound.

Source: paper sections III–V. The physical implementation is paper-reported; exact acquisition waveforms, pulse calibrations, full shot timing and actual randomized Clifford-index files are absent from this data release.

## Downloaded count contract

`rgst/data/` contains all fourteen small experimental text-count files: `gst_1.gst` through `gst_7.gst` and matching `rgst_*` files. Each has 3,505 ordered nominal circuit keys, two nonnegative integer counts, and exactly 1,000 outcomes per circuit. All fourteen key lists and ordering match. Total released outcomes represented: 49,070,000. Header order is `minus count, plus count`.

These are nominal logical gate strings plus aggregate counts, not exact randomized pulse sequences. Pair by `(run number, exact nominal key)`. File ordering is not a timestamp or shot-order record.

### Randomness interface

The author's `notebooks/Randomize.ipynb` explicitly says 1,000 precompiled randomized variants were generated, each sequence measured once in each of seven runs; baseline sequences were measured 1,000 times. Thus it is one shot per variant within a run, with a finite compiled ensemble reused across runs according to the notebook. It is not the usual many-shots-per-variant design, nor is online fresh private randomness demonstrated.

`pauli_rand_clifford_circuit` in `rgst/scripts/rand/randomize.jl` samples Paulis while compiling, tracks their propagation, and folds a final correction into the last Clifford (allowing an I or Z residual invisible to computational-basis measurement). The executable example sets `srand(0xcafe)`, described as useful for testing. That seed is not verified as the acquisition seed. No released mapping connects actual seeds/variants to measured shots.

Counts average away variant identity, individual outcome order, block order and bath history. Privacy/unpredictability of randomization from the bath is unmeasured. A theorem requiring expectation over fresh private frames therefore needs an additional experimental interface argument; this is a scope fact, not a criticism of the experiment.

### Gate/outcome conventions and length audit

The Dockerfile pins pyGSTi v0.9.3. Its `std1Q_XYI.py`, retained as text, defines Gi=I, Gx=X(pi/2), Gy=Y(pi/2), preparation `0`, plus effect `1`, minus the remainder. Therefore **minus is the ideal return-to-|0> label** for Gx/Gy powers divisible by four and every Gi power.

The maximum expanded released key length is 1,030 Cliffords. Example: `GyGyGy(Gy)^1024GyGyGy` has 3 + 1,024 + 3 gates. A length-six germ occurs as `(GxGxGyGxGyGy)^170`, with 1,020 body gates. The author notebook sets `germ_power=1024`, then its generator calls `make_lsgst_experiment_list` with `maxLengthList` and no truncation override. The retained pyGSTi v0.9.3 implementation defaults to `whole germ powers`: total repeated-germ length <= L. Its separate `length as exponent` option would have different semantics. This independently supports the parser's released-file contract.

The paper describes lengths up to 6,155. That coverage difference is unreconciled; the present evaluator claims only the verified released lengths, not that the paper is wrong. The special `{}` sentinel is excluded from physical-pulse inference because the example parser maps it to an identity sentinel whose physical handling is not supplied.

## Public diatomic compiler source, with version boundary

A matching implementation from the paper-cited [BBN-Q/QGL.jl repository](https://github.com/BBN-Q/QGL.jl/tree/70e66d76f2e5f518ff2d8b78bc93b65779182c9f) is retained in `qgl_source/`, pinned to commit `70e66d76f2e5f518ff2d8b78bc93b65779182c9f` (2018-04-27). The paper cites master August2016; the repository API returned no commit at/before that date. **This source matches the described construction but is not authenticated as the exact acquisition revision.**

- `src/pulses.jl`, `DiAC(q::Qubit,num)`, lines170–202: all24 Clifford angle triples and temporal sequence Z(alpha), X90, Z(beta), X90, Z(gamma). `diatomic_angles.csv` is a literal numeric extraction of its table, with the source factor0.5 applied.
- `X90` uses the channel's `pi2Amp` and pulse `length`, with phase0. `Y90` phase is0.25 and X90m phase0.5. `ZPulse` has duration0. The actual calibrated channel settings are not in this experiment release.
- `src/GSTsequences.jl`, `create_1Q_GST_seqs` and `create_1Q_GST10_seqs`: numerical Clifford indices map to `DiAC`. Index0 is separately mapped to a null Id with default length0. The latter routine repeats baseline sequences ten times, consistent with block acquisition. The null sentinel therefore needs special handling and is not part of the return-power comparison.
- `src/APS2.jl`, lines145–146: the physical waveform is phase-shifted by exp(i2*pi*phase), so phases are turns. Lines281–284 translate a Z angle to hardware `UPDATE_FRAME` using `mod(-angle,1)` quantized to28bits. Preserve this sign convention in any proposed control-error model.

This establishes a concrete compiler interface for a later bounded calculation. It does not determine measured amplitude/detuning-error distributions or whether the data's gains arise from those errors versus ambient noise. No such mechanism fit was attempted.

## Independently executable descriptive comparison

Before evaluating the expanded selection, `selection_rule.json` recorded: every exact bare pure Gx/Gy power divisible by four, and every exact bare Gi power, all seven runs. Earlier inspected examples are explicitly listed there. This is an **exploratory existing-dataset check**, with no untouched holdout or prospective preregistration claim.

- `all_pure_power_return_counts.csv`: 27 exact keys × 7 paired runs = 189 rows; both source outcome counts, pulse counts, and paired return differences.
- `all_pure_power_return_summary.csv`: every selected length, seven-run arithmetic means and ranges. No fit or significance test.
- `pure_power_selection_validation.json`: exact selected keys and conventions.
- Gx and Gy lengths: **4, 16, 32, 64, 128, 256, 512, 1024**. Length4 is a literal four-token key; exact bare length8 keys are absent. No fiducial-padded substitutes were included.
- Gi lengths: **1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024**.

For example, mean return probability at Gx32 is 0.3853 baseline versus 0.7230 randomized, and at Gy32 is 0.3780 versus 0.7160. At Gi128 it is 0.7156 versus 0.5490. The full export shows both gains and losses; long X/Y powers are near 0.5 in both arms. These are observed finite-sample fractions, not corrected fidelities or mechanism estimates.

For each nonempty n-gate sequence the paper implies **2n physical pulses in each arm**, with 0.1n microseconds of active pulse duration. This derived active duration excludes reset, readout, scheduling overhead and any unreported gaps. Equal pulse budget does not make pulse errors ideal. In particular, poorer Gi return is not evidence of the cost of *additional* pulses: both arms have the same count. Changing n changes task duration/depth, not independently the randomizer rate.

Reproduce the audit with `python validate_counts.py` from this directory. This script reads data and writes the small validation/CSV products only. The earlier four-row-family `direct_count_examples.csv` is retained for audit history, not used as a selected benchmark score.

## Incumbent analysis and data splits

The reproducible scientific comparator is the authors' GST analysis, not a fitted model invented here. The repository supplies `notebooks/RGST_analysis.ipynb`, precomputed `.npz` reconstructions and `.pkl` results. They were not downloaded/executed for this task. The retained `scripts/gst-1q-with-ci.py` fits its full input dataset with `do_long_sequence_gst`, then constructs Hessian-based confidence regions. No explicit held-out split is present in that inspected fitting pipeline. The seven run IDs are experimental repetitions, not declared train/test partitions.

A future model should preserve complete runs and circuit families when constructing a new split, disclose any data already inspected, and score held-out raw counts rather than only reproducing in-sample gate estimates. No such fit or split is claimed here. Neither stored aggregate counts nor interleaving alone permit a retrospective time-resolved bath-memory analysis.

## Secondary physical-pulse-cost baseline: deterministic IBM DD

[Ezzell et al., _Dynamical decoupling for superconducting qubits: a performance survey_](https://arxiv.org/abs/2207.03670) and its [public source/data](https://github.com/naezzell/edd/tree/fc72448880fa6132ffd09a9f15297306c9cd791e) provide an accessible physical DD comparison, including spacing sweeps and free-evolution baselines. The controls are deterministic DD; random Haar/Pauli **input states are not randomized control frames**. Keep this as a competitive pulse-cost reference, never combine its calibration with Ware to manufacture a device model.

`edd_subset/` retains one Armonk asymmetric XY4 long-duration acquisition condition: two jobs containing eight delay settings × 25 input states, plus the matching free-evolution job, calibration text and submission notebook. Raw result counts have 8,192 shots per circuit. The archive's submit-name prefix is shared, but actual job timestamps are:

- XY4 job1: 2022-04-07 06:53:04−07:00, ID `624ed1b2a5d4ee2c7b77ce6f`
- XY4 job2: 2022-04-07 08:04:39−07:00, ID `624ed1c7cfe45c0123e5a4b8`
- Free baseline: 2022-04-07 09:59:38−07:00, ID `624ed21a4b51529fd07c6c4a`

They are hours apart, so metadata do **not** establish drift-free paired acquisition. No comparison estimate is fitted here. Physical X/Y pulse construction is in `source/edd_pulse.py.txt`; the retained calibration gives X and sx lengths 71.111 ns and virtual rz length0.

There is also an exact-timing verification gap. In the archived submission notebook, `generate_schedules` computes a residual padding `T_diff` but calls `sched.add_pause(...)` on the scratch schedule rather than `seq_sched` that is submitted (both duplicated definitions). Static source inspection alone cannot prove which code actually generated the acquisition. Exact released pulse schedules would be needed before treating this extracted condition as independently verified equal-wall-clock timing.

## What remains missing for the requested added-randomizer-cost test

A single acquisition must vary actual physical randomizer pulse count/rate while holding the logical task and elapsed evolution time fixed, including zero-added-control and a strong deterministic-DD baseline. It must publish executed pulse/phase schedules, pulse widths and gaps, shot-level outcomes with timestamps and frame/seed bookkeeping, acquisition interleaving, repeated calibration blocks, and the randomization visibility assumption. It must cover enough rates to see net benefit and any turnover under real control errors. Gate infidelity by itself cannot supply the joint bath-norm/CP fault model.

The strongest extra randomized-DD hardware lead checked was [Will et al., Nature2025, Extended Data Fig.2](https://doi.org/10.1038/s41586-025-09456-3): physical random XX/YY pairs and a no-DD comparison. Its [Zenodo record](https://zenodo.org/records/15837492) is restricted/on-request, and the indicated experiment is not a published rate sweep. No restricted files were requested or accessed. The already-known phase-burst echo experiment and fixed Willow circuits were not counted as new randomizer interventions.

## Provenance and licensing

`provenance.json` lists retained files, hashes, original URLs and extraction/derivation status. Ware data/source and EDD source are under their retained Apache2.0 licenses. The small pyGSTi v0.9.3 convention/semantics source files are GPLv3-or-later, with the upstream license notice retained. These source excerpts are for reading; no combined executable package is created.

Only a bounded EDD condition is retained; the 22.75 MB source archive was used to extract those members and its original SHA256 is recorded in `edd_subset/extraction_manifest.json`. Source snapshots are pinned to commits or tags. Claims about unavailable schedules refer to the inspected release, not all possible author-held records.
