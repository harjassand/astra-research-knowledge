"""Exact PGF counterexample with typewise mean/covariance matching.

This is a mathematical witness, not a fit to a tumor. Every calculation uses
fractions; Python's standard library is sufficient.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb


def add_scaled(dst, src, scale=F(1)):
    for k, v in src.items():
        dst[k] = dst.get(k, F(0)) + scale * v
    return {k: v for k, v in dst.items() if v}


def poly_mul(a, b):
    out = defaultdict(F)
    for i, x in a.items():
        for j, y in b.items():
            degree = tuple(u + v for u, v in zip(i, j)) if isinstance(i, tuple) else i + j
            out[degree] += x * y
    return {k: v for k, v in out.items() if v}


def poly_pow(a, n):
    sample_key = next(iter(a))
    identity = (0, 0) if isinstance(sample_key, tuple) else 0
    out = {identity: F(1)}
    for _ in range(n):
        out = poly_mul(out, a)
    return out


def scalar_moments(coeffs):
    mean = sum(F(k) * p for k, p in coeffs.items())
    second = sum(F(k * k) * p for k, p in coeffs.items())
    return mean, second - mean * mean


def scalar_kappa3(coeffs):
    mean, _ = scalar_moments(coeffs)
    return sum(p * (F(k) - mean) ** 3 for k, p in coeffs.items())


def thin_scalar(coeffs, q):
    """Return f(1-q+q*s) exactly."""
    out = defaultdict(F)
    for k, pk in coeffs.items():
        for j in range(k + 1):
            out[j] += pk * comb(k, j) * q**j * (1 - q) ** (k - j)
    return {k: v for k, v in out.items() if v}


def hit_risk_scalar(coeffs, threshold, horizon):
    """Exact first-hit probability; all counts >= threshold enter hit state."""
    safe = {n: F(0) for n in range(threshold)}
    safe[1] = F(1)
    hit = F(0)
    for _ in range(horizon):
        nxt = {n: F(0) for n in range(threshold)}
        for n, mass in safe.items():
            if not mass:
                continue
            for k, pk in poly_pow(coeffs, n).items():
                if k >= threshold:
                    hit += mass * pk
                else:
                    nxt[k] += mass * pk
        safe = nxt
    return hit


def vector_distribution(total_law, pi_g, q):
    """Type-count PGF for one parent's total offspring law and daughter type."""
    daughter = {
        (0, 0): 1 - q,
        (1, 0): q * (1 - pi_g),
        (0, 1): q * pi_g,
    }
    out = {}
    for k, pk in total_law.items():
        add_scaled(out, poly_pow(daughter, k), pk)
    return out


def vector_mean_cov(dist):
    mean = tuple(sum(p * x[j] for x, p in dist.items()) for j in (0, 1))
    cov = tuple(
        tuple(sum(p * (x[i] - mean[i]) * (x[j] - mean[j]) for x, p in dist.items())
              for j in (0, 1))
        for i in (0, 1)
    )
    return mean, cov


def multitype_parent_pgfs(q, pi_g, burst_state):
    """PGFs for O/G parent types; only G bursts in model B."""
    daughter = {
        (0, 0): 1 - q,
        (1, 0): q * (1 - pi_g),
        (0, 1): q * pi_g,
    }
    law_a = {(0, 0): F(1, 2)}
    add_scaled(law_a, poly_pow(daughter, 2), F(1, 2))
    if burst_state:
        law_g = {(0, 0): F(1, 3)}
        add_scaled(law_g, daughter, F(1, 2))
        add_scaled(law_g, poly_pow(daughter, 3), F(1, 6))
        return law_a, law_g
    return law_a, law_a


def hit_risk_multitype(q, pi_g, threshold, horizon, burst_state):
    """Exact DP on safe (n_O,n_G) states; all total counts >= M are absorbing."""
    pgf_o, pgf_g = multitype_parent_pgfs(q, pi_g, burst_state)
    safe = defaultdict(F)
    safe[(1, 0)] = 1 - pi_g
    safe[(0, 1)] = pi_g
    hit = F(0)
    for _ in range(horizon):
        nxt = defaultdict(F)
        for (no, ng), mass in safe.items():
            trans = poly_mul(poly_pow(pgf_o, no), poly_pow(pgf_g, ng))
            for (ko, kg), pk in trans.items():
                if ko + kg >= threshold:
                    hit += mass * pk
                else:
                    nxt[(ko, kg)] += mass * pk
        safe = nxt
    return hit


def aggregate_laws(pi_g):
    law_a = {0: F(1, 2), 2: F(1, 2)}
    law_g_burst = {0: F(1, 3), 1: F(1, 2), 3: F(1, 6)}
    law_b = {}
    add_scaled(law_b, law_a, 1 - pi_g)
    add_scaled(law_b, law_g_burst, pi_g)
    return law_a, law_g_burst, law_b


def main():
    q = F(4, 5)
    probabilities_of_g = (F(1, 6), F(1, 2))
    for pi_g in probabilities_of_g:
        A, G_burst, B = aggregate_laws(pi_g)
        assert scalar_moments(A) == scalar_moments(G_burst) == (F(1), F(1))
        assert scalar_moments(B) == (F(1), F(1))
        assert scalar_kappa3(A) == 0
        assert scalar_kappa3(G_burst) == 1
        assert scalar_kappa3(B) == pi_g

        # Strong matching: for every parental type, both models have the same
        # full two-type offspring-vector mean and covariance, before/after q.
        for thinning in (F(1), q):
            expected_mean = (thinning * (1 - pi_g), thinning * pi_g)
            expected_cov = ((thinning * (1 - pi_g), F(0)),
                            (F(0), thinning * pi_g))
            for law_a, law_b in ((A, A), (A, G_burst)):
                mv_a = vector_mean_cov(vector_distribution(law_a, pi_g, thinning))
                mv_b = vector_mean_cov(vector_distribution(law_b, pi_g, thinning))
                assert mv_a == mv_b == (expected_mean, expected_cov)

        Aq, Bq = thin_scalar(A, q), thin_scalar(B, q)
        assert scalar_moments(Aq) == scalar_moments(Bq) == (q, q)
        print(f"pi_G={pi_g}: pre-control aggregate B law={B}")
        print("  post-control aggregate A law:", Aq)
        print("  post-control aggregate B law:", Bq)
        print("  post-control (mean,variance):", scalar_moments(Aq), scalar_moments(Bq))
        print("  pre-control third cumulant A/B:", scalar_kappa3(A), scalar_kappa3(B))
        for threshold in (3, 4):
            risk_a = hit_risk_scalar(Aq, threshold, 2)
            risk_b = hit_risk_scalar(Bq, threshold, 2)
            risk_b_multi = hit_risk_multitype(q, pi_g, threshold, 2, True)
            risk_a_multi = hit_risk_multitype(q, pi_g, threshold, 2, False)
            assert risk_a == risk_a_multi
            assert risk_b == risk_b_multi
            expected_a = {3: F(1024, 15625), 4: F(512, 15625)}[threshold]
            expected_b = {
                F(1, 6): {
                    3: F(7351088, 94921875),
                    4: F(46020918784, 1601806640625),
                },
                F(1, 2): {
                    3: F(116368, 1171875),
                    4: F(498947584, 19775390625),
                },
            }[pi_g][threshold]
            assert (risk_a, risk_b) == (expected_a, expected_b)
            print(
                f"  M={threshold},T=2: A={risk_a} ({float(risk_a):.12f}); "
                f"B={risk_b} ({float(risk_b):.12f}); multitype equality exact"
            )
        if pi_g == F(1, 6):
            risk_a = hit_risk_scalar(Aq, 3, 2)
            risk_b = hit_risk_scalar(Bq, 3, 2)
            for founders in (1, 4, 10):
                p_a = 1 - (1 - risk_a) ** founders
                p_b = 1 - (1 - risk_b) ** founders
                print(
                    f"  {founders} independent founders, any M=3 hit: "
                    f"A={float(p_a):.12f}; B={float(p_b):.12f}"
                )


if __name__ == "__main__":
    main()
