# Portable randomizer control-cost addendum

This is separate from the earlier delivered finite-rate packet, which has not been modified. Start with HANDOFF.md. The leading result is the coherent covariant-residual budget p≤min{1,(√q_ref+b_RMS)²}, with a separate full-support condition for memory composition.

## Documents
- control_cost/REPORT.md: complete hypotheses/proofs, coherent and CP budgets, deterministic finite-update corollary, paid-improvement inequalities and duration costs.
- control_cost/COHERENT_RESIDUAL_AUDIT.md: independent coherent-effect proof and covariance boundary.
- control_cost/INDEPENDENT_AUDIT.md: independent stochastic mixed-subset/count audit.
- control_cost/OBSTRUCTIONS.md: why reduced gate accuracy, marginal faults, seed leakage or zero-character labels alone are insufficient.
- control_cost/NEXT_GATE.md: exact missing physical/model qualification.
- control_cost/SOURCE_COMPARISON.md: closest latest-version primary-source comparison.
- control_cost/OPTIONAL_POISSON_TILT.md: explicitly optional scalar stochastic refinement.
- reference/: the direct Fourier reference theorem, scheduled composition contract, prior scheduled theorem/audit and completion-support inputs. These are imported mathematical dependencies, not newly validated hardware or contour theorems.

## Offline replay: two suites
Requires an existing Python3 environment with NumPy and SciPy. No installation or network access is performed.

Run: python replay.py

1. control_cost/check_control_cost.py regenerates checks.json and verifies the new algebraic checks.
2. reference/check_direct_fourier.py reproduces saved global-effect and virtual-seed checks.

Scripts are copied into a temporary directory; the packet is left unchanged. The runner compares regenerated results with saved values and reports the actual suite count. REPLAY_RESULT.json records packaging-time replay. Add --record only if you want to replace that record, which changes its original manifest hash.

Verify distributed file integrity with: sha256sum -c SHA256SUMS.txt

The full prior contour/common-decoder proof chain is not duplicated. The included scheduled statement and audits identify their named imports and exact limitations. Contextual references to the earlier qualified noisy-core work are not additional assumptions proved by this addendum. PROVENANCE.json records source-file hashes and the unchanged earlier ZIP hash. No raw experimental data, private routing messages or scratch notes are included.
