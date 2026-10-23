"""Exact rational audit of the coefficients in the 1D Poisson/Laplace proof.

No Fokker--Planck discretization or time integration.  The rational vectors
are limiting well masses in the order (well 1, well 2, well 0 lifted to 3).
"""

import json
from fractions import Fraction as F


def mv(a, x):
    return [sum(v * y for v, y in zip(row, x)) for row in a]


def solve(a, b):
    aug = [list(row) + [val] for row, val in zip(a, b)]
    for j in range(len(b)):
        p = next(i for i in range(j, len(b)) if aug[i][j])
        aug[j], aug[p] = aug[p], aug[j]
        den = aug[j][j]
        aug[j] = [v / den for v in aug[j]]
        for i in range(len(b)):
            if i != j:
                v = aug[i][j]
                aug[i] = [x - v * y for x, y in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def main():
    # exp(-w_i), exp(w_s), f_i, f_s, and the lift monodromy.
    lam = [F(25, 4), F(15, 8), F(3, 64)]
    edge = [F(1), F(160), F(1600, 3)]
    f = [F(0), F(0), F(1)]
    fs = [F(1, 2), F(0), F(1, 2)]
    c = F(64, 3)
    ledge = [-v * ff for v, ff in zip(edge, fs)]
    bp = sum(edge)
    bprime = sum(ledge)
    prefix = [sum(edge[:i + 1]) for i in range(3)]
    prefixprime = [sum(ledge[:i + 1]) for i in range(3)]
    v = [lam[i] * (bp / (c - 1) + prefix[i]) for i in range(3)]
    vp = [f[i] * v[i] + lam[i] * (bprime / (c - 1) + prefixprime[i])
          for i in range(3)]
    pi = [vi / sum(v) for vi in v]
    r = [(vp[i] - pi[i] * sum(vp)) / sum(v) for i in range(3)]
    assert pi == [F(13400, 37803), F(22320, 37803), F(2083, 37803)]
    assert sum(r) == 0

    # Current-oriented generator in this cyclic well order.
    q = [[F(0)] * 3 for _ in range(3)]
    for i in (0, 1):
        ee = edge[i + 1]  # saddle between well i and i+1
        q[i + 1][i] = 1 / (lam[i] * ee)
        q[i][i + 1] = 1 / (lam[i + 1] * ee)
    q[0][2] = 1 / (c * lam[2] * edge[0])
    q[2][0] = 1 / (lam[0] * edge[0])
    for j in range(3):
        q[j][j] = -sum(q[i][j] for i in range(3) if i != j)
    expected = [[F(v, 3000) for v in row] for row in
                [[-483, 10, 3000], [3, -13, 120], [480, 3, -3120]]]
    assert q == expected
    assert mv(q, pi) == [0, 0, 0]

    # Exact derivative of the geometric column generator, including its
    # diagonal.  This checks that stationary differentiation has the right
    # sign and that the limiting perturbation is the intended kinetic one.
    qp = [[(f[i] - f[j]) * q[i][j] / 2 if i != j else F(0)
           for j in range(3)] for i in range(3)]
    for j in range(3):
        qp[j][j] = -sum(qp[i][j] for i in range(3) if i != j)
    forcing = mv(qp, pi)
    assert mv(q, r) == [-b for b in forcing]

    # R at the three saddles in [1/4,13/4], then the leading well masses
    # of kappa*U_R from the continuum integrating-factor formula.
    rs = [F(0), r[0], r[0] + r[1]]
    br = sum(e * rr for e, rr in zip(edge, rs))
    t = [lam[i] * (br / (c - 1)
                   + sum(edge[j] * rs[j] for j in range(i + 1)))
         for i in range(3)]
    u = [t[i] - pi[i] * sum(t) for i in range(3)]
    assert sum(u) == 0 and mv(q, u) == r
    independently_solved = solve([q[0], q[1], [F(1)] * 3],
                                 [r[0], r[1], F(0)])
    assert u == independently_solved
    zeta = -sum(ff * ui for ff, ui in zip(f, u))
    assert zeta == -F(29239948720000, 54023012580627) < 0
    print(json.dumps({
        "scope": "exact limiting coefficients; no finite-H numerical sign",
        "pi_well_order_1_2_0": [str(x) for x in pi],
        "stationary_h_derivative": [str(x) for x in r],
        "rescaled_Poisson_masses": [str(x) for x in u],
        "limiting_kappa_zeta": str(zeta),
        "limiting_kappa_zeta_float": float(zeta),
        "checks": ["node generator", "stationary derivative",
                   "Poisson current coefficients", "negative friction"],
    }, indent=2))


if __name__ == "__main__":
    main()
