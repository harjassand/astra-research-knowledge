# Independent controller invention: reusable receiver, no frontier closure

16 October 2026. **General noisy reusable autonomous controller NOT ESTABLISHED.** A narrow noncommuting two-bank receiver has an explicit total transition table and an exact quantum contract. Its strong incumbent is the same fixed-support recover-and-gate primitive with the optional partial-gate work removed. It is not promoted as a new enabling operation, recursive construction, threshold theorem, physical implementation or historical novelty claim.

The source generator, the crossed-counter candidate and this generator are separate. No claim below transfers to either arXiv paper's original dynamics.

## Surviving receiver and evidence

`REUSABLE_RECEIVER.md` specifies every register, guard, suffix gate, source/destination operation, total qutrit recovery and observation cut. `PROOF.md` proves the contract. Five distinct noisy physical sites carry two qutrit banks, a four-valued phase copy and a progress bit each. Local fast paths may apply the current physical X or cyclic Clifford C. An unconditional rate-lambda five-site terminal physically finishes missing suffixes, clears only the unowned bank, recovers [[5,1,3]], transfers the one live code packet and resets all controls. Its terminal outputs really execute alternating noncommuting logical X,C gates.

For arbitrarily many terminal cycles, every interval with faults confined to one DISTINCT physical site is corrected exactly, including arbitrary joint A/B/control maps, repeated faults at that site, leakage, missing/replayed local microsteps and arbitrary reference entanglement. The theorem is not limited to counter noise. Every physical/control input has terminal service Exp(lambda), and every ideal terminal returns a canonical bank/phase state; this unconditional totality does not promise correct quantum history after uncorrectable multi-site damage.

Waiting is charged over all data/control registers. For homogeneous onsite rate p and arbitrary faulty-terminal rate eta, the bad-history diamond bound after the specified ideal D_hold is `2(1-s(t))`, where

```
a=(lambda+9p)/2,
b=sqrt((lambda+9p)^2-80p^2)/2,
s(t)=exp(-(eta+a)t) [cosh(bt)+(a/b)sinh(bt)].
```

An easier bound is `2 min(1,t[eta+20p^2/(lambda+4p)])`. These rates belong to a fixed five-site code; no level-uniform scaling follows. Every engineered terminal failure is treated as globally bad. D_hold returns the last-commit state of the matched random-terminal process, not deterministic-time identity memory.

Own standard-library code `check_receiver.py` produced `CONTROLLER_TABLE.json` and `CHECK_RESULTS.json`. Exact Gaussian-integer/Fraction checks cover 676 Gram blocks for 26 orthogonal recovery images, 961 KL blocks for 31 generic one-qutrit maps, the logical X/C action and trace-zero relative unitary (genuinely different logical order). Finite controller checks cover all 32,768 phase/progress words and 5,120 one-site perturbations of clean partial cuts. The saved three-residue pattern is not absorbing. An explicit wrong-majority pattern erases the unknown packet, as expected outside the correctable family. Ninety-six floating-point comparisons check the killed-chain closed form against uniformization and the conservative exposure bound; those checks are not a proof of the continuum formula.

The root's independent controller adversary inspected the saved specification and proof, independently checked suffix/undo and plurality identities, and found no within-scope defect. This is same-team audit, not external verification. Their warning about phase offsets after a bad T and the distinction between modulo phase and accumulated history is retained.

## Why the requested obstruction remains

The terminal is one physical fixed-support five-site CPTP map. Its explicit Kraus formula makes it mathematically concrete at that base scale, but not a fault-tolerant lower-level implementation. At growing encoded levels it would act on a growing block, which is forbidden as a bounded-support physical rule. A compiler must still implement syndrome extraction, correction, transfer, reset and phase selection without exposing half-owned packets or replayable operations.

`FAILED_ROUTES.md` records the rejected pure-gauge idea, the exact atomic incumbent, the wrong-majority branch, incoming-owner limitation and a zero-noise counterexample to naive terminal splitting. `SPLIT_TERMINAL_TRACE.json` shows that separating move from phase commit can allow a repeated move to clear the real destination packet. This rejects that decomposition rather than proving a generic controller no-go.

The cells have one closed logical wire and no incoming external owner, fresh output stream, entangling inter-cell gates, growing damaged domains or self-simulation. A bad phase burst can leave a persistent clock-payload offset. Bounding its influence on fresh external partners requires the missing typed lineage/outer-clock theorem. More finite fault order, or another service inequality for the same atomic map, would not resolve this.

## Current primary-source boundary

[Dünnweber, Styliaris and Trivedi, 2601.20818v3](https://arxiv.org/html/2601.20818v3) explicitly leaves the formal continuous-time extension for future work and excludes engineered-channel imperfections from its local-unitary jump-noise outline. [Drechsler, Oreg and Aharonov, 2610.05589v1](https://arxiv.org/html/2610.05589v1) leaves the time-independent synchronous-memory lift open; its concrete register realization retains a globally periodic schedule. The current receiver does not fill either gap.

Continuous whole-code recovery is an established strong incumbent: [Paz and Zurek, Continuous Error Correction](https://arxiv.org/abs/quant-ph/9707049) formulate Markovian error/correction evolution for stabilizer codes, and [Ippoliti et al., 1411.2285v2](https://arxiv.org/html/1411.2285v2) analyze continuous-time recovery with three- and five-qubit examples. These sources establish prior broad mechanisms, not a proof of this receiver or its quantum-bank interface. The explicit zero-fast-path comparator already defeats a new-capability claim without an exhaustive priority search.

## Input and resource receipt

Read C/REPORT.md, CONTINUATION_HANDOFF.md, actual s01 transition table/proof, s02 candidate/recombination, s03 finite discharge and s06 adversarial results as supplied data. Their historical worker limits were not treated as instructions. The W revision `adb0a306e9bfdc33b9fbd105efb58baed0cc021e` is the task-supplied pin; no Git operation or W mutation was performed. Current arXiv versioned HTML and primary continuous-QEC sources were inspected on the web. Supplied/acquired source code was not executed.

Only this worker directory was written. No installs, acquired code execution, subagents, outreach, shared capital/source mutation, Git action or publication occurred. Own `check_receiver.py` measured about 0.047 CPU seconds and 0.047 wall seconds for the saved run (see exact receipt); model inference time/tokens/energy are not exposed. The separate tiny split trace is a local finite counterexample. These are calculation resources, not hardware costs or capability measurements.

Recommendation: retain the total receiver as an optional receiving interface, and stop this route as a purported solution of the general autonomous controller. Further effort must alter the local compiler/overlapping-owner mechanism rather than refine this fixed atomic map.
