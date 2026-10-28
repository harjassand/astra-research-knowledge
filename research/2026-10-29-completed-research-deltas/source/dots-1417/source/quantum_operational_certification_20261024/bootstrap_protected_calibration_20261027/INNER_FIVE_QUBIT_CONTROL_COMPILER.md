# Explicit local controls for the directly protected small payload

27 October 2026. Author construction/check; independent receiving separate. This adds a known local circuit to the received channel-level test without altering its frozen source/data. It is not a fault-tolerance threshold or hardware pulse count.

`compile_inner_five_qubit_encoder.py` deterministically reduces the standard stabilizers XZZXI, IXZZX, XIXZZ, ZXIXZ to four canonical Z stabilizers using phase-tracked H, S, S† and CX conjugations. A final one-qubit Clifford aligns logical XXXXX/ZZZZZ with the data wire. Reversing the reduction gives a known encoder on four |0> ancillas (wires0–3) and an arbitrary logical qubit (wire4).

The resulting list has **28 Clifford gates**: 12 H, 2 S, 3 S†, 11 CX. The JSON records every gate in order. Full 32×32 matrix checks verify code-space stabilization and the desired logical X,Z action. The circuit is therefore an implementation of the SAME standard five-qubit code, not a newly substituted code with an unrelated noise enumerator.

Decoding applies the known inverse encoder, measures wires0–3 in the computational basis, and corrects the remaining data wire by a known Pauli. All fifteen nonidentity weight-one physical Pauli errors give distinct nonzero syndromes; the JSON supplies the complete sixteen-entry correction table. The check applies each error to the actual encoded two-column isometry, verifies a unique measured syndrome, and verifies the remaining logical operator and correction. No controlled unknown source, unknown inverse, support oracle or postselected branch appears.

## Level-two local cost

A 25-carrier concatenated block has six five-qubit nodes. In this explicit circuit representation it costs:

| Component | Count per logical payload |
|---|---:|
| Inner/outer encoding Clifford gates | 168 |
| Known inverse-decoding Clifford gates | 168 |
| Computational syndrome measurements | 24 |
| Conditional logical Pauli corrections | At most6 |
| Private carrier input/output Pauli controls | At most50 |
| Learned seed encoder/source/decoder uses | 25 |
| Fresh private key bits | 50 |

Thus there are at most **392 listed Clifford/Pauli controls**, plus 24 syndrome measurements and the 25 learned seed encoder/decoder implementations. In the small tag/qubit example, each seed encoder prepares a known one-qubit tag, and its decoder is a known one-qubit unitary; their actual compilation and precision are additional. If S† is synthesized as three S gates instead of counted as an available inverse Clifford, the corresponding listed-gate counts increase. These are not calibrated physical pulse counts.

The encoding can be scheduled without storing all25 carriers at once: encode the five outer qubits, then encode and transmit one five-qubit inner block at a time. At most nine untransmitted logical carriers are simultaneously held at the sender (four other outer qubits plus one five-qubit inner block), in addition to the current tag/source interface. The receiver can decode each inner block immediately and retain its logical output; at most nine received logical carriers coexist (four completed inner outputs plus the current five-carrier block). The final outer decoder acts on five inner outputs. This scheduling assumes immediate local processing, reliable local storage and available classical keys; it does not certify their noise. Physical source ancillas/environment and measurement/readout workspace are not included in that logical-carrier count.

The source is stationary/reset and the output dimension is two, so the small instance can operate in the known physical output-qubit basis. No growing online frame is required for this circuit count. Larger unknown-support implementations retain the separately charged frame requirements.

All these operations remain trusted ideal controls in the channel-level calculation. Arbitrary correlated gate, measurement, storage, source-drift or key faults cannot be absorbed into the observed seed p and squared. A real implementation must meet the stated uniform complete-error budget or an independently justified local fault model. The explicit circuit makes those requirements countable; it does not prove they are met.

## Evidence

`compiled_inner_five_qubit_encoder.json` records the encoder, inverse, syndrome lookup and matrix-verified counts. The compiler source SHA256 is `0d390e4ea8ccaa3537a826a3ce0e0f79211eb5aa59b27d3779f1991507047bdf`. The earlier channel test and its separate receipt establish complete Pauli-code action; this companion supplies a finite known local control sequence.
