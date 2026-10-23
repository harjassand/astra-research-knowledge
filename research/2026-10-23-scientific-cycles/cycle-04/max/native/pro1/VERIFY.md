# Receiving and replay instructions

## Artifact integrity

From the extracted archive directory, run:

    python verify_package.py

This checks every manifested file, the immutable parent ZIP identity and its CRC. It verifies bytes and provenance, not mathematical correctness.

## Exact algebra replays

From that same directory:

    python contributions/coherent_moments_replay.py
    python contributions/coherent_anisotropic_replay.py

These use only Python's standard library and the unchanged local `representation/exact_representation.py`. Both check exact identities in the infinite-bath normal-form algebra, including the explicit finite-series remainder. A finite number of successful identities does not certify the infinite norm series; read the analytical proof and focused challenges.

The only packaging edit to these replay scripts is their default path to the bundled representation. Original observed runs and root portability runs are kept separately. No finite reflecting bath is used. The optional exploratory commutator script needs NumPy/SciPy and is NOT part of the proof or required replay.

## Mathematical review

Read the complete four-part TeX manuscript or its PDF. To reuse the positive-tilt lemma, supply the actual normal channel, finite-band dilation, bounded correction and positive operator drift. To reuse the arbitrary-rank entropy argument, supply a finite-support head comparison with log dimension O(n) and a controlled weighted tail entropy o(n); entropy alone is insufficient. To reuse the iid information theorem, retain the same actual bath, tensor-power input restriction and the initial-bath purifier in the complementary output.

## Rebuild the PDF

    python build_pdf.py

This requires pdflatex and the standard packages named in the preamble. The delivered PDF is already compiled and visually checked. The script records build costs only. No installation, purchase or external service is necessary to inspect the source.

## Private UTF-8 transport

The delivery receipt lists ordered base64 text parts, each smaller than 1 MiB. Read their actual UTF-8 source, concatenate in the stated order, discard whitespace, and base64-decode. Verify the decoded byte count and SHA256 against the receipt before extracting. Native private file authorization remains in force. The new archive is immutable; the receipt is external because it records uploads made after archive creation.

Successful byte receipt does not imply recipient reading, scientific acceptance or integration. No user forwarding step is needed.
