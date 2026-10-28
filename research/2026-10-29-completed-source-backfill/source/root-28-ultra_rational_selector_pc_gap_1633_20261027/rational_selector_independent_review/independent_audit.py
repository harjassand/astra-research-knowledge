#!/usr/bin/env python3
"""Independent stdlib audit: read rational data, import no author code or maps.

The only serialization convention read from author source is the feature order:
lexicographic combinations-with-replacement of A indices, then X indices.
All mathematical polynomials, residuals, atoms and sensitivities are rebuilt here.
"""
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement as cwr
from math import comb, lcm
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
POS = BASE / "rational_selector/EXACT_RATIONAL_SUPPORT.json"
ATM = BASE / "quartic_boundary_alternative/EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json"
TARGET = BASE / "common_cone_review/EXACT_SYMMETRIC_TARGET.json"
ORIGINAL = BASE / "quartic_alternative/combined_full_cone/EXACT_COMMON_SEPARATOR.json"
ZERO = (0,) * 8


def clean(p):
    return {e: v for e, v in p.items() if v}


def add(*polys):
    ans = defaultdict(Q)
    for p in polys:
        for e, v in p.items():
            ans[e] += v
    return clean(ans)


def scale(p, s):
    return clean({e: s * v for e, v in p.items()})


def times(p, q):
    ans = defaultdict(Q)
    for e, v in p.items():
        for f, w in q.items():
            ans[tuple(ei + fi for ei, fi in zip(e, f))] += v * w
    return clean(ans)


def power(p, n):
    ans = {ZERO: Q(1)}
    for _ in range(n):
        ans = times(ans, p)
    return ans


def variable(i):
    e = list(ZERO)
    e[i] = 1
    return {tuple(e): Q(1)}


def derivative(p, i):
    ans = {}
    for e, v in p.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            ans[tuple(f)] = v * e[i]
    return clean(ans)


V = [variable(i) for i in range(8)]


def substitute_a_plus_x(p):
    ans = {}
    for e, v in p.items():
        assert not any(e[4:])
        term = {ZERO: v}
        for i in range(4):
            term = times(term, power(add(V[i], V[i + 4]), e[i]))
        ans = add(ans, term)
    return ans


def bregman(p):
    linear = add(*(times(derivative(p, i), V[i + 4]) for i in range(4)))
    return add(substitute_a_plus_x(p), scale(p, -1), scale(linear, -1))


def evaluate(p, point):
    ans = Q(0)
    for e, v in p.items():
        term = v
        for t, n in zip(point, e):
            term *= t ** n
        ans += term
    return ans


def exponent_from_indices(a_indices, x_indices):
    ans = [0] * 8
    for i in a_indices:
        ans[i] += 1
    for i in x_indices:
        ans[i + 4] += 1
    return tuple(ans)


def quartic_exponents():
    return [exponent_from_indices(ii, ()) for ii in cwr(range(4), 4)]


def matrix_is_integer_square(m, n):
    return len(m) == n and all(
        len(row) == n and all(type(v) is int for v in row) for row in m
    )


def main():
    start = time.monotonic()
    positive_bytes, atomic_bytes, target_bytes = POS.read_bytes(), ATM.read_bytes(), TARGET.read_bytes()
    original_bytes = ORIGINAL.read_bytes()
    hashes = {
        "positive": sha256(positive_bytes).hexdigest(),
        "atomic": sha256(atomic_bytes).hexdigest(),
        "target": sha256(target_bytes).hexdigest(),
        "original_unsymmetrized_source": sha256(original_bytes).hexdigest(),
    }
    assert hashes["positive"] == "ecbd2bd7d333abe79810625c7be6e1d218d4411095cc28c049fa731958059191"
    assert hashes["atomic"] == "e51d9be90ba977c34f5daab4a75901eb6acc377dc53c0004d479425fed945d22"
    assert hashes["target"] == "88769c8c3ff995312e7a34967c43959e4e46715b59d3ad781cbba545194ab4f3"
    data, atomic = json.loads(positive_bytes), json.loads(atomic_bytes)
    assert data["target_source_sha256"] == atomic["source_sha256"] == hashes["target"]

    # Literal row-major matrix invariants, with no imported interface arrays.
    a, b, c, d = V[:4]
    u = add(times(a, a), times(c, c))
    v = add(times(b, b), times(d, d))
    w = add(times(a, b), times(c, d))
    q = add(times(a, d), scale(times(b, c), -1))
    t = add(u, v)
    x, y, z = add(u, scale(v, -1)), scale(w, 2), scale(q, 2)
    assert power(t, 2) == add(power(x, 2), power(y, 2), power(z, 2))
    basis = [power(u, 2), power(v, 2), times(u, v), power(w, 2), times(u, w), times(v, w), times(q, u), times(q, v), times(q, w)]
    literal_coefficients = [Q(s) for s in [
        "55220381/10000000000", "55220381/10000000000", "114430029/625000000",
        "-801761987/5000000000", "0", "0", "118849817/4000000000",
        "-118849817/4000000000", "0",
    ]]
    assert literal_coefficients == list(map(Q, data["target_coefficients"])) == list(map(Q, atomic["coefficients"]))
    f = add(*(scale(p, s) for p, s in zip(basis, literal_coefficients)))
    assert all(sum(e[:4]) == 4 and not any(e[4:]) for e in f)
    bf = bregman(f)
    det_x = add(times(V[4], V[7]), scale(times(V[5], V[6]), -1))
    numerator_basis = [power(x, 3), times(power(x, 2), z), times(x, power(z, 2)), power(z, 3), times(x, power(y, 2)), times(power(y, 2), z)]
    assert data["selector_Hopf_basis"] == ["x3", "x2z", "xz2", "z3", "xy2", "y2z"]
    selector_coefficients = list(map(Q, data["selector_coefficients"]))
    assert selector_coefficients == list(map(Q, [
        "6222019/200000000", "1686519911/10000000000", "81172813/2000000000",
        "1726116771/10000000000", "128626163/5000000000", "373321239/2000000000",
    ]))
    p6 = add(*(scale(p, s) for p, s in zip(numerator_basis, selector_coefficients)))
    assert all(sum(e[:4]) == 6 and not any(e[4:]) for e in p6)
    literal = add(times(power(t, 2), bf), scale(times(p6, det_x), -1))
    assert len(literal) == 998 == data["positive_polynomial_nonzero_coefficients"]

    # Explicit feature order is independent of any saved monomial map.
    features = [exponent_from_indices(ii, (j,)) for ii in cwr(range(4), 3) for j in range(4)]
    features += [exponent_from_indices(ii, jj) for ii in cwr(range(4), 2) for jj in cwr(range(4), 2)]
    assert len(features) == len(set(features)) == 180
    k = data["gram_integer_matrix"]
    gram_den = data["gram_denominator"]
    assert gram_den == 80000000000 and matrix_is_integer_square(k, 180)
    gram_poly = defaultdict(int)
    span = set()
    for i, ei in enumerate(features):
        for j in range(i, 180):
            assert k[i][j] == k[j][i]
            e = tuple(a + b for a, b in zip(ei, features[j]))
            span.add(e)
            gram_poly[e] += (1 if i == j else 2) * k[i][j]
    gram_poly = clean(gram_poly)
    expected_integer = {e: v * gram_den for e, v in literal.items()}
    assert all(v.denominator == 1 for v in expected_integer.values())
    assert gram_poly == expected_integer
    assert len(span) == 3185 == data["full_Gram_monomial_span"]
    bidegrees = defaultdict(int)
    for e in span:
        bidegrees[(sum(e[:4]), sum(e[4:]))] += 1
    assert dict(bidegrees) == {(6, 2): 840, (5, 3): 1120, (4, 4): 1225}
    identity_seconds = time.monotonic() - start

    # Exact dyadic residual. No numerical eigenvalues or factor origin trusted.
    factor = data["dyadic_lower_integer_matrix"]
    fden = data["dyadic_factor_denominator"]
    shift, margin = Q(data["factor_reference_shift"]), Q(data["gram_proved_lower_bound"])
    assert matrix_is_integer_square(factor, 180) and fden == 2 ** 44
    assert shift == Q(1, 200000) and margin == Q(1, 400000)
    common_den = lcm(gram_den, fden * fden, shift.denominator)
    kmul, lmul = common_den // gram_den, common_den // (fden * fden)
    diagonal_shift = shift * common_den
    assert diagonal_shift.denominator == 1
    row_sums = [0] * 180
    residual_largest_entry = 0
    for i in range(180):
        for j in range(i, 180):
            dot = sum(a * b for a, b in zip(factor[i], factor[j]))
            residual = k[i][j] * kmul - dot * lmul
            if i == j:
                residual -= diagonal_shift.numerator
            size = abs(residual)
            residual_largest_entry = max(residual_largest_entry, size)
            row_sums[i] += size
            if i != j:
                row_sums[j] += size
    residual_bound = Q(max(row_sums), common_den)
    assert residual_bound == Q(data["exact_residual_operator_norm_upper_bound"])
    assert residual_bound < shift - margin
    positivity_seconds = time.monotonic() - start - identity_seconds

    # Actual rational atoms, evaluated without the three-cut derivation or symmetry.
    atoms = []
    for item in atomic["atoms"]:
        aa, xx, weight = tuple(map(Q, item["A"])), tuple(map(Q, item["X"])), Q(item["weight"])
        assert len(aa) == len(xx) == 4 and weight > 0
        atoms.append((aa, xx, weight))
    assert len(atoms) == 24 == atomic["atomic_count"]
    annihilators = {}
    for i, j in cwr(range(4), 2):
        value = sum(weight * aa[i] * aa[j] * (xx[0] * xx[3] - xx[1] * xx[2]) for aa, xx, weight in atoms)
        assert value == 0
        annihilators[f"{i},{j}"] = str(value)
    pairing = sum(weight * evaluate(bf, aa + xx) for aa, xx, weight in atoms)
    assert pairing == Q(atomic["negative_Bregman_pairing"]) and pairing < -Q(1, 100000)
    # Check the literal Bregman evaluation against independent direct F evaluations.
    gradient = [derivative(f, i) for i in range(4)]
    for aa, xx, _ in atoms:
        direct = evaluate(f, tuple(a + x for a, x in zip(aa, xx)) + (Q(0),) * 4)
        direct -= evaluate(f, aa + (Q(0),) * 4)
        direct -= sum(evaluate(gradient[i], aa + (Q(0),) * 4) * xx[i] for i in range(4))
        assert direct == evaluate(bf, aa + xx)
    atomic_seconds = time.monotonic() - start - identity_seconds - positivity_seconds

    # Full35 sensitivities, preserving a fixed rational numerator.
    epsilon = Q(data["full35_coefficient_sup_radius"])
    assert epsilon == Q(1, 4928000000)
    monomial_sensitivities = []
    total_atomic_sensitivity = Q(0)
    gram_sensitivity = 0
    for e in quartic_exponents():
        bm = bregman({e: Q(1)})
        multiplied = times(power(t, 2), bm)
        assert sum(abs(v) for v in bm.values()) == 11
        assert sum(abs(v) for v in multiplied.values()) == 176
        assert set(multiplied).issubset(span)
        gram_sensitivity += 176
        atom_value = sum(weight * evaluate(bm, aa + xx) for aa, xx, weight in atoms)
        total_atomic_sensitivity += abs(atom_value)
        monomial_sensitivities.append({"exponent_A": list(e[:4]), "atomic_pairing": str(atom_value), "multiplied_coefficient_l1": 176})
    assert len(monomial_sensitivities) == 35
    assert gram_sensitivity == 6160 == data["full35_perturbation_Gram_l1_bound"]
    perturbed_margin = margin - epsilon * gram_sensitivity
    assert perturbed_margin == Q(1, 800000) == Q(data["perturbed_Gram_lower_bound"])
    perturbed_pairing_upper = pairing + epsilon * total_atomic_sensitivity
    assert perturbed_pairing_upper < 0
    larger_atomic_radius = Q(1, 336000000)
    assert pairing + larger_atomic_radius * total_atomic_sensitivity < 0

    # Explicit original-target correction: q|A|^2 / 2e10, in ordinary monomials.
    correction = scale(times(q, t), Q(1, 20000000000))
    assert len(correction) == 8
    assert {abs(v) for v in correction.values()} == {Q(1, 20000000000)}
    assert max(abs(v) for v in correction.values()) < epsilon
    old_coefficients = literal_coefficients.copy()
    old_coefficients[6] += Q(1, 20000000000)
    old_coefficients[7] += Q(1, 20000000000)
    assert old_coefficients == list(map(Q, json.loads(original_bytes)["target_coefficients"]))
    old_f = add(*(scale(p, s) for p, s in zip(basis, old_coefficients)))
    assert add(old_f, scale(f, -1)) == correction

    # Numerical shape checks here are purely integer combinatorics, not positivity.
    assert len(list(cwr(range(4), 3))) == 20
    assert len(list(cwr(range(4), 2))) == 10
    # Exact norm lower bounds use multinomial coefficients <= 6 or <= 2.
    for degree, largest in [(3, 6), (2, 2)]:
        for ii in cwr(range(4), degree):
            counts = [ii.count(j) for j in range(4)]
            value, remaining = 1, degree
            for count in counts:
                value *= comb(remaining, count)
                remaining -= count
            assert 1 <= value <= largest

    receipt = {
        "status": "INDEPENDENT_EXACT_ALGEBRA_PASSED_ANALYTIC_REVIEW_RECORDED_SEPARATELY",
        "utc": datetime.now(timezone.utc).isoformat(),
        "certificate_sha256": hashes,
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_scope": "Python standard library only; no producer/verifier imports, saved maps, solver, or floating arithmetic",
        "literal_polynomial": {"nonzero_coefficients": len(literal), "gram_features": len(features), "span": len(span), "bidegree_counts": {str(k): v for k, v in bidegrees.items()}},
        "exact_positivity": {
            "residual_row_sum": str(residual_bound),
            "largest_residual_entry": str(Q(residual_largest_entry, common_den)),
            "proved_margin": str(margin),
            "actual_certified_lower": str(shift - residual_bound),
            "all_factor_entries_consumed": 180 ** 2,
            "row_sum_bound_uses_symmetry": True,
        },
        "atomic": {"actual_atom_count": len(atoms), "positive_weights": True, "annihilators": annihilators, "pairing": str(pairing)},
        "full35": {
            "coefficient_sup_radius": str(epsilon), "gram_entry_l1_sensitivity": gram_sensitivity,
            "perturbed_gram_lower": str(perturbed_margin),
            "atomic_l1_sensitivity": str(total_atomic_sensitivity),
            "perturbed_atomic_pairing_upper": str(perturbed_pairing_upper),
            "larger_atomic_radius_confirmed": str(larger_atomic_radius),
            "monomials": monomial_sensitivities,
        },
        "original_unsymmetrized_target": {
            "nine_coefficients": list(map(str, old_coefficients)),
            "delta_formula": "q*|A|^2/20000000000",
            "ordinary_nonzero_monomials": len(correction), "max_abs_ordinary_coefficient": "1/20000000000",
            "within_full35_radius": True,
        },
        "seconds": {"literal_identity": identity_seconds, "exact_residual": positivity_seconds, "atomic": atomic_seconds, "total": time.monotonic() - start},
    }
    output = HERE / "INDEPENDENT_EXACT_REPLAY.json"
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "seconds": receipt["seconds"], "receipt": str(output), "residual_row_sum": str(residual_bound), "atomic_pairing": str(pairing), "perturbed_gram_lower": str(perturbed_margin)}, indent=2))


if __name__ == "__main__":
    main()
