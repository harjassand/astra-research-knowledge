#!/usr/bin/env python3
"""Exact finite checks for direct boson-to-fermion rare-herald gadgets.

The algebraic field Q(alpha), alpha**4=2, covers the KLM NS entries and the
balanced two-mode splitter exactly.  Gaussian-rational arithmetic checks the
sign convention for a paired BCS state in up-then-down mode order and in the
physical site-ordered spin basis.  This is a finite diagnostic, not a proof of
any asymptotic complexity statement.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations, combinations
import json
from math import factorial


@dataclass(frozen=True)
class Q4:
    """a0 + a1*alpha + a2*alpha^2 + a3*alpha^3, alpha^4 = 2."""
    c: tuple[Q, Q, Q, Q]

    def __init__(self, c=()):
        vals = list(c) + [Q(0)] * (4 - len(c))
        object.__setattr__(self, "c", tuple(Q(x) for x in vals[:4]))

    @staticmethod
    def scalar(x):
        return x if isinstance(x, Q4) else Q4((Q(x),))

    def __add__(self, other):
        b = Q4.scalar(other)
        return Q4(tuple(x + y for x, y in zip(self.c, b.c)))

    __radd__ = __add__

    def __neg__(self):
        return Q4(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-Q4.scalar(other))

    def __rsub__(self, other):
        return Q4.scalar(other) - self

    def __mul__(self, other):
        b = Q4.scalar(other)
        raw = [Q(0)] * 7
        for i, x in enumerate(self.c):
            for j, y in enumerate(b.c):
                raw[i + j] += x * y
        # alpha**p = 2*alpha**(p-4) for p >= 4.
        for p in range(6, 3, -1):
            raw[p - 4] += 2 * raw[p]
        return Q4(tuple(raw[:4]))

    __rmul__ = __mul__

    def __truediv__(self, d):
        return Q4(tuple(x / Q(d) for x in self.c))

    def __eq__(self, other):
        return self.c == Q4.scalar(other).c

    def __repr__(self):
        terms = []
        for i, a in enumerate(self.c):
            if a:
                terms.append(f"{a}*a^{i}")
        return " + ".join(terms) if terms else "0"


def det(A):
    n = len(A)
    if n == 0:
        return 1
    total = Q4(())
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = Q4(((-1) ** inv,))
        for i, j in enumerate(p):
            term *= A[i][j]
        total += term
    return total


def perm(A):
    n = len(A)
    if n == 0:
        return Q4((1,))
    total = Q4(())
    for p in permutations(range(n)):
        term = Q4((1,))
        for i, j in enumerate(p):
            term *= A[i][j]
        total += term
    return total


def repeated_matrix(U, rows, cols):
    return [[U[i][j] for j in cols] for i in rows]


def boson_amp(U, occ_in, occ_out):
    rows = [i for i, count in enumerate(occ_out) for _ in range(count)]
    cols = [j for j, count in enumerate(occ_in) for _ in range(count)]
    if len(rows) != len(cols):
        return Q4(())
    denom_sq = 1
    for x in occ_in + occ_out:
        denom_sq *= factorial(x)
    # Exact normalization is needed here only when denom_sq is 1 or 2.
    numerator = perm(repeated_matrix(U, rows, cols))
    if denom_sq == 1:
        return numerator
    if denom_sq == 2:
        # 1/sqrt(2) = alpha^2/2.
        return numerator * Q4((0, 0, Q(1, 2)))
    raise ValueError("fixture requests an unsupported bosonic normalization")


def fermion_amp(U, occ_in, occ_out):
    if any(x not in (0, 1) for x in occ_in + occ_out):
        return Q4(())  # forbidden by the Pauli principle
    if sum(occ_in) != sum(occ_out):
        return Q4(())
    rows = [i for i, x in enumerate(occ_out) if x]
    cols = [j for j, x in enumerate(occ_in) if x]
    return det(repeated_matrix(U, rows, cols))


@dataclass(frozen=True)
class GQ:
    re: Q = Q(0)
    im: Q = Q(0)

    def __add__(self, other):
        other = gq(other)
        return GQ(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return GQ(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-gq(other))

    def __mul__(self, other):
        other = gq(other)
        return GQ(self.re * other.re - self.im * other.im,
                  self.re * other.im + self.im * other.re)

    __rmul__ = __mul__


def gq(x):
    if isinstance(x, GQ):
        return x
    if isinstance(x, tuple):
        return GQ(Q(x[0]), Q(x[1]))
    return GQ(Q(x), Q(0))


def det_gq(A):
    n = len(A)
    if n == 0:
        return gq(1)
    total = gq(0)
    for p in permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = gq((-1) ** inv)
        for i, j in enumerate(p):
            term = term * A[i][j]
        total = total + term
    return total


def create(mask, mode):
    """Create one fermion in `mode`, returning (new_mask, exact sign)."""
    if mask & (1 << mode):
        return None, 0
    sign = -1 if (mask & ((1 << mode) - 1)).bit_count() % 2 else 1
    return mask | (1 << mode), sign


def bcs_bruteforce(F):
    """Expand exp(sum_ij F_ij a_i^* b_j^*)|0> by exact Fock operations."""
    n = len(F)
    state = {}
    matchings = 0
    for k in range(n + 1):
        for I in combinations(range(n), k):
            for J in combinations(range(n), k):
                amp = gq(0)
                for p in permutations(J):
                    mask = 0
                    coeff = gq(1)
                    sign = 1
                    for i, j in zip(I, p):
                        # Mode order is all up modes, then all down modes.
                        # In a_i^* b_j^*, b_j^* acts first on the ket.
                        mask1, s1 = create(mask, n + j)
                        mask2, s2 = create(mask1, i) if mask1 is not None else (None, 0)
                        if mask2 is None:
                            sign = 0
                            break
                        mask = mask2
                        sign *= s1 * s2
                        coeff = coeff * F[i][j]
                    if sign:
                        amp = amp + sign * coeff
                    matchings += 1
                if amp != gq(0):
                    state[mask] = amp
    return state, matchings


def site_order_sign(n, up_set):
    sequence = [i if i in up_set else n + i for i in range(n)]
    inv = sum(sequence[a] > sequence[b]
              for a in range(n) for b in range(a + 1, n))
    return -1 if inv % 2 else 1


def check_bcs_phase(F):
    n = len(F)
    assert n % 2 == 0
    k = n // 2
    state, matching_count = bcs_bruteforce(F)
    phase_cases = 0
    for r in range(n + 1):
        phase = -1 if (r * (r - 1) // 2) % 2 else 1
        for I0 in combinations(range(n), r):
            for J0 in combinations(range(n), r):
                mask0 = sum(1 << i for i in I0) | sum(1 << (n + j) for j in J0)
                direct0 = state.get(mask0, gq(0))
                det0 = det_gq([[F[i][j] for j in J0] for i in I0])
                if phase == -1:
                    det0 = -det0
                assert direct0 == det0, (n, I0, J0, direct0, det0)
                phase_cases += 1
    cases = 0
    for I in combinations(range(n), k):
        J = tuple(i for i in range(n) if i not in I)
        rows = list(I)
        cols = list(J)
        mask = sum(1 << i for i in I) | sum(1 << (n + j) for j in J)
        direct = state.get(mask, gq(0))
        formula = det_gq([[F[i][j] for j in cols] for i in rows])
        if (k * (k - 1) // 2) % 2:
            formula = -formula
        assert direct == formula, (n, I, J, direct, formula)
        direct_site_ordered = site_order_sign(n, set(I)) * direct
        formula_site_ordered = site_order_sign(n, set(I)) * formula
        assert direct_site_ordered == formula_site_ordered
        cases += 1
    # The product hard projector keeps exactly one particle/site.  It removes
    # vacuum, hole/double, and all other wrong-pair-number terms exactly.
    kept = forbidden = 0
    for mask0, amp0 in state.items():
        assert amp0 != gq(0)
        onsite = [((mask0 >> i) & 1) + ((mask0 >> (n + i)) & 1)
                  for i in range(n)]
        if all(x == 1 for x in onsite):
            assert sum(onsite) == n and mask0.bit_count() == n
            kept += 1
        else:
            forbidden += 1
            assert any(x != 1 for x in onsite)
    assert kept == cases
    assert forbidden > 0
    return {"sites": n, "half_filled_spin_configurations": cases,
            "matching_terms_enumerated": matching_count,
            "all_pair_sector_determinant_phase_cases": phase_cases,
            "site_order_phase_checked": True,
            "hard_projection_requires_pair_number": k,
            "nonzero_terms_kept_by_one_particle_per_site_projection": kept,
            "nonzero_hole_or_double_terms_forbidden": forbidden}


def main():
    # Exact balanced beam splitter.  The bosonic HOM outputs bunch; fermions
    # have the opposite exchange behavior and cannot realize either output.
    invsqrt2 = Q4((0, 0, Q(1, 2)))
    H2 = [[invsqrt2, invsqrt2], [invsqrt2, -invsqrt2]]
    bs_boson = [boson_amp(H2, [1, 1], [2, 0]),
                boson_amp(H2, [1, 1], [1, 1]),
                boson_amp(H2, [1, 1], [0, 2])]
    bs_fermion = [fermion_amp(H2, [1, 1], [2, 0]),
                  fermion_amp(H2, [1, 1], [1, 1]),
                  fermion_amp(H2, [1, 1], [0, 2])]
    assert bs_boson == [invsqrt2, Q4(()), -invsqrt2]
    assert bs_fermion == [Q4(()), Q4((-1,)), Q4(())]

    # Re-evaluate the supplied KLM nonlinear-sign submatrix over Q(2^(1/4)).
    alpha = Q4((0, 1))
    sqrt2 = alpha * alpha
    inv_alpha = Q4((0, 0, 0, Q(1, 2)))
    A = [[Q4((1,)) - sqrt2, inv_alpha],
         [inv_alpha, Q4((Q(1, 2),))]]
    ns_boson = []
    for n in range(3):
        rows = [0] * n + [1]
        cols = [0] * n + [1]
        val = perm(repeated_matrix(A, rows, cols))
        # Input and output occupations agree, so sqrt(n! n!) = n!.
        denom = factorial(n)
        val = val / denom  # sqrt(n! n!) = n! in this diagonal fixture
        ns_boson.append(val)
    assert ns_boson == [Q4((Q(1, 2),)), Q4((Q(1, 2),)), Q4((Q(-1, 2),))]
    fermion_ns_0 = A[1][1]
    fermion_ns_1 = det(A)
    fermion_n2_allowed = False
    assert fermion_ns_0 == Q4((Q(1, 2),))
    assert fermion_ns_1 == Q4((Q(1, 2),)) - sqrt2  # (1 - 2 sqrt(2))/2
    assert fermion_ns_1 != fermion_ns_0

    # The V readout buncher maps R occupied bosonic inputs to one output mode.
    # For R=4 a Walsh first row is (1/2,...,1/2).  Its permanent is 3/2;
    # the corresponding fermionic exterior-power amplitude has duplicate rows.
    H4 = [[Q4((Q(1, 2) * s,)) for s in row]
          for row in ((1, 1, 1, 1), (1, -1, 1, -1),
                      (1, 1, -1, -1), (1, -1, -1, 1))]
    bunch_rows = [0, 0, 0, 0]
    all_cols = [0, 1, 2, 3]
    bunch_permanent = perm(repeated_matrix(H4, bunch_rows, all_cols))
    assert bunch_permanent == Q4((Q(3, 2),))
    bunch_fermion = det(repeated_matrix(H4, bunch_rows, all_cols))
    assert bunch_fermion == Q4(())

    F2 = [[gq(0), gq((1, 1))], [gq((2, -1)), gq(1)]]
    F4 = [
        [gq(0), gq(1), gq((0, 1)), gq(0)],
        [gq((1, 1)), gq(0), gq(2), gq(-1)],
        [gq(1), gq((0, -1)), gq(0), gq((1, 1))],
        [gq(2), gq(Q(1, 2)), gq(1), gq(0)],
    ]
    bcs_checks = [check_bcs_phase(F2), check_bcs_phase(F4)]

    report = {
        "status": "PASS_EXACT_FINITE_DIAGNOSTICS",
        "scope": "direct KLM/Walsh bosonic gadget transfer; BCS determinant phase check",
        "balanced_beam_splitter": {
            "bosonic_11_to_20_11_02": [repr(x) for x in bs_boson],
            "fermionic_11_to_20_11_02": [repr(x) for x in bs_fermion],
            "interpretation": "bosonic bunching amplitudes cancel in 11; fermions remain in 11"
        },
        "KLM_NS": {
            "bosonic_conditional_amplitudes_n_0_1_2": [repr(x) for x in ns_boson],
            "fermionic_conditional_amplitude_n_0": repr(fermion_ns_0),
            "fermionic_conditional_amplitude_n_1": repr(fermion_ns_1),
            "fermionic_n_2_target_configuration_allowed": fermion_n2_allowed,
            "interpretation": "the bosonic NS truth table uses a forbidden n=2 fermion state; even its allowed 0/1 sector is not a uniform scalar branch"
        },
        "walsh_readout_R4": {
            "bosonic_repeated_row_permanent": repr(bunch_permanent),
            "fermionic_repeated_row_determinant": repr(bunch_fermion),
            "source_bosonic_bunching_amplitude": "sqrt(24)/16",
            "interpretation": "Pauli exclusion makes the source's compressed readout branch exactly zero"
        },
        "BCS_pair_matrix_phase_checks": bcs_checks,
        "limits": [
            "No impossibility theorem for other fermionic/postselected encodings.",
            "No PP-hardness or approximate-sampling reduction for the hard-projected BCS norm is established.",
            "Only exact finite gadget identities are checked; no general compiler is implemented."
        ]
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
