#!/usr/bin/env python3
"""Exact checks for the separate cross-capital branching/factory delta.

Only Python's standard library is used. Logarithm ceilings are certified by
rational atanh-series intervals; the multitype tree cap is certified by exact
rational powers. This checks arithmetic and the finite examples, not the
general N722 theorem or finite-bit random-number implementations.
"""

from fractions import Fraction as Q
from math import factorial


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def ln_interval(x, terms=24):
    """Rational enclosure for ln(x), x>0, using range reduction and atanh."""
    x = Q(x)
    require(x > 0, "log input positive")
    k, y = 0, x
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1

    def reduced_log(q):
        z = (q - 1) / (q + 1)
        low = 2 * sum(
            (z ** (2 * j + 1)) / Q(2 * j + 1) for j in range(terms)
        )
        rem = Q(0) if z == 0 else (
            2 * z ** (2 * terms + 1)
            / (Q(2 * terms + 1) * (1 - z * z))
        )
        return low, low + rem

    log2_low, log2_high = reduced_log(Q(2))
    y_low, y_high = reduced_log(y)
    if k >= 0:
        return k * log2_low + y_low, k * log2_high + y_high
    return k * log2_high + y_low, k * log2_low + y_high


def e_interval(terms=30):
    """Rational enclosure for e; the omitted positive tail is <2/(N+1)! ."""
    low = sum((Q(1, factorial(j)) for j in range(terms + 1)), Q(0))
    return low, low + Q(2, factorial(terms + 1))


def ceil_cert(interval, expected, label):
    low, high = interval
    require(Q(expected - 1) < low, f"{label}: strict lower ceiling witness")
    require(high <= Q(expected), f"{label}: upper ceiling witness")
    return expected


def ceil_log_ratio_exact(a, z):
    """Return n with z**(n-1) < a <= z**n, using exact rationals."""
    a, z = Q(a), Q(z)
    require(a > 1 and z > 1, "log-ratio inputs exceed one")
    low, high = 0, 1
    while z ** high < a:
        low, high = high, 2 * high
    while high - low > 1:
        mid = (low + high) // 2
        if z ** mid < a:
            low = mid
        else:
            high = mid
    require(z ** low < a <= z ** high, "exact power bracket")
    return high, low


def mat_vec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), Q(0)) for row in matrix]


def mat_mul(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), Q(0))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def main():
    # Frozen FJ two-state nonlinear PDE sample.
    L = [[Q(-3), Q(3)], [Q(3), Q(-3)]]
    K = [[Q(5, 8), Q(3, 8)], [Q(3, 8), Q(5, 8)]]
    h = [Q(2), Q(1)]
    r = [Q(1), Q(0)]
    V = [Q(1), Q(2)]
    B2 = [Q(1, 2), Q(0)]
    lam = Q(2)
    a1 = [1 - v / lam for v in V]
    resolvent_left = [[lam - L[i][j] if i == j else -L[i][j] for j in range(2)] for i in range(2)]
    require(mat_mul(resolvent_left, K) == [[Q(2), Q(0)], [Q(0), Q(2)]], "FJ resolvent identity")

    A0 = mat_vec(K, [abs(x) / lam for x in r])
    A1 = mat_vec(K, [a * x for a, x in zip(a1, h)])
    A2 = mat_vec(K, [b * x * x / lam for b, x in zip(B2, h)])
    totals = [A0[i] + A1[i] + A2[i] for i in range(2)]
    require(A0 == [Q(5, 16), Q(3, 16)], "FJ source masses")
    require(A1 == [Q(5, 8), Q(3, 8)], "FJ unary masses")
    require(A2 == [Q(5, 8), Q(3, 8)], "FJ binary masses")
    require(totals[0] <= h[0] and totals[1] <= h[1], "FJ envelope")

    source_p = [A0[i] / h[i] for i in range(2)]
    unary_p = [A1[i] / h[i] for i in range(2)]
    binary_p = [A2[i] / h[i] for i in range(2)]
    zero_p = [1 - source_p[i] - unary_p[i] - binary_p[i] for i in range(2)]
    require(source_p == [Q(5, 32), Q(3, 16)], "FJ source event probabilities")
    require(unary_p == [Q(5, 16), Q(3, 8)], "FJ unary probabilities")
    require(binary_p == [Q(5, 16), Q(3, 8)], "FJ binary probabilities")
    require(zero_p == [Q(7, 32), Q(1, 16)], "FJ zero-leaf probabilities")

    # All child endpoints are A: a1*h and B2*h^2 are supported only at A.
    M = [[unary_p[i] + 2 * binary_p[i], Q(0)] for i in range(2)]
    require(M == [[Q(15, 16), Q(0)], [Q(9, 8), Q(0)]], "FJ mean progeny")
    w = [Q(1), Q(6, 5)]
    Mw = mat_vec(M, w)
    alpha = Q(15, 16)
    require(Mw == [alpha * w[0], alpha * w[1]], "FJ weighted mean-progeny witness")
    require(sum(M[1]) == Q(9, 8) > 1, "B-root mean offspring exceeds one")

    # Nonlinear probability-generating-function supersolution.
    tA, tB, z = Q(11, 10), Q(9, 8), Q(501, 500)
    GA = Q(3, 8) + Q(5, 16) * tA + Q(5, 16) * tA * tA
    GB = Q(1, 4) + Q(3, 8) * tA + Q(3, 8) * tA * tA
    require(GA == Q(351, 320), "FJ PGF at A")
    require(GB == Q(893, 800), "FJ PGF at B")
    require(z * GA == Q(175851, 160000) <= tA, "A nonlinear supersolution")
    require(z * GB == Q(447393, 400000) <= tB, "B nonlinear supersolution")
    require(tA >= 1 and tB >= 1 and z > 1, "positive supersolution domain")

    # The old scalar enclosure/derivative contraction fails at every radius.
    old_lambda, old_residual, old_B, old_h = Q(1), Q(1), Q(1, 2), Q(2)
    best_old_lhs = old_lambda * old_lambda / (4 * old_B)
    gamma = 2 * old_B * old_h
    require(best_old_lhs == Q(1, 2) < old_residual, "old scalar enclosure fails")
    require(gamma == 2 and gamma > old_lambda, "old pointwise Gamma criterion fails")

    # Exact PDE solution: u_A=(-11+3 sqrt(19))/5, u_B=(3/5)u_A.
    # Verify its quadratic identity in Q(sqrt(19)) by rational coefficients.
    xa, xb = Q(-11, 5), Q(3, 5)  # xa + xb*sqrt(19)
    rational_part = xa * xa + 19 * xb * xb + Q(22, 5) * xa - 2
    radical_part = 2 * xa * xb + Q(22, 5) * xb
    require(rational_part == 0 and radical_part == 0, "exact PDE solution identity")

    # Bounded vector correction oracle X=(S_A,S_B), sigma=1, d=2.
    R2, eps_g, delta, roots = Q(5), Q(1, 4), Q(1, 4), 2
    require(R2 == Q(2 * 2 + 1), "Euclidean radius squared")
    e_low, e_high = e_interval()
    e2_interval = (e_low * e_low, e_high * e_high)
    m_logarg = 64 * (1 + R2) / eps_g
    require(m_logarg == 1536, "N722 m logarithm argument")
    m_scale = 64 * (1 + R2)
    require(m_scale == 384, "N722 m logarithm scale")
    m_interval_raw = ln_interval(m_logarg)
    m_interval = (m_scale * m_interval_raw[0], m_scale * m_interval_raw[1])
    m = ceil_cert(m_interval, 2818, "N722 factor count m")
    Karg = ln_interval(Q(3 * m) / delta)
    Kinterval = (e2_interval[0] * Karg[0], e2_interval[1] * Karg[1])
    Kcap = ceil_cert(Kinterval, 78, "factory proposal cap K")
    Jarg = ln_interval(Q(3 * m * Kcap) / delta)
    Jinterval = (
        2 * (e_low - 1) + Jarg[0],
        2 * (e_high - 1) + Jarg[1],
    )
    Jcap = ceil_cert(Jinterval, 19, "Poisson inverse-CDF cap J")
    Btrees = roots * m * Kcap * Jcap
    require(Btrees == 8_352_552, "maximum number of branch trees")
    A_tree = Q(3 * Btrees) * tB / delta
    ncap, ncap_lower = ceil_log_ratio_exact(A_tree, z)
    require((ncap, ncap_lower) == (9280, 9279), "exact multitype tree cap")
    hard_nodes = Btrees * ncap
    require(hard_nodes == 77_511_682_560, "hard branch-node cap")

    # Cost/correlation statement is quantified by the exact mean progeny.
    # The random node count and bounded return can be dependent; each fresh
    # acquisition nonetheless has conditional expected count 16+19=35.
    expected_nodes_A = 1 / (1 - M[0][0])
    expected_nodes_B = 1 + M[1][0] / (1 - M[0][0])
    require(expected_nodes_A == 16 and expected_nodes_B == 19, "expected nodes by root")
    expected_A_nodes_vector = expected_nodes_A + (M[1][0] / (1 - M[0][0]))
    expected_B_nodes_vector = Q(1)
    active_A = source_p[0] + unary_p[0] + binary_p[0]
    active_B = source_p[1] + unary_p[1] + binary_p[1]
    expected_tilted_endpoints = expected_nodes_A * active_A + active_B + (M[1][0] / (1 - M[0][0])) * active_A
    require(expected_A_nodes_vector == 34 and expected_B_nodes_vector == 1, "expected type-specific node visits")
    require(active_A == Q(25, 32) and active_B == Q(15, 16), "active endpoint event probabilities")
    require(expected_tilted_endpoints == Q(55, 2), "expected tilted resolvent endpoint draws")

    # Independent uniform-subcritical queue-tail check on a second exact PDE.
    Lq = [[Q(-1), Q(1)], [Q(1), Q(-1)]]
    Kq = [[Q(3, 4), Q(1, 4)], [Q(1, 4), Q(3, 4)]]
    resolvent_left_q = [[Q(2) - Lq[i][j] if i == j else -Lq[i][j] for j in range(2)] for i in range(2)]
    require(mat_mul(resolvent_left_q, Kq) == [[Q(2), Q(0)], [Q(0), Q(2)]], "linear PDE resolvent identity")
    rq = [Q(1, 4), Q(1, 4)]
    Aq0 = mat_vec(Kq, [x / 2 for x in rq])
    Aq1 = mat_vec(Kq, [Q(1, 2), Q(1, 2)])
    require(Aq0 == [Q(1, 8), Q(1, 8)], "linear PDE source masses")
    require(Aq1 == [Q(1, 2), Q(1, 2)], "linear PDE unary masses")
    require(all(Aq0[i] + Aq1[i] == Q(5, 8) <= 1 for i in range(2)), "linear PDE envelope")
    require(Q(1, 2) * 1 + Q(1, 2) * 2 == Q(3, 2), "linear PDE frontier PGF")
    require(Q(4, 3) * Q(3, 2) == 2, "linear PDE t,z witness")
    require(1 / (1 - Q(1, 2)) == 2, "linear PDE expected nodes")

    # Exact uniform-queue N722 cap arithmetic using R^2=2 and
    # epsilon_g=delta=1/4, then r=2 tree roots per vector acquisition.
    mq_logarg = 64 * (1 + 2) / eps_g
    require(mq_logarg == 768, "uniform-case N722 m logarithm argument")
    mq_scale = 64 * (1 + 2)
    require(mq_scale == 192, "uniform-case N722 m logarithm scale")
    mq_iv_raw = ln_interval(mq_logarg)
    mq = ceil_cert((mq_scale * mq_iv_raw[0], mq_scale * mq_iv_raw[1]), 1276, "uniform-case N722 m")
    Kq_arg = ln_interval(Q(3 * mq) / delta)
    Kq_iv = (e2_interval[0] * Kq_arg[0], e2_interval[1] * Kq_arg[1])
    Kq_cap = ceil_cert(Kq_iv, 72, "uniform-case factory K")
    Jq_arg = ln_interval(Q(3 * mq * Kq_cap) / delta)
    Jq_iv = (2 * (e_low - 1) + Jq_arg[0], 2 * (e_high - 1) + Jq_arg[1])
    Jq_cap = ceil_cert(Jq_iv, 18, "uniform-case Poisson Jcap")
    Bq = 2 * mq * Kq_cap * Jq_cap
    require(Bq == 3_307_392, "uniform test tree count")
    uniform_arg = Q(3 * Bq) / delta
    uniform_n_interval = ln_interval(uniform_arg)
    uniform_n_interval = (8 * uniform_n_interval[0], 8 * uniform_n_interval[1])
    uniform_ncap = ceil_cert(uniform_n_interval, 140, "uniform Azuma tree cap")
    require(Bq * uniform_ncap == 463_034_880, "uniform hard branch-node cap")

    print("PASS: exact rational PDE envelopes, event probabilities, offspring PGFs, and t,z inequalities")
    print("PASS: exact rational cap ceilings and exact-power multitype ncap bracket 9279 < 9280")
    print("PASS: exact rational uniform-q PDE witness and Azuma ncap=140")
    print(f"FJ N722 composition caps: m={m}, K={Kcap}, Jcap={Jcap}, trees={Btrees}, ncap={ncap}, hard_nodes={hard_nodes}")
    print(f"FJ exact expected branch nodes per vector acquisition: {expected_nodes_A + expected_nodes_B}")
    print(f"FJ expected node types A/B and tilted endpoint draws per vector: {expected_A_nodes_vector}/{expected_B_nodes_vector}, {expected_tilted_endpoints}")
    print(f"Uniform comparison cap: trees={Bq}, ncap={uniform_ncap}, hard_nodes={Bq * uniform_ncap}")
    print("Scope: exact finite-state/ideal-real arithmetic certificate only; not continuous-diffusion acquisition or bit-complexity validation.")


if __name__ == "__main__":
    main()
