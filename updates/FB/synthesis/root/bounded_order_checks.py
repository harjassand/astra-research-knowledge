"""Independent finite CAR fixtures; exact integers and floating checks separated."""
import itertools
import json
import math
from pathlib import Path
import numpy as np


def subsets(n, q):
    return list(itertools.combinations(range(n), q))


def states(n, q):
    return [sum(1 << j for j in s) for s in subsets(n, q)]


def monomial(state, creators, annihilators):
    sign = 1
    for mode in annihilators:
        if not state & (1 << mode):
            return None
        if (state & ((1 << mode) - 1)).bit_count() % 2:
            sign = -sign
        state ^= 1 << mode
    for mode in reversed(creators):
        if state & (1 << mode):
            return None
        if (state & ((1 << mode) - 1)).bit_count() % 2:
            sign = -sign
        state ^= 1 << mode
    return state, sign


def lift(n, q, particle_number, coefficient):
    basis = states(n, particle_number)
    index = {s: j for j, s in enumerate(basis)}
    out = np.zeros((len(basis), len(basis)), dtype=coefficient.dtype)
    if q > particle_number:
        return out
    labels = subsets(n, q)
    for j, state in enumerate(basis):
        for b, annihilators in enumerate(labels):
            for a, creators in enumerate(labels):
                if coefficient[a, b] == 0:
                    continue
                result = monomial(state, creators, annihilators)
                if result is not None:
                    final, sign = result
                    out[index[final], j] += sign * coefficient[a, b]
    return out


def operator(n, coefficients, particle_number):
    size = math.comb(n, particle_number)
    out = np.zeros((size, size), dtype=coefficients[0].dtype)
    for q, coefficient in enumerate(coefficients):
        out += lift(n, q, particle_number, coefficient)
    return out


def reconstruct(n, restrictions):
    coefficients = []
    for q, supplied in enumerate(restrictions):
        residual = supplied.copy()
        for ell, known in enumerate(coefficients):
            residual -= lift(n, ell, q, known)
        coefficients.append(residual)
    return coefficients


def norm(matrix):
    return float(np.max(np.abs(np.linalg.eigvalsh(matrix))))


def main():
    rng = np.random.default_rng(130026)
    counts = dict(exact_reconstructions=0, exact_all_sector_equalities=0,
                  exact_sharp_identity_lifts=0, floating_lift_norms=0,
                  floating_coefficient_error_bounds=0,
                  floating_all_sector_error_bounds=0)
    max_norm_ratio = 0.0
    for n, p in [(3, 1), (4, 2), (5, 2), (5, 3), (6, 2), (6, 3)]:
        coefficients = []
        for q in range(p + 1):
            raw = rng.integers(-3, 4, (math.comb(n, q),) * 2)
            coefficients.append((raw + raw.T).astype(np.int64))
        restrictions = [operator(n, coefficients, q) for q in range(p + 1)]
        recovered = reconstruct(n, restrictions)
        assert all(np.array_equal(a, b) for a, b in zip(coefficients, recovered))
        counts['exact_reconstructions'] += 1
        for number in range(n + 1):
            assert np.array_equal(operator(n, coefficients, number),
                                  operator(n, recovered, number))
            counts['exact_all_sector_equalities'] += 1
            for q in range(p + 1):
                identity = np.eye(math.comb(n, q), dtype=np.int64)
                expected = math.comb(number, q) if q <= number else 0
                assert np.array_equal(lift(n, q, number, identity),
                                      expected * np.eye(math.comb(n, number), dtype=np.int64))
                counts['exact_sharp_identity_lifts'] += 1
                if q <= number:
                    lhs = norm(lift(n, q, number, coefficients[q].astype(float)))
                    rhs = expected * norm(coefficients[q])
                    assert lhs <= rhs + 1e-10
                    max_norm_ratio = max(max_norm_ratio, lhs / rhs if rhs else 0)
                    counts['floating_lift_norms'] += 1
        noisy = []
        delta = []
        for restricted in restrictions:
            raw = rng.normal(size=restricted.shape)
            error = 1e-5 * (raw + raw.T)
            noisy.append(restricted + error)
            delta.append(norm(error))
        noisy_coefficients = reconstruct(n, noisy)
        budgets = []
        for q in range(p + 1):
            budgets.append(delta[q] + sum(math.comb(q, ell) * budgets[ell]
                                           for ell in range(q)))
            assert norm(noisy_coefficients[q] - coefficients[q]) <= budgets[q] + 1e-10
            counts['floating_coefficient_error_bounds'] += 1
        for number in range(n + 1):
            bound = sum(math.comb(number, q) * budgets[q]
                        for q in range(min(p, number) + 1))
            error = operator(n, noisy_coefficients, number) - operator(n, coefficients, number)
            assert norm(error) <= bound + 1e-10
            counts['floating_all_sector_error_bounds'] += 1
    result = dict(status='PASS', seed=130026, fixtures=counts,
                  largest_floating_lift_ratio=max_norm_ratio,
                  exact_scope='Integer CAR actions/reconstruction and identity factors; no floating decision.',
                  floating_scope='Finite eigensolver diagnostics at tolerance1e-10; no interval certification.',
                  boundary='Finite implementation checks; written proof, acquisition and external validation remain separate.')
    Path('bounded_order_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
