# Verification and replay

## Integrity

From the extracted packet root, run `sha256sum -c MANIFEST.sha256`. The manifest covers every delivered file except itself. The outer ZIP has its own size and SHA256 in the delivery receipt. The unchanged R1 archive inside `preserved/` must be 457846 bytes with SHA256 `d0bd4ba562c2344fe5fed9545e08aa1cf26d320a960766d920f9d8dcd3753425`.

## Mathematical obligations

Read the complete proofs in `RECURRENT_RESERVOIRS.tex` or the rendered PDF. The generic coding step explicitly depends on affine Tverberg and Knill–Laflamme; the tree capacity is proved directly by Dyck counting, a weighted adjacency estimate, and a Kraus-rank fidelity bound. Neither R1 nor a reported finite check count is a theorem dependency.

## Finite diagnostic replay

Requirements: Python 3 and NumPy. Run:

```sh
python replay.py --output replay_local.json
```

Checks performed: exact rational periodic phase-bath distances; SWAP Choi Gram eigenvalues and full/half norm conversion; a seeded Hilbert–Schmidt identity; a period-two recurrent but nonstationary bath; exact rational tree edge detailed balance and normalization; finite walk counts and partial-permutation injection; colored Dyck-code dimension, bath return and output independence from multiple initial vertices.

These check representations and counterexamples. They do not establish recurrence or capacity by finite enumeration. Timing and memory depend on the receiving environment and are not expected to match the included receipt byte for byte. No R1 check is run.

## PDF build

With pdfLaTeX and ordinary TeX Live packages available, run `python build_pdf.py`. The source uses no generated figures or external data. Rebuilding may change PDF metadata, so compare scientific source, not rebuilt binary hash. The delivered PDF was compiled without unresolved references or overfull-box warnings and its fifteen pages were rendered and visually inspected.

## Resource boundary

The included production diagnostic receipt records about 0.073 seconds and 27280 KiB peak resident memory on this executor. No GPU, external compute job, purchased resource or hardware experiment was used. Model inference and search-service resource totals are unavailable. The tree unitary is an abstract countable-space device; no finite-energy implementation or practical transmission hardware is certified.
