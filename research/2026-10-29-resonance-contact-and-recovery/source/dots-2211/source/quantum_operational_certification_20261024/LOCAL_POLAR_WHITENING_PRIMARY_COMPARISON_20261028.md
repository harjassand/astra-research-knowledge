# Targeted primary-source comparison: local noisy inverse acquisition

28 October 2026, 20:18 UTC. Source comparison, not scientific receiving or a novelty certificate. Root candidates inspected: local_noise_polar_identifiability_extension_20261028.md and ordinary_unknown_axis_positive_bloch_whitening_20261028.md. No existing manuscript was changed.

## Closest established machinery

**Huang et al., Learning shallow quantum circuits, arXiv:2401.10095v1.** Actual passages read: §§2.1.2 and 5.2.2, Definitions14–15, Lemmas8–11, Eqs109–125; unitary promise discussion §1.3. Short passage: “directly sewing the Heisenberg-evolved Pauli operators”. Their local Pauli learning from product preparations/randomized readout, unknown-support handling, SWAP assembly, unitary projection and summed diamond-error theorem are direct prior overlap. These ingredients must be credited. Their noiseless-channel theorem does not itself remove a nonunital spectator factor from noisy response data. https://arxiv.org/html/2401.10095v1#S5.SS2.SSS2

**Wadhwa–Doosti, Noise-tolerant learnability of shallow quantum circuits from statistics and the cost of quantum pseudorandomness, arXiv:2405.12085v3 (27 April2025).** Actual passages: Theorems1–3, §§4–5, Eqs38–53. Short passage: “the tolerance of the queries needs to be lowered.” Theorem1 absorbs a supplied whole-channel diamond discrepancy eta below the ideal query tolerance tau by using tolerance tau−eta. The separate noise estimator treats global depolarization and uses a two-copy statistical query. This does not supply arbitrary-precision mixer identification under fixed substantial nonunital product noise. Its access/query tolerance must not be compared to raw ordinary shots for free. https://arxiv.org/html/2405.12085v3#S4

**Ruskai–Szarek–Werner, An Analysis of Completely-Positive Trace-Preserving Maps on 2x2 Matrices, quant-ph/0101003v2, LAA347(2002).** Actual passage: §1.2, printed pp4–5, Eqs2–4; §3.2 warning on printed p25. Short passage: “rotations rather than arbitrary real orthogonal matrices”. Bloch affine reduction under physical input/output unitaries and the signed-singular-value restriction are old. Thus the positive-determinant polar convention is a standard algebraic target choice, not a new physical principle. Their warning also prevents treating contraction and translation as separately physical channels. The root candidate avoids this by applying a physical unitary to the entire CPTP channel. https://arxiv.org/pdf/quant-ph/0101003

**Carignan-Dugas–Alexander–Emerson, A polar decomposition for quantum channels, Quantum3,173(2019), arXiv:1904.08897v3.** Actual passages: introduction and §4/Theorem3 context, full primary PDF. Short passage: “unitary-decoherent polar factorization”. Separating a removable unitary component from remaining decoherence is established. Their factor is defined through the leading Kraus operator, not the local three-contrast Gram convention; no equality of these conventions or acquisition guarantee is inferred. https://quantum-journal.org/papers/q-2019-08-12-173/pdf/

## What the candidate still has to add

The consequential bridge is specifically from actual noisy ordinary response operators

    Delta_j = sum_a T_aj B_a R

to fixed physical Pauli generators B_a when R is unknown, positive, possibly correlated across output sites, and commutes only with this input qubit's algebra. A small-noise perturbation theorem does not remove fixed unknown T and R. The proposed common-factor Gram identity followed by sign extraction does. The exact canonical target is V_eff, not an unidentifiable original mixer once arbitrary local coherent noise rotations are admitted.

This distinction is not a historical-priority finding. An equally informed conventional method can use exactly the same contrast matrices, Gram normalization, matrix sign and established circuit sewing. There is no algorithmic advantage merely from calling them a new architecture. A fair comparison must use those local noisy observations rather than gratuitously forcing the comparator to reconstruct a microscopic environment or a dense global Choi matrix.

The access direction must remain explicit. Prior Heisenberg objects are Udagger P_i U; current signed-output responses recover V P_i Vdagger. Replacing U by Vdagger is algebraically valid only AFTER the current noisy acquisition has produced those objects. It does not grant queries to Vdagger. Once such generators are certified, existing sewing is an alternative implementation comparator to the three-controlled-reflection receiver, including ancilla state, routing, finite gate synthesis and output-register selection costs.

## Remaining acquisition obligations that matter more than vocabulary

1. Common T across a calibration bank and common R across all three axes are structural promises. History-dependent mixtures correlating different T with different R generally break Gram cancellation. Passing finite Gram/sign guards cannot establish the promise at unseen histories.
2. Full physical product-input access and private current preparation coins are substantive. A logical black-box port or unknown preparation noise is a different experiment.
3. Bounded conjugated-generator support is not automatically a supplied shallow circuit layout. The support-discovery experiment and a compiled inverse must both be paid.
4. Gram and sign gaps can be tiny. Their acquired guards provide sound abstention, not a numerical scaling advantage. Compare actual charged shots, finite arithmetic and controls against the same local-patch learner.
5. Operator-norm inverse approximation gives complete-memory transfer to the same fixed inverse. It does not certify that remaining noise is correctable, product at future histories, or below a fault-tolerance threshold.

## Astra retrieval and freshness

Astra Research was queried first: “local unitary inverse product probes polar Bloch Gram whitening”; then “quantum local inverse acquisition”, “unitary circuit learning”, and “Heisenberg local inversion”. Published revision c6cec6185088eb2eb0dca204290516163d385dbb, input2dde18ffe626f298d6ccc81122a4b7e99f604e3e314f8e1679a6465f431e5b10, freshness current at20:17:01UTC. Returned menus did not identify a directly governing local-inverse/whitening result; no preview was promoted to a proof and no unrelated card was imported. This is a search limitation, not evidence of absence. Relevant current root sources were read directly above. Primary web search also checked recent circuit-learning results; nothing from an abstract alone was used to assert coverage of the noisy common-factor obligation.

Decision: preserve the construction but position it as a proposed noisy acquisition bridge built on established local-operator learning, circuit sewing and channel orientation machinery. The most useful next test is a nonunital, genuinely overlapping multi-qubit fixture with an equally informed local-process baseline and paid Gram/sign conditioning, not a claim that local inverse construction itself is new.
