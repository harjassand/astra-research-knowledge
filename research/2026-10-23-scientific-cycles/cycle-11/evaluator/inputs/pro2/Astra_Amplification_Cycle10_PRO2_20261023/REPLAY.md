# Receiving and replay instructions

The source has no third-party Python dependencies. Recorded calculations used
Python 3.12 with exact standard-library Fraction arithmetic. Preserve the
frozen original directory or ZIP; use a disposable copy for any scientific
replay, because producer and independent programs write result/cost files.
The external transport manifest binds the original ZIP size and SHA256.

## 1. Byte integrity only

From the extracted archive root:

```bash
python src/verify_payload.py .
```

Or pass the original ZIP path to the same verifier. This checks the exact
member inventory, sizes and SHA256s, plus ZIP safety/CRC when applicable.
It executes no scientific program. An integrity pass is not proof acceptance.

## 2. Read the all-size argument

Read PROOF.md and the accepted one-root dependency in the embedded unchanged
Cycle9 source. The independent review is in verification/reset_review/ and
verification/independent_receiving/RECEIVING_REVIEW.md. Finite calculation
cannot substitute for the all-depth induction. The exact old closure need
not be rerun to read or use its fixed certificate.

## 3. Optional independent verification of the NEW saved operations

In a disposable copy of the extracted root:

```bash
python verification/independent_receiving/verify_receiving.py
```

This reads saved native inputs/actions and independently reconstructs blocks,
component shapes, original support, actual message conditions, Fraction
normal-equation inverses and all error identities. It imports no producer
module and does not rerun old searches. It rewrites its VERDICT.json and
COSTS.json, so the original frozen manifest will no longer match that working
copy. New runtime is a replay cost, not the original discovery cost.

## 4. Optional producer reproduction of this checkpoint only

```bash
python src/run_receiving.py
python src/check_no_message_failure.py
```

These use existing actual inputs and fixed certificate data under sources/.
They overwrite their own result/cost files. The first program reproduces
the three full-action operations. The second constructs the exact C4-chain
failure witness and the successful complete coloring on the same graph.
Neither executes the inherited H8 closure, old NIST benchmark, molecular
work or evaluator experiments. It is unnecessary to rerun them just to
receive the exact source or read the proof.

The marked-atom helper accepts an explicit prepared bundle; use
prepare_marked_certificate('sources/loaded_star_certificate.json',
'sources/marked_root_projection.json') and pass that reusable bundle. Its
standalone fallback data path is historical; main production callers supply
the actual paths explicitly and load once.

For a new admitted native graph, use prepare_recovery(n, original_edges,
bundle) from src/block_reset_recovery.py. Its returned block structure,
design and decoding plan preserve original IDs. Give the decoder all n-by-4
original observations. Do not replace original actions with reduced ones.
Outside the promised intrinsic class the code may reject; acceptance must
still pass its actual support/color/spider certificate. It is not a complete
recognizer for every invalid input.

## 5. Additional bounded contributors

research/theta_explicit/ contains an independently derived table-free theta
operation, full proof and original diagnostic. Its native implementation is
also copied unchanged as src/theta_hub_split.py. The failed first shape
checker is evidence, not a recommended verifier.

The marked adapter's six-case diagnostic can be run in a disposable copy:

```bash
python research/marked_atom/run_diagnostic.py --certificate sources/loaded_star_certificate.json --projection sources/marked_root_projection.json
```

These auxiliary diagnostics already ran once. They are not required to repeat
the completed searches. Their historical source-binding records retain the
original authoring paths; the production operation and independent receiving
gate use locations relative to this archive.

## Numerical boundary for a practical receiving use

Exact rational examples pay zero projected numerical residual. A floating
implementation must bound R=Dhat X-Pi Y and use

    ||Dhat-D||op <= sqrt(3+sqrt5)(||E||F+||R||F).

Input conversion, probe/acquisition error, action assembly, precision and
sparse output costs are additional. Probe error contributes D deltaX and
is not bounded by the row norm alone. Cheap direct entries or AD remain
legitimate controls; no query-oracle advantage is assumed.
