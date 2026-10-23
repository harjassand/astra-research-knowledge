Independent heat-recovery-bound work, preserved 2026-10-21.

Contents:
- lp_check.py: exact inline Python source previously executed, now saved verbatim.
- lp_check.original.stdout: actual original checker output.
- lp_check.original.tool_receipt.json: actual original tool receipt and explicit resource-metering limitations.
- nist_shomate.original.js: exact prior functions.exec calculation source, using its text/store helpers.
- reproduce_nist.cjs: small Node adapter to run the original JavaScript outside functions.exec.
- nist_shomate.inputs.json: coefficients, units, branch choices, assumptions and primary NIST source URLs.
- nist_shomate.original.results.json: actual earlier calculation outputs, transcribed without recalculation.
- derivation.md: complete energy balance, staged-recovery screen, discrete/continuous pinch bound and proof, finite-rate challenge, physical qualifications and sources.
- manifest.sha256: SHA-256 checksums of the persisted files above.

Reproduction commands (not rerun while persisting):
  python lp_check.py
  node reproduce_nist.cjs

The LP checker was originally executed as an inline Python here-document. The stored source is the same body, rather than a claim that the saved filename had been executed earlier. Original wall time is reported by the tool. CPU and RSS were not metered and are explicitly null. No reconstructed resource estimates are presented as measurements. Per-case random outputs were not retained originally; the exact seed and code are retained.

The NIST computation originally ran inside functions.exec. Its 0.0-second rounded tool time is not useful precision, so wall/CPU/RSS are labeled unmetered. The Node adapter has not been executed in this persistence step.

No chemical kinetics simulation, other agent's tests, grid, or new scientific calculation was rerun during persistence. Only file creation, syntax/JSON validation and checksums were performed.
