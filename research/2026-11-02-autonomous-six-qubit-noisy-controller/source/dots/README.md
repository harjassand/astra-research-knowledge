# Autonomous quantum protection with physical small-qubit controllers

2026-11-01. Ordinary proof and code package. This extends, rather than replaces, the previously delivered noisy-witness memory construction.

## What was constructed

At the specified engineered Lindblad-generator level, syndrome acquisition and classical correction now run autonomously using operations on at most six physical qubits at a time. The clocks, probes, cached syndrome bits, Boolean wires and correction flags are included as noisy physical systems. There is no trusted external timing service, perfectly reliable collision flag, or primitive that directly reads an entire stabilizer.

The key change is to allow probes to overlap and produce wrong reports. An exact finite-clock Poisson potential pays their actual overlap occupation. A separate physical sorting process repairs malformed clock states. These mechanisms join the earlier protected-memory proof with a strictly positive, size-independent formal noise-admission region. The whole mathematical join received a separate internal review; the review's assumptions and limitations are included.

## Meaning and limits

This removes an essential implementation assumption from the formal autonomous-memory route. It is NOT a civilisation-level breakthrough, a practical quantum-memory demonstration, an economical threshold, or a proved advantage over active correction with the same hardware.

The construction still requires the particular admitted Tanner-code family, finite but potentially enormous apparatus and rate constants, non-Euclidean code wiring, actual reset/readout reservoirs, ideal encoded input and ideal terminal decoding. The local six-qubit dissipative operations are specified engineered primitives; a microscopic two-body Hamiltonian/reservoir realization is not supplied by this theorem. Physical errors of the faster repair apparatus must satisfy the actual bound after all rates are chosen.

## Read in this order

1. `NATIVE_DILUTE_SENSOR_MEMORY_JOIN.md`: complete joined theorem, physical primitives, rate hierarchy, protected logical interface and output bound.
2. `audits/NATIVE_DILUTE_SENSOR_WHOLE_RECEIPT.md`: separate whole-theorem review, including exact scope.
3. `construction/07_dilute_sensor_closed_join.md`: explicit source/Boolean prices and rate-density inequalities.
4. `construction/FLAG_FREE_SOURCE_ADMISSION.md` and `SMALL_QUBIT_SENSOR_CLOCK_RECEIPT.md`: actual quantum source and physical clock construction.
5. `audits/KILLED_SUBCHANNEL_RECEIPT.md` and `NONCOMMUTING_SENSOR_CONDITIONAL_THEOREM.md`: general comparison and exponential-potential tools. Their earlier pending-source language is resolved only by the later whole-theorem receipt.
6. `foundation/`: the prior delivered construction, assumptions, source comparisons, costs and failures, preserved unchanged.
7. `comparisons/`: strong active, synchronous and passive alternatives. No exhaustive historical novelty claim.

The root proposal is preserved in `history/`; its pending checks are superseded only where the later receipts explicitly close them. Failed collision-flag and transaction approaches are retained as scientific history, not accepted parts of the final controller.

## Verification and replay

The mathematical proofs concern arbitrary coherent physical states in their stated admission, not just classical simulated trajectories. The finite checks supplement those proofs:

- 16,380 exact clock configurations, M=1 through 12: legal guards, endpoints, injectivity, inversion repair and bounds.
- 180 numerical own/pair/detector Poisson cases, including return phases.
- 4,096 numerical verifier configurations.
- 12 additional numerical pair-clock tests.
- An exact rational counterexample showing why full J-dagger-J logical flatness is necessary.

Run the individual Python scripts in `tests/` with Python 3, NumPy and SciPy; the foundation also uses SymPy. Run from that directory. Numerical matrix/tolerance checks are not exact rational verification, despite any older script print labels. No tests are laboratory experiments or practical memory-lifetime benchmarks.

## Outcome standard

The next capability gate is a useful microscopic implementation and a matched-resource comparison against scheduled extraction. A collection of increasingly elaborate formal components is not enough: the complete apparatus must enable protection at worthwhile physical noise, cost, geometry and operating rates.
