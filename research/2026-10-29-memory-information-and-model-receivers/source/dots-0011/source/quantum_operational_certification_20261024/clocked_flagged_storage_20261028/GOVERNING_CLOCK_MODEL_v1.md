# Equal-elapsed-time clocked flagged storage, version1

28 October2026. Deterministic finite-dimensional channel model; independent review pending. This is a successor to, not an overwrite of, the received ideal-idle calculation. No hardware parameters, lifetime guarantee, optimal-code advantage or threshold are claimed.

## Fixed clock and fair elapsed time

Native source plus its previously acquired inverse form one declared phase of duration2 reference units, with five encoded sites operated in parallel. Its complete effective channel is the frozen earlier native-plus-learned-inverse map; no additional memory noise is added inside that phase. The same phase is used by each unencoded site baseline. The separate background process below applies during the additional controller/recovery window. This is a two-mode phenomenological model, not an inference that the two rates arise from the same material mechanism.

Clock parameters are dimensionless illustrative ratios:

| Operation | Default duration |
|---|---:|
| Single-qubit H or correction-site window |1|
| CX |2|
| Ancilla reset/preparation |2|
| Measurement |4|
| Classical readout/feedback slot |1|

A flagged window contains6CX,4H,2preparations,2measurements,2readout slots: duration30. An unflagged window contains4CX,4H,1preparation,1measurement,1readout: duration19. Every round reserves4flagged windows,4fresh-syndrome windows and5correction-site windows, total **201 controller-window units**, or203 including the common native/inverse phase.

Disabled adaptive windows **physically wait** for their full duration. They do not receive the earlier mathematical zero-duration bypass. The unencoded baseline experiences precisely the same201-unit memory interval after its native/inverse phase. Five encoded source calls versus one baseline-site source call, and seven versus one physical qubits, remain distinct resource costs. This is elapsed-time matching, not an assertion of equal hardware/resource cost.

Changing measurement duration to1 or16 changes controller-window duration to165 or345 respectively. These cases use a common background rate0.0001 per reference unit, so longer waiting is genuinely charged rather than renormalized away.

## Background-memory and gate-noise channels

During each interval of duration d, every **live** qubit, including active-gate supports, receives independent Markovian Z dephasing

    D_d(rho) = [(1+exp(−lambda d))/2] rho
             + [(1−exp(−lambda d))/2] Z rho Z.

Data qubits are always live. Ancillas become live at reset/preparation and cease to be live at measurement; their dephasing acts throughout intervening gates, preparation of the other ancilla and feedback waits. Disabled whole check windows have no live prepared ancilla, but still expose all five data qubits. Applying the background process also to active gate supports avoids giving artificial immunity to a qubit simply because a gate is scheduled on it.

This is an explicitly ordered discrete CPTP model: ideal gate and fixed systematic coherent overrotation occur at the beginning of an operation interval, followed by its background dephasing. Native preparation is followed by its coherent Y error and the interval's dephasing. For a measurement, background dephasing occurs before its coherent basis misalignment and terminal projective readout. Readout/feedback slots contain only background exposure on the still-live qubits. No continuous pulse Hamiltonian or commutation with its environment has been inferred.

The fixed coherent angle is eta=0.001 radians in this sweep. CX receives a post-gate ZZ rotation; H a post-gate X rotation; preparations Y rotation; syndrome measurement Y and flag measurement Z basis rotation; nonidentity correction Pauli a post-gate X rotation. These are the earlier model's declared axes, not optimized against the clocked data. Classical decisions/readout values are otherwise trusted. The acquired inverse's additional hardware synthesis error remains ideal/unmodeled, apart from its existing calibration mismatch.

The sweep varies **integrated background strength lambda times controller-window duration**, not a claimed experimental error probability. The distinction matters: the single-qubit Z-error probability over that whole free interval is (1−exp(−lambda tau))/2.

## Actual adaptive instrument and complete controller

The early-exit syndrome/flag decisions and physical corrections are unchanged. After a stop, the remaining flagged windows expose data to the background channel; then the full fresh pass occurs. If all flags and syndromes are trivial, the fresh-pass window is skipped but its elapsed time exposes data. All five correction-site windows elapse, including identity choices. Undefined multi-fault flag/syndrome pairs use the declared ordinary weight-one fallback, without postselection.

The program constructs each6/7-qubit noisy check as a real Pauli-transfer map, explicitly retaining the ancilla coordinates until its outcome contraction. Independent dephasing multiplies each Pauli word by exp(−lambda d times its number of X/Y factors on live qubits). Clifford and coherent operations act through their local Pauli-transfer matrices. Branch maps compose into a complete1024×1024 physical-data transfer matrix. Physical Pauli-coordinate state vectors, not decoded logical states, are carried between all rounds.

The noiseless-background full transfer matrix at eta=.001 agrees with the separately constructed193-Kraus earlier instrument on **all physical operators**, max-entry difference6.11e−15. At eta=0 and zero background it agrees with the full CPTP idempotent reset P, max-entry difference5.00e−15. These are author cross-representation numerical checks, not independent review of nonzero background.

The old751 potential-location count must not be reused blindly for this new timing/noise model: its disabled windows now expose data, active supports receive background noise, and all five correction windows elapse. The present numerical channel calculation is valid by its explicit CPTP composition, not by promoting the earlier single-fault receipt to an unreviewed timing theorem.

## Comparators and open interfaces

`same_elapsed_unencoded` records the fixed acquired inverse baseline over the same elapsed window. It is not the best possible unencoded decoder: a horizon-specific final correction can undo part of accumulated calibration rotation. A separate source-informed full-CPTP endpoint oracle and a budget-aware direct endpoint acquisition are being assessed in `endpoint_oracle_acquisition_20261028`; neither grants source parameters to the original learner. Ordinary coding can outperform a single qubit by spending redundancy and controls, so that alone is not a new scientific mechanism.

Initial unknown-state injection, physical terminal decoding/readout, actual gate synthesis, bath memory, crosstalk/leakage, continuously acting pulse dynamics, controller failures and hardware energy/timing constants remain separate obligations. Every result here is a deterministic numerical evaluation of the declared closed model, not new acquired measurements or a certified diamond bound.
