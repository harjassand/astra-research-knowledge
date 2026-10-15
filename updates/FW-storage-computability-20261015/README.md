# Effective storage-value approximation for the Heat18 quartic

Status: **source_derived_unreviewed**. This packet gives a source-derived terminating value-enclosure construction for effectively specified endpoint data for the particular certified Heat18 quartic G. It does not claim a practical solver, an executed storage-value computation, external mathematical validation, historical novelty, physical technology, practical superiority or resolution of general Morrey questions. PR97's newly exposed ROC ray and the full quartic cone are not covered.

Start with the [finite-horizon proof](package/storage_horizon/FINITE_HORIZON_STORAGE.md) and [buffered global-heat spatial proof](package/storage_spatial/THEOREM.md). The [horizon audit](package/storage_horizon/HORIZON_AUDIT.md) and [spatial audit](package/spatial_audit/INDEPENDENT_HEAT_AUDIT.md) are source-derived internal mathematical challenges, not external review. The [Heat18 audit](package/heat_certificate/PROOFCHECK.md) and [coercivity audit](package/heat_certificate/COERCIVITY_PROOFCHECK.md) separate finite rational identities from their analytic transfer arguments.

Finite-Fourier coefficients of B and U must be computable with certified enclosures. General critical endpoints additionally need a supplied effective strong-tail approximation and the applicable bounded-ball continuity bound; finite observations alone do not supply it. The fixed-endpoint horizon, free-terminal-mean surrogate and slightly enlarged spatial duration are distinguished in the proofs. The unadjusted affine term uses the actual endpoint mean.

For U=(cos y,sin y), B=0 and target width 0.01, the [resource account](package/storage_spatial/RESOURCE_RECEIPT.md) supplies N=10^22, K=10^44 and approximately **8×10^88 real parameters**, with log10 of the sufficient grid size below 662d (approximately 5.296×10^91). These are loose sufficient upper budgets, not lower bounds for other algorithms. No grid, objective evaluations or storage interval was computed. Input acquisition, interval precision and arithmetic work are part of the contract; measured total runtime, bit-operation, financial and energy costs are unavailable.

[Horizon prior art](package/storage_horizon/HORIZON_PRIOR_ART.md) credits cyclodissipativity and turnpike mechanisms. [Spatial prior art](package/storage_spatial/PRIOR_ART.md) compares effective extrema, heat localization and variational polynomial optimization. Primary-source readings are attributed to the supplied research; this integration did not independently repeat that literature audit. The separate [sign certificate](package/storage_horizon/ROBUST_STORAGE_SIGN.md) is conditional on a paid endpoint-tail envelope and does not evaluate the storage value.

## Provenance and portable versions

Research source pin: `a6190a1083f688a7e4bf64adbc5244ef150ff2c4` (PR96). Integration base: `33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d` (PR97).

The exact supplied archive was `Astra_storage_integration_2026-10-15.zip`, 78,519 bytes, SHA-256 `1a9d0397ece268afc78b5df3726ace53ebff0c90a88c4a60b1952522bca70301`. Direct Library transfer was blocked. Its 23 UTF-8 files (182,122 bytes) were transferred through Git in seed commit `8ff1d6489f8e917f72bb776b59e25759148b0c6a`; every file was verified against [TRANSFER_MANIFEST.json](package/TRANSFER_MANIFEST.json). The archive hash is supplied provenance, not a local rehash of inaccessible ZIP bytes.

The transfer manifest describes the immutable **seed**, not the edited working tree. Original file bytes remain recoverable with `git show 8ff1d6489f8e917f72bb776b59e25759148b0c6a:<repository-relative-path>`. Portable integration versions replace private/stale paths and assistant bookkeeping, add evidence boundaries, and replace three duplicate receiving documents with pinned repository-source pointers. Those duplicates match existing PR96 sources apart from terminal whitespace. Scripts, certificate and supplied receipts are unchanged. [INTEGRATED_MANIFEST.json](INTEGRATED_MANIFEST.json) hashes final package bytes; [EVIDENCE_REFS.json](EVIDENCE_REFS.json) records exact proof ranges.

The received certificate's original hash differs from the older quoted hash by exactly one extra terminal newline. Its original bytes are preserved; the replay verifies both the rational data and normalized digest. This is not an algebraic discrepancy.

## Verification

From the repository root:

```sh
python3 updates/FW-storage-computability-20261015/validate_intake.py
python3 frontier/build_access.py check
python3 frontier/test_access.py
```

The intake validator checks seed provenance, final hashes, portable links, scoped preservation of old records, and all three own standard-library scripts in a temporary copy. Each generated receipt must equal its supplied receipt. The three scripts are `heat_certificate/replay.py`, `heat_certificate/coercivity_replay.py`, and `storage_spatial/verify_resource_bounds.py`; direct execution writes receipts beside each script.

[VALIDATION_RECEIPT.json](VALIDATION_RECEIPT.json) records actual commands and failures. Exact arithmetic is finite evidence, not external mathematical validation. One N866 result card, reciprocal notices on N850/N860 and two new open gates provide routing; all PR97 claims and pre-existing gates are retained. No checkpoint or physical-technology record is promoted.
