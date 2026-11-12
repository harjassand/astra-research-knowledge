"""ROOT-owned bounded models; no producer code or measured-device inference.

Run with Python standard library. Parameters marked introduced are hypotheses.
The 8%/4h scalar is only an aggregate diagnostic of a published batch result,
not a measured steady-state biosynthetic capacity or per-protein renewal map.
"""
import json
import math


def solve(matrix, rhs):
    a = [list(row) + [b] for row, b in zip(matrix, rhs)]
    n = len(rhs)
    scale = max(abs(v) for row in matrix for v in row)
    for col in range(n):
        pivot = max(range(col, n), key=lambda j: abs(a[j][col]))
        if abs(a[pivot][col]) < 1e-12 * scale:
            raise ValueError("singular: a connected graph need not be load stable")
        a[pivot], a[col] = a[col], a[pivot]
        q = a[col][col]
        a[col] = [v / q for v in a[col]]
        for j in range(n):
            if j != col:
                q = a[j][col]
                a[j] = [x - q * y for x, y in zip(a[j], a[col])]
    return [row[-1] for row in a]


def structure(edges):
    # Introduced 1m square, left two nodes fixed, linear pin-jointed bars.
    # EA=1e6 N; 100N downward on lower-right node; no real joint qualification.
    points = [(0., 0.), (0., 1.), (1., 0.), (1., 1.)]
    k = [[0.] * 4 for _ in range(4)]
    records = []
    for i, j in edges:
        dx, dy = [b - a for a, b in zip(points[i], points[j])]
        length = math.hypot(dx, dy)
        direction = (dx / length, dy / length)
        b = [0.] * 4
        for node, sign in [(i, -1), (j, 1)]:
            if node >= 2:
                for axis in range(2):
                    b[2 * (node - 2) + axis] += sign * direction[axis]
        stiffness = 1e6 / length
        for m in range(4):
            for n in range(4):
                k[m][n] += stiffness * b[m] * b[n]
        records.append((i, j, stiffness, b))
    try:
        u = solve(k, [0., -100., 0., 0.])
    except ValueError as e:
        return {"stable_in_linear_model": False, "reason": str(e)}
    forces = [{"edge": [i, j], "axial_N": stiffness * sum(x*y for x, y in zip(b, u))}
              for i, j, stiffness, b in records]
    residual = max(abs(sum(k[m][n] * u[n] for n in range(4)) - [0., -100., 0., 0.][m])
                   for m in range(4))
    return {"stable_in_linear_model": True, "displacements_m": u,
            "max_component_displacement_mm": max(map(abs, u)) * 1000,
            "bar_forces": forces, "equilibrium_residual_N": residual}


def recovery_cycle():
    # A connection graph remains connected after removing the only diagonal,
    # but loses stiffness. A physically available alternate diagonal bypasses it.
    base = [(0, 2), (1, 3), (2, 3)]
    primary, bypass = (0, 3), (1, 2)
    stages = {
        "healthy": structure(base + [primary]),
        "unsafe_connected_removal": structure(base),
        "install_and_verify_bypass": structure(base + [primary, bypass]),
        "remove_primary_under_bypass": structure(base + [bypass]),
        "restore_primary": structure(base + [primary, bypass]),
        "remove_and_recover_bypass": structure(base + [primary]),
    }
    assert not stages["unsafe_connected_removal"]["stable_in_linear_model"]
    assert all(s["stable_in_linear_model"] for n, s in stages.items()
               if n != "unsafe_connected_removal")
    assert all(s.get("equilibrium_residual_N", 0) < 1e-8 for s in stages.values())
    return {"scope": "Introduced static truss only; installation access, preload, contact, robot loads, fatigue and dynamics unqualified",
            "stages": stages,
            "local_sensor_ambiguity": {
                "healthy_and_jammed_fixture_introduced_stiffness_N_m": 1e6,
                "probe_force_N": 50., "same_measured_displacement_um": 50.,
                "implication": "one force/displacement port cannot identify which load path carries the probe; fixture unloading and additional physical witnesses are operations"}}


def fault_scale():
    counts = [(478, 10, 7), (14185, 218, 118), (711, 46, 30), (596, 33, 7)]
    ops, faults, touches = [sum(x[j] for x in counts) for j in range(3)]
    target_ops, success = 100000, .95
    target_p = -math.expm1(math.log(success) / target_ops)
    # Not fitted to ARMADAS. Permanent faults invalidate independent retry powers.
    transient, permanent, failed_replacement = .01, .0002, .001
    cases = []
    for retries in [1, 2, 3, 4]:
        retry_only = permanent + (1-permanent) * transient**retries
        replace = permanent*failed_replacement + (1-permanent)*transient**retries
        cases.append({"independent_transient_tries": retries,
                      "retry_only_residual": retry_only,
                      "retry_only_mission_success": math.exp(target_ops * math.log1p(-retry_only)),
                      "introduced_replacement_residual": replace,
                      "introduced_replacement_mission_success": math.exp(target_ops * math.log1p(-replace))})
    return {"observed_source_counts": {"ops": ops, "mechanical_faults": faults, "touch_recoveries": touches},
            "observed_touches_per_listed_op": touches/ops,
            "iid_illustration_only_target_ops": target_ops,
            "iid_illustration_only_target_success": success,
            "iid_required_unrecovered_probability": target_p,
            "ratio_observed_touch_rate_to_iid_target": touches/ops/target_p,
            "introduced_mixture": {"transient": transient, "permanent": permanent,
                                   "replacement_failure": failed_replacement, "cases": cases},
            "limits": "source faults correlated; tether/communications excluded; counts are no mission reliability estimate"}


def renewal():
    capacity = .08 / 4  # introduced uniform diagnostic, not a measured flux
    cases = []
    for half_life in [20, 50, 100, 200]:
        delta = math.log(2) / half_life
        for inactive_limit in [.5, 1., 3.]:
            for selectivity in [1., 10.]:
                # Active P held at 1. Inactive formation delta*P.
                # Inactive clearance is selectivity*b; active loss b.
                b = delta/(selectivity*inactive_limit)
                maintenance = delta+b
                cases.append({"introduced_active_half_life_h": half_life,
                              "introduced_max_inactive_over_active": inactive_limit,
                              "introduced_inactive_vs_active_clearance_selectivity": selectivity,
                              "minimum_active_purge_h_inv": b,
                              "maintenance_mass_per_initial_active_mass_h": maintenance,
                              "remaining_scalar_payload_capacity": capacity-maintenance,
                              "scalar_capacity_closes": capacity >= maintenance})
    delta = math.log(2)/50
    return {"published_batch_mass_only": {"starting_nonribosome_ug": 350, "recovered_nonribosome_ug": 28},
            "introduced_uniform_capacity_h_inv": capacity,
            "nonselective_purge_with_inactive_ratio_at_most_half_requires_half_life_h": math.log(2)*3/capacity,
            "zero_purge_50h_half_life_inactive_over_maintained_active_at_100h": 100*delta,
            "cases": cases,
            "essential_vector_contract": "for EVERY essential i, viable functional production vi >= (deactivation_i + active_export_i)*Pi; RNA/ribosomes and waste have their own balances",
            "limits": "mass average not species capacity, activity, folding, retention, RNA/ribosome renewal or material qualification"}


def brine_ledger():
    output = 10*8760*.9
    crf = .08/(1-1.08**-20)
    cap, power, cost = 1525296., 8.943, 4.496
    capital = cap*crf/output
    electricity = power*.08
    remaining = cost-capital-electricity
    return {"unchanged_producer_favorable_ledger_only": True,
            "annual_tonnes": output, "capital_recovery_factor": crf,
            "capital_USD_t": capital, "electricity_USD_t": electricity,
            "remaining_USD_t": remaining,
            "free_initial_capital_only_USD_t": cost-capital,
            "free_electricity_only_USD_t": cost-electricity,
            "free_initial_capital_and_electricity_USD_t": remaining,
            "smaller_campaign_kWh_t": 94.375/4,
            "larger_surface_renewal_still_in_remaining": True,
            "limits": "not a universal separation bound; changing mechanism may change several lines together"}


def obtainable_stock_screen():
    # Actual maker catalogue dimensions/stock mass only. E and pinned ends are
    # introduced surrogates, not a material certificate or assembled-frame test.
    diameter, wall, modulus = .020, .0016, 70e9
    area = math.pi/4*(diameter**2-(diameter-2*wall)**2)
    inertia = math.pi/64*(diameter**4-(diameter-2*wall)**4)
    return {"maker_catalogue": "Capral EX5008 / 814025, 6060 T5, 20x1.6mm, 6.5m, 1.625kg",
            "introduced_E_Pa": modulus, "area_m2": area, "I_m4": inertia,
            "EA_N": modulus*area,
            "introduced_pinned_Euler_load_at_sqrt2_m_N": math.pi**2*modulus*inertia/2,
            "nominal_axial_stress_at_100sqrt2_N_Pa": math.sqrt(2)*100/area,
            "raw_stock_frame_plus_bypass_mass_kg": (3+2*math.sqrt(2))*1.625/6.5,
            "limits": "no joint/eccentricity/end-fixity/local-buckling/fatigue/tolerance/robot-load qualification; mass excludes joints and machinery"}


if __name__ == "__main__":
    print(json.dumps({"recovery": recovery_cycle(), "fault_scale": fault_scale(),
                      "molecular_renewal": renewal(), "brine": brine_ledger(),
                      "obtainable_stock": obtainable_stock_screen()}, indent=2))
