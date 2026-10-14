"""Exploratory floating-point checks for FOLLOWUP_DISSIPATION_AUDIT.md.

The analytic statements are proved in the report. Grid maxima printed here are
diagnostics, not certified global optima or empirical measurements.
"""

import math
from fractions import Fraction


q = 1 / 20
s = 1 + q
omega = math.sqrt(3) * (1 - q) / 2
gamma = 3 * s / 2
p = 2 / 3


def persistence(t):
    root = math.sqrt(q)
    return p * math.exp(-s * t) * (
        math.cosh(root * t) + s * math.sinh(root * t) / (2 * root)
    )


def third_difference(h):
    return persistence(3 * h) - 3 * persistence(2 * h) + 3 * persistence(h) - p


def fd_bound(h):
    d = third_difference(h)
    return 8 * d * d / (27 * h) if d > 0 else 0.0


def conditional_snapshot_bound(t):
    e = math.exp(-gamma * t)
    a = 2 / 3 + e * math.cos(omega * t) / 3
    delta = e * e * math.sin(omega * t) ** 2 / 3
    b = a * a - delta
    w = ((1 - a) ** 2 - delta, a * (1 - a) + delta,
         a * (1 - a) + delta, b)
    independent = ((1 - a) ** 2, a * (1 - a),
                   a * (1 - a), a * a)
    assert min(w) >= -1e-12
    info = sum(x * math.log(x / y) for x, y in zip(w, independent) if x > 0)
    return 2 * p * info / t, delta


def two_snapshot_bound(t, symmetric_error=0.0):
    covariance = (2 / 9) * math.exp(-gamma * t) * math.cos(omega * t)
    recorded_covariance = (1 - 2 * symmetric_error) ** 2 * covariance
    return (8 * recorded_covariance ** 2 / t if recorded_covariance < 0 else 0.0,
            recorded_covariance)


def geometric_path_bound(t):
    """New independent diagnostic; proof and exact small-time limit are in audit."""
    e = math.exp(-gamma * t)
    a = 2 / 3 + e * math.cos(omega * t) / 3
    delta = e * e * math.sin(omega * t) ** 2 / 3
    d = p * delta
    ratio = d / (a * (1 - a))
    return -math.log1p(-ratio) / t, a, delta, d, ratio


def optimized_geometric_path_bound(t):
    """Optimize the centered endpoint score over r in (0,1)."""
    _, a, delta, _, _ = geometric_path_bound(t)
    w11 = a * a - delta
    w00 = 1 - 2 * a + w11
    w01 = a - w11
    r_star = math.sqrt(w11) / (math.sqrt(w11) + math.sqrt(w00))
    c = 2 * p * (w01 - math.sqrt(w00 * w11))
    return -math.log1p(-c) / t, r_star, c


def ring_geometric_submeasure_check(t):
    """Closed-form check of killed G for the symmetric three-state ring."""
    _, a, _, d, _ = geometric_path_bound(t)
    lam_0 = -s + 2 * math.sqrt(q)
    lam_perp = -s - math.sqrt(q)
    affinity = math.exp(2 * t * lam_0)
    e_nu_w = p * (
        math.exp(t * lam_0) * (p - a)
        + math.exp(t * lam_perp) / 3
    ) ** 2
    return -d, e_nu_w, affinity, a * (1 - a) * (1 - affinity)


def transition_matrix(t):
    """Circulant three-state ring transition matrix from Fourier eigenvalues."""
    e = math.exp(-gamma * t)
    phases = (0.0, -2 * math.pi / 3, 2 * math.pi / 3)
    return [[1 / 3 + 2 * e * math.cos(omega * t + phases[(j - i) % 3]) / 3
             for j in range(3)] for i in range(3)]


def iid_gap_readout_bound(gaps, center, endpoint):
    """Exploratory equal-weight iid gaps and passive independent Bernoulli sensors."""
    n = len(gaps)
    mean_gap = sum(gaps) / n
    mats = [transition_matrix(t) for t in gaps]
    M = [[sum(mat[i][j] for mat in mats) / n for j in range(3)]
         for i in range(3)]
    future = [sum(M[i][j] * endpoint[j] for j in range(3)) for i in range(3)]
    past = [sum(M[j][i] * endpoint[j] for j in range(3)) for i in range(3)]
    p_center = sum(center) / 3
    r = sum(center[i] * future[i] for i in range(3)) / (3 * p_center)
    r_past = sum(center[i] * past[i] for i in range(3)) / (3 * p_center)
    assert abs(r - r_past) < 1e-12
    joint = sum(center[i] * past[i] * future[i] for i in range(3)) / (3 * p_center)
    d = p_center * (r * r - joint)
    bound = -math.log1p(-d / (r * (1 - r))) / mean_gap if d > 0 else 0.0
    return r, d, bound


def grid_best(fn, start=1, stop=10000):
    return max((fn(k / 1000)[0] if isinstance(fn(k / 1000), tuple)
                else fn(k / 1000), k / 1000) for k in range(start, stop + 1))


if __name__ == "__main__":
    assert Fraction(21, 20) * Fraction(341, 400) / 3 == Fraction(2387, 8000)
    print("H'''(0) =", Fraction(2387, 8000))
    print("best positive third-difference grid bound, h =", grid_best(fd_bound))
    print("best ideal three-snapshot grid bound, t =", grid_best(conditional_snapshot_bound))
    print("three-snapshot at t=0.2:", conditional_snapshot_bound(0.2))
    print("best ideal two-snapshot grid bound, t =", grid_best(two_snapshot_bound))
    print("two-snapshot at t=2.5, 5% symmetric noise:",
          two_snapshot_bound(2.5, 0.05))
    print("geometric-path at t=0.3:", geometric_path_bound(0.3))
    print("geometric-path at t=0.001:", geometric_path_bound(0.001))
    print("geometric-path exact small-time limit:",
          Fraction(361, 1260), float(Fraction(361, 1260)))
    print("optimized geometric-path at t=0.3:",
          optimized_geometric_path_bound(0.3))
    print("optimized geometric-path exact small-time limit:",
          "(21 - 4 sqrt(5))/30",
          (21 - 4 * math.sqrt(5)) / 30)
    print("ring geometric submeasure check at t=0.3:",
          ring_geometric_submeasure_check(0.3))
    gaps = (0.2, 0.4)
    print("iid jitter, ideal sensors:",
          iid_gap_readout_bound(gaps, (0, 1, 1), (0, 1, 1)))
    print("iid jitter, 10% error at all sensors:",
          iid_gap_readout_bound(gaps, (0.1, 0.9, 0.9), (0.1, 0.9, 0.9)))
    print("iid jitter, 10% error at endpoints:",
          iid_gap_readout_bound(gaps, (0, 1, 1), (0.1, 0.9, 0.9)))
