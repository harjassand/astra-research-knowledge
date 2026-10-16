# L32 diagnostic: completed authorized 12 endpoints

The first-pair continuation condition passed: at alpha 0.001, seed 101, the sweep endpoint used entirely local readout, while matched Poisson-Toom used fallback. The prescribed remaining 10 endpoints then completed. All use the unchanged phase 1 binary and decoder, L32,kappa 1,T5,seeds 101/102/103. The source/binary SHA256 values remain in SHA256 SUMS and the phase 2 manifest. No phase 1 results were replaced.

| Noise ratio alpha | Sweep failure / fallback | Equal-attempt Poisson-Toom failure / fallback |
|---|---|---|
|0.001|0/3 failures;0/3 fallback|2/3 failures;2/3 fallback|
|0.01|3/3 failures;3/3 fallback|3/3 failures;3/3 fallback|

All 12 recoveries passed boundary and closed-residual invariants, with zero unresolved endpoints. This is evidence that increasing the lattice to L32 removes global-fallback dependence for the three sampled sweep endpoints at alpha 0.001; it does not eliminate the limitation generally. At alpha 0.01 every endpoint still invokes fallback.

At alpha 0.001, ineligible-component counts by seed 101/102/103 are sweep[0,0,0] and Toom[2,0,4]. At alpha 0.01 they are sweep[2036,2057,2034] and Toom[372,347,329]. The frozen binary records eligibility counts but does not distinguish exact diameters from lift-inconsistency reasons, and does not persist raw error/syndrome chains. No instrumentation change was made during this phase.

Sample size is only three per condition. Exact two-sided 95% failure intervals are 0/3:[0,0.7076],2/3:[0.0943,0.9916],3/3:[0.2924,1]. The one-sided 95% upper bound for 0/3 is 0.6316. These endpoints establish neither a threshold nor a lifetime advantage.

## Normalization caveat

The methods match total attempted update intensity, not hardware resources or check reads. Sweep reads eight syndrome bits per attempt and Toom two. At alpha 0.001 the three-seed totals are 15,730,321 correction attempts per method, corresponding to 125,842,568 sweep reads versus 31,460,642 Toom reads. At alpha 0.01 they are 15,731,029 attempts,125,848,232 versus 31,462,058 reads. Consequently the observed low-noise separation cannot be called a resource-equivalent advantage. Both are the same independently implemented Poisson adaptations used in phase 1, not the original parallel Toom paper result.

## Resources and artifacts

All 12 endpoints used 45.5215 CPU seconds and 45.5425 wall seconds, with 280,300 KiB maximum RSS (273.7 MiB), inside the 180 CPU-second/1 GiB caps. No cap, schema, or invariant failure occurred. See phase 2_raw.jsonl for all counts/timings/seeds, phase 2_summary.json for grouped counts/intervals, phase 2_resources.json for resources, and phase 2_manifest.json for the frozen parameters/stop rule. run_phase 2.py reproduces that authorized diagnostic and overwrites only phase 2 files. No additional experiments were launched after these 12 endpoints.
