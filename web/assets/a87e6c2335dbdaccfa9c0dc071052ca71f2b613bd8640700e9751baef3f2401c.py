"""Acquired exact third-order coefficient and l1-Pauli norm certificate.

No 2**qubits matrix is constructed. Polynomial fixed-order dictionary algebra
is charged; admission caps are explicit. This refines the independent quadratic
gate error certificate and does not acquire any counting probabilities.
"""
from fractions import Fraction as F
from xxz_quadratic_gates import quadratic_plan, ceil_sqrt_fraction


ZERO, ONE = (F(0), F(0)), (F(1), F(0))


def cadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def cmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def pscale(a, s):
    return {key: (value[0] * s, value[1] * s) for key, value in a.items()
            if value != ZERO and s != 0}


def padd(a, b):
    result = dict(a)
    for key, value in b.items():
        result[key] = cadd(result.get(key, ZERO), value)
        if result[key] == ZERO:
            del result[key]
    return result


def pmul(a, b, *, key_cap=4096):
    result = {}
    for (x, z), ca in a.items():
        for (xx, zz), cb in b.items():
            new_x, new_z = x ^ xx, z ^ zz
            phase = ((x & z).bit_count() + (xx & zz).bit_count() -
                     (new_x & new_z).bit_count() + 2 * (z & xx).bit_count()) % 4
            rotation = [ONE, (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))][phase]
            key = (new_x, new_z)
            result[key] = cadd(result.get(key, ZERO), cmul(cmul(ca, cb), rotation))
            if result[key] == ZERO:
                del result[key]
            if len(result) > key_cap:
                raise ValueError("Pauli dictionary admission cap exceeded")
    return result


def local_paulis(edges, fields):
    terms = []
    for u, v, alpha, gamma in edges:
        alpha, gamma = F(alpha), F(gamma)
        bits = (1 << u) | (1 << v)
        term = {(0, 0): (3 * alpha, F(0)), (bits, 0): (alpha, F(0)),
                (bits, bits): (alpha, F(0)), (0, bits): (gamma, F(0))}
        terms.append({key: value for key, value in term.items() if value != ZERO})
    for v, b, c in fields:
        b, c = F(b), F(c)
        bit = 1 << v
        term = {(0, 0): (b + abs(c), F(0)), (bit, 0): (b, F(0)), (0, bit): (c, F(0))}
        terms.append({key: value for key, value in term.items() if value != ZERO})
    return terms


def third_defect(edges, fields, *, term_cap=12, key_cap=4096):
    terms = local_paulis(edges, fields)
    if len(terms) > term_cap:
        raise ValueError("local term admission cap exceeded")
    identity = {(0, 0): ONE}
    coefficients = [identity, {}, {}, {}]
    for A in terms + list(reversed(terms)):
        local = [identity, A, pscale(pmul(A, A, key_cap=key_cap), F(1, 2))]
        new = [{}, {}, {}, {}]
        for degree in range(4):
            for j in range(min(2, degree) + 1):
                new[degree] = padd(new[degree], pmul(coefficients[degree - j], local[j], key_cap=key_cap))
        coefficients = new
    S = coefficients[1]
    square = pmul(S, S, key_cap=key_cap)
    assert coefficients[2] == pscale(square, F(1, 2))
    defect = padd(coefficients[3], pscale(pmul(square, S, key_cap=key_cap), F(-1, 6)))
    assert all(imag == 0 for _, imag in defect.values())
    bound = sum((abs(real) for real, _ in defect.values()), F(0))
    return defect, bound


def ceil_root_fraction(value, degree):
    value = F(value)
    if value < 0 or degree < 1:
        raise ValueError("invalid root")
    upper = (value.numerator + value.denominator - 1) // value.denominator
    lo, hi = 0, max(1, upper)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** degree >= value:
            hi = mid
        else:
            lo = mid + 1
    return lo


def third_certificate_plan(qubits, edges, fields, beta, error, *, term_cap=12, key_cap=4096):
    original = quadratic_plan(qubits, edges, fields, beta, error)
    beta, error, tau = F(beta), F(error), original["tau"]
    defect, L3 = third_defect(edges, fields, term_cap=term_cap, key_cap=key_cap)
    m = max(1, (4 * tau.numerator + tau.denominator - 1) // tau.denominator,
            ceil_sqrt_fraction(beta ** 3 * L3 / error),
            ceil_root_fraction(8 * tau ** 4 / (9 * error), 3))
    refined_bound = beta ** 3 * L3 / (8 * m * m) + tau ** 4 / (9 * m ** 3)
    assert refined_bound <= error / 4
    if m < original["m"]:
        original.update({"m": m, "s": beta / (2 * m), "gates": 2 * m * original["local_terms"],
                         "ground_size": 8 * m * original["local_terms"],
                         "log_generator_error_bound": refined_bound})
    original.update({"acquired_third_pauli_l1_bound": L3,
                     "nonzero_third_paulis": len(defect), "refined_candidate_m": m,
                     "refined_candidate_log_error": refined_bound,
                     "third_coefficient": [{"x": key[0], "z": key[1], "real": value[0]}
                                           for key, value in sorted(defect.items())]})
    return original
