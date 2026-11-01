# Package audit scope

All 32 copied source/evidence files were read from local disk, matched to their controlling freeze/receipt hashes, and copied byte-for-byte. The package adds only its cover, controlling qualification, manifest, runtime dependency record, audit scope and verification wrapper. Frozen scientific sources are not edited.

The complete clock freeze lists 23 files; all are included. Its Python dependency closure is `clock_response`, `check_clock_response`, `ordinary_coupled_geometric`, `direct`, and `control`, plus standard-library modules and SymPy. Verification checks the resolved locations of all five local modules to exclude accidental reliance on an original workspace copy.

Fresh-extraction verification is recorded in the sidecar supplied alongside the ZIP. It checks ZIP CRC, archive entry safety, every packaged hash, source-copy identity before/after replay, saved data, full harness, independent checks, the withdrawn-gap counterexample and runtime local imports. Every full replay is charged 214 simulated calls; saved replay, independent synthetic/algebra checks and counterexample replay have zero new source calls.

The immutable whole-clock receipt contains one absolute-looking reviewer task identifier in its author line. It is provenance text, not a filesystem dependency, personal home path, or executable import. No private filesystem location is needed for execution. The sidecar distinguishes that preserved task label from private path leakage.

No upload, publication, external-source retrieval, nested historical ZIP or scientific scope expansion is part of packaging. The original observation bank and results remain unchanged.
