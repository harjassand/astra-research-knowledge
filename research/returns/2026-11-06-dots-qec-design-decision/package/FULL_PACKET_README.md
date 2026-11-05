# Model-conditioned surface-code design decision

**Select d23 from the fixed candidate set {19,21,23}.** The exact-rational p=.001 rotated-memory-Z experiment, T=d, and specified single-basis integer-cost MWPM decoder meet a terminal block-error target 10^-12 at d23 while d19 and d21 are rejected. The standalone three-candidate family has at least 99.9% simultaneous coverage under its explicit model, minimum-weight decoder and ideal-independent-bit assumptions.

Read qec_design_direct_20261105/REPORT.md first, then THEOREM.md, PRECOMMIT.md and DECISION.json. Exact input graph/table/source hashes, raw outcomes, inspected batches, resource receipts, full source and independent audits are included. The d21 sample is inherited fixed-shot evidence with a newly widened interval; d19/d23 are fresh anytime-valid experiments.

This is smallest only among the specified three candidates, not all distances or architectures. It is a specified memory-Z terminal parity event, not arbitrary-state quantum memory, a full logical Pauli-channel bound, an any-failure-during-block event, a per-cycle rate or hardware reliability. No best-incumbent performance or new-estimator-principle claim is made.

## Confidence and history

Each candidate receives alpha=1/3000. New d19/d23 sequences are inspected at fixed 250-trial batches under an all-time-valid beta-mixture confidence sequence; d21 uses exact fixed-shot Clopper-Pearson on its original precommitted 10,000 samples. All error intervals include graph-model conversion and dyadic rounding.

Additional constructors/history are not silently covered by this standalone allocation. The unchanged direct-family traces also support alpha=1/6000 each (total .0005), retaining the d23 pass; MULTIPLICITY_ADDENDUM.json provides separately labeled exact endpoints. The alpha=1/9000 evaluation is inconclusive at d23. No new sampling was done for these addenda. statistical_history_inventory.json in the independent-audit directory records known parallel/history evidence; it is not independent repetition of this operation.

RECORDED_FAMILY_CONFIDENCE.json supplies a separate completion allocation covering the enumerated ten-interval report family: fresh d19/d23 each1/6000; both historical d21 intervals and the other constructor's six distance-by-method intervals each1/12000; total .001. Under that allocation the direct d19/d21/d23 decisions remain reject/reject/pass, with d23 upper9.88298197899e-13. This global coverage statement is conditional on the inventory being exhaustive. The original preregistration is unchanged.

## Environment

Python 3.12.14; numpy2.3.5, scipy1.17.0, pymatching2.4.0, stim1.16.0. requirements.txt pins these. The optional portable full-pipeline resource wrapper additionally needs psutil7.2.2. A C++17 compiler named g++ is required for rebuilding/auditing integer certificates. OpenBLAS/OMP threads were set to1 in production. No network or private data is needed after dependencies are installed.

Run from this release root. Set MPLCONFIGDIR to a writable temporary directory if the default user config directory is read-only.

## Verify and reproduce

First verify every release byte:

    sha256sum -c RELEASE_SHA256SUMS

Fresh stopped-sequence deterministic replays with all-look endpoint and original detector/L0 checks:

    python qec_decision_independent_audit_20261105/check_sequential.py

Full-denominator integer-table checks and distance-potential checks:

    python qec_decision_independent_audit_20261105/check_fresh_certificate.py --distance 19
    python qec_decision_independent_audit_20261105/check_fresh_certificate.py --distance 23

Every original physical channel checked via independent forward packed-Pauli propagation:

    python qec_decision_independent_audit_20261105/check_fresh_projection.py 19
    python qec_decision_independent_audit_20261105/check_fresh_projection.py 23

Inherited fixed-shot d21 confidence and physical operation counts:

    python qec_decision_independent_audit_20261105/audit_decision.py
    python qec_design_direct_20261105/assemble_result.py

Direct fresh statistical replay alone, using supplied certified tables:

    python qec_design_direct_20261105/sequential_decision.py --distance 19
    python qec_design_direct_20261105/sequential_decision.py --distance 23

Expected terminal counts are d19 n750/k8 and d23 n3000/k6. Replays overwrite result/log files and timings, so perform them on a separate extracted copy. Identical seeds reproduce the same trajectories, not additional independent observations.

A portable full cold rebuild and replay wrapper is supplied:

    python qec_design_direct_20261105/reproduce_pipeline.py --distance 19
    python qec_design_direct_20261105/reproduce_pipeline.py --distance 23

It invokes the current interpreter and requires psutil. The original run_pipeline.py preserves the original interpreter path for provenance; use reproduce_pipeline.py in another environment. Floating tables are only proposals. Exact integer certification is mandatory; a changed valid proposal can preserve law but change fixed-seed trajectories.

## Costs and audit scope

New acquisition-through-decision pipelines cost99.89s (d19) and270.86s (d23), continuously timed per job and run concurrently on a shared host. The historical full d21 operation cost232.76s as a sum of separately timed stages. See receipt details before adding them or interpreting latency. Peak observed stage process-tree RSS was825.88MiB. These are measurements, not runtime/memory complexity guarantees. CPU time was not recorded for the original two new pipelines; no CPU cost claim is made. Verifier timings and clean-extraction CPU/wall/RSS are recorded separately where available.

Research/development, provenance assembly and packaging are disclosed separately and not claimed free. One initial resource-wrapper launch failed before any acquisition/sampling because psutil was absent from the chosen interpreter; the monitor was then run with the existing host interpreter while all scientific subprocesses retained the pinned scientific interpreter. No partial samples or counts from a failed launch were used.

The historical acquired operation, its proof and audited primitive source are retained under their original directory names. Generated compiler binaries and redundant binary intermediates are omitted; the supplied sources regenerate them. Existing upstream manifests are provenance records for their original packet. RELEASE_SHA256SUMS is authoritative for this assembled release. The authors and upstream dependency licenses retain their respective rights.
