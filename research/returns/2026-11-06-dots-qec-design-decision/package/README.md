# Surface-code sizing: compact proof and source packet

**d23 is the smallest passing member of the fixed candidate set {19,21,23}** for the specified memory-Z circuit, all four stochastic noise parameters exactly1/1000, T=d, and the frozen single-basis integer-cost MWPM decoder, at terminal block-failure target10^-12.

The separate conservative recorded-family allocation gives d19 lower1.99685e-12, d21 lower1.52253e-12 and d23 upper9.88298e-13, at joint confidence at least99.9% conditional on the recorded decision-eligible history being exhaustive. The original precommitted three-candidate results are preserved unchanged. See RECORDED_FAMILY_CONFIDENCE.json, the confidence ledger and independent audit.

This is a **model-conditioned sizing result**, not hardware reliability, full logical quantum-memory reliability, a per-cycle bound, or overall minimum distance. It makes no novelty claim for sequential profiling and no performance superiority claim over the best applicable incumbent.

## What is included and omitted

Included: decision proof; frozen circuit/graph inputs; full original scientific source and independent-audit source; original and adjusted exact intervals; all inspected batches and outcome counts; original precommit hashes; model/decoder contract; cost receipts; history inventory; audit summaries; dependency pins; table-regeneration instructions and preserved expected table digests.

**Large precomputed arrays, floating table caches, intermediate binary files, compiler binaries, and MCMC trajectory arrays are intentionally omitted.** Statistical/table replay therefore requires regeneration first. This packet alone can check the mathematical interval/decision evidence and original physical-channel projection, but cannot immediately execute an unchanged certified-table sampler until the arrays are rebuilt. The complete archival packet remains qec_design_decision_release_20261105.zip, SHA256 555438d2ed23e631867e88e7e406decc65277255ce4e0ab14525ebfdb7bf6c0b.

Start with qec_design_direct_20261105/REPORT.md, THEOREM.md, PRECOMMIT.md and DECISION.json. The original standalone family uses alpha=1/3000 each. The completion addendum accounts for ten enumerated intervals with exactly .001 total error and preserves the same sizing decision.

## Validate compact inputs

From this root:

    sha256sum -c COMPACT_SHA256SUMS
    python regenerate_tables.py --check-only
    python qec_design_direct_20261105/test_confidence_sequence.py
    python qec_design_direct_20261105/assemble_result.py

These commands do not require precomputed tables. They may rewrite local receipt/timing files; run on a separate extracted copy.

## Regenerate the frozen tables

Use Python3.12 with the pinned requirements.txt, a g++ C++17 compiler, and a writable working copy. A few hundred MiB of disk and roughly1GiB of memory are needed. Measured construction time was minutes, not a guaranteed runtime. No network is needed after dependencies are installed. Set MPLCONFIGDIR to a writable temporary directory if necessary.

    python regenerate_tables.py --distances 19,21,23

The script starts from the included hash-verified graph for each distance, rebuilds the floating proposal and exact integer certificate, and verifies every table digest, exact normalizer and TV bound against expected_frozen_parameters. Those expected records are retained separately before rebuilding can overwrite operational metadata. If the platform yields a different valid table, the script stops rather than claiming the original trajectory was reproduced. An independently certified different proposal can still be a valid new experiment, but that is outside this fixed-evidence reproduction.

After successful regeneration:

    python qec_decision_independent_audit_20261105/check_sequential.py
    python qec_decision_independent_audit_20261105/check_fresh_certificate.py --distance 19
    python qec_decision_independent_audit_20261105/check_fresh_certificate.py --distance 23
    python qec_decision_independent_audit_20261105/check_fresh_projection.py 19
    python qec_decision_independent_audit_20261105/check_fresh_projection.py 23
    python qec_decision_independent_audit_20261105/audit_decision.py

Expected stopped traces: d19 8 accepts in750 trials, d23 6 in3000. The historical d21 tuple evidence has55 accepts in10000 fixed shots. Identical-seed replay is verification, not a fresh independent sample.

## Costs and scope

Fresh acquisition-through-decision pipelines:99.89s for d19 and270.86s for d23, run concurrently on a shared host, with peak observed stage process-tree RSS825.88MiB. The inherited d21 full stages cost232.76s, not free cached setup. Their sums are not one uninterrupted benchmark. Review, development and packaging are separate; review timing and caveats are in REVIEW_COSTS.json. The original new pipeline CPU time was not recorded. The full archive's clean replay has separate CPU/wall/RSS receipts.

Read FULL_PACKET_README.md for additional historical context. Its immediate replay commands assume the full packet's tables and must follow regeneration when used here. Historic upstream manifests describe the larger original packets; COMPACT_SHA256SUMS is authoritative for the files actually included here.

The latest completed same-graph d21 conventional comparison is documented in MATCHED_CHALLENGER_ADDENDUM.md. Its diagnostic estimate agrees in scale, but all31 IAT screens remained unresolved and it does not provide certified coverage or a matched-accuracy speed comparison.
