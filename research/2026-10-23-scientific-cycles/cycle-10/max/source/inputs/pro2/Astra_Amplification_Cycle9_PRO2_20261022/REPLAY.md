# Receiving and replay instructions

The saved results are the actual Cycle9 operations. Replaying them is optional;
do not count replay as discovery or rerun inherited suites to create a receipt.
All scientific code here uses Python 3 standard-library facilities. The recorded
environment was CPython 3.12 on Linux. Exact arithmetic uses `fractions.Fraction`.

## Check bytes before science

From this extracted archive's root:

```bash
python src/verify_payload.py .
```

The same utility accepts the ZIP path. It verifies exact member bytes and hashes,
safe archive paths, duplicate-member absence, and ZIP CRC. It does not claim
mathematical validity or external acceptance.

For a receiver with only the authorized Page UTF-8 source reader, obtain the
transport manifest and its ordered text references. Preserve each returned text
verbatim, using the manifest's canonical or returned filenames. Then run:

```bash
python src/reconstruct_transport.py MANIFEST.json PARTS_DIRECTORY OUTPUT_DIRECTORY
```

This is an offline byte reconstruction utility, not an access or retrieval tool.
It checks every encoded and decoded part and the full frozen ZIP identity.

## Independent receiving verification

The most direct scientific gate checks the saved native inputs, all four full
original-action operations, their exact normal equations, the same-D/noise
comparison, and all 66 NEW marked-root witnesses:

```bash
python verification/receiving/verify_receiving.py --root . --output /tmp/pro2_cycle9_independent_receipt.json
```

Use a new output path if that path is already occupied. The checker imports no
producer module. Its exact normal-equation solve is deliberately independent
of the producer's signed-incidence subtree-sum decoder. It does not run the
old closure gate or rerun the star-obstruction enumeration. It binds the old
certificate and the already-saved original obstruction support by hashes.

`verification/receiving/RESULT.json` is the actual recorded first successful
gate, with its own cost scope; do not replace it with a later timing.

## Production interface on a new admitted input

Put `src/` on the Python import path. The original simple graph has vertices
`0,...,n-1` and unordered integer edge pairs, without duplicates. Recognition
uses only the original support, not a supplied block decomposition:

```python
from block_spider_recovery import native_blocks, prepare_design
from coordinate_decoder import decode

form = native_blocks(n, original_edges)
plan, design = prepare_design(form, mode="stable")
q = design["q"]
colors = design["colors"]
# X[i,j] = 1 exactly when j == colors[i]; otherwise zero.
# Acquire ALL q original columns Y = D X + E before decoding.
diagonal_hat, edges_hat = decode(plan, Y)
```

The recognizer rejects graphs outside the stated `C_p` contract. `mode="star"`
constructs the matched `2p+1`-action control, with stronger conditioning. It is
not the general five-action control for arbitrary width-two supports.

The stable design's certified squared operator and Frobenius bounds are
`3+sqrt(5)` in `design["guarantee"]`. Old conservative estimates retained in
the generic plan are not the new spider theorem. All observations and free
diagonals remain present. Actual acquisition and any arithmetic error must
be paid; a row-normalized but perturbed design does not bound `D deltaX`.

## Regenerate producer data only in a disposable copy

The following scripts write their default result paths. Copy the extracted
archive into a separate working directory before running them:

```bash
python src/make_inputs.py
python src/project_marked_guarantees.py
python src/run_receiving.py
```

The producer writes the two exact new receiving records and current timings.
Input construction starts from the saved original obstruction and the explicit
unequal-block recipe. Timing fields will differ; they are not byte-identical
replays. The first failed producer source under `failed/` is evidence, not
the entry point and not a required execution.

For the new finite star-four diagnostic, use
`python research/root_diagnostic/check_k24_path.py --output-dir NEW_DIRECTORY`.
It covers the analytic obstruction's three small graphs and local root states.
The structural and spider diagnostic scripts write adjacent `RESULT.json`
files and must likewise be run only in a disposable copy. These checks support
the saved records; the universal theorem rests on the written argument.

## Proof and source dependencies

Start with `PROOF.md`. The integration review pins the proof before a purely
terminological clarification of “bichromatic components”; the exact delta and
final proof identity are retained alongside that review. The marked-midpoint
claim uses the accepted Cycle8 certificate plus the new source-bound projection.
It does not provide simultaneously independent states at multiple marks.

The unchanged Cycle8 ZIP contains its Cycle7 predecessor and earlier native
dependencies. The separately necessary full Cycle5 ZIP was byte-verified from
the supplied common packet. Its exact persistent private routes and selected
native source are included; no unavailable original is required. Historical
paths in old receipts describe their original environment, not a shared disk.

No executable path here resumes another owner's programme or a retired
application benchmark. Any use outside `C_p`, especially multiple blocks at
one middle or longer theta branches, needs a new invariant and proof.
