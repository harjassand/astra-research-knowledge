# Overlapping finite weak pulses

This separate packet contains the composed scheduled finite-duration theorem, its completed independent internal audits, the chronological counterexample, and exact/numerical certificates. Begin with HANDOFF.md, then classical/SCHEDULED_FINITE_DURATION_MEMORY_THEOREM.md and classical/SCHEDULED_THEOREM_INDEPENDENT_AUDIT.md. Earlier delivered packets remain unchanged.

## Mathematical distinction

A small chronological conditional bad-label bound is false for crossing weak pulses sharing a bath. The exact echo example produces conditional probability 9801/10201 after a rare earlier outcome, despite small integrated pulse strengths. This does not refute the earlier atomic-post-error theorem or every possible correlated-fault estimate.

A different global statement can hold. For a deletion-stable privately framed Hamiltonian H_g(t)=H_0(t)+Σ_i V_{i,g_i}(t), with a_i=∫sup_g ||V_{i,g}(t)||dt, the full-horizon Fourier Kraus family obeys

    Σ_{χ: χ_i≠0 for all i∈S} K_χ† K_χ ≤ (Π_{i∈S} a_i²) I.

These are joint subset effects. They neither assert small probabilities after arbitrary label postselection nor create causal Fourier-label records at pulse completions. The mixed-derivative proof has no factorial loss because its ordered insertion domains partition the full integration cube.

The local-stochastic contour route uses specified subsets directly. Under its complete-primitive conditioning premise, a packet-coloring step gives q=(d0+pμ)^(1/Q); a weaker clocks-only premise gives q=(√d0+√(pμ))^(1/Q). Distinct contour sinks are bounded jointly, rather than by multiplying actual marginals or asserting iid domination. The deterministic Toom contour imports remain explicit. The composed theorem connects these statements under one consistent schedule, support and global-good-map definition. Under its exact premises and sufficiently small parameters, it proves a recovered joint-input bound min(2, A L⁴(1+κT) exp(−cL)) for sufficiently large compatible sizes and each deterministic T. The comparison bath map may depend on L and T.

## Substantive implementation premises

- Independent inaccessible private frames with a common full-joint dilation that remains frame-independent after deleting any selected coupling; genuine controllers must obey the same representation under deletion and interpolation.
- Fixed exogenous timing, bounded reservations covering full correction/error/frame/ancilla supports, and cleanliness against every intersecting memory operation. Shared-bath overlap may remain; intersecting memory supports cannot be treated as harmless just because vertex labels differ.
- Exact fresh resets and exact clean correction circuits; gatewise bath independence when correction gates are serialized. Only memory factors are regrouped term by term in the pulse locality argument. Bath factors keep chronological order.
- Only fully completed clean frames are Fourier transformed at deterministic T. Pending/conflicting prefixes remain charged bad operations. Global Fourier labels are unavailable to online control.
- An input-independent good predicate in a legitimate complete global Kraus representation, including every supported coherent Pauli sum. Its CP good map is trace-nonincreasing; bath completion gives the channel comparison.

These are strong modeling assumptions. No arbitrary continuous-noise theorem, faulty clean-control theorem, noisy readout, physical implementation, useful numerical threshold or priority claim follows.

## Contents and dependencies

quantum/ contains the chronological counterexample, global subset lemma and completion-time support proof with their reviews. classical/ contains the local-stochastic contour replacement and audit. prior_art/ distinguishes conventional coherent fault-path norm results, randomized compiling and the current tailored probability interface.

The earlier two delivered ZIPs are separate dependencies recorded with exact hashes in DEPENDENCIES.json. They remain unchanged. Extract all three archives into the same parent directory to resolve cross-packet relative references. Earlier candidate and historical open-gate language is preserved for provenance. The final scheduled theorem and end-to-end audit supply the operative composition status. The separate cancellation-sensitive norm-only restricted-amplitude route remains open and is not claimed solved by this packet.

## Exact and numerical evidence

checks/exact/ contains rational/symbolic crossing-echo, independent causal-measurement, three-pulse subset and memory-only reordering tests. checks/numeric/ contains a seeded floating-point stress test with three Z3 coordinates. Floating-point agreement is an illustration; it does not prove the operator theorem. Neither class computes a memory threshold or verifies the external contour theory.

With Python 3.12 and requirements.txt installed:

    python3 replay.py --exact
    python3 replay.py --numeric
    python3 replay.py

No network or automatic package installation is used. Run with assertions enabled. SHA256SUMS covers every other included file. Run `python3 verify_manifest.py` to check it. Final verification includes fresh-extraction replay, deterministic ZIP rebuilding, and both prior packet hashes. To recheck the earlier ZIPs run `python3 verify_dependencies.py COHERENT_PACKET.zip FINITE_DURATION_PACKET.zip`. To rebuild this archive run `python3 build_archive.py /path/outside/packet/rebuilt.zip`.
