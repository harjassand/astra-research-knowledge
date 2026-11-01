# Astra: reusable prediction from noisy scalar experiments

## North star and present result

The long-term aim is a scientific system whose earlier experiments make later discoveries and intervention decisions substantially cheaper. This package supplies one mathematical component toward that aim. It is not a civilisation-changing breakthrough or a practical experimental advantage.

The new construction learns a reusable way to predict finite sequences of operations from noisy scalar return experiments, without seeing hidden states, receiving a well-conditioned basis, or resolving tiny Gram eigenvalues. Instead of identifying a fixed linear hidden model, it repeatedly projects onto an expanded convex set of acquired experimental features and corrects the requested scalar output.

Under the stated low-dimensional-width and source assumptions, only O(r log(H/epsilon)) actual descriptors are retained over an adaptive lifetime. Both scalar sampling and an explicit rounded finite-bit optimization method have epsilon^-2 accuracy dependence, apart from logarithms and substantial polynomial rank/horizon factors. All failed acquisition, preparation and future execution remain payable.

## What is new relative to the reused machinery

Governing Astra N1515 already supplies noisy bounded-coefficient Gram fitting, kernel Frank-Wolfe and retention after failed fitting. Convex projection, Frank-Wolfe, dual-weighted output correction and determinant potentials have strong prior art.

The proposed new join abandons an invariant unit hull and a fixed linear intertwiner. It uses expanded hulls, nonlinear requested-word rollouts, corrected scalar certificates, and failed actual-prefix discovery. A ridge inverse is used only in the lifetime proof, never acquired by the algorithm. Independent reviews found no mathematical or source-faithful implementation blocker within the stated contract. Historical novelty remains unresolved.

## Required assumptions

- A fixed finite control alphabet of actual Hilbert-space contractions, with genuinely supplied adjoints.
- Fresh conditionally unbiased bounded binary return reports, with preparation and control costs charged.
- Fixed horizon and same-seed scalar outputs. No state reconstruction, full output law, changing-source transfer, feedback planner or recognizable upfront universal completion is implied.
- A sufficiently low-dimensional joint reachable family for the efficient lifetime bound. This structure is not given as coordinates, but its existence is still an efficiency premise.
- The implementation's qualified interface uses orderable alphabet labels and native/conforming n-shot binary-grid adapters. Arbitrary custom rational means do not establish the binary bit-cost contract.

## Evidence and limitations

Seven end-to-end receiver tests passed. They used explicitly validated UNSAMPLED scalar means. No physical episodes were drawn. The two main fixtures still have conservative unexecuted calibration budgets of roughly 9.19e23 and 1.08e26 binary reports. These are not practical performance results.

Small-instance optimization proposals use only the acquired scalar matrices and are checked by an exact Frank-Wolfe gap. The general rounded solver is explicit and finite, but enormous runs were budget-refused. A separate synthetic test executed 927 rounded steps; an independent exact-rational audit checked 350 descent/feasibility cases. Neither is a physical experiment.

## Physical bridge, kept separate

The conditional physical notes construct self-adjoint measurement instruments from a warm meter with real initial wavefunctions. A matched finite-time two-quadrature interaction removes the oscillator's free-evolution phase in an admitted Hamiltonian model. Code-conditioned signed preparations can remove rare-code trace dilution, but encoding, reset, precision, readout and branch failures are paid.

These notes establish a possible source family, not available hardware or cheap high-fidelity gates. Ordinary Pauli dephasing is a rank-one problem already solved by elementary attenuation calibration. Nontrivial low task dimension and an advantage over strong retaining learners remain unestablished. The unreviewed multiseed extension is explicitly not part of the same-seed theorem receipt.

## Read and reproduce

1. PROOF.md, ROUNDED_SOLVER.md and BINARY_SCHEDULER.md state the construction.
2. receipts/ contains independent mathematical and implementation reviews, including the distinction between historical unrounded and improved rounded digital costs.
3. code/ contains the receiver, shared exact arithmetic helpers, tests and saved outputs.
4. priors/ credits the governing Astra source and strong conventional machinery.
5. physical_leads/ contains conditional physical constructions and informative failures, not a practical advantage claim.

From code/, run:

    python test_bounded_projection_receiver.py
    python bounded_projection_stress.py
    python rounded_fw_stress.py

The original receiver.py is included solely because the new implementation imports its exact arithmetic utilities and binary adapter. The old inverse-Gram model is not used by BoundedProjectionReceiver. test_receiver.py supplies transparent hidden-oracle test fixtures, never hidden vectors to the new receiver.

This package has not been published to GitHub or sent to third parties. It preserves the useful result while the consequential physical and economic test remains open.
