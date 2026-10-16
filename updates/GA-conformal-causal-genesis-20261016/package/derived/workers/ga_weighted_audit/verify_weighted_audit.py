#!/usr/bin/env python3
"""Exact finite checks accompanying the independent weighted-polynomial audit.

Standard library only. These checks validate coefficient algebra, explicit
periodic fields, and finite null-polynomial linear systems. They do not
machine-formalize the analytic interpolation theorem or the general proof.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PIN = "f80a8f15137575133ad2c9af975513b32e8fa93e"
SOURCE = HERE.parents[1] / "originals/conformal_packet/RESEARCH_REPORT.md"
CHECKS = []


def require(condition, name, detail=None):
    if not condition:
        raise RuntimeError(f"FAILED: {name}: {detail}")
    CHECKS.append({"name": name, "passed": True, "detail": detail})


def exponents(degree, variables):
    if variables == 1:
        yield (degree,)
        return
    for first in range(degree + 1):
        for tail in exponents(degree - first, variables - 1):
            yield (first,) + tail


def weight(e):
    a, b, c, q = e
    return a + 2 * c + 2 * q


def exact_rank(rows):
    pivots = {}
    for source_row in rows:
        row = {k: F(v) for k, v in source_row.items() if v}
        while row:
            leading = min(row)
            if leading not in pivots:
                scale = row[leading]
                pivots[leading] = {k: v / scale for k, v in row.items()}
                break
            factor = row[leading]
            for k, v in pivots[leading].items():
                row[k] = row.get(k, F(0)) - factor * v
                if not row[k]:
                    del row[k]
    return len(pivots)


def derivative_map(e, indices):
    e = list(e)
    coefficient = 1
    for i in indices:
        coefficient *= e[i]
        e[i] -= 1
        if coefficient == 0:
            return None
    return tuple(e), coefficient


def null_equation_rows(degree):
    """H_Q=0; H_uu=H_uv=H_vz=H_zz=0; H_vv+2H_uz=0."""
    monomials = list(exponents(degree, 4))  # (u, v, z, Q)
    equations = [
        [(F(1), (3,))],
        [(F(1), (0, 0))],
        [(F(1), (0, 1))],
        [(F(1), (1, 2))],
        [(F(1), (2, 2))],
        [(F(1), (1, 1)), (F(2), (0, 2))],
    ]
    rows = []
    for equation in equations:
        coefficients = {}
        for column, e in enumerate(monomials):
            for multiplier, indices in equation:
                result = derivative_map(e, indices)
                if result is None:
                    continue
                out, coefficient = result
                row = coefficients.setdefault(out, {})
                row[column] = row.get(column, F(0)) + multiplier * coefficient
        rows.extend(coefficients.values())
    return monomials, rows


def clean(p):
    return {k: F(v) for k, v in p.items() if v}


def add(p, q):
    result = dict(p)
    for k, v in q.items():
        result[k] = result.get(k, F(0)) + v
    return clean(result)


def scale(p, c):
    return clean({k: c * v for k, v in p.items()})


def multiply(p, q):
    result = {}
    for (px, py), pv in p.items():
        for (qx, qy), qv in q.items():
            k = (px + qx, py + qy)
            result[k] = result.get(k, F(0)) + pv * qv
    return clean(result)


def power(p, n):
    result = {(0, 0): F(1)}
    for _ in range(n):
        result = multiply(result, p)
    return result


def average(p):
    return p.get((0, 0), F(0))


def cosine(kx, ky, amplitude=F(1)):
    amplitude = F(amplitude)
    return {(kx, ky): amplitude / 2, (-kx, -ky): amplitude / 2}


def second_derivative(p, i, j):
    return clean({k: -k[i] * k[j] * v for k, v in p.items()})


def frequency_multiply(p, axis, N):
    """A first derivative after removing its common factor i."""
    return clean({k: k[axis] * (N if axis == 1 else 1) * v for k, v in p.items()})


def determinant(a, b, c, d):
    return add(multiply(a, d), scale(multiply(b, c), -1))


def hessian(psi):
    return (
        second_derivative(psi, 0, 0),
        second_derivative(psi, 0, 1),
        second_derivative(psi, 1, 1),
    )


def compatible_components(psi, Q, sigma, N):
    """Exact components of the periodic two-scale map in REPORT.md."""
    eps = F(1, N)
    u, v, z = hessian(psi)
    h = {}
    for k, coefficient in Q.items():
        if k == (0, 0):
            if coefficient:
                raise RuntimeError("Q must have mean zero")
        else:
            h[k] = -coefficient / (k[0] ** 2 + k[1] ** 2)
    hxx, hxy, hyy = hessian(h)
    a = add(scale(v, eps), scale(hxx, eps ** 2 / sigma))
    b = add(z, scale(hxy, eps / sigma))
    c = add(scale(u, -sigma * eps ** 2), scale(hxy, eps ** 3))
    d = add(scale(v, -sigma * eps), scale(hyy, eps ** 2))
    q = add(scale(a, sigma), d)
    require(q == scale(Q, eps ** 2), f"exact defect scaling N={N}")
    require(
        frequency_multiply(a, 1, N) == frequency_multiply(b, 0, N),
        f"first-row compatibility N={N}",
    )
    require(
        frequency_multiply(c, 1, N) == frequency_multiply(d, 0, N),
        f"second-row compatibility N={N}",
    )
    require(all(average(x) == 0 for x in (a, b, c, d)), f"gradient means N={N}")
    require(average(determinant(a, b, c, d)) == 0, f"determinant null mean N={N}")
    return a, b, c, d, q


def allocate_defect(e, alpha):
    """A constructive capacity check for the Holder/interpolation proof."""
    a, b, c, q = e
    capacities = [F(1)] * (c + q) + [F(1, 2)] * a + [F(0)] * b
    remaining = alpha
    allocation = []
    for capacity in capacities:
        used = min(capacity, remaining)
        allocation.append(used)
        remaining -= used
    return remaining, allocation


def main():
    rank_receipts = []
    for degree in range(2, 9):
        monomials, rows = null_equation_rows(degree)
        rank = exact_rank(rows)
        expected_nullity = 1 if degree == 2 else 0
        require(
            len(monomials) - rank == expected_nullity,
            f"homogeneous Hessian/null-defect equations degree={degree}",
            {"dimension": len(monomials), "rank": rank, "nullity": len(monomials) - rank},
        )
        rank_receipts.append({"degree": degree, "dimension": len(monomials), "rank": rank})

    degree_two, degree_two_rows = null_equation_rows(2)
    det_vector = {
        degree_two.index((1, 0, 1, 0)): F(1),
        degree_two.index((0, 2, 0, 0)): F(-1),
    }
    require(
        all(sum(v * det_vector.get(k, 0) for k, v in row.items()) == 0 for row in degree_two_rows),
        "degree-two Hessian determinant spans the exception",
    )

    require(len(list(exponents(3, 4))) == 20, "cubic polynomial dimension")
    require(
        sum(weight(e) >= 2 for e in exponents(3, 4)) == 18,
        "packet cubic dimension recovered from weighted rule",
    )

    exponent_cases = [
        (3, F(1), F(2), F(4)),
        (3, F(3, 2), F(2), F(6)),
        (4, F(2), F(3), F(6)),
        (5, F(3), F(4), F(8)),
        (3, F(3), F(3), F(2)),
    ]
    for degree, alpha, p, s in exponent_cases:
        require(alpha / p + (degree - alpha) / s == 1, f"balanced exponents {degree, alpha, p, s}")
        for e in exponents(degree, 4):
            if weight(e) < 2 * alpha:
                continue
            remaining, allocation = allocate_defect(e, alpha)
            require(remaining == 0, f"defect allocation {degree, alpha, e}")
            reciprocal_sum = sum(beta / p + (1 - beta) / s for beta in allocation)
            require(reciprocal_sum == 1, f"Holder balance {degree, alpha, e}")

    psi = add(add(cosine(1, 1, -1), cosine(0, 1, -1)), cosine(1, 2, F(-1, 2)))
    u, v, z = hessian(psi)
    det_hessian = add(multiply(u, z), scale(power(v, 2), -1))
    require(average(multiply(v, power(z, 2))) == F(3, 2), "exact packet ab-squared coefficient")
    require(average(power(u, 2)) == F(5, 8), "exact packet xx squared norm")
    require(average(det_hessian) == 0, "Hessian determinant mean")
    require(average(multiply(z, det_hessian)) == F(3, 4), "cubic b times determinant is not null")

    sigma = F(2)
    for N in (1, 2, 7, 31):
        a, b, c, d, q = compatible_components(psi, {}, sigma, N)
        require(
            average(multiply(a, power(b, 2))) == F(3, 2 * N),
            f"forbidden ab-squared moment N={N}",
        )
        require(
            average(multiply(b, determinant(a, b, c, d))) == 3 * sigma / (4 * N * N),
            f"higher-degree determinant-product obstruction N={N}",
        )

    Q = add(power(z, 2), {(0, 0): -average(power(z, 2))})
    for N in (1, 5, 17):
        compatible_components(psi, Q, sigma, N)
    require(
        average(multiply(Q, power(z, 2))) > 0,
        "independent q-times-b-squared leading moment",
        str(average(multiply(Q, power(z, 2)))),
    )

    shear_b = add(cosine(0, 1), cosine(0, 2))
    require(average(power(shear_b, 3)) == F(3, 4), "pure-shear cubic obstruction")

    psi_a3 = add(add(cosine(1, 1, -1), cosine(1, 2, -1)), cosine(2, 3, -1))
    _, a3_base, _ = hessian(psi_a3)
    require(average(power(a3_base, 3)) == F(18), "a-cubed has nonzero signed leading coefficient")

    receipt = {
        "status": "PASS_FINITE_ALGEBRA_ONLY",
        "checks": len(CHECKS),
        "repository_pin_supplied_and_separately_verified": PIN,
        "source_path": str(SOURCE),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "exact_null_system_ranks": rank_receipts,
        "scope": "Exact finite coefficient algebra and declared compatible Fourier fields; not a formal analytic theorem proof, sharp constant, novelty clearance, or quasiconvexity proof.",
        "groups": CHECKS,
    }
    destination = HERE / "VERIFICATION_RECEIPT.json"
    destination.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS: {len(CHECKS)} exact checks; receipt: {destination}")


if __name__ == "__main__":
    main()
