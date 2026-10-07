"""Independent exact low-N checks for the critical-spin Bloch generator.

These checks supplement (and do not replace) the symbolic derivation in the
accompanying audit note.
"""
import json
from pathlib import Path

import sympy as sp


COORDS = sp.symbols("x y z")
X, Y, Z = COORDS
I2 = sp.eye(2)
PAULI = (
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[0, -sp.I], [sp.I, 0]]),
    sp.Matrix([[1, 0], [0, -1]]),
)


def kron_all(items):
    out = items[0]
    for item in items[1:]:
        out = sp.kronecker_product(out, item)
    return out


def matrix_derivative(a, variable):
    return a.applyfunc(lambda entry: sp.diff(entry, variable))


def bloch_kernel(n):
    tau = (I2 + sum((COORDS[i] * PAULI[i] for i in range(3)), sp.zeros(2))) / 2
    return kron_all([tau] * n)


def collective_spin(axis, n):
    one_site = sum((axis[i] * PAULI[i] for i in range(3)), sp.zeros(2))
    out = sp.zeros(2**n)
    for site in range(n):
        factors = [I2] * n
        factors[site] = one_site
        out += kron_all(factors) / 2
    return out


def B_apply(expr, axis, n):
    u = sum(axis[i] * COORDS[i] for i in range(3))
    v = [axis[i] - u * COORDS[i] for i in range(3)]
    return n * u * expr + sum(
        (v[i] * matrix_derivative(expr, COORDS[i]) for i in range(3)),
        sp.zeros(expr.rows, expr.cols),
    )


def R_apply(expr, axis):
    r = (
        axis[1] * Z - axis[2] * Y,
        axis[2] * X - axis[0] * Z,
        axis[0] * Y - axis[1] * X,
    )
    return sum(
        (r[i] * matrix_derivative(expr, COORDS[i]) for i in range(3)),
        sp.zeros(expr.rows, expr.cols),
    )


def check_s2(n, axis):
    k = bloch_kernel(n)
    F = collective_spin(axis, n)
    lhs = (F * F * k + k * F * F) / 2
    rhs = (B_apply(B_apply(k, axis, n), axis, n)
           - R_apply(R_apply(k, axis), axis)) / 4
    return all(sp.expand(v) == 0 for v in lhs - rhs)


def check_scalar_s4():
    f = sp.Function("f")(*COORDS)
    axes = (sp.Rational(3, 5), sp.Rational(4, 5), sp.Integer(0))
    n = sp.symbols("N", integer=True, positive=True)
    u = sum(axes[i] * COORDS[i] for i in range(3))
    v = tuple(axes[i] - u * COORDS[i] for i in range(3))
    r = (
        axes[1] * Z - axes[2] * Y,
        axes[2] * X - axes[0] * Z,
        axes[0] * Y - axes[1] * X,
    )

    def B(expr):
        return n * u * expr + sum(v[i] * sp.diff(expr, COORDS[i]) for i in range(3))

    def R(expr):
        return sum(r[i] * sp.diff(expr, COORDS[i]) for i in range(3))

    scalar = n**2 * u**2 + n * (1 - u**2)
    drift = []
    diffusion = sp.zeros(3)
    for i in range(3):
        drift.append(
            2 * n * u * v[i]
            + sum(v[j] * sp.diff(v[i], COORDS[j]) for j in range(3))
            - sum(r[j] * sp.diff(r[i], COORDS[j]) for j in range(3))
        )
        for j in range(3):
            diffusion[i, j] = v[i] * v[j] - r[i] * r[j]
    rhs = scalar * f
    rhs += sum(drift[i] * sp.diff(f, COORDS[i]) for i in range(3))
    rhs += sum(diffusion[i, j] * sp.diff(f, COORDS[i], COORDS[j])
               for i in range(3) for j in range(3))
    return sp.simplify(sp.expand(B(B(f)) - R(R(f)) - rhs)) == 0


def check_psd_fixture():
    # Exact rational point inside the certified ball for C=diag(1,2,4).
    C = sp.diag(1, 2, 4)
    m = sp.Matrix([sp.Rational(1, 10), sp.Rational(1, 20), -sp.Rational(1, 15)])
    P = sp.eye(3) - m * m.T
    cross = sp.Matrix([[0, -m[2], m[1]], [m[2], 0, -m[0]], [-m[1], m[0], 0]])
    D = sp.simplify(P * C * P - cross * C * cross.T)
    minors = [
        sp.factor(D[:1, :1].det()),
        sp.factor(D[:2, :2].det()),
        sp.factor(D.det()),
    ]
    # Positive leading principal minors prove this one symmetric fixture PD.
    return all(value > 0 for value in minors), [str(value) for value in minors], str(D)


def main():
    axes = [
        (sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        (sp.Integer(0), sp.Integer(0), sp.Integer(1)),
        (sp.Rational(3, 5), sp.Rational(4, 5), sp.Integer(0)),
    ]
    s2 = {
        f"N={n},axis={axis}": check_s2(n, axis)
        for n in (1, 2, 3)
        for axis in axes
    }
    psd_ok, minors, D = check_psd_fixture()
    out = {
        "status": "exact finite algebra diagnostics only; proof is in revisions/STOPPED_DIFFUSION_AUDIT.txt",
        "S2_checks": s2,
        "S4_symbolic_scalar_identity": check_scalar_s4(),
        "PSD_fixture_C_diag_1_2_4": {
            "positive_principal_minors": psd_ok,
            "minors": minors,
            "D": D,
        },
    }
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "S2_passes": sum(s2.values()),
        "S2_total": len(s2),
        "S4_pass": out["S4_symbolic_scalar_identity"],
        "PSD_fixture_pass": psd_ok,
        "path": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
