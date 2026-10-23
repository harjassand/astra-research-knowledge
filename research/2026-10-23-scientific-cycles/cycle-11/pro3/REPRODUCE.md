# Reproduction and source access

This is a mathematical checkpoint. The proof is in
NATIVE_PATH_COMPOSITION_THEOREM.md, with the unchanged full predecessor in
sources/ and readable governing dependencies in dependencies/.
Reading or replaying code does not independently prove the universal theorem.

## Delivered payload identities

From the extracted archive root:

    python3 -I replay.py

This verifies this archive's manifest and exact predecessor ZIP identity.
It does not run scientific tests, the predecessor's suites or the evaluator's
altered observation query. Do not run the predecessor's full-archive verifier
against a selected dependency directory.

## Optional new exact diagnostic

    python3 -I replay.py --run-new-diagnostic

This copies only contributors/tagged_path_check/ to a temporary directory,
runs its exact Fraction arithmetic, and checks the scientific RESULT.json
against the frozen result. It preserves delivered files. The new timing
receipt will naturally differ.

The inputs are frozen and admitted K=24. The code builds the actual four-state
local/global/lazy kernels, checks exact rows and target detailed balance,
reverses tagged finite paths, tests positive-progress event containment and
compares first-hit enumeration with an independent exact recurrence.
It does not estimate a critical rate or amplitude and does not certify K=1.
Python standard library is sufficient.

## Formula figure

    python3 code/phase_law_figure.py

Matplotlib and Pillow are needed only for this optional figure. It evaluates
the proved phase formula at the unchanged illustrative constants
K=1, alpha=1/2, d=3, s=-1. It performs no simulation or fitting.
The PNG is rendered in memory, written in checked small chunks and verified.
Rendering libraries can change image bytes between environments.

## Rebuild the source archive

    python3 -I code/build_archive.py

The source payload order and ZIP timestamps are deterministic. Exact
compressed bytes may depend on the Python/zlib environment, so compare
payload hashes as well as the delivered archive identity.

## Private source transport

The external delivery receipt gives the actual Library/backing IDs and
authorized private Page references after the ZIP is frozen. Base64 transport
parts are UTF-8 files no larger than 1,000,001 bytes each, for a receiver
whose Page source API reads text but cannot directly materialize binary ZIPs.
The ordered transport manifest includes exact part names, hashes and native
references. Decode with code/decode_transport.py and verify the expected ZIP
byte count and SHA256. No access change, public hosting or user relay is needed.

The receipt is external to avoid a circular self-hash or mutation of the
delivered ZIP. Delivery/readback status is separate from recipient reading,
scientific acceptance or integration.
