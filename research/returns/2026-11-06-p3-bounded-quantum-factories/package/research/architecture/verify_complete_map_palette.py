"""Small numerical verification of complete-map mixture and overlapping calls.

This is a finite-dimensional mathematical example, not a fabricated device
or a numerical proof of the general theorem. The noise includes a genuinely
entangling within-cell CZ fault, noisy selector fallback, and terminal local
depolarization. Every physical branch is a complete two-qubit CPTP map.
"""
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
SINGLE = [I2, X, Y, Z]
P = [np.kron(a, b) for a, b in itertools.product(SINGLE, repeat=2)]
D = 4
JDEP = np.eye(D*D, dtype=complex)/(D*D)
CZ = np.diag([1, 1, 1, -1]).astype(complex)


def unitary_choi(unitary):
    vector = unitary.reshape(-1)
    return np.outer(vector, vector.conj())/D


def product_depolarizing_choi(gamma):
    one = [1-3*gamma/4, gamma/4, gamma/4, gamma/4]
    return sum(one[i]*one[j]*unitary_choi(P[4*i+j])
               for i in range(4) for j in range(4))


def output_conjugate(choi, unitary):
    operator = np.kron(unitary, np.eye(D))
    return operator @ choi @ operator.conj().T


def output_depolarize(choi, gamma):
    one = [1-3*gamma/4, gamma/4, gamma/4, gamma/4]
    return sum(one[i]*one[j]*output_conjugate(choi, P[4*i+j])
               for i in range(4) for j in range(4))


def actual_map(ideal_choi, correlated_fault=.08, selector_fault=.03,
               terminal_depolarization=.01):
    # Selector fault invokes a fixed completely depolarizing fallback.
    # Otherwise a stochastic CZ fault can couple the two data wires.
    selected = ((1-correlated_fault)*ideal_choi
                + correlated_fault*output_conjugate(ideal_choi, CZ))
    selected = output_depolarize(selected, terminal_depolarization)
    return (1-selector_fault)*selected + selector_fault*JDEP


BASIS = [np.kron(P[a], P[b]) for a in range(1, 16)
         for b in range(16)]


def coordinates(choi):
    return np.array([np.trace(b @ choi).real for b in BASIS])


def trace_norm(matrix):
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def output_trace(choi):
    return np.einsum("aiaj->ij", choi.reshape(D, D, D, D))


def apply_choi(choi, state):
    return D*np.einsum("aibj,ij->ab", choi.reshape(D, D, D, D), state)


def kraus(choi):
    eigenvalues, eigenvectors = np.linalg.eigh(choi)
    assert eigenvalues.min() > -1e-10
    return [np.sqrt(D*value)*vector.reshape(D, D)
            for value, vector in zip(eigenvalues, eigenvectors.T)
            if value > 1e-13]


def embed(operator, sites, qubits):
    dim = 1 << qubits
    result = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        bits = [(col >> (qubits-1-j)) & 1 for j in range(qubits)]
        local_col = 2*bits[sites[0]]+bits[sites[1]]
        for local_row in range(4):
            out = bits.copy()
            out[sites[0]], out[sites[1]] = local_row >> 1, local_row & 1
            row = sum(bit << (qubits-1-j) for j, bit in enumerate(out))
            result[row, col] = operator[local_row, local_col]
    return result


def apply_local(choi, state, sites, qubits):
    result = np.zeros_like(state, dtype=complex)
    for operator in kraus(choi):
        full = embed(operator, sites, qubits)
        result += full @ state @ full.conj().T
    return result


def solve_palette(actual, target, entangling_index):
    matrix = np.stack([coordinates(j) for j in actual], axis=1)
    equality = np.vstack([np.ones(len(actual)), matrix])
    rhs = np.r_[1., coordinates(target)]
    bounds = [(0, None)]*len(actual)
    # Force the genuinely entangling complete branch to occur; this is not
    # merely an unused potentially bad map in the library.
    bounds[entangling_index] = (.002, None)
    result = linprog(np.zeros(len(actual)), A_eq=equality, b_eq=rhs,
                     bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    mixed = sum(w*j for w, j in zip(result.x, actual))
    return result.x, mixed


def main():
    # A small affine cross-polytope of CPTP maps around complete
    # depolarization. All perturbations have zero output partial trace.
    strength = .9
    ideal = [JDEP]
    for basis in BASIS:
        ideal.extend([JDEP + strength*basis/16,
                      JDEP - strength*basis/16])
    entangling_index = len(ideal)
    ideal.append(unitary_choi(CZ))
    actual = [actual_map(j) for j in ideal]

    inactive = product_depolarizing_choi(.9)
    sigma = (np.eye(4) + .08*np.kron(X, X) + .06*np.kron(Z, I2))/4
    replacer = np.kron(sigma, np.eye(4)/4)
    w_inactive, mixed_inactive = solve_palette(actual, inactive,
                                               entangling_index)
    w_replacer, mixed_replacer = solve_palette(actual, replacer,
                                               entangling_index)

    # Full Choi test of a channel on three data qubits, retaining three
    # reference qubits: first replace AB, then apply inactive map on BC.
    omega = np.eye(8).reshape(-1)/np.sqrt(8)
    initial = np.outer(omega, omega.conj())
    exact = apply_local(replacer, initial, (0, 1), 6)
    exact = apply_local(inactive, exact, (1, 2), 6)
    physical = apply_local(mixed_replacer, initial, (0, 1), 6)
    physical = apply_local(mixed_inactive, physical, (1, 2), 6)

    plusplus = np.ones((4, 4))/4
    branch_output = apply_choi(actual[entangling_index], plusplus)
    partial_transpose = branch_output.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1)
    partial_transpose = partial_transpose.reshape(4, 4)
    negativity = (trace_norm(partial_transpose)-1)/2

    results = {
        "menu_size": len(actual),
        "correlated_CZ_fault_probability": .08,
        "noisy_selector_fallback_probability": .03,
        "terminal_local_depolarization": .01,
        "inactive_local_depolarization": .9,
        "minimum_actual_Choi_eigenvalue": float(min(np.linalg.eigvalsh(j).min()
                                                   for j in actual)),
        "maximum_actual_TP_residual": max(trace_norm(output_trace(j)-np.eye(4)/4)
                                         for j in actual),
        "inactive_mixture_Choi_trace_error": trace_norm(mixed_inactive-inactive),
        "replacer_mixture_Choi_trace_error": trace_norm(mixed_replacer-replacer),
        "inactive_entangling_branch_weight": float(w_inactive[entangling_index]),
        "replacer_entangling_branch_weight": float(w_replacer[entangling_index]),
        "entangling_branch_output_negativity": negativity,
        "full_overlap_reference_Choi_trace_error": trace_norm(physical-exact),
        "overlap_diamond_error_upper_bound": 8*trace_norm(physical-exact),
        "inactive_positive_weights": int(np.sum(w_inactive > 1e-10)),
        "replacer_positive_weights": int(np.sum(w_replacer > 1e-10)),
    }
    assert results["maximum_actual_TP_residual"] < 1e-10
    assert results["inactive_mixture_Choi_trace_error"] < 1e-10
    assert results["replacer_mixture_Choi_trace_error"] < 1e-10
    assert results["full_overlap_reference_Choi_trace_error"] < 1e-10
    assert negativity > .2
    output = Path(__file__).with_name("complete_map_palette_results.json")
    output.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
