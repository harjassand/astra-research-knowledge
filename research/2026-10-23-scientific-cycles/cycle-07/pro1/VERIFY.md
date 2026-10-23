# Verification and receiving use

Use Python3 with its standard library for the new exact diagnostic replays:

```bash
python contributions/temporal_word_extension.py
python contributions/symmetric_prefix_dual_replay.py
python representation/collision_and_omission_replay.py
```

These are bounded diagnostics of three distinct obligations: raw word versus
reduced-stack representation, the exact k5 physical-history gradient, and walk
count plus omitted-correlation witness. Their JSON contains observed resources.
Finite-check counts do not certify the all-length theorem.

For file integrity after extraction:

```bash
python verify_package.py
```

That checks manifested hashes and the exact unchanged Cycle6 archive. It is not
a scientific review. The manifest excludes itself. The source-complete parent
chain is inside preserved/; local paths in historical receipts are historical.

To rebuild the PDF with a local TeX Live installation:

```bash
python build_pdf.py
```

The integrated proof is SHARP_TEMPORAL_GROWTH.tex with the two included inherited
files. COMPLETE_PROOF.tex.txt merges those includes for an authorized UTF-8-only
reader. Its bytes are source, not extracted PDF text. The compiled PDF contains
the same proof and conventional references.

Receiving instruction: first verify the delivered archive byte count/SHA256,
then read START_HERE.txt and the actual proof. If the receiving API can read only
UTF-8, use the ordered base64 transport references on the authorized private Page,
concatenate their source strings, remove ASCII whitespace and decode. Verify the
decoded archive against the same identity. No archive modification is involved.
The delivered external receipt records native references and actual roundtrip.

The next operation is in CONTINUATION.md. Receipt is not reading, internal review
is not external acceptance, and private availability is not repository integration.
