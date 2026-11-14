"""Introduced local growth and global thickness diagnostics; no material data."""
import json
import math
from fractions import Fraction as Q


def f(x):
    return {"exact": str(x), "float": float(x)}


def local_metrics():
    h = Q(1, 5000)
    rows = []
    for name, kappas in [("plane", (Q(0), Q(0))),
                         ("cylindrical_point", (Q(500), Q(0))),
                         ("saddle_point", (Q(500), -Q(500))),
                         ("spherical_point", (Q(500), Q(500)))]:
        lower = [1 + 2 * h * k / 3 for k in kappas]
        upper = [1 - 2 * h * k / 3 for k in kappas]
        a = [(lower[i] + upper[i]) / 2 for i in range(2)]
        b = [3 * (lower[i] - upper[i]) / (4 * h) for i in range(2)]
        assert a == [1, 1] and b == list(kappas)
        mean = sum(kappas) / 2
        residual_squared = sum((k - mean) ** 2 for k in kappas)
        rows.append({"point_type": name, "principal_curvatures_per_m": [f(k) for k in kappas],
                     "lower_layer_metric_eigenvalues": [f(x) for x in lower],
                     "upper_layer_metric_eigenvalues": [f(x) for x in upper],
                     "all_metric_eigenvalues_positive": all(x > 0 for x in lower + upper),
                     "minimum_isotropic_curvature_mismatch_squared": f(residual_squared),
                     "scope": "Pointwise orthonormal target frame only; no global flat-metric assumption or isotropic-energy impossibility."})
    return {"introduced_total_thickness_m": float(h), "cases": rows}


def position(r, theta, a, offset):
    scale = math.hypot(r, a)
    normal = (a * math.sin(theta) / scale, -a * math.cos(theta) / scale, r / scale)
    mid = (r * math.cos(theta), r * math.sin(theta), a * theta)
    return tuple(mid[i] + offset * normal[i] for i in range(3))


def helicoid_case(pitch, h, r=0.015):
    a = pitch / (2 * math.pi)
    scale = math.hypot(r, a)
    kappa = a / (r * r + a * a)
    # Opposite normal offsets on neighboring turns intersect when
    # z*r/scale + a*atan(z*a/(r*scale)) = pitch/2.
    def gap(z):
        return z * r / scale + a * math.atan(z * a / (r * scale)) - pitch / 2
    witness = None
    if gap(h / 2) > 0:
        lo, hi = 0.0, h / 2
        for _ in range(90):
            m = (lo + hi) / 2
            if gap(m) > 0:
                hi = m
            else:
                lo = m
        z = (lo + hi) / 2
        delta = math.atan(z * a / (r * scale))
        theta_a, theta_b = math.pi, 3 * math.pi - 2 * delta
        pa = position(r, theta_a, a, z)
        pb = position(r, theta_b, a, -z)
        error = math.dist(pa, pb)
        assert 0 < z < h / 2 and error < 1e-14
        witness = {"normal_offset_m": z, "theta_a": theta_a, "theta_b": theta_b,
                   "point_a_m": pa, "point_b_m": pb, "intersection_error_m": error}
    local_metric_min = 1 - 2 * h * kappa / 3
    assert local_metric_min > 0
    return {"introduced_pitch_m": pitch, "introduced_thickness_m": h,
            "introduced_radius_m": r, "maximum_abs_curvature_at_radius_per_m": kappa,
            "minimum_relative_layer_metric_eigenvalue": local_metric_min,
            "local_SPD_condition_satisfied": True,
            "adjacent_turn_normal_fiber_intersection": witness,
            "scope": "An exhibited intersection is a global finite-thickness counterexample. No witness is not a general self-avoidance certificate."}


print(json.dumps({"status": "INTRODUCED_GEOMETRY_DIAGNOSTICS_NOT_A_MATERIAL_OR_NEW_THEOREM",
                  "local_growth": local_metrics(),
                  "global_thickness": [helicoid_case(p, 0.0002) for p in (0.0001, 0.0002, 0.0004, 0.001)],
                  "limits": ["The primary inverse-growth theorem is credited, not refuted.",
                             "Local positive metrics and compatible midsurfaces do not certify a finite-thickness self-avoiding body.",
                             "No prepared growth field, actuation, constitutive coefficient, manufactured bilayer or global trajectory is supplied.",
                             "No producer code, linked SI or unavailable source was recovered or executed."]}, indent=2))
