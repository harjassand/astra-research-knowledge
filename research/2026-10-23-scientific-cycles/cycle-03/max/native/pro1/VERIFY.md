# Verification and replay

## Archive integrity

From the extracted archive root, run:

```bash
python verify_package.py
```

It checks every entry in `MANIFEST.sha256`, ZIP integrity of the unchanged parent source, and the parent's exact supplied size and SHA256. This is byte/provenance verification, not mathematical certification.

## New finite scientific diagnostics

```bash
python replay_critical.py --output replay/critical_reproduced.json
python representation/exact_representation.py --output replay/representation_reproduced.json
```

The first uses exact Gaussian-rational density evolution on actual finite-support states of the infinite tree, including the two seed vacua and coherent initial states. It checks the reduced depth law at four horizons and several fixed unit-circle points, the type-domination interface, and the input-coherent drift sign. Its final rational interval certificate proves only the positivity and entropy of the explicit next input density.

The second uses finite exact normal forms on the infinite bath. It checks the root algebra, two-slot amplitudes and normalization, coherent dark-pair identities, and every balanced input/output pair through m=3. No reflecting bath cutoff is used. The all-length balanced-filter proof and the asymptotic capacity theorem are in the manuscript, not inferred from this replay.

Original results are retained in `replay/critical.json` and `representation/replay.json`; writing reproduced outputs avoids modifying those observed receipts. Small representation code requires only Python's standard library. The older exploratory obstruction scripts in `reviews/` additionally use NumPy; their exact saved outputs are preserved, including inconclusive three-call probes. They are not mandatory gates for the floor theorem, and the old entire capacity audit is not rerun.

## Rebuild the proof PDF

```bash
python build_pdf.py
```

This needs `pdflatex` and the standard TeX packages in the source preamble. The delivered PDF was compiled, all pages checked in contact sheets, and the final dense formula/bibliography pages inspected at higher resolution. `PDF_QA.json` and the build receipts record those checks. PDF rendering verifies presentation; it does not verify a theorem.

## Receiving the ZIP through the private UTF-8 interface

The private handoff Page supplies the native binary ZIP plus ordered `.zip.b64.partNN.txt` attachments, each below 1 MiB. The external delivery receipt lists their native references, sizes and SHA256 values. Read them as authorized UTF-8 source, concatenate in numerical part order, remove ASCII whitespace, and base64-decode exactly once. Verify the decoded byte count and ZIP SHA256 against the receipt before extracting.

The standalone `.proof.tex.txt` attachment merges the two delivered TeX source files at the single input directive. It is a readable complete mathematical source for the same proof; the ZIP retains the separately editable original files. The delivery receipt is external to the immutable ZIP because the service references are created after packaging.

No shared local filesystem with another agent or Mac is presumed. No browser initialization, public hosting, sharing change or user relay is needed.
