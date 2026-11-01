# Cold construction of an actual clearance clock

This separate package preserves the earlier accepted finite-population result and adds a complete prospective cold numerical algorithm. The new algorithm computes its scalar enclosure afresh, verifies it with a different implementation, and returns both source-bound stochastic timing intervals. It does not take the old fine scalar certificate as an input.

## Accepted two-fixture result

For the exact twelve-channel rate-2 count model, start at (A,B,C,D,E)=(0,N,1,1,0). Let S=A+B+C+D+E and let tau be the first time S<=15(N+2)/16. Each interval below has coverage at least99%, separately for its stated fixture:

| N | T=N^(1/5) | Interval for tau, in model time units |
|---|---:|---|
| 10^20 | 10000 | [10358.028789, 11778.581481] |
| 10^25 | 100000 | [108894.954785, 112426.147917] |

This is not a joint99% claim for two realizations. Only these two fixed fixtures are received. These intervals are slightly wider than the earlier retained-fine-scalar output because the new cold algorithm deliberately acquires less scalar precision.

The governing acceptance is `boundary_clearance_kernel_root_20261101/audit_coarse_cold_20261101/REVIEW_RECEIPT.json`, SHA256 `46fc3785bb137f81af5b8574a5fbaef14934573e65e8f627228ee83e33469b15`.

It receives the unchanged author freeze `a6e1638f31b6d8055c2e158e4bdbabc0256b2a6c43cf49ea564ce4c1c69b4114` and proof `089266a8b28a5383d9e3ced048c2747251244bfa4fc22d7e368eb6e7259e86b8`.

## Run the complete cold algorithm

Requires Python3.10 or newer. From the package root:

```
python3 boundary_clearance_kernel_root_20261101/coarse_cold_algorithm_20261101/run_cold.py
```

This is the complete required sequence:

1. Authenticate the36 source-bound mathematical dependencies.
2. Run the coarse constructor, including two exact self-passes.
3. Run a different exact coarse-verification implementation, for a third scalar pass.
4. Compute both outward-rounded finite-population intervals.

The parameters are startup degree28, inverse Taylor order6, 80-bit arithmetic and terminal inverse coordinate16. The constructor uses315 steps in the saved run; the static proof pays up to320. Its fresh scalar enclosure is

`1.106580470126746169 <= s_* <= 1.106580556897779284`,

with width below8.678×10^-8. Running `coarse_windows.py` alone merely postprocesses an existing certificate and is **not** the cold algorithm.

The complete command writes fresh adjacent outputs, including an observed timing field. Run it on a working copy if preserving the shipped frozen bytes is important. `verify_package.py` checks the frozen package without starting another scalar solve. `PACKAGE_COLD_REPLAY.json` records the clean-copy packaging replay of the full pipeline. That extra replay is disclosed research work, not an additional mandatory prospective phase.

## Explicit prospective work bound

The accepted specified arithmetic/control/I/O machine bound for the complete fresh algorithm is

**282,578,068,509,184,000,000 abstract bit steps <3×10^20**, with storage at most2^27 bits.

This pays source authentication, all three scalar passes, verification and both interval evaluations. It is a static bound, not a benchmark inferred from one quick run.

At N=10^25 the successful-path theorem entails at least2×10^21−1 events for a literal one-event-at-a-time simulator. The new complete prospective bound is below that literal event count in the stated cost comparison. This is deliberately narrow: it establishes no superiority over non-enumerative validated, multiscale, retained or ordinary point predictors, parallel hardware, or the strongest available general method.

It is not a CPython, operating-system or wall-time guarantee. Nor does it reduce prior research expenditure retrospectively. The old conservative scalar reserve3×10^27, recorded failed/superseded calculations and prior measured subtotals remain unchanged. New construction history, reviewer work and the packaging replay are recorded separately. The earlier retained-only package remains intact.

## Scientific chain and acceptance hierarchy

The underlying actual-path proofs earn raw startup, source and A/Z gates, and a global upper-ratio barrier from exact adjacent-ratio cancellation. A source-weighted corrected clock pays its full drift and bracket, including all enabled startup and adverse terminal jumps. The first macro target is forced by original time4T; the actual admitted state then receives a five-unit factorial-entropy removal service. The failure ledger gives the per-fixture99% coverage.

The cold branch changes numerical scalar acquisition, not the actual source model or that same-path proof chain. No stationary preparation, independent artificial attempts, state reset, microscopic event enumeration, or physical model acquisition is supplied for free.

Original author files and JSON statuses remain unchanged, including historical “pending” labels. Their exact later receipts determine acceptance. `COARSE_WINDOWS.json` is received by the new coarse-cold receipt despite its preserved author status. Earlier fine-scalar files are included only as preserved scientific history/dependency evidence; the mandatory cold runtime does not read them. The clean packaging replay starts in a minimal36-source working tree with no old scalar certificate present.

## Scope and limits

- Exact stated model, raw initial state, two populations and separate99% coverage only.
- Model time units; no physical preparation, rate calibration or hardware demonstration.
- No finite-N Gaussian CDF, full-trajectory sampler or arbitrary-parameter interface.
- No standalone adversarial-certificate validation claim.
- No total past-research speedup, universal algorithmic superiority or historical novelty claim.
- Ongoing phase-law refinements and alternative compiler work are outside this package.

The complete ordinary mathematical/cost review, scoped checks, author history and exact source copies are included. Tests support the proofs; sampled numerical success is not their replacement.
