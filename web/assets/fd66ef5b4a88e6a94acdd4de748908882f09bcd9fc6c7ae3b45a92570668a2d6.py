#!/usr/bin/env python3
"""Exact type-A SU(m) LR and zero-weight multiplicity routines.

All multiplicities are counted by integer tableau enumeration. No numerical
character package or floating-point tensor decomposition is used.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product


def partitions(total, length, ceiling=None):
    if length == 0:
        if total == 0:
            yield ()
        return
    if ceiling is None:
        ceiling = total
    for first in range(min(ceiling, total), -1, -1):
        for tail in partitions(total - first, length - 1, first):
            yield (first,) + tail


@lru_cache(maxsize=None)
def tableau_count(shape, inner, content, lattice_word):
    """Count SSYT of shape/inner and content, optionally LR-lattice word."""
    m = len(shape)
    if len(inner) != m or len(content) != m:
        raise ValueError("shape, inner, and content must have equal length")
    if any(shape[i] < inner[i] for i in range(m)):
        return 0
    if sum(shape[i] - inner[i] for i in range(m)) != sum(content):
        return 0

    # Standard LR reading order: right to left within each row, top to bottom.
    cells = tuple(
        (row, col)
        for row in range(m)
        for col in range(shape[row] - 1, inner[row] - 1, -1)
    )
    counts = [0] * m
    filled = {}
    ways = 0

    def recurse(position):
        nonlocal ways
        if position == len(cells):
            ways += 1
            return
        row, col = cells[position]
        right_value = filled.get((row, col + 1))
        above_value = filled.get((row - 1, col))
        for value in range(1, m + 1):
            i = value - 1
            if counts[i] >= content[i]:
                continue
            if right_value is not None and value > right_value:
                continue  # rows are weakly increasing left to right
            if above_value is not None and value <= above_value:
                continue  # columns are strictly increasing top to bottom
            counts[i] += 1
            if lattice_word and value > 1 and counts[i] > counts[i - 1]:
                counts[i] -= 1
                continue
            filled[(row, col)] = value
            recurse(position + 1)
            del filled[(row, col)]
            counts[i] -= 1

    recurse(0)
    return ways


def lr_coefficient(lam, mu, gamma):
    if any(gamma[i] < lam[i] for i in range(len(lam))):
        return 0
    return tableau_count(gamma, lam, mu, True)


def canonical_partition(dynkin):
    m = len(dynkin) + 1
    return tuple(sum(dynkin[i:]) for i in range(m - 1)) + (0,)


def dual_partition(lam):
    return tuple(lam[0] - lam[-1 - i] for i in range(len(lam)))


def dynkin_from_partition(partition):
    return tuple(partition[i] - partition[i + 1] for i in range(len(partition) - 1))


def dimension(partition):
    m = len(partition)
    value = Fraction(1)
    for i in range(m):
        for j in range(i + 1, m):
            value *= Fraction(partition[i] - partition[j] + j - i, j - i)
    assert value.denominator == 1
    return value.numerator


def casimir(partition):
    """SU(m) quadratic Casimir for Tr_fund(T_a T_b)=delta_ab/2."""
    m = len(partition)
    total = sum(partition)
    gl_scalar = sum(
        partition[i] * (partition[i] + m + 1 - 2 * (i + 1))
        for i in range(m)
    )
    return Fraction(gl_scalar, 2) - Fraction(total * total, 2 * m)


@lru_cache(maxsize=None)
def zero_weight_multiplicity(partition):
    m = len(partition)
    total = sum(partition)
    if total % m:
        return 0
    q = total // m
    return tableau_count(partition, (0,) * m, (q,) * m, False)


def end_decomposition(dynkin):
    """Decompose V_lambda tensor V_lambda^* by the GL(m) LR rule."""
    lam = canonical_partition(dynkin)
    mu = dual_partition(lam)
    total_size = sum(lam) + sum(mu)
    m = len(lam)
    decomposition = {}
    lr_witnesses = {}
    for gamma in partitions(total_size, m):
        if any(gamma[i] < lam[i] for i in range(m)):
            continue
        coefficient = lr_coefficient(lam, mu, gamma)
        if not coefficient:
            continue
        delta = tuple(gamma[i] - gamma[-1] for i in range(m))
        nu = dynkin_from_partition(delta)
        decomposition[nu] = decomposition.get(nu, 0) + coefficient
        lr_witnesses[nu] = (gamma, coefficient)
    return lam, mu, decomposition, lr_witnesses


def cumulative_profile(decomposition, m, T):
    return sum(
        multiplicity * dimension(canonical_partition(nu))
        for nu, multiplicity in decomposition.items()
        if casimir(canonical_partition(nu)) <= T
    )


def low_rank_profile_integral(decomposition, m, carrier_dim, q):
    """Exact integral int [1-q D(T)/d]_+ dT from the finite step profile."""
    masses = {}
    for nu, multiplicity in decomposition.items():
        delta = canonical_partition(nu)
        c = casimir(delta)
        masses[c] = masses.get(c, 0) + multiplicity * dimension(delta)
    thresholds = sorted(masses)
    cumulative = 0
    left = Fraction(0)
    integral = Fraction(0)
    for threshold in thresholds:
        value = Fraction(1) - Fraction(q * cumulative, carrier_dim)
        if value <= 0:
            break
        integral += (threshold - left) * value
        cumulative += masses[threshold]
        left = threshold
    return integral


def near_full_green_profile(decomposition, m, carrier_dim, k):
    """Exact profile proxy int min(1,k D_+(t)/d) t^-2 dt."""
    masses = {}
    for nu, multiplicity in decomposition.items():
        delta = canonical_partition(nu)
        c = casimir(delta)
        if c > 0:
            masses[c] = masses.get(c, 0) + multiplicity * dimension(delta)
    thresholds = sorted(masses)
    if not thresholds:
        return Fraction(0)
    cumulative = 0
    left = thresholds[0]
    result = Fraction(0)
    for threshold in thresholds[1:]:
        cumulative += masses[left]
        height = min(Fraction(1), Fraction(k * cumulative, carrier_dim))
        result += height * (Fraction(1, left) - Fraction(1, threshold))
        left = threshold
    cumulative += masses[left]
    height = min(Fraction(1), Fraction(k * cumulative, carrier_dim))
    result += height / left  # exact saturated tail to infinity
    return result


def search_dimension(m, max_label):
    label_tuples = list(product(range(max_label + 1), repeat=m - 1))
    failures = []
    compared = 0
    equality_count = 0
    maximum_ratio = Fraction(0)
    maximum_record = None
    maximum_nontrivial_ratio = Fraction(0)
    maximum_nontrivial_record = None
    maximum_regular_ratio = Fraction(0)
    maximum_regular_record = None
    regular_count = 0
    boundary_count = 0
    profile_rows = []

    for labels in label_tuples:
        lam, mu, decomposition, witnesses = end_decomposition(labels)
        carrier_dim = dimension(lam)
        if all(x > 0 for x in labels):
            regular_count += 1
        elif any(x > 0 for x in labels):
            boundary_count += 1

        reconstructed_dim2 = sum(
            multiplicity * dimension(canonical_partition(nu))
            for nu, multiplicity in decomposition.items()
        )
        if reconstructed_dim2 != carrier_dim * carrier_dim:
            raise AssertionError(
                f"dimension sum failed for SU({m}), lambda={labels}: "
                f"{reconstructed_dim2} != {carrier_dim**2}"
            )

        for nu, multiplicity in decomposition.items():
            delta = canonical_partition(nu)
            zero = zero_weight_multiplicity(delta)
            compared += 1
            if multiplicity > zero:
                failures.append(
                    {
                        "lambda": labels,
                        "nu": nu,
                        "multiplicity": multiplicity,
                        "zero_weight": zero,
                        "gamma_witness": witnesses[nu][0],
                    }
                )
            if multiplicity == zero:
                equality_count += 1
            ratio = Fraction(multiplicity, max(1, zero))
            if ratio > maximum_ratio:
                maximum_ratio = ratio
                maximum_record = (labels, nu, multiplicity, zero)
            if any(nu) and ratio > maximum_nontrivial_ratio:
                maximum_nontrivial_ratio = ratio
                maximum_nontrivial_record = (labels, nu, multiplicity, zero)
            if all(x > 0 for x in labels) and any(nu) and ratio > maximum_regular_ratio:
                maximum_regular_ratio = ratio
                maximum_regular_record = (labels, nu, multiplicity, zero)

        # Record exact step-profile diagnostics along the regular ray.
        if all(x == labels[0] and x > 0 for x in labels):
            delta_min = min(labels) + 1
            p = m * (m - 1) // 2
            T = Fraction(delta_min * delta_min, 2)
            if T >= 1:
                profile_rows.append(
                    (labels[0], carrier_dim, T,
                     cumulative_profile(decomposition, m, T), p,
                     low_rank_profile_integral(decomposition, m, carrier_dim, 1),
                     near_full_green_profile(decomposition, m, carrier_dim, 1))
                )

    failures.sort(key=lambda z: (sum(z["lambda"]), z["lambda"], z["nu"]))
    return {
        "m": m,
        "max_label": max_label,
        "lambda_count": len(label_tuples),
        "regular_count": regular_count,
        "boundary_count": boundary_count,
        "comparisons": compared,
        "equalities": equality_count,
        "max_ratio": maximum_ratio,
        "max_record": maximum_record,
        "max_nontrivial_ratio": maximum_nontrivial_ratio,
        "max_nontrivial_record": maximum_nontrivial_record,
        "max_regular_ratio": maximum_regular_ratio,
        "max_regular_record": maximum_regular_record,
        "failures": failures,
        "profile_rows": profile_rows,
    }


def main():
    # Finite search boxes: all labels 0..12 for SU(3), 0..4 for SU(4).
    for m, bound in ((3, 12), (4, 4)):
        result = search_dimension(m, bound)
        print(
            f"SU({m}) labels 0..{bound}: lambda_count={result['lambda_count']}, "
            f"regular={result['regular_count']}, boundary={result['boundary_count']}, "
            f"output comparisons={result['comparisons']}, "
            f"equality cases={result['equalities']}, "
            f"max multiplicity/zero-weight={result['max_ratio']} "
            f"at {result['max_record']}; max nontrivial ratio="
            f"{result['max_nontrivial_ratio']} at {result['max_nontrivial_record']}; "
            f"max regular ratio={result['max_regular_ratio']} "
            f"at {result['max_regular_record']}"
        )
        if result["failures"]:
            print("FIRST COUNTEREXAMPLE:", result["failures"][0])
        else:
            print("No counterexample in this finite search box.")
        print("regular-ray profile diagnostics (label, d, T, D(T), p, Phi_1, S_1):")
        for row in result["profile_rows"]:
            print("  ", row)


if __name__ == "__main__":
    main()
