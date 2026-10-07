#!/usr/bin/env python3
"""Exact audit of a local paired-basis Metropolis worm kernel.

Uses only fractions and the six-term determinant formula for 3x3 minors.
The result is a scoped counterexample to this kernel family, not to all
microscopic samplers or to determinant-weighted parity counting.
"""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

N = 6
K = 3
EVEN_MODE = (0, 2, 4)
ODD_MODE = (1, 3, 5)


def sign_of_permutation(p):
    inversions = sum(p[a] > p[b] for a in range(len(p)) for b in range(a + 1, len(p)))
    return -1 if inversions % 2 else 1


def determinant3(matrix):
    total = Fraction(0)
    for p in permutations(range(3)):
        term = Fraction(sign_of_permutation(p))
        for row in range(3):
            term *= matrix[row][p[row]]
        total += term
    return total


def make_matrix(epsilon):
    matrix = [[Fraction(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        matrix[i][(i + 1) % N] = Fraction(1)
        matrix[i][(i - 1) % N] = epsilon
    return matrix


def amplitude(matrix, state):
    complement = tuple(i for i in range(N) if i not in state)
    minor = [[matrix[i][j] for j in complement] for i in state]
    return determinant3(minor)


def fstr(value):
    return f"{value.numerator}/{value.denominator}"


def run(bits):
    if bits < 1:
        raise ValueError("bits must be at least 1")
    epsilon = Fraction(1, 2**bits)
    matrix = make_matrix(epsilon)
    states = list(combinations(range(N), K))
    amps = {state: amplitude(matrix, state) for state in states}
    weights = {state: amps[state] ** 2 for state in states}
    z = sum(weights.values(), Fraction(0))
    mode_weight = weights[ODD_MODE]
    p = mode_weight / z

    neighbors = []
    for removed in ODD_MODE:
        for added in EVEN_MODE:
            state = tuple(sorted((set(ODD_MODE) - {removed}) | {added}))
            neighbors.append({
                "state": list(state),
                "amplitude": fstr(amps[state]),
                "weight": fstr(weights[state]),
            })

    # One-replica proposal: choose removed in I and added outside I uniformly.
    # The symmetric proposal probability is 1/9. Zero-weight destinations reject.
    exit_probability = sum(
        (min(Fraction(1), weights[tuple(sorted((set(ODD_MODE) - {removed}) | {added}))] / mode_weight)
         for removed in ODD_MODE for added in EVEN_MODE),
        Fraction(0),
    ) / 9

    expected_exit_formula = (epsilon**2 + epsilon**4) / (3 * (1 + epsilon**3) ** 2)
    assert exit_probability == expected_exit_formula
    assert weights[EVEN_MODE] == mode_weight == (1 + epsilon**3) ** 2
    assert 2 * mode_weight < z  # the singleton mode is the smaller side of the cut.

    positive = {state for state in states if weights[state] > 0}
    unseen = set(positive)
    frontier = [next(iter(unseen))]
    unseen.remove(frontier[0])
    while frontier:
        current = frontier.pop()
        for removed in current:
            for added in set(range(N)) - set(current):
                candidate = tuple(sorted((set(current) - {removed}) | {added}))
                if candidate in unseen:
                    unseen.remove(candidate)
                    frontier.append(candidate)
    connected = not unseen
    assert connected

    # Product pair kernel P: with probability 1/2 swap replicas; otherwise
    # choose one replica uniformly and apply the above one-replica Metropolis move.
    # For G(A,B)=1_{A=ODD_MODE}+1_{B=ODD_MODE}, replica swapping contributes zero.
    variance_g = 2 * p * (1 - p)
    variance_f = p * (1 - p)
    dirichlet_single_indicator = p * exit_probability
    dirichlet_g = dirichlet_single_indicator / 2
    ratio = variance_f / dirichlet_g

    return {
        "epsilon": fstr(epsilon),
        "epsilon_bit_parameter": bits,
        "matrix": [[fstr(x) for x in row] for row in matrix],
        "microstate_count": len(states),
        "positive_microstate_count": len(positive),
        "positive_support_local_exchange_connected": connected,
        "Z": fstr(z),
        "odd_mode": list(ODD_MODE),
        "even_mode": list(EVEN_MODE),
        "odd_mode_weight": fstr(mode_weight),
        "stationary_probability_odd_mode": fstr(p),
        "stationary_probability_odd_mode_decimal": float(p),
        "odd_mode_neighbors": neighbors,
        "single_replica_conductance_exact": fstr(exit_probability),
        "single_replica_conductance_decimal": float(exit_probability),
        "pair_test_function": "1[A=odd_mode] + 1[B=odd_mode]",
        "pair_variance_exact": fstr(variance_g),
        "theorem_lhs_variance_exact": fstr(variance_f),
        "pair_dirichlet_exact": fstr(dirichlet_g),
        "variance_over_dirichlet_exact": fstr(ratio),
        "variance_over_dirichlet_decimal": float(ratio),
    }


if __name__ == "__main__":
    bit_values = [int(value) for value in sys.argv[1:]] or [4, 8, 16]
    results = [run(bits) for bits in bit_values]
    out = Path(__file__).with_name("worm_conductance_results.json")
    out.write_text(json.dumps({"results": results}, indent=2) + "\n")
    print(json.dumps({
        "output": str(out),
        "results": [
            {key: result[key] for key in (
                "epsilon_bit_parameter", "epsilon", "Z",
                "stationary_probability_odd_mode",
                "single_replica_conductance_exact",
                "theorem_lhs_variance_exact", "pair_dirichlet_exact",
                "variance_over_dirichlet_exact", "positive_support_local_exchange_connected",
            )}
            for result in results
        ],
    }, indent=2))
