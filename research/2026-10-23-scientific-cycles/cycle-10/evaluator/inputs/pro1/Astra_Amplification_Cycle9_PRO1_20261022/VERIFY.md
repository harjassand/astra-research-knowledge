# Receiving and verification instructions

1. Verify the final archive's filename, byte count and SHA256 against the external private receipt.
2. Extract into a new directory. Absolute paths in old receipts are historical; they do not imply shared local storage.
3. Run `python verify_package.py` inside the extracted owner root. It verifies the manifest and unchanged predecessor identity.
4. Read `START_HERE.txt`, `RESULTS.txt`, `CONTINUATION.md` and the actual complete proof. A successful manifest check is not scientific acceptance.
5. If a bounded replay is useful, run `python representation/transfer_comparison.py --output /tmp/pro1_cycle9_transfer.json`. This is standard-library Python with 100-digit Decimal arithmetic.
6. The exact witness replay is `python contributions/spectral_structure/witness_replay.py`. It writes its JSON beside the script. Its all-length proof is separate.
7. Optional spectral diagnostics in `contributions/spectral_structure/spectrum.py` require NumPy and SciPy. They were not used to fit an exponent and need not be rerun for receipt verification.
8. To rebuild the PDF, use `python build_pdf.py` with standard pdflatex and Poppler installed. The build script also regenerates the merged proof text. PDF metadata may vary across rebuilds; the delivered byte identity remains frozen in the manifest.

The native Cycle8 ZIP and its embedded chain remain unchanged. The current appendix contains an extracted response proof with adjusted section levels and a corrected pointer to the preserved counterexamples. The operator-coding and joint-compression appendices are byte-identical to Cycle8.

For source-only private clients, the external ordered base64 transport pieces reconstruct the exact ZIP. Read the manifest, verify each returned UTF-8 part, concatenate payload text after removing whitespace, decode, and verify the full archive's supplied byte count and SHA256. No binary Page read, UI re-upload, sharing change or user relay is required.

Next scientific use: the positive repair's actual operator drift and charge cost at fixed small `bk`. Do not replace the supplied proof by this verification list or reopen settled nonlinear response work.
