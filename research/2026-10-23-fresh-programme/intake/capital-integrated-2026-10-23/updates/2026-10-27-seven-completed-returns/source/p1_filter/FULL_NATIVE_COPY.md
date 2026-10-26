## ASTRA — Coherently enforcing quantum symmetry

The strongest new construction replaces an assumed Hamiltonian symmetry with an active, heralded symmetry filter.

The previous service required the complete detector interaction to conserve the protected rail sector and commute with the combined rail–ancilla symmetry. The new construction can enforce those conditions on the accepted quantum operation, even when the underlying interaction violates them.

Let \\(U\\) be the complete physical evolution, including its hidden quantum bath. Introduce two commuting symmetries:

\\[ R=-Z_pZ_q,\qquad S=\operatorname{SWAP}\_{pq}Z_a. \\]

Two coherent check ancillas implement the accepted operation

\\[ \boxed{ U\_{\rm accepted} =\frac14(U+RUR+SUS+RSURS). } \\]

Direct algebra gives

\\[ [U\_{\rm accepted},R]=[U\_{\rm accepted},S]=0. \\]

Consequently, the accepted detector cannot produce a false arrival click from an off-code input. Within the protected dual-rail subspace, its successful branch again has precisely the logical \\(Y/Z\\) structure required by the preceding teleportation-based fault theorem.

### Executed full-memory verification

I implemented the actual coherent-control circuit and compared it with the operator formula, including noncommuting bath dynamics, code leakage and ancilla disturbances.

# 2.6 × 10²

Largest tested off-code interaction strength, in model units

# 1.07 × 10⁻¹⁶

Largest completed-teleportation identity residual

# 0

Off-code false-click amplitude in the exact adversarial example

# 100%

False-click probability for ordinary classical randomization in that example

The distinction between coherent and classical checks is essential. Randomly choosing which symmetry to apply does not enforce the symmetry. The check ancillas must retain coherence across the physical interaction, and their interference outcome must be postselected.

This mechanism is closely related to established Pauli-check sandwiching.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Scientific Reports

+1

&#x20;Its application here to a completed, hidden-memory, rail-heralded teleportation service is a programme-level construction, not an established new theorem of quantum information.



### A task-specific equivalence — and its limitation

For a fresh Bell candidate, I verified that the coherent symmetry filter produces the same accepted resource-and-bath state as applying a nondemolition \\(XX\\) stabilizer projection after the noisy interaction, together with the required code-space projection.

This holds separately for the Kraus branches of a noisy physical channel, not merely for average acceptance probabilities. The largest tested resource-and-bath residual was \\(6.83\times10^{-17}\\).

It offers two implementation routes:

- Coherent symmetry checks: protect the operation locally while it interacts with the bath.
- Late stabilizer projection: let the bath interaction finish, then verify the entangled resource before teleportation.

The second route avoids keeping check ancillas coherent throughout the uncontrolled interaction. However, it has a serious physical limitation for a communication link: the two halves of the Bell resource are normally at different locations.

A nondemolition \\(XX\\) parity projection across separated qubits cannot be implemented using only local operations and classical communication without an additional entanglement resource or nonlocal interaction. Applied to the product state \\(|00\rangle\\), the ideal projection creates a Bell pair with probability \\(1/2\\). Local operations alone cannot do that.

Ordinary local \\(X\\) measurements are not a substitute. They produce the same coarse parity statistics but reduce the surviving fidelity of a perfect Bell pair from 1 to \\(1/2\\).

Thus the late-verification route is potentially simpler for a local quantum processor, but not automatically cheaper for remote quantum transport. The coherent local checker remains the stronger architecture to investigate for the remote service.

## Strongest practical refinement: Clifford-only checks

The construction can now use an eight-gate verification network when the source is known to start in the protected code.

| Architecture                                     | Extra two-qubit gates | Coherent check ancillas surviving the unknown interaction |
| ------------------------------------------------ | --------------------- | --------------------------------------------------------- |
| Two-generator Clifford symmetry filter           | 10                    | 2                                                         |
| Single Pauli symmetry filter + output code check | 8                     | 1                                                         |
| Same design with an additional input code check  | 10                    | 1                                                         |

The eight-gate design uses six CNOT/CZ operations around the unknown interaction and two for the final nondemolition code-space check. Ten independently generated interactions, including unrestricted code-to-complement mixing and hidden-bath correlations, reproduced the full two-generator accepted operation to residuals below \\(3.5\times10^{-16}\\).

The initial code check removes the requirement of perfect code occupancy, but does not certify that the accepted source is a correct Bell resource. Source quality remains a separate physical and statistical requirement.

### Robustness to imperfect check gates

If the entire coherent checking circuit has a calibrated, full-boundary operator-amplitude deviation at most \\(\xi\\), then the previously forbidden logical Pauli components obey

\\[ \boxed{W\_{\mathrm{forbidden}}\preceq \xi^2 I_M.} \\]

This applies regardless of how strongly the underlying physical interaction couples to the hidden bath. It does not eliminate the need to bound errors during the additional control gates themselves.

Executed imperfect-control reference · Gate-error scale 0.012 radians

# 3.39 × 10⁻⁵

Simulated invisible Pauli-fault effect

# 1.66 × 10⁻³

Rigorous uniform effect ceiling

### The decisive remaining failure

An explicit density-operator experiment demonstrates why coherent checking cannot be replaced by classical randomization or by calibrating only the endpoints of individual gates.

When the bath acquires a complete copy of the check ancillas' computational-basis information:

- The ideal coherent checker gives zero false acceptance.
- The leaked checker produces the accepted syndrome with probability \\(1/4\\).
- Conditional on that accepted syndrome, the off-code false-click probability is 100%.

Thus reliable syndrome coherence across the actual physical operation is indispensable. An unconstrained device can also have zero acceptance probability, so correctness and availability remain distinct.

## Preserved research

All six executable studies passed the final consolidated validation, and the archive passed integrity checks.

Complete scientific derivation

Full-memory theorem, Clifford compilation, robustness proof, alternative architecture and counterexamples

Reproducible research archive

Six Python programs, six executed JSON result files, validation log and SHA-256 checksums

Scientific assessment: The main gain is replacing a hard-to-verify assumption about the entire uncontrolled Hamiltonian with a localized coherent-check interface, then reducing that interface to ordinary Clifford gates and one long-lived check ancilla. This builds directly on established Pauli-check sandwiching and stabilizer verification.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Scientific Reports

+2



The highest-leverage next attack is physically certifying that single coherent check ancilla and its controlled gates against bath information leakage. That is a narrower experimental target than proving the hidden interaction conserves the required symmetry at every instant, but it remains an unacquired capability.