"""Exact physical-coordinate Jacobian for a fixed-total-hazard ramp family.

The five chronological intervals have length log(2). Parameter x_(j,ell),
ell=0,...,3, adds x to stage j in interval ell and subtracts x in interval 4.
The baseline constant rates are distinct positive integers. Output rows are
the six strict-lower transient entries at speed 1, then the same at speed 2.
No eigenbasis or survival normalization remains in these output coordinates.

Import fixed_hazard_jacobian(rates); it returns SymPy exact matrices and norms.
"""

from pathlib import Path
import json
import sympy as S


HERE = Path(__file__).parent
LOWER = [(p, q) for p in range(4) for q in range(p)]


def generators(n=4):
    out = []
    for j in range(n):
        b = S.zeros(n)
        b[j, j] = -1
        if j + 1 < n:
            b[j + 1, j] = 1
        out.append(b)
    return out


def eigenbasis(rates):
    rates = tuple(map(S.Integer, rates))
    v = S.eye(len(rates))
    for q in range(len(rates)):
        for p in range(q + 1, len(rates)):
            v[p, q] = rates[p - 1] * v[p - 1, q] / (rates[p] - rates[q])
    return v


def fixed_hazard_jacobian(rates):
    rates = tuple(map(S.Integer, rates))
    assert len(rates) == 4 and len(set(rates)) == 4 and min(rates) > 0
    v, bs = eigenbasis(rates), generators()
    vi = v.inv()
    cs = [vi * b * v for b in bs]
    jac = S.zeros(12, 16)
    for j in range(4):
        for ell in range(4):
            for speed_index, speed in enumerate([1, 2]):
                derivative_eig = S.zeros(4)
                for p, q in LOWER:
                    gap = rates[p] - rates[q]
                    derivative_eig[p, q] = cs[j][p, q] * S.Integer(2) ** (-5 * speed * rates[p]) * (
                        S.Integer(2) ** (speed * gap * (ell + 1))
                        - S.Integer(2) ** (speed * gap * ell)
                        - S.Integer(2) ** (5 * speed * gap)
                        + S.Integer(2) ** (4 * speed * gap)
                    ) / gap
                derivative = v * derivative_eig * vi
                assert all(derivative[i, i] == 0 for i in range(4))
                for row, (p, q) in enumerate(LOWER):
                    jac[speed_index * 6 + row, j * 4 + ell] = derivative[p, q]
    pivots = list(jac.rref()[1])
    assert len(pivots) == 12
    square = jac[:, pivots]
    inverse = square.inv()
    inverse_norm = max(sum(abs(x) for x in inverse.row(i)) for i in range(12))
    baseline = [v * S.diag(*[S.Integer(2) ** (-5 * speed * a) for a in rates]) * vi
                for speed in [1, 2]]
    return {
        "rates": rates,
        "jacobian": jac,
        "pivots": pivots,
        "square_jacobian": square,
        "inverse": inverse,
        "inverse_norm_inf": inverse_norm,
        "baseline": baseline,
        "eigenbasis": v,
    }


def serializable_certificate(result):
    return {
        "rates": [int(x) for x in result["rates"]],
        "row_order_one_based": [[p + 1, q + 1] for p, q in LOWER] * 2,
        "row_speeds": [1] * 6 + [2] * 6,
        "column_order": "stage j=1,...,4, then chronological interval ell=0,...,3; compensate interval4",
        "jacobian": [[str(x) for x in row] for row in result["jacobian"].tolist()],
        "pivots_zero_based": result["pivots"],
        "square_inverse": [[str(x) for x in row] for row in result["inverse"].tolist()],
        "inverse_norm_inf": str(result["inverse_norm_inf"]),
        "square_determinant": str(result["square_jacobian"].det()),
        "baseline": [[[str(x) for x in row] for row in r.tolist()] for r in result["baseline"]],
        "bounds": {
            "scalar_hessian_entry_upper_bound": 64,
            "square_jacobian_lipschitz_inf_coefficient": 9216,
            "rate_positivity_if_parameter_inf_radius_lt": "1/4",
            "coordinate_scope": "raw physical strict-lower endpoint entries",
        },
    }


def main():
    certificates = []
    for rates in [(1, 10, 3, 8), (3, 8, 1, 10)]:
        result = fixed_hazard_jacobian(rates)
        assert result["pivots"] == list(range(12))
        certificates.append(serializable_certificate(result))
    (HERE / "fixed_hazard_jacobian.json").write_text(json.dumps({
        "status": "PASS_EXACT_FIXED_HAZARD_RAW_ENDPOINT_RANK12",
        "certificates": certificates,
        "no_optimizer_or_physical_data": True,
    }, indent=2) + "\n")
    print("PASS: fixed-total-hazard raw endpoint Jacobians rank12, same first12 columns, exact inverse norms saved.")


if __name__ == "__main__":
    main()
