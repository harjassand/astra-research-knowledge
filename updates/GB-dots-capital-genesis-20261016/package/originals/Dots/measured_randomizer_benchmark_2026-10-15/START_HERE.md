# Measured randomizer benchmark: audited portable packet

## What this is
A small, authentic aggregate-count interface for Ware et al.'s superconducting Pauli-frame-randomization experiment, plus a **separate** IBM deterministic-DD reference condition. Original data and licensed source snapshots are preserved unchanged. Start with INDEPENDENT_AUDIT.md, then README.md for the detailed scientific source report, and HANDOFF.md for exact use restrictions.

The Ware experiment compares compiled randomized and unrandomized realizations of the same nominal circuits at equal physical pulse budget. **It does not add physical randomizer pulses.** Every nonempty Clifford uses the paper-reported two 50 ns X(pi/2) pulses plus virtual Z updates in either arm. It is therefore not an evaluator of added-randomizer-rate cost or benefit.

## Reproduce
Python 3.10+ and its standard library suffice. No dependencies, network, account, installation, or author-code execution are needed. From this extracted folder:

    python replay.py

The runner verifies MANIFEST_SHA256.json, copies the packet to a temporary directory, executes only the two newly authored audit scripts, compares six saved outputs byte-for-byte, checks all original files remained unchanged, rechecks the source packet, and deletes the temporary copy. A PASS log is recorded in REPLAY_STATUS.txt. Running validate_counts.py or independent_audit.py directly writes their small outputs beside the script; use replay.py for a read-only packet workflow. Do not run make_provenance.py over the packet: the acquisition provenance is intentionally frozen.

## Verified result
- 14 Ware files × 3,505 matching ordered keys × 1,000 outcomes; 49,070,000 represented measurements.
- 27 exact pure-power keys × seven paired runs = 189 rows. All counts and descriptive means/ranges independently reproduce. No new fit, test or holdout claim.
- Gx32 mean return: 0.3853 → 0.7230; Gy32: 0.3780 → 0.7160. Gi128 worsens: 0.7156 → 0.5490. These are observed fractions, not a universal improvement or a mechanism estimate.
- Minus is the verified |0> return outcome under the pinned pyGSTi convention.
- Released maximum expanded length is 1,030, not the paper-reported 6,155; coverage remains unreconciled. pyGSTi's total-germ-length semantics are verified. The packet claims only its released subset.
- QGL's pinned 2018 source matches the compiler construction but is not authenticated as the acquisition revision.
- The same 1,000 precompiled randomized variants were each measured once per run and reused over seven runs according to the notebook. Actual acquisition seeds, shot ordering, private randomness, and executed waveforms are not available here.

The small IBM XY4/free condition has different hardware, deterministic controls, jobs hours apart and an exact-padding source ambiguity. Never blend it with Ware as a single calibration or matched randomizer experiment.

## Contents and integrity
README.md and provenance.json retain the acquisition report and its original hashes/URLs. INDEPENDENT_AUDIT.md is the independent review. The two CSV exports give the complete selected comparison; selection_rule.json explicitly identifies previously inspected examples and denies pristine preregistration. Source folders retain necessary copyright/license notices. LICENSES_AND_PROVENANCE.md maps components to their notices.

MANIFEST_SHA256.json governs the whole portable packet, except itself and the replay log. provenance.json covers the original 61 acquired/derived files; additions are governed by the packet manifest. No original research file was silently rewritten. No full primary-paper PDF, HTML or text, unused ZIP archive, compiled binary, private note, or credential is included. Third-party source is for reading only.

## Missing experiment
A controlled physical-randomizer-rate study must vary actual added pulse count/rate at fixed task and elapsed time, publish executed schedules and shot/frame timing, and include zero-added-control and strong deterministic DD. The present packet cannot identify that missing rate response, a joint bath norm, a CP fault-process theorem, or a decoder threshold.
