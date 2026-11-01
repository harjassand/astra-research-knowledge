"""Exact checks for the independent warm-mediator repeatability note.

Run with ordinary Python + NumPy.  This is an algebra/support audit, not a
simulation of a complete noisy fault-tolerant quantum computer.
"""

from itertools import combinations, product
import json
from pathlib import Path
import numpy as np


OUT = Path(__file__).parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = [I, X, Y, Z]


def kron_all(ops):
    result = np.array([[1]], dtype=complex)
    for op in ops:
        result = np.kron(result, op)
    return result


def controlled(control, target, target_op, n=3):
    p0 = np.diag([1, 0])
    p1 = np.diag([0, 1])
    no = [I] * n
    yes = [I] * n
    no[control] = p0
    yes[control] = p1
    yes[target] = target_op
    return kron_all(no) + kron_all(yes)


# Data qubits 0, 1; indefinitely retained mediator 2.
C_X = controlled(0, 2, X)
C_Z = controlled(1, 2, Z)
micro = [C_X, C_Z, C_X, C_Z]  # chronological order
target = controlled(0, 1, Z)
whole = np.eye(8, dtype=complex)
for gate in micro:
    whole = gate @ whole
closure_error = float(np.linalg.norm(whole - target, 2))
assert closure_error == 0

# Expand all allowed elementary faults in their Pauli basis.  A fault after
# a microgate may act on both its data qubit and the mediator.  Propagate it
# to the macro boundary; all 60 nonidentity basis terms remain confined to
# the intended pair and its mediator.
pauli_basis = [(label, kron_all([PAULIS[j] for j in label]))
               for label in product(range(4), repeat=3)]
fault_table = []
for slot, active_data in enumerate([0, 1, 0, 1]):
    suffix = np.eye(8, dtype=complex)
    for gate in micro[slot + 1:]:
        suffix = gate @ suffix
    for pd, pm in product(range(4), repeat=2):
        if pd == pm == 0:
            continue
        label = [0, 0, pm]
        label[active_data] = pd
        fault = kron_all([PAULIS[j] for j in label])
        propagated = suffix @ fault @ suffix.conj().T
        coeff = [np.trace(p.conj().T @ propagated) / 8 for _, p in pauli_basis]
        terms = [k for k, c in enumerate(coeff) if abs(c) > 1e-10]
        assert len(terms) == 1
        boundary = pauli_basis[terms[0]][0]
        fault_table.append({"slot": slot, "fault": label,
                            "boundary_pauli": boundary,
                            "data_support": [j for j in (0, 1) if boundary[j]]})

# Incoming data-bus correlations can be arbitrary linear combinations of
# Pauli tensors; no product-state input is required.  Whole-space closure
# implies all 64 incoming terms evolve exactly by CZ on data and identity
# on the mediator.
incoming_checks = 0
for label, p in pauli_basis:
    got = whole @ p @ whole.conj().T
    expected = target @ p @ target.conj().T
    assert np.allclose(got, expected)
    incoming_checks += 1

# Explicit classical terminal Z measurement for concatenated Steane code.
# The Hamming parity-check columns are all nonzero vectors in GF(2)^3.
# Every ideal inner/outer computational-basis codeword has zero syndrome.
# The logical bit is its parity after correcting the identified bit.
H = np.array([[int((j >> bit) & 1) for j in range(1, 8)]
              for bit in range(3)], dtype=np.uint8)


def steane_measure_decode(bits):
    bits = np.array(bits, dtype=np.uint8).copy()
    syndrome = H @ bits % 2
    loc = int(sum(int(syndrome[k]) << k for k in range(3)))
    if loc:
        bits[loc - 1] ^= 1
    return int(bits.sum() % 2)


def concatenated_decode(bits):
    inner = [steane_measure_decode(bits[7 * j:7 * (j + 1)]) for j in range(7)]
    return steane_measure_decode(inner)


measurement_checks = {}
for weight in range(4):
    failures = 0
    total = 0
    for locations in combinations(range(49), weight):
        raw = np.zeros(49, dtype=np.uint8)
        raw[list(locations)] = 1
        failures += concatenated_decode(raw)
        total += 1
    measurement_checks[weight] = {"patterns": total, "failures": failures}
    assert failures == 0

# Exhibit the limit of this simple hierarchical decoder: four bit flips in
# two inner blocks can make two wrong inner logical bits and fool the outer
# decoder.  The [[49,1,9]] code itself can correct four arbitrary errors with
# optimal recovery; this particular low-complexity measurement decoder is
# only guaranteed for three bit flips.  We do not hide the distinction.
four_error_failure = None
for locations in combinations(range(14), 4):
    raw = np.zeros(49, dtype=np.uint8)
    raw[list(locations)] = 1
    if concatenated_decode(raw):
        four_error_failure = locations
        break
assert four_error_failure is not None

# Warm oscillator limitation: a residual controlled displacement produces
# exp(-i epsilon Z p). For a zero-mean Gaussian with Var(p)=V, coherence is
# exp(-2 epsilon^2 V).  Holding epsilon small does not bound error uniformly
# as V grows.  This is analytic, not a truncated-Fock approximation.
epsilon = 0.01
oscillator_examples = [
    {"epsilon": epsilon, "momentum_variance": v,
     "coherence": float(np.exp(-2 * epsilon**2 * v)),
     "plus_input_trace_norm_distance": float(1 - np.exp(-2 * epsilon**2 * v))}
    for v in [0.5, 50, 5000, 50000]
]

result = {
    "whole_space_closure_spectral_error": closure_error,
    "microscopic_fault_pauli_terms_checked": len(fault_table),
    "arbitrary_incoming_joint_operator_basis_terms_checked": incoming_checks,
    "terminal_measurement_decoder_checks": measurement_checks,
    "hierarchical_decoder_four_error_failure_locations": four_error_failure,
    "oscillator_closure_examples": oscillator_examples,
    "limits": [
        "This verifies algebraic primitives, not a full noisy EC rectangle.",
        "Persistent-column theorem assumes all damaging support stays in the declared columns.",
        "The measurement decoding algorithm is explicit, but its own hardware faults need a separate bound.",
        "A full-space finite mediator model must include leakage levels or count leakage as a fault."
    ]
}
(OUT / "verification_results.json").write_text(json.dumps(result, indent=2) + "\n")
(OUT / "primitive_fault_table.json").write_text(json.dumps(fault_table, indent=2) + "\n")
print(json.dumps(result, indent=2))
