"""Independent small exact checks for c07_s02's stopped-diffusion formulas.

These fixtures check algebraic transcription only. They do not prove the
all-N stochastic argument, its tail constants, or the separability theorem.
Requires SymPy 1.14 for exact symbolic differentiation and rational matrices.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json
import sympy as sp


ROOT = Path(__file__).resolve().parent
I = sp.I
SIGMA = [sp.Matrix([[0, 1], [1, 0]]),
         sp.Matrix([[0, -I], [I, 0]]),
         sp.Matrix([[1, 0], [0, -1]])]
M = sp.symbols("m0:3", real=True)


def kron_all(mats):
    out = mats[0]
    for a in mats[1:]:
        out = sp.kronecker_product(out, a)
    return out


def collective(N):
    Js = []
    for a in range(3):
        total = sp.zeros(2**N)
        for site in range(N):
            factors = [sp.eye(2) for _ in range(N)]
            factors[site] = SIGMA[a] / 2
            total += kron_all(factors)
        Js.append(total)
    return Js


def kernel(N):
    rho = sp.Matrix([[1 + M[2], M[0] - I*M[1]],
                     [M[0] + I*M[1], 1 - M[2]]]) / 2
    return kron_all([rho] * N)


def deriv(F, coeffs):
    return sum((coeffs[i] * F.diff(M[i]) for i in range(3)), sp.zeros(*F.shape))


def Bop(F, n, N):
    u = sum(n[i] * M[i] for i in range(3))
    v = [n[i] - u*M[i] for i in range(3)]
    return N*u*F + deriv(F, v)


def Rop(F, n):
    mvec, nvec = sp.Matrix(M), sp.Matrix(n)
    r = nvec.cross(mvec)
    return deriv(F, list(r))


def sub_matrix(F, point):
    return F.subs(dict(zip(M, point))).applyfunc(sp.simplify)


def s2_fixtures():
    axes = [sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]),
            sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0]),
            sp.Matrix([sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(1, 3)])]
    points = [sp.Matrix([sp.Rational(1, 5), -sp.Rational(1, 7), sp.Rational(1, 4)]),
              sp.Matrix([sp.Rational(3, 5), 0, sp.Rational(3, 5)])]
    rows = []
    for N in (1, 2, 3):
        k = kernel(N)
        Js = collective(N)
        for n in axes:
            assert sp.simplify(sum(x*x for x in n)-1) == 0
            F = sum((n[i]*Js[i] for i in range(3)), sp.zeros(2**N))
            lhs_symbolic = (Bop(Bop(k, n, N), n, N)-Rop(Rop(k, n), n))/4
            rhs_symbolic = (F*F*k+k*F*F)/2
            difference = lhs_symbolic-rhs_symbolic
            for point in points:
                evaluated = sub_matrix(difference, point)
                assert evaluated == sp.zeros(2**N)
                rows.append({"N": N, "axis": [str(x) for x in n],
                             "m": [str(x) for x in point], "exact_zero": True})
    return rows


def s4_fixtures():
    # Fixed diagonal positive C and arbitrary rational field. The identity is
    # algebraic in s>0, so a rational s is used to keep every check exact.
    Cdiag = [sp.Rational(1), sp.Rational(5, 4), sp.Rational(3, 2)]
    b = sp.Matrix([sp.Rational(1, 7), -sp.Rational(2, 9), sp.Rational(1, 11)])
    R = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5), 0],
                    [sp.Rational(4, 5), sp.Rational(3, 5), 0],
                    [0, 0, 1]])
    assert R.T*R == sp.eye(3)
    models = [("diagonal", sp.diag(*Cdiag), [sp.eye(3)[:, i] for i in range(3)]),
              ("rotated", R*sp.diag(*Cdiag)*R.T, [R[:, i] for i in range(3)])]
    points = [sp.Matrix([sp.Rational(1, 5), -sp.Rational(1, 7), sp.Rational(1, 4)]),
              sp.Matrix([sp.Rational(3, 5), 0, sp.Rational(3, 5)])]
    rows = []
    for model_name, C, axes in models:
        for N in (1, 2, 3):
            s = sp.Rational(2)
            k = kernel(N)
            Js = collective(N)
            H = sp.zeros(2**N)
            for i, n in enumerate(axes):
                Fi = sum((n[j]*Js[j] for j in range(3)), sp.zeros(2**N))
                H += Cdiag[i] * Fi * Fi / s**2
            H += sum((b[i] * Js[i] for i in range(3)), sp.zeros(2**N)) / s
            lhs = (H*k+k*H)/2
            P = sp.eye(3)-sp.Matrix(M)*sp.Matrix(M).T
            D = P*C*P
            cross = sp.Matrix([[0, -M[2], M[1]],
                               [M[2], 0, -M[0]],
                               [-M[1], M[0], 0]])
            D -= cross*C*cross.T
            a = sp.zeros(3, 1)
            for i, n in enumerate(axes):
                u = sum(n[j]*M[j] for j in range(3))
                v = n-u*sp.Matrix(M)
                r = n.cross(sp.Matrix(M))
                dv_v = v.jacobian(M)*v
                dr_r = r.jacobian(M)*r
                a += Cdiag[i]*(2*N*u*v+dv_v-dr_r)/(4*s**2)
            bvec = sp.Matrix(b)
            a += (bvec-(bvec.dot(sp.Matrix(M)))*sp.Matrix(M))/(2*s)
            trC = sum(Cdiag)
            mvec = sp.Matrix(M)
            V = (N**2*(mvec.dot(C*mvec))+N*(trC-mvec.dot(C*mvec)))/(4*s**2)
            V += N*bvec.dot(mvec)/(2*s)
            rhs = V*k + deriv(k, list(a))
            for i in range(3):
                for j in range(3):
                    rhs += D[i, j]*k.diff(M[i], M[j])/(4*s**2)
            diff = lhs-rhs
            for point in points:
                assert sub_matrix(diff, point) == sp.zeros(2**N)
                rows.append({"orientation": model_name, "N": N,
                             "C_eigenvalues": [str(x) for x in Cdiag],
                             "b": [str(x) for x in b], "s": str(s),
                             "m": [str(x) for x in point], "exact_zero": True})
    return rows


def s5_and_global_fixture():
    # C>=I with ||C||=3. The report's explicit ball radius is 1/8.
    C = sp.diag(1, 2, 3)
    Lc = sp.Integer(3)
    r0sq = sp.Rational(1, 64)
    m = sp.Matrix([sp.Rational(1, 8), 0, 0])
    z = sp.Matrix([1, sp.Rational(2, 3), -sp.Rational(1, 3)])
    P = sp.eye(3)-m*m.T
    cross = sp.Matrix([[0, -m[2], m[1]],
                       [m[2], 0, -m[0]],
                       [-m[1], m[0], 0]])
    D = P*C*P-cross*C*cross.T
    lhs = sp.factor((z.T*D*z)[0])
    rhs = sp.factor(((1-(m.dot(m)))**2-Lc*m.dot(m))*(z.dot(z)))
    lower_coefficient = (1-(m.dot(m)))**2-Lc*m.dot(m)
    assert lhs >= rhs and rhs > 0
    def psd3(A):
        return (all(A[i, i] >= 0 for i in range(3))
                and all(A[i, i]*A[j, j]-A[i, j]*A[j, i] >= 0
                        for i, j in ((0, 1), (0, 2), (1, 2)))
                and A.det() >= 0)
    assert psd3(D-lower_coefficient*sp.eye(3))
    assert psd3(Lc*sp.eye(3)-D)

    # At the sphere boundary, anisotropy makes the same matrix indefinite.
    mb = sp.Matrix([0, 0, 1])
    Pb = sp.eye(3)-mb*mb.T
    cb = sp.Matrix([[0, -mb[2], mb[1]],
                     [mb[2], 0, -mb[0]],
                     [-mb[1], mb[0], 0]])
    Db = Pb*C*Pb-cb*C*cb.T
    assert Db == sp.diag(-1, 1, 0)
    return {
        "inside_ball": {"r0_squared": str(r0sq), "lhs_zDz": str(lhs),
                        "claimed_lower_rhs": str(rhs), "lower_coefficient": str(lower_coefficient),
                        "matrix_lower_and_upper_psd_checks": "exact principal minors >=0",
                        "inequality_holds_exactly": True},
        "outside_ball_counterexample": {"C": [[str(C[i, j]) for j in range(3)] for i in range(3)],
                                        "m": ["0", "0", "1"],
                                        "D_C": [[str(Db[i, j]) for j in range(3)] for i in range(3)],
                                        "eigenvalue_sign_witnesses": {"e1": "-1", "e2": "1"}},
    }


def main():
    data = {
        "scope": "Independent exact rational fixtures for S2, S4 and S5; not an all-N proof.",
        "S2_identity_checks": s2_fixtures(),
        "S4_generator_checks": s4_fixtures(),
        "S5_psd_and_global_failure": s5_and_global_fixture(),
        "totals": {"S2": 30, "S4": 12},
        "limitations": ["Point/axis checks do not establish symbolic identities for every m,n,N.",
                        "They do not prove S7-S12, Brownian stopping tails, or the exponential theorem.",
                        "The exact boundary fixture confirms that a global positive diffusion claim would be false."],
    }
    path = ROOT / "STOPPED_DIFFUSION_EXACT.json"
    path.write_text(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
