# Release notes

The mathematical sampler sources, exact input graph, certified table and frozen production results are copied unchanged. The environment and setup manifests omit machine-specific interpreter and temporary-directory paths. Workspace-specific process-launch helpers, compiler executables and temporary certificate-input files are omitted; their measured outputs are retained. Floating proposal tables can be regenerated from source.

The supplied binary table is little-endian uint64 data. The implementation was tested on 64-bit Linux with Python 3.12.14, PyMatching 2.4.0, NumPy 2.3.5, SciPy 1.17.0 and Stim 1.16.0. The original environment and source hashes are recorded. A C++17 compiler is needed only to rebuild the exact certificate, not to sample from or independently verify the supplied table.

Audit scripts write refreshed result files with new timing measurements when rerun. Verify the frozen release manifest before running them; changed timing JSON after a rerun is expected.

No hidden evaluation data, user accounts or hardware access is required. All model inputs are specified public constructions.
