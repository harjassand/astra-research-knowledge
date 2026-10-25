#!/usr/bin/env python3
"""Independent finite-count reconstruction for the Chain Theory alpha example.

Uses only Python's standard library.  It enumerates the six pairs of four slots,
then the signed exchange orbits described in the author's preprint.  It does not
import or execute the author's Lean file.

Run from the project root:
    python3 work/l02/chain_alpha_reconstruction.py
"""

from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations


# Four read slots, with traceless-basis sizes for qutrit/qubit/qutrit/qubit.
SLOT_NAMES = ("Q1", "q1", "Q2", "q2")
SLOT_DIMS = (8, 3, 8, 3)
# Exchanging the two read links sends 0<->2 and 1<->3.
EXCHANGE = (2, 3, 0, 1)


def exchange(record):
    """Move each old slot to its exchanged slot (an involution)."""
    return tuple(record[old_slot] for old_slot in EXCHANGE)


def enumerate_products():
    """Every two-letter product: choose two distinct slots and one letter each."""
    products = []
    for s1, s2 in combinations(range(4), 2):
        for i in range(SLOT_DIMS[s1]):
            for j in range(SLOT_DIMS[s2]):
                record = [None] * 4
                record[s1], record[s2] = i, j
                products.append(tuple(record))
    return products


def slot_pair(record):
    return tuple(i for i, letter in enumerate(record) if letter is not None)


def same_end(record):
    s1, s2 = slot_pair(record)
    return s1 % 2 == s2 % 2


def exchange_orbits(products):
    """Yield the one-element fixed or two-element orbits under slot exchange."""
    remaining = set(products)
    while remaining:
        p = min(remaining, key=lambda r: tuple(-1 if x is None else x for x in r))
        q = exchange(p)
        assert q in remaining
        if p == q:
            remaining.remove(p)
            yield (p,)
        else:
            remaining.remove(p)
            remaining.remove(q)
            yield (p, q)


def matrix_product(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def matrix_subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(2)] for i in range(2)]


def check_qubit_commutators():
    """Check commutators and order-sign record survival in the real Pauli basis."""
    basis = (
        [[0, 1], [1, 0]],       # symmetric off-diagonal
        [[0, 1], [-1, 0]],      # antisymmetric off-diagonal
        [[1, 0], [0, -1]],      # diagonal
    )
    pairs = list(combinations(range(3), 2))
    for i, j in pairs:
        comm = matrix_subtract(matrix_product(basis[i], basis[j]),
                               matrix_product(basis[j], basis[i]))
        reverse = matrix_subtract(matrix_product(basis[j], basis[i]),
                                  matrix_product(basis[i], basis[j]))
        assert comm != [[0, 0], [0, 0]]
        assert reverse == [[-x for x in row] for row in comm]
        assert any(
            comm == [[c * x for x in row] for row in target]
            for target in basis
            for c in (-2, -1, 1, 2)
        )

        # The record is C_ij at far slot 1 minus C_ij at far slot 3.  Both
        # read exchange and link exchange swap those slots, returning -record;
        # its commutator/order sign is also -1, so it survives both.
        coeff = next(
            c for target in basis for c in (-2, -1, 1, 2)
            if comm == [[c * x for x in row] for row in target]
        )
        form = ((1, coeff), (3, -coeff))
        image = tuple(sorted((EXCHANGE[slot], c) for slot, c in form))
        own_negative = tuple(sorted((slot, -c) for slot, c in form))
        assert image == own_negative

    # The Weyl phase is a sign only when the primitive d-th root is real:
    # among dimensions >=2, this occurs at d=2, not d=3.
    def weyl_phase_is_sign(d):
        return d >= 2 and 2 % d == 0

    assert weyl_phase_is_sign(2) and not weyl_phase_is_sign(3)
    return len(pairs) if weyl_phase_is_sign(2) else 0


def main():
    products = enumerate_products()
    assert len(products) == 169
    assert len(set(products)) == len(products)

    orbits = list(exchange_orbits(products))
    fixed = [orbit[0] for orbit in orbits if len(orbit) == 1]
    paired = [orbit for orbit in orbits if len(orbit) == 2]
    same_end_orbits = [o for o in orbits if same_end(o[0])]
    cross_end_orbits = [o for o in orbits if not same_end(o[0])]
    assert len(fixed) == 11
    assert len(paired) == 79
    assert len(fixed) + 2 * len(paired) == len(products)
    assert len(same_end_orbits) == 42  # 11 fixed + 31 two-element orbits
    assert len(cross_end_orbits) == 48
    assert sum(1 for p in products if same_end(p)) == 73
    assert sum(1 for p in products if not same_end(p)) == 96

    # Convert each product orbit into its exchange-adapted record(s).
    # In same-end sectors, the signed read-exchange eigenvalue supplies X;
    # in cross-end sectors, X is inactive and the signed link exchange supplies Y.
    sectors = Counter()
    for orbit in orbits:
        if same_end(orbit[0]):
            if len(orbit) == 1:
                sectors[(-1, +1)] += 1  # fixed product survives X
            else:
                sectors[(-1, +1)] += 1  # symmetric combination survives X
                sectors[(+1, +1)] += 1  # antisymmetric combination does not
        else:
            assert len(orbit) == 2
            sectors[(+1, -1)] += 1  # symmetric combination survives Y
            sectors[(+1, +1)] += 1  # antisymmetric combination does not

    # Three unordered pairs of qubit letters yield one order-sign record each.
    commutators = check_qubit_commutators()
    sectors[(-1, -1)] += commutators
    assert sectors == Counter({(+1, +1): 79, (+1, -1): 48,
                               (-1, +1): 42, (-1, -1): 3})
    assert sum(sectors.values()) == 172

    # The unread pair contributes (3^2-1)(2^2-1); each read link has (3*2)^2.
    readout_dimension = (3**2 - 1) * (2**2 - 1) * (3 * 2) ** 4
    assert readout_dimension == 31104

    # Each surviving X contributes 3 to k; surviving Y contributes 2.
    radical_counts = Counter()
    for (x, y), count in sectors.items():
        k = (3 if x == -1 else 1) * (2 if y == -1 else 1)
        radical_counts[k] += count
    assert radical_counts == Counter({1: 79, 2: 48, 3: 42, 6: 3})

    # Exact arithmetic is the formal Q-basis coefficient vector for
    # (1, sqrt(2), sqrt(3), sqrt(6)) over the exact integer denominator.
    exact_coefficients = tuple(Fraction(radical_counts[k], readout_dimension)
                               for k in (1, 2, 3, 6))
    assert exact_coefficients == (
        Fraction(79, 31104), Fraction(1, 648),
        Fraction(7, 5184), Fraction(1, 10368),
    )

    with localcontext() as ctx:
        ctx.prec = 60
        numerator = (Decimal(79) + Decimal(48) * Decimal(2).sqrt()
                     + Decimal(42) * Decimal(3).sqrt()
                     + Decimal(3) * Decimal(6).sqrt())
        alpha_candidate = numerator / Decimal(readout_dimension)
        inverse_candidate = Decimal(1) / alpha_candidate

    print("product records:", len(products))
    print("exchange fixed products:", len(fixed))
    print("two-product exchange orbits:", len(paired))
    print("records by (X,Y):", dict(sorted(sectors.items())))
    print("total records:", sum(sectors.values()))
    print("readout dimension:", readout_dimension)
    print("radical counts:", dict(sorted(radical_counts.items())))
    print("exact coefficient vector:", exact_coefficients)
    print("alpha candidate:", alpha_candidate)
    print("inverse candidate:", inverse_candidate)
    print("PASS")


if __name__ == "__main__":
    main()
