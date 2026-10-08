#!/usr/bin/env python3
"""Finite stress sweep for a shared culture glucose schedule.

Tests a common input (zero glucose for a fixed duration, then 0.1 mM) in the
full PLOS health/dilution model.  This is a finite RK4 diagnostic only.  The
genotype +/-10% corners and initial-state grid are declared design stresses,
not measured distributions or confidence intervals.
"""

from __future__ import annotations

from dataclasses import replace
import itertools
import json
from pathlib import Path

from full_growth_diagnostics import Params, integrate, timed_off_then_fixed


def main():
    base = Params()
    records = []
    for signs in itertools.product((-1, 1), repeat=4):
        p = replace(base,
                    vu=base.vu * (1 + 0.1 * signs[0]),
                    vl=base.vl * (1 + 0.1 * signs[1]),
                    katp=base.katp * (1 + 0.1 * signs[2]),
                    kp=base.kp * (1 + 0.1 * signs[3]))
        for f0 in (5.0, 20.0, 100.0, 300.0):
            for h0 in (0.1, 1.0):
                for off in (30.0, 35.0, 40.0):
                    final, dead = integrate(
                        (f0, 0.02, 0.02, h0),
                        timed_off_then_fixed(off, 0.1),
                        horizon=300.0, dt=0.02, p=p)
                    balanced = final[0] < 20.0 and final[1] > 0.5 and final[2] > 5.0
                    records.append({
                        "genotype_signs_vu_vl_katp_kp": signs,
                        "initial_F_ATP_Pi_H": [f0, 0.02, 0.02, h0],
                        "off_min": off,
                        "dead_by_300min": dead is not None,
                        "balanced_endpoint_F_lt20_A_gt0p5_Pi_gt5": balanced,
                        "final": list(final),
                    })
    grouped = {}
    for off in (30.0, 35.0, 40.0):
        rs = [r for r in records if r["off_min"] == off]
        grouped[str(int(off))] = {
            "runs": len(rs),
            "deaths": sum(r["dead_by_300min"] for r in rs),
            "balanced_endpoints": sum(r["balanced_endpoint_F_lt20_A_gt0p5_Pi_gt5"] for r in rs),
            "first_failures": [r for r in rs if r["dead_by_300min"] or not r["balanced_endpoint_F_lt20_A_gt0p5_Pi_gt5"]][:4],
        }
    out = {
        "model": "PLOS 2021 full health-and-dilution system; IC genotype Table 2",
        "method": "classical RK4, dt=0.02 min, final time=300 min; no validated error bounds",
        "input": "common external glucose G=0 for off_min, then fixed G=0.1 mM",
        "stress_set": {
            "initial_F_mM": [5.0, 20.0, 100.0, 300.0],
            "initial_ATP_Pi_mM": [0.02, 0.02],
            "initial_health": [0.1, 1.0],
            "genotype_parameters": "all 16 corners of +/-10% around (vup,vlo,katp,kp) IC Table 2 values",
            "other_parameters": "Table 1 point values",
        },
        "endpoint_rule": "Alive by 300 min, FBP<20 mM, ATP>0.5 mM, Pi>5 mM",
        "grouped": grouped,
        "records": records,
        "evidence_scope": "Finite numerical model sweep; not a theorem, wet-lab validation, or natural distribution estimate.",
    }
    path = Path(__file__).with_name("population_schedule_sweep.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(grouped, indent=2))
    print("wrote", path)


if __name__ == "__main__":
    main()
