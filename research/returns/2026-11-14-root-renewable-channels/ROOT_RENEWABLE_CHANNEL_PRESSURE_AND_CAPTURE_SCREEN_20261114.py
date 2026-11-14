"""ROOT-owned conditional mechanics, not a source fit or a physical experiment.

The pressure-bearing wall is an INTRODUCED thin elastic shell, not an asserted
property of a jammed liquid interface. No producer code or source data is used.
Standard library only; serial, bounded work. SI units internally.
"""

import itertools
import json
import math
from pathlib import Path


MU = 0.001
PROOF = 60000.0


def radius(p, r0, ys):
    """Linear hoop resultant N=Ys*(r/r0-1); p*r=N, ignoring axial/bending.

    This is a constitutive MODEL for p>=0 and p*r0<Ys. Algebra outside a
    small-strain region is reported but not a physical continuation certificate.
    """
    if p < 0 or p * r0 >= ys:
        raise ValueError("outside the declared nonnegative finite-radius domain")
    return r0 / (1.0 - p * r0 / ys)


def primitive(p, r0, ys):
    """Integral from 0 to p of r(s)^4 ds, with stable small-p evaluation."""
    c = r0 / ys
    if p < 0 or c * p >= 1:
        raise ValueError("outside primitive domain")
    return r0**4 * math.expm1(-3.0 * math.log1p(-c * p)) / (3.0 * c)


def flow(pin, pout, length, r0, ys):
    return math.pi * (primitive(pin, r0, ys) - primitive(pout, r0, ys)) / (8 * MU * length)


def bisect_increasing(f, target, lo, hi):
    if not f(lo) <= target <= f(hi):
        raise ValueError("target not bracketed")
    for _ in range(90):
        mid = (lo + hi) / 2
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def splitter(q_ml_min, r_a, ys_a, r_b, ys_b, trunk_r, trunk_ys):
    """10mm trunk, 40mm low-flow arm, 10mm high-flow arm, equal outlets.

    This hydraulic graph specifies no 3D embedding, port bond or writer route.
    All complete paths are at least 20mm. Fixed outer bath gauge pressure is 0.
    """
    q = q_ml_min * 1e-6 / 60
    ceiling = 0.8 * min(ys_a / r_a, ys_b / r_b, trunk_ys / trunk_r)
    branch_sum = lambda p: flow(p, 0, 0.04, r_a, ys_a) + flow(p, 0, 0.01, r_b, ys_b)
    pn = bisect_increasing(branch_sum, q, 0, ceiling)
    pi = bisect_increasing(lambda p: flow(p, pn, 0.01, trunk_r, trunk_ys), q, pn, ceiling)
    qa = flow(pn, 0, 0.04, r_a, ys_a)
    qb = flow(pn, 0, 0.01, r_b, ys_b)
    return {
        "q_ml_min": q_ml_min,
        "inlet_pa": pi,
        "node_pa": pn,
        "low_to_high_ratio": qa / qb,
        "relative_ratio_error": qa / qb / 0.25 - 1,
        "flow_balance_m3_s": qa + qb - q,
        "maximum_model_hoop_strain": max(
            radius(pn, r_a, ys_a) / r_a - 1,
            radius(pn, r_b, ys_b) / r_b - 1,
            radius(pi, trunk_r, trunk_ys) / trunk_r - 1,
        ),
    }


def simpson(f, a, b, n):
    assert n % 2 == 0
    h = (b - a) / n
    v = f(a) + f(b)
    v += 4 * sum(f(a + i * h) for i in range(1, n, 2))
    v += 2 * sum(f(a + i * h) for i in range(2, n, 2))
    return h * v / 3


def bath_account(g, compliance, p, duration):
    """Two permeable walls feed a shared closed compliant bath.

    Fixed useful-channel gauges are p and 0; each wall conductance is g.
    C*dp_b/dt=g*(p-p_b)-g*p_b. The bath is not reset at the endpoint.
    Pressure-volume compliance and conductance are introduced linear laws.
    """
    rate = 2 * g / compliance
    e = -math.expm1(-rate * duration)
    pb = p / 2 * e
    v_in = g * p * duration / 2 + compliance * p * e / 4
    v_cross = g * p * duration / 2 - compliance * p * e / 4
    storage = compliance * pb**2 / 2
    work = p * v_in
    # Integral of G*((p-pb)^2+pb^2); exact exponential form.
    dissipation = g * p**2 / 2 * (
        duration + (-math.expm1(-2 * rate * duration)) / (2 * rate)
    )
    return {
        "g_m3_s_pa": g,
        "compliance_m3_pa": compliance,
        "p_drive_pa": p,
        "duration_s": duration,
        "time_constant_s": 1 / rate,
        "final_bath_pa": pb,
        "inflow_ml": v_in * 1e6,
        "crossflow_ml": v_cross * 1e6,
        "bath_stored_volume_ml": compliance * pb * 1e6,
        "volume_residual_m3": v_in - v_cross - compliance * pb,
        "pressure_work_j": work,
        "dissipation_j": dissipation,
        "terminal_stored_energy_j": storage,
        "energy_residual_j": work - dissipation - storage,
        "terminal_crossflow_ml_min": g * pb * 1e6 * 60,
        "crossflow_fraction_of_5ml_min": g * pb / (5e-6 / 60),
        "required_finite_fresh_feed_for_5ml_min_ml": 5 * duration / 60,
    }


def main():
    # None of these simultaneous geometry/material values is source-qualified.
    r0 = 0.00025
    ys = 200.0
    wall_t = 5e-6
    nominal = [splitter(q, r0, ys, r0, ys, r0, ys) for q in (5, 10, 15)]
    corners = []
    for radial_fraction in (0.01, 0.025):
        rows = []
        for sa, sb, ya, yb, q in itertools.product((-1, 1), (-1, 1), (-1, 1), (-1, 1), (5, 10, 15)):
            row = splitter(q, r0*(1+sa*radial_fraction), ys*(1+ya*0.2),
                           r0*(1+sb*radial_fraction), ys*(1+yb*0.2), r0, ys)
            row.update(radial_fraction=radial_fraction, radius_signs=[sa, sb], stiffness_signs=[ya, yb])
            rows.append(row)
        # A separate continuous-box argument, not inference from these 48 cases.
        # r(p) increases with r0 and decreases with Ys. At Q<=15 the largest
        # possible branch-node pressure is obtained with BOTH arms rmin,Ymax.
        rmin, rmax = r0*(1-radial_fraction), r0*(1+radial_fraction)
        ymin, ymax = 0.8*ys, 1.2*ys
        slow = splitter(15, rmin, ymax, rmin, ymax, r0, ys)
        pmax = slow["node_pa"]
        # The ratio of largest/smallest admissible r(p) increases with p.
        # Bounding the pointwise ratio bounds the ratio of its positive integrals.
        kappa = radius(pmax, rmax, ymin) / radius(pmax, rmin, ymax)
        upper_ratio_factor = kappa**4
        class_bound = {"flow_interval_ml_min": [5, 15],
                       "independent_ys_interval_n_m": [ymin, ymax],
                       "independent_radius_interval_m": [rmin, rmax],
                       "node_pressure_upper_pa": pmax,
                       "inlet_pressure_upper_pa": slow["inlet_pa"],
                       "normalised_ratio_factor_interval": [1/upper_ratio_factor, upper_ratio_factor],
                       "maximum_absolute_ratio_error_bound": upper_ratio_factor-1,
                       "within_10percent_ratio_contract_IN_MODEL": upper_ratio_factor <= 1.1}
        assert max(abs(x["relative_ratio_error"]) for x in rows) <= upper_ratio_factor-1
        assert max(x["inlet_pa"] for x in rows) <= slow["inlet_pa"]*(1+1e-12)
        corners.append({"radial_fraction": radial_fraction, "cases": len(rows),
                        "maximum_absolute_ratio_error": max(abs(x["relative_ratio_error"]) for x in rows),
                        "maximum_inlet_pa": max(x["inlet_pa"] for x in rows),
                        "continuous_box_argument": class_bound,
                        "rows": rows})

    proof_rows = []
    for rr, yy in itertools.product((0.00015, 0.00025, 0.0005), (50.0, 100.0, 200.0)):
        rp = radius(PROOF, rr, yy)
        strain = rp / rr - 1
        proof_rows.append({"rest_radius_m": rr, "ys_n_m": yy,
                           "proof_pa": PROOF, "radius_m": rp,
                           "strain": strain, "hoop_resultant_n_m": PROOF * rp,
                           "stress_if_5um_pa": PROOF * rp / wall_t,
                           "inside_10percent_model_diagnostic": strain <= 0.1})

    pressure = 60000.0
    strain_limit = 0.1
    required_ys = pressure * r0 * (1 + 1 / strain_limit)
    capture = []
    for k in (0.01, 0.1, 1.0):
        wait = -math.log1p(-required_ys / ys) / k
        capture.append({"introduced_assembly_rate_per_s": k,
                        "ys_required_n_m": required_ys,
                        "wait_s": wait,
                        "check_ys_n_m": ys * (-math.expm1(-k * wait)),
                        "pressure_on_before_wait_has_no_10percent_certificate": True})

    # A viscous external bath slows deformation but supplies no static elasticity.
    # For a long cylindrical cavity in a Newtonian external bath, neglecting end
    # effects and interfacial tension, 2*mu_ext*d(log r)/dt=delta_p.
    viscous = [{"mu_ext_pa_s": m, "delta_p_pa": p,
                "time_to_10percent_radius_growth_s": 2*m*math.log(1.1)/p}
               for m, p in itertools.product((1.0, 60.0, 1000.0), (1000.0, 20000.0, 60000.0))]

    # A separate pure-tension scale is not a jammed-interface constitutive law.
    gamma = 0.03
    capillary = {"introduced_gamma_n_m": gamma, "cylindrical_laplace_pa": gamma/r0,
                 "use_nominal_10ml_min_pa": nominal[1]["inlet_pa"],
                 "proof_hoop_force_over_gamma": PROOF*r0/gamma,
                 "not_a_rupture_prediction_for_an_elastic_or_jammed_wall": True}

    # Analytical vs numerical quadrature; this checks algebra, not a device.
    integral_checks = []
    for p in (100.0, 2000.0, 20000.0, 60000.0):
        exact = primitive(p, r0, ys)
        integral_checks.append({"pressure_pa": p, "exact_m4_pa": exact,
                                "relative_quadrature_errors": [
                                    simpson(lambda s: radius(s, r0, ys)**4, 0, p, n)/exact - 1
                                    for n in (32, 64, 128)]})

    # Short-time energy integral to independently check finite retained bath energy.
    bath = [bath_account(g, 1e-12, 5000.0, 24*3600.0) for g in (1e-13, 1e-12)]
    short = bath_account(1e-13, 1e-12, 5000.0, 20.0)
    g = short["g_m3_s_pa"]
    c = short["compliance_m3_pa"]
    p = short["p_drive_pa"]
    pb = lambda t: p/2 * (-math.expm1(-2*g*t/c))
    short["independent_dissipation_quadrature_relative_errors"] = [
        simpson(lambda t: g*((p-pb(t))**2+pb(t)**2), 0, 20.0, n)/short["dissipation_j"]-1
        for n in (64, 128, 256)]

    result = {"scope": "INTRODUCED conditional models; zero physical fabrication, tests or qualified material points",
              "source_fit": False,
              "nominal_r0_m": r0, "nominal_ys_n_m": ys, "wall_thickness_m": wall_t,
              "E_if_Ys_equals_Et_pa": ys/wall_t,
              "wall_volume_thin_shell_mm3": 2*math.pi*r0*0.06*wall_t*1e9,
              "water_volume_rest_mm3": math.pi*r0*r0*0.06*1e9,
              "nominal_splitter": nominal, "independent_branch_corners": corners,
              "proof_screens": proof_rows, "capture_before_proof": capture,
              "viscous_only_cavity": viscous, "pure_tension_scale": capillary,
              "primitive_quadrature": integral_checks,
              "shared_bath_24h": bath, "shared_bath_short_check": short,
              "unconstructed": ["actual wall formulation and joint constitutive domain",
                                "nonplanar geometry and axial/bending/stability/fracture",
                                "port bonds, branches, anchors and 60kPa five-minute endurance",
                                "through-port writer and residue-free removal/renewal",
                                "installed pressure/flow/cleanliness observations",
                                "100 continuous services, stock capacity and whole advantage"]}
    # Meaningful invariant checks, with arithmetic rather than physical tolerances.
    assert max(abs(x["flow_balance_m3_s"]) for x in nominal) < 1e-19
    assert max(abs(x["relative_ratio_error"]) for x in nominal) < 1e-12
    assert max(abs(v) for row in integral_checks for v in row["relative_quadrature_errors"][-1:]) < 1e-9
    for row in bath + [short]:
        assert abs(row["volume_residual_m3"]) < 1e-16
        assert abs(row["energy_residual_j"]) < 1e-12
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    compact = {"output": str(out), "nominal": nominal,
               "corner_summary": [{k: v for k, v in row.items() if k != "rows"} for row in corners],
               "chosen_proof": next(x for x in proof_rows if x["rest_radius_m"] == r0 and x["ys_n_m"] == ys),
               "capture": capture, "shared_bath": bath,
               "maximum_last_quadrature_error": max(abs(x["relative_quadrature_errors"][-1]) for x in integral_checks)}
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
