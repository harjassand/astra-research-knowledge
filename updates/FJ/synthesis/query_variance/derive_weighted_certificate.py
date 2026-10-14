#!/usr/bin/env python3
"""Exact Fourier certificate for a target-weighted correction tree.

All Fourier coefficients and inequalities are rational.  The generated
certificate is for the supplied scalar periodic quartic example, target x=0.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import ceil, isqrt
import json
from pathlib import Path

# A Fourier polynomial is {integer_frequency: (real_fraction, imag_fraction)}
# for sum_k c_k exp(i k x).
Poly = dict[int, tuple[Q, Q]]


def clean(p: Poly) -> Poly:
    return {k: z for k, z in p.items() if z != (0, 0)}


def add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for k, (r, i) in b.items():
        ar, ai = out.get(k, (Q(0), Q(0)))
        out[k] = (ar + r, ai + i)
    return clean(out)


def scale(a: Poly, s: Q) -> Poly:
    return clean({k: (r * s, i * s) for k, (r, i) in a.items()})


def mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ka, (ar, ai) in a.items():
        for kb, (br, bi) in b.items():
            rr, ii = ar * br - ai * bi, ar * bi + ai * br
            oldr, oldi = out.get(ka + kb, (Q(0), Q(0)))
            out[ka + kb] = (oldr + rr, oldi + ii)
    return clean(out)


def powp(a: Poly, n: int) -> Poly:
    out: Poly = {0: (Q(1), Q(0))}
    base = a
    while n:
        if n & 1:
            out = mul(out, base)
        n >>= 1
        if n:
            base = mul(base, base)
    return out


def add_const(a: Poly, c: Q) -> Poly:
    return add(a, {0: (c, Q(0))})


def cosine(k: int, a: Q) -> Poly:
    return {k: (a / 2, Q(0)), -k: (a / 2, Q(0))}


def sine(k: int, a: Q) -> Poly:
    return {k: (Q(0), -a / 2), -k: (Q(0), a / 2)}


def resolvent(a: Poly, rate: int = 101) -> Poly:
    return {k: (r / (rate + k * k), i / (rate + k * k))
            for k, (r, i) in a.items()}


def l1(a: Poly) -> Q:
    # For real trigonometric polynomials, this is a rational upper bound on
    # sup_x |a(x)| by the triangle inequality in real and imaginary parts.
    return sum((abs(r) + abs(i) for r, i in a.values()), Q(0))


def eval_zero(a: Poly) -> Q:
    # At x=0 every Fourier phase is exactly 1. Reality implies zero imaginary sum.
    return sum((r for r, _ in a.values()), Q(0))


def sqrt_upper(x: Q, denominator: int = 10**18) -> Q:
    """Smallest k/denominator found with an exact rational square check."""
    if x < 0:
        raise ValueError("sqrt upper bound requires a nonnegative input")
    k = isqrt((x.numerator * denominator * denominator) // x.denominator)
    while Q(k * k, denominator * denominator) < x:
        k += 1
    return Q(k, denominator)


def cauchy_sup_bounds(a: Poly, max_s: int = 4) -> list[Q]:
    """Exact H^s Fourier/Cauchy upper bounds on sup |a|."""
    if not a:
        return [Q(0)]
    degree = max(abs(k) for k in a)
    result = []
    for s in range(max_s + 1):
        energy = Q(0)
        reciprocal = Q(0)
        for k in range(-degree, degree + 1):
            w = Q((1 + k * k) ** s)
            r, i = a.get(k, (Q(0), Q(0)))
            energy += w * (r * r + i * i)
            reciprocal += 1 / w
        result.append(sqrt_upper(energy * reciprocal))
    return result


def encode(x: Q) -> dict[str, object]:
    return {"numerator": x.numerator, "denominator": x.denominator,
            "decimal": float(x)}


def build() -> dict[str, object]:
    # The supplied first screened correction e0 is exact for A=(-d^2+101).
    e0: Poly = {}
    e0 = add(e0, cosine(1, Q(3, 68)))
    e0 = add(e0, cosine(7, Q(1, 50)))
    e0 = add(e0, sine(13, Q(1, 108)))

    N_e0 = add(add(scale(powp(e0, 2), Q(150)),
                   scale(powp(e0, 3), Q(100))),
               scale(powp(e0, 4), Q(25)))
    r1 = scale(N_e0, Q(-1))
    q = resolvent(r1)

    E = l1(e0)
    vmax = Q(1) + E
    dplus = 100 * (vmax**3 - 1)
    dminus = 100 * (1 - (1 - E)**3)
    D = max(dplus, dminus)
    B2, B3, B4 = 150 * vmax**2, 100 * vmax, Q(25)

    eta_candidates = [l1(q), *cauchy_sup_bounds(q)]
    eta = min(eta_candidates)
    assert eta > 0
    q2 = powp(q, 2)
    hbase = add_const(scale(q2, 1 / (2 * eta)), eta / 2)

    # Since ||H||_Fourier-l1 <= eta+c and ||G f||_infty <= ||f||_infty/101,
    # a scalar rational fixed point gives a certificate without repeatedly
    # constructing high-degree exact convolutions.
    c = Q(0)
    denom = 10**24
    for iteration in range(1, 80):
        s = eta + c
        c_req = (D * s + B2 * s**2 + B3 * s**3 + B4 * s**4) / 101
        c_next = Q(ceil(c_req * denom), denom)
        if c_next <= c:
            break
        c = c_next
    else:
        raise RuntimeError("majorant fixed point did not settle")
    s = eta + c
    c_required = (D * s + B2 * s**2 + B3 * s**3 + B4 * s**4) / 101
    assert c >= c_required

    H_min = eta / 2 + c
    work_majorant = (D * s + 2 * B2 * s**2 +
                     3 * B3 * s**3 + 4 * B4 * s**4) / 101
    H_min = eta / 2 + c
    Q_offspring = work_majorant / H_min
    H_max = eta + c
    H = add_const(hbase, c)
    q_at_zero = eval_zero(q)
    H_at_zero = eta / 2 + q_at_zero**2 / (2 * eta) + c
    proposal_bound = (D * H_max + B2 * H_max**2 +
                      B3 * H_max**3 + B4 * H_max**4) / (101 * H_min)

    # The one-correction baseline's global certificate uses h=11/1000.
    baseline_h = Q(11, 1000)
    assert Q(0) < H_at_zero
    assert Q(0) < Q_offspring < 1

    # Exact finite Fourier identities for the residual correction.
    # With delta=u-v1 and d=101-V(v1), A delta=r1+d*delta-sum c_m delta^m.
    # q=A^-1 r1, so delta=q+A^-1[d*delta-sum c_m delta^m].
    return {
        "method": "exact rational Fourier arithmetic",
        "equation": "-u'' + u + 25 u^4 = 26 + 10(0.45 cos x + 0.30 cos 7x + 0.25 sin 13x)",
        "target_x": 0,
        "base_operator": "A=-d^2+101 on the 2pi-periodic torus",
        "predictor": "v1=1+e0, with e0=A^-1(10g) as in supplied package",
        "control": "q=A^-1 r1, r1=-150 e0^2-100 e0^3-25 e0^4; q is integrated exactly in Fourier space",
        "fourier_degree": {"e0": max(abs(k) for k in e0),
                           "q": max(abs(k) for k in q),
                           "H": max(abs(k) for k in H)},
        "coefficient_bounds": {"E0_sup": encode(E), "D_abs_d": encode(D),
                               "B2": encode(B2), "B3": encode(B3), "B4": encode(B4)},
        "q_sup_certificate": {"method": "Fourier triangle and weighted Cauchy-Schwarz",
                              "candidate_bounds": [encode(x) for x in eta_candidates],
                              "selected_eta": encode(eta)},
        "majorant": {"eta_l1_q": encode(eta), "c": encode(c),
                     "c_required_scalar_majorant": encode(c_required),
                     "H_min_lower": encode(H_min), "H_max_upper": encode(H_max),
                     "q_at_target_x0": encode(q_at_zero),
                     "H_at_target_x0": encode(H_at_zero),
                     "H_at_target_vs_global_squared_ratio": encode((H_at_zero / H_max)**2),
                     "uniform_baseline_h": encode(baseline_h)},
        "work": {"offspring_contraction_upper": encode(Q_offspring),
                 "rejection_endpoint_proposals_per_node_upper": encode(proposal_bound),
                 "tree_nodes_upper": encode(1 / (1 - Q_offspring)),
                 "nodes_plus_proposals_upper": encode((1 + proposal_bound) / (1 - Q_offspring))},
        "sample_bound": "M >= 2 H(0)^2 epsilon^-2 log(2/delta) by Hoeffding for independent trees",
        "sample_radius_ratio_squared_vs_package": encode((H_at_zero / baseline_h)**2),
        "endpoint_count_constant_ratio_vs_package": encode(
            (H_at_zero / baseline_h)**2 * ((1 + proposal_bound) / (1-Q_offspring)) /
            Q(120557007166832000, 74191688310648511)),
        "certificate_scope": "The Fourier identities and listed scalar majorant inequalities are exact rational statements. The fixed-point c dominates the weighted source because the resolvent has sup-norm at most 1/101. Brownian/rejection sampling is ideal in the theorem; the later prototype uses floating point.",
    }


if __name__ == "__main__":
    result = build()
    out = Path(__file__).with_name("weighted_certificate.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
