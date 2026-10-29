# Independent review: clocked mandatory-channel model v1

28 October2026. **PASS as a scoped deterministic numerical model**, governed jointly by `GOVERNING_CLOCK_MODEL_v1.md` and `MANDATORY_CHANNEL_SCOPE_ADDENDUM_v1.md`. This is not a passive-memory lifetime, hardware or threshold certification. Original sources and data were preserved.

## Independent density/instrument challenge

The reviewer implemented a different representation:6/7-qubit density matrices, explicit computational-basis gate embedding, entrywise dephasing factors exp(−lambda*d*Hamming-distance) on exactly the live qubits, and immediate measurement projectors. Ancillas are traced out only after all declared operations. This differs from the author's Pauli-coordinate implementation and postponed measurement contraction.

At integrated background0,.01,.1 and eta=.001, all four flagged and four unflagged instruments were checked on a random full-rank physical density operator and an independent arbitrary complex non-Hermitian operator. Every outcome map agrees within6e−17. These tests support, but do not replace, inspection of the channel formulas; they are not exhaustive exact arithmetic proof of every matrix entry at nonzero background.

Using those checked transfer instruments, the reviewer independently composed the complete adaptive branches, physical waiting windows and correction operations, then propagated the actual physical1024-coordinate operators through all32 rounds. At T=1,2,4,8,16,32, saved logical PTMs agree within4e−15. Whole-round TP entry residuals are below6e−15. The zero-background full1024×1024 EC map matches the previously received193-Kraus instrument within6.11e−15. This is complete-superoperator agreement, not a single-codeword check.

Representative T32 encoded infidelities independently reproduced are .06178968105748 at background integral .01 and .63166494438400 at .1. The former is a surviving finite-model regime; the latter is a clear failure regime (even below the Bell fidelity1/2 of feasible classical measure/store/reprepare). Other saved sweep points were bound by the author manifest and inspected for clock consistency, but not all were independently re-simulated in this audit.

## Clock, liveness and conditional semantics

Direct recount gives30 units per flagged window and19 per unflagged window. Four of each plus five one-unit correction windows total201. Including the common mandatory native/inverse phase gives203. Measurement durations1,4,16 correspond to EC durations165,201,345, with the variable-duration studies holding rate fixed rather than integrated error fixed.

All data qubits dephase during every EC interval, including active gate supports. Each ancilla becomes live at its reset/preparation, receives dephasing during its preparation interval and all subsequent live intervals, and ceases exposure after measurement. The still-live flag therefore dephases during syndrome measurement/readout. A formal dormant initial ancilla state is harmless before preparation because no operation touches or exposes it. Immediate-projector density checks confirm that the postponed-coordinate contraction gives the same instrument.

Disabled flagged/fresh windows are real data waits, not the old zero-duration bypass. All five correction-site windows elapse even for identity corrections. The early-exit branch waits through remaining flagged windows before the fresh pass; the all-trivial branch waits through the omitted fresh pass. Deterministic weight-one fallback completes every higher-order flag/syndrome record. The physical map is a bounded composition and sum of complete CPTP instruments, not postselection. Trusted classical dispatch and record retirement remain assumptions.

The prior751-location one-fault budget is not silently transferred: this clock model adds charged waiting and dephasing even on active supports. The native phase is a separate declared effective map lasting2 units; background is excluded there by the two-mode model, not because physical environmental coupling has been proved absent.

## Propagation and comparator scope

The actual physical state, including retained syndrome leakage, is propagated into the next round. Diagnostic ideal terminal decoding does not alter it. Fresh source environments, discarded syndrome records and fixed learned controls define a closed Markovian finite-tile model; unmodeled returning memory is excluded.

For the three replayed cases all fixed-control single-site baseline PTMs match independent powers of the same native/inverse map followed by exactly201 units of dephasing. This is genuinely equal elapsed time under the declared clock, but not equal channel uses, qubit count, control work or energy. Source-informed endpoint-decoder optimality and endpoint-learning budgets are separate review dependencies; this receipt does not certify them. A conventional strategy with the same resources can run the identical standard flagged code.

The mandatory-channel/no-bypass addendum is load-bearing. Each information carrier must traverse the prescribed native link/noise region. Local ancillas cannot carry quantum information around it. Without that task restriction, a passive-memory comparator could use a less-noisy auxiliary qubit, and the claimed comparison would not answer the same question. No laboratory enforcement of the restriction is demonstrated.

## Limits

All precision statements above are floating numerical diagnostics, not outward-rounded diamond certificates or measurements. Gate/preparation/readout/reset durations are illustrative dimensionless ratios. Initial unknown-state injection, final physical decoding, inverse-gate synthesis error, bath memory, leakage/crosstalk, continuous pulse dynamics, classical-controller faults and hardware energy remain open interfaces. No global threshold, generic environment-independent recovery or new-code superiority follows.
