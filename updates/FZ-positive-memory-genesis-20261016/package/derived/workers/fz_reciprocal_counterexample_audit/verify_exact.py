#!/usr/bin/env python3
"""Independent exact audit of the supplied reciprocal-moment candidate.

Only the candidate's rational table supplies moment data. Proposed network
structure is separately reconstructed and checked. This
program never imports or executes the producer's constructor, never reads its
search output, and never uses its claimed positivity pivots.  It enumerates the
original polynomial spaces first and uses integer Bareiss determinants and
Sylvester's criterion, rather than the producer's LDL decomposition.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import lcm
from pathlib import Path
import json
import sys

F = Fraction
HERE = Path(__file__).resolve().parent
RUN = HERE.parents[1]
CANDIDATE = HERE / "frozen_inputs" / "EXACT_COUNTEREXAMPLE.json"
CONSTRUCTOR = CANDIDATE.with_name("verify_counterexample.py")
PASSIVE = CANDIDATE.with_name("PASSIVE_EMBEDDING.json")
REPORT = CANDIDATE.with_name("reciprocal_report.txt")
OUTPUT = HERE
HISTORICAL = "--historical" in sys.argv
if HISTORICAL:
    CANDIDATE = HERE / "earlier_read_snapshot.json"
    OUTPUT = HERE / "earlier_audit"
OUTPUT.mkdir(exist_ok=True)


def monomials(n, degree):
    """All exponent tuples, in graded lexicographic order."""
    return sorted((a for a in product(range(degree + 1), repeat=n)
                   if sum(a) <= degree), key=lambda a: (sum(a), a))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def rational_matrix(A):
    return [[str(v) for v in row] for row in A]


def integer_determinant(A):
    """Fraction-free Bareiss elimination, with exact integer divisions."""
    n = len(A)
    if n == 0:
        return 1
    B = [list(row) for row in A]
    sign = 1
    previous = 1
    for k in range(n - 1):
        if B[k][k] == 0:
            replacement = next((j for j in range(k + 1, n)
                                if B[j][k] != 0), None)
            if replacement is None:
                return 0
            B[k], B[replacement] = B[replacement], B[k]
            sign = -sign
        pivot = B[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = B[i][j] * pivot - B[i][k] * B[k][j]
                assert numerator % previous == 0, "Nonexact Bareiss division"
                B[i][j] = numerator // previous
        for i in range(k + 1, n):
            B[i][k] = 0
        previous = pivot
    return sign * B[-1][-1]


def sylvester(A):
    """Prove PD by every exact leading principal determinant being positive."""
    assert all(A[i][j] == A[j][i] for i in range(len(A))
               for j in range(len(A)))
    scale = lcm(*(v.denominator for row in A for v in row))
    integers = [[int(v * scale) for v in row] for row in A]
    determinants = []
    numerators = []
    for size in range(1, len(A) + 1):
        determinant = integer_determinant([row[:size] for row in integers[:size]])
        assert determinant > 0, ("Nonpositive principal determinant", size, determinant)
        numerators.append(str(determinant))
        determinants.append(F(determinant, scale ** size))
    return {
        "criterion": "Sylvester: all leading principal determinants strictly positive",
        "dimension": len(A),
        "integer_matrix_scale": str(scale),
        "integer_leading_principal_determinants": numerators,
        "rational_leading_principal_determinants": list(map(str, determinants)),
        "all_strictly_positive": True,
    }


def write_json(name, value):
    (OUTPUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    if not HISTORICAL:
        expected_hashes = {
            CANDIDATE: "ebc0dc8ebb72608e2ba883e3f8344adf4801c428a2f19638e34645a36ccdaa88",
            CONSTRUCTOR: "31546d7b6f789f3fb33415959dc8d45f355c6887a3d43e8e0c3cb04f1d21aff1",
            PASSIVE: "ce3b91f725bd7389903a9849a7f4325884122a554c5e5567563bbcb66c0290bd",
            REPORT: "278350fa610f1c51d511b4eab77a79f461d00ce86b946ecfb058783a2b15f075",
        }
        assert all(digest(path) == expected for path, expected in expected_hashes.items())
    supplied = json.loads(CANDIDATE.read_text())
    # These hypotheses are checked explicitly, rather than inherited from a status.
    assert supplied["voltage_vector"] == ["x", "y", "u", "v"]
    assert supplied["B_i"] == [0, 0, 1, 0]
    assert supplied["B_j"] == [0, 0, 0, 1]
    expected_bounds = [(F(1), F(4)), (F(1), F(4)),
                       (F(1, 64), F(64)), (F(1, 64), F(64))]
    assert [[F(v) for v in supplied["bounds"][name]]
            for name in ("x", "y", "u", "v")] == list(map(list, expected_bounds))
    assert supplied["direction"] == {"alpha": 1, "beta": -1}

    sparse = {}
    for entry in supplied["moments"]:
        key = (entry["k"], entry["l"])
        assert key not in sparse
        assert key[0] <= key[1]
        sparse[key] = F(entry["value"])

    # Quotient relation follows from the fixed-power equations: x*u=y*v=1.
    def label(a):
        assert len(a) == 4 and sum(a) <= 4 and min(a) >= 0
        return (a[0] - a[2], a[1] - a[3])

    def value(a):
        k, ell = label(a)
        return sparse[min(k, ell), max(k, ell)]

    full_degree4 = monomials(4, 4)
    degree2 = monomials(4, 2)
    degree1 = monomials(4, 1)
    assert len(full_degree4) == 70 and len(degree2) == 15 and len(degree1) == 5
    full_moments = {a: value(a) for a in full_degree4}
    assert full_moments[(0, 0, 0, 0)] == 1
    assert all(v == 0 for a, v in full_moments.items() if sum(a) % 2)
    assert all(value((a[1], a[0], a[3], a[2])) == v
               for a, v in full_moments.items())

    def matrix(basis, polynomial):
        return [[sum(c * value(add(add(a, b), t))
                     for t, c in polynomial.items()) for b in basis] for a in basis]

    unit = {(0, 0, 0, 0): F(1)}
    M = matrix(degree2, unit)

    # Independently derive a quotient basis from the full original basis.  Put
    # even polynomials first, so the vanishing odd moments produce two blocks.
    representative = {}
    for a in degree2:
        representative.setdefault(label(a), a)
    quotient_basis = sorted(representative.values(),
                            key=lambda a: (sum(a) % 2, sum(a), a))
    quotient_labels = [label(a) for a in quotient_basis]
    assert len(quotient_basis) == 13
    qindex = {key: i for i, key in enumerate(quotient_labels)}
    full_to_quotient = [qindex[label(a)] for a in degree2]
    Q = matrix(quotient_basis, unit)
    assert all(M[i][j] == Q[full_to_quotient[i]][full_to_quotient[j]]
               for i in range(15) for j in range(15))
    # M = C^T Q C, for the 13-by-15 one-hot matrix C below.
    C = [[int(full_to_quotient[j] == i) for j in range(15)] for i in range(13)]
    assert all(sum(C[k][i] * Q[k][ell] * C[ell][j]
                   for k in range(13) for ell in range(13)) == M[i][j]
               for i in range(15) for j in range(15))
    even = [i for i, a in enumerate(quotient_basis) if sum(a) % 2 == 0]
    odd = [i for i, a in enumerate(quotient_basis) if sum(a) % 2 == 1]
    assert len(even) == 9 and len(odd) == 4
    assert all(Q[i][j] == 0 for i in even for j in odd)
    positivity = {
        "quotient_moment_even_block": sylvester([[Q[i][j] for j in even] for i in even]),
        "quotient_moment_odd_block": sylvester([[Q[i][j] for j in odd] for i in odd]),
    }

    equality_checks = []
    for name, shift in [("x*u-1", (1, 0, 1, 0)), ("y*v-1", (0, 1, 0, 1))]:
        for multiplier in degree2:
            residual = value(add(multiplier, shift)) - value(multiplier)
            assert residual == 0
            equality_checks.append({"equality": name, "multiplier_exponents": multiplier,
                                    "residual": str(residual)})
    assert len(equality_checks) == 30

    localizers = {}
    real_bounds_polynomials = {}
    for coordinate, name in enumerate(("x", "y", "u", "v")):
        square = tuple(2 if j == coordinate else 0 for j in range(4))
        lower, upper = expected_bounds[coordinate]
        for side, coefficients in [("lower", {square: F(1), (0, 0, 0, 0): -lower}),
                                   ("upper", {square: F(-1), (0, 0, 0, 0): upper})]:
            key = name + "_" + side
            A = matrix(degree1, coefficients)
            real_bounds_polynomials[key] = coefficients
            positivity[key] = sylvester(A)
            localizers[key] = {"polynomial_terms": [
                {"exponents": a, "coefficient": str(c)} for a, c in coefficients.items()],
                "matrix": rational_matrix(A), "positive_definite": True, "rank": 5}

    # Rebuild the full eight-real-coordinate complex embedding, including all
    # 495 monomials through degree four, not merely its real principal submatrix.
    complex_degree4 = monomials(8, 4)
    complex_degree2 = monomials(8, 2)
    complex_degree1 = monomials(8, 1)
    assert len(complex_degree4) == 495
    assert len(complex_degree2) == 45 and len(complex_degree1) == 9

    def complex_value(a):
        assert sum(a) <= 4
        if any(a[j] for j in (1, 3, 5, 7)):
            return F(0)
        return value((a[0], a[2], a[4], a[6]))

    def complex_matrix(basis, polynomial):
        return [[sum(c * complex_value(add(add(a, b), t))
                     for t, c in polynomial.items()) for b in basis] for a in basis]

    complex_zero = (0,) * 8
    complex_M = complex_matrix(complex_degree2, {complex_zero: F(1)})
    real_d2_index = {a: i for i, a in enumerate(degree2)}
    complex_to_real = [None if any(a[j] for j in (1, 3, 5, 7))
                       else real_d2_index[(a[0], a[2], a[4], a[6])]
                       for a in complex_degree2]
    for i, ir in enumerate(complex_to_real):
        for j, jr in enumerate(complex_to_real):
            assert complex_M[i][j] == (F(0) if ir is None or jr is None else M[ir][jr])

    complex_equalities = []
    for name, first, second in [("h_i", 0, 4), ("h_j", 2, 6)]:
        rr = [0] * 8
        ii = [0] * 8
        ri = [0] * 8
        ir = [0] * 8
        rr[first] = rr[second] = 1
        ii[first + 1] = ii[second + 1] = 1
        ri[first] = ri[second + 1] = 1
        ir[first + 1] = ir[second] = 1
        # Re(conj(x)*u-1)=xr*ur+xi*ui-1; Im=xr*ui-xi*ur.
        for part, polynomial in [("real", {tuple(rr): F(1), tuple(ii): F(1), complex_zero: F(-1)}),
                                 ("imaginary", {tuple(ri): F(1), tuple(ir): F(-1)})]:
            for multiplier in complex_degree2:
                residual = sum(c * complex_value(add(multiplier, t))
                               for t, c in polynomial.items())
                assert residual == 0
                complex_equalities.append({"equality": name + "_" + part,
                                           "multiplier_exponents": multiplier,
                                           "residual": str(residual)})
    assert len(complex_equalities) == 180

    complex_localizers = {}
    complex_bounds_polynomials = {}
    real_d1_index = {a: i for i, a in enumerate(degree1)}
    complex_linear_to_real = [None if any(a[j] for j in (1, 3, 5, 7))
                              else real_d1_index[(a[0], a[2], a[4], a[6])]
                              for a in complex_degree1]
    for coordinate, name in enumerate(("x", "y", "u", "v")):
        real_square = tuple(2 if j == 2 * coordinate else 0 for j in range(8))
        imag_square = tuple(2 if j == 2 * coordinate + 1 else 0 for j in range(8))
        lower, upper = expected_bounds[coordinate]
        for side, coefficients in [("lower", {real_square: F(1), imag_square: F(1), complex_zero: -lower}),
                                   ("upper", {real_square: F(-1), imag_square: F(-1), complex_zero: upper})]:
            key = name + "_" + side
            A = complex_matrix(complex_degree1, coefficients)
            complex_bounds_polynomials[key] = coefficients
            real_A = [[F(v) for v in row] for row in localizers[key]["matrix"]]
            for i, ir in enumerate(complex_linear_to_real):
                for j, jr in enumerate(complex_linear_to_real):
                    assert A[i][j] == (F(0) if ir is None or jr is None else real_A[ir][jr])
            complex_localizers[key] = {"matrix": rational_matrix(A), "rank": 5,
                                       "positive_semidefinite_by_real_embedding": True}

    bound_products = check_bound_products(real_bounds_polynomials, value)
    complex_bound_products = check_bound_products(complex_bounds_polynomials, complex_value)
    assert bound_products == complex_bound_products

    cut_terms = {(2, 0, 0, 0): F(1), (0, 2, 0, 0): F(1),
                 (1, 1, 0, 0): F(-2), (0, 0, 2, 0): F(-1),
                 (0, 0, 0, 2): F(-1), (0, 0, 1, 1): F(2)}
    cut = sum(c * value(a) for a, c in cut_terms.items())
    assert cut == (F(-59330890897, 661500000000) if HISTORICAL else F(-897, 10000))
    assert cut == F(supplied["lower_cut_value"]) and cut < 0
    strengthened_current_diagonal = value((0, 0, 2, 0)) - value((0, 0, 4, 0))
    assert strengthened_current_diagonal < 0
    assert value((0, 0, 2, 0)) < 1 and value((0, 0, 0, 2)) < 1

    passive_result = None
    if not HISTORICAL:
        passive_result = audit_passive_embedding(value, degree2, degree1,
                                                 M, complex_degree2, complex_degree1,
                                                 complex_degree4)
        write_json("PASSIVE_EMBEDDING_AUDIT.json", passive_result)

    rebuilt = {
        "schema": "astra.independent-reciprocal-moment-functional.v1",
        "coordinate_order": ["x", "y", "u", "v"],
        "definition": "L(x^a y^b u^c v^d)=m[a-c,b-d], with m[k,l]=m[l,k]",
        "full_degree4_moments": [{"exponents": a, "value": str(full_moments[a])}
                                 for a in full_degree4],
        "moment_matrix": {"basis_exponents": degree2, "matrix": rational_matrix(M),
                          "dimension": 15, "rank": 13, "positive_semidefinite": True},
        "quotient": {"basis_exponents": quotient_basis, "labels": quotient_labels,
                     "matrix": rational_matrix(Q), "rank": 13,
                     "congruence_C": C, "identity": "M=C^T Q C",
                     "even_indices": even, "odd_indices": odd},
        "localizer_basis_exponents": degree1,
        "bound_localizers": localizers,
        "real_equality_checks": equality_checks,
        "all_scalar_degree4_voltage_bound_products": bound_products,
        "positivity_certificates": positivity,
        "complex_embedding": {
            "coordinate_order": ["x_real", "x_imag", "y_real", "y_imag",
                                 "u_real", "u_imag", "v_real", "v_imag"],
            "definition": "Every moment containing any imaginary coordinate is zero",
            "full_degree4_moments": [{"exponents": a, "value": str(complex_value(a))}
                                     for a in complex_degree4],
            "moment_matrix": {"basis_exponents": complex_degree2,
                              "matrix": rational_matrix(complex_M), "dimension": 45,
                              "rank": 13, "positive_semidefinite": True},
            "degree2_projection_to_real_basis": complex_to_real,
            "localizer_basis_exponents": complex_degree1,
            "degree1_projection_to_real_basis": complex_linear_to_real,
            "bound_localizers": complex_localizers,
            "all_equality_multiplier_checks": complex_equalities,
        },
    }
    write_json("REBUILT_MOMENT_FUNCTIONAL.json", rebuilt)
    result = {
        "schema": "astra.independent-order2-reciprocal-counterexample-audit.v1",
        "audit_status": "PASS_EXACT_ALGEBRAIC_COUNTEREXAMPLE",
        "normalization": "1",
        "all_70_real_moments_rebuilt": True,
        "real_M2": {"dimension": 15, "rank": 13, "PSD": True,
                    "method": "Exact congruence to PD 9x9 and 4x4 parity blocks"},
        "original_voltage_bound_localizers": {"number": 8, "dimension": 5,
                                              "all_PD": True},
        "scalar_degree4_original_voltage_bound_products": {"number": 36, "all_nonnegative": True,
                                                          "complex_embedding_same_exact_values": True},
        "real_equalities": {"number_of_quadratic_equalities": 2,
                            "all_degree_at_most_2_monomial_multipliers_checked": True,
                            "number_of_checks": 30, "all_zero": True},
        "complex_embedding": {"all_495_moments_rebuilt": True,
                              "M2_dimension": 45, "M2_rank": 13, "M2_PSD": True,
                              "localizer_number": 8, "localizer_dimension": 9,
                              "localizer_rank": 5, "all_localizers_PSD": True,
                              "equality_multiplier_checks": 180, "all_zero": True},
        "lower_cut_value": str(cut),
        "lower_cut_decimal_for_display_only": float(cut),
        "violating_polynomial": "(y-x)^2-(u-v)^2",
        "universal_unaugmented_order2_containment_under_reported_algebraic_hypotheses": "DISPROVED",
        "particular_selected_PGLib_network_counterexample": "NOT_ESTABLISHED",
        "actual_passive_admittance_realization": (
            "VERIFIED_CONNECTED_UNIT_CONDUCTANCE_PATH_WITH_BROAD_BOXES_AND_ENDPOINT_EQUATIONS"
            if passive_result else "NOT_CHECKED_FOR_HISTORICAL_VERSION"),
        "stronger_QC_RLT_OBBT_sparse_implementation_independence": "NOT_ESTABLISHED",
        "augmented_current_upper_localizer_u_p_equals_u_diagonal": str(strengthened_current_diagonal),
        "augmented_current_upper_localizer_has_negative_diagonal": True,
        "producer_checker_imported_or_executed": False,
        "producer_positivity_pivots_used": False,
        "arithmetic": "Python standard-library Fraction plus integer Bareiss determinants",
        "external_correctness_review": "UNKNOWN",
        "literature_priority": "UNKNOWN",
        "formal_proof_assistant_verification": "NOT_PERFORMED",
        "representing_measure_supported_on_stated_feasible_set": "IMPOSSIBLE_BY_NEGATIVE_VALID_CUT",
        "unrestricted_representing_measure_on_all_R4": "NOT_CHECKED",
        "software_trust": "Python integer/Fraction arithmetic and this saved verifier",
        "passive_embedding": None if passive_result is None else passive_result["summary"],
        "candidate_version": "EARLIER_TRANSCRIBED_MATHEMATICAL_SNAPSHOT" if HISTORICAL else "FROZEN_FINAL_RAW_INPUT",
    }
    write_json("EXACT_AUDIT_RESULT.json", result)

    proof = make_proof(sparse, quotient_basis, degree2, positivity, result)
    if passive_result:
        proof += passive_proof(passive_result)
    (OUTPUT / "ANALYTIC_PROOF.md").write_text(proof)
    summary = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (OUTPUT / "AUDIT_REPLAY.txt").write_text(summary)
    receipt_files = [REPORT, CANDIDATE, Path(__file__).resolve(),
                     OUTPUT / "REBUILT_MOMENT_FUNCTIONAL.json",
                     OUTPUT / "EXACT_AUDIT_RESULT.json", OUTPUT / "ANALYTIC_PROOF.md",
                     OUTPUT / "AUDIT_REPLAY.txt"]
    if passive_result:
        receipt_files.extend([CONSTRUCTOR, PASSIVE, OUTPUT / "PASSIVE_EMBEDDING_AUDIT.json"])
    write_json("HASH_RECEIPT.json", {
        "schema": "astra.independent-exact-audit-hash-receipt.v1",
        "hash_algorithm": "sha256",
        "scope": "Pinned supplied inputs and all substantive audit artifacts",
        "files": [{"absolute_path": str(path), "bytes": path.stat().st_size,
                   "sha256": digest(path)} for path in receipt_files],
        "receipt_self_hash": "Not included to avoid a self-referential hash",
        "software_trust_scope": "Integrity only; hashes are not external mathematical review",
        "python_runtime": sys.version,
    })
    print(summary, end="")


def poly_product(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            exponent = add(a, b)
            result[exponent] = result.get(exponent, F(0)) + ca * cb
    return {a: c for a, c in result.items() if c}


def poly_difference(left, right):
    result = dict(left)
    for a, coefficient in right.items():
        result[a] = result.get(a, F(0)) - coefficient
    return {a: c for a, c in result.items() if c}


def check_bound_products(polynomials, value):
    keys = list(polynomials)
    checks = []
    for i, first in enumerate(keys):
        for second in keys[i:]:
            product_polynomial = poly_product(polynomials[first], polynomials[second])
            scalar = sum(c * value(a) for a, c in product_polynomial.items())
            assert scalar >= 0, (first, second, scalar)
            checks.append({"first_bound": first, "second_bound": second, "value": str(scalar)})
    assert len(checks) == 36
    return checks


def audit_passive_embedding(old_value, degree2, degree1,
                            old_M, complex_degree2, complex_degree1,
                            complex_degree4):
    supplied = json.loads(PASSIVE.read_text())
    Y = [[F(v) for v in row] for row in supplied["Y"]]
    expected_Y = [[F(v) for v in row] for row in
                  [[1, 0, -1, 0], [0, 1, 0, -1],
                   [-1, 0, 2, -1], [0, -1, -1, 2]]]
    assert Y == expected_Y
    assert supplied["B_i"] == [1, 0, -1, 0]
    assert supplied["B_j"] == [0, 1, 0, -1]
    assert supplied["fixed_injection_buses"] == [0, 1]
    assert supplied["fixed_power_at_both"] == 1
    edges = [(0, 2), (2, 3), (3, 1)]
    edge_vectors = [tuple(int(j == first) - int(j == second) for j in range(4))
                    for first, second in edges]
    assert all(Y[i][j] == sum(e[i] * e[j] for e in edge_vectors)
               for i in range(4) for j in range(4))
    assert all(sum(row) == 0 for row in Y)
    assert integer_determinant([[int(v) for v in row[:3]] for row in Y[:3]]) == 1

    # Expand the pullback independently in the polynomial ring.  New variables
    # (x,y,w,t) map to (x,y,x-u,y-v) in the original variables.
    zero = (0, 0, 0, 0)
    images = [{(1, 0, 0, 0): F(1)}, {(0, 1, 0, 0): F(1)},
              {(1, 0, 0, 0): F(1), (0, 0, 1, 0): F(-1)},
              {(0, 1, 0, 0): F(1), (0, 0, 0, 1): F(-1)}]

    def expand(a):
        result = {zero: F(1)}
        for variable, exponent in enumerate(a):
            for _ in range(exponent):
                result = poly_product(result, images[variable])
        return result

    def value(a):
        return sum(coefficient * old_value(exponent)
                   for exponent, coefficient in expand(a).items())

    def matrix(basis, polynomial):
        return [[sum(c * value(add(add(a, b), t)) for t, c in polynomial.items())
                 for b in basis] for a in basis]

    M = matrix(degree2, {zero: F(1)})
    index2 = {a: i for i, a in enumerate(degree2)}
    A = [[expand(a).get(b, F(0)) for a in degree2] for b in degree2]
    assert all(v.denominator == 1 for row in A for v in row)
    determinant_A = integer_determinant([[int(v) for v in row] for row in A])
    assert abs(determinant_A) == 1
    assert all(M[i][j] == sum(A[k][i] * old_M[k][ell] * A[ell][j]
                             for k in range(15) for ell in range(15))
               for i in range(15) for j in range(15))
    assert value(zero) == 1
    all_moments = [{"exponents": a, "value": str(value(a))} for a in monomials(4, 4)]

    bounds = [(F(1), F(4)), (F(1), F(4)),
              (F(1, 10000), F(100)), (F(1, 10000), F(100))]
    assert [[F(v) for v in supplied["squared_voltage_bounds"][name]]
            for name in ("x", "y", "w", "t")] == list(map(list, bounds))
    localizers = {}
    real_bounds_polynomials = {}
    for coordinate, name in enumerate(("x", "y", "w", "t")):
        square = tuple(2 if j == coordinate else 0 for j in range(4))
        lower, upper = bounds[coordinate]
        for side, coefficients in [("lower", {square: F(1), zero: -lower}),
                                   ("upper", {square: F(-1), zero: upper})]:
            key = name + "_" + side
            local = matrix(degree1, coefficients)
            real_bounds_polynomials[key] = coefficients
            localizers[key] = {"matrix": rational_matrix(local), "rank": 5,
                               "positive_definite": True,
                               "certificate": sylvester(local)}

    equality_checks = []
    for name, polynomial in [("x*(x-w)-1", {(2, 0, 0, 0): F(1), (1, 0, 1, 0): F(-1), zero: F(-1)}),
                             ("y*(y-t)-1", {(0, 2, 0, 0): F(1), (0, 1, 0, 1): F(-1), zero: F(-1)})]:
        for multiplier in degree2:
            residual = sum(c * value(add(multiplier, t)) for t, c in polynomial.items())
            assert residual == 0
            equality_checks.append({"equality": name, "multiplier_exponents": multiplier,
                                    "residual": str(residual)})

    def complex_value(a):
        assert sum(a) <= 4
        if any(a[j] for j in (1, 3, 5, 7)):
            return F(0)
        return value((a[0], a[2], a[4], a[6]))

    def complex_matrix(basis, polynomial):
        return [[sum(c * complex_value(add(add(a, b), t))
                     for t, c in polynomial.items()) for b in basis] for a in basis]

    complex_zero = (0,) * 8
    complex_M = complex_matrix(complex_degree2, {complex_zero: F(1)})
    project2 = [None if any(a[j] for j in (1, 3, 5, 7))
                else index2[(a[0], a[2], a[4], a[6])] for a in complex_degree2]
    assert all(complex_M[i][j] == (F(0) if ir is None or jr is None else M[ir][jr])
               for i, ir in enumerate(project2) for j, jr in enumerate(project2))

    index1 = {a: i for i, a in enumerate(degree1)}
    project1 = [None if any(a[j] for j in (1, 3, 5, 7))
                else index1[(a[0], a[2], a[4], a[6])] for a in complex_degree1]
    complex_localizers = {}
    complex_bounds_polynomials = {}
    for coordinate, name in enumerate(("x", "y", "w", "t")):
        rr = tuple(2 if j == 2 * coordinate else 0 for j in range(8))
        ii = tuple(2 if j == 2 * coordinate + 1 else 0 for j in range(8))
        lower, upper = bounds[coordinate]
        for side, polynomial in [("lower", {rr: F(1), ii: F(1), complex_zero: -lower}),
                                 ("upper", {rr: F(-1), ii: F(-1), complex_zero: upper})]:
            key = name + "_" + side
            local = complex_matrix(complex_degree1, polynomial)
            complex_bounds_polynomials[key] = polynomial
            real_local = [[F(v) for v in row] for row in localizers[key]["matrix"]]
            assert all(local[i][j] == (F(0) if ir is None or jr is None else real_local[ir][jr])
                       for i, ir in enumerate(project1) for j, jr in enumerate(project1))
            complex_localizers[key] = {"matrix": rational_matrix(local), "rank": 5,
                                       "positive_semidefinite": True}

    bound_products = check_bound_products(real_bounds_polynomials, value)
    complex_bound_products = check_bound_products(complex_bounds_polynomials, complex_value)
    assert bound_products == complex_bound_products

    complex_equality_checks = []
    for name, endpoint, interior in [("x*(x-w)-1", 0, 4), ("y*(y-t)-1", 2, 6)]:
        def term(*indices):
            result = [0] * 8
            for i in indices:
                result[i] += 1
            return tuple(result)
        real = {term(endpoint, endpoint): F(1), term(endpoint, interior): F(-1),
                term(endpoint + 1, endpoint + 1): F(1),
                term(endpoint + 1, interior + 1): F(-1), complex_zero: F(-1)}
        imag = {term(endpoint + 1, interior): F(1), term(endpoint, interior + 1): F(-1)}
        for part, polynomial in [("real", real), ("imaginary", imag)]:
            for multiplier in complex_degree2:
                residual = sum(c * complex_value(add(multiplier, t))
                               for t, c in polynomial.items())
                assert residual == 0
                complex_equality_checks.append({"equality": name + "_" + part,
                                               "multiplier_exponents": multiplier,
                                               "residual": str(residual)})
    assert len(complex_equality_checks) == 180

    q = {(1, 0, 0, 0): F(-1), (0, 1, 0, 0): F(1)}
    z = {(1, 0, 0, 0): F(1), (0, 1, 0, 0): F(-1),
         (0, 0, 1, 0): F(-1), (0, 0, 0, 1): F(1)}
    cut_polynomial = poly_difference(poly_product(q, q), poly_product(z, z))
    cut = sum(c * value(a) for a, c in cut_polynomial.items())
    assert cut == F(-897, 10000) and cut == F(supplied["lower_cut_value"])

    # A concrete nonempty exact physical algebraic instance; this is separate
    # from the nonrepresenting truncated witness above, and adds no OPF limits.
    point = (F(3, 2), F(3, 2), F(5, 6), F(5, 6))
    currents = [sum(Y[i][j] * point[j] for j in range(4)) for i in range(4)]
    injections = [point[i] * currents[i] for i in range(4)]
    assert injections[:2] == [F(1), F(1)]
    assert all(lo <= point[j] ** 2 <= hi for j, (lo, hi) in enumerate(bounds))
    losses = sum((point[a] - point[b]) ** 2 for a, b in edges)
    assert losses == sum(injections) == F(8, 9)

    summary = {
        "status": "PASS_EXACT_CONNECTED_PASSIVE_PATH_EMBEDDING",
        "real_M2_dimension": 15, "real_M2_rank": 13,
        "moment_basis_transform_determinant": str(determinant_A),
        "all_8_original_network_voltage_localizers_PD": True,
        "localizer_dimension": 5, "real_equality_multiplier_checks": 30,
        "scalar_degree4_original_voltage_bound_products": 36,
        "all_scalar_bound_products_nonnegative": True,
        "complex_scalar_bound_products_same_exact_values": True,
        "complex_M2_dimension": 45, "complex_M2_rank": 13,
        "all_8_complex_network_voltage_localizers_PSD": True,
        "complex_localizer_dimension": 9, "complex_equality_multiplier_checks": 180,
        "Y_passive_connected_unit_conductance_path": True, "Y_rank": 3,
        "lower_cut_value": str(cut),
        "full_physical_OPF_additional_interior_power_or_branch_constraints": "NOT_CHECKED_OR_CLAIMED",
    }
    return {"schema": "astra.independent-passive-reciprocal-embedding-audit.v1",
            "summary": summary, "coordinate_order": ["x", "y", "w", "t"],
            "Y": rational_matrix(Y), "edges": edges,
            "Y_edge_outer_product_vectors": edge_vectors,
            "Y_principal_3x3_minor": "1",
            "moment_basis_transform": rational_matrix(A),
            "full_degree4_real_moments": all_moments,
            "full_real_M2": rational_matrix(M), "full_real_M2_basis": degree2,
            "identity": "M2_passive=A^T M2_original A; det(A)=1",
            "full_original_network_voltage_localizers": localizers,
            "all_scalar_degree4_voltage_bound_products": bound_products,
            "full_real_equality_checks": equality_checks,
            "complex_coordinate_order": ["xr", "xi", "yr", "yi", "wr", "wi", "tr", "ti"],
            "full_degree4_complex_moments": [{"exponents": a, "value": str(complex_value(a))}
                                             for a in complex_degree4],
            "full_complex_M2": rational_matrix(complex_M),
            "full_complex_original_network_voltage_localizers": complex_localizers,
            "full_complex_equality_checks": complex_equality_checks,
            "cut_polynomial_terms": [{"exponents": a, "coefficient": str(c)}
                                     for a, c in sorted(cut_polynomial.items())],
            "distinct_exact_feasible_point": {"voltage": list(map(str, point)),
                                              "currents": list(map(str, currents)),
                                              "injections": list(map(str, injections)),
                                              "total_resistive_losses": str(losses)},
            "scope": "Connected passive network; endpoint fixed powers and stated broad positive voltage boxes only",
            "excluded_claims": ["Selected PGLib case", "All prescribed interior injections",
                                "Branch angle/thermal limits", "Generator bounds/objective",
                                "Additional reference phasor sign restrictions",
                                "Strongest implemented incumbent independence", "External review", "Priority"]}


def passive_proof(passive):
    entries = []
    for name, localizer in passive["full_original_network_voltage_localizers"].items():
        determinants = localizer["certificate"]["rational_leading_principal_determinants"]
        entries.append("### Passive " + name + "\n\n" + "\n".join(
            f"{i + 1}. `{value}` > 0" for i, value in enumerate(determinants)))
    return f"""

## 11. Independently verified connected passive-network embedding

The final witness additionally has an exact passive embedding. Set `w=x-u`,
`t=y-v`, and use the four complex voltage coordinates `(x,y,w,t)` on the path
`x--w--t--y`, each edge having unit positive real admittance. Its complete
admittance matrix is

```text
Y = [[ 1,  0, -1,  0],
     [ 0,  1,  0, -1],
     [-1,  0,  2, -1],
     [ 0, -1, -1,  2]].
```

The verifier reconstructs `Y` as the sum of the three edge-incidence outer
products. Consequently `V*Y V=|x-w|^2+|w-t|^2+|t-y|^2>=0`, so the network is
passive. The graph is connected and a principal 3-by-3 minor is exactly one;
`Y` has rank three. Its endpoint currents are `x-w=u` and `y-t=v`, exactly the
required current rows. Set both endpoint fixed powers to one. The endpoint
equalities are then `conj(x)*(x-w)=1` and `conj(y)*(y-t)=1`.

The linear voltage transformation `(x,y,u,v)->(x,y,x-u,y-v)` is invertible and
is its own inverse. The verifier expands every original degree-at-most-four
monomial after this substitution. It explicitly builds the 15-by-15 induced
degree-two coefficient map `A`, checks `det(A)=1`, and verifies every entry of
`M2_passive=A^T M2_original A`. Hence the whole transformed moment matrix is
PSD of rank 13.

All original voltage-coordinate bounds for this constructed passive network are
included: `1<=|x|^2,|y|^2<=4` and
`1/10000<=|w|^2,|t|^2<=100`. The verifier reconstructs all eight 5-by-5
localizers in the new original-voltage basis `(1,t,w,y,x)` and proves each PD
using exact Sylvester determinants. It separately checks all 30 real endpoint
equality multipliers. It also reconstructs the full 45-by-45 complex-as-real
moment matrix, every 9-by-9 modulus-bound localizer, all 495 moments, and all 180
real/imaginary endpoint equality multiplier tests. They all pass. Exact
transformed matrices and certificates are in `PASSIVE_EMBEDDING_AUDIT.json`.

The audit additionally expands all 36 unordered scalar pair-products, including
self-products, of the eight original network voltage-bound polynomials. Every
degree-four moment value is nonnegative. It separately checks the full complex
modulus-bound products and obtains the same exact values. Thus adding these
degree-four scalar voltage-bound preordering products also preserves the
witness. All 36 exact values are saved in the passive embedding audit. This
additional statement concerns only these specified products.

The passive-network cut is

`(y-x)^2-((x-w)-(y-t))^2`,

and its reconstructed moment value is exactly `-897/10000`.

The algebraic feasible set is nonempty: the distinct exact voltage point
`(x,y,w,t)=(3/2,3/2,5/6,5/6)` meets these boxes and the endpoint fixed powers.
Its interior real injections are `-5/9,-5/9`; its total resistive loss is `8/9`.
That actual feasible point is separate from the truncated witness, which has no
representing positive measure supported on this feasible set. Unrestricted
representability on all real voltage space is not decided by this audit.

This strengthens the algebraic separation: it persists for a connected passive
network with broad positive voltage boxes and two endpoint fixed-power
equations. It still does not certify a full OPF with separately prescribed
interior bus injections, generator limits, branch-angle or thermal limits, or
the selected PGLib instance. No such additional constraints are silently
included in the conclusion. External correctness review and priority remain
UNKNOWN.

The transformed localizer determinants, in the basis `(1,t,w,y,x)`, are:

{chr(10).join(entries)}
"""


def monomial_name(a):
    parts = []
    for variable, exponent in zip(("x", "y", "u", "v"), a):
        if exponent:
            parts.append(variable if exponent == 1 else variable + "^" + str(exponent))
    return " ".join(parts) or "1"


def make_proof(sparse, quotient_basis, degree2, positivity, result):
    table = "\n".join(f"| {k} | {ell} | `{value}` |"
                       for (k, ell), value in sorted(sparse.items()))
    determinant_blocks = []
    for name, certificate in positivity.items():
        entries = "\n".join(f"{i + 1}. `{determinant}` > 0"
                             for i, determinant in enumerate(
                                 certificate["rational_leading_principal_determinants"]))
        determinant_blocks.append(f"### {name}\n\n{entries}")
    passive_scope = (
        "The final version also passes the separate connected passive-network embedding "
        "proved in Section 11. No selected PGLib model, prescribed interior power "
        "injections, branch/generator limits, or stronger incumbent formulation "
        "was checked."
        if result["passive_embedding"] else
        "No passive-network embedding was checked for this earlier transcribed version. "
        "No selected PGLib model, complete passive admittance matrix, branch/generator "
        "limits, prescribed interior power balances, or stronger incumbent formulation "
        "was checked."
    )
    input_scope = (
        "This final audit pins the report, the frozen EXACT_COUNTEREXAMPLE.json, "
        "the frozen producer verify_counterexample.py, and PASSIVE_EMBEDDING.json. "
        "The producer checker is never imported or executed."
        if result["passive_embedding"] else
        "This historical audit uses the exact rational table and model metadata "
        "transcribed from the earlier initial read, saved as earlier_read_snapshot.json. "
        "The earlier producer file was overwritten before its raw bytes were pinned; "
        "its original raw-file hash is NOT_CAPTURED_BEFORE_OVERWRITE. This snapshot "
        "is not claimed to reproduce those original file bytes."
    )
    final_passive_note = (
        "The final version's separately checked passive embedding is specified below."
        if result["passive_embedding"] else
        "No passive embedding claim is made for this historical snapshot."
    )
    return f"""# Independent exact audit: reciprocal lower cut at order two

**Verdict: the supplied candidate is a legal counterexample to universal
unaugmented full real order-two containment under the algebraic hypotheses
explicitly displayed in `reciprocal_report.txt`.** The whole truncated
functional passes, including its singular full moment matrix, all eight
original voltage-bound localizers, and every required equality multiplier.
The exact violated value is `{result['lower_cut_value']}`.

This conclusion concerns those algebraic hypotheses. {passive_scope}
External correctness review and literature priority are UNKNOWN.

## 1. Inputs, independence, and scope

{input_scope} The initial `rationalize_order2.py` was also read before the
producer finalized the candidate, but is never imported or executed. For moment
positivity the verifier uses only the rational table as witness data, not the producer's
status, positivity pivots, search output, numerical solution, or rounding recipe.
`verify_exact.py` regenerates all substantive artifacts in this audit directory.
`HASH_RECEIPT.json` pins the inputs and generated outputs.

The independently checked arithmetic is integer/Fraction arithmetic. Positivity
uses fraction-free Bareiss determinants and Sylvester's criterion. This is a
saved, replayable mathematical certificate with software trust, not a
proof-assistant proof or external review.

## 2. The exact problem instance

Use four complex voltage coordinates `V=(x,y,u,v)`, with all imaginary
coordinates zero in the embedded functional. Select the fixed-injection buses
`i=1,j=2` and linear rows `B_i=(0,0,1,0)`, `B_j=(0,0,0,1)`. Thus the currents
`J_i=B_i V=u` and `J_j=B_j V=v` are linear functions of the original voltage
coordinates; they are not additional independent current variables.

The fixed-power equations are `conj(x)u-1=0` and `conj(y)v-1=0`. On the real
subspace they are `xu=1` and `yv=1`. All four original voltage-coordinate bounds
are included:

* `1 <= |x|^2 <= 4` and `1 <= |y|^2 <= 4`;
* `1/64 <= |u|^2 <= 64` and `1/64 <= |v|^2 <= 64`.

The source's displayed containment hypotheses constrain `B_i,B_j` only by their
linearity in the voltages. The selector rows satisfy that requirement. This
selector construction itself does not rely on any physical admittance
realization. For the final version, Section 11 separately verifies a connected
passive realization after changing original voltage coordinates and boxes.
Neither construction certifies the selected PGLib case.

For `alpha=1`, `beta=-1`, the source definitions give `z=u-v`, `q=y-x`, and
`a_i a_j=1`. Therefore the lower reciprocal cut is
`f=(y-x)^2-(u-v)^2 >= 0` on this real subspace.

## 3. Complete normalized truncated functional

For every `a,b,c,d >= 0` with `a+b+c+d <= 4`, define

`L(x^a y^b u^c v^d)=m[a-c,b-d]`, with `m[k,l]=m[l,k]`.

The complete defining table for sorted labels `k<=l` is:

| k | l | m[k,l] |
|---:|---:|---:|
{table}

Every label arising from a degree-at-most-four monomial is covered. In
particular, `L(1)=1`. All odd-total-degree monomials vanish, and swapping
`x<->y,u<->v` preserves the functional. The audit explicitly enumerates and
saves all 70 original real moments in `REBUILT_MOMENT_FUNCTIONAL.json`.

## 4. Every equality multiplier through total degree four

Multiplication by `xu` leaves `(a-c,b-d)` unchanged, as does multiplication by
`yv`. Thus for each monomial `t` of degree at most two,

`L(t(xu-1))=0` and `L(t(yv-1))=0`.

The 15 such monomials span all permissible multipliers for quadratic equalities
at order two. The verifier separately evaluates all 30 identities from the
full degree-four table and saves their exact zero residuals. Linearity then
establishes the identities for every polynomial multiplier of degree at most
two, including every equality combination of total degree at most four.

## 5. Full 15-by-15 moment positivity

The full degree-at-most-two basis, in the audit's independently generated
graded lexicographic order, is

`({', '.join(monomial_name(a) for a in degree2)})`.

Reducing these monomials by `xu=yv=1` leaves the 13 distinct representatives

`({', '.join(monomial_name(a) for a in quotient_basis)})`.

Let `C` be the 13-by-15 one-hot matrix assigning each original monomial to its
representative, and let `Q` be the corresponding 13-by-13 Gram matrix. Every
entry is reconstructed from the full original moment table, and the audit
checks the exact identity `M_2=C^T Q C` entry by entry. The matrix `C` has row
rank 13 since every representative occurs in the original basis.

The first nine quotient representatives have even degree; the final four have
odd degree. Since every odd moment vanishes, `Q` is the direct sum of a 9-by-9
even block and a 4-by-4 odd block. Every leading principal determinant of each
block is strictly positive, with exact values reproduced below. Sylvester's
criterion proves both blocks positive definite, so `Q` is positive definite and
`M_2` is positive semidefinite of rank 13. Its two-dimensional kernel is exactly
the coefficient span of `xu-1` and `yv-1`.

This argument proves positivity for every square of a polynomial of degree at
most two, not just selected submatrices or the cut value.

## 6. Every original voltage-bound localizer

Use the complete degree-at-most-one basis `(1,v,u,y,x)`. For each of the eight
quadratic bound polynomials

`x^2-1, 4-x^2, y^2-1, 4-y^2, u^2-1/64, 64-u^2, v^2-1/64, 64-v^2`,

the verifier reconstructs the entire 5-by-5 localizing matrix with entries
`L(g*b_r*b_s)`. All five leading principal determinants of each matrix are
strictly positive. Thus all eight localizers are positive definite of rank five
and `L(g*p^2)>=0` for every linear polynomial `p`. The exact matrices and all
determinant certificates are saved and displayed below.

The verifier also explicitly expands and evaluates all 36 unordered scalar
pair-products, including self-products, of these eight quadratic bound
polynomials. Every degree-four value is nonnegative, and the full complex
modulus-bound products have the same exact values. These additional scalar
voltage-bound preordering constraints therefore do not remove the witness.
All 36 exact evaluations are saved in `REBUILT_MOMENT_FUNCTIONAL.json`.

## 7. Full complex embedding

Write the eight real coordinates as
`(xr,xi,yr,yi,ur,ui,vr,vi)`. Define a degree-at-most-four moment to be zero
whenever an imaginary coordinate occurs; otherwise use the corresponding real
moment above. This defines all 495 moments explicitly and has `L_C(1)=1`.

The complete complex-as-real order-two matrix has size 45. Its rows containing
an imaginary coordinate are zero; its remaining principal matrix is exactly
the full real 15-by-15 matrix. An explicit coordinate projection therefore gives
`M_2^C=P^T M_2 P`, proving PSD and rank 13.

Each modulus-square voltage localizer has size nine. Its imaginary-coordinate
rows are zero and its remaining principal matrix is the corresponding real
5-by-5 localizer, so all eight are PSD of rank five.

The real part of `conj(x)u-1` is `xr*ur+xi*ui-1`, and its imaginary part is
`xr*ui-xi*ur`; the analogous formulas hold for `y,v`. The real parts reduce to
the previously verified identities, and every imaginary term vanishes. The
verifier explicitly evaluates all four real equality components against all 45
degree-at-most-two monomial multipliers: 180 exact zero checks. Hence the
embedding meets the full complex-voltage order-two constraints.

## 8. Exact cut violation and consistency with other source claims

Expanding the cut directly in the original variables gives

`L(f)=L(x^2)+L(y^2)-2L(xy)-L(u^2)-L(v^2)+2L(uv)`

`=2*({sparse[(0, 2)]} - {sparse[(1, 1)]}`
`     - {sparse[(-2, 0)]} + {sparse[(-1, -1)]})`

`={result['lower_cut_value']} < 0`.

Thus a normalized feasible order-two truncated functional violates the claimed
universal lower containment. This is a rigorous algebraic separation witness,
not a physically feasible voltage vector. It has no representing positive
measure supported on the stated feasible voltage set. Unrestricted truncated
representability on all of `R^4` is not decided here.
Indeed, at every actual real point satisfying `xu=yv=1` and `x^2,y^2>=1`,

`f=(x-y)^2*(1-1/(x^2*y^2))>=0`.

The witness does not satisfy the source's *augmented* order-two relaxation. The
valid current upper bound `u^2<=1` has, for the linear test polynomial `p=u`,

`L((1-u^2)u^2)={result['augmented_current_upper_localizer_u_p_equals_u_diagonal']} < 0`.

The valid scalar current bounds `L(u^2),L(v^2)<=1` do hold, emphasizing the
distinction between scalar bounds and all their localizing constraints. There
is no contradiction with the source's upper-cut, order-three, or augmented
order-two containment statements. No independence from complete QC/RLT/OBBT or
any specified sparse implementation is established.

## 9. Exact positivity certificates

Each list below consists of the leading principal determinants in order, using
the bases and blocks already specified. For the eight localizers the basis is
`(1,v,u,y,x)`. The verifier clears a common positive denominator and computes
integer determinants by exact fraction-free elimination; the displayed reduced
fractions are the resulting exact determinants. All comparisons to zero use
integers, not floating-point approximations.

{chr(10).join(determinant_blocks)}

## 10. Replay and limits

Run `python3 verify_exact.py` from this directory, or use its absolute path. It
reconstructs all moments, every matrix, the congruence identities, determinant
certificates, equality checks, exact cut value, this proof, and the hash receipt.
No optimization solver or third-party Python package is required.

The certificate resolves the algebraic universal-containment question under the
reported hypotheses. It establishes no runtime advantage, external novelty,
selected-case strengthening against an unexecuted incumbent, experimental
physical validation, or new optimization capability. Those claims remain
outside this audit; external correctness and priority remain UNKNOWN.
{final_passive_note}
"""


if __name__ == "__main__":
    main()
