from fractions import Fraction
import json

def factory(n):
    # Data 0..n-1; edge-syndrome ancillas n..2*n-2.
    layers = []
    for edge_parity in (0, 1):
        for endpoint in (0, 1):
            gates = [(i+endpoint, n+i) for i in range(n-1) if i % 2 == edge_parity]
            wires = [w for g in gates for w in g]
            assert len(wires) == len(set(wires))
            layers.append(gates)
    # Equal amplitudes initially after one Hadamard layer on the data.
    basis = {x: x for x in range(1 << n)}
    for gates in layers:
        for original, state in list(basis.items()):
            for control, target in gates:
                if (state >> control) & 1:
                    state ^= 1 << target
            basis[original] = state
    branches = {}
    mask = (1 << n) - 1
    for state in basis.values():
        syndrome = state >> n
        branches.setdefault(syndrome, []).append(state & mask)
    assert len(branches) == 1 << (n-1)
    for syndrome, data in branches.items():
        assert len(data) == 2 and data[0] ^ data[1] == mask
        correction = 0
        bit = 0
        for i in range(n-1):
            bit ^= (syndrome >> i) & 1
            correction |= bit << (i+1)
        assert set(x ^ correction for x in data) == {0, mask}
    raw_prob = Fraction(1, 1 << n)
    felinity = 2 * (1 << n) * raw_prob * raw_prob
    correction_collision = Fraction(1, len(branches))
    assert felinity == correction_collision
    return {
        'n': n, 'total_qubits': 2*n-1,
        'quantum_unitary_layers_before_measurement': 5,
        'measured_syndrome_bits': n-1,
        'successful_adaptive_yield': 1,
        'success_without_feedback_accept_only_zero_syndrome': str(correction_collision),
        'correction_frames': len(branches),
        'collision_entropy_bits': n-1,
        'raw_felinity': str(felinity),
        'all_branches_correct_to_GHZ': True,
        'collision_bound_is_equality': True
    }

if __name__ == '__main__':
    results = [factory(n) for n in range(2, 13)]
    print(json.dumps(results, indent=2))
