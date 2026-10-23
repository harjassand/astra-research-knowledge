# Verification and replay

## Integrity

Run from the extracted native root:

    python verify_package.py

This checks the archive's file manifest, the unchanged native Cycle10 predecessor identity, the selected inherited dependency hashes, and exact recursive expansion of COMPLETE_PROOF.tex.txt. It does not replay historical scientific suites.

The frozen archive is accompanied by a separate byte-count/SHA256/private-reference delivery receipt. The archive cannot contain its own final hash or a receipt from a later upload.

## Proof reading

ENTROPY_DRIFT_AND_DEPTH_COST.tex is the governing new source. It includes the actual new depth-budget and moment-counterexample contributions. COMPLETE_PROOF.tex.txt is its exact recursive expansion.

dependencies/cycle10/COMPLETE_PROOF.tex.txt is the unchanged merged lower-construction and coding source. Its native archive, including the earlier source chain, is in preserved/. COMPLETE_SOURCE_PROOFS.txt contains the expanded new proof followed by the byte-identical merged predecessor proof, with explicit boundaries; it is a private UTF-8 reading convenience, not a new source version.

## New bounded executable evidence

The scalar and graph scripts use Python 3.12 standard-library functionality. The direct physical-history script also uses the available NumPy installation. No package installation, paid computation, huge matrix construction or predecessor-suite replay is required.

    python representation/cycle11_certificates.py --output /tmp/cycle11_certificates_replay.json
    python contributions/entropy_drift_challenge/physical_pressure_check.py
    python contributions/moment_comparison/counterexample_check.py
    python contributions/scalar_pressure/scalar_pressure_check.py
    python contributions/scalar_pressure/cost_envelope_check.py

The first command can preserve the observed packaged JSON. The contribution scripts write their adjacent output files, so copy the extracted package before optional replays if preserving exact original observations. Timings will change; compare mathematical fields rather than expecting byte-identical timing JSON.

The scalar-pressure script's historical source lookup was repaired to the packaged, byte-identical selected dependency. See evidence/SCRIPT_PATH_REPAIR.json. No numerical expression changed and no old suite was rerun.

Read each scope field. Fake rare-sector examples are not physical channel counterexamples; finite physical cases are not all-length proofs.

## PDF

The PDF was compiled with pdflatex and visually checked. build_pdf.py reproduces the document; render_pdf.py requires Pillow and Poppler for visual inspection. The current runtime's primary Python supplies Pillow. The direct physical diagnostic additionally uses NumPy; the scalar diagnostics use the standard library. Build and rendering times are not scientific discovery costs.

    python build_pdf.py

The artifact-operation marker was run once in this authoring session before creating the PDF. It is not a mathematical dependency or a command that receivers need to repeat.

## No automatic continuation

Verification does not activate another owner, run a future scientific job or poll for acceptance. CONTINUATION.md records the next owned question and its actual unproved obligation.
