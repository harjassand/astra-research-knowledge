CAUSAL RECOVERY FROM THE HOMOGENEOUS TRACIAL PARTIAL-SWAP STREAM
Research return, 5 November 2026

STATUS
The requested optimal general causal memory/processing tradeoff is unresolved.
This package does not claim a sublinear-memory high-fidelity reader and does
not claim a matching general impossibility theorem. It preserves exact proved
intermediate results and physical-policy diagnostics for the fixed source.

FIXED SOURCE AND CONVENTION
One arbitrary input qubit and its arbitrary reference; fresh independent I/2
carriers; each encounters the source once through cos(theta) I + i sin(theta)
SWAP, at the same known angle. No preparation keys, bath purifiers, return
link, or changed source program. The source is ultimately discarded.
All channel errors use HALF diamond norm. Every coherent register, including
waiting carriers and initialized workspace crossing a cut, counts as memory.

READ FIRST
weak_stream_memory.pdf / weak_stream_memory.tex:
  Explanatory report, general finite-error converse and proof, exact restricted
  boundaries, accepted all-output resource law, source comparisons, and the
  precise missing endpoint.
boundary/source_granted_converse.txt:
  Full general prefix spectral-profile converse. Includes arbitrary classical
  instruments, variable branch memory, tails/expected occupancy, exact moments,
  analytic trial operators, and the cost of the spectral calculation.

PROVED SOURCE-SPECIFIC BOUNDARIES
online/covariant_qubit_cptp_obstruction.txt:
  Complete covariant two-input/one-output CPTP region and a uniform sharp-scale
  Theta(theta^2) visibility bound for one tracially initialized retained qubit.
  Deterministically time-dependent dissipative maps and fresh discarded pure
  implementation ancillas are included. Retained instrument outcomes,
  outcome feedback, and a second coherent register are not covered.
online/crossed_statistic_obstruction.txt:
  Exact folded two-qubit virtual family and a robust causal distinguishability
  obstruction. The virtual SRA state must be the COMPLETE source-plus-memory
  statistic for that obstruction; extra correlated registers can evade it.
online/purified_block_gram.txt:
  Physical reverse-dummy blocks retaining BOTH the dummy and its locally
  prepared Bell purifier; exact symmetric Petz p,q formulas, repeated-block
  recurrence, arbitrary collective final-decoder bound, and joint weak-angle
  asymptotics. Other block instruments are not ruled out.
online/block_petz_obstruction.txt:
  Earlier, narrower blocks retaining only the dummy qubit.
schur/SCHUR_BOUNDARY.md:
  Ordinary measured-J Schur compression boundary and the two-carrier
  singlet/triplet coherence that carries the payload.
schur/FUSION_THEORY.md:
  Physical growing-spin instrument, finite control and backlog bill, exact
  consecutive-pair label loss, scope of ordinary integrable fusion, and
  additional representation diagnostics. A physical instrument definition
  is not itself a recovery-performance theorem.
schur/OPTIMAL_SPIN_READOUT.md:
  Exact final-readout calculation for the specified finite spin family.
schur/CLASSICAL_SPARSE_FAILURE_BOUND.md:
  Exact continuation bound for measured/dephased failure flags completing the
  specified crossed statistic, even with arbitrary memory on failure branches.
  Fully coherent flags and extra coherent success records are not covered.
schur/PURE_BASELINE_AND_FINAL_STATUS.md:
  Pure-initialized nontracial growing-spin construction and executed policy
  diagnostics. Its conditional-history fidelities are not ensemble guarantees
  or a general impossibility theorem for initialized or nonmyopic receivers.

EXECUTED NUMERICS
The JSON receipts beside scripts record finite exact-matrix checks and
specific control-policy trajectories. They are not physical experiments or
simulation of 43,462 retained bath qubits. Small prefix spectra do not prove
the large-prefix spectrum. Numerical infeasibility is not used as a theorem.

Useful reproductions, from the package root:
  python online/verify_covariant_qubit.py
  python online/verify_crossed_statistic.py
  python online/verify_purified_blocks.py
  python schur/check_schur.py
  python schur/fusion_proof_checks.py
  python boundary/moment_transfer.py
  python boundary/transfer_witness.py

Some diagnostic scripts have command-line options; inspect their argument
parser before launching larger runs. Adaptive fusion trajectories simulate
a compact known invariant Choi state for a physically specified policy, not
an arbitrary quantum output register. The optional extension SDP uses cvxpy
and a solver; its outcome is not a premise of the analytic obstruction.
The covariant one-qubit calculation includes 295 explicit channel-Choi/Kraus
checks, with recurrence residual below 1.34e-15. The adaptive fusion engine
online/adaptive_fusion.py uses constant-sized invariant matrices per realized
classical history and implements the exact immediate pinching-loss minimizer.
Its recorded trajectories, including staged source-residual weighting, do not
achieve the target fidelity. They do not rule out other adaptive policies.

RESOURCE ACCOUNTING
The accepted all-output decoder achieves error 3(1-sin(theta)^4)^N/4 with
N stored outputs, one tracial dummy, and N inverse gates before routing.
At theta=.1 and epsilon=.01 it needs 43,462 collisions. Collection alone
incurs 944,450,991 encounter-intervals of qubit-time. In the accepted
nearest-neighbour fixed-junction layout, the complete source/capture/decode
gate count is (N^2+5N-2)/2 = 944,581,376. This is a specified circuit
bill, not a universal lower bound on other physical layouts. Routing, memory
protection, source calibration, ancilla preparation, reset, gate precision,
service latency, and any buffer backlog remain actual paid resources.
No fault-tolerant factory or large protected reader was simulated.

WARM PRESERVATION
warm/causal_payload_memory_research_package.zip and
warm/tracial_acquisition_research_package.zip are byte-identical copies of
the completed earlier packages. warm/preservation.json records their hashes.
The complete finite-error payload-memory theorem, short-record construction,
prefix and expected-occupancy bounds, noisy-emission correction, and all three
companions remain in those archives unchanged. The programmed emitter is
distinct from this homogeneous weak source. Its results are not hypotheses
about the present stream.

PRIMARY MACHINERY CONSULTED
Bacon, Chuang, Harrow, quant-ph/0407082: efficient Schur and CG circuits.
Blume-Kohout, Croke, Zwolak, 1201.6625: coherent gathering of pure bounded-
Schmidt-rank state families; mixed i.i.d. extension uses permutation symmetry.
Claeys, Herzog-Arbeitman, Lamacraft, 2106.00640: integrable correlation transfer
matrices, homogeneous Jordan structure; eigenvalues are not singular values.
Yosifov, Iyer, Ebler, Vedral, 2412.14544: partial-SWAP homogenization and
correctability discussion; it does not supply the requested causal interface.
The exact local warm packages are used as accepted machinery. No fresh
successful retrieval of a newest Astra index is asserted in this return.

UNRESOLVED ENDPOINT
Either construct a CPTP causal receiver with reference-uniform high-fidelity
recovery at the quartic collision scale and a genuinely sublinear joint
quantum-memory/near-linear-processing bill, or establish a sharp general
lower bound for this very source with a matching operation. The present
spectral theorem is a necessary condition; its needed large-prefix spectral
estimate is not supplied. Restricted receiver failures are not that estimate.
