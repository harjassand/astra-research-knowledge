"""Finite exact tests for the matching dyadic compiler.

These tests use the exponential exhaustive signer only on tiny feature-column
sets. They exercise the exact wrapper, not Li's polynomial signing algorithm.
Run from any directory with ``python3 test_exact_behavior.py``.
"""

from fractions import Fraction as F

from matching_dyadic_compiler import (
    _compress_law,
    compile_matching_law,
    exhaustive_signer,
)


def verify_law(n, edges, marginals, features):
    bound, atoms, max_error = compile_matching_law(
        n, edges, marginals, features, exhaustive_signer
    )
    assert sum((atom.probability for atom in atoms), F(0)) == 1
    assert len(atoms) <= len(edges) + 1
    mean = [F(0)] * len(edges)
    for atom in atoms:
        assert len(atom.matching) == n
        assert len(set(atom.matching)) == n
        for edge_id in atom.matching:
            mean[edge_id] += atom.probability
    assert tuple(mean) == tuple(marginals)
    assert max_error < 100 * bound if bound else max_error == 0
    return bound, atoms, max_error


def check_k22_nondyadic_mean():
    edges = ((0, 0), (0, 1), (1, 0), (1, 1))
    marginals = (F(1, 3), F(2, 3), F(2, 3), F(1, 3))
    features = (
        (F(1), F(-1), F(2), F(0)),
        (F(0), F(1, 3), F(-1, 3), F(0)),
    )
    _, atoms, _ = verify_law(2, edges, marginals, features)
    assert {atom.matching for atom in atoms} == {(0, 3), (1, 2)}
    assert {atom.probability for atom in atoms} == {F(1, 3), F(2, 3)}


def check_even_cycle_sharp_obstruction(half_length):
    # The graph C_(2k) has exactly two perfect matchings. With alternating
    # scalar edge features and x_e=1/2, every exact-mean law must put half its
    # mass on each; the atom errors are exactly +/-k.
    k = half_length
    edges = tuple(
        edge
        for i in range(k)
        for edge in ((i, i), ((i + 1) % k, i))
    )
    marginals = (F(1, 2),) * (2 * k)
    features = (tuple(F(1 if edge_id % 2 == 0 else -1) for edge_id in range(2 * k)),)
    bound, atoms, error = verify_law(k, edges, marginals, features)
    atom_values = [sum((features[0][edge_id] for edge_id in atom.matching), F(0)) for atom in atoms]
    assert set(atom_values) == {F(-k), F(k)}
    assert all(abs(value) == k for value in atom_values)
    assert {atom.probability for atom in atoms} == {F(1, 2)}
    assert error == k
    assert bound == 2 * k  # exact ||A u_C||_1 bound for this feature row


def check_connected_multicycle_graph():
    # Uniform K4,4 enters an odd-numerator level whose Eulerian support splits
    # into several cycle columns. Record callback widths to verify that the
    # multi-column branch, not only the single-cycle case, is exercised.
    n = 4
    edges = tuple((left, right) for left in range(n) for right in range(n))
    marginals = (F(1, 4),) * (n * n)
    features = tuple(
        tuple(F(int(edge_id == coordinate)) for edge_id in range(n * n))
        for coordinate in range(n * n)
    )
    widths = []

    def recording_exhaustive_signer(columns):
        widths.append(len(columns))
        return exhaustive_signer(columns)

    bound, atoms, error = compile_matching_law(
        n, edges, marginals, features, recording_exhaustive_signer
    )
    assert max(widths) >= 2
    assert bound == 2 * n  # unit-norm columns use the explicit 2n cycle bound
    assert len(atoms) == 4
    assert error < 100 * bound
    mean = [F(0)] * len(edges)
    for atom in atoms:
        assert len(atom.matching) == n
        for edge_id in atom.matching:
            mean[edge_id] += atom.probability
    assert tuple(mean) == marginals


def check_zero_features():
    edges = ((0, 0), (0, 1), (1, 0), (1, 1))
    marginals = (F(1, 3), F(2, 3), F(2, 3), F(1, 3))
    features = ((F(0), F(0), F(0), F(0)),)
    bound, atoms, error = verify_law(2, edges, marginals, features)
    assert bound == 0
    assert error == 0
    assert len(atoms) == 2


def check_rank_deficient_compression():
    # Four distinct collinear points in R^2 give an affine-rank-one input to
    # the standalone exact compressor (edge_count=2, allowed support=3).
    original = [(F(1, 4), (F(i, 3), F(0))) for i in range(4)]
    compressed = _compress_law(original, edge_count=2)
    assert len(compressed) <= 3
    assert all(point in {point for _, point in original} for _, point in compressed)
    assert sum((weight for weight, _ in compressed), F(0)) == 1
    barycenter = tuple(
        sum((weight * point[coordinate] for weight, point in compressed), F(0))
        for coordinate in range(2)
    )
    assert barycenter == (F(1, 2), F(0))


if __name__ == "__main__":
    check_k22_nondyadic_mean()
    check_even_cycle_sharp_obstruction(3)  # C6
    check_even_cycle_sharp_obstruction(5)  # C10
    check_connected_multicycle_graph()
    check_zero_features()
    check_rank_deficient_compression()
    print("all exact behavioral checks passed; Li signer not tested")
