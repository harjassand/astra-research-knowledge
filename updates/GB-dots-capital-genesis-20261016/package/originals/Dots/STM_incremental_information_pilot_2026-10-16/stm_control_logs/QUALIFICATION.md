# STM logged-control qualification

## Decision

**Conditional pass for a narrow, real-experiment logged-outcome evaluator. Not a counterfactual controller evaluator.** The strongest observed endpoint is terminal, STM-image-localized target error and target attainment after the *actually executed* action sequence, with manipulation count. Missing timing does not invalidate those endpoints. It does prevent time/energy/throughput claims. No controller should be ranked on unexecuted actions using this archive alone.

This is a separate Ag/Ag(111) Createc STM experiment; no STEM data, other material/device, simulator, or manufacturing-scale conclusion is mixed in.

## Primary provenance and acquisition

Chen, Aapro, Kipnis, Ilin, Liljeroth and Foster, **Precise atom manipulation through deep reinforcement learning**, Nature Communications (2022), DOI https://doi.org/10.1038/s41467-022-35149-w . Original author code/data: https://github.com/SINGROUP/Atom_manipulation_with_RL .

Pinned commit: `ace9ca3f9be401bb9c8146d0bfc2882e87141f7e`. Complete recursive tree lists 2,921 sequential episode files, `00000.npy` through `02920.npy`, totaling 2,887,698,389 bytes. Only **00000, 01500 and 02920** were acquired and inspected as diagnostics. They must be excluded from any future test set. Remaining 2,918 episodes are untouched pending a benchmark contract and split. `provenance.json` contains source URLs, SHA-256 checksums, sizes and scope. `tree.json` preserves the inventory. Source/notebook cells were read, never run; no hardware calls or model loading occurred.

The files are NumPy object-array pickle payloads. `inspect_static.py` is an original bounded symbolic interpreter: GLOBAL is an allowlisted inert token; REDUCE and BUILD only build inert nodes; no callable is resolved or invoked; unknown opcodes/globals/dtypes fail. Numerical byte strings are decoded with Python struct. Neither pickle.load nor NumPy allow_pickle is used. Large arrays are summarized, not reconstructed as author objects. `sample_decoded_summary.json` is the resulting diagnostic evidence.

## Observed data and terminal semantics

Each episode has start information, ordered lists of state/action/next_state/reward/done/info, and terminal information. Actual diagnostic records include current traces, cumulative spatial trace `d`, requested relative tip start/end, image-localized atom coordinates, target coordinates, image extent/offset, and forward/backward STM images.

- Diagnostic 00000: four actions, done `[false,false,false,true]`, terminal error 2.4956105707 nm, failure.
- Diagnostic 01500: two actions, done `[false,true]`, terminal error 0.0634223213 nm, success.
- Diagnostic 02920: one action, done `[true]`, terminal error 0.1282519994 nm, success.
- All three contain terminal forward/backward 128×128 images. Current trace sample counts are respectively `[553,722,350,609]`, `[756,585]`, and `[1296]`.

Success threshold in code is strict error < `0.288*sqrt(3)/3` nm (~0.166277 nm). `done` is **not success**: it combines max episode length, success, excessive displacement from episode start, and leaving allowed manipulation bounds. No distinct terminal-reason field is stored. Success is recomputable from final coordinate and goal without guessing terminal reason.

`Env_new.py` forces a fresh STM scan at maximum-length termination; its other done conditions are assessed only within the fresh-scan branch. The notebook stores episode-end images on done. Thus **the published implementation records freshly measured terminal imaging on every normal completed episode**; that is a source invariant verified for three diagnostics, not a claim that all 2,921 records have already passed integrity checks. Crash/interrupted runs and absent records cannot be ruled out.

## What is measured versus carried forward

`scan_atom` obtains forward/back STM images, localizes each with image processing, and averages forward/back atom coordinates. The current classifier predicts whether motion likely happened and whether to scan. It does **not** localize the atom from current. If scanning is skipped, the next-state position and image info remain the previous scan's values. Therefore intermediate repeated positions are observation carry-forwards, not proof of zero physical motion.

Image identity/equality and source branch logic can indicate reuse, but no explicit `scan_performed` or timestamp is saved. Identical newly measured images cannot universally be distinguished from reused ones. Scan-count claims therefore need further checks; manipulation counts are directly observed. Reset may reuse the preceding episode's final scan and may execute pull-back manipulations outside the logged transition list. Do not treat contiguous episode numbers as a complete stream of every hardware action.

## Action and measurement calibration

Read `Env_new.py:277–348`, `createc_control.py:134–176`, and the saved notebook text. Six normalized actions specify relative start x/y, relative end x/y, voltage fraction and conductance fraction. Example notebook scales:

- start = first two action components × 0.4 nm;
- end = next two components × 2 nm;
- bias = min(action[4],1) × 15 mV;
- setpoint = min(action[5],1) × 6000 pA/mV × bias in mV.

Nominal policy bounds imply bias 5–15 mV and conductance 3–6 μA/V. Positions are added to the last observed absolute atom position, clipped to manipulation limits, then mapped to image pixels. Stored `start_nm/end_nm` are **pre-addition/pre-clipping relative requests**, not guaranteed executed absolute endpoints. Controller rounds/maps to pixel coordinates; current and spatial trace are acquired using Createc ampere/nanometer channels. The full time/x/y/topography tuple exists at controller level, but the environment retains only current and radial displacement `d`.

Important remaining calibration gaps: per-run voltage/conductance scale declarations, clipping limits and hardware gain/piezo calibration history are not stored in each episode; three diagnostics corroborate 0.4/2 nm spatial action scales, but one current notebook is not a run-by-run calibration certificate. Image extent changes from ~10.027 nm (00000) to ~6.956 nm (later samples), demonstrating nonconstant acquisition settings. The source-implied current unit is A, with no instrument calibration uncertainty certificate. No per-sample time, sampling rate or manipulation duration is retained. Forward/back localization disagreement should be explicitly audited as uncertainty rather than silently equated with sub-lattice ground-truth accuracy.

## Strongest same-device incumbent and split

The paper's serious experimentally evaluated incumbent is the manually tuned constant-parameter manipulation: **10 mV, 60 nA (6 μA/V), drag from atom toward target with 0.1 nm overshoot**. `baseline_eval.ipynb` implements it. It was compared under three tip conditions against DRL continuing to train; the publication reports fixed-baseline success rates 92%, 100%, and 68% under those conditions. This is a materially credible same-device comparator, not a simulator.

The repository includes baseline evaluation code but no separately identified baseline episode-log collection in the recursive tree. A notebook references a local `Ag_baseline_3` directory, not public baseline files. The publication's training curves and 100-episode windows are not a frozen episode-held-out predictive evaluation. No author-supplied training/test episode split or exact tip-change-to-episode annotation was found. Preserve this absence: do not relabel training episodes as an independent evaluation or claim offline superiority over the physical baseline.

## Exact narrower interface and qualification gate

1. **Available now:** provenance-preserving episode audit: sequence length; terminal goal/position/error; strict target-attainment label; terminal image presence; current/spatial trace availability; done versus success distinction. Use the three diagnostics only to validate the reader and schema. This audits recorded outcomes and experimental data quality.
2. **Possible after contract/split:** predict a *held-out logged endpoint* or its calibrated uncertainty from only pre-terminal observations and executed actions. The terminal image/coordinates/error/reward/done are labels or audit fields, never predictive input. If predicting before an entire sequence, later actions may themselves leak adaptive observations; prefer a precisely timed last-action-to-next-measured-image task. Split whole episodes chronologically, separating adjacent shared images and accounting for tip regime. Do not allow transition-level random splits or hindsight-relabeled samples to leak across folds.
3. **Incumbents for that predictive task remain to establish:** no-motion/last-measured-position persistence and commanded-endpoint kinematics are transparent physical baselines; a fitted action-conditioned model is a useful strong statistical comparator only after a disjoint training contract. The published current CNN/empirical jump detector is appropriate for binary motion detection, not demonstrated endpoint prediction. Do not present any of these as already evaluated. The fixed-parameter hardware policy remains the physical-control incumbent, but its counterfactual outcomes cannot be recovered here.
4. **Missing for a complete policy benchmark:** paired or suitably identified incumbent logs, behavior-policy probabilities/support and a justified off-policy design, run-specific calibrations and clipping bounds, clean tip/session regime metadata, and explicit measurement freshness. Missing timing blocks seconds/energy cost, not per-record action-count endpoints.

**Stopping condition:** the archive contains real usable logged outcomes, so it is not rejected as weights/figures-only. Acquisition stops at diagnostic qualification; no full archive ingestion, training, held-out scoring, unsafe deserialization or hardware execution is authorized by this report. The next decision is the narrow benchmark contract and split, not another search across devices.

## Addendum: leakage-safe pre-scan information task

The proposed task is supported **conditionally on identifiable, already-triggered scans**. At each such boundary, predict measured target attainment, displacement since the last measured position, and/or calibrated uncertainty *after manipulation and current acquisition but before the next STM image*. This tests inference from observed control/current data, not policy value and not experimentally demonstrated scan savings.

**Observation timing and fields:** `step` obtains `current_series` immediately after executing the action, then decides whether to scan, then records localized coordinates and images. Thus a scan-triggered row contains both the action/current information available before imaging and the image-derived answer afterward. Previous-measurement coordinates, target, preceding action history since that measurement, and current traces are eligible inputs. Goal is fixed at reset. If scans were skipped earlier, retain all actions/traces since the previous measured image; do not turn carried-forward coordinates into movement labels.

**Freshness evidence:** there is no explicit scan flag or timestamp. However, the original serialization preserves object identity. The environment constructs new forward/back image arrays during each scan and otherwise reuses the last pair. The inert symbolic parser retains those identities without executing pickle callbacks. `audit_scan_provenance.py` checks both identity and byte hashes. Its diagnostic findings:

- 00000: transition indices 0, 1 and 3 have new image objects with changed bytes; index 2 reuses both prior image objects and bytes.
- 01500: both transitions have new changed image pairs.
- 02920: its sole transition has a new changed image pair.
- Every diagnostic has a current trace at each of those fresh-image boundaries; every terminal image pair references the last transition's image pair.

This is stronger than judging freshness from coordinate changes: an atom can stay still in a genuinely new image. Require both forward/back objects to be new, confirm compatible schema/source lineage, and reject mixed/reused/ambiguous cases from fresh-scan labels. Image-byte changes support that inference. Neither different object identity nor byte changes alone is a universal timestamp certificate if historical logging code copied arrays; source-version compatibility still needs qualification on the fixed split. The parser can expose provenance IDs to a separate auditor without exposing label-bearing images to the predictor.

**Strict feature firewall:** rewards, done flags, next/post-scan coordinates, post-scan distance, current/future images, terminal data, future actions, future episode length and image-freshness identifiers are labels/audit metadata, never model features. Do not supply current `info` wholesale. Derive eligible pre-state from the latest prior measured state, not the current row's post-scan coordinates. Use only action/trace prefix available at the prediction moment. Outcome-dependent last-row selection is disallowed; include all identifiable already-triggered scan boundaries under the fixed contract.

**Split:** burn 00000/01500/02920. Fix chronological episode-disjoint train/development/test IDs before any additional outcome access. Group/deduplicate shared start/end images and prevent inherited images crossing train/test boundaries; guard neighboring episodes and regime changes. Serialize the feature whitelist and split as an immutable manifest. No training or test scoring has happened.

**Comparison and limits:** for target/displacement prediction, last-measured-position persistence and commanded-endpoint kinematics are mandatory transparent baselines; an action-only model versus action+current model directly tests the current signal's incremental information. A properly trained strong nonlinear action/current regressor/classifier and uncertainty calibration baseline must then be fitted only on the training/development split. The study's learned CNN and empirical current-spike detector are experimentally grounded incumbents for *motion detection*, not endpoint regression or target-attainment calibration; they cannot silently substitute for a matched endpoint comparator. The same-device fixed-parameter policy remains the control incumbent but cannot be scored counterfactually here.

Because scan selection depends on the classifier, empirical current features, randomness and episode-length limits, the observed scan subset is selected. Claims apply to that observed subset; the archive does not directly label missed motions during skipped scans, identify a prospective reduced-scan policy, prove actual saved scans, or establish safety. This restriction preserves a meaningful information-acquisition test without pretending the missing observations were measured.
