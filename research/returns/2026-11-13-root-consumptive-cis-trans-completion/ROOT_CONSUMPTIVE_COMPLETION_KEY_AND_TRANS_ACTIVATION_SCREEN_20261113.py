"""Introduced product-key transfer model; no measured chemistry or design qualification.
All rate constants, geometry, concentrations and inventory assumptions below are
introduced. The CTMC is an independent ROOT calculation, not producer code.
"""
import json, math, pathlib

OUT = pathlib.Path(__file__).with_suffix(".json")

def poisson_step(v, duration, k_cis, release, trap, trap_access):
    # Row-vector transient CTMC plus accumulated occupation of accessible key.
    # U -> C is intended first progression; U -> X is premature trap loss.
    # C -> F makes the used key accessible; F -> T quenches it.
    q = max(k_cis + trap_access * trap, release, trap)
    if q == 0:
        return list(v), duration * v[2]
    x = q * duration
    assert x <= 10.00000001
    p = list(v)
    reward = 0.0
    weight = math.exp(-x)
    mass = weight
    result = [weight * y for y in p]
    occupation = 0.0
    for n in range(1, 200):
        u, bound, free, trapped, lost = p
        next_p = [
            u * (1 - (k_cis + trap_access * trap) / q),
            bound * (1 - release / q) + u * k_cis / q,
            free * (1 - trap / q) + bound * release / q,
            trapped + free * trap / q,
            lost + u * trap_access * trap / q,
        ]
        reward += free / q
        p = next_p
        weight *= x / n
        mass += weight
        for j in range(5):
            result[j] += weight * p[j]
        occupation += weight * reward
        if n > x + 20 and weight < 1e-18:
            break
    assert abs(mass - 1) < 5e-14
    assert min(result) >= -1e-14
    # Remove accumulated floating-point mass drift at each exact-mass step.
    result_mass = math.fsum(result)
    assert abs(result_mass - 1) < 5e-14
    return [y / result_mass for y in result], occupation / result_mass

def coupled_gate(k_cis, release, trap, trap_access, window=60.0,
                 catalytic_rate=1.0, initially_correct_fraction=0.1):
    q = max(k_cis + trap_access * trap, release, trap)
    steps = max(1, math.ceil(q * window / 10))
    duration = window / steps
    v = [1., 0., 0., 0., 0.]
    occupation = 0.
    for _ in range(steps):
        v, extra = poisson_step(v, duration, k_cis, release, trap, trap_access)
        occupation += extra
    g = initially_correct_fraction
    hazard = g / (1 - g) * catalytic_rate * occupation
    return {
        "k_cis_per_s": k_cis, "used_key_release_per_s": release,
        "trap_per_s": trap, "trap_access_before_cis": trap_access,
        "window_s": window, "catalytic_rate_per_accessible_key_s": catalytic_rate,
        "initially_correct_fraction": g,
        "intended_progression_probability": v[1] + v[2] + v[3],
        "unprogressed_probability": v[0],
        "premature_trap_loss_probability": v[4],
        "used_key_accessible_occupation_s_per_initial_good_site": occupation,
        "false_progression_fraction_of_initial_bad_sites_mean_field":
            -math.expm1(-hazard),
        "end_states_U_C_F_T_X": v,
        "uniformization_subintervals": steps,
    }

def all_used_keys_at_start(release, trap, window):
    # Closed-form post-progression occupation: conservative earlier-release
    # comparison, NOT the joint gate trajectory.
    if trap == 0:
        return window + math.expm1(-release * window) / release if release else 0.
    def integral_exp(r):
        return -math.expm1(-r * window) / r if r else window
    if abs(trap - release) < 1e-14:
        return (1 - math.exp(-release * window) *
                (1 + release * window)) / release
    return release / (trap - release) * (
        integral_exp(release) - integral_exp(trap))

def single_use(k_cis, k_trans, window=60., fraction=0.1):
    total = k_cis + k_trans
    reacted = -math.expm1(-total * window) if total else 0.
    correct = k_cis / total * reacted if total else 0.
    wrong = k_trans / total * reacted if total else 0.
    # One consumed key has at most ONE transfer in this declared model.
    count_bound = fraction / (1 - fraction) * wrong
    return {
        "k_cis_per_s": k_cis, "k_trans_total_per_s": k_trans,
        "window_s": window, "correct_first_progression": correct,
        "wrong_first_progression": wrong,
        "false_fraction_count_upper_bound": min(1., count_bound),
        "false_fraction_mean_field_random_target_allocation":
            -math.expm1(-count_bound),
        "assumption": "both cut fragments are permanently inactive; no reassembly or residual catalysis",
    }

def ceff_molar(radius_nm):
    radius_m = radius_nm * 1e-9
    volume_litre = (4 / 3) * math.pi * radius_m ** 3 * 1000
    return 1 / (6.02214076e23 * volume_litre)

def run():
    cases = []
    for release, trap, access in [
        (.01, 0., 0.), (.01, 1., 0.), (.01, 100., 0.),
        (.01, 100., 1e-6), (.01, 100., 1e-4),
        (1e-6, 0., 0.), (.01, 1000., 1e-4),
    ]:
        case = coupled_gate(.1, release, trap, access)
        bound = all_used_keys_at_start(release, trap, 60.)
        case["post_cis_at_time_zero_occupation_bound_s"] = bound
        assert case["used_key_accessible_occupation_s_per_initial_good_site"] <= bound + 1e-10
        cases.append(case)
    # Independent analytic limit comparisons, not hardware tests.
    zero_release = coupled_gate(.1, 0., 0., 0.)
    assert abs(zero_release["intended_progression_probability"] -
               (-math.expm1(-6))) < 1e-12
    assert zero_release["false_progression_fraction_of_initial_bad_sites_mean_field"] == 0
    for c in cases:
        a = c["k_cis_per_s"] + c["trap_per_s"] * c["trap_access_before_cis"]
        intended = c["k_cis_per_s"] / a * (-math.expm1(-a * c["window_s"]))
        assert abs(intended - c["intended_progression_probability"]) < 2e-12
        assert abs(sum(c["end_states_U_C_F_T_X"]) - 1) < 2e-12
    geometric = []
    for radius in [10., 20., 30.]:
        eff = ceff_molar(radius)
        competitor = 1e-6
        ratio = competitor / eff
        geometric.append({
            "radius_nm": radius, "uniform_sphere_effective_molarity_M": eff,
            "competing_target_M": competitor,
            "equal_rate_constant_wrong_first_hit_probability": ratio / (1 + ratio),
            "single_use_screen": single_use(.1, .1 * ratio),
        })
    # Stocks are introduced counts and average 330 g/mol per nucleotide,
    # not a chemical synthesis yield, procurement quote or chemical lower bound.
    sites_nmole, steps, key_nt, nucleotide_mw = 32., 20, 25, 330.
    minimum_success_key_nmole = sites_nmole * steps
    data = {
        "scope": "introduced abiotic-manufacturing control model; no sequence design, chemistry fit, experimental validation or novelty claim",
        "catalytic_transfer_model": {
            "description": "U->C at kc; U->X at alpha*c; C->F at b; F->T at c. Free used key remains catalytic. Bad-site hazard is g/(1-g)*mu*F in an introduced well-mixed macroscopic limit.",
            "cases": cases,
            "limits": "release, mixing, binding, fragment inactivity, trap selectivity, hidden wrong chemistry and other false enzyme substrates are unqualified physical operations",
        },
        "consumptive_key_model": {
            "cases": geometric,
            "limits": "one-use removes repeated transfer only; it does not guarantee the first transfer is cis, authenticate the intended bond, block premature substrates or regenerate the scaffold",
        },
        "inventory": {
            "initial_sites_nmole": sites_nmole, "extensions_per_site": steps,
            "introduced_key_nucleotides": key_nt,
            "success_only_key_nmole": minimum_success_key_nmole,
            "success_only_key_mass_mg": minimum_success_key_nmole * 1e-9 * key_nt * nucleotide_mw * 1000,
            "three_attempt_all_sites_key_mass_mg": minimum_success_key_nmole * 3e-9 * key_nt * nucleotide_mw * 1000,
            "retention_after_600_events_at_loss_0_003": .997**600,
            "maximum_loss_per_600_events_for_0_95_retention": -math.expm1(math.log(.95)/600),
            "per_step_hidden_error_for_0_9_full_20step_fidelity": -math.expm1(math.log(.9)/20),
        },
        "verification": "uniformization mass conservation and exact zero-release/intended-progression limits checked; no external dependency or producer artifact",
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps({
        "catalytic_cases": [{k: c[k] for k in (
            "used_key_release_per_s", "trap_per_s", "trap_access_before_cis",
            "intended_progression_probability",
            "false_progression_fraction_of_initial_bad_sites_mean_field")} for c in cases],
        "geometry": [{"radius_nm": c["radius_nm"], "effective_M": c["uniform_sphere_effective_molarity_M"],
                      "single_use": c["single_use_screen"]} for c in geometric],
        "inventory": data["inventory"], "output": str(OUT)}, indent=2))

if __name__ == "__main__":
    run()
