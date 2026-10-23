# Replay and proof verification

The mathematical proof is CORRELATED_CAPACITY_GAIN.tex with
INHERITED_COMPRESSION.tex. COMPLETE_PROOF.tex.txt merges the latter into the
former and can be read as one UTF-8 source file. The PDF was compiled and all
14 rendered pages inspected. Proof review is distinct from code replay.

## Portable diagnostics

Only Python's standard library is required for these commands, run from the
extracted checkpoint directory:

```bash
python verify_package.py
python contributions/two_call_algebra.py
python contributions/two_call_entropy_replay.py
python replay_candidate.py
```

The first verifies the manifest and unchanged parent identity. The symbolic
algebra works in Gaussian-rational polynomials modulo alpha²+beta²=1 and uses
infinite-bath normal forms. It verifies the full cross superoperator, grade
Gram coefficients, root/level-one rows, normalization and bounded drift.
It does not introduce a finite bath cutoff. The entropy script records the
exact rational candidate and analytic lower certificate; Decimal entropy is
an observed diagnostic, not an interval proof. The root replay checks the
actual kernel, same-entropy sign flip, and exact eight-product separable
decomposition. None compiles a quantum code or simulates its asymptotic bath.

Output receipts can be directed to an external temporary path with `--output`;
do not overwrite manifested files if checking their immutable identity.

## Optional document build

With pdflatex installed, `python build_pdf.py` builds the PDF and writes build
receipts. This changes the generated PDF timestamp and therefore its hash;
use a separate copy when reproducing the build. The delivered PDF and receipts
are already in the archive. Rebuilding is not required to verify the proof.

## Private transport

The external delivery receipt records the native ZIP and readable source refs.
For a receiver limited to authorized UTF-8 sources below1MiB, read the ordered
base64 parts, concatenate their text, remove whitespace and decode once. Verify
the decoded byte count and SHA256 against that receipt before extraction.
These parts encode the existing completed archive; they do not change it.

Read CONTINUATION.md for the next scientific operation. A valid file digest or
successful replay is not a claim that Max or the evaluator has read, accepted
or integrated the result.
