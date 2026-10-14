"""Exact-rational checks for the hydroelectronic/Hall source claims.

Only this assigned directory is written.  The script uses Fraction arithmetic
for every matrix value and prints deterministic exact outputs.
"""
from fractions import Fraction as F
from itertools import product


def transpose(A):
    return [list(row) for row in zip(*A)]


def matmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def inverse(A):
    n = len(A)
    aug = [list(A[i]) + [F(i == j) for j in range(n)] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        q = aug[j][j]
        aug[j] = [x / q for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                q = aug[i][j]
                aug[i] = [aug[i][k] - q * aug[j][k] for k in range(2 * n)]
    return [row[n:] for row in aug]


def rank(A):
    A = [row[:] for row in A]
    m, n = len(A), len(A[0])
    r = 0
    for j in range(n):
        pivot = next((i for i in range(r, m) if A[i][j]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        q = A[r][j]
        A[r] = [x / q for x in A[r]]
        for i in range(m):
            if i != r and A[i][j]:
                q = A[i][j]
                A[i] = [A[i][k] - q * A[r][k] for k in range(n)]
        r += 1
        if r == m:
            break
    return r


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]


def sym(A):
    return [[(A[i][j] + A[j][i]) / 2 for j in range(len(A))]
            for i in range(len(A))]


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def chiral_Y(gp, gm):
    return [[gp + gm, -gm], [-gp, gp + gm]]


def H_matrix(K, C, G, Y):
    A = [[G[i][j] + Y[i][j] for j in range(len(G))]
         for i in range(len(G))]
    return sub(K, matmul(matmul(C, inverse(A)), C))


def eta_factor(chi, t):
    return chi * t / ((1 + t) * (1 + t - chi))


def eta_c(chi):
    # Rational whenever 1-chi is a rational square.
    value = 1 - chi
    sn, sd = int(value.numerator ** 0.5), int(value.denominator ** 0.5)
    assert sn * sn == value.numerator and sd * sd == value.denominator
    s = F(sn, sd)
    return (1 - s) / (1 + s)


def show(name, x):
    print(f"{name}={x}")


def equality_case():
    # K=G=1, C=4/5 gives chi=16/25; t=g/G=3/5 is its
    # exact matching value sqrt(1-chi).
    K = [[F(1), F(0)], [F(0), F(1)]]
    C = [[F(4, 5), F(0)], [F(0), F(4, 5)]]
    G = [[F(1), F(0)], [F(0), F(1)]]
    Y = chiral_Y(F(3, 5), F(0))
    H = H_matrix(K, C, G, Y)
    show("equal_H", H)
    kappa = H[0][0]
    b = H[1][0]
    eta_load = b * b / (4 * kappa * H[1][1])
    show("equal_eta_load_max", eta_load)
    show("equal_source_bound", F(1, 4) * eta_c(F(16, 25)) ** 2)
    show("equal_eta_factors", eta_factor(F(16, 25), F(3, 5)))


def heterogeneous_case():
    # chi_1=16/25, chi_2=9/25, G_1=G_2=1.  The independent
    # electrical matching points are 3/5 and 4/5, so no single g
    # attains both.  The point g=7/10 is an exact rational witness.
    chis = [F(16, 25), F(9, 25)]
    t = F(7, 10)
    eta_exact = F(1, 4) * eta_factor(chis[0], t) * eta_factor(chis[1], t)
    separate_sup = F(1, 4) * eta_c(chis[0]) * eta_c(chis[1])
    show("heterogeneous_t", t)
    show("heterogeneous_eta_at_t", eta_exact)
    show("heterogeneous_separate_optimum_bound", separate_sup)
    show("heterogeneous_strict_gap", separate_sup - eta_exact)
    show("heterogeneous_individual_matching_t", [F(3, 5), F(4, 5)])


def exact_network_checks():
    K = [[F(1), F(0)], [F(0), F(1)]]
    C = [[F(1, 2), F(0)], [F(0), F(1, 3)]]
    G = [[F(1), F(0)], [F(0), F(1)]]
    Y = chiral_Y(F(2), F(1))
    H = H_matrix(K, C, G, Y)
    skewY = sub(Y, transpose(Y))
    skewH = sub(H, transpose(H))
    A = [[G[i][j] + Y[i][j] for j in range(2)] for i in range(2)]
    rhs = matmul(matmul(matmul(matmul(C, inverse(transpose(A))), skewY),
                        inverse(A)), C)
    show("asymmetric_Y", Y)
    show("asymmetric_H", H)
    show("skew_identity_residual", sub(skewH, rhs))
    show("rank_skewY", rank(skewY))
    show("rank_skewH", rank(skewH))
    show("offdiag_ratio_H21_H12", H[1][0] / H[0][1])
    symY, symH = sym(Y), sym(H)
    show("symY_leading_minor", symY[0][0])
    show("symY_determinant", symY[0][0] * symY[1][1] - symY[0][1] ** 2)
    show("symH_leading_minor", symH[0][0])
    show("symH_determinant", symH[0][0] * symH[1][1] - symH[0][1] ** 2)

    p = [F(1), F(2)]
    A = [[G[i][j] + Y[i][j] for j in range(2)] for i in range(2)]
    V = [-v for v in [sum((inverse(A)[i][j] * C[j][j] * p[j]
                           for j in range(2)), F(0)) for i in range(2)]]
    Q = [sum((H[i][j] * p[j] for j in range(2)), F(0)) for i in range(2)]
    I = [-v for v in [sum((Y[i][j] * V[j] for j in range(2)), F(0))
                      for i in range(2)]]
    wet_power = dot(p, Q) + dot(V, I)
    dry_power = dot(V, [sum((Y[i][j] * V[j] for j in range(2)), F(0))
                        for i in range(2)])
    show("power_balance_residual", dot(p, Q) - wet_power - dry_power)

    # Exact counterexample to extending rank equality when a wet coupling
    # vanishes: electrically nonreciprocal Y is unobservable hydraulically.
    C0 = [[F(0), F(0)], [F(0), F(1, 3)]]
    H0 = H_matrix(K, C0, G, Y)
    show("inactive_coupling_rank_skewY", rank(skewY))
    show("inactive_coupling_rank_skewH", rank(sub(H0, transpose(H0))))

    # Ideal chirality gives a strictly triangular effective hydraulic H.
    Cpos = [[F(1, 2), F(0)], [F(0), F(1, 3)]]
    Hideal = H_matrix(K, Cpos, G, chiral_Y(F(2), F(0)))
    show("ideal_chiral_H", Hideal)

    # Three active wet ports: rank preservation is genuinely multiport.
    K3 = [[F(2) if i == j else F(0) for j in range(3)] for i in range(3)]
    G3 = [[F(1) if i == j else F(0) for j in range(3)] for i in range(3)]
    C3 = [[F(1, 2), F(0), F(0)],
          [F(0), F(2, 3), F(0)],
          [F(0), F(0), F(3, 4)]]
    Y3 = [[F(2), F(-1), F(0)],
          [F(0), F(2), F(-1)],
          [F(-1), F(0), F(2)]]
    H3 = H_matrix(K3, C3, G3, Y3)
    show("three_port_rank_skewY", rank(sub(Y3, transpose(Y3))))
    show("three_port_rank_skewH", rank(sub(H3, transpose(H3))))


def multiport_load_case():
    # Exact load-matching theorem for a one-way-isolated source and two
    # receiver ports with a passive, nonreciprocal receiver submatrix D.
    # H is passive because Sym(H) is positive definite.
    h00 = F(3)
    b = [F(1), F(1, 2)]
    D = [[F(2), F(1, 2)], [F(-1, 2), F(2)]]
    S = [[F(2), F(0)], [F(0), F(2)]]
    x = [F(1, 4), F(1, 8)]
    y = [b[i] - sum((D[i][j] * x[j] for j in range(2)), F(0))
         for i in range(2)]
    xty = sum((x[i] * y[i] for i in range(2)), F(0))
    xnorm2 = sum((v * v for v in x), F(0))
    B = [[y[i] * y[j] / xty + (F(i == j) - x[i] * x[j] / xnorm2)
          for j in range(2)] for i in range(2)]
    Bx = [sum((B[i][j] * x[j] for j in range(2)), F(0)) for i in range(2)]
    load_power = sum((x[i] * Bx[i] for i in range(2)), F(0))
    s_inv_b_norm = sum((b[i] * b[i] / S[i][i] for i in range(2)), F(0))
    eta = load_power / h00
    eta_bound = s_inv_b_norm / (4 * h00)
    show("multiport_optimal_x", x)
    show("multiport_constructed_B", B)
    show("multiport_Bx_equals_b_minus_Dx", Bx == y)
    show("multiport_B_leading_minor", B[0][0])
    show("multiport_B_determinant", B[0][0] * B[1][1] - B[0][1] ** 2)
    show("multiport_load_power", load_power)
    show("multiport_eta", eta)
    show("multiport_bound", eta_bound)
    show("multiport_schur_slack", h00 - s_inv_b_norm / 4)


def ideal_gyrator_counterexample():
    # A passive lossless two-port gyrator is not a one-way isolator, but it
    # shows that the grounded-Hall 25% bound cannot be exported to every
    # passive electrical topology.  All values are exact rationals.
    c = F(19, 20)
    K = [[F(1), F(0)], [F(0), F(1)]]
    C = [[c, F(0)], [F(0), c]]
    G = [[F(1), F(0)], [F(0), F(1)]]
    g, R = F(1, 3), F(3)
    Y = [[F(0), g], [-g, F(0)]]
    H = H_matrix(K, C, G, Y)
    kappa, b = H[0][0], H[0][1]
    eta = b * b * R / ((1 + kappa * R) ** 2 *
                       (kappa + b * b * R / (1 + kappa * R)))
    show("gyrator_H", H)
    show("gyrator_symY", sym(Y))
    show("gyrator_eta", eta)
    show("gyrator_eta_gt_1_4", eta > F(1, 4))
    show("gyrator_one_way_test_H12_plus_H21", H[0][1] + H[1][0])


if __name__ == "__main__":
    equality_case()
    heterogeneous_case()
    exact_network_checks()
    multiport_load_case()
    ideal_gyrator_counterexample()
