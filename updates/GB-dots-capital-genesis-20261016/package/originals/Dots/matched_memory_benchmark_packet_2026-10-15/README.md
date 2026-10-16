# Matched memory benchmark and readout sensitivity

The selected Toom endpoint's decoded outcome changes from failure mask 7 under D0 to success mask 0 under both D1 and D2, using the IDENTICAL saved error/syndrome endpoint. D1 keeps the original strict local cutoff. The selected sweep endpoint remains mask 0 under all three policies.

This demonstrates readout-policy sensitivity of this selected comparison. It does not establish which dynamics is better, an unbiased failure rate, a threshold, exponential lifetime or irreversible information loss. Phase 4 was selected after a failure was observed; its alternative syndrome-only policies were fixed before replay. Do not pool its outcomes into the earlier failure samples.

## Four phases

- Phase 1: L16, equal correction-attempt intensity, three independent seeds per positive noise ratio plus zero-noise checks. Global fallback dominated the positive-noise readouts.
- Phase 2: L32 with the unchanged original binary/readout. At α=0.001, sweep had 0/3 failures and equal-attempt Toom 2/3; at α=0.01 both had 3/3. These tiny samples do not establish a ranking.
- Phase 3: separately versioned Toom rate multiplier β=4, matching expected nominal syndrome-bit reads. It had 1/3 failures; the previously sampled sweep trio had 0/3. Same seed labels across β settings are not identical noise histories.
- Phase 4: the selected L32, α=0.001, T=5, seed=101 sweep β=1 and Toom β=4 trajectories were replayed and persisted. Alternative recoveries received S only, then E was used solely for scoring. All legacy nontiming outputs matched before the alternative readouts.

Read benchmark/PILOT_RESULTS.md, PHASE2_RESULTS.md, PHASE3_RESULTS.md and PHASE4_RESULTS.md for the full results, CIs, caps and predeclared continuation rules. Raw results and manifests are retained exactly.

## Exact normalization

κ=1. Phases 1–2 match total attempted updates L⁴: sweep rate 1 per vertex and Toom rate 1/6 per face. Sweep inspects eight logical syndrome bits per attempt and Toom two, so this is not equal expected check-read cost. Phase 3 uses Toom β=4, face-attempt rate 2/3, giving 8L⁴ expected inspections for both methods. These are algorithmic logical reads, not hardware time, energy or bandwidth equivalence. Physical noise remains α per face; the sampler's total noise intensity is 6L⁴α regardless of β.

For n=3, exact two-sided 95% Clopper–Pearson intervals include 0/3: [0,0.7076], 1/3: [0.0084,0.9057], 2/3: [0.0943,0.9916] and 3/3: [0.2924,1]. The one-sided 95% upper bound for 0/3 is 0.6316. Full precision is preserved in saved summaries. Paired methods/selected endpoints must not be pooled as independent trials.

## What changed in the selected endpoint

D0 discards all partial local fills when any component fails its strict lift/diameter test, then applies tensor fallback H to the whole syndrome. D1 preserves the SAME strict local fills and applies H only to the combined unresolved syndrome. D2 permits consistent injective lifted boxes with every coordinate span <L before using combined fallback.

The lone D0-ineligible Toom component has 16 edges, 15 vertices, a consistent lift and spans [1,1,2,4]. Strict diameter <L/8 excludes equality at 4. It is a small width-4 component, not macroscopic winding. D1 succeeds without relaxing that cutoff; D2 accepts its injective box. This diagnosis concerns the selected endpoint and specified recovery choices.

## Scope

This is an independently written one-CSS-sector ideal instantaneous Pauli trajectory simulation with perfect final readout. The Toom comparison is an own matched POISSONIZED adaptation, not reproduction of the published parallel experiment. It is not an empirical test of the separate finite-coherent-gate, shared-bath, qualified-core or perturbed-generator theorems. No hardware, population ranking or useful threshold claim follows.

## Safe analysis replay

The default packet replay verifies SAVED data only:

    python3 verify_manifest.py
    python3 replay_analysis.py

It checks historical source hashes, all exact endpoint/recovery hashes, boundary(E)=S, boundary(R)=S, closed residuals and homology at cuts 0,1,31; it also recomputes phase counts and CIs from saved raw records. It launches no trajectories, compiles nothing, selects no new recovery, writes no archived data, accesses no network and requires only Python's standard library. Assertions must remain enabled.

The analysis imports only the pure functions in benchmark/independent_audit.py. It never runs the archived experiment runners or executable-dependent tests. Its saved results are in verification/.

## Archived reproduction recipes and source versions

benchmark/ contains all three independently authored simulator .cpp versions, the deterministic readout harness, own audit/check/runner scripts, patches, frozen review-gate records and every phase's saved JSON/JSONL. Original source hashes and exact phase4 endpoint/recovery hashes are preserved. Machine executables and Python bytecode are deliberately absent. Historical binary hashes attest to the original runs; they are reported as intentionally unavailable, not falsely checked. Rebuilt binaries can have different hashes.

benchmark/PORTABLE_REPRODUCTION.md explains optional compilation and rerun requirements. Archived runners can overwrite their phase outputs and launch new trajectories; they are included as recipes only. Do not invoke them as part of this read-only analysis replay. Any future experiment belongs in a new working copy with its own reviewed settings. No new trajectories were run to package or validate this archive.

model/ contains the mathematical model contract, original theorem source, tensor-readout analysis and two independently authored algebra checkers with their saved outputs. No downloaded author code is included. Historical comments about prospective experiments in source reports are not new instructions.

SHA256SUMS covers every other packet file; PROVENANCE.json records exact source copies. To rebuild the same archive in the same Python/zlib environment run `python3 build_archive.py /path/outside/packet/rebuilt.zip`. Fresh-extraction analysis replay is checked before delivery.
