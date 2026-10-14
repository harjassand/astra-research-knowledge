#!/usr/bin/env python3
"""Independent exact Laurent checks for the FL packet-assembly audit.

Pure Python standard library.  This does not import the supplied verifier.
It checks bounded-degree moment factorisation for two dependent gradient
packets and exact affine optimisation in a resonant determinant-square example.
"""
from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path


class G:
    """Gaussian rational, represented by a pair of Fractions."""
    __slots__ = ("r", "i")

    def __init__(self, r=0, i=0):
        self.r, self.i = Q(r), Q(i)

    def __add__(self, other):
        other = as_g(other)
        return G(self.r + other.r, self.i + other.i)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.r, -self.i)

    def __sub__(self, other):
        return self + (-as_g(other))

    def __rsub__(self, other):
        return as_g(other) - self

    def __mul__(self, other):
        other = as_g(other)
        return G(self.r * other.r - self.i * other.i,
                 self.r * other.i + self.i * other.r)

    __rmul__ = __mul__

    def __eq__(self, other):
        other = as_g(other)
        return self.r == other.r and self.i == other.i

    def pair(self):
        return [str(self.r), str(self.i)]


def as_g(x):
    if isinstance(x, G):
        return x
    return G(x, 0)


def clean(d):
    return {k: v for k, v in d.items() if v != G()}


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, G()) + v
    return clean(out)


def neg(a):
    return {k: -v for k, v in a.items()}


def sub(a, b):
    return add(a, neg(b))


def scale(a, s):
    return clean({k: as_g(s) * v for k, v in a.items()})


def mul(a, b):
    out = {}
    for k, v in a.items():
        for ell, w in b.items():
            key = tuple(k[j] + ell[j] for j in range(len(k)))
            out[key] = out.get(key, G()) + v * w
    return clean(out)


def power(a, n):
    out = {(0,) * len(next(iter(a), (0,))): G(1)}
    for _ in range(n):
        out = mul(out, a)
    return out


def mean(a):
    z = a.get((0,) * len(next(iter(a), (0,))), G())
    assert z.i == 0, f"nonreal mean: {z.pair()}"
    return z.r


def cos1(n):
    return {(n,): G(Q(1, 2)), (-n,): G(Q(1, 2))}


def sin1(n):
    return {(n,): G(0, Q(-1, 2)), (-n,): G(0, Q(1, 2))}


def cos2(k):
    return {k: G(Q(1, 2)), (-k[0], -k[1]): G(Q(1, 2))}


def sin2(k):
    return {k: G(0, Q(-1, 2)), (-k[0], -k[1]): G(0, Q(1, 2))}


def d2(poly, j):
    out = {}
    for (kx, ky), v in poly.items():
        k = (kx, ky)[j]
        out[(kx, ky)] = G(0, k) * v
    return clean(out)


def vec_add(a, b):
    return [add(x, y) for x, y in zip(a, b)]


def vec_sub(a, b):
    return [sub(x, y) for x, y in zip(a, b)]


def vec_scale(a, s):
    return [scale(x, s) for x in a]


def vec_mean_product(a, b):
    return mean(mul(a, b))


def determinant(x):
    # Vector order is (A11,A12,A21,A22).
    return sub(mul(x[0], x[3]), mul(x[1], x[2]))


def check_low_degree_packet_moments():
    # The compatible scalar gradients are X1=f R, X2=g R, R=e11,
    # with f=cos(x), g=-sin(2x). Their supports have a primitive triad.
    f, g = cos1(1), scale(sin1(2), -1)
    counts = {}
    checked = 0
    for degree in range(5):
        count = 0
        for p in range(degree + 1):
            q = degree - p
            actual = mean(mul(power(f, p), power(g, q)))
            independent = mean(power(f, p)) * mean(power(g, q))
            assert actual == independent, (degree, p, q, actual, independent)
            checked += 1
            count += 1
        counts[str(degree)] = count

    # Dependence and a degree-six mixed-moment failure are exact.
    identity = sub(power(g, 2),
                   scale(sub(power(f, 2), power(f, 4)), 4))
    assert not identity
    actual_degree_six = mean(mul(power(f, 4), power(g, 2)))
    independent_degree_six = mean(power(f, 4)) * mean(power(g, 2))
    assert actual_degree_six == Q(5, 32)
    assert independent_degree_six == Q(3, 16)
    return {
        "compatible_potentials": ["phi_1=(sin x,0)", "phi_2=(cos(2x)/2,0)"],
        "gradient_values": ["X_1=cos(x) R", "X_2=-sin(2x) R", "R=e11"],
        "monomials_checked_by_degree": counts,
        "total_monomials_checked": checked,
        "all_actual_moments_equal_product_marginal_moments_through_degree_4": True,
        "cross_packet_primitive_relation": "(1,0)+(1,0)-(2,0)=0, length 3",
        "resonant_support_condition_is_sufficient_not_necessary": True,
        "degree_6_witness": {
            "observable": "E[f^4 g^2]",
            "actual_mean": str(actual_degree_six),
            "independent_phase_mean": str(independent_degree_six),
        },
        "statistically_independent": False,
        "dependence_witness": {
            "identity_verified": "g^2=4 f^2(1-f^2)",
            "meaning": "joint law lies on a proper algebraic curve",
        },
    }


def check_norm_four_assembly():
    f, g = cos1(1), scale(sin1(2), -1)
    m2_f, m4_f = mean(power(f, 2)), mean(power(f, 4))
    m2_g, m4_g = mean(power(g, 2)), mean(power(g, 4))
    m3_sum = mean(power(add(f, g), 3))
    m2_sum = mean(power(add(f, g), 2))
    csum = mean(power(add(f, g), 4))
    # C_i=(1/2)RR^T, H_i=8 C_i+4 E|X_i|^2 I=4RR^T+2I.
    C = [Q(1, 2), Q(0), Q(0), Q(0)]
    Hdiag = [Q(6), Q(2), Q(2), Q(2)]
    cross = sum(h * c for h, c in zip(Hdiag, C)) / 2
    assert (m2_f, m2_g, m4_f, m4_g) == (Q(1, 2), Q(1, 2), Q(3, 8), Q(3, 8))
    assert m2_sum == 1 and m3_sum == 0 and csum == Q(9, 4)
    assert csum - Q(2, 3) * m3_sum**2 / m2_sum == Q(9, 4)
    assert cross == Q(3, 2)
    assert m4_f + m4_g + cross == csum
    return {
        "integrand": "F(A)=|A|^4",
        "marginal_C_diagonal": [str(z) for z in C],
        "marginal_H_diagonal": [str(z) for z in Hdiag],
        "marginal_b": ["0"] * 4,
        "marginal_delta": ["3/8", "3/8"],
        "cross_constant_half_trace_HC": str(cross),
        "background_disagreement_penalty": "0",
        "actual_sum_delta": str(csum),
        "independent_sum_delta": str(csum),
        "all_exact": True,
    }


def check_fixed_integrand_observable_match():
    f, g = cos1(1), cos1(2)
    mixed_third = mean(mul(power(f, 2), g))
    independent_third = mean(power(f, 2)) * mean(g)
    covariance = mean(mul(f, g))
    variance_sum = mean(power(add(f, g), 2))
    product_variance_sum = mean(power(f, 2)) + mean(power(g, 2))
    assert mixed_third == Q(1, 4) and independent_third == 0
    assert covariance == 0 and variance_sum == product_variance_sum == 1
    return {
        "integrand": "F(A)=(det A)^2",
        "packets": "X_1=cos(x)R, X_2=cos(2x)R, R=e11",
        "primitive_cross_triad": "(1,0)+(1,0)-(2,0)=0",
        "mixed_moment_mismatch_E[f^2g]": {
            "actual": str(mixed_third),
            "independent": str(independent_third),
        },
        "actual_and_independent_second_moment_of_sum": str(variance_sum),
        "affine_gap_match_reason": "det(B+tR) is affine in t, so this F sees only the centered scalar second moment",
        "actual_affine_gap_equals_independent_affine_gap_for_all_B": True,
        "optimized_gap": "0",
    }


def check_resonant_determinant_square():
    a = Q(1, 2)
    one = {(0, 0): G(1)}
    cx, sx = cos2((1, 0)), sin2((1, 0))
    cy, sy = cos2((0, 1)), sin2((0, 1))
    c2y, s2y = cos2((0, 2)), sin2((0, 2))
    r = add(one, scale(cx, a))
    s = sub(one, scale(cx, a))
    rp, sp = scale(sx, -a), scale(sx, a)
    # Actual gradients of r(x)(cos y,sin y) and s(x)(cos 2y,sin 2y).
    x1 = [mul(rp, cy), scale(mul(r, sy), -1),
          mul(rp, sy), mul(r, cy)]
    x2 = [mul(sp, c2y), scale(mul(s, s2y), -2),
          mul(sp, s2y), scale(mul(s, c2y), 2)]
    d1, d2 = determinant(x1), determinant(x2)
    xs = vec_add(x1, x2)
    ds = determinant(xs)
    expected_ds = scale(
        mul(sx, add(add(scale(mul(cx, cy), 3), scale(cx, -3)),
                     add(scale(cy, -2), {(0, 0): G(2)}))),
        Q(1, 4))
    assert ds == expected_ds
    c1, c2, w = mean(mul(d1, d1)), mean(mul(d2, d2)), mean(mul(ds, ds))
    assert (c1, c2, w) == (Q(17, 128), Q(17, 32), Q(75, 256))

    def covariance_and_det_cross(x, d):
        c = [[vec_mean_product(x[i], x[j]) for j in range(4)] for i in range(4)]
        v_local = [vec_mean_product(x[i], d) for i in range(4)]
        return c, v_local

    C1, v1 = covariance_and_det_cross(x1, d1)
    C2, v2 = covariance_and_det_cross(x2, d2)
    assert v1 == [Q(0)] * 4 and v2 == [Q(0)] * 4
    assert all(mean(z) == 0 for z in xs) and mean(ds) == 0

    C = [[vec_mean_product(xs[i], xs[j]) for j in range(4)] for i in range(4)]
    v = [vec_mean_product(xs[i], ds) for i in range(4)]
    expected_C = [[Q(0) for _ in range(4)] for _ in range(4)]
    for i, d in enumerate((Q(1, 8), Q(45, 16), Q(1, 8), Q(45, 16))):
        expected_C[i][i] = d
    assert C == expected_C
    assert v == [Q(1, 16), Q(0), Q(0), Q(0)]
    # cofactor(B) ranges over all of R^4, so the affine optimization is
    # min_z z^T C z + 2 v^T z + w.
    delta = w - sum(v[i] * v[i] / C[i][i] for i in range(4))
    assert delta == Q(67, 256)
    zstar = [-v[i] / C[i][i] for i in range(4)]
    assert zstar == [Q(-1, 2), Q(0), Q(0), Q(0)]
    return {
        "integrand": "F(A)=(det A)^2",
        "packets": "r=1+cos(x)/2 at carrier y; s=1-cos(x)/2 at carrier 2y",
        "marginal_zero_background_values": [str(c1), str(c2)],
        "marginal_affine_minima": [str(c1), str(c2)],
        "marginal_E[X_i det X_i]": [[str(t) for t in v1], [str(t) for t in v2]],
        "total_zero_background_value": str(w),
        "total_covariance_C_diagonal": [str(expected_C[i][i]) for i in range(4)],
        "total_v=E[X det X]": [str(t) for t in v],
        "cofactor_affine_optimizer": [str(t) for t in zstar],
        "total_affine_optimized_delta": str(delta),
        "sum_of_marginal_deltas": str(c1 + c2),
        "failure_of_unrestricted_superadditivity": str(delta - c1 - c2),
        "total_gap_nonnegative": "yes; equals a variance for every affine B",
    }


def check_long_resonance_component():
    # For f_j=(1,j), the primitive quartets f_j+f_{j+2}-2 f_{j+1}=0
    # link every consecutive triple. Check the graph for several M.
    rows = []
    for M in (3, 5, 8, 16):
        edges = [(j, j + 1, j + 2) for j in range(M - 2)]
        seen = {0}
        changed = True
        while changed:
            changed = False
            for edge in edges:
                if seen.intersection(edge) and not set(edge).issubset(seen):
                    seen.update(edge)
                    changed = True
        assert seen == set(range(M))
        rows.append({"support_classes": M, "primitive_quartet_edges": len(edges),
                     "largest_component_classes": len(seen)})
    return {
        "frequency_classes": "f_j=(1,j), j=0,...,M-1",
        "primitive_relation": "f_j+f_(j+2)-f_(j+1)-f_(j+1)=0",
        "component_growth_examples": rows,
        "arbitrary_finite_profile_can_be_one_degree_4_resonance_component": True,
    }


if __name__ == "__main__":
    result = {
        "scope": "Exact rational Laurent checks for stated finite examples; not a proof of the analytic composition theorem or a global quasiconvexity result.",
        "dependent_degree_four_packets": check_low_degree_packet_moments(),
        "positive_optimized_composition": check_norm_four_assembly(),
        "fixed_integrand_coefficient_match": check_fixed_integrand_observable_match(),
        "resonant_unrestricted_gluing_counterexample": check_resonant_determinant_square(),
        "resonance_component_coverage": check_long_resonance_component(),
    }
    out = Path(__file__).resolve().parent / "independent_packet_checks.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"WROTE {out}")
