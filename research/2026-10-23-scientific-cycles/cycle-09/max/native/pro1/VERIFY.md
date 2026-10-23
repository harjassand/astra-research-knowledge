# Integrity and bounded replay

Run from the extracted archive root with Python 3. The scientific theorem is
proved in the TeX source; these commands test file integrity and bounded exact
examples. They do not certify an all-length theorem by enumeration.

## Integrity

```bash
python verify_package.py
```

This checks every SHA256 in `MANIFEST.sha256` and the exact unchanged Cycle7
ZIP identity. The manifest does not hash itself. The outer ZIP identity and
private delivery receipt are external to avoid circular self-hashing.

## New diagnostics

Use a temporary extraction when replaying. The independent witness writes its
JSON alongside its source, so a replay changes that observation file's timing.

```bash
python contributions/fourth_order_words/exact_coefficients.py --output /tmp/pro1_cycle8_coefficients.json
python contributions/independent_challenge/four_endpoint_witness.py
python representation/fixed_angle_comparison.py --output /tmp/pro1_cycle8_comparison.json
```

The first command checks exact small-block contracted coefficients and the
incorrect shorter-optimizer substitution. The second independently implements
the sixteen complementary mask pairs for the omitted-pair-support witness.
The third evaluates known closed formulas at beta=1/512 with 90 decimal
digits. None optimizes a code, constructs an encoder, or measures physical
communication performance.

The exact-coefficient script uses its included byte-identical inherited
representation module. All replay dependencies are included; it must not
import from a different owner's workspace or a historical absolute path.
The scripts otherwise use Python's standard library and the dependencies
declared in their source. Check the portability receipt for the tested local
runtime and observed replay costs.

## Proof rendering

```bash
python build_pdf.py
```

This requires a local `pdflatex` installation and the TeX packages used in the
source. The already-built 16-page PDF is included, along with build and visual
QA records. Building the PDF or checking file hashes does not replace reading
the argument.

## Reassembly

```bash
python make_archive.py --destination /tmp/pro1_cycle8_reassembled
```

The script excludes temporary files, extracted predecessor duplicates and
Python caches, writes the file manifest, and uses deterministic ZIP entry
timestamps. It preserves the original predecessor ZIP bytes. The source
archive intentionally excludes its own external delivery receipt.
