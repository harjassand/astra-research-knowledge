#!/usr/bin/env python3
"""Finite full-source RK4 stress sweep for an ideal cell-specific F trigger.

This uses one independent G command per simulated cell, so it is not a shared
culture actuator result. The +/-10% genotype corners are stress values, not
measured confidence intervals. No validated numerical error bounds are used.
"""

from dataclasses import replace
from itertools import product
import json
from pathlib import Path

from full_growth_diagnostics import Params, integrate


def f_trigger(threshold=5.0, restart=0.1):
    return lambda t, y, p: 0.0 if y[0] > threshold else restart


def main():
    base = Params()
    records = []
    for signs in product((-1, 1), repeat=4):
        p = replace(base,
                    vu=base.vu * (1 + 0.1 * signs[0]),
                    vl=base.vl * (1 + 0.1 * signs[1]),
                    katp=base.katp * (1 + 0.1 * signs[2]),
                    kp=base.kp * (1 + 0.1 * signs[3]))
        for f0 in (5.0, 20.0, 100.0, 300.0):
            for h0 in (0.1, 1.0):
                final, dead = integrate((f0, 0.02, 0.02, h0), f_trigger(),
                                        horizon=300.0, dt=0.02, p=p)
                balanced = final[0] < 20 and final[1] > 0.5 and final[2] > 5
                records.append({
                    "genotype_signs_vu_vl_katp_kp": signs,
                    "initial_F_ATP_Pi_H": [f0, 0.02, 0.02, h0],
                    "dead_by_300min": dead is not None,
                    "balanced_endpoint_F_lt20_A_gt0p5_Pi_gt5": balanced,
                    "final": list(final),
                })
    data = {
        "model": "PLOS 2021 full health/dilution model; CellML fourth-power expression cost recomputed per genotype",
        "policy": "cell-specific G=0 while F>5 mM, then G=0.1 mM",
        "method": "classical RK4 dt=0.02 min; horizon 300 min; no validated error bounds",
        "stress_set": "all 16 +/-10% corners of IC Table 2 vu, vl, katp, kp; F0 in {5,20,100,300} mM; ATP=Pi=0.02 mM; H0 in {0.1,1}",
        "counts": {
            "runs": len(records),
            "deaths": sum(r["dead_by_300min"] for r in records),
            "balanced_endpoints": sum(r["balanced_endpoint_F_lt20_A_gt0p5_Pi_gt5"] for r in records),
        },
        "first_failures": [r for r in records if r["dead_by_300min"] or not r["balanced_endpoint_F_lt20_A_gt0p5_Pi_gt5"]][:8],
        "scope": "Finite numerical result for ideal independent per-cell control; not a theorem, validated numerics, naturally sampled states, or a realizable shared-glucose experiment.",
        "records": records,
    }
    path = Path(__file__).with_name("cell_trigger_corner_sweep.json")
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({k: v for k, v in data.items() if k not in ("records", "first_failures")}, indent=2))
    print("first_failures", json.dumps(data["first_failures"], indent=2))


if __name__ == "__main__":
    main()
