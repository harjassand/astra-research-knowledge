#!/usr/bin/env python3
"""Finite model calculations; no material or laboratory validation."""
import json
import math
from fractions import Fraction as F
from pathlib import Path


def dose(x, t, length=F(1), speed=F(1), concentration=F(1)):
    return concentration * (max(F(0), t-x/speed)
                            + max(F(0), t-(2*length-x)/speed))


def main():
    positions = [F(i, 100) for i in range(101)]
    for t in [F(2), F(5, 2), F(3), F(4)]:
        assert all(dose(x, t) == 2*(t-1) for x in positions)
    threshold = F(3)
    ideal_erase_time = F(5, 2)
    assert all(dose(x, ideal_erase_time) == threshold for x in positions)
    # A small faster proximal reaction exhausts before the unperturbed sites.
    proximal_rate = F(101, 100)
    proximal_erase_time = 1 + threshold/(2*proximal_rate)
    assert proximal_erase_time < ideal_erase_time
    residual_dose = threshold-dose(F(1), proximal_erase_time)
    assert residual_dose > 0
    result = {
        "status": "FINITE_MODEL_CHECK_ONLY",
        "scope": "equal-speed nondepleting plug flow and ideal dose-threshold erosion",
        "rational_positions_checked": len(positions),
        "uniform_threshold": str(threshold),
        "ideal_simultaneous_erasure_time": str(ideal_erase_time),
        "one_percent_faster_proximal_erasure_time": str(proximal_erase_time),
        "distal_remaining_dose_at_proximal_breakthrough": str(residual_dose),
        "leakage_model_from_blind_channel_adversary": [
            {"kappa_L": z, "distal_flow_ratio": z/math.sinh(z)}
            for z in [0.1, 1, 2, 5, 10]
        ],
        "secondary_mass_export_countermodel": {
            "after_instantaneous_erasure": "nonzero dissolved wall mass in final blind branch",
            "steady_graph_volume_flow": 0,
            "consequence": "the advective graph model alone leaves that mass in place indefinitely",
            "scope": "diffusion, countercirculation, pulses, and chemistry can remove it; no physical removal impossibility follows"
        },
        "laboratory_outcome": None,
    }
    output = Path(__file__).with_name("ERASURE_DESIGN_RESULTS.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
