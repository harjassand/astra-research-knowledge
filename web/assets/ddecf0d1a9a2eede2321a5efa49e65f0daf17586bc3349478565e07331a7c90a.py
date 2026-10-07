"""Exact checks for the XXZ boundary portion of the gadget no-go.

The closure lemma is proved in lorentzian_gadget_closure.md and is not
verified by this finite script. This script checks the displayed Hessian
eigenvalue formulas, including invariance under a scalar identity shift.
"""
from fractions import Fraction as F


def matvec(M, v):
    return [sum((M[i][j] * v[j] for j in range(len(v))), F(0))
            for i in range(len(M))]


def main():
    cases = [
        # (alpha, gamma, s, kappa), above the upper boundary
        (F(1), F(11, 10), F(1, 10), F(0)),
        (F(1), F(11, 10), F(1, 10), F(10)),
        (F(3, 2), F(2), F(1, 7), F(4)),
        # below the lower boundary
        (F(1), F(-11, 10), F(1, 10), F(0)),
        (F(1), F(-11, 10), F(1, 10), F(10)),
        (F(3, 2), F(-2), F(1, 7), F(4)),
    ]
    rows = []
    for alpha, gamma, s, kappa in cases:
        a = 1 + s * (kappa + gamma)
        b = 1 + s * (kappa - gamma)
        c = 2 * s * alpha
        # Hessian of q in variable order x1,x2,x3,x4.
        H = [[F(0) for _ in range(4)] for _ in range(4)]
        for coeff, i, j in [
            (a, 0, 1), (a, 2, 3), (b, 0, 3),
            (b, 1, 2), (c, 0, 2), (c, 1, 3),
        ]:
            H[i][j] = H[j][i] = coeff
        candidates = [
            ((1, 1, 1, 1), a + b + c),
            ((1, 1, -1, -1), a - b - c),
            ((1, -1, 1, -1), -a - b + c),
            ((1, -1, -1, 1), -a + b - c),
        ]
        eigenchecks = []
        for v, lam in candidates:
            v = [F(x) for x in v]
            assert matvec(H, v) == [lam * x for x in v]
            eigenchecks.append(lam)
        if gamma > alpha:
            assert eigenchecks[1] == 2 * s * (gamma - alpha) > 0
            assert a + b + c > 0
            assert a > 0 and b > 0 and c >= 0
            side = "gamma>alpha"
        else:
            assert gamma < -alpha
            assert eigenchecks[3] == -2 * s * (gamma + alpha) > 0
            assert a + b + c > 0
            assert a > 0 and b > 0 and c >= 0
            side = "gamma<-alpha"
        rows.append((side, alpha, gamma, s, kappa, eigenchecks))

    print("PASS: 6 rational shifted/outside-cone Hessian cases")
    for side, alpha, gamma, s, kappa, eigs in rows:
        print(side, "alpha=", alpha, "gamma=", gamma, "s=", s,
              "kappa=", kappa, "eigenvalues=", eigs)
    print("Finite arithmetic only; the all-parameter identities are derived in the report.")


if __name__ == "__main__":
    main()
