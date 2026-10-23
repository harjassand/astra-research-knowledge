# Independent audit: frozen Markov receiving check

**Verdict: PASS for the stated small, conventional receiving-operation check.** I found no concrete mathematical or implementation gap in the inspected adapter, refinement, or history-query logic. This is independent static review plus read-only checking of saved rational certificates and hashes; it is **not an independent rerun** of the worker, native model, or Pro3 scientific admission suite. I did not import or execute either scientific program, reconstruct the native transition matrix, rerun refinement, or propagate a chain.

The check supports exact reuse of an observation-equivalence principle on this admitted 32-state model. It does not establish scientific invention, an acquired reasoning policy, an advantage over ordinary aggregation, a scientific capability benchmark, or an asymptotic result. The strong conventional method is the tested operation itself.

## Source and semantics

Experiment directory: `/workspace/scratch/f2e6b9408a0a/work/cycle10_20261023/meta_transfer/markov_query`.

Original source directory: `/workspace/scratch/f2e6b9408a0a/work/cycle10_20261023/inputs/pro3/Astra_Amplification_Cycle9_PRO3_20261022`.

I compared original `code/exact_checks.py`, lines 125–242, against receiving `markov_query.py`, lines 72–147. The adapter reproduces the breadth-first depth-4 binary tree, core vertex 31, level masses and multiplicities, local proposals and accepted moves, independence-MH kernel, and the full mixture `C=(I+alpha G+(1-alpha)L)/2`. It uses the original native proposal start. The original screen identity is consistent with this fixture: the expansion child/parent proposal-mass ratio is `R^(-8)` and the reverse/forward edge-proposal ratio is `R`, so their screened product is one. No alternate local kernel is introduced.

The adapter checks exact q/pi agreement, the original native edge digest, stochasticity, detailed balance, and every native row's aggregation to the stored original six-level kernel. The unchanged admitted fixture is `expansion_native32`, with `M=2`, depth 4, `R=3/2`, `eta=1/2`, `kappa=4`, `b=1/2`, `p=1/512`, `alpha=1/2`, `K=1`, and horizon 64. My JSON audit independently confirmed that the certificate's fixture equals both `EXACT_INPUTS.json` and the preserved `expansion_native32.json` admission input, whose `all_frozen_gates_pass` is true. This admission is inherited; I did not recertify KL or the owner's other scientific conditions. The inadmissible coalescence fixture is not used by this adapter.

## Mathematical and algorithmic review

`QUERY_SUFFICIENCY.md` gives a sound strong-lumpability argument. Equal transition sums into every block make the next-block distribution independent of the hidden conditional distribution inside the current block. An observation constant on each block therefore has the same complete finite-word law under native and quotient chains, for every initial distribution. First hits, survival, final membership, and exit/reentry histories follow as functions of the observation word. The coarsest-partition argument is also sound **within observation-refining strongly lumpable partitions**; it correctly avoids a claim of minimality for one start or horizon.

`markov_query.py`, lines 150–180, implements exact rational partition refinement and explicitly checks the stable block-transition equalities. Its positive control recovers the original six levels. For the frozen subset `{15,16,19,26}`, the recorded refinement takes six strict rounds and yields 24 blocks. I independently checked partition coverage, block observation constancy, the 24-by-24 saved quotient's nonnegative unit row sums, and normalized quotient initial masses. The full native-to-quotient row equalities are checked by the reviewed worker code; my audit did not regenerate them independently.

`markov_query.py`, lines 191–248, correctly uses common integer denominators for forward and backward propagation. For first hit at time t and final membership at H, the arriving first-hit numerator is multiplied by the **unabsorbed** continuation vector for H−t; its common denominator is `q*d^H`. The four forward phases correctly distinguish never hit, hit without exit, exited without reentry, and reentered at least once. The final phase continues under the full kernel even after a later exit. Time-zero hits are included. The implementation does not enumerate every observation word; the strong-lumpability proof supplies that broader sufficiency guarantee, and the listed finite queries are checked exactly.

My read-only rational audit confirmed exact native/refined equality for both 65-entry arrays and all four scalar queries, normalization of saved laws, and equality between native final masses aggregated into the 24 blocks and the saved refined final vector. It also checked first-hit plus survival equals one and the sum of first-hit/final-membership joints equals final membership.

## Counterexamples and interpretation

The old six-level partition fails observation measurability: vertices 15 and 17 share level 4 but have different event membership. The seven-block level×membership partition fails strong lumpability: parents 7 and 8 share level and membership, but their one-step event probabilities differ by exactly `1/7`. This has a transparent native explanation: parent 7 has two selected children, parent 8 has none; their global-event contributions agree, and the full-kernel local difference is `(1-alpha)/2 × 2/(M+R) = 1/7`. I checked the saved rational witness arithmetic.

The actual prescribed q-start also exposes a history error in the naturally q-weighted seven-block averaged chain. My saved-law audit confirmed that the earliest first-hit mismatch is time 2, with native minus averaged probability

`−1048576/90797989253740209` (approximately `−1.15484495705e−11`).

The earliest first-hit/final-membership joint mismatch is time 0. The small numerical size does not affect exact falsification. This averaged chain is explicitly labelled invalid; it is not substituted for the strong conventional comparator.

**Scope qualification:** the native and invalid averaged chains have exactly the same final-event marginal in the saved result. Under the symmetric q-start, the old level representation can recover this single-time subset marginal using the selected fraction of terminal vertices. Its failure concerns the changed history query and statewise observation sufficiency, not every possible use of the old representation. This distinction should remain in any summary.

## Freeze, resources, and limits of assurance

All six frozen input/source file hashes and byte counts match `FREEZE.json`; its timestamp precedes the recorded worker start. The three output hashes linked from `RESULT.json` also match. `PROCESS_RESOURCE.json` records one successful worker execution, 0.511385 CPU seconds, peak RSS 19,460 KiB, and 0.515557 wall seconds. It records that the earlier missing-`/usr/bin/time` launch did not execute the worker. These are inspected process receipts, not measurements rerun by this auditor. The figures meet the declared resource bounds; a single tiny run with unmetered development/inference cost cannot establish a transfer speedup or research advantage. Zero stage CPU readings should be read as clock-resolution effects.

No claim beyond this scoped pass is warranted by the audit. In particular, a 32-to-24-state quotient obtained by conventional exact refinement is assurance of the receiving interface and a useful counterexample to indiscriminate reuse of the six-level representation; it is not evidence of stronger scientific intelligence.

## Audited identities

Paths below are relative to the experiment directory unless prefixed `source/`, which denotes the original source directory above. SHA-256 values were independently recomputed from the files during this audit.

| File | SHA-256 |
|---|---|
| `PROTOCOL.json` | `788c848aa69c6f5402dfd51ad7cf1b31baee420a23043b59fbddba11bc9fdd7f` |
| `QUERY_SUFFICIENCY.md` | `ca3cb1c6aae41f7149390fe0b735d61dc1c52a1a996b529880e62a73ea404c98` |
| `markov_query.py` | `d196b360c6942f613f99dfdb3d581b9ac5cf3a22ce34342d84cb8009a51de21a` |
| `source/code/exact_checks.py` | `c78a5576bc5861501a9f936e495e84d03a0b7f8dffbf80799455c9b814b91711` |
| `source/evidence/exact/EXACT_INPUTS.json` | `357cb63fb78fa1fe0fe627e84c0cf58942cd64261834805224635028736e0253` |
| `source/evidence/exact/expansion_native32.json` | `e220f874f6b140a61742daea2af1bb38e092f2c103b41f2a45b21eac68187273` |
| `FREEZE.json` | `71a201892038b22d0bbb485919ba9b56b718b840640b328c8104384f813cab6d` |
| `RESULT.json` | `a64a68318e68f2d841b980d465637f7918201919483628ce5238459ebdad58ae` |
| `CERTIFICATE.json` | `b2321e361199627e264916b0f993d76fbf5e813667a781cbcd560a9df2bb8b82` |
| `EXACT_LAWS.json` | `dcfcff6d1a697a59be80d635ca7a39249f0fc854aad9fd909abfea1a89e4eeff` |
| `PROCESS_RESOURCE.json` | `b0fc490fe1486c804e9bf6a223c1542aaf96e74f59aa7e05fb01ea0adb81346f` |
