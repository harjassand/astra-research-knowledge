#!/usr/bin/env python3
"""Reduced two-channel BET/selectivity check; all assumptions are explicit.

This is not a fit or a reconstruction of the full Nature-SI model. It tests the
steady-state two-channel hazard identity against a mechanism-ablation control.
"""
from __future__ import annotations

import json
from pathlib import Path


def channel(k_set: float, substrate_m: float, k_trap: float,
            k_bet_m_inv_s: float, acceptor_m: float) -> dict[str, float]:
    capture = k_set * substrate_m  # pseudo-first-order electron capture
    bet = k_bet_m_inv_s * acceptor_m
    commitment = k_trap / (k_trap + bet)
    return {"capture_s_inv": capture, "bet_s_inv": bet,
            "commitment_probability": commitment,
            "product_flux_per_electron_pool_s_inv": capture * commitment}


def calculate(target_trap: float, easy_trap: float, bet: float,
              capture_target: float, capture_easy: float) -> dict[str, float]:
    """Given captured-electron fluxes, calculate product fraction and yield."""
    total_capture = capture_target + capture_easy
    w_t, w_e = capture_target / total_capture, capture_easy / total_capture
    p_t = target_trap / (target_trap + bet)
    p_e = easy_trap / (easy_trap + bet)
    product_t, product_e = w_t * p_t, w_e * p_e
    product_total = product_t + product_e
    ratio = product_t / product_e
    return {
        "target_capture_share": w_t,
        "target_commitment_probability": p_t,
        "easy_channel_commitment_probability": p_e,
        "target_product_share": product_t / product_total,
        "target_to_easy_product_ratio": ratio,
        "total_product_per_captured_electron": product_total,
        "captured_electrons_per_target_product": 1.0 / product_t,
    }


def main() -> None:
    # Separate source inputs: solvated-electron capture k values at equal
    # substrate concentrations; illustrative Fig. 5c BET and easy-channel
    # trap settings. Combining them is a scenario, not a fit to experiment.
    k_set_target = 4.0e9       # M^-1 s^-1, cyclopropyl ketone (SI S30/S80)
    k_set_easy = 3.0e10        # M^-1 s^-1, styrene (SI S25/S80)
    substrate_m = 0.080        # M, source's catalytically relevant concentration
    k_bet = 1.0e10             # M^-1 s^-1, diffusion-limit model setting
    acceptor_m = 5.6e-5        # M, source SI Fig. 5c illustration
    easy_trap = 1.0e3          # s^-1, source SI Fig. 5c illustration
    bet = k_bet * acceptor_m
    cap_t = k_set_target * substrate_m
    cap_e = k_set_easy * substrate_m

    rows = []
    for trap_ratio in (1, 10, 100, 1_000, 1_000_000):
        result = calculate(trap_ratio * easy_trap, easy_trap, bet, cap_t, cap_e)
        rows.append({"target_to_easy_trap_ratio": trap_ratio, **result})

    # Mechanism ablation: no BET returns both radical-anion channels to product,
    # so selectivity is just the unequal initial capture share.
    no_bet = calculate(1_000 * easy_trap, easy_trap, 0.0, cap_t, cap_e)

    capture_ratio = k_set_target / k_set_easy
    target_share_90 = 0.90
    target_odds_90 = target_share_90 / (1.0 - target_share_90)
    # In the target-trap >> BET limit: R ~= (kSET,t/kSET,e)*(x+k2)/k2.
    bet_needed_90_infinite_trap = max(
        0.0, (target_odds_90 / capture_ratio - 1.0) * easy_trap)
    bet_needed_99_infinite_trap = max(
        0.0, (99.0 / capture_ratio - 1.0) * easy_trap)

    # Exact finite-trap BET needed for desired odds R, provided g*r > R.
    def exact_bet_needed(target_odds: float, ratio: float) -> float | None:
        g = capture_ratio
        if g * ratio <= target_odds:
            return None
        return ratio * easy_trap * (target_odds - g) / (g * ratio - target_odds)

    output = {
        "status": "finite illustrative calculation; not experimental fit",
        "inputs": {
            "kSET_target_ketone_M_inv_s": k_set_target,
            "kSET_easy_styrene_M_inv_s": k_set_easy,
            "equal_substrate_concentration_M": substrate_m,
            "kBET_common_M_inv_s": k_bet,
            "acceptor_A_M": acceptor_m,
            "effective_easy_trap_s_inv": easy_trap,
            "effective_target_trap_s_inv_is_sweep": True,
            "source_bases": ["SI S25/S30/S80 measured capture constants",
                             "SI Fig. 5c illustrative BET acceptor and k2"]
        },
        "derived": {
            "pseudo_first_order_capture_target_s_inv": cap_t,
            "pseudo_first_order_capture_easy_s_inv": cap_e,
            "target_capture_share": cap_t / (cap_t + cap_e),
            "common_BET_hazard_s_inv": bet,
            "BET_to_easy_trap_ratio": bet / easy_trap,
        },
        "no_BET_mechanism_ablation": no_bet,
        "sweep": rows,
        "selectivity_threshold_design": {
            "for_90pct_product_selectivity": {
                "odds_required": target_odds_90,
                "BET_hazard_min_if_target_trap_infinite_s_inv":
                    bet_needed_90_infinite_trap,
                "BET_hazard_min_if_target_to_easy_trap_ratio_1000_s_inv":
                    exact_bet_needed(target_odds_90, 1_000),
            },
            "for_99pct_product_selectivity": {
                "odds_required": 99.0,
                "BET_hazard_min_if_target_trap_infinite_s_inv":
                    bet_needed_99_infinite_trap,
                "BET_hazard_min_if_target_to_easy_trap_ratio_1000_s_inv":
                    exact_bet_needed(99.0, 1_000),
            }
        },
        "interpretation_limit": (
            "Electron attempts are normalized to the toy capture pool; this is not "
            "experimental Faradaic efficiency, photon efficiency, or energy per mole. "
            "The target trap is an effective commitment hazard, not an identified "
            "single elementary step."
        )
    }
    out = Path(__file__).with_name("MODEL_OUTPUT.json")
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
