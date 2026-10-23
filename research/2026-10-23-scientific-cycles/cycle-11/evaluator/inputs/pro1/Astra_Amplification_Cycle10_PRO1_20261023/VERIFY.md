# Receiving and verification instructions

## Complete native source and identity

Verify the delivered archive's exact filename, byte count and SHA256 against
the external private delivery receipt. Extract into a new directory. Historical
absolute paths in older receipts do not imply shared local filesystems.

From the extracted native root, run:

```sh
python verify_package.py
```

Default verification uses Python's standard library and writes no package
files. Python 3.10 or later is recommended. It checks:

- Every listed `MANIFEST.sha256` file, with relative-path and duplicate checks.
- The exact preserved Cycle9 ZIP: 5,895,441 bytes; SHA256
  `5aa0f7400b36a04a470043a20d3c39382b66893766eb62d97b07a7721f1f52e5`.
- The current endpoint-response, operator-coding and compression appendices
  against their actual ZIP-member bytes in that unchanged native predecessor.
- The current final-delta review bindings, when the final receipt is present,
  including the main proof, final comparison and source correction records.
- The integrated review's earlier source versions against their retained
  reviewed snapshots. An old review is not silently relabelled as a review
  of later bytes.

Read `START_HERE.txt`, `RESULTS.txt`, `CONTINUATION.md`,
`QUADRATIC_CAPACITY_FLOOR.tex` and its supplied contributions/appendices, or
the merged `COMPLETE_PROOF.tex.txt`. Hash verification is not mathematical
proof checking, historical novelty, external acceptance or integration.

## Optional bounded replay of the new work

The optional replay requires a Unix-like Python environment with NumPy and
SciPy already installed. The scripts use the standard `resource` module;
their recorded RSS convention is the Linux KiB convention. No network,
package installation, paid compute or hardware operation is performed.

```sh
python verify_package.py --replay
```

This copies the manifest-listed package into a disposable temporary directory
and runs exactly these four new scripts, with single-thread BLAS settings:

1. `representation/gram_input_check.py`: actual small positive input matrices,
   charge normalization, entropy and analytic inward-drift margins.
2. `representation/capacity_comparison.py`: proved rate-certificate formulas,
   retained ordinary comparators and analytic scalar parameter assertions.
3. `contributions/charge_structure/exact_charge_check.py`: exact bounded
   checks of the new charge-bias identity against its defining classification.
4. `contributions/hamming_response/physical_hamming_check.py`: exact bounded
   coherent path identities and numerical new operator-bound diagnostics.

Each script has a 60-second timeout. Scripts write their fresh JSON only in
the isolated temporary copy. The verifier checks their explicit pass flags
or analytic-assertion flags, then rechecks every original manifest hash.
No frozen JSON evidence is overwritten, and no earlier scientific suite is
run. Running the scripts directly in the frozen owner directory would rewrite
their stored JSON; use the isolated `--replay` route instead.

The check does not compare elapsed-time/RSS fields byte-for-byte: resource
observations and floating diagnostic rounding can depend on the receiving
environment. The original supplied outputs remain the exact frozen evidence.
Executable checks are finite diagnostics, not proofs of the all-length
response theorem, the asymptotic charge law or the capacity conclusion.
Their elapsed time is not discovery or total review cost.

The new `independent_delta_checks.py` and its saved JSON are ordinary manifest
payloads and are bound by the final review receipt; `--replay` does not run
that additional review calculation or an inherited suite.

## Other receiving operations and boundaries

Use the supplied proof source and complete native predecessor chain for a
new scientific extension. The selected-source common evaluator packet has
its own integrity verifier; it is not a substitute for the complete native
archive when running this owner's package verifier.

Rebuilding the proof PDF requires the supplied build script and its LaTeX
dependencies. Rebuild in a separate working copy: regenerated PDF metadata
or execution records need not have the frozen delivery identity.

For a source-only private receiver, use the delivery Page's ordered UTF-8
transport manifest and exact returned part identities, decode the stated
payload in order, then verify the complete ZIP size and SHA256. Delivery,
reading, scientific acceptance and repository integration are distinct.
