# Stronger conventional control baseline: synthesize only occupied columns

2026-10-29 UTC. This supersedes the full-unitary circuit COST for the three recorded sample receivers, not its correctness or its saved source. The underlying finite rational synthesis method and physical-interface limitations in FINITE_POVM_CONTROL_INTERFACE_v3.md remain governing.

The ancillas start00, so only two of the eight Naimark input columns are ever occupied. There is no need to build and compile an entire arbitrary unitary completion. `thin_isometry_receiver_v4.py` applies13 Givens eliminations to the8-by-2 stacked-square-root isometry, retains only its two input-column phases, and reverses those operations. The resulting15 rational two-level/phase gates form a complete unitary circuit, but its action on the other six input columns is deliberately unconstrained. Exact output effects and exact controlled-primitive compilation are rechecked from scratch.

Each of the same three learned receiver POVMs now uses31 controlled primitives, expanded to248 CNOTs and646 rational single-qubit gates:894 local gates rather than1,928. Exact correction-channel half-diamond upper bounds including local-gate approximation are3.915e-13,4.277e-13,4.049e-13. This demonstrates why comparison against an equally informed conventional isometry compiler matters: the earlier full-unitary construction was needlessly expensive. It does not establish that894 is optimal or practically competitive.

The conditional physical budget is correspondingly

nu <=4.277e-13 +248 delta_CX +646 delta_1 +epsilon_prep +epsilon_readout +epsilon_storage +epsilon_Pauli +epsilon_private_coins,

for the tested circuits, with valid composable worst-case primitive errors. The quoted numerical bound is a rounded-up presentation of the exact rational values saved in thin_isometry_receiver_v4.json. It excludes unknown actual-device calibration, duration, energy and leakage. No hardware, new source call, or complete online physical trajectory was executed. Further synthesis optimization and actual control validation remain open.
