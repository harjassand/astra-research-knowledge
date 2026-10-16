# Completed bounded matched-memory pilot

## Main result

The own implementation passed the independent release gate, then completed all 20 prescribed finite-time endpoints within the cap:4.1704 CPU seconds,4.1864 wall seconds,25,708 KiB peak resident memory. Two deterministic repeat checks used another 0.3466 CPU seconds. This phase stopped at the declared grid; a later separately authorized L32 diagnostic is recorded in PHASE2_RESULTS.md. Every nonzero-noise endpoint used global fallback, so these data are **fallback-dependent decoder-specific endpoints**, not a useful threshold or lifetime comparison. They do not establish which local memory dynamics is better.

All runs use L=16,kappa=1,T=5, one classical CSS/X-error sector, no Y/Z noise, ideal syndrome, equal total correction-attempt intensity L^4. Toom has face-attempt rate 1/6 and is explicitly a Poissonized matched adaptation of the primary north/east rule, not the original parallel-paper result. Positive-alpha seeds are 2026101501,2026101502,2026101503. Zero uses 2026101501 once per method. Exact choices are in manifest.json.

| alpha=lambda/kappa | Sweep failures | Poisson-Toom failures | Whole-syndrome fallback | Unresolved |
|---|---:|---:|---:|---:|
|0|0/1|0/1|0/2|0/2|
|0.001|3/3|3/3|6/6|0/6|
|0.01|3/3|2/3|6/6|0/6|
|0.05|3/3|3/3|6/6|0/6|

For 3/3 failures, the two-sided exact 95% Clopper–Pearson interval is [0.2924,1]. For 2/3 it is [0.0943,0.9916]. For 0/1 it is [0,0.975]; zero noise also has an exact model-level absorbing-zero sanity expectation. No pooling across methods: matching shares clock/type/noise streams within seed pairs. The six-bit outcome for every seed is retained in pilot_raw.jsonl and pilot_summary.json.

## Decoder interpretation

This frozen decoder first tests all connected syndrome components for consistent lift and strict wrapped infinity diameter<L/8. At L16 this is diameter<2, so even width 2 components trigger fallback. If any component fails, all partial local fillings are discarded and the tensor contraction is applied to the whole syndrome. Consequently the local-only readout fraction is 0/18 at positive noise, although many individual components remain eligible. Global H is algebraically complete but has documented poor logical behavior, including isolated-face seam defects when used globally. The pilot cannot attribute its large failure counts separately to physical dynamics versus these recovery choices. No decoder was changed after seeing results.

Mean final syndrome weights, sweep versus Toom: alpha 0.001:1588 versus 5303.33; alpha 0.01:21594 versus 45372.67; alpha 0.05:109448.67 versus 102541.33. These describe this tiny fixed-time sample only. No statistical advantage claim is made.

## Counts and costs

Per method, positive-noise three-seed totals are:

| alpha | Noise attempts | Correction attempts | Sweep check reads | Toom check reads |
|---|---:|---:|---:|---:|
|0.001|5939|984448|7875584|1968896|
|0.01|58911|984609|7876872|1969218|
|0.05|294663|985425|7883400|1970850|

The matched event totals agree by construction. Check reads are logical correction-rule inspections,8 per sweep attempt versus 2 per Toom attempt; readout and invariant-check reads are not included. Successful operations, two-face events, total face flips, RNG draws, syndrome/recovery weights, component counts, per-trial dynamics/readout timings and seeds are in the raw JSONL. Aggregate timing includes all endpoint validation and readout in child processes; the 4.1704 CPU-second total is well below 180. Each process had a 1 GiB address-space limit. Maximum reported RSS was 25.1 MiB; no cap was approached. There were no unresolved or aborted trajectories.

## Validation and reproduction

- Built-in selftest: all 393216 single-face faults on L16, including periodic seams, recover locally with trivial residual homology.
-263492 cube boundaries on L3,4,16 have zero syndrome and logical parity. Six sheets at odd/even sizes have identity parity at all tested cuts.
-2000 scripted/random updates agree with an independently written gather syndrome.
- External verifier:5150 decode cases;704 kernel truth-table cases; independent incidence ranks and boundary-squared identities; literal tensor-H agreement; wrapped-loop pairs; mixed local/winding components; strict cutoff; syndrome-identical logical-sheet inputs.
- Each readout checks recovery boundary equals input syndrome and residual boundary vanishes before scoring.
- Same-seed repeats at alpha 0.01 for both methods match every recorded nontiming field exactly. They are diagnostics, not new independent samples.

Read INDEPENDENT_AUDIT.md for the independent gate. README.md gives reproduction and interface commands. SHA256SUMS pins the validated C++ source and binary. No third-party simulator source was executed or software installed.

## Stopping and limits

The predeclared pilot is complete and stopped. Its fallback frequency identifies a readout-quality issue worth resolving before any performance study, but changing the decoder or running another grid would be a separate explicitly specified experiment. These endpoints give no threshold, exponential lifetime, continuous-time first-failure distribution, theorem large-size applicability, optimal-decoder comparison, or physical engineering cost claim.
