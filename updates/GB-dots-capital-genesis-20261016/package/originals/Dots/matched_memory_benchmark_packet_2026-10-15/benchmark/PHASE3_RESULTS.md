# Equal nominal check-read diagnostic: three endpoints completed

The separately versioned parameter patch passed independent review before execution. Only the authorized three Toom endpoints were run: L=32, alpha=0.001, T=5, seeds 101/102/103, correction multiplier beta=4. The old source, binary and phase1/phase2 raw results remain unchanged.

Result: **1/3 decoded failures and 1/3 global-fallback readouts**. Seed 101 has logical bit mask 7 and exactly one ineligible component among 8733; seeds 102 and 103 have zero logical bits, no ineligible components and local-only readout. All three recovery-boundary and closed-residual checks passed; zero unresolved endpoints.

The existing sweep endpoints at the same L, alpha and T have 0/3 failures and 0/3 fallback. The former equal-attempt Toom endpoints have 2/3 failures and 2/3 fallback. These are descriptive counts only. For 1/3 the exact two-sided 95% binomial interval is [0.0084,0.9057]; for 0/3 it is [0,0.7076], with one-sided 95% upper bound 0.6316. The pilot cannot establish a method advantage or threshold. A single oversized/unliftable syndrome component still switches this frozen decoder to whole-syndrome H, so the one observed failure cannot be separated from the chosen recovery policy without an additional common-readout comparison. Exact diameter versus lift-failure cause is not instrumented in this frozen version.

## What is matched

Sweep vertex-attempt rate remains 1, giving 8 L^4 expected logical syndrome-bit inspections per unit time. Toom face-attempt rate is now beta/6=2/3, giving 2*(4 L^4)=8 L^4 expected inspections. Physical noise remains 0.001 per face and Toom's noise/face-attempt ratio is 0.0015. Actual inspection counts fluctuate: the three Toom endpoints record 125,826,824 total reads, versus 125,842,568 for the existing sweep trio. This matches expected nominal reads, not precise realized counts or hardware/energy/latency resources.

The patched superposition rate is L^4*(beta+6 alpha), with noise-selection probability 6 alpha/(beta+6 alpha). Their product is 6 L^4*alpha; conditional locations stay uniform. Thus the physical per-face noise rate is unchanged. The changed total proposal rate means the same seed labels do not imply identical physical-noise event records across beta settings. Do not analyze these as a common-noise paired comparison.

This experiment tests only the base ideal instantaneous-Pauli-jump model and the specified perfect final readout. It is **not** a test of a finite coherent-gate, shared-bath, engineered-reservoir or other perturbed-generator theorem. Toom remains an own Poissonized adaptation, not the primary paper's parallel schedule.

## Implementation and independent gate

The patch changes only the correction multiplier, two sampler-rate expressions, interface validation and output metadata. Geometry, local kernels, RNG, component test, local prism, global tensor recovery and scoring are unchanged. Four beta=1 deterministic regressions (default/explicit 1 under both methods) match all 22 legacy non-timing output fields. The new selftest passes all 393216 L16 single faces and the existing algebra/incremental checks. Independent review additionally passed 5150 decoder cases and 704 kernel cases, inspected the exact rate derivation and froze the binary before the run.

See simulator_equalreads.cpp, simulator_equalreads, equalreads.patch, PHASE3_SHA256 SUMS, equalreads_regression.json and PHASE3_GATE_APPROVED.txt. The face_attempt_rate field is 0 as a nonapplicable sentinel for sweep's vertex process; phase 3 contains Toom only, with rate 2/3 explicitly recorded.

## Resources and reproducibility

All three endpoints completed in 7.4801 CPU seconds and 7.4895 wall seconds, with 108,104 KiB peak RSS (105.6 MiB), below the 90 CPU-second/1 GiB cap. No timeouts or schema/invariant failures occurred. No extra beta=4 repeats or broader experiments were run.

phase3_manifest.json freezes the rates, seeds, comparison, model scope, caps and hashes. phase3_raw.jsonl preserves per-endpoint counts/timings; phase3_summary.json and phase3_resources.json provide summaries. run_phase 3.py reproduces exactly this three-endpoint grid after verifying the gate and hash, overwriting only phase 3 result files. Stop here pending a separately authorized scientific next step.
