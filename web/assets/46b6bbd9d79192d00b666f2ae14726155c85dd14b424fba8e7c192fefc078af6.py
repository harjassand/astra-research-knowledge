#!/usr/bin/env python3
"""Exact microscopic-kernel diagnostics for a cyclic paired-determinant law.

Only the Python standard library is used.  All determinants, transition
probabilities, Dirichlet energies, and energy-constant calculations are exact
integers or Fractions.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def det_bareiss(a: list[list[int]]) -> int:
    """Fraction-free exact determinant for a square integer matrix."""
    n = len(a)
    if n == 0:
        return 1
    m = [row[:] for row in a]
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot_row = next((r for r in range(k, n) if m[r][k] != 0), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            m[k], m[pivot_row] = m[pivot_row], m[k]
            sign = -sign
        pivot = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = m[i][j] * pivot - m[i][k] * m[k][j]
                assert numerator % previous == 0
                m[i][j] = numerator // previous
        for i in range(k + 1, n):
            m[i][k] = 0
        previous = pivot
    return sign * m[n - 1][n - 1]


def cyclic_permutation(n: int) -> list[list[int]]:
    f = [[0] * n for _ in range(n)]
    for i in range(n):
        f[i][(i + 1) % n] = 1
    return f


def enumerate_microstates(f: list[list[int]]) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], int]]:
    n = len(f)
    assert n % 2 == 0
    k = n // 2
    all_states = list(combinations(range(n), k))
    weights: dict[tuple[int, ...], int] = {}
    universe = set(range(n))
    for state in all_states:
        complement = sorted(universe.difference(state))
        minor = [[f[i][j] for j in complement] for i in state]
        determinant = det_bareiss(minor)
        weight = determinant * determinant
        if weight:
            weights[state] = weight
    return all_states, weights


def mh_kernel(
    all_states: list[tuple[int, ...]],
    weights: dict[tuple[int, ...], int],
    exchange_radius: int | None,
) -> tuple[list[tuple[int, ...]], list[list[Fraction]], int]:
    """Symmetric-proposal Metropolis kernel on supported states.

    None means propose uniformly among every fixed-cardinality state.
    An integer t means propose uniformly among states at exactly t pair swaps.
    Zero-weight proposals are rejected.  Returns kernel and proposal count.
    """
    support = list(weights)
    support_sets = {s: set(s) for s in all_states}
    qmat = [[Fraction(0) for _ in support] for _ in support]
    nproposal = 0
    for i, s in enumerate(support):
        proposals = []
        for t in all_states:
            if t == s:
                continue
            swaps = len(support_sets[s] - support_sets[t])
            if exchange_radius is None or swaps == exchange_radius:
                proposals.append(t)
        if exchange_radius is None:
            # Include the current state in the uniform full-space proposal.
            proposals = [t for t in all_states]
        count = len(proposals)
        if i == 0:
            nproposal = count
        assert count == nproposal
        off_sum = Fraction(0)
        for t in proposals:
            if t == s:
                continue
            j = support.index(t) if t in weights else None
            if j is None:
                continue
            accept = min(Fraction(1), Fraction(weights[t], weights[s]))
            qmat[i][j] += accept / count
            off_sum += accept / count
        qmat[i][i] = 1 - off_sum
    # Exact detailed balance under probabilities proportional to weights.
    z = sum(weights.values())
    pi = {s: Fraction(weights[s], z) for s in support}
    for i, s in enumerate(support):
        for j, t in enumerate(support):
            assert pi[s] * qmat[i][j] == pi[t] * qmat[j][i]
    return support, qmat, nproposal


def pair_kernel(qmat: list[list[Fraction]]) -> list[list[Fraction]]:
    """One-third update first layer, one-third second, one-third layer swap."""
    m = len(qmat)
    pairs = [(i, j) for i in range(m) for j in range(m)]
    index = {x: k for k, x in enumerate(pairs)}
    p = [[Fraction(0) for _ in pairs] for _ in pairs]
    for xidx, (i, j) in enumerate(pairs):
        for ii in range(m):
            p[xidx][index[(ii, j)]] += qmat[i][ii] / 3
        for jj in range(m):
            p[xidx][index[(i, jj)]] += qmat[j][jj] / 3
        p[xidx][index[(j, i)]] += Fraction(1, 3)
    return p


def dirichlet(
    p: list[list[Fraction]],
    pi: list[Fraction],
    values: list[Fraction],
) -> Fraction:
    assert len(p) == len(pi) == len(values)
    return sum(
        (pi[i] * p[i][j] * (values[i] - values[j]) ** 2) / 2
        for i in range(len(p))
        for j in range(len(p))
    )


def two_state_heatbath_pair() -> list[list[Fraction]]:
    """Pair kernel that refreshes one of two equal-weight states per step."""
    q = [[Fraction(1, 2), Fraction(1, 2)], [Fraction(1, 2), Fraction(1, 2)]]
    m = 2
    pairs = [(i, j) for i in range(m) for j in range(m)]
    index = {x: k for k, x in enumerate(pairs)}
    p = [[Fraction(0) for _ in pairs] for _ in pairs]
    for xidx, (i, j) in enumerate(pairs):
        for ii in range(m):
            p[xidx][index[(ii, j)]] += q[i][ii] / 2
        for jj in range(m):
            p[xidx][index[(i, jj)]] += q[j][jj] / 2
    return p


def frac_record(x: Fraction) -> dict[str, str]:
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def run_case(n: int) -> dict[str, object]:
    f = cyclic_permutation(n)
    all_states, weights = enumerate_microstates(f)
    k = n // 2
    expected = [tuple(range(0, n, 2)), tuple(range(1, n, 2))]
    assert set(weights) == set(expected)
    assert all(w == 1 for w in weights.values())
    support = list(weights)
    assert len(support) == 2
    m = len(all_states)
    q = k

    # Bounded one-replica t-swap Metropolis and layer exchange.
    local_support, local_q, local_degree = mh_kernel(all_states, weights, 1)
    assert local_support == support
    assert local_q == [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    p_local = pair_kernel(local_q)
    pi_pair = [Fraction(1, 4)] * 4
    sign = [Fraction(1), Fraction(-1)]
    f_local = [sign[i] + sign[j] for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    local_energy = dirichlet(p_local, pi_pair, f_local)
    assert local_energy == 0
    # Var_pi(sign)=1 exactly.

    # Full-candidate-space, normalizer-free global MH proposal.
    global_support, global_q, global_proposals = mh_kernel(all_states, weights, None)
    assert global_support == support
    a = Fraction(1, m)
    assert global_q == [[1 - a, a], [a, 1 - a]]
    p_global = pair_kernel(global_q)
    y = 1 / (1 + 2 * a)
    f_global = [sign[i] + y * sign[j] for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    global_energy = dirichlet(p_global, pi_pair, f_global)
    predicted_energy = Fraction(4) * a * (1 + a) / (3 * (1 + 2 * a))
    assert global_energy == predicted_energy
    optimal_l = 1 / predicted_energy
    expected_l = Fraction(3 * m * (m + 2), 4 * (m + 1))
    assert optimal_l == expected_l
    # One-replica spectral gap of global MH on this two-state support.
    one_replica_gap = 2 * a

    # Exhaustive exact heat-bath refresh; then P=half refresh-A, half refresh-B.
    p_heatbath = two_state_heatbath_pair()
    f_heatbath = [sign[i] for i, _ in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    heatbath_energy = dirichlet(p_heatbath, pi_pair, f_heatbath)
    assert heatbath_energy == Fraction(1, 2)
    heatbath_l = Fraction(1, 1) / heatbath_energy
    assert heatbath_l == 2

    return {
        "n": n,
        "k": k,
        "candidate_configurations": m,
        "supported_configurations": len(weights),
        "two_replica_supported_states": len(weights) ** 2,
        "supported_states": [list(s) for s in support],
        "raw_integer_weights": [weights[s] for s in support],
        "bounded_exchange": {
            "swaps_per_proposal": 1,
            "candidate_neighbors_per_state": local_degree,
            "one_replica_kernel": [[str(x) for x in row] for row in local_q],
            "pair_kernel_energy_for_f1_eq_f2_sign": frac_record(local_energy),
            "variance_of_sign": 1,
            "energy_constant": "infinite (nonconstant additive invariant)",
        },
        "global_uniform_MH": {
            "candidate_proposals_per_state": global_proposals,
            "accepted_transition_probability_between_support_states": frac_record(a),
            "one_replica_spectral_gap": frac_record(one_replica_gap),
            "pair_additive_energy_at_minimizing_f2": frac_record(global_energy),
            "minimizing_f2_scale_relative_to_f1": frac_record(y),
            "optimal_pair_energy_constant": frac_record(optimal_l),
        },
        "exhaustive_heatbath": {
            "determinant_evaluations_to_build_weights": m,
            "pair_additive_energy_with_f2_zero": frac_record(heatbath_energy),
            "optimal_pair_energy_constant": frac_record(heatbath_l),
        },
    }


def main() -> None:
    cases = [run_case(n) for n in (4, 6, 8, 10, 12)]
    result = {
        "status": "PASS",
        "arithmetic": "exact integer and Fraction",
        "matrix_family": "F[i,(i+1) mod n]=1, all other entries zero",
        "claim_scope": "finite checks corroborate the general directed-cycle proof in INITIAL.txt",
        "cases": cases,
    }
    out = Path(__file__).with_name("exact_kernels_result.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
