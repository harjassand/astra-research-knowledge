#!/usr/bin/env python3
"""Small continuum prestress audit; all material numbers are illustrative.

Run with Python 3; standard library only. No files are written. These checks
verify arithmetic/model identities, not material feasibility or device safety.
"""
import json
import math


def laminate(P, tc, Ec, nuc, Mr, ratio):
    Mc = Ec / (1 - nuc)
    compliance = 1 / Mc + 1 / (ratio * Mr)
    return {
        "core_biaxial_modulus_Pa": Mc,
        "total_skin_to_core_thickness_ratio": ratio,
        "skin_tension_Pa": P / ratio,
        "required_eigenstrain_mismatch": P * compliance,
        "stored_elastic_energy_J_per_m2": P * P * tc * compliance,
        "skin_conductivity_over_core_for_20pct_added_ASR": ratio / 0.2,
        "elastic_cooling_delta_T_for_CTE_difference_5e-6_K": P * compliance / 5e-6,
    }


def ring(P, Ec, nuc, Er, nur, allowable_hoop):
    assert allowable_hoop > P
    f = (allowable_hoop - P) / (allowable_hoop + P)
    hoop = P * (1 + f) / (1 - f)
    delta_over_a = P * ((1 - nuc) / Ec + ((1 + f) / (1 - f) + nur) / Er)
    return {
        "allowable_principal_hoop_tension_Pa": allowable_hoop,
        "core_area_fraction_within_ring": f,
        "hex_packed_device_active_fraction_upper_bound": math.pi / (2 * math.sqrt(3)) * f,
        "peak_hoop_Pa": hoop,
        "inner_edge_von_Mises_Pa": math.sqrt(hoop**2 + P**2 + hoop * P),
        "required_radial_interference_fraction": delta_over_a,
    }


def von_mises_ring_fill(P, Y):
    assert Y > math.sqrt(3) * P
    allowable_hoop = (math.sqrt(4 * Y**2 - 3 * P**2) - P) / 2
    f = (allowable_hoop - P) / (allowable_hoop + P)
    return f, allowable_hoop


def square_buckling(E, nu, thickness, side):
    """Equal biaxial compression; isotropic simply supported Kirchhoff plate."""
    return math.pi**2 * E / (6 * (1 - nu**2)) * (thickness / side)**2


def main():
    P, tc, Ec, nuc = 330e6, 20e-6, 150e9, 0.25
    Mr, Er, nur, ratio = 250e9, 250e9, 0.25, 0.33
    lam = laminate(P, tc, Ec, nuc, Mr, ratio)
    rings = [ring(P, Ec, nuc, Er, nur, S) for S in (1e9, 2e9, 5e9)]
    checks = 0

    def check(condition):
        nonlocal checks
        assert condition
        checks += 1

    check(math.isclose(lam["skin_tension_Pa"] * ratio, P, rel_tol=1e-12))
    check(math.isclose(lam["required_eigenstrain_mismatch"], 0.00565, rel_tol=1e-12))
    check(math.isclose(lam["stored_elastic_energy_J_per_m2"], 37.29, rel_tol=1e-12))
    # Axisymmetric ring has angle-averaged sigma_xx=(sigma_rr+sigma_tt)/2=A.
    # Its area-integrated tensile xx stress exactly balances the disk's -P.
    a = 1.0
    for row in rings:
        f = row["core_area_fraction_within_ring"]
        b = a / math.sqrt(f)
        A = P * a*a / (b*b - a*a)
        B = A * b*b
        check(math.isclose(-P*math.pi*a*a + A*math.pi*(b*b-a*a), 0, abs_tol=1e-6))
        check(math.isclose(A - B / a**2, -P, rel_tol=1e-12))
        check(math.isclose(A - B / b**2, 0, abs_tol=1e-6))
        check(math.isclose(A + B / a**2, row["peak_hoop_Pa"], rel_tol=1e-12))
        check(math.isclose(row["peak_hoop_Pa"], row["allowable_principal_hoop_tension_Pa"], rel_tol=1e-12))

    vm_f, vm_hoop = von_mises_ring_fill(P, 2e9)
    check(math.isclose(vm_hoop**2 + P*vm_hoop + P**2, (2e9)**2, rel_tol=1e-12))
    check(vm_f < rings[1]["core_area_fraction_within_ring"])
    side_crit = tc * math.sqrt(math.pi**2 * Ec / (6 * (1 - nuc**2) * P))
    check(math.isclose(square_buckling(Ec, nuc, tc, side_crit), P, rel_tol=1e-12))
    D = Ec * tc**3 / (12 * (1 - nuc**2))
    foundation_k = (P * tc)**2 / (4 * D)
    check(math.isclose(2 * math.sqrt(D * foundation_k) / tc, P, rel_tol=1e-12))
    # Equal thermal eigenstrains supply no prestress in a free laminate.
    compliance = 1 / (Ec / (1 - nuc)) + 1 / (ratio * Mr)
    check(0 / compliance == 0)
    retention_time_multiplier = 1 / (-math.log(0.9))
    check(math.isclose(math.exp(-1 / retention_time_multiplier), 0.9, rel_tol=1e-12))
    print(json.dumps({
        "status": "ILLUSTRATIVE_CONTINUUM_ARITHMETIC_ONLY",
        "passed_checks": checks,
        "P_Pa": P, "core_thickness_m": tc,
        "laminate": lam, "rings": rings,
        "ring_fill_for_von_Mises_yield_2GPa": vm_f,
        "simply_supported_square_critical_side_m": side_crit,
        "square_buckling_Pa_at_1mm": square_buckling(Ec, nuc, tc, 1e-3),
        "square_buckling_Pa_at_10mm": square_buckling(Ec, nuc, tc, 1e-2),
        "core_plate_flexural_rigidity_Nm": D,
        "bilateral_Winkler_k_N_per_m3_to_match_P": foundation_k,
        "Maxwell_tau_over_service_time_for_90pct_retention": retention_time_multiplier,
    }, indent=2))


if __name__ == "__main__":
    main()
