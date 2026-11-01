#!/usr/bin/env python3
"""Resource and identifiability tests for programmable repairable matter.

This is an analytically solved toy model, not a calibrated molecular simulation.
It deliberately gives the repair mechanism no oracle for a damaged chemical
payload whose address-bearing recognition domain remains intact. Standard library
only. Run: python discriminating_test.py > results.json
"""
import json
import math


def majority_error(copies, independent_error, common_mode_error=0.0):
    """Odd repetition code; common-mode event flips every stored reference."""
    assert copies % 2 == 1
    independent_tail = sum(
        math.comb(copies, k) * independent_error**k
        * (1 - independent_error)**(copies - k)
        for k in range(copies // 2 + 1, copies + 1)
    )
    return common_mode_error + (1 - common_mode_error) * independent_tail


def log10_whole_object_yield(n, p_error):
    """Independent-site illustration; correlation is not implicitly excluded."""
    return n * math.log1p(-p_error) / math.log(10)


def finite_species_error(species, discrimination_kT):
    """Occupied equilibrium site: one correct, S-1 equal wrong competitors."""
    odds = (species - 1) * math.exp(-discrimination_kT)
    return odds / (1 + odds)


def repair_stationary(species, total_arrival=10.0, contamination=1e-5,
                      correct_off=1e-6, other_address_off=1e3,
                      payload_damage=1e-5, turnover=0.0,
                      payload_detector_off=None):
    """Exact stationary distribution of a four-state continuous-time chain.

    States: U vacancy; C correct; H hidden wrong payload/right address;
    A wrong address. All species arrive at finite total rate. A correct-address
    arrival has contamination probability q. Chemical damage C->H preserves
    recognition. Blind fuel-driven turnover ejects all occupied states equally.

    A payload-specific detector is *not* assumed. Setting payload_detector_off
    adds one explicitly as a positive control and creates an engineering debt:
    its stated selectivity must be implemented and measured, not stipulated.
    """
    a_c = total_arrival * (1 - contamination) / species
    a_h = total_arrival * contamination / species
    a_a = total_arrival * (species - 1) / species
    c_exit = correct_off + turnover + payload_damage
    h_exit = (correct_off if payload_detector_off is None
              else payload_detector_off) + turnover
    a_exit = other_address_off + turnover
    c_weight = a_c / c_exit
    h_weight = (a_h + payload_damage * c_weight) / h_exit
    a_weight = a_a / a_exit
    norm = 1 + c_weight + h_weight + a_weight
    p_u, p_c, p_h, p_a = [w / norm for w in (1, c_weight, h_weight, a_weight)]
    # Check stationary incoming and outgoing probability fluxes independently.
    assert abs(a_c * p_u - c_exit * p_c) < 1e-12
    assert abs(a_h * p_u + payload_damage * p_c - h_exit * p_h) < 1e-12
    assert abs(a_a * p_u - a_exit * p_a) < 1e-12
    return {
        "turnover_s-1": turnover,
        "correct": p_c,
        "vacant": p_u,
        "hidden_wrong_payload": p_h,
        "wrong_address": p_a,
        "all_site_error": 1 - p_c,
        "fuel_events_per_site_second": turnover * (1 - p_u),
    }


def main():
    p_ind = 0.01
    outputs = {
        "model_status": "Illustrative exact stochastic models; no fitted physical parameters.",
        "indistinguishability": {
            "claim": "For M target fillings with identical surviving accessible state, mean exact-repair probability is at most 1/M.",
            "reason": "All targets induce the same output law; mutually exclusive correct fillings have total probability <=1.",
            "binary_hidden_payload": 0.5,
            "erased_16_bit_unreferenced_patch": 2**-16,
        },
        "template_redundancy": [],
        "finite_species": [],
        "blind_payload_repair": [],
        "transport": [],
    }
    for common in (0.0, 1e-6):
        for copies in (1, 3, 5, 9, 17):
            p = majority_error(copies, p_ind, common)
            outputs["template_redundancy"].append({
                "copies": copies, "independent_error": p_ind,
                "common_mode_error": common, "decoded_error": p,
                "log10_yield_N_1e6": log10_whole_object_yield(10**6, p),
            })
    for species in (4, 100, 30000):
        for delta in (10, 20, 40):
            p = finite_species_error(species, delta)
            outputs["finite_species"].append({
                "species": species, "discrimination_kT": delta,
                "occupied_error": p,
                "log10_yield_N_1e6": log10_whole_object_yield(10**6, p),
                "mean_correct_encounter_s_at_kon_1e6_Ctotal_10uM": species / 10,
            })
    for u in (0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
        outputs["blind_payload_repair"].append(repair_stationary(100, turnover=u))
    outputs["positive_control_unimplemented_payload_detector"] = repair_stationary(
        100, payload_detector_off=1e3)
    for depth_m in (1e-6, 1e-4, 1e-3, 1e-2):
        outputs["transport"].append({
            "depth_m": depth_m,
            "one_dimensional_diffusion_timescale_s_D_1e-10": depth_m**2 / (2e-10),
        })
    print(json.dumps(outputs, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
