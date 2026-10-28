# Focused comparison: positive operator-block recovery and acquired Pauli algebra

28 October 2026. Independent targeted primary-source comparison, not a historical-priority certificate. Governing current root sources: `positive_operator_clifford_acquisition_20261028.md` (SHA a6e70c6b4445b0c18c91073ecf8c81dac1449db8e36de52129f6239b1bace27f) and `convex_positive_operator_clifford_acquisition_20261028.md` (SHA 4bb1b5ce0a9f688e8127a65651ba0059ab5f98a4d570b891c8880c82373ee439). Their separate substantive receipts govern mathematical acceptance; this note changes neither.

## 1. The convex objective is an established recovery objective

Let rho_(j,s)=N((I+s sigma_j)/2), C_j=(rho_(j,+)-rho_(j,-))/2, and Phi=R†. Direct expansion gives

    F_six(R N)=(1/6) sum_(j,s) Tr[(I+s sigma_j)/2 R(rho_(j,s))]
              =1/2+(1/6) sum_j Tr[Phi(sigma_j) C_j].
    Fe(R N)=1/4+(1/4) sum_j Tr[Phi(sigma_j) C_j].

Thus the proposed SDP optimizes ordinary six-state average fidelity, equivalently maximally-mixed-input entanglement fidelity. Neither convex channel optimization nor this objective is new machinery.

**Fletcher–Shor–Win, Optimum Quantum Error Recovery using Semidefinite Programming, quant-ph/0606035v1, §IV Eqs20–22, printed p4.** They express entanglement fidelity as Tr(X_R C), then optimize with X_R positive and a partial-trace identity. Their §V also reduces dimension by combining encoding with noise and decoding with recovery. Relevant passage: “the linearity of the objective function”. This is direct overlap with our candidate stage, not merely a distant analogy. Their stated input is a specified noise model/encoding, but an equally informed implementation can estimate the requisite objective matrix from the same observations rather than reconstruct a microscopic environment. https://arxiv.org/pdf/quant-ph/0606035

**Fletcher–Shor–Win, Structured Near-Optimal Channel-Adapted Quantum Error Correction, arXiv:0708.3658v2, §V Eqs24–29, printed pp10–11; appendix pp16–17.** They derive the dual min TrY subject to I⊗Y−C>=0 and explicitly use feasible dual points to certify recovery quality. Relevant passage: “a certificate of convergence for a recovery operation”. They construct dual bounds from structured recoveries; the appendix establishes an optimum for stabilizer codes under Pauli-group errors. Therefore recovery dual certification, including algebraic special-family optima, is prior overlap. The inspected passage does not state our noncommuting positive coefficient-block sum-of-squares/curvature theorem. That observation is not a search-complete novelty claim. https://arxiv.org/pdf/0708.3658

## 2. What must actually carry the present bridge

For C_j=sum_k B_k T_kj with symmetric Hermitian T_kj in the true Pauli commutant and the entire block T>=0, the specific factorization

    I⊗sum_j T_jj−sum_j sigma_j^T⊗C_j
       =(1/2) sum_jk D_j(I⊗T_jk)D_k,
    D_j=sigma_j^T⊗I−I⊗B_j

makes the hidden embedding globally optimal over ALL unital CP maps. Strict T>=tau I yields operator-Frobenius curvature. This continues to allow mutually noncommuting spectator coefficients, unlike scalar polar/Gram cancellation. The acquired positive fitted block S>=kappa I, fit residual and simultaneous data bounds then certify the rounded physical algebra without knowing true tau. These are the specific new obligations discharged by the local receipts, not an assertion that the standard SDP is new.

The same-algebra conditional family has a substantive consequence: the same subsystem extraction is the single-logical native fidelity oracle across varying admissible noise. Pointwise oracle reuse is stronger than simply reoptimizing a known channel. Nevertheless, a conventional learner given this theorem and promise can use precisely the same SDP, rounding and certificate. No algorithmic separation has been established.

## 3. Algebra identification and robust self-testing are relevant but distinct

**Choi–Kribs, A Method To Find Quantum Noiseless Subsystems, quant-ph/0507213v2, introduction and Theorem1, printed pp1–2.** Relevant passage: “if an operator-sum decomposition of Kraus (or ‘error’) operators”. Their construction identifies invariant/noiseless subsystem structure for general, including nonunital, operations using the channel or compressed noise commutants. It is prior art for recovering subsystem structure from noise algebra. It does not imply that a nonzero-contraction, dissipative logical channel has a noiseless subsystem, nor that three measured contrasts identify its hidden orientation. Conversely, the present positive-block premise is not arbitrary-channel noiseless-subsystem discovery: it assumes a particular common information algebra and only learns that algebra under excitation. https://arxiv.org/pdf/quant-ph/0507213

**McKague–Yang–Scarani, Robust self-testing of the singlet, arXiv:1203.2976v1, Eqs1–7/Theorem1 and Fig1, printed pp1–2.** Their theorem controls anticommutation and consistency on the tested state, then constructs a local extraction isometry controlling vectors obtained by applying I,X,Z. Relevant passage: “Then there exists a local isometry”. This is direct precedent for robust Pauli-to-extraction reasoning. It is not a whole-output operator-norm certificate: an unoccupied subspace can be unconstrained by the tested state. Present finite matrix reconstruction, common-basis exact rounding and controlled-reflection compilation use trusted preparations/readout/control and a known finite envelope, stronger access than device-independent correlations. No superiority over self-testing is implied. https://arxiv.org/pdf/1203.2976v1

Prior local-unitary learning is already examined in `LOCAL_POLAR_WHITENING_PRIMARY_COMPARISON_20261028.md`: Huang et al. 2401.10095 local Heisenberg-Pauli acquisition and circuit sewing are established. Current work must retain its noisy acquisition bridge; it must not rebrand local Pauli learning/sewing itself as discovery.

## 4. Astra's already accumulated bridge

Astra was queried first for noiseless subsystem/quantum recovery/semidefinite/Pauli algebra. Current N1144, revision d6672151ce8e86d4af3e74b3b880abcdc82ae304, was fetched with all pages; its governing `ordinary_local_mixed_gauge_decoder_tournament_20261028.md` was read with its continuation. Source SHA b1102426bfb3af58483e0d84fedde59e9317a6c0bfaac0a9e59a761f4976a9be. Its mixed noncommuting gauges, positive axis contrasts, Bures/sign extraction, unrestricted decoder comparison, coarse support overlap and expanded-envelope alternative are meaningful internal predecessors. In particular §10.4 already grants an equally informed conventional subsystem learner the simpler expanded-envelope route. Its reset/iid banks, supplied excitation and axis-aligned contrasts are not silently exchanged for the current predictable-history cross-axis positive block.

The current capsule's transport notice and exact SOURCE_PORTABILITY_CORRECTION.json were read completely. The latter SHA is d52518581482a48a2fe3b25512d9be7751cc5471e4858a7bc86de4d6bb4bcefa. It restores source prose/relative paths damaged by an earlier sanitizer; it explicitly does NOT constitute new scientific review or withdrawal. Use current-portable-v2 sources, retain historical originals. Input version 9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef was fresh at retrieval 20:40–20:44 UTC. No unrelated capsule's acceptance is transferred.

## 5. Equally informed comparison and unresolved costs

Three d×d contrast matrices carry O(d²) data, versus O(d²) for the full qubit-input output channel. Avoid claiming an asymptotic single-logical process-tomography saving solely because the unsigned output is unused. Neither approach needs a microscopic environment reconstruction. Locality and reusable orientation across many changing channels, if their promises hold, are the substantive potential savings.

Charge the same private ordinary probes, simultaneous matrix confidence bounds, acquired support, local dimension d=2^W, inverse excitation/gap, calibration drift assumptions and finite controls to both methods. Polynomial local SDP arithmetic is exponential in W; no production SDP speed advantage or experimentally favorable budget follows. Physical source examples justify membership only in their declared family, not all unknown noise. Unknown future history outside the shared-B positive-block contract is not certified by a bank fit. Whole inverse/complete-memory comparison concerns a fixed implemented inverse, whereas native fidelity regret concerns a reduced one-use channel.

Decision: credit recovery SDP/dual certificates, subsystem identification, and Pauli extraction as established machinery. Retain the positive noncommuting operator-block identifiability/curvature and acquired fit as the concrete bridge worth pursuing. The next decisive practical comparison is identical-data recovery SDP with exact confidence/control costs, not an artificially forced environment-tomography baseline. Historical novelty and broad practical advantage remain unresolved.
