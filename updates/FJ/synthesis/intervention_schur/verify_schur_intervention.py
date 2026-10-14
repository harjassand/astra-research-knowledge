#!/usr/bin/env python3
"""Exact checks for the shunt-intervention Schur theorem.

Uses only SymPy exact rational/algebraic arithmetic. These checks validate the
displayed identities and counterexamples, not experimental assumptions.
"""
from sympy import Matrix, Rational, Symbol, eye, simplify, sqrt, zeros


def response(K, C, A, u, t):
    return simplify(K - C * (A + t * u * u.T).inv() * C.T)


def frobenius_norm_sq(M):
    return simplify(sum(x * x for x in M))


def main():
    # A passive but nonreciprocal 3-hydraulic/2-electrical model. The wet block
    # is PSD by its unit Schur complement; the dry network is a lossless skew
    # two-port, so sym(Y)=0 and sym(A)=I.
    G = eye(2)
    Y = Matrix([[0, Rational(1, 3)], [-Rational(1, 3), 0]])
    A = G + Y
    assert simplify((Y + Y.T) / 2) == zeros(2, 2)
    assert simplify((A + A.T) / 2) == eye(2)
    C = Matrix([[1, 0], [0, 1], [1, 1]])
    K = C * C.T + eye(3)
    assert simplify(K - C * G.inv() * C.T) == eye(3)
    u = Matrix([1, 0])
    q = simplify((u.T * A.inv() * u)[0])
    v = simplify(C * A.inv() * u)
    w = simplify(C * A.T.inv() * u)
    F = simplify(v * w.T)
    assert q > 0
    assert F.rank() == 1

    H0 = response(K, C, A, u, Rational(0))
    t1, t2, t3 = Rational(1, 3), Rational(1), Rational(2)
    H1 = response(K, C, A, u, t1)
    H2 = response(K, C, A, u, t2)
    H3 = response(K, C, A, u, t3)
    d1, d2, d3 = H1 - H0, H2 - H0, H3 - H0
    for t, dH in [(t1, d1), (t2, d2), (t3, d3)]:
        assert simplify(dH - (t / (1 + t * q)) * F) == zeros(3, 3)
        assert dH.rank() == 1

    # Frobenius norm ratio is exact because each response is a positive scalar
    # multiple of the same exact rational outer product.
    r = simplify(sqrt(frobenius_norm_sq(d1)) / sqrt(frobenius_norm_sq(d2)))
    q_recovered = simplify((r * t2 - t1) / (t1 * t2 * (1 - r)))
    F_recovered = simplify((1 / t1 + q_recovered) * d1)
    assert simplify(q_recovered - q) == 0
    assert simplify(F_recovered - F) == zeros(3, 3)
    assert simplify(d3 - (t3 * (1 + t1 * q) / (t1 * (1 + t3 * q))) * d1) == zeros(3, 3)

    # Rank-r Woodbury extension with U=I on this same exact model.
    U = eye(2)
    Q_U = simplify(U.T * A.inv() * U)
    V_U = simplify(C * A.inv() * U)
    W_U = simplify(U.T * A.inv() * C.T)
    dU = simplify(K - C * (A + t2 * U * U.T).inv() * C.T - H0)
    woodbury_U = simplify(t2 * V_U * (eye(2) + t2 * Q_U).inv() * W_U)
    assert simplify(dU - woodbury_U) == zeros(3, 3)

    # Explicit strictly passive scalar pair: same baseline and same t=1
    # response, different q,F; t=2 separates them.
    models = [
        (Rational(2), Rational(1), Rational(1)),
        (Rational(5, 3), sqrt(2) / 3, Rational(1, 3)),
    ]
    scalar_data = []
    for Ks, Cs, Gs in models:
        assert simplify(Ks * Gs - Cs**2) > 0
        Hs0 = simplify(Ks - Cs**2 / Gs)
        qs = simplify(1 / Gs)
        Fs = simplify((Cs / Gs) ** 2)
        d_at_1 = simplify(Fs / (1 + qs))
        d_at_2 = simplify(2 * Fs / (1 + 2 * qs))
        scalar_data.append((Hs0, d_at_1, d_at_2, qs, Fs))
    assert scalar_data[0][0] == scalar_data[1][0] == 1
    assert scalar_data[0][1] == scalar_data[1][1] == Rational(1, 2)
    assert scalar_data[0][2] == Rational(2, 3)
    assert scalar_data[1][2] == Rational(4, 7)
    assert scalar_data[0][3:] == (1, 1)
    assert scalar_data[1][3:] == (3, 2)

    # Passive direct-effect confound: a load-dependent K(t) with no coupling
    # reproduces the same fractional response curve as an electrical path.
    q_conf = Rational(2, 3)
    F_conf = Matrix([[2]])
    K0_conf = Matrix([[1]])
    C_conf = zeros(1, 1)
    for t in [Rational(1, 5), Rational(1), Rational(3)]:
        Kt_conf = K0_conf + t / (1 + t * q_conf) * F_conf
        assert Kt_conf[0, 0] > 0
        H_conf = Kt_conf - C_conf * eye(1) * C_conf.T
        assert simplify(H_conf - (K0_conf + t / (1 + t * q_conf) * F_conf)) == zeros(1, 1)

    # Exact weak-coupling family: baseline response is identical to the null,
    # while one fixed shunt produces an O(epsilon^2) mean difference.
    eps = Symbol("eps", positive=True)
    Pvar = Symbol("P", positive=True)
    sigma = Symbol("sigma_Q", positive=True)
    t_fixed = Rational(2)
    K_eps = Matrix([[1 + eps**2]])
    C_eps = Matrix([[eps]])
    G_eps = eye(1)
    A_eps = G_eps
    u_eps = Matrix([1])
    K_null = eye(1)
    C_null = zeros(1, 1)
    H_eps_0 = response(K_eps, C_eps, A_eps, u_eps, Rational(0))
    H_null_0 = response(K_null, C_null, A_eps, u_eps, Rational(0))
    H_eps_t = response(K_eps, C_eps, A_eps, u_eps, t_fixed)
    H_null_t = response(K_null, C_null, A_eps, u_eps, t_fixed)
    delta_eps = simplify(H_eps_t[0, 0] - H_null_t[0, 0])
    assert H_eps_0 == H_null_0 == eye(1)
    assert simplify(K_eps - C_eps * G_eps.inv() * C_eps.T) == eye(1)
    assert simplify(delta_eps - eps**2 * t_fixed / (1 + t_fixed)) == 0
    kl_one = simplify((Pvar * delta_eps) ** 2 / (2 * sigma**2))
    assert simplify(kl_one - Pvar**2 * eps**4 * (t_fixed / (1 + t_fixed))**2 / (2 * sigma**2)) == 0

    # Exact cancellation: a passive nonreciprocal electrical element and one
    # nonzero dual visibility factor can still yield no port response.
    Gv = eye(2)
    Yv = Matrix([[0, 1], [-1, 0]])
    Av = Gv + Yv
    assert simplify((Yv + Yv.T) / 2) == zeros(2, 2)
    assert simplify((Av + Av.T) / 2) == eye(2)
    Cv = Matrix([[-1, 1]])
    Kv = Matrix([[2]])
    uv = Matrix([1, 0])
    qv = simplify((uv.T * Av.inv() * uv)[0])
    vv = simplify(Cv * Av.inv() * uv)
    wv = simplify(Cv * Av.T.inv() * uv)
    assert qv == Rational(1, 2) and vv == Matrix([[0]]) and wv == Matrix([[-1]])
    assert simplify(Kv - Cv * Gv.inv() * Cv.T) == zeros(1, 1)
    Hbase_v = response(Kv, Cv, Av, uv, Rational(0))
    for t in [Rational(1, 7), Rational(1), Rational(5)]:
        assert response(Kv, Cv, Av, uv, t) == Hbase_v

    # Visible differential nonreciprocity: the shunt changes the skew part of
    # hydraulic H even though K is symmetric and the wet block is reciprocal.
    Gn = eye(2)
    Yn = Matrix([[0, 1], [-1, 0]])
    An = Gn + Yn
    assert simplify((Yn + Yn.T) / 2) == zeros(2, 2)
    assert simplify((An + An.T) / 2) == eye(2)
    Cn = eye(2)
    Kn = 2 * eye(2)
    un = Matrix([1, 0])
    Hn0 = response(Kn, Cn, An, un, Rational(0))
    Hn1 = response(Kn, Cn, An, un, Rational(1))
    dn = Hn1 - Hn0
    vn = simplify(Cn * An.inv() * un)
    wn = simplify(Cn * An.T.inv() * un)
    fn = simplify(vn * wn.T)
    assert simplify(dn - Rational(2, 3) * fn) == zeros(2, 2)
    assert simplify(dn[1, 0] - dn[0, 1]) == Rational(1, 3)
    assert simplify(Kn - Cn * Gn.inv() * Cn.T) == eye(2)

    # Sensitivity check: high q under two overlarge loads is dramatically
    # worse conditioned than q~1 with the same t1,t2.
    def dr_dq(qval, a, b):
        return simplify(a * (b - a) / (b * (1 + a * qval) ** 2))

    sens_q1 = simplify(1 / dr_dq(Rational(1), Rational(1), Rational(2)))
    sens_q100 = simplify(1 / dr_dq(Rational(100), Rational(1), Rational(2)))
    assert sens_q1 == 8
    assert sens_q100 == 20402

    print("PASS: passive nonsymmetric A gives exact rank-one differential Schur response")
    print(f"PASS: two positive shunt strengths recover q={q} and the exact outer-product F")
    print("PASS: the held-out third shunt matches its predicted scale and matrix shape")
    print("PASS: full-rank shunt subspace satisfies the exact Woodbury quotient formula")
    print("PASS: strictly passive scalar models agree at baseline and t=1, then separate at t=2")
    print("PASS: a strictly passive direct shunt effect can counterfeit the fractional curve with C=0")
    print("PASS: weak-coupling passive pair has identical baseline and exact O(eps^2) shunt signal")
    print("PASS: one-sided hidden visibility can cancel exactly under a passive nonreciprocal A")
    print("PASS: a symmetric wet block plus passive nonreciprocal network gives a visible skew update")
    print(f"PASS: inverse-ratio sensitivity is {sens_q1} at q=1 and {sens_q100} at q=100 (t1=1,t2=2)")
    print("SCOPE: exact algebraic examples only; no apparatus, sensor, material, or novelty validation")


if __name__ == "__main__":
    main()
