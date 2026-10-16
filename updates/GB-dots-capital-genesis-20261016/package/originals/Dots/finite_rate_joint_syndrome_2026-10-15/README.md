# Finite-rate joint syndrome theorem packet

Start with HANDOFF.md. All claims concern the mathematical generators and measurements explicitly specified in the documents. No experimental outcome data is included or analyzed here.

## Read in order
1. HANDOFF.md: conditional scheduled-memory extension, evidence and remaining physical qualification.
2. tracked_control/SCHEDULED_MEMORY_COMPOSITION_GATE_AUDIT.md: exact budget substitution, geometric/private-clock separation, and optional bounded-update cap.
3. tracked_control/DIRECT_FOURIER_INDEPENDENT_AUDIT.md: audited global effect theorem and virtual seed-qubit proof.
4. prior_inputs/: the prior scheduled theorem/audit and support contract on which the memory conclusion depends; its README identifies omitted larger imports.
5. tracked_control/REPORT.md and INDEPENDENT_AUDIT.md: ideal tracked full-Pauli clean-interval interpretation, with private-seed/support restrictions.
6. joint/REPORT.md and independent/: simultaneous endpoint block-norm theorem and separate endpoint/grouped audits.
7. joint/DYSON_CONSTRUCTION.md, PRIOR_ART.md and BRIDGE_PRIOR_ART.md: construction provenance and bounded primary-source comparisons, including closest continuous-process precedent He Wang 2610.01521v2; novelty unresolved.
8. single/DERIVATION.md: exact one-parity channel and arbitrary-bath finite-rate bound.
9. scope/ENDPOINT_FLAGS_MISS_LOGICAL_HISTORIES.md: why untracked endpoint syndrome flags alone do not certify logical support.
10. tracked_control/FOURIER_INTERFACE_ADDENDUM.md: separate additive-private-sign lemma and required physical interface.

## Offline replay
An existing Python3 environment with NumPy and SciPy is required. No packages are installed and no network is used.

Run: python replay.py

The replay copies check scripts into a temporary directory, reruns their assertions and compares their numerical results with the saved outputs. It leaves the packet unchanged. REPLAY_RESULT.json records the actual packaging-time replay. Default scripts cover scalar channels, serial measurement bounds, local group majorants, independent grouped effects, independent endpoint effects, the five-qubit logical obstruction, the tracked-control bridge, and direct global Fourier/virtual-seed effects.

Optional: python replay.py --search

This also reproduces the 3,600-instance bounded searches and compares their saved results. Random seeds are fixed. The search is supporting evidence only. Performance depends on the machine; original search-only CPU was under6 seconds. See REPLAY_RESULT.json for the actual final replay time.

To record a new replay in this directory, add --record; this changes REPLAY_RESULT.json and hence invalidates its original manifest entry. SHA256SUMS.txt covers every distributed file except itself. Verify it before replay with: sha256sum -c SHA256SUMS.txt

## Contents and exclusions
Small derivations, independent audits, source links, check scripts, JSON/text results and tiny representative matrices are included. No installs, private communications, raw measurement data, superseded proposals or large artifacts are included. Scripts use local relative paths and temporary outputs. The original narrow sharp-ε product question is explicitly unresolved; the proven q-factor endpoint theorem is separate.
