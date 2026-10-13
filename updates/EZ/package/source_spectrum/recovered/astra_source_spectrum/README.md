# Astra source-spectrum research packet

Start with `research_note.md`. It contains the exact hypotheses, proofs, constructions, counterexamples, acquisition costs, and limitations.

`claims.json` is a compact local result ledger. These are local identifiers, not assigned Astra repository card IDs. `source_ledger.json` records prior art and the scope of repository reading.

`verify.py` runs finite diagnostics; `verification_results.json` is the output actually produced in this run. Execute with Python 3.10+ and NumPy:

```sh
python verify.py --output verification_results.json
```

The script separates exact rational/integer assertions from floating-point diagnostics. None of its finite checks is a substitute for the universal proofs. The floating calculations are not interval-certified.

No historical novelty clearance, independent proof review, formal verification, major-open-problem resolution, or demonstrated scientific speedup is claimed. No files were published to GitHub.

`MANIFEST.json` records file hashes for integrity only, not mathematical validation.
